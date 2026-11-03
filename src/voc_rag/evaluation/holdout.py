"""Conjunto retido: estimativa sem o viés de ajustar e medir nas mesmas perguntas.

As perguntas de eval/perguntas_retidas.json foram escritas depois de congelado o sistema
(prompts, configuração e limiar) e versionadas num commit antes da primeira execução. Elas não
guiam nenhuma decisão: o resultado é reportado como saiu, mesmo quando é pior que o das 44
perguntas de desenvolvimento (D23).
"""
from __future__ import annotations

import json
import logging
from dataclasses import replace

import numpy as np
import pandas as pd

from voc_rag.config import EVAL_DIR, REPORTS_DIR
from voc_rag.evaluation.generation_eval import (
    PESO_VEREDITO,
    acerto_filtros,
    completa_fidelidade,
    material_auditoria,
)
from voc_rag.evaluation.judge import juiz, julga_relevancia
from voc_rag.evaluation.retrieval_eval import K, metricas_ranking
from voc_rag.pipeline import STATUS_ABSTENCAO, VoCPipeline
from voc_rag.retrieval.filters import Filtros
from voc_rag.retrieval.retriever import recupera

log = logging.getLogger(__name__)

PERGUNTAS_JSON = EVAL_DIR / "perguntas_retidas.json"
JULGAMENTOS_CSV = EVAL_DIR / "julgamentos_retidos.csv"
RESPOSTAS_JSON = REPORTS_DIR / "respostas_retidas.json"
RESULTADO_JSON = REPORTS_DIR / "avaliacao_retida.json"


def carrega_perguntas() -> list[dict]:
    return json.loads(PERGUNTAS_JSON.read_text(encoding="utf-8"))


