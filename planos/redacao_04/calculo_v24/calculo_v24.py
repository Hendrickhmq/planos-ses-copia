"""v24 do plano 4 (20/10/2026): seis polos, o quadro de gestao do cenario 3 e os dois cenarios de tomografia.

Decisoes do usuario (20/10/2026):
- quadro: cenario 3 com o preco proposto (cenarios_quadro.py): Direcao Executiva, tres coordenacoes, tres supervisores
  de polo, 8 operadores (4 no pre-exame, 4 no pos-exame), 6 assistentes administrativos (apoio administrativo e
  documental, um por polo) e a assessoria, por 8 meses;
- seis polos, um por Regiao de Saude, com a Central e a Centro-Sul num polo so;
- plano A: tomografia nos seis polos, um tomografo por polo; a carga da Sudoeste que passa de um equipamento e absorvida
  no polo da Oeste, na agenda que o proponente libera ali;
- plano B: tomografia em rede, sem numero de tomografos no texto, so a carga e as horas.

Metodo igual ao da v22 (calculo_v22.py): fila de 10/09 inteira, acrescimo pelas entradas de 2026, rateio por nome de
fila com as participacoes de 15/09, agora nas 7 Regioes e somado nos 6 polos. Salas e tomografos pela regra dos 80% sobre
1.344 h no periodo; medicos a 1.200 h no periodo. Grava v24.json.
"""
import json, math, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
from cenarios_quadro import quadro, PROPOSTO   # noqa: E402

SRC = open(os.path.join(AQUI, "..", "calculo_v22", "calculo_v22.py"), encoding="utf-8").read()
REG7 = ["Oeste", "Sudoeste", "Norte", "Leste", "Central", "Sul", "Centro-Sul"]
ORD = ["Oeste", "Sudoeste", "Norte", "Leste", "Central e Centro-Sul", "Sul"]
POLO_REG = {"Oeste": ["Oeste"], "Sudoeste": ["Sudoeste"], "Norte": ["Norte"], "Leste": ["Leste"],
            "Central e Centro-Sul": ["Central", "Centro-Sul"], "Sul": ["Sul"]}

q = quadro(PROPOSTO, True, 8)
bloco = "QUADRO = [\n" + "".join(f'    ("{p}", {n}, D("{v}"), {m}, "{i}"),\n' for p, n, v, m, i in q) + "]\n"
s = re.sub(r"QUADRO = \[.*?\n\]\n", bloco, SRC, flags=re.S).replace('assert APOIO == D("919640.00") and APOIO <= TETO', "")
s = re.sub(r"K\.POLO = \{.*?\}\n", "K.POLO = {" + ", ".join(f'"{r}": ["Região {r}"]' for r in REG7) + "}\n", s, flags=re.S)
s = re.sub(r"K\.ORD = ORD = \[.*?\]\n", "K.ORD = ORD = " + json.dumps(REG7, ensure_ascii=False) + "\n", s)
s = re.sub(r"POLOS = \{.*?\}\n", "POLOS = {" + ", ".join(f'"{r}": 1' for r in REG7) + "}\n", s)
DUMP = ("print('RES', json.dumps({'Q': Q, 'qc': qc, 'producao': str(producao), 'glob': str(glob), 'sobra': str(sobra), "
        "'apoio': str(APOIO), 'envelope': str(envelope), 'tot': tot, 'us': us, 'tc': tc, 'hus': hus, 'htc': htc, "
        "'curva': curva_b, 'prod_b': [str(x) for x in prod_b], 'apoio_p': [str(x) for x in apoio_p], "
        "'parcelas': [str(x) for x in parcelas], 'dias_p': dias_p, 'i_pico': i_pico, 'contraste': contraste, "
        "'periodos': PERIODOS}, ensure_ascii=False))\n")
s = re.sub(r"\nout = \{.*", "\n" + DUMP, s, flags=re.S)
tmp = os.path.join(AQUI, "_calculo_v24_tmp.py")
open(tmp, "w", encoding="utf-8").write(s)
try:
    out = subprocess.run([sys.executable, tmp], capture_output=True, text=True, check=True)
finally:
    os.remove(tmp)
