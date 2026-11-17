"""Aplica a v24 sobre a v23 (versoes/plano_v23_20261008.docx, descompactada).

uso: aplicar_v24.py <docx_descompactado> limpo|marcado A|B

- seis polos, um por Regiao de Saude, com as Regioes Central e Centro-Sul num polo comum;
- o quadro de gestao do cenario 3 (D-005): Direcao Executiva, tres coordenacoes, tres supervisores de polo, oito
  operadores de registro (quatro no pre-exame, quatro no pos-exame) e seis assistentes administrativos (um por polo,
  documentacao do atendimento e da prestacao de contas);
- todos os numeros recalculados (calculo_v24.py, v24.json);
- A: tomografia nos seis polos, um tomografo por polo, com o excedente da Sudoeste absorvido no polo da Oeste;
- B: tomografia em rede, sem numero de tomografos nem distribuicao por polo: so a carga e as horas no total.
"""
import sys, os, json, math
from decimal import Decimal as D
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v20"))
from docxlib import Doc, q

pasta, modo, var = sys.argv[1], sys.argv[2], sys.argv[3]
assert var in ("A", "B")
REDE = var == "B"
V = json.load(open(os.path.join(AQUI, "v24.json")))
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))


def n(x):
    return f"{int(x):,}".replace(",", ".")


def r(x):
    s = f"{D(str(x)).quantize(D('0.01')):,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def dec(x, k):
    return f"{x:.{k}f}".replace(".", ",")


def lista(itens):
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def set_row(tbl, ri, vals, novos=()):
    cs = d.cells(d.rows(tbl)[ri])
    for ci, v in enumerate(vals):
        if v is None:
            continue
        d.set_cell(cs[ci], v, novo=ci in novos)


def cel(tbl, ri, ci):
    return d.cells(d.rows(tbl)[ri])[ci].find(q("p"))


def remover_linha(tbl, ri, comeca):
    linha = d.rows(tbl)[ri]
    assert d.text(d.cells(linha)[0].find(q("p"))).startswith(comeca), d.text(d.cells(linha)[0].find(q("p")))
    if d.marcado:
        for run in d.runs_all(linha):
            d.mark_old(run)
    else:
        linha.getparent().remove(linha)


def trocar(p, novo):
    d.replace(p, d.text(p), novo)


ORD = V["ORD"]                      # Oeste, Sudoeste, Norte, Leste, Central e Centro-Sul, Sul
CCS = "Central e Centro-Sul"
P = V["polos"]
M, DIAS, HM = V["meses"], V["dias"], V["h_medico"]
TOTAL, US, TC = V["total"], V["us_total"], V["tc_total"]
APOIO, GLOB, PROD = D(V["apoio"]), D(V["global"]), D(V["producao"])
qc, HUS, HTC = V["qc"], V["hus"], V["htc"]
CARGA = V["carga_tc"]
UNIT = {"02.05.02.009-7": D("99.94"), "02.05.02.018-6": D("99.94"), "02.05.01.004-0": D("100.18"),
        "02.05.02.004-6": D("100.18"), "02.05.02.005-4": D("99.94"), "02.05.02.012-7": D("99.94"),
        "02.05.02.010-0": D("99.94"), "02.05.02.003-8": D("99.94"), "02.06.03.001-0": D("299.44"),
        "02.06.03.003-7": D("299.44"), "02.06.02.003-1": D("300.10")}
NA = {x: ("nas Regiões Central e Centro-Sul" if x == CCS else f"na Região {x}") for x in ORD}
DO_POLO = {x: ("O polo das Regiões Central e Centro-Sul" if x == CCS else f"O polo da Região {x}") for x in ORD}
EXT_F = {1: "uma", 2: "duas", 3: "três", 4: "quatro", 5: "cinco", 6: "seis", 7: "sete"}
EXT_N = {6: "seis", 8: "oito", 20: "vinte"}
POSTO = {p: (qt, D(v), D(tt)) for p, qt, v, _, _, tt in V["quadro"]}
PER = V["periodos"]
salas = {x: P[x]["salas"] for x in ORD}
SALAS = sum(salas.values())
assert SALAS == 20
dia_us_soma = sum(P[x]["dia_us"] for x in ORD)
dia_tc_soma = sum(P[x]["dia_tc"] for x in ORD)
dia_tc_rede = math.ceil(TC / DIAS)
mes_tc_rede = math.ceil(TC / M)
pct = {x: f"{(P[x]['us'] if REDE else P[x]['tot']) / TOTAL * 100:.2f}%".replace(".", ",") for x in ORD}
pct_tc = f"{TC / TOTAL * 100:.2f}%".replace(".", ",")