def _salva_respostas(registros: list[dict]) -> None:
    RESPOSTAS_JSON.write_text(
        json.dumps(registros, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )


def _julga(p: dict, ids: list[str], docs: pd.DataFrame, julg: pd.DataFrame, llm) -> pd.DataFrame:
    """Julga os pares ainda sem veredito da pergunta e salva (nada julgado se perde)."""
    ja = set(julg.loc[julg["qid"] == p["id"], "review_id"])
    faltam = sorted(i for i in set(ids) if i not in ja)
    if not faltam:
        return julg
    g = julga_relevancia(p["pergunta"], p["criterio"], docs.loc[faltam], llm,
                         metadados=bool(p.get("filtros_esperados")))
    novos = pd.DataFrame([{"qid": p["id"], "review_id": d, "relevancia": v,
                           "juiz": llm.ultimo_modelo} for d, v in g.items()])
    julg = pd.concat([julg, novos], ignore_index=True)
    julg.sort_values(["qid", "review_id"]).to_csv(JULGAMENTOS_CSV, index=False)
    return julg


def run() -> dict:
    perguntas = carrega_perguntas()
    pipe = VoCPipeline()
    docs = pipe.kb.docs
    llm_juiz = juiz()
    julg = (pd.read_csv(JULGAMENTOS_CSV) if JULGAMENTOS_CSV.exists()
            else pd.DataFrame(columns=["qid", "review_id", "relevancia", "juiz"]))
    registros, rankings = [], {}
    for p in perguntas:
        r = pipe.responder(p["pergunta"])
        if (r.analise and r.analise.origem == "fallback") or r.status == "erro_llm":
            raise RuntimeError(f"{p['id']}: LLM indisponível; rode de novo (usa o cache)")
        d = r.to_dict()
        d.update({"id": p["id"], "grupo": p["grupo"], "esperado": p["esperado"]})
        if r.gerada is not None and r.gerada.insights:
            d["auditoria"] = material_auditoria(r, d["pergunta"])
        registros.append(d)
        log.info("%s %s", p["id"], r.status)
        if p["esperado"] == "responder":
            ids: list[str] = []
            if r.analise.escopo == "dentro":
                # Mesma medição do desenvolvimento: top-10 sem o limiar do porteiro.
                rec = recupera(p["pergunta"], r.analise,
                               replace(pipe.cfg, limiar_relevancia=0.0), pipe.kb)
                if not rec.candidatos.empty:
                    ids = rec.candidatos["review_id"].tolist()[:K]
            rankings[p["id"]] = ids
            contexto = r.evidencias["review_id"].tolist() if not r.evidencias.empty else []
            julg = _julga(p, ids + contexto, docs, julg, llm_juiz)
    _salva_respostas(registros)
    completa_fidelidade(registros, salvar=_salva_respostas)
    return resume(registros, rankings, julg, docs)


def resume(registros: list[dict], rankings: dict[str, list[str]], julg: pd.DataFrame,
           docs: pd.DataFrame) -> dict:
    perguntas = {p["id"]: p for p in carrega_perguntas()}
    graus_por_q = {q: dict(zip(g["review_id"], g["relevancia"], strict=True))
                   for q, g in julg.groupby("qid")}

    metricas, conformidade, por_pergunta = [], [], {}
    for qid, ids in rankings.items():
        graus = graus_por_q.get(qid, {})
        m = metricas_ranking(ids, graus, list(graus.values()))
        esperado = perguntas[qid].get("filtros_esperados")
        if esperado:
            mask = Filtros(**esperado).mask(docs.loc[ids]) if ids else []
            m["conformidade@10"] = float(np.mean(mask)) if len(ids) else 0.0
            conformidade.append(m["conformidade@10"])
        metricas.append(m)
        por_pergunta[qid] = {k: round(float(v), 3) for k, v in m.items()}

    def media(chave: str) -> float:
        return round(float(np.mean([m[chave] for m in metricas])), 4)

    erros = []
    corretas = 0
    for d in registros:
        absteve = d["status"] in STATUS_ABSTENCAO
        if absteve == (d["esperado"] == "abster"):
            corretas += 1
        else:
            erros.append({"id": d["id"], "pergunta": d["pergunta"], "esperado": d["esperado"],
                          "status": d["status"]})

    cit = [d["citacoes"] for d in registros if isinstance(d.get("citacoes"), dict)]
    total = sum(c["citacoes_total"] for c in cit)
    invalidas = sum(c["citacoes_invalidas"] for c in cit)
    vereditos = [v["veredito"] for d in registros if d.get("fidelidade")
                 for v in d["fidelidade"]["insights"]]
    filtros = [acerto_filtros(perguntas[d["id"]]["filtros_esperados"], d["analise"]["filtros"])
               for d in registros
               if perguntas[d["id"]].get("filtros_esperados") and d.get("analise")]

    resultado = {
        "n_perguntas": len(registros),
        "n_respondiveis": len(rankings),
        "n_abster": len(registros) - len(rankings),
        "decisoes": {"corretas": corretas, "total": len(registros), "erros": erros},
        "status_por_pergunta": {d["id"]: d["status"] for d in registros},
        "recuperacao": {"p@5": media("p@5"), "p@10": media("p@10"),
                        "p@10_leniente": media("p@10_leniente"), "mrr": media("mrr"),
                        "hit@5": media("hit@5"),
                        "conformidade@10": round(float(np.mean(conformidade)), 4)
                        if conformidade else None},
        "citacoes": {"total": int(total),
                     "validas_pct": round(1 - invalidas / max(total, 1), 4)},
        "fidelidade": {
            "insights_julgados": len(vereditos),
            "sustentados": sum(v == "sustentado" for v in vereditos),
            "escore": round(float(np.mean([PESO_VEREDITO[v] for v in vereditos])), 4)
            if vereditos else None,
        },
        "extracao_filtros": {"perguntas": len(filtros),
                             "corretas": int(sum(filtros))},
        "n_julgamentos": int(len(julg)),
        "por_pergunta": por_pergunta,
    }
    RESULTADO_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2),
                              encoding="utf-8")
    return resultado
