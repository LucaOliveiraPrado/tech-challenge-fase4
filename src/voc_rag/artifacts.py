"""Artefatos prontos publicados como asset de release.

Reproduzir do zero exige baixar a base do Kaggle (`voc prepare`) e calcular 42 mil embeddings
bge-m3 (`voc build`), o que leva minutos numa GPU e horas na CPU. O pacote leva:

* `data/processed/*.parquet`: base de conhecimento e rótulos de aspecto;
* `index/embeddings/baai-bge-m3.*`: embeddings já calculados; com eles o `voc build` só
  monta o Chroma e o BM25 (cerca de um minuto, sem GPU);
* `.cache/llm/`: respostas do Gemini da avaliação e da demo; repetir essas perguntas não gasta
  cota nem exige chave.
"""
from __future__ import annotations

import logging
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

from voc_rag.config import CACHE_DIR, INDEX_DIR, PROCESSED_DIR, ROOT

log = logging.getLogger(__name__)

URL_PADRAO = ("https://github.com/LucaOliveiraPrado/tech-challenge-fase4/releases/download/"
              "artefatos-v1/artefatos.zip")
PREFIXOS = ("data/processed/", "index/embeddings/baai-bge-m3.", ".cache/llm/")


def _arquivos() -> list[Path]:
    arqs = sorted(PROCESSED_DIR.glob("*.parquet"))
    arqs += sorted((INDEX_DIR / "embeddings").glob("baai-bge-m3.*"))
    arqs += sorted(p for p in (CACHE_DIR / "llm").rglob("*.json"))
    return arqs


def empacota(destino: Path) -> dict:
    arqs = _arquivos()
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for p in arqs:
            z.write(p, p.relative_to(ROOT).as_posix())
    return {"arquivo": str(destino), "arquivos": len(arqs),
            "mb": round(destino.stat().st_size / 2**20, 1)}


def _baixa(url: str, destino: Path) -> None:
    log.info("baixando %s", url)
    with urllib.request.urlopen(url) as r, destino.open("wb") as f:
        while bloco := r.read(1 << 20):
            f.write(bloco)


def extrai(zip_path: Path | None, url: str = URL_PADRAO) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        if zip_path is None:
            zip_path = Path(tmp) / "artefatos.zip"
            _baixa(url, zip_path)
        extraidos = 0
        with zipfile.ZipFile(zip_path) as z:
            for nome in z.namelist():
                caminho = PurePosixPath(nome)
                # Só caminhos esperados: o zip é dado externo, não pode escrever fora deles.
                if ".." in caminho.parts or not nome.startswith(PREFIXOS):
                    log.warning("ignorado: %s", nome)
                    continue
                alvo = ROOT / caminho
                alvo.parent.mkdir(parents=True, exist_ok=True)
                alvo.write_bytes(z.read(nome))
                extraidos += 1
    return {"extraidos": extraidos, "proximo_passo": "uv run voc build"}
