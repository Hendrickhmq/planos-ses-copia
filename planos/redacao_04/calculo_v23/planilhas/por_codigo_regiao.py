"""Exames por procedimento e por Regiao na v23 (= v22): mesma parte de cada fila por Regiao que o rateio usa,
arredondada para inteiros que fecham nas duas margens - total do codigo (planilha) e total de US e de TC por
Regiao (subsecao 7.3)."""
import json, math, os, sys
from fractions import Fraction as F
R4 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, R4 + "/calculo_v19")
import calculo as K

K.POLO = {"Oeste": ["Região Oeste"], "Sudoeste": ["Região Sudoeste"],
          "Norte e Leste": ["Região Norte", "Região Leste"], "Central": ["Região Central"],
          "Sul": ["Região Sul"], "Centro-Sul": ["Região Centro-Sul"]}
K.ORD = ORD = ["Oeste", "Sudoeste", "Norte e Leste", "Central", "Sul", "Centro-Sul"]
v = json.load(open(R4 + "/calculo_v22/v22.json"))
Q, qc, us, tc = v["Q"], v["qc"], v["us"], v["tc"]
tot_reg = v["tot"]

# conferencia: o rateio refeito da as Regioes da v22
t2, u2, c2, *_ = K.rateio(Q)
assert t2 == tot_reg and u2 == us and c2 == tc

x = {c: {p: F(0) for p in ORD} for c in qc}
for n, q in Q.items():
    s = K.share(n)
    for p in ORD:
        x[K.COD[n]][p] += q * s[p]
for c in qc:
    assert sum(x[c].values()) == qc[c]


def arredonda(cods, alvo_col):
    """inteiros com soma por linha = qc e por coluna = alvo_col; parte do piso e sobe pelos maiores restos,
    com caminho de aumento quando o guloso trava"""
    a = {c: {p: math.floor(x[c][p]) for p in ORD} for c in cods}
    falta_l = {c: qc[c] - sum(a[c].values()) for c in cods}
    falta_c = {p: alvo_col[p] - sum(a[c][p] for c in cods) for p in ORD}
    assert sum(falta_l.values()) == sum(falta_c.values())
    cand = sorted(((x[c][p] - a[c][p], c, p) for c in cods for p in ORD if x[c][p] != a[c][p]), reverse=True)
    sobe = set()
    for _, c, p in cand:
        if falta_l[c] > 0 and falta_c[p] > 0:
            sobe.add((c, p)); falta_l[c] -= 1; falta_c[p] -= 1
    # se sobrou falta, troca por caminho alternante sobre as celulas com fracao
    while any(falta_l.values()):
        c0 = next(c for c in cods if falta_l[c] > 0)
        # busca em largura linha -> coluna (celula nao usada) -> linha (celula usada)
        from collections import deque
        prev, fila, achou = {("l", c0): None}, deque([("l", c0)]), None
        while fila and not achou:
            no = fila.popleft()
            if no[0] == "l":
                for p in ORD:
                    if (no[1], p) not in sobe and x[no[1]][p] != a[no[1]][p] and ("c", p) not in prev:
                        prev[("c", p)] = no; fila.append(("c", p))
                        if falta_c[p] > 0:
                            achou = ("c", p); break
            else:
                for c in cods:
                    if (c, no[1]) in sobe and ("l", c) not in prev:
                        prev[("l", c)] = no; fila.append(("l", c))
        assert achou, "sem caminho"
        p_fim = achou[1]
        no = achou
        while prev[no] is not None:
            ant = prev[no]
            cel = (ant[1], no[1]) if no[0] == "c" else (no[1], ant[1])
            if no[0] == "c":
                sobe.add(cel)
            else:
                sobe.discard(cel)
            no = ant
        falta_l[c0] -= 1; falta_c[p_fim] -= 1
    for c, p in sobe:
        a[c][p] += 1
    for c in cods:
        assert sum(a[c].values()) == qc[c]
        for p in ORD:
            assert abs(a[c][p] - x[c][p]) < 1
    for p in ORD:
        assert sum(a[c][p] for c in cods) == alvo_col[p]
    return a


COD_US = [c for c in qc if c.startswith("02.05")]
COD_TC = [c for c in qc if c.startswith("02.06")]
m = {**arredonda(COD_US, us), **arredonda(COD_TC, tc)}
json.dump({"ORD": ORD, "matriz": m, "unit": {c: str(K.UNIT[c]) for c in qc}}, open(sys.argv[1], "w"),
          ensure_ascii=False, indent=1)
for c in COD_US + COD_TC:
    print(c, [m[c][p] for p in ORD], qc[c])
print("US", [sum(m[c][p] for c in COD_US) for p in ORD]); print("TC", [sum(m[c][p] for c in COD_TC) for p in ORD])
