"""Aplica a v25 sobre a v24A (versoes/plano_v24a_20261020.docx, descompactada).

uso: aplicar_v25.py <docx_descompactado> limpo|marcado A|B

Validado pelo usuario em 21/10/2026 (comparativo "como esta e como fica" e a conversa que se seguiu):
- quadro: sai a Coordenacao Operacional; a Assistencial assume polos, agendas, redistribuicao, supervisores e o
  pre-exame; a Administrativa e Financeira, o pos-exame e os assistentes, com as atribuicoes do pt_ses_01 e do pt_ses_02;
  operadores 5 + 5 (calculo_v25.py, v25.json);
- o polo de cada solicitacao e definido pela regulacao da SES-DF, em regra pela Regiao de Saude da unidade solicitante
  (o campo regiao_saude_solicitante do Mapa Social), e nao pelo domicilio;
- capacidade da ultrassonografia em horas, sem numero de salas por polo;
- sem o paragrafo de absenteismo da 4.12 (tratamento interno do proponente);
- linguagem: sem "cheia", "lotado", "custa", "estoque" e expressoes do genero; repeticoes da 4.11, 4.13, 4.14 e 4.15;
  o laudo do ultrassom na 4.3; "idem" por extenso; remissoes "na forma da subsecao" viram "(subsecao X)";
- tomografia sem obrigacao de tomografo em todo polo: uma regra na 4.2 deixa a tomografia de um polo ser feita em
  outro da rede. A: o texto fala em seis tomografos, dimensionados um por polo. B: o texto nao diz quantos
  tomografos, so a carga de 3,33 equipamentos, que a rede atende com folga.
"""
import sys, os, json, re
from decimal import Decimal as D
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v20"))
from docxlib import Doc, q

pasta, modo, var = sys.argv[1], sys.argv[2], sys.argv[3]
assert var in ("A", "B")
B = var == "B"
V = json.load(open(os.path.join(AQUI, "v25.json")))
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))

TOCADOS = set()
_replace = d.replace


def _rep(p, *a, **k):
    TOCADOS.add(p)
    return _replace(p, *a, **k)


d.replace = _rep


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
        TOCADOS.add(cs[ci].find(q("p")))
        d.set_cell(cs[ci], v, novo=ci in novos)


def cel(tbl, ri, ci):
    return d.cells(d.rows(tbl)[ri])[ci].find(q("p"))


def trocar(p, novo):
    d.replace(p, d.text(p), novo)


def sub(contains, old, new, within=None):
    d.replace(d.find(contains, within=within), old, new)


def remover_par(p):
    TOCADOS.add(p)
    if d.marcado:
        for run in d.runs(p):
            d.mark_old(run)
    else:
        p.getparent().remove(p)


def remover_linha(tbl, ri, col, comeca):
    linha = d.rows(tbl)[ri]
    txt = d.text(d.cells(linha)[col].find(q("p")))
    assert txt.startswith(comeca), txt
    if d.marcado:
        for run in d.runs_all(linha):
            d.mark_old(run)
    else:
        linha.getparent().remove(linha)


ORD = V["ORD"]
CCS = "Central e Centro-Sul"
P = V["polos"]
TOTAL, US, TC = V["total"], V["us_total"], V["tc_total"]
APOIO, GLOB, PROD = D(V["apoio"]), D(V["global"]), D(V["producao"])
qc, HUS, HTC, HM = V["qc"], V["hus"], V["htc"], V["h_medico"]
CARGA = dec(V["carga_tc"], 2)
NA = {x: ("nas Regiões Central e Centro-Sul" if x == CCS else f"na Região {x}") for x in ORD}
UNIT = {"02.05.02.009-7": D("99.94"), "02.05.02.018-6": D("99.94"), "02.05.01.004-0": D("100.18"),
        "02.05.02.004-6": D("100.18"), "02.05.02.005-4": D("99.94"), "02.05.02.012-7": D("99.94"),
        "02.05.02.010-0": D("99.94"), "02.05.02.003-8": D("99.94"), "02.06.03.001-0": D("299.44"),
        "02.06.03.003-7": D("299.44"), "02.06.02.003-1": D("300.10")}
POSTO = {p: (qt, D(v), D(tt)) for p, qt, v, _, _, tt in V["quadro"]}
dia_us = sum(P[x]["dia_us"] for x in ORD)
dia_tc = sum(P[x]["dia_tc"] for x in ORD)
assert dia_us + dia_tc > V["pico_dia"]
assert CARGA == "3,33"
T = d.tables()

