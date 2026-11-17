#!/usr/bin/env python3
"""
consultar.py - a base de erros e acertos, consultada pelo terminal.

Uso:
    python consultar.py                           panorama da base
    python consultar.py LI-013                    um registro, o que ele cita e quem o cita
    python consultar.py buscar locacao consultorio   busca em todos os registros
    python consultar.py plano pt_ses_01           erros, acertos e controle de um plano aprovado
    python consultar.py tema dimensionamento      as licoes de um tema, com a evidencia
    python consultar.py licoes --gravidade questiona  as licoes, com filtros
    python consultar.py checklist                 o checklist de um plano novo
    python consultar.py checklist planos/redacao_05/ --saida planos/redacao_05/checklist.md
                                                  o mesmo, com o resultado do conferir_plano.py
    python consultar.py criterios                 regenera metodo/criterios.md de licoes.csv
    python consultar.py criterios --conferir      so confere se criterios.md esta em dia

POR QUE ISTO EXISTE

Os registros guardam tres coisas diferentes: o que se OBSERVOU nos planos
aprovados (achados.csv), o que a norma e o termo EXIGEM (obrigacoes.csv) e o que
o controle ATACOU depois da aprovacao (as pecas CT do acervo). Nenhum dos tres
responde, sozinho, a pergunta de quem redige: o que fazer no nosso plano. A
resposta mora em licoes.csv - regra no imperativo, com a origem e o modo de
conferir - e este script liga as quatro pontas:

  - de uma licao se chega a evidencia (o achado, a clausula, a representacao);
  - de um achado se chega a licao que ele gerou e ao registro que o corrige
    (o AC-014 aponta para o AC-058, que o desmente);
  - de um plano aprovado se chega a tudo o que ele ensinou, de bom e de ruim;
  - do nosso plano se chega ao checklist, com as verificacoes automaticas ja
    rodadas pelo conferir_plano.py e as perguntas que so uma pessoa responde.

A busca ignora acento e caixa. So biblioteca padrao. Nada aqui altera registro,
salvo o criterios.md, que e derivado de licoes.csv e se regenera inteiro.
"""

import argparse
import csv
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

from comum import CRITERIOS, REGISTROS, escrever_texto, saida_utf8, sem_acento

REG = REGISTROS

# arquivo, campo que resume a linha
ARQUIVOS = [("licoes.csv", "regra"), ("achados.csv", "achado"), ("obrigacoes.csv", "exigencia"),
            ("exigencias_resposta.csv", "exigencia"), ("acervo.csv", "titulo")]

TEMAS = [
    ("codigos_sigtap", "Códigos SIGTAP"),
    ("valor_unitario", "Valor unitário"),
    ("objeto", "Objeto e unidade de aferição"),
    ("enquadramento_cnes", "Enquadramento no CNES"),
    ("metas", "Metas e indicadores"),
    ("dimensionamento", "Dimensionamento"),
    ("custo_apoio", "Custo de apoio"),
    ("precos", "Preços e planilha"),
    ("sobreposicao", "Sobreposição entre convênios"),
    ("capacidade_executor", "Capacidade do executor"),
    ("instrumento", "Instrumento, base legal e recurso"),
    ("desembolso_vigencia", "Desembolso e vigência"),
    ("faturamento_sus", "Registro e faturamento no SUS"),
    ("controle_social", "Controle social"),
    ("riscos", "Riscos"),
    ("redacao", "Redação"),
    ("uso_do_acervo", "Uso do acervo"),
    ("diligencia", "Diligência da SES-DF"),
]
ROTULO_TEMA = dict(TEMAS)
ORDEM_TEMA = {t: i for i, (t, _) in enumerate(TEMAS)}

GRAVIDADES = [
    ("reprova", "Reprova", "a análise da SES-DF ou o termo barram"),
    ("questiona", "Questiona", "passou na SES-DF, e o controle externo atacou ou atacaria"),
    ("melhora", "Melhora", "boa prática, que separa o plano excelente do mínimo viável"),
]
ORDEM_GRAVIDADE = {g: i for i, (g, _, _) in enumerate(GRAVIDADES)}

