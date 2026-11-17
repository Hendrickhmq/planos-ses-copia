#!/usr/bin/env python3
"""
ler_dou.py - o que o Ministerio da Saude publicou no DOU, dia a dia.

Uso:
    python3 ler_dou.py --de 2026-09-01 --ate 2026-10-09
    python3 ler_dou.py --de 2026-09-01 --ate 2026-10-09 --saida registros/vigia/dou_2026-10-10.md \\
        --bruto <pasta fora do repositorio>

Le a pagina "leitura do jornal" do in.gov.br de cada dia, na Secao 1, na edicao extra e no
suplemento (a SAES 4.795/2026 saiu em edicao extra e uma busca comum a perdia), separa os
atos do Ministerio da Saude e classifica cada um:

  PROJETO    altera ou cita na ementa uma norma do acervo (registros/acervo.csv), ou a
             republica; trata de emenda parlamentar; ou trata do Distrito Federal. A frase
             generica "Estados, Distrito Federal e Municipios" so conta se o texto
             integral do ato, com o anexo, tiver o DF - pede validacao no texto
  NOVIDADE   ato normativo sobre o que pode virar objeto ou mudar regra: OCI, Agora Tem
             Especialistas, Tabela de Procedimentos, incremento, MAC, atencao
             especializada, regulacao
  LOCAL      ato sobre um estabelecimento ou um repasse de outro ente: habilitacao,
             qualificacao, CEBAS, recurso para um municipio. Lista curta, so com o link
  resto      registro de produto da Anvisa, Funasa, pessoal, despacho: so a contagem

Contam so o titulo e a ementa. O preambulo cita as normas de base de todo ato, e a
assinatura "O SECRETARIO DE ATENCAO ESPECIALIZADA A SAUDE" esta em todo ato da SAES: no
piloto de 09/10/2026, ler o resumo inteiro pos 160 CEBAS em novidade. A norma do acervo se
reconhece pela especie e pelo numero do titulo da linha do acervo, nao por um numero solto
("101", da LC 101, casava com a Portaria SGTES/SAPS 101).

Metodo: metodo/coleta/normas.md. A lista e o ponto de partida do agente normas; a
validacao e sempre no texto do ato.
"""
from __future__ import annotations
import argparse, csv, json, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

from comum import REGISTROS, escrever_texto, saida_utf8, sem_acento
from extrair_html import Leitor, decodificar, recorte_dou

URL = "https://www.in.gov.br/leiturajornal?data={dia}&secao={secao}"
SECOES = ("do1", "do1e", "do1a")          # Secao 1, edicao extra, suplemento
LINK = "https://www.in.gov.br/web/dou/-/{url}"
ACERVO = REGISTROS / "acervo.csv"

FORA = re.compile(r"Agência Nacional de Vigilância Sanitária", re.I)
# da Anvisa interessa a norma de servico (RDC e IN), nao o registro de produto (RE)
ANVISA_QUE_IMPORTA = re.compile(r"^(RESOLUÇÃO.RDC|RESOLUÇÃO DA DIRETORIA COLEGIADA|INSTRUÇÃO NORMATIVA)", re.I)
FUNASA = re.compile(r"Fundação Nacional de Saúde", re.I)     # saneamento, nao servico de saude
TIPOS_QUE_IMPORTAM = re.compile(r"portaria|resolu[çc][ãa]o|instru[çc][ãa]o normativa|nota t[ée]cnica", re.I)