# ================= 1.4 =================
d.replace(d.find("valor global do plano, dentro do recurso disponível"), "R$ 11.592.700,94", f"R$ {r(GLOB)}")

# ================= 2.2 =================
sub("O objeto é a realização de 79.152 exames", "79.152", n(TOTAL))
for ri, tr in enumerate(d.rows(T[2])[1:12], start=1):
    cod = d.text(d.cells(tr)[0].find(q("p")))
    set_row(T[2], ri, [None, None, n(qc[cod])])
set_row(T[2], 12, [None, None, n(TOTAL)])
p = d.find("São 65.530 exames de ultrassonografia")
d.replace(p, "65.530", n(US))
d.replace(p, "13.622", n(TC))

# ================= 3.1 =================
p = d.find("A parceria resolve a totalidade das 78.572 solicitações")
d.replace(p, "atende mais 580", f"atende mais {n(V['acrescimo'])}")
d.replace(p, "79.152 exames ao todo", f"{n(TOTAL)} exames ao todo")
for ri, val in [(2, f"R$ {r(APOIO)}"), (3, f"R$ {r(V['envelope'])}"), (4, f"{n(TOTAL)} exames"),
                (5, f"R$ {r(PROD)}"), (6, f"R$ {r(GLOB)}"), (7, f"R$ {r(V['sobra'])}")]:
    set_row(T[4], ri, [None, val])

# ================= 3.4 =================
for i, x in enumerate(ORD, start=1):
    set_row(T[5], i, [None, None, f"{P[x]['tot'] / TOTAL * 100:.2f}%".replace(".", ","), n(P[x]["tot"])])
set_row(T[5], 7, [None, None, None, n(TOTAL)])
sub("Essas solicitações são encaminhadas ao polo de referência do domicílio do usuário.",
    "Essas solicitações são encaminhadas ao polo de referência do domicílio do usuário.",
    "O polo dessas solicitações, como o das demais, é definido pela regulação da SES-DF.")

# ================= 4.2 =================
sub("Os seis polos realizam ultrassonografia e tomografia computadorizada (subseção 7.3).",
    "proponente. Os seis polos realizam ultrassonografia e tomografia computadorizada (subseção 7.3).",
    f"proponente, dimensionada {'' if B else 'por polo '}na subseção 7.3. A tomografia computadorizada de um polo pode "
    "ser realizada em outro polo da rede, sem alteração do quantitativo, quando a capacidade instalada ou a manutenção "
    "de equipamento o recomendar.")
p = d.find("O usuário é encaminhado ao polo de referência do seu domicílio. Na tomografia")
d.replace(p, "O usuário é encaminhado ao polo de referência do seu domicílio.",
          "O polo de cada solicitação é definido pela regulação da SES-DF, em regra pela Região de Saúde da unidade "
          "solicitante.")
if B:
    d.replace(p, "Na tomografia, o polo da Região Oeste recebe também a parte da carga da Região Sudoeste que excede a "
                 "capacidade de um equipamento (subseção 7.3).",
              "Na tomografia, a carga de um polo que excede a capacidade disponível nele é absorvida em outro polo da "
              "rede (subseção 7.3).")
d.replace(p, "A redistribuição entre polos", "A redistribuição da agenda entre polos")
d.replace(p, "Coordenação Operacional, na forma da subseção 4.13.", "Coordenação Assistencial (subseção 4.13).")

# ================= 4.3 =================
d.replace(cel(T[8], 7, 1), "laudo assinado por médico radiologista",
          "laudo assinado pelo médico que realiza a ultrassonografia ou, na tomografia, pelo médico radiologista")
d.replace(cel(T[8], 7, 2), "médico radiologista", "médico que realiza a ultrassonografia; médico radiologista, na "
          "tomografia")

# ================= 4.4 e 4.5 =================
sub("As solicitações do segundo grupo são encaminhadas ao polo de referência do domicílio do usuário.",
    "As solicitações do segundo grupo são encaminhadas ao polo de referência do domicílio do usuário.",
    "O polo das solicitações do segundo grupo também é definido pela regulação da SES-DF.")
p = d.find("O preparo é a causa mais frequente de exame perdido")
d.replace(p, "O preparo é a causa mais frequente de exame perdido, e é por isso que ele aparece três vezes no percurso",
          "O preparo inadequado é a causa mais frequente de exame não realizado e, por isso, a orientação aparece três "
          "vezes no percurso")