T = d.tables()

# ================= 1. Informacoes iniciais e 1.9 =================
d.replace(d.find("valor global do plano, dentro do recurso disponível"), "R$ 11.592.666,22", f"R$ {r(GLOB)}")
d.sub("Dez polos nas Regiões de Saúde do Distrito Federal", "Dez polos", "Seis polos")

# ================= 2.2 composicao =================
d.sub("O objeto é a realização de 79.373 exames", "79.373", n(TOTAL))
t2 = T[2]
for ri, tr in enumerate(d.rows(t2)[1:12], start=1):
    cod = d.text(d.cells(tr)[0].find(q("p")))
    set_row(t2, ri, [None, None, n(qc[cod])])
set_row(t2, 12, [None, None, n(TOTAL)])
p = d.find("São 65.687 exames de ultrassonografia")
d.replace(p, "65.687", n(US))
d.replace(p, "13.686", n(TC))

# ================= 3.1 a fila =================
p = d.find("A parceria resolve a totalidade das 78.572 solicitações")
d.replace(p, "atende mais 801", f"atende mais {n(V['acrescimo'])}")
d.replace(p, "79.373 exames ao todo", f"{n(TOTAL)} exames ao todo")
for ri, val in [(2, f"R$ {r(APOIO)}"), (3, f"R$ {r(V['envelope'])}"), (4, f"{n(TOTAL)} exames"),
                (5, f"R$ {r(PROD)}"), (6, f"R$ {r(GLOB)}"), (7, f"R$ {r(V['sobra'])}")]:
    set_row(T[4], ri, [None, val])

# ================= 3.4 distribuicao entre os polos =================
p = d.find("A participação dos polos de cada Região corresponde à participação dessa Região")
if REDE:
    trocar(p, "A ultrassonografia se distribui entre os polos na proporção das solicitações de ultrassonografia "
           "originadas nas Regiões de Saúde que cada um atende, e a tomografia computadorizada se distribui em rede, na "
           "forma da subseção 4.2. A participação é a de cada parcela no total de exames.")
else:
    d.replace(p, "A participação dos polos de cada Região corresponde à participação dessa Região",
              "A participação de cada polo corresponde à participação das Regiões de Saúde que ele atende")
t5 = T[5]
for i, x in enumerate(ORD, start=1):
    set_row(t5, i, [x, "1", pct[x], n(P[x]["us"] if REDE else P[x]["tot"])])
if REDE:
    d.clone_row(t5, 6)
    set_row(t5, 7, ["tomografia computadorizada, na rede dos polos", "", pct_tc, n(TC)], novos={0, 1, 2, 3})
    set_row(t5, 8, [None, "6", None, n(TOTAL)])
else:
    set_row(t5, 7, [None, "6", None, n(TOTAL)])

# ================= 3.12 e 4.2 =================
d.sub("compatível com a implantação dos dez polos no mês 1", "dez polos", "seis polos")
trocar(d.find("A execução ocorre em dez polos, distribuídos de modo que"),
       "A execução ocorre em seis polos, um em cada Região de Saúde do Distrito Federal, com as Regiões Central e "
       "Centro-Sul atendidas por um polo comum, de modo que as sete Regiões tenham polo de referência:")
t7 = T[7]
for i, x in enumerate(ORD, start=1):
    set_row(t7, i, [x, "1"])
set_row(t7, 7, [None, "6"])
p = d.find("Os exames são realizados na capacidade instalada do proponente. Os dez polos")
if REDE:
    trocar(p, "Os exames são realizados na capacidade instalada do proponente. Os seis polos realizam ultrassonografia. "
           "A tomografia computadorizada se organiza em rede entre os polos do projeto: o proponente libera as vagas de "
           "tomografia nos tomógrafos da rede, e a regulação da SES-DF as ocupa (subseção 7.3).")
else:
    trocar(p, "Os exames são realizados na capacidade instalada do proponente. Os seis polos realizam ultrassonografia "
           "e tomografia computadorizada (subseção 7.3).")
