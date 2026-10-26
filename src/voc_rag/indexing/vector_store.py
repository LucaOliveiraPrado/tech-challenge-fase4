"""Banco vetorial: ChromaDB persistente em disco.

Por que Chroma: roda embutido (sem servidor), persiste em disco, faz busca
aproximada HNSW com distância de cosseno e aplica filtros de metadado na
própria consulta, que é o que o desafio adicional pede. Os vetores são
calculados por nós (embeddings.py) e entregues prontos, então o mesmo índice
serve a qualquer modelo comparado.
"""
from __future__ import annotations

import logging
import math
from pathlib import Path

import chromadb
import numpy as np
import pandas as pd
from chromadb.config import Settings as ChromaSettings

from voc_rag.config import INDEX_DIR
from voc_rag.indexing.embeddings import slug

log = logging.getLogger(__name__)

CHROMA_DIR = INDEX_DIR / "chroma"

# Campos de metadado gravados junto de cada vetor (todos escalares).
METADADOS = [
    "order_id", "nota", "sentimento", "ano", "mes", "ano_mes", "entrega_status",
    "atraso_dias", "tempo_entrega_dias", "categoria", "categoria_en", "uf",
    "regiao", "pagamento", "valor_itens", "n_vendedores", "n_palavras", "texto_repetido",
]


def _limpa_valor(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        return None if np.isnan(v) else float(v)
    if isinstance(v, np.bool_):
        return bool(v)
    if v is pd.NA or v is pd.NaT:
        return None
    return v


def doc_metadata(row: dict) -> dict:
    meta = {}
    for campo in METADADOS:
        v = _limpa_valor(row.get(campo))
        if v is not None:
            meta[campo] = v
    return meta


def collection_name(model_name: str) -> str:
    return f"avaliacoes-{slug(model_name)}"[:60]


class VectorStore:
    def __init__(self, model_name: str, path: Path = CHROMA_DIR):
        path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(path), settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.model_name = model_name
        self.name = collection_name(model_name)
        self._col = None

    @property
    def collection(self):
        if self._col is None:
            self._col = self.client.get_collection(self.name)
        return self._col

    def exists(self) -> bool:
        return self.name in [c.name for c in self.client.list_collections()]

    def build(self, docs: pd.DataFrame, embeddings: np.ndarray, batch: int = 4000) -> None:
        if len(docs) != len(embeddings):
            raise ValueError("docs e embeddings com tamanhos diferentes")
        if self.exists():
            self.client.delete_collection(self.name)
        self._col = self.client.create_collection(
            self.name,
            metadata={"hnsw:space": "cosine", "modelo": self.model_name},
        )
        registros = docs.to_dict("records")
        for i in range(0, len(docs), batch):
            fatia = registros[i : i + batch]
            self._col.add(
                ids=[r["review_id"] for r in fatia],
                embeddings=embeddings[i : i + batch],
                documents=[r["texto"] for r in fatia],
                metadatas=[doc_metadata(r) for r in fatia],
            )
        log.info("coleção %s: %s vetores", self.name, self._col.count())

    def query(
        self, query_vecs: np.ndarray, k: int, where: dict | None = None
    ) -> list[list[tuple[str, float]]]:
        """Devolve, para cada vetor de consulta, [(review_id, similaridade_cosseno)]."""
        res = self.collection.query(
            query_embeddings=query_vecs,
            n_results=k,
            where=where,
            include=["distances"],
        )
        saida = []
        for ids, dists in zip(res["ids"], res["distances"], strict=True):
            saida.append([(i, 1.0 - float(d)) for i, d in zip(ids, dists, strict=True)])
        return saida

    def count(self) -> int:
        return self.collection.count()
