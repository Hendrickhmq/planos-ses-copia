"""Estudo de imagem pela Tabela SUS Candanga: filas do Mapa Social (29/10/2026) x Anexo Único.

Uso: python3 gerar_estudo.py <filas_20261029.csv> <candanga.csv> <v25.json> <saida.xlsx>
"""
import csv, json, sys, unicodedata, collections
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

filas_csv, cand_csv, v25_json, saida = sys.argv[1:5]

cand, cand_nome = {}, {}
for x in csv.DictReader(open(cand_csv, encoding="utf-8")):
    if x["modalidade"] == "SIA":
        cand[x["codigo_sigtap"]] = float(x["valor"])
        cand_nome[x["codigo_sigtap"]] = x["procedimento"]

# valor do plano 4 (Portaria SAES/MS 4.282/2026: tabela x incremento, truncado)
PLANO4 = {"02.05.02.009-7": 99.94, "02.05.01.004-0": 100.18, "02.05.02.004-6": 100.18,
          "02.05.02.018-6": 99.94, "02.05.02.005-4": 99.94, "02.05.02.012-7": 99.94,
          "02.05.02.010-0": 99.94, "02.05.02.003-8": 99.94, "02.06.03.001-0": 299.44,
          "02.06.03.003-7": 299.44, "02.06.02.003-1": 300.10}
v25 = json.load(open(v25_json))
qc4 = v25["qc"]

linhas = [x for x in csv.DictReader(open(filas_csv, encoding="utf-8-sig"), delimiter=";")
          if x["escopo"] == "exame" and int(x["fila"] or 0) > 0]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def tem(n, *ps):
    return any(p in n for p in ps)


IEV = "PARTES MOLES"
DIRETO, AGRUP, CONF = "Direto", "Agrupado pela SES no código", "Código a conferir"


def enquadra(nome, cod):
    """(categoria, observação) do nome da fila contra o procedimento do código."""
    n = sem_acento(nome)
    if cod not in cand:
        return "Fora da Candanga", "Código fora do Anexo Único: vale o SIGTAP da ficha."
    if cod == "02.05.02.006-2":
        if tem(n, "PELVICA"):
            return CONF, "US pélvica cadastrada no código de articulação; o código próprio é 02.05.02.016-0 (R$ 43,41)."
        if tem(n, "DOPPLER"):
            return CONF, "Doppler cadastrado no código de articulação; o código de Doppler é 02.05.01.004-0 (R$ 115,61)."
        if tem(n, IEV, "INGUINAL", "AXILA", "GLUTEA", "PESCOCO", "CERVICAL", "LOMBAR",
               "GLANDULAS", "SUPERFICIE", "BACIA"):
            return AGRUP, "Região de partes moles, sem código próprio no SIGTAP: a SES registra como US de articulação (R$ 70,97)."
        if tem(n, "ARTICULACAO", "QUADRIL", "OMBRO") and not tem(n, "COXA ESQ", "COXA DIR"):
            return DIRETO, ""
        return AGRUP, "Segmento de membro (mão, pé, braço, perna, dedo, tendão) registrado como US de articulação."
    if cod == "02.05.02.004-6" and tem(n, "PAREDE"):
        return AGRUP, "Parede abdominal registrada como abdômen total: paga R$ 117,51, mais do que um US de região isolada."
    if cod == "02.05.02.012-7" and tem(n, "DOPPLER"):
        return AGRUP, "Doppler de tireoide pago como US de tireoide simples (R$ 64,07), não como Doppler (R$ 115,61)."
    if cod == "02.05.01.004-0":
        if tem(n, "TRANSVAGINAL"):
            return AGRUP, "Transvaginal com Doppler registrada só como Doppler de vasos."
        if tem(n, "PAROTIDA"):
            return CONF, "Parótidas (glândula, sem Doppler no nome) no código de Doppler de vasos."
        if tem(n, "BOLSA ESCROTAL"):
            return AGRUP, "Bolsa escrotal com Doppler no código de Doppler; a mesma fila aparece também no 02.05.02.007-0."
        return DIRETO, "Doppler de vasos: 1 unidade por exame, qualquer que seja o número de vasos (ficha SIGTAP 10/2026)."
    if cod == "02.05.02.007-0" and tem(n, "DOPPLER"):
        return AGRUP, "Doppler de bolsa escrotal pago como US de bolsa escrotal (R$ 100,00)."
    if cod == "02.05.02.014-3" and tem(n, "MORFOLOG"):
        return AGRUP, "US morfológica paga como obstétrica simples (R$ 62,22)."
    if cod.startswith("02.06"):
        if tem(n, "CORONARIA"):
            return AGRUP, "Angiotomografia de coronárias sem código próprio: registrada como TC de tórax (R$ 309,25), abaixo do custo de mercado."
        if tem(n, "ANGIOTOMOGRAFIA"):
            return AGRUP, "Angiotomografia sem código próprio no SIA: registrada como TC da região (contraste incluso, sem cobrança à parte)."
        if cod == "02.06.01.006-0" and tem(n, "ORBITA"):
            return AGRUP, "TC de órbitas registrada como TC de sela túrcica (R$ 371,02)."
        if cod == "02.06.01.004-4" and tem(n, "MASTOIDE", "OUVIDO"):
            return AGRUP, "Mastoides/ouvidos registrados como TC de face."
        if cod == "02.06.02.001-5" and tem(n, "SACRO"):
            return CONF, "Sacro-ilíaca no código de articulações de membro superior."
        if cod == "02.06.03.002-9" and tem(n, " PE ", "CALCANEO"):
            return AGRUP, "Pé/calcâneo em articulações de membro inferior; outras filas de pé usam segmentos apendiculares (02.06.02.002-3). Mesmo valor."
        return DIRETO, ""
    return DIRETO, ""


