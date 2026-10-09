"""Recuperação: busca híbrida, fusão RRF, reranking e seleção do contexto.

Fluxo para uma pergunta já analisada (query.py):

  consultas (reescrita + variações + avaliação hipotética)
      │                 │
  busca densa       busca BM25          ← ambas respeitam os filtros de metadado
  (Chroma, cosseno) (bm25s, stemming)
      └──────┬──────────┘
        fusão RRF (Reciprocal Rank Fusion)
             │  top N candidatos
        reranker cross-encoder  →  relevância em [0, 1]
             │
        seleção: limiar de relevância + deduplicação de texto + MMR (diversidade)
             │
        evidências do contexto
"""
from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from functools import lru_cache

import numpy as np
import pandas as pd

from voc_rag.config import get_settings
from voc_rag.data.prepare import load_documents
from voc_rag.indexing.bm25_index import BM25Index
from voc_rag.indexing.embeddings import get_embedder, load_embeddings
from voc_rag.indexing.vector_store import VectorStore
from voc_rag.retrieval.filters import Filtros
from voc_rag.retrieval.query import AnalisePergunta
from voc_rag.retrieval.rerank import get_reranker

log = logging.getLogger(__name__)


@dataclass
class RetrievalConfig:
    usar_reescrita: bool = True          # False = busca com a pergunta crua (baseline)
    usar_denso: bool = True
    usar_bm25: bool = True
    usar_alternativas: bool = True       # multi-query
    usar_hyde: bool = True               # avaliação hipotética
    usar_polaridade: bool = True         # filtro implícito de nota pela polaridade
    usar_filtros: bool = True            # filtros explícitos de metadado
    usar_rerank: bool = True
    # Texto contra o qual o cross-encoder pontua cada avaliação:
    #   "pergunta"       pergunta original do gestor (registro analítico)
    #   "consulta_busca" consulta reescrita no vocabulário do cliente
    #   "max_consultas"  maior score entre reescrita e variações (padrão)
    consulta_rerank: str = "max_consultas"
    k_por_consulta: int = 50
    rrf_k: int = 60
    n_rerank: int = 80
    limiar_relevancia: float = 0.30      # calibrado em reports/avaliacao (ver decisões)
    min_evidencias: int = 3              # abaixo disso: evidência insuficiente
    n_contexto_tema: int = 15
    n_contexto_panorama: int = 30
    mmr_lambda: float = 0.75
    modelo_embedding: str | None = None


@dataclass
class ResultadoRecuperacao:
    filtros_aplicados: Filtros
    consultas: list[str]
    candidatos: pd.DataFrame                   # todos os candidatos com scores
    selecionados: pd.DataFrame                 # evidências que vão para o contexto
    n_relevantes: int
    n_universo: int                            # documentos que passam no filtro
    tempos: dict = field(default_factory=dict)

    def resumo(self) -> dict:
        return {
            "filtros": self.filtros_aplicados.model_dump(exclude_defaults=True),
            "consultas": self.consultas,
            "n_universo": self.n_universo,
            "n_candidatos": int(len(self.candidatos)),
            "n_relevantes": self.n_relevantes,
            "n_selecionados": int(len(self.selecionados)),
            "tempos": self.tempos,
        }


# --------------------------------------------------------------------------
# Recursos carregados uma vez por processo
# --------------------------------------------------------------------------
class KnowledgeBase:
    def __init__(self, modelo_embedding: str | None = None):
        self.modelo = modelo_embedding or get_settings().embedding_model
        self.docs = load_documents().set_index("review_id", drop=False)
        # Índice sem nome: evita ambiguidade índice x coluna nos merges.
        self.docs.index.name = None
        self.docs_pos = pd.Series(np.arange(len(self.docs)), index=self.docs.index)
        self.store = VectorStore(self.modelo)
        self.bm25 = BM25Index.load()
        if self.bm25.doc_ids != self.docs["review_id"].tolist():
            raise RuntimeError("Índice BM25 desalinhado com documents.parquet: rode `voc build`.")
        self.emb = load_embeddings(self.modelo, self.docs["review_id"].tolist())
        self.categorias = sorted(self.docs["categoria"].unique().tolist())

    @property
    def embedder(self):
        return get_embedder(self.modelo)

    @property
    def reranker(self):
        return get_reranker()

    def aquece(self) -> None:
        """Carrega os modelos e roda uma consulta, para a 1ª pergunta ter latência real."""
        self.embedder.encode_queries(["entrega atrasada"])
        self.reranker.score("entrega atrasada", ["o produto chegou atrasado"])