d.replace(p, "garantem que o usuário compreenda", "permitem confirmar que o usuário compreendeu")
d.replace(p, "preexistente, na forma da subseção 4.8.", "preexistente (subseção 4.8).")
sub("A escolha do polo segue o domicílio do usuário", "A escolha do polo segue o domicílio do usuário, na forma da "
    "subseção 4.2.", "A escolha do polo é da regulação da SES-DF (subseção 4.2).")

# ================= 4.6 e 4.7 =================
trocar(d.find("A véspera ainda admite correção; o dia do exame, não."),
       "A confirmação na véspera permite corrigir falhas que, no dia do exame, já não admitem correção: a compreensão do "
       "preparo, o endereço do polo e a documentação. Identificada na véspera, a falha admite correção ou troca de data; "
       "identificada na recepção, implica a perda da vaga e o deslocamento do usuário sem o exame.")
sub("Descoberto o descumprimento ainda na chegada",
    "Descoberto o descumprimento ainda na chegada, a vaga do dia é oferecida a outro usuário e o exame é remarcado; "
    "descoberto dentro da sala, ele consome o intervalo inteiro.",
    "Identificado o descumprimento na chegada, a vaga do dia é oferecida a outro usuário e o exame é remarcado; "
    "identificado já na sala, o descumprimento ocupa todo o intervalo reservado ao exame.")

# ================= 4.8 =================
sub("são 12.894 dos 13.622 exames de tomografia", "12.894 dos 13.622", f"{n(V['contraste'])} dos {n(TC)}")

# ================= 4.11 =================
sub("O registro conclui o exame, na forma da subseção 2.3",
    "O registro conclui o exame, na forma da subseção 2.3, e é feito com a data. É esse registro que o indicador I-03 lê.",
    "O registro, feito com a data, conclui o exame (subseção 2.3) e é o que o indicador I-03 lê.")
sub("A unidade solicitante consulta o resultado no TrakCare, pelo CPF ou pelo Cartão Nacional de Saúde do usuário.",
    "do usuário.", "do usuário, sem envio direto, e a partir desse registro a condução do cuidado é dela.")
sub("Nada é enviado à unidade de forma direta",
    " Nada é enviado à unidade de forma direta, uma vez que o laudo e o prontuário são registrados no TrakCare.",
    " Registrado o laudo, a chave da solicitação é fechada no sistema de regulação.")
remover_par(d.find("A partir do registro do laudo no TrakCare, a condução do cuidado é da unidade solicitante"))
remover_par(d.find("Registrado o laudo no TrakCare, a chave da solicitação é fechada no sistema de regulação."))

# ================= 4.12 =================
remover_par(d.find("Absenteísmo. As metas e o dimensionamento não usam taxa de absenteísmo"))

# ================= 4.13 =================
t9 = T[9]
assert d.text(cel(t9, 2, 1)) == "Coordenação Operacional"
d.replace(cel(t9, 3, 3), "conformidade dos protocolos", "funcionamento dos polos e das agendas e redistribuição de "
          "agenda entre polos (4.2); conformidade dos protocolos")
d.replace(cel(t9, 3, 3), "(4.15 e 4.16)", "(4.15 e 4.16); chefia dos supervisores de polo e dos operadores do "
          "pré-exame")
d.replace(cel(t9, 4, 3), "7.4 e 7.6", "planejamento, organização e controle dos fluxos administrativos e financeiros do "
          "projeto, com a execução orçamentária, os pagamentos e a conformidade com as normas aplicáveis; contratos e "
          "aquisições, inclusive de manutenção de equipamentos e de insumos (4.16); gestão dos recursos humanos do "
          "projeto; prestação de contas parcial e final, com a assessoria (7.4 e 7.6); chefia dos operadores do "
          "pós-exame e dos assistentes administrativos")
set_row(t9, 6, ["5"])
set_row(t9, 7, ["5"])
p = d.find("A direção, as três coordenações e os oito operadores de registro atuam de forma centralizada")
d.replace(p, "as três coordenações e os oito operadores", "as duas coordenações e os dez operadores")
d.replace(p, "para os seis polos, e não se lotam em nenhum deles.", "para os seis polos, sem vínculo a um polo "
          "específico.")
trocar(d.find("A Coordenação Operacional distribui entre os operadores a carga de contato"),
       "A Coordenação Assistencial distribui entre os operadores do pré-exame a carga de contato com os usuários "
       "agendados, e a Coordenação Administrativa e Financeira, entre os do pós-exame, a carga de registro dos seis "
       "polos, ao longo da vigência e conforme a execução de cada um — trabalho que não depende de o posto estar "
       "fisicamente no polo.")
