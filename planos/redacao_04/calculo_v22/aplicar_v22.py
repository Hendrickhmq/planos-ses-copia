"""Aplica a v22 sobre a v7 FINAL da equipe (PT_simplificado_exames_de_imagem_v7_FINAL.docx, descompactada).

uso: aplicar_v22.py <docx_descompactado> limpo|marcado

Numa passada so, a partir da v7 FINAL: os dez polos da v21 (sem localizacao, por Regiao), oito meses de
vigencia e execucao (dois trimestres e um bimestre final), o novo quadro de gestao (Direcao Executiva de Projeto,
Coordenacao Administrativa e Financeira, Coordenacao Operacional, 10 operadores e 10 assistentes) e todos os
numeros recalculados (calculo_v22.py). A secao de riscos fica com a redacao da v7; so os numeros e o nome da
coordenacao que deixou de existir mudam.
"""
import sys, os, json
from decimal import Decimal as D
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v20"))
from docxlib import Doc, q

pasta, modo = sys.argv[1], sys.argv[2]
V = json.load(open(os.path.join(AQUI, "v22.json")))
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


ORD = V["ORD"]                      # Oeste, Sudoeste, Norte e Leste, Central, Sul, Centro-Sul
POLOS = V["POLOS"]
M = V["meses"]
TOTAL, US, TC = V["total"], V["us_total"], V["tc_total"]
APOIO, GLOB, PROD = D(V["apoio"]), D(V["global"]), D(V["producao"])
qc, tot, hus, htc = V["qc"], V["tot"], V["hus"], V["htc"]
salas, tomo, mus, rad = V["salas"], V["tomografos"], V["medicos_us"], V["radiologistas"]
HUS, HTC = sum(hus.values()), sum(htc.values())
PCT = {x: f"{tot[x] / TOTAL * 100:.2f}%".replace(".", ",") for x in ORD}
UNIT = {"02.05.02.009-7": D("99.94"), "02.05.02.018-6": D("99.94"), "02.05.01.004-0": D("100.18"),
        "02.05.02.004-6": D("100.18"), "02.05.02.005-4": D("99.94"), "02.05.02.012-7": D("99.94"),
        "02.05.02.010-0": D("99.94"), "02.05.02.003-8": D("99.94"), "02.06.03.001-0": D("299.44"),
        "02.06.03.003-7": D("299.44"), "02.06.02.003-1": D("300.10")}
