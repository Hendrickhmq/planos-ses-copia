#!/usr/bin/env python3
"""
testar_extrair_html.py - testes do extrair_html.py.

    python testar_extrair_html.py

So biblioteca padrao. Cada teste monta o pedaco de HTML que importa: o recorte do
ato na pagina do DOU, o texto riscado do Planalto, a tabela que vira CSV e a
quebra de linha do codigo-fonte que nao e quebra do texto.
"""

import tempfile
import unittest
from pathlib import Path

import extrair_html as X

DOU = """<html><head><title>x</title><script>var lixo = 1;</script></head><body>
<nav>menu do portal</nav>
<p class="publicado-dou-data">12/06/2024</p><span class="orgao-dou-data">Ministério da Saúde</span>
<div class="texto-dou"><p class="identifica">PORTARIA SAES/MS Nº 1, DE 1 DE JUNHO DE 2024</p>
<p>Art. 1º Fica incluída a OCI.</p><div><p>Art. 2º Esta Portaria entra em vigor.</p></div>
<table><tr><td>PROCEDIMENTO</td><td>09.03.01.001-1</td></tr><tr><td>Valor</td><td>R$ 100,00</td></tr></table>
</div><footer>rodapé do portal</footer></body></html>"""

PLANALTO = """<html><body><p>Art. 1º Texto
quebrado no meio da linha.</p><p><strike>Art. 2º Redação antiga.</strike></p>
<p>Art. 2º Redação vigente.</p></body></html>"""


class Extracao(unittest.TestCase):

    def extrair(self, html, nome="n"):
        with tempfile.TemporaryDirectory() as td:
            origem = Path(td) / f"{nome}.html"
            origem.write_text(html, encoding="utf-8")
            X.extrair(origem, Path(td) / "saida")
            pasta = Path(td) / "saida" / nome
            tabelas = {p.name: p.read_text(encoding="utf-8") for p in (pasta / "tabelas").glob("*.csv")}
            return (pasta / "texto.md").read_text(encoding="utf-8"), tabelas

    def test_dou_recorta_so_o_ato(self):
        texto, _ = self.extrair(DOU)
        self.assertIn("Art. 1º Fica incluída a OCI.", texto)
        self.assertIn("Art. 2º Esta Portaria entra em vigor.", texto)
        for lixo in ("menu do portal", "rodapé do portal", "var lixo"):
            self.assertNotIn(lixo, texto)
        self.assertIn("Publicação: 12/06/2024 | Ministério da Saúde", texto)

    def test_tabela_vira_csv_com_marcador(self):
        texto, tabelas = self.extrair(DOU)
        self.assertIn("[[tabela: t01]]", texto)
        self.assertEqual(tabelas["t01.csv"], "PROCEDIMENTO,09.03.01.001-1\nValor,\"R$ 100,00\"\n")

    def test_planalto_riscado_e_quebra_de_linha(self):
        texto, _ = self.extrair(PLANALTO)
        self.assertIn("Art. 1º Texto quebrado no meio da linha.", texto)
        self.assertIn("~~Art. 2º Redação antiga.~~", texto)
        self.assertIn("Art. 2º Redação vigente.", texto)

    def test_cp1252_sem_declaracao(self):
        dados = "<p>Atenção à Saúde</p>".encode("cp1252")
        self.assertEqual(X.decodificar(dados), "<p>Atenção à Saúde</p>")


if __name__ == "__main__":
    unittest.main(verbosity=2)
