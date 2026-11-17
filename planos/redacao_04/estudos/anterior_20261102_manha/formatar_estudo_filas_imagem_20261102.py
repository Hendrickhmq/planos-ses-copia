"""Cópia organizada da planilha do estudo das filas de imagem, para ler e mostrar.

Lê o que o estudo_filas_imagem_20261102.py gravou (o .json e o .xlsx, nesta pasta) e escreve
estudo_filas_imagem_20261102_organizada.xlsx. Não refaz conta: só reorganiza e formata.

    python3 planos/redacao_04/estudos/formatar_estudo_filas_imagem_20261102.py
"""
import json
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

AQUI = Path(__file__).resolve().parent
ORIGEM_JSON = AQUI / "estudo_filas_imagem_20261102.json"
ORIGEM_XLSX = AQUI / "estudo_filas_imagem_20261102.xlsx"
DESTINO = AQUI / "estudo_filas_imagem_20261102_organizada.xlsx"

AZUL, AZUL_CLARO, CINZA, CINZA_TEXTO = "1F3864", "D9E2F3", "F2F2F2", "595959"
COR_SITUACAO = {"livre": "E2EFDA", "parcial": "FFF2CC", "fora": "F8CBAD"}
FINO = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINO, right=FINO, top=FINO, bottom=FINO)
INTEIRO, REAL, PCT = '#,##0;-#,##0;"—"', '"R$" #,##0.00;-"R$" #,##0.00;"—"', "0%"

LETRAS, RECOMENDADA = "12345", "1"
SEM_ANGIO = "15"        # prioridade do usuário (02/11/2026): não atender angio coronária
MINIMO_FILA = 30        # o mesmo corte do estudo: fila menor não vira item próprio na carteira
SUFIXO_NOVOS = " — pedidos novos esperados em 8 meses"
TRANSVAGINAL = "02.05.02.018-6"

# a situação de cada pedido no plano 4, com a cor da barra (forte) e da célula (clara)
SITUACOES = {
    "Na carteira 1": ("70AD47", "C6E0B4"),
    "Só em outra carteira": ("FFC000", "FFE699"),
    "Livre, fila pequena": ("5B9BD5", "DDEBF7"),
    "Livre, sem carteira": ("9DC3E6", "DDEBF7"),
    "Fora: tem dono": ("C55A5A", "F8CBAD"),
    "Fora: emergência": ("ED7D31", "FCE4D6"),
    "Fora: outra equipe ou equipamento": ("7F7F7F", "D9D9D9"),
    "Fora do foco agora": ("BFBFBF", "EDEDED"),
}
COR_FILA = {"No plano": "C6E0B4", "No plano, em parte": "E2EFDA",
            **{s: claro for s, (_, claro) in SITUACOES.items() if s != "Na carteira 1"}}


