#!/usr/bin/env python3
"""
testar_revisao.py - as ferramentas da revisao externa sabem falhar?

O pacote nao deixa sair CPF nem CNS; a conferencia literal aceita o que nao muda o
texto e recusa o que muda; a resposta sem fonte e o veredito que falta derrubam a
conferencia; as perguntas saem do metodo e so de la; os blocos do Gemini viram achados.
Nada aqui chama o ChatGPT nem o Google. So biblioteca padrao.
"""
import json
import os
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import conferir_revisao as CR
import pacote_revisao as PR
import revisar_chatgpt as RA
import revisar_claude as RC
import revisar_gemini as RG

DOC = """# PLANO DE TRABALHO

## 3. Justificativa

A fila soma **24.868** pessoas pendentes de regulação, e o quantitativo
resulta da divisão do valor disponível pelo valor unitário vigente.

| meta | quantidade | valor |
|---|---|---|
| Meta 2 | 12.967 OCI | R$ 7.781.800,00 |
"""
NORMA = "Art. 14. O registro da produção se faz obrigatoriamente por meio do CPF do usuário."


class Pacote(unittest.TestCase):
    def montar(self, doc_txt, fonte_txt):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "doc.md").write_text(doc_txt, encoding="utf-8")
        (tmp / "fonte.md").write_text(fonte_txt, encoding="utf-8")
        args = Namespace(documento=str(tmp / "doc.md"), saida=str(tmp / "pacote"), titulo="teste",
                         norma=None, aprovados=False, fichas_de=None, fonte=[str(tmp / "fonte.md")])
        return PR.montar(args), tmp / "pacote"

    def test_cpf_e_cns_saem_mascarados(self):
        cod, pac = self.montar(DOC + "\nCPF 123.456.789-01\n", "CNS 700000000000005 do paciente")
        self.assertEqual(cod, 0)
        todos = "".join(p.read_text(encoding="utf-8") for p in pac.rglob("*.md"))
        self.assertNotIn("123.456.789-01", todos)
        self.assertNotIn("700000000000005", todos)
        self.assertIn("[CPF mascarado]", todos)
        man = json.loads((pac / "manifesto.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(a["mascarados"] for a in man["arquivos"]), 2)

    def test_valor_em_reais_nao_e_cns(self):
        cod, pac = self.montar(DOC, "R$ 7.781.800,00 e 12.967 OCI")
        self.assertEqual(cod, 0)
        self.assertIn("7.781.800,00", (pac / "documento.md").read_text(encoding="utf-8"))

    def test_pasta_cheia_nao_e_sobrescrita(self):
        cod, pac = self.montar(DOC, NORMA)
        args = Namespace(documento=str(pac / "documento.md"), saida=str(pac), titulo=None, norma=None,
                         aprovados=False, fichas_de=None, fonte=None)
        with self.assertRaises(SystemExit):
            PR.montar(args)


class Literal(unittest.TestCase):
    def test_tolera_o_que_nao_muda_o_texto(self):
        self.assertTrue(CR.existe("A fila soma 24.868 pessoas pendentes de regulação", DOC))
        self.assertTrue(CR.existe("quantitativo resulta da divisão", DOC))          # quebra de linha
        self.assertTrue(CR.existe("Meta 2 12.967 OCI R$ 7.781.800,00", DOC))         # barras de tabela
        self.assertTrue(CR.existe("“A fila soma 24.868” [1]", DOC))                   # aspas e marca do Gemini
        self.assertTrue(CR.existe("A fila soma ... pendentes de regulação", DOC))    # reticências em ordem

    def test_aproximado_aceita_tabela_achatada_e_recusa_invencao(self):
        tabela = "| agendamento do exame e do retorno | 150,58 atos | 4 min | 10,04 |\n| busca ativa | 30,12 contatos | 5 min | 2,51 |"
        self.assertFalse(CR.existe("agendamento do exame e do retorno: 150,58 atos, 4 min, 10,04 h/dia", tabela))
        self.assertTrue(CR.aproximado("agendamento do exame e do retorno: 150,58 atos, 4 min, 10,04 h/dia", tabela))
        self.assertFalse(CR.aproximado("o agendamento é feito por telefone em até cinco dias úteis pela equipe", tabela))
        self.assertFalse(CR.aproximado("busca ativa 99,99 contatos 9 min 7,77", tabela))

    def test_recusa_o_que_muda_o_texto(self):
        self.assertFalse(CR.existe("A fila soma 24.869 pessoas", DOC))
        self.assertFalse(CR.existe("pendentes de regulação ... A fila soma", DOC))   # ordem trocada
        self.assertFalse(CR.existe("", DOC))
        self.assertFalse(CR.existe("fila", DOC))                                      # curto demais


class Conferencia(unittest.TestCase):
    def setUp(self):
        self.pac = Path(tempfile.mkdtemp())
        (self.pac / "documento.md").write_text(DOC, encoding="utf-8")
        (self.pac / "fontes").mkdir()
        (self.pac / "fontes" / "norma.md").write_text(NORMA, encoding="utf-8")
        self.dados = {"achados": [
            {"id": "X-01", "trecho_documento": "A fila soma 24.868 pessoas", "fonte_arquivo": None, "trecho_fonte": None},
            {"id": "X-02", "trecho_documento": "A fila soma 99.999 pessoas", "fonte_arquivo": None, "trecho_fonte": None},
            {"id": "X-03", "trecho_documento": "A fila soma 24.868 pessoas", "fonte_arquivo": "fontes/norma.md",
             "trecho_fonte": "obrigatoriamente por meio do CPF"},
            {"id": "X-04", "trecho_documento": "A fila soma 24.868 pessoas", "fonte_arquivo": "fontes/norma.md",
             "trecho_fonte": "preferencialmente pelo CNS"},
            {"id": "X-05", "trecho_documento": "A fila soma 24.868 pessoas", "fonte_arquivo": "fontes/nao_existe.md",
             "trecho_fonte": "qualquer coisa aqui"}]}
        CR.conferir_achados(self.pac, self.dados)

    def test_fonte_achada_pelo_conteudo(self):
        dados = {"achados": [
            {"id": "Y-01", "trecho_documento": "A fila soma 24.868 pessoas", "fonte_arquivo": None,
             "trecho_fonte": "obrigatoriamente por meio do CPF"},
            {"id": "Y-02", "trecho_documento": "A fila soma 24.868 pessoas", "fonte_arquivo": None,
             "trecho_fonte": "um texto que não está em lugar nenhum"}]}
        CR.conferir_achados(self.pac, dados)
        a, b = dados["achados"]
        self.assertEqual((a["fonte_arquivo"], a["citacao"]), ("fontes/norma.md", "ok"))
        self.assertEqual(b["citacao"], "fonte: trecho não encontrado em nenhum arquivo do pacote")

    def test_citacao_de_cada_achado(self):
        c = {a["id"]: a["citacao"] for a in self.dados["achados"]}
        self.assertEqual(c["X-01"], "ok")
        self.assertEqual(c["X-02"], "documento: trecho não encontrado")
        self.assertEqual(c["X-03"], "ok")
        self.assertEqual(c["X-04"], "fonte: trecho não encontrado")
        self.assertEqual(c["X-05"], "fonte: arquivo não existe no pacote")

    def resposta(self, **trocas):
        base = {"X-01": {"status": "aceito", "secao_alterada": "3", "fonte_arquivo": "fontes/norma.md",
                         "trecho_fonte": None, "nota": "corrigido"},
                "X-02": {"status": "citacao_invalida", "secao_alterada": None, "fonte_arquivo": None,
                         "trecho_fonte": None, "nota": "o trecho não existe"},
                "X-03": {"status": "contestado", "secao_alterada": None, "fonte_arquivo": "fontes/norma.md",
                         "trecho_fonte": "obrigatoriamente por meio do CPF", "nota": "a norma diz CPF"},
                "X-04": {"status": "decisao_do_usuario", "secao_alterada": None, "fonte_arquivo": None,
                         "trecho_fonte": None, "nota": "estado.yaml, 05/09/2026"},
                "X-05": {"status": "citacao_invalida", "secao_alterada": None, "fonte_arquivo": None,
                         "trecho_fonte": None, "nota": "arquivo inexistente"}}
        for k, v in trocas.items():
            base[k].update(v)
        return {"respostas": [{"id": k, **v} for k, v in base.items()]}

    def test_resposta_completa_passa(self):
        self.assertEqual(CR.conferir_resposta(self.pac, self.dados["achados"], self.resposta()), [])

    def test_contestar_sem_fonte_falha(self):
        r = self.resposta(**{"X-03": {"trecho_fonte": "a norma permite o CNS"}})
        self.assertTrue(any("X-03" in f for f in CR.conferir_resposta(self.pac, self.dados["achados"], r)))

    def test_aceitar_sem_fonte_falha(self):
        r = self.resposta(**{"X-01": {"fonte_arquivo": None}})
        self.assertTrue(any("X-01" in f for f in CR.conferir_resposta(self.pac, self.dados["achados"], r)))

    def test_achado_sem_resposta_falha(self):
        r = self.resposta()
        r["respostas"] = r["respostas"][1:]
        self.assertTrue(any("X-01: sem resposta" in f for f in CR.conferir_resposta(self.pac, self.dados["achados"], r)))

    def test_citacao_invalida_que_confere_falha(self):
        r = self.resposta(**{"X-01": {"status": "citacao_invalida"}})
        self.assertTrue(any("X-01" in f for f in CR.conferir_resposta(self.pac, self.dados["achados"], r)))

    def test_veredito_que_falta_falha(self):
        v = {"vereditos": [{"id": "X-01", "veredito": "resolvido"}]}
        self.assertEqual(len(CR.conferir_veredito(self.dados["achados"], v)), 4)


class Perguntas(unittest.TestCase):
    def test_as_perguntas_saem_do_metodo(self):
        a = RA.prompts()
        for nome in ("comum", "A1", "A2", "A4", "A5", "A7", "G1", "G2", "G3", "G5", "G7", "G9"):
            self.assertIn(nome, a, f"perguntas.md sem o bloco {nome}")
        g = RG.prompts()
        for nome in ("instrucao", "formato", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"):
            self.assertIn(nome, g, f"o Gemini sem o bloco {nome}")
        self.assertIn("{pasta}", RC.blocos(RC.REVISAO / "claude.md")["subagente"])
        for _, (_, lista) in RC.GRUPOS.items():
            for q in lista:
                self.assertIn(q, a, f"o Claude cego pede {q}, que perguntas.md não tem")
        self.assertIn("{afirmacao}", g["G6"])
        self.assertIn("{achados_e_respostas}", g["G8"])

    def test_o_codex_roda_isolado(self):
        # no CI nao ha Codex: o comando so se monta, com um executavel que existe em toda maquina
        os.environ["CODEX_BIN"] = sys.executable
        cmd = " ".join(RA.comando(Path("."), Path("e.json"), Path("s.json"), "gpt-6.1-sol", "high"))
        for opcao in ("--ephemeral", "--ignore-user-config", "-s read-only", "--disable memories",
                      "--disable plugins", "--disable apps", 'web_search="disabled"'):
            self.assertIn(opcao, cmd)


class Gemini(unittest.TestCase):
    RESPOSTA = """### ACHADO
classe: contradicao
trecho_documento: "A fila soma 24.868 pessoas pendentes de regulação" [1]
fonte: norma.md
trecho_fonte: "obrigatoriamente por meio do CPF" [2]
gravidade: diligencia
por_que: O documento contraria o art. 14.

**### ACHADO**
classe: sem_lastro
trecho_documento: "quantitativo resulta da divisão"
fonte: norma.md
trecho_fonte: "algo que não está lá"
gravidade: ajuste
por_que: Sem fonte
que sustente.

VAZIO: dado_divergente
"""

    def test_blocos_viram_achados(self):
        cad = {"fontes": {"s-doc": {"arquivo": "documento.md", "titulo": RG.TITULO_DOC},
                          "s-norma": {"arquivo": "fontes/norma.md", "titulo": "norma.md"}}}
        bruto = {"answer": self.RESPOSTA, "sources_used": ["s-norma"],
                 "references": [{"citation_number": 2, "source_id": "s-norma",
                                 "cited_text": "Art. 14. O registro da produção se faz obrigatoriamente por meio do CPF"}]}
        achados = RG.converter(cad, "G1", bruto)
        self.assertEqual(len(achados), 2)
        a, b = achados
        self.assertEqual(a["id"], "GEM-G1-01")
        self.assertEqual(a["fonte_arquivo"], "fontes/norma.md")
        self.assertNotIn("[1]", a["trecho_documento"])
        self.assertIn("obrigatoriamente", a["citacao_do_caderno"])
        self.assertEqual(b["por_que"], "Sem fonte que sustente.")
        self.assertFalse(a["sem_marca_de_citacao"])

    def test_fonte_pela_marca_quando_o_google_apaga_o_nome(self):
        cad = {"fontes": {"s-doc": {"arquivo": "documento.md", "titulo": RG.TITULO_DOC},
                          "s-cfm": {"arquivo": "fontes/normas/cfm.md", "titulo": "cfm"}}}
        resposta = """### ACHADO
classe: contradicao
trecho_documento: "A fila soma 24.868 pessoas"
fonte: [suspicious link removed]
trecho_fonte: "acompanhamento a cargo de outro médico"
gravidade: ajuste
por_que: O documento diz uma coisa [1], e a norma outra [2].
"""
        bruto = {"answer": resposta, "sources_used": ["s-doc", "s-cfm"],
                 "references": [{"citation_number": 1, "source_id": "s-doc", "cited_text": "A fila"},
                                {"citation_number": 2, "source_id": "s-cfm", "cited_text": "a cargo de outro médico"}]}
        a = RG.converter(cad, "G1", bruto)[0]
        self.assertEqual(a["fonte_arquivo"], "fontes/normas/cfm.md")
        self.assertEqual(a["citacao_do_caderno"], "a cargo de outro médico")

    def test_titulo_sem_extensao(self):
        self.assertEqual(RG.titulo_da_fonte("documento.md"), RG.TITULO_DOC)
        self.assertEqual(RG.titulo_da_fonte("fontes/normas/Resolucao_CFM_2174-2017.md"), "Resolucao CFM 2174-2017")



class ClaudeCego(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        pac = self.tmp / "pacote"
        (pac / "fontes" / "aprovados").mkdir(parents=True)
        (pac / "fontes" / "normas").mkdir()
        (pac / "documento.md").write_text(DOC, encoding="utf-8")
        (pac / "manifesto.json").write_text('{"origem": "planos/redacao_99"}', encoding="utf-8")
        (pac / "fontes" / "aprovados" / "pt_ses_01.md").write_text("aprovado", encoding="utf-8")
        (pac / "fontes" / "normas" / "norma.md").write_text(NORMA, encoding="utf-8")
        self.pac = pac

    def test_preparar_isola_e_separa_os_revisores(self):
        pasta = self.tmp / "cega"
        textos = RC.preparar(self.pac, pasta, faturamento=False, treplica=None)
        self.assertEqual([g for g, _ in textos], ["contas", "leitura"])
        for grupo in ("contas", "leitura"):
            self.assertFalse((pasta / grupo / "pacote" / "manifesto.json").exists(), "a origem vazou")
            self.assertTrue((pasta / grupo / "esquema.json").exists())
        self.assertTrue((pasta / "contas" / "pacote" / "fontes" / "aprovados").exists())
        self.assertFalse((pasta / "leitura" / "pacote" / "fontes" / "aprovados").exists())
        perg = (pasta / "leitura" / "perguntas.md").read_text(encoding="utf-8")
        self.assertNotIn("# Pergunta G2", perg)                      # sem --faturamento
        self.assertIn(str(pasta / "contas"), dict(textos)["contas"])

    def test_pasta_dentro_do_repositorio_e_recusada(self):
        with self.assertRaises(SystemExit):
            RC.preparar(self.pac, RC.RAIZ / "planos" / "_cega_teste", faturamento=False, treplica=None)

    def test_juntar_da_ids_por_revisor(self):
        pasta = self.tmp / "cega"
        RC.preparar(self.pac, pasta, faturamento=False, treplica=None)
        achado = {"classe": "conta", "secao": "3", "trecho_documento": "A fila soma 24.868 pessoas",
                  "fonte_arquivo": None, "trecho_fonte": None, "conta": None, "gravidade": "ajuste", "por_que": "x"}
        (pasta / "contas" / "saida" / "A1.json").write_text(json.dumps(
            {"achados": [achado, achado], "listas_vazias": [], "falta_fonte": []}), encoding="utf-8")
        (pasta / "leitura" / "saida" / "G1.json").write_text(json.dumps(
            {"achados": [achado], "listas_vazias": [], "falta_fonte": []}), encoding="utf-8")
        tudo = RC.juntar(pasta, self.tmp / "saida", treplica=False)
        self.assertEqual([a["id"] for a in tudo["achados"]], ["CLC-A1-01", "CLC-A1-02", "CLL-G1-01"])
        self.assertIn("contas/A2", tudo["faltam"])


if __name__ == "__main__":
    unittest.main()
