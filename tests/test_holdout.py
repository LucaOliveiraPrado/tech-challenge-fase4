"""O conjunto retido precisa ser bem formado e não repetir as perguntas de desenvolvimento."""
import json

from voc_rag.config import EVAL_DIR
from voc_rag.retrieval.filters import Filtros


def _carrega(nome: str) -> list[dict]:
    return json.loads((EVAL_DIR / nome).read_text(encoding="utf-8"))


def test_retidas_nao_repetem_as_de_desenvolvimento():
    dev = {p["pergunta"].lower() for p in _carrega("perguntas.json")}
    assert not dev & {p["pergunta"].lower() for p in _carrega("perguntas_retidas.json")}


def test_retidas_bem_formadas():
    perguntas = _carrega("perguntas_retidas.json")
    assert len({p["id"] for p in perguntas}) == len(perguntas)
    for p in perguntas:
        assert p["esperado"] in ("responder", "abster")
        if p["esperado"] == "responder":
            assert p["criterio"].strip()
        if p.get("filtros_esperados"):
            assert not Filtros(**p["filtros_esperados"]).vazio()
