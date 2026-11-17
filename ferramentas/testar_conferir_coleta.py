#!/usr/bin/env python3
"""
testar_conferir_coleta.py - a conferencia da coleta do Mapa Social sabe falhar?

Uma coleta sintetica completa passa; cada falta e cada dado pessoal injetado tem de
derrubar a verificacao certa. A coleta do contrato da ordem (27/10/2026) e montada pelo
montador, sobre a saida do kit de verdade no node (ColetaMontada); as de antes ficam escritas
a mao, como eram.
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import conferir_coleta as C

COMPLETA = """# Mapa Social da Saúde — coleta de 06/10/2026

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde (MPDFT), paineis-ext.mpdft.mp.br |
| Última recarga da base | 06/10/2026 21:32:49 |
| Consulta | 06/10/2026 22:36 |
| Solicitação mais recente na base | 30/09/2026 |
| Medida | fila: os três status (pendente de regulação, corrigida e reenviada, pendente por fila de espera); devolvidas fora |

| fila | fila | pessoas | devolvidas | espera |
|---|---|---|---|---|
| Mama bilateral | 13.738 | 13.715 | 7.762 | 622 |

## Varredura das filas

| fila | fila | decisão |
|---|---|---|
| ECOGRAFIA DE MAMAS - BILATERAL | 13.738 | entra |
| ECOGRAFIA DE MAMA - UNILATERAL | 120 | a decidir |

## Por Região de Saúde

| Região | fila |
|---|---|
| Oeste | 3.100 |
"""


class Coleta(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.md = Path(self.tmp.name) / "mapa_social_20261006.md"
        self.bruto = Path(self.tmp.name) / "mapa_social_20261006_bruto"
        self.bruto.mkdir()
        (self.bruto / "coleta.json").write_text(
            '{"filtro_fila": "status_solicitacao_alias={...}", '
            '"nomes_internos": {"ECOGRAFIA DE MAMAS - BILATERAL": "Mama bilateral"}, '
            '"fila": 13738, "espera": 621.675988209088912}', encoding="utf-8")
        (self.bruto / "montar.py").write_text("print('monta a planilha')\n", encoding="utf-8")
        self.escrever(COMPLETA)

    def tearDown(self):
        self.tmp.cleanup()

    def escrever(self, txt):
        self.md.write_text(txt, encoding="utf-8")

    def falhas(self):
        return {s for s, _, ok, _, _ in C.verificar(self.md) if not ok}

    def test_coleta_completa_passa(self):
        # o decimal longo do JSON nao e CNS
        self.assertEqual(self.falhas(), set())

    def test_coleta_anterior_aos_alarmes_nao_se_aplica(self):
        na = {s for s, _, _, _, na in C.verificar(self.md) if na}
        self.assertEqual(na, {"H", "I", "J", "K"})

    def test_sem_fonte(self):
        self.escrever(COMPLETA.replace("MPDFT", "XX").replace("mpdft", "xx"))
        self.assertIn("A", self.falhas())

    def test_sem_hora_da_consulta(self):
        self.escrever(COMPLETA.replace("| Consulta | 06/10/2026 22:36 |\n", ""))
        self.assertEqual(self.falhas(), {"B"})

    def test_medida_sem_os_tres_status(self):
        self.escrever(COMPLETA.replace("os três status (pendente de regulação, corrigida e reenviada, "
                                       "pendente por fila de espera); ", ""))
        self.assertIn("C", self.falhas())

    def test_sem_regiao(self):
        self.escrever(COMPLETA.replace("Região", "Area"))
        self.assertEqual(self.falhas(), {"D"})

    def test_sem_pasta_bruta(self):
        for f in self.bruto.iterdir():
            f.unlink()
        self.bruto.rmdir()
        self.assertEqual(self.falhas(), {"E"})

    def test_json_sem_enquadramento(self):
        (self.bruto / "coleta.json").write_text('{"fila": 13738}', encoding="utf-8")
        self.assertEqual(self.falhas(), {"E"})

    def test_sem_varredura(self):
        self.escrever(COMPLETA.replace("## Varredura das filas", "## Outras filas"))
        self.assertEqual(self.falhas(), {"G"})

    def test_cpf_no_bruto(self):
        (self.bruto / "lista.json").write_text('["123.456.789-09"]', encoding="utf-8")
        self.assertEqual(self.falhas(), {"F"})

    def test_cns_no_md(self):
        self.escrever(COMPLETA + "\n| usuário | 708123456789012 |\n")
        self.assertEqual(self.falhas(), {"F"})


# uma OCI de CID largo, no formato do metodo de 25/10/2026: os numeros imitam a
# cardiologia do redacao_08 (ECG e Holter com o capitulo I, a consulta de IC)
ECG, HOLTER, CONS = "ELETROCARDIOGRAMA", "HOLTER 24 HORAS", "CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA"
OCI_JSON = {
    "metodo": "2026-10-25", "janela_viva_meses": 24,
    "filtro_fila": "status_solicitacao_alias={...}",
    "nomes_internos": {ECG: ECG, HOLTER: HOLTER, CONS: CONS},
    "filas": {
        ECG: {"papel": "exame", "generica": True, "fila": 20194, "fila_viva": 14415, "agendadas_12m": 14223,
              "recortes": {"I": {"fila": 11584, "fila_viva": 7962, "cid_principais": [["I10", 10157], ["I25", 300]]},
                           "I50": {"fila": 200, "fila_viva": 150, "cid_principais": [["I50", 200]]}}},
        HOLTER: {"papel": "exame", "generica": True, "fila": 36152, "fila_viva": 10193, "agendadas_12m": 2735,
                 "recortes": {"I": {"fila": 25259, "fila_viva": 6908, "cid_principais": [["I10", 6365], ["I49", 3862]]},
                              "I50": {"fila": 2304, "fila_viva": 900, "cid_principais": [["I50", 2304]]}}},
        CONS: {"papel": "consulta", "generica": False, "fila": 1090, "fila_viva": 1090, "agendadas_12m": 609,
               "recortes": {"I": {"fila": 1042, "fila_viva": 1042, "cid_principais": [["I50", 773], ["I509", 106]]},
                            "I50": {"fila": 879, "fila_viva": 879, "cid_principais": [["I50", 879]]}}},
    },
    "ocis": {"09.02.01.006-9": {
        "cid_aceito": 'codigo_cid_solicitado={"I*"}', "cid_finalidade": 'codigo_cid_solicitado={"I50*"}',
        "recorte_teto": "I", "recorte_finalidade": "I50", "filas": [ECG, HOLTER, CONS],
        "teto": {"pessoas": 30000, "pessoas_viva": 12000},
        "finalidade": {"pessoas": 3000, "pessoas_viva": 1800},
        "nucleo": {"pessoas": 879, "pessoas_viva": 879, "como": "consulta de entrada"}}},
}

OCI_MD = """# Mapa Social da Saúde — OCI 09.02.01.006-9, coleta de 25/10/2026

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde (MPDFT), paineis-ext.mpdft.mp.br |
| Última recarga da base | 25/10/2026 08:32:12 |
| Consulta | 25/10/2026 09:10 |
| Solicitação mais recente na base | 25/10/2026 |
| Medida | fila: os três status; devolvidas fora |

