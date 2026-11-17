#!/usr/bin/env python3
"""
extrair_html.py - extracao de normas publicadas em HTML (DOU e Planalto).

Uso:
    python extrair_html.py normas/ extraidos_normas/
    python extrair_html.py normas/ extraidos_normas/ --doc "LC 210-2024 emendas parlamentares"

POR QUE ESTE SCRIPT EXISTE

Parte das normas nao tem PDF acessivel: a portaria do Ministerio da Saude so se
baixa pela pagina do ato no Diario Oficial (in.gov.br) quando a BVS esta fora do
ar e o gov.br recusa acesso automatico, e a lei federal vem do Planalto, que
publica em HTML. O extrair_planos.py le PDF; este le a pagina.

O que a pagina tem e o PDF nao tem, e o que se faz com isso:

- DOU: a pagina traz o portal inteiro em volta do ato. Recorta-se o bloco
  `texto-dou`, que e o ato, e o cabecalho de publicacao (data, edicao, secao,
  pagina, orgao) que o precede.
- Planalto: o texto revogado continua na pagina, riscado (<strike>, <s>, <del>).
  Ele e mantido e marcado com ~~ ~~, porque a redacao anterior as vezes explica
  a vigente - mas quem cita tem de ver que esta riscada.
- Tabela vira CSV em tabelas/, e o lugar dela no texto recebe o marcador
  [[tabela: tNN]], como no extrator de PDF.

SAIDA - a mesma convencao do extrair_planos.py:

    <destino>/<nome>/texto.md
    <destino>/<nome>/tabelas/tNN.csv
    <destino>/<nome>/meta.yaml

So biblioteca padrao.
"""

import argparse
import csv
import io
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

from comum import escrever_texto, nfc, saida_utf8, sha256_arquivo, yaml_simples

BLOCO = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "blockquote",
         "section", "article", "ul", "ol", "center"}
RISCADO = {"strike", "s", "del"}
IGNORAR = {"script", "style", "noscript", "head", "nav", "footer", "form", "button", "select"}


def decodificar(dados: bytes) -> str:
    """UTF-8 quando a pagina declara ou quando decodifica sem erro; senao, cp1252 (Planalto)."""
    cab = dados[:4000].decode("ascii", errors="ignore").lower()
    m = re.search(r'charset=["\']?([a-z0-9_-]+)', cab)
    for cod in ([m.group(1)] if m else []) + ["utf-8", "cp1252"]:
        try:
            return dados.decode(cod)
        except (LookupError, UnicodeDecodeError):
            continue
    return dados.decode("utf-8", errors="replace")


