"""Recalculo da v19 do plano 4 com os metodos da v18 (estado.yaml: rateio_polo, parcelas,
capacidade). Primeiro reproduz a v18; so depois aplica as quantidades novas."""
from decimal import Decimal as D, ROUND_FLOOR
from fractions import Fraction as F
import math, json, sys

POLO = {"Ceilândia": ["Região Oeste", "Região Sudoeste"],
        "Sobradinho": ["Região Norte", "Região Leste", "Região Central"],
        "Gama": ["Região Sul", "Região Centro-Sul"]}
ORD = ["Ceilândia", "Sobradinho", "Gama"]
REG = ["Região Central", "Região Centro-Sul", "Região Leste", "Região Norte", "Região Oeste", "Região Sudoeste", "Região Sul"]

# regiao por nome de fila, coletas de 15/09/2026 (US: medida fila; TC: medida Total de Solicitacoes)
R = {
 "mama":      {"Região Sudoeste":5422,"Região Leste":2506,"Região Sul":2143,"Região Oeste":1605,"Região Central":1303,"Região Centro-Sul":927,"Região Norte":337},
 "abd_total": {"Região Sul":2897,"Região Sudoeste":2434,"Região Leste":1801,"Região Centro-Sul":1755,"Região Central":554,"Região Oeste":223,"Região Norte":131},
 "transvag":  {"Região Sudoeste":4376,"Região Leste":3154,"Região Sul":1251,"Região Norte":536,"Região Oeste":502,"Região Centro-Sul":424,"Região Central":48},
 "dop_mmii":  {"Região Sul":3704,"Região Norte":2779,"Região Sudoeste":2608,"Região Central":594,"Região Centro-Sul":2,"Região Leste":2},
 "urinario":  {"Região Sudoeste":1304,"Região Centro-Sul":901,"Região Sul":799,"Região Leste":791,"Região Oeste":65,"Região Norte":8,"Região Central":2},
 "carotidas": {"Região Sudoeste":705,"Região Oeste":608,"Região Centro-Sul":576,"Região Norte":519,"Região Central":451,"Região Sul":335,"Região Leste":231},
 "prostata":  {"Região Sul":1127,"Região Leste":877,"Região Centro-Sul":603,"Região Sudoeste":562,"Região Oeste":48,"Região Norte":11,"Região Central":1},
 "tireoide":  {"Região Sul":974,"Região Sudoeste":795,"Região Leste":704,"Região Centro-Sul":586,"Região Oeste":83,"Região Norte":50,"Região Central":4},
 "abd_sup":   {"Região Sudoeste":1607,"Região Centro-Sul":371,"Região Leste":217,"Região Sul":38,"Região Oeste":33,"Região Norte":8,"Região Central":1},
 "parede":    {"Região Sudoeste":1473,"Região Sul":812,"Região Leste":361,"Região Centro-Sul":342,"Região Oeste":81,"Região Norte":39},
 "tc_abd":    {"Região Central":673,"Região Centro-Sul":409,"Região Leste":566,"Região Norte":847,"Região Oeste":329,"Região Sudoeste":2051,"Região Sul":797},
 "tc_pelve":  {"Região Central":444,"Região Centro-Sul":290,"Região Leste":383,"Região Norte":644,"Região Oeste":210,"Região Sudoeste":1438,"Região Sul":674},
 "tc_torax_c":{"Região Central":239,"Região Centro-Sul":92,"Região Leste":222,"Região Norte":264,"Região Oeste":179,"Região Sudoeste":914,"Região Sul":214},
 "coronarias":{"Região Central":123,"Região Centro-Sul":113,"Região Leste":133,"Região Norte":191,"Região Oeste":278,"Região Sudoeste":231,"Região Sul":142},
 "tc_torax_s":{"Região Central":163,"Região Centro-Sul":159,"Região Leste":155,"Região Norte":303,"Região Oeste":24,"Região Sudoeste":631,"Região Sul":237},
}
COD = {"mama":"02.05.02.009-7","transvag":"02.05.02.018-6","abd_total":"02.05.02.004-6","parede":"02.05.02.004-6",
       "dop_mmii":"02.05.01.004-0","carotidas":"02.05.01.004-0","urinario":"02.05.02.005-4","tireoide":"02.05.02.012-7",
       "prostata":"02.05.02.010-0","abd_sup":"02.05.02.003-8","tc_abd":"02.06.03.001-0","tc_pelve":"02.06.03.003-7",
       "tc_torax_c":"02.06.02.003-1","coronarias":"02.06.02.003-1","tc_torax_s":"02.06.02.003-1"}
