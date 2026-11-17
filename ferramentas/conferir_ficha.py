#!/usr/bin/env python3
"""
conferir_ficha.py - confere uma ficha do SIGTAP contra o metodo.

Uso:
    python3 conferir_ficha.py planos/redacao_NN/dados/fontes/sigtap_0904010031_092026.md

O metodo e metodo/coleta/ficha_sigtap.md. A conferencia nao le o SIGTAP: diz se o
arquivo traz o que o plano e a coleta do Mapa Social precisam, e se a ficha de uma OCI
bate com o catalogo do grupo 09 que a verificacao W usa.

AS VERIFICACOES
  A  ARQUIVO     sigtap_<10 digitos>_<MMAAAA>.md, e o codigo do titulo e o do nome
  B  LEITURA     "Lido em dd/mm/aaaa" e a competencia, igual a do nome do arquivo
  C  CAMPOS      as linhas da tabela da ficha, com o Servico Ambulatorial em reais
  D  HISTORICO   a secao, com ao menos uma linha
  E  CID         a expressao do painel, quando a ficha tem CID principal
  F  CATALOGO    OCI: valor, idade e situacao contra registros/fontes/sigtap_grupo09_*.csv
                 da mesma competencia; divergencia quer dizer catalogo desatualizado
  G  PORTARIAS   toda portaria citada no historico esta em biblioteca/normas/, pelo numero
                 e pelo ano (a validacao do texto e de quem le; regra do usuario, 09/10/2026)
  H  PACOTE      a ficha contra o pacote oficial da competencia (ler_tabela_unificada.py),
                 quando ele esta no cache: valor, idade, o CID aceito pela expressao do
                 painel e, na OCI, os obrigatorios e os compativeis

Nas fichas lidas a partir de 25/10/2026, a B exige que a linha da leitura diga de onde a
competencia veio (a tela, o pacote do FTP ou reconstituida), e a E, a expressao do CID
aceito e a do CID da finalidade, com "CID largo" quando a lista cobre um capitulo ou mais
de 20 categorias.

Codigo 1 se alguma falhar.
"""
from __future__ import annotations
import argparse, csv, re, sys
from pathlib import Path

from comum import NORMAS, REGISTROS, saida_utf8, valor_moeda
import ler_tabela_unificada as TU
from conferir_coleta import categorias, dentro, tokens

CAMPOS = [("grupo", r"grupo"), ("modalidade", r"modalidade"), ("financiamento", r"financiamento"),
          ("instrumento", r"instrumento"), ("sexo e idade", r"sexo|idade"),
          ("quantidade maxima", r"quantidade m[áa]xima"), ("atributos", r"atributo"),
          ("habilitacoes", r"habilita"), ("regras condicionadas", r"regras? condicionad"), ("CBO", r"\bcbo\b"),
          ("Servico Ambulatorial", r"servi[çc]o ambulatorial"), ("descricao", r"descri[çc][ãa]o"),
          ("CID principal", r"\bcid\b")]


def linhas_da_tabela(txt):
    """{rotulo em minusculas: valor} das linhas | rotulo | valor | da primeira tabela"""
    out = {}
    for l in txt.splitlines():
        m = re.match(r"^\|\s*\**([^|*]+?)\**\s*\|\s*(.+?)\s*\|\s*$", l)
        if m and not set(m.group(1)) <= set("-: "):
            out.setdefault(m.group(1).strip().lower(), m.group(2).strip())
    return out


def catalogo(competencia: str):
    """{codigo: linha} do catalogo do grupo 09 na competencia MMAAAA, ou None"""
    arq = REGISTROS / "fontes" / f"sigtap_grupo09_{competencia}.csv"
    if not arq.exists():
        return None
    with arq.open(encoding="utf-8", newline="") as f:
        return {l["codigo"]: l for l in csv.DictReader(f)}


# o numero da norma e o ano, no nome do arquivo: 'SAES 4282-2026', 'Portaria 287 de 07_04_2022',
# 'No 2.331, DE 10 DE DEZEMBRO DE 2024'
NUMERO_ANO = re.compile(r"(?<!\d)(\d{1,5})(?:\s*[-/]\s*|,?\s+de\s+(?:\d{1,2}[_./]\d{1,2}[_./]|"
                        r"\d{1,2}\s+de\s+[a-zçã]+\s+de\s+))((?:19|20)\d{2})(?!\d)", re.I)


