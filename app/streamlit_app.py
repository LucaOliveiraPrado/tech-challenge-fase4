"""Interface de exploração da voz do cliente (Streamlit).

    uv run streamlit run app/streamlit_app.py
"""
from __future__ import annotations

import html
import json
import re
import warnings

import altair as alt
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

from voc_rag.config import REPORTS_DIR  # noqa: E402
from voc_rag.pipeline import VoCPipeline  # noqa: E402
from voc_rag.retrieval.filters import ROTULO_ENTREGA, ROTULO_PAGAMENTO, Filtros  # noqa: E402

st.set_page_config(page_title="Voz do Cliente Olist", page_icon="💬", layout="wide")

AZUL = "#2a78d6"
STATUS_UI = {
    "respondida": ("success", "Resposta fundamentada nas avaliações recuperadas"),
    "fora_escopo": ("warning", "Abstenção: pergunta fora do escopo da base"),
    "recorte_vazio": ("warning", "Abstenção: nenhuma avaliação no recorte pedido"),
    "sem_evidencia": ("warning", "Abstenção: nenhuma avaliação relevante encontrada"),
    "evidencia_insuficiente": ("warning", "Abstenção: evidência insuficiente para um padrão"),
    "nao_respondida": ("warning", "Abstenção: as evidências não sustentam uma resposta"),
    "erro_llm": ("error", "Geração indisponível: mostrando só as evidências"),
}

EXEMPLOS = {
    "Reclamações": [
        "Quais são os principais problemas relatados pelos clientes em suas avaliações?",
        "Quais reclamações relacionadas à entrega aparecem com maior frequência?",
    ],
    "Elogios": [
        "Quais aspectos da experiência de compra são mais elogiados pelos clientes?",
        "O que os clientes mais elogiam na categoria cama, mesa e banho?",
    ],
    "Investigação": [
        "Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?",
        "Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?",
        "Quais avaliações sustentam a conclusão de que existem problemas recorrentes "
        "relacionados ao prazo de entrega?",
    ],
    "Metadados": [
        "Quais são os principais problemas relatados nas avaliações com nota baixa?",
        "Quais temas aparecem nas avaliações de pedidos entregues com atraso?",
        "Quais problemas aparecem em pedidos com produtos de mais de um vendedor?",
    ],
    "Limites": [
        "Qual foi o faturamento da Olist em 2018?",
        "O que os clientes acharam das entregas feitas por drone?",
    ],
}

st.markdown(
    """
<style>
.cite {background:#e8f1fc;color:#184f95;border-radius:4px;padding:0 4px;font-size:0.85em;
       font-weight:600;white-space:nowrap}
.ev {border:1px solid rgba(11,11,11,0.10);border-left:4px solid #c3c2b7;border-radius:6px;
     padding:8px 12px;margin-bottom:8px;background:#ffffff}
.ev.citada {border-left-color:#2a78d6}
.ev .meta {color:#52514e;font-size:0.8em;margin-bottom:4px}
.ev .texto {font-size:0.95em}
.ev .rid {color:#898781;font-size:0.72em;font-family:monospace}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Carregando modelos e índices...")
def pipeline() -> VoCPipeline:
    return VoCPipeline()


def realca_citacoes(md: str) -> str:
    return re.sub(r"\[(R\d+)\]", r'<span class="cite">\1</span>', md)


def estrelas(n: int) -> str:
    return "★" * int(n) + "☆" * (5 - int(n))


def card(ev: pd.Series, citada: bool, insights: list[int]) -> str:
    """Cartão da evidência; `insights` são os números dos insights que ela sustenta."""
    relev = f"{ev['relevancia']:.2f}".replace(".", ",")
    meta = [f"<b>{ev['rotulo']}</b>", estrelas(ev["nota"]), f"relevância {relev}"]
    if insights:
        meta.insert(1, f"<b>sustenta: insight {', '.join(map(str, insights))}</b>")
    if isinstance(ev.get("categoria"), str):
        meta.append(ev["categoria"])
    if isinstance(ev.get("entrega_status"), str):
        rot = ROTULO_ENTREGA.get(ev["entrega_status"], ev["entrega_status"])
        if ev["entrega_status"] == "atrasado" and pd.notna(ev.get("atraso_dias")):
            rot += f" ({int(ev['atraso_dias'])} dias)"
        meta.append(rot)
    if isinstance(ev.get("uf"), str):
        meta.append(ev["uf"])
    if pd.notna(ev.get("ano_mes")):
        am = int(ev["ano_mes"])
        meta.append(f"{am % 100:02d}/{am // 100}")
    classe = "ev citada" if citada else "ev"
    return (
        f'<div class="{classe}"><div class="meta">{" · ".join(meta)}</div>'
        f'<div class="texto">“{html.escape(ev["texto"])}”</div>'
        f'<div class="rid">review_id {ev["review_id"]}</div></div>'
    )


# ------------------------------------------------------------------ cabeçalho
st.title("Voz do Cliente Olist")
st.caption(
    "Pergunte em linguagem natural. A resposta é construída só com avaliações reais "
    "de clientes, e cada afirmação aponta as avaliações que a sustentam."
)

try:
    rastro = json.loads((REPORTS_DIR / "base_conhecimento.json").read_text(encoding="utf-8"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avaliações com comentário", f"{rastro['documentos']:,}".replace(",", "."))
    c2.metric("Avaliações na base", f"{rastro['avaliacoes_unicas']:,}".replace(",", "."))
    c3.metric("Período das compras", "2016 a 2018")
    c4.metric("Documentos negativos", f"{rastro['documentos_por_sentimento']['negativo']:,}"
              .replace(",", "."))
except FileNotFoundError:
    st.info("Base não construída: rode `uv run voc prepare` e `uv run voc build`.")
    st.stop()

pipe = pipeline()
categorias = pipe.kb.categorias

# ------------------------------------------------------------------ barra lateral
with st.sidebar:
    st.header("Perguntas de exemplo")
    for grupo, perguntas in EXEMPLOS.items():
        with st.expander(grupo, expanded=grupo == "Reclamações"):
            for p in perguntas:
                if st.button(p, key=p, use_container_width=True):
                    st.session_state["pergunta"] = p
                    st.session_state["executar"] = True

    st.header("Filtros manuais (opcional)")
    st.caption("Somam-se aos filtros que o sistema extrai da pergunta.")
    notas = st.slider("Nota", 1, 5, (1, 5))
    cats = st.multiselect("Categoria", categorias, placeholder="Todas")
    entrega = st.multiselect("Entrega", list(ROTULO_ENTREGA), format_func=ROTULO_ENTREGA.get,
                             placeholder="Todas")
    regioes = st.multiselect("Região", ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"],
                             placeholder="Todas")
    pagamentos = st.multiselect("Pagamento", list(ROTULO_PAGAMENTO),
                                format_func=ROTULO_PAGAMENTO.get, placeholder="Todos")
    valor_min = st.number_input("Valor mínimo dos itens (R$)", min_value=0, value=0, step=50)
    multi = st.checkbox("Só pedidos com mais de um vendedor")
    mostrar_rastro = st.toggle("Mostrar rastro do pipeline", value=True)

filtros_manuais = Filtros(
    nota_min=notas[0] if notas != (1, 5) else None,
    nota_max=notas[1] if notas != (1, 5) else None,
    categorias=cats, entrega_status=entrega, regioes=regioes, pagamentos=pagamentos,
    valor_min=float(valor_min) if valor_min else None, multi_vendedor=True if multi else None,
)

# ------------------------------------------------------------------ pergunta
with st.form("pergunta_form"):
    pergunta = st.text_input(
        "Sua pergunta", key="pergunta",
        placeholder="Ex.: O que os clientes relatam sobre problemas relacionados à entrega?",
    )
    enviar = st.form_submit_button("Perguntar", type="primary")

if (enviar or st.session_state.pop("executar", False)) and pergunta.strip():
    with st.spinner("Analisando a pergunta, recuperando avaliações e gerando a resposta..."):
        st.session_state["resposta"] = pipe.responder(
            pergunta, None if filtros_manuais.vazio() else filtros_manuais
        )

r = st.session_state.get("resposta")
if r is None:
    st.stop()

# ------------------------------------------------------------------ resposta
tipo, titulo = STATUS_UI.get(r.status, ("info", r.status))
getattr(st, tipo)(titulo)

col_resp, col_ev = st.columns([3, 2], gap="large")
with col_resp:
    st.subheader("Resposta")
    st.markdown(realca_citacoes(r.markdown), unsafe_allow_html=True)

    # Rastreabilidade insight -> avaliações: cada insight abre as evidências que o sustentam.
    sustenta: dict[str, list[int]] = {}
    if r.gerada is not None and not r.evidencias.empty:
        por_rotulo = r.evidencias.set_index("rotulo")
        for i, ins in enumerate(r.gerada.insights, 1):
            rots = [e for e in ins.evidencias if e in por_rotulo.index]
            for e in rots:
                sustenta.setdefault(e, []).append(i)
            with st.expander(f"Evidências do insight {i}: {ins.titulo.strip()} ({len(rots)})"):
                for e in rots:
                    ev = por_rotulo.loc[e]
                    st.markdown(f"**{e}** · nota {int(ev['nota'])} · `{ev['review_id']}`  \n"
                                f"“{ev['texto']}”")

    if r.quadro is not None and not r.quadro.empty:
        st.subheader("Frequência dos temas no recorte")
        st.caption("Base completa do recorte (classificador de aspectos), não só a amostra.")
        q = r.quadro.head(10).assign(
            pct_txt=lambda d: d["pct"].map(lambda v: f"{v:.1f}%".replace(".", ","))
        )
        base = alt.Chart(q).encode(
            y=alt.Y("rotulo:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260, labelOverlap=False)),
            x=alt.X("avaliacoes:Q", title="avaliações (estimativa)", axis=alt.Axis(format="d")),
            tooltip=[alt.Tooltip("rotulo:N", title="aspecto"),
                     alt.Tooltip("avaliacoes:Q", title="avaliações"),
                     alt.Tooltip("pct_txt:N", title="% do recorte")],
        )
        barras = base.mark_bar(color=AZUL, cornerRadiusEnd=4, height=16)
        rotulos = base.mark_text(align="left", dx=4, color="#52514e").encode(text="pct_txt:N")
        st.altair_chart((barras + rotulos).properties(height=28 * len(q)),
                        use_container_width=True)

with col_ev:
    if not r.evidencias.empty:
        citadas = set(r.evidencias_citadas["rotulo"]) if r.gerada else set()
        st.subheader(f"Evidências ({len(r.evidencias)})")
        st.caption("Borda azul: citada na resposta, com os insights que sustenta. Na ordem do "
                   "contexto enviado ao LLM (fusão RRF da busca híbrida, diversificada por MMR).")
        for _, ev in r.evidencias.iterrows():
            st.markdown(card(ev, ev["rotulo"] in citadas, sustenta.get(ev["rotulo"], [])),
                        unsafe_allow_html=True)

# ------------------------------------------------------------------ rastro
if mostrar_rastro and r.analise is not None:
    st.divider()
    st.subheader("Como a resposta foi construída")
    a = r.analise
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**1. Análise da pergunta**")
        st.markdown(
            f"- Escopo: `{a.escopo}` ("
            + (a.motivo_escopo if a.motivo_escopo.startswith("regra:") else
               f"motivo dado pelo LLM, sem consultar a base: {a.motivo_escopo}")
            + ")\n"
            f"- Tipo: `{a.tipo}` · Polaridade: `{a.polaridade}`\n"
            f"- Filtros extraídos: `{a.filtros.descricao()}`"
        )
        if r.recuperacao is not None:
            st.markdown("**2. Consultas usadas na busca**")
            for q in r.recuperacao.consultas:
                st.markdown(f"- _{q}_")
    with c2:
        if r.recuperacao is not None:
            rec = r.recuperacao
            st.markdown("**3. Funil da recuperação**")
            funil = pd.DataFrame({
                "etapa": ["no recorte (filtros)", "candidatas (híbrido + RRF)",
                          "relevantes (reranker)", "no contexto (dedup + MMR)"],
                "documentos": [f"{n:,}".replace(",", ".") for n in (
                    rec.n_universo, len(rec.candidatos), rec.n_relevantes,
                    len(rec.selecionados))],
            })
            st.dataframe(funil, hide_index=True, use_container_width=True)
            st.markdown(f"Recorte efetivo: `{rec.filtros_aplicados.descricao()}`")
        st.markdown("**4. Tempos**")
        etapas = {"analise_s": "análise da pergunta (LLM)", "recuperacao_s": "recuperação",
                  "geracao_s": "geração (LLM)", "total_s": "total"}
        st.dataframe(
            pd.DataFrame([{"etapa": nome, "segundos": f"{r.tempos[k]:.2f}".replace(".", ",")}
                          for k, nome in etapas.items() if k in r.tempos]),
            hide_index=True, use_container_width=True,
        )
        st.caption("Respostas já feitas antes vêm do cache do LLM e aparecem quase instantâneas.")
    if r.recuperacao is not None and not r.recuperacao.candidatos.empty:
        with st.expander("Candidatas e escores (denso, BM25, RRF, reranker)"):
            cols = ["pos_rrf", "relevancia", "score_denso", "score_bm25", "rrf", "nota", "texto"]
            st.dataframe(r.recuperacao.candidatos[cols].head(40), hide_index=True,
                         use_container_width=True)
    if r.citacoes is not None:
        st.caption(
            f"Validação das citações: {r.citacoes.citacoes_total} citações, "
            f"{r.citacoes.citacoes_invalidas} inválidas removidas, "
            f"{r.citacoes.insights_descartados} insights sem evidência descartados."
        )