EIXOS = [
    ("administracao", "Eixo 1 — Administração: o que aprova, o que reprova e o que o controle ataca"),
    ("qualidade", "Eixo 2 — Qualidade: o que é boa prática"),
]

# qualidade do achado -> como o plano entra na conta de quem o le
LADO = {"falha": "erros", "bom_exemplo": "acertos", "aceitavel": "acertos", "neutro": "observacoes"}

RE_ID = re.compile(r"\b(?:AC|OB|CT|IT|NM|DD|EX|LI)-\d{3}\b|\bpt_ses_\d{2}(?:\.\.\d{2})?\b")
RE_FAIXA = re.compile(r"pt_ses_(\d{2})\.\.(\d{2})")
RE_VEREDITO = re.compile(r"\s{2}([A-Z])\s{2}(.+?)\s+(PASSOU|FALHOU|NAO SE APLICA)\s*$")
LARGURA = 100


# ------------------------------------------------------------------ a base

def expandir(ref):
    """'pt_ses_02..04' -> [pt_ses_02, pt_ses_03, pt_ses_04]"""
    m = RE_FAIXA.fullmatch(ref)
    if not m:
        return [ref]
    return [f"pt_ses_{k:02d}" for k in range(int(m.group(1)), int(m.group(2)) + 1)]


class Base:
    """os registros lidos de uma vez, com as referencias nos dois sentidos"""

    def __init__(self, pasta=REG):
        self.reg = {}            # id -> (arquivo, linha)
        self.ordem = []
        for arquivo, _ in ARQUIVOS:
            caminho = pasta / arquivo
            if not caminho.exists():
                continue
            with caminho.open(encoding="utf-8", newline="") as f:
                for linha in csv.DictReader(f):
                    self.reg[linha["id"]] = (arquivo, linha)
                    self.ordem.append(linha["id"])
        self.cita = {}
        self.citado_por = {}
        for i in self.ordem:
            _, linha = self.reg[i]
            refs = []
            for campo, valor in linha.items():
                if campo == "id" or not valor:
                    continue
                for r in RE_ID.findall(valor):
                    refs.extend(expandir(r))
            refs = [r for r in dict.fromkeys(refs) if r != i]
            self.cita[i] = refs
            for r in refs:
                self.citado_por.setdefault(r, []).append(i)

    def resumo(self, i, n=110):
        if i not in self.reg:
            return "(nao registrado)"
        arquivo, linha = self.reg[i]
        campo = dict(ARQUIVOS)[arquivo]
        txt = re.sub(r"\s+", " ", linha.get(campo, "")).strip()
        return txt if len(txt) <= n else txt[:n - 3].rstrip() + "..."

    def licoes(self, **filtro):
        out = []
        for i in self.ordem:
            arquivo, l = self.reg[i]
            if arquivo != "licoes.csv":
                continue
            if all(not v or l.get(k) == v for k, v in filtro.items()):
                out.append(l)
        return out

    def achados_do_plano(self, plano):
        out = []
        for i in self.ordem:
            arquivo, l = self.reg[i]
            if arquivo == "achados.csv" and plano in expandir(l["acervo_id"]):
                out.append(l)
        return out

    def documentos_do_plano(self, plano):
        out = []
        for i in self.ordem:
            arquivo, l = self.reg[i]
            if arquivo == "acervo.csv" and l["tipo"] in ("controle", "instrumento") \
                    and plano in expandir(l.get("plano_relacionado", "")):
                out.append(l)
        return out


# ------------------------------------------------------------------ saida

def envolver(txt, recuo="    ", largura=LARGURA):
    """quebra em linhas; a continuacao alinha pelo recuo, com seta ou sem"""
    return textwrap.fill(re.sub(r"\s+", " ", txt).strip(), largura, initial_indent=recuo,
                         subsequent_indent=" " * len(recuo))


