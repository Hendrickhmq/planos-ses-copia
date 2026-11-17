#!/usr/bin/env python3
"""
testar_conferencia_pre_plano.py - a conferencia do pre-plano sabe falhar?

Uso:
    python3 testar_conferencia_pre_plano.py planos/redacao_05/plano_v1_geral.md

Injeta um erro conhecido por vez numa copia do documento e exige que a verificacao
certa do conferir_pre_plano.py falhe. Suite que passa nao prova nada; prova que nao
acusou. E o mesmo arnes do testar_conferencia_plano.py, para a outra trilha.
"""
from __future__ import annotations
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

from comum import RAIZ

AQUI = Path(__file__).resolve().parent


def na_secao(t, n, extra):
    """acrescenta texto no fim da secao de primeiro nivel n"""
    m = re.search(rf"^## {n}\. .*$", t, re.M)
    if not m:
        return None
    fim = re.search(r"^## \d+\. ", t[m.end():], re.M)
    i = m.end() + fim.start() if fim else len(t)
    return t[:i] + "\n" + extra + "\n\n" + t[i:]


def mut_PA(t):    # linha de gestao na aplicacao das despesas
    m = re.search(r"^## 8\. [\s\S]*?^\| aplica[çc][ãa]o \| valor \|\n\|[-| ]+\|\n", t, re.M)
    return t[:m.end()] + "| Coordenação e gestão do projeto | R$ 10.000,00 |\n" + t[m.end():] if m else None
def mut_PA2(t):   # percentual na aplicacao das despesas
    return na_secao(t, 8, "A gestão corresponde a 8,2% do Valor Total.")
def mut_PB(t):    # quadro de equipe
    return na_secao(t, 4, "| cargo | quantidade | salário |\n|---|---|---|\n| Coordenador | 1 | R$ 6.000,00 |")
def mut_PB2(t):   # curva mensal
    return na_secao(t, 7, "| mês | OCIs |\n|---|---|\n| Mês 2 | 350 |\n| Mês 3 | 350 |")
def mut_PE(t):    # Valor Total acima do recurso
    m = re.search(r"(\| Valor Total \| R\$ )([\d.]+,\d{2})", t)
    return t[:m.start(2)] + "9.999.999,99" + t[m.end(2):] if m else None
def mut_J(t):     # campo do formulario renomeado
    return re.sub(r"^## 5\. .*$", "## 5. Objetivos e premissas", t, count=1, flags=re.M)
def mut_S(t):     # indicador abaixo de 100%
    m = re.search(r"^## 6\. [\s\S]*?\| 100% \|", t, re.M)
    return t[:m.end() - len("| 100% |")] + "| 95% |" + t[m.end():] if m else None
def mut_W(t):     # digito verificador errado no primeiro codigo SIGTAP (OCI ou exame)
    m = re.search(r"(?<![\d.])0[1-9]\.\d{2}\.\d{2}\.\d{3}-(\d)", t)
    return t[:m.start(1)] + str((int(m.group(1)) + 3) % 10) + t[m.end(1):] if m else None
def mut_L(t):     # expressao de metodo
    return na_secao(t, 3, "O custo acessório completa o Valor Total.")
def mut_M(t):     # norma sem lastro
    return na_secao(t, 3, "Os valores seguem a Portaria SAES/MS nº 9.999/2026.")
def mut_T(t):     # percentual sem fonte
    return na_secao(t, 3, "Cerca de 37% dos usuários faltam ao primeiro agendamento.")
def mut_T2(t):    # percentual arredondado errado de um decimal da fonte
    m = re.search(r"(?<![\d,.])(\d{2})(%)", t)
    return t[:m.start(1)] + str(int(m.group(1)) + 2) + t[m.end(1):] if m and int(m.group(1)) < 98 else None
def mut_Q(t):     # voz defensiva
    return na_secao(t, 4, "O décimo mês não é folga.")