NOVIDADE = [
    (r"oferta[s]? de cuidados? integrad|\bOCI\b", "OCI"),
    (r"agora tem especialistas|mais acesso a especialistas|\bPMAE\b", "Agora Tem Especialistas"),
    (r"tabela de procedimentos|\bSIGTAP\b|inclui procedimento|altera(m)? (os )?(atributos|valores)", "Tabela do SUS"),
    # a GM 12.116/2026 (a Tabela SUS deixa de ser teto) so fala em "tabela diferenciada na
    # remuneracao" e em Portaria de Consolidacao: sem estes dois temas, ficava no resto
    (r"remunera[çc][ãa]o|complementa[çc][ãa]o financeira|tabela diferenciada", "remuneração"),
    (r"Altera[^.;]{0,60}?Portaria de Consolida[çc][ãa]o", "consolidação"),
    (r"incremento", "incremento"),
    (r"incentivo financeiro|Bloco de Manuten[çc][ãa]o", "financiamento"),
    (r"m[ée]dia e alta complexidade|\bMAC\b", "MAC"),
    (r"aten[çc][ãa]o especializada", "atenção especializada"),
    (r"regula[çc][ãa]o", "regulação"),
    (r"emenda[s]? parlamentar|emendas individuais|emendas de bancada", "emenda"),
]
# ato sobre um estabelecimento ou um repasse, nao uma regra
ATO_LOCAL = re.compile(r"^(Habilita|Desabilita|Renova|Qualifica|Desqualifica|Credencia|Descredencia|"
                       r"Concede|Mant[ée]m|Suspende|Prorroga|Reabilita|Altera a habilita|Defere|Indefere|Homologa|Disponibiliza|"
                       r"Autoriza (?:o|a|os|as) (?:Estados?|Munic[íi]pios?|Distrito|repasses?)|"
                       r"Estabelece (?:o |os )?recursos?|Destina recursos?)", re.I)

DF = re.compile(r"Distrito Federal|\bSES[-/]DF\b|\bFSDF\b", re.I)
# "Estados, Distrito Federal e Municipios", "o Estado, Municipio ou Distrito Federal"
DF_GENERICO = re.compile(r"(?:Estados?|Munic[íi]pios?)[^.;]{0,40}?Distrito Federal"
                         r"|Distrito Federal[^.;]{0,12}?\b(?:e|ou)\b[^.;]{0,12}?Munic[íi]pios?", re.I)
# no anexo, o DF aparece como UF, pelo Fundo ou pela cidade
DF_NO_ANEXO = re.compile(r"Distrito Federal|\bFSDF\b|\bSES[-/]DF\b|\bDF\b|Bras[íi]lia", re.I)

ESPECIE = (r"Portaria de Consolida[çc][ãa]o|Portaria(?: Conjunta)?|Resolu[çc][ãa]o(?:-RDC)?|RDC|Decreto|"
           r"Lei Complementar|Lei|Instru[çc][ãa]o Normativa|IN|Delibera[çc][ãa]o")
NUMERO = r"(\d{1,3}(?:\.\d{3})+|\d{1,5})"
TITULO = re.compile(rf"^({ESPECIE})\b[^,;]{{0,40}}?\bn[ºo°]?\.?\s*{NUMERO}", re.I)
CITA = re.compile(rf"\b({ESPECIE})\b[^,;]{{0,30}}?\bn[ºo°]\.?\s*{NUMERO}", re.I)


def especie(nome: str) -> str:
    n = sem_acento(nome).lower()
    for prefixo, esp in (("portaria de consolidacao", "prc"), ("portaria", "portaria"),
                         ("resolucao", "resolucao"), ("rdc", "resolucao"), ("decreto", "decreto"),
                         ("lei complementar", "lc"), ("lei", "lei"), ("instrucao", "in"), ("in", "in"),
                         ("deliberacao", "deliberacao")):
        if n.startswith(prefixo):
            return esp
    return n


def norma_do_titulo(titulo: str):
    """(especie, numero) de 'Portaria GM/MS nº 12.116, de ...', ou None"""
    m = TITULO.match(titulo.strip())
    return (especie(m.group(1)), str(int(m.group(2).replace(".", "")))) if m else None


def normas_do_acervo(caminho: Path = ACERVO):
    """(especie, numero) de cada norma do acervo, pelo titulo da linha. Pega tambem a norma
    sem arquivo, como a PRC GM/MS 1/2017"""
    if not caminho.exists():
        return set()
    with open(caminho, encoding="utf-8", newline="") as f:
        return {n for l in csv.DictReader(f) if l.get("tipo") == "norma"
                for n in [norma_do_titulo(l.get("titulo", ""))] if n}


