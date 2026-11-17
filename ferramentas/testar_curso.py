#!/usr/bin/env python3
"""
testar_curso.py - o curso aponta para o que existe?

O curso (curso/) nao guarda regra: aponta para o metodo/, a biblioteca/ e os registros/.
Este teste confere que o apontamento nao quebrou: cada caminho e cada registro citado
existe, cada modulo tem as sete partes, o LEIA.md lista os modulos escritos, o comando
/aula aponta para o curso, e nao ha dado de paciente.

So biblioteca padrao.
"""
import csv
import re
import subprocess
import unittest
from pathlib import Path

from comum import CURSO, RAIZ, REGISTROS
from testar_padrao import caminhos_citados, existe, texto

COMANDO = RAIZ / ".claude" / "commands" / "aula.md"
MODULOS = sorted((CURSO / "modulos").glob("*.md"))
COFRE = RAIZ / "conhecimento"
DOCS = sorted(CURSO.rglob("*.md")) + sorted(COFRE.rglob("*.md")) + [COMANDO]
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

PARTES = ["Para que serve", "A lógica", "Pode e não pode", "O caso", "Leia na fonte", "Faça", "Confira"]
REGISTRO = re.compile(r"\b(NM|CT|IT|DD|OB|AC|LI)-(\d{3})\b")
CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
CNS = re.compile(r"(?<![\d.,])\d{15}(?![\d.,])")


def em_algum_ramo(caminho: str) -> bool:
    """o caminho existe em algum ramo local? (planos em andamento ficam fora do main)"""
    c = caminho.rstrip("/")
    try:
        ramos = subprocess.run(["git", "-C", str(RAIZ), "for-each-ref", "--format=%(refname)",
                                "refs/heads", "refs/remotes"],
                               capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        return False
    # no GitHub o checkout traz um ramo so: os planos dos outros ramos nao dao para conferir
    if len(ramos) <= 2:
        return True
    return any(subprocess.run(["git", "-C", str(RAIZ), "cat-file", "-e", f"{r}:{c}"],
                              capture_output=True).returncode == 0 for r in ramos)


def ids_dos_registros():
    ids = set()
    for nome in ("acervo.csv", "obrigacoes.csv", "achados.csv", "licoes.csv"):
        with open(REGISTROS / nome, encoding="utf-8", newline="") as f:
            ids |= {linha["id"] for linha in csv.DictReader(f)}
    return ids


class Curso(unittest.TestCase):

    def test_todo_caminho_citado_existe(self):
        faltam = []
        for doc in DOCS:
            for c in caminhos_citados(texto(doc)):
                # o arquivo de cada pessoa em curso/progresso/ nasce na primeira aula
                if c.startswith("curso/progresso/") or c == "ana.md":
                    continue
                # a pasta de dentro de um plano e o nome de um ramo: o curso descreve, nao aponta
                if re.match(r"(dados|dossie|versoes|recebidos|estudos|conferencia|secoes)(/|$)|(backup|ajustes|melhorias)/", c):
                    continue
                # plano em andamento mora no ramo dele: basta existir em algum ramo
                if c.startswith("planos/") and em_algum_ramo(c):
                    continue
                if not (existe(c, doc) or (CURSO / c).exists()):
                    faltam.append(f"{doc.relative_to(RAIZ)}: `{c}`")
        self.assertEqual(faltam, [], "caminhos citados no curso que nao existem")

    def test_todo_registro_citado_existe(self):
        ids = ids_dos_registros()
        faltam = []
        for doc in DOCS:
            for m in REGISTRO.finditer(texto(doc)):
                if m.group(0) not in ids:
                    faltam.append(f"{doc.relative_to(RAIZ)}: {m.group(0)}")
        self.assertEqual(sorted(set(faltam)), [], "registros citados no curso que nao existem")

    def test_todo_link_do_cofre_resolve(self):
        """[[nota]] do Obsidian aponta para nota que existe: pelo nome, pelo alias ou pelo caminho"""
        nomes = set()
        for p in RAIZ.rglob("*.md"):
            if {".git", "node_modules"} & set(p.parts):
                continue
            nomes.add(p.stem.lower())
            t = texto(p)
            if t.startswith("---"):
                fm = t.split("---", 2)[1]
                nomes |= {a.strip().lower() for a in re.findall(r'^\s*-\s*"([^"]+)"', fm, re.M)}
        ruins = []
        for doc in DOCS:
            for m in WIKILINK.finditer(texto(doc)):
                alvo = m.group(1).strip()
                if alvo.lower() not in nomes and not (RAIZ / f"{alvo}.md").exists():
                    ruins.append(f"{doc.relative_to(RAIZ)}: [[{alvo}]]")
        self.assertEqual(sorted(set(ruins)), [], "links do cofre que nao resolvem")

    def test_cada_nota_do_cofre_tem_tipo(self):
        sem = [p.name for p in COFRE.rglob("*.md") if not re.search(r"^tipo: ", texto(p), re.M)]
        self.assertEqual(sem, [], "nota do cofre sem 'tipo' no cabecalho")

    def test_cada_modulo_tem_as_sete_partes_na_ordem(self):
        self.assertTrue(MODULOS, "nenhum modulo em curso/modulos/")
        problemas = []
        for mod in MODULOS:
            titulos = re.findall(r"^## (.+?)\s*$", texto(mod), re.M)
            if titulos != PARTES:
                problemas.append(f"{mod.name}: {titulos}")
        self.assertEqual(problemas, [], f"as partes de cada modulo sao, nesta ordem: {PARTES}")

    def test_nome_do_modulo_comeca_pelo_numero(self):
        fora = [m.name for m in MODULOS if not re.match(r"\d{2}_[a-z0-9_]+\.md$", m.name)]
        self.assertEqual(fora, [], "modulo sem o numero de dois digitos na frente do nome")

    def test_leia_lista_os_modulos_escritos(self):
        leia = texto(CURSO / "LEIA.md")
        fora = [m.name for m in MODULOS if f"modulos/{m.name}" not in leia]
        self.assertEqual(fora, [], "modulos escritos que o curso/LEIA.md nao lista")
        citados = re.findall(r"`modulos/([^`]+\.md)`", leia)
        faltam = [c for c in citados if not (CURSO / "modulos" / c).exists()]
        self.assertEqual(faltam, [], "modulos que o curso/LEIA.md lista e nao existem")

    def test_comando_aula_aponta_para_o_curso(self):
        self.assertTrue(COMANDO.exists(), "falta .claude/commands/aula.md")
        self.assertIn("`curso/LEIA.md`", texto(COMANDO))

    def test_nenhum_dado_de_paciente(self):
        achados = []
        for doc in DOCS:
            txt = texto(doc)
            for padrao, nome in ((CPF, "CPF"), (CNS, "CNS")):
                for m in padrao.finditer(txt):
                    achados.append(f"{doc.relative_to(RAIZ)}: {nome} {m.group(0)[:4]}...")
        self.assertEqual(achados, [], "numero com cara de CPF ou CNS no curso")


if __name__ == "__main__":
    unittest.main(verbosity=1)