class Leitor(HTMLParser):
    """texto corrido com quebras de bloco; tabelas separadas; riscado marcado"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self.tabelas = []
        self.ignorando = 0
        self.riscando = 0
        self.tabela = None       # linhas da tabela aberta
        self.linha = None
        self.celula = None
        self.profundidade_tabela = 0

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self.ignorando += 1
            return
        if self.ignorando:
            return
        if tag == "table":
            self.profundidade_tabela += 1
            if self.profundidade_tabela == 1:
                self.tabela = []
            return
        if self.tabela is not None:
            if tag == "tr":
                self.linha = []
            elif tag in ("td", "th"):
                self.celula = []
            elif tag == "br" and self.celula is not None:
                self.celula.append(" ")
            return
        if tag in RISCADO:
            self.riscando += 1
            self.partes.append("~~")
        elif tag in BLOCO:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in IGNORAR:
            self.ignorando = max(0, self.ignorando - 1)
            return
        if self.ignorando:
            return
        if tag == "table" and self.profundidade_tabela:
            self.profundidade_tabela -= 1
            if self.profundidade_tabela == 0 and self.tabela is not None:
                linhas = [l for l in self.tabela if any(c.strip() for c in l)]
                if linhas:
                    self.tabelas.append(linhas)
                    self.partes.append(f"\n\n[[tabela: t{len(self.tabelas):02d}]]\n\n")
                self.tabela = None
            return
        if self.tabela is not None:
            if tag in ("td", "th") and self.celula is not None and self.linha is not None:
                self.linha.append(re.sub(r"\s+", " ", "".join(self.celula)).strip())
                self.celula = None
            elif tag == "tr" and self.linha is not None:
                self.tabela.append(self.linha)
                self.linha = None
            return
        if tag in RISCADO and self.riscando:
            self.riscando -= 1
            self.partes.append("~~")
        elif tag in BLOCO:
            self.partes.append("\n")

    def handle_data(self, data):
        if self.ignorando:
            return
        # a quebra de linha do codigo-fonte nao e quebra do texto: o Planalto quebra
        # o paragrafo no meio; quem quebra linha e a tag de bloco
        data = re.sub(r"\s+", " ", data)
        if self.tabela is not None:
            if self.celula is not None:
                self.celula.append(data)
            return
        self.partes.append(data)

    def texto(self):
        t = "".join(self.partes).replace("\xa0", " ")
        t = re.sub(r"~~\s*~~", "", t)
        linhas = [re.sub(r"[ \t]+", " ", l).strip() for l in t.split("\n")]
        saida, vazio = [], 0
        for l in linhas:
            if not l:
                vazio += 1
                if vazio == 1:
                    saida.append("")
                continue
            vazio = 0
            saida.append(l)
        return "\n".join(saida).strip() + "\n"


def recorte_dou(html: str):
    """o bloco do ato e o cabecalho de publicacao; None se a pagina nao for do DOU"""
    i = html.find('class="texto-dou"')
    if i < 0:
        return None, ""
    ini = html.rfind("<div", 0, i)
    # fecha no primeiro </div> que equilibra o <div> de abertura
    nivel, pos = 0, ini
    for m in re.finditer(r"<div\b|</div>", html[ini:]):
        nivel += 1 if m.group(0) != "</div>" else -1
        if nivel == 0:
            pos = ini + m.end()
            break
    cab = ""
    m = re.search(r"Publicado em:.*?(?:Órgão|&Oacute;rg&atilde;o|Orgão):\s*</?[^>]*>?\s*([^<]+)", html, re.S)
    info = re.findall(r'class="(?:publicado-dou-data|edicao-dou-data|secao-dou|secao-dou-data|'
                      r'pagina-dou|pagina-dou-data|orgao-dou-data)"[^>]*>([^<]*)<', html)
    if info:
        cab = " | ".join(x.strip() for x in info if x.strip())
    elif m:
        cab = re.sub(r"\s+", " ", m.group(0))[:300]
    return html[ini:pos], cab


def extrair(caminho: Path, destino: Path):
    dados = caminho.read_bytes()
    html = decodificar(dados)
    trecho, cab = recorte_dou(html)
    origem = "DOU (bloco texto-dou)" if trecho else "página inteira"
    leitor = Leitor()
    leitor.feed(trecho or html)
    texto = leitor.texto()
    nome = nfc(caminho.stem)
    pasta = destino / nome
    (pasta / "tabelas").mkdir(parents=True, exist_ok=True)
    for antiga in (pasta / "tabelas").glob("t*.csv"):
        antiga.unlink()
    for n, linhas in enumerate(leitor.tabelas, 1):
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerows(linhas)
        escrever_texto(pasta / "tabelas" / f"t{n:02d}.csv", buf.getvalue())
    corpo = f"# {nome}\n\nFonte: `{caminho.name}` — {origem}\n"
    if cab:
        corpo += f"\nPublicação: {cab}\n"
    escrever_texto(pasta / "texto.md", corpo + "\n" + texto)
    meta = {
        "id": nome,
        "arquivo": nfc(caminho.name),
        "sha256": sha256_arquivo(caminho),
        "formato": "html",
        "recorte": origem,
        "chars_texto": len(texto),
        "tabelas_total": len(leitor.tabelas),
        "trechos_riscados": texto.count("~~") // 2,
        "ferramenta": "html.parser (biblioteca padrão)",
        "data_extracao": datetime.now().isoformat(timespec="seconds"),
    }
    escrever_texto(pasta / "meta.yaml", yaml_simples(meta))
    return len(texto), len(leitor.tabelas), meta["trechos_riscados"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origem", type=Path)
    ap.add_argument("destino", type=Path)
    ap.add_argument("--doc", action="append", default=[], help="nome do arquivo, sem extensão")
    a = ap.parse_args()
    saida_utf8()
    pedidos = {nfc(d) for d in a.doc}
    arquivos = sorted(p for p in a.origem.glob("*.htm*") if not pedidos or nfc(p.stem) in pedidos)
    if not arquivos:
        print("nenhum HTML encontrado.")
        return 1
    for p in arquivos:
        chars, tabs, risc = extrair(p, a.destino)
        aviso = "  <- pouco texto, conferir" if chars < 1500 else ""
        print(f"  {p.stem}: {chars} caracteres, {tabs} tabela(s), {risc} trecho(s) riscado(s){aviso}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
