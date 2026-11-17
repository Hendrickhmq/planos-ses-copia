"""Gera .docx e .pdf de cada versão do pré-plano (plano_v*.md), via HTML e LibreOffice.

Uso: python3 gerar_pre_plano.py planos/redacao_NN/                  todos os plano_v*.md da pasta
     python3 gerar_pre_plano.py planos/redacao_NN/plano_v1_geral.md  só este
Precisa de soffice no PATH. Os arquivos saem ao lado do .md.

Do estado.yaml da pasta saem o cabeçalho do documento (`cabecalho_documento`, o nome
do proponente em caixa alta) e o começo do nome dos arquivos (`prefixo_arquivo`,
padrão "pt_simplificado_"). Nasceu no redacao_05 como gerar_docx.py, com os dois fixos
no código; ver metodo/pre_plano/procedimento.md.
Markdown suportado: título (#), seção (##), parágrafo, lista (-), tabela (|), **negrito**.
"""
import glob, html, os, re, subprocess, sys, zipfile

VALOR = re.compile(r"R\$ [\d.,]+")                 # célula só com valor em reais: não quebra
ATTR_VALOR = " width='20%' nowrap"


def inline(s):
    s = s.replace("\\|", "\x00")
    s = html.escape(s).replace("\x00", "|")
    s = re.sub(r"R\$ ", "R$&nbsp;", s)          # valor em reais não quebra linha
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def celulas(linha):
    linha = linha.strip().replace("\\|", "\x00")
    return [c.strip().replace("\x00", "\\|") for c in linha.strip("|").split("|")]


def converter(md):
    out, linhas, i = [], md.splitlines(), 0
    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            i += 1
        elif l.startswith("# "):
            out.append(f"<h1>{inline(l[2:])}</h1>"); i += 1
        elif l.startswith("## "):
            out.append(f"<h2>{inline(l[3:])}</h2>"); i += 1
        elif l.startswith("- "):
            itens = []
            while i < len(linhas) and linhas[i].startswith("- "):
                itens.append(f"<li>{inline(linhas[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(itens) + "</ul>")
        elif l.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith("|"):
                bloco.append(linhas[i]); i += 1
            cab, corpo = celulas(bloco[0]), [celulas(b) for b in bloco[2:]]
            t = ["<table width='100%' border='1' cellspacing='0' cellpadding='5'><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cab) + "</tr></thead><tbody>"]
            for r in corpo:
                tot = r[0].lower().startswith("total")
                t.append("<tr>" + "".join(f"<td{ATTR_VALOR if VALOR.fullmatch(c) else ''}>{'<b>' if tot else ''}{inline(c)}{'</b>' if tot else ''}</td>" for c in r) + "</tr>")
            out.append("".join(t) + "</tbody></table>")
        else:
            out.append(f"<p>{inline(l)}</p>"); i += 1
    return "\n".join(out)


CSS = """
body { font-family: 'Arial'; font-size: 11pt; line-height: 1.35; }
.casa { font-size: 9pt; font-weight: bold; letter-spacing: 1px; color: #1F3864; border-bottom: 1px solid #1F3864; padding-bottom: 4px; }
h1 { font-size: 18pt; color: #1F3864; margin: 18px 0 4px 0; }
h2 { font-size: 13pt; color: #1F3864; margin: 18px 0 6px 0; }
p { margin: 0 0 8px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 12px 0; }
th, td { border: 1px solid #8EA9DB; padding: 4px 6px; font-size: 10pt; vertical-align: top; text-align: left; }
th { background: #D9E2F3; }
"""


def do_estado(pasta, chave_, padrao=None):
    """uma chave de primeiro nível do estado.yaml da pasta"""
    caminho = os.path.join(pasta, "estado.yaml")
    txt = open(caminho, encoding="utf-8").read() if os.path.exists(caminho) else ""
    m = re.search(rf'^{chave_}:\s*"([^"]+)"', txt, re.M)
    return m.group(1) if m else padrao


def gerar(md_path):
    pasta = os.path.dirname(os.path.abspath(md_path))
    cabecalho = do_estado(pasta, "cabecalho_documento")
    if not cabecalho:
        sys.exit(f'sem cabeçalho: declare cabecalho_documento: "..." no estado.yaml de {pasta}')
    prefixo = do_estado(pasta, "prefixo_arquivo", "pt_simplificado_")
    md = open(md_path, encoding="utf-8").read()
    corpo = converter(md)
    doc = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><p class='casa'>{html.escape(cabecalho)}</p>{corpo}</body></html>"
    base = os.path.splitext(os.path.basename(md_path))[0].replace("plano_", prefixo)
    h = os.path.join(pasta, base + ".html")
    open(h, "w", encoding="utf-8").write(doc)
    d = os.path.join(pasta, base + ".docx")
    soffice("docx:MS Word 2007 XML", h, pasta)
    linha_inteira(d)
    soffice("pdf:writer_pdf_Export", d, pasta)          # o PDF sai do .docx já ajustado
    os.remove(h)
    print("gerado:", base + ".docx", base + ".pdf")


def soffice(fmt, origem, pasta):
    subprocess.run(["soffice", "--headless", "--convert-to", fmt, "--outdir", pasta, origem], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def linha_inteira(docx):
    """Linha de tabela não se parte entre páginas (cantSplit em cada w:tr)."""
    tmp = docx + ".tmp"
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            dados = zin.read(item.filename)
            if item.filename == "word/document.xml":
                x = dados.decode("utf-8")
                x = re.sub(r"(<w:tr\b[^>]*>)(?!<w:trPr>)", r"\1<w:trPr></w:trPr>", x)
                x = re.sub(r"<w:trPr>(?!<w:cantSplit/>)", "<w:trPr><w:cantSplit/>", x)
                dados = x.encode("utf-8")
            zout.writestr(item, dados)
    os.replace(tmp, docx)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for alvo in sys.argv[1:]:
        arquivos = sorted(glob.glob(os.path.join(alvo, "plano_v*.md"))) if os.path.isdir(alvo) else [alvo]
        for md in arquivos:
            gerar(md)


if __name__ == "__main__":
    sys.exit(main())
