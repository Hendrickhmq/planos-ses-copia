#!/usr/bin/env python3
"""
testar_ler_dou.py - a leitura do DOU classifica certo?

Sem rede: atos sinteticos no formato da pagina "leitura do jornal" do in.gov.br.
So biblioteca padrao.
"""
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

import ler_dou as L

ACERVO = {("portaria", "8283"), ("portaria", "10297"), ("portaria", "4795"), ("lc", "101")}
SAES = "Ministério da Saúde/Secretaria de Atenção Especializada à Saúde"


def ato(titulo, conteudo, orgao="Ministério da Saúde/Gabinete do Ministro", tipo="Portaria", url="x"):
    return {"title": titulo, "content": f"{titulo} {conteudo}", "hierarchyStr": orgao,
            "artType": tipo, "urlTitle": url}


class Classificacao(unittest.TestCase):

    def classe(self, a):
        return L.classificar(a, ACERVO)[0]

    def test_altera_norma_do_acervo_toca_o_projeto(self):
        a = ato("Portaria GM/MS Nº 12.500, DE 1º DE OUTUBRO DE 2026",
                "Altera a Portaria GM/MS nº 8.283, de 30 de setembro de 2025, que dispõe sobre emendas.")
        self.assertEqual(self.classe(a), "PROJETO")

    def test_distrito_federal_toca_o_projeto(self):
        a = ato("Portaria GM/MS Nº 12.129, DE 26 DE agosto DE 2026",
                "Desabilita leitos e estabelece a dedução do limite MAC do Distrito Federal.")
        self.assertEqual(self.classe(a), "PROJETO")

    def test_ato_normativo_sobre_oci_e_novidade(self):
        a = ato("Portaria SAES/MS Nº 4.900, DE 1º DE OUTUBRO DE 2026",
                "Inclui Oferta de Cuidados Integrados na Tabela de Procedimentos.",
                orgao="Ministério da Saúde/Secretaria de Atenção Especializada à Saúde")
        self.assertEqual(self.classe(a), "NOVIDADE")

    def test_habilitacao_de_estabelecimento_e_local(self):
        a = ato("Portaria SAES/MS Nº 4.799, DE 27 DE agosto DE 2026",
                "Habilita estabelecimento no componente créditos financeiros do Programa Agora Tem Especialistas.",
                orgao="Ministério da Saúde/Secretaria de Atenção Especializada à Saúde")
        self.assertEqual(self.classe(a), "LOCAL")

    def test_habilitacao_no_distrito_federal_toca_o_projeto(self):
        a = ato("Portaria SAES/MS Nº 4.801, DE 27 DE agosto DE 2026",
                "Habilita estabelecimento do Distrito Federal no Programa Agora Tem Especialistas.",
                orgao="Ministério da Saúde/Secretaria de Atenção Especializada à Saúde")
        self.assertEqual(self.classe(a), "PROJETO")

    def test_registro_de_produto_da_anvisa_fica_fora(self):
        a = ato("RESOLUÇÃO-RE nº 3.396, DE 27 DE AGOSTO DE 2026", "Defere registro de produto.",
                orgao="Ministério da Saúde/Agência Nacional de Vigilância Sanitária/2ª Diretoria", tipo="Resolução")
        self.assertIsNone(self.classe(a))

    def test_rdc_da_anvisa_sobre_servico_fica(self):
        a = ato("RESOLUÇÃO-RDC Nº 1.050, DE 1º DE OUTUBRO DE 2026",
                "Dispõe sobre requisitos de serviços de atenção especializada em radiologia.",
                orgao="Ministério da Saúde/Agência Nacional de Vigilância Sanitária/Diretoria Colegiada", tipo="Resolução")
        self.assertEqual(self.classe(a), "NOVIDADE")

    def test_ato_de_outro_ministerio_fica_fora(self):
        a = ato("Portaria Nº 1, DE 1º DE OUTUBRO DE 2026", "Altera a Portaria nº 8.283.",
                orgao="Ministério da Educação/Gabinete do Ministro")
        self.assertIsNone(self.classe(a))

    def test_o_proprio_numero_nao_conta_como_citacao(self):
        a = ato("Portaria SAES/MS Nº 4.795, DE 26 DE agosto DE 2026",
                "Inclui atributo complementar e altera procedimentos na Tabela de Procedimentos.",
                orgao="Ministério da Saúde/Secretaria de Atenção Especializada à Saúde")
        self.assertEqual(self.classe(a), "NOVIDADE")

    # os erros do piloto de 09/10/2026

    def test_df_generico_sem_o_texto_integral_nao_toca_o_projeto(self):
        a = ato("Portaria GM/MS Nº 12.070, DE 7 DE agosto DE 2026",
                "Autoriza o Estado, Município ou Distrito Federal a receber recursos para aquisição de equipamentos.")
        self.assertNotEqual(self.classe(a), "PROJETO")

    def test_df_generico_com_o_fundo_do_df_no_anexo_toca_o_projeto(self):
        a = ato("Portaria GM/MS Nº 12.082, DE 6 DE agosto DE 2026",
                "Estabelece recursos de incremento temporário da atenção especializada dos Estados, "
                "Distrito Federal e Municípios.")
        classe, motivos = L.classificar(a, ACERVO, leitor=lambda _: "Anexo\nDF | BRASÍLIA | Fundo de Saúde do DF")
        self.assertEqual(classe, "PROJETO")
        self.assertIn("Distrito Federal no texto integral", motivos)

    def test_df_generico_sem_o_df_no_anexo_e_local(self):
        a = ato("Portaria GM/MS Nº 12.083, DE 6 DE agosto DE 2026",
                "Estabelece recursos de incremento temporário da atenção especializada dos Estados, "
                "Distrito Federal e Municípios.")
        classe, _ = L.classificar(a, ACERVO, leitor=lambda _: "Anexo\nGO | GOIÂNIA | Fundo Municipal\n"
                                                              "Brasília, 6 de agosto de 2026")
        self.assertEqual(classe, "LOCAL")

    def test_df_generico_com_o_texto_que_nao_veio_fica_no_projeto(self):
        a = ato("Portaria GM/MS Nº 12.084, DE 6 DE agosto DE 2026",
                "Estabelece recursos de incremento dos Estados, Distrito Federal e Municípios.")
        classe, motivos = L.classificar(a, ACERVO, leitor=lambda _: "")
        self.assertEqual(classe, "PROJETO")
        self.assertIn("não lido", motivos[0])

    def test_a_assinatura_da_saes_nao_e_novidade(self):
        a = ato("Portaria SAES/MS Nº 4.700, DE 10 DE agosto DE 2026",
                "Aprova o regimento interno da comissão. O SECRETÁRIO DE ATENÇÃO ESPECIALIZADA À SAÚDE, "
                "no uso das atribuições", orgao=SAES)
        self.assertIsNone(self.classe(a))

    def test_cebas_de_entidade_de_brasilia_e_local(self):
        a = ato("Portaria SAES/MS Nº 4.701, DE 10 DE agosto DE 2026",
                "Indefere a concessão do CEBAS da entidade X, com sede em Brasília. O SECRETÁRIO DE ATENÇÃO "
                "ESPECIALIZADA À SAÚDE, no uso das atribuições", orgao=SAES)
        self.assertEqual(self.classe(a), "LOCAL")

    def test_numero_curto_de_outra_especie_nao_e_do_acervo(self):
        a = ato("Portaria SGTES/SAPS/MS Nº 300, DE 10 DE agosto DE 2026",
                "Altera a Portaria SGTES/SAPS nº 101, de 2025, sobre médicos intercambistas.",
                orgao="Ministério da Saúde/Secretaria de Gestão do Trabalho")
        self.assertIsNone(self.classe(a))

    def test_norma_citada_no_preambulo_nao_conta(self):
        a = ato("Portaria GM/MS Nº 12.300, DE 10 DE agosto DE 2026",
                "Institui o comitê de cooperação. O MINISTRO DE ESTADO DA SAÚDE, considerando a Portaria "
                "GM/MS nº 8.283, de 2025")
        self.assertIsNone(self.classe(a))

    def test_republicacao_de_norma_do_acervo_toca_o_projeto(self):
        a = ato("PORTARIA SAES/MS Nº 4.795, DE 26 DE AGOSTO DE 2026 (*)",
                "(Publicada no DOU de 31/08/2026, Seção 1 Extra)", orgao=SAES)
        classe, motivos = self.classe(a), L.classificar(a, ACERVO)[1]
        self.assertEqual(classe, "PROJETO")
        self.assertIn("republica norma do acervo", motivos)

    def test_republicacao_sem_ementa_da_saes_e_novidade(self):
        a = ato("PORTARIA SAES/MS Nº 4.288, DE 19 DE JUNHO DE 2026 (*)",
                "(Publicada no DOU de 22/06/2026, Seção 1) ANEXO II", orgao=SAES)
        self.assertEqual(self.classe(a), "NOVIDADE")

    def test_tabela_diferenciada_na_consolidacao_e_novidade(self):
        """a GM 12.116/2026 ficava no resto: nem DF de fato, nem norma do acervo, nem tema"""
        a = ato("Portaria GM/ms Nº 12.116, DE 21 DE agosto DE 2026",
                "Altera a Portaria de Consolidação GM/MS nº 6, de 28 de setembro de 2017 para dispor sobre regras "
                "para estados, Distrito Federal e municípios que adotarem tabela diferenciada na remuneração das "
                "ações e serviços de saúde no âmbito do SUS.")
        classe, motivos = L.classificar(a, ACERVO, leitor=lambda _: "Os Estados, o Distrito Federal e os "
                                                                    "Municípios poderão adotar remuneração superior")
        self.assertEqual(classe, "NOVIDADE")
        self.assertIn("remuneração", motivos)

    def test_repasse_a_um_municipio_e_local(self):
        a = ato("PORTARIA GM/MS Nº 12.163, DE 14 DE SETEMBRO DE 2026",
                "Autoriza o repasse referente ao incremento financeiro emergencial de custeio no Município de X.")
        self.assertEqual(self.classe(a), "LOCAL")

    def test_incentivo_homologado_para_municipio_e_local(self):
        a = ato("PORTARIA GM/MS Nº 12.185, DE 17 DE SETEMBRO DE 2026",
                "Homologa a adesão e disponibiliza incentivo financeiro, em caráter excepcional e temporário, "
                "aos Municípios no Estado de Goiás.")
        self.assertEqual(self.classe(a), "LOCAL")

    def test_funasa_fica_fora(self):
        a = ato("Portaria Funasa Nº 3.462, DE 10 DE agosto DE 2026",
                "Dispõe sobre emendas parlamentares para saneamento.",
                orgao="Ministério da Saúde/Fundação Nacional de Saúde")
        self.assertIsNone(self.classe(a))


