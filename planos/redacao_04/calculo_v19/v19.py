from calculo import *
EXT_COD = {"02.05.02.009-7":1406,"02.05.02.018-6":1047,"02.05.01.004-0":1843,"02.05.02.004-6":1492,"02.05.02.005-4":400,
           "02.05.02.012-7":363,"02.05.02.010-0":283,"02.05.02.003-8":205,"02.06.03.001-0":1099,"02.06.03.003-7":951,"02.06.02.003-1":857}
AB = {"mama":5528,"transvag":4117,"abd_total":4737,"parede":1128,"dop_mmii":2834,"carotidas":4411,"urinario":1576,"tireoide":1430,
      "prostata":1116,"abd_sup":807,"tc_abd":4321,"tc_pelve":3739,"tc_torax_c":2477,"coronarias":783,"tc_torax_s":110}
# reparte o acrescimo de cada codigo entre os seus nomes de fila, pelas abertas de 2026 (maiores restos)
Q19 = dict(Q18)
for c, e in EXT_COD.items():
    nomes = [n for n in COD if COD[n] == c]
    fr = {n: F(e * AB[n], sum(AB[m] for m in nomes)) for n in nomes}
    for n, v in maiores_restos(fr, e).items(): Q19[n] += v
qc = por_codigo(Q19)
assert sum(qc.values()) == 88518
tot, us, tc, hus, htc, pct = rateio(Q19)
dias = 252
out = {}
print("por nome:", {n: Q19[n] for n in Q19})
print("por código:", qc)
print("US", sum(us.values()), "TC", sum(tc.values()))
print("total por polo", tot, "pct", {p: f"{float(pct[p])*100:.2f}" for p in ORD})
print("US por polo", us, "| TC por polo", tc)
print("h US", hus, sum(hus.values()), "| h TC", htc, sum(htc.values()), "| total h", sum(hus.values())+sum(htc.values()))
mes_us = {p: math.ceil(us[p]/12) for p in ORD}; mes_tc = {p: math.ceil(tc[p]/12) for p in ORD}
dia_us = {p: math.ceil(us[p]/dias) for p in ORD}; dia_tc = {p: math.ceil(tc[p]/dias) for p in ORD}
salas = {"Ceilândia":5,"Sobradinho":4,"Gama":4}
print("mês US", mes_us, sum(mes_us.values()), "| mês TC", mes_tc, sum(mes_tc.values()))
print("dia US", dia_us, sum(dia_us.values()), "| dia TC", dia_tc, sum(dia_tc.values()))
print("exames/sala/dia", {p: math.ceil(dia_us[p]/salas[p]) for p in ORD})
print("ocupação salas", {p: f"{hus[p]/(salas[p]*2520):.1%}" for p in ORD}, "| regra 80%:", {p: math.ceil(hus[p]/(2520*0.8)) for p in ORD})
print("ocupação TC", {p: f"{htc[p]/2520:.1%}" for p in ORD}, "| carga agregada TC em tomógrafos:", f"{sum(htc.values())/2520:.2f}")
for a in ORD:
    for b in ORD:
        if a!=b: pass
# ponto 4: concentrar em dois polos - o polo que fecha manda a carga a cada um dos outros
for fecha in ORD:
    for rec in [p for p in ORD if p!=fecha]:
        print(f"  fecha {fecha} -> {rec}: {htc[rec]+htc[fecha]} h ({(htc[rec]+htc[fecha])/2520:.1%})")
tri = curva(qc)
print("curva", [sum(t.values()) for t in tri], "máx/dia", math.ceil(max(sum(t.values()) for t in tri)/63))
prod = [sum(t[c]*UNIT[c] for c in t) for t in tri]
print("produção/trimestre", [f"{x:.2f}" for x in prod], f"soma {sum(prod):.2f}")
apoio = D("973860.00")
print("apoio/trimestre", apoio/4, "| parcelas", [f"{x+apoio/4:.2f}" for x in prod], f"| global {sum(prod)+apoio:.2f}")
# contraste
contr = sum(Q19[n] for n in ["tc_abd","tc_pelve","tc_torax_c","coronarias"])
print("TC com contraste", contr, "de", sum(tc.values()))
# postos por polo: 7 operadores e 8 assistentes, pela producao de cada polo (maiores restos)
for nome, n in [("operadores",7),("assistentes",8)]:
    fr = {p: F(n*tot[p], sum(tot.values())) for p in ORD}
    print(nome, maiores_restos(fr, n), {p: f"{float(fr[p]):.2f}" for p in ORD})
# 5.16 medicos
print("médicos US", {p: (hus[p], f"{hus[p]/1800:.1f}", math.ceil(hus[p]/1800)) for p in ORD})
print("radiologistas", {p: (htc[p], f"{htc[p]/1800:.2f}", math.ceil(htc[p]/1800)) for p in ORD})
json.dump({"Q19":Q19,"qc":qc,"tot":tot,"us":us,"tc":tc,"hus":hus,"htc":htc,"pct":{p:float(pct[p]) for p in ORD},
           "tri":[{c:t[c] for c in t} for t in tri],"prod":[str(x) for x in prod]}, open("v19.json","w"), ensure_ascii=False, indent=1)
