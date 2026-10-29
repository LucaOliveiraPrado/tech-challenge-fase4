"""Relatório legível a partir dos JSON da avaliação: exemplos de perguntas e respostas."""
from __future__ import annotations

import json

from voc_rag.config import REPORTS_DIR

EXEMPLOS = ["Q01", "Q04", "Q08", "Q19", "Q22", "Q26", "Q42", "Q29", "Q35", "Q37"]

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


def ic_diferenca(pp: dict, com: str, sem: str, n_boot: int = 10_000) -> tuple[float, float, float]:
    """Diferença média de P@10 (com - sem) e IC 95% por bootstrap pareado nas perguntas."""
    import numpy as np

    qids = [q for q in pp if com in pp[q] and sem in pp[q]]
    d = np.array([pp[q][com]["p@10"] - pp[q][sem]["p@10"] for q in qids])
    rng = np.random.default_rng(42)
    medias = d[rng.integers(0, len(d), size=(n_boot, len(d)))].mean(axis=1)
    return float(d.mean()), float(np.percentile(medias, 2.5)), float(np.percentile(medias, 97.5))


def _wilson(k: int, n: int, z: float = 1.96) -> str:
    """Intervalo de Wilson para uma proporção (adequado a n pequeno e a 100%)."""
    if n == 0:
        return "n/a"
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    meia = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / (1 + z * z / n)
    return f"[{_n(max(0.0, centro - meia), 2)}; {_n(min(1.0, centro + meia), 2)}]"


def _ic_txt(pp: dict, com: str, sem: str) -> str:
    m, lo, hi = ic_diferenca(pp, com, sem)
    def s(x: float) -> str:
        return ("+" if x > 0 else "") + _n(x)
    empate = " (empate)" if lo <= 0 <= hi else ""
    return f"{s(m)} [{s(lo)}; {s(hi)}]{empate}"


