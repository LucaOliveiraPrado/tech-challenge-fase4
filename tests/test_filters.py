import numpy as np
import pandas as pd
import pytest

from voc_rag.retrieval.filters import Filtros

DOCS = pd.DataFrame(
    {
        "review_id": list("abcdef"),
        "nota": [1, 2, 3, 4, 5, 1],
        "sentimento": ["negativo", "negativo", "neutro", "positivo", "positivo", "negativo"],
        "categoria": ["moveis", "beleza", "moveis", "beleza", "moveis", "telefonia"],
        "entrega_status": ["atrasado", "no_prazo", "atrasado", "no_prazo", "no_prazo",
                           "nao_entregue"],
        "ano_mes": pd.array([201701, 201706, 201712, 201801, 201806, None], dtype="Int64"),
        "uf": ["SP", "RJ", "SP", "MG", "BA", "SP"],
        "regiao": ["Sudeste", "Sudeste", "Sudeste", "Sudeste", "Nordeste", "Sudeste"],
        "pagamento": ["boleto", "credit_card", "boleto", "voucher", "credit_card", None],
        "valor_itens": [120.0, 600.0, 35.5, None, 900.0, 59.9],
        "n_vendedores": [1.0, 2.0, 1.0, None, 3.0, 1.0],
    }
)


def _avalia_where(where: dict | None, row: pd.Series) -> bool:
    """Interpretador mínimo da sintaxe where do Chroma, para comparar com a máscara."""
    if where is None:
        return True
    if "$and" in where:
        return all(_avalia_where(w, row) for w in where["$and"])
    ((campo, cond),) = where.items()
    ((op, val),) = cond.items()
    v = row[campo]
    if pd.isna(v):
        return False
    return {
        "$gte": lambda: v >= val,
        "$lte": lambda: v <= val,
        "$in": lambda: v in val,
    }[op]()


CASOS = [
    Filtros(),
    Filtros(nota_max=2),
    Filtros(nota_min=4),
    Filtros(nota_min=1, nota_max=1),
    Filtros(categorias=["moveis"]),
    Filtros(nota_max=3, entrega_status=["atrasado"]),
    Filtros(ano_mes_inicio=201706, ano_mes_fim=201801),
    Filtros(ufs=["SP"], sentimentos=["negativo"]),
    Filtros(regioes=["Nordeste"], nota_min=4),
    Filtros(pagamentos=["boleto"]),
    Filtros(valor_min=500),
    Filtros(valor_max=100, nota_max=2),
    Filtros(multi_vendedor=True),
    Filtros(multi_vendedor=False, pagamentos=["credit_card", "boleto"]),
]


@pytest.mark.parametrize("f", CASOS)
def test_mascara_e_where_selecionam_o_mesmo_conjunto(f: Filtros):
    mascara = f.mask(DOCS)
    where = f.to_chroma_where()
    esperado = np.array([_avalia_where(where, r) for _, r in DOCS.iterrows()])
    assert (mascara == esperado).all()


def test_vazio():
    assert Filtros().vazio()
    assert not Filtros(nota_max=2).vazio()
    assert Filtros().to_chroma_where() is None


def test_where_condicao_unica_sem_and():
    assert Filtros(nota_max=2).to_chroma_where() == {"nota": {"$lte": 2}}


def test_descricao_legivel():
    d = Filtros(nota_max=2, categorias=["moveis"], entrega_status=["atrasado"]).descricao()
    assert "nota de 1 a 2" in d and "moveis" in d and "atraso" in d