CBR = "CBR 2017"
HIP = "hipótese (plano 4)"


def tempo(nome, cod):
    """(grupo, minutos de agendamento, base, nota). US: Recomendação CBR de 14/11/2017. TC: intervalos do plano 4."""
    n = sem_acento(nome)
    if cod == "02.05.01.004-0":
        if tem(n, "VENOSO") and tem(n, "MMII", "MMSS", "BILATERAL"):
            return ("Doppler venoso de membros, bilateral", 40, CBR, "2 × 20 min (o CBR é por membro); fatura 1 unidade: a ficha diz que a quantidade independe dos vasos estudados")
        if tem(n, "ARTERIAL") and tem(n, "MMII", "MMSS", "BILATERAL"):
            return ("Doppler arterial de membros, bilateral", 40, CBR, "2 × 20 min (o CBR é por membro); fatura 1 unidade: a ficha diz que a quantidade independe dos vasos estudados")
        if tem(n, "VENOSO", "ARTERIAL", " MI", "M I", "M S"):
            return ("Doppler de um membro", 20, CBR, "")
        if tem(n, "CAROTIDA", "VERTEBR"):
            return ("Doppler de carótidas e vertebrais", 20, CBR, "bilateral num item só no CBR")
        if tem(n, "RENAIS"):
            return ("Doppler de aorta e artérias renais", 30, CBR, "")
        if tem(n, "TRANSVAGINAL"):
            return ("Transvaginal com Doppler", 20, CBR, "Doppler de órgão isolado")
        return ("Doppler, outros", 20, CBR, "Doppler de órgão ou estrutura isolada")
    if cod == "02.05.01.005-9":
        return ("Doppler de fluxo obstétrico", 25, CBR, "obstétrica com Doppler")
    if cod == "02.05.02.004-6":
        if tem(n, "PAREDE"):
            return ("Parede abdominal", 15, CBR, "estruturas superficiais; paga como abdômen total")
        return ("Abdômen total", 20, CBR, "")
    if cod == "02.05.02.006-2":
        if tem(n, IEV):
            return ("Partes moles (IEV)", 15, CBR, "dermatológico/estruturas superficiais")
        if tem(n, "INGUINAL", "AXILA", "GLUTEA", "PESCOCO", "CERVICAL", "LOMBAR", "GLANDULAS", "SUPERFICIE", "BACIA", "DEDO", "TENDAO", "CALCANEO"):
            return ("Partes moles por região", 15, CBR, "estruturas superficiais")
        if tem(n, "PELVICA", "DOPPLER"):
            return ("Articulação: código a conferir", 15, CBR, "")
        return ("Articulação e segmentos", 15, CBR, "por articulação")
    if cod == "02.05.02.012-7":
        if tem(n, "DOPPLER"):
            return ("Doppler de tireoide", 20, CBR, "Doppler de órgão isolado; paga como tireoide simples")
        return ("Tireoide", 15, CBR, "órgãos superficiais")
    if cod == "02.05.02.007-0":
        if tem(n, "DOPPLER"):
            return ("Bolsa escrotal com Doppler", 20, CBR, "Doppler de órgão isolado")
        return ("Bolsa escrotal", 15, CBR, "órgãos superficiais")
    if cod == "02.05.02.014-3":
        if tem(n, "MORFOLOG") and tem(n, "1"):
            return ("Obstétrica morfológica 1º trimestre", 20, CBR, "translucência nucal; paga como obstétrica simples")
        if tem(n, "MORFOLOG"):
            return ("Obstétrica morfológica", 45, CBR, "paga como obstétrica simples")
        return ("Obstétrica", 20, CBR, "")
    us = {"02.05.02.009-7": ("Mamas", 20, ""), "02.05.02.018-6": ("Transvaginal", 15, ""),
          "02.05.02.005-4": ("Aparelho urinário", 15, ""), "02.05.02.010-0": ("Próstata abdominal", 15, ""),
          "02.05.02.003-8": ("Abdômen superior", 15, ""), "02.05.02.016-0": ("Pélvica (ginecológica)", 15, "abdome inferior feminino"),
          "02.05.02.017-8": ("Transfontanela", 25, "crânio para criança"), "02.05.02.015-1": ("Obstétrica com Doppler", 25, ""),
          "02.05.02.011-9": ("Próstata transretal", 15, ""), "02.05.02.013-5": ("Tórax extracardíaco", 15, ""),
          "02.05.02.008-9": ("Globo ocular", 15, "")}
    if cod in us:
        g, m, nt = us[cod]
        return (g, m, CBR, nt)
    if cod.startswith("02.06"):
        reg = cand_nome.get(cod, cod).replace("TOMOGRAFIA COMPUTADORIZADA ", "").lower()
        reg = reg.split(" c/ ou")[0].removeprefix("de ").removeprefix("do ")
        if tem(n, "CORONARIA"):
            return ("TC angio de coronárias", 30, "hipótese", "preparo e aquisição mais longos; validar com a clínica")
        if tem(n, "ANGIOTOMOGRAFIA"):
            return (f"TC angio — {reg}", 20, HIP, "como TC com contraste")
        contraste = tem(n, "C/CONTRASTE", "C/ CONTRASTE")
        if tem(n, "EMERG"):
            return (f"TC {'com' if contraste else 'sem'} contraste, emergência — {reg}", 20 if contraste else 15, HIP, "fora do perfil eletivo")
        if contraste:
            return (f"TC com contraste — {reg}", 20, HIP, "")
        return (f"TC sem contraste — {reg}", 15, HIP, "")
    return ("outros", None, "", "")


