"""Transformação da pergunta (primeira etapa do pipeline RAG).

Problema central: a pergunta do gestor ("Quais os principais problemas de
entrega?") e o documento ("comprei dia 10 e até hoje nada, péssimo") estão em
registros de linguagem muito diferentes. Uma chamada ao LLM converte a
pergunta em:

  * escopo (dentro/fora da base) para abster cedo e sem gastar recuperação;
  * tipo de pergunta (panorama, tema, evidência), que muda o tamanho do
    contexto e liga o quadro de frequências;
  * polaridade (problemas x elogios), usada como filtro implícito de nota;
  * filtros EXPLÍCITOS de metadado (nota, categoria, período, entrega, UF);
  * consulta reescrita no vocabulário do cliente + variações (multi-query);
  * uma avaliação hipotética (HyDE) no estilo dos comentários reais.
"""
from __future__ import annotations

import logging
from typing import Literal

from pydantic import BaseModel, Field

from voc_rag.generation.llm import LLMClient, LLMIndisponivel
from voc_rag.retrieval.filters import Filtros

log = logging.getLogger(__name__)


class AnalisePergunta(BaseModel):
    escopo: Literal["dentro", "fora"]
    motivo_escopo: str = Field(description="Uma frase justificando o escopo")
    tipo: Literal["panorama", "tema", "evidencia"]
    polaridade: Literal["negativa", "positiva", "qualquer"]
    filtros: Filtros = Field(default_factory=Filtros)
    consulta_busca: str
    consultas_alternativas: list[str] = Field(default_factory=list)
    avaliacao_hipotetica: str = ""
    origem: Literal["llm", "fallback"] = "llm"


SYSTEM = """Você é o módulo de entendimento de perguntas de um sistema de Voice of Customer.
A base de conhecimento contém SOMENTE avaliações escritas por clientes de um marketplace
brasileiro (Olist) entre 2016 e 2018, cada uma com: texto do comentário, nota de 1 a 5,
data da compra, situação da entrega (no_prazo, atrasado, nao_entregue, cancelado),
categoria do produto, UF/região do cliente e forma de pagamento.

Analise a pergunta e preencha o JSON:

escopo
- "dentro": pode ser respondida com opiniões e relatos de clientes nessas avaliações
  (experiência de compra, entrega, produto, atendimento, vendedor, embalagem, preço etc.).
- "fora": exige conhecimento externo ou dados que não estão nos comentários (fatos gerais,
  outras empresas, eventos depois de 2018, faturamento, lucro, estoque, funcionários,
  métricas internas), pedidos de tarefas sem relação (código, receitas, piadas) ou conversa.
- Um tema que talvez não apareça nas avaliações (ex.: um produto específico) continua
  "dentro": a falta de evidência é verificada depois, pela recuperação.

tipo
- "panorama": visão geral, principais/mais frequentes, padrões, ranking de temas.
- "tema": o que os clientes dizem sobre um assunto específico.
- "evidencia": pede avaliações/exemplos que sustentem ou refutem uma afirmação.

polaridade: "negativa" (problemas, reclamações, insatisfação), "positiva" (elogios, o que
valorizam) ou "qualquer".

filtros: preencha SOMENTE o que a pergunta delimita explicitamente.
- "nota baixa" → nota_max=2; "nota alta" → nota_min=4; "nota 1" → nota_min=1 e nota_max=1.
- "clientes insatisfeitos" sem nota explícita → NÃO preencha nota (a polaridade cuida disso).
- categorias: use apenas nomes da lista válida; mapeie sinônimos para todos os nomes
  pertinentes (ex.: "eletrônicos" → eletronicos, informatica_acessorios, telefonia...).
- período: ano_mes_inicio/ano_mes_fim no formato AAAAMM.
- entrega_status: só quando a pergunta recorta por situação do pedido ("pedidos que
  atrasaram", "entregas no prazo"). Se atraso é o próprio TEMA ("reclamações sobre
  atraso"), NÃO filtre: muitos clientes reclamam antes de o pedido constar como entregue.
- ufs (siglas) e regioes (Norte, Nordeste, Centro-Oeste, Sudeste, Sul).
- informações do pedido: pagamentos (credit_card, boleto, voucher, debit_card) quando a
  pergunta cita a forma de pagamento; valor_min/valor_max (R$, valor dos itens) para
  "compras acima de R$ 500", "pedidos baratos" (use um valor explícito só se a pergunta der
  um); multi_vendedor=true para pedidos com itens de mais de um vendedor/loja.

consulta_busca: reescreva a pergunta como consulta de busca semântica usando o vocabulário
que CLIENTES usam nos comentários (ex.: "produto não chegou, atraso na entrega, prazo não
cumprido"). Não inclua filtros nem palavras como "quais", "principais", "clientes".

consultas_alternativas: 2 ou 3 variações que cubram outros aspectos ou sinônimos do tema.

Regra de fidelidade (consulta_busca, variações e avaliação hipotética): mantenha SEMPRE o
assunto específico da pergunta. Não generalize nem acrescente temas vizinhos. Ex.: para
"entregas feitas por drone", todas as consultas falam de drone; nunca "entrega rápida".
Para "cashback", todas falam de cashback/pontos; nunca "dinheiro de volta" de reembolso.

avaliacao_hipotetica: UMA avaliação curta e realista (1 a 2 frases, linguagem informal de
cliente brasileiro) que seria um exemplo perfeito do que se procura. Em panorama negativo
genérico, misture problemas comuns de compra online.

Se escopo = "fora", preencha os demais campos com valores mínimos."""


