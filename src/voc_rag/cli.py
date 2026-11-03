"""Linha de comando: `uv run voc --help`."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

app = typer.Typer(add_completion=False, help="Voice of Customer Intelligence com RAG (Olist).")
console = Console()


def _logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


@app.command()
def prepare(
    zip_path: Path | None = typer.Option(
        None, "--zip", help="archive.zip baixado manualmente (opcional; sem ele baixa do Kaggle)"
    ),
) -> None:
    """Constrói a base de conhecimento (data/processed/*.parquet)."""
    _logging(True)
    from voc_rag.data.prepare import run

    rastro = run(zip_path)
    console.print_json(json.dumps(rastro, ensure_ascii=False))


@app.command()
def build(
    modelo: list[str] = typer.Option(None, "--modelo", help="Modelo(s) de embedding"),
    force: bool = typer.Option(False, help="Recalcula embeddings mesmo se em cache"),
) -> None:
    """Gera embeddings e índices (Chroma + BM25)."""
    _logging(True)
    from voc_rag.indexing.build import build as _build

    console.print_json(json.dumps(_build(modelo or None, force), ensure_ascii=False))


@app.command()
def aspectos(
    n_amostra: int = typer.Option(3000, help="Avaliações rotuladas pelo LLM"),
) -> None:
    """Rotula amostra com LLM, treina o classificador de aspectos e rotula a base."""
    _logging(True)
    from voc_rag.themes.classifier import run

    console.print_json(json.dumps(run(n_amostra), ensure_ascii=False))


@app.command()
def avaliar(
    etapa: str = typer.Option(
        "tudo",
        help="recuperacao | geracao | fidelidade | exemplos | concordancia | humano | latencia"
             " | retidas | tudo"),
) -> None:
    """Avaliação quantitativa (recuperação, geração, abstenção) e exemplos."""
    _logging(True)
    from voc_rag.evaluation import generation_eval, report, retrieval_eval

    if etapa == "retidas":
        # Fora de "tudo" de propósito: o conjunto retido não participa do desenvolvimento.
        from voc_rag.evaluation import holdout

        console.print_json(json.dumps(holdout.run(), ensure_ascii=False, default=str))
        report.gera_tabelas_readme()
        return
    if etapa == "humano":
        from voc_rag.evaluation import agreement

        console.print_json(json.dumps(agreement.run_humano(), ensure_ascii=False, default=str))
        report.gera_tabelas_readme()
        return
    if etapa == "concordancia":
        from voc_rag.evaluation import agreement

        modelo = os.getenv("VOC_SEGUNDO_JUIZ", "gemini-3.5-flash")
        console.print_json(json.dumps(agreement.run(modelo), ensure_ascii=False, default=str))
        return
    if etapa == "latencia":
        console.print_json(json.dumps(generation_eval.mede_latencia(), ensure_ascii=False,
                                      default=str))
        return
    if etapa == "fidelidade":
        # Conclui a auditoria pendente a partir das respostas salvas (sem rodar o pipeline).
        registros = generation_eval.carrega_registros()
        generation_eval.completa_fidelidade(registros)
        console.print_json(json.dumps(generation_eval.resume(registros), ensure_ascii=False,
                                      default=str))
        report.gera_exemplos()
        report.gera_tabelas_readme()
        return
    if etapa in ("recuperacao", "tudo"):
        r = retrieval_eval.run()
        console.print_json(json.dumps(r["configuracoes"], ensure_ascii=False))
    if etapa in ("geracao", "tudo"):
        console.print_json(json.dumps(generation_eval.run(), ensure_ascii=False, default=str))
    if etapa in ("exemplos", "geracao", "tudo"):
        report.gera_exemplos()
        report.gera_tabelas_readme()
        console.print("reports/exemplos_perguntas_respostas.md e tabelas_readme.md atualizados")


@app.command()
def anotacao(
    por_nota: int = typer.Option(20, help="Pares sorteados por nota do juiz (0, 1 e 2)"),
    sobrescrever: bool = typer.Option(False, help="Substitui uma amostra já existente"),
) -> None:
    """Gera eval/anotacao_humana.csv para validar o juiz com anotação humana."""
    from voc_rag.evaluation import agreement

    n = agreement.gera_amostra_humana(por_nota, sobrescrever)
    console.print(f"{n} pares em {agreement.ANOTACAO_CSV}; preencha relevancia_humana e rode "
                  "`uv run voc avaliar --etapa humano`")


@app.command()
def artefatos(
    destino: Path = typer.Option(Path("artefatos.zip"), help="Arquivo .zip a gerar"),
) -> None:
    """Empacota base processada, embeddings bge-m3 e cache do LLM para a release."""
    from voc_rag.artifacts import empacota

    console.print_json(json.dumps(empacota(destino), ensure_ascii=False))


@app.command()
def baixar(
    url: str = typer.Option(None, help="URL do artefatos.zip (padrão: release do repositório)"),
    zip_path: Path | None = typer.Option(None, "--zip", help="artefatos.zip já baixado"),
) -> None:
    """Baixa e extrai os artefatos prontos: dispensa `voc prepare` e a GPU no `voc build`."""
    _logging(True)
    from voc_rag.artifacts import URL_PADRAO, extrai

    console.print_json(json.dumps(extrai(zip_path, url or URL_PADRAO), ensure_ascii=False))


@app.command()
def ask(
    pergunta: str,
    como_json: bool = typer.Option(False, "--json", help="Saída completa em JSON"),
    verbose: bool = typer.Option(False, "-v"),
) -> None:
    """Faz uma pergunta ao pipeline RAG."""
    _logging(verbose)
    from voc_rag.pipeline import VoCPipeline

    r = VoCPipeline().responder(pergunta)
    if como_json:
        console.print_json(json.dumps(r.to_dict(), ensure_ascii=False, default=str))
        return
    console.rule(f"[bold]{r.status}")
    console.print(Markdown(r.markdown))
    if not r.evidencias.empty:
        t = Table(title="Evidências", show_lines=True)
        for c in ("id", "nota", "relev.", "review_id", "texto"):
            t.add_column(c, overflow="fold")
        citadas = set(r.evidencias_citadas["rotulo"])
        for row in r.evidencias.itertuples():
            marca = "*" if row.rotulo in citadas else ""
            t.add_row(f"{row.rotulo}{marca}", str(row.nota), f"{row.relevancia:.2f}",
                      row.review_id[:8], row.texto)
        console.print(t)
    if r.analise:
        console.print(f"[dim]consulta: {r.analise.consulta_busca} | tipo: {r.analise.tipo} | "
                      f"polaridade: {r.analise.polaridade}[/dim]")
    if r.recuperacao:
        console.print(f"[dim]{r.recuperacao.resumo()}[/dim]")
    console.print(f"[dim]tempos: {r.tempos}[/dim]")


if __name__ == "__main__":
    app()
