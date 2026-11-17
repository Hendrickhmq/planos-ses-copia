#!/usr/bin/env python3
"""
testar_conferir_dossie.py - a conferencia do dossie do objeto sabe falhar?

Um dossie sintetico de duas OCI passa; cada parte sem fonte, cada numero que nao bate
com a ficha, a coleta ou os precos, cada conta errada, o comparativo fora de ordem e a
justificativa que fala de dinheiro tem de derrubar a verificacao certa. So biblioteca
padrao.
"""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import conferir_dossie as C

# a Tabela SUS Candanga dos testes, fixa: a da biblioteca muda a cada versao do Anexo.
# A 09.04.01.003-1 esta nela abaixo do SIGTAP (vale a ficha); a 09.04.01.001-5, fora dela
C.tabela_candanga = lambda: {"09.04.01.003-1": [255.61]}


def ficha(codigo, nome, valor):
    return (f"# SIGTAP {codigo} — {nome}\n\nLido em 09/10/2026 (competência 09/2026).\n\n"
            f"| campo | valor |\n|---|---|\n| **Serviço Ambulatorial** | **R$ {valor}** |\n")


COLETA = """# Mapa Social da Saúde — fila das OCIs de otorrino

| conjunto | CID | fila | **pessoas** |
|---|---|---|---|
| **001-5** — audiometria | H60–H95 | 4.276 | **4.276** |
| **003-1** — videoendoscopias | J30–J39 | 3.478 | **3.459** |
"""

PRECOS = """# Preços — OCIs de otorrino

## 5. A conta

| código | base | valor recebido | mercado mínimo | mercado mediana | cobertura | oferta inicial | teto | margem no teto |
|---|---|---|---|---|---|---|---|---|
| 09.04.01.003-1 | DF | R$ 393,55 | R$ 395,50 | R$ 700,00 | 100% | R$ 196,78 | R$ 196,78 | R$ 196,77 |
| 09.04.01.001-5 | DF | R$ 100,00 | R$ 150,00 | R$ 250,00 | 67% | R$ 50,00 | R$ 50,00 | R$ 50,00 |
"""


def pagina(codigo, nome, valor, arq_ficha, pessoas, minimo, mediana, cobertura, margem, qtd, atend, parte, sobra):
    return f"""# Dossiê — {codigo} {nome}

**Controle interno: não vai ao documento.**

## 1. Ficha

| | |
|---|---|
| valor | R$ {valor} |
| idade e sexo | ambos · 0 meses a 130 anos |
| fonte | `dados/fontes/{arq_ficha}` |

## 2. Fila

| | |
|---|---|
| pessoas que se enquadram | {pessoas} |
| espera média | 520 dias |
| fonte | `dados/fontes/mapa_social_20261008.md` |

## 3. Normas

- o valor é o da Tabela SUS Candanga, ou o SIGTAP quando ele é maior (LI-002).

## 4. Aprovados

- pt_ses_04 executa a OCI; apoio de 36,6% do global (AC-075).

## 5. Custo de executar

| | |
|---|---|
| mercado mínimo | R$ {minimo} |
| mercado mediana | R$ {mediana} |
| cobertura | {cobertura} |
| margem no teto | R$ {margem} |
| fonte | `dados/precos.md` |

## 6. A conta

| | |
|---|---|
| recurso | R$ 1.502.687,00 |
| apoio | R$ 123.600,00 |
| OCI que o recurso compra | {qtd} |
| pessoas atendidas | {atend} |
| parte da fila | {parte} |
| sobra do recurso | R$ {sobra} |
"""


P31 = pagina("09.04.01.003-1", "OCI de nasofaringe", "393,55", "sigtap_0904010031_092026.md", "3.459",
             "395,50", "700,00", "100%", "196,77", "3.504", "3.459", "100%", "17.797,55")
P15 = pagina("09.04.01.001-5", "OCI de déficit auditivo", "100,00", "sigtap_0904010015_092026.md", "4.276",
             "150,00", "250,00", "67%", "50,00", "13.790", "4.276", "100%", "951.487,00")

