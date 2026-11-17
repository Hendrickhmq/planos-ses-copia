"""Cópia organizada da planilha do estudo das filas de imagem, para ler e mostrar.

Lê o que o estudo_filas_imagem_20261102.py gravou (o .json e o .xlsx, nesta pasta) e escreve
estudo_filas_imagem_20261102_organizada.xlsx. Não refaz conta: só reorganiza e formata.

    python3 planos/redacao_04/estudos/formatar_estudo_filas_imagem_20261102.py
"""
import json
import math
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

LETRAS, RECOMENDADA = "123456", "1"
SEM_ANGIO = "156"        # prioridade do usuário (02/11/2026): não atender angio coronária
MINIMO_FILA = 30        # o mesmo corte do estudo: fila menor não vira item próprio na carteira
SUFIXO_NOVOS = " — pedidos novos esperados em 8 meses"
SUFIXO_ENCAMINHADOS = " — encaminhados pela SES em 8 meses"   # carteira 6: contam junto dos pedidos novos
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


POLOS = ("Oeste", "Sudoeste", "Norte", "Leste", "Central e Centro-Sul", "Sul")
DEC = '0.00'
# pessoas por pedido no objeto da v26, coleta de 05/10/2026 (dados/fontes/mapa_social_20261005.md, seção 6):
# 55.546 pessoas em 64.068 pedidos de ultrassom e 6.229 em 11.645 de tomografia
PESSOAS_POR_PEDIDO = {"Ultrassom": 55546 / 64068, "Tomografia": 6229 / 11645}
CURTO = {"02.05.01.004-0": "Doppler (carótidas, membros, renais)", "02.05.02.004-6": "Abdômen total (com a parede)",
         "02.05.02.009-7": "Mama bilateral", "02.05.02.018-6": "Transvaginal (sem os 4.000 do IEV)",
         "02.05.02.005-4": "Aparelho urinário", "02.05.02.012-7": "Tireoide", "02.05.02.010-0": "Próstata por via abdominal",
         "02.05.02.003-8": "Abdômen superior", "02.05.02.007-0": "Bolsa escrotal", "02.05.02.016-0": "Pélvica",
         "02.05.02.017-8": "Transfontanela", "02.06.03.001-0": "TC de abdômen superior", "02.06.03.003-7": "TC de pelve",
         "02.06.02.003-1": "TC de tórax, sem a angio coronária", "02.06.01.007-9": "TC de crânio",
         "02.06.01.005-2": "TC de pescoço", "02.06.01.004-4": "TC de face"}
SIGLAS = [
    ("L-006", "Pendência do parque instalado: as salas e os tomógrafos das clínicas ainda não foram confirmados."),
    ("L-007", "Pendência da parede abdominal: a SES confirmar, por escrito, que a fila \"Ultrassonografia de parede "
              "abdominal\" é feita e faturada no código do abdômen total (02.05.02.004-6)."),
    ("L-008", "Regra \"um pedido, um plano\": nenhum pedido entra no plano 4 e num convênio do IEV ao mesmo tempo. Foi "
              "revista em 02/11: a US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas ao IEV."),
    ("D-009", "Decisão de atender só ambulatório: nenhuma fila de emergência entra no plano."),
    ("LI-002", "Regra de preço: vale a Tabela SUS Candanga, ou o SIGTAP quando ele for igual ou maior."),
    ("Candanga", "Tabela SUS Candanga: o preço que o DF paga por procedimento (Anexo Único, modalidade ambulatorial)."),
    ("IEV", "O proponente dos convênios 030975, 030976 e 030977 com a SES, que executam OCI de ortopedia, ginecologia, "
            "cardiologia e outras."),
    ("OCI", "Oferta de Cuidados Integrados: um pacote do SUS com consulta, exames e retorno, pago de uma vez."),
    ("GIN1", "A OCI de ginecologia (09.06.01.001-2) que o IEV executa; a transvaginal é exame obrigatório dela."),
    ("URD", "Unidade de Referência Distrital: hospital ou serviço de referência do DF inteiro, sem Região de Saúde."),
    ("CBR", "Colégio Brasileiro de Radiologia, de onde vêm os tempos de ultrassom (2017)."),
    ("Fila viva", "Os pedidos feitos nos últimos 24 meses."),
    ("Filas do plano", "As filas que a carteira 1 atende: sem emergência, angio coronária, sedação, reservas do IEV e "
                       "filas com menos de 30 pedidos."),
]


def br(n):
    return f"{round(n):,}".replace(",", ".")


def reais(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x):
    return f"{x:.0%}"


