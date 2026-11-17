#!/usr/bin/env python3
"""
testar_conferir_plano.py - testes de unidade do conferir_plano.py.

    python testar_conferir_plano.py
    python testar_conferir_plano.py -v

So a biblioteca padrao, e nao le plano nenhum: cada teste monta o pedaco de
texto que a funcao le. O arnes que injeta erro num plano real e outro arquivo,
o testar_conferencia_plano.py - ele prova que cada verificacao acusa o erro
que existe para acusar; estes provam que as pecas em que elas se apoiam leem o
que devem ler.

O que protegem:

1. A LEITURA DO estado.yaml. A regex anterior atravessava o arquivo: faltando
   a chave dentro do bloco pedido, devolvia a primeira de mesmo nome que
   aparecesse depois, de outra secao. `test_chave_de_outro_bloco_nao_vale` e o
   caso.
2. A C NO MODO fila_define_recurso. Conferia que (global - apoio) + apoio =
   global, conta que fecha por construcao.
3. A FILA DA I contra o estado.yaml, por numero inteiro e nao por pedaco de
   texto.
"""

import unittest

import conferir_plano as P


class LeituraDoEstado(unittest.TestCase):

    ESTADO = """\
parametros:
  valor_unitario:
    fonte: "Portaria SAES/MS 4.653 # com cerquilha dentro das aspas"
    nota: "sem valor aqui"
  origem_recurso:
    valor: 8500000.00      # comentario
    tipo: emenda
  objeto:
    oci: null
  vigencia_meses:
    valor: 10
    fonte: usuario
  dias_uteis: 21
  motivo: |
    texto longo
    valor: 999
derivados:
  valor: 123
  lista:
    - id: 7
      nome: "x"
"""

    def v(self, caminho):
        return P.yaml_valor(self.ESTADO, caminho)

    def test_escalar_aninhado(self):
        self.assertEqual(P.escalar(self.ESTADO, "origem_recurso.valor"), 8500000.0)

    def test_chave_de_outro_bloco_nao_vale(self):
        """valor_unitario nao tem `valor`; o `valor: 123` de derivados nao serve."""
        self.assertIsNone(self.v("valor_unitario.valor"))

    def test_comentario_sai_e_cerquilha_entre_aspas_fica(self):
        self.assertEqual(self.v("valor_unitario.fonte"),
                         "Portaria SAES/MS 4.653 # com cerquilha dentro das aspas")

    def test_null_e_nenhum_valor(self):
        self.assertIsNone(self.v("objeto.oci"))

    def test_chave_que_abre_bloco_nao_e_escalar(self):
        self.assertIsNone(self.v("vigencia_meses"))
        self.assertIsNone(self.v("motivo"))

    def test_parametro_le_escalar_ou_bloco_com_valor(self):
        self.assertEqual(P.parametro(self.ESTADO, "dias_uteis", int), 21)
        self.assertEqual(P.parametro(self.ESTADO, "vigencia_meses", int), 10)

    def test_item_de_lista(self):
        self.assertEqual(self.v("lista.id"), "7")

    def test_chave_inexistente(self):
        self.assertIsNone(self.v("nao_existe.valor"))
        self.assertIsNone(P.escalar(self.ESTADO, "origem_recurso.tipo"))  # nao e numero


class Numeros(unittest.TestCase):

    def test_num(self):
        self.assertEqual(P.num("1.284.120,10"), 1284120.10)
        self.assertEqual(P.num("38,80%"), 38.80)
        self.assertEqual(P.num("**12.967**"), 12967)
        self.assertIsNone(P.num("—"))
        self.assertIsNone(P.num("sem numero"))

    def test_inteiros_do_texto(self):
        texto = "fila: 11.456 e 5031; unitario 600.11; ano 2026-08-31"
        achados = P.inteiros_do_texto(texto)
        self.assertIn(11456, achados)
        self.assertIn(5031, achados)
        self.assertNotIn(60011, achados)      # decimal nao vira inteiro colado
        self.assertNotIn(600, achados)
        self.assertNotIn(56, P.inteiros_do_texto("total 1256"))

    def test_radical(self):
        self.assertEqual(P.radical("exames"), P.radical("exame"))
        self.assertEqual(P.radical("postos"), P.radical("posto"))
        self.assertEqual(P.radical("sessões"), "sessao")