def baixar(dia: date, secao: str, tentativas=5):
    """os atos do dia na secao, ou [] se a edicao nao existe.

    Pelo curl: o in.gov.br responde 403 ao urllib do Python e ao navegador embutido,
    e aceita o curl (o mesmo caminho que baixa as portarias). A rede de entrega dele
    (Azion) as vezes devolve uma pagina de erro com HTTP 200 e sem o bloco de dados: isso
    nao e dia sem edicao, que traz o bloco com a lista vazia. Tenta de novo e, se o bloco
    nao vier, para com erro em vez de seguir com o dia vazio."""
    url = URL.format(dia=dia.strftime("%d-%m-%Y"), secao=secao)
    for n in range(tentativas):
        r = subprocess.run(["curl", "-s", "--max-time", "60", "-A", "Mozilla/5.0", url],
                           capture_output=True)
        if r.returncode == 0 and r.stdout:
            atos = atos_da_pagina(r.stdout.decode("utf-8", "replace"))
            if atos is not None:
                return atos
        time.sleep(5 * (n + 1))
    raise RuntimeError(f"nao consegui ler {url}: {tentativas} tentativas sem o bloco de dados")


def com_bruto(pasta: Path, baixador=baixar, hoje=None):
    """guarda a lista de cada dia em <pasta>/<AAAA-MM-DD>_<secao>.json e le dali na vez
    seguinte: reclassificar o periodo, ou procurar falso negativo, nao baixa tudo de novo.
    O dia de hoje nao se guarda, porque a edicao extra sai ao longo do dia."""
    pasta.mkdir(parents=True, exist_ok=True)
    hoje = hoje or date.today()

    def ler_ou_baixar(dia: date, secao: str):
        arq = pasta / f"{dia.isoformat()}_{secao}.json"
        if arq.exists():
            return json.loads(arq.read_text(encoding="utf-8"))
        atos = baixador(dia, secao)
        if dia < hoje:
            arq.write_text(json.dumps(atos, ensure_ascii=False), encoding="utf-8")
        return atos
    return ler_ou_baixar


def texto_integral(ato: dict, pasta: Path | None = None) -> str:
    """o ato inteiro, com as tabelas do anexo: o resumo da pagina do dia tem uns 300
    caracteres e esconde o anexo. '' se a pagina nao veio."""
    url_titulo = ato.get("urlTitle", "")
    arq = pasta / f"ato_{re.sub(r'[^0-9A-Za-z-]', '_', url_titulo)[:150]}.txt" if pasta else None
    if arq and arq.exists():
        return arq.read_text(encoding="utf-8")
    trecho = None
    for n in range(3):                       # a pagina de erro da Azion vem sem o bloco do ato
        r = subprocess.run(["curl", "-s", "--max-time", "60", "-A", "Mozilla/5.0",
                            LINK.format(url=url_titulo)], capture_output=True)
        if r.returncode == 0 and r.stdout:
            trecho, _ = recorte_dou(decodificar(r.stdout))
            if trecho:
                break
        time.sleep(5 * (n + 1))
    if not trecho:
        return ""
    leitor = Leitor()
    leitor.feed(trecho)
    txt = leitor.texto() + "\n".join(" | ".join(linha) for tabela in leitor.tabelas for linha in tabela)
    if arq:
        arq.write_text(txt, encoding="utf-8")
    return txt


def atos_da_pagina(pagina: str):
    """a lista de atos; [] se a edicao nao existe; None se a pagina nao e a do jornal"""
    m = re.search(r'<script id="params" type="application/json">\s*(\{.*?\})\s*</script>', pagina, re.S)
    return json.loads(m.group(1)).get("jsonArray", []) if m else None


def _corpo(ato: dict) -> str:
    """o resumo do ato sem o titulo repetido no comeco"""
    c = re.sub(r"\s+", " ", ato.get("content", "")).strip()
    t = ato.get("title", "")
    if c.lower().startswith(t.lower()[:30]):
        c = c[len(t):].strip()
    return c


def republicacao(ato: dict) -> bool:
    return "(*)" in ato.get("title", "") or bool(re.match(r"\W*(?:re)?publicad[ao]", _corpo(ato), re.I))


