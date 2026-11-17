#!/usr/bin/env python3
"""
testar_ler_controle.py - a leitura do controle externo acha e classifica certo?

Sem rede: um trecho de ata do TCDF no DODF, a listagem de pastas do DODF e paginas de feed
sinteticas. So biblioteca padrao.
"""
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

import ler_controle as L

VIG = {"nomes": {"ISHP", "IEV"}, "numeros": {"030989/2026"}}

ATA = """TRIBUNAL DE CONTAS
PROCESSO Nº 00600-00002022/2026-83-e - Representação ofertada pelo Deputado Federal X, versando sobre
projetos da Secretaria de Estado de Saúde do Distrito Federal – SES/DF (mediante Termos de Fo-
mento nºs 10/2024 e 01/2025), financiados com emendas parlamentares. DECISÃO Nº 715/2026 - O
Tribunal, por unanimidade, decidiu: I - tomar conhecimento; II - determinar à SES/DF que apresente
esclarecimentos.
PROCESSO Nº 00600-00001408/2026-78-e - Aposentadoria de FULANA DE TAL, servidora da Secretaria de
Estado de Saúde do Distrito Federal. DECISÃO Nº 733/2026 - O Tribunal, por unanimidade, decidiu
considerar legal a concessão.
PROCESSO Nº 00600-00000999/2026-11-e - Pregão da Secretaria de Estado de Saúde do Distrito Federal
para compra de luvas. DECISÃO Nº 740/2026 - O Tribunal, por unanimidade, decidiu tomar conhecimento.
PROCESSO Nº 00600-00000888/2026-22-e - Edital da Sedes para restaurantes comunitários.
DECISÃO Nº 741/2026 - O Tribunal decidiu tomar conhecimento.
PROCESSO Nº 00600-00000777/2026-33-e - Processo citado sem decisão nesta ata.
"""

LISTAGEM = """<html><head><title>DODF - Sistema de busca do novo Diário Oficial do Distrito Federal</title></head>
<a href="/dodf/jornal/visualizar-pdf?pasta=2026/10_Outubro/DODF 189 09-10-2026|&amp;arquivo=DODF 189 09-10-2026 INTEGRA.pdf ">a</a>
<a href="/dodf/jornal/visualizar-pdf?pasta=2026/10_Outubro/DODF 114 09-10-2026 EDICAO EXTRA A|&amp;arquivo=DODF 114 09-10-2026 EDICAO EXTRA A.pdf">b</a>
</html>"""


def feed(itens):
    corpo = "".join(f"<item><title>{t}</title><link>https://x/{i}</link><pubDate>{d}</pubDate>"
                    f"<description>{desc}</description></item>" for i, (t, d, desc) in enumerate(itens))
    return f'<?xml version="1.0"?><rss version="2.0"><channel>{corpo}</channel></rss>'.encode()


class Decisoes(unittest.TestCase):

    def test_so_os_blocos_com_decisao_do_tribunal(self):
        ds = L.decisoes(ATA)
        self.assertEqual([d["decisao"] for d in ds], ["715/2026", "733/2026", "740/2026", "741/2026"])
        self.assertEqual(ds[0]["processo"], "00600-00002022/2026-83")

    def test_o_bloco_para_no_processo_de_numero_antigo_e_no_relator(self):
        """a Representacao 14/2026 (SECTI) engolia a auditoria da SES que vinha depois"""
        ata = ("PROCESSO Nº 00600-00010449/2026-55-e - Representação nº 14/2026 – G4P, sobre a capacidade da "
               "SECTI/DF para analisar prestações de contas de parcerias (MROSC). DECISÃO Nº 2784/2026 - O "
               "Tribunal, por unanimidade, decidiu conhecer. RELATADO(S) PELA CONSELHEIRA X PROCESSO Nº "
               "29590/2013-e - Auditoria na Secretaria de Estado de Saúde do Distrito Federal – SES/DF. "
               "DECISÃO Nº 2785/2026 - O Tribunal decidiu tomar conhecimento.")
        ds = L.decisoes(ata)
        self.assertEqual([d["decisao"] for d in ds], ["2784/2026", "2785/2026"])
        self.assertNotIn("SES/DF", ds[0]["texto"])
        self.assertIsNone(L.classificar(ds[0]["texto"], VIG)[0])
        self.assertEqual(ds[1]["processo"], "29590/2013")

    def test_assunto_e_palavra_partida(self):
        d = L.decisoes(ATA)[0]
        self.assertTrue(d["assunto"].startswith("Representação ofertada"))
        self.assertIn("Termos de Fomento", d["texto"])

    def test_ato_de_pessoal_e_reconhecido(self):
        assuntos = [d["assunto"] for d in L.decisoes(ATA)]
        self.assertTrue(L.ato_de_pessoal(assuntos[1]))
        self.assertFalse(L.ato_de_pessoal(assuntos[0]))
        self.assertTrue(L.ato_de_pessoal("Duas concessões de aposentadoria de FULANA - SES/DF"))
        self.assertFalse(L.ato_de_pessoal("Representação sobre o convênio da SES/DF, com a reforma do prédio "
                                          "do hospital"))