def flags(nome):
    n = sem_acento(nome)
    f = []
    if tem(n, "C/CONTRASTE", "C/ CONTRASTE", "C/CONTRASTE", "ANGIOTOMOGRAFIA"):
        f.append("contraste")
    if tem(n, "C/SEDACAO", "C/ SEDACAO"):
        f.append("sedação")
    if tem(n, "EMERG"):
        f.append("emergência")
    if tem(n, "INFANTIL", "INFAN.", "TRANSFONTANELA"):
        f.append("infantil")
    return ", ".join(f)


# ---------- estilos
VERM = Font(color="C00000", bold=True)
VERM_FILL = PatternFill("solid", fgColor="FDE2E2")
CAB = Font(bold=True, color="FFFFFF")
CAB_FILL = PatternFill("solid", fgColor="1F4E79")
TOT = Font(bold=True)
BRL = '"R$" #,##0.00'
INT = "#,##0"


def folha(wb, titulo, cab, larg):
    ws = wb.create_sheet(titulo)
    ws.append(cab)
    for c in ws[1]:
        c.font, c.fill = CAB, CAB_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    return ws


def formatar(ws, fmt):
    for row in ws.iter_rows(min_row=2):
        for c, f in zip(row, fmt):
            if f:
                c.number_format = f


# Regera só as abas deste script; as abas de outros (ex.: "8 Achados Codex") ficam como estão.
PROPRIAS = ["Leia", "0 Modalidades", "1 Panorama todas", "2 US e TC por fila", "3 US e TC por código",
            "4 Plano 4 pela Candanga", "5 Enquadramento", "6 Valor por hora", "7 Quatro critérios"]
if os.path.exists(saida):
    wb = load_workbook(saida)
    for nome in PROPRIAS:
        if nome in wb.sheetnames:
            del wb[nome]
else:
    wb = Workbook()
    del wb[wb.active.title]
leia = wb.create_sheet("Leia")

# ---------- 1. Panorama de todas as modalidades, por código
mods = collections.defaultdict(lambda: [0, 0, 0, 0.0, set(), set()])
porcod = collections.defaultdict(lambda: {"fila": 0, "viva": 0, "nomes": 0, "mod": ""})
for x in linhas:
    c = x["codigo_formatado"]
    p = porcod[(x["modalidade"], c)]
    p["fila"] += int(x["fila"]); p["viva"] += int(x["fila_viva"]); p["nomes"] += 1
ws = folha(wb, "1 Panorama todas", ["Modalidade", "Código", "Procedimento na Candanga", "Filas (nomes)",
                                  "Pendentes", "Pendentes últimos 24 meses", "Candanga SIA (R$)",
                                  "Valor da fila de 24 meses (R$)", "Na Candanga?"],
           [26, 16, 60, 9, 11, 13, 13, 18, 22])
for (m, c), p in sorted(porcod.items(), key=lambda kv: (kv[0][0], -kv[1]["fila"])):
    v = cand.get(c)
    ws.append([m, c, cand_nome.get(c, "(fora do Anexo: vale SIGTAP)"), p["nomes"], p["fila"], p["viva"],
               v, round(p["viva"] * v, 2) if v else None, "sim" if v else "não, SIGTAP"])
    mo = mods[m]; mo[0] += p["nomes"]; mo[1] += p["fila"]; mo[2] += p["viva"]
    if v: mo[3] += p["viva"] * v
    else: mo[4].add(c)
formatar(ws, [None, None, None, INT, INT, INT, BRL, BRL, None])
ws.auto_filter.ref = ws.dimensions

import pathlib
cons = json.load(open(pathlib.Path(filas_csv).with_name("consolidado_20261029.json"), encoding="utf-8"))
distinto = {g["modalidade"]: g["total"]["fila"] for g in cons["grupos"] if g["escopo"] == "exame"}
ws0 = folha(wb, "0 Modalidades", ["Modalidade", "Filas com pendentes", "Pendentes (soma das filas)",
                                 "Pendentes últimos 24 meses", "Valor Candanga da fila de 24 meses (R$)",
                                 "Códigos fora da Candanga", "Pendentes distintos (união no motor)"],
            [28, 12, 14, 14, 22, 30, 16])
tot = [0, 0, 0, 0.0]
for m, mo in sorted(mods.items(), key=lambda kv: -kv[1][1]):
    ws0.append([m, mo[0], mo[1], mo[2], round(mo[3], 2), ", ".join(sorted(mo[4])) or "—", distinto.get(m)])
    for i in range(4): tot[i] += mo[i]
ws0.append(["Total", tot[0], tot[1], tot[2], round(tot[3], 2), "", distinto.get("TOTAL EXAMES")])
for c in ws0[ws0.max_row]: c.font = TOT
formatar(ws0, [None, INT, INT, INT, BRL, None, INT])
ws0.append([])
ws0.append(["A soma das filas pode passar do total distinto: no ultrassom, 82.983 na soma e 82.981 pedidos distintos. Pessoas não se somam entre filas."])

def tempo_cols(nome, cod):
    g, m, _, _ = tempo(nome, cod)
    v = cand.get(cod)
    return g, m, round(v * 60 / m, 2) if v and m else None