def ementa(ato: dict) -> str:
    """o resumo ate o preambulo ('O MINISTRO...', 'A SECRETARIA...'), sem a nota de republicacao"""
    c = re.sub(r"^\(\s*\*\s*\)\s*", "", _corpo(ato))
    c = re.sub(r"^\((?:re)?publicad[ao][^)]*\)\s*", "", c, flags=re.I)
    m = re.match(r"(.+?)(?:\s(?:O|A) (?:MINISTR[OA]|SECRETÁRI[OA]|SUBSECRETÁRI[OA]|DIRETORA?|DIRETORIA|"
                 r"PRESIDENTE|PLENÁRIO|COORDENADORA?)\b|$)", c)
    return (m.group(1) if m else c)[:400]


def trata_do_df(texto: str) -> bool:
    return bool(DF.search(DF_GENERICO.sub(" ", texto)))


def df_no_texto(texto: str) -> bool:
    t = DF_GENERICO.sub(" ", texto)
    t = re.sub(r"Bras[íi]lia\s*[,/-]\s*\d", " ", t)          # local e data da assinatura
    return bool(DF_NO_ANEXO.search(t))


def classificar(ato: dict, acervo: set, leitor=None):
    """('PROJETO'|'NOVIDADE'|'LOCAL'|None, [motivos]). leitor(ato) devolve o texto
    integral; sem ele, a frase generica do DF nao conta."""
    orgao = ato.get("hierarchyStr", "")
    titulo = ato.get("title", "")
    if not orgao.startswith("Ministério da Saúde") or FUNASA.search(orgao):
        return None, []
    if FORA.search(orgao) and not ANVISA_QUE_IMPORTA.search(titulo):
        return None, []
    if not TIPOS_QUE_IMPORTAM.search(ato.get("artType", "") + " " + titulo):
        return None, []
    em = ementa(ato)
    texto = f"{titulo} {em}"
    propria = norma_do_titulo(titulo)
    republica = republicacao(ato)
    temas = [rot for pad, rot in NOVIDADE if re.search(pad, texto, re.I)]

    motivos = []
    citadas = {(especie(m.group(1)), str(int(m.group(2).replace(".", "")))) for m in CITA.finditer(texto)}
    do_acervo = sorted(f"{e} {n}" for e, n in citadas - {propria} if (e, n) in acervo)
    if do_acervo:
        motivos.append(f"cita na ementa norma do acervo: {', '.join(do_acervo)}")
    if republica and propria in acervo:
        motivos.append("republica norma do acervo")
    if trata_do_df(texto):
        motivos.append("Distrito Federal")
    elif DF_GENERICO.search(texto) and leitor is not None:
        integral = leitor(ato)
        if not integral:
            motivos.append("Distrito Federal genérico: texto integral não lido")
        elif df_no_texto(integral):
            motivos.append("Distrito Federal no texto integral")
    if "emenda" in temas:
        motivos.append("emenda")
    if motivos:
        return "PROJETO", motivos + [t for t in temas if t != "emenda"]
    if ATO_LOCAL.match(em):
        return "LOCAL", temas
    if temas:
        return "NOVIDADE", temas + (["republicação"] if republica else [])
    if republica and re.search(r"Gabinete do Ministro|Atenção Especializada", orgao):
        return "NOVIDADE", ["republicação: ler o texto"]
    return None, []


def ler(de: date, ate: date, acervo: set, espera=0.5, baixador=baixar, leitor=None, paralelo=2):
    """baixa os dias em paralelo e classifica na ordem do calendario"""
    pares = [(de + timedelta(days=i), s) for i in range((ate - de).days + 1) for s in SECOES]

    def pagina(par):
        atos = baixador(*par)
        if espera:
            time.sleep(espera)
        return atos
    with ThreadPoolExecutor(max_workers=max(1, paralelo)) as ex:
        paginas = list(ex.map(pagina, pares))

    linhas, contagem = [], {"PROJETO": 0, "NOVIDADE": 0, "LOCAL": 0, "resto": 0}
    for (d, secao), atos in zip(pares, paginas):
        for ato in atos:
            if not ato.get("hierarchyStr", "").startswith("Ministério da Saúde"):
                continue
            classe, motivos = classificar(ato, acervo, leitor)
            if classe is None:
                contagem["resto"] += 1
                continue
            contagem[classe] += 1
            linhas.append({"classe": classe, "dia": d.isoformat(), "secao": secao,
                           "titulo": ato.get("title", ""), "orgao": ato.get("hierarchyStr", ""),
                           "ementa": ementa(ato), "motivos": motivos,
                           "link": LINK.format(url=ato.get("urlTitle", ""))})
    return linhas, contagem, (ate - de).days + 1