class Classificacao(unittest.TestCase):

    def test_ses_com_termo_de_fomento_e_emenda_toca_o_projeto(self):
        classe, motivos = L.classificar(L.decisoes(ATA)[0]["texto"], VIG)
        self.assertEqual(classe, "PROJETO")
        self.assertIn("SES-DF e termo de fomento, emenda", motivos)

    def test_ses_sem_instrumento_e_saude(self):
        self.assertEqual(L.classificar(L.decisoes(ATA)[2]["texto"], VIG)[0], "SAUDE")

    def test_outro_orgao_fica_fora(self):
        self.assertIsNone(L.classificar(L.decisoes(ATA)[3]["texto"], VIG)[0])

    def test_entidade_e_instrumento_do_acervo(self):
        classe, motivos = L.classificar("Convênio 030989/2026 com o ISHP, da área de oftalmologia.", VIG)
        self.assertEqual(classe, "PROJETO")
        self.assertEqual(motivos, ["entidade do acervo: ISHP", "instrumento do acervo: 030989/2026"])

    def test_sigla_dentro_de_outra_palavra_nao_conta(self):
        self.assertIsNone(L.classificar("O LIEVRE e uma empresa.", VIG)[0])


class Acervo(unittest.TestCase):

    def test_vigiados_das_pecas_de_controle_e_dos_proponentes(self):
        with tempfile.TemporaryDirectory() as d:
            acervo = Path(d) / "acervo.csv"
            acervo.write_text("id,titulo,processo_sei\nCT-001,\"Representacao - Convenio 030989/2026 (ISHP, 'Visao')\",TCDF 00600-00005737/2026-98\n"
                              "CT-002,\"Representacao - Convenios 030975 e 030977/2026 (IEV, R$ 31 mi)\",\n"
                              "CT-007,\"Decisão TCDF nº 715/2026 (DODF, edição extra nº 27-A)\",\n"
                              "NM-001,\"Lei (LGPD) nº 13.709\",\n", encoding="utf-8")
            prop = Path(d) / "proponentes"
            (prop / "ishp").mkdir(parents=True)
            v = L.vigiados(acervo, prop)
        self.assertEqual(v["nomes"], {"ISHP", "IEV"})
        self.assertEqual(v["numeros"], {"030989/2026", "030977/2026", "00600-00005737/2026-98"})

    def test_o_acervo_do_repositorio(self):
        v = L.vigiados()
        self.assertTrue({"ISHP", "IEV", "IBCS"} <= v["nomes"])
        self.assertIn("030989/2026", v["numeros"])