def abas_da_revisao(wb, rv, itens1):
    """As abas da revisão de 02/11 (tarde): enquadramento, capacidade, tempos, pedidos novos, encaminhamento, faltas,
    filas do plano, IEV e origem regional."""
    pr = rv["premissas"]
    cp = rv["capacidade"]
    enc, dem, fal, iev = rv["encaminhamento"], rv["demanda"], rv["faltas"], {l["exame"]: l for l in rv["iev"]}
    meta = sum(i["meta"] for i in itens1)
    valor = sum(i["valor"] for i in itens1)
    us = sum(i["meta"] for i in itens1 if i["modalidade"] == "Ultrassom")
    parede = sum(i["meta"] for i in itens1 if "PAREDE" in i["nome"].upper())
    parede_valor = sum(i["valor"] for i in itens1 if "PAREDE" in i["nome"].upper())
    novos = [i for i in itens1 if i["cobertura"] == "crescimento da fila"]
    infantil = sum(i["meta"] for i in itens1 if "INFANTIL" in i["nome"].upper() or "TRANSFONTANELA" in i["nome"].upper())
    preco_torax = next(i["preco"] for i in itens1 if i["codigo"] == "02.06.02.003-1")
    ses = sum(e["ses_agenda_periodo"] for e in enc)
    red_b = sum(round(e["ses_agenda_periodo"] * e["cenarios"]["b"]["reducao_ses"]) for e in enc)
    red_min = sum(round(e["ses_agenda_periodo"] * e["x_minimo"]) for e in enc)
    tent = sum(f["tentativas_20"] for f in fal)
    art, tv = iev["US de articulação, sem as partes moles"], iev["US transvaginal"]
    sala_h = cp["horas_de_exame_por_sala"]

    # Enquadramento
    a = Aba(wb, "Enquadramento", "Carteira 1: o que está decidido, o que é premissa e o que falta",
            "02/11/2026. Controle interno: nada daqui foi aplicado ao plano de trabalho, ao estado.yaml nem a outro plano.",
            [30, 120])
    blocos = [
        ("Siglas e códigos usados nesta planilha", SIGLAS),
        ("Decisões já tomadas (usuário)", [
            ("Carteira", f"A carteira 1 é a base: {br(meta)} exames e {reais(valor)} de procedimentos pela Candanga "
                         f"({br(us)} de ultrassom e {br(meta - us)} de tomografia, em {len({i['codigo'] for i in itens1})} códigos)."),
            ("Foco", "Ultrassom e tomografia ambulatoriais. Emergência, radiologia, ressonância e medicina nuclear ficam fora."),
            ("Equipamentos", f"{pr['salas']} salas de ultrassom e {pr['tomografos']} tomógrafos."),
            ("Prazo", f"{pr['meses']} meses de produção."),
            ("Angio coronária", f"Não entra. Ela usa o código da TC de tórax e paga o mesmo ({reais(preco_torax)} pela "
                                "Candanga), mas ocupa o tomógrafo por mais tempo (30 minutos, contra 20). Só em último "
                                "caso, para compor valor."),
            ("Parede abdominal", f"É essencial para a proposta e fica na carteira: {br(parede)} exames, "
                                 f"{reais(parede_valor)}. A SES ainda precisa confirmar (L-007)."),
            ("Custos", "A revisão de custos e a cotação dos médicos ficam para outra etapa."),
            ("IEV", "A US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas à GIN1 do IEV (L-008). "
                    "A situação completa está na aba IEV."),
            ("Filas pequenas", "Fila com menos de 30 pedidos não vira item próprio da carteira."),
        ]),
        ("Premissas de planejamento", [
            ("Jornada da sala", f"Cada sala ou tomógrafo funciona {pr['horas_dia']} horas por dia útil. Dessas, "
                                f"{pr['horas_de_exame']:.0f} horas são de exame; as outras "
                                f"{pr['horas_dia'] - pr['horas_de_exame']:.0f} ficam para preparo, limpeza, intervalo "
                                f"entre pacientes, atraso e manutenção. São {pr['dias_uteis_mes']} dias úteis por mês: em "
                                f"{pr['meses']} meses, {br(cp['dias'])} dias e {br(sala_h)} horas de exame por sala."),
            ("Faltas", "As 2 horas de folga não cobrem falta. A falta que não é reposta por encaixe come hora de exame; "
                       "por isso a aba Capacidade por polo mostra o uso com 0%, 10% e 20% das faltas sem reposição. Para "
                       f"abrir vagas, conta-se {pct(pr['falta_planejamento'])} de faltas."),
            ("Tempos", "Na tabela abaixo, por exame."),
            ("Origem dos pedidos", "A Região de Saúde da unidade que pediu o exame, medida no Mapa Social em 02/11 só nas "
                                   "filas da carteira 1 (aba Origem regional). O polo de atendimento é o da Região. Os "
                                   "pedidos de URD e de contratados, que não têm Região, se repartem como os outros."),
            ("Filas do plano", "O Mapa Social dá as entradas e os agendamentos por código, com todas as filas do código "
                               "juntas, inclusive as que o plano não atende (emergência, angio coronária). Para saber "
                               "quanto desse movimento é das filas do plano, usa-se a parte delas nos agendamentos dos "
                               "últimos 12 meses. Exemplo: na TC de tórax, as filas do plano tiveram 88% dos agendamentos; "
                               "então 88% da oferta da SES nesse código conta como sendo delas. A aba Filas do plano tem "
                               "a conta de cada código."),
            ("Pedidos novos", f"{br(sum(i['meta'] for i in novos))} exames da carteira 1 são pedidos que ainda vão entrar. "
                              "A aba Pedidos novos explica de onde vem cada número."),
        ]),
    ]
    for titulo, linhas in blocos:
        a.subtitulo(titulo)
        a.tabela(["Item", "O quê"], [[x, y] for x, y in linhas], [None, None])

    a.subtitulo("Tempos de sala por exame")
    base = {(t[0], t[2]): t[3] for t in rv["tempos"]}
    grupos = defaultdict(lambda: [0, set(), ""])
    for nome, codigo, m, mins, gid in rv["origem_por_fila"]:
        g = grupos[(codigo[:5], gid, mins)]
        g[0] += m
        g[1].add(nome.split(" — ")[0].strip())
        g[2] = base[(codigo, mins)]
    linhas = []
    for (mod, gid, mins), (m, nomes, b) in sorted(grupos.items(), key=lambda x: (x[0][0], -x[0][2], x[0][1])):
        linhas.append([rv["participacoes"][gid]["nome"], mins, m, m * mins / 60, len(nomes), b])
    a.tabela(["Exame", "Minutos", "Exames na carteira 1", "Horas", "Filas", "De onde vem o tempo"], linhas,
             [None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, None])
    a.nota("O Doppler bilateral de membros leva 40 minutos porque se examina um lado de cada vez (2 × 20); o SIGTAP o "
           "conta como um exame só. Na TC, o tempo depende do contraste. Nenhum tempo foi reduzido para caber nas salas.")

    a.subtitulo("Para confirmar com a SES")
    a.tabela(["Item", "O quê"], [
        ("Parede abdominal (L-007)", f"Que a fila de parede abdominal é feita e faturada como abdômen total "
                                     f"(02.05.02.004-6), por escrito. São {br(parede)} exames e {reais(parede_valor)}."),
        ("Se faltar fila", "A tratativa, em ordem (abaixo)."),
        ("IEV (L-008)", f"Se a regulação manda às OCI do IEV os pedidos das filas de exame. US de articulação: "
                        f"{br(art['pedidos'])} pedidos de {br(art['pessoas'])} pessoas na fila; o IEV contratou "
                        f"{br(art['contratado'])} OCI que incluem essa US e, até 26/10, não recebeu nenhum pedido dessa "
                        f"fila. Transvaginal: {br(tv['pedidos'])} pedidos de {br(tv['pessoas'])} pessoas; o IEV contratou "
                        f"{br(tv['contratado'])} OCI GIN1 e fez 20 consultas. A aba IEV tem tudo."),
    ], [None, None])
    a.subtitulo("Se faltar fila: a tratativa, em ordem")
    a.tabela(["Passo", "O quê"], [
        ("1. Acompanhar", "Medir todo mês a fila de cada procedimento do plano e avisar a SES com antecedência quando uma "
                          "fila for acabar antes da meta."),
        ("2. Pedidos novos", "A regulação manda ao projeto os pedidos que entram nas filas do plano, antes de agendá-los "
                             "na rede própria."),
        ("3. A SES encaminha parte da agenda dela", f"A SES deixa de agendar na rede própria uma parte dos pedidos e os "
                                                    f"manda ao projeto. Pela conta, de {br(red_min)} a {br(red_b)} "
                                                    f"agendamentos em 8 meses ({pct(red_b / ses)} da agenda dela nessas "
                                                    "filas, no pior caso). Não precisa suspender o atendimento."),
        ("4. Remanejar", "Se ainda faltar, o quantitativo passa a outro procedimento do objeto que tenha fila, por termo "
                         "aditivo, como a v26 já prevê."),
        ("5. Último caso", "A angio coronária, só para compor valor."),
    ], [None, None])

    a.subtitulo("Dados a medir depois (não agora)")
    a.tabela(["Item", "O quê"], [
        ("Reagendamento", "Quantos pedidos têm mais de um agendamento, e o que acontece com o pedido depois da falta."),
        ("Fila perto do início", "Medir de novo a fila do plano quando houver data: a TC e a mama caem rápido."),
        ("Capacidade real", "Salas, horário e tempo por exame de cada clínica (L-006)."),
        ("Pedidos antigos", "Quantos pedidos com mais de 24 meses ainda têm paciente (busca ativa)."),
    ], [None, None])

    a.subtitulo("Proposta de formulação das metas (para avaliar depois; o plano não foi alterado)")
    a.tabela(["Item", "O quê"], [
        ("Objeto", "Oferecer à regulação da SES-DF exames de ultrassonografia e de tomografia, dos procedimentos e "
                   "filas listados no plano, para usuários regulados com indicação ambulatorial."),
        ("Meta de produção", f"{br(meta)} exames realizados e laudados, por procedimento, verificáveis no TrakCare e na APAC."),
        ("Meta de oferta", f"No mínimo {br(tent)} vagas publicadas à regulação em 8 meses, na curva mensal; a vaga "
                           "liberada por falta volta à regulação no mesmo dia."),
        ("Demanda", "A que a regulação encaminhar, na ordem que ela define. A execução fica condicionada ao envio regular "
                    "da demanda regulada, como no item 13.7 do plano do IEV."),
        ("Resultado", "Redução da espera e da fila dos procedimentos do objeto, medida pelo Mapa Social no início, no "
                      "meio e no fim. Indicador de acompanhamento, e não promessa de zerar a fila."),
        ("Remanejamento", "Esgotada a demanda de um procedimento, o quantitativo passa a outro do objeto, por termo aditivo."),
        ("Não sobreposição", "A regulação não encaminha ao convênio pedido vinculado a OCI em execução por outro convênio."),
        ("Sai do texto", "\"Resolve a totalidade das N solicitações da extração\". A fila apurada fica como justificativa."),
    ], [None, None])
    a.subtitulo("Proteções: para não ter de atender o que o plano não previu")
    a.tabela(["Item", "O quê"], [
        ("Lista fechada", "O plano lista os procedimentos e as filas do SISREG que atende, pelo nome e pelo código. "
                          "Pedido de outra fila não entra, mesmo que use um código do objeto."),
        ("Fora, por escrito", "Emergência e urgência; paciente internado; exame com sedação ou anestesia; angiotomografia "
                              "de coronárias; ultrassom obstétrico; ecocardiografia; US de articulação e de partes moles; "
                              "TC de coluna e de articulações; qualquer exame que peça outro equipamento ou outro especialista."),
        ("Contraste", "Triagem antes do exame (v26, 4.8). Quem não pode receber contraste volta à regulação; o pedido não "
                      "conta na meta nem como falta do projeto."),
        ("Limite do equipamento", "Paciente acima do peso ou do diâmetro que a mesa ou o gantry aceitam, ou que só faria o "
                                  "exame sedado, volta à regulação, nas mesmas condições."),
        ("Crianças", f"A carteira tem {br(infantil)} exames de filas infantis (a transfontanela saiu em 03/11/2026). "
                     "É preciso decidir se a rede atende criança e a partir de que idade. Se não atender, "
                     "essas filas saem da lista e o valor se remaneja."),
        ("Devolução", "Pedido fora do escopo se devolve à regulação em prazo curto, sem contar na meta e sem penalidade."),
        ("Teto, não piso", "O quantitativo de cada procedimento é o máximo a produzir, e não a obrigação de atender toda "
                           "a demanda que chegar. Vaga publicada e não ocupada pela regulação conta na meta de oferta."),
    ], [None, None])

    # Capacidade por polo
    a = Aba(wb, "Capacidade por polo", f"As {pr['salas']} salas de ultrassom e os {pr['tomografos']} tomógrafos, polo a polo",
            f"Carteira 1, {pr['meses']} meses. Cada sala dá {br(sala_h)} horas de exame no período ({pr['horas_de_exame']:.0f} "
            f"de cada {pr['horas_dia']} horas por dia útil; o resto é preparo, intervalo e manutenção). O polo de "
            "atendimento é o da Região de Saúde da unidade que pediu o exame (Mapa Social, 02/11).",
            [30, 14, 14, 12, 14, 14, 14, 14, 14, 14])
    u = cp["ultrassom"]
    ex_p = "Sudoeste"
    tem = cp["salas"][ex_p] * sala_h
    a.subtitulo(f"Como ler, com o polo {ex_p}")
    a.tabela(["Coluna", "Conta", "Resultado"], [
        ["Horas que o polo tem", f"{cp['salas'][ex_p]} salas × {br(sala_h)} horas de exame por sala em 8 meses",
         f"{br(tem)} horas"],
        ["Horas de exame", f"{br(cp['exames_us'][ex_p])} exames, cada um com o seu tempo (15, 20 ou 40 minutos)",
         f"{br(cp['horas_us'][ex_p])} horas"],
        ["Uso, 0% das faltas sem reposição", f"{br(cp['horas_us'][ex_p])} ÷ {br(tem)}: toda falta é reposta por outro "
         "paciente, e nenhum horário fica parado", pct(u[0]["uso"][ex_p])],
        ["Uso, 10% das faltas sem reposição", f"1 de cada 10 horários fica vazio: é preciso marcar {br(cp['horas_us'][ex_p])} "
         f"÷ 0,9 = {br(u[1]['horas_de_agenda'][ex_p])} horas de agenda; ÷ {br(tem)}", pct(u[1]["uso"][ex_p])],
        ["Uso, 20% das faltas sem reposição", f"2 de cada 10 horários vazios: {br(cp['horas_us'][ex_p])} ÷ 0,8 = "
         f"{br(u[2]['horas_de_agenda'][ex_p])} horas de agenda; ÷ {br(tem)}", pct(u[2]["uso"][ex_p])],
        ["Salas que bastariam com 20% sem reposição", f"{br(u[2]['horas_de_agenda'][ex_p])} ÷ {br(sala_h)} horas por sala, "
         "arredondado para cima", f"{u[2]['salas_necessarias'][ex_p]} salas"],
        ["Vagas por dia útil", f"{br(cp['exames_us'][ex_p])} exames ÷ 0,8 (20% de faltas) ÷ {cp['dias']} dias úteis: os "
         "horários publicados à regulação; uns 20% não vêm", f"{cp['vagas_por_dia_us'][ex_p]} vagas"],
    ], [None, None, None])
    a.nota("Publicar mais vagas do que cabe na sala, sabendo que 20% faltam, é a forma de repor as faltas: o polo fica na "
           "coluna de 0%. Se o polo marcar só o que cabe e não repuser quem falta, ele cai nas colunas de 10% ou 20%.")
    a.subtitulo("Ultrassom")
    linhas = [[p, cp["exames_us"][p], cp["horas_us"][p], cp["salas"][p], *[x["uso"][p] for x in u],
               u[-1]["salas_necessarias"][p], cp["vagas_por_dia_us"][p]] for p in POLOS]
    a.tabela(["Polo", "Exames", "Horas de exame", f"Salas (das {pr['salas']})",
              *[f"Uso, {r:.0%} das faltas sem reposição" for r in pr["faltas_residuais"]],
              "Salas que bastariam com 20% sem reposição", "Vagas por dia útil (20% de faltas)"], linhas,
             [None, INTEIRO, INTEIRO, INTEIRO, PCT, PCT, PCT, INTEIRO, INTEIRO],
             total=["Total", sum(cp["exames_us"].values()), sum(cp["horas_us"].values()), pr["salas"],
                    *[x["uso_rede"] for x in u], sum(u[-1]["salas_necessarias"].values()),
                    sum(cp["vagas_por_dia_us"].values())])
    a.nota(f"As {pr['salas']} salas se repartem com pelo menos uma por polo, e cada sala a mais vai ao polo mais carregado. "
           f"Na rede, elas aguentam até {pct(cp['falta_residual_que_cabe'])} de faltas sem reposição; acima de 100% num "
           "polo, ele precisa de encaixe (repor a falta com outro paciente) ou de mandar pacientes a um polo vizinho.")
    a.subtitulo("Tomografia")
    t0 = cp["tomografia"]
    linhas = []
    for p in POLOS:
        linhas.append([p, cp["exames_tc"][p], cp["horas_tc"][p], t0[0]["carga_propria"][p],
                       "sim" if p in pr["polos_com_tomografo"] else "não: vai à Central e Centro-Sul",
                       *[x["carga_final"].get(p) for x in t0]])
    a.tabela(["Polo", "Exames", "Horas de exame", "Carga própria (tomógrafos)", "Tem tomógrafo?",
              *[f"Carga final, {r:.0%} das faltas sem reposição" for r in pr["faltas_residuais"]]], linhas,
             [None, INTEIRO, INTEIRO, DEC, None, DEC, DEC, DEC],
             total=["Total", sum(cp["exames_tc"].values()), sum(cp["horas_tc"].values()),
                    sum(t0[0]["carga_propria"].values()), pr["tomografos"], *[x["uso_rede"] for x in t0]])
    a.nota("Carga 1 = um tomógrafo cheio. Os 5 tomógrafos seguem o cenário de 5 polos do estudo de 20/10: a Leste é "
           "atendida na Central e Centro-Sul, e o que passa de um tomógrafo num polo vai ao vizinho com folga (a Sudoeste "
           "manda à Oeste). A linha Total mostra o uso dos 5 tomógrafos na rede.")

    # Pedidos novos
    a = Aba(wb, "Pedidos novos", "Os pedidos novos da carteira 1: o que são e de onde vêm",
            None, [34, 50, 12, 14, 12, 14, 14, 14, 30])
    total_novos = sum(i["meta"] for i in novos)
    valor_novos = sum(i["valor"] for i in novos)
    for texto in (
        f"O que são: exames da carteira 1 que não estão na fila de hoje. São pedidos que devem entrar nas filas durante "
        f"os 8 meses. Somam {br(total_novos)} exames e {reais(valor_novos)}.",
        f"Por que existem: a fila de hoje das filas do plano, inteira, soma {br(meta - total_novos)} exames e "
        f"{reais(rv['valor_fila_de_hoje'])}. Para chegar ao valor dos exames da v26 (R$ 10.636.542,52), faltavam "
        f"{reais(10636542.52 - rv['valor_fila_de_hoje'])}.",
        "Como foram contados: só nos exames em que a SES agenda menos do que entra (a fila cresce). Em cada um, no máximo "
        "o que sobra por mês (entradas − agendamentos da SES no código) × 8 meses. Primeiro os que rendem mais por hora "
        "de sala, até fechar o valor.",
        "O risco: eles só existem se a fila continuar crescendo. A conta usou o código inteiro; só nas filas do plano, o "
        "que sobra por mês é menor (coluna ao lado). Se a SES atender acima das entradas, ou se a regulação não mandar "
        "esses pedidos ao projeto, eles não chegam, e o valor se remaneja (aba Encaminhamento SES).",
    ):
        a.nota(texto)
    a.linha += 1
    linhas = []
    for p in rv["pedidos_novos"]:
        cabe = p["meta"] <= p["saldo_elegivel_8m"]
        linhas.append([CURTO[p["codigo"]], p["fila"], p["meta"], p["valor"], p["saldo_codigo_mes"], p["limite"],
                       p["saldo_elegivel_8m"], p["fila_elegivel_hoje"],
                       "cabe no que sobra nas filas do plano" if cabe else
                       f"passa {br(p['meta'] - p['saldo_elegivel_8m'])} do que sobra nas filas do plano"])
    a.tabela(["Exame", "Fila", "Pedidos novos", "Valor", "Sobra por mês no código", "Limite (sobra × 8)",
              "Sobra em 8 meses só nas filas do plano", "Fila de hoje nas filas do plano", "Leitura"], linhas,
             [None, None, INTEIRO, REAL, "#,##0.0", INTEIRO, INTEIRO, INTEIRO, None],
             total=["Total", None, total_novos, valor_novos, None, sum(p["limite"] for p in rv["pedidos_novos"]),
                    sum(p["saldo_elegivel_8m"] for p in rv["pedidos_novos"]), None, None])

    # Encaminhamento SES
    SOBRA = '"sobram "#,##0;"faltam "#,##0;"zero"'
    fal_t = {k: sum(f[k] for f in fal) for k in ("ses_agendamentos_12m", "ses_realizados", "ses_faltas", "ses_cancelados",
                                                 "ses_pendentes_confirmacao")}
    realiza_ses = sum(e["ses_realiza_periodo"] for e in enc)
    a = Aba(wb, "Encaminhamento SES", "A SES precisa passar pedidos ao projeto?",
            "A pergunta, exame a exame: se a SES continuar agendando como agenda hoje, sobra pedido para o projeto fazer "
            "a meta? Se não sobra, quantos pedidos a SES precisa passar ao projeto em 8 meses, deixando de agendá-los na "
            "rede dela. Só as filas do plano, a partir da fila de hoje. Nada foi decidido com a SES.",
            [42, 14, 18, 18, 18, 18, 18, 16])
    ex = next(e for e in enc if e["codigo"] == "02.05.02.018-6")
    disp = ex["cenarios"]["a"]["ao_projeto"]
    a.subtitulo("Como ler, com a transvaginal")
    a.tabela(["Passo", "Conta", "Resultado"], [
        ["Fila de hoje", "pedidos esperando nas filas do plano (sem os 4.000 do IEV)", br(ex["estoque_inicio"])],
        ["Entram em 8 meses", "pedidos novos por mês nos últimos 12 meses × 8", br(ex["entradas_periodo"])],
        ["A SES agenda em 8 meses", "o ritmo dela nos últimos 12 meses × 8", br(ex["ses_agenda_periodo"])],
        ["Sobra para o projeto", f"{br(ex['estoque_inicio'])} + {br(ex['entradas_periodo'])} − "
         f"{br(ex['ses_agenda_periodo'])}", br(disp)],
        ["O projeto precisa", f"{br(ex['meta'])} pedidos se toda falta for reagendada no mesmo pedido; "
         f"{br(ex['pedidos_alto'])} se cada falta gastar o pedido (20% de faltas)",
         f"{br(ex['meta'])} a {br(ex['pedidos_alto'])}"],
        ["Faltam", f"{br(ex['meta'])} − {br(disp)} e {br(ex['pedidos_alto'])} − {br(disp)}",
         f"{br(max(0, ex['meta'] - disp))} a {br(max(0, ex['pedidos_alto'] - disp))}"],
        ["A SES precisa passar", "esses pedidos ao projeto, e deixa de agendá-los na rede dela",
         f"{pct(max(0, ex['pedidos_alto'] - disp) / ex['ses_agenda_periodo'])} da agenda dela, no pior caso"],
    ], [None, None, None])
    a.subtitulo("Exame a exame")
    linhas = []
    for e in sorted(enc, key=lambda e: -(e["pedidos_alto"] - e["cenarios"]["a"]["ao_projeto"])):
        d_ = e["cenarios"]["a"]["ao_projeto"]
        passa_b, passa_a = max(0, e["meta"] - d_), max(0, e["pedidos_alto"] - d_)
        linhas.append([CURTO[e["codigo"]], e["meta"], d_, d_ - e["meta"], d_ - e["pedidos_alto"], passa_b, passa_a,
                       passa_a / e["ses_agenda_periodo"] if e["ses_agenda_periodo"] else 0])
    a.tabela(["Exame", "Meta", "Sobra para o projeto, se a SES mantiver a agenda",
              "Basta? Toda falta reagendada", "Basta? Cada falta gasta o pedido",
              "A SES precisa passar: falta reagendada", "A SES precisa passar: falta gasta o pedido",
              "Parte da agenda da SES (pior caso)"], linhas,
             [None, INTEIRO, INTEIRO, SOBRA, SOBRA, INTEIRO, INTEIRO, PCT],
             total=["Total", meta, sum(l[2] for l in linhas), None, None, sum(l[5] for l in linhas),
                    sum(l[6] for l in linhas), sum(l[6] for l in linhas) / ses])
    a.nota("Pedido passado ao projeto não é pedido novo: a SES deixa de agendá-lo na rede dela. Por isso a rede ganha "
           "menos do que o projeto produz: os exames do projeto menos os que a SES deixa de fazer (ela realiza cerca de "
           f"{pct(realiza_ses / ses)} do que agenda).")
    a.subtitulo("Para comparar: três jeitos de a SES agir")
    desc = {"a": "a SES mantém a agenda dela", "b": "a SES passa ao projeto só o que falta (a tabela acima)",
            "c": "a SES para o eletivo e passa tudo ao projeto"}
    linhas = []
    for k in "abc":
        c = [e["cenarios"][k] for e in enc]
        linhas.append([desc[k], sum(round(e["ses_agenda_periodo"] * e["cenarios"][k]["reducao_ses"]) for e in enc),
                       sum(1 for x in c if x["estoque_final_alto"] < 0), sum(1 for x in c if x["estoque_final_baixo"] < 0),
                       sum(x["estoque_final_alto"] for x in c), sum(x["aumento_liquido"] for x in c)])
    a.tabela(["Jeito", "Pedidos que a SES passa ao projeto", "Exames sem pedido suficiente: falta reagendada",
              "Exames sem pedido suficiente: falta gasta o pedido", "Pedidos que sobram na fila no fim (falta reagendada)",
              "Exames a mais na rede"], linhas, [None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO])
    a.nota("Mantendo a agenda, a SES e o projeto disputam os mesmos pedidos, e falta pedido em vários exames. Parando o "
           "eletivo, chegam pedidos demais, o projeto não dá conta, a fila fica do tamanho da de hoje, e a rede ganha "
           "pouco; na TC, a rede perde exame. Passar só o que falta é o meio-termo que sustenta a meta.")
    a.subtitulo("De onde vêm os números")
    a.tabela(["Número", "Valor", "De onde vem"], [
        ["Fila de hoje", sum(e["estoque_inicio"] for e in enc), "Os pedidos esperando hoje nas filas do plano (Mapa Social, 02/11)."],
        ["Entram em 8 meses", sum(e["entradas_periodo"] for e in enc),
         "A média de pedidos novos por mês de out./2025 a set./2026, × 8, só nas filas do plano."],
        ["A SES agenda em 8 meses", ses,
         "Os agendamentos por mês nos mesmos 12 meses, só na parte das filas do plano (na TC de tórax, 88%; no "
         "ultrassom, quase tudo), × 8."],
        ["A SES realiza em 8 meses", realiza_ses, "Dos mesmos agendamentos, os que ficaram como \"procedimento realizado\"."],
    ], [None, INTEIRO, None])

    # Faltas e pedidos
    a = Aba(wb, "Faltas e pedidos", "Faltas: o que a SES registrou e o que isso quer dizer para o projeto",
            "Controle interno: o plano não traz taxa de faltas. A primeira tabela é o que a SES registrou nos 12 meses (Mapa "
            "Social, 02/11). A segunda é a conta para o projeto, com 20% de faltas. A fonte não diz o que acontece com o "
            "pedido depois da falta: se volta à fila, ganha outra vaga ou é encerrado.",
            [40, 15, 15, 15, 15, 15, 15])
    fm = next(f for f in fal if f["codigo"] == "02.05.02.009-7")
    a.subtitulo("Como ler, com a mama")
    a.tabela(["Passo", "Conta", "Resultado"], [
        ["A SES agendou em 12 meses", "agendamentos de mama bilateral, out./2025 a set./2026", br(fm["ses_agendamentos_12m"])],
        ["Realizados", "ficaram como \"procedimento realizado\"", br(fm["ses_realizados"])],
        ["Faltas", "ficaram como \"não realizado por falta do paciente\"", br(fm["ses_faltas"])],
        ["Cancelados", "pela regulação, pelo solicitante ou pelo coordenador", br(fm["ses_cancelados"])],
        ["Sem desfecho", "a data passou, e a unidade não registrou se o exame foi feito", br(fm["ses_pendentes_confirmacao"])],
        ["Falta na SES", f"{br(fm['ses_faltas'])} ÷ ({br(fm['ses_realizados'])} + {br(fm['ses_faltas'])})", pct(fm["falta_ses"])],
        ["Meta do projeto", "exames realizados e laudados", br(fm["meta"])],
        ["Vagas a publicar", f"{br(fm['meta'])} ÷ 0,8 (20% de faltas)", br(fm["tentativas_20"])],
        ["Faltas esperadas", f"{br(fm['tentativas_20'])} − {br(fm['meta'])}", br(fm["faltas_20"])],
        ["Pedidos que o projeto gasta", f"{br(fm['meta'])} se toda falta for reagendada no mesmo pedido; "
         f"{br(fm['tentativas_20'])} se cada falta gastar o pedido",
         f"{br(fm['meta'])} a {br(fm['tentativas_20'])}"],
    ], [None, None, None])
    t = {k: sum(f[k] for f in fal) for k in fal[0] if isinstance(fal[0][k], (int, float))}
    a.subtitulo("1. O que a SES registrou nos 12 meses")
    a.tabela(["Exame", "Agendamentos", "Realizados", "Faltas", "Cancelados", "Sem desfecho", "Falta na SES"],
             [[CURTO[f["codigo"]], f["ses_agendamentos_12m"], f["ses_realizados"], f["ses_faltas"], f["ses_cancelados"],
               f["ses_pendentes_confirmacao"], f["falta_ses"]] for f in fal],
             [None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, PCT],
             total=["Total", t["ses_agendamentos_12m"], t["ses_realizados"], t["ses_faltas"], t["ses_cancelados"],
                    t["ses_pendentes_confirmacao"], t["ses_faltas"] / (t["ses_realizados"] + t["ses_faltas"])])
    a.nota("Os números são do código inteiro (todas as filas dele). A falta na SES fica entre 24% e 44%, conforme o exame. "
           "\"Sem desfecho\" pode esconder exame feito e não registrado.")
    a.subtitulo("2. O que isso quer dizer para o projeto (20% de faltas)")
    a.tabela(["Exame", "Meta (exames)", "Vagas a publicar", "Faltas esperadas",
              "Pedidos gastos: toda falta reagendada", "Pedidos gastos: cada falta gasta o pedido"],
             [[CURTO[f["codigo"]], f["meta"], f["tentativas_20"], f["faltas_20"], f["pedidos_todos_reagendados"],
               f["pedidos_nenhum_reagendado"]] for f in fal],
             [None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO],
             total=["Total", t["meta"], t["tentativas_20"], t["faltas_20"], t["pedidos_todos_reagendados"],
                    t["pedidos_nenhum_reagendado"]])
    fs = rv["faltas_ses"]
    ts = {k: sum(f[k] for f in fs) for k in fs[0] if isinstance(fs[0][k], (int, float)) and k != "falta_ses"}
    a.subtitulo("3. Com a mesma falta da SES em cada exame")
    a.tabela(["Exame", "Falta na SES", "Meta (exames)", "Pedidos: metade reagendada", "Pedidos: nenhuma reagendada",
              "A mais que a meta", "A mais que com 20%", "Faltam se a SES mantém a agenda (metade; nenhuma)",
              "A SES encaminha (nenhuma reagendada)", "Parte da agenda da SES", "Faltam mesmo se a SES parar"],
             [[CURTO[f["codigo"]], f["falta_ses"], f["meta"], f["pedidos_metade_ses"], f["pedidos_nenhum_ses"],
               f["a_mais_que_a_meta"], f["a_mais_que_20"], f"{br(f['faltam_a_metade'])}; {br(f['faltam_a_nenhum'])}",
               f["encaminhar_nenhum"], f["parte_da_agenda_ses"], f["faltam_c"]] for f in fs],
             [None, PCT, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, None, INTEIRO, PCT, INTEIRO],
             total=["Total", ts["pedidos_nenhum_ses"] and 1 - ts["meta"] / ts["pedidos_nenhum_ses"], ts["meta"],
                    ts["pedidos_metade_ses"], ts["pedidos_nenhum_ses"], ts["a_mais_que_a_meta"], ts["a_mais_que_20"],
                    f"{br(ts['faltam_a_metade'])}; {br(ts['faltam_a_nenhum'])}", ts["encaminhar_nenhum"],
                    ts["encaminhar_nenhum"] / ts["ses_agenda_periodo"], ts["faltam_c"]])
    a.nota("Pedidos = meta ÷ (1 − falta da SES do exame) se nenhuma falta for reagendada no mesmo pedido; com metade "
           "reagendada, a meta mais metade das faltas. \"Faltam se a SES mantém a agenda\" compara com a fila de hoje + as "
           "entradas de 8 meses − o que a SES agenda (arranjo a da aba Encaminhamento SES). \"Faltam mesmo se a SES parar\" "
           "compara com a fila de hoje + as entradas (arranjo c): é pedido que não existe nas filas do plano. A falta total "
           "da linha Total é a média pesada pela meta.")
    p_est = sum(i["meta"] * PESSOAS_POR_PEDIDO[i["modalidade"]] for i in itens1)
    for texto in (
        "Vaga não é pedido: a vaga é o horário publicado; o pedido é a solicitação na fila. O reagendamento não é pedido "
        "novo, e o exame realizado conta uma vez.",
        "Baixa na fila não é exame feito: o pedido sai da fila quando é agendado, cancelado ou devolvido, e só o exame "
        "realizado resolve.",
        f"Pessoas: os {br(meta)} exames devem ser de cerca de {br(p_est)} pessoas (na TC, a de abdômen e a de pelve "
        "chegam juntas para a mesma pessoa; estimativa pela coleta de 05/10).",
    ):
        a.nota(texto)

    # Metas pela falta da SES
    a = Aba(wb, "Metas pela falta da SES", "Quanto agendar em cada exame, se o projeto faltar tanto quanto a SES",
            "Controle interno: o plano não traz taxa de faltas. A falta de cada exame é a da SES nos 12 meses (Mapa Social, "
            "02/11): faltas ÷ (realizados + faltas), no código inteiro. A meta é o exame realizado; as vagas são o que é "
            "preciso agendar para chegar nela. A fonte só dá a falta por código: nas filas, vale a do código.",
            [38, 16, 11, 11, 12, 12, 12, 11, 11, 11, 12, 12, 12])
    mes, dias = pr["meses"], pr["dias_uteis_mes"]
    p20 = pr["falta_planejamento"]
    tx = {f["codigo"]: f["ses_faltas"] / (f["ses_realizados"] + f["ses_faltas"]) for f in fal}
    fm = next(f for f in fal if f["codigo"] == "02.05.02.009-7")
    fx = tx[fm["codigo"]]
    a.subtitulo("Como ler, com a mama")
    a.tabela(["Passo", "Conta", "Resultado"], [
        ["Falta na SES", f"{br(fm['ses_faltas'])} faltas ÷ ({br(fm['ses_realizados'])} realizados + {br(fm['ses_faltas'])} faltas)", pct(fx)],
        ["Comparecimento", f"1 − {pct(fx)}", pct(1 - fx)],
        ["Meta", "exames realizados e laudados em 8 meses", br(fm["meta"])],
        ["Vagas a agendar", f"{br(fm['meta'])} ÷ {pct(1 - fx)}", br(round(fm["meta"] / (1 - fx)))],
        ["Faltas esperadas", "vagas − meta", br(round(fm["meta"] / (1 - fx) - fm["meta"]))],
        ["Por mês e por dia útil", f"vagas ÷ {mes} meses; ÷ {dias} dias úteis",
         f"{br(round(fm['meta'] / (1 - fx) / mes))} por mês; {br(math.ceil(fm['meta'] / (1 - fx) / mes / dias))} por dia"],
        ["Pedidos gastos", "a meta se toda falta for reagendada no mesmo pedido; as vagas se nenhuma for",
         f"{br(fm['meta'])} a {br(round(fm['meta'] / (1 - fx)))}"],
    ], [None, None, None])
    ordem = sorted(fal, key=lambda f: -f["meta"])
    linhas, t = [], defaultdict(float)
    for f in ordem:
        x, m = tx[f["codigo"]], f["meta"]
        v = m / (1 - x)
        l = [CURTO[f["codigo"]], f["codigo"], x, 1 - x, m, round(v), round(v - m), round(m / mes), round(v / mes),
             math.ceil(v / mes / dias), round(v - m / (1 - p20)), round(m + (v - m) / 2), round(v)]
        linhas.append(l)
        for k, val in zip(("meta", "vagas", "faltas", "vagas_20"), (m, v, v - m, m / (1 - p20))):
            t[k] += val
    a.subtitulo("1. Por exame (código do procedimento)")
    a.tabela(["Exame", "Código", "Falta na SES", "Comparecimento", "Meta (exames realizados)", "Vagas a agendar",
              "Faltas esperadas", "Exames por mês", "Vagas por mês", "Vagas por dia útil", "Vagas a mais que com 20%",
              "Pedidos gastos: metade reagendada", "Pedidos gastos: nenhuma reagendada"],
             linhas, [None, None, PCT, PCT, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO, INTEIRO],
             total=["Total", "", 1 - t["meta"] / t["vagas"], t["meta"] / t["vagas"], t["meta"], round(t["vagas"]),
                    round(t["faltas"]), round(t["meta"] / mes), round(t["vagas"] / mes),
                    sum(l[9] for l in linhas), round(t["vagas"] - t["vagas_20"]),
                    round(t["meta"] + t["faltas"] / 2), round(t["vagas"])])
    a.nota(f"Vagas a agendar = meta ÷ (1 − falta na SES). Vagas por dia útil = vagas ÷ {mes} meses ÷ {dias} dias, para "
           "cima; o total soma os exames. Na linha Total, a falta é a média que resulta das vagas (1 − meta ÷ vagas). Com "
           f"{pct(p20)} de faltas (premissa do estudo), seriam {br(round(t['vagas_20']))} vagas.")
    filas_m = sorted(rv["origem_por_fila"], key=lambda o: (CURTO[o[1]], -o[2]))
    linhas = []
    for nome, cod, m, _min, _g in filas_m:
        x = tx[cod]
        v = m / (1 - x)
        linhas.append([nome.split(" — ")[0] + (" (pedidos novos em 8 meses)" if " — " in nome else ""), CURTO[cod], x, m,
                       round(v), round(v - m), round(v / mes)])
    a.subtitulo("2. Por fila da carteira 1 (com a falta do código)")
    a.tabela(["Fila", "Exame", "Falta na SES (do código)", "Meta (exames realizados)", "Vagas a agendar",
              "Faltas esperadas", "Vagas por mês"], linhas, [None, None, PCT, INTEIRO, INTEIRO, INTEIRO, INTEIRO],
             total=["Total", "", None, sum(l[3] for l in linhas), sum(l[4] for l in linhas), sum(l[5] for l in linhas),
                    sum(l[6] for l in linhas)], filtro=False)
    a.nota("A soma das filas pode diferir do total por exame em poucas unidades, pelo arredondamento fila a fila.")

    # Filas do plano
    a = Aba(wb, "Filas do plano", "Quanto entra e quanto a SES atende, só nas filas do plano",
            "O Mapa Social dá entradas e agendamentos por código, com todas as filas do código juntas. Aqui o movimento "
            "fica só com as filas que o plano atende: a parte delas nos agendamentos dos últimos 12 meses dá a parte da "
            "oferta da SES; a parte delas na fila de hoje dá a parte do que sobra (a emergência quase não acumula fila). "
            "Sobra negativa = a SES agenda mais do que entra, e a fila cai. Agendamento não é exame realizado.",
            [36, 16, 11, 11, 11, 40, 11, 11, 11, 11, 11, 11])
    linhas = [[CURTO[d["codigo"]], d["codigo"], d["meta"], d["fila_codigo"], d["fila_elegivel"],
               "; ".join(f"{k}: {br(v)}" for k, v in d["fora"].items() if v), d["parte_agendamentos"],
               d["entram_elegivel_mes"], d["ses_agenda_elegivel_mes"], d["ses_realiza_elegivel_mes"],
               d["saldo_elegivel_mes"], d["variacao_observada_mes"]] for d in dem]
    a.tabela(["Exame", "Código", "Meta", "Fila do código", "Fila das filas do plano", "Fora do plano",
              "Parte das filas do plano nos agendamentos", "Entram por mês", "SES agenda por mês", "SES realiza por mês",
              "Sobra por mês", "Variação observada por mês, 15/09 a 02/11"], linhas,
             [None, None, INTEIRO, INTEIRO, INTEIRO, None, PCT, INTEIRO, INTEIRO, INTEIRO, "#,##0;-#,##0", "#,##0;-#,##0"],
             total=["Total", None, *[sum(l[j] or 0 for l in linhas) for j in (2, 3, 4)], None, None,
                    *[sum(l[j] or 0 for l in linhas) for j in range(7, 12)]])
    a.nota("A variação observada compara a fila dos mesmos nomes em 15/09 e em 02/11 (48 dias). Ela cai em quase todos, "
           "inclusive onde a sobra de 12 meses diz que cresce: há saídas além do agendamento (cancelamento, devolução). "
           "Os meses para zerar da aba Rumo das filas são projeção, e não previsão.")

    # IEV
    a = Aba(wb, "IEV", "As filas que o IEV também pode atender: a situação completa",
            "Duas coisas diferentes: quem espera nas filas de exame da SES (Mapa Social, 02/11, sem emergência) e o que o "
            "IEV atendeu nas unidades dele (coleta de 26/10). O IEV recebe pacientes pela consulta de especialidade, e "
            "não pela fila do exame.",
            [34, 16, 12, 12, 14, 32, 44, 12, 40, 18, 40])
    a.subtitulo("1. Quem espera nas filas de exame que o IEV também pode atender")
    a.tabela(["Exame", "Código", "Pedidos na fila", "Fila viva", "Pessoas esperando na fila", "Convênio", "OCI e papel do exame",
              "OCI contratadas", "O que o IEV fez até 26/10", "Fim da vigência", "Regra no plano 4"],
             [[l["exame"], l["codigo"], l["pedidos"], l["fila_viva"], l["pessoas"], l["convenio"], l["oci"],
               l["contratado"], l["feito"], l["vigencia"], l["regra"]] for l in rv["iev"]],
             [None, None, INTEIRO, INTEIRO, INTEIRO, None, None, INTEIRO, None, None, None])
    for texto in (
        f"US de articulação: {br(art['pedidos'])} pedidos, de {br(art['pessoas'])} pessoas. O IEV contratou "
        f"{br(art['contratado'])} OCI de ortopedia com essa US (convênios 030975 e 030977), mais do que a fila inteira. "
        "Até 26/10, ele não recebeu nenhum pedido dessa fila: a OCI entra pela consulta de ortopedia. Se a regulação "
        "passar a mandar a fila ao IEV, ele tem contrato para atendê-la; se não mandar, ela fica sem ninguém.",
        f"Transvaginal: {br(tv['pedidos'])} pedidos, de {br(tv['pessoas'])} pessoas. O IEV contratou "
        f"{br(tv['contratado'])} OCI GIN1 e fez 20 consultas. Por isso, 4.000 pedidos ficam reservados a ele (as OCI com "
        "folga de faltas), e o plano 4 conta só com o resto.",
        "A pergunta à regulação, por escrito: os pedidos das filas de exame (US de articulação e transvaginal) são "
        "encaminhados às OCI do IEV? Com a resposta, a articulação pode voltar ao plano, sem os pedidos reservados ao IEV.",
    ):
        a.nota(texto)
    a.subtitulo("2. O que o IEV atendeu nas unidades dele, de 29/04 a 26/10/2026 (consultas de entrada)")
    a.tabela(["Consulta", "Agendadas", "Realizadas", "Faltas", "Contratado"],
             [[c, ag, re_, fa, ct] for c, ag, re_, fa, ct in rv["iev_consultas"]],
             [None, INTEIRO, INTEIRO, INTEIRO, None])
    for texto in (
        "Fonte: coleta do agente mapa-social de 26/10 nas três unidades onde o IEV executa (Centro Clínico Samambaia, "
        "Centro Clínico e Ecográfico de Sobradinho e CIG Centro de Imagens Gama), output/mapeamento_iev_20261026.md, "
        "seção 3. As agendadas incluem as que ainda vão acontecer.",
        "O painel não traz a APAC, que é como a OCI se fatura: não se sabe quantas consultas viraram OCI. O exame feito "
        "dentro da OCI não passa pelo SISREG e não aparece aqui.",
        "As três unidades existem no CNES com esses nomes, mas são clínicas privadas, cada uma com o seu CNPJ; nenhuma é "
        "do IEV (dados/fontes/cnes_unidades_iev_20261102.md). A ligação com o IEV é por indício. A CIG Gama é a mesma "
        "clínica indicada para o polo Sul do plano 4.",
    ):
        a.nota(texto)

    # Origem regional
    a = Aba(wb, "Origem regional", "De onde vêm os pedidos, por polo",
            "Região de Saúde da unidade que pediu o exame, Mapa Social de 02/11/2026, só nas filas da carteira 1 "
            "(dados/fontes/mapa_social_20261102_regiao.md). Os pedidos sem Região (URD, contratados) se repartem como os "
            "outros.", [40, 12, 12, 12, 12, 12, 14, 12, 14])
    pt = rv["participacoes"]
    a.tabela(["Grupo de filas", "Pedidos", *POLOS, "Sem Região (rateado)"],
             [[v["nome"], v["pedidos"], *[v["polos"][p] for p in POLOS], v["sem_regiao"]] for v in pt.values()],
             [None, INTEIRO, *[PCT] * 6, PCT])


