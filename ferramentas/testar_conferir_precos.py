#!/usr/bin/env python3
"""
testar_conferir_precos.py - a conferencia dos precos sabe falhar?

Um arquivo de precos sintetico completo passa; cada falta, cada conta errada e cada
preco sem fonte, velho ou de fora do DF tem de derrubar a verificacao certa. So
biblioteca padrao.
"""
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

import conferir_precos as C

# a Tabela SUS Candanga dos testes, fixa: a da biblioteca muda a cada versao do Anexo
C.tabela_candanga = lambda: {"09.04.01.003-1": [255.61], "09.04.01.001-5": [127.80]}

FICHA = """# SIGTAP 09.04.01.003-1 — OCI Avaliação Diagnóstica de Nasofaringe e de Orofaringe

Lido em 09/10/2026 na Tabela Unificada (competência 09/2026).

| campo | valor |
|---|---|
| **Serviço Ambulatorial** | **R$ 393,55** |
"""

PRECOS = """# Preços — OCI de nasofaringe e orofaringe

**Controle interno: não vai ao documento.**

Plano: planos/redacao_05/ · Pesquisado em 09/10/2026 · Origem do recurso: federal
Oferta inicial: 50% · Teto: 70% · decisão do usuário em 09/10/2026

## 1. Valor que a unidade recebe

| código | nome | valor | fonte |
|---|---|---|---|
| 09.04.01.003-1 | OCI Avaliação Diagnóstica de Nasofaringe e de Orofaringe | R$ 393,55 | SIGTAP 09/2026, `dados/fontes/sigtap_0904010031_092026.md` |

## 2. O que a SES-DF paga

| código | fonte | valor | o que é |
|---|---|---|---|
| 09.04.01.003-1 | convênios de emenda federal aprovados (LI-002) | a tabela, R$ 393,55 | convênio |

## 3. Mercado privado

| código | componente | fonte | endereço | data | local | preço | tipo | inclui |
|---|---|---|---|---|---|---|---|---|
| 09.04.01.003-1 | consulta otorrino | Doctoralia | https://www.doctoralia.com.br/otorrinolaringologista/brasilia | 09/10/2026 | Asa Sul | R$ 250,00 | fixo | consulta |
| 09.04.01.003-1 | consulta otorrino | Clínica A | https://a.example/precos | 01/10/2026 | Taguatinga | R$ 300,00 | fixo | consulta |
| 09.04.01.003-1 | consulta otorrino | Clínica B | https://b.example/otorrino | 05/10/2026 | Águas Claras | R$ 400,00 | a partir de | consulta |
| 09.04.01.003-1 | videolaringoscopia | Doctoralia | https://www.doctoralia.com.br/servicos-de-tratamento/videolaringoscopia/brasilia | 09/10/2026 | Brasília | R$ 200,00 | faixa mín | exame |
| 09.04.01.003-1 | videolaringoscopia | Doctoralia | https://www.doctoralia.com.br/servicos-de-tratamento/videolaringoscopia/brasilia | 09/10/2026 | Brasília | R$ 400,00 | faixa máx | exame |
| 09.04.01.003-1 | videolaringoscopia | Clínica C | https://c.example/exames | 09/10/2026 | fora do DF: São Paulo/SP | R$ 350,00 | fixo | exame |
| 09.04.01.003-1 | laringoscopia | Clínica D | https://d.example/exames | 09/10/2026 | fora do DF: Goiânia/GO | R$ 280,00 | fixo | exame |

## 4. Resumo do mercado

| código | componente | base | na conta | preços | mínimo | mediana | máximo |
|---|---|---|---|---|---|---|---|
| 09.04.01.003-1 | consulta otorrino | DF | sim | 3 | R$ 250,00 | R$ 300,00 | R$ 400,00 |
| 09.04.01.003-1 | videolaringoscopia | DF | sim | 2 | R$ 200,00 | R$ 300,00 | R$ 400,00 |
| 09.04.01.003-1 | videolaringoscopia | fora do DF | sim | 1 | R$ 350,00 | R$ 350,00 | R$ 350,00 |
| 09.04.01.003-1 | laringoscopia | fora do DF | não (alternativa à videolaringoscopia) | 1 | R$ 280,00 | R$ 280,00 | R$ 280,00 |

## 5. A conta

| código | base | valor recebido | mercado mínimo | mercado mediana | cobertura | oferta inicial | teto | margem no teto |
|---|---|---|---|---|---|---|---|---|
| 09.04.01.003-1 | DF | R$ 393,55 | R$ 450,00 | R$ 600,00 | 87% | R$ 196,78 | R$ 275,49 | R$ 118,06 |

## 6. Apoio

Não se aplica: o pré-plano leva só o custo assistencial.

## 7. O que falta

- cotação direta com três clínicas de otorrino do DF.
"""