p = d.find("A equipe assistencial — médico radiologista, técnico em radiologia")
d.replace(p, "médico radiologista, técnico em radiologia e o pessoal", "médicos, técnicos em radiologia, enfermagem e o "
          "pessoal")
d.replace(p, "é remunerada pelo valor unitário do exame. O quadro de pessoal assistencial, com nome completo, número de "
             "registro no conselho de classe e, para os médicos, Registro de Qualificação de Especialista (RQE), será "
             "apresentado na formalização do instrumento, na forma da subseção 4.15.",
          "é remunerada pelo valor unitário do exame (subseção 4.15).")

# ================= 4.14 =================
p = d.find("A execução assistencial não é subcontratada. Ela ocorre")
d.replace(p, "A execução assistencial não é subcontratada. Ela ocorre", "A execução assistencial não é subcontratada: "
          "ocorre")
d.replace(p, "As funções de direção e de coordenação relacionadas na subseção 4.13 são exercidas diretamente pelo "
             "proponente.",
          "As funções de direção, coordenação e gestão da subseção 4.13 são exercidas diretamente pelo proponente; a "
          "assessoria especializada que apoia a prestação de contas executa atividade acessória e não substitui a "
          "Coordenação Administrativa e Financeira.")
remover_par(d.find("As funções de gestão, coordenação e direção não são subcontratadas."))

# ================= 4.15 =================
sub("Cada profissional é identificado, no quadro de pessoal a apresentar",
    "Cada profissional é identificado, no quadro de pessoal a apresentar na formalização do instrumento, por nome "
    "completo, número de registro no conselho de classe e, para os médicos, RQE. O quadro nominal será apresentado na "
    "formalização do instrumento.",
    "O quadro nominal, com nome completo, número de registro no conselho de classe e, para os médicos, RQE, será "
    "apresentado na formalização do instrumento.")
t11 = T[11]
d.replace(cel(t11, 1, 8), "salas: 1, 6, 2, 3, 3 e 5; ", "")
velho_rad = "horas de sala da tomografia 351, 1.602, 664, 448, 807 e 609 ÷ 1.200 h no período (0,29; 1,33; 0,55; 0,37; 0,67; 0,51)"
if B:
    set_row(t11, 2, [None, f"no mínimo {V['radiologistas_rede']}"] + [""] * 6)
    d.replace(cel(t11, 2, 8), velho_rad, f"horas de tomógrafo da rede ({n(HTC)}) ÷ {n(HM)} h no período "
              f"({dec(HTC / HM, 2)})")
    set_row(t11, 5, [None, "3 por tomógrafo"] + [""] * 6)
    set_row(t11, 6, [None, "2 por tomógrafo"] + [""] * 6)
else:
    rad = {x: P[x]["radiologistas"] for x in ORD}
    set_row(t11, 2, [None, str(sum(rad.values()))] + [str(rad[x]) for x in ORD])
    d.replace(cel(t11, 2, 8), velho_rad, "horas de sala da tomografia " + lista([n(P[x]["htc"]) for x in ORD]) +
              f" ÷ {n(HM)} h no período (" + "; ".join(dec(P[x]["htc"] / HM, 2) for x in ORD) + ")")
mus = {x: P[x]["medicos_us"] for x in ORD}
set_row(t11, 1, [None, str(sum(mus.values()))] + [str(mus[x]) for x in ORD])
p = d.find("Ultrassonografia: as 24.261 horas de sala")
d.replace(p, "24.261 horas de sala (1.318 na Região Oeste, 7.917 na Região Sudoeste, 2.147 na Região Norte, 3.700 na "
             "Região Leste, 3.661 nas Regiões Central e Centro-Sul e 5.518 na Região Sul)",
          f"{n(HUS)} horas de sala (" + lista([f"{n(P[x]['hus'])} {NA[x]}" for x in ORD]) + ")")
d.replace(p, "5 na Região Sul (5.518 ÷ 1.200 = 4,6)", f"{mus['Sul']} na Região Sul ({n(P['Sul']['hus'])} ÷ {n(HM)} = "
          f"{dec(P['Sul']['hus'] / HM, 1)})")
d.replace(p, "sempre em número igual ou superior ao de salas (1, 6, 2, 3, 3 e 5)", "sempre em número igual ou superior ao "
          "de salas de cada polo")
