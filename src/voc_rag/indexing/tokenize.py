"""Tokenização para a busca lexical (BM25).

Escolhas para o português informal das avaliações:
  * acentos removidos ANTES do stemming: clientes escrevem "nao", "voce",
    "entrega rapida" sem acento com frequência;
  * stemming Snowball (português) junta flexões: entrega/entregue/entregou;
  * stopwords SEM negações nem restritivos: "não chegou" e "chegou" são
    opiniões opostas, e "só veio um" depende do "só".
"""
from __future__ import annotations

import re
from functools import lru_cache

import Stemmer

from voc_rag.data.text import strip_accents

_TOKEN = re.compile(r"[a-z0-9]+")

# Palavras mantidas de propósito (NÃO são stopwords aqui): nao, nunca, nem,
# nada, nenhum, nenhuma, sem, so, apenas, ainda, mal, falta, faltou.
STOPWORDS = frozenset(
    """
    a o as os um uma uns umas de do da dos das d em no na nos nas num numa
    por pelo pela pelos pelas para pra pro pros pras com e ou que se ao aos
    eu me mim meu minha meus minhas voce voces vc ele ela eles elas lhe lhes
    seu sua seus suas nosso nossa nossos nossas te ti tu
    este esta estes estas esse essa esses essas isso isto aquele aquela aquilo
    ser sou e era eram foi fui foram sera seria sendo sido
    estar estou esta estao estava estavam esteve estive
    ter tenho tem tinha tinham teve tive tido
    haver ha havia
    ja mas mais tambem ate como quando onde qual quais quem
    la aqui ai entao pois porque porem
    """.split()
)


@lru_cache(maxsize=1)
def _stemmer() -> Stemmer.Stemmer:
    return Stemmer.Stemmer("portuguese")


def tokenize(text: str) -> list[str]:
    tokens = _TOKEN.findall(strip_accents(text.lower()))
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return _stemmer().stemWords(tokens)
