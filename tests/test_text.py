import math

from voc_rag.data.text import clean_text, compose_document, count_words, normalize_key
from voc_rag.indexing.tokenize import tokenize


def test_clean_text_normaliza_espacos_e_quebras():
    assert clean_text("  Chegou\r\nrápido!\t\tAdorei  ") == "Chegou rápido! Adorei"


def test_clean_text_descarta_sem_letras():
    for v in (None, math.nan, "", "   ", ".", "...", "0", "!!!"):
        assert clean_text(v) is None


def test_clean_text_preserva_acentos_e_caixa():
    assert clean_text("Não RECEBI o produto") == "Não RECEBI o produto"


def test_compose_document_ignora_titulo_redundante():
    assert compose_document("recomendo", "Recomendo, ótimo!") == "Recomendo, ótimo!"


def test_compose_document_junta_titulo_util():
    assert compose_document("Atrasou", "Mas o produto é bom") == "Atrasou. Mas o produto é bom"
    assert compose_document("Atrasou!", "Mas é bom") == "Atrasou! Mas é bom"


def test_compose_document_so_um_campo():
    assert compose_document(None, "texto") == "texto"
    assert compose_document("titulo", None) == "titulo"
    assert compose_document(None, None) is None


def test_normalize_key():
    assert normalize_key("Muito BOM!!!") == normalize_key("muito bom")
    assert normalize_key("Não chegou") == "nao chegou"


def test_count_words():
    assert count_words("Produto ótimo, chegou antes do prazo.") == 6
    assert count_words(None) == 0


def test_tokenize_preserva_negacao_e_junta_flexoes():
    t = tokenize("Não chegou! A entrega atrasou")
    assert "nao" in t
    assert tokenize("entrega")[0] == tokenize("entregue")[0][: len(tokenize("entrega")[0])]
    assert tokenize("atrasou") == tokenize("atraso")


def test_tokenize_sem_acento_equivale():
    assert tokenize("não recebi") == tokenize("nao recebi")