p = d.find("O usuário é encaminhado ao polo de referência do seu domicílio. A redistribuição entre polos")
if REDE:
    trocar(p, "Na ultrassonografia, o usuário é encaminhado ao polo de referência do seu domicílio; na tomografia, à "
           "vaga que a regulação lhe atribui na rede. A redistribuição entre polos, quando necessária para cumprir a "
           "curva de produção, é atribuição da Coordenação Operacional, na forma da subseção 4.13.")
else:
    trocar(p, "O usuário é encaminhado ao polo de referência do seu domicílio. Na tomografia, o polo da Região Oeste "
           "recebe também a parte da carga da Região Sudoeste que excede a capacidade de um equipamento (subseção 7.3). "
           "A redistribuição entre polos, quando necessária para cumprir a curva de produção, é atribuição da "
           "Coordenação Operacional, na forma da subseção 4.13.")

# ================= 4.3 etapas =================
t8 = T[8]
set_row(t8, 2, [None, None, "Operador de registro de sistemas, no pré-exame"])
set_row(t8, 3, [None, None, "Operador de registro de sistemas, no pré-exame"])
set_row(t8, 9, [None, None, "Operador de registro de sistemas, no pós-exame"])

# ================= 4.8 contraste =================
d.sub("são 12.958 dos 13.686 exames de tomografia", "12.958 dos 13.686", f"{n(V['contraste'])} dos {n(TC)}")

# ================= 4.13 equipe de gestao e apoio =================
t9 = T[9]
d.clone_row(t9, 2)                       # Coordenacao Assistencial, depois da Operacional
d.clone_row(t9, 4)                       # Supervisao de Polo, depois da Adm. e Financeira
d.clone_row(t9, 6)                       # Operador do pos-exame
set_row(t9, 2, [None, None, None, "funcionamento dos polos e das agendas, redistribuição de agenda entre polos (4.2) e "
                "supervisão de polo"])
set_row(t9, 3, ["1", "Coordenação Assistencial", f"{M} meses",
                "conformidade dos protocolos de preparo, contraste, realização, laudo e entrega nos polos (4.7 a 4.11), "
                "com os responsáveis técnicos dos polos (4.15 e 4.16)"], novos={0, 1, 2, 3})
set_row(t9, 5, ["3", "Supervisão de Polo Assistencial", f"{M} meses",
                "acompanhamento presencial de dois polos cada: funcionamento, fluxo de usuários, agenda no local e "
                "ocorrências (4.7 a 4.9)"], novos={0, 1, 2, 3})
set_row(t9, 6, ["4", "Operador de registro de sistemas — pré-exame", None, "4.5, 4.6 e 4.12"])
set_row(t9, 7, ["4", "Operador de registro de sistemas — pós-exame", f"{M} meses", "9.2"], novos={0, 1, 2, 3})
set_row(t9, 8, ["6", None, None, "documentação do atendimento e da prestação de contas de cada polo (4.8, 4.9 e 7.6)"])
trocar(d.find("Os dez operadores de registro e os dez assistentes administrativos são um de cada por polo"),
       "Os seis assistentes administrativos são um por polo:")
t10 = T[10]
set_row(t10, 0, [None] + ORD)
set_row(t10, 2, [None] + ["1"] * 6 + ["6"])
remover_linha(t10, 3, "por Região")
remover_linha(t10, 1, "Operador")
trocar(d.find("A direção e as duas coordenações são únicas para os dez polos"),
       "A direção, as três coordenações e os oito operadores de registro atuam de forma centralizada, para os seis "
       "polos, e não se lotam em nenhum deles. Os três supervisores de polo acompanham presencialmente dois polos cada, "
       "com atuação operacional e de apoio local, sem atribuição de coordenação, de gestão de equipe ou de decisão "
       "assistencial.")
trocar(d.find("A Coordenação Operacional redistribui a carga de contato"),
       "A Coordenação Operacional distribui entre os operadores a carga de contato com os usuários agendados e de "
       "registro dos seis polos ao longo da vigência, conforme a execução de cada um — trabalho que não depende de o "
       "posto estar fisicamente no polo.")
p = d.find("integra a capacidade instalada do proponente e é remunerada pelo valor unitário do exame. O quadro")
d.replace(p, "na forma da subseção 4.15.", "na forma da subseção 4.15. A Coordenação Assistencial coordena os polos; "
          "a execução e a responsabilidade técnica em cada um são do responsável técnico médico do polo, remunerado pelo "
          "valor unitário do exame.")