# ---------- 2. US e TC por fila
ust = [x for x in linhas if x["modalidade"] in ("Ultrassonografia e Doppler", "Tomografia")]
ws2 = folha(wb, "2 US e TC por fila", ["Modalidade", "Código", "Nome da fila (exato)", "Pendentes",
                                       "Pendentes 24 meses", "Pessoas 24 meses", "Devolvidas",
                                       "Espera média (dias)", "Pedido mais antigo", "Candanga SIA (R$)",
                                       "Valor da fila de 24 meses (R$)", "No plano 4?", "Marcas",
                                       "Enquadramento", "Observação", "IEV", "Grupo de tempo", "Minutos de agendamento",
                                       "R$ por hora de sala"],
           [12, 15, 62, 10, 11, 11, 10, 10, 12, 11, 15, 9, 22, 24, 70, 6, 34, 11, 12])
cont = collections.Counter(); cont_viva = collections.Counter()
for x in sorted(ust, key=lambda x: (x["modalidade"] != "Ultrassonografia e Doppler", -int(x["fila"]))):
    c = x["codigo_formatado"]; v = cand.get(c)
    cat, obs = enquadra(x["nome"], c)
    iev = IEV in sem_acento(x["nome"])
    cont[cat] += int(x["fila"]); cont_viva[cat] += int(x["fila_viva"])
    ws2.append(["US" if x["modalidade"].startswith("Ultra") else "TC", c, x["nome"].strip(), int(x["fila"]),
                int(x["fila_viva"]), int(x["pessoas_viva"] or 0), int(x["devolvidas"] or 0),
                round(float(x["espera_media"]), 0) if x["espera_media"] else None, x["mais_antiga"],
                v, round(int(x["fila_viva"]) * v, 2) if v else None, "sim" if c in PLANO4 else "",
                flags(x["nome"]), cat, obs, "IEV" if iev else ""] + list(tempo_cols(x["nome"], c)))
    if iev:
        for cell in ws2[ws2.max_row]:
            cell.font, cell.fill = VERM, VERM_FILL
formatar(ws2, [None, None, None, INT, INT, INT, INT, INT, None, BRL, BRL] + [None] * 6 + [INT, BRL])
ws2.auto_filter.ref = ws2.dimensions

# ---------- 3. US e TC por código
agg = collections.defaultdict(lambda: {"fila": 0, "viva": 0, "iev": 0, "iev_viva": 0, "nomes": 0, "agr": 0, "conf": 0})
for x in ust:
    a = agg[x["codigo_formatado"]]; a["fila"] += int(x["fila"]); a["viva"] += int(x["fila_viva"]); a["nomes"] += 1
    cat, _ = enquadra(x["nome"], x["codigo_formatado"])
    if cat == AGRUP: a["agr"] += int(x["fila_viva"])
    if cat == CONF: a["conf"] += int(x["fila_viva"])
    if IEV in sem_acento(x["nome"]):
        a["iev"] += int(x["fila"]); a["iev_viva"] += int(x["fila_viva"])
ws3 = folha(wb, "3 US e TC por código", ["Código", "Procedimento na Candanga", "Filas", "Pendentes",
                                         "Pendentes 24 meses", "dos quais partes moles (IEV), 24 meses",
                                         "24 meses sem partes moles", "Candanga SIA (R$)", "Plano 4, Portaria (R$)",
                                         "Diferença por exame (R$)", "Diferença (%)",
                                         "Valor 24 meses sem partes moles (R$)",
                                         "24 meses em filas agrupadas", "24 meses em filas a conferir"],
           [15, 58, 7, 10, 11, 14, 13, 11, 12, 12, 9, 18, 12, 12])
for c, a in sorted(agg.items(), key=lambda kv: -kv[1]["viva"] * cand.get(kv[0], 0)):
    v = cand.get(c); p4 = PLANO4.get(c)
    sem = a["viva"] - a["iev_viva"]
    ws3.append([c, cand_nome.get(c, ""), a["nomes"], a["fila"], a["viva"], a["iev_viva"] or None, sem, v, p4,
                round(v - p4, 2) if p4 else None, (v - p4) / p4 if p4 else None,
                round(sem * v, 2) if v else None, a["agr"] or None, a["conf"] or None])
    if a["iev_viva"]:
        ws3.cell(ws3.max_row, 6).font = VERM
        ws3.cell(ws3.max_row, 6).fill = VERM_FILL
formatar(ws3, [None, None, INT, INT, INT, INT, INT, BRL, BRL, BRL, "0.0%", BRL, INT, INT])

# ---------- 4. Plano 4 repreçado
ws4 = folha(wb, "4 Plano 4 pela Candanga", ["Código", "Procedimento", "Exames no plano 4 (v26)",
                                            "Portaria (R$)", "Candanga (R$)", "Plano 4 pela Portaria (R$)",
                                            "Mesmos exames pela Candanga (R$)", "Diferença (R$)", "Diferença (%)"],
           [15, 50, 12, 11, 11, 17, 17, 15, 9])
t = [0, 0.0, 0.0]
for c, q in sorted(qc4.items(), key=lambda kv: -kv[1]):
    a, b = round(q * PLANO4[c], 2), round(q * cand[c], 2)
    ws4.append([c, cand_nome[c], q, PLANO4[c], cand[c], a, b, round(b - a, 2), (b - a) / a])
    t[0] += q; t[1] += a; t[2] += b
ws4.append(["Total", "", t[0], None, None, round(t[1], 2), round(t[2], 2), round(t[2] - t[1], 2), (t[2] - t[1]) / t[1]])
for c in ws4[ws4.max_row]: c.font = TOT
formatar(ws4, [None, None, INT, BRL, BRL, BRL, BRL, BRL, "0.0%"])

