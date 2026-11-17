#!/usr/bin/env python3
"""
testar_tratar.py - testes do tratar_planos.py.

    python testar_tratar.py

So a biblioteca padrao. Os de unidade montam um documento extraido de mentira
numa pasta temporaria; o de integracao reconstroi normalizados/ inteiro a partir
de extraidos/, extraidos_ocr/ e registros/correcoes.csv e exige os mesmos bytes
que estao no repositorio - a promessa do README, "apagar e reconstruir da igual".

O que protegem:

1. A REPRODUCAO. normalizados/ e derivado; se ele diverge do que o tratamento
   produz, alguem editou a mao ou o codigo mudou sem regerar.
2. O LIXO DE RODADA ANTERIOR. CSV que sumiu da extracao nao pode continuar em
   normalizados/.
3. O CABECALHO DE LINHA 0 e a PLANILHA COSTURADA, que trouxeram a planilha do
   pt_ses_05 para o tratamento.
4. O CODIGO DE ITEM nao vira dinheiro: "1.24" nao pode sair "1,24".
"""

import csv
import filecmp
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import tratar_planos as T

from comum import EXTRAIDOS, EXTRAIDOS_OCR, NORMALIZADOS, RAIZ, REGISTROS  # noqa: F401
CABECALHO = ["Item", "DESCRICAO", "Quantidade", "Valor Unitario", "Valor Total"]


def escrever_csv(caminho, linhas):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(linhas)


def ler_csv(caminho):
    with caminho.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


