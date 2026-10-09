"""Avaliação ponta a ponta: abstenção, citações, fidelidade, filtros e custo.

Roda o pipeline completo nas 40 perguntas de eval/perguntas.json e mede:
  * abstenção: o sistema responde o que deve e se abstém do que deve
    (fora de escopo e sem evidência);
  * citações: % de citações válidas antes da limpeza e insights descartados;
  * fidelidade: o LLM-juiz verifica se cada insight é sustentado pelas
    evidências que ele cita;
  * filtros: a análise da pergunta extraiu os metadados esperados?
  * latência e tokens por etapa.
"""
from __future__ import annotations

import json
import logging
import time

import numpy as np
import pandas as pd

from voc_rag.config import REPORTS_DIR
from voc_rag.evaluation.judge import juiz, julga_fidelidade_lote
from voc_rag.evaluation.retrieval_eval import carrega_perguntas
from voc_rag.generation.llm import LLMClient, LLMIndisponivel
from voc_rag.pipeline import STATUS_ABSTENCAO, VoCPipeline

log = logging.getLogger(__name__)

PESO_VEREDITO = {"sustentado": 1.0, "parcial": 0.5, "nao_sustentado": 0.0}


def acerto_filtros(esperado: dict, extraido: dict) -> bool:
    for campo, valor in esperado.items():
        v = extraido.get(campo)
        if isinstance(valor, list):
            if set(valor) - set(v or []):
                return False
        elif v != valor:
            return False
    return True


def run(llm: LLMClient | None = None) -> dict:
    perguntas = carrega_perguntas()
    pipe = VoCPipeline(llm=llm)
    registros = []
    for p in perguntas:
        r = pipe.responder(p["pergunta"])
        if (r.analise and r.analise.origem == "fallback") or r.status == "erro_llm":
            raise RuntimeError(f"{p['id']}: LLM indisponível; avaliação abortada")
        d = r.to_dict()
        d.update({"id": p["id"], "grupo": p["grupo"], "esperado": p["esperado"]})
        registros.append(d)
        log.info("%s %s", p["id"], r.status)

        # Material da auditoria de fidelidade guardado junto da resposta: a auditoria pode
        # ser concluída depois (`voc avaliar --etapa fidelidade`) sem refazer o pipeline.
        if r.gerada is not None and r.gerada.insights:
            quadro_txt = None
            if r.quadro is not None:
                quadro_txt = "\n".join(f"- {q.rotulo}: ~{q.avaliacoes} ({q.pct:.1f}%)"
                                       for q in r.quadro.itertuples())
            d["auditoria"] = {
                "pergunta": d["pergunta"], "resumo": r.gerada.resumo,
                "insights": [i.model_dump() for i in r.gerada.insights],
                "evidencias": dict(zip(r.evidencias["rotulo"], r.evidencias["texto"],
                                       strict=True)),
                "quadro": quadro_txt,
            }

    salva_registros(registros)
    completa_fidelidade(registros)
    return resume(registros, pipe)


PERGUNTAS_LATENCIA = [
    "O que os clientes falam sobre o prazo de entrega dos pedidos?",
    "Quais problemas os compradores relatam com produtos eletrônicos?",
    "O que os clientes elogiam nos produtos de esporte e lazer?",
    "Há reclamações sobre cobrança indevida no cartão?",
    "Como os clientes descrevem pedidos que chegaram com peças faltando?",
]


