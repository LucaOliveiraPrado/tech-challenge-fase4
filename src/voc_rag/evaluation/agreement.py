"""Concordância entre juízes.

No plano gratuito, a maior parte dos julgamentos de relevância caiu para o juiz de reserva
(`gemini-3.1-flash-lite`) quando os modelos "flash" esgotaram ou sobrecarregaram. Para saber se
isso compromete as métricas, uma amostra de perguntas é rejulgada por um modelo "flash" e
comparada com o julgamento registrado: concordância exata, kappa de Cohen ponderado (escala
ordinal 0/1/2) e concordância na decisão binária "evidência clara" (2 x resto), que é a usada
na P@10.

A mesma comparação vale para um anotador humano: `gera_amostra_humana` sorteia pares
estratificados pela nota do juiz (sem mostrá-la) em `eval/anotacao_humana.csv`; depois de
preenchida a coluna `relevancia_humana`, `run_humano` mede a concordância humano x juiz.
"""
from __future__ import annotations

import json
import logging

import pandas as pd
from sklearn.metrics import cohen_kappa_score

from voc_rag.config import EVAL_DIR, REPORTS_DIR, SEED
from voc_rag.evaluation.judge import _linha, carrega_julgamentos, julga_relevancia
from voc_rag.evaluation.retrieval_eval import carrega_perguntas
from voc_rag.generation.llm import LLMClient
from voc_rag.retrieval.retriever import get_kb

log = logging.getLogger(__name__)

AMOSTRA = ["Q04", "Q10", "Q13", "Q20", "Q22", "Q28"]
ANOTACAO_CSV = EVAL_DIR / "anotacao_humana.csv"


def _metricas(a: pd.Series, b: pd.Series) -> dict:
    return {
        "pares": int(len(a)),
        "concordancia_exata": round(float((a == b).mean()), 4),
        "kappa_ponderado": round(float(cohen_kappa_score(a, b, weights="linear")), 4),
        "concordancia_binaria_relevante": round(float(((a == 2) == (b == 2)).mean()), 4),
        "kappa_binario_relevante": round(float(cohen_kappa_score(a == 2, b == 2)), 4),
        "matriz": pd.crosstab(a, b).to_dict(),
    }


def run(modelo: str = "gemini-3.8-flash", qids: list[str] | None = None) -> dict:
    qids = qids or AMOSTRA
    perg = {p["id"]: p for p in carrega_perguntas()}
    julg = carrega_julgamentos()
    docs = get_kb().docs
    llm = LLMClient(model=modelo, fallbacks=[])
    linhas = []
    for qid in qids:
        p = perg[qid]
        reg = julg[julg["qid"] == qid]
        reg = reg[reg["juiz"] != modelo]
        if reg.empty:
            continue
        ids = sorted(reg["review_id"])
        g = julga_relevancia(p["pergunta"], p["criterio"], docs.loc[ids], llm,
                             metadados=bool(p.get("filtros_esperados")))
        for r in reg.itertuples():
            if r.review_id in g:
                linhas.append({"qid": qid, "juiz_original": r.juiz, "original": int(r.relevancia),
                               "segundo": int(g[r.review_id])})
        log.info("%s rejulgada por %s", qid, modelo)
    df = pd.DataFrame(linhas)
    res = {
        "segundo_juiz": modelo,
        "juizes_originais": df["juiz_original"].value_counts().to_dict(),
        "perguntas": sorted(df["qid"].unique().tolist()),
        **_metricas(df["original"], df["segundo"]),
    }
    (REPORTS_DIR / "concordancia_juizes.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return res


def gera_amostra_humana(por_nota: int = 20, sobrescrever: bool = False) -> int:
    """Sorteia `por_nota` pares de cada nota do juiz (0, 1, 2), espalhados pelas perguntas.
    A nota do juiz não vai para o arquivo, para não ancorar o anotador."""
    if ANOTACAO_CSV.exists() and not sobrescrever:
        raise FileExistsError(f"{ANOTACAO_CSV} já existe (use --sobrescrever)")
    # Só perguntas respondíveis (com critério): são elas que entram na P@10.
    perg = {p["id"]: p for p in carrega_perguntas() if "criterio" in p}
    docs = get_kb().docs
    julg = carrega_julgamentos()
    julg = julg[julg["qid"].isin(perg) & julg["review_id"].isin(docs.index)]
    julg = julg.sample(frac=1, random_state=SEED)
    # Uma avaliação por pergunta em cada nota antes de repetir pergunta.
    amostra = julg.groupby(["relevancia", "qid"]).head(1).groupby("relevancia").head(por_nota)
    resto = julg.drop(amostra.index)
    extra = [resto[resto["relevancia"] == n].head(por_nota - k)
             for n, k in amostra.groupby("relevancia").size().items() if k < por_nota]
    amostra = pd.concat([amostra, *extra]).sample(frac=1, random_state=SEED)
    linhas = []
    for i, r in enumerate(amostra.itertuples(), 1):
        p = perg[r.qid]
        doc = docs.loc[r.review_id]
        linhas.append({
            "id": f"H{i:02d}", "qid": r.qid, "review_id": r.review_id,
            "pergunta": p["pergunta"], "criterio": p["criterio"],
            "avaliacao": _linha(0, doc, bool(p.get("filtros_esperados"))).removeprefix("0. "),
            "relevancia_humana": "",
        })
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    # ";" e BOM para o Excel em português abrir direto, com acentos.
    pd.DataFrame(linhas).to_csv(ANOTACAO_CSV, sep=";", index=False, encoding="utf-8-sig")
    return len(linhas)


def run_humano() -> dict:
    """Concordância entre a anotação humana e o juiz registrado."""
    hum = pd.read_csv(ANOTACAO_CSV, sep=";", encoding="utf-8-sig")
    hum["relevancia_humana"] = pd.to_numeric(hum["relevancia_humana"], errors="coerce")
    hum = hum[hum["relevancia_humana"].isin([0, 1, 2])]
    if hum.empty:
        raise ValueError(f"preencha relevancia_humana (0, 1 ou 2) em {ANOTACAO_CSV}")
    df = hum.merge(carrega_julgamentos(), on=["qid", "review_id"])
    res = {
        "anotador": "humano",
        "juizes": df["juiz"].value_counts().to_dict(),
        "perguntas": int(df["qid"].nunique()),
        "amostragem": "estratificada pela nota do juiz (mesmo número de 0, 1 e 2)",
        **_metricas(df["relevancia"].astype(int), df["relevancia_humana"].astype(int)),
    }
    (REPORTS_DIR / "concordancia_humana.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return res