def revisto_por(base, i):
    """registros que corrigem ou retificam este - o AC-058 desmente o AC-014"""
    return [r for r in base.citado_por.get(i, [])
            if re.search(r"\b(corrige|retifica)", " ".join(base.reg[r][1].values()), re.I)
            and re.search(rf"(corrige|retifica)[^.]{{0,40}}{i}", " ".join(base.reg[r][1].values()), re.I)]


def origem(l):
    return [i.strip() for i in l["origem"].split(";") if i.strip()]


def letras(verificacao):
    m = re.fullmatch(r"(?:automatica|parcial):([A-Z,]+)", verificacao)
    return m.group(1).split(",") if m else []


def rotulo_verificacao(v):
    if v == "manual":
        return "manual"
    modo, ls = v.split(":")
    return f"{'automática' if modo == 'automatica' else 'parcial'} ({', '.join(ls.split(','))})"


def imprimir_licao(base, l, com_origem=True):
    print(f"  {l['id']}  [{l['gravidade']}] {l['tipo']} · {ROTULO_TEMA.get(l['tema'], l['tema'])}"
          f" · {l['eixo']}")
    print(envolver(l["regra"]))
    print(envolver("por quê: " + l["por_que"], "      "))
    print(envolver("verificação: " + rotulo_verificacao(l["verificacao"]), "      "))
    if l["pergunta"]:
        print(envolver("pergunta: " + l["pergunta"], "      "))
    if com_origem:
        for i in origem(l):
            print(envolver(f"{i}  {base.resumo(i, 90)}", "      <- "))
    print()


# ------------------------------------------------------------------ comandos

def cmd_panorama(base, _args):
    contagem = {}
    for i in base.ordem:
        contagem[base.reg[i][0]] = contagem.get(base.reg[i][0], 0) + 1
    print("\nBASE DE ERROS E ACERTOS")
    print("=" * LARGURA)
    for arquivo, _ in ARQUIVOS:
        print(f"  registros/{arquivo:<26} {contagem.get(arquivo, 0):>4} linhas")
    lic = base.licoes()
    print(f"\nLICOES ({len(lic)})")
    for g, rotulo, sentido in GRAVIDADES:
        n = [l for l in lic if l["gravidade"] == g]
        erros = sum(1 for l in n if l["tipo"] == "erro")
        print(f"  {rotulo:<10} {len(n):>3}  ({erros} erros, {len(n) - erros} acertos) — {sentido}")
    print("\n  por tema:")
    for t, rotulo in TEMAS:
        n = len([l for l in lic if l["tema"] == t])
        if n:
            print(f"    {t:<22} {n:>3}  {rotulo}")
    print("\nPLANOS APROVADOS")
    for i in base.ordem:
        arquivo, l = base.reg[i]
        if arquivo != "acervo.csv" or l["tipo"] != "plano":
            continue
        lados = {"erros": 0, "acertos": 0, "observacoes": 0}
        for a in base.achados_do_plano(i):
            lados[LADO.get(a["qualidade"], "observacoes")] += 1
        ctrl = [d["id"] for d in base.documentos_do_plano(i) if d["tipo"] == "controle"]
        print(f"  {i}  {lados['erros']:>3} erros  {lados['acertos']:>3} acertos  "
              f"{lados['observacoes']:>3} observacoes   controle: {', '.join(ctrl) or '-'}")
    print("\n  python consultar.py <id> | buscar <termo> | plano <pt_ses_NN> | tema <tema> | "
          "licoes | checklist [plano/]\n")
    return 0


def cmd_registro(base, args):
    i = args.id
    if i not in base.reg:
        print(f"{i} nao existe nos registros. Tente: python consultar.py buscar {i}")
        return 1
    arquivo, l = base.reg[i]
    print(f"\n{i} — registros/{arquivo}")
    print("=" * LARGURA)
    if revisto_por(base, i):
        print(f"  ATENCAO: revisto por {', '.join(revisto_por(base, i))} - ler junto\n")
    for campo, valor in l.items():
        if campo == "id" or not valor:
            continue
        if len(valor) < 80:
            print(f"  {campo}: {valor}")
        else:
            print(f"  {campo}:")
            print(envolver(valor))
    if base.cita.get(i):
        print("\n  cita:")
        for r in base.cita[i]:
            print(envolver(f"{r}  {base.resumo(r, 90)}", "    -> "))
    if base.citado_por.get(i):
        print("\n  citado por:")
        for r in base.citado_por[i]:
            print(envolver(f"{r}  {base.resumo(r, 90)}", "    <- "))
    print()
    return 0