if B:
    d.replace(p, "logo no mínimo 3 técnicos por tomógrafo e 18 nos seis tomógrafos,", "logo no mínimo 3 técnicos por "
              "tomógrafo da rede,")

# ================= 4.16 (a) =================
sub("supervisor de proteção radiológica de cada polo", "responsável técnico do serviço e supervisor de proteção "
    "radiológica de cada polo", "responsável técnico do serviço de cada polo e supervisor de proteção radiológica de cada "
    "serviço de tomografia")

# ================= 5 =================
p = d.find("reduzindo o estoque da fila de regulação da SES-DF")
d.replace(p, "reduzindo o estoque da fila de regulação da SES-DF", "reduzindo o número de solicitações pendentes na fila "
          "de regulação da SES-DF")
d.replace(p, "79.152", n(TOTAL))
t12 = T[12]
d.replace(d.find("79.152 vagas", within=t12), "79.152", n(TOTAL))
d.replace(d.find("79.152 exames registrados", within=t12), "79.152", n(TOTAL))
d.replace(d.find("65.530 exames", within=t12), "65.530", n(US))
d.replace(d.find("13.622 exames", within=t12), "13.622", n(TC))

# ================= 6.1 =================
t13 = T[13]
d.replace(d.find("79.152 vagas disponibilizadas", within=t13), "79.152", n(TOTAL))
d.replace(d.find("79.152 exames registrados", within=t13), "79.152", n(TOTAL))
d.replace(d.find("65.530 exames", within=t13), "65.530", n(US))
d.replace(d.find("13.622 exames", within=t13), "13.622", n(TC))
p = d.find("As Metas 4 e 5 se decompõem por polo")
for x, velho in zip(ORD, ["4.596 exames na Região Oeste", "26.821 na Região Sudoeste", "6.700 na Região Norte",
                          "12.301 na Região Leste", "12.436 nas Regiões Central e Centro-Sul", "16.298 na Região Sul"]):
    novo = velho.replace(velho.split(" ")[0], n(P[x]["tot"]))
    if novo != velho:
        d.replace(p, velho, novo)

# ================= 7.1 e 7.2 =================
sub("conferência da capacidade instalada de cada polo contra os parâmetros da subseção 7.3", "de cada polo", "da rede",
    within=T[15])
for i in range(3):
    set_row(T[16], i + 1, [None, None, n(V["curva"][i])])
set_row(T[16], 4, [None, None, n(TOTAL)])

# ================= 7.3 =================
sub("A produção do período de maior carga", "com 19.793 exames", f"com {n(V['curva'][2])} exames")
p = d.find("A execução do objeto requer 28.742 horas de sala")
d.replace(p, "28.742 horas de sala no período — 24.261 de ultrassonografia e 4.481",
          f"{n(HUS + HTC)} horas de sala no período — {n(HUS)} de ultrassonografia e {n(HTC)}")
p = d.find("Não há fração de exame nem de sala")
if B:
    d.replace(p, "Não há fração de exame nem de sala: os quantitativos diários e os equipamentos de cada polo são",
              "Não há fração de exame: os quantitativos diários são")
else:
    d.replace(p, "Não há fração de exame nem de sala:", "Não há fração de exame:")
t17 = T[17]
VAZIO = [""] * 6
set_row(t17, 2, [None, n(TOTAL)] + [n(P[x]["tot"]) for x in ORD])
set_row(t17, 3, [None, n(US)] + [n(P[x]["us"]) for x in ORD])
set_row(t17, 4, [None, n(TC)] + [n(P[x]["tc"]) for x in ORD])
d.replace(cel(t17, 4, 8), "idem", "cada procedimento distribuído pela origem das suas solicitações")
set_row(t17, 5, [None, n(sum(P[x]["mes_us"] for x in ORD))] + [n(P[x]["mes_us"]) for x in ORD])
set_row(t17, 6, [None, n(sum(P[x]["mes_tc"] for x in ORD))] + [n(P[x]["mes_tc"]) for x in ORD])
d.replace(cel(t17, 6, 8), "idem; total: soma dos polos", "exames do período ÷ 8 meses; total: soma dos polos")
set_row(t17, 9, [None, n(dia_us)] + [n(P[x]["dia_us"]) for x in ORD])
set_row(t17, 10, [None, n(dia_tc)] + [n(P[x]["dia_tc"]) for x in ORD])
d.replace(cel(t17, 10, 8), "idem; total: soma dos polos", "exames do período ÷ 168 dias úteis; total: soma dos polos")
set_row(t17, 13, [None, n(HUS)] + [n(P[x]["hus"]) for x in ORD])
if B:
    set_row(t17, 14, ["Carga de tomografia, em equipamentos", CARGA] + VAZIO)
    trocar(cel(t17, 14, 8), "horas de tomógrafo ÷ (168 dias úteis × 10 horas × 80% de ocupação); a rede atende a carga "
           "com folga (4.2)")
    set_row(t17, 15, [None, n(HTC)] + VAZIO)
    d.replace(cel(t17, 15, 8), "exames do polo", "exames de tomografia")
