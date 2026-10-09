"""Construção da base de conhecimento a partir dos CSVs da Olist.

Etapas (cada uma justificada em reports/decisoes_tecnicas.md):
  1. Seleção: a tabela de avaliações é o centro; pedidos, itens, produtos,
     clientes e pagamentos entram só como METADADOS da avaliação.
  2. Deduplicação: um mesmo review_id aparece ligado a mais de um pedido na
     fonte; mantemos uma linha por review_id.
  3. Limpeza do texto: título + mensagem limpos e fundidos num documento.
  4. Ausentes: avaliação sem texto útil fica na base de avaliações (conta para
     as estatísticas de nota) mas NÃO vira documento (não há o que recuperar).
  5. Metadados: nota, sentimento, período, situação da entrega, categoria,
     UF e pagamento, prontos para filtros na recuperação.

Saídas:
  data/processed/reviews.parquet    todas as avaliações (uma por review_id)
  data/processed/documents.parquet  documentos da base de conhecimento
  reports/base_conhecimento.json    contagens de cada etapa (rastro)
"""
from __future__ import annotations

import json
import logging
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from voc_rag.config import DOCUMENTS_PARQUET, PROCESSED_DIR, RAW_DIR, REPORTS_DIR, REVIEWS_PARQUET
from voc_rag.data.text import (
    clean_text,
    compose_document,
    count_words,
    is_missing,
    normalize_key,
)

log = logging.getLogger(__name__)

ARQUIVOS = {
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "translation": "product_category_name_translation.csv",
    "customers": "olist_customers_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
}

REGIAO_POR_UF = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte", "RO": "Norte",
    "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste",
    "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}

SEM_CATEGORIA = "sem_categoria"