class Acervo(unittest.TestCase):

    def test_especie_e_numero_pelo_titulo(self):
        casos = {"Portaria GM/MS nº 12.116, de 21 de agosto de 2026": ("portaria", "12116"),
                 "Portaria de Consolidacao GM/MS n 1, de 28 de setembro de 2017": ("prc", "1"),
                 "Lei n 8.080, de 19 de setembro de 1990": ("lei", "8080"),
                 "Lei Complementar nº 101, de 4 de maio de 2000": ("lc", "101"),
                 "Instrução Normativa nº 01, de 22 de dezembro de 2005": ("in", "1"),
                 "Deliberação nº 46, de 21 de setembro de 2026": ("deliberacao", "46"),
                 "Manual Operacional da FPO": None}
        for titulo, esperado in casos.items():
            self.assertEqual(L.norma_do_titulo(titulo), esperado, titulo)

    def test_o_acervo_do_repositorio(self):
        normas = L.normas_do_acervo()
        for n in [("portaria", "4795"), ("prc", "1"), ("decreto", "48727"), ("lei", "7897")]:
            self.assertIn(n, normas)


class Bruto(unittest.TestCase):

    def test_o_dia_guardado_nao_se_baixa_de_novo_e_o_de_hoje_nao_se_guarda(self):
        chamadas = []

        def baixador(dia, secao):
            chamadas.append((dia, secao))
            return [ato("Portaria GM/MS Nº 1", "texto")]
        with tempfile.TemporaryDirectory() as d:
            ler = L.com_bruto(Path(d), baixador, hoje=date(2026, 10, 9))
            for _ in range(2):
                self.assertEqual(len(ler(date(2026, 10, 8), "do1")), 1)
                ler(date(2026, 10, 9), "do1")
        self.assertEqual(chamadas.count((date(2026, 10, 8), "do1")), 1)
        self.assertEqual(chamadas.count((date(2026, 10, 9), "do1")), 2)