else:
    d.replace(cel(t17, 14, 8), "um por polo; a carga da Região Sudoeste que excede um equipamento é absorvida no polo da "
              "Região Oeste (4.2)", "dimensionamento de um por polo; a carga que excede um equipamento, como a da "
              "Região Sudoeste, é absorvida em outro polo da rede (4.2)")
    set_row(t17, 15, [None, n(HTC)] + [n(P[x]["htc"]) for x in ORD])
d.replace(cel(t17, 16, 0), "lotados no polo", "em cada polo")
trocar(d.find("O polo da Região Oeste realiza, por dia útil"),
       "Por dia útil, o polo da Região Oeste responde por " + f"{P['Oeste']['dia_us']} exames de ultrassonografia e "
       f"{P['Oeste']['dia_tc']} de tomografia computadorizada; " +
       "; ".join(f"o {('das Regiões Central e Centro-Sul' if x == CCS else 'da Região ' + x)}, por {P[x]['dia_us']} e "
                 f"{P[x]['dia_tc']}" for x in ORD[1:-1]) +
       f"; e o da Região Sul, por {P['Sul']['dia_us']} e {P['Sul']['dia_tc']}. Os seis polos funcionam dez horas por dia "
       "útil, e cada um conta com um posto de gestão e apoio.")
p = d.find("A soma dos polos, de 393 exames de ultrassonografia")
d.replace(p, "e 86 de tomografia", f"e {dia_tc} de tomografia")
d.replace(p, "porque a capacidade de cada polo é arredondada para cima", "porque o quantitativo diário de cada polo é "
          "arredondado para cima")
d.replace(p, "absorve exame que se estende e manutenção.", "absorve exame que se estende e manutenção. As salas de "
          "ultrassonografia de cada polo são as que absorvem as horas de sala do polo no horário de funcionamento, no "
          "mínimo uma; o número de salas resulta do tempo de exame praticado em cada polo e é conferido no mês 1 contra "
          "essas horas (Meta 1).")
p = d.find("Aos seis postos lotados nos polos")
d.replace(p, "Aos seis postos lotados nos polos", "Aos seis postos de gestão e apoio dos polos")
d.replace(p, "as três coordenações e os oito operadores de registro, que atuam de forma centralizada, na forma da "
             "subseção 4.13,", "as duas coordenações e os dez operadores de registro, que atuam de forma centralizada "
          "(subseção 4.13),")
p = d.find("Um tomógrafo em cada polo mantém o exame perto")
if B:
    trocar(p, f"A tomografia é dimensionada sobre a carga do conjunto, de {CARGA} equipamentos em turno de dez horas, com "
           "ocupação de 80% do horário de funcionamento, e a capacidade da rede atende essa carga com folga. A folga "
           "absorve a manutenção de cada equipamento e a realização da tomografia de um polo em outro da rede (subseção "
           "4.2).")
else:
    so, oe = dec(P["Sudoeste"]["carga_tc"], 2), dec(P["Oeste"]["carga_tc"], 2)
    assert (so, oe) == ("1,19", "0,26")
    d.replace(p, "Um tomógrafo em cada polo mantém o exame perto do domicílio do usuário.",
              "O dimensionamento de um tomógrafo por polo mantém o exame perto da unidade solicitante.")
    d.replace(p, "A folga do conjunto absorve a manutenção de cada equipamento.",
              f"A folga do conjunto — seis equipamentos para uma carga de {CARGA} — absorve a manutenção de cada "
              "equipamento e a realização da tomografia de um polo em outro da rede (subseção 4.2).")

# ================= 7.5 =================
for i in range(3):
    set_row(T[18], i + 1, [None, None, n(V["curva"][i]), r(V["prod_b"][i]), r(V["apoio_periodo"][i]), r(V["parcelas"][i])])
