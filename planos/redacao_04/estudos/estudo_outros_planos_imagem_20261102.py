"""Os exames, OCI e procedimentos que outros planos já contratam (controle interno, 02/11/2026).

Lê as planilhas orçamentárias dos planos aprovados (estudo/normalizados/pt_ses_0*/planilha.csv), a ficha
das OCI do IEV (output/ocis_iev_20261027.md) e a coleta do panorama de imagem de 02/11/2026, e escreve a
planilha do estudo dos outros planos:

    python3 planos/redacao_04/estudos/estudo_outros_planos_imagem_20261102.py <coleta.json> [<coleta_gin1.json>]

Os planos em elaboração deste repositório (redacao_06 a 09) entram só numa aba à parte: estão no campo
das ideias e não cobrem fila nenhuma (usuário, 02/11/2026).
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]

# os planos aprovados do acervo (registros/acervo.csv) e o controle externo de cada um
PLANOS = {
    "pt_ses_01": ("030989/2026", "ISHP", "29/04/2026", "Representação 28/2026 no TCDF; Decisão 1500/2026 pede esclarecimentos, em pauta em 28/09 (CT-001, CT-003)"),
    "pt_ses_02": ("030975/2026", "IEV", "29/04/2026", "Representação 31/2026 no TCDF; Decisão 1501/2026 pede esclarecimentos (CT-002, CT-005)"),
    "pt_ses_03": ("030976/2026", "IEV", "29/04/2026", "Representação 31/2026 no TCDF; Decisão 1501/2026 pede esclarecimentos (CT-002, CT-005)"),
    "pt_ses_04": ("030977/2026", "IEV", "29/04/2026", "Representação 31/2026 no TCDF; Decisão 1501/2026 pede esclarecimentos (CT-002, CT-005)"),
    "pt_ses_05": ("031061/2026", "ISHP", "09/07/2026", "sem representação no acervo"),
}
EM_ELABORACAO = [
    ["redacao_06", "pré-plano do plano 4 (exames de imagem)", "o mesmo recurso do plano 4", "não conta: é o próprio plano 4"],
    ["redacao_07", "pré-plano de imagem da Emenda de Bancada 71080005 (R$ 1,5 mi)", "12 exames de imagem (mamografia, densitometria, US e TC de cabeça e pescoço)", "não conta: está no campo das ideias (usuário, 02/11/2026)"],
    ["redacao_08", "OCI de cardiologia, Instituto Fazer o Bem (R$ 2 mi)", "OCI 09.02.01.002-6, 003-4 e 007-7, em estudo: eco, ECG, ergométrico e radiografia", "não conta: fase 0, sem escolha do usuário"],
    ["redacao_09", "MROSC de saúde mental infantojuvenil", "sem exame de imagem", "não conta"],
]
# (exame, OCI, convênio, fim da vigência, OCI contratadas, realizadas até 26/10, pedidos com o CID na fila do exame,
#  pedidos na fila do exame). Vigência: texto dos planos, item 12 (início e meses). Realizadas: consultas com o CID da
# OCI no IEV (output/ocis_iev_20261027.md). Pedidos com o CID: mapa_social_20261102_gin1.md (transvaginal) e
# output/mapeamento_iev_20261026.md (articulação, TC de pelve); fila do exame: coleta de 02/11/2026.
RESERVA_IEV = [
    ("US transvaginal", "09.06.01.001-2 GIN1", "030977", "05/2027", 3218, 20, 3068, 9295),
    ("US de articulação", "09.03.01.002-0", "030975 e 030977", "08/2027 e 05/2027", 19070, 308, 879, 14355),
    ("TC de pelve", "09.03.01.003-8", "030977", "05/2027", 539, 94, 7, 5044),
    ("US de próstata transretal", "09.01.01.004-9", "030977", "05/2027", 1015, 0, 22, 22),
]
CODIGO = re.compile(r"\b(0\d\.\d\d\.\d\d\.\d{3}-\d)\b")
CODIGO_CURTO = re.compile(r"\b(09\.\d\d\.\d\d\.\d{3})(-\d)?\b")
MODALIDADE = {"02.04": "Radiologia", "02.05": "Ultrassom", "02.06": "Tomografia", "02.07": "Ressonância",
              "02.08": "Medicina nuclear"}


def numero(texto):
    t = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return float(t) if t else None


def itens_assistenciais():
    """A Meta 2 (execução assistencial) de cada plano aprovado, item a item."""
    saida = []
    for plano, (convenio, proponente, assinatura, controle) in PLANOS.items():
        caminho = RAIZ / "estudo" / "normalizados" / plano / "planilha.csv"
        na_meta2 = False
        for r in csv.reader(open(caminho, encoding="utf-8")):
            if r[2].startswith("Meta 02"):
                na_meta2 = True
            elif r[2].startswith("Meta 03"):
                na_meta2 = False
            if not na_meta2 or not re.match(r"\d+\.\d+\.\d+", r[2]):
                continue
            descricao = " ".join(r[3].split())
            m = CODIGO_CURTO.search(descricao)
            oci = m.group(1) if m else ""
            saida.append({"plano": plano, "convenio": convenio, "proponente": proponente, "assinatura": assinatura,
                          "controle": controle, "item": r[2], "descricao": descricao[:160], "oci": oci,
                          "quantidade": int(numero(r[6]) or 0), "preco": numero(r[8]), "valor": numero(r[9])})
    return saida


def fichas_oci():
    """Exames obrigatórios e compatíveis, CID e execução no SISREG, da ficha de 10/2026 (ocis_iev_20261027.md)."""
    texto = open(RAIZ / "output" / "ocis_iev_20261027.md", encoding="utf-8").read()
    fichas = {}
    for secao in re.split(r"\n### ", texto)[1:]:
        m = re.match(r"(09\.\d\d\.\d\d\.\d{3}-\d) — (.+)", secao)
        if not m:
            continue
        campos = dict(re.findall(r"^\| ([^|]+?) \| (.+?) \|$", secao, re.M))
        fichas[m.group(1)] = {
            "nome": m.group(2).strip(),
            "obrigatorio": CODIGO.findall(campos.get("exame obrigatório", "")),
            "compativel": CODIGO.findall(campos.get("exames compatíveis", "")),
            "ficha": campos.get("ficha de 10/2026", ""),
            "sisreg": campos.get("no SISREG (até 26/10)", ""),
            "cids": len(re.findall(r"^\| [A-Z]\d\d \|", secao, re.M)),
        }
    return fichas


def fila_por_codigo(coleta):
    fila = defaultdict(lambda: [0, 0, 0])
    for bloco in coleta["panorama"].values():
        for f in bloco["filas"]:
            if "EMERG" in f["nome"].upper():
                continue
            fila[f["codigo"]][0] += f["fila"]
            fila[f["codigo"]][1] += f.get("fila_viva") or 0
            fila[f["codigo"]][2] += 1
    return fila


def main():
    coleta = json.load(open(sys.argv[1], encoding="utf-8"))
    gin1 = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else None
    itens = itens_assistenciais()
    fichas = fichas_oci()
    fila = fila_por_codigo(coleta)

    # contratado por OCI, somando os convênios; a ficha só existe para as do IEV
    por_oci = defaultdict(lambda: {"quantidade": 0, "planos": []})
    for i in itens:
        chave = next((c for c in fichas if c.startswith(i["oci"])), i["oci"]) if i["oci"] else i["descricao"][:60]
        por_oci[chave]["quantidade"] += i["quantidade"]
        por_oci[chave]["planos"].append(f"{i['plano']} ({i['convenio']}, {i['proponente']}): {i['quantidade']:,}".replace(",", "."))

    # exame de imagem × OCI: o teto do que o outro plano pode fazer daquele código
    imagem = []
    for oci, ficha in fichas.items():
        q = por_oci.get(oci, {}).get("quantidade", 0)
        for papel, codigos in (("obrigatório", ficha["obrigatorio"]), ("compatível", ficha["compativel"])):
            for c in codigos:
                mod = MODALIDADE.get(c[:5])
                if not mod:
                    continue
                f = fila.get(c, [0, 0, 0])
                imagem.append([mod, c, oci, ficha["nome"], papel, q if papel == "obrigatório" else None,
                               "até " + f"{q:,}".replace(",", ".") if papel == "compatível" else q,
                               f[0], f[1], ficha["cids"], ficha["sisreg"]])
    imagem.sort(key=lambda l: (["Ultrassom", "Tomografia", "Radiologia", "Ressonância", "Medicina nuclear"].index(l[0]), l[1]))

    wb = Workbook()
    wb.remove(wb.active)
    negrito, cinza = Font(bold=True), PatternFill("solid", fgColor="EEEEEE")

    def aba(nome, nota, cabecalho, linhas):
        ws = wb.create_sheet(nome)
        ws["A1"], ws["A1"].font = nome, Font(bold=True, size=13)
        ws["A2"] = nota
        ws["A2"].alignment = Alignment(wrap_text=True)
        ws.append([])
        ws.append(cabecalho)
        for c in ws[4]:
            c.font, c.fill = negrito, cinza
        for l in linhas:
            ws.append(l)
        for i in range(1, len(cabecalho) + 1):
            ws.column_dimensions[get_column_letter(i)].width = 20
        ws.freeze_panes = "A5"
        ws.auto_filter.ref = f"A4:{get_column_letter(len(cabecalho))}{ws.max_row}"

    aba("Planos aprovados", "A Meta 2 (execução assistencial) de cada plano de convênio aprovado pela SES-DF que está no acervo "
        "(estudo/normalizados). Quantidade, preço e valor como estão no plano.",
        ["Plano", "Convênio", "Proponente", "Assinatura", "Item", "OCI ou procedimento", "Código", "Quantidade",
         "Preço no plano (R$)", "Valor (R$)", "Controle externo"],
        [[i["plano"], i["convenio"], i["proponente"], i["assinatura"], i["item"], i["descricao"], i["oci"],
          i["quantidade"], i["preco"], i["valor"], i["controle"]] for i in itens])
    aba("Imagem nas OCI", "Cada exame de imagem que entra numa OCI contratada. Obrigatório: a OCI só fecha com ele, então o "
        "contratado é o teto de exames daquele código. Compatível: pode entrar, sem número. A fila é a de 02/11/2026, sem "
        "as filas de emergência; somar filas não dá pessoas.",
        ["Modalidade", "Código do exame", "OCI", "Nome da OCI", "Papel", "OCI contratadas", "Exames que a OCI pode fazer",
         "Fila hoje (sem emergência)", "Fila viva", "CID aceitos", "Execução no SISREG (até 26/10)"], imagem)
    linhas_gin1 = []
    if gin1:
        for nome, f in gin1["filas"].items():
            for rotulo, rec in (f.get("recortes") or {}).items():
                linhas_gin1.append([nome, rotulo, rec["fila"], rec["fila_viva"], f.get("fila"),
                                    "; ".join(f"{c} ({n})" for c, n in rec["cid_principais"][:5])])
    aba("Transvaginal e GIN1", "Quantos pedidos da fila de transvaginal têm um dos 37 CID da OCI GIN1 (09.06.01.001-2), que o IEV "
        "executa com 3.218 OCI no convênio 030977. Medição de 02/11/2026.",
        ["Fila", "Recorte", "Fila no recorte", "Fila viva no recorte", "Fila inteira", "CID principais no recorte"], linhas_gin1)
    # a reserva do IEV: o que falta cumprir, com a folga de faltas, contra os pedidos com o CID da OCI na fila do exame
    reserva = []
    for exame, oci, convenio, fim, contratado, realizadas, com_cid, fila_exame in RESERVA_IEV:
        falta_cumprir = contratado - realizadas
        r20, r30 = round(falta_cumprir / 0.8), round(falta_cumprir / 0.7)
        reserva.append([exame, oci, convenio, fim, contratado, realizadas, falta_cumprir, r20, r30, com_cid,
                        max(0, com_cid - r20), max(0, com_cid - r30), fila_exame - com_cid])
    aba("Reserva do IEV", "Regra do usuário (02/11/2026): o IEV se comprometeu com uma quantidade num prazo; o que passar "
        "disso, com folga de 20% a 30% de faltas, o plano 4 pode pegar. Reserva = OCI que faltam ÷ (1 − faltas). Só os pedidos "
        "com o CID da OCI podem virar OCI do IEV; os sem o CID já são livres. Realizadas = consultas com o CID da OCI "
        "realizadas no IEV até 26/10 (o painel não mostra a APAC).",
        ["Exame", "OCI", "Convênio", "Fim da vigência", "OCI contratadas", "Realizadas até 26/10", "Faltam cumprir",
         "Reserva com 20% de faltas", "Reserva com 30% de faltas", "Pedidos com o CID na fila do exame",
         "Sobra para o plano 4 (20%)", "Sobra para o plano 4 (30%)", "Pedidos sem o CID (já livres)"], reserva)
    aba("Nossos planos em elaboração", "Planos deste repositório que ainda não foram aprovados. Não cobrem fila nenhuma; "
        "ficam aqui para não haver sobreposição quando um deles avançar.",
        ["Pasta", "O que é", "Exames ou OCI", "Na cobertura do plano 4"], EM_ELABORACAO)
    aba("Fontes", "De onde vem cada número.", ["Fonte", "Arquivo"], [
        ["Planos aprovados", "estudo/normalizados/pt_ses_01 a 05/planilha.csv; registros/acervo.csv"],
        ["Fichas das OCI (Tabela Unificada 10/2026) e execução no SISREG", "output/ocis_iev_20261027.md"],
        ["Controle externo", "registros/acervo.csv, CT-001 a CT-005"],
        ["Fila de hoje", sys.argv[1]], ["Transvaginal × GIN1", sys.argv[2] if len(sys.argv) > 2 else "não medida"]])
    destino = AQUI / "estudo_outros_planos_imagem_20261102.xlsx"
    wb.save(destino)
    json.dump({"itens": itens, "imagem": imagem, "por_oci": por_oci, "gin1": linhas_gin1},
              open(AQUI / "estudo_outros_planos_imagem_20261102.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(destino)


if __name__ == "__main__":
    main()
