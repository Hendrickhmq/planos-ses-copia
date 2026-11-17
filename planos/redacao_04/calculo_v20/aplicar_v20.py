"""Aplica a v20 sobre a v6 da equipe (PT_simplificado_exames_de_imagem_v6.docx, ja descompactada).

uso: aplicar_v20.py <docx_descompactado> limpo|marcado

So valores e polos (decisao do usuario em 06/10/2026): recurso do Oficio 40/2026, apoio da
opcao C (6 operadores e 8 assistentes) e seis polos. O resto do texto da v6 fica como esta.
"""
import sys, os, json, math, copy
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docxlib import Doc, q, etree

pasta, modo = sys.argv[1], sys.argv[2]
V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v20.json")))
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))


def n(x):
    return f"{int(x):,}".replace(",", ".")


def r(x):
    s = f"{D(str(x)).quantize(D('0.01')):,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def dec(x, k):
    return f"{x:.{k}f}".replace(".", ",")


ORD = V["ORD"]
NOVOS = {"Taguatinga", "Plano Piloto", "Guará"}
REG = {"Ceilândia": "Oeste", "Taguatinga": "Sudoeste", "Sobradinho": "Norte e Leste", "Plano Piloto": "Central",
       "Gama": "Sul", "Guará": "Centro-Sul"}
EM = {"Ceilândia": "em Ceilândia", "Taguatinga": "em Taguatinga", "Sobradinho": "em Sobradinho",
      "Plano Piloto": "no Plano Piloto", "Gama": "no Gama", "Guará": "no Guará"}
LISTA = "Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama e Guará"
qc, tot, us, tc = V["qc"], V["tot"], V["us"], V["tc"]
hus, htc, salas = V["hus"], V["htc"], V["salas"]
UNIT = {"02.05.02.009-7": D("99.94"), "02.05.02.018-6": D("99.94"), "02.05.01.004-0": D("100.18"),
        "02.05.02.004-6": D("100.18"), "02.05.02.005-4": D("99.94"), "02.05.02.012-7": D("99.94"),
        "02.05.02.010-0": D("99.94"), "02.05.02.003-8": D("99.94"), "02.06.03.001-0": D("299.44"),
        "02.06.03.003-7": D("299.44"), "02.06.02.003-1": D("300.10")}
TOTAL, US, TC = V["total"], V["us_total"], V["tc_total"]
APOIO, GLOB, PROD = D(V["apoio"]), D(V["global"]), D(V["producao"])

# participacao por polo: exames do polo / total, arredondada no centesimo (como na v19, que fechava 39,74/30,07/30,19)
PCT = {p: f"{tot[p] / TOTAL * 100:.2f}%".replace(".", ",") for p in ORD}

