#!/usr/bin/env python3
"""
testar_conferir.py - testes do conferir.py.

    python testar_conferir.py           tudo
    python testar_conferir.py -v        dizendo o nome de cada teste

So a biblioteca padrao - o conferir.py so exige o pdfplumber quando vai fazer
OCR, e nenhum teste daqui abre PDF: os de unidade usam linhas sinteticas e os
de integracao leem as CSVs que ja estao em normalizados/.

O que estes testes protegem, em ordem de importancia:

1. A ESCADA E UMA SO. O C encadeia paginas de extraidos/ e o I le a planilha.csv
   consolidada, mas os dois sobem a mesma hierarquia pela mesma funcao. Se
   alguem duplicar a logica de novo e as duas divergirem, o relatorio passa a
   afirmar coisas diferentes sobre o mesmo documento - e quem le nao tem como
   saber qual das duas esta certa. `test_C_e_I_concordam` falha nesse caso.

2. O ROTULO PERDIDO. Linha so com valor, sem rotulo e sem descricao, e total, e
   nao item. Ler como item faz o subtotal seguinte contar o valor duas vezes.
   Isso ja aconteceu: acusava R$ 2.338.220,00 de diferenca no pt_ses_04 e a
   diferenca nao existia. `test_rotulo_perdido_nao_conta_duas_vezes` fixa o caso
   com os numeros reais daquele plano.

3. OS PLANOS FECHAM. Teste de integracao sobre normalizados/ - os cinco,
   desde que a planilha do pt_ses_05 passou a chegar pelo tratamento. E o que
   avisa quando um ajuste no extrator ou no tratamento estraga a consolidacao.

4. O CODIGO DO ITEM NAO E FATOR. A D multiplicava o "2141" que o OCR leu sem
   os pontos. `test_codigo_do_item_nao_entra_no_produto` fixa o caso.
"""

import csv
import tempfile
import unittest
from pathlib import Path

import conferir as K

from comum import NORMALIZADOS, RAIZ  # noqa: F401


# --------------------------------------------------------------- unidade -----

class TipoDaLinha(unittest.TestCase):
    """Classificacao de uma linha na hierarquia da planilha."""

    def afirmar(self, linha, tipo, perdido=False):
        self.assertEqual(K.tipo_da_linha(linha), (tipo, perdido), linha)

    def test_item_comum(self):
        self.afirmar(["1.2.1", "Locacao de espaco", "SIGTAP", "Unidade",
                      "1", "12", "R$ 20.000,00", "R$ 240.000,00"], "item")

    def test_item_de_um_nivel(self):
        self.afirmar(["3", "Servico", "", "", "2", "", "R$ 10,00", "R$ 20,00"],
                     "item")

    def test_subtotal_pela_primeira_coluna(self):
        self.afirmar(["SUBTOTAL", "", "", "", "", "", "", "R$ 307.200,00"],
                     "subtotal")

    def test_subtotal_com_hifen_e_caixa_variando(self):
        # 'sub-total', 'Sub-Total Etapa 1.1' e 'SUBTOTAL' sao a mesma coisa.
        for rot in ("sub-total", "Sub-Total Etapa 1.1", "SUBTOTAL", "sub total"):
            self.afirmar([rot, "", "", "", "", "", "", "R$ 1,00"], "subtotal")

    def test_total_geral_com_rotulo_deslocado(self):
        # pt_ses_03 p028:9 - o rotulo foi parar na coluna 'Valor Unitario'.
        self.afirmar(["", "", "", "", "", "", "TOTAL GERAL", "R$ 5.998.920,00"],
                     "total_geral")

    def test_rotulo_de_etapa_sem_valor_nao_e_total(self):
        # 'Etapa 2.4 - Execucao das OCIs' nao abre nem fecha nada sozinho.
        self.afirmar(["Etapa 2.4 - Execucao das OCIs", "", "", "", "", "", "", ""],
                     "item")

    def test_rotulo_perdido(self):
        # pt_ses_04 p050:3 - o sub-total da Etapa 2.3 sem a palavra 'sub-total'.
        self.afirmar(["", "", "", "", "", "", "", "R$ 1.169.110,00"],
                     "subtotal", perdido=True)

    def test_linha_sem_texto_e_sem_valor_nao_vira_total(self):
        self.afirmar(["", "", "", "", "", "", "", ""], "item")

    def test_item_com_valor_mas_sem_codigo_continua_item(self):
        # Tem descricao, entao nao cai na heuristica do rotulo perdido.
        self.afirmar(["", "Rabicho de descricao", "", "", "", "", "",
                      "R$ 100,00"], "item")