# --------------------------------------------------------------------------
# Leitura
# --------------------------------------------------------------------------
def extract_zip(zip_path: Path, raw_dir: Path = RAW_DIR) -> list[str]:
    """Extrai do zip do Kaggle apenas os CSVs usados pelo projeto."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    extraidos = []
    with zipfile.ZipFile(zip_path) as zf:
        nomes = {Path(n).name: n for n in zf.namelist()}
        for arquivo in ARQUIVOS.values():
            if arquivo not in nomes:
                raise FileNotFoundError(f"{arquivo} não encontrado em {zip_path}")
            (raw_dir / arquivo).write_bytes(zf.read(nomes[arquivo]))
            extraidos.append(arquivo)
    return extraidos


KAGGLE_DATASET = "olistbr/brazilian-ecommerce"


def baixar_kaggle(raw_dir: Path = RAW_DIR) -> list[str]:
    """Baixa o dataset oficial pela API pública do Kaggle (sem login) e copia os CSVs."""
    import shutil

    import kagglehub

    origem = Path(kagglehub.dataset_download(KAGGLE_DATASET))
    raw_dir.mkdir(parents=True, exist_ok=True)
    for arquivo in ARQUIVOS.values():
        shutil.copy2(origem / arquivo, raw_dir / arquivo)
    log.info("dataset %s copiado de %s", KAGGLE_DATASET, origem)
    return list(ARQUIVOS.values())


def load_raw(raw_dir: Path = RAW_DIR) -> dict[str, pd.DataFrame]:
    faltando = [a for a in ARQUIVOS.values() if not (raw_dir / a).exists()]
    if faltando:
        raise FileNotFoundError(
            f"CSVs ausentes em {raw_dir}: {faltando}. Rode `voc prepare` (baixa do Kaggle)."
        )
    return {
        chave: pd.read_csv(raw_dir / arquivo, encoding="utf-8-sig")
        for chave, arquivo in ARQUIVOS.items()
    }


# --------------------------------------------------------------------------
# Metadados por pedido
# --------------------------------------------------------------------------
def _datas(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    df = df.copy()
    for c in colunas:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def order_features(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Uma linha por order_id com entrega, categoria, cliente e pagamento."""
    orders = _datas(
        raw["orders"],
        [
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    # Entrega: atraso em dias contra a data estimada informada ao cliente.
    entregue = orders["order_delivered_customer_date"].notna() & (
        orders["order_status"] == "delivered"
    )
    atraso = (
        orders["order_delivered_customer_date"].dt.normalize()
        - orders["order_estimated_delivery_date"].dt.normalize()
    ).dt.days
    tempo = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    status = np.select(
        [
            entregue & (atraso > 0),
            entregue,
            orders["order_status"].isin(["canceled", "unavailable"]),
        ],
        ["atrasado", "no_prazo", "cancelado"],
        default="nao_entregue",
    )
    feats = pd.DataFrame(
        {
            "order_id": orders["order_id"],
            "order_status": orders["order_status"],
            "data_compra": orders["order_purchase_timestamp"],
            "entrega_status": status,
            "atraso_dias": atraso.where(entregue),
            "tempo_entrega_dias": tempo.where(entregue).round(1),
            "customer_id": orders["customer_id"],
        }
    )

    # Categoria: a do item de maior preço é a "principal"; todas ficam listadas.
    products = raw["products"][["product_id", "product_category_name"]]
    trad = raw["translation"].rename(
        columns={"product_category_name_english": "categoria_en"}
    )
    items = raw["items"].merge(products, on="product_id", how="left")
    items["product_category_name"] = items["product_category_name"].fillna(SEM_CATEGORIA)
    items = items.sort_values(["order_id", "price"], ascending=[True, False])
    principal = items.drop_duplicates("order_id")[["order_id", "product_category_name"]]
    agg = items.groupby("order_id").agg(
        n_itens=("order_item_id", "count"),
        n_vendedores=("seller_id", "nunique"),
        valor_itens=("price", "sum"),
        valor_frete=("freight_value", "sum"),
        categorias=("product_category_name", lambda s: "|".join(sorted(set(s)))),
    )
    cat = principal.rename(columns={"product_category_name": "categoria"}).merge(
        agg, on="order_id"
    )
    cat = cat.merge(
        trad, left_on="categoria", right_on="product_category_name", how="left"
    ).drop(columns="product_category_name")
    cat["categoria_en"] = cat["categoria_en"].fillna(cat["categoria"])
    feats = feats.merge(cat, on="order_id", how="left")

    # Cliente.
    cust = raw["customers"][["customer_id", "customer_state", "customer_city"]]
    feats = feats.merge(cust, on="customer_id", how="left").drop(columns="customer_id")
    feats = feats.rename(columns={"customer_state": "uf", "customer_city": "cidade"})
    feats["regiao"] = feats["uf"].map(REGIAO_POR_UF)

    # Pagamento principal (maior valor) e parcelas.
    pay = raw["payments"].sort_values(
        ["order_id", "payment_value"], ascending=[True, False]
    )
    pay_main = pay.drop_duplicates("order_id")[
        ["order_id", "payment_type", "payment_installments"]
    ].rename(columns={"payment_type": "pagamento", "payment_installments": "parcelas"})
    feats = feats.merge(pay_main, on="order_id", how="left")
    return feats


# --------------------------------------------------------------------------
# Avaliações e documentos
# --------------------------------------------------------------------------
def sentimento_por_nota(nota: pd.Series) -> pd.Series:
    return pd.Series(
        np.select([nota <= 2, nota == 3], ["negativo", "neutro"], default="positivo"),
        index=nota.index,
    )


def build_reviews(raw: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    rev = raw["reviews"].copy()
    rastro: dict = {"linhas_fonte": int(len(rev))}

    # Um mesmo review_id ligado a vários pedidos: mesma opinião, conta uma vez.
    n_ped = rev.groupby("review_id")["order_id"].transform("nunique")
    rastro["review_ids_em_multiplos_pedidos"] = int(
        rev.loc[n_ped > 1, "review_id"].nunique()
    )
    rev = rev.sort_values(["review_id", "order_id"]).drop_duplicates("review_id")
    rev["n_pedidos_review"] = n_ped.loc[rev.index].astype(int)
    rastro["avaliacoes_unicas"] = int(len(rev))

    rev["titulo"] = rev["review_comment_title"].map(clean_text)
    rev["mensagem"] = rev["review_comment_message"].map(clean_text)
    rastro["mensagem_ausente_na_fonte"] = int(rev["review_comment_message"].isna().sum())
    rastro["titulo_ausente_na_fonte"] = int(rev["review_comment_title"].isna().sum())
    rastro["mensagem_sem_conteudo_apos_limpeza"] = int(
        (rev["review_comment_message"].notna() & rev["mensagem"].isna()).sum()
    )
    rev["texto"] = [
        compose_document(t, m) for t, m in zip(rev["titulo"], rev["mensagem"], strict=True)
    ]
    rev["tem_texto"] = rev["texto"].notna()

    rev["data_avaliacao"] = pd.to_datetime(rev["review_creation_date"], errors="coerce")
    rev = rev.rename(columns={"review_score": "nota"})
    rev["nota"] = rev["nota"].astype(int)
    rev["sentimento"] = sentimento_por_nota(rev["nota"])

    feats = order_features(raw)
    rev = rev.merge(feats, on="order_id", how="left")
    rastro["avaliacoes_sem_pedido"] = int(rev["order_status"].isna().sum())
    rastro["avaliacoes_sem_categoria"] = int(
        (rev["categoria"].isna() | (rev["categoria"] == SEM_CATEGORIA)).sum()
    )
    rev["categoria"] = rev["categoria"].fillna(SEM_CATEGORIA)
    rev["categoria_en"] = rev["categoria_en"].fillna(SEM_CATEGORIA)
    rev["categorias"] = rev["categorias"].fillna(SEM_CATEGORIA)

    # Período: compra quando existir, senão a data da avaliação.
    ref = rev["data_compra"].fillna(rev["data_avaliacao"])
    rev["ano"] = ref.dt.year.astype("Int64")
    rev["mes"] = ref.dt.month.astype("Int64")
    rev["ano_mes"] = (ref.dt.year * 100 + ref.dt.month).astype("Int64")

    rev["n_palavras"] = rev["texto"].map(count_words)
    rev["texto_chave"] = rev["texto"].map(lambda s: None if is_missing(s) else normalize_key(s))

    colunas = [
        "review_id", "order_id", "nota", "sentimento", "titulo", "mensagem", "texto",
        "tem_texto", "n_palavras", "texto_chave", "data_avaliacao", "data_compra", "ano",
        "mes", "ano_mes", "order_status", "entrega_status", "atraso_dias",
        "tempo_entrega_dias", "categoria", "categoria_en", "categorias", "n_itens",
        "n_vendedores", "valor_itens", "valor_frete", "uf", "cidade", "regiao",
        "pagamento", "parcelas", "n_pedidos_review",
    ]
    rev = rev[colunas].reset_index(drop=True)
    rastro["avaliacoes_com_texto"] = int(rev["tem_texto"].sum())
    return rev, rastro


def build_documents(reviews: pd.DataFrame) -> pd.DataFrame:
    """Documentos da base de conhecimento: uma avaliação com texto = um documento.

    Sem chunking: os comentários são curtos (poucas dezenas de palavras) e uma
    avaliação é a menor unidade de evidência que faz sentido citar.
    """
    docs = reviews[reviews["tem_texto"]].copy()
    # Texto só com letras fora do alfabeto latino gera chave vazia: usa o id.
    vazia = docs["texto_chave"].fillna("").str.len() == 0
    docs.loc[vazia, "texto_chave"] = docs.loc[vazia, "review_id"]
    # Duplicatas de texto entre clientes diferentes são vozes distintas e ficam
    # no índice (contam como frequência); a deduplicação acontece na montagem
    # do contexto, para o LLM não receber a mesma frase repetida.
    docs["texto_repetido"] = docs.duplicated("texto_chave", keep=False)
    docs = docs.drop(columns=["tem_texto"]).reset_index(drop=True)
    return docs


def run(zip_path: Path | None = None) -> dict:
    if zip_path is not None:
        extract_zip(zip_path)
    elif not all((RAW_DIR / a).exists() for a in ARQUIVOS.values()):
        baixar_kaggle()
    raw = load_raw()
    reviews, rastro = build_reviews(raw)
    docs = build_documents(reviews)
    rastro["documentos"] = int(len(docs))
    rastro["documentos_texto_repetido"] = int(docs["texto_repetido"].sum())
    rastro["palavras_por_documento"] = {
        "mediana": float(docs["n_palavras"].median()),
        "p90": float(docs["n_palavras"].quantile(0.9)),
        "max": int(docs["n_palavras"].max()),
    }
    rastro["documentos_por_sentimento"] = {
        k: int(v) for k, v in docs["sentimento"].value_counts().items()
    }

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    reviews.to_parquet(REVIEWS_PARQUET, index=False)
    docs.to_parquet(DOCUMENTS_PARQUET, index=False)
    (REPORTS_DIR / "base_conhecimento.json").write_text(
        json.dumps(rastro, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log.info("base pronta: %s avaliações, %s documentos", len(reviews), len(docs))
    return rastro


def load_documents() -> pd.DataFrame:
    if not DOCUMENTS_PARQUET.exists():
        raise FileNotFoundError("Base não construída. Rode `voc prepare` antes.")
    return pd.read_parquet(DOCUMENTS_PARQUET)


def load_reviews() -> pd.DataFrame:
    if not REVIEWS_PARQUET.exists():
        raise FileNotFoundError("Base não construída. Rode `voc prepare` antes.")
    return pd.read_parquet(REVIEWS_PARQUET)