# ---------- 5. Enquadramento, resumo
ws5 = folha(wb, "5 Enquadramento", ["Categoria", "Pendentes US e TC", "Pendentes 24 meses", "O que quer dizer"],
            [30, 14, 14, 100])
DESC = {DIRETO: "O nome da fila é o procedimento do código; o código está no Anexo Único (SIA). Preço = Candanga.",
        AGRUP: "A fila é de um exame que não tem código próprio, ou que a SES registra num código mais geral. Está na Candanga pelo código, mas o plano precisa dizer o enquadramento (nome da fila → código) e o valor pode não refletir o exame (ex.: angiotomografia de coronárias a R$ 309,25).",
        CONF: "O código cadastrado não parece o do exame. Antes de entrar no plano, conferir na ficha SIGTAP e com a regulação qual código a SES fatura.",
        "Fora da Candanga": "O código não está no Anexo Único: vale o SIGTAP da ficha."}
for k in (DIRETO, AGRUP, CONF, "Fora da Candanga"):
    ws5.append([k, cont.get(k, 0), cont_viva.get(k, 0), DESC[k]])
    ws5.cell(ws5.max_row, 4).alignment = Alignment(wrap_text=True, vertical="top")
formatar(ws5, [None, INT, INT, None])
ws5.append([])
ws5.append(["Itens que a Candanga não paga à parte"])
ws5.cell(ws5.max_row, 1).font = TOT
for a, b in [("Contraste", "02.06.03.004-5 não está no Anexo Único. A TC com contraste recebe só o valor da TC (R$ 309,25 ou o da região); o contraste é custo dentro do exame."),
             ("Sedação", "Nenhum código de sedação nas filas; as filas C/SEDACAO pagam só a TC."),
             ("Bilateral / mais de um vaso", "Doppler venoso ou arterial de MMII bilateral e carótidas + vertebrais são 1 unidade do 02.05.01.004-0: a descrição SIGTAP (10/2026) diz que a quantidade independe da quantidade de vasos estudados."),
             ("Emergência", "Filas EMERG estão no mesmo código e valor; o preço não muda, mas o perfil não é eletivo.")]:
    ws5.append([a, None, None, b])
    ws5.cell(ws5.max_row, 4).alignment = Alignment(wrap_text=True, vertical="top")

# ---------- 6. Valor por hora
grp = collections.OrderedDict()
for x in ust:
    c = x["codigo_formatado"]
    g, m, base, nota = tempo(x["nome"], c)
    k = (g, c)
    if k not in grp:
        grp[k] = {"m": m, "base": base, "nota": nota, "viva": 0, "fila": 0, "filas": 0}
    grp[k]["viva"] += int(x["fila_viva"]); grp[k]["fila"] += int(x["fila"]); grp[k]["filas"] += 1
ws6 = folha(wb, "6 Valor por hora", ["Modalidade", "Exame (grupo de filas)", "Código", "Filas", "Pendentes 24 meses",
                                     "Candanga (R$)", "Minutos de agendamento (editável)", "Unidades faturadas por exame (editável)",
                                     "Exames por hora", "R$ por hora de sala (Candanga)", "Portaria plano 4 (R$)",
                                     "R$ por hora pela Portaria", "Base do tempo", "Nota"],
            [8, 40, 15, 6, 11, 11, 13, 13, 9, 14, 11, 13, 16, 70])
AMAR = PatternFill("solid", fgColor="FFF2CC")
ordem = sorted(grp.items(), key=lambda kv: (not kv[0][1].startswith("02.05"),
                                           -(cand.get(kv[0][1], 0) * 60 / kv[1]["m"]) if kv[1]["m"] else 0))
for (g, c), d in ordem:
    if d["viva"] < 5:
        continue
    r = ws6.max_row + 1
    v = cand.get(c); p4 = PLANO4.get(c)
    ws6.append(["US" if c.startswith("02.05") else "TC", g, c, d["filas"], d["viva"], v, d["m"], 1,
                f"=60/G{r}", f"=F{r}*H{r}*60/G{r}", p4, f"=K{r}*H{r}*60/G{r}" if p4 else None, d["base"], d["nota"]])
    ws6.cell(r, 7).fill = AMAR; ws6.cell(r, 8).fill = AMAR
    if "IEV" in g:
        for cell in ws6[r]:
            cell.font, cell.fill = VERM, VERM_FILL
formatar(ws6, [None, None, None, INT, INT, BRL, INT, INT, "0.0", BRL, BRL, BRL])
ws6.auto_filter.ref = ws6.dimensions
ws6.append([])
for nota6 in ["Minutos: intervalo mínimo de agendamento da Recomendação do CBR de 14/11/2017 (ultrassom, por item). Tomografia: os intervalos do plano 4 (20 min com contraste, 15 sem); angio de coronárias, 30 min por hipótese.",
          "As células amarelas são editáveis: troque pelos tempos que as clínicas praticarem e a coluna R$ por hora se recalcula.",
          "R$ por hora = preço × unidades × 60 ÷ minutos. Dentro do ultrassom o custo da hora (médico e sala) é quase o mesmo para qualquer exame, então o exame que paga mais por hora é o que deixa mais folga.",
          "Não compare a hora de ultrassom com a de tomógrafo: o custo da hora de cada aparelho é outro.",
          "Doppler bilateral: o CBR conta 20 min por membro, mas o pedido é 1 unidade do 02.05.01.004-0. A descrição SIGTAP (10/2026) diz que a quantidade independe da quantidade de vasos estudados (planos/redacao_04/dados/fontes/sigtap_0205010040_102026.md)."]:
    ws6.append([nota6])