class FechamentoFilaDefineRecurso(unittest.TestCase):
    """A C no modo em que a fila define o recurso."""

    def setUp(self):
        self.antigos = (P.DIRECAO, P.RECURSO, P.METAS_EXEC)
        P.DIRECAO, P.RECURSO, P.METAS_EXEC = "fila_define_recurso", 1100.0, [2]

    def tearDown(self):
        P.DIRECAO, P.RECURSO, P.METAS_EXEC = self.antigos

    def rodar(self, exec_total, apoio, glob):
        r = P.R()
        d = {"_apoio": apoio, "_qtd": 10, "_global": glob, "_exec": exec_total,
             "estado": "custo_acessorio:\n  teto: 0.5\n"}
        P.verificar_C(d, r)
        return r.itens[0]

    def test_fecha(self):
        _, _, ok, det, _ = self.rodar(1000.0, 100.0, 1100.0)
        self.assertTrue(ok, det)

    def test_execucao_que_nao_soma_o_global_e_acusada(self):
        """A versao anterior calculava a execucao como global - apoio: nunca acusava."""
        _, _, ok, det, _ = self.rodar(900.0, 100.0, 1100.0)
        self.assertFalse(ok)
        self.assertTrue(any("execucao" in x for x in det), det)

    def test_sem_meta_de_execucao(self):
        _, _, ok, det, _ = self.rodar(0.0, 100.0, 1100.0)
        self.assertFalse(ok)


class Dimensionamento(unittest.TestCase):
    """A +G da endoscopia mora na bateria do redacao_03 desde 08/10/2026; o teste
    carrega a bateria como o conferir_plano.py carrega."""

    def test_parametros_ausentes_sao_listados(self):
        import importlib.util
        from comum import PLANOS
        arq = PLANOS / "redacao_03" / "conferencia" / "verificacoes.py"
        spec = importlib.util.spec_from_file_location("bateria_redacao_03", arq)
        bateria = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bateria)
        valores, faltando = bateria.parametros_dimensionamento(
            P, "dimensionamento:\n  horas_sala_dia: 6\n")
        self.assertEqual(valores, {"horas_sala_dia": 6.0})
        self.assertIn("min_sala_por_paciente", faltando)


class PlanoContraPrePlano(unittest.TestCase):
    """A Y: o plano detalhado nao contradiz o pre-plano que a SES ja recebeu."""

    PRE = ("## 1. Informações iniciais\n\n| item | conteúdo |\n|---|---|\n"
           "| Valor Total | R$ 1.000,00, dentro do recurso |\n\n"
           "## 2. Objeto\n\nOCI 09.04.01.003-1 – Nasofaringe.\n\n"
           "## 8. Indicação da aplicação das despesas\n\n| aplicação | valor |\n|---|---|\n"
           "| Execução das OCIs | R$ 900,00 |\n\n## 9. Interface\n\ntexto\n")

    def setUp(self):
        import tempfile
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        (Path(self.tmp.name) / "pp.md").write_text(self.PRE, encoding="utf-8")
        self.antiga, P.RAIZ = P.RAIZ, Path(self.tmp.name)

    def tearDown(self):
        P.RAIZ = self.antiga
        self.tmp.cleanup()

    def rodar(self, plano="OCI 09.04.01.003-1", glob=1000.0, exec_=900.0, extra=""):
        r = P.R()
        P.verificar_Y({"plano": plano, "estado": 'pre_plano_enviado: "pp.md"\n' + extra,
                       "_global": glob, "_exec": exec_}, r)
        return r.itens[0]

    def test_sem_pre_plano_nao_se_aplica(self):
        r = P.R()
        P.verificar_Y({"plano": "", "estado": "", "_global": 1.0}, r)
        self.assertTrue(r.itens[0][4])

    def test_plano_que_concorda(self):
        _, _, ok, det, _ = self.rodar()
        self.assertTrue(ok, det)

    def test_codigo_novo(self):
        _, _, ok, det, _ = self.rodar(plano="OCI 09.04.01.003-1 e 09.04.01.001-5")
        self.assertFalse(ok)
        self.assertTrue(any("09.04.01.001-5" in x for x in det), det)

    def test_valor_e_producao_divergentes(self):
        _, _, ok, det, _ = self.rodar(glob=1200.0, exec_=1100.0)
        self.assertFalse(ok)
        self.assertEqual(len(det), 2, det)

    def test_divergencia_declarada_com_motivo(self):
        extra = ("pre_plano_divergencias:\n"
                 '  valor_total: "a SUCONV pediu o Valor Total igual ao recurso"\n'
                 '  producao: "x"\n')          # motivo curto demais: nao vale
        _, _, ok, det, _ = self.rodar(glob=1200.0, exec_=1100.0, extra=extra)
        self.assertFalse(ok)
        self.assertEqual(len(det), 1, det)
        self.assertIn("producao", det[0])