@lru_cache(maxsize=3)
def get_kb(modelo_embedding: str | None = None) -> KnowledgeBase:
    return KnowledgeBase(modelo_embedding)


# --------------------------------------------------------------------------
# Etapas
# --------------------------------------------------------------------------
def filtros_efetivos(analise: AnalisePergunta, cfg: RetrievalConfig) -> Filtros:
    f = analise.filtros.model_copy(deep=True) if cfg.usar_filtros else Filtros()
    tem_nota = f.nota_min is not None or f.nota_max is not None or f.sentimentos
    if cfg.usar_polaridade and not tem_nota:
        if analise.polaridade == "negativa":
            f.nota_max = 3
        elif analise.polaridade == "positiva":
            f.nota_min = 4
    return f


def consultas_de(
    analise: AnalisePergunta, cfg: RetrievalConfig, pergunta: str | None = None
) -> list[str]:
    if not cfg.usar_reescrita and pergunta:
        return [pergunta.strip()]
    qs = [analise.consulta_busca]
    if cfg.usar_alternativas:
        qs += analise.consultas_alternativas
    if cfg.usar_hyde and analise.avaliacao_hipotetica:
        qs.append(analise.avaliacao_hipotetica)
    vistos, saida = set(), []
    for q in qs:
        q = q.strip()
        if q and q.lower() not in vistos:
            vistos.add(q.lower())
            saida.append(q)
    return saida


def rrf(listas: list[list[tuple[str, float]]], k: int) -> dict[str, float]:
    """Reciprocal Rank Fusion: soma 1/(k + posição) de cada lista.

    Funde rankings de naturezas diferentes (cosseno e BM25 não são comparáveis
    em escala) usando apenas a posição; k=60 é o valor padrão da literatura.
    """
    score: dict[str, float] = {}
    for lista in listas:
        for pos, (doc_id, _) in enumerate(lista):
            score[doc_id] = score.get(doc_id, 0.0) + 1.0 / (k + pos + 1)
    return score


def mmr(
    ids: list[str], relevancia: np.ndarray, vetores: np.ndarray, n: int, lam: float
) -> list[int]:
    """Maximal Marginal Relevance: relevante E diferente do que já foi escolhido."""
    if len(ids) <= n:
        return list(range(len(ids)))
    escolhidos: list[int] = [int(np.argmax(relevancia))]
    sim = vetores @ vetores.T
    restantes = set(range(len(ids))) - set(escolhidos)
    while len(escolhidos) < n and restantes:
        r = np.array(sorted(restantes))
        redund = sim[np.ix_(r, escolhidos)].max(axis=1)
        valor = lam * relevancia[r] - (1 - lam) * redund
        melhor = int(r[np.argmax(valor)])
        escolhidos.append(melhor)
        restantes.discard(melhor)
    return escolhidos


