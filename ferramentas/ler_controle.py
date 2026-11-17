#!/usr/bin/env python3
"""
ler_controle.py - o que o controle externo do DF disse no periodo: as decisoes do TCDF, as
representacoes e noticias do MPCDF e as noticias do TCDF.

Uso:
    python3 ler_controle.py --de 2026-09-01 --ate 2026-10-10
    python3 ler_controle.py --de 2026-09-01 --ate 2026-10-10 \\
        --saida registros/vigia/controle_2026-10-10.md --bruto <pasta fora do repositorio>

As fontes:
  TCDF   desde 10/03/2026, o Diario Oficial Eletronico do TCDF (DOE-TCDF), pela API publica
         (https://api-doe.tc.df.gov.br/api/publico/diarios): as atas das sessoes, com cada
         processo e a decisao ("PROCESSO No ... DECISAO No N/AAAA - O Tribunal..."), as pautas,
         os acordaos e as comunicacoes da Segecex. Antes disso, as atas no DODF, pela listagem
         por pasta (integra e edicoes extras de cada dia) e o pdftotext (poppler).
  MPCDF  o feed de noticias do site do MPC (https://mpc.tc.df.gov.br/feed/?paged=N), onde ele
         publica o resumo de cada representacao. A busca do site e fechada (REST API 401).
  TCDF   o feed de noticias (https://www2.tc.df.gov.br/category/noticias/feed/).

Classifica cada decisao e cada noticia:
  PROJETO  cita entidade ou instrumento do acervo (as siglas das entidades nas pecas de
           controle, os proponentes de biblioteca/proponentes/, os numeros de convenio dos
           planos aprovados), ou a SES-DF junto de convenio, termo de fomento, emenda,
           parceria, OCI, credenciamento ou entidade sem fins lucrativos
  SAUDE    cita a SES-DF, o IGESDF ou o Fundo de Saude do DF, sem o resto
  resto    so a contagem; o ato de pessoal (aposentadoria, pensao, admissao) fica sempre fora,
           porque nao interessa e traz o nome de terceiros

A lista e o ponto de partida: cada peca do projeto se le no texto e, se importa, vira registro
CT no acervo (metodo/coleta/normas.md, controle externo).
"""
from __future__ import annotations
import argparse, csv, html, json, re, subprocess, sys, time
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlencode

from comum import BIBLIOTECA, REGISTROS, escrever_texto, saida_utf8

ACERVO = REGISTROS / "acervo.csv"
PROPONENTES = BIBLIOTECA / "proponentes"
DODF = "https://dodf.df.gov.br/dodf/jornal"
DOE_API = "https://api-doe.tc.df.gov.br/api/publico/diarios"
DOE_SITE = "https://doe.tc.df.gov.br"
# Portaria TCDF 103/2026: desde 10/03/2026 o TCDF publica no DOE-TCDF; o DODF deixou de ter as
# atas depois de 30 dias de transicao. O DOE tem tudo desde o comeco.
DOE_INICIO = date(2026, 3, 10)
# no DOE, o que interessa e o Plenario, a Segecex e a Procuradoria; o resto e administracao
# do proprio Tribunal (pessoal, contratos, beneficios)
SECAO_DOE = re.compile(r"Plen[áa]rio|Segecex|Procuradoria", re.I)
ACORDAO = re.compile(r"AC[ÓO]RD[ÃA]O\s+N[ºo°]\s*(\d+/\d{4})")
# na ata, o registro de cada despacho singular do relator: "Representacao: PROCESSO No ... - Despacho
# Singular No N/AAAA". O despacho inteiro so sai quando o Plenario o referenda.
DESPACHO = re.compile(r"([A-Za-zÀ-ú][A-Za-zÀ-ú ]{2,60}):\s*PROCESSO\s+N[ºo°]\s*(\d{5}-\d{8}/\d{4}-\d{2})(?:-e)?\s*[-–]\s*"
                      r"Despacho Singular\s+N[ºo°]\s*(\d+/\d{4})")
