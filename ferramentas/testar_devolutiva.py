#!/usr/bin/env python3
"""
testar_devolutiva.py - testes do extrair_devolutiva.py.

    python testar_devolutiva.py

So a biblioteca padrao. Cada teste monta um .docx minimo numa pasta
temporaria - so o word/document.xml, que e o que o script le.

O que protegem: o texto que o revisor escreve DENTRO do documento. Com o
controle de alteracoes ligado, o que ele digita fica em w:ins; texto de link
fica em w:hyperlink. O script lia so os runs filhos diretos do paragrafo, e os
dois sumiam da leitura - justamente o que ele existe para achar.
"""

import tempfile
import unittest
import zipfile
from pathlib import Path

import extrair_devolutiva as E

NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def docx(pasta: Path, corpo: str, comentarios: str = "") -> Path:
    caminho = pasta / "d.docx"
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr("word/document.xml",
                   f'<?xml version="1.0"?><w:document {NS}><w:body>{corpo}</w:body></w:document>')
        if comentarios:
            z.writestr("word/comments.xml",
                       f'<?xml version="1.0"?><w:comments {NS}>{comentarios}</w:comments>')
    return caminho


class Leitura(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pasta = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def paragrafo(self, xml):
        doc, _ = E.ler(docx(self.pasta, f"<w:p>{xml}</w:p>"))
        return E.paragrafos(doc)[0]

    def test_texto_de_link_e_lido(self):
        _, _, texto, _, _, _ = self.paragrafo(
            '<w:r><w:t xml:space="preserve">ver </w:t></w:r>'
            '<w:hyperlink><w:r><w:t>portaria</w:t></w:r></w:hyperlink>')
        self.assertEqual(texto, "ver portaria")

    def test_insercao_controlada_e_lida_com_a_cor(self):
        _, _, texto, grifos, _, _ = self.paragrafo(
            '<w:ins w:id="1" w:author="Prof"><w:r><w:rPr><w:highlight w:val="green"/>'
            '</w:rPr><w:t>texto dele</w:t></w:r></w:ins>')
        self.assertEqual(texto, "texto dele")
        self.assertEqual(grifos, [("green", "texto dele")])

    def test_texto_apagado_fica_de_fora(self):
        _, _, texto, _, _, _ = self.paragrafo(
            '<w:r><w:t>fica</w:t></w:r>'
            '<w:del w:id="2"><w:r><w:delText>sai</w:delText></w:r></w:del>')
        self.assertEqual(texto, "fica")

    def test_cor_de_fundo_da_celula(self):
        _, _, _, grifos, _, _ = self.paragrafo(
            '<w:r><w:rPr><w:shd w:fill="F4CCCC"/></w:rPr><w:t>12,00</w:t></w:r>')
        self.assertEqual(grifos, [("#f4cccc", "12,00")])

    def test_comentario_sem_data_nao_quebra(self):
        caminho = docx(self.pasta, "<w:p><w:r><w:t>x</w:t></w:r></w:p>",
                       '<w:comment w:id="0"><w:p><w:r><w:t>veja</w:t></w:r></w:p></w:comment>')
        _, coms = E.ler(caminho)
        self.assertEqual(coms["0"]["data"], "")
        self.assertEqual(coms["0"]["texto"], "veja")


if __name__ == "__main__":
    unittest.main(verbosity=2)