set_row(T[18], 4, [None, None, n(TOTAL), r(PROD), r(APOIO), r(GLOB)])

# ================= 7.8 =================
t19 = T[19]
sub("conferência da capacidade instalada de cada polo contra os parâmetros da subseção 7.3, no mês 1", "de cada polo",
    "da rede", within=t19)
p = d.find("quantitativo pactuado de 79.152 inclui 580", within=t19)
d.replace(p, "79.152 inclui 580", f"{n(TOTAL)} inclui {n(V['acrescimo'])}")
d.replace(p, ", na forma da mesma subseção, de modo que o risco é de fluxo e não de estoque;",
          " (mesma subseção), de modo que o risco está no ritmo de envio das solicitações, e não na existência de "
          "demanda;")
d.replace(p, "ajuste da meta por termo aditivo, na forma da subseção 2.2", "ajuste da meta por termo aditivo (subseção 2.2)")
p = d.find("seis equipamentos, um por polo, para uma carga de 3,33", within=t19)
if B:
    d.replace(p, "seis equipamentos, um por polo, para uma carga de 3,33, na forma da subseção 7.3, com redistribuição da "
                 "agenda de tomografia entre os polos no mesmo dia",
              f"capacidade da rede de tomografia dimensionada sobre a carga de {CARGA} equipamentos, com a folga da "
              "subseção 7.3, e redistribuição da agenda entre os tomógrafos da rede no mesmo dia")
else:
    d.replace(p, "seis equipamentos, um por polo, para uma carga de 3,33, na forma da subseção 7.3,",
              f"seis equipamentos para uma carga de {CARGA} (subseção 7.3),")
sub("redistribuição de agenda pela Coordenação Operacional", "Coordenação Operacional", "Coordenação Assistencial",
    within=t19)

# ================= 7.9 =================
p = d.find("R-01 é o risco que define este objeto.")
d.replace(p, "R-01 é o risco que define este objeto.", "R-01 é o risco central deste objeto.")
if B:
    d.replace(p, "A meta de 79.152 exames em oito meses exige vinte salas de ultrassonografia e seis tomógrafos em turno de "
                 "dez horas. A conferência da capacidade instalada de cada polo",
              f"A meta de {n(TOTAL)} exames em oito meses exige {n(HUS)} horas de sala de ultrassonografia e {n(HTC)} "
              f"horas de tomógrafo em turno de dez horas, uma carga de {CARGA} equipamentos que a rede atende com folga "
              "(subseção 7.3). A conferência da capacidade instalada da rede")
else:
    d.replace(p, "A meta de 79.152 exames em oito meses exige vinte salas de ultrassonografia e seis tomógrafos em turno de "
                 "dez horas. A conferência da capacidade instalada de cada polo",
              f"A meta de {n(TOTAL)} exames em oito meses exige {n(HUS)} horas de sala de ultrassonografia e {n(HTC)} "
              "horas de tomógrafo em turno de dez horas, com seis tomógrafos. A conferência da capacidade instalada da "
              "rede")
p = d.find("R-02 é o risco de maior probabilidade do conjunto.")
d.replace(p, "e cada falta é uma sala ociosa", "e cada falta deixa a sala sem uso no horário reservado")
d.replace(p, "são o que sustenta o ritmo", "sustentam o ritmo")
p = d.find("R-04 é o risco que o valor de tabela não elimina.")
d.replace(p, "R-04 é o risco que o valor de tabela não elimina. O meio de contraste iodado é insumo de 12.894 dos 13.622",
          f"R-04 decorre do custo do meio de contraste iodado, insumo de {n(V['contraste'])} dos {n(TC)}")
d.replace(p, "(estimativa de planejamento, subseção 4.8) e está dentro do valor unitário",
          "(estimativa de planejamento, subseção 4.8) que está dentro do valor unitário")
sub("R-10 é o risco próprio deste objeto.", "R-10 é o risco próprio deste objeto.", "R-10 é o risco específico deste "
    "objeto.")
sub("R-16 é o risco de forma, não de mérito.", "R-16 é o risco de forma, não de mérito.", "R-16 refere-se à forma de "
    "composição da rubrica, e não ao mérito da despesa.")

