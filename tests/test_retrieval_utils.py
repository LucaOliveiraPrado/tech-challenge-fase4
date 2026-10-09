import numpy as np

from voc_rag.retrieval.filters import Filtros
from voc_rag.retrieval.query import AnalisePergunta, sanitiza
from voc_rag.retrieval.retriever import RetrievalConfig, consultas_de, filtros_efetivos, mmr, rrf


def _analise(**kw) -> AnalisePergunta:
    base = dict(escopo="dentro", motivo_escopo="", tipo="tema", polaridade="qualquer",
                consulta_busca="atraso na entrega")
    base.update(kw)
    return AnalisePergunta(**base)


def test_rrf_premia_consenso_entre_listas():
    a = [("x", 0.9), ("y", 0.8), ("z", 0.7)]
    b = [("y", 12.0), ("w", 9.0)]
    s = rrf([a, b], k=60)
    assert max(s, key=s.get) == "y"
    assert set(s) == {"x", "y", "z", "w"}


def test_mmr_evita_redundancia():
    v = np.array([[1, 0], [0.99, 0.141], [0, 1]], dtype=np.float32)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    rel = np.array([0.9, 0.89, 0.6])
    escolhidos = mmr(["a", "b", "c"], rel, v, n=2, lam=0.5)
    assert escolhidos == [0, 2]


def test_polaridade_vira_filtro_implicito_de_nota():
    cfg = RetrievalConfig()
    assert filtros_efetivos(_analise(polaridade="negativa"), cfg).nota_max == 3
    assert filtros_efetivos(_analise(polaridade="positiva"), cfg).nota_min == 4
    assert filtros_efetivos(_analise(), cfg).vazio()


def test_filtro_explicito_de_nota_prevalece_sobre_polaridade():
    a = _analise(polaridade="negativa", filtros=Filtros(nota_min=1, nota_max=1))
    f = filtros_efetivos(a, RetrievalConfig())
    assert (f.nota_min, f.nota_max) == (1, 1)


def test_ablacao_desliga_filtros():
    a = _analise(polaridade="negativa", filtros=Filtros(categorias=["moveis"]))
    cfg = RetrievalConfig(usar_filtros=False, usar_polaridade=False)
    assert filtros_efetivos(a, cfg).vazio()


def test_consultas_deduplicadas_e_hyde_opcional():
    a = _analise(consultas_alternativas=["Atraso na entrega", "demorou a chegar"],
                 avaliacao_hipotetica="comprei e até hoje não chegou")
    assert consultas_de(a, RetrievalConfig()) == [
        "atraso na entrega", "demorou a chegar", "comprei e até hoje não chegou"]
    assert consultas_de(a, RetrievalConfig(usar_hyde=False, usar_alternativas=False)) == [
        "atraso na entrega"]
    cru = RetrievalConfig(usar_reescrita=False)
    assert consultas_de(a, cru, "Quais os problemas de entrega?") == [
        "Quais os problemas de entrega?"]


def test_sanitiza_remove_categoria_inexistente_e_periodo_invalido():
    a = _analise(filtros=Filtros(categorias=["moveis", "inventada"], ano_mes_inicio=202301,
                                 nota_min=4, nota_max=2, ufs=["sp", "Sao Paulo"]))
    s = sanitiza(a, ["moveis", "beleza"])
    assert s.filtros.categorias == ["moveis"]
    assert s.filtros.ano_mes_inicio is None
    assert (s.filtros.nota_min, s.filtros.nota_max) == (2, 4)
    assert s.filtros.ufs == ["SP"]