def recupera(
    pergunta: str,
    analise: AnalisePergunta,
    cfg: RetrievalConfig | None = None,
    kb: KnowledgeBase | None = None,
) -> ResultadoRecuperacao:
    cfg = cfg or RetrievalConfig()
    kb = kb or get_kb(cfg.modelo_embedding)
    tempos: dict[str, float] = {}

    filtros = filtros_efetivos(analise, cfg)
    mascara = filtros.mask(kb.docs)
    n_universo = int(mascara.sum())
    consultas = consultas_de(analise, cfg, pergunta)
    vazio = ResultadoRecuperacao(filtros, consultas, pd.DataFrame(), pd.DataFrame(), 0, n_universo)
    if n_universo == 0:
        return vazio

    listas: list[list[tuple[str, float]]] = []
    melhor_denso: dict[str, float] = {}
    melhor_bm25: dict[str, float] = {}
    k = min(cfg.k_por_consulta, n_universo)

    t = time.perf_counter()
    if cfg.usar_denso:
        qv = kb.embedder.encode_queries(consultas)
        for lista in kb.store.query(qv, k=k, where=filtros.to_chroma_where()):
            listas.append(lista)
            for d, s in lista:
                melhor_denso[d] = max(s, melhor_denso.get(d, -1.0))
    tempos["denso_s"] = round(time.perf_counter() - t, 3)

    t = time.perf_counter()
    if cfg.usar_bm25:
        # A avaliação hipotética é texto "inventado": serve à busca semântica,
        # mas no BM25 só traria ruído lexical. Fica de fora da busca lexical.
        lexicais = [q for q in consultas if q != analise.avaliacao_hipotetica] or consultas
        for q in lexicais:
            lista = kb.bm25.search(q, k=k, mask=mascara)
            if lista:
                listas.append(lista)
            for d, s in lista:
                melhor_bm25[d] = max(s, melhor_bm25.get(d, 0.0))
    tempos["bm25_s"] = round(time.perf_counter() - t, 3)

    fundidos = rrf(listas, cfg.rrf_k)
    if not fundidos:
        return vazio
    ordem = sorted(fundidos, key=lambda d: -fundidos[d])[: cfg.n_rerank]
    cand = kb.docs.loc[ordem].reset_index(drop=True)
    cand["rrf"] = [fundidos[d] for d in ordem]
    cand["score_denso"] = [melhor_denso.get(d, np.nan) for d in ordem]
    cand["score_bm25"] = [melhor_bm25.get(d, np.nan) for d in ordem]
    cand["pos_rrf"] = np.arange(1, len(cand) + 1)

    t = time.perf_counter()
    if cfg.usar_rerank:
        textos = cand["texto"].tolist()
        if cfg.consulta_rerank == "pergunta" or not cfg.usar_reescrita:
            cand["relevancia"] = kb.reranker.score(pergunta, textos)
        elif cfg.consulta_rerank == "consulta_busca":
            cand["relevancia"] = kb.reranker.score(analise.consulta_busca, textos)
        else:
            # A avaliação hipotética (HyDE) não entra: é texto inventado, serve
            # para a busca vetorial, não como critério de relevância.
            qs = [q for q in consultas if q != analise.avaliacao_hipotetica] or consultas
            cand["relevancia"] = np.max([kb.reranker.score(q, textos) for q in qs], axis=0)
    else:
        # Sem reranker, a relevância é o cosseno denso (ou o RRF normalizado).
        if cfg.usar_denso:
            base = cand["score_denso"].fillna(0.0)
        else:
            base = cand["rrf"] / cand["rrf"].max()
        cand["relevancia"] = base.astype(np.float32)
    tempos["rerank_s"] = round(time.perf_counter() - t, 3)
    cand = cand.sort_values("relevancia", ascending=False, kind="stable").reset_index(drop=True)

    relevantes = cand[cand["relevancia"] >= cfg.limiar_relevancia]
    # Deduplicação: mesmo texto (ex.: "muito bom") de clientes diferentes entra
    # uma vez no contexto, com a contagem de repetições anotada.
    repeticoes = relevantes.groupby("texto_chave")["review_id"].transform("count")
    relevantes = relevantes.assign(repeticoes_no_topo=repeticoes.astype(int))
    unicos = relevantes.drop_duplicates("texto_chave")

    n_ctx = cfg.n_contexto_panorama if analise.tipo == "panorama" else cfg.n_contexto_tema
    if len(unicos):
        vet = kb.emb[kb.docs_pos.loc[unicos["review_id"]].to_numpy()]
        idx = mmr(
            unicos["review_id"].tolist(), unicos["relevancia"].to_numpy(), vet, n_ctx,
            cfg.mmr_lambda,
        )
        selecionados = unicos.iloc[sorted(idx, key=lambda i: -unicos["relevancia"].iloc[i])]
    else:
        selecionados = unicos
    selecionados = selecionados.reset_index(drop=True)

    return ResultadoRecuperacao(
        filtros_aplicados=filtros,
        consultas=consultas,
        candidatos=cand,
        selecionados=selecionados,
        n_relevantes=int(len(relevantes)),
        n_universo=n_universo,
        tempos=tempos,
    )


def config_dict(cfg: RetrievalConfig) -> dict:
    return asdict(cfg)
