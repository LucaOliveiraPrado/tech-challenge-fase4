"""Escopo decidido em código a partir das respostas objetivas da análise."""
import pytest

from voc_rag.retrieval.query import AnalisePergunta, decide_escopo


def _a(escopo, experiencia, posterior=False, manipula=False) -> AnalisePergunta:
    return AnalisePergunta(experiencia_de_compra=experiencia, posterior_a_2018=posterior,
                           tenta_manipular=manipula, escopo=escopo, motivo_escopo="x",
                           tipo="tema", polaridade="qualquer", consulta_busca="x")


@pytest.mark.parametrize(("escopo", "experiencia", "posterior", "manipula", "esperado"), [
    ("fora", True, False, False, "dentro"),   # drone, criptomoeda: quem decide é a recuperação
    ("fora", False, False, False, "fora"),    # faturamento, capital da Austrália
    ("dentro", True, True, False, "fora"),    # iPhone 15
    ("dentro", True, False, True, "fora"),    # prompt injection
    ("dentro", False, False, False, "fora"),  # o campo livre do LLM não decide
])
def test_decide_escopo(escopo, experiencia, posterior, manipula, esperado):
    assert decide_escopo(_a(escopo, experiencia, posterior, manipula)).escopo == esperado


def test_motivo_inventado_nao_sobrevive_quando_vira_dentro():
    a = decide_escopo(_a("fora", True))
    assert a.motivo_escopo.startswith("regra:") and "recuperação" in a.motivo_escopo


def test_motivo_do_llm_fica_quando_a_regra_concorda():
    assert decide_escopo(_a("fora", False)).motivo_escopo == "x"
