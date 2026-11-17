#!/usr/bin/env python3
"""
testar_consultar.py - testes do consultar.py sobre os registros de verdade.

    python testar_consultar.py

So a biblioteca padrao. O que se exige: o criterios.md esta em dia com o
licoes.csv; as referencias andam nos dois sentidos, e o achado desmentido aponta
para quem o desmente; a busca ignora acento; o checklist so marca como feito o
que o conferir_plano.py conferiu e passou.
"""

import unittest

import consultar as C
import verificar_registros as V


class Consulta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base = C.Base()

    def test_criterios_em_dia(self):
        atual = C.CRITERIOS.read_text(encoding="utf-8")
        self.assertEqual(atual, C.gerar_criterios(self.base),
                         "rode: python consultar.py criterios")

    def test_destilados_so_citam_registro_que_existe(self):
        """o modelo e a nota do CNES apontam para licoes, obrigacoes e pecas; id que
        some dos registros deixa o documento apontando para o nada"""
        import re
        from comum import BIBLIOTECA, METODO
        for caminho in (METODO / "plano" / "modelo.md", METODO / "plano" / "procedimento.md",
                        BIBLIOTECA / "instrumento" / "enquadramento_cnes.md",
                        BIBLIOTECA / "instrumento" / "fluxo_emenda.md"):
            nome = caminho.name
            texto = caminho.read_text(encoding="utf-8")
            citados = set(re.findall(r"\b(?:LI|AC|OB|CT|IT|NM|DD|EX)-\d{3}\b", texto))
            self.assertTrue(citados, nome)
            faltam = sorted(i for i in citados if i not in self.base.reg)
            self.assertEqual(faltam, [], f"{nome} cita ids que nao existem")

    def test_temas_espelham_o_schema(self):
        self.assertEqual({t for t, _ in C.TEMAS}, V.LICAO_TEMA)

    def test_referencia_nos_dois_sentidos(self):
        self.assertIn("AC-014", self.base.cita["AC-058"])
        self.assertIn("AC-058", self.base.citado_por["AC-014"])

    def test_achado_desmentido_aponta_quem_desmente(self):
        self.assertEqual(C.revisto_por(self.base, "AC-014"), ["AC-058"])
        self.assertEqual(C.revisto_por(self.base, "AC-041"), ["AC-042"])
        self.assertEqual(C.revisto_por(self.base, "AC-070"), [])

    def test_faixa_de_planos(self):
        self.assertEqual(C.expandir("pt_ses_02..04"), ["pt_ses_02", "pt_ses_03", "pt_ses_04"])
        self.assertIn("AC-071", [a["id"] for a in self.base.achados_do_plano("pt_ses_03")])

    def test_busca_ignora_acento_e_caixa(self):
        com = [i for i, _ in C.buscar(self.base, ["LOCAÇÃO"])]
        sem = [i for i, _ in C.buscar(self.base, ["locacao"])]
        self.assertTrue(com)
        self.assertEqual(com, sem)

    def test_checklist_sem_plano_nao_marca_nada(self):
        texto, falhas = C.checklist(self.base)
        self.assertEqual(falhas, 0)
        self.assertNotIn("- [x]", texto)
        for l in self.base.licoes():
            self.assertIn(f"**{l['id']}**", texto)

    def test_checklist_marca_o_que_falhou(self):
        vered = {x: "PASSOU" for x in "ABCDEFGHIJKLMNOPQRSTUVWX"}
        vered["W"] = "FALHOU"
        antigo = C.rodar_conferencia
        C.rodar_conferencia = lambda plano: (vered, "")
        try:
            texto, falhas = C.checklist(self.base, "redacao_xx")
        finally:
            C.rodar_conferencia = antigo
        self.assertGreater(falhas, 0)
        linha = next(l for l in texto.splitlines() if "**LI-001**" in l)
        self.assertTrue(linha.startswith("- [ ]") and "FALHOU" in linha, linha)
        # automatica que passou fica marcada; parcial que passou continua aberta
        auto = next(l for l in self.base.licoes() if l["verificacao"].startswith("automatica")
                    and "W" not in l["verificacao"])
        parc = next(l for l in self.base.licoes() if l["verificacao"].startswith("parcial")
                    and "W" not in l["verificacao"])
        linhas = texto.splitlines()
        self.assertTrue(next(x for x in linhas if f"**{auto['id']}**" in x).startswith("- [x]"))
        self.assertTrue(next(x for x in linhas if f"**{parc['id']}**" in x).startswith("- [ ]"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