def precisao_citacoes(registros: list[dict]) -> dict | None:
    """Fração das avaliações citadas que o juiz de relevância marcou como evidência clara (2),
    entre as citadas que foram julgadas para aquela pergunta."""
    import pandas as pd

    from voc_rag.config import EVAL_DIR

    caminho = EVAL_DIR / "julgamentos_relevancia.csv"
    if not caminho.exists():
        return None
    julg = pd.read_csv(caminho).set_index(["qid", "review_id"])["relevancia"].to_dict()
    graus = []
    for r in registros:
        mapa = _citadas_por_insight(r)
        for e in r.get("evidencias", []):
            if e["rotulo"] in mapa and (r["id"], e["review_id"]) in julg:
                graus.append(julg[(r["id"], e["review_id"])])
    n_cit = sum(len(_citadas_por_insight(r)) for r in registros)
    if not graus:
        return None
    return {"julgadas": len(graus), "citadas": n_cit,
            "clara": sum(g == 2 for g in graus) / len(graus),
            "relacionada": sum(g >= 1 for g in graus) / len(graus)}


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

    # O porteiro (limiar do reranker) não entra no top-10 medido: a ablação recupera com
    # limiar 0, e o porteiro atua na abstenção e no contexto final (tabela "geracao").
    caminho = [
        ("A0_denso_pergunta_crua", "RAG ingênuo (pergunta crua, só vetor)"),
        ("A1_reescrita", "+ reescrita da pergunta"),
        ("V1_hibrido_so_reescrita", "+ BM25 (busca híbrida, fusão RRF)"),
        ("F1_final_so_reescrita", "**+ filtros de metadado e polaridade (sistema final)**"),
    ]
    linhas = ["| Etapa | P@5 | P@10 | nDCG@10 | MRR | Hit@5 |", "|---|---|---|---|---|---|"]
    for k, nome in caminho:
        c = cfg[k]
        linhas.append(f"| {nome} | {_n(c['p@5'])} | {_n(c['p@10'])} | {_n(c['ndcg@10'])} | "
                      f"{_n(c['mrr'])} | {_n(c['hit@5'])} |")
    t["ablacao"] = "\n".join(linhas)

    # Mesma ablação separando perguntas com e sem recorte: mostra de onde vem o ganho final.
    from voc_rag.evaluation.retrieval_eval import carrega_perguntas

    perguntas = {p["id"]: p for p in carrega_perguntas()}
    pp = rec["por_pergunta"]
    grupos = {
        "sem": [q for q in pp if not perguntas.get(q, {}).get("filtros_esperados")],
        "com": [q for q in pp if perguntas.get(q, {}).get("filtros_esperados")],
    }

    def _media(k: str, qids: list[str]) -> float:
        vals = [pp[q][k]["p@10"] for q in qids if k in pp[q]]
        return sum(vals) / len(vals)

    linhas = [f"| Etapa | P@10 sem recorte ({len(grupos['sem'])} perguntas) | "
              f"P@10 com recorte ({len(grupos['com'])} perguntas) |", "|---|---|---|"]
    for k, nome in caminho:
        linhas.append(f"| {nome.strip('*')} | {_n(_media(k, grupos['sem']))} | "
                      f"{_n(_media(k, grupos['com']))} |")
    t["ablacao_recorte"] = "\n".join(linhas)

    testes = [
        ("multi-query + HyDE no sistema completo", "F2_final_multiquery",
         "F1_final_so_reescrita"),
        ("reranker ordenando o resultado da busca híbrida", "A4_reranker",
         "A3_hibrido_bm25_rrf"),
        ("reranker contra a consulta principal (em vez do máximo)",
         "V3_reranker_consulta_principal", "A3_hibrido_bm25_rrf"),
        ("sistema completo ordenado pelo reranker", "A5_metadados_polaridade",
         "F1_final_so_reescrita"),
    ]
    linhas = ["| Técnica testada | P@10 com | P@10 sem | Diferença (IC 95%) | Decisão |",
              "|---|---|---|---|---|"]
    for nome, com, sem in testes:
        linhas.append(f"| {nome} | {_n(cfg[com]['p@10'])} | {_n(cfg[sem]['p@10'])} | "
                      f"{_ic_txt(pp, com, sem)} | descartada |")
    t["descartadas"] = "\n".join(linhas)

    emb = [("E_minilm", "paraphrase-multilingual-MiniLM-L12-v2"),
           ("E_e5_base", "multilingual-e5-base"), ("E_bge_m3", "**bge-m3 (escolhido)**")]
    linhas = ["| Modelo de embedding | P@10 | nDCG@10 | MRR | P@10 contra o bge-m3 (IC 95%) |",
              "|---|---|---|---|---|"]
    for k, nome in emb:
        if k not in cfg:  # índice do modelo ausente nesta execução (retrieval_eval._configs)
            continue
        c = cfg[k]
        ic = "referência" if k == "E_bge_m3" else _ic_txt(pp, k, "E_bge_m3")
        linhas.append(f"| {nome} | {_n(c['p@10'])} | {_n(c['ndcg@10'])} | {_n(c['mrr'])} | "
                      f"{ic} |")
    t["embeddings"] = "\n".join(linhas)

    sem_f, com_f = cfg["V1_hibrido_so_reescrita"], cfg["F1_final_so_reescrita"]
    n_meta = sum(1 for p in perguntas.values() if p.get("filtros_esperados"))
    t["metadados"] = "\n".join([
        f"| {n_meta} perguntas com recorte por metadado | Sem filtros | "
        "Com filtros (sistema final) |",
        "|---|---|---|",
        f"| Conformidade ao recorte (top-10) | {_pct(sem_f['metadados_conformidade@10'])} | "
        f"**{_pct(com_f['metadados_conformidade@10'])}** |",
        f"| P@10 (juiz vê os metadados) | {_n(sem_f['metadados_p@10'])} | "
        f"**{_n(com_f['metadados_p@10'])}** |",
    ])

    ab, ci, fi = ger["abstencao"], ger["citacoes"], ger["fidelidade"]
    n_abster = ab["matriz"]["abstencao_correta"] + ab["matriz"]["resposta_indevida"]
    resp_path = REPORTS_DIR / "respostas_avaliacao.json"
    registros = (json.loads(resp_path.read_text(encoding="utf-8"))
                 if resp_path.exists() else [])
    pc = precisao_citacoes(registros)
    m = ab["matriz"]
    cal = rec["calibracao_limiar"]
    t["geracao"] = "\n".join([
        "| Métrica | Resultado |",
        "|---|---|",
        f"| Decisão responder x abster correta | {_pct(ab['acuracia'])} "
        f"({m['resposta_correta'] + m['abstencao_correta']} de {ger['n_perguntas']}) |",
        f"| Abstenções corretas (fora de escopo + sem evidência) | {m['abstencao_correta']} de "
        f"{n_abster} (IC 95% {_wilson(m['abstencao_correta'], n_abster)}) |",
        f"| Perguntas respondíveis recusadas indevidamente | {m['abstencao_indevida']} de "
        f"{m['abstencao_indevida'] + m['resposta_correta']} |",
        f"| Citações válidas (verificadas por código) | {_pct(ci['citacoes_validas_pct'])} "
        f"de {ci['citacoes_total']} |",
        *([f"| Avaliações citadas que o juiz marcou como evidência clara (relacionadas) | "
           f"{_pct(pc['clara'])} ({_pct(pc['relacionada'])}) de {pc['julgadas']} julgadas |"]
          if pc else []),
        f"| Fidelidade dos insights (juiz; sustentado = 1, parcial = 0,5) | "
        f"{_n(fi['escore_fidelidade'], 2)} em {fi['insights_julgados']} insights |",
        f"| Insights integralmente sustentados (critério estrito) | "
        f"{fi['distribuicao'].get('sustentado', 0)} de {fi['insights_julgados']} "
        f"({_pct(fi['distribuicao'].get('sustentado', 0) / fi['insights_julgados'])}) |",
        f"| Resumos sustentados pelas evidências citadas | "
        f"{_pct(fi['resumos_sustentados_pct'])} |",
        f"| Precisão do contexto enviado ao LLM | {_pct(rec['precisao_contexto_final'])} |",
        f"| Extração correta dos filtros de metadado | "
        f"{_pct(ger['extracao_filtros']['acerto_pct'], 0)} |",
        f"| AUC do reranker contra o juiz | {_n(cal['auc_reranker_vs_juiz'])} |",
    ])

    if registros:
        t["abstencao"] = tabela_abstencao(registros)

    mv = multivendedor(base)
    if mv:
        t["multivendedor"] = (
            f"pedidos com itens de **mais de um vendedor** ({_milhar(mv['documentos'])} "
            f"comentários) têm {_pct(mv['negativos_pct'])} de avaliações negativas, contra "
            f"{_pct(mv['negativos_pct_base'])} na base de comentários"
        )

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

    hum_path = REPORTS_DIR / "concordancia_humana.json"
    if hum_path.exists():
        h = json.loads(hum_path.read_text(encoding="utf-8"))
        t["humano"] = "\n".join([
            f"| Anotação humana x juiz ({h['pares']} pares de {h['perguntas']} perguntas, "
            "estratificados pela nota do juiz) | Resultado |",
            "|---|---|",
            f"| Concordância exata na escala 0/1/2 | {_pct(h['concordancia_exata'])} |",
            f"| Kappa de Cohen ponderado (0/1/2) | {_n(h['kappa_ponderado'])} |",
            f"| Concordância em \"evidência clara\" (decisão usada na P@10) | "
            f"{_pct(h['concordancia_binaria_relevante'])} |",
            f"| Kappa de Cohen nessa decisão | {_n(h['kappa_binario_relevante'])} |",
        ])

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


