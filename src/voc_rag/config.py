"""Caminhos e configurações do projeto (lidos do .env quando existirem)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

# Windows sem modo desenvolvedor não cria symlinks no cache do Hugging Face;
# o cache funciona mesmo assim, o aviso só polui a saída.
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")  # modelos públicos dispensam HF_TOKEN
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
INDEX_DIR = ROOT / "index"
REPORTS_DIR = ROOT / "reports"
IMAGES_DIR = ROOT / "images"
EVAL_DIR = ROOT / "eval"
CACHE_DIR = ROOT / ".cache"

# Todas as avaliações (com e sem comentário), uma linha por review_id.
REVIEWS_PARQUET = PROCESSED_DIR / "reviews.parquet"
# Documentos da base de conhecimento (apenas avaliações com texto útil).
DOCUMENTS_PARQUET = PROCESSED_DIR / "documents.parquet"

SEED = 42


@dataclass(frozen=True)
class Settings:
    llm_model: str
    judge_model: str
    embedding_model: str
    reranker_model: str
    device: str
    gemini_api_key: str | None


def _device() -> str:
    pedido = os.getenv("VOC_DEVICE", "auto").lower()
    if pedido != "auto":
        return pedido
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        llm_model=os.getenv("VOC_LLM_MODEL", "gemini-3.5-flash-lite"),
        judge_model=os.getenv("VOC_JUDGE_MODEL", "gemini-3.6-flash"),
        embedding_model=os.getenv("VOC_EMBEDDING_MODEL", "BAAI/bge-m3"),
        reranker_model=os.getenv("VOC_RERANKER_MODEL", "BAAI/bge-reranker-v2-m3"),
        device=_device(),
        gemini_api_key=os.getenv("GEMINI_API_KEY") or None,
    )