def normas_no_acervo(normas: Path):
    """{(numero, ano)} das normas em biblioteca/normas/, pelo nome do arquivo: 'SAES 4795-2026'
    da ('4795', '2026'), e 'No 2.331, DE 10 DE DEZEMBRO DE 2024' da ('2331', '2024'). Nome sem
    ano nao conta: o mesmo numero de outro ano e outra norma (a SAS 287/2011 nao e a Portaria
    287 de 2022). Origem: as fichas do redacao_07, 15 a 19/10/2026."""
    if not normas.exists():
        return set()
    pares = set()
    for f in normas.rglob("*"):
        if f.is_file():
            nome = re.sub(r"(?<=\d)\.(?=\d{3}(?!\d))", "", f.name)
            pares |= {(str(int(n)), ano) for n, ano in NUMERO_ANO.findall(nome)}
    return pares


# a portaria citada: 'SAES 4.795/2026', 'SAS 7/2008', 'GM/MS nº 15/2018'
CITADA = re.compile(r"(?:SAES|GM|SAS|SCTIE|SECTICS)(?:/MS)?\s*(?:n[ºo°]\s*)?(\d{1,2}\.\d{3}|\d{1,5})/(\d{4})")


def portarias_citadas(txt):
    """{(numero, ano)} das portarias citadas no texto"""
    return {(str(int(re.sub(r"\D", "", n))), ano) for n, ano in CITADA.findall(txt)}


DESDE_FINALIDADE = "20261025"     # a data da leitura, AAAAMMDD: a regra das duas expressoes


def contra_o_pacote(txt, tabela, valor, codigo, pac):
    """as divergencias entre a ficha e o pacote oficial da competencia"""
    d = pac.get(TU.sem_pontos(codigo))
    if not d:
        return [f"{codigo} nao esta no pacote {next(iter(pac.values()), {}).get('pacote', '')}"]
    falhas = []
    if valor is not None and abs(valor - d["valor_sa"]) > 0.005:
        falhas.append(f"Servico Ambulatorial R$ {valor:.2f} na ficha e R$ {d['valor_sa']:.2f} no pacote {d['pacote']}")
    si = next((v for k, v in tabela.items() if re.search(r"sexo|idade", k)), "")
    mi = re.search(r"(\d+)\s*(mes(?:es)?|anos?)?\s*a\s*(\d+)\s*anos", si)
    if mi:
        ini = int(mi.group(1)) * (1 if (mi.group(2) or "").startswith("mes") else 12)
        if ini != d["idade_min_meses"] or int(mi.group(3)) != d["idade_max_meses"] // 12:
            falhas.append(f"idade '{mi.group(0)}' na ficha e {TU.idade(d['idade_min_meses'])} a "
                          f"{TU.idade(d['idade_max_meses'])} no pacote")
    expr = (re.search(r"^\|\s*aceito\s*\|\s*`([^`]+)`", txt, re.M | re.I)
            or re.search(r"`(codigo_cid_solicitado=\{[^`]+\})`", txt))
    if expr and d["cid_principal"]:
        e = expr.group(1)
        fora = [c for c in d["cid_principal"] if not dentro(c[:3], e)]
        sobra = [t for t in tokens(e) if not any(c.startswith(t.rstrip("*")) for c in d["cid_principal"])]
        if fora:
            falhas.append(f"{len(fora)} CID do pacote fora da expressao da ficha: {', '.join(fora[:8])}")
        if sobra:
            falhas.append(f"a expressao da ficha tem {', '.join(sobra)}, que o pacote nao traz como CID principal")
    if codigo.startswith("09."):
        ficha = {}
        for l in txt.splitlines():
            m = re.match(r"^\|\s*(\d{2}\.\d{2}\.\d{2}\.\d{3}-\d)\b[^|]*\|\s*([^|]+?)\s*\|", l)
            tipo = re.sub(r"\*", "", m.group(2)) if m else ""
            if re.match(r"\s*(obrigat|compat)", tipo, re.I):
                ficha[m.group(1)] = "obrigatória" if re.match(r"\s*obrigat", tipo, re.I) else "compatível"
        pacote = {x["codigo"]: x["tipo"] for x in d["compatibilidades"] if x["tipo"] in ("obrigatória", "compatível")}
        for c, tp in sorted(pacote.items()):
            if c not in ficha:
                falhas.append(f"{c} ({tp} no pacote) nao esta nos componentes da ficha")
            elif ficha[c] != tp:
                falhas.append(f"{c}: {ficha[c]} na ficha e {tp} no pacote")
        for c in sorted(set(ficha) - set(pacote)):
            falhas.append(f"{c} ({ficha[c]} na ficha) nao esta no pacote {d['pacote']}")
    return falhas