def respostas(rv, itens1):
    """As perguntas da revisão, respondidas com os números das abas novas."""
    pr, cp = rv["premissas"], rv["capacidade"]
    u = cp["ultrassom"]
    enc = rv["encaminhamento"]
    ses = sum(e["ses_agenda_periodo"] for e in enc)
    red_b = sum(round(e["ses_agenda_periodo"] * e["cenarios"]["b"]["reducao_ses"]) for e in enc)
    red_min = sum(round(e["ses_agenda_periodo"] * e["x_minimo"]) for e in enc)
    liq_b = sum(e["cenarios"]["b"]["aumento_liquido"] for e in enc)
    acima = lambda x: [p for p in POLOS if x["uso"][p] > 1]
    polos = "; ".join(f"{p} {cp['salas'][p]}" for p in POLOS)
    tc = cp["tomografia"]
    return [
        (f"As {pr['salas']} salas de ultrassom dão conta?",
         f"Sim, com as faltas repostas: a rede fica em {pct(u[0]['uso_rede'])}. Ela aguenta até "
         f"{pct(cp['falta_residual_que_cabe'])} de faltas sem reposição. Com 10%, a rede fica em {pct(u[1]['uso_rede'])}"
         + (f" e passam de 100%: {', '.join(acima(u[1]))}" if acima(u[1]) else "") + f"; com 20%, em "
         f"{pct(u[2]['uso_rede'])}. Repor as faltas com encaixe é o que faz caber."),
        ("Como ficam as salas por polo?", f"{polos}."),
        (f"Os {pr['tomografos']} tomógrafos dão conta?",
         f"Sim: {pct(tc[0]['uso_rede'])} da capacidade com as faltas repostas e {pct(tc[2]['uso_rede'])} com 20% sem "
         "reposição. A Leste vai à Central e Centro-Sul, e a Sudoeste manda o excedente à Oeste."),
        ("Que encaminhamento da SES sustenta as metas?",
         "A regulação manda ao projeto, código a código, a parte que falta, e a SES reduz a própria agenda na mesma "
         f"medida, sem suspender nada: de {br(red_min)} a {br(red_b)} agendamentos em 8 meses ({pct(red_b / ses)} da "
         f"agenda dela nessas filas, no pior caso). A rede ganha {br(liq_b)} exames líquidos."),
    ]


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
            if i["nome"].endswith(SUFIXO_NOVOS) or i["nome"].endswith(SUFIXO_ENCAMINHADOS):
                suf = SUFIXO_NOVOS if i["nome"].endswith(SUFIXO_NOVOS) else SUFIXO_ENCAMINHADOS
                chave_n = (i["nome"][: -len(suf)], i["codigo"])
                novos[chave_n][k] = novos[chave_n].get(k, 0) + i["meta"]
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
            [44, 17, 17, 17, 17, 17, 17, 17])
    a.subtitulo("As carteiras lado a lado")
    linhas = [["Exames"], ["Valor dos exames"], ["Na fila viva (pedidos dos últimos 24 meses)"], ["Códigos"],
              ["Horas de ultrassom"], ["Uso das 20 salas de ultrassom"], ["Horas de tomógrafo"], ["Uso dos 5 tomógrafos"],
              ["Depende de a SES confirmar"]]
    v26_total = (79144, 10636542.52, None, 11)
    linhas[0].append(v26_total[0]); linhas[1].append(v26_total[1]); linhas[2].append(None); linhas[3].append(11)
    for l, v in zip(linhas[4:8], (24260, 24260 / 26880, 4478, 4478 / 6720)):
        l.append(v)
    linhas[8].append("parede e angio coronária")
    pendente = {k: "" for k in LETRAS}
    for k in LETRAS:
        p_ = sum(i["meta"] for i in cenarios[k] if "PAREDE" in i["nome"].upper())
        a_ = sum(i["meta"] for i in cenarios[k] if "coronária" in (i["protocolo"] or ""))
        n_ = sum(i["meta"] for i in cenarios[k] if i["cobertura"] == "crescimento da fila")
        e_ = sum(i["meta"] for i in cenarios[k] if i["cobertura"] == "encaminhamento da SES")
        partes = ([f"parede ({p_:,})".replace(",", ".")] if p_ else []) + \
                 ([f"angio coronária ({a_:,})".replace(",", ".")] if a_ else []) + \
                 ([f"{n_:,} pedidos novos".replace(",", ".")] if n_ else []) + \
                 ([f"{e_:,} TC encaminhadas pela SES; metade das faltas reagendada".replace(",", ".")] if e_ else [])
        pendente[k] = "; ".join(partes) or "nada"
    for k in LETRAS:
        t = totais(k)
        h = horas[k]
        for l, v in zip(linhas, (t[0], t[1], t[2], t[3], h[0], h[1], h[2], h[3], pendente[k])):
            l.append(v)
    formatos_linha = [INTEIRO, REAL, INTEIRO, INTEIRO, INTEIRO, PCT, INTEIRO, PCT, None]
    ws = a.ws
    cab = ["", "v26 assinada", *[f"Carteira {k}" + (" (escolhida)" if k == RECOMENDADA else
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
    a.nota("1 — escolhida pelo usuário em 02/11/2026: a parede abdominal no código do abdômen total (confirmação da SES pendente, L-007), sem a angio coronária, e os pedidos novos esperados nas filas em déficit. Sem a transfontanela (03/11/2026): o valor dela se espalhou pelos exames com folga sob a falta da SES (Doppler, tireoide, próstata e TC), como encaminhados pela SES.")
    a.nota("6 — a carteira com folga (02/11/2026): a 1 limitada, exame a exame, aos pedidos que chegam com a falta da SES, "
           "se metade das faltas for reagendada no mesmo pedido e a SES encaminhar 20% da própria agenda; o valor que sai "
           "do ultrassom (mama, transvaginal, aparelho urinário, abdômen) vai para a TC de abdômen, de pelve e de pescoço. "
           "Detalhe na seção 7.2 do estudo.")
    a.nota("2 a 5 — ficam só para comparação. A 2, a 3 e a 4 levam a angio coronária; a 3 é a saída sem parede, que não é caminho principal (a parede é essencial, usuário, 02/11/2026).")
    a.nota("Valor de referência: R$ 10.636.542,52 de exames (v26). Com o apoio de R$ 956.160,00, todas cabem no recurso de R$ 11.592.762,00.")
    a.nota("As horas e o uso desta tabela são da rede inteira, contra as 20 salas e os 5 tomógrafos. A conta polo a polo, com as faltas à parte, está na aba Capacidade por polo.")
    a.subtitulo("A carteira 1: as respostas")
    for pergunta, resposta in respostas(d["revisao"], cenarios[RECOMENDADA]):
        c = ws.cell(a.linha, 1, pergunta)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = BORDA
        ws.merge_cells(start_row=a.linha, start_column=2, end_row=a.linha, end_column=7)
        c = ws.cell(a.linha, 2, resposta)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        for j in range(2, 8):
            ws.cell(a.linha, j).border = BORDA
        ws.row_dimensions[a.linha].height = 15 * (len(resposta) // 95 + 1)
        a.linha += 1
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

    abas_da_revisao(wb, d["revisao"], cenarios[RECOMENDADA])

    # 1b. Painel: onde caem os pedidos de hoje, em pedidos
    colunas = [s for s in SITUACOES if any(p[s] for p in por_cod.values())]
    a = Aba(wb, "Painel", "Onde caem os pedidos de hoje",
            "Todas as 656 filas de imagem do Mapa Social de 02/11/2026, em pedidos. Na carteira 1 = o que a carteira "
            "escolhida leva da fila de hoje (sem os pedidos novos esperados). O resto de cada fila cai na situação que "
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
        "Na carteira 1": "a carteira escolhida leva estes pedidos",
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
            "A parte com o CID da OCI vem das medições de 26/10 (articulação), 27/10 (TC de pelve) e 02/11 (transvaginal). "
            "As OCI contratadas são as quantidades da planilha de aplicação de cada plano aprovado do IEV "
            "(estudo/normalizados/pt_ses_02 e pt_ses_04, planilha.csv); a coluna ao lado diz o plano e o item. A coluna "
            "Com o IEV diz quem atende a fila: só o plano 4, os dois juntos (a fila se divide), só o IEV, ou nenhum.",
            [40, 16, 11, 26, 30, 46, 12, 36, 12, 12, 12, 11, 11, 11, 11, 11])
    quem = ler_aba(original, "Quem atende o quê")
    cabecalho = ["Exame", "Código", "Situação", "Com o IEV", "Quem atende", "OCI e papel do exame, ou por que fica fora",
                 "OCI contratadas", "De onde vem o número de OCI (plano do IEV e item)", "Pedidos na fila",
                 "Reservados ao IEV", "Livres para o plano 4", *[f"Carteira {k}" for k in LETRAS]]
    formatos = [None, None, None, None, None, None, INTEIRO, None, INTEIRO, INTEIRO, INTEIRO, *[INTEIRO] * len(LETRAS)]
    cor_iev = {"só o plano 4": "E2EFDA", "juntos": "FFE699", "só o IEV": "F8CBAD", "o IEV atende só": "FCE4D6",
               "nenhum": "EDEDED"}
    for situacao, titulo in (("livre", "Livres: nenhum plano aprovado atende"),
                             ("parcial", "Parciais: uma parte da fila fica reservada ao IEV"),
                             ("fora", "Fora do plano 4")):
        linhas = []
        for r in quem:
            if r[2] != situacao:
                continue
            explica = r[4] if situacao != "fora" else (f"{r[4]} — {r[6]}" if r[4] and "partes moles" in r[4] else r[6])
            n = 10 + len(LETRAS)
            linhas.append([r[0].capitalize(), r[1], r[2], r[n + 1], r[3], explica, r[5], r[n], r[7], r[8], r[9],
                           *r[10:n]])
        a.subtitulo(titulo)
        inicio = a.linha + 1
        a.tabela(cabecalho, linhas, formatos, situacao_col=2,
                 total=["Total", None, None, None, None, None, None, None,
                        *[sum(l[j] or 0 for l in linhas) for j in range(8, 11 + len(LETRAS))]])
        for k, l in enumerate(linhas):
            cor = next((v for chave, v in cor_iev.items() if (l[3] or "").startswith(chave)), None)
            if cor:
                a.ws.cell(inicio + k, 4).fill = PatternFill("solid", fgColor=cor)
                a.ws.cell(inicio + k, 4).font = Font(bold=True)

    # 4. Rumo das filas: primeiro os 17 exames do plano, depois os outros códigos de imagem
    CLASSE_PLANA = {"capacidade da SES": "a SES dá conta: zera em até 8 meses no ritmo dela",
                    "zera devagar": "a SES zera, mas leva mais de 8 meses",
                    "esforço pontual": "caiu por mutirão; sem ele, a fila não zera",
                    "déficit persistente": "não zera: a SES agenda menos do que entra",
                    "inconclusivo": "incerto: os últimos meses diferem do resto do ano",
                    "sem série": "sem dados de movimento"}
    rumo_cod = {r[0]: r for r in ler_aba(original, "Rumo por código")}
    obs = {x["codigo"]: x["variacao_observada_mes"] for x in d["revisao"]["demanda"]}
    cod1 = sorted({i["codigo"] for i in cenarios[RECOMENDADA]}, key=lambda c: (c[:5], -rumo_cod[c][2]))
    a = Aba(wb, "Rumo das filas", "A fila de cada exame cresce ou cai?",
            "Movimento do código inteiro (todas as filas dele) nos 12 meses de out./2025 a set./2026. Entram = pedidos "
            "novos por mês; a SES agenda = agendamentos por mês; sobra = entram − a SES agenda. Sobra positiva, a fila "
            "cresce; negativa, a fila cai. A variação observada é a fila medida de verdade em 15/09 e em 02/11, nos nomes "
            "medidos nas duas datas. Os meses para zerar são projeção no ritmo dos 12 meses, e não previsão.",
            [40, 16, 12, 12, 12, 12, 14, 14, 50])
    a.subtitulo("Os 17 exames do plano")
    linhas = [[CURTO[c], c, rumo_cod[c][2], round(rumo_cod[c][5] / 12), round(rumo_cod[c][7] / 12), rumo_cod[c][12],
               obs.get(c), rumo_cod[c][16], CLASSE_PLANA.get(rumo_cod[c][19], rumo_cod[c][19])] for c in cod1]
    a.tabela(["Exame", "Código", "Fila de hoje (código)", "Entram por mês", "A SES agenda por mês", "Sobra por mês",
              "Variação observada por mês (15/09 a 02/11)", "Meses para zerar só com a SES", "O que acontece com a fila"],
             linhas, [None, None, INTEIRO, INTEIRO, INTEIRO, "#,##0;-#,##0", "#,##0;-#,##0", "0", None],
             total=["Total", None, *[sum(l[j] or 0 for l in linhas) for j in range(2, 7)], None, None])
    a.nota("Exemplo: na mama, entram 913 pedidos por mês e a SES agenda 815: sobram 99 por mês, e pela conta a fila "
           "cresceria. Mas a fila medida caiu 916 por mês entre 15/09 e 02/11, por causa dos mutirões de agosto e "
           "setembro. Quando as duas colunas discordam, vale olhar a aba Quem oferta.")
    a.subtitulo("Os outros códigos de imagem (fora da carteira 1)")
    linhas = []
    for c, r in rumo_cod.items():
        if c in cod1:
            continue
        linhas.append([modal_cod.get(c, ""), nome_exame.get(c, c), c, situar_codigo(c), r[2], "; ".join(motivos_cod[c]),
                       round(r[5] / 12), round(r[7] / 12), r[12], CLASSE_PLANA.get(r[19], r[19])])
    ordem = ("Ultrassom", "Tomografia", "Radiologia", "Ressonância", "Medicina nuclear", "Radiologia intervencionista", "outra")
    linhas.sort(key=lambda l: (ordem.index(l[0]) if l[0] in ordem else 9, -l[4]))
    a.larguras = [14, 40, 16, 22, 12, 50, 12, 12, 12, 46]
    for k, w in enumerate(a.larguras, 1):
        a.ws.column_dimensions[get_column_letter(k)].width = max(w, a.ws.column_dimensions[get_column_letter(k)].width or 0)
    a.tabela_excel("Rumo", ["Modalidade", "Exame", "Código", "Situação no plano 4", "Fila de hoje", "Por que fica fora",
                            "Entram por mês", "A SES agenda por mês", "Sobra por mês", "O que acontece com a fila"], linhas,
                   [None, None, None, None, INTEIRO, None, INTEIRO, INTEIRO, "#,##0;-#,##0", None],
                   somar=(4, 6, 7), barras=(4,), cores={3: COR_FILA}, congelar_col=1)

    # 5. Filas: primeiro as da carteira 1, por exame; depois as outras
    a = Aba(wb, "Filas", "Fila por fila",
            "As filas de imagem do Mapa Social de 02/11/2026, pelo nome exato. A fila são os três status pendentes; as "
            "devolvidas ficam de fora. Somar filas não dá pessoas: quem espera dois exames conta duas vezes.",
            [36, 52, 12, 12, 12, 12, 14, 12, 12, 12, 46])
    a.subtitulo("As filas da carteira 1, por exame")
    linhas = []
    for c in cod1:
        for f in sorted((f for f in filas if f["codigo"] == c), key=lambda f: -f["fila"]):
            k = (f["nome"], f["codigo"])
            na = base.get(k, {}).get(RECOMENDADA, 0)
            nv = novos.get(k, {}).get(RECOMENDADA, 0)
            if not (na or nv):
                continue
            s_, motivo, _ = sit_fila[k]
            linhas.append([CURTO[c], f["nome"], f["fila"], f["fila_viva"], f["pessoas"],
                           round(f["espera_mediana"]) if f["espera_mediana"] is not None else None, f["mais_antiga"],
                           na, nv or None, f["fila"] - na or None, motivo if f["fila"] > na else ""])
    a.tabela(["Exame", "Fila (nome exato)", "Pedidos na fila", "Fila viva (24 meses)", "Pessoas", "Espera mediana (dias)",
              "Pedido mais antigo", "Na carteira 1", "Pedidos novos na carteira 1", "Fica fora da carteira",
              "Por que fica fora"], linhas,
             [None, None, INTEIRO, INTEIRO, INTEIRO, INTEIRO, None, INTEIRO, INTEIRO, INTEIRO, None],
             total=["Total", None, *[sum(l[j] or 0 for l in linhas) for j in (2, 3, 4)], None, None,
                    *[sum(l[j] or 0 for l in linhas) for j in (7, 8, 9)], None])
    a.subtitulo("As outras filas de imagem")
    linhas = []
    for f in sorted(filas, key=lambda f: (ordem.index(f["modalidade"]) if f["modalidade"] in ordem else 9,
                                          f["codigo"], -f["fila"])):
        k = (f["nome"], f["codigo"])
        if base.get(k, {}).get(RECOMENDADA) or novos.get(k, {}).get(RECOMENDADA):
            continue
        s_, motivo, _ = sit_fila[k]
        outras = ", ".join(c for c in LETRAS[1:] if base.get(k, {}).get(c) or novos.get(k, {}).get(c)) or "—"
        linhas.append([f["modalidade"], nome_exame.get(f["codigo"], f["codigo"]), f["codigo"], f["nome"],
                       f["protocolo"] or "", f["fila"], f["fila_viva"], s_, motivo, outras])
    a.larguras = [14, 36, 16, 52, 18, 12, 12, 22, 46, 14]
    for k, w in enumerate(a.larguras, 1):
        a.ws.column_dimensions[get_column_letter(k)].width = max(w, a.ws.column_dimensions[get_column_letter(k)].width or 0)
    a.tabela_excel("Filas", ["Modalidade", "Exame", "Código", "Fila (nome exato)", "Protocolo", "Pedidos na fila",
                             "Fila viva", "Situação no plano 4", "Por que fica fora", "Outras carteiras que usam"], linhas,
                   [None, None, None, None, None, INTEIRO, INTEIRO, None, None, None],
                   somar=(5, 6), barras=(5,), cores={7: COR_FILA}, congelar_col=1)

    # 6. Viabilidade: só a carteira 1, com as parcelas do custo e o efeito da falta
    v, cu = d["revisao"]["viabilidade"], d["revisao"]["custos"]
    sala_h = cu["sala_mes"] / cu["horas_exame_mes"]
    a = Aba(wb, "Viabilidade", "Quanto sobra em cada exame da carteira 1",
            "Preço = Tabela SUS Candanga. Custo = premissas, sem cotação: a revisão de custos e a cotação dos médicos ficam "
            "para outra etapa (usuário, 02/11). A conta mostra as parcelas para cada uma poder ser trocada depois.",
            [40, 46, 12, 12, 10, 11, 11, 10, 12, 12, 12, 14, 14, 16])
    a.subtitulo("Como a conta é feita")
    a.tabela(["Parcela", "Como se calcula", "Valor"], [
        ["Sala com aparelho (ultrassom)", f"R$ {cu['sala_mes']:,.0f} por mês ÷ {cu['horas_exame_mes']} horas de exame no "
         "mês (8 por dia útil × 21 dias), × os minutos do exame".replace(",", "."), f"{reais(sala_h)} por hora"],
        ["Médico (ultrassom)", "R$ 100 por hora, × os minutos do exame", f"{reais(cu['medico_hora'])} por hora"],
        ["Insumo (ultrassom)", "gel, papel, impressão; hipótese", f"{reais(cu['insumo'])} por exame"],
        ["Tomografia", "preço por exame na clínica, com contraste (média cotada na rede de TC do ISHP)",
         f"{reais(cu['tc_clinica'])} por exame"],
        ["Falta não reposta", "no ultrassom, a sala e o médico ficam parados: o custo da hora se divide por menos exames "
         "(÷ 0,8 com 20%). Na TC, a clínica cobra por exame feito, e a falta não muda o custo", "—"],
        ["Sobra por hora de sala", "sobra por exame × 60 ÷ minutos; só no ultrassom, que ocupa a nossa sala", "—"],
    ], [None, None, None])
    a.subtitulo("Exame a exame")
    linhas = []
    for x in v:
        us_ = x["modalidade"] == "Ultrassom"
        linhas.append([CURTO[x["codigo"]], x["fila"], x["meta"], x["preco"], x["minutos"], x["sala"], x["medico"],
                       x["insumo"], x["custo"]["0.0"], x["margem"]["0.0"], x["margem_hora"]["0.0"] if us_ else None,
                       x["custo"]["0.2"], x["margem"]["0.2"], x["margem"]["0.0"] * x["meta"]])
    inicio = a.linha + 1
    a.tabela(["Exame", "Fila", "Exames na carteira 1", "Preço", "Minutos", "Sala", "Médico", "Insumo",
              "Custo, faltas repostas", "Sobra por exame", "Sobra por hora de sala", "Custo, 20% das faltas sem reposição",
              "Sobra por exame, 20% sem reposição", "Sobra na carteira, faltas repostas"], linhas,
             [None, None, INTEIRO, REAL, INTEIRO, REAL, REAL, REAL, REAL, REAL, REAL, REAL, REAL, REAL],
             total=["Total", None, sum(l[2] for l in linhas), None, None, None, None, None, None, None, None, None, None,
                    sum(l[13] for l in linhas)])
    for k, l in enumerate(linhas):
        for j, limite in ((10, 50), (12, 0)):
            if l[j] is not None and l[j] < limite:
                a.ws.cell(inicio + k, j + 1).fill = PatternFill("solid", fgColor="F8CBAD")
    finos = sorted({CURTO[x["codigo"]] for x in v if x["margem"]["0.2"] < 0})
    a.nota("Em vermelho: sobra por hora abaixo de R$ 50, ou sobra negativa com 20% das faltas sem reposição. "
           f"Negativa com 20% sem reposição: {', '.join(finos) or 'nenhum'}. O Doppler de membros (40 minutos) e a mama "
           "ficam com a sobra mais fina. Todos os exames da carteira têm sobra positiva com as faltas repostas.")
    a.subtitulo("O que ainda falta para a conta ficar precisa (etapa de custos)")
    a.tabela(["Item", "O quê"], [
        ["Médico", "a cotação real e a forma de pagamento (por hora, por plantão ou por exame); por exame, a falta não "
                   "pesa no custo do médico"],
        ["Sala e aparelho", "o aluguel real de cada clínica e quantas horas por mês ela fica com o projeto"],
        ["Insumo", "a cotação do gel, do papel e da impressão do laudo"],
        ["Laudo, encargos e gestão", "separar o laudo, os encargos e a parte da gestão que cabe a cada exame"],
        ["Tomografia", "o preço por clínica, e não a média da rede"],
        ["Tempo", "o tempo real por exame de cada clínica, que pode ser menor que o do CBR (L-006)"],
    ], [None, None])

    # 7. Quem oferta
    a = Aba(wb, "Quem oferta", "Quem sustenta a oferta em cada código",
            "Só os 17 códigos da carteira 1 (Mapa Social, 02/11). Agendamentos por unidade que executa o exame, pelo mês "
            "em que o exame acontece. O painel dá a unidade por código, e não por nome de fila: na TC, os números incluem "
            "a emergência e a angio coronária do mesmo código. Unidade que sobe e volta a zero é mutirão; contratado e "
            "URD estáveis são oferta que fica. Novembro ainda vai receber agendamentos.",
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
        ws.sheet_properties.tabColor = AZUL if ws.title in ("Resumo", "Enquadramento", "Capacidade por polo", "Encaminhamento SES", "Painel", "Carteiras por código", "Rumo das filas", "Filas", "Viabilidade") else "A6A6A6"
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