PALAVRA_F = {1: "uma", 2: "duas", 3: "três", 4: "quatro", 5: "cinco"}
PALAVRA_M = {1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco", 6: "seis"}
lotados = {p: V["operadores"][p] + V["assistentes"][p] for p in ORD}


def set_row(tbl, ri, vals, novos=()):
    cs = d.cells(d.rows(tbl)[ri])
    for ci, v in enumerate(vals):
        if v is None:
            continue
        d.set_cell(cs[ci], v, novo=ci in novos)


def colunas_polo(tbl, primeira):
    """[.., Ceilandia, Sobradinho, Gama, ..] -> [.., Ceilandia, Taguatinga, Sobradinho, Plano Piloto, Gama, Guara, ..];
    devolve os indices das colunas novas"""
    a = primeira
    d.insert_columns(tbl, src=a, after=a, n=1)
    d.insert_columns(tbl, src=a + 2, after=a + 2, n=1)
    d.insert_columns(tbl, src=a + 4, after=a + 4, n=1)
    return {a + 1, a + 3, a + 5}


def cabecalho_vertical(tbl, cols, altura=1250):
    tr = d.rows(tbl)[0]
    trpr = tr.find(q("trPr"))
    if trpr is None:
        trpr = etree.Element(q("trPr"))
        tr.insert(0, trpr)
    h = etree.Element(q("trHeight"))
    h.set(q("val"), str(altura))
    h.set(q("hRule"), "atLeast")
    after = [c for c in trpr if etree.QName(c).localname in ("tblHeader", "tblCellSpacing", "jc", "hidden")]
    (after[0].addprevious(h) if after else trpr.append(h))
    for ci in cols:
        tc = d.cells(tr)[ci]
        tcpr = tc.find(q("tcPr"))
        td = etree.Element(q("textDirection"))
        td.set(q("val"), "btLr")
        later = [c for c in tcpr if etree.QName(c).localname in ("tcFitText", "vAlign", "hideMark")]
        (later[0].addprevious(td) if later else tcpr.append(td))
        for p in tc.findall(q("p")):
            ppr = p.find(q("pPr"))
            jc = ppr.find(q("jc")) if ppr is not None else None
            if jc is not None:
                jc.set(q("val"), "left")


def mover_linha(tbl, de, para):
    rows = d.rows(tbl)
    row = rows[de]
    alvo = rows[para]
    if para < de:
        alvo.addprevious(row)
    else:
        alvo.addnext(row)


T = d.tables()

# ---------------- 1. Informacoes iniciais ----------------
cel = d.find("valor global do plano, dentro do recurso disponível")
d.replace(cel, "R$ 13.095.356,94", f"R$ {r(GLOB)}")
d.replace(cel, "R$ 13.095.449,00 das propostas nº 36000722999202500 e nº 36000720055202500",
          "R$ 11.592.762,00 da proposta nº 36000720055202500")
cel = d.find("com duas propostas reunidas em um único plano de trabalho")
d.replace(cel, ", com duas propostas reunidas em um único plano de trabalho, conforme confirmado com a Assessoria de "
               "Gestão Participativa e Relações Institucionais (ARINS) da SES-DF: Proposta nº 36000722999202500, "
               "R$ 1.502.687,00, com indicação do ISHP pelo Ofício nº 38/2026 do Senado Federal; e Proposta",
          ": Proposta")
d.replace(cel, " Total das duas propostas: R$ 13.095.449,00.", "")
d.replace(cel, "nos ofícios que indicam", "no ofício que indica")
d.sub("Polos de Ceilândia, Sobradinho e Gama", "Ceilândia, Sobradinho e Gama", LISTA)

# ---------------- 2.2 Composicao ----------------
d.sub("O objeto é a realização de 88.518 exames", "88.518", n(TOTAL))
t2 = T[2]
# ordem decrescente, como na v6: a mamaria passa o doppler e o urinario passa a pelve
mover_linha(t2, 2, 1)
mover_linha(t2, 8, 7)
for ri, tr in enumerate(d.rows(t2)[1:12], start=1):
    cod = d.text(d.cells(tr)[0].find(q("p")))
    set_row(t2, ri, [None, None, n(qc[cod])])
set_row(t2, 12, [None, None, n(TOTAL)])
d.sub("São 72.159 exames de ultrassonografia", "72.159", n(US))
d.replace(d.find("exames de ultrassonografia e 16.359 de tomografia computadorizada."), "16.359", n(TC))

# ---------------- 3.1 A fila ----------------
p = d.find("A parceria resolve a totalidade das 78.572 solicitações")
d.replace(p, "atende mais 9.946", f"atende mais {n(V['acrescimo'])}")
d.replace(p, "88.518 exames ao todo", f"{n(TOTAL)} exames ao todo")
t4 = T[4]
for ri, val in [(1, "R$ 11.592.762,00"), (2, f"R$ {r(APOIO)}"), (3, f"R$ {r(V['envelope'])}"),
                (4, f"{n(TOTAL)} exames"), (5, f"R$ {r(PROD)}"), (6, f"R$ {r(GLOB)}"), (7, f"R$ {r(V['sobra'])}")]:
    set_row(t4, ri, [None, val])


# ---------------- 3.4 e 4.2: linhas dos polos ----------------
def linhas_polo(tbl, com_numeros):
    # 1 Ceilandia, 2 Sobradinho, 3 Gama -> clona cada uma para o polo novo que sai dela
    for ri in (3, 2, 1):
        d.clone_row(tbl, ri)
    for ri, polo in enumerate(ORD, start=1):
        novo = polo in NOVOS
        vals = [polo, REG[polo]] + ([PCT[polo], n(tot[polo])] if com_numeros else [])
        set_row(tbl, ri, vals, novos=set(range(len(vals))) if novo else ())
    if com_numeros:
        set_row(tbl, 7, [None, None, None, n(TOTAL)])


linhas_polo(T[5], True)
linhas_polo(T[7], False)

# ---------------- 3.12, 4.2 ----------------
d.sub("compatível com a implantação dos três polos no mês 1", "três polos", "seis polos")
d.sub("A execução ocorre em três polos", "três polos", "seis polos")
d.sub("e os três polos realizam ultrassonografia", "os três polos", "os seis polos")
d.sub("Os polos situam-se nas Regiões Administrativas de Ceilândia, Sobradinho e Gama",
      "Ceilândia, Sobradinho e Gama", LISTA)

# ---------------- 4.8 contraste ----------------
d.sub("são 15.605 dos 16.359 exames de tomografia", "15.605 dos 16.359", f"{n(V['contraste'])} dos {n(TC)}")

# ---------------- 4.13 equipe de gestao e apoio ----------------
set_row(T[9], 3, ["6"])
d.sub("Os sete operadores de registro e os oito assistentes", "Os sete operadores", "Os seis operadores")
d.sub("assistentes administrativos se distribuem entre os três polos", "três polos", "seis polos")
t10 = T[10]
novas = colunas_polo(t10, 1)
d.set_widths(t10, [2870] + [850] * 6 + [1100])
cabecalho_vertical(t10, range(1, 7), altura=1250)
set_row(t10, 0, [None] + ORD, novos=novas)
set_row(t10, 1, [None] + [str(V["operadores"][p]) for p in ORD] + ["6"], novos=novas)
set_row(t10, 2, [None] + [str(V["assistentes"][p]) for p in ORD] + ["8"], novos=novas)
set_row(t10, 3, [None] + [str(lotados[p]) for p in ORD] + [str(sum(lotados.values()))], novos=novas)
d.sub("As duas coordenações são únicas para os três polos", "três polos", "seis polos")

# ---------------- 4.15 equipe assistencial ----------------
t11 = T[11]
novas = colunas_polo(t11, 2)
d.set_widths(t11, [1700, 800] + [560] * 6 + [3210])
cabecalho_vertical(t11, range(2, 8), altura=1250)
mus, rad = V["medicos_us"], V["radiologistas"]
set_row(t11, 0, [None, None] + ORD, novos=novas)
set_row(t11, 1, [None, n(sum(mus.values()))] + [str(mus[p]) for p in ORD], novos=novas)
set_row(t11, 2, [None, n(sum(rad.values()))] + [str(rad[p]) for p in ORD], novos=novas)
set_row(t11, 3, [None, "6 por dia útil"] + ["1"] * 6, novos=novas)
set_row(t11, 4, [None, "6"] + ["1"] * 6, novos=novas)
set_row(t11, 5, [None, "18"] + ["3"] * 6, novos=novas)
set_row(t11, 6, [None, "12"] + ["2"] * 6, novos=novas)
set_row(t11, 7, [None, "12"] + ["2"] * 6, novos=novas)
crit = d.cells(d.rows(t11)[1])[8].find(q("p"))
d.replace(crit, "salas: 5, 4 e 4", "salas: " + ", ".join(str(salas[p]) for p in ORD[:-1]) + f" e {salas[ORD[-1]]}")
crit = d.cells(d.rows(t11)[2])[8].find(q("p"))
d.replace(crit, "2.349, 1.939 e 1.102 ÷ 1.800 h anuais (1,30; 1,08; 0,61)",
          ", ".join(n(htc[p]) for p in ORD[:-1]) + f" e {n(htc[ORD[-1]])} ÷ 1.800 h anuais ("
          + "; ".join(dec(htc[p] / 1800, 2) for p in ORD) + ")")
p = d.find("Ultrassonografia: as 26.760 horas de sala")
d.replace(p, "26.760 horas de sala (10.189 em Ceilândia, 7.855 em Sobradinho e 8.716 no Gama)",
          f"{n(sum(hus.values()))} horas de sala ("
          + ", ".join(f"{n(hus[x])} {EM[x]}" for x in ORD[:-1]) + f" e {n(hus[ORD[-1]])} {EM[ORD[-1]]})")


def med(x):
    k = mus[x]
    return f"{k} {'médico' if k == 1 else 'médicos'} {EM[x]} ({n(hus[x])} ÷ 1.800 = {dec(hus[x] / 1800, 1)})" \
        if x == ORD[0] else f"{k} {EM[x]} ({n(hus[x])} ÷ 1.800 = {dec(hus[x] / 1800, 1)})"


d.replace(p, "6 médicos em Ceilândia (10.189 ÷ 1.800 = 5,7), 5 em Sobradinho (7.855 ÷ 1.800 = 4,4) e 5 no Gama "
             "(8.716 ÷ 1.800 = 4,8), 16 no total, sempre em número igual ou superior ao de salas (5, 4 e 4)",
          ", ".join(med(x) for x in ORD[:-1]) + f" e {med(ORD[-1])}, {sum(mus.values())} no total, sempre em número "
          f"igual ou superior ao de salas (" + ", ".join(str(salas[x]) for x in ORD[:-1]) + f" e {salas[ORD[-1]]})")
d.replace(p, "3 técnicos por tomógrafo e 9 nos três polos", "3 técnicos por tomógrafo e 18 nos seis polos")

# ---------------- 5 Objetivos, 6 Metas ----------------
d.sub("mediante a realização de 88.518 exames", "88.518", n(TOTAL))
t12 = T[12]
d.replace(d.find("coordenar três polos de execução", within=t12), "três polos", "seis polos")
d.replace(d.find("3 polos em operação por 12 meses", within=t12), "3 polos", "6 polos")
d.replace(d.find("88.518 vagas", within=t12), "88.518", n(TOTAL))
d.replace(d.find("88.518 exames registrados", within=t12), "88.518", n(TOTAL))
d.replace(d.find("72.159 exames", within=t12), "72.159", n(US))
d.replace(d.find("16.359 exames", within=t12), "16.359", n(TC))
t13 = T[13]
d.replace(d.find("3 polos em operação a partir do mês 1", within=t13), "3 polos", "6 polos")
d.replace(d.find("88.518 vagas disponibilizadas", within=t13), "88.518", n(TOTAL))
d.replace(d.find("88.518 exames registrados", within=t13), "88.518", n(TOTAL))
d.replace(d.find("72.159 exames", within=t13), "72.159", n(US))
d.replace(d.find("16.359 exames", within=t13), "16.359", n(TC))
d.sub("As Metas 4 e 5 se decompõem por polo",
      "35.174 exames em Ceilândia, 26.617 em Sobradinho e 26.727 no Gama",
      f"{n(tot[ORD[0]])} exames {EM[ORD[0]]}, " + ", ".join(f"{n(tot[x])} {EM[x]}" for x in ORD[1:-1])
      + f" e {n(tot[ORD[-1]])} {EM[ORD[-1]]}")

# ---------------- 7.1, 7.2 ----------------
d.replace(d.find("publicação das agendas dos três polos", within=T[15]), "três polos", "seis polos")
t16 = T[16]
for ri, k in enumerate(V["curva"], start=1):
    set_row(t16, ri, [None, None, n(k)])
set_row(t16, 5, [None, None, n(TOTAL)])

# ---------------- 7.3 capacidade ----------------
p = d.find("A produção do trimestre de maior carga, de 22.132 exames")
d.replace(p, "22.132", n(max(V["curva"])))
d.replace(p, "352 exames por dia útil", f"{V['pico_dia']} exames por dia útil")
p = d.find("A execução do objeto requer 32.150 horas de sala")
HUS, HTC = sum(hus.values()), sum(htc.values())
d.replace(p, "32.150", n(HUS + HTC))
d.replace(p, "26.760 de ultrassonografia e 5.390", f"{n(HUS)} de ultrassonografia e {n(HTC)}")
t17 = T[17]
novas = colunas_polo(t17, 2)
d.set_widths(t17, [1900, 780] + [720] * 6 + [2070])
cabecalho_vertical(t17, range(2, 8), altura=1250)
mus_, mtc_, dus_, dtc_ = V["mes_us"], V["mes_tc"], V["dia_us"], V["dia_tc"]
linhas = [
    (0, [None, None] + ORD),
    (1, [None, n(TOTAL)] + [n(tot[x]) for x in ORD]),
    (2, [None, n(US)] + [n(us[x]) for x in ORD]),
    (3, [None, n(TC)] + [n(tc[x]) for x in ORD]),
    (4, [None, n(sum(mus_.values()))] + [n(mus_[x]) for x in ORD]),
    (5, [None, n(sum(mtc_.values()))] + [n(mtc_[x]) for x in ORD]),
    (6, [None, None] + ["252 dias úteis"] * 6),
    (7, [None, None] + ["10 horas por dia útil"] * 6),
    (8, [None, n(sum(dus_.values()))] + [n(dus_[x]) for x in ORD]),
    (9, [None, n(sum(dtc_.values()))] + [n(dtc_[x]) for x in ORD]),
    (10, [None, n(sum(salas.values()))] + [str(salas[x]) for x in ORD]),
    (11, [None, None] + [str(V["por_sala"][x]) for x in ORD]),
    (12, [None, n(HUS)] + [n(hus[x]) for x in ORD]),
    (13, [None, "6"] + ["1"] * 6),
    (14, [None, None] + [str(dtc_[x]) for x in ORD]),
    (15, [None, n(HTC)] + [n(htc[x]) for x in ORD]),
    (16, [None, str(sum(lotados.values()))] + [str(lotados[x]) for x in ORD]),
]
for ri, vals in linhas:
    set_row(t17, ri, vals, novos=novas)
p = d.find("Ceilândia realiza, por dia útil,")
velho = d.text(p)


def frase_polo(x, primeira):
    art = {"Plano Piloto": "O Plano Piloto", "Gama": "O Gama", "Guará": "O Guará"}.get(x, x)
    s = salas[x]
    us_txt = f"{dus_[x]} exames de ultrassonografia em {PALAVRA_F[s]} {'sala' if s == 1 else 'salas'}"
    tc_txt = f"{dtc_[x]} de tomografia computadorizada" if primeira else f"{dtc_[x]} de tomografia"
    return f"{art} realiza{', por dia útil,' if primeira else ''} {us_txt} e {tc_txt} em um tomógrafo."


def postos_txt():
    partes = []
    for i, x in enumerate(ORD):
        k = lotados[x]
        nome = {"Plano Piloto": "o Plano Piloto", "Gama": "o Gama", "Guará": "o Guará"}.get(x, x)
        if i == 0:
            partes.append(f"{nome} tem {PALAVRA_M[k]} {'posto' if k == 1 else 'postos'} de gestão e apoio "
                          f"{'lotado' if k == 1 else 'lotados'}")
        else:
            partes.append(f"{nome} {PALAVRA_M[k]}")
    return ", ".join(partes[:-1]) + " e " + partes[-1] + "."


novo = " ".join(frase_polo(x, i == 0) for i, x in enumerate(ORD)) + \
    " Os seis polos funcionam dez horas por dia útil; " + postos_txt()
d.replace(p, velho, novo)
p = d.find("A soma dos polos, de 288 exames de ultrassonografia")
d.replace(p, "288 exames de ultrassonografia e 67 de tomografia", f"{sum(dus_.values())} exames de ultrassonografia "
          f"e {sum(dtc_.values())} de tomografia")
d.replace(p, "excede os 352", f"excede os {V['pico_dia']}")
assert sum(dus_.values()) + sum(dtc_.values()) > V["pico_dia"]
p = d.find("Aos quinze postos lotados nos polos")
d.replace(p, "Aos quinze postos", "Aos catorze postos")
d.replace(p, "únicas para os três", "únicas para os seis")
p = d.find("A carga agregada de 5.390 horas")
d.replace(p, "5.390 horas equivale a 2,14 tomógrafos", f"{n(HTC)} horas equivale a "
          f"{dec(V['tomografos_equivalentes'], 2)} tomógrafo")
d.replace(p, ", e concentrá-la em dois polos elevaria a carga do polo receptor acima da capacidade de um equipamento "
             "— o que exigiria o terceiro assim mesmo, e faria o usuário do Gama atravessar o Distrito Federal", "")

# ---------------- 7.5 parcelas ----------------
t18 = T[18]
apoio_tri = APOIO / 4
for ri in range(4):
    set_row(t18, ri + 1, [None, None, n(V["curva"][ri]), r(V["prod_tri"][ri]), r(apoio_tri), r(V["parcelas"][ri])])
set_row(t18, 5, [None, None, n(TOTAL), r(PROD), r(APOIO), r(GLOB)])

# ---------------- 7.8 e 7.9 riscos ----------------
t19 = T[19]
p = d.find("Capacidade instalada insuficiente para o ritmo de 352", within=t19)
d.replace(p, "352", str(V["pico_dia"]))
d.replace(d.find("redistribuição da agenda entre os três polos", within=t19), "três polos", "seis polos")
p = d.find("a fila apurada na subseção 3.1 é de 78.572", within=t19)
d.replace(p, "quantitativo pactuado de 88.518 inclui 9.946", f"quantitativo pactuado de {n(TOTAL)} inclui "
          f"{n(V['acrescimo'])}")
d.replace(d.find("três equipamentos para uma carga de 2,14", within=t19), "três equipamentos para uma carga de 2,14",
          f"seis equipamentos para uma carga de {dec(V['tomografos_equivalentes'], 2)}")
p = d.find("A meta de 88.518 exames em doze meses exige treze salas")
d.replace(p, "88.518 exames em doze meses exige treze salas de ultrassonografia e três tomógrafos",
          f"{n(TOTAL)} exames em doze meses exige catorze salas de ultrassonografia e seis tomógrafos")
d.sub("é insumo de 15.605 dos 16.359 exames", "15.605 dos 16.359", f"{n(V['contraste'])} dos {n(TC)}")

# ---------------- 8.1 valor unitario: mesma ordem da 2.2 ----------------
t20 = T[20]
mover_linha(t20, 2, 1)
mover_linha(t20, 8, 7)

# ---------------- 8.2 planilha ----------------
t21 = T[21]
set_row(t21, 11, [None, None, None, None, "6", None, None, r(D("4300.00") * 6 * 12)])
set_row(t21, 12, [None, None, None, None, "6", None, None, r(D("4300.00") * 6 * 12)])
mover_linha(t21, 16, 15)   # mamaria antes do doppler
set_row(t21, 15, ["4.1.1"])
set_row(t21, 16, ["4.1.2"])
m4 = D(0)
for ri in range(15, 23):
    cod = [c for c in qc if c in d.text(d.cells(d.rows(t21)[ri])[1].find(q("p")))][0]
    v = qc[cod] * UNIT[cod]
    m4 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 23, [None, None, None, None, n(US), None, None, r(m4)])