## Alarmes

- **CID largo** (006-9): a ficha aceita o capítulo I inteiro.
- **CID dominante** (006-9): I10 em 88% do ECG com CID do capítulo I.
- **Fila velha** (006-9): 1.200 das 3.000 pessoas só têm pedido de antes de 25/10/2024.
- **Estoque:** Holter, 13,2 anos de agendamentos.
- **Fila genérica** (006-9): ECG e Holter.

## 1. Os três números

| OCI | CID aceito | CID da finalidade | teto | teto viva | finalidade | finalidade viva | núcleo | núcleo viva | espera média (finalidade) |
|---|---|---|---|---|---|---|---|---|---|
| 09.02.01.006-9 | I00 a I99 | I50 | 30.000 | 12.000 | **3.000** | 1.800 | 879 | 879 | 400 |

Pessoas por Região de Saúde na aba 3.

## Varredura das filas

| fila | decisão |
|---|---|
| ELETROCARDIOGRAMA | a decidir (genérica) |
"""


class ColetaOCI(unittest.TestCase):

    def setUp(self):
        import json
        self.tmp = tempfile.TemporaryDirectory()
        self.md = Path(self.tmp.name) / "mapa_social_20261025.md"
        self.bruto = Path(self.tmp.name) / "mapa_social_20261025_bruto"
        self.bruto.mkdir()
        self.json = self.bruto / "coleta.json"
        self.dados = json.loads(json.dumps(OCI_JSON))
        self.gravar()
        (self.bruto / "montar.py").write_text("print('monta a planilha')\n", encoding="utf-8")
        self.md.write_text(OCI_MD, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def gravar(self):
        import json
        self.json.write_text(json.dumps(self.dados, ensure_ascii=False), encoding="utf-8")

    def falhas(self):
        return {s for s, _, ok, _, _ in C.verificar(self.md) if not ok}

    def test_alarmes_refeitos(self):
        tipos = {a["tipo"] for a in C.alarmes(OCI_JSON)}
        self.assertEqual(tipos, {"CID largo", "CID dominante", "fila velha", "estoque", "fila genérica"})

    def test_cid_raro(self):
        d = json_copia(OCI_JSON)
        for f in d["filas"].values():
            f["recortes"]["I50"]["fila"] = 10
        self.assertIn("CID raro", {a["tipo"] for a in C.alarmes(d)})

    def test_finalidade_igual_ao_teto_sem_dominante(self):
        d = json_copia(OCI_JSON)
        d["ocis"]["09.02.01.006-9"]["cid_finalidade"] = d["ocis"]["09.02.01.006-9"]["cid_aceito"]
        self.assertNotIn("CID dominante", {a["tipo"] for a in C.alarmes(d)})

    def test_coleta_oci_completa_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_alarme_que_falta_no_resumo(self):
        self.md.write_text(OCI_MD.replace("- **Estoque:** Holter, 13,2 anos de agendamentos.\n", ""),
                           encoding="utf-8")
        self.assertEqual(self.falhas(), {"H"})

    def test_sem_secao_de_alarmes(self):
        self.md.write_text(OCI_MD.replace("## Alarmes", "## Observações"), encoding="utf-8")
        self.assertEqual(self.falhas(), {"H"})

    def test_json_sem_filas(self):
        del self.dados["filas"]
        self.gravar()
        self.assertIn("H", self.falhas())

    def test_numero_da_tabela_diferente_do_json(self):
        self.md.write_text(OCI_MD.replace("**3.000**", "**50.317**"), encoding="utf-8")
        self.assertEqual(self.falhas(), {"I"})

    def test_sem_a_tabela_dos_tres_numeros(self):
        self.md.write_text(OCI_MD.replace("| núcleo | núcleo viva ", "| piso | piso 2 "), encoding="utf-8")
        self.assertEqual(self.falhas(), {"I"})

    def test_oci_sem_ocis_no_json(self):
        del self.dados["ocis"]
        self.gravar()
        self.assertIn("I", self.falhas())


class ColetaExame(unittest.TestCase):
    """a coleta de um exame avulso, no formato de 25/10/2026, que cita as OCI que usam o exame"""

    MD = OCI_MD.replace("# Mapa Social da Saúde — OCI 09.02.01.006-9, coleta de 25/10/2026",
                        "# Mapa Social da Saúde — fila do eletrocardiograma, coleta de 25/10/2026")

    def setUp(self):
        import json
        self.tmp = tempfile.TemporaryDirectory()
        self.md = Path(self.tmp.name) / "mapa_social_20261025.md"
        bruto = Path(self.tmp.name) / "mapa_social_20261025_bruto"
        bruto.mkdir()
        dados = json_copia(OCI_JSON)
        del dados["ocis"]
        (bruto / "coleta.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        (bruto / "montar.py").write_text("print('monta a planilha')\n", encoding="utf-8")
        self.md.write_text(self.MD + "\nO ECG compõe as OCI 09.02.01.001-8 e 09.02.01.006-9.\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_citar_a_oci_no_texto_nao_faz_a_coleta_ser_de_oci(self):
        na = {s for s, _, _, _, na in C.verificar(self.md) if na}
        falhas = {s for s, _, ok, _, _ in C.verificar(self.md) if not ok}
        self.assertIn("I", na)
        self.assertNotIn("I", falhas)


@unittest.skipUnless(shutil.which("node"), "sem o node: o kit nao roda")
class ColetaMontada(unittest.TestCase):
    """a coleta do contrato da ordem: o kit mede, os scripts montam, e a mao nao entra"""

    def setUp(self):
        from testar_montar_coleta import ORDEM_MEDICAO, coleta_sintetica
        self.tmp = tempfile.TemporaryDirectory()
        self.bruto, self.md = coleta_sintetica(Path(self.tmp.name), ORDEM_MEDICAO)
        self.coleta_arq = self.bruto / "coleta_20261027.json"

    def tearDown(self):
        self.tmp.cleanup()

    def falhas(self):
        return {s for s, _, ok, _, _ in C.verificar(self.md) if not ok}

    def rehash(self, arq):
        """a edicao que tambem refaz o hash do montagem.json: so a remontagem a pega"""
        import ler_motor as L
        reg_arq = self.bruto / "montagem.json"
        reg = json.loads(reg_arq.read_text(encoding="utf-8"))
        rel = next(k for k in reg["arquivos"] if (self.bruto / k).resolve() == arq.resolve())
        reg["arquivos"][rel] = L.djb2(arq.read_text(encoding="utf-8"))
        reg_arq.write_text(json.dumps(reg), encoding="utf-8")

    def editar_coleta(self, f):
        d = json.loads(self.coleta_arq.read_text(encoding="utf-8"))
        f(d)
        self.coleta_arq.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def test_passa(self):
        self.assertEqual(self.falhas(), set())

    def test_md_editado_a_mao(self):
        self.md.write_text(self.md.read_text(encoding="utf-8").replace("## Lacunas", "## Lacunas\n\nnota do agente"), encoding="utf-8")
        self.assertEqual(self.falhas(), {"K"})

    def test_md_editado_com_o_hash_refeito(self):
        self.md.write_text(self.md.read_text(encoding="utf-8").replace("## Lacunas", "## Lacunas\n\nnota do agente"), encoding="utf-8")
        self.rehash(self.md)
        self.assertEqual(self.falhas(), {"K"})

    def test_numero_trocado_no_json_da_coleta(self):
        def f(d):
            d["ocis"]["09.02.01.006-9"]["finalidade"]["pessoas"] = 50317
        self.editar_coleta(f)
        self.rehash(self.coleta_arq)
        self.assertIn("K", self.falhas())

    def test_ordem_sem_numero_nem_lacuna(self):
        def f(d):
            d["ocis"]["09.02.01.006-9"]["nucleo"]["pessoas_viva"] = None
        self.editar_coleta(f)
        self.assertIn("J", self.falhas())

    def test_dimensao_pedida_que_nao_veio(self):
        def f(d):
            del d["dimensoes"]["02.06.01.007-9"]["regiao"]
        self.editar_coleta(f)
        self.assertIn("J", self.falhas())

    def test_lacuna_com_motivo_responde_a_ordem(self):
        def f(d):
            d["ocis"]["09.02.01.006-9"]["nucleo"]["pessoas_viva"] = None
            d["lacunas"].append({"onde": "09.02.01.006-9 nucleo", "motivo": "o motor recusou o Aggr"})
        self.editar_coleta(f)
        self.assertNotIn("J", self.falhas())

    def test_ordem_trocada_depois(self):
        o = json.loads((self.bruto / "ordem.json").read_text(encoding="utf-8"))
        o["pedido"] = "outra coisa"
        (self.bruto / "ordem.json").write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
        self.assertIn("J", self.falhas())

    def test_sem_a_ordem(self):
        (self.bruto / "ordem.json").unlink()
        self.assertTrue({"E", "J"} <= self.falhas())

    def test_parte_trocada_depois(self):
        p = self.bruto / "motor_parte_1.txt"
        t = p.read_text(encoding="utf-8")
        p.write_text(t[:-1] + ("0" if t[-1] != "0" else "1"), encoding="utf-8")
        self.assertEqual(self.falhas(), {"K"})

    def test_cns_injetado_no_bruto(self):
        (self.bruto / "nota.txt").write_text("708123456789012", encoding="utf-8")
        self.assertEqual(self.falhas(), {"F"})

    def test_montador_de_outra_versao_confere_so_os_hashes(self):
        reg_arq = self.bruto / "montagem.json"
        reg = json.loads(reg_arq.read_text(encoding="utf-8"))
        reg["montador"] = "2026-10-01"
        reg_arq.write_text(json.dumps(reg), encoding="utf-8")
        self.assertEqual(self.falhas(), set())
        self.md.write_text(self.md.read_text(encoding="utf-8") + "\nnota\n", encoding="utf-8")
        self.assertEqual(self.falhas(), {"K"})


def json_copia(d):
    import json
    return json.loads(json.dumps(d))


if __name__ == "__main__":
    unittest.main(verbosity=2)
