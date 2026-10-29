"""Extração dos artefatos de release: só grava nos caminhos esperados."""
import zipfile

from voc_rag import artifacts


def test_extrai_ignora_caminhos_fora_do_esperado(tmp_path, monkeypatch):
    raiz = tmp_path / "projeto"
    monkeypatch.setattr(artifacts, "ROOT", raiz)
    zp = tmp_path / "artefatos.zip"
    with zipfile.ZipFile(zp, "w") as z:
        z.writestr("data/processed/documents.parquet", b"ok")
        z.writestr("index/embeddings/baai-bge-m3.npy", b"ok")
        z.writestr(".cache/llm/ab/abc.json", b"{}")
        z.writestr("data/processed/../../fora.txt", b"x")
        z.writestr("src/voc_rag/config.py", b"x")
        z.writestr("index/embeddings/outro-modelo.npy", b"x")

    r = artifacts.extrai(zp)

    assert r["extraidos"] == 3
    assert (raiz / "data/processed/documents.parquet").read_bytes() == b"ok"
    assert (raiz / ".cache/llm/ab/abc.json").exists()
    assert not (tmp_path / "fora.txt").exists()
    assert not (raiz / "src").exists()
    assert not (raiz / "index/embeddings/outro-modelo.npy").exists()
