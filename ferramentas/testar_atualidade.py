#!/usr/bin/env python3
"""
testar_atualidade.py - o dado do projeto esta atual?

O testar_padrao.py confere se o padrao e coerente; este confere se o dado envelheceu.
A Tabela do SUS muda a cada competencia, e o catalogo do grupo 09 passou um mes com os
valores de antes da SAES 4.795/2026 sem ninguem notar. Metodo: metodo/coleta/normas.md.

As tres verificacoes:
  1. toda ficha dos planos bate com o catalogo do grupo 09, e as portarias do historico
     dela estao no acervo (as F e G do conferir_ficha.py, em todas as fichas);
  2. toda portaria citada no estado.yaml de um plano esta no acervo;
  3. ha vigia recente: registros/vigia/vigia_<AAAA-MM-DD>.md de no maximo 40 dias, com a
     competencia vigiada. O agente normas a escreve todo dia 10.

Este teste depende da data de hoje de proposito: vigia velha e dado velho.
So biblioteca padrao.
"""
import re
import unittest
from datetime import date

import conferir_ficha as F
from comum import NORMAS, PLANOS, REGISTROS

VIGIA = REGISTROS / "vigia"
PRAZO_DIAS = 40


class Atualidade(unittest.TestCase):

    def test_fichas_batem_com_o_catalogo_e_o_acervo(self):
        problemas = []
        for ficha in sorted(PLANOS.glob("*/dados/fontes/sigtap_*.md")):
            for sigla, _, ok, falhas, na in F.verificar(ficha):
                if sigla in ("F", "G") and not ok and not na:
                    problemas += [f"{ficha.relative_to(PLANOS)}: {x}" for x in falhas]
        self.assertEqual(problemas, [], "fichas que nao batem com o catalogo ou com o acervo")

    def test_portaria_do_estado_esta_no_acervo(self):
        no_acervo = F.normas_no_acervo(NORMAS)
        faltam = []
        for estado in sorted(PLANOS.glob("*/estado.yaml")):
            txt = estado.read_text(encoding="utf-8")
            for m in re.finditer(r"Portaria (?:SAES|GM|SAS)/MS(?: n[ºo°])?\s*(\d{1,2}\.\d{3}|\d{1,5})/(\d{4})", txt):
                if (str(int(re.sub(r"\D", "", m.group(1)))), m.group(2)) not in no_acervo:
                    faltam.append(f"{estado.relative_to(PLANOS)}: {m.group(0)}")
        self.assertEqual(sorted(set(faltam)), [], "portarias citadas no estado.yaml sem arquivo no acervo")

    def test_ha_vigia_recente(self):
        relatorios = sorted(VIGIA.glob("vigia_*.md")) if VIGIA.exists() else []
        self.assertTrue(relatorios, "nenhuma vigia em registros/vigia/ — rodar o agente normas")
        ultimo = relatorios[-1]
        m = re.fullmatch(r"vigia_(\d{4})-(\d{2})-(\d{2})\.md", ultimo.name)
        self.assertTrue(m, f"{ultimo.name}: nome fora do padrao vigia_AAAA-MM-DD.md")
        dias = (date.today() - date(*map(int, m.groups()))).days
        self.assertLessEqual(dias, PRAZO_DIAS, f"a ultima vigia ({ultimo.name}) tem {dias} dias")
        self.assertRegex(ultimo.read_text(encoding="utf-8"), r"compet[êe]ncia vigiada: \d{2}/\d{4}",
                         f"{ultimo.name} sem a linha 'competência vigiada: MM/AAAA'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
