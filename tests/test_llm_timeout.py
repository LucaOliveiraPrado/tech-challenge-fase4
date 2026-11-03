"""Chamada sem resposta não pode travar a avaliação: repete e passa ao próximo modelo."""
from types import SimpleNamespace

import httpx

from voc_rag.generation import llm as modulo
from voc_rag.generation.llm import LLMClient


class _ClienteFalso:
    """Primeiro modelo nunca responde; o segundo responde na hora."""

    def __init__(self):
        self.chamados: list[str] = []
        self.models = SimpleNamespace(generate_content=self._gera)

    def _gera(self, model, contents, config):
        self.chamados.append(model)
        if model == "travado":
            raise httpx.ReadTimeout("sem resposta")
        return SimpleNamespace(text="ok", usage_metadata=None)


def test_timeout_passa_ao_proximo_modelo(tmp_path, monkeypatch):
    monkeypatch.setattr(modulo.time, "sleep", lambda _: None)
    cli = LLMClient(model="travado", fallbacks=["reserva"], cache_dir=tmp_path, usar_cache=False)
    cli._client = _ClienteFalso()
    texto, _, _, modelo = cli._chama("sistema", "prompt", None, 0.0, "baixo")
    assert (texto, modelo) == ("ok", "reserva")
    assert cli._client.chamados == ["travado"] * 3 + ["reserva"]