# ================= 4.15 equipe assistencial =================
t11 = T[11]
set_row(t11, 0, [None, None] + ORD)
mus = {x: P[x]["medicos_us"] for x in ORD}
set_row(t11, 1, [None, str(sum(mus.values()))] + [str(mus[x]) for x in ORD])
d.replace(cel(t11, 1, 8), "salas: 1, 6, 5, 2, 5 e 2", "salas: " + lista([str(salas[x]) for x in ORD]))
c = cel(t11, 2, 8)
velho = "horas de sala da tomografia 353, 1.609, 1.117, 503, 612 e 307 ÷ 1.200 h no período (0,29; 1,34; 0,93; 0,42; 0,51; 0,26)"
if REDE:
    set_row(t11, 2, [None, f"no mínimo {V['radiologistas_rede']}"] + [""] * 6)
    d.replace(c, velho, f"horas de tomógrafo da rede ({n(HTC)}) ÷ {n(HM)} h no período ({dec(HTC / HM, 2)})")
else:
    rad = {x: P[x]["radiologistas"] for x in ORD}
    set_row(t11, 2, [None, str(sum(rad.values()))] + [str(rad[x]) for x in ORD])
    d.replace(c, velho, "horas de sala da tomografia " + lista([n(P[x]["htc"]) for x in ORD]) + f" ÷ {n(HM)} h no "
              "período (" + "; ".join(dec(P[x]["htc"] / HM, 2) for x in ORD) + ")")
set_row(t11, 3, [None, "6 por dia útil"] + ["1"] * 6)
set_row(t11, 4, [None, "6"] + ["1"] * 6)
if REDE:
    set_row(t11, 5, [None, "3 por tomógrafo"] + [""] * 6)
    set_row(t11, 6, [None, "2 por tomógrafo"] + [""] * 6)
else:
    set_row(t11, 5, [None, "18"] + ["3"] * 6)
    set_row(t11, 6, [None, "12"] + ["2"] * 6)
set_row(t11, 7, [None, "12"] + ["2"] * 6)
p = d.find("Ultrassonografia: as 24.321 horas de sala")
d.replace(p, "24.321 horas de sala (1.322 na Região Oeste, 7.936 na Região Sudoeste, 5.861 nas Regiões Norte e Leste, "
             "1.269 na Região Central, 5.530 na Região Sul e 2.403 na Região Centro-Sul)",
          f"{n(HUS)} horas de sala (" + lista([f"{n(P[x]['hus'])} {NA[x]}" for x in ORD]) + ")")


def med(x, i):
    k, h = mus[x], P[x]["hus"]
    base = f"{k} {'médico' if k == 1 else 'médicos'} {NA[x]}" if i == 0 else f"{k} {NA[x]}"
    return f"{base} ({n(h)} ÷ {n(HM)} = {dec(h / HM, 1)})"


d.replace(p, "2 médicos na Região Oeste (1.322 ÷ 1.200 = 1,1), 7 na Região Sudoeste (7.936 ÷ 1.200 = 6,6), 5 nas "
             "Regiões Norte e Leste (5.861 ÷ 1.200 = 4,9), 2 na Região Central (1.269 ÷ 1.200 = 1,1), 5 na Região Sul "
             "(5.530 ÷ 1.200 = 4,6) e 3 na Região Centro-Sul (2.403 ÷ 1.200 = 2,0), 24 no total, sempre em número igual "
             "ou superior ao de salas (1, 6, 5, 2, 5 e 2)",
          lista([med(x, i) for i, x in enumerate(ORD)]) + f", {sum(mus.values())} no total, sempre em número igual ou "
          "superior ao de salas (" + lista([str(salas[x]) for x in ORD]) + ")")
if REDE:
    d.replace(p, "logo no mínimo 3 técnicos por tomógrafo e 21 nos sete tomógrafos,",
              "logo no mínimo 3 técnicos por tomógrafo da rede,")
else:
    d.replace(p, "e 21 nos sete tomógrafos", "e 18 nos seis tomógrafos")

# ================= 5 objetivos =================
d.sub("mediante a realização de 79.373 exames", "79.373", n(TOTAL))
t12 = T[12]
d.replace(d.find("coordenar dez polos de execução", within=t12), "dez polos", "seis polos")
d.replace(d.find("10 polos em operação por 8 meses", within=t12), "10 polos", "6 polos")
d.replace(d.find("79.373 vagas", within=t12), "79.373", n(TOTAL))
d.replace(d.find("79.373 exames registrados", within=t12), "79.373", n(TOTAL))
d.replace(d.find("65.687 exames", within=t12), "65.687", n(US))
d.replace(d.find("13.686 exames", within=t12), "13.686", n(TC))