m5 = D(0)
for ri in range(26, 29):
    cod = [c for c in qc if c in d.text(d.cells(d.rows(t21)[ri])[1].find(q("p")))][0]
    v = qc[cod] * UNIT[cod]
    m5 += v
    set_row(t21, ri, [None, None, None, None, n(qc[cod]), None, None, r(v)])
set_row(t21, 29, [None, None, None, None, n(TC), None, None, r(m5)])
m3 = D("4300.00") * 6 * 12
total_geral = D("126000.00") + D("307200.00") + m3 + m4 + m5 + D("179460.00")
assert total_geral == GLOB, (total_geral, GLOB)
assert m4 + m5 == PROD
set_row(t21, 35, [None, None, None, None, None, None, None, r(total_geral)])

# ---------------- 8.3 consolidacao ----------------
t22 = T[22]
set_row(t22, 3, [None, r(m3)])
set_row(t22, 4, [None, r(m4)])
set_row(t22, 5, [None, r(m5)])
set_row(t22, 7, [None, r(total_geral)])

# ---------------- remissoes erradas na renumeracao da v6 (usuario, 06/10/2026) ----------------
def remissao(p, velha, nova):
    txt = d.text(p)
    d.replace(p, velha, nova, desde=txt.index(f"subseção {velha}") + len("subseção "))


remissao(d.find("reapresentação dos rejeitados, na forma da subseção 8.2", within=T[13]), "8.2", "9.2")
remissao(d.find("perfis de acesso por posto de trabalho, na forma da subseção 8.3", within=T[19]), "8.3", "9.3")
t8 = T[8]
assert d.text(d.cells(d.rows(t8)[10])[0].find(q("p"))).startswith("10. Conclusão")
set_row(t8, 10, [None, None, None, "4.11"])

d.save()
print(f"{modo}: {len(d.log)} trocas de texto; global {r(GLOB)}; {n(TOTAL)} exames")