PAUTA = re.compile(r"\d+\)\s*((?:\d{5}-)?\d{3,8}/\d{4}(?:-\d{2})?-e),\s*([^;]+);")
FEEDS = {"MPCDF": "https://mpc.tc.df.gov.br/feed/",
         "TCDF, notícias": "https://www2.tc.df.gov.br/category/noticias/feed/"}
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
         "Setembro", "Outubro", "Novembro", "Dezembro"]
CONTENT = "{http://purl.org/rss/1.0/modules/content/}encoded"

# o numero novo (00600-00010449/2026-55) e o antigo (29590/2013): sem o antigo, o bloco de uma
# decisao engolia a seguinte (piloto de 10/10/2026: a Representacao 14/2026, da SECTI, pegou a
# SES/DF da auditoria que vinha depois)
PROCESSO = re.compile(r"PROCESSO\s+N[ºo°]\s*(\d{5}-\d{8}/\d{4}-\d{2}|\d{1,6}/\d{4})(?:-e)?")
# o cabecalho do relator na ata tambem fecha o bloco
FIM_DE_BLOCO = re.compile(r"\s(?:RELATADOS?(?:\(S\))?\s+PEL[OA]|JULGAMENTO\s+RELATADO)", re.I)
DECISAO = re.compile(r"DECIS[ÃA]O\s+N[ºo°]\s*(\d+/\d{4})\s*[-–]\s*O\s+Tribunal")
# ato de pessoal (aposentadoria, pensao, admissao): nao interessa e traz o nome de terceiros
PESSOAL = re.compile(r"\b(aposentadorias?|pens[ãa]o|pens[õo]es|admiss[ãa]o de pessoal|transfer[êe]ncia para a "
                     r"reserva|an[áa]lise de concess[ãa]o)\b|^reforma\b|reforma \(militar\)", re.I)


def ato_de_pessoal(assunto: str) -> bool:
    """o ato de pessoal se diz logo no comeco do assunto ("Aposentadoria de...", "Duas concessoes
    de aposentadoria de...")"""
    return bool(PESSOAL.search(assunto[:60]))
SES = re.compile(r"Secretaria de Estado de Sa[úu]de do Distrito Federal|\bSES[/-]DF\b", re.I)
SAUDE = re.compile(r"Secretaria de Estado de Sa[úu]de|\bSES[/-]DF\b|\bIGESDF\b|Instituto de Gest[ãa]o "
                   r"Estrat[ée]gica de Sa[úu]de|Fundo de Sa[úu]de do Distrito Federal|\bFSDF\b", re.I)
INSTRUMENTO = [(r"conv[êe]nio", "convênio"), (r"termos? de fomento", "termo de fomento"),
               (r"termos? de colabora[çc][ãa]o", "termo de colaboração"), (r"emendas? parlamentar", "emenda"),
               (r"\bparcerias?\b", "parceria"), (r"\bOCI\b|ofertas? de cuidados integrados", "OCI"),
               (r"sem fins lucrativos|organiza[çc][ãa]o da sociedade civil", "entidade sem fins lucrativos"),
               (r"participa[çc][ãa]o complementar", "participação complementar"),
               (r"credenciamento", "credenciamento")]


# --- o que o projeto vigia ---------------------------------------------------------------

# siglas que aparecem entre parenteses nos titulos e nao sao entidade: diarios, orgaos, sistemas
NAO_ENTIDADE = {"DODF", "DOU", "DOE", "TCDF", "MPCDF", "MPC", "SES", "SEI", "OCI", "SUS", "SIGTAP", "FNS",
                "SUCONV", "ARINS", "CNES", "APAC", "PMAE", "MROSC"}