# ================= 6 metas =================
t13 = T[13]
d.replace(d.find("10 polos em operação a partir do mês 1", within=t13), "10 polos", "6 polos")
d.replace(d.find("79.373 vagas disponibilizadas", within=t13), "79.373", n(TOTAL))
d.replace(d.find("79.373 exames registrados", within=t13), "79.373", n(TOTAL))
d.replace(d.find("65.687 exames", within=t13), "65.687", n(US))
d.replace(d.find("13.686 exames", within=t13), "13.686", n(TC))
p = d.find("As Metas 4 e 5 se decompõem por Região")
if REDE:
    trocar(p, "A Meta 4 se decompõe por polo, na proporção da subseção 3.4 — " + lista(
        [f"{n(P[x]['us'])} exames {NA[x]}" if i == 0 else f"{n(P[x]['us'])} {NA[x]}" for i, x in enumerate(ORD)]) +
        " —, e a Meta 5 se executa na rede de tomografia da subseção 4.2. As duas se decompõem por procedimento, no "
        "quantitativo da subseção 2.2, e por período, na curva da subseção 7.2.")
else:
    trocar(p, "As Metas 4 e 5 se decompõem por polo, na proporção da subseção 3.4 — " + lista(
        [f"{n(P[x]['tot'])} exames {NA[x]}" if i == 0 else f"{n(P[x]['tot'])} {NA[x]}" for i, x in enumerate(ORD)]) +
        " —, por procedimento, no quantitativo da subseção 2.2, e por período, na curva da subseção 7.2.")

# ================= 7.1 etapas e 7.2 curva =================
d.replace(d.find("publicação das agendas dos dez polos", within=T[15]), "dez polos", "seis polos")
t16 = T[16]
for i in range(3):
    set_row(t16, i + 1, [None, None, n(V["curva"][i])])
set_row(t16, 4, [None, None, n(TOTAL)])

# ================= 7.3 capacidade =================
ip = V["pico_periodo"]
p = d.find("A produção do período de maior carga")
d.replace(p, f"com 19.849 exames em 42 dias úteis — corresponde a 473",
          f"com {n(V['curva'][ip])} exames em {V['dias_periodo'][ip]} dias úteis — corresponde a {V['pico_dia']}")
if REDE:
    d.replace(p, "distribuídos entre as Regiões na proporção da subseção 3.4",
              "distribuídos entre os polos, na ultrassonografia, e a rede, na tomografia (subseções 3.4 e 4.2)")
else:
    d.replace(p, "distribuídos entre as Regiões", "distribuídos entre os polos")
d.sub("A execução do objeto requer 28.822 horas de sala", "28.822 horas de sala no período — 24.321 de "
      "ultrassonografia e 4.501", f"{n(HUS + HTC)} horas de sala no período — {n(HUS)} de ultrassonografia e {n(HTC)}")
d.sub("os quantitativos diários e os equipamentos de cada Região", "de cada Região", "de cada polo")
t17 = T[17]
set_row(t17, 0, [None, None] + ORD)
set_row(t17, 1, [None, "6"] + ["1"] * 6)
VAZIO = [""] * 6
if REDE:
    set_row(t17, 2, [None, n(TOTAL)] + VAZIO)
    d.replace(cel(t17, 2, 8), "distribuição da subseção 3.4", "soma da ultrassonografia e da tomografia")
else:
    set_row(t17, 2, [None, n(TOTAL)] + [n(P[x]["tot"]) for x in ORD])
set_row(t17, 3, [None, n(US)] + [n(P[x]["us"]) for x in ORD])
set_row(t17, 5, [None, n(sum(P[x]["mes_us"] for x in ORD))] + [n(P[x]["mes_us"]) for x in ORD])
set_row(t17, 9, [None, n(dia_us_soma)] + [n(P[x]["dia_us"]) for x in ORD])
set_row(t17, 11, [None, str(SALAS)] + [str(salas[x]) for x in ORD])
set_row(t17, 12, [None, None] + [str(P[x]["por_sala"]) for x in ORD])
set_row(t17, 13, [None, n(HUS)] + [n(P[x]["hus"]) for x in ORD])
d.replace(cel(t17, 11, 8), "da Região no horário de funcionamento, no mínimo uma por polo,",
          "do polo no horário de funcionamento, no mínimo uma,")