def buscar(base, termos):
    """[(id, trecho)] dos registros que tem todos os termos, sem acento nem caixa"""
    termos = [sem_acento(t).lower() for t in termos]
    out = []
    for i in base.ordem:
        texto = " | ".join(v for v in base.reg[i][1].values() if v)
        plano = sem_acento(texto).lower()
        if all(t in plano for t in termos):
            k = plano.find(termos[0])
            out.append((i, re.sub(r"\s+", " ", texto[max(0, k - 70):k + 110]).strip()))
    return out


def cmd_buscar(base, args):
    achados = buscar(base, args.termos)
    print()
    for i, trecho in achados:
        print(f"  {i:<10} {base.reg[i][0]:<24} {base.resumo(i, 62)}")
        print(envolver("..." + trecho + "...", "             "))
    print(f"\n  {len(achados)} registro(s) com: {' + '.join(args.termos)}\n")
    return 0 if achados else 1


def cmd_plano(base, args):
    p = args.plano
    if p not in base.reg:
        print(f"{p} nao esta no acervo")
        return 1
    print(f"\n{p} — {base.resumo(p)}")
    print("=" * LARGURA)
    docs = base.documentos_do_plano(p)
    if docs:
        print("\n  INSTRUMENTO E CONTROLE")
        for d in docs:
            print(envolver(f"{d['id']}  [{d['especie']}] {d['titulo']}"))
    grupos = {"erros": [], "acertos": [], "observacoes": []}
    for a in base.achados_do_plano(p):
        grupos[LADO.get(a["qualidade"], "observacoes")].append(a)
    for lado, titulo in (("erros", "ERROS - o que nao repetir"),
                         ("acertos", "ACERTOS - o que aproveitar"),
                         ("observacoes", "OBSERVACOES")):
        if not grupos[lado]:
            continue
        print(f"\n  {titulo} ({len(grupos[lado])})")
        for a in grupos[lado]:
            print(envolver(f"{a['id']}  [{a['classificacao']}] {base.resumo(a['id'], 200)}"))
            if revisto_por(base, a["id"]):
                print(envolver(f"atencao: revisto por {', '.join(revisto_por(base, a['id']))}",
                               "        "))
    origens = {a["id"] for g in grupos.values() for a in g} | {d["id"] for d in docs}
    lic = [l for l in base.licoes() if origens & set(origem(l))]
    if lic:
        print(f"\n  LICOES QUE SAIRAM DAQUI ({len(lic)})")
        for l in lic:
            print(envolver(f"{l['id']}  [{l['gravidade']}] {l['regra']}"))
    print()
    return 0


def cmd_tema(base, args):
    if args.tema not in ROTULO_TEMA:
        print("tema desconhecido. Temas: " + ", ".join(t for t, _ in TEMAS))
        return 1
    lic = base.licoes(tema=args.tema)
    print(f"\n{ROTULO_TEMA[args.tema].upper()} — {len(lic)} licao(oes)")
    print("=" * LARGURA)
    for l in sorted(lic, key=lambda l: (ORDEM_GRAVIDADE[l["gravidade"]], l["id"])):
        imprimir_licao(base, l)
    return 0


def cmd_licoes(base, args):
    lic = base.licoes(eixo=args.eixo, tipo=args.tipo, gravidade=args.gravidade, tema=args.tema)
    print()
    for l in sorted(lic, key=lambda l: (ORDEM_GRAVIDADE[l["gravidade"]], ORDEM_TEMA[l["tema"]], l["id"])):
        print(f"  {l['id']}  {l['gravidade']:<9} {l['tipo']:<6} {l['tema']:<20} "
              f"{rotulo_verificacao(l['verificacao'])}")
        print(envolver(l["regra"], "        "))
    print(f"\n  {len(lic)} licao(oes)\n")
    return 0