def _prompt(pergunta: str, categorias: list[str]) -> str:
    return (
        f"Categorias válidas: {', '.join(categorias)}\n\n"
        f"Pergunta: {pergunta.strip()}"
    )


def sanitiza(analise: AnalisePergunta, categorias: list[str]) -> AnalisePergunta:
    """Corrige o que o LLM pode devolver fora do domínio da base."""
    f = analise.filtros
    # Sentimento é papel da polaridade (vira filtro implícito de nota na
    # recuperação); se o LLM também o preenche, o recorte fica restrito demais.
    f.sentimentos = []
    validas = set(categorias)
    descartadas = [c for c in f.categorias if c not in validas]
    if descartadas:
        log.warning("categorias inexistentes descartadas: %s", descartadas)
    f.categorias = [c for c in f.categorias if c in validas]
    if f.nota_min and f.nota_max and f.nota_min > f.nota_max:
        f.nota_min, f.nota_max = f.nota_max, f.nota_min
    for campo in ("ano_mes_inicio", "ano_mes_fim"):
        v = getattr(f, campo)
        if v is not None and not (201601 <= v <= 201812):
            setattr(f, campo, None)
    f.ufs = [u.upper() for u in f.ufs if len(u) == 2]
    alternativas = [a for a in analise.consultas_alternativas if a.strip()][:3]
    analise.consultas_alternativas = alternativas
    return analise


def fallback(pergunta: str) -> AnalisePergunta:
    """Sem LLM: a pergunta crua vira a consulta, sem filtros (degrada, não quebra)."""
    return AnalisePergunta(
        escopo="dentro",
        motivo_escopo="LLM indisponível: escopo não verificado",
        tipo="tema",
        polaridade="qualquer",
        consulta_busca=pergunta,
        origem="fallback",
    )


def analisa_pergunta(
    pergunta: str, categorias: list[str], llm: LLMClient | None = None
) -> AnalisePergunta:
    llm = llm or LLMClient()
    try:
        analise = llm.generate(
            SYSTEM, _prompt(pergunta, categorias), AnalisePergunta, etapa="analise_pergunta"
        )
    except LLMIndisponivel as e:
        log.warning("análise da pergunta sem LLM: %s", e)
        return fallback(pergunta)
    analise.origem = "llm"
    return sanitiza(analise, categorias)