class Fontes(unittest.TestCase):

    def test_pasta_do_dia(self):
        self.assertEqual(L.pasta_do_dia(date(2026, 3, 5)), "2026/03_Março/05 03 2026")

    def test_listagem_do_dodf(self):
        arqs = L.arquivos_da_listagem(LISTAGEM)
        self.assertEqual(arqs[0], ("2026/10_Outubro/DODF 189 09-10-2026|", "DODF 189 09-10-2026 INTEGRA.pdf"))
        self.assertEqual(len(arqs), 2)

    def test_listagem_que_nao_veio_e_erro(self):
        with self.assertRaises(RuntimeError):
            L.arquivos_do_dia(date(2026, 10, 9), get=lambda url, params=None: b"<html>erro</html>")

    def test_feed_para_quando_passa_do_periodo(self):
        paginas = {1: feed([("Nova", "Fri, 09 Oct 2026 10:00:00 +0000", "a SES-DF e o convênio"),
                            ("Fora do fim", "Sat, 10 Oct 2026 10:00:00 +0000", "x")]),
                   2: feed([("Velha", "Mon, 21 Sep 2026 10:00:00 +0000", "y"),
                            ("Antiga", "Mon, 31 Aug 2026 10:00:00 +0000", "z")]),
                   3: feed([("Nunca lida", "Mon, 03 Aug 2026 10:00:00 +0000", "w")])}
        lidas = []

        def get(url, params=None):
            n = int((params or {}).get("paged", 1))
            lidas.append(n)
            return paginas.get(n, b"<html>404</html>")
        itens = L.itens_do_feed("https://x/feed/", date(2026, 9, 1), date(2026, 10, 9), get)
        self.assertEqual([i["titulo"] for i in itens], ["Nova", "Velha"])
        self.assertEqual(lidas, [1, 2])

    def test_relatorio(self):
        linhas = [{"classe": "PROJETO", "dia": date(2026, 4, 1), "fonte": "TCDF, DODF", "peca": "Decisão 715/2026",
                   "link": "https://x", "motivos": ["SES-DF e emenda"], "resumo": "Representação", "edicao": "DODF 027"}]
        txt = L.relatorio(linhas, {"dias": 1, "arquivos": 1, "decisoes": 4, "diarios": 0, "noticias": 0},
                          date(2026, 4, 1), date(2026, 4, 1))
        self.assertIn("## Tocam o projeto (1)", txt)
        self.assertIn("## Saúde do DF (0)", txt)


DIARIO = {"member": [{"id": "x", "tipo": "O", "numero": 60, "ano": 2026, "secoes": {
    "1": {"id": 50, "descricao": "Atos do Plenário", "publicacoes": [], "secoes": {
        "5": {"descricao": "Atos do Plenário/Atas das Sessões", "secoes": [], "publicacoes": [
            {"titulo": "ATA DA SESSÃO ORDINÁRIA Nº 5473", "texto": "<p>" + ATA.replace("\n", " ") + "</p>"}]},
        "6": {"descricao": "Atos do Plenário/Pauta das Sessões", "secoes": [], "publicacoes": [
            {"titulo": "EXTRATO DE PAUTA Nº 28/2026", "texto": "<p>Conselheiro X: 1) 00600-00005737/2026-98-e, "
             "Representação, Instituto de Saúde Humanidade e Pesquisa - ISHP; 2) 7193/2015-e, Tomada de Contas "
             "Especial, GPCF;</p>"}]}}},
    "2": {"descricao": "Atos da Segep", "publicacoes": [], "secoes": [
        {"descricao": "Atos da Segep/Despachos - Segep", "secoes": [], "publicacoes": [
            {"titulo": "AUXÍLIO", "texto": "<p>Nome: FULANO, convênio com a SES/DF</p>"}]}]}}}]}