class Escada(unittest.TestCase):
    """Subida item -> subtotal -> total de bloco -> total geral."""

    @staticmethod
    def rodar(linhas):
        return K.escada([(f"L{i + 1}", l) for i, l in enumerate(linhas)])

    def test_um_nivel(self):
        testes, perdidos = self.rodar([
            ["1.1.1", "a", "", "", "", "", "", "R$ 100,00"],
            ["1.1.2", "b", "", "", "", "", "", "R$ 200,00"],
            ["SUBTOTAL", "", "", "", "", "", "", "R$ 300,00"],
        ])
        self.assertEqual(perdidos, [])
        self.assertEqual(len(testes), 1)
        nome, origem, declarado, calculado, fonte, n_base = testes[0]
        self.assertEqual((nome, origem, declarado, calculado, n_base),
                         ("SUBTOTAL", "L3", 300.0, 300.0, 2))

    def test_tres_niveis_nao_contam_duas_vezes(self):
        """Total geral fecha contra os totais de bloco, nao contra os itens.

        Somar tudo num nivel so faria o total geral valer 2x - e o pt_ses_01,
        que tem Sub-Total Etapa, Total Meta e Total Geral, acusaria erro.
        """
        testes, _ = self.rodar([
            ["1.1.1", "a", "", "", "", "", "", "R$ 100,00"],
            ["Sub-Total Etapa 1.1", "", "", "", "", "", "", "R$ 100,00"],
            ["1.2.1", "b", "", "", "", "", "", "R$ 400,00"],
            ["Sub-Total Etapa 1.2", "", "", "", "", "", "", "R$ 400,00"],
            ["Total Meta 1", "", "", "", "", "", "", "R$ 500,00"],
            ["Total Geral", "", "", "", "", "", "", "R$ 500,00"],
        ])
        nomes = [t[0] for t in testes]
        self.assertEqual(nomes, ["SUBTOTAL", "SUBTOTAL", "TOTAL", "TOTAL GERAL"])
        for nome, _, declarado, calculado, fonte, n_base in testes:
            self.assertAlmostEqual(declarado, calculado, places=2,
                                   msg=f"{nome} nao fechou ({fonte})")
        self.assertEqual(testes[-1][4], "soma dos totais de meta")

    def test_rotulo_perdido_nao_conta_duas_vezes(self):
        """Regressao do pt_ses_04, com os numeros reais da Etapa 2.3.

        Antes, a linha sem rotulo era lida como item: o subtotal da Etapa 2.4
        somava R$ 1.169.110,00 de novo e acusava R$ 2.338.220,00 de diferenca.
        """
        testes, perdidos = self.rodar([
            ["2.3.1", "risco cirurgico", "", "", "", "", "", "R$ 604.110,00"],
            ["2.3.2", "in loco", "", "", "", "", "", "R$ 250.000,00"],
            ["2.3.3", "progressao", "", "", "", "", "", "R$ 315.000,00"],
            ["", "", "", "", "", "", "", "R$ 1.169.110,00"],          # sem rotulo
            ["Etapa 2.4 - OTORRINOLARINGOLOGIA", "", "", "", "", "", "", ""],
            ["2.4.1", "inicial", "", "", "", "", "", "R$ 625.000,00"],
            ["2.4.2", "progressao", "", "", "", "", "", "R$ 801.000,00"],
            ["sub-total", "", "", "", "", "", "", "R$ 1.426.000,00"],
        ])
        self.assertEqual(perdidos, [("L4", 1169110.0)])
        self.assertEqual([t[0] for t in testes], ["SUBTOTAL", "SUBTOTAL"])
        # O da Etapa 2.3, reconhecido apesar de nao ter rotulo.
        self.assertAlmostEqual(testes[0][2], 1169110.0, places=2)
        self.assertAlmostEqual(testes[0][3], 1169110.0, places=2)
        # E o da 2.4, que so fecha porque o anterior zerou o acumulador.
        self.assertAlmostEqual(testes[1][3], 1426000.0, places=2)

    def test_total_sem_subtotal_fecha_contra_os_itens(self):
        testes, _ = self.rodar([
            ["1.1.1", "a", "", "", "", "", "", "R$ 100,00"],
            ["1.1.2", "b", "", "", "", "", "", "R$ 200,00"],
            ["Total Geral", "", "", "", "", "", "", "R$ 300,00"],
        ])
        self.assertEqual(testes[0][4], "soma dos itens")
        self.assertAlmostEqual(testes[0][3], 300.0, places=2)

    def test_subtotal_sem_itens_e_nao_verificavel(self):
        """n_base == 0 nao e o mesmo que teste que falhou."""
        testes, _ = self.rodar([
            ["SUBTOTAL", "", "", "", "", "", "", "R$ 300,00"],
        ])
        self.assertEqual(testes[0][5], 0)
        res = {"ok": 0, "falha": 0, "nao_verificavel": 0}
        K.contar(testes, res)
        self.assertEqual(res, {"ok": 0, "falha": 0, "nao_verificavel": 1})

    def test_diferenca_real_e_acusada(self):
        testes, _ = self.rodar([
            ["1.1.1", "a", "", "", "", "", "", "R$ 100,00"],
            ["SUBTOTAL", "", "", "", "", "", "", "R$ 999,00"],
        ])
        res = {"ok": 0, "falha": 0, "nao_verificavel": 0}
        K.contar(testes, res)
        self.assertEqual(res["falha"], 1)


