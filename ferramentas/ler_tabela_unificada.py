#!/usr/bin/env python3
"""
ler_tabela_unificada.py - le a ficha de um procedimento no pacote oficial da Tabela
Unificada de uma competencia, sem a tela do SIGTAP.

Uso:
    python3 ler_tabela_unificada.py --baixar 102026              baixa o pacote para o cache
    python3 ler_tabela_unificada.py 102026 0902010069 [...]      a ficha de cada codigo
    python3 ler_tabela_unificada.py 102026 09.02.01.006-9 --json

O pacote e o TabelaUnificada_<AAAAMM>_v<data>.zip de
ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/, a base que o SIGTAP carrega. Ele sai
quando a competencia abre, mesmo com a tela servindo a base velha: em 22/10/2026 a tela
parou em 05/2026, e o pacote de 10/2026 estava no FTP desde 15/10 (redacao_08). As fichas
de 10/2026 foram reconstituidas pelas Notas Tecnicas sem que ninguem lesse o pacote.

O cache fica fora do repositorio (uns 2 MB por competencia): $TABELA_UNIFICADA_DIR, ou
~/.cache/planos-ses/tabela_unificada/. Vale a versao mais nova de cada competencia, porque
o FTP republica (06 a 08/2026 sairam de novo em 23/10/2026).

O que sai, por codigo: nome, valores (SA, SH, SP), sexo, idade minima e maxima (a tabela
guarda em meses), quantidade maxima, financiamento, o CID principal e as compatibilidades
com o tipo e a quantidade. Tipo 1 e "compativel" e 5 e "obrigatoria" (conferidos nas OCI
de cardiologia de 10/2026); os outros saem pelo numero.

So biblioteca padrao.
"""
from __future__ import annotations
import argparse, ftplib, io, json, os, re, sys, zipfile
from pathlib import Path

FTP_HOST, FTP_DIR = "ftp2.datasus.gov.br", "/pub/sistemas/tup/downloads"
TIPO_COMPAT = {"1": "compatível", "5": "obrigatória"}
SEXO = {"I": "ambos", "M": "masculino", "F": "feminino", "N": "não se aplica"}


def cache() -> Path:
    return Path(os.environ.get("TABELA_UNIFICADA_DIR") or Path.home() / ".cache" / "planos-ses" / "tabela_unificada")


def aaaamm(competencia: str) -> str:
    """'102026' (MMAAAA, como o nome da ficha) ou '202610' (AAAAMM, como o pacote) -> '202610'"""
    c = re.sub(r"\D", "", competencia)
    if len(c) != 6:
        raise ValueError(f"competencia {competencia!r}: MMAAAA ou AAAAMM")
    return c if int(c[:2]) > 12 else c[2:] + c[:2]


def sem_pontos(codigo: str) -> str:
    return re.sub(r"\D", "", codigo)


def com_pontos(c: str) -> str:
    return f"{c[:2]}.{c[2:4]}.{c[4:6]}.{c[6:9]}-{c[9]}"


def pacote(competencia: str) -> Path | None:
    """o pacote mais novo da competencia no cache, ou None"""
    nomes = sorted(cache().glob(f"TabelaUnificada_{aaaamm(competencia)}_v*.zip"))
    return nomes[-1] if nomes else None


def baixar(competencia: str) -> Path:
    """baixa do FTP a versao mais nova do pacote da competencia"""
    alvo = aaaamm(competencia)
    with ftplib.FTP(FTP_HOST, timeout=120) as ftp:
        ftp.login()
        ftp.cwd(FTP_DIR)
        nomes = sorted(n for n in ftp.nlst() if re.fullmatch(rf"TabelaUnificada_{alvo}_v\d+\.zip", n))
        if not nomes:
            raise SystemExit(f"o FTP ainda nao tem o pacote de {alvo[4:]}/{alvo[:4]}")
        destino = cache() / nomes[-1]
        destino.parent.mkdir(parents=True, exist_ok=True)
        if not destino.exists():
            buf = io.BytesIO()
            ftp.retrbinary(f"RETR {nomes[-1]}", buf.write)
            destino.write_bytes(buf.getvalue())
    return destino


def linhas(zf: zipfile.ZipFile, tabela: str):
    """as linhas de <tabela>.txt como dicionarios, pelas posicoes de <tabela>_layout.txt"""
    layout = zf.read(f"{tabela}_layout.txt").decode("latin-1").splitlines()[1:]
    cols = []
    for l in layout:
        nome, _, ini, fim, _ = l.split(",")
        cols.append((nome, int(ini) - 1, int(fim)))
    for l in zf.read(f"{tabela}.txt").decode("latin-1").splitlines():
        if l.strip():
            yield {nome: l[a:b].strip() for nome, a, b in cols}


