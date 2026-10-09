"""Avaliação da recuperação: ablação, comparação de embeddings e calibração do limiar.

Protocolo (pooling, como nas avaliações TREC):
  1. Cada configuração recupera para cada pergunta; guarda-se o top-10.
  2. A união dos top-10 de todas as configurações (+ o contexto final do
     sistema + uma amostra ao longo do ranking do reranker) forma o "pool"
     de cada pergunta.
  3. O LLM-juiz dá relevância 0/1/2 a cada par (pergunta, avaliação) do pool.
  4. As métricas de cada configuração são calculadas sobre esses julgamentos,
     então todas são medidas com a MESMA régua.

Perguntas usadas: as respondíveis (Q01-Q28) para as métricas de qualidade e as
sem evidência (Q35-Q40) como negativos na calibração do limiar.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import replace

import numpy as np
import pandas as pd

from voc_rag.config import EVAL_DIR, REPORTS_DIR
from voc_rag.evaluation.judge import (
    carrega_julgamentos,
    juiz,
    julga_relevancia,
    salva_julgamentos,
)
from voc_rag.generation.llm import LLMClient, LLMIndisponivel
from voc_rag.retrieval.filters import Filtros
from voc_rag.retrieval.query import analisa_pergunta
from voc_rag.retrieval.retriever import RetrievalConfig, get_kb, recupera

log = logging.getLogger(__name__)

K = 10

_SEM_EXTRAS = dict(usar_filtros=False, usar_polaridade=False)

# Ablação incremental: cada linha acrescenta UMA técnica à anterior.
ABLACAO: dict[str, RetrievalConfig] = {
    "A0_denso_pergunta_crua": RetrievalConfig(
        usar_reescrita=False, usar_alternativas=False, usar_hyde=False, usar_bm25=False,
        usar_rerank=False, **_SEM_EXTRAS),
    "A1_reescrita": RetrievalConfig(
        usar_alternativas=False, usar_hyde=False, usar_bm25=False, usar_rerank=False,
        **_SEM_EXTRAS),
    "A2_multiquery_hyde": RetrievalConfig(usar_bm25=False, usar_rerank=False, **_SEM_EXTRAS),
    "A3_hibrido_bm25_rrf": RetrievalConfig(usar_rerank=False, **_SEM_EXTRAS),
    "A4_reranker": RetrievalConfig(ordenar_por="reranker", **_SEM_EXTRAS),
    "A5_metadados_polaridade": RetrievalConfig(
        usar_alternativas=True, usar_hyde=True, ordenar_por="reranker"),
}

ROTULO_ABLACAO = {
    "A0_denso_pergunta_crua": "RAG ingênuo (pergunta crua, só vetor)",
    "A1_reescrita": "+ reescrita da pergunta",
    "A2_multiquery_hyde": "+ multi-query e HyDE",
    "A3_hibrido_bm25_rrf": "+ BM25 (híbrido, RRF)",
    "A4_reranker": "+ reranker cross-encoder",
    "A5_metadados_polaridade": "+ filtros de metadado e polaridade",
}

# Comparação de embeddings: mesma configuração (A1: consulta reescrita, só vetor).
EMBEDDINGS = {
    "E_minilm": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "E_e5_base": "intfloat/multilingual-e5-base",
    "E_bge_m3": "BAAI/bge-m3",
}


def carrega_perguntas() -> list[dict]:
    return json.loads((EVAL_DIR / "perguntas.json").read_text(encoding="utf-8"))


# Variantes que isolam o efeito de cada componente (diagnóstico da ablação).
VARIANTES: dict[str, RetrievalConfig] = {
    "V1_hibrido_so_reescrita": RetrievalConfig(
        usar_alternativas=False, usar_hyde=False, usar_rerank=False, **_SEM_EXTRAS),
    "V2_hibrido_sem_hyde": RetrievalConfig(usar_hyde=False, usar_rerank=False, **_SEM_EXTRAS),
    "V3_reranker_consulta_principal": RetrievalConfig(
        consulta_rerank="consulta_busca", ordenar_por="reranker", **_SEM_EXTRAS),
    "V4_reranker_media": RetrievalConfig(
        consulta_rerank="media_consultas", ordenar_por="reranker", **_SEM_EXTRAS),
    # Candidatos a sistema final: ordem RRF, reranker como porteiro, metadados ligados.
    "F1_final_so_reescrita": RetrievalConfig(
        usar_alternativas=False, usar_hyde=False, ordenar_por="rrf"),
    "F2_final_multiquery": RetrievalConfig(
        usar_alternativas=True, usar_hyde=True, ordenar_por="rrf"),
}

ROTULO_VARIANTES = {
    "V1_hibrido_so_reescrita": "híbrido só com a consulta reescrita",
    "V2_hibrido_sem_hyde": "híbrido com variações, sem HyDE",
    "V3_reranker_consulta_principal": "reranker contra a consulta principal",
    "V4_reranker_media": "reranker pela média das consultas",
    "F1_final_so_reescrita": "final: reescrita + híbrido + metadados, ordem RRF",
    "F2_final_multiquery": "final: + multi-query e HyDE, ordem RRF",
}


# Configuração que representa o sistema entregue (igual ao RetrievalConfig() padrão).
SISTEMA_FINAL = "F1_final_so_reescrita"
COM_CONTEXTO = ["A5_metadados_polaridade", "F1_final_so_reescrita", "F2_final_multiquery"]


def _configs() -> dict[str, RetrievalConfig]:
    cfgs = dict(ABLACAO) | dict(VARIANTES)
    for nome, modelo in EMBEDDINGS.items():
        cfgs[nome] = replace(ABLACAO["A1_reescrita"], modelo_embedding=modelo)
    return cfgs


# --------------------------------------------------------------------------
# Métricas
# --------------------------------------------------------------------------
def ndcg(graus: list[int], ideais: list[int], k: int = K) -> float:
    def dcg(gs):
        return sum((2**g - 1) / np.log2(i + 2) for i, g in enumerate(gs[:k]))

    ideal = dcg(sorted(ideais, reverse=True))
    return float(dcg(graus) / ideal) if ideal > 0 else 0.0


def metricas_ranking(ids: list[str], graus: dict[str, int], ideais: list[int]) -> dict:
    g = [graus.get(i, 0) for i in ids[:K]]
    estritos = [x == 2 for x in g]
    primeiro = next((i for i, x in enumerate(estritos) if x), None)
    return {
        "p@5": float(np.mean(estritos[:5])) if g else 0.0,
        "p@10": float(np.mean(estritos)) if g else 0.0,
        "p@10_leniente": float(np.mean([x >= 1 for x in g])) if g else 0.0,
        "ndcg@10": ndcg(g, ideais),
        "mrr": 0.0 if primeiro is None else 1.0 / (primeiro + 1),
        "hit@5": float(any(estritos[:5])),
    }


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------
def run(llm: LLMClient | None = None) -> dict:
    llm = llm or LLMClient()
    perguntas = [p for p in carrega_perguntas() if p["grupo"] not in ("fora_escopo",)]
    cfgs = _configs()
    kb_padrao = get_kb()
    analises = {p["id"]: analisa_pergunta(p["pergunta"], kb_padrao.categorias, llm)
                for p in perguntas}
    degradadas = [q for q, a in analises.items() if a.origem == "fallback"]
    if degradadas:
        # Sem LLM a análise cai no modo degradado; medir assim contaminaria a avaliação.
        raise RuntimeError(f"análise sem LLM em {degradadas}: avaliação abortada")

    rankings: dict[str, dict[str, list[str]]] = {n: {} for n in cfgs}
    # Contexto efetivamente enviado ao LLM (com limiar, dedupe e MMR) das configurações
    # candidatas a sistema final, e escores do porteiro para calibrar o limiar.
    contextos: dict[str, dict[str, list[str]]] = {n: {} for n in COM_CONTEXTO}
    escores_final: dict[str, pd.DataFrame] = {}
    for nome, cfg in cfgs.items():
        kb = get_kb(cfg.modelo_embedding)
        kb.aquece()
        for p in perguntas:
            a = analises[p["id"]]
            if a.escopo == "fora":
                continue
            r = recupera(p["pergunta"], a, replace(cfg, limiar_relevancia=0.0), kb)
            if r.candidatos.empty:
                rankings[nome][p["id"]] = []
                continue
            rankings[nome][p["id"]] = r.candidatos["review_id"].tolist()[:K]
            if nome == SISTEMA_FINAL:
                escores_final[p["id"]] = r.candidatos[["review_id", "relevancia"]]
            if nome in COM_CONTEXTO:
                final = recupera(p["pergunta"], a, cfg, kb)
                contextos[nome][p["id"]] = final.selecionados["review_id"].tolist() \
                    if not final.selecionados.empty else []
        log.info("configuração %s concluída", nome)

    # Pool por pergunta, julgado pergunta a pergunta e salvo a cada uma (a cota gratuita
    # e a sobrecarga do Gemini interrompem execuções; nada julgado se perde).
    julg = carrega_julgamentos()
    docs = kb_padrao.docs
    llm_juiz = juiz()
    pendentes = list(perguntas)
    for rodada in range(4):
        falharam = []
        for p in pendentes:
            qid = p["id"]
            pool: set[str] = set()
            for nome in cfgs:
                pool.update(rankings[nome].get(qid, []))
            for ctx in contextos.values():
                pool.update(ctx.get(qid, []))
            if qid in escores_final:  # amostra ao longo do ranking, para calibrar o limiar
                pool.update(escores_final[qid]["review_id"].iloc[::4].tolist())
            ja = set(julg.loc[julg["qid"] == qid, "review_id"])
            faltam = sorted(d for d in pool if d not in ja)
            if not faltam:
                continue
            criterio = p.get("criterio") or (
                f"a avaliação trata do assunto da pergunta: {p['pergunta']}")
            try:
                g = julga_relevancia(p["pergunta"], criterio, docs.loc[faltam], llm_juiz,
                                     metadados=bool(p.get("filtros_esperados")))
            except LLMIndisponivel as e:
                log.warning("%s adiada (juiz indisponível: %s)", qid, str(e)[:80])
                falharam.append(p)
                continue
            novos = pd.DataFrame([{"qid": qid, "review_id": d, "relevancia": v,
                                   "juiz": llm_juiz.ultimo_modelo} for d, v in g.items()])
            julg = pd.concat([julg, novos], ignore_index=True)
            salva_julgamentos(julg)
            log.info("%s: %s pares julgados", qid, len(g))
        if not falharam:
            break
        pendentes = falharam
        log.warning("%s perguntas adiadas; nova rodada em %s s", len(pendentes), 60 * (rodada + 1))
        time.sleep(60 * (rodada + 1))
    else:
        raise RuntimeError(f"juiz indisponível para {[p['id'] for p in pendentes]}: "
                           "rode de novo mais tarde (o que foi julgado está salvo)")
    graus_por_q = {q: dict(zip(g["review_id"], g["relevancia"], strict=True))
                   for q, g in julg.groupby("qid")}

    # Métricas por configuração
    respondiveis = [p for p in perguntas if p["esperado"] == "responder"]
    resultado: dict = {"k": K, "configuracoes": {}, "por_pergunta": {}}
    for nome in cfgs:
        linhas = []
        for p in respondiveis:
            graus = graus_por_q.get(p["id"], {})
            m = metricas_ranking(rankings[nome].get(p["id"], []), graus, list(graus.values()))
            if p.get("filtros_esperados"):
                ids = rankings[nome].get(p["id"], [])
                mask = Filtros(**p["filtros_esperados"]).mask(docs.loc[ids]) if ids else []
                m["conformidade_metadado@10"] = float(np.mean(mask)) if len(ids) else 0.0
            linhas.append({"qid": p["id"], "grupo": p["grupo"], **m})
            resultado["por_pergunta"].setdefault(p["id"], {})[nome] = m
        df = pd.DataFrame(linhas)
        agg = df.drop(columns=["qid", "grupo"]).mean(numeric_only=True).round(4).to_dict()
        meta = df[df["grupo"] == "metadados"]
        agg["metadados_p@10"] = round(float(meta["p@10"].mean()), 4)
        agg["metadados_conformidade@10"] = round(float(meta["conformidade_metadado@10"].mean()), 4)
        resultado["configuracoes"][nome] = agg

    # Precisão do contexto (o que de fato vai para o LLM), por configuração candidata
    def precisao(ctx: dict[str, list[str]]) -> float:
        valores = []
        for p in respondiveis:
            ids = ctx.get(p["id"], [])
            if ids:
                graus = graus_por_q.get(p["id"], {})
                valores.append(np.mean([graus.get(i, 0) == 2 for i in ids]))
        return round(float(np.mean(valores)), 4)

    resultado["precisao_contexto"] = {n: precisao(c) for n, c in contextos.items()}
    resultado["precisao_contexto_final"] = resultado["precisao_contexto"][SISTEMA_FINAL]
    resultado["sistema_final"] = SISTEMA_FINAL

    # Calibração do limiar do reranker
    pares = []
    for p in perguntas:
        if p["id"] not in escores_final:
            continue
        graus = graus_por_q.get(p["id"], {})
        for r in escores_final[p["id"]].itertuples():
            if r.review_id in graus:
                pares.append({"qid": p["id"], "esperado": p["esperado"],
                              "relevancia_reranker": float(r.relevancia),
                              "juiz": int(graus[r.review_id])})
    resultado["calibracao_limiar"] = calibra_limiar(pd.DataFrame(pares))
    (REPORTS_DIR / "calibracao_pares.csv").parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(pares).to_csv(REPORTS_DIR / "calibracao_pares.csv", index=False)

    resultado["n_perguntas_respondiveis"] = len(respondiveis)
    resultado["n_julgamentos"] = int(len(julg))
    resultado["rotulos"] = ROTULO_ABLACAO | ROTULO_VARIANTES | dict(EMBEDDINGS)
    (REPORTS_DIR / "avaliacao_recuperacao.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return resultado


def calibra_limiar(pares: pd.DataFrame) -> dict:
    """Escolhe o limiar do reranker que maximiza o F1 de 'relevante' (juiz = 2)."""
    if pares.empty:
        return {}
    from sklearn.metrics import roc_auc_score

    y = (pares["juiz"] == 2).to_numpy()
    s = pares["relevancia_reranker"].to_numpy()
    grade = np.round(np.arange(0.05, 0.96, 0.05), 2)
    tabela = []
    for t in grade:
        pred = s >= t
        tp = int((pred & y).sum())
        prec = tp / max(int(pred.sum()), 1)
        rec = tp / max(int(y.sum()), 1)
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        tabela.append({"limiar": float(t), "precisao": round(prec, 4), "recall": round(rec, 4),
                       "f1": round(f1, 4)})
    melhor = max(tabela, key=lambda r: r["f1"])
    sem_ev = pares[pares["esperado"] == "abster"]
    max_sem_ev = (
        round(float(sem_ev["relevancia_reranker"].max()), 4) if not sem_ev.empty else None
    )
    return {
        "n_pares": int(len(pares)),
        "auc_reranker_vs_juiz": round(float(roc_auc_score(y, s)), 4) if y.any() and (~y).any()
        else None,
        "limiar_f1_max": melhor,
        "tabela": tabela,
        "max_relevancia_perguntas_sem_evidencia": max_sem_ev,
    }