COMPARATIVO = """# Dossiê — OCIs de otorrino: comparativo

**Controle interno: não vai ao documento.**

Ponto de partida: escolher a fila · Recurso: R$ 1.502.687,00, federal · Apoio: R$ 123.600,00 (decisão do usuário em 08/10/2026) · Montado em 01/11/2026

| código | OCI | valor | mercado mínimo | cobertura | margem no teto | pessoas que se enquadram | OCI que o recurso compra | pessoas atendidas | parte da fila | sobra do recurso |
|---|---|---|---|---|---|---|---|---|---|---|
| 09.04.01.003-1 | nasofaringe | R$ 393,55 | R$ 395,50 | 100% | R$ 196,77 | 3.459 | 3.504 | 3.459 | 100% | R$ 17.797,55 |
| 09.04.01.001-5 | déficit auditivo | R$ 100,00 | R$ 150,00 | 67% | R$ 50,00 | 4.276 | 13.790 | 4.276 | 100% | R$ 951.487,00 |
"""

JUSTIFICATIVA = """# Justificativa

A fila de videoendoscopia nasal e videolaringoscopia tem 3.459 pessoas com CID J30 a J39,
com espera média de 520 dias (Mapa Social da Saúde, 08/10/2026). A OCI executa a linha de
cuidado inteira: consulta e exame no mesmo percurso.
"""


