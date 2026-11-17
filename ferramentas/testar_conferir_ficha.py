#!/usr/bin/env python3
"""
testar_conferir_ficha.py - a conferencia da ficha do SIGTAP sabe falhar?

Uma ficha sintetica completa passa; cada falta e cada divergencia com o catalogo tem
de derrubar a verificacao certa. So biblioteca padrao.
"""
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

import conferir_ficha as C

FICHA = """# SIGTAP 09.04.01.003-1 — OCI Avaliação Diagnóstica de Nasofaringe e de Orofaringe

Lido em 07/10/2026 na Tabela Unificada (competência 09/2026).

| campo | valor |
|---|---|
| Grupo / subgrupo | 09 — OCI · 04 — Atenção em Otorrinolaringologia |
| Modalidade / complexidade | Ambulatorial · média |
| Financiamento | FAEC (só referência: a emenda não paga por FAEC) |
| Instrumento | APAC |
| Sexo / idade | ambos · 0 meses a 130 anos |
| Quantidade máxima | 1 |
| Atributos | 072 — Exige procedimento de Videolaringoscopia ou Laringoscopia (número: SAES 4.795/2026, art. 1º) |
| Habilitações | 3801 PMAE (descrevem o programa federal) |
| Regras condicionadas | 0009; 0011 |
| CBO | 2251 |
| **Serviço Ambulatorial** | **R$ 393,55** |
| Descrição | consulta médica especializada, videolaringoscopia ou laringoscopia |
| CID principal | J30 a J39 |

## Histórico

| competência | portaria | mudança |
|---|---|---|
| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |

## CID para o Mapa Social

`codigo_cid_solicitado={"J3*"}`
"""

CATALOGO = {"09.04.01.003-1": {"codigo": "09.04.01.003-1", "situacao": "vigente",
                               "valor_total_ambulatorial": "393,55"}}