d.replace(cel(t17, 12, 8), "salas da Região", "salas do polo")
d.replace(cel(t17, 13, 8), "exames da Região", "exames do polo")
set_row(t17, 16, ["Postos de gestão e apoio lotados no polo", "6"] + ["1"] * 6)
if REDE:
    set_row(t17, 4, [None, n(TC)] + VAZIO)
    d.replace(cel(t17, 4, 8), "idem", "rede de tomografia: a regulação distribui as vagas entre os tomógrafos (4.2)")
    set_row(t17, 6, [None, n(mes_tc_rede)] + VAZIO)
    d.replace(cel(t17, 6, 8), "idem; total: soma dos polos", f"exames do período ÷ {M} meses")
    set_row(t17, 10, [None, n(dia_tc_rede)] + VAZIO)
    d.replace(cel(t17, 10, 8), "idem; total: soma dos polos", f"exames do período ÷ {DIAS} dias úteis")
    set_row(t17, 14, ["Carga de tomografia, em equipamentos", dec(CARGA, 2)] + VAZIO)
    trocar(cel(t17, 14, 8), f"horas de tomógrafo ÷ ({DIAS} dias úteis × 10 horas × 80% de ocupação); rede de "
           "tomografia (4.2)")
    set_row(t17, 15, [None, n(HTC)] + VAZIO)
    d.replace(cel(t17, 15, 8), "exames da Região", "exames de tomografia")
else:
    set_row(t17, 4, [None, n(TC)] + [n(P[x]["tc"]) for x in ORD])
    set_row(t17, 6, [None, n(sum(P[x]["mes_tc"] for x in ORD))] + [n(P[x]["mes_tc"]) for x in ORD])
    set_row(t17, 10, [None, n(dia_tc_soma)] + [n(P[x]["dia_tc"]) for x in ORD])
    set_row(t17, 14, [None, "6"] + ["1"] * 6)
    trocar(cel(t17, 14, 8), "um por polo; a carga da Região Sudoeste que excede um equipamento é absorvida no polo da "
           "Região Oeste (4.2)")
    set_row(t17, 15, [None, n(HTC)] + [n(P[x]["htc"]) for x in ORD])
    d.replace(cel(t17, 15, 8), "exames da Região", "exames do polo")
p = d.find("A Região Oeste realiza, por dia útil,")


def frase(x, i):
    s = salas[x]
    us_txt = f"{P[x]['dia_us']} exames de ultrassonografia em {EXT_F[s]} {'sala' if s == 1 else 'salas'}"
    if REDE:
        return f"{DO_POLO[x]} realiza{', por dia útil,' if i == 0 else ''} {us_txt}."
    tc_txt = f"{P[x]['dia_tc']} de tomografia computadorizada" if i == 0 else f"{P[x]['dia_tc']} de tomografia"
    return f"{DO_POLO[x]} realiza{', por dia útil,' if i == 0 else ''} {us_txt} e {tc_txt}."


fim = (f" A rede de tomografia realiza {dia_tc_rede} exames por dia útil." if REDE else "") + \
    " Os seis polos funcionam dez horas por dia útil, e cada um tem um posto de gestão e apoio lotado."
trocar(p, " ".join(frase(x, i) for i, x in enumerate(ORD)) + fim)
p = d.find("A soma das Regiões, de 395 exames")
if REDE:
    assert dia_us_soma + dia_tc_rede > V["pico_dia"]
    trocar(p, f"A soma dos polos, de {dia_us_soma} exames de ultrassonografia por dia útil, com os {dia_tc_rede} de "
           f"tomografia da rede, excede os {V['pico_dia']} do período de maior carga porque a capacidade é arredondada "
           "para cima. A folga que o arredondamento produz absorve exame que se estende e manutenção.")
else:
    assert dia_us_soma + dia_tc_soma > V["pico_dia"]
    trocar(p, f"A soma dos polos, de {dia_us_soma} exames de ultrassonografia e {dia_tc_soma} de tomografia por dia "
           f"útil, excede os {V['pico_dia']} do período de maior carga porque a capacidade de cada polo é arredondada "
           "para cima. A folga que o arredondamento produz absorve exame que se estende e manutenção.")
trocar(d.find("Aos vinte postos lotados nas Regiões"),
       "Aos seis postos lotados nos polos somam-se os três supervisores de polo, que acompanham dois polos cada, e a "
       "direção, as três coordenações e os oito operadores de registro, que atuam de forma centralizada, na forma da "
       "subseção 4.13, e a Assessoria de Prestação de Contas, que é serviço contratado.")