class ProdutoPorLinha(unittest.TestCase):
    """A D: total da linha = produto dos fatores da propria linha."""

    def rodar(self, linha):
        doc = DocumentoFalso(".", {1: [(Path("p001_t01.csv"), [linha])]})
        return K.verificar_D(doc)

    def test_codigo_do_item_nao_entra_no_produto(self):
        """O OCR leu 2.1.1 como "2141": o produto saia 2141 vezes maior."""
        r = self.rodar(["2141", "Consulta", "Unidade", "8.400", "1",
                        "R$ 200,00", "R$ 1.680.000,00"])
        self.assertEqual((r["ok"], r["falha"]), (1, 0))

    def test_codigo_lido_como_dinheiro_tambem_fica_fora(self):
        r = self.rodar(["1.24", "Locacao", "Mes", "1", "2", "R$ 6.260,00", "R$ 12.520,00"])
        self.assertEqual((r["ok"], r["falha"]), (1, 0))

    def test_produto_errado_continua_acusado(self):
        r = self.rodar(["1.1.1", "x", "Unidade", "2", "1", "R$ 10,00", "R$ 30,00"])
        self.assertEqual(r["falha"], 1)


class MarcadorDePagina(unittest.TestCase):
    """O texto.md dos dois extratores separa as paginas do mesmo jeito."""

    def test_os_dois_formatos(self):
        with tempfile.TemporaryDirectory() as td:
            caminho = Path(td) / "texto.md"
            caminho.write_text("# x\n<!-- pagina 1 -->\num\n"
                               "<!-- pagina 2 | confianca OCR 91.0 -->\ndois\n",
                               encoding="utf-8")
            paginas = K.ler_texto_md(caminho)
        self.assertEqual([t for _, t in paginas[1]], ["um"])
        self.assertEqual([t for _, t in paginas[2]], ["dois"])