# Camada que barrou cada recusa (status do pipeline -> camada de abstenção).
CAMADA = {
    "fora_escopo": "1. Escopo (análise da pergunta, antes de buscar)",
    "recorte_vazio": "1. Escopo (análise da pergunta, antes de buscar)",
    "sem_evidencia": "2. Relevância (porteiro: menos de 3 evidências acima do limiar)",
    "evidencia_insuficiente": "2. Relevância (porteiro: menos de 3 evidências acima do limiar)",
    "nao_respondida": "3. Suficiência (geração: evidências não respondem)",
}


def tabela_abstencao(registros: list[dict]) -> str:
    """Quantas recusas cada camada fez, com as perguntas (as respondíveis não aparecem)."""
    por_camada: dict[str, list[str]] = {}
    for r in registros:
        if r["status"] in CAMADA:
            por_camada.setdefault(CAMADA[r["status"]], []).append(r["id"])
    linhas = ["| Camada que recusou | Recusas | Perguntas |", "|---|---|---|"]
    for camada in sorted(por_camada):
        qids = sorted(por_camada[camada])
        linhas.append(f"| {camada} | {len(qids)} | {', '.join(qids)} |")
    return "\n".join(linhas)


def multivendedor(base: dict) -> dict | None:
    """Negativas em pedidos com mais de um vendedor. Calculado da base quando ela existe e
    guardado em base_conhecimento.json, para o README ser reproduzível sem os parquets."""
    from voc_rag.config import DOCUMENTS_PARQUET

    if DOCUMENTS_PARQUET.exists():
        import pandas as pd

        docs = pd.read_parquet(DOCUMENTS_PARQUET, columns=["n_vendedores", "sentimento"])
        neg = docs["sentimento"] == "negativo"
        multi = docs["n_vendedores"] >= 2
        base["multivendedor"] = {
            "documentos": int(multi.sum()),
            "negativos_pct": round(float(neg[multi].mean()), 4),
            "negativos_pct_base": round(float(neg.mean()), 4),
        }
        (REPORTS_DIR / "base_conhecimento.json").write_text(
            json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return base.get("multivendedor")


def _citadas_por_insight(r: dict) -> dict[str, list[int]]:
    """rótulo da evidência -> números dos insights que ela sustenta."""
    mapa: dict[str, list[int]] = {}
    for i, ins in enumerate((r.get("resposta") or {}).get("insights", []), 1):
        for rot in ins["evidencias"]:
            mapa.setdefault(rot, []).append(i)
    return mapa


def _tabela_evidencias(r: dict, com_relevancia: bool = False) -> list[str]:
    mapa = _citadas_por_insight(r)
    ev = [e for e in r.get("evidencias", []) if e["rotulo"] in mapa]
    cab = "| id | sustenta o insight | review_id | nota |"
    sep = "|---|---|---|---|"
    if com_relevancia:
        cab, sep = cab + " relevância |", sep + "---|"
    linhas = [cab + " texto do cliente |", sep + "---|"]
    for e in ev:
        rel = f" {_n(e['relevancia'], 2)} |" if com_relevancia else ""
        linhas.append(
            f"| {e['rotulo']} | {', '.join(map(str, mapa[e['rotulo']]))} | `{e['review_id']}` | "
            f"{e['nota']} |{rel} {_cel(e['texto'])} |")
    return linhas


def exemplo_inline(qid: str) -> str:
    """Exemplo para o README: resposta e todas as evidências citadas, com o insight que cada
    uma sustenta e o review_id completo."""
    registros = json.loads((REPORTS_DIR / "respostas_avaliacao.json").read_text(encoding="utf-8"))
    r = next(x for x in registros if x["id"] == qid)
    linhas = [f"**Pergunta:** {r['pergunta']}", ""]
    linhas += ["> " + ln if ln else ">" for ln in r["markdown"].splitlines()]
    linhas += [""] + _tabela_evidencias(r)
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


def gera_exemplos() -> str:
    registros = json.loads((REPORTS_DIR / "respostas_avaliacao.json").read_text(encoding="utf-8"))
    por_id = {r["id"]: r for r in registros}
    linhas = [
        "# Exemplos de perguntas e respostas",
        "",
        "> Gerado automaticamente por `uv run voc avaliar` a partir de",
        f"> `reports/respostas_avaliacao.json` (todas as {len(registros)} respostas estão lá, "
        "com análise da",
        "> pergunta, filtros, evidências e tempos). Cada evidência é rastreável pelo `review_id`",
        "> na base da Olist; a coluna \"sustenta o insight\" liga cada avaliação aos insights da",
        "> resposta que a citam. \"Apoio: X de N\" diz quantas das N evidências do contexto o",
        "> modelo listou como sustentação do insight (todas validadas por código; o texto mostra",
        "> só as mais representativas entre colchetes).",
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
        if _citadas_por_insight(r):
            n = len(_citadas_por_insight(r))
            linhas += ["", f"<details><summary><b>As {n} evidências citadas</b> (review_id "
                       "completo e insight que cada uma sustenta)</summary>", ""]
            linhas += _tabela_evidencias(r, com_relevancia=True)
            linhas += ["", "</details>"]
        linhas.append("")
    texto = "\n".join(linhas)
    (REPORTS_DIR / "exemplos_perguntas_respostas.md").write_text(texto, encoding="utf-8")
    return texto
