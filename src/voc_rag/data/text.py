"""Limpeza e normalização de texto das avaliações.

Duas representações convivem no projeto:
  * `clean_text`: texto limpo mas FIEL ao original (acentos, caixa, pontuação).
    É o que vai para o modelo de embeddings, para o LLM e para a tela: o
    cliente precisa ser citado como escreveu.
  * `normalize_key`: forma agressiva (minúsculas, sem acento, sem pontuação),
    usada só como chave de deduplicação e de comparação.
"""
from __future__ import annotations

import html
import math
import re
import unicodedata

_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_WS = re.compile(r"\s+")
_LETRA = re.compile(r"[^\W\d_]", re.UNICODE)
_NAO_ALNUM = re.compile(r"[^0-9a-z ]+")


def is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    try:
        import pandas as pd

        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def clean_text(value: object) -> str | None:
    """Limpa um campo de texto livre. Devolve None se não sobrar conteúdo útil.

    Conteúdo útil = ao menos uma letra. Comentários como ".", "..." ou "0"
    viram ausentes: não carregam opinião e só poluiriam a recuperação.
    """
    if is_missing(value):
        return None
    s = html.unescape(str(value))
    s = unicodedata.normalize("NFC", s)
    s = _CTRL.sub(" ", s)
    s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    s = _WS.sub(" ", s).strip()
    if not _LETRA.search(s):
        return None
    return s


def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_key(s: str) -> str:
    """Chave de comparação: minúsculas, sem acento, sem pontuação."""
    s = strip_accents(s.lower())
    s = _NAO_ALNUM.sub(" ", s)
    return _WS.sub(" ", s).strip()


def compose_document(titulo: str | None, mensagem: str | None) -> str | None:
    """Junta título e mensagem num único texto de documento.

    O título é curto e muitas vezes repete a mensagem ("Recomendo" /
    "recomendo"); só entra quando acrescenta informação.
    """
    # pandas devolve NaN (float) onde clean_text devolveu None.
    titulo = None if is_missing(titulo) else titulo
    mensagem = None if is_missing(mensagem) else mensagem
    if not mensagem and not titulo:
        return None
    if not titulo:
        return mensagem
    if not mensagem:
        return titulo
    if normalize_key(titulo) in normalize_key(mensagem):
        return mensagem
    sep = " " if titulo.rstrip()[-1:] in ".!?" else ". "
    return f"{titulo.rstrip()}{sep}{mensagem}"


def count_words(s: str | None) -> int:
    if is_missing(s) or not s:
        return 0
    return len(normalize_key(s).split())