class Doe(unittest.TestCase):

    def test_publicacoes_descem_pelas_secoes(self):
        secoes = [s for s, _, _ in L.publicacoes(DIARIO["member"][0]["secoes"])]
        self.assertEqual(secoes, ["Atos do Plenário/Atas das Sessões", "Atos do Plenário/Pauta das Sessões",
                                  "Atos da Segep/Despachos - Segep"])

    def test_ata_por_decisao_pauta_por_processo_e_fora_a_administracao(self):
        us = list(L.unidades_doe(DIARIO))
        pecas = [p for _, p, _, _ in us]
        self.assertIn("Decisão 715/2026 (processo 00600-00002022/2026-83)", pecas)
        self.assertIn("Pauta: processo 00600-00005737/2026-98-e", pecas)
        self.assertIn("Pauta: processo 7193/2015-e", pecas)
        self.assertFalse(any("Segep" in s for s, _, _, _ in us))

    def test_pauta_com_entidade_do_acervo_toca_o_projeto(self):
        u = [x for x in L.unidades_doe(DIARIO) if x[1] == "Pauta: processo 00600-00005737/2026-98-e"][0]
        self.assertEqual(L.classificar(u[3], VIG)[0], "PROJETO")

    def test_registro_de_despacho_de_processo_vigiado(self):
        j = {"member": [{"secoes": [{"descricao": "Atos do Plenário/Atas das Sessões", "secoes": [], "publicacoes": [
            {"titulo": "ATA", "texto": "<p>Representação: PROCESSO Nº 00600-00005737/2026-98-e - Despacho Singular Nº "
             "252/2026, Licitação: PROCESSO Nº 00600-00005178/2026-16-e - Despacho Singular Nº 222/2026.</p>"}]}]}]}
        us = [x for x in L.unidades_doe(j) if x[1].startswith("Despacho")]
        self.assertEqual([x[1] for x in us], ["Despacho singular 252/2026 (processo 00600-00005737/2026-98)",
                                              "Despacho singular 222/2026 (processo 00600-00005178/2026-16)"])
        vig = {"nomes": set(), "numeros": {"00600-00005737/2026-98"}}
        self.assertEqual(L.classificar(us[0][3], vig)[0], "PROJETO")
        self.assertIsNone(L.classificar(us[1][3], vig)[0])

    def test_acordaos_um_a_um(self):
        j = {"member": [{"secoes": [{"descricao": "Atos do Plenário/Acórdãos", "secoes": [], "publicacoes": [
            {"titulo": "ACÓRDÃOS NºS 126 A 127/2026", "texto": "<p>ACÓRDÃO Nº 126/2026 Ementa: contas da SEE/DF. "
             "ACÓRDÃO Nº 127/2026 Ementa: convênio da SES/DF com entidade.</p>"}]}]}]}
        us = list(L.unidades_doe(j))
        self.assertEqual([p for _, p, _, _ in us], ["Acórdão 126/2026", "Acórdão 127/2026"])
        self.assertIsNone(L.classificar(us[0][3], VIG)[0])
        self.assertEqual(L.classificar(us[1][3], VIG)[0], "PROJETO")

    def test_lista_de_diarios_por_pagina(self):
        paginas = {1: {"totalItems": 3, "member": [{"id": "a"}, {"id": "b"}]}, 2: {"totalItems": 3, "member": [{"id": "c"}]}}
        lidas = []

        def get(url, params=None):
            lidas.append(params["page"])
            return json.dumps(paginas[int(params["page"])]).encode()
        self.assertEqual([d["id"] for d in L.diarios_doe(date(2026, 8, 1), date(2026, 8, 31), get)], ["a", "b", "c"])
        self.assertEqual(lidas, ["1", "2"])

    def test_o_dodf_so_antes_do_doe(self):
        pedidos = []

        def get(url, params=None):
            pedidos.append(url)
            if url == L.DOE_API:
                return json.dumps({"totalItems": 0, "member": []}).encode()
            if url.endswith("/pastas"):
                return b"<title>DODF - Sistema de busca</title>"
            return b'<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>'
        L.ler(date(2026, 3, 8), date(2026, 3, 12), VIG, get=get, espera=0)
        self.assertEqual(pedidos.count(L.DODF + "/pastas"), 2)          # 08 e 09/03
        self.assertEqual(pedidos.count(L.DOE_API), 1)
        pedidos.clear()
        L.ler(date(2026, 8, 1), date(2026, 8, 3), VIG, get=get, espera=0)
        self.assertEqual(pedidos.count(L.DODF + "/pastas"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
