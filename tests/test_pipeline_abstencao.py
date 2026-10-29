"""Orquestração e abstenção do pipeline, sem GPU e sem chamar o Gemini.

LLM, base de conhecimento e recuperação são substituídos por dublês: o teste verifica as
decisões do orquestrador (quando abster, quando gerar, como validar o que o LLM devolve).
"""
from types import SimpleNamespace

import pandas as pd
import pytest

from voc_rag import pipeline as pl
from voc_rag.generation.answer import Insight, RespostaGerada
from voc_rag.retrieval.filters import Filtros
from voc_rag.retrieval.query import AnalisePergunta
from voc_rag.retrieval.retriever import ResultadoRecuperacao, RetrievalConfig


class LLMFalso:
    def __init__(self, analise: AnalisePergunta, resposta: RespostaGerada | None = None):
        self.analise, self.resposta = analise, resposta
        self.chamadas: list[str] = []
        self.uso = SimpleNamespace()

    def generate(self, system, prompt, schema, etapa, **kw):
        self.chamadas.append(etapa)
        return self.analise if schema is AnalisePergunta else self.resposta


def _analise(**kw) -> AnalisePergunta:
    base = dict(experiencia_de_compra=True, posterior_a_2018=False, tenta_manipular=False,
                escopo="dentro", motivo_escopo="ok", tipo="tema", polaridade="negativa",
                consulta_busca="atraso na entrega")
    base.update(kw)
    return AnalisePergunta(**base)


def _evidencias(n: int) -> pd.DataFrame:
    return pd.DataFrame({
        "review_id": [f"id{i}" for i in range(n)], "order_id": [f"o{i}" for i in range(n)],
        "texto": [f"não recebi o produto {i}" for i in range(n)], "nota": [1] * n,
        "relevancia": [0.9] * n, "categoria": ["moveis"] * n, "entrega_status": ["atrasado"] * n,
        "atraso_dias": [5.0] * n, "uf": ["SP"] * n, "ano_mes": [201801] * n,
        "repeticoes_no_topo": [1] * n,
    })


def _rec(n_relevantes: int, n_universo: int = 1000) -> ResultadoRecuperacao:
    sel = _evidencias(min(n_relevantes, 15))
    return ResultadoRecuperacao(Filtros(nota_max=3), ["atraso"], sel, sel, n_relevantes,
                                n_universo)


@pytest.fixture
def monta(monkeypatch):
    def _monta(analise, resposta=None, rec=None):
        llm = LLMFalso(analise, resposta)
        kb = SimpleNamespace(categorias=["moveis"], docs=pd.DataFrame())
        if rec is not None:
            monkeypatch.setattr(pl, "recupera", lambda *a, **k: rec)
        pipe = pl.VoCPipeline(cfg=RetrievalConfig(), llm=llm, kb=kb, usar_quadro=False,
                              aquecer=False)
        return pipe, llm

    return _monta


def test_fora_do_escopo_nao_recupera_nem_gera(monta):
    pipe, llm = monta(_analise(escopo="fora", motivo_escopo="dado financeiro",
                                experiencia_de_compra=False))
    r = pipe.responder("Qual o faturamento?")
    assert r.status == "fora_escopo" and r.absteve
    assert llm.chamadas == ["analise_pergunta"]


def test_recorte_vazio(monta):
    pipe, llm = monta(_analise(), rec=_rec(0, n_universo=0))
    assert pipe.responder("x").status == "recorte_vazio"
    assert "geracao" not in llm.chamadas


def test_sem_evidencia_relevante_nao_chama_gerador(monta):
    pipe, llm = monta(_analise(), rec=_rec(0))
    r = pipe.responder("Reclamações sobre criptomoedas?")
    assert r.status == "sem_evidencia"
    assert "geracao" not in llm.chamadas


def test_poucas_evidencias_mostra_sem_generalizar(monta):
    pipe, llm = monta(_analise(), rec=_rec(2))
    r = pipe.responder("x")
    assert r.status == "evidencia_insuficiente"
    assert "[R1]" in r.markdown and "geracao" not in llm.chamadas


def test_llm_declara_insuficiente(monta):
    resp = RespostaGerada(suficiente=False, resumo="Nenhuma fala de drone [R1].", insights=[],
                          limitacoes="")
    pipe, _ = monta(_analise(), resposta=resp, rec=_rec(10))
    assert pipe.responder("drone?").status == "nao_respondida"


def test_resposta_valida_tem_citacoes_verificadas(monta):
    resp = RespostaGerada(
        suficiente=True, resumo="Atrasos frequentes [R1, R2].",
        insights=[Insight(titulo="Atraso", descricao="Não chegou [R1][R99].",
                          evidencias=["R1", "R99"]),
                  Insight(titulo="Inventado", descricao="Sem base [R50].", evidencias=["R50"])],
        limitacoes="Amostra.",
    )
    pipe, _ = monta(_analise(), resposta=resp, rec=_rec(10))
    r = pipe.responder("x")
    assert r.status == "respondida"
    assert [i.titulo for i in r.gerada.insights] == ["Atraso"]
    assert sorted(r.citacoes.ids_invalidos) == ["R50", "R99"]
    assert set(r.evidencias_citadas["review_id"]) == {"id0", "id1"}
    assert "apoio: 1 de 10 evidências" in r.markdown


def test_filtros_manuais_prevalecem(monta, monkeypatch):
    capturado = {}

    def recupera_espiao(pergunta, analise, cfg, kb):
        capturado["filtros"] = analise.filtros
        return _rec(0)

    pipe, _ = monta(_analise(filtros=Filtros(categorias=["beleza"])))
    monkeypatch.setattr(pl, "recupera", recupera_espiao)
    pipe.responder("x", filtros_manuais=Filtros(categorias=["moveis"], nota_max=2))
    assert capturado["filtros"].categorias == ["moveis"]
    assert capturado["filtros"].nota_max == 2