class Documento(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        self.origem = raiz / "extraidos" / "pt_ses_99"
        self.destino = raiz / "normalizados" / "pt_ses_99"
        (self.origem / "tabelas").mkdir(parents=True)
        (self.origem / "texto.md").write_text("# pt_ses_99\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def tratar(self, correcoes=None):
        with redirect_stdout(io.StringIO()):
            return T.tratar_documento("pt_ses_99", self.origem, self.destino,
                                      correcoes or {})

    def correcao(self, arquivo, linha, campo, valor):
        return {(f"pt_ses_99/tabelas/{arquivo}", linha): [(campo, valor, "teste")]}


class Tratamento(Documento):

    def test_decimal_americano_vira_brasileiro(self):
        escrever_csv(self.origem / "tabelas" / "p001_t01.csv",
                     [["a", "b"], ["x", "1,216.00"], ["y", "R$ 1.216,00"]])
        self.tratar()
        linhas = ler_csv(self.destino / "tabelas" / "p001_t01.csv")
        self.assertEqual(linhas[1][1], "1.216,00")
        self.assertEqual(linhas[2][1], "R$ 1.216,00")

    def test_codigo_de_item_nao_vira_dinheiro(self):
        escrever_csv(self.origem / "tabelas" / "p001_t01.csv",
                     [["1.24", "Locacao", "R$ 6.260,00"]])
        self.tratar()
        self.assertEqual(ler_csv(self.destino / "tabelas" / "p001_t01.csv")[0][0], "1.24")

    def test_csv_de_rodada_anterior_e_apagada(self):
        antiga = self.destino / "tabelas" / "p009_t01.csv"
        escrever_csv(antiga, [["sobra"]])
        escrever_csv(self.origem / "tabelas" / "p001_t01.csv", [["a"]])
        self.tratar()
        self.assertFalse(antiga.exists())
        self.assertFalse((self.destino / "planilha.csv").exists())

    def test_correcao_por_numero_e_por_nome_de_coluna(self):
        escrever_csv(self.origem / "tabelas" / "p001_t01.csv",
                     [CABECALHO, ["1.1.1", "Loca cao", "2", "R$ 5,00", "R$ 10,00"]])
        correcoes = self.correcao("p001_t01.csv", 2, "DESCRICAO", "Locacao")
        resumo = self.tratar(correcoes)
        self.assertEqual(resumo["correcoes"], 1)
        self.assertEqual(ler_csv(self.destino / "tabelas" / "p001_t01.csv")[1][1], "Locacao")


class Planilha(Documento):

    ITENS = [["1.1.1", "primeiro", "2", "R$ 50,00", "R$ 100,00"],
             ["SUBTOTAL", "", "", "", "R$ 100,00"],
             ["TOTAL GERAL", "", "", "", "R$ 100,00"]]

    def test_consolidada_pelas_csvs_por_pagina(self):
        escrever_csv(self.origem / "tabelas" / "p001_t01.csv", [CABECALHO] + self.ITENS[:1])
        escrever_csv(self.origem / "tabelas" / "p002_t01.csv", self.ITENS[1:])
        self.tratar()
        planilha = ler_csv(self.destino / "planilha.csv")
        self.assertEqual(planilha[0], ["pagina_origem", "csv_origem"] + CABECALHO)
        self.assertEqual([l[0] for l in planilha[1:]], ["1", "2", "2"])

    def test_costurada_com_cabecalho_de_linha_zero(self):
        """O caso do pt_ses_05: a grade reconstruida nao pegou o cabecalho."""
        escrever_csv(self.origem / "tabelas" / "planilha_p041-p043.csv", self.ITENS)
        correcoes = {("pt_ses_99/tabelas/planilha_p041-p043.csv", 0):
                     [(str(i), nome, "teste") for i, nome in enumerate(CABECALHO, 1)]}
        resumo = self.tratar(correcoes)
        planilha = ler_csv(self.destino / "planilha.csv")
        self.assertEqual(planilha[0][2:], CABECALHO)
        self.assertEqual(planilha[1][:3], ["41-43", "planilha_p041-p043.csv:1", "1.1.1"])
        self.assertEqual(resumo["costurada"], "planilha_p041-p043.csv")
        # a linha 0 so acrescenta: as coordenadas das outras linhas nao mudam
        self.assertEqual(planilha[3][1], "planilha_p041-p043.csv:3")

    def test_costurada_sem_cabecalho_para_com_instrucao(self):
        escrever_csv(self.origem / "tabelas" / "planilha_p041-p043.csv", self.ITENS)
        with self.assertRaises(SystemExit) as ctx:
            self.tratar()
        self.assertIn("linha 0", str(ctx.exception))


class Reproducao(unittest.TestCase):
    """normalizados/ e o que o tratamento produz, byte a byte."""

    def test_normalizados_se_reconstroi_igual(self):
        correcoes, _ = T.ler_correcoes(REGISTROS / "correcoes.csv")
        fontes = T.documentos(EXTRAIDOS)
        fontes.update(T.documentos(EXTRAIDOS_OCR))
        with tempfile.TemporaryDirectory() as td, redirect_stdout(io.StringIO()):
            for doc_id, dir_doc in sorted(fontes.items()):
                T.tratar_documento(doc_id, dir_doc, Path(td) / doc_id, correcoes,
                                   dir_doc.parent.name + "/")
            divergentes = []
            for doc_id in fontes:
                comparar = filecmp.dircmp(NORMALIZADOS / doc_id, Path(td) / doc_id)
                pilha = [comparar]
                while pilha:
                    c = pilha.pop()
                    divergentes += [f"{doc_id}: {x}" for x in
                                    c.left_only + c.right_only + c.diff_files]
                    pilha += c.subdirs.values()
            # dircmp compara por stat; o que ele deu como igual e conferido pelo conteudo
            for doc_id in fontes:
                for arq in (NORMALIZADOS / doc_id).rglob("*"):
                    if arq.is_file():
                        outro = Path(td) / doc_id / arq.relative_to(NORMALIZADOS / doc_id)
                        if outro.exists() and arq.read_bytes() != outro.read_bytes():
                            divergentes.append(f"{doc_id}: {arq.name} (conteudo)")
        self.assertEqual(sorted(set(divergentes)), [],
                         "normalizados/ nao e o que o tratamento produz - rode "
                         "tratar_planos.py extraidos/ normalizados/ e confira o diff")


if __name__ == "__main__":
    unittest.main(verbosity=2)