class Sequencia(unittest.TestCase):
    """Numeracao dos itens: buraco significa linha perdida."""

    @staticmethod
    def rodar(codigos):
        return K.conferir_sequencia(
            [(f"L{i}", [c, "desc", "", "", "", "", "", "R$ 1,00"])
             for i, c in enumerate(codigos, 1)])

    def test_integra(self):
        self.assertEqual(self.rodar(["1.1.1", "1.1.2", "1.2.1", "1.2.2", "2.1.1"]),
                         ([], []))

    def test_buraco_no_meio(self):
        buracos, repetidos = self.rodar(["1.1.1", "1.1.3"])
        self.assertEqual(buracos, ["1.1.2"])
        self.assertEqual(repetidos, [])

    def test_buraco_no_comeco(self):
        buracos, _ = self.rodar(["1.1.2", "1.1.3"])
        self.assertEqual(buracos, ["1.1.1"])

    def test_repeticao(self):
        buracos, repetidos = self.rodar(["1.1.1", "1.1.2", "1.1.2"])
        self.assertEqual(buracos, [])
        self.assertEqual([c for c, _ in repetidos], ["1.1.2", "1.1.2"])

    def test_etapas_independentes(self):
        """1.1.x ir ate 13 nao exige que 1.2.x tambem va."""
        self.assertEqual(self.rodar(["1.1.1", "1.1.2", "1.1.3", "1.2.1"]),
                         ([], []))

    def test_linha_sem_codigo_e_ignorada(self):
        self.assertEqual(
            K.conferir_sequencia([
                ("L1", ["1.1.1", "d", "", "", "", "", "", "R$ 1,00"]),
                ("L2", ["SUBTOTAL", "", "", "", "", "", "", "R$ 1,00"]),
                ("L3", ["1.1.2", "d", "", "", "", "", "", "R$ 1,00"]),
            ]),
            ([], []))


# ------------------------------------------------------------ equivalencia ---

class DocumentoFalso:
    """O minimo que verificar_C e verificar_I usam. Nao abre PDF."""

    def __init__(self, dir_doc, tabelas):
        self.dir = Path(dir_doc)
        self.tabelas = tabelas
        self.paginas_com_tabela = sorted(tabelas)

    def rel(self, caminho):
        return Path(caminho).name


class EquivalenciaCeI(unittest.TestCase):
    """O C e o I tem que subir a MESMA escada sobre o mesmo conteudo.

    Este e o teste que impede a duplicacao de voltar. Monta uma planilha que
    atravessa duas paginas, entrega as CSVs por pagina ao C e a consolidada ao
    I, e exige o mesmo veredito.
    """

    PAGINA_1 = [
        ["Item", "DESCRICAO", "REFERENCIA", "Unidade", "Quantidade",
         "Frequencia", "Valor Unitario", "Valor Total"],
        ["Etapa 1.1", "", "", "", "", "", "", ""],
        ["1.1.1", "primeiro", "SIGTAP", "Unidade", "2", "", "R$ 50,00",
         "R$ 100,00"],
    ]
    PAGINA_2 = [
        ["1.1.2", "segundo", "SIGTAP", "Unidade", "4", "", "R$ 50,00",
         "R$ 200,00"],
        ["SUBTOTAL", "", "", "", "", "", "", "R$ 300,00"],
        ["", "", "", "", "", "", "", "R$ 300,00"],      # total geral sem rotulo
    ]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        (raiz / "tabelas").mkdir()
        for nome, linhas in (("p001_t01.csv", self.PAGINA_1),
                             ("p002_t01.csv", self.PAGINA_2)):
            with (raiz / "tabelas" / nome).open("w", newline="",
                                                encoding="utf-8") as f:
                csv.writer(f).writerows(linhas)
        # A consolidada: cabecalho unico, procedencia na frente, sem o rotulo
        # de etapa que nao carrega valor.
        consolidada = [["pagina_origem", "csv_origem"] + self.PAGINA_1[0]]
        for n, linha in enumerate(self.PAGINA_1[1:], 2):
            consolidada.append(["1", f"p001_t01.csv:{n}"] + linha)
        for n, linha in enumerate(self.PAGINA_2, 1):
            consolidada.append(["2", f"p002_t01.csv:{n}"] + linha)
        with (raiz / "planilha.csv").open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(consolidada)

        self.doc = DocumentoFalso(raiz, {
            1: [(raiz / "tabelas" / "p001_t01.csv", self.PAGINA_1)],
            2: [(raiz / "tabelas" / "p002_t01.csv", self.PAGINA_2)],
        })

    def tearDown(self):
        self.tmp.cleanup()

    def test_mesmos_totais_e_mesmo_veredito(self):
        c = K.verificar_C(self.doc)
        i = K.verificar_I(self.doc)
        # Origem e formatada diferente nos dois - o resto tem que bater.
        sem_origem = lambda testes: [(t[0], t[2], t[3], t[4], t[5]) for t in testes]
        self.assertEqual(sem_origem(c["cadeias"][0]["testes"]),
                         sem_origem(i["testes"]))
        for chave in ("ok", "falha", "nao_verificavel"):
            self.assertEqual(c[chave], i[chave], chave)

    def test_os_dois_veem_o_rotulo_perdido(self):
        c = K.verificar_C(self.doc)
        i = K.verificar_I(self.doc)
        self.assertEqual(len(c["rotulos_perdidos"]), 1)
        self.assertEqual([v for _, v in c["rotulos_perdidos"]],
                         [v for _, v in i["rotulos_perdidos"]])

    def test_item_que_atravessa_a_pagina_entra_no_subtotal(self):
        """O 1.1.2 esta na pagina 2 e o subtotal so fecha se ele for contado."""
        i = K.verificar_I(self.doc)
        subtotal = next(t for t in i["testes"] if t[0] == "SUBTOTAL")
        self.assertEqual(subtotal[5], 2, "o subtotal tem que somar 2 itens")
        self.assertAlmostEqual(subtotal[2], subtotal[3], places=2)