def rodar_conferencia(plano):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    # check=False: plano com verificacao falhando sai com codigo 1, e o relatorio e o que interessa
    r = subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "conferir_plano.py"), str(plano)],
                       capture_output=True, encoding="utf-8", errors="replace", env=env, check=False)
    v = {}
    for linha in r.stdout.splitlines():
        m = RE_VEREDITO.match(linha)
        # a N tem duas funcoes; a pior das duas decide
        if m and v.get(m.group(1)) != "FALHOU":
            v[m.group(1)] = m.group(3)
    return v, r.stdout + r.stderr


def checklist(base, plano=None):
    vered, saida = ({}, "") if plano is None else rodar_conferencia(plano)
    if plano is not None and not vered:
        raise SystemExit("o conferir_plano.py nao produziu relatorio legivel:\n" + saida)
    alvo = f"o plano `{Path(plano).name}`" if plano else "um plano novo"
    ls = [f"# Checklist — {alvo}", "",
          "Gerado por `python3 ferramentas/consultar.py checklist` a partir de `registros/licoes.csv`.",
          "Marcado `[x]` só o que o `conferir_plano.py` conferiu e passou; o resto é pergunta",
          "que uma pessoa responde antes do protocolo. `python3 ferramentas/consultar.py LI-NNN` abre a lição",
          "com a evidência.", ""]
    pend = falhas = 0
    for g, rotulo, sentido in GRAVIDADES:
        lic = sorted(base.licoes(gravidade=g), key=lambda l: (ORDEM_TEMA[l["tema"]], l["id"]))
        ls += [f"## {rotulo} — {sentido}", ""]
        for l in lic:
            modo = l["verificacao"].split(":")[0]
            estados = [vered.get(x) for x in letras(l["verificacao"])]
            if modo == "manual" or not vered:
                marca, nota = " ", ("" if modo == "manual" else
                                    f" — conferir_plano {', '.join(letras(l['verificacao']))}")
            elif "FALHOU" in estados:
                marca, nota = " ", " — **FALHOU** no conferir_plano " + ", ".join(
                    x for x in letras(l["verificacao"]) if vered.get(x) == "FALHOU")
                falhas += 1
            elif all(e == "NAO SE APLICA" for e in estados):
                marca, nota = "x", " — não se aplica a este plano"
            else:
                marca, nota = ("x" if modo == "automatica" else " "), \
                    f" — conferir_plano {', '.join(letras(l['verificacao']))} passou"
            if marca == " ":
                pend += 1
            ls.append(f"- [{marca}] **{l['id']}** {l['regra']}{nota}")
            if modo != "automatica" and l["pergunta"]:
                ls.append(f"  - {l['pergunta']}")
        ls.append("")
    ls.append(f"{pend} item(ns) em aberto" + (f", {falhas} com verificação que falhou" if falhas else "") + ".")
    return "\n".join(ls) + "\n", falhas


def cmd_checklist(base, args):
    texto, falhas = checklist(base, args.plano)
    if args.saida:
        escrever_texto(Path(args.saida), texto)
        print(f"checklist gravado em {args.saida}")
    else:
        print(texto)
    return 1 if falhas else 0