def mede_latencia(perguntas: list[str] = PERGUNTAS_LATENCIA) -> dict:
    """Latência real (sem cache do LLM), com modelos já carregados e aquecidos."""
    pipe = VoCPipeline(llm=LLMClient(usar_cache=False))
    linhas = []
    for p in perguntas:
        r = pipe.responder(p)
        linhas.append({"pergunta": p, "status": r.status, **r.tempos})
    df = pd.DataFrame(linhas)
    res = {
        "n": int(len(df)),
        "dispositivo": pipe.kb.embedder.device,
        "modelo_llm": pipe.llm.model,
        "mediana_s": {c: round(float(df[c].median()), 2) for c in
                      ("analise_s", "recuperacao_s", "geracao_s", "total_s") if c in df},
        "por_pergunta": linhas,
    }
    (REPORTS_DIR / "latencia.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return res


def salva_registros(registros: list[dict]) -> None:
    (REPORTS_DIR / "respostas_avaliacao.json").write_text(
        json.dumps(registros, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )


def carrega_registros() -> list[dict]:
    return json.loads((REPORTS_DIR / "respostas_avaliacao.json").read_text(encoding="utf-8"))


def completa_fidelidade(registros: list[dict], lote: int = 3, rodadas: int = 4) -> int:
    """Audita as respostas ainda sem veredito, em lotes, salvando a cada lote.
    Devolve quantas continuam pendentes (juiz indisponível em todas as rodadas)."""
    llm_juiz = juiz()
    for rodada in range(rodadas):
        pendentes = [d for d in registros if d.get("auditoria") and "fidelidade" not in d]
        if not pendentes:
            return 0
        falhou = False
        for i in range(0, len(pendentes), lote):
            fatia = pendentes[i : i + lote]
            try:
                vereditos = julga_fidelidade_lote([d["auditoria"] for d in fatia], llm_juiz,
                                                  lote=lote)
            except LLMIndisponivel as e:
                log.warning("auditoria adiada (%s)", str(e)[:80])
                falhou = True
                continue
            for d, f in zip(fatia, vereditos, strict=True):
                if f is not None:
                    d["fidelidade"] = f.model_dump()
                    d["fidelidade"]["juiz"] = llm_juiz.ultimo_modelo
            salva_registros(registros)
        if falhou and rodada < rodadas - 1:
            log.warning("nova rodada de auditoria em %s s", 60 * (rodada + 1))
            time.sleep(60 * (rodada + 1))
    restantes = sum(1 for d in registros if d.get("auditoria") and "fidelidade" not in d)
    if restantes:
        log.warning("%s respostas sem auditoria de fidelidade: rode `voc avaliar --etapa "
                    "fidelidade` mais tarde", restantes)
    return restantes


def resume(registros: list[dict], pipe: VoCPipeline | None = None) -> dict:
    df = pd.DataFrame(registros)
    df["absteve"] = df["status"].isin(STATUS_ABSTENCAO)
    df["deve_abster"] = df["esperado"] == "abster"

    tp = int((df["absteve"] & df["deve_abster"]).sum())
    fp = int((df["absteve"] & ~df["deve_abster"]).sum())
    fn = int((~df["absteve"] & df["deve_abster"]).sum())
    tn = int((~df["absteve"] & ~df["deve_abster"]).sum())
    abst = {
        "acuracia": round((tp + tn) / len(df), 4),
        "precisao_abstencao": round(tp / max(tp + fp, 1), 4),
        "recall_abstencao": round(tp / max(tp + fn, 1), 4),
        "matriz": {"abstencao_correta": tp, "abstencao_indevida": fp,
                   "resposta_indevida": fn, "resposta_correta": tn},
        "status_por_grupo": {g: s["status"].value_counts().to_dict()
                             for g, s in df.groupby("grupo")},
    }

    cit = [c for c in df["citacoes"] if isinstance(c, dict)]
    total = sum(c["citacoes_total"] for c in cit)
    invalidas = sum(c["citacoes_invalidas"] for c in cit)
    citacoes = {
        "respostas_com_citacao": len(cit),
        "citacoes_total": int(total),
        "citacoes_validas_pct": round(1 - invalidas / max(total, 1), 4),
        "insights_total": int(sum(c["insights_total"] for c in cit)),
        "insights_descartados_sem_evidencia": int(sum(c["insights_descartados"] for c in cit)),
    }

    vereditos = []
    resumos = []
    for f in df.get("fidelidade", pd.Series(dtype=object)).dropna():
        vereditos += [v["veredito"] for v in f["insights"]]
        resumos.append(f["resumo"])
    fid = {
        "insights_julgados": len(vereditos),
        "distribuicao": pd.Series(vereditos).value_counts().to_dict() if vereditos else {},
        "escore_fidelidade": round(float(np.mean([PESO_VEREDITO[v] for v in vereditos])), 4)
        if vereditos else None,
        "resumos_sustentados_pct": round(float(np.mean([r == "sustentado" for r in resumos])), 4)
        if resumos else None,
    }

    perg = {p["id"]: p for p in carrega_perguntas()}
    filtros_linhas = []
    for d in registros:
        esp = perg[d["id"]].get("filtros_esperados")
        if esp and d.get("analise"):
            ok = acerto_filtros(esp, d["analise"]["filtros"])
            filtros_linhas.append({"id": d["id"], "acerto": ok})
    filtros = {
        "perguntas": len(filtros_linhas),
        "acerto_pct": round(float(np.mean([x["acerto"] for x in filtros_linhas])), 4)
        if filtros_linhas else None,
        "por_pergunta": filtros_linhas,
    }

    tempos = pd.DataFrame([t for t in df["tempos"] if isinstance(t, dict)])
    respondidas = df[df["status"] == "respondida"]
    t_resp = pd.DataFrame([t for t in respondidas["tempos"]])
    lat = {
        "total_mediana_s_respondidas": round(float(t_resp["total_s"].median()), 2)
        if not t_resp.empty else None,
        "recuperacao_mediana_s": round(float(tempos["recuperacao_s"].dropna().median()), 3)
        if "recuperacao_s" in tempos else None,
        "geracao_mediana_s": round(float(t_resp["geracao_s"].median()), 2)
        if "geracao_s" in t_resp else None,
        "analise_mediana_s": round(float(tempos["analise_s"].median()), 2),
    }

    resumo = {
        "n_perguntas": int(len(df)),
        "abstencao": abst,
        "citacoes": citacoes,
        "fidelidade": fid,
        "extracao_filtros": filtros,
        "latencia": lat,
    }
    if pipe is not None:
        resumo["uso_llm_execucao"] = vars(pipe.llm.uso)
    (REPORTS_DIR / "avaliacao_geracao.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return resumo
