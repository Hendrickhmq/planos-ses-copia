#!/usr/bin/env python3
"""
testar_conferencia.py - testes do conferencia.py.

    python testar_conferencia.py
    python testar_conferencia.py -v

So a biblioteca padrao, e nao toca em nada do projeto: cada teste monta um
documento de mentira numa pasta temporaria.

O que protegem, em ordem de importancia:

1. A MARCACAO CADUCA QUANDO O CONTEUDO MUDA. E a razao de o registro ser
   ancorado em hash e nao um booleano. Um `true` que sobrevive a uma reextracao
   e pior que campo nenhum: afirma "conferido" sobre numero que ninguem viu.
   `test_caduca_quando_o_conteudo_muda` e o teste central.

2. O META.YAML NAO MANDA MAIS NISSO. Reprocessar um documento zerava o
   `tabelas_conferidas` sem avisar. `test_reextracao_nao_apaga_a_marcacao`
   simula a reescrita do meta.yaml e exige que o registro sobreviva.

3. O HASH DO DOCUMENTO INTEIRO VE ARQUIVO ENTRANDO E SAINDO, nao so mudanca de
   conteudo - uma reextracao que detecta uma tabela a mais tem que caducar.
"""

import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import conferencia as C


class Sandbox(unittest.TestCase):
    """Um documento de mentira, com o minimo que o script le."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name) / "extraidos"
        self.doc = self.base / "pt_ses_99"
        (self.doc / "tabelas").mkdir(parents=True)
        self.escrever("texto.md", "texto do plano\n")
        self.escrever("tabelas/p001_t01.csv", "Item,Valor\n1.1.1,100\n")
        self.escrever("tabelas/p002_t01.csv", "Item,Valor\n1.1.2,200\n")
        self.escrever("meta.yaml", 'id: "pt_ses_99"\ndata_extracao: "2026-08-16"\n')
        self.registro = Path(self.tmp.name) / "conferencia.csv"

    def tearDown(self):
        self.tmp.cleanup()

    def escrever(self, rel, conteudo):
        caminho = self.doc / rel
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(conteudo, encoding="utf-8")

    def marcar(self, alvo=C.DOCUMENTO_INTEIRO, por="HB", resultado="ok",
               observacao=""):
        with redirect_stdout(io.StringIO()):
            C.marcar(self.base, "pt_ses_99", alvo, por, resultado, observacao,
                     self.registro)

    def linhas(self):
        return C.ler_registro(self.registro)

    def estado(self, alvo=C.DOCUMENTO_INTEIRO):
        """'vale', 'caducou' ou 'sumiu', comparando com o hash gravado."""
        guardado = next((l.sha256 for l in self.linhas() if l.alvo == alvo), None)
        self.assertIsNotNone(guardado, f"nao ha linha para {alvo}")
        agora = C.hash_alvo(self.doc, alvo)
        if agora is None:
            return "sumiu"
        return "vale" if agora == guardado else "caducou"


class Marcacao(Sandbox):

    def test_marcar_grava_uma_linha_com_o_hash_de_agora(self):
        self.marcar()
        linhas = self.linhas()
        self.assertEqual(len(linhas), 1)
        l = linhas[0]
        self.assertEqual((l.plano, l.pasta, l.alvo, l.conferido_por, l.resultado),
                         ("pt_ses_99", "extraidos", "*", "HB", "ok"))
        self.assertEqual(l.sha256, C.hash_alvo(self.doc, "*"))
        self.assertEqual(self.estado(), "vale")

    def test_marcar_de_novo_substitui_em_vez_de_acumular(self):
        self.marcar(resultado="ok")
        self.marcar(resultado="com_achado", observacao="ver achados.csv")
        linhas = self.linhas()
        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0].resultado, "com_achado")
        self.assertEqual(linhas[0].observacao, "ver achados.csv")

    def test_alvos_diferentes_convivem(self):
        self.marcar(alvo="tabelas/p001_t01.csv")
        self.marcar(alvo="tabelas/p002_t01.csv")
        self.assertEqual(len(self.linhas()), 2)
        self.assertEqual(self.estado("tabelas/p001_t01.csv"), "vale")

    def test_com_achado_continua_conferido(self):
        """Defeito do documento nao deixa o alvo de ser conferido.

        Sao coisas diferentes: `com_achado` diz que a leitura foi feita e o que
        sobrou de errado esta em achados.csv.
        """
        self.marcar(resultado="com_achado")
        self.assertEqual(self.estado(), "vale")
        self.assertEqual(self.linhas()[0].resultado, "com_achado")

    def test_registro_sai_ordenado(self):
        """Ordem estavel: o arquivo e dado versionado, e o diff tem de ser legivel."""
        self.marcar(alvo="tabelas/p002_t01.csv")
        self.marcar(alvo="tabelas/p001_t01.csv")
        self.marcar(alvo="texto.md")
        alvos = [l.alvo for l in self.linhas()]
        self.assertEqual(alvos, sorted(alvos))

    def test_cabecalho_preservado(self):
        self.marcar()
        with self.registro.open(encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), C.CAMPOS)


class Caducidade(Sandbox):

    def test_caduca_quando_o_conteudo_muda(self):
        """O teste central: marcacao amarrada ao conteudo, nao ao nome."""
        self.marcar()
        self.assertEqual(self.estado(), "vale")
        self.escrever("tabelas/p002_t01.csv", "Item,Valor\n1.1.2,999\n")
        self.assertEqual(self.estado(), "caducou")

    def test_caduca_quando_entra_arquivo_novo(self):
        """Reextracao que detecta uma tabela a mais tem que caducar.

        O hash do documento inteiro e o do MANIFESTO, entao ele ve arquivo
        entrando, nao so celula mudando.
        """
        self.marcar()
        self.escrever("tabelas/p003_t01.csv", "Item,Valor\n1.1.3,300\n")
        self.assertEqual(self.estado(), "caducou")

    def test_caduca_quando_sai_arquivo(self):
        self.marcar()
        (self.doc / "tabelas" / "p002_t01.csv").unlink()
        self.assertEqual(self.estado(), "caducou")

    def test_meta_yaml_fica_fora_do_hash(self):
        """Reextracao identica nao pode caducar so pela data_extracao.

        O meta.yaml carrega data e versao do pdfplumber: se entrasse no hash,
        toda marcacao caducaria a cada rodada, por nada.
        """
        self.marcar()
        self.escrever("meta.yaml", 'id: "pt_ses_99"\ndata_extracao: "2027-01-01"\n')
        self.assertEqual(self.estado(), "vale")

    def test_reextracao_nao_apaga_a_marcacao(self):
        """Regressao do bug que motivou o arquivo todo.

        O extrator reescreve o meta.yaml do zero. Antes isso zerava o
        `tabelas_conferidas`; agora a marcacao mora fora e o conteudo nao mudou,
        entao ela continua valendo.
        """
        self.marcar()
        self.escrever("meta.yaml", 'id: "pt_ses_99"\ndata_extracao: "2027-03-09"\n')
        self.assertEqual(len(self.linhas()), 1)
        self.assertEqual(self.estado(), "vale")

    def test_alvo_que_sumiu(self):
        self.marcar(alvo="tabelas/p001_t01.csv")
        (self.doc / "tabelas" / "p001_t01.csv").unlink()
        self.assertEqual(self.estado("tabelas/p001_t01.csv"), "sumiu")

    def test_marcacao_de_um_alvo_nao_caduca_por_causa_de_outro(self):
        self.marcar(alvo="tabelas/p001_t01.csv")
        self.escrever("tabelas/p002_t01.csv", "Item,Valor\n1.1.2,999\n")
        self.assertEqual(self.estado("tabelas/p001_t01.csv"), "vale")


class Relatorio(Sandbox):

    def rodar(self):
        saida = io.StringIO()
        with redirect_stdout(saida):
            C.status(self.base, ["pt_ses_99"], self.registro)
        return saida.getvalue()

    def test_nunca_conferido(self):
        self.assertIn("NUNCA CONFERIDO", self.rodar())

    def test_vale_e_caducou_aparecem(self):
        self.marcar()
        self.assertIn("vale", self.rodar())
        self.escrever("texto.md", "outro texto\n")
        saida = self.rodar()
        self.assertIn("CADUCOU", saida)
        # Nao pode dizer "sem marcacao" dos arquivos que ELE MESMO cobria: eles
        # foram conferidos, o que aconteceu e que o conteudo mudou depois.
        self.assertNotIn("sem marcacao", saida)

    def test_conferencia_parcial_lista_o_que_falta(self):
        self.marcar(alvo="tabelas/p001_t01.csv")
        saida = self.rodar()
        self.assertIn("sem marcacao", saida)
        self.assertIn("texto.md", saida)

    def test_avisa_meta_yaml_com_campo_aposentado(self):
        self.escrever("meta.yaml", 'id: "x"\ntabelas_conferidas: true\n')
        saida = self.rodar()
        self.assertIn("tabelas_conferidas", saida)
        self.assertIn("aposentado", saida)

    def test_nao_avisa_quando_o_meta_esta_limpo(self):
        self.assertNotIn("aposentado", self.rodar())


class RegistroAusente(Sandbox):

    def test_registro_inexistente_nao_e_erro(self):
        """Pasta recem-clonada nao tem o arquivo, e status tem que rodar."""
        self.assertEqual(C.ler_registro(Path(self.tmp.name) / "nao_existe.csv"), [])
        self.assertIn("NUNCA CONFERIDO", Relatorio.rodar(self))

    def test_registro_sem_as_colunas_certas_para_o_script(self):
        self.registro.write_text("plano,alvo\nx,y\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            C.ler_registro(self.registro)


class Pasta(Sandbox):
    """A marcacao pertence a pasta em que a leitura foi feita.

    O pt_ses_05 tem uma leitura em extraidos/ e outra em extraidos_ocr/, com
    conteudo diferente. A conferencia da leitura por OCR aparecia como CADUCOU
    quando o status rodava em extraidos/ - e continuava valendo onde foi feita.
    """

    def outra_pasta(self):
        base = Path(self.tmp.name) / "extraidos_ocr"
        doc = base / "pt_ses_99"
        doc.mkdir(parents=True)
        (doc / "texto.md").write_text("outra leitura\n", encoding="utf-8")
        return base

    def rodar(self, base):
        saida = io.StringIO()
        with redirect_stdout(saida):
            C.status(base, ["pt_ses_99"], self.registro)
        return saida.getvalue()

    def test_marcacao_de_uma_pasta_nao_caduca_na_outra(self):
        self.marcar()
        saida = self.rodar(self.outra_pasta())
        self.assertNotIn("CADUCOU", saida)
        self.assertIn("NUNCA CONFERIDO", saida)
        self.assertIn("ha conferencia em extraidos/", saida)

    def test_as_duas_pastas_convivem_no_registro(self):
        self.marcar()
        with redirect_stdout(io.StringIO()):
            C.marcar(self.outra_pasta(), "pt_ses_99", C.DOCUMENTO_INTEIRO, "HB",
                     "ok", "", self.registro)
        self.assertEqual(sorted(l.pasta for l in self.linhas()),
                         ["extraidos", "extraidos_ocr"])


class RegistroAntigo(Sandbox):
    """O arquivo de antes da coluna `pasta` continua legivel."""

    def escrever_antigo(self, sha):
        self.registro.write_text(
            "plano,alvo,sha256,conferido_por,data,resultado,observacao\n"
            f"pt_ses_99,*,{sha},CC,2026-08-31,ok,\n", encoding="utf-8")

    def test_linha_sem_pasta_e_lida_e_mostrada_com_aviso(self):
        self.escrever_antigo(C.hash_alvo(self.doc, "*"))
        self.assertEqual(self.linhas()[0].pasta, "")
        saida = Relatorio.rodar(self)
        self.assertIn("vale", saida)
        self.assertIn("[sem pasta]", saida)

    def test_marcar_de_novo_migra_a_linha_antiga(self):
        self.escrever_antigo("0" * 64)
        self.marcar()
        linhas = self.linhas()
        self.assertEqual(len(linhas), 1)
        self.assertEqual(linhas[0].pasta, "extraidos")


class FimDeLinha(Sandbox):
    """O mesmo conteudo tem o mesmo hash no Mac e no Windows."""

    def test_texto_com_crlf_nao_caduca(self):
        self.marcar()
        (self.doc / "texto.md").write_bytes(b"texto do plano\r\n")
        self.assertEqual(self.estado(), "vale")

    def test_csv_continua_byte_a_byte(self):
        """CSV sai do modulo csv com CRLF em todo sistema: mexer nisso e mudanca."""
        self.marcar()
        caminho = self.doc / "tabelas" / "p001_t01.csv"
        caminho.write_bytes(caminho.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(self.estado(), "caducou")


if __name__ == "__main__":
    unittest.main(verbosity=2)
