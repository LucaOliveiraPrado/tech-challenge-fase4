"""Garante que os números do README são cópia fiel dos gerados pela avaliação.

`uv run voc avaliar --etapa exemplos` regenera reports/tabelas_readme.md a partir dos JSON;
cada bloco precisa aparecer literalmente no README.
"""
import re

import pytest

from voc_rag.config import REPORTS_DIR, ROOT

TABELAS = REPORTS_DIR / "tabelas_readme.md"


@pytest.mark.skipif(not TABELAS.exists(), reason="avaliação ainda não executada")
def test_tabelas_do_readme_batem_com_os_json():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    blocos = re.split(r"<!-- (\w+) -->\n", TABELAS.read_text(encoding="utf-8"))[1:]
    for nome, conteudo in zip(blocos[::2], blocos[1::2], strict=True):
        assert conteudo.strip() in readme, f"tabela '{nome}' do README desatualizada"