class Leitura(unittest.TestCase):

    def test_pagina_do_dia(self):
        pagina = ('<html><script id="params" type="application/json">'
                  + json.dumps({"jsonArray": [ato("Portaria GM/MS Nº 1", "texto")]})
                  + "</script></html>")
        self.assertEqual(len(L.atos_da_pagina(pagina)), 1)
        vazia = '<html><script id="params" type="application/json">{"jsonArray": []}</script></html>'
        self.assertEqual(L.atos_da_pagina(vazia), [])

    def test_pagina_de_erro_nao_e_dia_sem_edicao(self):
        """a Azion devolve erro com HTTP 200; tratar como dia vazio perdia o dia em silencio"""
        self.assertIsNone(L.atos_da_pagina("<html><title>Azion - Default error page</title></html>"))

    def test_ler_conta_e_marca_a_edicao_extra(self):
        def baixador(dia, secao):
            if secao == "do1e":
                return [ato("Portaria SAES/MS Nº 4.795, DE 26 DE agosto DE 2026",
                            "Altera procedimentos na Tabela de Procedimentos.",
                            orgao="Ministério da Saúde/Secretaria de Atenção Especializada à Saúde")]
            if secao == "do1":
                return [ato("RESOLUÇÃO-RE nº 1", "registro",
                            orgao="Ministério da Saúde/Agência Nacional de Vigilância Sanitária/1ª Diretoria",
                            tipo="Resolução")]
            return []
        linhas, contagem, dias = L.ler(date(2026, 8, 31), date(2026, 8, 31), ACERVO, espera=0,
                                       baixador=baixador)
        self.assertEqual((contagem["NOVIDADE"], contagem["resto"], dias), (1, 1, 1))
        self.assertEqual(linhas[0]["secao"], "do1e")
        self.assertIn("(extra)", L.relatorio(linhas, contagem, date(2026, 8, 31), date(2026, 8, 31)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