class Base:
    """a pasta temporaria, o acervo de normas e o cache vazio do pacote"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.md = Path(self.tmp.name) / "sigtap_0904010031_092026.md"
        self.normas = Path(self.tmp.name) / "normas"
        self.normas.mkdir()
        (self.normas / "SAES 4795-2026 atributos e compatibilidades.html").write_text("x", encoding="utf-8")
        # o cache do pacote da Tabela Unificada, vazio: a H nao se aplica
        self.cache_antes = os.environ.get("TABELA_UNIFICADA_DIR")
        os.environ["TABELA_UNIFICADA_DIR"] = str(Path(self.tmp.name) / "cache")
        self.escrever(FICHA)

    def tearDown(self):
        if self.cache_antes is None:
            os.environ.pop("TABELA_UNIFICADA_DIR", None)
        else:
            os.environ["TABELA_UNIFICADA_DIR"] = self.cache_antes
        self.tmp.cleanup()

    def escrever(self, txt):
        self.md.write_text(txt, encoding="utf-8")

    def falhas(self, cat=CATALOGO):
        return {s for s, _, ok, _, na in C.verificar(self.md, cat, self.normas) if not ok}


class Ficha(Base, unittest.TestCase):

    def test_ficha_completa_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_codigo_do_titulo_diferente_do_arquivo(self):
        self.escrever(FICHA.replace("# SIGTAP 09.04.01.003-1", "# SIGTAP 09.04.01.002-3"))
        self.assertIn("A", self.falhas())

    def test_competencia_diferente_do_arquivo(self):
        self.escrever(FICHA.replace("(competência 09/2026)", "(competência 10/2026)"))
        self.assertEqual(self.falhas(), {"B"})

    def test_sem_cbo(self):
        self.escrever(FICHA.replace("| CBO | 2251 |\n", ""))
        self.assertEqual(self.falhas(), {"C"})

    def test_portaria_do_historico_fora_do_acervo(self):
        self.escrever(FICHA.replace("| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |",
                                    "| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |\n"
                                    "| 10/2026 | SAES 9.999/2026 | altera descrição |"))
        self.assertEqual(self.falhas(), {"G"})

    def test_portaria_com_numero_por_extenso_no_nome_do_arquivo(self):
        (self.normas / "PORTARIA SAES_MS No 2.331, DE 10 DE DEZEMBRO DE 2024 - DOU.pdf").write_text("x")
        self.escrever(FICHA.replace("| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |",
                                    "| 01/2025 | SAES 2.331/2024 | exames obrigatórios |\n"
                                    "| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |"))
        self.assertEqual(self.falhas(), set())

    def com_historico(self, *linhas):
        self.escrever(FICHA.replace("| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |",
                                    "\n".join(linhas) + "\n| 09/2026 | SAES 4.795/2026, Anexo I | R$ 393,55 |"))

    def falhas_g(self):
        return next(f for s, _, ok, f, na in C.verificar(self.md, CATALOGO, self.normas) if s == "G")

    def test_mesmo_numero_de_outro_ano_nao_conta(self):
        # a SAS 287/2011 nao e a Portaria 287 de 2022 (fichas do redacao_07, 19/10/2026)
        (self.normas / "Portaria 287 de 07_04_2022.pdf").write_text("x")
        self.com_historico("| 01/2012 | SAS 287/2011 | inclui CBO |")
        self.assertEqual(self.falhas(), {"G"})
        self.assertEqual(self.falhas_g(), ["portaria 287/2011 citada no historico e sem arquivo em biblioteca/normas/"])

    def test_mesmo_numero_e_mesmo_ano_conta(self):
        (self.normas / "Portaria 287 de 07_04_2022.pdf").write_text("x")
        self.com_historico("| 05/2022 | SAES 287/2022 | inclui CBO |")
        self.assertEqual(self.falhas(), set())

    def test_portaria_de_um_ou_dois_digitos(self):
        # a SAS 7/2008 e a GM 15/2018 passavam sem conferencia (fichas do redacao_07, 19/10/2026)
        self.com_historico("| 01/2008 | SAS 7/2008 | inclusão |", "| 01/2018 | GM 15/2018 | quantidade |")
        self.assertEqual(self.falhas_g(), ["portaria 7/2008 citada no historico e sem arquivo em biblioteca/normas/",
                                          "portaria 15/2018 citada no historico e sem arquivo em biblioteca/normas/"])
        (self.normas / "SAS 7-2008 tabela.pdf").write_text("x")
        (self.normas / "GM 15-2018 quantidade.pdf").write_text("x")
        self.assertEqual(self.falhas(), set())

    def test_portaria_com_data_no_nome_do_arquivo(self):
        (self.normas / "Portaria GM_MS 10.297 de 27_02_2026 - emendas individuais RP6.pdf").write_text("x")
        self.com_historico("| 03/2026 | GM/MS nº 10.297/2026 | regra |")
        self.assertEqual(self.falhas(), set())

    def test_sem_quantidade_maxima(self):
        self.escrever(FICHA.replace("| Quantidade máxima | 1 |\n", ""))
        self.assertEqual(self.falhas(), {"C"})

    def test_sem_historico(self):
        self.escrever(FICHA.replace("## Histórico", "## Notas"))
        self.assertEqual(self.falhas(), {"D"})

    def test_sem_expressao_de_cid(self):
        self.escrever(FICHA.replace('`codigo_cid_solicitado={"J3*"}`', "J30 a J39"))
        self.assertEqual(self.falhas(), {"E"})

    def test_catalogo_desatualizado(self):
        velho = {"09.04.01.003-1": dict(CATALOGO["09.04.01.003-1"], valor_total_ambulatorial="200,00")}
        self.assertEqual(self.falhas(velho), {"F"})

    def test_codigo_fora_do_catalogo(self):
        self.assertEqual(self.falhas({}), {"F"})


# o pacote oficial da competencia, com so o que a H le
LAYOUTS = {
    "tb_procedimento": [("CO_PROCEDIMENTO", 10), ("NO_PROCEDIMENTO", 250), ("TP_COMPLEXIDADE", 1), ("TP_SEXO", 1),
                        ("QT_MAXIMA_EXECUCAO", 4), ("QT_DIAS_PERMANENCIA", 4), ("QT_PONTOS", 4),
                        ("VL_IDADE_MINIMA", 4), ("VL_IDADE_MAXIMA", 4), ("VL_SH", 12), ("VL_SA", 12), ("VL_SP", 12),
                        ("CO_FINANCIAMENTO", 2), ("CO_RUBRICA", 6), ("QT_TEMPO_PERMANENCIA", 4), ("DT_COMPETENCIA", 6)],
    "tb_financiamento": [("CO_FINANCIAMENTO", 2), ("NO_FINANCIAMENTO", 100), ("DT_COMPETENCIA", 6)],
    "rl_procedimento_cid": [("CO_PROCEDIMENTO", 10), ("CO_CID", 4), ("ST_PRINCIPAL", 1), ("DT_COMPETENCIA", 6)],
    "rl_procedimento_compativel": [("CO_PROCEDIMENTO_PRINCIPAL", 10), ("CO_REGISTRO_PRINCIPAL", 2),
                                   ("CO_PROCEDIMENTO_COMPATIVEL", 10), ("CO_REGISTRO_COMPATIVEL", 2),
                                   ("TP_COMPATIBILIDADE", 1), ("QT_PERMITIDA", 4), ("DT_COMPETENCIA", 6)],
}


def linha(tabela, **v):
    return "".join(str(v.get(nome, "")).ljust(n)[:n] for nome, n in LAYOUTS[tabela])


def gravar_pacote(pasta, sa="000000039355", cids=None, compat=None):
    pasta.mkdir(parents=True, exist_ok=True)
    cids = cids or [f"J3{i}" for i in range(10)]
    compat = compat or [("0209040041", "1"), ("0209040025", "1"), ("0301010072", "1")]
    with zipfile.ZipFile(pasta / "TabelaUnificada_202609_v2610050950.zip", "w") as z:
        for tab, cols in LAYOUTS.items():
            ini, lay = 1, ["Coluna,Tamanho,Inicio,Fim,Tipo"]
            for nome, n in cols:
                lay.append(f"{nome},{n},{ini},{ini + n - 1},VARCHAR2")
                ini += n
            z.writestr(f"{tab}_layout.txt", "\n".join(lay))
        z.writestr("tb_procedimento.txt", linha(
            "tb_procedimento", CO_PROCEDIMENTO="0904010031", NO_PROCEDIMENTO="OCI NASOFARINGE", TP_COMPLEXIDADE="2",
            TP_SEXO="I", QT_MAXIMA_EXECUCAO="0001", VL_IDADE_MINIMA="0000", VL_IDADE_MAXIMA="1571",
            VL_SH="000000000000", VL_SA=sa, VL_SP="000000000000", CO_FINANCIAMENTO="04", DT_COMPETENCIA="202609"))
        z.writestr("tb_financiamento.txt", linha("tb_financiamento", CO_FINANCIAMENTO="04", NO_FINANCIAMENTO="FAEC"))
        z.writestr("rl_procedimento_cid.txt", "\n".join(
            linha("rl_procedimento_cid", CO_PROCEDIMENTO="0904010031", CO_CID=c, ST_PRINCIPAL="S") for c in cids))
        z.writestr("rl_procedimento_compativel.txt", "\n".join(
            linha("rl_procedimento_compativel", CO_PROCEDIMENTO_PRINCIPAL="0904010031", CO_REGISTRO_PRINCIPAL="06",
                  CO_PROCEDIMENTO_COMPATIVEL=c, CO_REGISTRO_COMPATIVEL="07", TP_COMPATIBILIDADE=tp, QT_PERMITIDA="0001")
            for c, tp in compat))


COMPONENTES = """
| componente | tipo na OCI | quantidade | desde | valor avulso |
|---|---|---|---|---|
| 02.09.04.004-1 videolaringoscopia | compatível (ela **ou** a laringoscopia) | 1 | 09/2026 | R$ 45,50 |
| 02.09.04.002-5 laringoscopia | compatível (ela **ou** a videolaringoscopia) | 1 | 09/2026 | R$ 47,14 |
| 03.01.01.007-2 consulta médica em atenção especializada | compatível | 2 | 07/2024 | R$ 10,00 |

