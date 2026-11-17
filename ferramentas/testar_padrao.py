#!/usr/bin/env python3
"""
testar_padrao.py - o padrao e coerente consigo mesmo?

Nao confere plano nenhum: confere o metodo/, o README, a biblioteca de proponentes e os
agentes. E a regra "uma verdade so" virada em teste. Na reorganizacao de 08/10/2026
estas conferencias foram feitas a mao, com grep; aqui elas pegam sozinhas o proximo
caminho quebrado, a regra citada que nao existe e a referencia ao lugar antigo.

So biblioteca padrao.
"""
import re
import unittest
from pathlib import Path

from comum import METODO, RAIZ

AQUI = Path(__file__).resolve().parent
AGENTES = RAIZ / ".claude" / "agents"

# os documentos que descrevem o padrao e onde ele mora
DOCS = (sorted(METODO.rglob("*.md")) + [RAIZ / "README.md", RAIZ / "biblioteca" / "proponentes" / "README.md"]
        + sorted(AGENTES.glob("*.md")))
# o registro de mudancas e o criterios.md gerado citam o passado de proposito
HISTORICOS = {METODO / "MUDANCAS.md", METODO / "criterios.md"}


def texto(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def caminhos_citados(txt: str):
    """caminhos do repositorio entre crases: com barra ou com extensao conhecida"""
    for m in re.finditer(r"`([^`\s]+)`", txt):
        c = m.group(1).rstrip(".,;:)")
        if re.search(r"[<>*{}$|]|NN|AAAA|MMAAAA|\.\.\.|…|^[a-z]+://|^https?:|^/|=|\(|^\.", c):
            continue                      # modelo, padrao ou endereco, nao arquivo
        if "/" in c or re.search(r"\.(md|py|csv|yaml|js|json)$", c):
            yield c


# arquivos que o padrao descreve como previstos, antes de existirem
PREVISTOS = {
    "ficha.yaml": "biblioteca/proponentes/README.md, o que cada pasta de proponente deve ter",
    "retornos.md": "idem",
    "ordem.json": "metodo/coleta/mapa_social.md, a pasta bruta de cada coleta do Mapa Social",
    "montagem.json": "idem",
    "arbitro.json": "metodo/agentes/gauntlet.md, a pasta de cada caso de uma rodada, fora do repositorio",
    "resposta.md": "idem",
}
_NOMES = None


def nomes_no_repositorio():
    """todo nome de arquivo do repositorio, para citacao sem pasta ('texto.md')"""
    global _NOMES
    if _NOMES is None:
        _NOMES = {p.name for p in RAIZ.rglob("*")
                  if p.is_file() and not {".git", "node_modules"} & set(p.parts)}
    return _NOMES


def existe(c: str, doc: Path) -> bool:
    if "/" not in c:
        return c in PREVISTOS or c in nomes_no_repositorio()
    c = c.rstrip("/")
    bases = [RAIZ, doc.parent, METODO, METODO / "plano", METODO / "pre_plano", METODO / "coleta",
             AQUI, RAIZ / "registros", RAIZ / "biblioteca"]
    return any((b / c).exists() for b in bases)


class Padrao(unittest.TestCase):

    def test_todo_caminho_citado_existe(self):
        """caminho entre crases que nao existe e regra apontando para o nada"""
        faltam = []
        for doc in DOCS:
            if doc in HISTORICOS:
                continue
            for c in caminhos_citados(texto(doc)):
                # arquivo dentro da pasta de um plano: o padrao descreve, nao aponta
                if re.match(r"(dados|secoes|versoes|conferencia|dossie)/|^(estado\.yaml|plano\.md|plano\.docx|"
                            r"pendencias\.md|licoes\.md|00_metodo\.md|checklist\.md)$", c):
                    continue
                if not existe(c, doc):
                    faltam.append(f"{doc.relative_to(RAIZ)}: `{c}`")
        self.assertEqual(faltam, [], "caminhos citados que nao existem")

    def test_regra_do_comum_citada_existe(self):
        regras = {int(n) for n in re.findall(r"^\*\*(\d+)\. ", texto(METODO / "comum.md"), re.M)}
        self.assertTrue(regras, "comum.md sem regras numeradas")
        erradas = []
        for doc in DOCS:
            for m in re.finditer(r"comum(?:\.md)?`?,\s*regras?\s+(\d+)(?:\s+(?:e|a)\s+(\d+))?", texto(doc)):
                for n in filter(None, m.groups()):
                    if int(n) not in regras:
                        erradas.append(f"{doc.relative_to(RAIZ)}: comum, regra {n}")
        self.assertEqual(erradas, [], f"regras citadas que o comum.md nao tem (tem 1 a {max(regras)})")

    def test_regras_do_comum_em_sequencia_com_origem(self):
        txt = texto(METODO / "comum.md")
        nums = [int(n) for n in re.findall(r"^\*\*(\d+)\. ", txt, re.M)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)), "regras do comum.md fora de sequencia")
        blocos = re.split(r"^\*\*\d+\. ", txt, flags=re.M)[1:]
        sem = [i for i, b in enumerate(blocos, 1) if "*Origem:" not in b]
        self.assertEqual(sem, [], "regra do comum.md sem linha de origem")

    def test_verificacao_citada_existe_na_ferramenta(self):
        letras = set(re.findall(r"^def verificar_([A-Z])\b", texto(AQUI / "conferir_plano.py"), re.M))
        erradas = []
        for doc in sorted((METODO / "plano").glob("*.md")) + [METODO / "comum.md"]:
            for m in re.finditer(r"verifica[çc][ãa]o ([A-Z])\b", texto(doc)):
                if m.group(1) not in letras:
                    erradas.append(f"{doc.relative_to(RAIZ)}: verificacao {m.group(1)}")
        self.assertEqual(erradas, [], "verificacoes citadas que o conferir_plano.py nao tem")

    def test_nenhuma_referencia_ao_lugar_antigo(self):
        ANTIGOS = [(r"`PADRAO\.md`|PADRAO\.md,? se[çc][ãa]o|PADRAO, regra", "o PADRAO.md, dividido em metodo/"),
                   (r"destilados/(modelo|criterios|fluxo_emenda|enquadramento_cnes)\.md", "destilados/ que saiu para metodo/ ou biblioteca/"),
                   (r"(?<![/\w])normas/(?!_)", "normas/ sem biblioteca/"),
                   (r"(?<![/\w.])redacao_NN/", "redacao_NN/ sem planos/"),
                   (r"python3? (conferir_plano|consultar|testar_tudo|extrair_devolutiva)\.py", "script sem ferramentas/")]
        achados = []
        for doc in DOCS:
            if doc in HISTORICOS:
                continue
            for n, linha in enumerate(texto(doc).splitlines(), 1):
                for pad, o_que in ANTIGOS:
                    if re.search(pad, linha) and "biblioteca/normas" not in linha[:0]:
                        if o_que.startswith("normas/") and "biblioteca/normas" in linha:
                            continue
                        achados.append(f"{doc.relative_to(RAIZ)}:{n}: {o_que}")
        self.assertEqual(achados, [], "referencias ao lugar antigo")

    def test_cada_agente_segue_um_metodo_e_esta_no_readme(self):
        readme = texto(RAIZ / "README.md")
        problemas = []
        for ag in sorted(AGENTES.glob("*.md")):
            txt = texto(ag)
            nome = re.search(r"^name:\s*(\S+)", txt, re.M)
            if not nome or not re.search(r"^description:\s*\S", txt, re.M):
                problemas.append(f"{ag.name}: sem name ou description no cabecalho"); continue
            cabecalho = txt.split("\n---", 1)[0]
            for campo in ("model", "effort"):
                if not re.search(rf"^{campo}:\s*\S", cabecalho, re.M):
                    problemas.append(f"{ag.name}: sem {campo} no cabecalho (herdaria o da conversa)")
            metodo = re.search(r"`(metodo/[^`]+\.md)`", txt)
            if not metodo or not (RAIZ / metodo.group(1)).exists():
                problemas.append(f"{ag.name}: nao aponta para um metodo que exista em metodo/")
            if f"`{nome.group(1)}`" not in readme:
                problemas.append(f"{ag.name}: o agente {nome.group(1)} nao esta na tabela do README")
        self.assertEqual(problemas, [])

    def test_leia_lista_todos_os_arquivos_do_metodo(self):
        leia = texto(METODO / "LEIA.md")
        fora = [p.relative_to(METODO).as_posix() for p in sorted(METODO.rglob("*.md"))
                if p.name not in leia]
        self.assertEqual(fora, [], "arquivos de metodo/ que o LEIA.md nao lista")


if __name__ == "__main__":
    unittest.main(verbosity=2)