def vigiados(acervo: Path = ACERVO, proponentes: Path = PROPONENTES):
    """as siglas das entidades nas pecas de controle (CT-) e nos planos aprovados (pt_ses_),
    os proponentes, os numeros de convenio e termo citados nesses registros e os processos do
    TCDF das pecas de controle (a pauta e o registro de despacho so dizem o numero)"""
    nomes, numeros = set(), set()
    if acervo.exists():
        with open(acervo, encoding="utf-8", newline="") as f:
            for l in csv.DictReader(f):
                if not l.get("id", "").startswith(("CT-", "pt_ses")):
                    continue
                t = l.get("titulo", "")
                nomes |= set(re.findall(r"\(([A-Z][A-Z0-9]{2,7})[,)]", t)) - NAO_ENTIDADE
                numeros |= set(re.findall(r"\b(\d{6}/20\d\d)\b", t))
                numeros |= set(re.findall(r"\b(\d{5}-\d{8}/\d{4}-\d{2})\b", t + " " + l.get("processo_sei", "")))
    if proponentes.exists():
        nomes |= {p.name.upper() for p in proponentes.iterdir() if p.is_dir()}
    return {"nomes": nomes, "numeros": numeros}


def classificar(texto: str, vig: dict):
    """('PROJETO'|'SAUDE'|None, [motivos])"""
    motivos = []
    nomes = sorted(n for n in vig["nomes"] if re.search(rf"\b{re.escape(n)}\b", texto))
    nums = sorted(n for n in vig["numeros"] if n in texto)
    if nomes:
        motivos.append(f"entidade do acervo: {', '.join(nomes)}")
    if nums:
        motivos.append(f"instrumento do acervo: {', '.join(nums)}")
    inst = [rot for pad, rot in INSTRUMENTO if re.search(pad, texto, re.I)]
    if SES.search(texto) and inst:
        motivos.append(f"SES-DF e {', '.join(inst)}")
    if motivos:
        return "PROJETO", motivos
    if SAUDE.search(texto):
        return "SAUDE", ["saúde do DF"]
    return None, []


# --- rede ----------------------------------------------------------------------------------