def verificar(md: Path, cat=None, normas: Path = NORMAS):
    txt = md.read_text(encoding="utf-8")
    itens = []

    def add(sigla, nome, falhas, na=False):
        itens.append((sigla, nome, not falhas, falhas, na))

    falhas = []
    mn = re.fullmatch(r"sigtap_(\d{10})_(\d{2})(\d{4})\.md", md.name)
    mt = re.search(r"^# SIGTAP (\d{2})\.(\d{2})\.(\d{2})\.(\d{3})-(\d)\b", txt, re.M)
    if not mn:
        falhas.append("o nome nao e sigtap_<10 digitos>_<MMAAAA>.md")
    if not mt:
        falhas.append("o titulo nao e '# SIGTAP <codigo com pontos e digito> — <nome>'")
    if mn and mt and "".join(mt.groups()) != mn.group(1):
        falhas.append(f"o codigo do titulo ({'.'.join(mt.groups()[:4])}-{mt.group(5)}) "
                      f"nao e o do nome do arquivo ({mn.group(1)})")
    add("A", "arquivo", falhas)
    codigo = f"{'.'.join(mt.groups()[:4])}-{mt.group(5)}" if mt else None
    comp_nome = f"{mn.group(2)}/{mn.group(3)}" if mn else None

    falhas = []
    ml = re.search(r"lido em (\d{2})/(\d{2})/(\d{4})", txt, re.I)
    nova = bool(ml) and ml.group(3) + ml.group(2) + ml.group(1) >= DESDE_FINALIDADE
    if not ml:
        falhas.append("sem 'Lido em dd/mm/aaaa'")
    elif nova and not re.search(r"na tela|no pacote|reconstitu", txt[:1500], re.I):
        falhas.append("a linha da leitura nao diz de onde veio a competencia: na tela, no pacote do FTP "
                      "ou reconstituida")
    mc = re.search(r"compet[êe]ncia (\d{2}/\d{4})", txt, re.I)
    if not mc:
        falhas.append("sem a competencia (MM/AAAA)")
    elif comp_nome and mc.group(1) != comp_nome:
        falhas.append(f"competencia lida {mc.group(1)}, a do nome do arquivo e {comp_nome}")
    add("B", "leitura", falhas)

    tabela = linhas_da_tabela(txt)
    falhas = [f"sem a linha '{nome}'" for nome, pad in CAMPOS
              if not any(re.search(pad, k) for k in tabela)]
    sa = next((v for k, v in tabela.items() if re.search(r"servi[çc]o ambulatorial", k)), "")
    ms = re.search(r"R\$\s*([\d.]+,\d{2})", sa)
    if sa and not ms:
        falhas.append("o Servico Ambulatorial nao traz valor em reais")
    valor = valor_moeda(ms.group(1)) if ms else None
    add("C", "campos da ficha", falhas)

    mh = re.search(r"^## Hist[óo]rico\s*$([\s\S]*?)(?=^## |\Z)", txt, re.M)
    linhas_h = [l for l in (mh.group(1).splitlines() if mh else [])
                if l.startswith("|") and not re.match(r"^\|[-|: ]+\|$", l)]
    add("D", "historico", [] if len(linhas_h) >= 2 else ["sem a secao '## Historico' com ao menos uma mudanca"])

    cid = next((v for k, v in tabela.items() if re.search(r"\bcid\b", k)), "")
    tem_cid = bool(re.search(r"[A-Z]\d{2}", cid))
    if tem_cid:
        ok = re.search(r"^## CID para o Mapa Social", txt, re.M) and re.search(
            r"codigo_cid_solicitado=\{", txt)
        falhas = [] if ok else ["sem a secao '## CID para o Mapa Social' com a expressao codigo_cid_solicitado={...}"]
        if ok and nova:
            # o CID aceito pela APAC nao e quem precisa da OCI (redacao_08, 22/10/2026)
            sec = re.search(r"^## CID para o Mapa Social\s*$([\s\S]*?)(?=^## |\Z)", txt, re.M).group(1)
            exprs = {k.lower(): v for k, v in re.findall(r"^\|\s*(aceito|finalidade)\s*\|\s*`([^`]+)`", sec, re.M | re.I)}
            for k in ("aceito", "finalidade"):
                if k not in exprs:
                    falhas.append(f"sem a linha '| {k} | `codigo_cid_solicitado={{...}}` |'")
            aceito = exprs.get("aceito", "")
            largo = any(t.endswith("*") and len(t) == 2 for t in tokens(aceito)) or categorias(aceito) > 20
            if largo and not re.search(r"CID largo", sec):
                falhas.append("o CID aceito cobre um capitulo ou mais de 20 categorias e a secao nao diz 'CID largo'")
        add("E", "CID para o Mapa Social", falhas)
    else:
        add("E", "CID para o Mapa Social", [], na=True)

    citadas = sorted(portarias_citadas(mh.group(1) if mh else ""), key=lambda p: (p[1], int(p[0])))
    no_acervo = normas_no_acervo(normas)
    faltam = [p for p in citadas if p not in no_acervo]
    add("G", f"portarias do historico no acervo ({len(citadas)})",
        [f"portaria {n}/{ano} citada no historico e sem arquivo em biblioteca/normas/" for n, ano in faltam],
        na=not citadas)

    # H: a ficha contra o pacote oficial da competencia, quando ele esta no cache
    pac = TU.ler(mn.group(2) + mn.group(3), [codigo]) if (codigo and mn) else None
    if pac is None:
        add("H", "pacote da Tabela Unificada (sem o pacote no cache)", [], na=True)
    else:
        add("H", f"pacote da Tabela Unificada", contra_o_pacote(txt, tabela, valor, codigo, pac))

    if not codigo or not codigo.startswith("09.") or not mn:
        add("F", "catalogo do grupo 09", [], na=True)
    else:
        cat = cat if cat is not None else catalogo(mn.group(2) + mn.group(3))
        if cat is None:
            add("F", "catalogo do grupo 09", [f"sem o catalogo registros/fontes/sigtap_grupo09_"
                                              f"{mn.group(2)}{mn.group(3)}.csv"]); return itens
        linha = cat.get(codigo)
        falhas = []
        if not linha:
            falhas.append(f"{codigo} nao esta no catalogo do grupo 09 da competencia")
        else:
            if "vigente" not in linha["situacao"]:
                falhas.append(f"o catalogo da {codigo} como '{linha['situacao']}'")
            vc = valor_moeda(linha["valor_total_ambulatorial"]) if linha["valor_total_ambulatorial"] else None
            if valor is not None and vc is not None and abs(vc - valor) > 0.005:
                falhas.append(f"valor da ficha R$ {ms.group(1)}, catalogo R$ {linha['valor_total_ambulatorial']}"
                              " — catalogo desatualizado: corrigir a linha pela ficha, com a portaria")
        add("F", "catalogo do grupo 09", falhas)
    return itens


def main():
    ap = argparse.ArgumentParser(description="confere uma ficha do SIGTAP")
    ap.add_argument("ficha", help="dados/fontes/sigtap_<codigo>_<MMAAAA>.md")
    args = ap.parse_args()
    saida_utf8()
    md = Path(args.ficha).resolve()
    if not md.exists():
        raise SystemExit(f"erro: {md} nao existe")
    itens = verificar(md)
    print(f"\nCONFERENCIA DA FICHA — {md.name}")
    print("=" * 78)
    for sigla, nome, ok, falhas, na in itens:
        print(f"  {sigla}  {nome:<46} {'NAO SE APLICA' if na else ('PASSOU' if ok else 'FALHOU')}")
        for x in falhas:
            print(f"        - {x}")
    print("=" * 78)
    n_ok = sum(1 for i in itens if i[2] and not i[4])
    print(f"  {n_ok}/{len(itens)} verificacoes passaram\n")
    return 0 if all(i[2] for i in itens) else 1


if __name__ == "__main__":
    sys.exit(main())
