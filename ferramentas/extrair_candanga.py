#!/usr/bin/env python3
"""
extrair_candanga.py - a Tabela SUS Candanga do Anexo Unico oficial para CSV e XLSX.

Uso:
    python extrair_candanga.py <pdf> <pasta_destino> [--json arquivo.json]

POR QUE ESTE SCRIPT EXISTE

A Tabela SUS Candanga e o Anexo Unico da Deliberacao CG-SES-DF 46/2026 (art. 15):
codigo, descricao, modalidade e Valor Tabela SUS Candanga. A SES-DF a publicou no SEI
(processo 00060-00238687/2026-88, documento 212117347, assinado em 24/08/2026) como PDF
de 57 paginas, uma tabela HTML impressa. Para precificar, ela precisa ser pesquisavel.

A modalidade e SIA, SIH, OPME ou Medicamento (Deliberacao 46/2026, art. 2). O mesmo
codigo pode vir em mais de uma modalidade (o ultrassom de abdomen total vem no SIA e no
SIH): a chave e codigo + modalidade.

O valor do Anexo e o valor final, ja com o SIGTAP dentro (art. 5): a complementacao
distrital e a diferenca entre ele e o SIGTAP vigente (art. 4, par. 5). Nas OCI (grupo
09), o script compara com registros/fontes/sigtap_grupo09_<competencia>.csv e marca
onde o SIGTAP vigente ja e igual ou maior que o Valor Tabela SUS Candanga.

CONFERENCIA

Cada pagina e lida duas vezes: pela tabela (pdfplumber) e pelo texto corrido, contando
os codigos de 10 digitos no inicio de linha. As duas contagens tem de bater pagina a
pagina, e cada linha tem de ter codigo, modalidade conhecida e valor em reais. O script
para se algo nao bater.

SAIDA

    <destino>/tabela_sus_candanga.csv
    <destino>/tabela_sus_candanga.xlsx
"""
import argparse
import csv
import json
import re
from pathlib import Path

import pdfplumber

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO_09 = RAIZ / "registros" / "fontes" / "sigtap_grupo09_092026.csv"
COMPETENCIA_09 = "09/2026"
MODALIDADES = ("SIA", "SIH", "OPME", "Medicamento")

CAMPOS = [
    ("codigo", "Código"),
    ("codigo_sigtap", "Código SIGTAP"),
    ("procedimento", "Procedimento/Item"),
    ("modalidade", "Modalidade"),
    ("valor", "Valor Tabela SUS Candanga"),
    ("sigtap_vigente", f"SIGTAP {COMPETENCIA_09} (OCI)"),
    ("alerta", "Alerta"),
    ("pagina", "Página"),
]


def numero(s):
    s = s.replace("R$", "").strip().replace(".", "").replace(",", ".")
    return float(s)


def brl(v):
    return f"{v:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def pontuado(c):
    return f"{c[0:2]}.{c[2:4]}.{c[4:6]}.{c[6:9]}-{c[9]}"


def ler_pdf(caminho):
    linhas = []
    with pdfplumber.open(caminho) as pdf:
        for n, pg in enumerate(pdf.pages, 1):
            da_pagina = []
            for t in pg.extract_tables():
                for cod, nome, mod, valor in t:
                    if cod == "Código":
                        continue
                    cod = (cod or "").strip()
                    assert re.fullmatch(r"\d{10}", cod), f"p. {n}: código {cod!r}"
                    mod = (mod or "").strip()
                    assert mod in MODALIDADES, f"p. {n}, {cod}: modalidade {mod!r}"
                    assert re.fullmatch(r"R\$ [\d.]+,\d{2}", (valor or "").strip()), \
                        f"p. {n}, {cod}: valor {valor!r}"
                    da_pagina.append({
                        "codigo": cod,
                        "codigo_sigtap": pontuado(cod),
                        "procedimento": " ".join((nome or "").split()),
                        "modalidade": mod,
                        "valor": numero(valor),
                        "pagina": n,
                    })
            no_texto = len(re.findall(r"(?m)^\s*\d{10}\b", pg.extract_text(layout=True) or ""))
            assert no_texto == len(da_pagina), \
                f"p. {n}: {len(da_pagina)} linhas na tabela e {no_texto} códigos no texto"
            linhas.extend(da_pagina)
    return linhas


def conferir(linhas):
    """O Anexo repete quatro itens no fim (OPME e medicamento, p. 55 e 56), com o mesmo
    valor. Fica a primeira linha; repetido com valor diferente para o script."""
    unicas, vistas = [], {}
    for r in linhas:
        chave = (r["codigo"], r["modalidade"])
        if chave in vistas:
            assert vistas[chave]["valor"] == r["valor"], f"{chave}: dois valores no Anexo"
            continue
        vistas[chave] = r
        unicas.append(r)
    return unicas, len(linhas) - len(unicas)


