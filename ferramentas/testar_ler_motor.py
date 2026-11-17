#!/usr/bin/env python3
"""
testar_ler_motor.py - o leitor da saida do kit do Mapa Social derruba a copia errada?

As partes saem do kit de verdade, rodando no node sobre o motor falso. Cada falha que a
transcricao ou a area de transferencia pode trazer (um caractere trocado, uma parte que faltou,
a ordem trocada, o kit editado, um CNS) tem de parar a leitura com o motivo.
"""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import ler_motor as L
from testar_montar_coleta import NODE, ORDEM_MEDICAO, coleta_sintetica

KIT = Path(__file__).resolve().parent / "mapa_social" / "motor.js"


class Texto(unittest.TestCase):

    def test_djb2(self):
        self.assertEqual(L.djb2(""), 5381)
        self.assertEqual(L.djb2("a"), 177670)

    def test_ascii_e_desfazer(self):
        s = "A\u00a0B{É}\n" + "\U0001F600"
        a = L.ascii_kit(s)
        self.assertTrue(a.isascii())
        self.assertEqual(a[:30], "A{U+00A0}B{U+007B}{U+00C9}}{U+")
        self.assertEqual(L.desfazer(a), s)

    @unittest.skipUnless(NODE, "sem o node")
    def test_hash_da_ordem_igual_ao_do_kit(self):
        o = json.loads(json.dumps(ORDEM_MEDICAO))
        o["objetos"][1]["filas"][0]["nome"] = "ANGIOTOMOGRAFIA\u00a0 DE CORONÁRIAS – \"x\"\\"
        with tempfile.TemporaryDirectory() as tmp:
            arq = Path(tmp) / "ordem.json"
            arq.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")
            r = subprocess.run([NODE, str(KIT), "--hash-ordem", str(arq)], capture_output=True, text=True, check=True)
        self.assertEqual(int(r.stdout), L.hash_ordem(o))

    def test_datas_seriais(self):
        self.assertEqual(L.serial_data(46321), "26/10/2026")
        self.assertEqual(L.serial_hora(46321.958240740), "26/10/2026 22:59:52")
        self.assertEqual(L.brasilia("2026-10-27T01:32:42.805Z"), "26/10/2026 22:32:42")


@unittest.skipUnless(NODE, "sem o node: o kit nao roda")
class Partes(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.bruto, _ = coleta_sintetica(Path(self.tmp.name), ORDEM_MEDICAO, montar=False)

    def tearDown(self):
        self.tmp.cleanup()
        L._ASSINATURA = None

    def erro(self):
        with self.assertRaises(L.ErroMotor) as cm:
            L.ler(self.bruto)
        return str(cm.exception)

    def parte(self, i):
        return self.bruto / f"motor_parte_{i}.txt"

    def test_le_confere_e_converte(self):
        saida = L.gravar(self.bruto)
        m = json.loads(saida.read_text(encoding="utf-8"))
        self.assertGreater(m["leitura"]["partes"], 1)
        self.assertEqual(m["datas"]["inicio"]["solicitacao_max"], "26/10/2026")
        self.assertRegex(m["datas"]["inicio"]["consulta"], r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$")
        self.assertEqual(m["datas"]["inicio"]["recarga_brasilia"], "26/10/2026 16:32:44")
        self.assertIn("ANGIOTOMOGRAFIA\u00a0 DE CORONARIAS", json.dumps(m, ensure_ascii=False))
        mais = m["objetos"]["09.02.01.006-9"]["filas"]
        i = mais["cols"].index("mais_antiga")
        self.assertTrue(all(re.match(r"\d{2}/\d{2}/\d{4}$", l[i]) for l in mais["linhas"]))

    def test_quebra_de_linha_no_fim_nao_derruba(self):
        p = self.parte(1)
        p.write_text(p.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        L.ler(self.bruto)

    def test_um_caractere_trocado(self):
        p = self.parte(2)
        t = p.read_text(encoding="utf-8")
        cab, corpo = t.split("\n", 1)
        i = next(j for j, ch in enumerate(corpo) if ch.isdigit())
        corpo = corpo[:i] + str((int(corpo[i]) + 1) % 10) + corpo[i + 1:]
        p.write_text(cab + "\n" + corpo, encoding="utf-8")
        self.assertIn("nao bate com o hash", self.erro())

    def test_parte_faltando(self):
        self.parte(2).unlink()
        self.assertIn("faltam as partes [2]", self.erro())

    def test_sem_cabecalho(self):
        p = self.parte(1)
        p.write_text(p.read_text(encoding="utf-8").split("\n", 1)[1], encoding="utf-8")
        self.assertIn("sem o cabecalho", self.erro())

    def test_ordem_trocada_depois(self):
        o = json.loads((self.bruto / "ordem.json").read_text(encoding="utf-8"))
        o["pedido"] = "outra coisa"
        (self.bruto / "ordem.json").write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
        self.assertIn("rodou outra ordem", self.erro())

    def test_kit_que_nao_e_o_do_repositorio(self):
        L._ASSINATURA = 12345
        self.assertIn("nao e o ferramentas/mapa_social/motor.js", self.erro())

    def test_cns_na_saida(self):
        # uma parte valida (hash refeito) que traz um numero com a forma de CNS
        p = self.parte(1)
        cab, corpo = p.read_text(encoding="utf-8").split("\n", 1)
        corpo = corpo.replace('"tipo":"medicao"', '"tipo":"medicao","x":708123456789012', 1)
        m = re.match(r"#ms-parte (\d+)/(\d+) ", cab)
        partes = [corpo] + [self.parte(i).read_text(encoding="utf-8").split("\n", 1)[1] for i in range(2, int(m.group(2)) + 1)]
        total = "".join(partes)
        for i, c in enumerate(partes, 1):
            self.parte(i).write_text(f"#ms-parte {i}/{len(partes)} tamanho={len(c)} hash={L.djb2(c)} total={len(total)} "
                                     f"total_hash={L.djb2(total)}\n{c}", encoding="utf-8")
        self.assertIn("possivel CNS", self.erro())


if __name__ == "__main__":
    unittest.main(verbosity=2)
