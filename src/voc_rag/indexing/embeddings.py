"""Modelos de embedding locais (Hugging Face / sentence-transformers).

Rodar localmente (GPU quando houver) em vez de uma API de embeddings:
custo zero, sem limite de requisições para indexar ~40 mil documentos, e o
mesmo vetor é reproduzível por qualquer avaliador.
"""
from __future__ import annotations

import json
import logging
import re
from functools import lru_cache
from pathlib import Path

import numpy as np

from voc_rag.config import INDEX_DIR, get_settings

log = logging.getLogger(__name__)

EMB_DIR = INDEX_DIR / "embeddings"

# Modelos da família E5 foram treinados com prefixos assimétricos.
PREFIXOS: dict[str, tuple[str, str]] = {
    "intfloat/multilingual-e5-small": ("query: ", "passage: "),
    "intfloat/multilingual-e5-base": ("query: ", "passage: "),
    "intfloat/multilingual-e5-large": ("query: ", "passage: "),
}

# Avaliações são curtas; 256 tokens cobrem praticamente todas e poupam memória.
MAX_SEQ_LENGTH = 256


def slug(model_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", model_name.lower()).strip("-")


def embeddings_path(model_name: str) -> Path:
    """Matriz de embeddings dos documentos (cache .npy, alinhada a documents.parquet)."""
    return EMB_DIR / f"{slug(model_name)}.npy"


def load_embeddings(model_name: str, ids_esperados: list[str]) -> np.ndarray:
    p = embeddings_path(model_name)
    ids = json.loads(p.with_suffix(".ids.json").read_text(encoding="utf-8"))
    if ids != ids_esperados:
        raise RuntimeError(f"Embeddings de {model_name} desalinhados: rode `voc build`.")
    return np.load(p)


class Embedder:
    def __init__(self, model_name: str, device: str | None = None):
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self.device = device or get_settings().device
        kwargs = {}
        if self.device == "cuda":
            import torch

            kwargs["model_kwargs"] = {"torch_dtype": torch.float16}
        self.model = SentenceTransformer(model_name, device=self.device, **kwargs)
        self.model.max_seq_length = min(self.model.max_seq_length or MAX_SEQ_LENGTH, MAX_SEQ_LENGTH)
        self.query_prefix, self.doc_prefix = PREFIXOS.get(model_name, ("", ""))
        if hasattr(self.model, "get_embedding_dimension"):
            self.dim = self.model.get_embedding_dimension()
        else:
            self.dim = self.model.get_sentence_embedding_dimension()

    def _encode(self, texts: list[str], batch_size: int, progress: bool) -> np.ndarray:
        vecs = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=progress,
        )
        return vecs.astype(np.float32)

    def encode_documents(self, texts: list[str], batch_size: int = 128) -> np.ndarray:
        return self._encode([self.doc_prefix + t for t in texts], batch_size, progress=True)

    def encode_queries(self, texts: list[str]) -> np.ndarray:
        return self._encode([self.query_prefix + t for t in texts], 32, progress=False)


@lru_cache(maxsize=4)
def get_embedder(model_name: str | None = None) -> Embedder:
    return Embedder(model_name or get_settings().embedding_model)
