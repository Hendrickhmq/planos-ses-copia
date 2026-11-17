"""Os 6 polos do plano 4 (20/10/2026): demanda por Regiao, distancia, capacidade com margem e tomografia em 6 e 5 polos.

Roda o calculo_v22 com o quadro do cenario 3 (preco proposto) e o rateio nas 7 Regioes de Saude (o mesmo metodo
do plano: participacoes por fila de 15/09/2026). A divisao de cada Regiao entre as RAs segue a populacao do Censo
2022 (simulador dados/polos_de_imagem_no_df_v20.html, que traz tambem a posicao de cada RA, em km). Distancia em
linha reta entre o centro da RA e a cidade do polo. Grava polos_capacidade.json.

Uso: python3 polos_capacidade.py
"""
import json, math, os, re, subprocess, sys
from itertools import combinations

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(AQUI, "..", "calculo_v22", "calculo_v22.py"), encoding="utf-8").read()
from cenarios_quadro import quadro, PROPOSTO   # noqa: E402  (o cenario 3 escolhido: 3 coordenacoes, 8 operadores)

REG7 = ["Oeste", "Sudoeste", "Norte", "Leste", "Central", "Sul", "Centro-Sul"]
q = quadro(PROPOSTO, True, 8)
bloco = "QUADRO = [\n" + "".join(f'    ("{p}", {n}, D("{v}"), {m}, "{i}"),\n' for p, n, v, m, i in q) + "]\n"
s = re.sub(r"QUADRO = \[.*?\n\]\n", bloco, SRC, flags=re.S).replace('assert APOIO == D("919640.00") and APOIO <= TETO', "")
s = re.sub(r"K\.POLO = \{.*?\}\n", "K.POLO = {" + ", ".join(f'"{r}": ["Região {r}"]' for r in REG7) + "}\n", s, flags=re.S)
s = re.sub(r"K\.ORD = ORD = \[.*?\]\n", "K.ORD = ORD = " + json.dumps(REG7, ensure_ascii=False) + "\n", s)
s = re.sub(r"POLOS = \{.*?\}\n", "POLOS = {" + ", ".join(f'"{r}": 1' for r in REG7) + "}\n", s)
s = re.sub(r"\nout = \{.*", "\nprint('RES', json.dumps({'tot': tot, 'us': us, 'tc': tc, 'hus': hus, 'htc': htc, "
           "'N': sum(qc.values())}, ensure_ascii=False))\n", s, flags=re.S)
tmp = os.path.join(AQUI, "_polos_7regioes.py")
open(tmp, "w", encoding="utf-8").write(s)
try:
    out = subprocess.run([sys.executable, tmp], capture_output=True, text=True, check=True)
finally:
    os.remove(tmp)
R = json.loads([l for l in out.stdout.splitlines() if l.startswith("RES ")][0][4:])

SIM = json.loads(re.search(r"const D = (\{.*?\});\n", open(os.path.join(AQUI, "..", "dados", "polos_de_imagem_no_df_v20.html"),
                                                             encoding="utf-8").read(), re.S).group(1))
RAS = {a["nome"]: a for a in SIM["ras"]}
pop = {r: sum(a["pop"] for a in RAS.values() if a["regiao"] == r) for r in REG7}
for a in RAS.values():
    for m in ("tot", "us", "tc"):
        a[m] = R[m][a["regiao"]] * a["pop"] / pop[a["regiao"]]
dist = lambda a, b: math.hypot(a["x"] - b["x"], a["y"] - b["y"])
N = R["N"]

# 1. qual dupla de Regioes junta: polo na RA que minimiza exames x km
def melhor(regs):
    g = [a for a in RAS.values() if a["regiao"] in regs]
    c = min(g, key=lambda c: sum(a["tot"] * dist(a, c) for a in g))
    return c["nome"], sum(a["tot"] * dist(a, c) for a in g), max(dist(a, c) for a in g)
