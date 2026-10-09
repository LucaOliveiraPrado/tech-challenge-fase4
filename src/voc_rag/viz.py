"""Identidade visual dos gráficos (matplotlib) usada nos notebooks e relatórios.

Paleta validada para daltonismo (ΔE CVD >= 8 entre cores adjacentes); série
única sempre na cor 1; sentimento em escala divergente (vermelho, cinza neutro,
azul); grades em linha fina e sólida; texto nunca na cor da série.
"""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

from voc_rag.config import IMAGES_DIR

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
TINTA_MUDA = "#898781"
GRADE = "#e1e0d9"
EIXO = "#c3c2b7"

CATEGORICAS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]
SERIE = CATEGORICAS[0]
DESTAQUE = CATEGORICAS[1]
SENTIMENTO = {"negativo": "#e34948", "neutro": "#b4b2a9", "positivo": "#2a78d6"}


def aplica_estilo() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": SUPERFICIE,
            "axes.facecolor": SUPERFICIE,
            "savefig.facecolor": SUPERFICIE,
            "figure.dpi": 110,
            "savefig.dpi": 150,
            "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"],
            "font.size": 10,
            "text.color": TINTA,
            "axes.labelcolor": TINTA_2,
            "axes.titlecolor": TINTA,
            "axes.titlesize": 12,
            "axes.titleweight": "semibold",
            "axes.titlelocation": "left",
            "axes.titlepad": 24,
            "axes.edgecolor": EIXO,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRADE,
            "grid.linewidth": 0.8,
            "grid.linestyle": "-",
            "xtick.color": TINTA_MUDA,
            "ytick.color": TINTA_MUDA,
            "xtick.labelcolor": TINTA_2,
            "ytick.labelcolor": TINTA_2,
            "legend.frameon": False,
            "lines.linewidth": 2,
            "lines.solid_capstyle": "round",
            "axes.prop_cycle": mpl.cycler(color=CATEGORICAS),
        }
    )


def subtitulo(ax, texto: str) -> None:
    ax.text(0, 1.02, texto, transform=ax.transAxes, color=TINTA_2, fontsize=9, va="bottom")


def rotula_barras(ax, barras, fmt: str = "{:.0f}", horizontal: bool = False, pad: float = 3):
    for b in barras:
        v = b.get_width() if horizontal else b.get_height()
        if horizontal:
            ax.annotate(fmt.format(v), (v, b.get_y() + b.get_height() / 2),
                        xytext=(pad, 0), textcoords="offset points", va="center",
                        color=TINTA_2, fontsize=9)
        else:
            ax.annotate(fmt.format(v), (b.get_x() + b.get_width() / 2, v),
                        xytext=(0, pad), textcoords="offset points", ha="center",
                        color=TINTA_2, fontsize=9)


def salva(fig, nome: str) -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMAGES_DIR / f"{nome}.png", bbox_inches="tight")
    plt.close(fig)
