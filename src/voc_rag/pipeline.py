"""Pipeline RAG ponta a ponta, com três camadas de abstenção.

  pergunta
    │ 1. análise da pergunta (LLM): escopo, tipo, polaridade, filtros, reescrita
    ├── fora do escopo ─────────────────────────────► abstém (sem recuperar)
    │ 2. recuperação híbrida + reranker + seleção
    ├── recorte vazio / nenhuma evidência relevante ─► abstém
    ├── poucas evidências relevantes ────────────────► mostra evidências, sem generalizar
    │ 3. quadro de frequências (perguntas de panorama)
    │ 4. geração (LLM) com contexto numerado
    ├── LLM declara evidência insuficiente ──────────► abstém
    │ 5. validação das citações (código)
    ▼
  resposta + insights + evidências rastreáveis (review_id)
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import pandas as pd

from voc_rag.generation.answer import (
    REFORCO_ACENTOS,
    RelatorioCitacoes,
    RespostaGerada,
    ids_citados,
    monta_contexto,
    monta_prompt,
    rotula_evidencias,
    sem_acentos,
    valida_citacoes,
)
from voc_rag.generation.answer import (
    SYSTEM as SYSTEM_RESPOSTA,
)
from voc_rag.generation.llm import LLMClient, LLMIndisponivel
from voc_rag.retrieval.filters import Filtros
from voc_rag.retrieval.query import AnalisePergunta, analisa_pergunta
from voc_rag.retrieval.retriever import (
    KnowledgeBase,
    ResultadoRecuperacao,
    RetrievalConfig,
    get_kb,
    recupera,
)

log = logging.getLogger(__name__)

STATUS_RESPONDIDA = "respondida"
STATUS_ABSTENCAO = {"fora_escopo", "recorte_vazio", "sem_evidencia", "evidencia_insuficiente",
                    "nao_respondida"}

ESCOPO_TEXTO = (
    "A base contém apenas avaliações escritas por clientes da Olist entre 2016 e 2018 "
    "sobre suas compras (entrega, produto, atendimento, vendedor, embalagem, preço)."
)


@dataclass
class Resposta:
    pergunta: str
    status: str
    markdown: str
    analise: AnalisePergunta | None = None
    recuperacao: ResultadoRecuperacao | None = None
    evidencias: pd.DataFrame = field(default_factory=pd.DataFrame)
    gerada: RespostaGerada | None = None
    citacoes: RelatorioCitacoes | None = None
    quadro: pd.DataFrame | None = None
    tempos: dict = field(default_factory=dict)
    quadro_txt: str | None = None  # quadro exatamente como o gerador o recebeu

    @property
    def absteve(self) -> bool:
        return self.status in STATUS_ABSTENCAO

    @property
    def evidencias_citadas(self) -> pd.DataFrame:
        if self.gerada is None or self.evidencias.empty:
            return self.evidencias
        ids = set(ids_citados(self.gerada))
        return self.evidencias[self.evidencias["rotulo"].isin(ids)]

    def to_dict(self) -> dict:
        ev_cols = ["rotulo", "review_id", "order_id", "nota", "texto", "relevancia",
                   "categoria", "entrega_status", "ano_mes", "uf"]
        ev = self.evidencias[[c for c in ev_cols if c in self.evidencias.columns]]
        return {
            "pergunta": self.pergunta,
            "status": self.status,
            "markdown": self.markdown,
            "analise": self.analise.model_dump() if self.analise else None,
            "recuperacao": self.recuperacao.resumo() if self.recuperacao else None,
            "resposta": self.gerada.model_dump() if self.gerada else None,
            "citacoes": vars(self.citacoes) if self.citacoes else None,
            "evidencias": ev.astype(object).where(ev.notna(), None).to_dict("records"),
            "quadro": self.quadro.to_dict("records") if self.quadro is not None else None,
            "tempos": self.tempos,
        }


def render_markdown(g: RespostaGerada, n_evidencias: int) -> str:
    linhas = [g.resumo.strip(), ""]
    for ins in g.insights:
        apoio = f"apoio: {len(ins.evidencias)} de {n_evidencias} evidências"
        linhas.append(f"- **{ins.titulo.strip()}**: {ins.descricao.strip()} *({apoio})*")
    if g.limitacoes.strip():
        linhas += ["", f"*Limitações: {g.limitacoes.strip()}*"]
    return "\n".join(linhas).strip()


def _milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _decimal(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


def _lista_evidencias(ev: pd.DataFrame) -> str:
    return "\n".join(
        f"- [{r.rotulo}] (nota {int(r.nota)}/5) \"{r.texto}\"" for r in ev.itertuples()
    )


class VoCPipeline:
    def __init__(
        self,
        cfg: RetrievalConfig | None = None,
        llm: LLMClient | None = None,
        kb: KnowledgeBase | None = None,
        usar_quadro: bool = True,
        aquecer: bool = True,
    ):
        self.cfg = cfg or RetrievalConfig()
        self.llm = llm or LLMClient()
        self.kb = kb or get_kb(self.cfg.modelo_embedding)
        self.usar_quadro = usar_quadro
        if aquecer:
            self.kb.aquece()

    # ---------------------------------------------------------------- etapas
    def _quadro(self, analise: AnalisePergunta, rec: ResultadoRecuperacao):
        if not self.usar_quadro or analise.tipo != "panorama":
            return None, None
        from voc_rag.themes.taxonomy import quadro_frequencias

        return quadro_frequencias(self.kb.docs, rec.filtros_aplicados, analise.polaridade)

    def responder(self, pergunta: str, filtros_manuais: Filtros | None = None) -> Resposta:
        """Responde a pergunta. Filtros manuais (da interface) prevalecem sobre os do LLM."""
        t0 = time.perf_counter()
        tempos: dict[str, float] = {}

        analise = analisa_pergunta(pergunta, self.kb.categorias, self.llm)
        if filtros_manuais is not None:
            for campo, valor in filtros_manuais.model_dump(exclude_defaults=True).items():
                setattr(analise.filtros, campo, valor)
        tempos["analise_s"] = round(time.perf_counter() - t0, 3)

        if analise.escopo == "fora":
            # O motivo do LLM fica só no rastro (análise): ele é escrito sem consultar a base
            # e pode afirmar fatos que ela não sustenta ("a loja não tem cashback").
            md = (
                "**Fora do escopo da base de conhecimento.**\n\n"
                f"{ESCOPO_TEXTO} Não respondo com conhecimento externo para não "
                "apresentar algo que os dados não sustentam."
            )
            tempos["total_s"] = round(time.perf_counter() - t0, 3)
            return Resposta(pergunta, "fora_escopo", md, analise, tempos=tempos)

        t = time.perf_counter()
        rec = recupera(pergunta, analise, self.cfg, self.kb)
        tempos["recuperacao_s"] = round(time.perf_counter() - t, 3)
        tempos.update({f"recuperacao_{k}": v for k, v in rec.tempos.items()})
        recorte = rec.filtros_aplicados.descricao()

        if rec.n_universo == 0:
            md = (
                f"**Nenhuma avaliação com comentário no recorte pedido** ({recorte}). "
                "Sem dados, não há o que analisar."
            )
            tempos["total_s"] = round(time.perf_counter() - t0, 3)
            return Resposta(pergunta, "recorte_vazio", md, analise, rec, tempos=tempos)

        if rec.n_relevantes == 0:
            md = (
                "**Não encontrei avaliações relevantes para responder com segurança.** "
                f"Analisei {len(rec.candidatos)} candidatas no recorte ({recorte}; "
                f"{_milhar(rec.n_universo)} avaliações com comentário), e nenhuma atingiu a "
                f"relevância mínima ({_decimal(self.cfg.limiar_relevancia)}). Prefiro não "
                "responder a inventar uma conclusão sem suporte nos dados."
            )
            tempos["total_s"] = round(time.perf_counter() - t0, 3)
            return Resposta(pergunta, "sem_evidencia", md, analise, rec, tempos=tempos)

        evidencias = rotula_evidencias(rec.selecionados)

        if rec.n_relevantes < self.cfg.min_evidencias:
            md = (
                f"**Evidência insuficiente para apontar um padrão.** Encontrei apenas "
                f"{rec.n_relevantes} avaliação(ões) relevante(s) no recorte ({recorte}), "
                f"abaixo do mínimo de {self.cfg.min_evidencias}. Seguem as evidências, "
                f"sem generalização:\n\n{_lista_evidencias(evidencias)}"
            )
            tempos["total_s"] = round(time.perf_counter() - t0, 3)
            return Resposta(pergunta, "evidencia_insuficiente", md, analise, rec, evidencias,
                            tempos=tempos)

        quadro_df, quadro_txt = self._quadro(analise, rec)

        t = time.perf_counter()
        prompt = monta_prompt(pergunta, monta_contexto(evidencias), recorte, rec.n_universo,
                              quadro_txt)
        try:
            gerada = self.llm.generate(SYSTEM_RESPOSTA, prompt, RespostaGerada, etapa="geracao",
                                       pensamento="alto")
            if sem_acentos(gerada):
                # Controle de qualidade: o modelo lite às vezes escreve sem acentos;
                # uma nova geração com reforço explícito resolve.
                log.info("resposta sem acentos; gerando de novo com reforço")
                gerada = self.llm.generate(SYSTEM_RESPOSTA + REFORCO_ACENTOS, prompt,
                                           RespostaGerada, etapa="geracao_reforco",
                                           pensamento="alto")
        except LLMIndisponivel as e:
            log.error("geração indisponível: %s", e)
            md = (
                "**Geração indisponível no momento** (LLM fora do ar ou sem chave). "
                f"Evidências recuperadas para a pergunta:\n\n{_lista_evidencias(evidencias)}"
            )
            tempos["total_s"] = round(time.perf_counter() - t0, 3)
            return Resposta(pergunta, "erro_llm", md, analise, rec, evidencias, quadro=quadro_df,
                            tempos=tempos)
        tempos["geracao_s"] = round(time.perf_counter() - t, 3)

        gerada, rel = valida_citacoes(gerada, set(evidencias["rotulo"]))
        if not gerada.suficiente or not gerada.insights:
            md = f"**As evidências recuperadas não sustentam uma resposta.** {gerada.resumo}"
            status = "nao_respondida"
        else:
            md = render_markdown(gerada, len(evidencias))
            if quadro_df is not None:
                # Denominador dos percentuais escrito pelo código, não pelo modelo.
                md += (f"\n\n*Percentuais: estimativa do classificador de aspectos sobre as "
                       f"{_milhar(rec.n_universo)} avaliações com comentário do recorte "
                       f"({recorte}).*")
            status = STATUS_RESPONDIDA
        tempos["total_s"] = round(time.perf_counter() - t0, 3)
        return Resposta(pergunta, status, md, analise, rec, evidencias, gerada, rel, quadro_df,
                        tempos, quadro_txt)