base = {r: melhor([r]) for r in REG7}
duplas = []
for r1, r2 in combinations(REG7, 2):
    sede, ek, dmax = melhor([r1, r2])
    dem = R["tot"][r1] + R["tot"][r2]
    duplas.append({"regioes": [r1, r2], "sede": sede, "exames": dem, "pct": dem / N,
                   "km_a_mais_por_exame": (ek - base[r1][1] - base[r2][1]) / dem, "ra_mais_longe_km": dmax})

# 2. os 6 polos, com as cidades das unidades que a rede ja tem
SEDE = {"Oeste": "Ceilândia", "Sudoeste": "Taguatinga", "Norte": "Sobradinho", "Leste": "São Sebastião",
        "Central": "Plano Piloto", "Centro-Sul": "Plano Piloto", "Sul": "Gama"}
POLOS = [("Oeste", ["Oeste"]), ("Sudoeste", ["Sudoeste"]), ("Norte", ["Norte"]), ("Leste", ["Leste"]),
         ("Central e Centro-Sul", ["Central", "Centro-Sul"]), ("Sul", ["Sul"])]
polos = []
for nome, regs in POLOS:
    polos.append({"polo": nome, "regioes": regs, "us": sum(R["us"][r] for r in regs), "tc": sum(R["tc"][r] for r in regs),
                  "h_us": sum(R["hus"][r] for r in regs), "h_tc": sum(R["htc"][r] for r in regs)})
KM6 = sum(a["tot"] * dist(a, RAS[SEDE[a["regiao"]]]) for a in RAS.values()) / N

# 3. tomografia: para onde vai a demanda de cada RA, em 6 e em 5 polos (a Leste sem tomografo)
H_POR_TC = sum(R["htc"].values()) / sum(R["tc"].values())
VAI_A_CEILANDIA = {"Samambaia", "Recanto das Emas e Água Quente"}   # alivia Taguatinga, que sozinha passa de 1 tomografo
def destino6(a):
    return "Ceilândia" if a["nome"] in VAI_A_CEILANDIA else SEDE[a["regiao"]]
def destino5(a):
    if a["nome"] == "Itapoã":
        return "Sobradinho"          # mais perto de Sobradinho (10,8 km) que da Asa Sul (13,3 km)
    if a["regiao"] == "Leste":
        return "Plano Piloto"        # onibus direto da Leste ao Plano Piloto
    return destino6(a)
def tomografia(f, nome):
    por_sede, por_ra = {}, []
    for a in RAS.values():
        sd = f(a)
        por_sede[sd] = por_sede.get(sd, 0) + a["tc"]
        por_ra.append({"ra": a["nome"], "regiao": a["regiao"], "tc": a["tc"], "vai_a": sd, "km": dist(a, RAS[sd])})
    km = sum(x["tc"] * x["km"] for x in por_ra) / sum(x["tc"] for x in por_ra)
    return {"cenario": nome, "km_medio": km, "por_sede": por_sede, "por_ra": por_ra}
tc6 = tomografia(destino6, "6 polos com tomografia")
tc5 = tomografia(destino5, "5 polos com tomografia (Leste sem)")
tc6_sem_ajuste = tomografia(lambda a: SEDE[a["regiao"]], "6 polos, cada Regiao no seu")

res = {"N": N, "R": R, "pop": pop, "duplas": sorted(duplas, key=lambda d: d["km_a_mais_por_exame"]), "polos": polos,
       "km_medio_6_polos": KM6, "h_por_tc": H_POR_TC, "tc6": tc6, "tc5": tc5, "tc6_sem_ajuste": tc6_sem_ajuste,
       "ras": [{k: a[k] for k in ("nome", "regiao", "pop", "x", "y", "tot", "us", "tc")} for a in RAS.values()]}
json.dump(res, open(os.path.join(AQUI, "polos_capacidade.json"), "w"), ensure_ascii=False, indent=1)
print("exames", N, "| km medio 6 polos", round(KM6, 1))
for t in (tc6_sem_ajuste, tc6, tc5):
    print(t["cenario"], round(t["km_medio"], 1), {k: (round(v), round(v / 8), round(v * H_POR_TC / 1344, 2)) for k, v in
                                                  sorted(t["por_sede"].items(), key=lambda x: -x[1])})
