"""Índice lexical BM25 (bm25s) sobre os documentos tokenizados.

Complementa a busca densa: termos exatos e raros ("nota fiscal", "correios",
"lacrado", nomes de produto) às vezes se perdem no vetor semântico e o BM25
os recupera com precisão.
"""
from __future__ import annotations

import json
from pathlib import Path

import bm25s
import numpy as np
import pandas as pd

from voc_rag.config import INDEX_DIR
from voc_rag.indexing.tokenize import tokenize

BM25_DIR = INDEX_DIR / "bm25"


class BM25Index:
    def __init__(self, retriever: bm25s.BM25, doc_ids: list[str]):
        self.retriever = retriever
        self.doc_ids = doc_ids
        self._vocab = retriever.vocab_dict

    @classmethod
    def build(cls, docs: pd.DataFrame) -> BM25Index:
        corpus = [tokenize(t) for t in docs["texto"]]
        retriever = bm25s.BM25()
        retriever.index(corpus, show_progress=False)
        return cls(retriever, docs["review_id"].tolist())

    def save(self, path: Path = BM25_DIR) -> None:
        path.mkdir(parents=True, exist_ok=True)
        self.retriever.save(str(path))
        (path / "doc_ids.json").write_text(json.dumps(self.doc_ids), encoding="utf-8")

    @classmethod
    def load(cls, path: Path = BM25_DIR) -> BM25Index:
        retriever = bm25s.BM25.load(str(path))
        doc_ids = json.loads((path / "doc_ids.json").read_text(encoding="utf-8"))
        return cls(retriever, doc_ids)

    def scores(self, query: str) -> np.ndarray:
        """Score BM25 da consulta contra TODOS os documentos (ordem de doc_ids)."""
        tokens = [t for t in tokenize(query) if t in self._vocab]
        if not tokens:
            return np.zeros(len(self.doc_ids), dtype=np.float32)
        return np.asarray(self.retriever.get_scores(tokens), dtype=np.float32)

    def search(
        self, query: str, k: int, mask: np.ndarray | None = None
    ) -> list[tuple[str, float]]:
        s = self.scores(query)
        if mask is not None:
            s = np.where(mask, s, 0.0)
        positivos = np.flatnonzero(s > 0)
        if positivos.size == 0:
            return []
        k = min(k, positivos.size)
        top = positivos[np.argsort(-s[positivos], kind="stable")[:k]]
        return [(self.doc_ids[i], float(s[i])) for i in top]
