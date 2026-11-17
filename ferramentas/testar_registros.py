#!/usr/bin/env python3
"""
testar_registros.py - testes do verificar_registros.py.

    python testar_registros.py

So a biblioteca padrao. Os testes de unidade montam uma pasta de projeto de
mentira; o de integracao exige que os registros de verdade nao tenham erro -
e o que avisa quando uma linha nova entra fora do schema.
"""

import csv
import tempfile
import unicodedata
import unittest
from pathlib import Path

import verificar_registros as V

ACERVO = ["id", "tipo", "especie", "hierarquia", "titulo", "orgao", "instrumento",
          "base_legal", "processo_sei", "plano_relacionado", "data_doc", "situacao",
          "paginas", "arquivo", "url", "data_acesso", "acesso", "extracao_conferida"]


class Projeto(unittest.TestCase):
    """Uma pasta de projeto minima, com uma norma e um plano."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        for pasta in ("registros", V.PASTA_NORMAS, V.PASTAS_ARQUIVO["plano"][0],
                      V.PASTAS_EXTRACAO[0]):
            (raiz / pasta).mkdir(parents=True)
        (raiz / V.PASTA_NORMAS / "Portaria 1.pdf").write_bytes(b"%PDF")
        (raiz / V.PASTAS_ARQUIVO["plano"][0] / "pt_ses_01_x.pdf").write_bytes(b"%PDF")
        self.acervo = [
            self.linha(id="pt_ses_01", tipo="plano", especie="plano_trabalho",
                       situacao="aprovado", arquivo="pt_ses_01_x.pdf"),
            self.linha(id="NM-001", tipo="norma", especie="portaria", hierarquia="4",
                       arquivo="Portaria 1.pdf"),
        ]
        self.achados = []
        self.antigos = (V.RAIZ, V.REG)
        V.RAIZ, V.REG = raiz, raiz / "registros"
        self.raiz = raiz

    def tearDown(self):
        V.RAIZ, V.REG = self.antigos
        self.tmp.cleanup()

    @staticmethod
    def linha(**kw):
        base = {c: "" for c in ACERVO}
        base.update(titulo="t", orgao="o", instrumento="-", situacao="vigente",
                    url="https://exemplo", data_acesso="2026-09-01",
                    acesso="integral", extracao_conferida="sim")
        base.update(kw)
        return base

    def gravar(self, nome, campos, linhas):
        with (self.raiz / "registros" / nome).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            w.writerows(linhas)

    def rodar(self):
        self.gravar("acervo.csv", ACERVO, self.acervo)
        self.gravar("achados.csv", ["id", "acervo_id", "secao", "achado",
                                    "classificacao", "qualidade", "vira_obrigacao_id"],
                    self.achados)
        return V.verificar()


class Acervo(Projeto):

    def test_projeto_limpo_nao_tem_erro_nem_pendencia(self):
        rel = self.rodar()
        self.assertEqual(rel.erros, [])
        self.assertEqual(rel.pendentes, {})

    def test_id_fora_do_padrao(self):
        self.acervo[1]["id"] = "Portaria GM/MS 10.297/2026"
        self.assertTrue(any("fora do padrao" in e for e in self.rodar().erros))

    def test_hierarquia_que_contradiz_a_especie(self):
        self.acervo[1]["hierarquia"] = "3"
        self.assertTrue(any("o schema da 4" in e for e in self.rodar().erros))

    def test_texto_decomposto(self):
        self.acervo[1]["titulo"] = unicodedata.normalize("NFD", "Instrução")
        self.assertTrue(any("NFD" in e for e in self.rodar().erros))

    def test_arquivo_ausente_do_disco(self):
        self.acervo[1]["arquivo"] = "nao existe.pdf"
        self.assertTrue(any(f"nao esta em {V.PASTA_NORMAS}/" in e for e in self.rodar().erros))

    def test_pdf_sem_linha_no_acervo(self):
        (self.raiz / V.PASTA_NORMAS / "Portaria 2.pdf").write_bytes(b"%PDF")
        self.assertTrue(any("sem linha em acervo.csv" in e for e in self.rodar().erros))

    def test_url_ausente_e_pendencia_nao_erro(self):
        """Ninguem inventa URL: o que falta e dado de pessoa, nao defeito."""
        self.acervo[1]["url"] = ""
        rel = self.rodar()
        self.assertEqual(rel.erros, [])
        self.assertIn("NM-001", next(iter(rel.pendentes.values())))


class Achados(Projeto):

    def achado(self, acervo_id, qualidade="falha"):
        self.achados.append({"id": f"AC-{len(self.achados) + 1:03d}", "acervo_id": acervo_id,
                             "secao": "s", "achado": "a", "classificacao": "pratica_ses",
                             "qualidade": qualidade, "vira_obrigacao_id": ""})

    def test_faixa_de_planos_existentes(self):
        self.acervo.append(self.linha(id="pt_ses_02", tipo="plano",
                                      especie="plano_trabalho", situacao="aprovado"))
        self.achado("pt_ses_01..02", qualidade="neutro")
        self.assertEqual(self.rodar().erros, [])

    def test_faixa_com_plano_que_nao_existe(self):
        self.achado("pt_ses_01..03")
        erros = self.rodar().erros
        self.assertTrue(any("pt_ses_02, pt_ses_03" in e for e in erros), erros)


class Licoes(Projeto):
    """A licao aponta para registro que existe e para verificacao que o
    conferir_plano.py tem; sem verificacao automatica, precisa de pergunta."""

    CAMPOS = ("id", "eixo", "tema", "tipo", "gravidade", "regra", "por_que", "origem",
              "verificacao", "pergunta")

    def setUp(self):
        super().setUp()
        (self.raiz / "conferir_plano.py").write_text("def verificar_A(d, r):\n    pass\n",
                                                     encoding="utf-8")
        self.licao = {"id": "LI-001", "eixo": "administracao", "tema": "metas", "tipo": "erro",
                      "gravidade": "questiona", "regra": "r", "por_que": "p",
                      "origem": "NM-001; pt_ses_01", "verificacao": "automatica:A", "pergunta": ""}

    def rodar(self):
        self.gravar("licoes.csv", self.CAMPOS, [self.licao])
        return super().rodar()

    def test_licao_limpa(self):
        self.assertEqual(self.rodar().erros, [])

    def test_origem_que_nao_existe(self):
        self.licao["origem"] = "NM-001; AC-999"
        self.assertTrue(any("AC-999" in e for e in self.rodar().erros))

    def test_letra_que_o_conferir_plano_nao_tem(self):
        self.licao["verificacao"] = "parcial:A,Z"
        self.licao["pergunta"] = "q?"
        self.assertTrue(any("'Z'" in e for e in self.rodar().erros))

    def test_manual_sem_pergunta(self):
        self.licao["verificacao"] = "manual"
        self.assertTrue(any("sem pergunta" in e for e in self.rodar().erros))

    def test_tema_fora_do_schema(self):
        self.licao["tema"] = "diversos"
        self.assertTrue(any("tema 'diversos'" in e for e in self.rodar().erros))


class RegistrosReais(unittest.TestCase):
    """Os registros do projeto seguem o schema."""

    def test_sem_erro(self):
        rel = V.verificar()
        self.assertEqual(rel.erros, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