def comparar_catalogo(linhas):
    cat = {}
    with open(CATALOGO_09, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cat[re.sub(r"\D", "", row["codigo"])] = row
    for r in linhas:
        r["sigtap_vigente"] = None
        r["alerta"] = ""
        c = cat.get(r["codigo"])
        if not c or not c["valor_total_ambulatorial"]:
            continue
        v = numero(c["valor_total_ambulatorial"])
        r["sigtap_vigente"] = v
        if v >= r["valor"]:
            r["alerta"] = (f"SIGTAP {COMPETENCIA_09} (R$ {brl(v)}) igual ou acima do Valor Tabela "
                           f"SUS Candanga (R$ {brl(r['valor'])}): não há complementação distrital")


def gravar_csv(linhas, destino):
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([k for k, _ in CAMPOS])
        for r in linhas:
            w.writerow(["" if r[k] is None else (f"{r[k]:.2f}" if isinstance(r[k], float) else r[k])
                        for k, _ in CAMPOS])


def gravar_xlsx(linhas, destino, pdf_nome):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Tabela"
    fonte = Font(name="Arial", size=9)
    cab = Font(name="Arial", size=9, bold=True, color="FFFFFF")
    fundo_cab = PatternFill("solid", fgColor="1F4E5A")
    alerta = PatternFill("solid", fgColor="F8D7D3")
    fino = Border(bottom=Side(style="thin", color="D0D7DA"))
    ws.append([t for _, t in CAMPOS])
    for c in ws[1]:
        c.font, c.fill = cab, fundo_cab
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for r in linhas:
        ws.append([r[k] for k, _ in CAMPOS])
    for j, (k, _) in enumerate(CAMPOS, 1):
        largura = {"procedimento": 70, "alerta": 50, "codigo": 12, "codigo_sigtap": 15,
                   "modalidade": 13, "pagina": 8}.get(k, 14)
        ws.column_dimensions[get_column_letter(j)].width = largura
        for cell in ws.iter_cols(min_col=j, max_col=j, min_row=2).__next__():
            cell.font = fonte
            cell.border = fino
            if k in ("valor", "sigtap_vigente"):
                cell.number_format = '#,##0.00;-#,##0.00;"-"'
            if k == "valor":
                cell.font = Font(name="Arial", size=9, bold=True)
            if k == "alerta" and cell.value:
                cell.fill = alerta
            if k in ("codigo", "codigo_sigtap"):
                cell.number_format = "@"
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = ws.dimensions

    por_mod = {m: sum(1 for r in linhas if r["modalidade"] == m) for m in MODALIDADES}
    leia = wb.create_sheet("Leia")
    textos = [
        ("Tabela SUS Candanga - Anexo Único", True),
        (f"Fonte: {pdf_nome}, Anexo Único da Deliberação CG-SES-DF 46/2026 (Tabela - SES/SECCIC, "
         "SEI 00060-00238687/2026-88, documento 212117347, assinado em 24/08/2026), 57 páginas, "
         f"{len(linhas)} linhas: " + ", ".join(f"{n} {m}" for m, n in por_mod.items()) + ".", False),
        ("Norma: Deliberação CG-SES-DF 46, de 21/09/2026 (DODF 178, de 24/09/2026); Lei distrital "
         "7.897/2026.", False),
        ("", False),
        ("O preço", True),
        ("A coluna Valor Tabela SUS Candanga é o valor do Anexo, o que a SES-DF paga. Ele já contém o "
         "SIGTAP: a complementação distrital é a diferença entre os dois (Deliberação 46/2026, art. 4º, "
         "§ 5º). O mesmo código pode vir em mais de uma modalidade (SIA e SIH): use a do objeto.", False),
        ("", False),
        ("SIGTAP das OCI", True),
        (f"Nas OCI (grupo 09), a coluna SIGTAP {COMPETENCIA_09} traz o valor do catálogo do repositório "
         f"(registros/fontes/{CATALOGO_09.name}), e a coluna Alerta marca onde ele já é igual ou maior "
         "que o Valor Tabela SUS Candanga. Os outros grupos não foram comparados.", False),
        ("", False),
        ("Conferência da extração", True),
        ("Cada página foi lida pela tabela e pelo texto corrido, e as contagens de códigos batem página "
         "a página. Gerado por ferramentas/extrair_candanga.py.", False),
        ("", False),
        ("Como pesquisar", True),
        ("Na aba Tabela, use as setas do filtro no cabeçalho (por texto, por modalidade) ou Ctrl+F "
         "(Cmd+F no Mac) para procurar código ou nome.", False),
    ]
    leia.column_dimensions["A"].width = 110
    for i, (t, negrito) in enumerate(textos, 1):
        c = leia.cell(row=i, column=1, value=t)
        c.font = Font(name="Arial", size=10, bold=negrito)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.move_sheet("Leia", offset=-1)
    wb.active = 1
    wb.save(destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("destino")
    ap.add_argument("--json")
    a = ap.parse_args()
    linhas, repetidas = conferir(ler_pdf(a.pdf))
    comparar_catalogo(linhas)
    destino = Path(a.destino)
    destino.mkdir(parents=True, exist_ok=True)
    gravar_csv(linhas, destino / "tabela_sus_candanga.csv")
    gravar_xlsx(linhas, destino / "tabela_sus_candanga.xlsx", Path(a.pdf).name)
    if a.json:
        Path(a.json).write_text(json.dumps(linhas, ensure_ascii=False, separators=(",", ":")),
                                encoding="utf-8")
    por_mod = ", ".join(f"{sum(1 for r in linhas if r['modalidade'] == m)} {m}" for m in MODALIDADES)
    print(f"{len(linhas)} linhas ({por_mod}), fora {repetidas} repetidas com o mesmo valor; "
          f"tabela e texto batem em todas as páginas; "
          f"{sum(1 for r in linhas if r['alerta'])} OCI com o SIGTAP igual ou acima")


if __name__ == "__main__":
    main()