class Aba:
    """Uma aba com título, nota e tabelas, no mesmo estilo."""

    def __init__(self, wb, nome, titulo, nota, larguras):
        self.ws = wb.create_sheet(nome)
        self.ws.sheet_view.showGridLines = False
        self.larguras = larguras
        for i, w in enumerate(larguras, 1):
            self.ws.column_dimensions[get_column_letter(i)].width = w
        self.ws["A1"] = titulo
        self.ws["A1"].font = Font(bold=True, size=15, color=AZUL)
        self.ws.row_dimensions[1].height = 24
        self.linha = 2
        if nota:
            self.nota(nota)
        self.linha += 1

    def nota(self, texto, altura=None):
        ws, n = self.ws, len(self.larguras)
        ws.merge_cells(start_row=self.linha, start_column=1, end_row=self.linha, end_column=n)
        c = ws.cell(self.linha, 1, texto)
        c.font = Font(italic=True, color=CINZA_TEXTO, size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        largura = sum(self.larguras)
        ws.row_dimensions[self.linha].height = altura or max(15, 14 * (len(texto) // int(largura * 1.1) + 1))
        self.linha += 1

    def subtitulo(self, texto):
        self.linha += 1
        c = self.ws.cell(self.linha, 1, texto)
        c.font = Font(bold=True, size=12, color=AZUL)
        self.linha += 1

    def tabela(self, cabecalho, linhas, formatos, total=None, situacao_col=None, filtro=False, congelar=False):
        ws = self.ws
        inicio = self.linha
        for j, h in enumerate(cabecalho, 1):
            c = ws.cell(self.linha, j, h)
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor=AZUL)
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
            c.border = BORDA
        ws.row_dimensions[self.linha].height = 46
        if congelar:
            ws.freeze_panes = ws.cell(self.linha + 1, 1)
        self.linha += 1
        for k, l in enumerate(linhas):
            for j, v in enumerate(l, 1):
                c = ws.cell(self.linha, j, v)
                c.border = BORDA
                fmt = formatos[j - 1]
                if fmt:
                    c.number_format = fmt
                    c.alignment = Alignment(horizontal="right", vertical="top")
                else:
                    c.alignment = Alignment(wrap_text=True, vertical="top")
                if k % 2:
                    c.fill = PatternFill("solid", fgColor=CINZA)
            if situacao_col is not None and l[situacao_col] in COR_SITUACAO:
                ws.cell(self.linha, situacao_col + 1).fill = PatternFill("solid", fgColor=COR_SITUACAO[l[situacao_col]])
                ws.cell(self.linha, situacao_col + 1).font = Font(bold=True)
            self.linha += 1
        if total:
            for j, v in enumerate(total, 1):
                c = ws.cell(self.linha, j, v)
                c.font = Font(bold=True)
                c.fill = PatternFill("solid", fgColor=AZUL_CLARO)
                c.border = BORDA
                if formatos[j - 1]:
                    c.number_format = formatos[j - 1]
            self.linha += 1
        if filtro:
            ws.auto_filter.ref = f"A{inicio}:{get_column_letter(len(cabecalho))}{self.linha - 1}"
        self.linha += 1

    def tabela_excel(self, nome, cabecalho, linhas, formatos, somar=(), barras=(), cores=None, congelar_col=1):
        """Tabela do Excel: filtro e ordem em cada coluna. A linha de cima soma só o que o filtro deixa à vista."""
        ws = self.ws
        topo, cab = self.linha, self.linha + 1
        ini, fim = cab + 1, cab + len(linhas)
        ws.cell(topo, 1, "Total do que está à vista (muda com o filtro)").font = Font(bold=True, color=AZUL)
        for j in somar:
            col = get_column_letter(j + 1)
            c = ws.cell(topo, j + 1, f"=SUBTOTAL(109,{col}{ini}:{col}{fim})")
            c.number_format = formatos[j]
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor=AZUL_CLARO)
        for j, h in enumerate(cabecalho, 1):
            c = ws.cell(cab, j, h)
            c.font = Font(bold=True, color="FFFFFF")
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.row_dimensions[cab].height = 46
        for k, l in enumerate(linhas):
            for j, v in enumerate(l, 1):
                c = ws.cell(ini + k, j, v)
                if formatos[j - 1]:
                    c.number_format = formatos[j - 1]
                    c.alignment = Alignment(horizontal="right", vertical="top")
                else:
                    c.alignment = Alignment(wrap_text=True, vertical="top")
            for j, mapa in (cores or {}).items():
                if l[j] in mapa:
                    ws.cell(ini + k, j + 1).fill = PatternFill("solid", fgColor=mapa[l[j]])
                    ws.cell(ini + k, j + 1).font = Font(bold=True)
        ultima = get_column_letter(len(cabecalho))
        ws.add_table(Table(displayName=nome, ref=f"A{cab}:{ultima}{fim}",
                           tableStyleInfo=TableStyleInfo(name="TableStyleLight9", showRowStripes=True)))
        for j in barras:
            col = get_column_letter(j + 1)
            ws.conditional_formatting.add(f"{col}{ini}:{col}{fim}",
                                          DataBarRule(start_type="num", start_value=0, end_type="max", color="5B9BD5"))
        ws.freeze_panes = ws.cell(ini, congelar_col)
        self.linha = fim + 2


TORAX = "02.06.02.003-1"
ANGIO = TORAX + " (angio coronária)"


def chave(i):
    """O código da linha; a angio coronária fica à parte da TC de tórax, embora use o mesmo código."""
    return ANGIO if i["codigo"] == TORAX and "coronária" in (i["protocolo"] or "") else i["codigo"]


def situar(f, metas):
    """A situação da fila no plano 4, o porquê do que fica fora da carteira 1 e onde cai o resto dos pedidos.

    metas = {carteira: exames da fila de hoje}, sem os pedidos novos esperados.
    """
    m = f["motivo"] or ""
    if f["cobertura"] == "fora":
        if m.startswith("D-009"):
            s, m = "Fora: emergência", "fila de emergência; o plano 4 é só ambulatorial (D-009)"
        elif "L-008" in m:
            s = "Fora: tem dono"
        elif "fora do foco" in m:
            s = "Fora do foco agora"
        else:
            s = "Fora: outra equipe ou equipamento"
        return s, m, s
    c1 = metas.get(RECOMENDADA, 0)
    if c1 >= f["fila"]:
        return "No plano", "", "Na carteira 1"
    if f["codigo"] == TRANSVAGINAL:
        motivo, resto = "4.000 pedidos reservados à OCI GIN1 do IEV (3.218 OCI, com folga de faltas)", "Fora: tem dono"
    elif f["cobertura"] == "parcial":
        motivo, resto = "sem os pedidos com o CID da OCI do IEV: " + m, "Fora: tem dono"
    elif "coronária" in (f["protocolo"] or ""):
        motivo, resto = "angio coronária: a prioridade é não atender (usuário, 02/11/2026)", "Só em outra carteira"
    elif f["fila"] < MINIMO_FILA:
        motivo, resto = "menos de 30 pedidos: não vira item próprio na carteira", "Livre, fila pequena"
    else:
        motivo, resto = "a carteira 1 não usa esta fila", "Livre, sem carteira"
    if any(metas.values()) and not c1 and resto.startswith("Livre"):
        resto = "Só em outra carteira"
    return ("No plano, em parte" if c1 else resto), motivo, resto


def ler_aba(wb, nome):
    """As linhas de dados de uma aba do estudo (cabeçalho na linha 4)."""
    ws = wb[nome]
    linhas = []
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] is None:
            break
        linhas.append(list(r))
    return linhas


