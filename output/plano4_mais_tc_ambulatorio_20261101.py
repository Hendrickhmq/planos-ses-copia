"""Plano 4 + TC, só ambulatório (sem fila de emergência) e sem sobreposição (L-008). Filas de 29/10/2026, Candanga SIA."""
import csv, json, re, sys, unicodedata
def nz(t): return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t)).strip().upper()
cand = {x["codigo_sigtap"]: float(x["valor"]) for x in csv.DictReader(open(sys.argv[1])) if x["modalidade"] == "SIA"}
F = {}
JUNTAS = []
for x in csv.DictReader(open("registros/mapa_social/imagem/filas_20261029.csv", encoding="utf-8-sig"), delimiter=";"):
    if x["escopo"] == "exame" and int(x["fila"] or 0) > 0:
        k = nz(x["nome"])
        if k in F and F[k][0] != x["codigo_formatado"]:
            k = k + " [" + x["codigo_formatado"] + "]"  # mesmo nome em outro código: fila à parte
        if k in F:  # grafias que só diferem em espaço, no mesmo código: soma
            JUNTAS.append(k)
            F[k] = (F[k][0], F[k][1] + int(x["fila"]))
        else:
            F[k] = (x["codigo_formatado"], int(x["fila"]))
ALVO = 10636542.52
print("grafias somadas:", JUNTAS)
# o plano 4 (v26): fila nominal, quantidade
P4 = [("Mama bilateral", "ECOGRAFIA DE MAMAS - BILATERAL", 14689), ("Transvaginal", "ECOGRAFIA TRANSVAGINAL", 10541),
      ("Abdômen total adulto", "ECOGRAFIA DE ABDOMEN TOTAL ADULTO", 10028),
      ("Doppler venoso de MMII", "ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)", 9834),
      ("Doppler de carótidas", "10. ECODOPPLER DE CAROTIDAS", 4674),
      ("Aparelho urinário adulto", "ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO", 3944),
      ("Tireoide adulto", "ECOGRAFIA DE TIREOIDE ADULTO", 3216), ("Próstata", "ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL )", 3201),
      ("Parede abdominal", "ULTRASONOGRAFIA DE PAREDE ABDOMINAL", 3138), ("Abdômen superior adulto", "ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO", 2261),
      ("TC abdômen superior c/ contraste", "063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO", 4516),
      ("TC pelve c/ contraste", "111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO", 3862),
      ("TC tórax c/ contraste", "055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO", 3104),
      ("Angiotomografia de coronárias", "ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO", 1408),
      ("TC tórax s/ contraste EMERGÊNCIA", "TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA", 728)]
P4 = [(r, nz(n), q) for r, n, q in P4]
for r, n, q in P4: assert n in F, n
def val(n, q): return q * cand[F[n][0]]
emerg = [x for x in P4 if "EMERG" in x[1]]
amb = [x for x in P4 if "EMERG" not in x[1]]
print("v26 Portaria:", 79144, "exames; pela Candanga:", round(sum(val(n, q) for _, n, q in P4), 2))
print("sai a emergência:", emerg[0][2], "exames,", round(val(emerg[0][1], emerg[0][2]), 2))
# ---- pura: v26 ambulatorial como está + TC
v = sum(val(n, q) for _, n, q in amb); falta = ALVO - v; tc = int(falta // 309.25)
print(f"\nPURA: v26 sem emergência = {sum(q for *_, q in amb)} exames, R$ {v:,.2f}; falta R$ {falta:,.2f} = {tc} TC; total {sum(q for *_, q in amb)+tc} exames, R$ {v+tc*309.25:,.2f}")
acima = [(r, q - F[n][1]) for r, n, q in amb if q > F[n][1]]
print("  metas acima da fila de hoje:", acima, "soma", sum(a for _, a in acima))
# ---- TC ambulatorial livre nos códigos do plano 4 (sem emergência, sem sedação, fora das filas do plano)
TCC = ("02.06.03.001-0", "02.06.03.003-7", "02.06.02.003-1")
usadas = {n for _, n, _ in P4}
livre = {n: f for n, (c, f) in F.items() if c in TCC and n not in usadas and "EMERG" not in n and "C/SEDACAO" not in n and "C/ SEDACAO" not in n}
print("\nTC ambulatorial livre nos 3 códigos:", sum(livre.values()))
for n, f in sorted(livre.items(), key=lambda x: -x[1]): print(f"   {f:5} {n}")
tc_amb_fila = sum(F[n][1] for _, n, _ in amb if F[n][0] in TCC) + sum(livre.values())
print("TC ambulatorial total nos 3 códigos (filas do plano + livres):", tc_amb_fila)
print("PURA pede de TC:", sum(q for _, n, q in amb if F[n][0] in TCC) + tc)
# ---- ajustada: cada fila do plano limitada à de hoje
cap = [(r, n, min(q, F[n][1])) for r, n, q in amb]
vc = sum(val(n, q) for _, n, q in cap); nc = sum(q for *_, q in cap)
print(f"\nAJUSTADA: plano limitado à fila de hoje = {nc} exames, R$ {vc:,.2f}; falta R$ {ALVO-vc:,.2f}")
extra = []  # o que a fila de hoje tem a mais nas filas do plano
for r, n, q in amb:
    if F[n][1] > q: extra.append((r + " (a mais que no plano)", n, F[n][1] - q))
camadas = [("1 TC ambulatorial livre e a mais", [(n, f) for n, f in livre.items()] + [(n, q) for r, n, q in extra if F[n][0] in TCC])]
INF = [nz(x) for x in ["ECOGRAFIA DE ABDOMEN TOTAL INFANTIL", "ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL", "ECOGRAFIA DE TIREOIDE INFANTIL", "ECOGRAFIA DE ABDOMEN SUPERIOR INFANTIL", "ULTRASSONOGRAFIA RENAL"]]
camadas.append(("2 US das mesmas filas e códigos (a mais e infantis)", [(n, q) for r, n, q in extra if F[n][0] not in TCC] + [(n, F[n][1]) for n in INF if n in F]))
DOP = [nz(x) for x in ["ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL)", "ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL)", "ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL)", "ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS", "ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS", "ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE"]]
camadas.append(("3 Doppler do mesmo código fora do plano (arterial, MMSS, carótidas e vertebrais, renais) e Doppler de tireoide", [(n, F[n][1]) for n in DOP if n in F]))
acc = vc; tot = nc
for rot, itens in camadas:
    s = sum(q * cand[F[n][0]] for n, q in itens); k = sum(q for _, q in itens); acc += s; tot += k
    print(f"  + {rot}: {k} exames, R$ {s:,.2f} -> acumulado R$ {acc:,.2f}, {tot} exames; falta R$ {ALVO-acc:,.2f}")
    for n, q in itens: print(f"       {q:5} {F[n][0]} {n}")
falta = ALVO - acc
print(f"  falta fechar com articulação (sem CID do IEV, R$ 70,97): {falta/70.97:,.0f} exames de ~9.197")