# a mutacao com predicado so conta quando o documento tem a construcao que ela morde:
# o pre-plano de exames de imagem (redacao_06) nao publica percentual da fila
MUTACOES = [
    ("PA", "linha de gestao na aplicacao das despesas", mut_PA),
    ("PA", "percentual na aplicacao das despesas",      mut_PA2),
    ("PB", "quadro de equipe com salario",              mut_PB),
    ("PB", "curva mensal de producao",                  mut_PB2),
    ("PE", "Valor Total acima do recurso",              mut_PE),
    ("J",  "campo do formulario renomeado",             mut_J),
    ("S",  "indicador pactuado abaixo de 100%",         mut_S),
    ("W",  "digito verificador errado",                 mut_W,
     lambda t: mut_W(t) is not None),   # so quando o documento cita codigo SIGTAP
    ("L",  "expressao de metodo no documento",          mut_L),
    ("M",  "norma citada sem lastro",                   mut_M),
    ("Q",  "voz defensiva",                             mut_Q),
    ("T",  "percentual sem fonte",                      mut_T),
    ("T",  "percentual da fila alterado",               mut_T2,
     lambda t: mut_T2(t) is not None),  # so quando o documento publica percentual da fila
]


def rodar(doc: Path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(AQUI / "conferir_pre_plano.py"), str(doc), "--raiz", str(RAIZ)],
                       capture_output=True, encoding="utf-8", errors="replace", env=env)
    v = {}
    for linha in r.stdout.splitlines():
        m = re.match(r"\s{2}([A-Z][A-Z0-9]*)\s{2}(.+?)\s+(PASSOU|FALHOU|NAO SE APLICA)\s*$", linha)
        if m:
            v[m.group(1)] = m.group(3)
    return v, r.stdout + r.stderr


def copia(td, doc: Path) -> Path:
    destino = Path(td) / doc.parent.name
    shutil.copytree(doc.parent, destino)
    return destino / doc.name


def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python3 testar_conferencia_pre_plano.py planos/redacao_NN/plano_vN.md")
    doc = Path(sys.argv[1]).resolve()
    print(f"\nTESTE DA CONFERENCIA DO PRE-PLANO — {doc.parent.name}/{doc.name}")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        base, saida = rodar(copia(td, doc))
    ruins = [s for s, v in base.items() if v == "FALHOU"]
    if not base:
        print("  a conferencia nao produziu relatorio legivel:"); print(saida); return 1
    if ruins:
        print(f"  ATENCAO: o estado atual ja falha em {ruins} — corrija antes de testar"); return 1
    print(f"  linha de base: {len(base)} verificacoes, nenhuma falhando")
    print("-" * 78)
    problemas, aplicadas = [], 0
    for entrada in MUTACOES:
        sigla, desc, mutador = entrada[:3]
        aplica = entrada[3] if len(entrada) > 3 else None
        with tempfile.TemporaryDirectory() as td:
            alvo = copia(td, doc)
            txt = alvo.read_text(encoding="utf-8")
            if aplica and not aplica(txt):
                print(f"  {sigla:<3} {desc:<50} NAO SE APLICA A ESTE PRE-PLANO")
                continue
            aplicadas += 1
            novo = mutador(txt)
            if novo is None or novo == txt:
                print(f"  {sigla:<3} {desc:<50} SEM ANCORA")
                problemas.append(f"{sigla}: nao achou onde injetar — {desc}"); continue
            alvo.write_text(novo, encoding="utf-8")
            v, _ = rodar(alvo)
        estado = v.get(sigla)
        outras = sorted(x for x, y in v.items() if y == "FALHOU" and x != sigla)
        extra = f"  (tambem: {','.join(outras)})" if outras else ""
        rotulo = {"FALHOU": "APANHOU", "PASSOU": "PASSOU BATIDO",
                  "NAO SE APLICA": "DESLIGADA", None: "NAO LIDA"}[estado]
        print(f"  {sigla:<3} {desc:<50} {rotulo}{extra}")
        if estado != "FALHOU":
            problemas.append(f"{sigla}: {rotulo.lower()} — {desc}")
    print("=" * 78)
    if problemas:
        print(f"  {len(problemas)} problema(s) na propria conferencia:")
        for x in problemas:
            print(f"    - {x}")
        return 1
    fora = len(MUTACOES) - aplicadas
    resto = f" ({fora} nao se aplica a este pre-plano)" if fora else ""
    print(f"  {aplicadas}/{aplicadas} erros injetados foram apanhados pela verificacao certa{resto}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