def main():
    d = json.load(open(ORIGEM_JSON, encoding="utf-8"))
    original = load_workbook(ORIGEM_XLSX)
    filas = d["filas"]
    cenarios = dict(zip(LETRAS, d["cenarios"].values()))
    v26 = {l["codigo"]: l for l in d["v26"]}

    # por código, em cada carteira
    por_codigo = {k: defaultdict(lambda: [0, 0.0]) for k in cenarios}
    descricao, preco, modalidade = {}, {}, {}
    for k, itens in cenarios.items():
        for i in itens:
            c = chave(i)
            por_codigo[k][c][0] += i["meta"]
            por_codigo[k][c][1] += i["valor"]
            descricao[c] = i["descricao_candanga"] if c == i["codigo"] else "Angiotomografia de coronárias (no código da TC de tórax)"
            preco[c] = i["preco"]
            modalidade[c] = i["modalidade"]
    for c, l in v26.items():
        descricao.setdefault(c, l["descricao"])
        preco.setdefault(c, l["preco_candanga"])
        modalidade.setdefault(c, "Ultrassom" if c.startswith("02.05") else "Tomografia")
    # elegível = os livres da aba Quem atende o quê: a fila livre inteira e, na parcial, só os pedidos sem o CID da OCI
    elegivel = defaultdict(int)
    for r in ler_aba(original, "Quem atende o quê"):
        if r[2] in ("livre", "parcial"):
            elegivel[r[1]] += r[9] or 0
    # a angio coronária sai da linha da TC de tórax: a fila dela, sem emergência, vira linha própria
    angio = sum(f["fila"] for f in filas if chave(f) == ANGIO and "emergência" not in (f["protocolo"] or ""))
    elegivel[ANGIO] = angio
    elegivel[TORAX] -= angio

    def totais(k):
        itens = cenarios[k]
        return (sum(i["meta"] for i in itens), sum(i["valor"] for i in itens),
                sum(min(i["meta"], i["fila_viva"] or 0) for i in itens),
                len({i["codigo"] for i in itens}))

    cap = {r[0]: r for r in ler_aba(original, "Carteiras") if r[0] and r[0][0] in LETRAS and isinstance(r[1], int)}
    horas = {nome[0]: (r[3], r[4], r[5], r[6]) for nome, r in cap.items()}

    # fila por fila: a meta de cada carteira (a da fila de hoje e a dos pedidos novos) e a situação no plano 4
    base, novos = defaultdict(dict), defaultdict(dict)
    for k, itens in cenarios.items():
        for i in itens:
            if i["nome"].endswith(SUFIXO_NOVOS):
                novos[(i["nome"][: -len(SUFIXO_NOVOS)], i["codigo"])][k] = i["meta"]
            else:
                base[(i["nome"], i["codigo"])][k] = i["meta"]
    chaves = {(f["nome"], f["codigo"]) for f in filas}
    assert set(base) <= chaves and set(novos) <= chaves, "item de carteira sem fila no inventário"
    sit_fila = {(f["nome"], f["codigo"]): situar(f, base.get((f["nome"], f["codigo"]), {})) for f in filas}
    nome_exame = {}
    for f in filas:
        if f["descricao_candanga"]:
            nome_exame.setdefault(f["codigo"], f["descricao_candanga"].capitalize())
    for r in ler_aba(original, "Rumo por código"):
        nome_exame.setdefault(r[0], (r[1] or "").capitalize())
    modal_cod = {f["codigo"]: f["modalidade"] for f in filas}
    # por código: onde caem os pedidos de hoje
    por_cod = defaultdict(lambda: defaultdict(int))
    motivos_cod = defaultdict(list)
    for f in filas:
        k = (f["nome"], f["codigo"])
        s, motivo, resto = sit_fila[k]
        dentro = min(base.get(k, {}).get(RECOMENDADA, 0), f["fila"])
        por_cod[f["codigo"]]["Na carteira 1"] += dentro
        por_cod[f["codigo"]][resto] += f["fila"] - dentro
        if f["fila"] > dentro and motivo and motivo not in motivos_cod[f["codigo"]]:
            motivos_cod[f["codigo"]].append(motivo)

    def situar_codigo(c):
        p = por_cod[c]
        ambulatorial = sum(p.values()) - p["Fora: emergência"]
        if ambulatorial and p["Na carteira 1"] >= 0.99 * ambulatorial:
            return "No plano"
        if p["Na carteira 1"]:
            return "No plano, em parte"
        return max((s for s in SITUACOES if s != "Na carteira 1"), key=lambda s: p[s])

    def fora_codigo(c):
        p = por_cod[c]
        partes = [s.lower() + ": " + f"{p[s]:,}".replace(",", ".") for s in SITUACOES if s != "Na carteira 1" and p[s]]
        return "; ".join(partes)

    def carteiras_da(k):
        tem = [c for c in LETRAS if base.get(k, {}).get(c) or novos.get(k, {}).get(c)]
        return ", ".join(tem) or "—"

    def faixa(n):
        return ("5.000 ou mais" if n >= 5000 else "1.000 a 4.999" if n >= 1000 else "100 a 999" if n >= 100
                else "30 a 99" if n >= MINIMO_FILA else "menos de 30")

    wb = Workbook()
    wb.remove(wb.active)

    # 1. Resumo
    a = Aba(wb, "Resumo", "Plano 4 — estudo das filas de imagem (02/11/2026)",
            "Controle interno. Ultrassom e tomografia ambulatoriais, preço da Tabela SUS Candanga (Anexo Único, SIA). "
            "As filas são do Mapa Social de 02/11/2026. Nada daqui vai ao plano sem decisão do usuário.",
            [44, 17, 17, 17, 17, 17, 17])
    a.subtitulo("As carteiras lado a lado")
    linhas = [["Exames"], ["Valor dos exames"], ["Na fila viva (pedidos dos últimos 24 meses)"], ["Códigos"],
              ["Horas de ultrassom"], ["Uso das 13 salas de ultrassom"], ["Horas de tomógrafo"], ["Uso dos 6 tomógrafos"],
              ["Depende de a SES confirmar"]]
    v26_total = (79144, 10636542.52, None, 11)
    linhas[0].append(v26_total[0]); linhas[1].append(v26_total[1]); linhas[2].append(None); linhas[3].append(11)
    for l, v in zip(linhas[4:8], (24260, 24260 / 17472, 4478, 4478 / 8064)):
        l.append(v)
    linhas[8].append("parede e angio coronária")
    pendente = {k: "" for k in LETRAS}
    for k in LETRAS:
        p_ = sum(i["meta"] for i in cenarios[k] if "PAREDE" in i["nome"].upper())
        a_ = sum(i["meta"] for i in cenarios[k] if "coronária" in (i["protocolo"] or ""))
        n_ = sum(i["meta"] for i in cenarios[k] if i["cobertura"] == "crescimento da fila")
        partes = ([f"parede ({p_:,})".replace(",", ".")] if p_ else []) + \
                 ([f"angio coronária ({a_:,})".replace(",", ".")] if a_ else []) + \
                 ([f"{n_:,} pedidos novos".replace(",", ".")] if n_ else [])
        pendente[k] = "; ".join(partes) or "nada"
    for k in LETRAS:
        t = totais(k)
        h = horas[k]
        for l, v in zip(linhas, (t[0], t[1], t[2], t[3], h[0], h[1], h[2], h[3], pendente[k])):
            l.append(v)
    formatos_linha = [INTEIRO, REAL, INTEIRO, INTEIRO, INTEIRO, PCT, INTEIRO, PCT, None]
    ws = a.ws
    cab = ["", "v26 assinada", *[f"Carteira {k}" + (" (recomendada)" if k == RECOMENDADA else
                                                     " (sem angio)" if k in SEM_ANGIO else " (com angio)") for k in LETRAS]]
    for j, h in enumerate(cab, 1):
        c = ws.cell(a.linha, j, h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=AZUL)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA
    ws.row_dimensions[a.linha].height = 32
    a.linha += 1
    for k, (l, fmt) in enumerate(zip(linhas, formatos_linha)):
        for j, v in enumerate(l, 1):
            c = ws.cell(a.linha, j, v)
            c.border = BORDA
            if j == 1:
                c.font = Font(bold=True)
            elif fmt:
                c.number_format = fmt
            c.alignment = Alignment(horizontal="left" if j == 1 or not fmt else "right", vertical="center", wrap_text=True)
            if k % 2:
                c.fill = PatternFill("solid", fgColor=CINZA)
        for k in SEM_ANGIO:
            ws.cell(a.linha, 3 + LETRAS.index(k)).fill = PatternFill("solid", fgColor=AZUL_CLARO)
        a.linha += 1
    a.linha += 1
    a.nota("Só as carteiras que chegam ao valor dos exames da v26. Todas sem a US de articulação (comprometida com o IEV) e com 4.000 transvaginais reservadas à GIN1 do IEV.")
    a.nota("1 — recomendada: a parede abdominal no código do abdômen total, sem a angio coronária, e os pedidos novos esperados nas filas em déficit (saldo por mês × 8 meses).")
    a.nota("2 — a parede abdominal e a angio coronária, se a SES confirmar as duas (L-007); só a fila de hoje.")
    a.nota("3 — se a SES não aceitar a parede: a angio coronária e os pedidos novos esperados.")
    a.nota("4 — a v26 como está, limitada à fila de hoje, mais TC e os pedidos novos esperados (com parede e angio coronária, como a v26).")
    a.nota("5 — a mesma v26 com mais TC, sem angio coronária; depende de 6.842 pedidos novos.")
    a.nota("Valor de referência: R$ 10.636.542,52 de exames (v26). Com o apoio de R$ 956.160,00, todas cabem no recurso de R$ 11.592.762,00.")
    a.nota("Prioridade do usuário (02/11/2026): não atender angio coronária. Ficam de pé as carteiras 1 e 5; "
           "a 2, a 3 e a 4 levam a angio e só servem se essa prioridade mudar (a 3 é a saída se a SES recusar a parede).")
    a.subtitulo("Como ler a situação de cada fila")
    legenda = [("livre", "Nenhum plano aprovado atende. Todos os pedidos podem entrar no plano 4."),
               ("parcial", "Uma OCI que o IEV já contratou aceita parte dos pedidos (os com o CID dela). "
                           "Esses ficam com o IEV; o resto é livre."),
               ("fora", "A fila inteira já tem dono, é emergência ou não cabe no plano 4 (outra equipe ou outro equipamento).")]
    for situacao, texto in legenda:
        c = ws.cell(a.linha, 1, situacao)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=COR_SITUACAO[situacao])
        c.border = BORDA
        c.alignment = Alignment(vertical="center")
        ws.merge_cells(start_row=a.linha, start_column=2, end_row=a.linha, end_column=7)
        c = ws.cell(a.linha, 2, texto)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        for j in range(2, 8):
            ws.cell(a.linha, j).border = BORDA
        ws.row_dimensions[a.linha].height = 32
        a.linha += 1

    # 1b. Painel: onde caem os pedidos de hoje, em pedidos
    colunas = [s for s in SITUACOES if any(p[s] for p in por_cod.values())]
    a = Aba(wb, "Painel", "Onde caem os pedidos de hoje",
            "Todas as 656 filas de imagem do Mapa Social de 02/11/2026, em pedidos. Na carteira 1 = o que a carteira "
            "recomendada leva da fila de hoje (sem os pedidos novos esperados). O resto de cada fila cai na situação que "
            "explica por que fica de fora. A aba Filas tem o porquê fila por fila.",
            [40, 13, 13, 13, 13, 13, 13, 13, 13, 13])
    a.subtitulo("Por modalidade")
    linhas = []
    for mod in ("Ultrassom", "Tomografia", "Radiologia", "Ressonância", "Medicina nuclear",
                "Radiologia intervencionista", "outra"):
        cods = [c for c in por_cod if modal_cod[c] == mod]
        if cods:
            linhas.append([mod, *[sum(por_cod[c][s] for c in cods) for s in colunas]])
    tot = ["Total", *[sum(l[j] for l in linhas) for j in range(1, len(colunas) + 1)]]
    linha_mod, n_mod = a.linha + 1, len(linhas)
    a.tabela(["Modalidade", *colunas], linhas, [None, *[INTEIRO] * len(colunas)], total=tot)
    a.subtitulo("Situação no plano 4: o que cada uma quer dizer")
    legenda = {
        "Na carteira 1": "a carteira recomendada leva estes pedidos",
        "Só em outra carteira": "fica fora da 1 e entra noutra; hoje, a angio coronária (carteiras 2, 3 e 4)",
        "Livre, fila pequena": "ninguém atende, mas a fila tem menos de 30 pedidos e não vira item próprio",
        "Fora: tem dono": "comprometida com um plano aprovado do IEV (articulação, partes moles, TC ortopédica, a reserva da GIN1, os CID das OCI)",
        "Fora: emergência": "o plano 4 é só ambulatorial (D-009)",
        "Fora: outra equipe ou equipamento": "eco, globo ocular, obstétricas, PET-CT, cone beam, sedação, ressonância, medicina nuclear",
        "Fora do foco agora": "radiologia: mapeada, sem ataque agora (usuário, 02/11/2026)",
    }
    for s, texto in legenda.items():
        c = a.ws.cell(a.linha, 1, s)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=SITUACOES[s][1])
        c.border = BORDA
        a.ws.merge_cells(start_row=a.linha, start_column=2, end_row=a.linha, end_column=10)
        a.ws.cell(a.linha, 2, texto).alignment = Alignment(wrap_text=True, vertical="center")
        a.linha += 1
    a.subtitulo("Ultrassom e tomografia, por código (filas de 100 pedidos ou mais)")
    cods = sorted((c for c in por_cod if modal_cod[c] in ("Ultrassom", "Tomografia") and sum(por_cod[c].values()) >= 100),
                  key=lambda c: -sum(por_cod[c].values()))
    linhas = [[f"{nome_exame.get(c, c)[:48]} ({c})", *[por_cod[c][s] for s in colunas]] for c in cods]
    linha_cod = a.linha + 1
    a.tabela(["Exame (código)", *colunas], linhas, [None, *[INTEIRO] * len(colunas)])

    def grafico(titulo, primeira, n, ancora, altura):
        g = BarChart()
        g.type, g.grouping, g.overlap = "bar", "stacked", 100
        g.title, g.height, g.width = titulo, altura, 26
        dados = Reference(a.ws, min_col=2, max_col=1 + len(colunas), min_row=primeira - 1, max_row=primeira + n - 1)
        g.add_data(dados, titles_from_data=True)
        g.set_categories(Reference(a.ws, min_col=1, min_row=primeira, max_row=primeira + n - 1))
        for serie, s in zip(g.series, colunas):
            serie.graphicalProperties.solidFill = SITUACOES[s][0]
            serie.graphicalProperties.line.solidFill = SITUACOES[s][0]
        g.x_axis.scaling.orientation = "maxMin"
        g.x_axis.delete = g.y_axis.delete = False
        g.y_axis.numFmt = "#,##0"
        g.y_axis.majorGridlines = None
        g.legend.position = "b"
        a.ws.add_chart(g, ancora)

    grafico("Pedidos de hoje por modalidade", linha_mod, n_mod, "L3", 9)
    grafico("Ultrassom e tomografia: onde cai cada pedido de hoje", linha_cod, len(linhas), "L24", 2 + 0.55 * len(linhas))
    a = Aba(wb, "Carteiras por código", "Quanto de cada exame entra em cada carteira",
            "Meta em exames. Fila elegível = pedidos de hoje sem emergência e sem os que já têm dono. "
            "A meta só passa da fila elegível nos pedidos novos esperados das carteiras 1 e 3 (filas em déficit, saldo por mês × 8 meses). "
            "A angio coronária usa o código da TC de tórax e está em linha própria; na coluna v26 ela segue dentro dos 5.240 da TC de tórax (a reunião de 07/10 contava 1.413 angios).",
            [46, 19, 19, 17, 13, 13, 13, 13, 13, 15, 13])
    codigos = sorted(set(elegivel) & (set(descricao)), key=lambda c: (modalidade[c], -(por_codigo[RECOMENDADA][c][1])))
    codigos = [c for c in codigos if any(por_codigo[k][c][0] for k in LETRAS) or c in v26]
    for mod in ("Ultrassom", "Tomografia"):
        a.subtitulo(mod)
        linhas = []
        for c in [c for c in codigos if modalidade[c] == mod]:
            nome = descricao[c] if c == ANGIO else descricao[c].capitalize() + (" (sem a angio coronária)" if c == TORAX else "")
            linhas.append([nome, c.split(" ")[0], preco[c], v26.get(c, {}).get("meta", 0),
                           *[por_codigo[k][c][0] for k in LETRAS], elegivel[c], "novo" if c not in v26 and c != ANGIO else ""])
        n = len(LETRAS)
        tot = ["Total", None, None, *[sum(l[j] for l in linhas) for j in range(3, 5 + n)], None]
        a.tabela(["Exame", "Código", "Preço Candanga", "v26", *[f"Carteira {k}" for k in LETRAS],
                  "Fila elegível hoje", "Código novo no plano"],
                 linhas, [None, None, REAL, INTEIRO, *[INTEIRO] * n, INTEIRO, None], total=tot)
    a.subtitulo("Valor por carteira")
    linhas = []
    for mod in ("Ultrassom", "Tomografia"):
        linhas.append([mod, *[sum(i["valor"] for i in cenarios[k] if i["modalidade"] == mod) for k in LETRAS]])
    a.tabela(["", *[f"Carteira {k}" for k in LETRAS]], linhas, [None, *[REAL] * len(LETRAS)],
             total=["Total", *[totais(k)[1] for k in LETRAS]])

    # 3. Quem atende o quê
    a = Aba(wb, "Quem atende o quê", "Quem atende cada fila hoje",
            "Só contam os planos aprovados (os cinco convênios do acervo). Os nossos planos em elaboração não cobrem fila. "
            "A parte com o CID da OCI vem das medições de 26/10 (articulação), 27/10 (TC de pelve) e 02/11 (transvaginal).",
            [40, 16, 11, 30, 46, 12, 12, 12, 12, 11, 11, 11, 11, 11])
    quem = ler_aba(original, "Quem atende o quê")
    cabecalho = ["Exame", "Código", "Situação", "Quem atende", "OCI e papel do exame, ou por que fica fora",
                 "OCI contratadas", "Pedidos na fila", "Reservados ao IEV", "Livres para o plano 4",
                 *[f"Carteira {k}" for k in LETRAS]]
    formatos = [None, None, None, None, None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, *[INTEIRO] * len(LETRAS)]
    for situacao, titulo in (("livre", "Livres: nenhum plano aprovado atende"),
                             ("parcial", "Parciais: uma parte da fila fica reservada ao IEV"),
                             ("fora", "Fora do plano 4")):
        linhas = []
        for r in quem:
            if r[2] != situacao:
                continue
            explica = r[4] if situacao != "fora" else (f"{r[4]} — {r[6]}" if r[4] and "partes moles" in r[4] else r[6])
            linhas.append([r[0].capitalize(), r[1], r[2], r[3], explica, r[5], r[7], r[8], r[9], *r[10:10 + len(LETRAS)]])
        a.subtitulo(titulo)
        a.tabela(cabecalho, linhas, formatos, situacao_col=2,
                 total=["Total", None, None, None, None, None, *[sum(l[j] or 0 for l in linhas) for j in range(6, 9 + len(LETRAS))]])

    # 4. Rumo por código: todos os códigos de imagem, com a situação no plano 4
    a = Aba(wb, "Rumo das filas", "Todos os códigos de imagem: estão no plano? a fila cresce?",
            "Os 133 códigos das 656 filas de imagem, sem corte. Situação no plano 4 = onde cai a fila de hoje: "
            "na carteira 1, ou fora, e por quê (a coluna Fica fora diz quantos pedidos em cada motivo; a aba Filas, fila "
            "por fila). Rumo nos 12 meses fechados (out./2025 a set./2026): entram = pedidos novos por mês; oferta = "
            "agendamentos por mês; estimativa por entradas e agendamentos, não a queda observada do estoque. "
            "Use as setas do cabeçalho para filtrar por modalidade, situação ou classe e para ordenar por tamanho da fila.",
            [14, 40, 16, 20, 11, 11, 11, 46, 46, 13, 11, 11, 11, 11, 11, 12, 12, 10, 20, 46])
    linhas = []
    for r in ler_aba(original, "Rumo por código"):
        c = r[0]
        p = por_cod[c]
        motivos = "; ".join(motivos_cod[c])
        cart = ", ".join(k for k in LETRAS if any(base.get((f["nome"], c), {}).get(k) for f in filas if f["codigo"] == c))
        linhas.append([modal_cod.get(c, ""), nome_exame.get(c, c), c, situar_codigo(c), sum(p.values()),
                       p["Na carteira 1"], sum(p.values()) - p["Na carteira 1"], fora_codigo(c), motivos, cart or "—",
                       r[3], round(r[5] / 12), round(r[7] / 12), round(r[15]), r[12], r[16], r[17], r[11], r[19], r[20]])
    ordem = ("Ultrassom", "Tomografia", "Radiologia", "Ressonância", "Medicina nuclear", "Radiologia intervencionista", "outra")
    linhas.sort(key=lambda l: (ordem.index(l[0]) if l[0] in ordem else 9, -l[4]))
    a.tabela_excel("Rumo", ["Modalidade", "Exame", "Código", "Situação no plano 4", "Fila de hoje",
                            "Na carteira 1", "Fica fora", "Onde cai o que fica fora (pedidos)", "Por que fica fora",
                            "Carteiras que usam", "Fila viva", "Entram por mês", "Oferta por mês",
                            "Oferta, 3 últimos meses", "Saldo por mês", "Meses para zerar (ritmo 12 m)",
                            "Meses para zerar (ritmo 3 m)", "Falta na SES", "Classe", "Por quê (classe)"], linhas,
                   [None, None, None, None, INTEIRO, INTEIRO, INTEIRO, None, None, None, INTEIRO, INTEIRO, INTEIRO,
                    INTEIRO, "#,##0;-#,##0", "0.0", "0.0", PCT, None, None],
                   somar=(4, 5, 6, 10, 11, 12, 13), barras=(4,), cores={3: COR_FILA}, congelar_col=4)

    # 4b. Crescimento e faltas
    a = Aba(wb, "Crescimento e faltas", "Há pedidos para repor as faltas?",
            "Carteira 1. Para cumprir a meta com faltas, é preciso agendar meta ÷ (1 − faltas). Disponíveis = fila elegível "
            "de hoje + o crescimento líquido em 8 meses (o que entra além do que a SES agenda). O que faltar a regulação "
            "precisa mandar das entradas do período. Controle interno: o plano não traz taxa de faltas.",
            [40, 16, 12, 11, 11, 11, 12, 11, 11, 12, 12, 12, 12, 12])
    cf = ler_aba(original, "Crescimento e faltas")
    linhas = [[r[1].capitalize(), r[0], r[2], r[3], r[4], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[17], r[18]] for r in cf]
    tot = ["Total", None, *[sum(l[j] or 0 for l in linhas) for j in range(2, 7)], None,
           *[sum(l[j] or 0 for l in linhas) for j in range(8, 12)], None, None]
    a.tabela(["Exame", "Código", "Fila elegível hoje", "Entram por mês", "SES agenda por mês",
              "Cresce em 8 meses (líquido)", "Entram em 8 meses", "Faltas na SES", "Meta", "Agendar com 20% de faltas",
              "Agendar com 30% de faltas", "Disponíveis no período", "Parte das entradas a pedir (20%)",
              "Parte das entradas a pedir (30%)"], linhas,
             [None, None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, PCT, INTEIRO, INTEIRO, INTEIRO, INTEIRO, PCT, PCT],
             total=tot)

    # 5. Filas: uma linha por fila, com a situação e as carteiras que a usam
    a = Aba(wb, "Filas", "Fila por fila: situação no plano 4 e carteiras",
            "As 656 filas de imagem do Mapa Social (02/11/2026), nome exato × código, sem corte. Uma linha por fila: a "
            "coluna Carteiras diz em quais ela entra, e as colunas Carteira 1 a 5 dizem quantos exames (com os pedidos novos "
            "esperados). A fila são os três status pendentes; as devolvidas ficam ao lado e não se subtraem; somar filas "
            "não dá pessoas. Filtre por modalidade, exame, protocolo, tamanho ou situação; ordene pela fila.",
            [13, 34, 16, 48, 18, 13, 10, 10, 10, 10, 10, 12, 20, 20, 46, 12, 10, 10, 10, 10, 10, 11, 11, 34])
    rumo_cod = {r[0]: r for r in ler_aba(original, "Rumo por código")}
    linhas = []
    for f in sorted(filas, key=lambda f: (ordem.index(f["modalidade"]) if f["modalidade"] in ordem else 9,
                                          f["codigo"], -f["fila"])):
        k = (f["nome"], f["codigo"])
        s, motivo, _ = sit_fila[k]
        metas = [(base.get(k, {}).get(c, 0) + novos.get(k, {}).get(c, 0)) or None for c in LETRAS]
        linhas.append([f["modalidade"], nome_exame.get(f["codigo"], f["codigo"]), f["codigo"], f["nome"],
                       f["protocolo"] or "", faixa(f["fila"]), f["fila"], f["fila_viva"], f["devolvidas"], f["pessoas"],
                       round(f["espera_mediana"]) if f["espera_mediana"] is not None else None, f["mais_antiga"],
                       (rumo_cod.get(f["codigo"]) or [None] * 20)[19], s, motivo, carteiras_da(k), *metas,
                       novos.get(k, {}).get(RECOMENDADA), f["agendadas_12m"], f["cid"]])
    a.tabela_excel("Filas", ["Modalidade", "Exame", "Código", "Fila (nome exato)", "Protocolo", "Tamanho da fila",
                             "Fila", "Fila viva", "Devolvidas (à parte)", "Pessoas", "Espera mediana (dias)",
                             "Pedido mais antigo", "Classe do código", "Situação no plano 4",
                             "Por que fica fora (ou só em parte)", "Carteiras", *[f"Carteira {c}" for c in LETRAS],
                             "Pedidos novos na carteira 1", "Agendadas 12 m", "CID principais"], linhas,
                   [None, None, None, None, None, None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, None, None, None,
                    None, None, *[INTEIRO] * len(LETRAS), INTEIRO, INTEIRO, None],
                   somar=(6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22), barras=(6,), cores={13: COR_FILA}, congelar_col=5)

    # 6. Viabilidade
    a = Aba(wb, "Viabilidade", "Quanto cada exame paga por hora de sala",
            "Ultrassom feito por nós: médico R$ 100/h, sala e aparelho R$ 5.500/mês, insumo R$ 3 (premissas). "
            "Tomografia na clínica: R$ 171,44 com contraste (cotado). Não compare a hora do ultrassom com a do tomógrafo.",
            [52, 16, 13, 10, 13, 14, 14, 20, 11])
    vi = ler_aba(original, "Viabilidade")
    linhas = [[r[0], r[1], r[3], r[5], r[7], r[9], r[10], r[11], r[13]] for r in vi]
    a.tabela_excel("Viabilidade", ["Fila (nome exato)", "Código", "Preço", "Minutos", "Custo por exame", "R$ por hora",
                                   "Margem por hora", "Classe", "Situação"], linhas,
                   [None, None, REAL, INTEIRO, REAL, REAL, REAL, None, None], cores={8: COR_SITUACAO}, congelar_col=2)

    # 7. Quem oferta
    a = Aba(wb, "Quem oferta", "Quem sustenta a oferta em cada código",
            "Agendamentos por unidade executante. Unidade que sobe e volta a zero é mutirão; contratado e URD estáveis "
            "são oferta que fica. Novembro ainda vai receber agendamentos.",
            [16, 40, 30, 24, 13, 13, 13, 11, 11, 11, 13])
    qo = [[r[0], nome_exame.get(r[0], ""), *r[1:]] for r in ler_aba(original, "Quem oferta")]
    a.tabela_excel("Oferta", ["Código", "Exame", "Unidade", "Tipo", "12 meses fechados", "Média out.–mar.",
                              "Média jul.–set.", "Maior mês", "Mês do maior", "Out./2026", "Nov./2026 (já agendado)"], qo,
                   [None, None, None, None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, None, INTEIRO, INTEIRO],
                   somar=(4, 9, 10), barras=(4,), congelar_col=4)

    # 8. Fontes
    a = Aba(wb, "Fontes", "De onde vem cada número", None, [40, 90])
    a.tabela(["Fonte", "Arquivo"], ler_aba(original, "Fontes") + [
        ["Planilha completa, com todas as colunas", "estudo_filas_imagem_20261102.xlsx (esta é a cópia organizada)"],
        ["Relatório de decisão", "estudo_filas_imagem_20261102.md"],
        ["Os outros planos", "estudo_outros_planos_imagem_20261102.md e .xlsx"]], [None, None])

    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = AZUL if ws.title in ("Resumo", "Painel", "Carteiras por código", "Rumo das filas", "Filas") else "A6A6A6"
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.print_options.horizontalCentered = True
    wb.save(DESTINO)
    print(DESTINO)


if __name__ == "__main__":
    main()
