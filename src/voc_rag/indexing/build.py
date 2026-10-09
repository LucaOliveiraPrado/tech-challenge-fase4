"""Construção dos índices: embeddings (cache .npy), coleção Chroma e BM25."""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime

import numpy as np

from voc_rag.config import INDEX_DIR, get_settings
from voc_rag.data.prepare import load_documents
from voc_rag.indexing.bm25_index import BM25Index
from voc_rag.indexing.embeddings import EMB_DIR, embeddings_path, get_embedder
from voc_rag.indexing.vector_store import VectorStore

log = logging.getLogger(__name__)


def build_embeddings(model_name: str, force: bool = False) -> tuple[np.ndarray, float]:
    docs = load_documents()
    ids = docs["review_id"].tolist()
    p = embeddings_path(model_name)
    ids_path = p.with_suffix(".ids.json")
    if p.exists() and ids_path.exists() and not force:
        if json.loads(ids_path.read_text(encoding="utf-8")) == ids:
            return np.load(p), 0.0
    t = time.perf_counter()
    emb = get_embedder(model_name).encode_documents(docs["texto"].tolist())
    seg = time.perf_counter() - t
    EMB_DIR.mkdir(parents=True, exist_ok=True)
    np.save(p, emb)
    ids_path.write_text(json.dumps(ids), encoding="utf-8")
    return emb, seg


def build(models: list[str] | None = None, force: bool = False) -> dict:
    models = models or [get_settings().embedding_model]
    docs = load_documents()
    anterior = INDEX_DIR / "manifest.json"
    modelos_anteriores = {}
    if anterior.exists():
        antigo = json.loads(anterior.read_text(encoding="utf-8"))
        if antigo.get("documentos") == len(docs):
            modelos_anteriores = antigo.get("modelos", {})
    manifest: dict = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "documentos": int(len(docs)),
        "dispositivo": get_settings().device,
        "modelos": modelos_anteriores,
    }
    for m in models:
        emb, seg_emb = build_embeddings(m, force)
        t = time.perf_counter()
        VectorStore(m).build(docs, emb)
        manifest["modelos"][m] = {
            "dimensao": int(emb.shape[1]),
            "segundos_embeddings": round(seg_emb, 1),
            "segundos_indexacao": round(time.perf_counter() - t, 1),
        }
        log.info("modelo %s indexado", m)

    t = time.perf_counter()
    BM25Index.build(docs).save()
    manifest["bm25_segundos"] = round(time.perf_counter() - t, 1)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    (INDEX_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest
