"""Relatório legível a partir dos JSON da avaliação: exemplos de perguntas e respostas."""
from __future__ import annotations

import json

from voc_rag.config import REPORTS_DIR

EXEMPLOS = ["Q01", "Q04", "Q08", "Q19", "Q22", "Q26", "Q29", "Q35", "Q37"]

TITULO_STATUS = {
    "respondida": "respondida com evidências",
    "fora_escopo": "abstenção: fora do escopo",
    "sem_evidencia": "abstenção: sem evidência relevante",
    "evidencia_insuficiente": "abstenção: evidência insuficiente",
    "nao_respondida": "abstenção: evidências não sustentam resposta",
    "recorte_vazio": "abstenção: recorte vazio",
}


def _cel(s: str) -> str:
    return str(s).replace("|", "/").replace("\n", " ")


def _milhar(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _n(x: float, casas: int = 3) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def _pct(x: float, casas: int = 1) -> str:
    return f"{100 * x:.{casas}f}%".replace(".", ",")


def gera_tabelas_readme() -> dict[str, str]:
    """Tabelas do README geradas dos JSON (o teste test_readme_numeros garante a cópia fiel)."""
    rec = json.loads((REPORTS_DIR / "avaliacao_recuperacao.json").read_text(encoding="utf-8"))
    ger = json.loads((REPORTS_DIR / "avaliacao_geracao.json").read_text(encoding="utf-8"))
    base = json.loads((REPORTS_DIR / "base_conhecimento.json").read_text(encoding="utf-8"))
    asp = json.loads((REPORTS_DIR / "metricas_aspectos.json").read_text(encoding="utf-8"))
    cfg = rec["configuracoes"]
    t: dict[str, str] = {}

    t["base"] = "\n".join([
        "| Etapa | Quantidade |",
        "|---|---|",
        f"| Linhas na fonte | {base['linhas_fonte']:,} |".replace(",", "."),
        f"| `review_id` ligados a mais de um pedido (contam uma vez) | "
        f"{base['review_ids_em_multiplos_pedidos']} |",
        f"| Avaliações únicas | {base['avaliacoes_unicas']:,} |".replace(",", "."),
        f"| Sem mensagem na fonte | {base['mensagem_ausente_na_fonte']:,} |".replace(",", "."),
        f"| Mensagem vazia após limpeza | {base['mensagem_sem_conteudo_apos_limpeza']} |",
        f"| **Documentos na base de conhecimento** | **{base['documentos']:,}** |"
        .replace(",", "."),
    ])

    caminho = [
        ("A0_denso_pergunta_crua", "RAG ingênuo (pergunta crua, só vetor)"),
        ("A1_reescrita", "+ reescrita da pergunta"),
        ("V1_hibrido_so_reescrita", "+ BM25 (busca híbrida, fusão RRF)"),
        ("F1_final_so_reescrita",
         "**+ filtros de metadado, polaridade e reranker como porteiro (sistema final)**"),
    ]
    linhas = ["| Etapa | P@5 | P@10 | nDCG@10 | MRR | Hit@5 |", "|---|---|---|---|---|---|"]
    for k, nome in caminho:
        c = cfg[k]
        linhas.append(f"| {nome} | {_n(c['p@5'])} | {_n(c['p@10'])} | {_n(c['ndcg@10'])} | "
                      f"{_n(c['mrr'])} | {_n(c['hit@5'])} |")
    t["ablacao"] = "\n".join(linhas)

    testes = [
        ("multi-query + HyDE sobre a consulta reescrita", "A2_multiquery_hyde",
         "A1_reescrita"),
        ("reranker ordenando o resultado da busca híbrida", "A4_reranker",
         "A3_hibrido_bm25_rrf"),
        ("reranker contra a consulta principal (em vez do máximo)",
         "V3_reranker_consulta_principal", "A3_hibrido_bm25_rrf"),
        ("sistema completo ordenado pelo reranker", "A5_metadados_polaridade",
         "F1_final_so_reescrita"),
    ]
    linhas = ["| Técnica testada | P@10 com | P@10 sem | Decisão |", "|---|---|---|---|"]
    for nome, com, sem in testes:
        linhas.append(f"| {nome} | {_n(cfg[com]['p@10'])} | {_n(cfg[sem]['p@10'])} | "
                      "descartada |")
    t["descartadas"] = "\n".join(linhas)

    emb = [("E_minilm", "paraphrase-multilingual-MiniLM-L12-v2"),
           ("E_e5_base", "multilingual-e5-base"), ("E_bge_m3", "**bge-m3 (escolhido)**")]
    linhas = ["| Modelo de embedding | P@10 | nDCG@10 | MRR |", "|---|---|---|---|"]
    for k, nome in emb:
        c = cfg[k]
        linhas.append(f"| {nome} | {_n(c['p@10'])} | {_n(c['ndcg@10'])} | {_n(c['mrr'])} |")
    t["embeddings"] = "\n".join(linhas)

    sem_f, com_f = cfg["V1_hibrido_so_reescrita"], cfg["F1_final_so_reescrita"]
    t["metadados"] = "\n".join([
        "| 8 perguntas com recorte por metadado | Sem filtros | Com filtros (sistema final) |",
        "|---|---|---|",
        f"| Conformidade ao recorte (top-10) | {_pct(sem_f['metadados_conformidade@10'])} | "
        f"**{_pct(com_f['metadados_conformidade@10'])}** |",
        f"| P@10 (juiz vê os metadados) | {_n(sem_f['metadados_p@10'])} | "
        f"**{_n(com_f['metadados_p@10'])}** |",
    ])

    ab, ci, fi = ger["abstencao"], ger["citacoes"], ger["fidelidade"]
    m = ab["matriz"]
    cal = rec["calibracao_limiar"]
    t["geracao"] = "\n".join([
        "| Métrica | Resultado |",
        "|---|---|",
        f"| Decisão responder x abster correta | {_pct(ab['acuracia'])} "
        f"({m['resposta_correta'] + m['abstencao_correta']} de {ger['n_perguntas']}) |",
        f"| Abstenções corretas (fora de escopo + sem evidência) | {m['abstencao_correta']} de "
        f"{m['abstencao_correta'] + m['resposta_indevida']} |",
        f"| Perguntas respondíveis recusadas indevidamente | {m['abstencao_indevida']} de "
        f"{m['abstencao_indevida'] + m['resposta_correta']} |",
        f"| Citações válidas (verificadas por código) | {_pct(ci['citacoes_validas_pct'])} "
        f"de {ci['citacoes_total']} |",
        f"| Fidelidade dos insights (juiz; sustentado = 1, parcial = 0,5) | "
        f"{_n(fi['escore_fidelidade'], 2)} em {fi['insights_julgados']} insights |",
        f"| Precisão do contexto enviado ao LLM | {_pct(rec['precisao_contexto_final'])} |",
        f"| Extração correta dos filtros de metadado | "
        f"{_pct(ger['extracao_filtros']['acerto_pct'], 0)} |",
        f"| AUC do reranker contra o juiz | {_n(cal['auc_reranker_vs_juiz'])} |",
    ])

    lat_path = REPORTS_DIR / "latencia.json"
    if lat_path.exists():
        lat = json.loads(lat_path.read_text(encoding="utf-8"))
        m = lat["mediana_s"]
        t["latencia"] = "\n".join([
            "| Etapa (mediana, sem cache) | Segundos |",
            "|---|---|",
            f"| Análise da pergunta (LLM) | {_n(m['analise_s'], 1)} |",
            f"| Recuperação (embeddings, ChromaDB, BM25, reranker; "
            f"{'GPU' if lat['dispositivo'] == 'cuda' else 'CPU'}) | "
            f"{_n(m['recuperacao_s'], 1)} |",
            f"| Geração (LLM) | {_n(m['geracao_s'], 1)} |",
            f"| **Total por pergunta** | **{_n(m['total_s'], 1)}** |",
        ])

    conc_path = REPORTS_DIR / "concordancia_juizes.json"
    if conc_path.exists():
        c = json.loads(conc_path.read_text(encoding="utf-8"))
        t["concordancia"] = "\n".join([
            f"| Concordância entre juízes ({c['pares']} pares rejulgados por "
            f"`{c['segundo_juiz']}`) | Resultado |",
            "|---|---|",
            f"| Concordância exata na escala 0/1/2 | {_pct(c['concordancia_exata'])} |",
            f"| Kappa de Cohen ponderado (0/1/2) | {_n(c['kappa_ponderado'])} |",
            f"| Concordância em \"evidência clara\" (decisão usada na P@10) | "
            f"{_pct(c['concordancia_binaria_relevante'])} |",
            f"| Kappa de Cohen nessa decisão | {_n(c['kappa_binario_relevante'])} |",
        ])

    resp_path = REPORTS_DIR / "respostas_avaliacao.json"
    if resp_path.exists():
        t["exemplo"] = exemplo_inline("Q19")

    t["aspectos"] = (
        f"micro-F1 {_n(asp['micro_f1'])} e macro-F1 {_n(asp['macro_f1'])} em "
        f"{asp['n_teste']} rótulos de teste"
    )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    corpo = "\n\n".join(f"<!-- {k} -->\n{v}" for k, v in t.items())
    (REPORTS_DIR / "tabelas_readme.md").write_text(corpo + "\n", encoding="utf-8")
    sincroniza_readme(t)
    return t


def exemplo_inline(qid: str, n_evidencias: int = 3) -> str:
    """Versão curta de um exemplo para o README (resposta + primeiras evidências citadas)."""
    registros = json.loads((REPORTS_DIR / "respostas_avaliacao.json").read_text(encoding="utf-8"))
    r = next(x for x in registros if x["id"] == qid)
    linhas = [f"**Pergunta:** {r['pergunta']}", ""]
    linhas += ["> " + ln if ln else ">" for ln in r["markdown"].splitlines()]
    citadas = set()
    for ins in (r.get("resposta") or {}).get("insights", []):
        citadas.update(ins["evidencias"])
    ev = [e for e in r["evidencias"] if e["rotulo"] in citadas][:n_evidencias]
    linhas += ["", "| id | review_id | nota | texto do cliente |", "|---|---|---|---|"]
    linhas += [f"| {e['rotulo']} | `{e['review_id']}` | {e['nota']} | {_cel(e['texto'])} |"
               for e in ev]
    return "\n".join(linhas)


def sincroniza_readme(tabelas: dict[str, str]) -> None:
    """Reescreve no README o conteúdo entre <!-- num:X --> e <!-- /num:X -->."""
    import re

    from voc_rag.config import ROOT

    caminho = ROOT / "README.md"
    if not caminho.exists():
        return
    texto = caminho.read_text(encoding="utf-8")
    for nome, conteudo in tabelas.items():
        padrao = re.compile(rf"(<!-- num:{nome} -->).*?(<!-- /num:{nome} -->)", re.S)
        texto = padrao.sub(lambda m, c=conteudo: f"{m.group(1)}\n{c}\n{m.group(2)}", texto)
    caminho.write_text(texto, encoding="utf-8")


def gera_exemplos(max_evidencias: int = 5) -> str:
    registros = json.loads((REPORTS_DIR / "respostas_avaliacao.json").read_text(encoding="utf-8"))
    por_id = {r["id"]: r for r in registros}
    linhas = [
        "# Exemplos de perguntas e respostas",
        "",
        "> Gerado automaticamente por `uv run voc avaliar` a partir de",
        "> `reports/respostas_avaliacao.json` (todas as 40 respostas estão lá, com análise da",
        "> pergunta, filtros, evidências e tempos). Cada evidência é rastreável pelo `review_id`",
        "> na base da Olist.",
        "",
    ]
    for qid in EXEMPLOS:
        r = por_id.get(qid)
        if not r:
            continue
        linhas += [f"## {qid}. {r['pergunta']}", ""]
        linhas.append(f"**Status:** {TITULO_STATUS.get(r['status'], r['status'])}")
        a = r.get("analise") or {}
        if a:
            filtros = {k: v for k, v in a["filtros"].items() if v not in (None, [], "")}
            linhas.append(
                f"  \n**Análise da pergunta:** tipo `{a['tipo']}`, polaridade `{a['polaridade']}`"
                + (f", filtros `{json.dumps(filtros, ensure_ascii=False)}`" if filtros else "")
            )
            linhas.append(f"  \n**Consulta reescrita:** _{a['consulta_busca']}_")
        rec = r.get("recuperacao")
        if rec:
            linhas.append(
                f"  \n**Recuperação:** {_milhar(rec['n_universo'])} avaliações no recorte, "
                f"{rec['n_relevantes']} relevantes entre {rec['n_candidatos']} candidatas, "
                f"{rec['n_selecionados']} no contexto"
            )
        linhas += ["", "**Resposta:**", ""]
        linhas += ["> " + ln if ln else ">" for ln in r["markdown"].splitlines()]
        citadas = set()
        if r.get("resposta"):
            for ins in r["resposta"]["insights"]:
                citadas.update(ins["evidencias"])
        ev = [e for e in r.get("evidencias", []) if not citadas or e["rotulo"] in citadas]
        if ev:
            linhas += ["", "| id | review_id | nota | relevância | texto do cliente |",
                       "|---|---|---|---|---|"]
            for e in ev[:max_evidencias]:
                linhas.append(
                    f"| {e['rotulo']} | `{e['review_id'][:12]}…` | {e['nota']} | "
                    f"{_n(e['relevancia'], 2)} | {_cel(e['texto'])} |"
                )
            if len(ev) > max_evidencias:
                linhas.append(f"\n_+{len(ev) - max_evidencias} evidências no JSON completo._")
        linhas.append("")
    texto = "\n".join(linhas)
    (REPORTS_DIR / "exemplos_perguntas_respostas.md").write_text(texto, encoding="utf-8")
    return texto