def relatorio(linhas, contagem, de, ate):
    out = [f"# DOU — atos do Ministério da Saúde, {de.strftime('%d/%m/%Y')} a {ate.strftime('%d/%m/%Y')}",
           "",
           f"Gerado por `ferramentas/ler_dou.py` (Seção 1, edição extra e suplemento; classificado pelo "
           f"título e pela ementa). PROJETO: {contagem['PROJETO']} · NOVIDADE: {contagem['NOVIDADE']} · "
           f"LOCAL: {contagem['LOCAL']} · resto do Ministério, fora da lista: {contagem['resto']}.",
           "",
           "**Esta lista é o ponto de partida, não a validação:** cada ato que importa se lê no texto "
           "(`metodo/coleta/normas.md`).", ""]
    for classe, titulo in (("PROJETO", "Tocam o projeto"), ("NOVIDADE", "Novidades")):
        sel = [x for x in linhas if x["classe"] == classe]
        out += [f"## {titulo} ({len(sel)})", ""]
        if not sel:
            out += ["Nenhum ato.", ""]
            continue
        out += ["| dia | ato | órgão | por quê | ementa |", "|---|---|---|---|---|"]
        for x in sel:
            org = x["orgao"].replace("Ministério da Saúde/", "")
            out.append(f"| {x['dia']}{' (extra)' if x['secao'] != 'do1' else ''} | [{x['titulo']}]({x['link']}) "
                       f"| {org} | {'; '.join(x['motivos'])} | {x['ementa'].replace('|', '/')} |")
        out.append("")
    loc = [x for x in linhas if x["classe"] == "LOCAL"]
    out += [f"## Estabelecimentos e repasses de outros entes ({len(loc)})", ""]
    out += [f"- {x['dia']} [{x['titulo']}]({x['link']}): {x['ementa'][:140]}" for x in loc] or ["Nenhum ato."]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="atos do Ministerio da Saude no DOU, classificados")
    ap.add_argument("--de", required=True, help="AAAA-MM-DD")
    ap.add_argument("--ate", default=date.today().isoformat(), help="AAAA-MM-DD (padrao: hoje)")
    ap.add_argument("--saida", help="grava o relatorio neste .md (padrao: imprime)")
    ap.add_argument("--bruto", help="pasta, fora do repositorio, onde guardar e reler o que foi baixado")
    ap.add_argument("--sem-texto", action="store_true",
                    help="nao abre o texto integral dos atos com o DF generico")
    ap.add_argument("--paralelo", type=int, default=2, help="paginas baixadas ao mesmo tempo (padrao 2)")
    args = ap.parse_args()
    saida_utf8()
    de, ate = date.fromisoformat(args.de), date.fromisoformat(args.ate)
    bruto = Path(args.bruto) if args.bruto else None
    baixador = com_bruto(bruto) if bruto else baixar
    leitor = None if args.sem_texto else (lambda ato: texto_integral(ato, bruto))
    linhas, contagem, dias = ler(de, ate, normas_do_acervo(), baixador=baixador, leitor=leitor,
                                 paralelo=args.paralelo)
    txt = relatorio(linhas, contagem, de, ate)
    if args.saida:
        escrever_texto(Path(args.saida), txt)
        print(f"{dias} dias lidos; PROJETO {contagem['PROJETO']}, NOVIDADE {contagem['NOVIDADE']}, "
              f"LOCAL {contagem['LOCAL']}, resto {contagem['resto']} -> {args.saida}")
    else:
        print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
