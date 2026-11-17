#!/usr/bin/env python3
"""
conferir_pre_plano.py - a bateria do pre-plano (PT simplificado).

Nao altera nada. Le o documento indicado e o estado.yaml da pasta dele.

Uso:
    python3 conferir_pre_plano.py planos/redacao_05/plano_v1_geral.md
    python3 conferir_pre_plano.py planos/redacao_05/plano_v1_geral.md --verboso

POR QUE ISTO EXISTE

O pre-plano e outro produto: serve para a SES decidir se e como fazer o projeto, e
todo numero escrito nele vira a regua do plano detalhado (metodo/pre_plano/). Ate
08/10/2026 nao tinha conferencia nenhuma, e o conferir_plano.py nao serve: cobra
planilha, curva e desembolso que o pre-plano nao pode ter.

AS VERIFICACOES

DO PADRAO, AS MESMAS DO conferir_plano.py - as regras de metodo/comum.md valem para
as duas trilhas, e o codigo e um so:
  J  a estrutura do formulario da SES, campo a campo (formulario_ses_parceria)
  K  forma dos titulos          L  regra do metodo           M  normas com lastro
  Q  voz do documento           S  regua contra o proponente T  numero sem lastro
  U  ausencia anunciada
  W  codigos e valores contra o catalogo do SIGTAP           X  rubrica vedada

PROPRIAS DO PRE-PLANO
  PA SO CUSTO ASSISTENCIAL   nenhuma linha de valor da aplicacao das despesas e de
                             gestao, apoio ou pessoal; nenhum percentual ali.
  PB NADA DO PLANO DETALHADO nenhum quadro de equipe, curva mensal, capacidade por
                             polo ou parcela de desembolso.
  PE TOTAIS                  Valor Total <= recurso do estado.yaml; aplicacao das
                             despesas <= Valor Total; a meta em valor = a aplicacao.

Saida: uma linha por verificacao, PASSOU / FALHOU / NAO SE APLICA. Codigo 1 se
alguma falhar.
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

import comum
import conferir_plano as P
from comum import reais, saida_utf8

ESTRUTURA_DO_FORMULARIO = "formulario_ses_parceria"
REUSADAS = (P.verificar_J, P.verificar_K, P.verificar_L, P.verificar_M, P.verificar_Q,
            P.verificar_S, P.verificar_T, P.verificar_U, P.verificar_W, P.verificar_X)

APOIO = re.compile(r"gest[ãa]o|apoio|coordena|administra|recursos humanos|pessoal|\bpostos?\b|"
                   r"sal[áa]ri|encargo|dire[çc][ãa]o|assessoria|contab|custo acess", re.I)
EQUIPE = re.compile(r"\bcargo|\bposto|sal[áa]rio|remunera[çc][ãa]o", re.I)
DESEMBOLSO = re.compile(r"parcela|desembolso", re.I)
CAPACIDADE = re.compile(r"\bsalas?\b|tom[óo]grafo|equipamentos?\b|capacidade|por dia [úu]til|\bpolos?\b", re.I)
MES_UNICO = re.compile(r"^\**\s*m[êe]s\s+\d+\s*\**$", re.I)


secao = P.secao        # uma funcao so, a do conferir_plano.py


def valores_reais(txt: str):
    return [comum.valor_moeda(v) for v in re.findall(r"R\$\s*([\d.]+,\d{2})", txt)]


def verificar_PA(d, r):
    """so custo assistencial na aplicacao das despesas"""
    falhas = []
    s8 = secao(d["plano"], 8)
    for t in P.tabelas(s8):
        for linha in t[1:]:
            if not any(re.search(r"R\$\s*[\d.]+,\d{2}", c) for c in linha):
                continue
            if APOIO.search(linha[0]):
                falhas.append(f"linha de apoio na aplicacao das despesas: '{linha[0][:60]}'")
    for m in re.finditer(r"\d+(?:,\d+)?\s*%", s8):
        falhas.append(f"percentual na aplicacao das despesas: '{m.group(0)}'")
    r.add("PA", "so custo assistencial", not falhas, falhas)


def verificar_PB(d, r):
    """nada do plano detalhado: equipe, curva mensal, capacidade, parcelas"""
    falhas = []
    for t in d["tbs"]:
        cab = " ".join(t[0])
        if EQUIPE.search(cab):
            falhas.append(f"quadro de equipe ou de postos: cabecalho '{cab[:60]}'")
        if DESEMBOLSO.search(cab):
            falhas.append(f"quadro de desembolso: cabecalho '{cab[:60]}'")
        meses = [l for l in t[1:] if l and MES_UNICO.match(l[0].strip())
                 and any(P.num(c) is not None for c in l[1:])]
        if len(meses) >= 2:
            falhas.append(f"curva mensal: {len(meses)} linhas de mes com quantidade")
        for l in t[1:]:
            if l and CAPACIDADE.search(l[0]) and any(P.num(c) is not None for c in l[1:]):
                falhas.append(f"capacidade ou polo com numero: '{l[0][:60]}'")
    r.add("PB", "nada do plano detalhado", not falhas, falhas)


def verificar_PE(d, r):
    """os totais: Valor Total, recurso, aplicacao e meta em valor"""
    falhas = []
    recurso = P.escalar(d["estado"], "recurso.valor")
    total = None
    for t in P.tabelas(secao(d["plano"], 1)):
        for l in t:
            if l and re.search(r"valor total", l[0], re.I):
                vs = valores_reais(" ".join(l[1:]))
                total = vs[0] if vs else None
    if total is None:
        r.add("PE", "totais", False, ["Valor Total nao encontrado na primeira secao"]); return
    if recurso and total > recurso + P.TOL:
        falhas.append(f"Valor Total {reais(total)} acima do recurso {reais(recurso)}")
    aplic = 0.0
    for t in P.tabelas(secao(d["plano"], 8)):
        for l in t[1:]:
            vs = valores_reais(l[-1]) if l else []
            aplic += vs[0] if vs else 0.0
    if aplic > total + P.TOL:
        falhas.append(f"aplicacao das despesas {reais(aplic)} acima do Valor Total {reais(total)}")
    metas = [v for t in P.tabelas(secao(d["plano"], 6))
             if any("meta" in P.chave(c) for c in t[0])
             for l in t[1:] for v in valores_reais(" ".join(l[1:]))]
    if metas and aplic and not P.perto(sum(metas), aplic):
        falhas.append(f"metas em valor somam {reais(sum(metas))}, aplicacao das despesas {reais(aplic)}")
    det = f"Valor Total {reais(total)}" + (f", recurso {reais(recurso)}" if recurso else "")
    r.add("PE", f"totais ({det})", not falhas, falhas)


def main():
    ap = argparse.ArgumentParser(description="confere um pre-plano do projeto")
    ap.add_argument("documento", help="o pre-plano, por exemplo planos/redacao_05/plano_v1_geral.md")
    ap.add_argument("--verboso", action="store_true")
    ap.add_argument("--raiz", help="raiz do projeto; padrao: a raiz do repositorio")
    args = ap.parse_args()
    saida_utf8()
    doc = Path(args.documento).resolve()
    if not doc.exists():
        raise SystemExit(f"erro: {doc} nao existe")
    raiz = Path(args.raiz).resolve() if args.raiz else comum.RAIZ
    P.BASE, P.RAIZ = doc.parent, raiz
    P.ESTRUTURA = raiz / comum.ESTRUTURA_PLANO.relative_to(comum.RAIZ)
    P.NORMAS = raiz / comum.NORMAS.relative_to(comum.RAIZ)
    estado = doc.parent / "estado.yaml"
    texto = doc.read_text(encoding="utf-8")
    d = {"plano": texto, "tbs": P.tabelas(texto),
         # o pre-plano segue o formulario da SES por definicao
         "estado": f"estrutura: {ESTRUTURA_DO_FORMULARIO}\n"
                   + (estado.read_text(encoding="utf-8") if estado.exists() else "")}
    r = P.R()
    for f in REUSADAS + (verificar_PA, verificar_PB, verificar_PE):
        try:
            f(d, r)
        except Exception as e:
            r.add(f.__name__.split("_")[1], f.__name__, False, [f"erro na verificacao: {e!r}"])
    print()
    print(f"CONFERENCIA DO PRE-PLANO — {doc.parent.name}/{doc.name}")
    print("=" * 78)
    for sigla, nome, ok, det, na in r.itens:
        veredito = "NAO SE APLICA" if na else ("PASSOU" if ok else "FALHOU")
        print(f"  {sigla}  {nome:<46} {veredito}")
        if det and (not ok or args.verboso):
            for x in det[:20]:
                print(f"        - {x}")
    print("=" * 78)
    n_ok = sum(1 for _, _, ok, _, na in r.itens if ok and not na)
    print(f"  {n_ok}/{len(r.itens)} verificacoes passaram")
    print()
    return 1 if r.falhou else 0


if __name__ == "__main__":
    sys.exit(main())