# ---------- 7. Os quatro critérios
# família de equipamento e de quem executa: (família, requisito, nota de compartilhamento 1–3)
FAM = {
    "Abdômen total": ("Abdome (convexo)", "radiologista geral, sala comum", 3),
    "Abdômen superior": ("Abdome (convexo)", "radiologista geral, sala comum", 3),
    "Parede abdominal": ("Abdome (convexo + linear)", "radiologista geral, sala comum", 3),
    "Aparelho urinário": ("Abdome (convexo)", "radiologista geral, sala comum", 3),
    "Próstata abdominal": ("Abdome (convexo)", "radiologista geral, sala comum", 3),
    "Tireoide": ("Pequenas partes (linear)", "radiologista geral, sala comum", 3),
    "Mamas": ("Pequenas partes (linear)", "radiologista geral; leitura de mama (BI-RADS)", 2),
    "Bolsa escrotal": ("Pequenas partes (linear)", "radiologista geral, sala comum", 3),
    "Articulação e segmentos": ("Pequenas partes (linear)", "radiologista com prática musculoesquelética", 2),
    "Partes moles por região": ("Pequenas partes (linear)", "radiologista geral, sala comum", 3),
    "Partes moles (IEV)": ("Pequenas partes (linear)", "radiologista geral, sala comum", 3),
    "Transvaginal": ("Ginecológico (endocavitário)", "maca ginecológica, banheiro, acompanhante", 2),
    "Pélvica (ginecológica)": ("Abdome (convexo)", "bexiga cheia; sala comum", 3),
    "Doppler de carótidas e vertebrais": ("Plataforma geral (linear + Doppler)", "mesma plataforma com Doppler; médico que lauda Doppler; exame curto", 3),
    "Doppler venoso de membros, bilateral": ("Vascular (linear + convexo + Doppler)", "Doppler vascular; exame longo, ocupa a sala 40 min", 1),
    "Doppler arterial de membros, bilateral": ("Vascular (linear + convexo + Doppler)", "Doppler vascular; exame longo, ocupa a sala 40 min", 1),
    "Doppler de tireoide": ("Plataforma geral (linear + Doppler)", "radiologista geral com Doppler", 3),
    "Transfontanela": ("Pediátrico (microconvexo)", "público infantil, médico com prática pediátrica", 1),
    "Obstétrica": ("Obstétrico (convexo)", "obstetrícia; fila pequena", 2),
    "Obstétrica com Doppler": ("Obstétrico + Doppler", "medicina fetal", 1),
}
TCG = [  # (rótulo, filtro do grupo de tempo, família, requisito, compartilhamento)
    ("TC com contraste eletiva — abdômen, pelve, tórax, pescoço", lambda g: g.startswith("TC com contraste —") and any(k in g for k in ("abdomen", "pelve", "torax", "pescoco")),
     "Tomógrafo + bomba injetora", "enfermagem para o contraste; protocolo comum", 3),
    ("TC com contraste eletiva — crânio, face, coluna", lambda g: g.startswith("TC com contraste —") and any(k in g for k in ("cranio", "face", "coluna")),
     "Tomógrafo + bomba injetora", "enfermagem para o contraste; protocolo comum", 3),
    ("TC sem contraste eletiva", lambda g: g.startswith("TC sem contraste —"),
     "Tomógrafo", "protocolo comum; fila eletiva pequena", 3),
    ("TC angiotomografias (exceto coronárias)", lambda g: g.startswith("TC angio —"),
     "Tomógrafo multicorte + bomba injetora", "protocolo vascular", 2),
    ("TC angio de coronárias", lambda g: g == "TC angio de coronárias",
     "Tomógrafo ≥ 64 canais, sincronia com ECG", "betabloqueador, cardiologia; preço da clínica a cotar", 1),
]
POS = {  # carteira que as duas revisões sustentam (comparativo de 01/11/2026)
    "Abdômen total": "1 Núcleo", "Abdômen superior": "1 Núcleo", "Aparelho urinário": "1 Núcleo",
    "Doppler de carótidas e vertebrais": "1 Núcleo",
    "Parede abdominal": "2 Condicionada", "Partes moles por região": "2 Condicionada",
    "Articulação e segmentos": "3 Complemento", "Bolsa escrotal": "3 Complemento", "Próstata abdominal": "3 Complemento",
    "Tireoide": "3 Complemento", "Mamas": "3 Complemento",
    "Transvaginal": "4 À parte", "Doppler venoso de membros, bilateral": "4 À parte",
    "Doppler arterial de membros, bilateral": "4 À parte", "Obstétrica": "4 À parte",
    "Obstétrica com Doppler": "4 À parte", "Transfontanela": "4 À parte", "Doppler de tireoide": "4 À parte",
    "Pélvica (ginecológica)": "4 À parte", "Partes moles (IEV)": "Fora (IEV)",
    "TC com contraste eletiva — abdômen, pelve, tórax, pescoço": "1 Núcleo",
    "TC angiotomografias (exceto coronárias)": "3 Complemento", "TC sem contraste eletiva": "3 Complemento",
    "TC com contraste eletiva — crânio, face, coluna": "3 Complemento", "TC angio de coronárias": "4 À parte"}
us_rows, tc_rows = [], []
for (g, c), d in grp.items():
    if g in FAM and d["viva"] >= 50:
        us_rows.append((g, c, d))
tc_agg = []
for rot, f, fam, req, comp in TCG:
    viva = sum(d["viva"] for (g, c), d in grp.items() if c.startswith("02.06") and f(g))
    receita = sum(d["viva"] * cand[c] for (g, c), d in grp.items() if c.startswith("02.06") and f(g))
    mins = [d["m"] for (g, c), d in grp.items() if c.startswith("02.06") and f(g)]
    if viva:
        tc_agg.append((rot, viva, round(receita / viva, 2), max(mins), fam, req, comp))

