"""Filtros por metadado (desafio adicional).

Um único objeto de filtro gera as duas representações usadas na recuperação:
a cláusula `where` do Chroma (busca densa) e uma máscara booleana sobre o
DataFrame de documentos (busca lexical e estatísticas). Os testes garantem que
as duas selecionam exatamente o mesmo conjunto.
"""
from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

Sentimento = Literal["negativo", "neutro", "positivo"]
EntregaStatus = Literal["no_prazo", "atrasado", "nao_entregue", "cancelado"]

ROTULO_ENTREGA = {
    "no_prazo": "entregue no prazo",
    "atrasado": "entregue com atraso",
    "nao_entregue": "não entregue até a avaliação",
    "cancelado": "pedido cancelado",
}


class Filtros(BaseModel):
    nota_min: int | None = Field(default=None, ge=1, le=5)
    nota_max: int | None = Field(default=None, ge=1, le=5)
    sentimentos: list[Sentimento] = Field(default_factory=list)
    categorias: list[str] = Field(default_factory=list)
    entrega_status: list[EntregaStatus] = Field(default_factory=list)
    ano_mes_inicio: int | None = Field(default=None, description="AAAAMM inclusivo")
    ano_mes_fim: int | None = Field(default=None, description="AAAAMM inclusivo")
    ufs: list[str] = Field(default_factory=list)
    regioes: list[str] = Field(default_factory=list)

    def vazio(self) -> bool:
        return not any(
            [
                self.nota_min, self.nota_max, self.sentimentos, self.categorias,
                self.entrega_status, self.ano_mes_inicio, self.ano_mes_fim,
                self.ufs, self.regioes,
            ]
        )

    # ------------------------------------------------------------------ Chroma
    def to_chroma_where(self) -> dict | None:
        conds: list[dict] = []
        if self.nota_min is not None:
            conds.append({"nota": {"$gte": self.nota_min}})
        if self.nota_max is not None:
            conds.append({"nota": {"$lte": self.nota_max}})
        if self.ano_mes_inicio is not None:
            conds.append({"ano_mes": {"$gte": self.ano_mes_inicio}})
        if self.ano_mes_fim is not None:
            conds.append({"ano_mes": {"$lte": self.ano_mes_fim}})
        for campo, valores in (
            ("sentimento", self.sentimentos),
            ("categoria", self.categorias),
            ("entrega_status", self.entrega_status),
            ("uf", self.ufs),
            ("regiao", self.regioes),
        ):
            if valores:
                conds.append({campo: {"$in": list(valores)}})
        if not conds:
            return None
        if len(conds) == 1:
            return conds[0]
        return {"$and": conds}

    # ---------------------------------------------------------------- pandas
    def mask(self, df: pd.DataFrame) -> np.ndarray:
        m = np.ones(len(df), dtype=bool)
        if self.nota_min is not None:
            m &= (df["nota"] >= self.nota_min).to_numpy()
        if self.nota_max is not None:
            m &= (df["nota"] <= self.nota_max).to_numpy()
        if self.ano_mes_inicio is not None:
            m &= (df["ano_mes"] >= self.ano_mes_inicio).fillna(False).to_numpy(dtype=bool)
        if self.ano_mes_fim is not None:
            m &= (df["ano_mes"] <= self.ano_mes_fim).fillna(False).to_numpy(dtype=bool)
        for campo, valores in (
            ("sentimento", self.sentimentos),
            ("categoria", self.categorias),
            ("entrega_status", self.entrega_status),
            ("uf", self.ufs),
            ("regiao", self.regioes),
        ):
            if valores:
                m &= df[campo].isin(valores).to_numpy()
        return m

    # ------------------------------------------------------------- descrição
    def descricao(self) -> str:
        partes = []
        if self.nota_min is not None or self.nota_max is not None:
            lo, hi = self.nota_min or 1, self.nota_max or 5
            partes.append(f"nota {lo}" if lo == hi else f"nota de {lo} a {hi}")
        if self.sentimentos:
            partes.append("sentimento " + "/".join(self.sentimentos))
        if self.categorias:
            partes.append("categoria " + ", ".join(self.categorias))
        if self.entrega_status:
            partes.append(", ".join(ROTULO_ENTREGA[s] for s in self.entrega_status))
        if self.ano_mes_inicio or self.ano_mes_fim:
            ini = _fmt_ano_mes(self.ano_mes_inicio) if self.ano_mes_inicio else "início"
            fim = _fmt_ano_mes(self.ano_mes_fim) if self.ano_mes_fim else "fim"
            partes.append(f"compras de {ini} a {fim}")
        if self.ufs:
            partes.append("UF " + ", ".join(self.ufs))
        if self.regioes:
            partes.append("região " + ", ".join(self.regioes))
        return "; ".join(partes) if partes else "sem filtros"


def _fmt_ano_mes(v: int) -> str:
    return f"{v % 100:02d}/{v // 100}"
