"""Estudo das filas de imagem para decidir o plano 4 (controle interno, 02/11/2026).

Lê a coleta do panorama de imagem do Mapa Social e o Anexo Único da Tabela SUS Candanga e
escreve a planilha única do estudo e os números do relatório de decisão:

    python3 planos/redacao_04/estudos/estudo_filas_imagem_20261102.py \
        <coleta.json> <tabela_sus_candanga.csv> [<coleta_executante.json>]

A coleta sai de planos/redacao_04/dados/fontes/mapa_social_20261102_imagem_bruto/. O Anexo é o
de biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv do main (2.952 linhas).

O que é regra do usuário e o que é premissa está nas constantes abaixo, cada uma com a fonte.
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

# --- limites do plano 4 (v26, plano.md 8.2; D-007 em pendencias.md) ---
RECURSO = 11_592_762.00
APOIO = 956_160.00
TETO_EXAMES = RECURSO - APOIO          # o que sobra para exames com o apoio da v26
VALOR_EXAMES_V26 = 10_636_542.52       # o alvo dos estudos de 01/11
MESES = 8

# --- a v26: meta e preço por código (plano.md 2.2 e 8.2) ---
V26 = {
    "02.05.02.009-7": (14689, 99.94), "02.05.01.004-0": (14508, 100.18),
    "02.05.02.004-6": (13166, 100.18), "02.05.02.018-6": (10541, 99.94),
    "02.06.02.003-1": (5240, 300.10), "02.06.03.001-0": (4516, 299.44),
    "02.05.02.005-4": (3944, 99.94), "02.06.03.003-7": (3862, 299.44),
    "02.05.02.012-7": (3216, 99.94), "02.05.02.010-0": (3201, 99.94),
    "02.05.02.003-8": (2261, 99.94),
}

# --- cobertura dos outros planos: só os aprovados (estudo_outros_planos_imagem_20261102.md) ---
# O redacao_07 e os demais planos em elaboração não cobrem fila: estão no campo das ideias (usuário, 02/11/2026).
IEV_TC_ORTOPEDIA = {  # OCI 09.03.01.003-8: fora inteiras (L-008, item 2)
    "02.06.01.001-0", "02.06.01.002-8", "02.06.01.003-6", "02.06.02.001-5", "02.06.03.002-9",
    "02.06.02.002-3",
}
IEV_POR_CID = {  # o código fica, sem os pedidos com o CID da OCI
    "02.06.03.003-7": "OCI 09.03.01.003-8 (IEV, ortopedia com TC): TC de pelve sem os 46 CID",
    "02.05.02.006-2": "OCI 09.03.01.002-0 (IEV, ortopedia com US): articulação sem os 32 CID",
    "02.05.02.018-6": "OCI 09.06.01.001-2 GIN1 (IEV, 3.218 contratadas): transvaginal obrigatória, 37 CID (C51-C58, D25, N70-N99) — não está na L-008",
    "02.05.02.011-9": "OCI 09.01.01.004-9 (IEV, próstata): transretal obrigatória, 6 CID",
    "02.05.01.001-6": "OCI 09.02.01.004-2 (IEV, coronariana): eco de estresse obrigatória",
    "02.05.01.003-2": "OCI 09.02.01.006-9 (IEV): ecocardiografia transtorácica, compatível",
}
# a parte da fila com o CID da OCI, onde já foi medida; sem medida, a fila parcial não entra na carteira
PARTE_COM_CID = {
    "02.06.03.003-7": 7 / 5944,      # output/mapeamento_iev_20261026.md, 27/10/2026
    "02.05.02.006-2": 879 / 14391,   # output/mapeamento_iev_20261026.md, 26/10/2026
    # transvaginal: 4.000 reservados à GIN1 do IEV (usuário, 02/11/2026; L-008 revista). A medição de 02/11 achou
    # 3.068 pedidos com os 37 CID da GIN1 (dados/fontes/mapa_social_20261102_gin1.md); a reserva é maior, pela folga de faltas
    "02.05.02.018-6": 4000 / 9295,
}
# no código de ultrassom ou TC, mas pede outro profissional ou outro equipamento
OUTRA_EQUIPE = {
    "02.05.01.001-6": "eco de estresse: laudo do cardiologista ecocardiografista; é exame obrigatório da OCI coronariana "
                      "do IEV (900 contratadas)",
    "02.05.01.002-4": "eco transesofágica: laudo do cardiologista ecocardiografista",
    "02.05.01.003-2": "ecocardiografia: o IEV alcança só até 1.000 (OCI de insuficiência cardíaca), e o resto da fila "
                      "está livre; fica fora porque o laudo é do cardiologista ecocardiografista, que a rede do plano 4 "
                      "não tem",
    "02.06.01.009-5": "PET-CT: medicina nuclear",
    "02.05.02.002-0": "paquimetria: oftalmologia",
    "02.05.02.008-9": "globo ocular: exame do oftalmologista, com sonda própria, e a Candanga paga R$ 24,20, abaixo "
                      "do custo do exame",
    "02.05.02.014-3": "obstétrica: o exame tem o prazo da gestação, e o pedido antigo não tem mais paciente",
    "02.05.02.015-1": "obstétrica com Doppler: o prazo da gestação",
    "02.05.01.005-9": "Doppler de fluxo obstétrico: o prazo da gestação",
}
MINIMO_FILA = 30         # fila menor que isto não vira item de agenda próprio na carteira

# --- capacidade do plano 4: polos de ultrassom e tomografia (estudo_polos_rede_capacidade) ---
MODALIDADE = {"02.04": "Radiologia", "02.05": "Ultrassom", "02.06": "Tomografia",
              "02.07": "Ressonância", "02.08": "Medicina nuclear", "02.10": "Radiologia intervencionista"}
NO_PLANO_4 = {"Ultrassom", "Tomografia"}
SALAS_US = 13            # salas_ultrassom_metricas_20261020.xlsx, cenário 1 (documento da equipe)
HORAS_DIA = 10
OCUPACAO = 0.8
DIAS_UTEIS_MES = 21
TOMOGRAFOS = 6           # v26: seis tomógrafos na rede

# --- custo (estudos/custo_por_exame_v2_20261020.xlsx, aba Premissas e Tomografia por polo) ---
SALA_APARELHO_HORA = (3000 + 2500) / 168   # premissa: aluguel de sala e aparelho, 168 h por mês
MEDICO_HORA = 100.0                         # premissa: R$ 1.000 por 30 exames de 20 min
INSUMO = 3.0                                # hipótese
TC_CLINICA = 171.44                         # cotado: média da rede de TC do ISHP, R$ 165-175 com contraste

EMERGENCIA = re.compile(r"\b(EMERG|URGEN|PRONTO.SOCORRO|P\.S\.|INTERNAD|LEITO|UTI)\w*")
CONTRASTE = re.compile(r"C/\s*CONTR|COM CONTRASTE|C/CONT")
SEM_CONTRASTE = re.compile(r"S/\s*CONTR|SEM CONTRASTE")
INFANTIL = re.compile(r"INFANT|PEDIAT|CRIAN|NEONAT|RN\b")
ANGIO_CORONARIA = re.compile(r"ANGIO\w*.*CORON")
ANGIO = re.compile(r"ANGIO")
MEMBROS = re.compile(r"MMII|MMSS|MEMBRO|VENOSO|ARTERIAL DE M|ARTERIAL - M")
AORTA = re.compile(r"AORTA|ILIAC")


def minutos(codigo, nome):
    """Tempo de sala: o CBR 2017 no ultrassom, os intervalos do plano 4 na TC (estudo de 01/11, aba 6)."""
    if codigo.startswith("02.06"):
        if ANGIO_CORONARIA.search(nome):
            return 30, "hipótese (angio coronária)"
        return (15, "plano 4 (sem contraste)") if SEM_CONTRASTE.search(nome) else (20, "plano 4 (com contraste)")
    if codigo.startswith("02.05"):
        if codigo == "02.05.01.004-0":
            if MEMBROS.search(nome):
                return 40, "CBR 2017, 2 × 20 (extrapolação)"
            if AORTA.search(nome):
                return 30, "CBR 2017"
            return 20, "CBR 2017"
        if codigo.startswith("02.05.01"):
            return 30, "hipótese (eco)"
        if codigo in ("02.05.02.004-6", "02.05.02.009-7"):
            return 20, "CBR 2017"
        if "MORFOL" in nome:
            return 45, "CBR 2017"
        if "TRANSFONTANELA" in nome:
            return 25, "CBR 2017"
        return 15, "CBR 2017"
    return None, "fora do ultrassom e da TC"


def custo_exame(codigo, mins):
    if codigo.startswith("02.06"):
        return TC_CLINICA, "cotado"
    if codigo.startswith("02.05") and mins:
        return round((MEDICO_HORA + SALA_APARELHO_HORA) * mins / 60 + INSUMO, 2), "premissa"
    return None, ""


def ler_candanga(caminho):
    """Valor SIA do Anexo Único; vale o SIGTAP quando é maior ou igual (LI-002, F-04)."""
    preco = {}
    with open(caminho, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["modalidade"] != "SIA":
                continue
            valor = float(r["valor"])
            sigtap = float(r["sigtap_vigente"]) if r["sigtap_vigente"] else 0.0
            preco[r["codigo_sigtap"]] = (max(valor, sigtap), r["procedimento"],
                                         "SIGTAP ≥ Candanga" if sigtap >= valor else "Candanga SIA")
    return preco


def meses_para_zerar(fila, entram_mes, oferta_mes):
    """Meses até a fila zerar se o ritmo continuar: a fila ÷ o que a oferta passa da entrada. None = não zera."""
    folga = oferta_mes - entram_mes
    return round(fila / folga, 1) if folga > 0 else None


def tempos(r):
    e_mes = (r["entrantes_12m"] or 0) / 12
    z12 = meses_para_zerar(r["fila"], e_mes, (r["oferta_12m"] or 0) / 12)
    z3 = meses_para_zerar(r["fila"], e_mes, r["oferta_media_3m"] or 0)
    return z12, z3


def classe_rumo(r):
    """A classe do código pelo tempo que a fila leva para zerar no ritmo da SES (relatório, seção 3).

    O prazo de referência é o do plano (MESES). É estimativa por entradas e agendamentos, não a queda
    observada do estoque.
    """
    if r is None:
        return "sem série", "o código não veio no rumo"
    e12, o12 = r["entrantes_12m"] or 0, r["oferta_12m"] or 0
    o_antes = r["oferta_12m_antes"] or 0
    if e12 < 120:
        return "inconclusivo", "menos de 10 pedidos por mês"
    z12, z3 = tempos(r)
    pico = r["pico_oferta"] or 0
    if o12 and pico > 2.5 * (o12 / 12) and o12 > o_antes * 1.2 and (z12 is None or z12 > MESES):
        return "esforço pontual", (f"pico de {pico} em {r['pico_oferta_mes']}, mais de 2,5 vezes a média do ano; "
                                   "acabado o esforço, a fila não zera")
    if z12 is not None and z12 <= MESES:
        return "capacidade da SES", f"no ritmo dos 12 meses, a SES zera a fila em {z12:.0f} meses, dentro do prazo do plano"
    if z12 is not None:
        return "zera devagar", (f"no ritmo dos 12 meses, a fila leva {z12:.0f} meses para zerar"
                                + (f" ({z3:.0f} no ritmo dos 3 últimos)" if z3 else ""))
    if z3 is not None and z3 <= 24:
        return "inconclusivo", (f"no ritmo dos 12 meses a fila não zera; no dos 3 últimos, levaria {z3:.0f} meses")
    if z3 is not None:
        return "déficit persistente", (f"no ritmo dos 12 meses a fila não zera; no dos 3 últimos, levaria {z3:.0f} "
                                       "meses, mais de dois anos")
    return "déficit persistente", "a oferta fica abaixo dos pedidos nos 12 meses e nos 3 últimos: a fila não zera"


def tags(nome):
    t = []
    if EMERGENCIA.search(nome):
        t.append("emergência")
    if ANGIO_CORONARIA.search(nome):
        t.append("angio coronária")
    elif ANGIO.search(nome):
        t.append("angio")
    if CONTRASTE.search(nome):
        t.append("com contraste")
    if SEM_CONTRASTE.search(nome):
        t.append("sem contraste")
    if "SEDAC" in nome and "S/SEDAC" not in nome.replace(" ", ""):
        t.append("sedação")
    if INFANTIL.search(nome):
        t.append("infantil")
    return t


def cobertura(codigo, nome, ts):
    """Quem já atende a fila: D-009, L-008, o IEV por CID, ou a capacidade do plano 4."""
    if "emergência" in ts:
        return "fora", "D-009: só ambulatório"
    if codigo in IEV_TC_ORTOPEDIA:
        return "fora", "L-008: TC compatível com a OCI 09.03.01.003-8 do IEV"
    if codigo == "02.05.02.006-2" and "PARTES MOLES" in nome and "REGIA" not in nome:
        return "fora", "L-008: partes moles são do IEV"
    if codigo == "02.05.02.006-2":
        return "fora", "L-008 revista: articulação comprometida com a OCI 09.03.01.002-0 do IEV (usuário, 02/11/2026)"
    if MODALIDADE.get(codigo[:5]) == "Radiologia":
        return "fora", "mapeada, fora do foco: o plano 4 ataca agora ultrassom e TC (usuário, 02/11/2026)"
    if MODALIDADE.get(codigo[:5]) not in NO_PLANO_4:
        return "fora", "o plano 4 tem polos de ultrassom e tomografia; esta modalidade pede outro equipamento"
    if codigo in OUTRA_EQUIPE:
        return "fora", f"pede outra equipe: {OUTRA_EQUIPE[codigo]}"
    if "CONE BEA" in nome:
        return "fora", "pede outra equipe: TC cone beam, odontologia"
    if codigo.startswith("02.06") and "sedação" in ts:
        return "fora", "TC com sedação: pede anestesia, fora da rede de clínicas do plano"
    if codigo in IEV_POR_CID:
        return "parcial", IEV_POR_CID[codigo]
    return "livre", ""


def montar(coleta, preco, executante=None):
    rumo = {r["codigo"]: r for r in coleta.get("rumo", [])}
    vistos, filas = set(), []
    for rotulo, bloco in coleta["panorama"].items():
        for f in bloco["filas"]:
            chave = (f["nome"], f["codigo"])
            if chave in vistos:
                continue
            vistos.add(chave)
            nome = f["nome"].upper()
            ts = tags(nome)
            cob, motivo = cobertura(f["codigo"], nome, ts)
            mins, base_tempo = minutos(f["codigo"], nome)
            p, desc, origem_preco = preco.get(f["codigo"], (None, "", "fora do Anexo: SIGTAP da ficha"))
            custo, tipo_custo = custo_exame(f["codigo"], mins)
            classe, por_que = classe_rumo(rumo.get(f["codigo"]))
            filas.append({
                "rotulo": rotulo, "modalidade": MODALIDADE.get(f["codigo"][:5], "outra"),
                "nome": f["nome"], "codigo": f["codigo"], "protocolo": ", ".join(ts),
                "fila": f["fila"], "fila_viva": f.get("fila_viva"), "pessoas": f.get("pessoas"),
                "devolvidas": f.get("devolvidas"), "espera_mediana": f.get("espera_mediana"),
                "mais_antiga": f.get("mais_antiga"), "agendadas_12m": f.get("agendadas_12m"),
                "cid": "; ".join(f"{c} ({n})" for c, n in (f.get("cid_principais") or [])[:3]),
                "cobertura": cob, "motivo": motivo, "classe": classe, "classe_por_que": por_que,
                "preco": p, "descricao_candanga": desc, "origem_preco": origem_preco,
                "minutos": mins, "base_tempo": base_tempo, "custo": custo, "tipo_custo": tipo_custo,
                "r_hora": round(p * 60 / mins, 2) if p and mins else None,
                "margem_hora": round((p - custo) * 60 / mins, 2) if p and mins and custo else None,
            })
    return filas, rumo


def carteira(filas, rumo, alvo, regra, crescimento=False):
    """Enche o valor dos exames pela ordem da regra, sem passar da fila de hoje."""
    # o esforço pontual que acabou deixa por baixo o déficit de antes (a mama: mutirões do HRS e da FHB, 01/11)
    ordem_classe = {"déficit persistente": 0, "esforço pontual": 0, "inconclusivo": 1, "sem série": 1,
                    "zera devagar": 2, "capacidade da SES": 3}
    def disponivel(f):
        if f["cobertura"] == "livre":
            return f["fila"]
        if f["codigo"] in PARTE_COM_CID:
            return int(f["fila"] * (1 - PARTE_COM_CID[f["codigo"]]))
        return 0   # parcial sem medida do CID: fica para a medição final
    candidatas = [f for f in filas if f["cobertura"] in ("livre", "parcial") and f["preco"]
                  and f["fila"] >= MINIMO_FILA and disponivel(f) > 0
                  and f["margem_hora"] is not None and f["margem_hora"] > 0 and regra(f)]
    candidatas.sort(key=lambda f: (ordem_classe.get(f["classe"], 1), -(f["margem_hora"] or 0)))
    itens, total = [], 0.0
    for f in candidatas:
        if total >= alvo:
            break
        qtd = min(disponivel(f), int((alvo - total) // f["preco"]))
        if qtd <= 0:
            continue
        itens.append({**f, "meta": qtd, "valor": round(qtd * f["preco"], 2)})
        total += qtd * f["preco"]
    # o que faltar sai das filas parciais ainda sem a medida do CID, marcadas para a medição final
    resto = [f for f in filas if f["cobertura"] == "parcial" and f["codigo"] not in PARTE_COM_CID
             and f["codigo"] not in OUTRA_EQUIPE and f["preco"] and f["fila"] >= MINIMO_FILA
             and f["margem_hora"] and f["margem_hora"] > 0 and regra(f)]
    for f in sorted(resto, key=lambda f: -f["fila"]):
        qtd = min(f["fila"], int((alvo - total) // f["preco"]))
        if qtd <= 0:
            break
        itens.append({**f, "meta": qtd, "valor": round(qtd * f["preco"], 2), "cobertura": "parcial, CID a medir"})
        total += qtd * f["preco"]
    if not crescimento:
        return itens
    return pedidos_novos(itens, rumo, alvo, total)


def pedidos_novos(itens, rumo, alvo, total):
    """Completa o valor com os pedidos novos esperados: só nos códigos em déficit persistente, até o saldo por mês ×
    os meses de execução, pela maior fila do código já na carteira, da que rende mais por hora para a que rende menos."""
    novos = []
    for codigo, r in rumo.items():
        if classe_rumo(r)[0] != "déficit persistente" or (r["saldo_mes"] or 0) <= 0:
            continue
        no_codigo = [i for i in itens if i["codigo"] == codigo]
        if no_codigo:
            novos.append((max(no_codigo, key=lambda i: i["meta"]), round(r["saldo_mes"] * MESES)))
    for f, limite in sorted(novos, key=lambda x: -(x[0]["margem_hora"] or 0)):
        qtd = min(limite, int((alvo - total) // f["preco"]))
        if qtd <= 0:
            continue
        itens.append({**f, "nome": f"{f['nome']} — pedidos novos esperados em {MESES} meses", "meta": qtd,
                      "valor": round(qtd * f["preco"], 2), "fila": limite, "fila_viva": qtd,
                      "cobertura": "crescimento da fila"})
        total += qtd * f["preco"]
    return itens


def carteira_v26_mais_tc(filas, alvo, regra, rumo=None):
    """A v26 como está, código por código, limitada à fila elegível de hoje; o que faltar do valor vira TC.

    Em cada código, as filas entram da maior para a menor. A TC extra sai das filas de TC elegíveis que sobraram,
    da que rende mais por hora para a que rende menos.
    """
    def disponivel(f):
        if f["cobertura"] == "livre":
            return f["fila"]
        if f["codigo"] in PARTE_COM_CID:
            return int(f["fila"] * (1 - PARTE_COM_CID[f["codigo"]]))
        return 0
    elegiveis = [f for f in filas if f["cobertura"] in ("livre", "parcial") and f["preco"] and regra(f)
                 and disponivel(f) > 0 and f["margem_hora"] is not None and f["margem_hora"] > 0]
    itens, usado, total = [], defaultdict(int), 0.0
    for codigo, (meta, _) in V26.items():
        resta = meta
        for f in sorted([f for f in elegiveis if f["codigo"] == codigo], key=lambda f: -f["fila"]):
            qtd = min(resta, disponivel(f))
            if qtd <= 0:
                break
            itens.append({**f, "meta": qtd, "valor": round(qtd * f["preco"], 2)})
            usado[(f["nome"], f["codigo"])] += qtd
            total += qtd * f["preco"]
            resta -= qtd
    tc = [f for f in elegiveis if f["modalidade"] == "Tomografia" and f["fila"] >= MINIMO_FILA]
    for f in sorted(tc, key=lambda f: -(f["margem_hora"] or 0)):
        livre = disponivel(f) - usado[(f["nome"], f["codigo"])]
        qtd = min(livre, int((alvo - total) // f["preco"]))
        if qtd <= 0:
            continue
        itens.append({**f, "nome": f["nome"], "meta": qtd, "valor": round(qtd * f["preco"], 2),
                      "cobertura": f["cobertura"] + ", TC a mais"})
        usado[(f["nome"], f["codigo"])] += qtd
        total += qtd * f["preco"]
    # o mesmo item pode ter entrado duas vezes (meta da v26 e TC a mais): junta
    juntos = {}
    for i in itens:
        k = (i["nome"], i["codigo"])
        if k in juntos:
            juntos[k]["meta"] += i["meta"]
            juntos[k]["valor"] = round(juntos[k]["valor"] + i["valor"], 2)
        else:
            juntos[k] = dict(i)
    itens = list(juntos.values())
    if rumo is None:
        return itens
    return pedidos_novos(itens, rumo, alvo, sum(i["valor"] for i in itens))


def crescimento_e_faltas(filas, rumo, itens, regra):
    """Para cada código da carteira: quanto a fila cresce em MESES meses e se há pedidos para cobrir as faltas.

    Agendamentos necessários = meta ÷ (1 − faltas), com 20% e 30%. Pedidos disponíveis = a fila elegível de hoje
    mais o crescimento líquido (o que entra além do que a SES agenda) no período, na mesma proporção de livres.
    É controle interno: o plano não traz taxa de faltas (absenteísmo é tratamento interno).
    """
    meta = defaultdict(int)
    for i in itens:
        meta[i["codigo"]] += i["meta"]
    elegivel, total_fila = defaultdict(int), defaultdict(int)
    for f in filas:
        if f["modalidade"] not in NO_PLANO_4 or f["motivo"].startswith("D-009"):
            continue
        total_fila[f["codigo"]] += f["fila"]
        if f["cobertura"] == "fora" or not regra(f):
            continue
        parte = PARTE_COM_CID.get(f["codigo"], 0) if f["cobertura"] == "parcial" else 0
        elegivel[f["codigo"]] += int(f["fila"] * (1 - parte))
    linhas = []
    for codigo in sorted(meta, key=lambda c: -meta[c]):
        r = rumo.get(codigo)
        if not r:
            continue
        entram = (r["entrantes_12m"] or 0) / 12
        oferta = (r["oferta_12m"] or 0) / 12
        liquido = entram - oferta
        proporcao = elegivel[codigo] / total_fila[codigo] if total_fila[codigo] else 0
        cresce = round(max(0, liquido) * MESES * proporcao)
        disponivel = elegivel[codigo] + cresce
        m = meta[codigo]
        n20, n30 = round(m / 0.8), round(m / 0.7)
        bruto = round(entram * MESES)
        faltam20, faltam30 = max(0, n20 - disponivel), max(0, n30 - disponivel)
        linhas.append([codigo, next(i["descricao_candanga"] for i in itens if i["codigo"] == codigo), elegivel[codigo],
                       round(entram), round(oferta), round(liquido), round(max(0, liquido) * MESES), bruto,
                       r["falta_12m"], m, n20, n30, disponivel, disponivel - n20, disponivel - n30,
                       faltam20, faltam30, round(faltam20 / bruto, 3) if bruto else None,
                       round(faltam30 / bruto, 3) if bruto else None])
    return linhas


def horas(itens):
    us = sum(i["meta"] * i["minutos"] for i in itens if i["modalidade"] == "Ultrassom") / 60
    tc = sum(i["meta"] * i["minutos"] for i in itens if i["modalidade"] == "Tomografia") / 60
    return us, tc


def capacidade():
    por_sala = HORAS_DIA * OCUPACAO * DIAS_UTEIS_MES * MESES
    return SALAS_US * por_sala, TOMOGRAFOS * por_sala


def resumo_v26(preco):
    linhas = []
    for c, (meta, p_antigo) in V26.items():
        p = preco[c][0]
        linhas.append({"codigo": c, "descricao": preco[c][1], "meta": meta, "preco_v26": p_antigo,
                       "preco_candanga": p, "valor_v26": round(meta * p_antigo, 2),
                       "valor_candanga": round(meta * p, 2)})
    return linhas


# quem atende cada código, pelos planos aprovados (estudo_outros_planos_imagem_20261102.md)
QUEM_ATENDE = {
    "02.05.02.006-2": ("IEV — convênios 030975 (pt_ses_02) e 030977 (pt_ses_04)",
                       "OCI 09.03.01.002-0, ortopedia com US: a US de articulação é obrigatória", 19070),
    "02.05.02.018-6": ("IEV — convênio 030977 (pt_ses_04)",
                       "OCI 09.06.01.001-2 GIN1, ginecologia: a transvaginal é obrigatória", 3218),
    "02.06.03.003-7": ("IEV — convênio 030977 (pt_ses_04)",
                       "OCI 09.03.01.003-8, ortopedia com TC: a TC de pelve é compatível (até 539 TC no conjunto)", 539),
    "02.05.02.011-9": ("IEV — convênio 030977 (pt_ses_04)",
                       "OCI 09.01.01.004-9, próstata: a transretal é obrigatória", 1015),
    "02.05.01.001-6": ("IEV — convênio 030977 (pt_ses_04)",
                       "OCI 09.02.01.004-2, coronariana: o eco de estresse é obrigatório", 900),
    "02.05.01.003-2": ("IEV — convênio 030977 (pt_ses_04)",
                       "OCI 09.02.01.006-9, insuficiência cardíaca: a eco é compatível", 1000),
}
for _c in IEV_TC_ORTOPEDIA:
    QUEM_ATENDE[_c] = ("IEV — convênio 030977 (pt_ses_04)",
                       "OCI 09.03.01.003-8, ortopedia com TC: a TC é compatível (até 539 TC no conjunto)", 539)


def quem_atende(filas, cenarios):
    """Uma linha por código e situação: quem atende, a regra e o que sobra para o plano 4."""
    nomes = list(cenarios)
    meta = [defaultdict(int) for _ in nomes]
    for k, itens in enumerate(cenarios.values()):
        for i in itens:
            meta[k][i["codigo"]] += i["meta"]
    grupos = defaultdict(lambda: {"fila": 0, "desc": "", "motivo": ""})
    for f in filas:
        if f["modalidade"] not in NO_PLANO_4 or f["motivo"].startswith("D-009"):
            continue
        situacao = f["cobertura"]
        motivo = f["motivo"] if situacao == "fora" else ""
        g = grupos[(f["codigo"], situacao, motivo)]
        g["fila"] += f["fila"]
        g["desc"] = f["descricao_candanga"] or f["nome"]
        g["motivo"] = motivo
    linhas = []
    for (codigo, situacao, motivo), g in sorted(grupos.items(), key=lambda x: (["livre", "parcial", "fora"].index(x[0][1]), x[0][0])):
        plano, oci, contratado = QUEM_ATENDE.get(codigo, ("", "", None))
        if situacao == "livre":
            quem, regra, com_cid, livres = "nenhum plano aprovado", "todos os pedidos podem entrar", 0, g["fila"]
            plano, oci, contratado = "", "", None
        elif situacao == "parcial":
            quem = plano
            if codigo in PARTE_COM_CID:
                com_cid = round(g["fila"] * PARTE_COM_CID[codigo])
                regra = ("4.000 pedidos reservados à OCI do IEV (usuário, 02/11/2026); o resto é livre"
                         if codigo == "02.05.02.018-6" else
                         "entram só os pedidos SEM o CID da OCI; os com o CID ficam com o outro plano")
            else:
                com_cid, regra = None, "CID ainda não medido: fica fora até a medição"
            livres = g["fila"] - com_cid if com_cid is not None else 0
        else:
            com_cid, livres = None, 0
            if "partes moles" in motivo:
                quem = "IEV — convênios 030975 e 030977"
                oci = "partes moles no código da articulação: ficam com o IEV por decisão do usuário (01/11/2026)"
                regra = "fila inteira fora do plano 4"
            elif "IEV" in motivo or "L-008" in motivo:
                quem, regra = plano, "fila inteira fora do plano 4"
            elif codigo in OUTRA_EQUIPE and plano:
                quem, regra = f"{plano}, em parte", f"fora do plano 4 por viabilidade — {motivo}"
            else:
                quem, regra, oci, contratado = "ninguém", f"fora do plano 4 por viabilidade — {motivo}", "", None
        linhas.append([g["desc"], codigo, situacao, quem, oci, contratado, regra, g["fila"], com_cid, livres,
                       *[meta[k].get(codigo, 0) if situacao != "fora" else 0 for k in range(len(nomes))]])
    return linhas, nomes


def escrever(filas, rumo, cenarios, v26, destino, fontes, executante=None):
    wb = Workbook()
    titulo = Font(bold=True, size=13)
    negrito = Font(bold=True)
    cinza = PatternFill("solid", fgColor="EEEEEE")

    def aba(nome, cabecalho, linhas, nota):
        ws = wb.create_sheet(nome)
        ws["A1"] = nome
        ws["A1"].font = titulo
        ws["A2"] = nota
        ws["A2"].alignment = Alignment(wrap_text=True)
        ws.append([])
        ws.append(cabecalho)
        for c in ws[4]:
            c.font = negrito
            c.fill = cinza
        for l in linhas:
            ws.append(l)
        for i, _ in enumerate(cabecalho, 1):
            ws.column_dimensions[get_column_letter(i)].width = 18
        ws.freeze_panes = "A5"
        ws.auto_filter.ref = f"A4:{get_column_letter(len(cabecalho))}{ws.max_row}"
        return ws

    wb.remove(wb.active)
    linhas_quem, nomes = quem_atende(filas, cenarios)
    ws = aba("Quem atende o quê", ["Exame (descrição Candanga)", "Código", "Situação", "Quem atende hoje",
                                   "OCI e papel do exame", "Contratado no outro plano (OCI)", "Regra para o plano 4",
                                   "Pedidos na fila (sem emergência)", "Reservados ao outro plano",
                                   "Livres para o plano 4", *[f"Na carteira {n.split(':')[0].split(' ')[0]}" for n in nomes]],
             linhas_quem,
             "Ultrassom e TC ambulatoriais. LIVRE: nenhum plano aprovado atende; todos os pedidos podem entrar. PARCIAL: "
             "uma OCI que o IEV já contratou aceita parte dos pedidos (os com o CID dela); esses ficam com o IEV e o resto "
             "fica livre (L-008, um pedido, um plano). FORA: a fila inteira já tem dono ou não cabe no plano 4. Só contam os "
             "planos aprovados; os nossos em elaboração (redacao_06 a 09) não cobrem fila. A parte com CID vem das medições "
             "de 26/10 (articulação), 27/10 (TC de pelve) e 02/11 (transvaginal); a medição final se refaz na fase 0. "
             f"Nas carteiras, fila com menos de {MINIMO_FILA} pedidos não vira item, por isso a carteira pode ficar abaixo "
             "dos livres; e a carteira para quando o valor acaba.")
    ws.row_dimensions[2].height = 90
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["D"].width = 34
    ws.column_dimensions["E"].width = 44
    ws.column_dimensions["G"].width = 44
    cores = {"livre": "E2F0D9", "parcial": "FFF2CC", "fora": "F4CCCC"}
    for linha in ws.iter_rows(min_row=5):
        if linha[2].value in cores:
            linha[2].fill = PatternFill("solid", fgColor=cores[linha[2].value])
    aba("Inventário", ["Modalidade", "Nome exato da fila", "Código", "Protocolo", "Fila", "Fila viva 24 m",
                       "Pessoas", "Devolvidas (à parte)", "Espera mediana (dias)", "Pedido mais antigo",
                       "Agendadas 12 m", "CID principais"],
        [[f["modalidade"], f["nome"], f["codigo"], f["protocolo"], f["fila"], f["fila_viva"], f["pessoas"],
          f["devolvidas"], round(f["espera_mediana"]) if f["espera_mediana"] else None, f["mais_antiga"],
          f["agendadas_12m"], f["cid"]] for f in sorted(filas, key=lambda f: (f["codigo"], -f["fila"]))],
        "Todas as filas de imagem do panorama (nome exato × código), sem corte de tamanho. A fila são os três status "
        "pendentes; as devolvidas ficam ao lado e não se subtraem. Somar filas não dá pessoas únicas.")
    aba("Rumo por código", ["Código", "Maior fila", "Fila", "Fila viva", "Devolvidas", "Entrantes 12 m",
                            "Entrantes 12 m antes", "Oferta 12 m", "Oferta 12 m antes", "Realizados 12 m",
                            "Faltas 12 m", "Falta (%)", "Saldo por mês", "Pico de oferta", "Mês do pico",
                            "Oferta média 3 m", "Meses para zerar (ritmo 12 m)", "Meses para zerar (ritmo 3 m)",
                            "Meses de oferta no estoque", "Classe", "Por quê"],
        [[c, r["fila_maior"], r["fila"], r["fila_viva"], r["devolvidas"], r["entrantes_12m"],
          r["entrantes_12m_antes"], r["oferta_12m"], r["oferta_12m_antes"], r["realizados_12m"], r["faltas_12m"],
          r["falta_12m"], r["saldo_mes"], r["pico_oferta"], r["pico_oferta_mes"], r["oferta_media_3m"],
          *[t if t is not None else "não zera" for t in tempos(r)],
          round(r["fila"] / (r["oferta_12m"] / 12), 1) if r["oferta_12m"] else None,
          *classe_rumo(r)] for c, r in sorted(rumo.items())],
        "Série por código, não por fila: a rede oferta o exame, e um código junta muitos nomes. Entrantes pelo mês do "
        "pedido; oferta pelo mês do agendamento. É estimativa por entradas e agendamentos, e não a queda observada do "
        "estoque. As faltas servem ao estudo e não vão para o plano (absenteísmo é tratamento interno).")
    aba("Cobertura", ["Nome exato da fila", "Código", "Fila", "Situação", "Quem atende ou por que fica fora"],
        [[f["nome"], f["codigo"], f["fila"], f["cobertura"], f["motivo"]]
         for f in sorted(filas, key=lambda f: (f["cobertura"], f["codigo"])) if f["cobertura"] != "livre"],
        "Só as filas fora ou parciais. Parcial: o código fica, sem os pedidos com o CID da OCI; a quantidade exata "
        "sai da medição final com o filtro de CID. Um código compartilhado não é cobertura integral da fila.")
    aba("Viabilidade", ["Nome exato da fila", "Código", "Descrição Candanga", "Preço (R$)", "Origem do preço",
                        "Minutos", "Base do tempo", "Custo por exame (R$)", "Custo é", "R$ por hora",
                        "Margem por hora (R$)", "Classe do código", "Fila", "Situação"],
        [[f["nome"], f["codigo"], f["descricao_candanga"], f["preco"], f["origem_preco"], f["minutos"],
          f["base_tempo"], f["custo"], f["tipo_custo"], f["r_hora"], f["margem_hora"], f["classe"], f["fila"],
          f["cobertura"]] for f in sorted(filas, key=lambda f: -(f["margem_hora"] or -1e9))
         if f["modalidade"] in NO_PLANO_4 and f["cobertura"] != "fora"],
        "Ultrassom feito por nós: médico R$ 100 por hora, sala e aparelho R$ 5.500 por mês em 168 h, insumo R$ 3 "
        "(premissas da custo_por_exame_v2). Tomografia na clínica: R$ 171,44 com contraste (cotado na rede do ISHP). "
        "Não se compara a hora do ultrassom com a do tomógrafo.")
    cap_us, cap_tc = capacidade()
    linhas = []
    for nome, itens in cenarios.items():
        us, tc = horas(itens)
        linhas.append([nome, sum(i["meta"] for i in itens), round(sum(i["valor"] for i in itens), 2),
                       round(us), round(us / cap_us, 3), round(tc), round(tc / cap_tc, 3),
                       sum(i["meta"] for i in itens if i["cobertura"] == "parcial")])
    ws = aba("Carteiras", ["Carteira", "Exames", "Valor dos exames (R$)", "Horas de ultrassom", "Uso das salas",
                           "Horas de tomógrafo", "Uso dos tomógrafos", "Exames de filas parciais (filtro de CID)"],
             linhas, f"Capacidade em {MESES} meses a {OCUPACAO:.0%} de {HORAS_DIA} h por dia útil: {SALAS_US} salas de "
             f"ultrassom ({cap_us:,.0f} h) e {TOMOGRAFOS} tomógrafos ({cap_tc:,.0f} h). Alvo: R$ {VALOR_EXAMES_V26:,.2f}.")
    ws.append([])
    ws.append(["Carteira", "Nome exato da fila", "Código", "Meta", "Preço (R$)", "Valor (R$)", "Classe", "Situação"])
    for c in ws[ws.max_row]:
        c.font = negrito
    for nome, itens in cenarios.items():
        for i in itens:
            ws.append([nome, i["nome"], i["codigo"], i["meta"], i["preco"], i["valor"], i["classe"], i["cobertura"]])
    primeira = next(iter(cenarios.values()))
    aba("Crescimento e faltas", ["Código", "Exame", "Fila elegível hoje", "Entram por mês", "SES agenda por mês",
                                 "Cresce por mês (líquido)", f"Cresce em {MESES} meses (líquido)",
                                 f"Entram em {MESES} meses (bruto)", "Faltas na SES (12 m)", "Meta da carteira 1",
                                 "Agendamentos com 20% de faltas", "Agendamentos com 30% de faltas",
                                 "Pedidos disponíveis no período", "Sobra com 20%", "Sobra com 30%",
                                 "Pedidos que a regulação precisa mandar a mais (20%)",
                                 "Pedidos que a regulação precisa mandar a mais (30%)",
                                 "Parte das entradas do período (20%)", "Parte das entradas do período (30%)"],
        crescimento_e_faltas(filas, rumo, primeira, lambda f: "angio coronária" not in f["protocolo"]),
        f"Carteira 1. Para cumprir a meta com faltas, é preciso agendar meta ÷ (1 − faltas). Pedidos disponíveis = fila "
        f"elegível de hoje + o crescimento líquido em {MESES} meses (o que entra além do que a SES agenda), na proporção "
        "de livres. Sobra negativa: faltam pedidos para repor as faltas, e a meta depende de a SES agendar menos ou de "
        "pedidos novos além do crescimento líquido: a regulação precisa mandar ao plano essa parte das entradas do "
        "período. Faltas na SES: faltas ÷ (realizados + faltas), 12 meses. Controle "
        "interno: o plano não traz taxa de faltas.")
    aba("v26 pela Candanga", ["Código", "Descrição Candanga", "Meta v26", "Preço v26 (R$)", "Preço Candanga (R$)",
                              "Valor v26 (R$)", "Valor Candanga (R$)"],
        [[l["codigo"], l["descricao"], l["meta"], l["preco_v26"], l["preco_candanga"], l["valor_v26"],
          l["valor_candanga"]] for l in v26],
        "As metas da v26 assinada com o preço da Portaria 4.282 e com o da Candanga.")
    if executante:
        aba("Quem oferta", ["Código", "Unidade executante", "Tipo", "Agendamentos 12 m fechados",
                            "Média por mês, out. a mar.", "Média por mês, jul. a set.", "Maior mês", "Mês do maior",
                            "Out. 2026 (até 28)", "Nov. 2026 (já agendado)"], executante,
            "Oferta por unidade executante (agendamentos pelo mês em que acontecem), nos 12 meses fechados de "
            "out./2025 a set./2026. Serve para separar a oferta que fica (contratado, URD, unidade nova) do mutirão "
            "que acaba (unidade que sobe e volta a zero). Novembro ainda vai receber agendamentos.")
    aba("Fontes", ["Fonte", "Arquivo e localização"], fontes, "Toda conta do estudo sai destes arquivos.")
    wb.save(destino)


def quem_oferta(coleta):
    ex = coleta["por_codigo"]["executante"]
    linhas = [dict(zip(ex["cols"], l)) for l in ex["linhas"]]
    fechados = [f"2025-{m:02d}" for m in (10, 11, 12)] + [f"2026-{m:02d}" for m in range(1, 10)]
    por = defaultdict(lambda: defaultdict(int))
    tipo = {}
    for l in linhas:
        por[(l["codigo"], l["unidade"])][l["mes"]] += l["agendamentos"]
        tipo[(l["codigo"], l["unidade"])] = l["tipo"]
    saida = []
    for (codigo, unidade), s in por.items():
        total = sum(s[m] for m in fechados)
        if not total:
            continue
        pico, mes = max((s[m], m) for m in fechados)
        saida.append([codigo, unidade, tipo[(codigo, unidade)], total, round(sum(s[m] for m in fechados[:6]) / 6),
                      round(sum(s[m] for m in fechados[-3:]) / 3), pico, mes, s.get("2026-10", 0), s.get("2026-11", 0)])
    return sorted(saida, key=lambda l: (l[0], -l[3]))


def main():
    coleta = json.load(open(sys.argv[1], encoding="utf-8"))
    preco = ler_candanga(sys.argv[2])
    filas, rumo = montar(coleta, preco)
    # só as carteiras que chegam ao valor dos exames da v26 (usuário, 02/11/2026)
    cenarios = {
        "1 (recomendada): parede abdominal no abdômen total, sem angio coronária, com os pedidos novos esperados": carteira(
            filas, rumo, VALOR_EXAMES_V26, lambda f: "angio coronária" not in f["protocolo"], crescimento=True),
        "2: parede abdominal e angio coronária (se a SES confirmar as duas, L-007)": carteira(
            filas, rumo, VALOR_EXAMES_V26, lambda f: True),
        "3: se a SES não aceitar a parede — angio coronária e pedidos novos esperados": carteira(
            filas, rumo, VALOR_EXAMES_V26, lambda f: "PAREDE" not in f["nome"].upper(), crescimento=True),
        "4: a v26 como está, limitada à fila de hoje, mais TC e os pedidos novos esperados (com parede e angio coronária)":
            carteira_v26_mais_tc(filas, VALOR_EXAMES_V26, lambda f: True, rumo),
        "5: a v26 como está, limitada à fila de hoje, mais TC e os pedidos novos esperados, sem angio coronária":
            carteira_v26_mais_tc(filas, VALOR_EXAMES_V26, lambda f: "angio coronária" not in f["protocolo"], rumo),
    }
    v26 = resumo_v26(preco)
    fontes = [["Coleta do Mapa Social", sys.argv[1]], ["Tabela SUS Candanga, Anexo Único", sys.argv[2]],
              ["Metas e preços da v26", "planos/redacao_04/plano.md, 2.2 e 8.2"],
              ["Regras de sobreposição", "planos/redacao_04/pendencias.md, L-008; estudo_outros_planos_imagem_20261102.md"],
              ["Custos", "planos/redacao_04/estudos/custo_por_exame_v2_20261020.xlsx"],
              ["Capacidade", "planos/redacao_04/estudos/salas_ultrassom_metricas_20261020.xlsx e estudo_polos_rede_capacidade_20261020.md"],
              ["Tempos", "output/estudo_imagem_candanga_20261101.xlsx, aba 6"]]
    executante = None
    if len(sys.argv) > 3:
        executante = quem_oferta(json.load(open(sys.argv[3], encoding="utf-8")))
        fontes.append(["Oferta por unidade executante", sys.argv[3]])
    destino = AQUI / "estudo_filas_imagem_20261102.xlsx"
    escrever(filas, rumo, cenarios, v26, destino, fontes, executante)
    json.dump({"filas": filas, "cenarios": cenarios, "v26": v26}, open(AQUI / "estudo_filas_imagem_20261102.json", "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)
    print(destino)


if __name__ == "__main__":
    main()