p = d.find("A tomografia em pelo menos um polo de cada Região mantém o exame perto")
if REDE:
    trocar(p, f"A rede de tomografia é dimensionada sobre a carga do conjunto, de {dec(CARGA, 2)} equipamentos em turno "
           "de dez horas, com folga de 20%. O proponente libera as vagas nos tomógrafos da rede, a regulação da SES-DF "
           "as ocupa, e a folga do conjunto absorve a manutenção de cada equipamento.")
else:
    so, oe = P["Sudoeste"]["carga_tc"], P["Oeste"]["carga_tc"]
    trocar(p, "Um tomógrafo em cada polo mantém o exame perto do domicílio do usuário. A carga da Região Sudoeste, de "
           f"{dec(so, 2)} equipamento, excede a capacidade de um tomógrafo; o proponente libera no polo da Região Oeste, "
           f"vizinho e com carga de {dec(oe, 2)}, a agenda que absorve o excedente. A folga do conjunto absorve a "
           "manutenção de cada equipamento.")

# ================= 7.5 parcelas =================
t18 = T[18]
for i in range(3):
    set_row(t18, i + 1, [None, None, n(V["curva"][i]), r(V["prod_b"][i]), r(V["apoio_periodo"][i]), r(V["parcelas"][i])])
set_row(t18, 4, [None, None, n(TOTAL), r(PROD), r(APOIO), r(GLOB)])

# ================= 7.8 e 7.9 riscos =================
t19 = T[19]
d.replace(d.find("Capacidade instalada insuficiente para o ritmo de 473", within=t19), "473", str(V["pico_dia"]))
d.replace(d.find("redistribuição da agenda entre os dez polos", within=t19), "dez polos", "seis polos")
d.replace(d.find("quantitativo pactuado de 79.373 inclui 801", within=t19), "79.373 inclui 801",
          f"{n(TOTAL)} inclui {n(V['acrescimo'])}")
p = d.find("sete equipamentos para uma carga de 2,68", within=t19)
if REDE:
    d.replace(p, "sete equipamentos para uma carga de 2,68, na forma da subseção 7.3, com redistribuição da agenda de "
                 "tomografia entre os polos no mesmo dia",
              f"capacidade da rede de tomografia dimensionada sobre a carga de {dec(CARGA, 2)} equipamentos, com a folga "
              "da subseção 7.3, e redistribuição da agenda entre os tomógrafos da rede no mesmo dia")
else:
    d.replace(p, "sete equipamentos para uma carga de 2,68", f"seis equipamentos, um por polo, para uma carga de "
              f"{dec(CARGA, 2)}")
d.replace(d.find("operador de registro dedicado em cada polo, que lança no mesmo dia do exame", within=t19),
          "operador de registro dedicado em cada polo, que lança", "operadores de registro dedicados ao pós-exame, que lançam")
p = d.find("A meta de 79.373 exames em oito meses exige vinte e uma salas")
if REDE:
    d.replace(p, "79.373 exames em oito meses exige vinte e uma salas de ultrassonografia e sete tomógrafos em turno de dez "
                 "horas", f"{n(TOTAL)} exames em oito meses exige vinte salas de ultrassonografia em turno de dez horas e "
              "a capacidade de tomografia da subseção 7.3")
else:
    d.replace(p, "79.373 exames em oito meses exige vinte e uma salas de ultrassonografia e sete tomógrafos",
              f"{n(TOTAL)} exames em oito meses exige vinte salas de ultrassonografia e seis tomógrafos")
d.sub("é insumo de 12.958 dos 13.686 exames", "12.958 dos 13.686", f"{n(V['contraste'])} dos {n(TC)}")

