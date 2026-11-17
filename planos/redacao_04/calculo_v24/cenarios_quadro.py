"""Cenarios do quadro de gestao do plano 4 (20/10/2026), rodados no calculo da v22.

Cada cenario troca so o QUADRO do calculo_v22.py (o resto igual: 8 meses, 168 dias uteis, unitarios da
Portaria SAES/MS 4.282/2026, fila de 10/09/2026 e acrescimo pelas entradas de 2026) e grava o resultado em
cenarios_quadro.json, que planilha_cenarios_quadro.py transforma na planilha de dados/.

Uso: python3 cenarios_quadro.py
"""
import json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v19"))

SRC = open(os.path.join(AQUI, "..", "calculo_v22", "calculo_v22.py"), encoding="utf-8").read()
HOJE = {"dir": "14500.00", "op": "9500.00", "assist": "10500.00", "sup": "6155.00", "asst": "3200.00",
        "oper": "4300.00", "admfin": "10500.00", "assess": "5455.00"}
PROPOSTO = dict(HOJE, op="8400.00", admfin="8400.00")   # aba "Precificacao proposta" da planilha


def quadro(preco, terc, n_oper):
    q = [("Direção Executiva de Projeto", 1, preco["dir"], 1, "1.1.1"),
         ("Coordenação Operacional", 1, preco["op"], 1, "1.1.2")]
    if terc:
        q.append(("Coordenação Assistencial", 1, preco["assist"], 1, "1.1.3"))
    q += [("Supervisão de Polo Assistencial", 3, preco["sup"], 1, "1.1.4"),
          ("Assistente Administrativo", 6, preco["asst"], 2, "2.1.1"),
          ("Operador de registro de sistemas", n_oper, preco["oper"], 3, "3.1.1"),
          ("Coordenação Administrativa e Financeira", 1, preco["admfin"], 6, "6.1.1"),
          ("Assessoria de Prestação de Contas", 1, preco["assess"], 6, "6.1.2")]
    return q


CENARIOS = {  # chave: (preco, 3a coordenacao, operadores)
    "1": (HOJE, False, 10), "2": (HOJE, True, 6), "3": (HOJE, True, 8),
    "1p": (PROPOSTO, False, 10), "2p": (PROPOSTO, True, 6), "3p": (PROPOSTO, True, 8),
}
SAIDA_RES = ("print('RES', json.dumps({'total': sum(qc.values()), 'apoio': str(APOIO), 'producao': str(producao), "
             "'global': str(glob), 'sobra': str(sobra), 'curva': curva_b, 'parcelas': [str(x) for x in parcelas], "
             "'prod_p': [str(x) for x in prod_b], 'apoio_p': [str(x) for x in apoio_p], 'qc': qc}))\n")

def main():
    from calculo import Q18, por_codigo
    res = {}
    for k, (preco, terc, n_oper) in CENARIOS.items():
        q = quadro(preco, terc, n_oper)
        bloco = "QUADRO = [\n" + "".join(f'    ("{p}", {n}, D("{v}"), {m}, "{i}"),\n' for p, n, v, m, i in q) + "]\n"
        s = re.sub(r"QUADRO = \[.*?\n\]\n", bloco, SRC, flags=re.S)
        s = s.replace('assert APOIO == D("919640.00") and APOIO <= TETO', "")
        s = re.sub(r"\nout = \{.*", "\n" + SAIDA_RES, s, flags=re.S)
        tmp = os.path.join(AQUI, f"_cenario_{k}.py")
        open(tmp, "w", encoding="utf-8").write(s)
        try:
            out = subprocess.run([sys.executable, tmp], capture_output=True, text=True, check=True)
        finally:
            os.remove(tmp)
        r = json.loads([l for l in out.stdout.splitlines() if l.startswith("RES ")][0][4:])
        r["quadro"] = q
        res[k] = r
    res["fila"] = por_codigo(dict(Q18))
    json.dump(res, open(os.path.join(AQUI, "cenarios_quadro.json"), "w"), ensure_ascii=False, indent=1, default=str)
    for k in CENARIOS:
        r = res[k]
        print(k, r["total"], r["apoio"], f'{float(r["apoio"]) / float(r["global"]) * 100:.3f}%', r["producao"], r["global"])


if __name__ == "__main__":
    main()