ws7 = wb.create_sheet("7 Quatro critérios")
AMAR = PatternFill("solid", fgColor="FFF2CC")
prem = [("Premissas (amarelo = editável)", None, None),
        ("Médico de ultrassom, por hora (R$)", 100, "R$ 33,33 por exame do modelo do ISHP × 3 exames/h de 20 min"),
        ("Sala + aparelho, por mês (R$)", 5500, "R$ 3.000 + R$ 2.500 (custo_por_exame_v2, Premissas)"),
        ("Horas de sala úteis por mês", 168, "10 h × 21 dias × 80% (regra do plano 4)"),
        ("Insumos por exame de ultrassom (R$)", 3, "hipótese do custo_por_exame_v2"),
        ("Tomografia na clínica, por exame (R$)", 170, "R$ 165–175 com contraste incluído (rede do ISHP); angio de coronárias a cotar"),
        ("Peso: compartilhamento do equipamento", 1, None),
        ("Peso: receita por hora", 1, None),
        ("Peso: custo de execução (margem)", 1, None),
        ("Peso: tamanho da fila", 1, None)]
for i, (a, b, c) in enumerate(prem, 1):
    ws7.cell(i, 1, a); ws7.cell(i, 2, b); ws7.cell(i, 3, c)
    if b is not None:
        ws7.cell(i, 2).fill = AMAR
ws7.cell(1, 1).font = TOT
MED, SALA, HORAS, INS, TCP, W1, W2, W3, W4 = ("$B$2", "$B$3", "$B$4", "$B$5", "$B$6", "$B$7", "$B$8", "$B$9", "$B$10")
H0 = 12
cab7 = ["Modalidade", "Exame", "Código", "Família de equipamento", "Requisito de quem executa",
        "Pendentes 24 meses", "Candanga (R$)", "Minutos", "R$ por hora", "Custo por exame (R$)",
        "Margem por exame (R$)", "Margem por hora (R$)", "Nota: compartilhamento (editável)",
        "Nota: receita por hora", "Nota: custo (margem)", "Nota: fila", "Pontos", "Posição na carteira", "Leitura"]
for j, h in enumerate(cab7, 1):
    c = ws7.cell(H0, j, h); c.font, c.fill = CAB, CAB_FILL
    c.alignment = Alignment(wrap_text=True, vertical="center")
for j, w in enumerate([8, 40, 15, 28, 46, 11, 11, 8, 10, 11, 11, 11, 13, 10, 10, 9, 8, 16, 70], 1):
    ws7.column_dimensions[get_column_letter(j)].width = w
ws7.freeze_panes = ws7.cell(H0 + 1, 3)

LEIT = {
    "Doppler de carótidas e vertebrais": "mesma tarifa do Doppler de membros, metade do tempo; cabe na plataforma geral com Doppler",
    "Doppler venoso de membros, bilateral": "1 unidade por pedido (ficha SIGTAP); 40 min = 2 × 20 do CBR unilateral, extrapolação a confirmar; pede médico de Doppler vascular",
    "Doppler arterial de membros, bilateral": "idem ao venoso",
    "Parede abdominal": "condicionada: 15 min por analogia (o CBR não cita parede) e pagamento como abdômen total a confirmar com a SES",
    "Partes moles por região": "condicionada: confirmar se também são do IEV",
    "Mamas": "fila grande, mas 20 min a R$ 70,97: entra pela necessidade, não pelo preço",
    "Partes moles (IEV)": "do IEV: fora da conta",
    "Transfontanela": "melhor por hora, mas fila pequena e infantil",
    "Transvaginal": "depende do custo do transdutor endocavitário e da sala com maca ginecológica",
}
linhas7 = []
for g, c, d in us_rows:
    fam, req, comp = FAM[g]
    linhas7.append(("US", g, c, fam, req, d["viva"], cand[c], d["m"], comp, LEIT.get(g, "")))
for rot, viva, preco, m, fam, req, comp in tc_agg:
    linhas7.append(("TC", rot, "02.06", fam, req, viva, preco, m, comp,
                    "contraste e laudo no preço da clínica" if "coronárias" not in rot else "R$ 309,25 provavelmente abaixo do preço da clínica: cotar"))
r = H0 + 1
for mod, g, c, fam, req, viva, preco, m, comp, leit in linhas7:
    us = mod == "US"
    custo = f"=({MED}+{SALA}/{HORAS})*H{r}/60+{INS}" if us else f"={TCP}"
    nota_rh = f"=IF(I{r}>=330,3,IF(I{r}>=250,2,1))" if us else f"=IF(I{r}>=900,3,IF(I{r}>=700,2,1))"
    nota_cu = f"=IF(L{r}>=200,3,IF(L{r}>=100,2,1))" if us else f"=IF(K{r}>=130,3,IF(K{r}>=80,2,1))"
    coron = g == "TC angio de coronárias"
    if coron:  # sem preço de clínica: a nota de custo fica editável
        custo, nota_cu = "a cotar", 1
    vals = [mod, g, c, fam, req, viva, preco, m, f"=G{r}*60/H{r}", custo,
            None if coron else f"=G{r}-J{r}", None if coron else f"=K{r}*60/H{r}",
            comp, nota_rh, nota_cu, f"=IF(F{r}>=5000,3,IF(F{r}>=1000,2,1))",
            f"=M{r}*{W1}+N{r}*{W2}+O{r}*{W3}+P{r}*{W4}", POS.get(g, ""), leit]
    for j, v in enumerate(vals, 1):
        ws7.cell(r, j, v)
    ws7.cell(r, 13).fill = AMAR
    if coron:
        ws7.cell(r, 15).fill = AMAR
    if "IEV" in g:
        for j in range(1, len(vals) + 1):
            ws7.cell(r, j).font, ws7.cell(r, j).fill = VERM, VERM_FILL
    for j, f in zip(range(6, 13), [INT, BRL, INT, BRL, BRL, BRL, BRL]):
        ws7.cell(r, j).number_format = f
    r += 1
