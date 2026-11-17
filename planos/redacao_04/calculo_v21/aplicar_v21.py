"""Aplica a v21 sobre a v7 FINAL da equipe (PT_simplificado_exames_de_imagem_v7_FINAL.docx, descompactada).

uso: aplicar_v21.py <docx_descompactado> limpo|marcado

Dez polos sem localizacao fixa: o plano diz so quantos polos ha em cada Regiao de Saude. Os seis
territorios da v20 viram as colunas e linhas por Regiao; o resto do texto da v7 fica como esta.
"""
import sys, os, json
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v20"))
from docxlib import Doc, q

pasta, modo = sys.argv[1], sys.argv[2]
V = json.load(open(os.path.join(AQUI, "v21.json")))
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))


def n(x):
    return f"{int(x):,}".replace(",", ".")


def dec(x, k):
    return f"{x:.{k}f}".replace(".", ",")


POLO_ANTIGO = ["Ceilândia", "Taguatinga", "Sobradinho", "Plano Piloto", "Gama", "Guará"]
ORD = V["ORD_REGIAO"]                      # Oeste, Sudoeste, Norte e Leste, Central, Sul, Centro-Sul
POLOS = V["POLOS"]
NA = {r: ("nas Regiões Norte e Leste" if r == "Norte e Leste" else f"na Região {r}") for r in ORD}
A = {r: ("As Regiões Norte e Leste realizam" if r == "Norte e Leste" else f"A Região {r} realiza") for r in ORD}
EXT_F = {1: "uma", 2: "duas", 3: "três", 4: "quatro", 5: "cinco"}
EXT_M = {1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco", 6: "seis"}
salas, hus, htc = V["salas_r"], V["hus_r"], V["htc_r"]
mus = V["medicos_us_r"]
lotados = {r: V["operadores_r"][r] + V["assistentes_r"][r] for r in ORD}


def lista(itens):
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def set_row(tbl, ri, vals, novos=()):
    cs = d.cells(d.rows(tbl)[ri])
    for ci, v in enumerate(vals):
        if v is None:
            continue
        d.set_cell(cs[ci], v, novo=ci in novos)


T = d.tables()

# ---------------- 1.9 local de execucao ----------------
d.sub("Polos de Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama e Guará",
      "Polos de Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama e Guará",
      "Dez polos nas Regiões de Saúde do Distrito Federal, na forma da subseção 4.2")

# ---------------- 3.4 distribuicao (linhas = Regioes, com o numero de polos) ----------------
d.sub("A participação de cada polo corresponde à participação das Regiões de Saúde que ele atende",
      "A participação de cada polo corresponde à participação das Regiões de Saúde que ele atende",
      "A participação dos polos de cada Região corresponde à participação dessa Região")
t5 = T[5]
set_row(t5, 0, ["Regiões de Saúde", "polos"])
for i, r in enumerate(ORD, start=1):
    set_row(t5, i, [r, str(POLOS[r])])
set_row(t5, 7, [None, "10"])

# ---------------- 3.12, 4.2 ----------------
d.sub("compatível com a implantação dos seis polos no mês 1", "seis polos", "dez polos")
d.sub("A execução ocorre em seis polos, situados de modo", "seis polos, situados", "dez polos, distribuídos")
t7 = T[7]
nova = d.clone_row(t7, 6)                      # linha de total, copiada da ultima
set_row(t7, 0, ["Regiões de Saúde", "polos"])
for i, r in enumerate(ORD, start=1):
    set_row(t7, i, [r, str(POLOS[r])])
set_row(t7, 7, ["total", "10"], novos={0, 1})
d.sub("e os seis polos realizam ultrassonografia e tomografia computadorizada.",
      ", e os seis polos realizam ultrassonografia e tomografia computadorizada.",
      ". Os dez polos realizam ultrassonografia, e a tomografia computadorizada é realizada em pelo menos um polo "
      "de cada Região de Saúde, consideradas em conjunto as Regiões Norte e Leste (subseção 7.3).")
p = d.find("quando necessária para cumprir a curva de produção, é atribuição da Coordenação Administrativa")
d.replace(p, ".", ". Nas Regiões com dois polos, a produção da Região se divide entre eles conforme a capacidade de "
          "cada um.", desde=len(d.text(p)) - 1)
d.sub("Os polos situam-se nas Regiões Administrativas de",
      "Os polos situam-se nas Regiões Administrativas de Ceilândia, Taguatinga, Sobradinho, Plano Piloto, Gama "
      "e Guará, no Distrito Federal. O endereço", "A Região Administrativa, o endereço")

# ---------------- 4.13 equipe de gestao e apoio ----------------
d.sub("se distribuem entre os seis polos:", "entre os seis polos:", "entre as Regiões de Saúde:")
t10 = T[10]
set_row(t10, 0, [None] + ORD)
set_row(t10, 3, ["por Região"])
d.sub("As duas coordenações são únicas para os seis polos", "seis polos", "dez polos")

# ---------------- 4.15 equipe assistencial ----------------
t11 = T[11]
set_row(t11, 0, [None, None] + ORD)
set_row(t11, 1, [None, str(sum(mus.values()))] + [str(mus[r]) for r in ORD])
set_row(t11, 3, [None, f"{sum(V['retaguarda_r'].values())} por dia útil"] + [str(V["retaguarda_r"][r]) for r in ORD])
set_row(t11, 4, [None, str(sum(V["rt_r"].values()))] + [str(V["rt_r"][r]) for r in ORD])
set_row(t11, 7, [None, str(sum(V["recepcao_r"].values()))] + [str(V["recepcao_r"][r]) for r in ORD])
crit = d.cells(d.rows(t11)[1])[8].find(q("p"))
d.replace(crit, "salas: 1, 4, 3, 1, 3 e 2", "salas: " + lista([str(salas[r]) for r in ORD]))
p = d.find("Ultrassonografia: as 24.317 horas de sala")
d.replace(p, "(1.322 em Ceilândia, 7.934 em Taguatinga, 5.860 em Sobradinho, 1.269 no Plano Piloto, 5.529 no Gama "
             "e 2.403 no Guará)", "(" + lista([f"{n(hus[r])} {NA[r]}" for r in ORD]) + ")")


def med(r):
    k = mus[r]
    base = f"{k} {'médico' if k == 1 else 'médicos'} {NA[r]}" if r == ORD[0] else f"{k} {NA[r]}"
    extra = ", um por polo" if mus[r] > -(-hus[r] // 1800) else ""
    return f"{base} ({n(hus[r])} ÷ 1.800 = {dec(hus[r] / 1800, 1)}{extra})"


d.replace(p, "1 médico em Ceilândia (1.322 ÷ 1.800 = 0,7), 5 em Taguatinga (7.934 ÷ 1.800 = 4,4), 4 em Sobradinho "
             "(5.860 ÷ 1.800 = 3,3), 1 no Plano Piloto (1.269 ÷ 1.800 = 0,7), 4 no Gama (5.529 ÷ 1.800 = 3,1) e 2 no "
             "Guará (2.403 ÷ 1.800 = 1,3), 17 no total, sempre em número igual ou superior ao de salas (1, 4, 3, 1, 3 e 2)",
          lista([med(r) for r in ORD]) + f", {sum(mus.values())} no total, sempre em número igual ou superior ao de "
          "salas (" + lista([str(salas[r]) for r in ORD]) + ")")
d.replace(p, "e 18 nos seis polos", "e 18 no conjunto")

# ---------------- 5 e 6 ----------------
d.replace(d.find("coordenar seis polos de execução", within=T[12]), "seis polos", "dez polos")
d.replace(d.find("6 polos em operação por 12 meses", within=T[12]), "6 polos", "10 polos")
d.replace(d.find("6 polos em operação a partir do mês 1", within=T[13]), "6 polos", "10 polos")
d.sub("As Metas 4 e 5 se decompõem por polo",
      "se decompõem por polo, na proporção da subseção 3.4 — 4.610 exames em Ceilândia, 26.888 em Taguatinga, 19.050 em "
      "Sobradinho, 4.721 no Plano Piloto, 16.336 no Gama e 7.752 no Guará —",
      "se decompõem por Região, na proporção da subseção 3.4 — " + lista(
          [f"{n(V['tot_r'][r])} exames {NA[r]}" if r == ORD[0] else f"{n(V['tot_r'][r])} {NA[r]}" for r in ORD]) + " —")

# ---------------- 7.1 ----------------
d.replace(d.find("publicação das agendas dos seis polos", within=T[15]), "seis polos", "dez polos")

# ---------------- 7.3 capacidade ----------------
d.sub("distribuídos entre os polos na proporção da subseção 3.4", "entre os polos", "entre as Regiões")
d.sub("os quantitativos diários e os equipamentos de cada polo", "de cada polo", "de cada Região")
t17 = T[17]
d.clone_row(t17, 13, after=0)                  # linha nova "Polos", copiada da linha "Tomógrafos"
set_row(t17, 0, [None, None] + ORD)
set_row(t17, 1, ["Polos", "10"] + [str(POLOS[r]) for r in ORD] + ["subseção 4.2"], novos=set(range(9)))
# linhas abaixo andaram uma posicao
set_row(t17, 11, [None, str(sum(salas.values()))] + [str(salas[r]) for r in ORD])
d.replace(d.cells(d.rows(t17)[11])[8].find(q("p")), "a carga do polo no horário de funcionamento,",
          "a carga da Região no horário de funcionamento, no mínimo uma por polo,")
set_row(t17, 12, [None, None] + [str(V["por_sala_r"][r]) for r in ORD])
d.replace(d.cells(d.rows(t17)[12])[8].find(q("p")), "salas do polo", "salas da Região")
d.replace(d.cells(d.rows(t17)[13])[8].find(q("p")), "exames do polo", "exames da Região")
set_row(t17, 14, [None, "pelo menos 6"] + ["≥ 1"] * 6)
d.replace(d.cells(d.rows(t17)[14])[8].find(q("p")), "um por polo",
          "pelo menos um por Região, consideradas em conjunto as Regiões Norte e Leste")
d.replace(d.cells(d.rows(t17)[16])[8].find(q("p")), "exames do polo", "exames da Região")
set_row(t17, 17, ["Postos de trabalho lotados na Região"])
# sai a linha "Exames por tomografo por dia util": com pelo menos um tomografo por Regiao, a conta por equipamento
# deixa de ser fixa (decisao do usuario, 07/10/2026)
linha = d.rows(t17)[15]
assert d.text(d.cells(linha)[0].find(q("p"))).startswith("Exames por tomógrafo")
if d.marcado:
    for r in d.runs_all(linha):
        d.mark_old(r)
else:
    linha.getparent().remove(linha)
p = d.find("Ceilândia realiza, por dia útil,")
velho = d.text(p)


def frase(r, primeira):
    s = salas[r]
    us_txt = f"{V['dia_us_r'][r]} exames de ultrassonografia em {EXT_F[s]} {'sala' if s == 1 else 'salas'}"
    tc_txt = f"{V['dia_tc_r'][r]} de tomografia computadorizada" if primeira else f"{V['dia_tc_r'][r]} de tomografia"
    return f"{A[r]}{', por dia útil,' if primeira else ''} {us_txt} e {tc_txt}."


def postos():
    partes = []
    for i, r in enumerate(ORD):
        k = lotados[r]
        quem = "as Regiões Norte e Leste" if r == "Norte e Leste" else f"a Região {r}"
        if i == 0:
            partes.append(f"{quem} {'têm' if r == 'Norte e Leste' else 'tem'} {EXT_M[k]} "
                          f"{'posto' if k == 1 else 'postos'} de gestão e apoio {'lotado' if k == 1 else 'lotados'}")
        else:
            partes.append(f"{quem} {EXT_M[k]}")
    return lista(partes) + "."


novo = " ".join(frase(r, i == 0) for i, r in enumerate(ORD)) + \
    " Os dez polos funcionam dez horas por dia útil; " + postos()
d.replace(p, velho, novo)
d.sub("A soma dos polos, de 265 exames", "A soma dos polos", "A soma das Regiões")
d.sub("porque a capacidade de cada polo é arredondada para cima", "de cada polo", "de cada Região")
p = d.find("Aos catorze postos lotados nos polos")
d.replace(p, "lotados nos polos", "lotados nas Regiões")
d.replace(p, "únicas para os seis", "únicas para os dez polos")
p = d.find("A carga agregada de 4.500 horas equivale a")
d.replace(p, d.text(p), "A tomografia em pelo menos um polo de cada Região mantém o exame perto do domicílio do "
          "usuário, e a folga do conjunto absorve a manutenção de cada equipamento.")

# ---------------- 7.8 e 7.9 riscos ----------------
t19 = T[19]
d.replace(d.find("redistribuição da agenda entre os seis polos", within=t19), "seis polos", "dez polos")
d.replace(d.find("seis equipamentos para uma carga de", within=t19), "seis equipamentos para uma carga de 1,79",
          "tomografia em pelo menos um polo de cada Região")
d.replace(d.find("operador de registro dedicado em cada polo", within=t19), "em cada polo", "em cada Região")
d.replace(d.find("execução por polo apurada no relatório mensal", within=t19), "execução por polo", "execução por Região")
d.sub("exige catorze salas de ultrassonografia e seis tomógrafos",
      "catorze salas de ultrassonografia e seis tomógrafos",
      "quinze salas de ultrassonografia e pelo menos seis tomógrafos")

# ---------------- 9.2 registro ----------------
d.sub("O registro é feito no polo, no mesmo dia do exame",
      "O registro é feito no polo, no mesmo dia do exame, pelo operador de registro de sistemas ali lotado. "
      "Os dados não transitam entre unidades antes de serem lançados.",
      "O registro é feito no mesmo dia do exame, pelo operador de registro de sistemas da Região do polo.")

d.save()
print(f"{modo}: {len(d.log)} trocas de texto; 10 polos em {len(ORD)} Regiões")