# ================= 8.2 planilha (de baixo para cima, para os indices das linhas de cima nao mudarem) =================
t21 = T[21]
q_dir, v_dir, t_dir = POSTO["Direção Executiva de Projeto"]
q_op, v_op, t_op = POSTO["Coordenação Operacional"]
q_ca, v_ca, t_ca = POSTO["Coordenação Assistencial"]
q_sp, v_sp, t_sp = POSTO["Supervisão de Polo Assistencial"]
q_as, v_as, t_as = POSTO["Assistente Administrativo"]
q_or, v_or, t_or = POSTO["Operador de registro de sistemas"]
q_af, v_af, t_af = POSTO["Coordenação Administrativa e Financeira"]
q_ac, v_ac, t_ac = POSTO["Assessoria de Prestação de Contas"]
assert q_or == 8 and q_as == 6 and q_sp == 3
t_pre = t_pos = t_or / 2
# Meta 6: Coordenacao Adm. e Financeira, Assessoria e o Assistente Administrativo (novo)
d.clone_row(t21, 34)
set_row(t21, 33, [None, None, None, None, None, None, r(v_af), r(t_af)])
set_row(t21, 35, ["6.1.3", "Assistente Administrativo — documentação do atendimento e da prestação de contas de cada polo",
                  "4.8 · 4.9 · 7.6", "posto", str(q_as), f"{M} meses", r(v_as), r(t_as)], novos=set(range(8)))
m6 = t_af + t_ac + t_as
set_row(t21, 36, [None, None, None, None, str(1 + 1 + q_as), None, None, r(m6)])
# Meta 5 e Meta 4
m5 = D(0)
for ri in range(27, 30):
    cod = [c for c in qc if c in d.text(cel(t21, ri, 1))][0]
    v = qc[cod] * UNIT[cod]
    m5 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 30, [None, None, None, None, n(TC), None, None, r(m5)])
m4 = D(0)
for ri in range(16, 24):
    cod = [c for c in qc if c in d.text(cel(t21, ri, 1))][0]
    v = qc[cod] * UNIT[cod]
    m4 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 24, [None, None, None, None, n(US), None, None, r(m4)])
# Meta 3: operador do pos-exame; Meta 2: operador do pre-exame (no lugar do assistente)
set_row(t21, 12, [None, "Operador de registro de sistemas — pós-exame: registro no TrakCare e na Autorização de "
                  "Procedimento Ambulatorial", None, None, str(q_or // 2), None, None, r(t_pos)])
set_row(t21, 13, [None, None, None, None, str(q_or // 2), None, None, r(t_pos)])
set_row(t21, 8, [None, "Operador de registro de sistemas — pré-exame: agenda no SISREG, contato com os usuários "
                 "agendados, confirmação e busca ativa", None, None, str(q_or // 2), None, r(v_or), r(t_pre)])
set_row(t21, 9, [None, None, None, None, str(q_or // 2), None, None, r(t_pre)])
# Meta 1: Coordenacao Operacional com o preco novo, Coordenacao Assistencial e Supervisao de Polo (novas)
set_row(t21, 4, [None, None, None, None, None, None, r(v_op), r(t_op)])
d.clone_row(t21, 4)
d.clone_row(t21, 5)
set_row(t21, 5, ["1.1.3", "Coordenação Assistencial", "4.7 a 4.11 · 4.13", "posto", str(q_ca), f"{M} meses", r(v_ca),
                 r(t_ca)], novos=set(range(8)))
set_row(t21, 6, ["1.1.4", "Supervisão de Polo Assistencial", "4.13", "posto", str(q_sp), f"{M} meses", r(v_sp), r(t_sp)],
        novos=set(range(8)))
m1 = t_dir + t_op + t_ca + t_sp
set_row(t21, 7, [None, None, None, None, str(q_dir + q_op + q_ca + q_sp), None, None, r(m1)])
total_geral = m1 + t_pre + t_pos + m4 + m5 + m6
assert total_geral == GLOB, (total_geral, GLOB)
assert m4 + m5 == PROD and m1 + t_pre + t_pos + m6 == APOIO
set_row(t21, 39, [None, None, None, None, None, None, None, r(total_geral)])

# ================= 8.3 consolidacao =================
t22 = T[22]
for ri, v in [(1, m1), (2, t_pre), (3, t_pos), (4, m4), (5, m5), (6, m6), (7, total_geral)]:
    set_row(t22, ri, [None, r(v)])

# ================= 9.2 registro =================
trocar(d.find("O registro é feito no polo, no mesmo dia do exame, pelo operador de registro de sistemas ali lotado."),
       "O registro é feito no mesmo dia do exame pelos operadores de registro de sistemas do pós-exame, que atuam de "
       "forma centralizada para os seis polos, com acesso aos sistemas oficiais pelo meio corporativo da subseção 9.3.")

d.save()
print(f"{var} {modo}: {len(d.log)} trocas de texto; {n(TOTAL)} exames; global {r(GLOB)}; apoio {r(APOIO)}")