# ================= 8.2 (as linhas saem no fim) =================
t21 = T[21]
q_dir, v_dir, t_dir = POSTO["Direção Executiva de Projeto"]
q_ca, v_ca, t_ca = POSTO["Coordenação Assistencial"]
q_sp, v_sp, t_sp = POSTO["Supervisão de Polo Assistencial"]
q_pre, v_pre, t_pre = POSTO["Operador de registro de sistemas — pré-exame"]
q_pos, v_pos, t_pos = POSTO["Operador de registro de sistemas — pós-exame"]
q_af, v_af, t_af = POSTO["Coordenação Administrativa e Financeira"]
q_ac, v_ac, t_ac = POSTO["Assessoria de Prestação de Contas"]
q_as, v_as, t_as = POSTO["Assistente Administrativo"]
assert d.text(cel(t21, 4, 1)) == "Coordenação Operacional"
set_row(t21, 5, ["1.1.2", None, "4.2 · 4.7 a 4.11 · 4.13"])
set_row(t21, 6, ["1.1.3"])
m1 = t_dir + t_ca + t_sp
set_row(t21, 7, [None, None, None, None, str(q_dir + q_ca + q_sp), None, None, r(m1)])
set_row(t21, 10, [None, None, None, None, str(q_pre), None, None, r(t_pre)])
set_row(t21, 11, [None, None, None, None, str(q_pre), None, None, r(t_pre)])
set_row(t21, 14, [None, None, None, None, str(q_pos), None, None, r(t_pos)])
set_row(t21, 15, [None, None, None, None, str(q_pos), None, None, r(t_pos)])
m4 = D(0)
for ri in range(18, 26):
    cod = [c for c in qc if c in d.text(cel(t21, ri, 1))][0]
    v = qc[cod] * UNIT[cod]
    m4 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 26, [None, None, None, None, n(US), None, None, r(m4)])
m5 = D(0)
for ri in range(29, 32):
    cod = [c for c in qc if c in d.text(cel(t21, ri, 1))][0]
    v = qc[cod] * UNIT[cod]
    m5 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 32, [None, None, None, None, n(TC), None, None, r(m5)])
m6 = t_af + t_ac + t_as
assert r(m6) == d.text(cel(t21, 38, 7))
total_geral = m1 + t_pre + t_pos + m4 + m5 + m6
assert total_geral == GLOB and m4 + m5 == PROD and m1 + t_pre + t_pos + m6 == APOIO, (total_geral, GLOB)
set_row(t21, 39, [None, None, None, None, None, None, None, r(total_geral)])

# ================= 8.3 =================
for ri, v in [(1, m1), (2, t_pre), (3, t_pos), (4, m4), (5, m5), (6, m6), (7, total_geral)]:
    set_row(T[22], ri, [None, r(v)])

# ================= remissoes: "na forma da subsecao X" vira "(subsecao X)" =================
SEC = r"\d+(?:\.\d+)*"
REGRAS = [(re.compile(rf" — na forma da subseção ({SEC})"), r" (subseção \1)"),
          (re.compile(r",? na forma da mesma subseção"), " (mesma subseção)"),
          (re.compile(r",? na forma do risco (R-\d+)"), r" (risco \1)"),
          (re.compile(rf",? na forma das subseções ({SEC}(?:, {SEC})* e {SEC})"), r" (subseções \1)"),
          (re.compile(rf",? na forma da subseção ({SEC}(?:, alínea [a-z])?)"), r" (subseção \1)")]
n_rem = 0
for p in d.paragraphs():
    if p in TOCADOS:
        continue
    achados = []
    txt = d.text(p)
    for rx, novo in REGRAS:
        for m in rx.finditer(txt):
            if not any(a <= m.start() < b for a, b, _, _ in achados):
                achados.append((m.start(), m.end(), m.group(0), m.expand(novo)))
    for a, b, velho, novo in sorted(achados, reverse=True):
        _replace(p, velho, novo, desde=a)
        n_rem += 1
resto = [d.text(p) for p in d.paragraphs() if p not in TOCADOS and re.search(r"na forma d[ao]s? (subseç|risco|mesma subseção)",
                                                                                d.text(p))]
assert d.marcado or not resto, resto

# ================= linhas que saem (de baixo para cima em cada tabela) =================
remover_linha(t21, 4, 1, "Coordenação Operacional")
remover_linha(t17, 12, 0, "Exames por sala de ultrassonografia")
remover_linha(t17, 11, 0, "Salas de ultrassonografia")
remover_linha(t9, 2, 1, "Coordenação Operacional")

d.save()
print(f"{var} {modo}: {len(d.log)} trocas, {n_rem} remissões; {n(TOTAL)} exames; global {r(GLOB)}; apoio {r(APOIO)}")
