"""Artefatos prontos publicados como asset de release.

Reproduzir do zero exige baixar a base do Kaggle (`voc prepare`) e calcular 42 mil embeddings
bge-m3 (`voc build`), o que leva minutos numa GPU e horas na CPU. O pacote leva:

* `data/processed/*.parquet`: base de conhecimento e rótulos de aspecto;
* `index/chroma/` (só a coleção bge-m3) e `index/bm25/`: o índice exatamente como foi
  avaliado. Ele vai pronto, e não reconstruído, porque o grafo HNSW do ChromaDB não é
  determinístico: um `voc build` novo devolve vizinhos ligeiramente diferentes, muda a
  seleção de evidências e, com ela, a chave do cache do LLM;
* `index/embeddings/baai-bge-m3.*`: embeddings já calculados, para quem quiser reconstruir;
* `.cache/llm/`: respostas do Gemini da avaliação e da demo; repetir essas perguntas não gasta
  cota nem exige chave.
"""
from __future__ import annotations

import logging
import shutil
import sqlite3
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

from voc_rag.config import CACHE_DIR, INDEX_DIR, PROCESSED_DIR, ROOT, get_settings

log = logging.getLogger(__name__)

URL_PADRAO = ("https://github.com/LucaOliveiraPrado/tech-challenge-fase4/releases/download/"
              "artefatos-v2/artefatos.zip")
PREFIXOS = ("data/processed/", "index/embeddings/baai-bge-m3.", "index/chroma/", "index/bm25/",
            "index/manifest.json", ".cache/llm/")


def _chroma_enxuto(tmp: Path) -> tuple[Path, set[str]]:
    """Cópia do ChromaDB só com a coleção do modelo do sistema (as dos modelos da comparação
    de embeddings triplicariam o pacote)."""
    import chromadb

    from voc_rag.indexing.vector_store import collection_name

    destino = tmp / "chroma"
    shutil.copytree(INDEX_DIR / "chroma", destino)
    manter = collection_name(get_settings().embedding_model)
    cliente = chromadb.PersistentClient(str(destino))
    for c in cliente.list_collections():
        if c.name != manter:
            cliente.delete_collection(c.name)
    # No Windows o cliente segura o sqlite aberto; sem isso a cópia não pode ser apagada.
    from chromadb.api.client import SharedSystemClient

    SharedSystemClient.clear_system_cache()
    del cliente
    con = sqlite3.connect(destino / "chroma.sqlite3")
    usados = {r[0] for r in con.execute("select id from segments")}
    con.execute("vacuum")
    con.close()
    # Segmentos de coleções apagadas ficam na cópia (o Windows pode segurá-los abertos) e
    # simplesmente não entram no pacote.
    return destino, usados


def empacota(destino: Path) -> dict:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        chroma, usados = _chroma_enxuto(Path(tmp))
        itens = [(p, p.relative_to(ROOT).as_posix())
                 for p in sorted(PROCESSED_DIR.glob("*.parquet"))]
        itens += [(p, p.relative_to(ROOT).as_posix())
                  for p in sorted((INDEX_DIR / "embeddings").glob("baai-bge-m3.*"))]
        itens += [(p, f"index/chroma/{p.relative_to(chroma).as_posix()}")
                  for p in sorted(chroma.rglob("*"))
                  if p.is_file() and (p.parent == chroma or p.parent.name in usados)]
        itens += [(p, p.relative_to(ROOT).as_posix())
                  for p in sorted((INDEX_DIR / "bm25").glob("*"))]
        itens.append((INDEX_DIR / "manifest.json", "index/manifest.json"))
        itens += [(p, p.relative_to(ROOT).as_posix())
                  for p in sorted((CACHE_DIR / "llm").rglob("*.json"))]
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
            for p, nome in itens:
                z.write(p, nome)
    return {"arquivo": str(destino), "arquivos": len(itens),
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
    return {"extraidos": extraidos,
            "proximo_passo": "índice pronto; não rode `voc build` (reconstruir muda o índice)"}
