from voc_rag.generation.answer import Insight, RespostaGerada, ids_citados, valida_citacoes


def _resp(insights, resumo="Resumo [R1].") -> RespostaGerada:
    return RespostaGerada(suficiente=True, resumo=resumo, insights=insights, limitacoes="")


def test_citacao_inexistente_e_removida_do_texto():
    r = _resp([Insight(titulo="Atraso", descricao="Clientes relatam atraso [R1][R9].",
                       evidencias=["R1", "R9"])])
    limpa, rel = valida_citacoes(r, {"R1", "R2"})
    assert limpa.insights[0].evidencias == ["R1"]
    assert "[R9]" not in limpa.insights[0].descricao
    assert rel.citacoes_invalidas == 1 and rel.ids_invalidos == ["R9"]


def test_insight_sem_evidencia_valida_e_descartado():
    r = _resp([
        Insight(titulo="Ok", descricao="Bom [R2].", evidencias=["R2"]),
        Insight(titulo="Inventado", descricao="Sem suporte [R7].", evidencias=["R7"]),
        Insight(titulo="Sem marca", descricao="Nada citado.", evidencias=[]),
    ])
    limpa, rel = valida_citacoes(r, {"R1", "R2"})
    assert [i.titulo for i in limpa.insights] == ["Ok"]
    assert rel.insights_descartados == 2


def test_evidencia_so_no_texto_e_recuperada():
    r = _resp([Insight(titulo="T", descricao="Veio quebrado [R3].", evidencias=[])])
    limpa, _ = valida_citacoes(r, {"R3"})
    assert limpa.insights[0].evidencias == ["R3"]


def test_citacoes_agrupadas_sao_validadas_e_normalizadas():
    r = _resp([Insight(titulo="T", descricao="Atrasos [R1, R9; R2] e mais [R3,R4].",
                       evidencias=[])], resumo="Resumo [R2, R7].")
    limpa, rel = valida_citacoes(r, {"R1", "R2", "R3"})
    assert limpa.insights[0].descricao == "Atrasos [R1][R2] e mais [R3]."
    assert limpa.insights[0].evidencias == ["R1", "R2", "R3"]
    assert limpa.resumo == "Resumo [R2]."
    assert rel.citacoes_total == 7 and sorted(rel.ids_invalidos) == ["R4", "R7", "R9"]


def test_ids_citados_ordenados():
    r = _resp([Insight(titulo="a", descricao="x [R10]", evidencias=["R10", "R2"])],
              resumo="[R1] e [R2]")
    assert ids_citados(r) == ["R1", "R2", "R10"]
