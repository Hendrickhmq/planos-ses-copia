#!/usr/bin/env python3
"""
testar_montar_coleta.py - o montador da coleta do Mapa Social monta so o que a ordem pediu,
com a decisao do enquadramento, e para quando a ordem esta incompleta?

A coleta sintetica sai do kit de verdade (mapa_social/motor.js) rodando no node sobre o motor
falso (mapa_social/motor_falso.mjs), com as partes gravadas como o navegador gravaria. Sem o
node, os testes que precisam do kit ficam de fora, dizendo.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import conferir_coleta as C
import ler_motor as L
import montar_coleta as M

AQUI = Path(__file__).resolve().parent
NODE = shutil.which("node")
FALSO = AQUI / "mapa_social" / "motor_falso.mjs"
NBSP = "\u00a0"

ORDEM_MEDICAO = {
    "contrato": "2026-10-27", "tipo": "medicao", "plano": "planos/redacao_99", "pedido": "teste do montador",
    "saida": "transcricao", "janela_viva_meses": 24, "dimensoes": ["regiao", "idade", "cid", "entrantes", "ano"],
    "objetos": [
        {"id": "09.02.01.006-9", "tipo": "oci", "nome": "insuficiência cardíaca", "ficha": "dados/fontes/sigtap_0902010069_102026.md",
         "codigos": ["02.11.02.003-6", "02.11.02.004-4"], "cid_aceito": 'codigo_cid_solicitado={"I*"}',
         "cid_finalidade": 'codigo_cid_solicitado={"I50*"}', "idade": {"min": 18, "max": 130}, "sexo": "ambos",
         "filas": [{"nome": "CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA", "papel": "consulta", "entrada": True},
                   {"nome": "ELETROCARDIOGRAMA", "papel": "exame", "obrigatorio": True},
                   {"nome": "HOLTER 24 HORAS", "papel": "exame", "obrigatorio": True}]},
        {"id": "02.06.01.007-9", "tipo": "exame", "nome": "angiotomografia de coronárias", "codigos": ["02.06.01.007-9"],
         "filas": [{"nome": "ANGIOTOMOGRAFIA  DE CORONARIAS"}]},
    ]}
ORDEM_PANORAMA = {
    "contrato": "2026-10-27", "tipo": "panorama", "plano": "planos/redacao_99", "pedido": "R$ 10 mi: onde aplicar?",
    "saida": "transcricao", "janela_viva_meses": 24, "dimensoes": ["regiao"],
    "universo": [{"rotulo": "imagem", "codigos": ["02.04*", "02.05*", "02.06*"]}, {"rotulo": "cardiologia", "termos": ["CARDIO"]}]}


def copia(d):
    return json.loads(json.dumps(d))


def coleta_sintetica(raiz: Path, ordem: dict, data="20261027", enquadramento=None, montar=True, tamanho=4000):
    """uma coleta inteira numa pasta de plano de mentira: ordem, partes do kit, motor, coleta e .md"""
    plano = raiz / "planos" / "redacao_99"
    fontes = plano / "dados" / "fontes"
    bruto = fontes / f"mapa_social_{data}_bruto"
    bruto.mkdir(parents=True)
    (fontes / "sigtap_0902010069_102026.md").write_text("# ficha\n", encoding="utf-8")
    if enquadramento is not None:
        (plano / "dados" / "enquadramento_mapa_social.json").write_text(json.dumps(enquadramento, ensure_ascii=False), encoding="utf-8")
    (bruto / "ordem.json").write_text(json.dumps(ordem, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run([NODE, str(FALSO), str(bruto / "ordem.json"), str(bruto), str(tamanho)], check=True)
    if montar:
        L.gravar(bruto)
        M.montar_pasta(bruto)
    return bruto, fontes / f"mapa_social_{data}.md"


class Ordem(unittest.TestCase):

    def test_a_ordem_completa_passa(self):
        self.assertEqual(M.validar_ordem(ORDEM_MEDICAO), [])
        self.assertEqual(M.validar_ordem(ORDEM_PANORAMA), [])

    def test_oci_sem_a_finalidade_e_sem_a_ficha_para(self):
        # o caso P5 do gauntlet: a OCI sem o CID da finalidade e sem a ficha na pasta
        o = copia(ORDEM_MEDICAO)
        del o["objetos"][0]["cid_finalidade"]
        with tempfile.TemporaryDirectory() as tmp:
            faltas = M.validar_ordem(o, Path(tmp))
        self.assertTrue(any("cid_finalidade" in f for f in faltas), faltas)
        self.assertTrue(any("ficha" in f and "nao existe" in f for f in faltas), faltas)

    def test_oci_sem_entrada_nem_obrigatorio(self):
        o = copia(ORDEM_MEDICAO)
        for f in o["objetos"][0]["filas"]:
            f.pop("entrada", None)
            f.pop("obrigatorio", None)
        self.assertTrue(any("nucleo" in f for f in M.validar_ordem(o)))

    def test_o_codigo_de_toda_consulta_nao_entra(self):
        o = copia(ORDEM_MEDICAO)
        o["objetos"][0]["codigos"].append("03.01.01.007-2")
        self.assertTrue(any("03.01.01.007-2" in f for f in M.validar_ordem(o)))

    def test_panorama_sem_universo_e_dimensao_desconhecida(self):
        o = copia(ORDEM_PANORAMA)
        o["universo"] = []
        o["dimensoes"] = ["sexo"]
        faltas = M.validar_ordem(o)
        self.assertTrue(any("universo" in f for f in faltas))
        self.assertTrue(any("'sexo'" in f for f in faltas))

    def test_forma_do_kit_guarda_o_espaco_nao_separavel_em_ascii(self):
        o = copia(ORDEM_MEDICAO)
        o["objetos"][1]["filas"][0]["nome"] = "ANGIOTOMOGRAFIA" + NBSP + " DE CORONARIAS"
        forma = M.forma_do_kit(o)
        self.assertIn("\\u00a0", forma)
        self.assertTrue(forma.isascii())
        self.assertEqual(json.loads(forma), o)

    def test_por_codigo_so_no_panorama_e_so_o_que_o_kit_mede(self):
        o = copia(ORDEM_PANORAMA)
        o["por_codigo"] = ["oferta", "faltas"]
        self.assertTrue(any("por_codigo 'faltas'" in f for f in M.validar_ordem(o)))
        o = copia(ORDEM_MEDICAO)
        o["por_codigo"] = ["oferta"]
        self.assertTrue(any("so do panorama" in f for f in M.validar_ordem(o)))
        o["dimensoes"] = ["oferta", "situacao"]
        del o["por_codigo"]
        self.assertEqual(M.validar_ordem(o), [])

    def test_meses_fechados(self):
        ult, ant = M.meses_fechados({"datas": {"solicitacao_mais_recente": "27/10/2026"}})
        self.assertEqual((ult[0], ult[-1], ant[0], ant[-1]), ("2025-10", "2026-09", "2024-10", "2025-09"))
        ult, _ = M.meses_fechados({"datas": {"solicitacao_mais_recente": "05/01/2027"}})
        self.assertEqual((ult[0], ult[-1]), ("2026-01", "2026-12"))

    def test_cli_da_ordem_incompleta(self):
        o = copia(ORDEM_MEDICAO)
        del o["objetos"][0]["cid_finalidade"]
        with tempfile.TemporaryDirectory() as tmp:
            b = Path(tmp) / "planos" / "redacao_99" / "dados" / "fontes" / "mapa_social_20261027_bruto"
            b.mkdir(parents=True)
            (b / "ordem.json").write_text(json.dumps(o), encoding="utf-8")
            r = subprocess.run([sys.executable, str(AQUI / "montar_coleta.py"), "--ordem", str(b)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ORDEM INCOMPLETA", r.stdout)
        self.assertIn("cid_finalidade", r.stdout)


@unittest.skipUnless(NODE, "sem o node: o kit nao roda")
class Montador(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def falhas(self, md):
        return {s for s, _, ok, _, na in C.verificar(md) if not ok}

    def test_medicao_passa_em_tudo(self):
        _, md = coleta_sintetica(self.raiz, ORDEM_MEDICAO)
        self.assertEqual(self.falhas(md), set())
        na = {s for s, _, _, _, na in C.verificar(md) if na}
        self.assertEqual(na, set())

    def test_o_md_sai_igual_do_mesmo_json(self):
        bruto, md = coleta_sintetica(self.raiz, ORDEM_MEDICAO)
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        self.assertEqual(M.renderizar_md(coleta), md.read_text(encoding="utf-8"))
        self.assertTrue(md.with_suffix(".xlsx").exists())

    def test_o_nome_digitado_sem_o_espaco_nao_separavel(self):
        bruto, _ = coleta_sintetica(self.raiz, ORDEM_MEDICAO)
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        self.assertEqual(coleta["nomes_internos"]["ANGIOTOMOGRAFIA  DE CORONARIAS"], ["ANGIOTOMOGRAFIA" + NBSP + " DE CORONARIAS"])
        self.assertIn("ANGIOTOMOGRAFIA" + NBSP + " DE CORONARIAS", coleta["filas"])

    def test_tres_numeros_e_nucleo_pelo_maior(self):
        bruto, _ = coleta_sintetica(self.raiz, ORDEM_MEDICAO)
        o = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))["ocis"]["09.02.01.006-9"]
        for k in ("teto", "finalidade", "nucleo"):
            self.assertIsInstance(o[k]["pessoas"], int, k)
            self.assertIsInstance(o[k]["pessoas_viva"], int, k)
        self.assertEqual(o["nucleo"]["pessoas"], max(c["pessoas"] for c in o["nucleo"]["candidatos"]))
        self.assertFalse(o["finalidade_igual_ao_teto"])

    def test_decisao_vem_do_enquadramento_e_a_generica_sem_decisao_fica_a_decidir(self):
        enq = {"atualizado": "26/10/2026", "filas": {
            "ECOGRAFIA DE MAMAS - BILATERAL": {"decisao": "fica fora", "motivo": "não é cardiologia (usuário, 26/10/2026)"},
            "CONSULTA EM CARDIOLOGIA - INSUFICIENCIA CARDIACA": {"decisao": "entra", "motivo": "consulta da OCI (usuário)", "papel": "consulta"}}}
        bruto, md = coleta_sintetica(self.raiz, ORDEM_MEDICAO, enquadramento=enq)
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        v = {(x["tabela"], x["nome"]): x for x in coleta["varredura"]}
        self.assertEqual(v[("sol", "ECOGRAFIA DE MAMAS - BILATERAL")]["decisao"], "fica fora")
        self.assertEqual(v[("sol", "ELETROCARDIOGRAMA")]["decisao"], "a decidir")
        self.assertTrue(v[("sol", "ELETROCARDIOGRAMA")]["generica"])
        # a fila que tambem esta nas solicitacoes nao repete como "so agendamentos"
        self.assertNotIn(("ag", "ELETROCARDIOGRAMA"), v)
        self.assertIn(("ag", "MAMOGRAFIA DE RASTREAMENTO"), v)
        resp = M.resposta(coleta, md)
        self.assertNotIn("ECOGRAFIA DE MAMAS", resp.split("ACHADOS")[1].split("LACUNAS")[0])
        self.assertNotIn("A DECIDIR NO ENQUADRAMENTO", resp)

        # o nome so de agendamentos achado so pelo CID fica no JSON, fora do resumo, contado
        self.assertFalse(v[("ag", "MAMOGRAFIA DE RASTREAMENTO")]["no_resumo"])
        self.assertNotIn("MAMOGRAFIA DE RASTREAMENTO", md.read_text(encoding="utf-8"))
        self.assertIn("achadas só pelo CID", resp)
        self.assertNotIn("09.02.01.006-9: 09.02.01.006-9", resp)
        self.assertEqual(self.falhas(md), set())

    def test_fila_que_o_enquadramento_deixou_a_decidir_vai_a_resposta(self):
        enq = {"filas": {"ECOGRAFIA DE MAMAS - BILATERAL": {"decisao": "a decidir", "motivo": "emergência (usuário, 26/10/2026)"}}}
        bruto, md = coleta_sintetica(self.raiz, ORDEM_MEDICAO, enquadramento=enq)
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        resp = M.resposta(coleta, md)
        self.assertIn("A DECIDIR NO ENQUADRAMENTO (1):", resp)
        self.assertIn("ECOGRAFIA DE MAMAS - BILATERAL", resp.split("A DECIDIR NO ENQUADRAMENTO")[1])

    def test_diferenca_para_a_coleta_anterior(self):
        coleta_sintetica(self.raiz, ORDEM_MEDICAO, data="20261026")
        plano = self.raiz / "planos" / "redacao_99"
        fontes = plano / "dados" / "fontes"
        b2 = fontes / "mapa_social_20261027_bruto"
        b2.mkdir()
        (b2 / "ordem.json").write_text(json.dumps(ORDEM_MEDICAO, ensure_ascii=False), encoding="utf-8")
        subprocess.run([NODE, str(FALSO), str(b2 / "ordem.json"), str(b2)], check=True)
        L.gravar(b2)
        coleta, md = M.montar_pasta(b2)
        self.assertEqual(coleta["diferenca"]["arquivo"], "dados/fontes/mapa_social_20261026_bruto/coleta_20261026.json")
        self.assertIn("09.02.01.006-9", coleta["diferenca"]["ocis"])
        self.assertIn("Contra `dados/fontes/mapa_social_20261026_bruto/coleta_20261026.json`", md.read_text(encoding="utf-8"))
        self.assertEqual(self.falhas(md), set())

    def test_panorama(self):
        bruto, md = coleta_sintetica(self.raiz, ORDEM_PANORAMA)
        itens = {s: (ok, na) for s, _, ok, _, na in C.verificar(md)}
        self.assertTrue(itens["H"][1] and itens["I"][1], "H e I nao se aplicam ao panorama")
        self.assertTrue(all(ok for ok, _ in itens.values()), {s: v for s, v in itens.items() if not v[0]})
        txt = md.read_text(encoding="utf-8")
        for t in ("### imagem: por pessoas", "### imagem: as 20 de maior espera média", "### imagem: as 20 de mais anos de estoque"):
            self.assertIn(t, txt)
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        pessoas = [r["pessoas"] for r in coleta["panorama"]["imagem"]["filas"]]
        self.assertEqual(pessoas, sorted(pessoas, reverse=True))
        self.assertEqual(coleta["alarmes"], [])
        # o total do universo e do motor, e nao a soma das filas
        self.assertEqual(set(coleta["panorama"]["imagem"]["total"]), {"fila", "fila_viva", "pessoas"})
        self.assertNotIn("ACHADOS", M.resposta(coleta, md))

    def test_oferta_e_situacao_na_medicao(self):
        o = copia(ORDEM_MEDICAO)
        o["dimensoes"] = ["entrantes", "oferta", "situacao"]
        bruto, md = coleta_sintetica(self.raiz, o)
        self.assertEqual(self.falhas(md), set())
        txt = md.read_text(encoding="utf-8")
        self.assertIn("## Oferta por mês do agendamento", txt)
        self.assertIn("## Situação dos agendamentos em 12 meses", txt)
        self.assertIn("| PROCEDIMENTO REALIZADO |", txt)
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        self.assertEqual(coleta["dimensoes"]["02.06.01.007-9"]["oferta"]["cols"], ["mes", "agendamentos", "realizados", "faltas"])

    def test_panorama_com_o_rumo_por_codigo(self):
        o = copia(ORDEM_PANORAMA)
        o["por_codigo"] = ["entrantes", "oferta", "situacao"]
        bruto, md = coleta_sintetica(self.raiz, o)
        self.assertEqual(self.falhas(md), set())
        coleta = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        self.assertEqual(set(coleta["por_codigo"]), {"entrantes", "oferta", "situacao"})
        self.assertTrue(all(l[0].startswith("02.") for l in coleta["por_codigo"]["oferta"]["linhas"]))
        r = {x["codigo"]: x for x in coleta["rumo"]}
        self.assertIn("02.04.03.018-8", r)
        x = r["02.04.03.018-8"]
        # a serie do motor falso tem 2025-06 nos 12 meses de antes e 2026-10 fora dos fechados (o mes da solicitacao)
        of = {l[1]: l[2] for l in coleta["por_codigo"]["oferta"]["linhas"] if l[0] == "02.04.03.018-8"}
        self.assertEqual(x["oferta_12m_antes"], of["2024-10"] + of["2025-06"])
        self.assertEqual(x["oferta_12m"], 0)
        self.assertIn("## Rumo por código", md.read_text(encoding="utf-8"))
        self.assertIn("rumo por código:", M.resposta(coleta, md))
        # pedido e nao veio: a conferencia cai
        dados = json.loads((bruto / "coleta_20261027.json").read_text(encoding="utf-8"))
        dados["por_codigo"].pop("situacao")
        self.assertTrue(any("'situacao' foi pedido" in f for f in C.verificar_ordem(bruto, dados)))

    def test_recarga_no_meio_o_kit_para(self):
        b = self.raiz / "b"
        b.mkdir()
        (b / "ordem.json").write_text(json.dumps(ORDEM_MEDICAO), encoding="utf-8")
        r = subprocess.run([NODE, str(FALSO), str(b / "ordem.json"), str(b), "--recarga-no-meio"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("recarga no meio", r.stderr)
        self.assertEqual(list(b.glob("motor_parte_*.txt")), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