ws7.auto_filter.ref = f"A{H0}:S{r - 1}"
r += 1
for nota7 in ["Notas de 1 a 3. Compartilhamento: 3 = sala comum com radiologista geral; 2 = transdutor, sala ou habilidade própria; 1 = exige equipe ou equipamento que os outros exames não usam (Doppler vascular longo, pediatria, angio de coronárias).",
              "Receita por hora: US 3 ≥ R$ 330/h, 2 ≥ R$ 250/h; TC 3 ≥ R$ 900/h, 2 ≥ R$ 700/h. Custo: US pela margem por hora (3 ≥ R$ 200, 2 ≥ R$ 100); TC pela margem por exame na clínica (3 ≥ R$ 130, 2 ≥ R$ 80). Fila: 3 ≥ 5.000, 2 ≥ 1.000 pedidos nos últimos 24 meses.",
              "Custo do US feito por nós = (médico por hora + sala e aparelho por hora) × minutos ÷ 60 + insumos. Pagando a clínica a 50% do valor, a margem por exame vira metade do preço, e a clínica é quem sente o tempo: o exame longo e barato é o mais difícil de negociar.",
              "A margem não é lucro: no convênio, a sobra volta como saldo ou vira mais exames. Ela mede quanto o exame aperta ou folga o orçamento de execução.",
              "Emergência fica fora da tomografia eletiva. A fila de TC é a soma dos grupos de tempo da aba 6."]:
    ws7.cell(r, 1, nota7); r += 1

# ---------- Leia
txt = [
    ("Estudo de imagem pela Tabela SUS Candanga — 01/11/2026", TOT),
    ("Controle interno, para escolher os exames do plano de R$ 11,5 mi (plano 4) com a Candanga no lugar da Portaria SAES/MS 4.282/2026.", None),
    ("", None),
    ("Filas: Mapa Social da Saúde (MPDFT), SISREG/DATASUS, coleta do agente mapa-social de 29/10/2026 (recarga 29/10 18:32; pedido mais recente 27/10). Base em registros/mapa_social/imagem/.", None),
    ("Pendentes = fila sem os devolvidos. Pendentes 24 meses = pedidos desde 27/10/2024 (a fila viva do método). Pessoas não se somam entre filas.", None),
    ("Preço: Tabela SUS Candanga, Anexo Único da Deliberação CG-SES 46/2026 (SEI 212117347), modalidade SIA, pp. 5–6 para US e TC. biblioteca/precos/tabela_sus_candanga/ no main.", None),
    ("Plano 4: v26 (PT v1 assinado), calculo_v25/v25.json; valores da Portaria = tabela × incremento, truncados.", None),
    ("", None),
    ("EM VERMELHO: filas de US de partes moles — são do IEV. Estão no estudo para referência e não devem entrar na conta do plano 4 sem decisão.", VERM),
    ("", None),
    ("Abas: 0 resumo por modalidade; 1 todas as filas de imagem por código com o valor da Candanga; 2 cada fila de US e TC com enquadramento; 3 US e TC por código, com a diferença Portaria × Candanga; 4 o plano 4 reprecificado; 5 o resumo do enquadramento; 6 quanto cada exame paga por hora de sala; 7 os quatro critérios juntos (equipamento, receita por hora, custo, fila) e a posição na carteira conjunta.", None),
    ("A aba 8, quando existe, é do Codex: comparação independente por aparelho. Este script não a gera nem a altera; regera só as abas Leia e 0 a 7.", None),
    ("O 'valor da fila' é quantidade × preço, para comparar tamanhos. Não é meta, nem receita garantida.", None),
]
for s, f in txt:
    leia.append([s])
    if f: leia.cell(leia.max_row, 1).font = f
leia.column_dimensions["A"].width = 150

outras = [ws for ws in wb.worksheets if ws.title not in PROPRIAS]
wb._sheets = [wb[n] for n in PROPRIAS] + outras
wb.active = 0
wb.save(saida)

print("enquadramento (pendentes, 24 meses):", dict(cont), dict(cont_viva))
print("plano 4: portaria", round(t[1], 2), "candanga", round(t[2], 2), "dif", round(t[2] - t[1], 2), f"{(t[2]-t[1])/t[1]:.2%}")
print("modalidades:")
for m, mo in sorted(mods.items(), key=lambda kv: -kv[1][1]):
    print(f"  {m}: {mo[0]} filas, {mo[1]} pend, {mo[2]} viva, R$ {mo[3]:,.2f}")
print("US/TC por código (viva, iev_viva, valor sem iev):")
for c, a in sorted(agg.items(), key=lambda kv: -kv[1]["viva"] * cand.get(kv[0], 0)):
    print(f"  {c} {cand_nome.get(c,'')[:45]:45} fila {a['fila']:6} viva {a['viva']:6} iev {a['iev_viva']:5} agr {a['agr']:5} conf {a['conf']:4} R$ {cand.get(c,0):7.2f} p4 {PLANO4.get(c,'')}")
