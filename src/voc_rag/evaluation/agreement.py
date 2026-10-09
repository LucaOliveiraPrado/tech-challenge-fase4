"""Concordância entre juízes.

No plano gratuito, a maior parte dos julgamentos de relevância caiu para o juiz de reserva
(`gemini-3.1-flash-lite`) quando os modelos "flash" esgotaram ou sobrecarregaram. Para saber se
isso compromete as métricas, uma amostra de perguntas é rejulgada por um modelo "flash" e
comparada com o julgamento registrado: concordância exata, kappa de Cohen ponderado (escala
ordinal 0/1/2) e concordância na decisão binária "evidência clara" (2 x resto), que é a usada
na P@10.
"""
from __future__ import annotations

import json
import logging

import pandas as pd
from sklearn.metrics import cohen_kappa_score

from voc_rag.config import REPORTS_DIR
from voc_rag.evaluation.judge import carrega_julgamentos, julga_relevancia
from voc_rag.evaluation.retrieval_eval import carrega_perguntas
from voc_rag.generation.llm import LLMClient
from voc_rag.retrieval.retriever import get_kb

log = logging.getLogger(__name__)

AMOSTRA = ["Q04", "Q10", "Q13", "Q20", "Q22", "Q28"]


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
    a, b = df["original"], df["segundo"]
    res = {
        "segundo_juiz": modelo,
        "juizes_originais": df["juiz_original"].value_counts().to_dict(),
        "perguntas": sorted(df["qid"].unique().tolist()),
        "pares": int(len(df)),
        "concordancia_exata": round(float((a == b).mean()), 4),
        "kappa_ponderado": round(float(cohen_kappa_score(a, b, weights="linear")), 4),
        "concordancia_binaria_relevante": round(float(((a == 2) == (b == 2)).mean()), 4),
        "kappa_binario_relevante": round(float(cohen_kappa_score(a == 2, b == 2)), 4),
        "matriz": pd.crosstab(a, b).to_dict(),
    }
    (REPORTS_DIR / "concordancia_juizes.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return res