# ------------------------------------------------------------ integracao -----

def planos_normalizados():
    if not NORMALIZADOS.is_dir():
        return []
    return sorted(d for d in NORMALIZADOS.iterdir()
                  if (d / "planilha.csv").exists())


class PlanosReais(unittest.TestCase):
    """Os quatro planos de normalizados/ continuam fechando.

    Avisa quando um ajuste no extrair_planos.py ou no tratar_planos.py estraga
    a consolidacao - a falha aparece aqui antes de virar numero errado numa
    ficha.
    """

    def setUp(self):
        self.planos = planos_normalizados()
        if not self.planos:
            self.skipTest("normalizados/ vazio - rode o tratar_planos.py antes")

    def test_numeracao_integra(self):
        for dir_plano in self.planos:
            with self.subTest(plano=dir_plano.name):
                doc = DocumentoFalso(dir_plano, {})
                r = K.verificar_I(doc)
                self.assertEqual(r["buracos"], [], "item faltando na consolidada")
                self.assertEqual(r["repetidos"], [], "item repetido")

    def test_hierarquia_fecha(self):
        for dir_plano in self.planos:
            with self.subTest(plano=dir_plano.name):
                r = K.verificar_I(DocumentoFalso(dir_plano, {}))
                falhas = [t for t in r["testes"]
                          if t[5] and not K.perto(t[2], t[3])]
                self.assertEqual(falhas, [], "total que nao fecha")
                self.assertGreater(r["ok"], 0, "nenhum total conferido")

    def test_termina_em_total_geral(self):
        """Consolidada truncada e cadeia que parou antes do fim da planilha."""
        for dir_plano in self.planos:
            with self.subTest(plano=dir_plano.name):
                r = K.verificar_I(DocumentoFalso(dir_plano, {}))
                self.assertEqual(r["termina_em"], "total_geral")

    def test_sem_planilha_a_verificacao_nao_se_aplica(self):
        """Rodar em extraidos/ nao pode virar falha - la nao ha planilha.csv."""
        with tempfile.TemporaryDirectory() as vazio:
            self.assertIsNone(K.verificar_I(DocumentoFalso(vazio, {})))


if __name__ == "__main__":
    unittest.main(verbosity=2)