def pegar(url: str, params: dict | None = None, tentativas=4) -> bytes:
    """o corpo da resposta, pelo curl (o mesmo caminho do ler_dou.py)"""
    cmd = ["curl", "-sL", "--max-time", "120", "-A", "Mozilla/5.0"]
    if params:
        cmd += ["-G"] + [x for k, v in params.items() for x in ("--data-urlencode", f"{k}={v}")]
    for n in range(tentativas):
        r = subprocess.run(cmd + [url], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
        time.sleep(5 * (n + 1))
    raise RuntimeError(f"nao consegui ler {url} {params or ''}")


# --- TCDF no DODF --------------------------------------------------------------------------

def pasta_do_dia(d: date) -> str:
    return f"{d.year}/{d.month:02d}_{MESES[d.month - 1]}/{d:%d %m %Y}"


def arquivos_da_listagem(pagina: str):
    """[(pasta, arquivo)] dos PDFs de um dia, da pagina /dodf/jornal/pastas"""
    out = []
    for href in re.findall(r'href="([^"]*visualizar-pdf\?[^"]*)"', pagina):
        h = html.unescape(href)
        m = re.search(r"pasta=(.*?)&arquivo=(.*)$", h)
        if m:
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def arquivos_do_dia(d: date, get=pegar):
    """os PDFs do dia (integra e edicoes extras); [] em dia sem DODF"""
    pagina = get(f"{DODF}/pastas", {"pasta": pasta_do_dia(d)}).decode("utf-8", "replace")
    if "DODF - Sistema de busca" not in pagina:
        raise RuntimeError(f"a listagem do DODF de {d:%d/%m/%Y} nao veio")
    return arquivos_da_listagem(pagina)


def link_do_pdf(pasta: str, arquivo: str) -> str:
    return f"{DODF}/visualizar-pdf?{urlencode({'pasta': pasta, 'arquivo': arquivo})}"


def texto_do_pdf(pasta: str, arquivo: str, bruto: Path | None = None, get=pegar) -> str:
    """o texto do PDF pelo pdftotext; guardado em <bruto>/dodf/<arquivo>.txt"""
    arq = bruto / "dodf" / (arquivo + ".txt") if bruto else None
    if arq and arq.exists():
        return arq.read_text(encoding="utf-8")
    pdf = get(f"{DODF}/visualizar-pdf", {"pasta": pasta, "arquivo": arquivo})
    if not pdf.startswith(b"%PDF"):
        raise RuntimeError(f"{arquivo}: o DODF nao devolveu um PDF")
    r = subprocess.run(["pdftotext", "-", "-"], input=pdf, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"{arquivo}: o pdftotext falhou (o poppler esta instalado?)")
    txt = r.stdout.decode("utf-8", "replace")
    if arq:
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(txt, encoding="utf-8")
    return txt


def decisoes(texto: str):
    """os blocos 'PROCESSO No ... DECISAO No N/AAAA - O Tribunal ...' das atas do TCDF"""
    t = re.sub(r"(?<=[a-zà-ú])-\n(?=[a-zà-ú])", "", texto)      # palavra partida no fim da linha
    t = re.sub(r"\s+", " ", t)
    ms = list(PROCESSO.finditer(t))
    out = []
    for i, m in enumerate(ms):
        fim = ms[i + 1].start() if i + 1 < len(ms) else min(len(t), m.end() + 6000)
        bloco = t[m.start():fim][:8000]
        mf = FIM_DE_BLOCO.search(bloco, 20)
        if mf:
            bloco = bloco[:mf.start()]
        md = DECISAO.search(bloco)
        if md:
            assunto = bloco[m.end() - m.start():md.start()].strip(" -–.")
            out.append({"processo": m.group(1), "decisao": md.group(1), "assunto": assunto[:400],
                        "texto": bloco})
    return out


# --- TCDF no DOE-TCDF ------------------------------------------------------------------------

def diarios_doe(de: date, ate: date, get=pegar):
    """os diarios publicados de 'de' a 'ate': [{id, tipo, numero, ano, dataPublicacao}]"""
    out, pagina = [], 1
    while True:
        d = json.loads(get(DOE_API, {"situacao": "P", "dataPublicacao[after]": f"{de}T00:00:00",
                                     "dataPublicacao[before]": f"{ate}T23:59:59", "itemsPerPage": "100",
                                     "page": str(pagina)}))
        ms = d.get("member", [])
        out += ms
        if not ms or len(out) >= d.get("totalItems", 0):
            return out
        pagina += 1


def conteudo_doe(diario: dict, bruto: Path | None = None, get=pegar):
    """o JSON de um diario; guardado em <bruto>/doe/<tipo>_<ano>_<numero>.json"""
    arq = bruto / "doe" / f"{diario['tipo']}_{diario['ano']}_{diario['numero']}.json" if bruto else None
    if arq and arq.exists():
        return json.loads(arq.read_text(encoding="utf-8"))
    corpo = get(f"{DOE_API}/{diario['id']}/json")
    j = json.loads(corpo)
    if arq:
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_bytes(corpo)
    return j


def publicacoes(secoes, caminho=""):
    """(secao, titulo, texto sem tags) de cada publicacao, descendo pelas secoes"""
    if isinstance(secoes, dict) and "descricao" not in secoes:
        secoes = list(secoes.values())
    if isinstance(secoes, list):
        for s in secoes:
            yield from publicacoes(s, caminho)
        return
    if not isinstance(secoes, dict):
        return
    desc = secoes.get("descricao") or caminho
    for p in secoes.get("publicacoes") or []:
        yield desc, p.get("titulo") or "", sem_tags(p.get("texto"))
    yield from publicacoes(secoes.get("secoes") or [], desc)


def unidades_doe(j: dict):
    """as pecas de um diario: (secao, peca, assunto, texto). A ata se divide por decisao; a
    pauta, por processo; o resto vai inteiro"""
    raiz = (j.get("member") or [{}])[0].get("secoes") or []
    for secao, titulo, texto in publicacoes(raiz):
        if not SECAO_DOE.search(secao):
            continue
        if re.search(r"Atas", secao):
            for b in decisoes(texto):
                yield secao, f"Decisão {b['decisao']} (processo {b['processo']})", b["assunto"], b["texto"]
            for m in DESPACHO.finditer(texto):
                yield (secao, f"Despacho singular {m.group(3)} (processo {m.group(2)})",
                       f"{m.group(1).strip()}: registro do despacho na ata", m.group(0))
        elif re.search(r"Pauta", secao):
            for m in PAUTA.finditer(texto):
                yield secao, f"Pauta: processo {m.group(1)}", m.group(2).strip(), m.group(2)
        elif re.search(r"Ac[óo]rd[ãa]os", secao):
            ms = list(ACORDAO.finditer(texto))
            for i, m in enumerate(ms):
                bloco = texto[m.start():ms[i + 1].start() if i + 1 < len(ms) else len(texto)]
                yield secao, f"Acórdão {m.group(1)}", bloco[m.end() - m.start():][:400].strip(" :-–"), bloco
        else:
            yield secao, titulo.strip(), texto[:400], f"{titulo} {texto}"


# --- feeds ---------------------------------------------------------------------------------

def sem_tags(x: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", x or ""))).strip()


def itens_do_feed(url: str, de: date, ate: date, get=pegar, max_paginas=40):
    """as noticias do feed WordPress de 'de' a 'ate', pagina a pagina, da mais nova para a
    mais antiga, ate passar de 'de'"""
    out = []
    for n in range(1, max_paginas + 1):
        corpo = get(url, {"paged": str(n)} if n > 1 else None)
        if b"<rss" not in corpo[:2000]:
            break                                    # pagina alem do fim
        itens = ET.fromstring(corpo).findall("./channel/item")
        if not itens:
            break
        passou = False
        for it in itens:
            dia = parsedate_to_datetime(it.findtext("pubDate")).date()
            if dia < de:
                passou = True
                break
            if dia > ate:
                continue
            titulo = sem_tags(it.findtext("title"))
            texto = sem_tags((it.findtext("description") or "") + " " + (it.findtext(CONTENT) or ""))
            out.append({"dia": dia, "titulo": titulo, "link": (it.findtext("link") or "").strip(),
                        "texto": f"{titulo} {texto}"})
        if passou:
            break
    return out


# --- leitura e relatorio ---------------------------------------------------------------------

def ler(de: date, ate: date, vig: dict, get=pegar, bruto: Path | None = None, dodf=True, espera=0.3):
    linhas, conta = [], {"dias": 0, "arquivos": 0, "decisoes": 0, "diarios": 0, "noticias": 0}
    if dodf and ate >= DOE_INICIO:
        for diario in diarios_doe(max(de, DOE_INICIO), ate, get):
            conta["diarios"] += 1
            dia = date.fromisoformat(diario["dataPublicacao"][:10])
            link = f"{DOE_SITE}/{diario['tipo']}/{diario['ano']}/{diario['numero']}"
            for secao, peca, assunto, texto in unidades_doe(conteudo_doe(diario, bruto, get)):
                conta["decisoes"] += 1
                if ato_de_pessoal(assunto):
                    continue
                classe, motivos = classificar(texto, vig)
                if classe == "SAUDE" and peca.startswith(("Pauta", "Despacho")):
                    classe = None                 # pauta e registro de despacho so interessam quando tocam o projeto
                if classe:
                    linhas.append({"classe": classe, "dia": dia, "fonte": "TCDF, DOE", "peca": peca, "link": link,
                                   "motivos": motivos, "resumo": assunto,
                                   "edicao": f"{'extra' if diario['tipo'] == 'E' else 'nº'} {diario['numero']}, {secao}"})
    if dodf and de < DOE_INICIO:
        d, fim = de, min(ate, DOE_INICIO - timedelta(days=1))
        while d <= fim:
            for pasta, arquivo in arquivos_do_dia(d, get):
                conta["arquivos"] += 1
                for b in decisoes(texto_do_pdf(pasta, arquivo, bruto, get)):
                    conta["decisoes"] += 1
                    if ato_de_pessoal(b["assunto"]):
                        continue
                    classe, motivos = classificar(b["texto"], vig)
                    if classe:
                        linhas.append({"classe": classe, "dia": d, "fonte": "TCDF, DODF",
                                       "peca": f"Decisão {b['decisao']} (processo {b['processo']})",
                                       "link": link_do_pdf(pasta, arquivo), "motivos": motivos,
                                       "resumo": b["assunto"], "edicao": arquivo})
                if espera:
                    time.sleep(espera)
            conta["dias"] += 1
            d += timedelta(days=1)
    for fonte, url in FEEDS.items():
        for it in itens_do_feed(url, de, ate, get):
            conta["noticias"] += 1
            classe, motivos = classificar(it["texto"], vig)
            if classe:
                linhas.append({"classe": classe, "dia": it["dia"], "fonte": fonte, "peca": it["titulo"],
                               "link": it["link"], "motivos": motivos, "resumo": it["texto"][len(it["titulo"]):][:300],
                               "edicao": ""})
    linhas.sort(key=lambda x: (x["dia"], x["fonte"]))
    return linhas, conta


def relatorio(linhas, conta, de: date, ate: date):
    n = {c: sum(1 for x in linhas if x["classe"] == c) for c in ("PROJETO", "SAUDE")}
    out = [f"# Controle externo — {de:%d/%m/%Y} a {ate:%d/%m/%Y}", "",
           f"Gerado por `ferramentas/ler_controle.py`. TCDF: {conta['diarios']} diários do DOE-TCDF e "
           f"{conta['dias']} dias do DODF ({conta['arquivos']} arquivos), {conta['decisoes']} peças. Notícias do "
           f"MPCDF e do TCDF: {conta['noticias']}. PROJETO: {n['PROJETO']} · SAÚDE: {n['SAUDE']}.", "",
           "**Esta lista é o ponto de partida, não a validação:** cada peça do projeto se lê no texto "
           "(`metodo/coleta/normas.md`).", ""]
    for classe, titulo in (("PROJETO", "Tocam o projeto"), ("SAUDE", "Saúde do DF")):
        sel = [x for x in linhas if x["classe"] == classe]
        out += [f"## {titulo} ({len(sel)})", ""]
        if not sel:
            out += ["Nenhuma peça.", ""]
            continue
        out += ["| dia | fonte | peça | por quê | resumo |", "|---|---|---|---|---|"]
        for x in sel:
            ed = f" ({x['edicao']})" if x["edicao"] else ""
            out.append(f"| {x['dia']:%d/%m/%Y} | {x['fonte']}{ed} | [{x['peca'].replace('|', '/')}]({x['link']}) "
                       f"| {'; '.join(x['motivos'])} | {x['resumo'].replace('|', '/')[:300]} |")
        out.append("")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="o controle externo do DF no periodo, classificado")
    ap.add_argument("--de", required=True, help="AAAA-MM-DD")
    ap.add_argument("--ate", default=date.today().isoformat(), help="AAAA-MM-DD (padrao: hoje)")
    ap.add_argument("--saida", help="grava o relatorio neste .md (padrao: imprime)")
    ap.add_argument("--bruto", help="pasta, fora do repositorio, onde guardar o texto dos DODF")
    ap.add_argument("--sem-dodf", action="store_true", help="so os feeds do MPCDF e do TCDF")
    args = ap.parse_args()
    saida_utf8()
    de, ate = date.fromisoformat(args.de), date.fromisoformat(args.ate)
    linhas, conta = ler(de, ate, vigiados(), bruto=Path(args.bruto) if args.bruto else None,
                        dodf=not args.sem_dodf)
    txt = relatorio(linhas, conta, de, ate)
    if args.saida:
        escrever_texto(Path(args.saida), txt)
        n = {c: sum(1 for x in linhas if x["classe"] == c) for c in ("PROJETO", "SAUDE")}
        print(f"{conta['diarios']} diarios do DOE-TCDF, {conta['dias']} dias do DODF, {conta['decisoes']} pecas do TCDF, "
              f"{conta['noticias']} noticias; "
              f"PROJETO {n['PROJETO']}, SAUDE {n['SAUDE']} -> {args.saida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