def gerar_criterios(base):
    lic = base.licoes()
    n_adm = len([l for l in lic if l["eixo"] == "administracao"])
    ls = ["# criterios.md — o que aprova, o que o controle ataca e o que é boa prática", "",
          "> Gerado por `python3 ferramentas/consultar.py criterios` a partir de `registros/licoes.csv`.",
          "> Não editar à mão: corrigir a lição e gerar de novo.", "",
          (f"{len(lic)} lições: {n_adm} no eixo da administração, {len(lic) - n_adm} no da "
           "qualidade. Cada uma é uma regra para o nosso plano, destilada do que os cinco planos "
           "aprovados fizeram, do que a norma e o termo exigem e do que o controle externo atacou "
           "depois da aprovação."), "",
          "Como ler:", ""]
    for g, _, sentido in GRAVIDADES:
        ls.append(f"- **{g}** — {sentido};")
    ls += [("- **verificação** — `automática`: o `conferir_plano.py` confere sozinho; `parcial`: "
            "confere uma parte e a pergunta cobre o resto; `manual`: só a pergunta;"),
           ("- **origem** — os registros de onde a lição saiu. `python3 ferramentas/consultar.py <id>` abre "
            "cada um, com o que ele cita e quem o cita."), "",
           "Para um plano em redação: `python3 ferramentas/consultar.py checklist planos/redacao_NN/`.", ""]
    for eixo, titulo in EIXOS:
        ls += [f"## {titulo}", ""]
        doeixo = [l for l in lic if l["eixo"] == eixo]
        for t, rotulo in TEMAS:
            dotema = sorted([l for l in doeixo if l["tema"] == t],
                            key=lambda l: (ORDEM_GRAVIDADE[l["gravidade"]], l["id"]))
            if not dotema:
                continue
            ls += [f"### {rotulo}", ""]
            for l in dotema:
                ls += [f"**{l['id']}** · {l['tipo']} · {l['gravidade']} — {l['regra']}", "",
                       f"- Por quê: {l['por_que']}",
                       f"- Verificação: {rotulo_verificacao(l['verificacao'])}"
                       + (f" — {l['pergunta']}" if l["pergunta"] else ""),
                       f"- Origem: {', '.join(origem(l))}", ""]
    return "\n".join(ls).rstrip() + "\n"


def cmd_criterios(base, args):
    texto = gerar_criterios(base)
    atual = CRITERIOS.read_text(encoding="utf-8") if CRITERIOS.exists() else None
    if args.conferir:
        if atual != texto:
            print("criterios.md desatualizado em relacao a registros/licoes.csv - "
                  "rode: python3 ferramentas/consultar.py criterios")
            return 1
        print("criterios.md em dia")
        return 0
    escrever_texto(CRITERIOS, texto)
    print(f"criterios.md {'regenerado' if atual else 'criado'} — {len(base.licoes())} licoes")
    return 0


# ------------------------------------------------------------------ main

def main(argv=None):
    saida_utf8()
    argv = sys.argv[1:] if argv is None else argv
    base = Base()
    if not argv:
        return cmd_panorama(base, None)
    # atalhos: "consultar.py AC-070" e "consultar.py pt_ses_01"
    if re.fullmatch(r"pt_ses_\d{2}", argv[0]):
        argv = ["plano"] + argv
    elif RE_ID.fullmatch(argv[0]):
        argv = ["ver"] + argv

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("ver", help="um registro")
    s.add_argument("id")
    s = sub.add_parser("buscar", help="busca em todos os registros")
    s.add_argument("termos", nargs="+")
    s = sub.add_parser("plano", help="erros, acertos e controle de um plano aprovado")
    s.add_argument("plano")
    s = sub.add_parser("tema", help="as licoes de um tema")
    s.add_argument("tema")
    s = sub.add_parser("licoes", help="lista de licoes, com filtros")
    s.add_argument("--eixo")
    s.add_argument("--tipo")
    s.add_argument("--gravidade")
    s.add_argument("--tema")
    s = sub.add_parser("checklist", help="checklist de um plano")
    s.add_argument("plano", nargs="?")
    s.add_argument("--saida", help="grava o checklist em markdown neste arquivo")
    s = sub.add_parser("criterios", help="regenera criterios.md")
    s.add_argument("--conferir", action="store_true")
    args = ap.parse_args(argv)
    return {"ver": cmd_registro, "buscar": cmd_buscar, "plano": cmd_plano, "tema": cmd_tema,
            "licoes": cmd_licoes, "checklist": cmd_checklist,
            "criterios": cmd_criterios}[args.cmd](base, args)


if __name__ == "__main__":
    sys.exit(main())