def ler(competencia: str, codigos, zip_path: Path | None = None):
    """{codigo sem pontos: ficha} dos codigos no pacote; None se o pacote nao esta no cache"""
    zip_path = zip_path or pacote(competencia)
    if not zip_path:
        return None
    alvos = {sem_pontos(c) for c in codigos}
    out = {}
    with zipfile.ZipFile(zip_path) as zf:
        nomes = {}
        for l in linhas(zf, "tb_procedimento"):
            nomes[l["CO_PROCEDIMENTO"]] = l["NO_PROCEDIMENTO"]
            if l["CO_PROCEDIMENTO"] in alvos:
                out[l["CO_PROCEDIMENTO"]] = {
                    "codigo": com_pontos(l["CO_PROCEDIMENTO"]), "nome": l["NO_PROCEDIMENTO"],
                    "competencia": l["DT_COMPETENCIA"], "pacote": zip_path.name,
                    "valor_sa": int(l["VL_SA"]) / 100, "valor_sh": int(l["VL_SH"]) / 100,
                    "valor_sp": int(l["VL_SP"]) / 100, "sexo": SEXO.get(l["TP_SEXO"], l["TP_SEXO"]),
                    "idade_min_meses": int(l["VL_IDADE_MINIMA"]), "idade_max_meses": int(l["VL_IDADE_MAXIMA"]),
                    "quantidade_maxima": int(l["QT_MAXIMA_EXECUCAO"]), "financiamento": l["CO_FINANCIAMENTO"],
                    "cid_principal": [], "cid_secundario": [], "compatibilidades": []}
        fin = {l["CO_FINANCIAMENTO"]: l["NO_FINANCIAMENTO"] for l in linhas(zf, "tb_financiamento")}
        for d in out.values():
            d["financiamento"] = f"{d['financiamento']} {fin.get(d['financiamento'], '')}".strip()
        for l in linhas(zf, "rl_procedimento_cid"):
            d = out.get(l["CO_PROCEDIMENTO"])
            if d:
                d["cid_principal" if l["ST_PRINCIPAL"] == "S" else "cid_secundario"].append(l["CO_CID"])
        for l in linhas(zf, "rl_procedimento_compativel"):
            d = out.get(l["CO_PROCEDIMENTO_PRINCIPAL"])
            if d:
                tp = l["TP_COMPATIBILIDADE"]
                c = l["CO_PROCEDIMENTO_COMPATIVEL"]
                d["compatibilidades"].append({
                    "codigo": com_pontos(c), "nome": nomes.get(c, ""), "tipo": TIPO_COMPAT.get(tp, f"tipo {tp}"),
                    "quantidade": int(l["QT_PERMITIDA"]), "registro": l["CO_REGISTRO_COMPATIVEL"]})
    return out


def idade(meses: int) -> str:
    return f"{meses} meses" if meses < 12 else f"{meses // 12} anos"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("competencia", nargs="?", help="MMAAAA ou AAAAMM")
    ap.add_argument("codigos", nargs="*", help="codigos SIGTAP, com ou sem pontos")
    ap.add_argument("--baixar", metavar="COMPETENCIA", help="baixa o pacote da competencia para o cache")
    ap.add_argument("--json", action="store_true", help="a saida em JSON")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if args.baixar:
        print(baixar(args.baixar))
        if not args.codigos:
            return 0
        args.competencia = args.competencia or args.baixar
    if not args.competencia or not args.codigos:
        ap.error("informe a competencia e os codigos (ou --baixar)")
    fichas = ler(args.competencia, args.codigos)
    if fichas is None:
        raise SystemExit(f"sem o pacote de {args.competencia} em {cache()}: rode --baixar {args.competencia}")
    if args.json:
        print(json.dumps(fichas, ensure_ascii=False, indent=2))
        return 0
    for c in args.codigos:
        d = fichas.get(sem_pontos(c))
        if not d:
            print(f"\n{c}: nao esta no pacote")
            continue
        print(f"\n{d['codigo']} — {d['nome']}  ({d['pacote']})")
        print(f"  Serviço Ambulatorial R$ {d['valor_sa']:.2f} · hospitalar R$ {d['valor_sh']:.2f} · "
              f"profissional R$ {d['valor_sp']:.2f}")
        print(f"  {d['sexo']} · {idade(d['idade_min_meses'])} a {idade(d['idade_max_meses'])} · "
              f"quantidade máxima {d['quantidade_maxima']} · {d['financiamento']}")
        print(f"  CID principal ({len(d['cid_principal'])}): {', '.join(d['cid_principal'][:40])}"
              + (" ..." if len(d["cid_principal"]) > 40 else ""))
        for x in sorted(d["compatibilidades"], key=lambda x: (x["tipo"] != "obrigatória", x["codigo"])):
            print(f"  {x['tipo']:<12} {x['codigo']}  qtd {x['quantidade']}  {x['nome']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