class Dossie(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.plano = Path(self.tmp.name) / "redacao_05"
        fontes = self.plano / "dados" / "fontes"
        fontes.mkdir(parents=True)
        (fontes / "sigtap_0904010031_092026.md").write_text(ficha("09.04.01.003-1", "OCI", "393,55"), encoding="utf-8")
        (fontes / "sigtap_0904010015_092026.md").write_text(ficha("09.04.01.001-5", "OCI", "100,00"), encoding="utf-8")
        (fontes / "mapa_social_20261008.md").write_text(COLETA, encoding="utf-8")
        (self.plano / "dados" / "precos.md").write_text(PRECOS, encoding="utf-8")
        self.pasta = self.plano / "dossie"
        self.pasta.mkdir()
        self.escrever(P31, P15, COMPARATIVO, JUSTIFICATIVA)

    def tearDown(self):
        self.tmp.cleanup()

    def escrever(self, p31=None, p15=None, comp=None, just=None):
        for nome, txt in (("0904010031.md", p31), ("0904010015.md", p15),
                          ("comparativo.md", comp), ("justificativa.md", just)):
            if txt is not None:
                (self.pasta / nome).write_text(txt, encoding="utf-8")

    def falhas(self):
        return {s for s, _, ok, _, na in C.verificar(self.pasta) if not ok}

    def test_completo_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_sem_a_pagina_de_uma_oci(self):
        (self.pasta / "0904010015.md").unlink()
        self.assertIn("A", self.falhas())

    def test_sem_o_ponto_de_partida(self):
        self.escrever(comp=COMPARATIVO.replace("Ponto de partida: escolher a fila · ", ""))
        self.assertEqual(self.falhas(), {"A"})

    def test_pessoas_que_nao_estao_na_coleta(self):
        self.escrever(p31=P31.replace("| pessoas que se enquadram | 3.459 |", "| pessoas que se enquadram | 3.500 |"))
        self.assertIn("B", self.falhas())

    def test_ficha_que_nao_existe(self):
        self.escrever(p31=P31.replace("sigtap_0904010031_092026.md", "sigtap_0904010031_082026.md"))
        self.assertIn("B", self.falhas())

    def test_parte_que_falta(self):
        self.escrever(p15=P15.replace("## 4. Aprovados\n\n- pt_ses_04 executa a OCI; apoio de 36,6% do global (AC-075).\n", ""))
        self.assertEqual(self.falhas(), {"B"})

    def test_valor_abaixo_da_candanga(self):
        with mock.patch.object(C, "tabela_candanga", lambda: {"09.04.01.003-1": [450.00]}):
            self.assertIn("C", self.falhas())

    def test_parte_3_sem_a_candanga(self):
        for arq in (self.pasta / "0904010031.md",):
            arq.write_text(arq.read_text(encoding="utf-8").replace("Tabela SUS Candanga", "tabela"), encoding="utf-8")
        self.assertIn("C", self.falhas())

    def test_comparativo_antigo_segue_a_regra_de_entao(self):
        self.escrever(comp=COMPARATIVO.replace("Montado em 01/11/2026", "Montado em 09/10/2026"))
        with mock.patch.object(C, "tabela_candanga", lambda: {"09.04.01.003-1": [450.00]}):
            self.assertEqual(self.falhas(), set())

    def test_valor_diferente_da_ficha(self):
        (self.plano / "dados" / "fontes" / "sigtap_0904010015_092026.md").write_text(
            ficha("09.04.01.001-5", "OCI", "150,00"), encoding="utf-8")
        self.assertEqual(self.falhas(), {"C"})

    def test_custo_diferente_do_precos(self):
        self.escrever(p31=P31.replace("| mercado mínimo | R$ 395,50 |", "| mercado mínimo | R$ 450,00 |"),
                      comp=COMPARATIVO.replace("| R$ 393,55 | R$ 395,50 |", "| R$ 393,55 | R$ 450,00 |"))
        self.assertEqual(self.falhas(), {"D"})

    def test_conta_errada(self):
        self.escrever(p31=P31.replace("| OCI que o recurso compra | 3.504 |", "| OCI que o recurso compra | 3.505 |"),
                      comp=COMPARATIVO.replace("| 3.459 | 3.504 |", "| 3.459 | 3.505 |"))
        self.assertEqual(self.falhas(), {"E"})

    def test_comparativo_diferente_da_pagina(self):
        self.escrever(comp=COMPARATIVO.replace("| 4.276 | 13.790 |", "| 4.276 | 13.791 |"))
        self.assertEqual(self.falhas(), {"F"})

    def test_comparativo_fora_de_ordem(self):
        a = "| 09.04.01.003-1 | nasofaringe | R$ 393,55 | R$ 395,50 | 100% | R$ 196,77 | 3.459 | 3.504 | 3.459 | 100% | R$ 17.797,55 |\n"
        b = "| 09.04.01.001-5 | déficit auditivo | R$ 100,00 | R$ 150,00 | 67% | R$ 50,00 | 4.276 | 13.790 | 4.276 | 100% | R$ 951.487,00 |\n"
        self.escrever(comp=COMPARATIVO.replace(a + b, b + a))
        self.assertEqual(self.falhas(), {"F"})

    def test_sobra_errada(self):
        self.escrever(p15=P15.replace("| sobra do recurso | R$ 951.487,00 |", "| sobra do recurso | R$ 951.000,00 |"),
                      comp=COMPARATIVO.replace("| R$ 951.487,00 |", "| R$ 951.000,00 |"))
        self.assertEqual(self.falhas(), {"E"})

    def test_ordem_e_a_cobertura_e_nao_a_margem(self):
        """a OCI de margem maior e cobertura menor vem depois"""
        p31 = P31.replace("| cobertura | 100% |", "| cobertura | 60% |")
        precos = PRECOS.replace("| R$ 395,50 | R$ 700,00 | 100% |", "| R$ 395,50 | R$ 700,00 | 60% |")
        (self.plano / "dados" / "precos.md").write_text(precos, encoding="utf-8")
        a = "| 09.04.01.003-1 | nasofaringe | R$ 393,55 | R$ 395,50 | 60% | R$ 196,77 | 3.459 | 3.504 | 3.459 | 100% | R$ 17.797,55 |\n"
        b = "| 09.04.01.001-5 | déficit auditivo | R$ 100,00 | R$ 150,00 | 67% | R$ 50,00 | 4.276 | 13.790 | 4.276 | 100% | R$ 951.487,00 |\n"
        comp = COMPARATIVO.replace("| 100% | R$ 196,77 |", "| 60% | R$ 196,77 |")
        self.escrever(p31=p31, comp=comp)
        self.assertEqual(self.falhas(), {"F"})
        self.escrever(comp=comp.replace(a, "").replace(b, b + a))
        self.assertEqual(self.falhas(), set())

    def test_justificativa_com_o_nome_da_oci_passa(self):
        self.escrever(just=JUSTIFICATIVA + "\nA Oferta de Cuidados Integrados reúne consulta e exame.\n")
        self.assertEqual(self.falhas(), set())

    def test_justificativa_com_codigo_do_metodo(self):
        self.escrever(just=JUSTIFICATIVA + "\nA OCI é executada inteira (LI-004).\n")
        self.assertEqual(self.falhas(), {"G"})

    def test_justificativa_com_dinheiro(self):
        self.escrever(just=JUSTIFICATIVA + "\nÉ a OCI que paga melhor, R$ 393,55, perto do mercado.\n")
        self.assertEqual(self.falhas(), {"G"})

    def test_justificativa_com_margem(self):
        self.escrever(just=JUSTIFICATIVA + "\nA margem permite atender mais.\n")
        self.assertEqual(self.falhas(), {"G"})

    def test_justificativa_sem_a_fonte_da_fila(self):
        self.escrever(just=JUSTIFICATIVA.replace(" (Mapa Social da Saúde, 08/10/2026)", ""))
        self.assertEqual(self.falhas(), {"G"})

    def test_justificativa_marcada_como_interna(self):
        self.escrever(just="**Controle interno: não vai ao documento.**\n\n" + JUSTIFICATIVA)
        self.assertEqual(self.falhas(), {"H"})

    def test_pagina_sem_a_marca_de_interno(self):
        self.escrever(p15=P15.replace("**Controle interno: não vai ao documento.**\n", ""))
        self.assertEqual(self.falhas(), {"H"})


# a coleta no formato de 25/10/2026: o teto (5.000) passa da finalidade (3.459), e a
# fila velha dispara (1.459 das 3.459 pessoas so tem pedido de antes da janela)
FILA = "VIDEOENDOSCOPIA NASAL RIGIDA"
COLETA_V2 = {
    "metodo": "2026-10-25", "janela_viva_meses": 24, "filtro_fila": "...", "nomes_internos": {FILA: FILA},
    "filas": {FILA: {"papel": "exame", "generica": False, "fila": 3478, "fila_viva": 2010, "agendadas_12m": 2000,
                     "recortes": {"teto": {"fila": 3478, "fila_viva": 2010, "cid_principais": [["J35", 3000]]},
                                  "fin": {"fila": 3459, "fila_viva": 2000, "cid_principais": [["J35", 3000]]}}}},
    "ocis": {"09.04.01.003-1": {
        "cid_aceito": 'codigo_cid_solicitado={"J3*"}', "cid_finalidade": 'codigo_cid_solicitado={"J35*"}',
        "recorte_teto": "teto", "recorte_finalidade": "fin", "filas": [FILA],
        "teto": {"pessoas": 5000, "pessoas_viva": 3000},
        "finalidade": {"pessoas": 3459, "pessoas_viva": 2000},
        "nucleo": {"pessoas": 900, "pessoas_viva": 800, "como": "consulta de entrada"}}},
}


class DossieFinalidade(Dossie):
    """a pagina da 003-1 cita a coleta de 25/10/2026"""

    def setUp(self):
        import json
        super().setUp()
        fontes = self.plano / "dados" / "fontes"
        (fontes / "mapa_social_20261025.md").write_text(COLETA + "\n| 003-1 | teto 5.000 | finalidade 3.459 | viva 2.000 |\n",
                                                        encoding="utf-8")
        bruto = fontes / "mapa_social_20261025_bruto"
        bruto.mkdir()
        (bruto / "coleta.json").write_text(json.dumps(COLETA_V2), encoding="utf-8")
        self.p31 = P31.replace("mapa_social_20261008.md", "mapa_social_20261025.md").replace(
            "| pessoas que se enquadram | 3.459 |",
            "| medida | finalidade, fila inteira |\n| pessoas que se enquadram | 3.459 |\n"
            "| fila viva | 2.000 |\n| teto (referência) | 5.000 |\n| alarmes | fila velha |")
        self.escrever(p31=self.p31)

    def test_finalidade_com_os_alarmes_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_pagina_com_o_teto(self):
        self.escrever(p31=self.p31.replace("| pessoas que se enquadram | 3.459 |", "| pessoas que se enquadram | 5.000 |"))
        self.assertIn("B", self.falhas())

    def test_alarme_que_nao_esta_na_pagina(self):
        self.escrever(p31=self.p31.replace("| alarmes | fila velha |", "| alarmes | nenhum |"))
        self.assertEqual(self.falhas(), {"B"})

    def test_medida_viva_confere_com_a_viva(self):
        p31 = self.p31.replace("finalidade, fila inteira", "finalidade, fila viva")
        self.escrever(p31=p31)
        self.assertIn("B", self.falhas())        # 3.459 nao e a viva
        self.escrever(p31=p31.replace("| pessoas que se enquadram | 3.459 |", "| pessoas que se enquadram | 2.000 |"))
        self.assertNotIn("B", self.falhas())

    def test_justificativa_com_o_teto(self):
        self.escrever(just=JUSTIFICATIVA + "\nAs filas com CID J30 a J39 reúnem 5.000 pessoas.\n")
        self.assertEqual(self.falhas(), {"G"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
