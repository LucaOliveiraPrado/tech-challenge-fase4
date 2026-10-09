"""Taxonomia de aspectos da experiência do cliente e quadro de frequências.

Por que existe: a recuperação devolve as K avaliações MAIS RELEVANTES, não uma
contagem. Perguntas como "quais reclamações aparecem com maior frequência?"
exigem contar sobre a base inteira. Cada documento recebe rótulos de aspecto
(multirrótulo) por um classificador treinado sobre os embeddings (ver
themes/classifier.py), e o quadro de frequências entra no contexto do LLM como
dado agregado, enquanto as evidências [R#] continuam sustentando o conteúdo.
"""
from __future__ import annotations

import pandas as pd

from voc_rag.config import PROCESSED_DIR
from voc_rag.retrieval.filters import Filtros

ASPECTOS_PARQUET = PROCESSED_DIR / "aspectos.parquet"

# aspecto -> (polaridade, descrição usada no prompt de rotulagem e na tela)
ASPECTOS: dict[str, tuple[str, str]] = {
    "atraso_entrega": ("negativa", "entrega atrasada, demorou, prazo não cumprido"),
    "nao_recebido": ("negativa", "produto não chegou / ainda não recebido"),
    "pedido_incompleto": ("negativa", "faltou item, veio só parte do pedido, quantidade errada"),
    "produto_errado": ("negativa", "produto diferente do anunciado ou comprado (modelo, cor)"),
    "defeito_avaria": ("negativa", "produto com defeito, quebrado, danificado, não funciona"),
    "qualidade_baixa": ("negativa", "qualidade ruim ou inferior ao esperado, material fraco"),
    "atendimento_ruim": ("negativa", "atendimento ruim da loja ou vendedor, sem resposta"),
    "troca_reembolso": ("negativa", "dificuldade com troca, devolução, cancelamento ou reembolso"),
    "embalagem_ruim": ("negativa", "embalagem inadequada, violada ou mal feita"),
    "entrega_elogio": ("positiva", "entrega rápida, antes do prazo ou no prazo"),
    "produto_elogio": ("positiva", "produto bom, boa qualidade, conforme anunciado"),
    "atendimento_elogio": ("positiva", "bom atendimento, vendedor atencioso"),
    "preco_elogio": ("positiva", "bom preço, custo-benefício"),
    "recomendacao": ("positiva", "satisfação geral, recomenda a loja ou o produto"),
}

ROTULO = {
    "atraso_entrega": "Atraso na entrega",
    "nao_recebido": "Produto não recebido",
    "pedido_incompleto": "Pedido incompleto",
    "produto_errado": "Produto diferente do anunciado",
    "defeito_avaria": "Defeito ou avaria",
    "qualidade_baixa": "Qualidade abaixo do esperado",
    "atendimento_ruim": "Atendimento ruim",
    "troca_reembolso": "Troca, devolução ou reembolso",
    "embalagem_ruim": "Embalagem ruim",
    "entrega_elogio": "Entrega rápida / no prazo",
    "produto_elogio": "Produto bom / conforme anunciado",
    "atendimento_elogio": "Bom atendimento",
    "preco_elogio": "Bom preço / custo-benefício",
    "recomendacao": "Satisfação geral / recomenda",
}


def aspectos_da_polaridade(polaridade: str) -> list[str]:
    if polaridade == "qualquer":
        return list(ASPECTOS)
    return [a for a, (p, _) in ASPECTOS.items() if p == polaridade]


def load_aspectos() -> pd.DataFrame | None:
    if not ASPECTOS_PARQUET.exists():
        return None
    return pd.read_parquet(ASPECTOS_PARQUET)


def quadro_frequencias(
    docs: pd.DataFrame, filtros: Filtros, polaridade: str
) -> tuple[pd.DataFrame | None, str | None]:
    """Frequência de cada aspecto no recorte (base completa, não a amostra)."""
    asp = load_aspectos()
    if asp is None:
        return None, None
    recorte = docs.loc[filtros.mask(docs), ["review_id"]]
    base = recorte.merge(asp, on="review_id", how="left")
    n = len(base)
    if n == 0:
        return None, None
    linhas = []
    for a in aspectos_da_polaridade(polaridade):
        if a not in base.columns:
            continue
        k = int(base[a].fillna(False).astype(bool).sum())
        linhas.append({"aspecto": a, "rotulo": ROTULO[a], "avaliacoes": k, "pct": 100 * k / n})
    df = pd.DataFrame(linhas).sort_values("avaliacoes", ascending=False).reset_index(drop=True)
    df = df[df["avaliacoes"] > 0]
    texto = "\n".join(
        f"- {r.rotulo}: {r.avaliacoes} avaliações ({r.pct:.1f}% das {n} do recorte)"
        for r in df.itertuples()
    )
    texto += (
        "\n(Estimativa por classificador de aspectos; uma avaliação pode ter mais de um aspecto.)"
    )
    return df, texto