NA = {x: ("nas Regiões Norte e Leste" if x == "Norte e Leste" else f"na Região {x}") for x in ORD}
A = {x: ("As Regiões Norte e Leste realizam" if x == "Norte e Leste" else f"A Região {x} realiza") for x in ORD}
EXT_F = {1: "uma", 2: "duas", 3: "três", 4: "quatro", 5: "cinco", 6: "seis", 7: "sete"}
EXT_M = {1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco", 6: "seis", 7: "sete"}
EXT_N = {7: "sete", 8: "oito", 20: "vinte", 21: "vinte e uma"}
lotados = {x: V["operadores"][x] + V["assistentes"][x] for x in ORD}
POSTO = {p: (qt, D(v), D(tt)) for p, qt, v, _, _, tt in V["quadro"]}
PER = V["periodos"]                 # [rotulo, meses, duracao]: 1º trimestre, 2º trimestre, bimestre final

T = d.tables()

# ================= 1. Informacoes iniciais =================
cel1 = d.find("valor global do plano, dentro do recurso disponível")
d.replace(cel1, "R$ 11.592.687,16", f"R$ {r(GLOB)}")
d.sub("Polos de Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama e Guará",
      "Polos de Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama e Guará",
      "Dez polos nas Regiões de Saúde do Distrito Federal, na forma da subseção 4.2")
d.replace(d.find("12 (doze) meses", within=T[1]), "12 (doze) meses", f"{M} (oito) meses")

# ================= 2.2 composicao =================
d.sub("O objeto é a realização de 79.357 exames", "79.357", n(TOTAL))
t2 = T[2]
for ri, tr in enumerate(d.rows(t2)[1:12], start=1):
    cod = d.text(d.cells(tr)[0].find(q("p")))
    set_row(t2, ri, [None, None, n(qc[cod])])
set_row(t2, 12, [None, None, n(TOTAL)])
p = d.find("São 65.676 exames de ultrassonografia")
d.replace(p, "65.676", n(US))
d.replace(p, "13.681", n(TC))

# ================= 3.1 a fila =================
p = d.find("A parceria resolve a totalidade das 78.572 solicitações")
d.replace(p, "atende mais 785", f"atende mais {n(V['acrescimo'])}")
d.replace(p, "79.357 exames ao todo", f"{n(TOTAL)} exames ao todo")
for ri, val in [(2, f"R$ {r(APOIO)}"), (3, f"R$ {r(V['envelope'])}"), (4, f"{n(TOTAL)} exames"),
                (5, f"R$ {r(PROD)}"), (6, f"R$ {r(GLOB)}"), (7, f"R$ {r(V['sobra'])}")]:
    set_row(T[4], ri, [None, val])

# ================= 3.4 distribuicao (linhas = Regioes) =================
d.sub("A participação de cada polo corresponde à participação das Regiões de Saúde que ele atende",
      "A participação de cada polo corresponde à participação das Regiões de Saúde que ele atende",
      "A participação dos polos de cada Região corresponde à participação dessa Região")
t5 = T[5]
set_row(t5, 0, ["Regiões de Saúde", "polos"])
for i, x in enumerate(ORD, start=1):
    set_row(t5, i, [x, str(POLOS[x]), PCT[x], n(tot[x])])
set_row(t5, 7, [None, "10", None, n(TOTAL)])

# ================= 3.12, 4.2 =================
d.sub("compatível com a implantação dos seis polos no mês 1", "seis polos", "dez polos")
d.sub("A execução ocorre em seis polos, situados de modo", "seis polos, situados", "dez polos, distribuídos")
t7 = T[7]
d.clone_row(t7, 6)
set_row(t7, 0, ["Regiões de Saúde", "polos"])
for i, x in enumerate(ORD, start=1):
    set_row(t7, i, [x, str(POLOS[x])])
set_row(t7, 7, ["total", "10"], novos={0, 1})
d.sub("e os seis polos realizam ultrassonografia e tomografia computadorizada.",
      ", e os seis polos realizam ultrassonografia e tomografia computadorizada.",
      ". Os dez polos realizam ultrassonografia, e a tomografia computadorizada é realizada em pelo menos um polo "
      "de cada Região de Saúde, consideradas em conjunto as Regiões Norte e Leste (subseção 7.3).")
p = d.find("quando necessária para cumprir a curva de produção, é atribuição da Coordenação Administrativa")
d.replace(p, "Coordenação Administrativa", "Coordenação Operacional")
d.replace(p, ".", ". Nas Regiões com dois polos, a produção da Região se divide entre eles conforme a capacidade de "
          "cada um.", desde=len(d.text(p)) - 1)
d.sub("Os polos situam-se nas Regiões Administrativas de",
      "Os polos situam-se nas Regiões Administrativas de Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama "
      "e Guará, no Distrito Federal. O endereço", "A Região Administrativa, o endereço")

# ================= 4.8 contraste =================
d.sub("são 12.953 dos 13.681 exames de tomografia", "12.953 dos 13.681", f"{n(V['contraste'])} dos {n(TC)}")

# ================= 4.13 equipe de gestao e apoio =================
t9 = T[9]
d.clone_row(t9, 1)                       # linha nova para a Coordenacao Operacional
set_row(t9, 1, ["1", "Direção Executiva de Projeto", f"{M} meses",
                "supervisão de todos os passos, interlocução com a SES-DF e acompanhamento das metas"])
set_row(t9, 2, ["1", "Coordenação Operacional", f"{M} meses",
                "funcionamento dos polos e das agendas, redistribuição de agenda entre polos (4.2)"], novos={0, 1, 2, 3})
set_row(t9, 3, ["1", "Coordenação Administrativa e Financeira", f"{M} meses", None])
set_row(t9, 4, [str(POSTO["Operador de registro de sistemas"][0]), None, f"{M} meses", None])
set_row(t9, 5, [str(POSTO["Assistente Administrativo"][0]), None, f"{M} meses", None])
d.sub("Os seis operadores de registro e os oito assistentes administrativos se distribuem entre os seis polos:",
      "Os seis operadores de registro e os oito assistentes administrativos se distribuem entre os seis polos:",
      "Os dez operadores de registro e os dez assistentes administrativos são um de cada por polo e se distribuem "
      "entre as Regiões de Saúde:")
t10 = T[10]
set_row(t10, 0, [None] + ORD)
set_row(t10, 1, [None] + [str(V["operadores"][x]) for x in ORD] + [str(sum(V["operadores"].values()))])
set_row(t10, 2, [None] + [str(V["assistentes"][x]) for x in ORD] + [str(sum(V["assistentes"].values()))])
set_row(t10, 3, ["por Região"] + [str(lotados[x]) for x in ORD] + [str(sum(lotados.values()))])
d.sub("As duas coordenações são únicas para os seis polos", "As duas coordenações são únicas para os seis polos",
      "A direção e as duas coordenações são únicas para os dez polos")
d.sub("A Coordenação Administrativa redistribui a carga de contato", "Coordenação Administrativa",
      "Coordenação Operacional")

# ================= 4.14 =================
d.sub("As funções de coordenação relacionadas na subseção 4.13", "As funções de coordenação",
      "As funções de direção e de coordenação")
d.sub("e não substitui a Coordenação Financeira.", "Coordenação Financeira", "Coordenação Administrativa e Financeira")

# ================= 4.15 equipe assistencial =================
t11 = T[11]
set_row(t11, 0, [None, None] + ORD)
set_row(t11, 1, [None, str(sum(mus.values()))] + [str(mus[x]) for x in ORD])
set_row(t11, 2, [None, str(sum(rad.values()))] + [str(rad[x]) for x in ORD])
set_row(t11, 3, [None, f"{sum(V['retaguarda'].values())} por dia útil"] + [str(V["retaguarda"][x]) for x in ORD])
set_row(t11, 4, [None, str(sum(V["rt"].values()))] + [str(V["rt"][x]) for x in ORD])
set_row(t11, 5, [None, str(sum(V["tecnicos"].values()))] + [str(V["tecnicos"][x]) for x in ORD])
set_row(t11, 6, [None, str(sum(V["enfermagem"].values()))] + [str(V["enfermagem"][x]) for x in ORD])
set_row(t11, 7, [None, str(sum(V["recepcao"].values()))] + [str(V["recepcao"][x]) for x in ORD])
c = cel(t11, 1, 8)
d.replace(c, "salas: 1, 4, 3, 1, 3 e 2", "salas: " + lista([str(salas[x]) for x in ORD]))
d.replace(c, "1.800 h anuais por médico", f"{n(V['h_medico'])} h por médico nos {M} meses (1.800 h anuais)")
c = cel(t11, 2, 8)
d.replace(c, "353, 1.609, 1.116, 503, 612 e 307 ÷ 1.800 h anuais (0,20; 0,89; 0,62; 0,28; 0,34; 0,17), "
             "arredondadas para cima",
          lista([n(htc[x]) for x in ORD]) + f" ÷ {n(V['h_medico'])} h no período (" +
          "; ".join(dec(htc[x] / V["h_medico"], 2) for x in ORD) + "), arredondadas para cima, e no mínimo um "
          "por tomógrafo")
p = d.find("Ultrassonografia: as 24.317 horas de sala")
d.replace(p, "24.317 horas de sala (1.322 em Ceilândia, 7.934 em Taguatinga, 5.860 em Sobradinho, 1.269 no Plano "
             "Piloto, 5.529 no Gama e 2.403 no Guará)",
          f"{n(HUS)} horas de sala (" + lista([f"{n(hus[x])} {NA[x]}" for x in ORD]) + ")")
d.replace(p, "pelas horas anuais de cada médico", "pelas horas de cada médico no período")
d.replace(p, "a carga horária contratual é 1.800 horas anuais por médico",
          f"a carga horária contratual é de 1.800 horas anuais por médico, {n(V['h_medico'])} horas nos {EXT_N[M]} "
          "meses do projeto")


def med(x):
    k = mus[x]
    h = V["h_medico"]
    base = f"{k} {'médico' if k == 1 else 'médicos'} {NA[x]}" if x == ORD[0] else f"{k} {NA[x]}"
    extra = ", um por polo" if k > -(-hus[x] // h) else ""
    return f"{base} ({n(hus[x])} ÷ {n(h)} = {dec(hus[x] / h, 1)}{extra})"


d.replace(p, "1 médico em Ceilândia (1.322 ÷ 1.800 = 0,7), 5 em Taguatinga (7.934 ÷ 1.800 = 4,4), 4 em Sobradinho "
             "(5.860 ÷ 1.800 = 3,3), 1 no Plano Piloto (1.269 ÷ 1.800 = 0,7), 4 no Gama (5.529 ÷ 1.800 = 3,1) e 2 no "
             "Guará (2.403 ÷ 1.800 = 1,3), 17 no total, sempre em número igual ou superior ao de salas (1, 4, 3, 1, 3 e 2)",
          lista([med(x) for x in ORD]) + f", {sum(mus.values())} no total, sempre em número igual ou superior ao de "
          "salas (" + lista([str(salas[x]) for x in ORD]) + ")")
d.replace(p, "e 18 nos seis polos", f"e {sum(V['tecnicos'].values())} nos {EXT_M[sum(tomo.values())]} tomógrafos")

# ================= 5 objetivos =================
p = d.find("mediante a realização de 79.357 exames")
d.replace(p, "79.357", n(TOTAL))
d.replace(p, "em doze meses", f"em {EXT_N[M]} meses")
t12 = T[12]
d.replace(d.find("coordenar seis polos de execução", within=t12), "seis polos", "dez polos")
d.replace(d.find("6 polos em operação por 12 meses", within=t12), "6 polos em operação por 12 meses",
          f"10 polos em operação por {M} meses")
d.replace(d.find("79.357 vagas", within=t12), "79.357", n(TOTAL))
d.replace(d.find("79.357 exames registrados", within=t12), "79.357", n(TOTAL))
d.replace(d.find("65.676 exames", within=t12), "65.676", n(US))
d.replace(d.find("13.681 exames", within=t12), "13.681", n(TC))
d.replace(d.find("12 relatórios mensais e 1 relatório final", within=t12), "12 relatórios", f"{M} relatórios")

# ================= 6 metas =================
t13 = T[13]
d.replace(d.find("6 polos em operação a partir do mês 1", within=t13), "6 polos", "10 polos")
d.replace(d.find("mantidos por 12 meses", within=t13), "mantidos por 12 meses", f"mantidos por {M} meses")
d.replace(d.find("79.357 vagas disponibilizadas", within=t13), "79.357", n(TOTAL))
d.replace(d.find("79.357 exames registrados", within=t13), "79.357", n(TOTAL))
d.replace(d.find("65.676 exames", within=t13), "65.676", n(US))
d.replace(d.find("13.681 exames", within=t13), "13.681", n(TC))
d.replace(d.find("12 relatórios mensais e 1 relatório final", within=t13), "12 relatórios", f"{M} relatórios")
for p in [p for p in t13.iter(q("p")) if "meses 1 a 12" in d.text(p)]:
    d.replace(p, "meses 1 a 12", f"meses 1 a {M}")
d.sub("As Metas 4 e 5 se decompõem por polo",
      "se decompõem por polo, na proporção da subseção 3.4 — 4.610 exames em Ceilândia, 26.888 em Taguatinga, 19.050 em "
      "Sobradinho, 4.721 no Plano Piloto, 16.336 no Gama e 7.752 no Guará —, por procedimento, no quantitativo da "
      "subseção 2.2, e por trimestre",
      "se decompõem por Região, na proporção da subseção 3.4 — " + lista(
          [f"{n(tot[x])} exames {NA[x]}" if x == ORD[0] else f"{n(tot[x])} {NA[x]}" for x in ORD]) +
      " —, por procedimento, no quantitativo da subseção 2.2, e por período")

# ================= 7.1 etapas =================
t15 = T[15]
d.replace(d.find("publicação das agendas dos seis polos", within=t15), "seis polos", "dez polos")
set_row(t15, 2, [None, None, None, f"1 a {M}"])
d.replace(cel(t15, 3, 3), "12 e o prazo", f"{M} e o prazo")

# ================= 7.2 curva =================
p = d.find("A produção começa no mês 1 e se reparte pelos quatro trimestres")
d.replace(p, d.text(p), "A produção começa no mês 1 e se reparte por dois trimestres e um bimestre final, na "
          "proporção dos meses de cada período. Cada procedimento tem três oitavos do seu quantitativo em cada "
          "trimestre e dois oitavos no bimestre final, e o resto da divisão se acomoda nos últimos.")
t16 = T[16]
set_row(t16, 0, ["período"])
for i, (rot, meses, _) in enumerate(PER):
    set_row(t16, i + 1, [rot, meses, n(V["curva"][i])])
set_row(t16, 5, [None, None, n(TOTAL)])
remover_linha(t16, 4, "4º")

# ================= 7.3 capacidade =================
p = d.find("A produção do trimestre de maior carga")
ip = V["pico_periodo"]
d.replace(p, "do trimestre de maior carga, de 19.843 exames, corresponde a 315",
          f"do período de maior carga — o {PER[ip][0]}, com {n(V['curva'][ip])} exames em {V['dias_periodo'][ip]} "
          f"dias úteis — corresponde a {V['pico_dia']}")
d.replace(p, "entre os polos", "entre as Regiões")
p = d.find("A execução do objeto requer 28.817 horas de sala")
d.replace(p, "28.817 horas de sala no período — 24.317 de ultrassonografia e 4.500",
          f"{n(HUS + HTC)} horas de sala no período — {n(HUS)} de ultrassonografia e {n(HTC)}")
d.sub("os quantitativos diários e os equipamentos de cada polo", "de cada polo", "de cada Região")
t17 = T[17]
d.clone_row(t17, 13, after=0)            # linha "Polos"
set_row(t17, 0, [None, None] + ORD)
set_row(t17, 1, ["Polos", "10"] + [str(POLOS[x]) for x in ORD] + ["subseção 4.2"], novos=set(range(9)))
lin = [
    (2, n(TOTAL), [n(tot[x]) for x in ORD]),
    (3, n(US), [n(V["us"][x]) for x in ORD]),
    (4, n(TC), [n(V["tc"][x]) for x in ORD]),
    (5, n(sum(V["mes_us"].values())), [n(V["mes_us"][x]) for x in ORD]),
    (6, n(sum(V["mes_tc"].values())), [n(V["mes_tc"][x]) for x in ORD]),
    (7, None, [f"{V['dias']} dias úteis"] * 6),
    (9, n(sum(V["dia_us"].values())), [n(V["dia_us"][x]) for x in ORD]),
    (10, n(sum(V["dia_tc"].values())), [n(V["dia_tc"][x]) for x in ORD]),
    (11, str(sum(salas.values())), [str(salas[x]) for x in ORD]),
    (12, None, [str(V["por_sala"][x]) for x in ORD]),
    (13, n(HUS), [n(hus[x]) for x in ORD]),
    (14, f"pelo menos {sum(tomo.values())}", [f"≥ {tomo[x]}" for x in ORD]),
    (16, n(HTC), [n(htc[x]) for x in ORD]),
    (17, str(sum(lotados.values())), [str(lotados[x]) for x in ORD]),
]
for ri, total, cols in lin:
    set_row(t17, ri, [None, total] + cols)
d.replace(cel(t17, 5, 8), "÷ 12 meses", f"÷ {M} meses")
d.replace(cel(t17, 7, 8), "12 meses de 21 dias úteis", f"{M} meses de 21 dias úteis")
d.replace(cel(t17, 9, 8), "÷ 252 dias úteis", f"÷ {V['dias']} dias úteis")
d.replace(cel(t17, 11, 8), "a carga do polo no horário de funcionamento,",
          "a carga da Região no horário de funcionamento, no mínimo uma por polo,")
d.replace(cel(t17, 12, 8), "salas do polo", "salas da Região")
d.replace(cel(t17, 13, 8), "exames do polo", "exames da Região")
d.replace(cel(t17, 14, 8), "um por polo", "pelo menos um por Região, consideradas em conjunto as Regiões Norte e "
          "Leste, e dois na Sudoeste")
d.replace(cel(t17, 16, 8), "exames do polo", "exames da Região")
set_row(t17, 17, ["Postos de trabalho lotados na Região"])
remover_linha(t17, 15, "Exames por tomógrafo")
p = d.find("Ceilândia realiza, por dia útil,")
velho = d.text(p)


def frase(x, primeira):
    s = salas[x]
    us_txt = f"{V['dia_us'][x]} exames de ultrassonografia em {EXT_F[s]} {'sala' if s == 1 else 'salas'}"
    tc_txt = f"{V['dia_tc'][x]} de tomografia computadorizada" if primeira else f"{V['dia_tc'][x]} de tomografia"
    return f"{A[x]}{', por dia útil,' if primeira else ''} {us_txt} e {tc_txt}."


def postos():
    partes = []
    for i, x in enumerate(ORD):
        k = lotados[x]
        quem = "as Regiões Norte e Leste" if x == "Norte e Leste" else f"a Região {x}"
        if i == 0:
            partes.append(f"{quem} {'têm' if x == 'Norte e Leste' else 'tem'} {EXT_M[k]} "
                          f"{'posto' if k == 1 else 'postos'} de gestão e apoio {'lotado' if k == 1 else 'lotados'}")
        else:
            partes.append(f"{quem} {EXT_M[k]}")
    return lista(partes) + "."


d.replace(p, velho, " ".join(frase(x, i == 0) for i, x in enumerate(ORD)) +
          " Os dez polos funcionam dez horas por dia útil; " + postos())
p = d.find("A soma dos polos, de 265 exames")
d.replace(p, "A soma dos polos, de 265 exames de ultrassonografia e 58 de tomografia por dia útil, excede os 315 do "
             "trimestre", f"A soma das Regiões, de {sum(V['dia_us'].values())} exames de ultrassonografia e "
          f"{sum(V['dia_tc'].values())} de tomografia por dia útil, excede os {V['pico_dia']} do período")
d.replace(p, "de cada polo é arredondada", "de cada Região é arredondada")
assert sum(V["dia_us"].values()) + sum(V["dia_tc"].values()) > V["pico_dia"]
p = d.find("Aos catorze postos lotados nos polos")
d.replace(p, "Aos catorze postos lotados nos polos somam-se duas coordenações únicas para os seis",
          f"Aos {EXT_N[sum(lotados.values())]} postos lotados nas Regiões somam-se a direção e duas coordenações "
          "únicas para os dez polos")
p = d.find("A carga agregada de 4.500 horas equivale a")
d.replace(p, d.text(p), "A tomografia em pelo menos um polo de cada Região mantém o exame perto do domicílio do "
          "usuário, e a folga do conjunto absorve a manutenção de cada equipamento.")

# ================= 7.4 a 7.6 desembolso =================
p = d.find("O desembolso é feito em quatro parcelas trimestrais")
d.replace(p, "quatro parcelas trimestrais, correspondentes aos quatro trimestres",
          "três parcelas, duas trimestrais e a última bimestral, correspondentes aos três períodos")
d.sub("As demais são liberadas no início do trimestre a que se referem", "do trimestre", "do período")
t18 = T[18]
for i, (rot, meses, _) in enumerate(PER):
    set_row(t18, i + 1, [None, meses, n(V["curva"][i]), r(V["prod_b"][i]), r(V["apoio_periodo"][i]),
                         r(V["parcelas"][i])])
set_row(t18, 5, [None, None, n(TOTAL), r(PROD), r(APOIO), r(GLOB)])
remover_linha(t18, 4, "4")
d.sub("Os exames de cada parcela são os do trimestre correspondente", "do trimestre", "do período")
d.sub("A produção executada em cada trimestre", "em cada trimestre", "em cada período")

# ================= 7.8 e 7.9 riscos: redacao da v7, numeros novos =================
t19 = T[19]
p = d.find("Capacidade instalada insuficiente para o ritmo de 315", within=t19)
d.replace(p, "315", str(V["pico_dia"]))
d.replace(d.find("redistribuição da agenda entre os seis polos", within=t19), "seis polos", "dez polos")
d.replace(d.find("quantitativo pactuado de 79.357 inclui 785", within=t19), "79.357 inclui 785",
          f"{n(TOTAL)} inclui {n(V['acrescimo'])}")
d.replace(d.find("seis equipamentos para uma carga de 1,79", within=t19), "seis equipamentos para uma carga de 1,79",
          f"{EXT_M[sum(tomo.values())]} equipamentos para uma carga de {dec(V['tomografos_equivalentes'], 2)}")
d.replace(d.find("redistribuição de agenda pela Coordenação Administrativa", within=t19), "Coordenação Administrativa",
          "Coordenação Operacional")
p = d.find("A meta de 79.357 exames em doze meses exige catorze salas")
d.replace(p, "79.357 exames em doze meses exige catorze salas de ultrassonografia e seis tomógrafos",
          f"{n(TOTAL)} exames em {EXT_N[M]} meses exige {EXT_N[sum(salas.values())]} salas de ultrassonografia e "
          f"{EXT_N[sum(tomo.values())]} tomógrafos")
d.sub("é insumo de 12.953 dos 13.681 exames", "12.953 dos 13.681", f"{n(V['contraste'])} dos {n(TC)}")

# ================= 8.2 planilha =================
t21 = T[21]
d.clone_row(t21, 3)                      # 1.1.2 Coordenacao Operacional
q_dir, v_dir, t_dir = POSTO["Direção Executiva de Projeto"]
q_op, v_op, t_op = POSTO["Coordenação Operacional"]
q_as, v_as, t_as = POSTO["Assistente Administrativo"]
q_or, v_or, t_or = POSTO["Operador de registro de sistemas"]
q_af, v_af, t_af = POSTO["Coordenação Administrativa e Financeira"]
q_ac, v_ac, t_ac = POSTO["Assessoria de Prestação de Contas"]
set_row(t21, 3, [None, "Direção Executiva de Projeto", None, None, str(q_dir), f"{M} meses", r(v_dir), r(t_dir)])
set_row(t21, 4, ["1.1.2", "Coordenação Operacional", "4.2 · 4.13", "posto", str(q_op), f"{M} meses", r(v_op), r(t_op)],
        novos=set(range(8)))
m1 = t_dir + t_op
set_row(t21, 5, [None, None, None, None, str(q_dir + q_op), None, None, r(m1)])
set_row(t21, 8, [None, None, None, None, str(q_as), f"{M} meses", None, r(t_as)])
set_row(t21, 9, [None, None, None, None, str(q_as), None, None, r(t_as)])
set_row(t21, 12, [None, None, None, None, str(q_or), f"{M} meses", None, r(t_or)])
set_row(t21, 13, [None, None, None, None, str(q_or), None, None, r(t_or)])
m4 = D(0)
for ri in range(16, 24):
    cod = [c for c in qc if c in d.text(cel(t21, ri, 1))][0]
    v = qc[cod] * UNIT[cod]
    m4 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 24, [None, None, None, None, n(US), None, None, r(m4)])
m5 = D(0)
for ri in range(27, 30):
    cod = [c for c in qc if c in d.text(cel(t21, ri, 1))][0]
    v = qc[cod] * UNIT[cod]
    m5 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 30, [None, None, None, None, n(TC), None, None, r(m5)])
set_row(t21, 33, [None, "Coordenação Administrativa e Financeira", None, None, None, f"{M} meses", r(v_af), r(t_af)])
set_row(t21, 34, [None, None, None, None, None, f"{M} meses", None, r(t_ac)])
m6 = t_af + t_ac
set_row(t21, 35, [None, None, None, None, None, None, None, r(m6)])
total_geral = m1 + t_as + t_or + m4 + m5 + m6
assert total_geral == GLOB, (total_geral, GLOB)
assert m4 + m5 == PROD
set_row(t21, 36, [None, None, None, None, None, None, None, r(total_geral)])
d.sub("Nota ao item 6.1.2.", "com atuação nos doze meses", f"com atuação nos {EXT_N[M]} meses")

# ================= 8.3 consolidacao =================
t22 = T[22]
for ri, v in [(1, m1), (2, t_as), (3, t_or), (4, m4), (5, m5), (6, m6), (7, total_geral)]:
    set_row(t22, ri, [None, r(v)])

d.save()
print(f"{modo}: {len(d.log)} trocas de texto; {n(TOTAL)} exames; global {r(GLOB)}")
