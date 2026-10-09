"""Reranker cross-encoder.

A busca vetorial compara vetores calculados SEPARADAMENTE para pergunta e
documento (bi-encoder): rápida, mas grosseira. O cross-encoder lê o par
(pergunta, avaliação) junto e devolve uma relevância calibrada em [0, 1].
É caro demais para 40 mil documentos, mas barato para os ~80 candidatos que a
busca híbrida entrega, e o score dele é o que decide o limiar de abstenção.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np

from voc_rag.config import get_settings


class Reranker:
    def __init__(self, model_name: str | None = None, device: str | None = None):
        import torch
        from sentence_transformers import CrossEncoder

        cfg = get_settings()
        self.model_name = model_name or cfg.reranker_model
        device = device or cfg.device
        kwargs = {"model_kwargs": {"torch_dtype": torch.float16}} if device == "cuda" else {}
        self.model = CrossEncoder(self.model_name, device=device, max_length=320, **kwargs)
        self._sigmoid = torch.nn.Sigmoid()

    def score(self, query: str, texts: list[str], batch_size: int = 32) -> np.ndarray:
        if not texts:
            return np.zeros(0, dtype=np.float32)
        pares = [(query, t) for t in texts]
        s = self.model.predict(
            pares,
            batch_size=batch_size,
            activation_fn=self._sigmoid,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.asarray(s, dtype=np.float32)


@lru_cache(maxsize=2)
def get_reranker(model_name: str | None = None) -> Reranker:
    return Reranker(model_name)