R = json.loads([l for l in out.stdout.splitlines() if l.startswith("RES ")][0][4:])

MESES, DIAS, HORAS_DIA = 8, 168, 10
CAP = DIAS * HORAS_DIA * 0.8                  # 1.344 h por sala ou tomografo a 80%
H_MEDICO = 1800 * MESES // 12                 # 1.200 h por medico no periodo
soma = lambda m, x: sum(R[m][r] for r in POLO_REG[x])
P = {}
for x in ORD:
    p = {k: soma(k, x) for k in ("tot", "us", "tc", "hus", "htc")}
    p["salas"] = max(math.ceil(p["hus"] / CAP), 1)
    p["medicos_us"] = max(math.ceil(p["hus"] / H_MEDICO), p["salas"])
    p["mes_us"], p["mes_tc"] = math.ceil(p["us"] / MESES), math.ceil(p["tc"] / MESES)
    p["dia_us"], p["dia_tc"] = math.ceil(p["us"] / DIAS), math.ceil(p["tc"] / DIAS)
    p["por_sala"] = math.ceil(p["dia_us"] / p["salas"])
    p["carga_tc"] = p["htc"] / CAP
    p["radiologistas"] = max(math.ceil(p["htc"] / H_MEDICO), 1)      # plano A: um tomografo por polo
    p["tomografos"] = 1
    p["tecnicos"], p["enfermagem"] = 3, 2
    p["rt"], p["retaguarda"], p["recepcao"], p["assistentes"] = 1, 1, 2, 1
    P[x] = p
N = sum(R["qc"].values())
US = sum(v for c, v in R["qc"].items() if c.startswith("02.05"))
TC = N - US
HUS, HTC = sum(P[x]["hus"] for x in ORD), sum(P[x]["htc"] for x in ORD)
ip = R["i_pico"]
pico_dia = math.ceil(R["curva"][ip] / R["dias_p"][ip])
V = {"meses": MESES, "dias": DIAS, "h_medico": H_MEDICO, "cap": CAP, "ORD": ORD, "POLO_REG": POLO_REG,
     "quadro": [(p_, n_, v_, m_, i_, str(float(v_) * n_ * MESES)) for p_, n_, v_, m_, i_ in q],
     "total": N, "us_total": US, "tc_total": TC, "acrescimo": N - 78572, "qc": R["qc"], "Q": R["Q"],
     "producao": R["producao"], "global": R["glob"], "sobra": R["sobra"], "apoio": R["apoio"], "envelope": R["envelope"],
     "polos": P, "hus": HUS, "htc": HTC, "carga_tc": HTC / CAP, "radiologistas_rede": math.ceil(HTC / H_MEDICO),
     "curva": R["curva"], "prod_b": R["prod_b"], "apoio_periodo": R["apoio_p"], "parcelas": R["parcelas"],
     "dias_periodo": R["dias_p"], "pico_periodo": ip, "pico_dia": pico_dia, "contraste": R["contraste"],
     "periodos": R["periodos"]}
json.dump(V, open(os.path.join(AQUI, "v24.json"), "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    print("exames", N, "US", US, "TC", TC, "acrescimo", N - 78572, "contraste", R["contraste"])
    print("apoio", R["apoio"], "| producao", R["producao"], "| global", R["glob"], "| sobra", R["sobra"])
    print("curva", R["curva"], "| pico", R["periodos"][ip][0], pico_dia, "por dia util")
    print("parcelas", R["parcelas"], "| apoio por periodo", R["apoio_p"])
    print("h US", HUS, "h TC", HTC, "carga TC", round(HTC / CAP, 2), "radiologistas da rede", math.ceil(HTC / H_MEDICO))
    for x in ORD:
        p = P[x]
        print(f"{x:22s} tot {p['tot']:6d} us {p['us']:6d} tc {p['tc']:5d} hus {p['hus']:5d} htc {p['htc']:5d} salas {p['salas']}"
              f" med {p['medicos_us']} rad {p['radiologistas']} carga {p['carga_tc']:.2f} dia {p['dia_us']}/{p['dia_tc']}"
              f" mes {p['mes_us']}/{p['mes_tc']} por_sala {p['por_sala']}")
