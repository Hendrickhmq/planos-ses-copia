#!/usr/bin/env python3
"""Monta ../mapa_social_20261028.xlsx a partir de coleta_20261028.json (saída do motor).

Rodar de dentro desta pasta: python3 montar_20261028.py
Só contagens agregadas: nenhum CNS, CPF ou nome sai do painel.
As abas calculadas dizem isso no título.
"""
import json
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

AQUI = Path(__file__).resolve().parent
D = json.loads((AQUI / "coleta_20261028.json").read_text(encoding="utf-8"))
SAIDA = AQUI.parent / "mapa_social_20261028.xlsx"

NUCLEO = ["CONSULTA EM SAUDE MENTAL - PEDIATRIA",
          "CONSULTA EM SAUDE MENTAL - ADOLESCENTE",
          "CONSULTA DE PROFISSIONAIS DE NIVEL SUPERIOR NA ATENCAO ESPECIALIZADA (EXCETO MEDICO)"]


def data(serial):
    if serial is None:
        return None
    return (date(1899, 12, 30) + timedelta(days=int(serial))).strftime("%d/%m/%Y")


def r1(x):
    return None if x is None else round(x, 1)


def aba(wb, titulo, cab, linhas, nota=None):
    ws = wb.create_sheet(titulo[:31])
    i = 1
    if nota:
        ws.cell(row=1, column=1, value=nota).font = Font(italic=True)
        i = 3
    for j, c in enumerate(cab, 1):
        ws.cell(row=i, column=j, value=c).font = Font(bold=True)
    for lin in linhas:
        i += 1
        for j, v in enumerate(lin, 1):
            ws.cell(row=i, column=j, value=v)
    ws.column_dimensions["A"].width = 60
    return ws


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Leia-me"
    dt = D["datas"]
    leia = [
        "Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas",
        D["painel"],
        f"App Qlik {D['app']} ({D['titulo_app']}) · dados SISREG/DATASUS · via {D['via']}",
        f"Última recarga da base: {dt['recarga']} (qLastReloadTime {dt['recarga_utc']})",
        f"Consulta: {dt['consulta_inicio']} a {dt['consulta_fim']} (relógio do motor), sem recarga no meio",
        f"Solicitação mais recente na base: {dt['solicitacao_mais_recente']} · agendamento mais distante: {dt['agendamento_mais_distante']}",
        "Medida: fila = os três status (pendente de regulação; corrigida e reenviada para regulação; "
        "pendente de regulação por fila de espera). Devolvidas para complementação ficam fora e se contam à parte.",
        "Pessoas = CNS distintos no conjunto; só a contagem sai do motor. Espera em dias, no motor, sobre os registros.",
        f"Objeto: {D['enquadramento']['objeto']}",
        "Abas com '(calculado)' no nome somam ou dividem números do motor; as demais são do motor.",
        "redacao_09 · coleta de 28/10/2026 · script montar_20261028.py",
    ]
    for i, t in enumerate(leia, 1):
        ws.cell(row=i, column=1, value=t)
    ws.column_dimensions["A"].width = 140

    dec = {x["nome_sisreg"]: x["decisao"] for x in D["enquadramento"]["nomes_internos"]}
    E = D["estudo"]
    cab = ["fila (nome exato)", "código", "decisão", "fila", "pessoas", "devolvidas", "total (todos os status)",
           "espera média", "espera mediana", "espera máxima", "pedido mais antigo na fila",
           "primeira solicitação na base", "última solicitação na base",
           "fila 0–11", "fila 12–17", "fila 18+", "fila com CID F",
           "pessoas <18", "fila <18", "devolvidas <18", "espera média <18", "espera mediana <18", "espera máx. <18"]
    lin = []
    for r in E["linhas"]:
        lin.append([r[0], r[1], dec.get(r[0]), r[2], r[3], r[4], r[5], r1(r[6]), r1(r[7]), r1(r[8]),
                    data(r[9]), data(r[10]), data(r[11]), r[12], r[13], r[14], r[15],
                    r[22], r[23], r[18], r1(r[19]), r1(r[20]), r1(r[21])])
    aba(wb, "1 Varredura das filas", cab, lin,
        "Toda fila estudada, com a decisão. Recorte pelo nome da fila no SISREG (descrição_procedimento_solicitacao).")

    V = D["varredura_cid_F_menor_18"]
    aba(wb, "2 Varredura CID F <18", ["fila", "fila com CID F e <18", "fila <18", "fila (todas as idades)",
                                       "todos os status, CID F e <18"], V["linhas"],
        "Todas as filas da base com ao menos 5 pedidos na fila com CID F e idade < 18 na solicitação.")

    U = D["uniao"]
    cabu = ["conjunto", "fila", "pessoas", "devolvidas", "espera média", "espera mediana", "espera máxima",
            "pessoas 0–11", "pessoas 12–17", "pessoas 18+", "fila 0–11", "fila 12–17", "fila 18+"]
    lu = [["SAUDE MENTAL - PEDIATRIA + SAUDE MENTAL - ADOLESCENTE"] +
          [r1(x) if isinstance(x, float) else x for x in U["saude_mental_ped_mais_ado"]],
          ["as duas + NIVEL SUPERIOR (EXCETO MEDICO)"] +
          [r1(x) if isinstance(x, float) else x for x in U["saude_mental_mais_nivel_superior"]]]
    ws3 = aba(wb, "3 Uniões (motor)", cabu, lu,
              "Conjuntos calculados no motor, com cada pedido e cada pessoa uma vez.")
    ws3.cell(row=7, column=1, value=f"Pessoas nas duas filas de saúde mental: {U['pessoas_em_ped_e_ado']}")
    ws3.cell(row=8, column=1, value=f"Pessoas numa fila de saúde mental e na NIVEL SUPERIOR: {U['pessoas_em_saude_mental_e_nivel_superior']}")

    R = D["regiao"]
    lr = []
    for n in NUCLEO:
        for r in R[n]:
            lr.append([n, r[0] if r[0] is not None else "(sem região)", r[1], r[2], r1(r[3]), r[4]])
    for r in R["uniao_saude_mental"]:
        lr.append(["SAUDE MENTAL - PEDIATRIA + ADOLESCENTE (motor)", r[0] if r[0] is not None else "(sem região)",
                   r[1], r[2], None, None])
    aba(wb, "4 Região de Saúde", ["fila", "Região de Saúde do solicitante", "fila", "pessoas", "espera mediana",
                                 "devolvidas"], lr,
        "Região de Saúde da unidade solicitante, na medida da fila. URD = unidade de referência distrital. "
        "(sem região) = solicitante sem Região de Saúde no painel: não rateada.")

    C = D["cid_principais"]
    lc = [[n] + r for n in NUCLEO for r in C[n]]
    aba(wb, "5 CID principais", ["fila", "CID", "descrição", "fila"], lc, "Os 15 CIDs mais frequentes na fila.")

    K = D["classificacao_risco"]
    aba(wb, "5b Classificação de risco", ["classificação de risco", "PED", "ADO", "NS"], K["linhas"],
        "Pedidos na fila por classificacao_risco do SISREG.")

    S = D["series"]
    ab = {r[0]: r[1:] for r in S["abertas_por_mes_da_solicitacao"]}
    ag = {r[0]: r[1:] for r in S["agendadas_por_mes_da_solicitacao"]}
    of = {r[0]: r[1:] for r in S["agendadas_por_mes_do_agendamento"]}
    meses = sorted(set(ab) | set(ag) | set(of))
    le = []
    for m in meses:
        a = ab.get(m, [0, 0, 0]); g = ag.get(m, [0, 0, 0]); o = of.get(m, [0, 0, 0])
        le.append([m] + a + g + [a[i] + g[i] for i in range(3)] + o)
    cabe = ["mês"] + [f"abertas {k}" for k in ("PED", "ADO", "NS")] + \
           [f"agendadas pelo mês da solicitação {k}" for k in ("PED", "ADO", "NS")] + \
           [f"entrantes {k}" for k in ("PED", "ADO", "NS")] + \
           [f"agendadas pelo mês do agendamento {k}" for k in ("PED", "ADO", "NS")]
    aba(wb, "6 Entrantes e oferta (calculado)", cabe, le,
        "PED = SAUDE MENTAL - PEDIATRIA; ADO = SAUDE MENTAL - ADOLESCENTE; NS = NIVEL SUPERIOR (EXCETO MEDICO). "
        "Entrantes = abertas + agendadas pelo mês da solicitação (soma calculada). O mês corrente está incompleto.")

    aba(wb, "7 Agendadas por status", ["status do agendamento", "PED", "ADO", "NS"], S["agendadas_por_status"],
        "Todos os anos. Dado de controle interno: não entra no documento como taxa.")

    X = D["unidades_executantes"]
    aba(wb, "8 Executantes", X["cols"], X["linhas"], X["nota"])
    Y = D["agendadas_em_compp_e_adolescentro"]
    aba(wb, "9 Agendado em COMPP-Adol", ["executante", "fila", "código", "agendadas", "primeiro agendamento",
                                          "último agendamento"],
        [[r[0], r[1], r[2], r[3], data(r[4]), data(r[5])] for r in Y["linhas"]],
        "Tudo o que o painel registra como executado no COMPP e no Adolescentro (todos os anos).")
    Z = D["executante_das_filas_de_saude_mental"]
    aba(wb, "10 Executante das filas", ["fila", "executante", "agendadas", "primeiro agendamento",
                                         "último agendamento", "agendadas desde 28/10/2025"],
        [[r[0], r[1], r[2], data(r[3]), data(r[4]), r[5]] for r in Z["linhas"]],
        "Onde as filas de saúde mental e psicologia infantil foram agendadas. CRDF = Complexo Regulador (executante não identificado).")
    W = D["solicitante_compp_adolescentro"]
    aba(wb, "11 COMPP como solicitante", ["fila", "unidade solicitante", "valor", "medida"],
        [[r[0], r[1], r[2], "fila"] for r in W["fila"]] + [[r[0], r[1], r[3], "todos os status"] for r in W["fila"]] +
        [[r[0], r[1], r[2], "agendadas"] for r in W["agendadas"]],
        "COMPP e Adolescentro como unidade solicitante nas três filas do núcleo.")

    wb.save(SAIDA)
    print("gravado", SAIDA)


if __name__ == "__main__":
    main()