class CodigosDeOCI(unittest.TestCase):
    """A W contra os erros reais dos planos aprovados (AC-017, AC-058, AC-059).
    Le o catalogo de registros/fontes/, unica excecao ao 'nao le plano nenhum'."""

    @classmethod
    def setUpClass(cls):
        cls.antiga = P.RAIZ
        from comum import RAIZ
        P.RAIZ = RAIZ

    @classmethod
    def tearDownClass(cls):
        P.RAIZ = cls.antiga

    def w(self, texto):
        r = P.R()
        P.verificar_W({"plano": texto}, r)
        return r.itens[0]

    def test_digito_confere_os_codigos_do_grupo_09(self):
        _, cat = P.catalogo_sigtap()
        self.assertGreater(len(cat), 40)
        for codigo in cat:
            base, dv = codigo.split("-")
            self.assertEqual(P.digito_sigtap(base.replace(".", "")), int(dv), codigo)

    def test_digito_errado_do_iev(self):
        _, _, ok, det, _ = self.w("OCI 09.03.01.004-0 AVALIAÇÃO DIAGNÓSTICA EM ORTOPEDIA")
        self.assertFalse(ok)
        self.assertIn("09.03.01.004-6", det[0])

    def test_codigo_sem_digito(self):
        _, _, ok, det, _ = self.w("| 2.3.1 | OCI 09.02.01.001 AVALIAÇÃO DE RISCO CIRÚRGICO | 130,00 |")
        self.assertFalse(ok)
        self.assertIn("sem digito", det[0])

    def test_nome_trocado_da_cardiologia(self):
        _, _, ok, det, _ = self.w("II. OCI 09.02.01.004-2 – Avaliação Cardiológica")
        self.assertFalse(ok)
        self.assertIn("SÍNDROME CORONARIANA", det[0])

    def test_valor_trocado_na_planilha(self):
        linha = ("| 2.3.2 | OCI 09.02.01.006-9 AVALIAÇÃO DIAGNÓSTICA - INSUFICIÊNCIA CARDÍACA "
                 "| Unidade | 1000 | 250,00 | 250.000,00 |")
        _, _, ok, det, _ = self.w(linha)
        self.assertFalse(ok)
        self.assertIn("350,00", det[0])

    def test_codigo_certo_com_nome_e_valor_certos(self):
        texto = ("código 09.01.01.007-3 — OCI Avaliação Diagnóstica de Câncer Gástrico, concluída\n"
                 "| 2.1.1 | OCI 09.01.01.007-3 — Avaliação Diagnóstica de Câncer Gástrico | OCI "
                 "| 12.967 | 1 | 600,11 | 7.781.626,37 |")
        _, _, ok, det, _ = self.w(texto)
        self.assertTrue(ok, det)

    def test_frase_depois_do_codigo_nao_e_nome(self):
        _, _, ok, det, _ = self.w("procedimento 09.05.01.003-5 – OCI, integrante da Tabela do SUS")
        self.assertTrue(ok, det)

    def test_exame_avulso_confere_so_o_digito(self):
        """o plano de ultrassom e so exame: fora do grupo 09 nao ha catalogo, ha digito"""
        certo = "| 4.1.1 | 02.05.02.009-7 ULTRASSONOGRAFIA | exame | 14.608 | 99,94 | 1.459.923,52 |"
        _, _, ok, det, _ = self.w(certo)
        self.assertTrue(ok, det)
        _, _, ok, det, _ = self.w(certo.replace("009-7", "009-8"))
        self.assertFalse(ok)
        self.assertIn("02.05.02.009-7", det[0])

    def test_revogado(self):
        _, _, ok, det, _ = self.w("OCI 09.01.01.003-0")
        self.assertFalse(ok)
        self.assertIn("revogado", det[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