## Histórico"""


class FichaPacote(Base, unittest.TestCase):
    """a ficha contra o pacote oficial da competencia (H)"""

    def setUp(self):
        super().setUp()
        self.cache = Path(os.environ["TABELA_UNIFICADA_DIR"])
        gravar_pacote(self.cache)
        self.ficha = FICHA.replace("\n## Histórico", COMPONENTES)
        self.escrever(self.ficha)

    def test_ficha_completa_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_valor_diferente_do_pacote(self):
        gravar_pacote(self.cache, sa="000000040000")
        self.assertEqual(self.falhas(), {"H"})

    def test_cid_do_pacote_fora_da_expressao(self):
        gravar_pacote(self.cache, cids=[f"J3{i}" for i in range(10)] + ["K00"])
        self.assertEqual(self.falhas(), {"H"})

    def test_obrigatoria_no_pacote_e_compativel_na_ficha(self):
        gravar_pacote(self.cache, compat=[("0209040041", "5"), ("0209040025", "1"), ("0301010072", "1")])
        self.assertEqual(self.falhas(), {"H"})

    def test_componente_da_ficha_que_o_pacote_nao_tem(self):
        gravar_pacote(self.cache, compat=[("0209040041", "1"), ("0301010072", "1")])
        self.assertEqual(self.falhas(), {"H"})


class FichaNova(Base, unittest.TestCase):
    """a ficha lida a partir de 25/10/2026: de onde veio a competencia e as duas expressoes"""

    NOVA = (FICHA.replace("Lido em 07/10/2026 na Tabela Unificada", "Lido em 25/10/2026 na tela da Tabela Unificada")
            .replace('`codigo_cid_solicitado={"J3*"}`',
                     '| | expressão |\n|---|---|\n| aceito | `codigo_cid_solicitado={"J3*"}` |\n'
                     '| finalidade | `codigo_cid_solicitado={"J3*"}` (igual ao aceito) |'))

    def setUp(self):
        super().setUp()
        self.escrever(self.NOVA)

    def test_ficha_completa_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_sem_dizer_de_onde_veio(self):
        self.escrever(self.NOVA.replace("na tela da Tabela Unificada", "na Tabela Unificada"))
        self.assertEqual(self.falhas(), {"B"})

    def test_sem_a_finalidade(self):
        self.escrever(self.NOVA.replace('| finalidade | `codigo_cid_solicitado={"J3*"}` (igual ao aceito) |', ""))
        self.assertEqual(self.falhas(), {"E"})

    def test_capitulo_inteiro_sem_cid_largo(self):
        largo = self.NOVA.replace('| aceito | `codigo_cid_solicitado={"J3*"}` |', '| aceito | `codigo_cid_solicitado={"J*"}` |')
        self.escrever(largo)
        self.assertEqual(self.falhas(), {"E"})
        self.escrever(largo + "\nCID largo: a ficha aceita o capítulo X inteiro.\n")
        self.assertEqual(self.falhas(), set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