APOIO = """## 6. Apoio

| posto ou serviço | preço | fonte | data |
|---|---|---|---|
| Coordenação Administrativa-Financeira | R$ 6.000,00 | cargos_no_acervo.md (pt_ses_02) | 09/10/2026 |
| locação de consultório | R$ 2.500,00 | portal A; portal B; portal C | 09/10/2026 |
"""


class Precos(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.plano = Path(self.tmp.name) / "redacao_05"
        (self.plano / "dados" / "fontes").mkdir(parents=True)
        (self.plano / "dados" / "fontes" / "sigtap_0904010031_092026.md").write_text(FICHA, encoding="utf-8")
        self.md = self.plano / "dados" / "precos.md"
        self.escrever(PRECOS)

    def tearDown(self):
        self.tmp.cleanup()

    def escrever(self, txt):
        self.md.write_text(txt, encoding="utf-8")

    def troca(self, de, para):
        self.assertIn(de, PRECOS)
        self.escrever(PRECOS.replace(de, para))

    def falhas(self):
        return {s for s, _, ok, _, na in C.verificar(self.md) if not ok}

    def test_completo_passa(self):
        self.assertEqual(self.falhas(), set())
        na = {s for s, _, ok, _, na in C.verificar(self.md) if na}
        self.assertEqual(na, {"I", "J"})

    def test_sem_a_marca_de_controle_interno(self):
        self.troca("**Controle interno: não vai ao documento.**", "")
        self.assertEqual(self.falhas(), {"A"})

    def test_sem_a_origem_do_recurso(self):
        self.troca(" · Origem do recurso: federal", "")
        self.assertIn("A", self.falhas())

    # 09.04.01.003-1 vale R$ 255,61 na Candanga e R$ 393,55 no SIGTAP de 09/2026: o SIGTAP fica.
    # A pesquisa sintetica e de 09/10/2026; para a regra nova, o corte vai para antes dela
    def nova(self):
        return mock.patch.object(C, "CANDANGA_PARA_TODOS", date(2026, 10, 1))

    def test_pesquisa_antiga_segue_a_regra_de_entao(self):
        self.troca("SIGTAP 09/2026, `dados", "Tabela SUS Candanga, `dados")
        self.assertEqual(self.falhas(), {"B"})
        self.troca("Origem do recurso: federal", "Origem do recurso: distrital")
        self.assertEqual(self.falhas(), {"B"})

    def test_regra_nova_completo_passa(self):
        with self.nova():
            self.assertEqual(self.falhas(), set())

    def test_candanga_com_o_valor_errado(self):
        self.troca("SIGTAP 09/2026, `dados", "Tabela SUS Candanga, `dados")
        with self.nova():
            self.assertEqual(self.falhas(), {"B"})

    def test_a_origem_nao_muda_o_valor(self):
        self.troca("Origem do recurso: federal", "Origem do recurso: distrital")
        with self.nova():
            self.assertEqual(self.falhas(), set())

    def test_sigtap_abaixo_da_candanga(self):
        (self.plano / "dados" / "fontes" / "sigtap_0904010031_092026.md").write_text(
            FICHA.replace("393,55", "200,00"), encoding="utf-8")
        self.troca("| R$ 393,55 | SIGTAP", "| R$ 200,00 | SIGTAP")
        with self.nova():
            self.assertIn("B", self.falhas())

    def test_codigo_fora_da_candanga(self):
        with self.nova(), mock.patch.object(C, "tabela_candanga", lambda: {}):
            self.assertEqual(self.falhas(), {"B"})
            self.troca("SIGTAP 09/2026, `dados", "SIGTAP 09/2026, fora da Tabela SUS Candanga, `dados")
            self.assertEqual(self.falhas(), set())

    def test_valor_diferente_da_ficha(self):
        (self.plano / "dados" / "fontes" / "sigtap_0904010031_092026.md").write_text(
            FICHA.replace("393,55", "200,00"), encoding="utf-8")
        self.assertEqual(self.falhas(), {"B"})

    def test_incremento_sem_a_portaria(self):
        self.troca("SIGTAP 09/2026, `dados", "SIGTAP 09/2026 mais incremento, `dados")
        self.assertEqual(self.falhas(), {"B"})

    def test_ses_vazia_sem_a_frase(self):
        self.troca("| 09.04.01.003-1 | convênios de emenda federal aprovados (LI-002) | a tabela, R$ 393,55 | convênio |\n", "")
        self.assertEqual(self.falhas(), {"C"})

    def test_ses_vazia_com_a_frase_passa(self):
        self.troca("| 09.04.01.003-1 | convênios de emenda federal aprovados (LI-002) | a tabela, R$ 393,55 | convênio |\n",
                   "\nPara a 09.04.01.003-1, nada se achou: SINJ e acervo, 09/10/2026.\n")
        self.assertEqual(self.falhas(), set())

    def test_ses_sem_dizer_de_um_codigo(self):
        self.troca("| 09.04.01.003-1 | convênios de emenda federal aprovados (LI-002) | a tabela, R$ 393,55 | convênio |\n",
                   "\nNada se achou: SINJ e acervo, 09/10/2026.\n")
        self.assertEqual(self.falhas(), {"C"})

    def test_componente_comum_a_dois_codigos_numa_linha(self):
        """a consulta vale para as duas OCI: uma linha, os dois codigos"""
        txt = (PRECOS
               .replace("| 09.04.01.003-1 | OCI Avaliação Diagnóstica de Nasofaringe e de Orofaringe | R$ 393,55 | SIGTAP 09/2026, `dados/fontes/sigtap_0904010031_092026.md` |\n",
                        "| 09.04.01.003-1 | OCI Avaliação Diagnóstica de Nasofaringe e de Orofaringe | R$ 393,55 | SIGTAP 09/2026, `dados/fontes/sigtap_0904010031_092026.md` |\n"
                        "| 09.04.01.001-5 | OCI Déficit Auditivo | R$ 100,00 | SIGTAP 09/2026 |\n")
               .replace("| 09.04.01.003-1 | consulta otorrino | Clínica A |", "| 09.04.01.003-1, 09.04.01.001-5 | consulta otorrino | Clínica A |")
               .replace("| 09.04.01.003-1 | convênios de emenda federal aprovados (LI-002) |",
                        "| 09.04.01.003-1 e 09.04.01.001-5 | convênios de emenda federal aprovados (LI-002) |")
               .replace("| 09.04.01.003-1 | laringoscopia | fora do DF |",
                        "| 09.04.01.001-5 | consulta otorrino | DF | sim | 1 | R$ 300,00 | R$ 300,00 | R$ 300,00 |\n| 09.04.01.003-1 | laringoscopia | fora do DF |")
               .replace("| 09.04.01.003-1 | DF | R$ 393,55 |",
                        "| 09.04.01.001-5 | DF | R$ 100,00 | R$ 300,00 | R$ 300,00 | 33% | R$ 50,00 | R$ 70,00 | R$ 30,00 |\n| 09.04.01.003-1 | DF | R$ 393,55 |"))
        self.escrever(txt)
        self.assertEqual(self.falhas(), set())

    def test_fonoaudiologa_com_nome_na_fonte(self):
        self.troca("| Clínica A | https://a.example/precos |", "| Fonoaudióloga Fulana, SGAS 613 | https://a.example/precos |")
        self.assertEqual(self.falhas(), {"D"})

    def test_preco_sem_endereco(self):
        self.troca("https://a.example/precos", "")
        self.assertEqual(self.falhas(), {"D"})

    def test_tipo_desconhecido(self):
        self.troca("| R$ 300,00 | fixo |", "| R$ 300,00 | aproximado |")
        self.assertEqual(self.falhas(), {"D"})

    def test_cotacao_sem_endereco_com_documento_passa(self):
        self.troca("| https://a.example/precos | 01/10/2026 | Taguatinga | R$ 300,00 | fixo |",
                   "| proposta por e-mail de 01/10/2026 | 01/10/2026 | Taguatinga | R$ 300,00 | cotação |")
        self.assertEqual(self.falhas(), set())

    def test_nome_de_profissional_na_fonte(self):
        self.troca("| Clínica A | https://a.example/precos |", "| Doctoralia: Dra. Fulana de Tal, SGAS 613 | https://a.example/precos |")
        self.assertEqual(self.falhas(), {"D"})

    def test_doutor_no_endereco_nao_e_profissional(self):
        self.troca("| Clínica A | https://a.example/precos |", "| Clínica A, Ed. Dr. Crispim | https://a.example/precos |")
        self.assertEqual(self.falhas(), set())

    def test_mesma_fonte_repetida(self):
        self.troca("| Clínica B | https://b.example/otorrino |", "| Clínica A | https://b.example/otorrino |")
        self.assertEqual(self.falhas(), {"D"})

    def test_alternativa_de_componente_que_nao_existe(self):
        self.troca("não (alternativa à videolaringoscopia)", "não (alternativa à nasofibroscopia)")
        self.assertEqual(self.falhas(), {"F"})

    def test_ses_sem_codigo(self):
        self.troca("| 09.04.01.003-1 | convênios de emenda federal aprovados (LI-002) |",
                   "| a OCI | convênios de emenda federal aprovados (LI-002) |")
        self.assertEqual(self.falhas(), {"C"})

    def test_local_fora_do_df_sem_marca(self):
        self.troca("| Taguatinga |", "| Goiânia |")
        self.assertEqual(self.falhas(), {"E"})

    def test_mediana_errada(self):
        self.troca("| 3 | R$ 250,00 | R$ 300,00 | R$ 400,00 |", "| 3 | R$ 250,00 | R$ 325,00 | R$ 400,00 |")
        self.assertEqual(self.falhas(), {"F"})

    def test_preco_de_fora_no_resumo_do_df(self):
        self.troca("| DF | sim | 2 | R$ 200,00 | R$ 300,00 | R$ 400,00 |", "| DF | sim | 3 | R$ 200,00 | R$ 350,00 | R$ 400,00 |")
        self.assertEqual(self.falhas(), {"F"})

    def test_fora_do_df_sem_resumo(self):
        self.troca("| 09.04.01.003-1 | laringoscopia | fora do DF | não (alternativa à videolaringoscopia) | 1 | R$ 280,00 | R$ 280,00 | R$ 280,00 |\n", "")
        self.assertEqual(self.falhas(), {"F"})

    def test_na_conta_diferente_entre_as_bases(self):
        self.troca("| videolaringoscopia | fora do DF | sim |", "| videolaringoscopia | fora do DF | não |")
        self.assertEqual(self.falhas(), {"F"})

    def test_alternativa_somada_na_conta(self):
        """a laringoscopia e alternativa: se entra na soma, a conta tem de mudar"""
        self.troca("| fora do DF | não (alternativa à videolaringoscopia) |", "| fora do DF | sim |")
        self.assertEqual(self.falhas(), {"G"})

    def test_componente_so_de_fora_entra_na_conta_com_a_base_dita(self):
        """sem preco do DF na videolaringoscopia, a conta usa o de fora e diz isso"""
        txt = PRECOS
        for l in ("| 09.04.01.003-1 | videolaringoscopia | Doctoralia | https://www.doctoralia.com.br/servicos-de-tratamento/videolaringoscopia/brasilia | 09/10/2026 | Brasília | R$ 200,00 | faixa mín | exame |\n",
                  "| 09.04.01.003-1 | videolaringoscopia | Doctoralia | https://www.doctoralia.com.br/servicos-de-tratamento/videolaringoscopia/brasilia | 09/10/2026 | Brasília | R$ 400,00 | faixa máx | exame |\n",
                  "| 09.04.01.003-1 | videolaringoscopia | DF | sim | 2 | R$ 200,00 | R$ 300,00 | R$ 400,00 |\n"):
            self.assertIn(l, txt)
            txt = txt.replace(l, "")
        # consulta 250/300 + videolaringoscopia de fora 350/350: 600 e 650; 393,55/600 = 66%
        txt = txt.replace("| DF | R$ 393,55 | R$ 450,00 | R$ 600,00 | 87% |",
                          "| DF e fora do DF | R$ 393,55 | R$ 600,00 | R$ 650,00 | 66% |")
        self.escrever(txt)
        self.assertEqual(self.falhas(), set())
        self.escrever(txt.replace("| DF e fora do DF |", "| DF |"))
        self.assertEqual(self.falhas(), {"G"})

    def test_cobertura_errada(self):
        self.troca("| 87% |", "| 95% |")
        self.assertEqual(self.falhas(), {"G"})

    def test_teto_errado(self):
        self.troca("| R$ 275,49 | R$ 118,06 |", "| R$ 275,48 | R$ 118,07 |")
        self.assertEqual(self.falhas(), {"G"})

    def test_oferta_a_definir_com_valores(self):
        self.troca("Oferta inicial: 50% · Teto: 70%", "Oferta inicial e teto: a definir")
        self.assertEqual(self.falhas(), {"G"})

    def test_oferta_a_definir_passa(self):
        self.escrever(PRECOS.replace("Oferta inicial: 50% · Teto: 70%", "Oferta inicial e teto: a definir")
                      .replace("| R$ 196,78 | R$ 275,49 | R$ 118,06 |", "| a definir | a definir | a definir |"))
        self.assertEqual(self.falhas(), set())

    def test_preco_velho(self):
        self.troca("| 01/10/2026 | Taguatinga |", "| 01/02/2026 | Taguatinga |")
        self.assertEqual(self.falhas(), {"H"})

    def test_preco_depois_da_pesquisa(self):
        self.troca("| 01/10/2026 | Taguatinga |", "| 11/10/2026 | Taguatinga |")
        self.assertEqual(self.falhas(), {"H"})

    def test_apoio_completo_passa(self):
        self.troca("## 6. Apoio\n\nNão se aplica: o pré-plano leva só o custo assistencial.\n", APOIO)
        self.assertEqual(self.falhas(), set())

    def test_locacao_com_um_orcamento(self):
        self.troca("## 6. Apoio\n\nNão se aplica: o pré-plano leva só o custo assistencial.\n",
                   APOIO.replace("portal A; portal B; portal C", "portal A"))
        self.assertEqual(self.falhas(), {"I"})


# a mesma pesquisa no formato de 25/10/2026: o minimo da APAC, a APAC num so prestador
# e o preco fraco
PRECOS_APAC = (PRECOS.replace("Pesquisado em 09/10/2026", "Pesquisado em 25/10/2026")
               .replace("| consulta otorrino | DF | sim |", "| consulta otorrino | DF | sim, consulta |")
               .replace("| videolaringoscopia | DF | sim |", "| videolaringoscopia | DF | sim, obrigatório |")
               .replace("| videolaringoscopia | fora do DF | sim |", "| videolaringoscopia | fora do DF | sim, obrigatório |")
               .replace("| cobertura | oferta inicial |", "| cobertura | mínimo da APAC | cobertura APAC | oferta inicial |")
               .replace("|---|---|---|---|---|---|---|---|---|\n| 09.04.01.003-1 | DF |",
                        "|---|---|---|---|---|---|---|---|---|---|---|\n| 09.04.01.003-1 | DF |")
               .replace("| 87% | R$ 196,78 |", "| 87% | R$ 450,00 | 87% | R$ 196,78 |")
               .replace("## 6. Apoio", "- 09.04.01.003-1: APAC num só prestador: nenhum prestador do DF faz a APAC mínima inteira\n\n## 6. Apoio"))


class PrecosAPAC(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.plano = Path(self.tmp.name) / "redacao_08"
        (self.plano / "dados" / "fontes").mkdir(parents=True)
        (self.plano / "dados" / "fontes" / "sigtap_0904010031_092026.md").write_text(FICHA, encoding="utf-8")
        self.md = self.plano / "dados" / "precos.md"
        self.md.write_text(PRECOS_APAC, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def com(self, de, para):
        self.assertIn(de, PRECOS_APAC)
        self.md.write_text(PRECOS_APAC.replace(de, para), encoding="utf-8")

    def falhas(self):
        return {s for s, _, ok, _, na in C.verificar(self.md) if not ok}

    def test_apac_completa_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_minimo_da_apac_errado(self):
        self.com("| 87% | R$ 450,00 | 87% |", "| 87% | R$ 400,00 | 98% |")
        self.assertEqual(self.falhas(), {"J"})

    def test_sem_a_apac_num_so_prestador(self):
        self.com("- 09.04.01.003-1: APAC num só prestador: nenhum prestador do DF faz a APAC mínima inteira\n", "")
        self.assertEqual(self.falhas(), {"J"})

    def test_sem_a_consulta_marcada(self):
        self.com("| consulta otorrino | DF | sim, consulta |", "| consulta otorrino | DF | sim |")
        self.assertIn("J", self.falhas())

    def test_minimo_a_partir_de_sem_preco_fraco(self):
        de = "| Asa Sul | R$ 250,00 | fixo |"
        self.com(de, "| Asa Sul | R$ 250,00 | a partir de |")
        self.assertEqual(self.falhas(), {"J"})
        self.md.write_text(PRECOS_APAC.replace(de, "| Asa Sul | R$ 250,00 | a partir de |").replace(
            "## 6. Apoio", "- preço fraco: consulta otorrino, o mínimo é um a partir de\n\n## 6. Apoio"), encoding="utf-8")
        self.assertEqual(self.falhas(), set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
