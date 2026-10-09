"""Linha de comando: `uv run voc --help`."""
from __future__ import annotations

import json
import logging
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