TC = {"tc_abd","tc_pelve","tc_torax_c","coronarias","tc_torax_s"}
MIN = {n: (30 if n in ("dop_mmii","carotidas") else 15 if n=="tc_torax_s" else 20) for n in R}
UNIT = {"02.05.02.009-7":D("99.94"),"02.05.02.018-6":D("99.94"),"02.05.01.004-0":D("100.18"),"02.05.02.004-6":D("100.18"),
        "02.05.02.005-4":D("99.94"),"02.05.02.012-7":D("99.94"),"02.05.02.010-0":D("99.94"),"02.05.02.003-8":D("99.94"),
        "02.06.03.001-0":D("299.44"),"02.06.03.003-7":D("299.44"),"02.06.02.003-1":D("300.10")}
Q18 = {"mama":14608,"transvag":10481,"abd_total":9959,"dop_mmii":9793,"carotidas":4608,"urinario":3921,"tireoide":3195,
       "prostata":3185,"parede":3121,"abd_sup":2249,"tc_abd":4453,"tc_pelve":3808,"tc_torax_c":3068,"coronarias":1397,"tc_torax_s":726}

def share(n):
    tot = sum(R[n].get(r, 0) for r in REG)
    return {p: F(sum(R[n].get(r, 0) for r in POLO[p]), tot) for p in ORD}

def maiores_restos(frac, total):
    base = {p: math.floor(frac[p]) for p in frac}
    falta = total - sum(base.values())
    for p in sorted(frac, key=lambda p: frac[p] - base[p], reverse=True)[:falta]:
        base[p] += 1
    return base

def rateio(Q):
    frac_tot = {p: sum(Q[n] * share(n)[p] for n in Q) for p in ORD}
    frac_tc = {p: sum(Q[n] * share(n)[p] for n in Q if n in TC) for p in ORD}
    tot = maiores_restos(frac_tot, sum(Q.values()))
    tc = maiores_restos(frac_tc, sum(Q[n] for n in Q if n in TC))
    us = {p: tot[p] - tc[p] for p in ORD}
    h_us = {p: round(sum(Q[n] * share(n)[p] * MIN[n] for n in Q if n not in TC) / 60) for p in ORD}
    h_tc = {p: round(sum(Q[n] * share(n)[p] * MIN[n] for n in Q if n in TC) / 60) for p in ORD}
    pct = {p: frac_tot[p] / sum(Q.values()) for p in ORD}
    return tot, us, tc, h_us, h_tc, pct

def por_codigo(Q):
    c = {}
    for n, v in Q.items():
        c[COD[n]] = c.get(COD[n], 0) + v
    return c

def curva(qcod):
    """um quarto de cada codigo por trimestre; o resto vai aos ultimos trimestres"""
    tri = [{}, {}, {}, {}]
    for c, q in qcod.items():
        b, r = divmod(q, 4)
        for t in range(4):
            tri[t][c] = b + (1 if t >= 4 - r else 0)
    return tri

if __name__ == "__main__":
    tot, us, tc, hus, htc, pct = rateio(Q18)
    print("v18 reproduzida?")
    print("  total", tot, "| esperado 31183/23527/23862")
    print("  US", us, "| esperado 25327/18685/21108")
    print("  TC", tc, "| esperado 5856/4842/2754")
    print("  h US", hus, sum(hus.values()), "| esperado 9176/7066/7864 = 24106")
    print("  h TC", htc, sum(htc.values()), "| esperado 1928/1592/904 = 4424")
    print("  pct", {p: f"{float(pct[p])*100:.2f}%" for p in ORD}, "| esperado 39,69/29,94/30,37")
    tri = curva(por_codigo(Q18))
    print("  curva", [sum(t.values()) for t in tri], "| esperado 19640/19642/19642/19648")
    prod = [sum(t[c] * UNIT[c] for c in t) for t in tri]
    print("  produção por trimestre", [f"{x:.2f}" for x in prod], "| esperado 2636045.42/2636445.46/2636445.46/2637244.84")
