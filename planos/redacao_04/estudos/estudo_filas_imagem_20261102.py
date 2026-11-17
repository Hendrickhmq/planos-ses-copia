"""Estudo das filas de imagem para decidir o plano 4 (controle interno, 02/11/2026).

Lê a coleta do panorama de imagem do Mapa Social e o Anexo Único da Tabela SUS Candanga e
escreve a planilha única do estudo e os números do relatório de decisão:

    python3 planos/redacao_04/estudos/estudo_filas_imagem_20261102.py \
        <coleta.json> <tabela_sus_candanga.csv> [<coleta_executante.json>]

A coleta de executante é a de dados/fontes/mapa_social_20261102_executante_c_bruto/ (os 17 códigos da carteira 1).

A coleta sai de planos/redacao_04/dados/fontes/mapa_social_20261102_imagem_bruto/. O Anexo é o
de biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv do main (2.952 linhas).

O que é regra do usuário e o que é premissa está nas constantes abaixo, cada uma com a fonte.
"""
import csv
import math
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
SALAS_US = 20            # usuário, 02/11/2026 (tarde): vão ser 20 salas de ultrassom
HORAS_DIA = 10
OCUPACAO = 0.8
DIAS_UTEIS_MES = 21
TOMOGRAFOS = 5           # usuário, 02/11/2026 (tarde): vão ser 5 tomógrafos

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


# --- revisão de 02/11/2026, à tarde: a carteira 1 é a base (usuário) ---
# A conta "Crescimento e faltas" da manhã foi superada: ela tomava o fluxo do código inteiro como acessível ao
# plano, somava só o crescimento positivo e lia meta ÷ (1 − faltas) como pedidos novos. As funções abaixo a
# substituem. Ajuste do usuário no fim da tarde: 20 salas de ultrassom, 5 tomógrafos, 8 meses, sem data de início.
SEM_ANGIO = lambda f: "angio coronária" not in f["protocolo"]   # a regra da carteira 1
FALTAS_RESIDUAIS = (0.0, 0.10, 0.20)   # a parte das faltas que a confirmação e o encaixe não repõem: premissa
FALTA_PLANEJAMENTO = 0.20        # premissa para abrir vagas; o plano não traz taxa (absenteísmo é interno)
HORAS_DE_EXAME = HORAS_DIA * OCUPACAO   # das 10 horas da sala, 8 de exame e 2 de preparo, intervalo e manutenção
POLOS = ("Oeste", "Sudoeste", "Norte", "Leste", "Central e Centro-Sul", "Sul")   # v26, 4.2
POLO_DA_REGIAO = {"Região Oeste": "Oeste", "Região Sudoeste": "Sudoeste", "Região Norte": "Norte",
                  "Região Leste": "Leste", "Região Central": "Central e Centro-Sul",
                  "Região Centro-Sul": "Central e Centro-Sul", "Região Sul": "Sul"}
# os 5 tomógrafos: o cenário de 5 polos do estudo de 20/10 (estudo_polos_rede_capacidade_20261020.md, seção 6), com a
# Leste atendida na Central e Centro-Sul; o que passa de um tomógrafo na Sudoeste vai à Oeste e depois à Central
POLOS_COM_TOMOGRAFO = ("Oeste", "Sudoeste", "Norte", "Central e Centro-Sul", "Sul")
TC_SEM_TOMOGRAFO_VAI = {"Leste": "Central e Centro-Sul"}
EXCEDENTE_TC_VAI = ("Oeste", "Central e Centro-Sul", "Sul", "Norte")
COLETA_REGIAO = AQUI.parent / "dados/fontes/mapa_social_20261102_regiao_bruto/coleta_20261102.json"
# a fila (três status) dos onze nomes da v26 em 15/09 e 05/10: dados/fontes/mapa_social_20261005.md, seção 6
FILA_ANTES = {
    "ECOGRAFIA DE MAMAS - BILATERAL": (14396, 13732), "ECOGRAFIA TRANSVAGINAL": (10383, 9950),
    "ECOGRAFIA DE ABDOMEN TOTAL ADULTO": (9912, 10130),
    "ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL)": (9824, 9899), "10. ECODOPPLER DE CAROTIDAS": (4537, 4533),
    "ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO": (3914, 3884), "ECOGRAFIA DE TIREOIDE ADULTO": (3216, 3152),
    "ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL )": (3243, 3325), "ULTRASONOGRAFIA DE PAREDE ABDOMINAL": (3143, 3189),
    "ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO": (2276, 2274),
    "063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO": (4467, 4088),
    "111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO": (3836, 3631),
    "055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO": (2987, 2447),
}
DIAS_ENTRE_COLETAS = 48           # de 15/09 à recarga de 02/11
MESES_12 = [f"2025-{m:02d}" for m in (10, 11, 12)] + [f"2026-{m:02d}" for m in range(1, 10)]
CANCELADOS = ("PROCEDIMENTO CANCELADO PELA REGULAÇÃO", "PROCEDIMENTO CANCELADO PELO SOLICITANTE",
              "AGENDAMENTO CANCELADO PELO COORD. DA REGULAÇÃO LOCAL")
# o que o IEV executou até 26/10 (estudo_outros_planos_imagem_20261102.md, seção 2) e o fim das vigências (item 12)
IEV_EXECUTADO = {"02.05.02.006-2": ("308 consultas com CID da OCI realizadas; nenhuma US agendada pela fila do exame",
                                    "08/2027 (030975) e 05/2027 (030977)"),
                 "02.05.02.018-6": ("20 consultas de ginecologia realizadas", "05/2027"),
                 "02.06.03.003-7": ("94 consultas com CID da OCI realizadas", "05/2027"),
                 "02.05.02.011-9": ("nenhuma consulta de urologia agendada", "05/2027")}


def eh_da_carteira1(f):
    """O recorte elegível da carteira 1: o mesmo filtro da função carteira, sem o valor."""
    return (f["cobertura"] in ("livre", "parcial") and f["preco"] and f["fila"] >= MINIMO_FILA
            and f["margem_hora"] is not None and f["margem_hora"] > 0 and SEM_ANGIO(f)
            and (f["cobertura"] == "livre" or f["codigo"] in PARTE_COM_CID))


def elegivel_da_fila(f):
    return f["fila"] if f["cobertura"] == "livre" else int(f["fila"] * (1 - PARTE_COM_CID[f["codigo"]]))


def por_que_fora(f):
    """O motivo de a fila (ou parte dela) ficar fora do recorte da carteira 1, em poucas categorias."""
    if "emergência" in f["protocolo"]:
        return "emergência"
    if not SEM_ANGIO(f):
        return "angio coronária"
    if "sedação" in f["protocolo"]:
        return "sedação"
    if f["cobertura"] == "fora":
        return "tem dono (IEV)" if ("IEV" in f["motivo"] or "L-008" in f["motivo"]) else "outra equipe ou equipamento"
    return "fila pequena ou sem margem"


def grupo_regional(nome, codigo):
    """O objeto da coleta de Região de 02/11 a que a fila pertence (a ordem.json da pasta bruta)."""
    n = nome.upper()
    if codigo == "02.05.01.004-0":
        return "doppler_membros" if MEMBROS.search(n) else "doppler_outros"
    if codigo == "02.05.02.004-6":
        return "parede" if "PAREDE" in n else "abdomen_total"
    return {"02.05.02.009-7": "mama", "02.05.02.018-6": "transvaginal", "02.05.02.005-4": "urinario",
            "02.05.02.012-7": "tireoide", "02.05.02.010-0": "prostata", "02.05.02.003-8": "abdomen_superior",
            "02.05.02.007-0": "bolsa_escrotal", "02.05.02.016-0": "pelvica", "02.05.02.017-8": "transfontanela",
            "02.06.03.001-0": "tc_abdomen", "02.06.03.003-7": "tc_pelve", "02.06.02.003-1": "tc_torax",
            "02.06.01.007-9": "tc_cranio", "02.06.01.005-2": "tc_pescoco", "02.06.01.004-4": "tc_face"}[codigo]


def participacoes(coleta_regiao):
    """A Região de Saúde da unidade solicitante de cada grupo de filas, na coleta de 02/11. Os pedidos sem Região
    (URD, contratados, sem registro) se rateiam como os outros: o polo deles é a regulação que define (v26, 3.4)."""
    part = {}
    for gid, dims in coleta_regiao["dimensoes"].items():
        reg = dims["regiao"]
        por = {r[0]: r[1] for r in reg["linhas"]}
        terr = {p: sum(v for r, v in por.items() if POLO_DA_REGIAO.get(r) == p) for p in POLOS}
        t = sum(terr.values())
        total = sum(por.values()) + (reg.get("sem_regiao") or {}).get("fila", 0)
        part[gid] = {"nome": coleta_regiao["exames"][gid]["nome"], "pedidos": total,
                     "por_regiao": {**por, "sem registro": (reg.get("sem_regiao") or {}).get("fila", 0)},
                     "polos": {p: terr[p] / t for p in POLOS}, "sem_regiao": round(1 - t / total, 3) if total else 0}
    return part


def horas_por_polo(itens, part):
    """Exames e horas de exame de cada polo, pela origem dos pedidos (local = polo da Região, v26 4.2)."""
    ex, h = defaultdict(float), defaultdict(float)
    for i in itens:
        for p, s in part[grupo_regional(i["nome"].split(" — ")[0], i["codigo"])]["polos"].items():
            ex[(i["modalidade"], p)] += i["meta"] * s
            h[(i["modalidade"], p)] += i["meta"] * s * i["minutos"] / 60
    return ex, h


def repartir_salas(horas, total, cap):
    """Reparte um número fixo de salas entre os polos: pelo menos uma em cada; cada sala a mais vai ao polo mais
    carregado naquele momento."""
    salas = {p: max(1, math.floor(horas[p] / cap)) for p in horas}
    while sum(salas.values()) < total:
        p = max(salas, key=lambda p: horas[p] / (salas[p] * cap))
        salas[p] += 1
    return salas


def tomografos(carga):
    """A carga de cada um dos 5 tomógrafos: a Leste vai à Central e Centro-Sul; o que passa de um tomógrafo vai ao
    próximo polo da lista que ainda tem folga."""
    c = {p: carga[p] for p in POLOS_COM_TOMOGRAFO}
    for p, destino in TC_SEM_TOMOGRAFO_VAI.items():
        c[destino] += carga[p]
    recebe = defaultdict(float)
    for p in POLOS_COM_TOMOGRAFO:
        while c[p] > 1:
            alvo = next((q for q in EXCEDENTE_TC_VAI if q != p and c[q] < 1), None)
            if alvo is None:
                break
            passa = min(c[p] - 1, 1 - c[alvo])
            c[p] -= passa
            c[alvo] += passa
            recebe[alvo] += passa
    return c, recebe


def capacidade_por_polo(itens, part):
    """As 20 salas de ultrassom e os 5 tomógrafos, polo a polo, em 8 meses: o uso com e sem reposição das faltas."""
    ex, h = horas_por_polo(itens, part)
    dias = DIAS_UTEIS_MES * MESES
    cap = HORAS_DE_EXAME * dias
    h_us = {p: h[("Ultrassom", p)] for p in POLOS}
    salas = repartir_salas(h_us, SALAS_US, cap)
    us = []
    for r in FALTAS_RESIDUAIS:
        agenda = {p: h_us[p] / (1 - r) for p in POLOS}
        us.append({"falta_residual": r, "horas_de_agenda": {p: round(agenda[p]) for p in POLOS},
                   "uso": {p: round(agenda[p] / (salas[p] * cap), 3) for p in POLOS},
                   "uso_rede": round(sum(agenda.values()) / (SALAS_US * cap), 3),
                   "salas_necessarias": {p: math.ceil(agenda[p] / cap - 1e-9) for p in POLOS}})
    tc = []
    for r in FALTAS_RESIDUAIS:
        carga = {p: h[("Tomografia", p)] / (1 - r) / cap for p in POLOS}
        final, recebe = tomografos(carga)
        tc.append({"falta_residual": r, "carga_propria": {p: round(carga[p], 2) for p in POLOS},
                   "carga_final": {p: round(final[p], 2) for p in POLOS_COM_TOMOGRAFO},
                   "recebe": {p: round(v, 2) for p, v in recebe.items()},
                   "uso_rede": round(sum(carga.values()) / TOMOGRAFOS, 3)})
    folga = (SALAS_US * cap) / sum(h_us.values())
    return {"horas_de_exame_por_sala": cap, "dias": dias, "salas": salas,
            "exames_us": {p: round(ex[("Ultrassom", p)]) for p in POLOS},
            "horas_us": {p: round(h_us[p]) for p in POLOS},
            "exames_tc": {p: round(ex[("Tomografia", p)]) for p in POLOS},
            "horas_tc": {p: round(h[("Tomografia", p)]) for p in POLOS},
            "vagas_por_dia_us": {p: math.ceil(ex[("Ultrassom", p)] / (1 - FALTA_PLANEJAMENTO) / dias) for p in POLOS},
            "falta_residual_que_cabe": round(1 - 1 / folga, 3), "ultrassom": us, "tomografia": tc}


def serie(coleta, codigo, meses):
    """Entradas, agendamentos, realizados e faltas por mês do código, nos meses pedidos."""
    pc = coleta["por_codigo"]
    ent = sum(a + g for c, m, a, g in pc["entrantes"]["linhas"] if c == codigo and m in meses)
    ag = re_ = fa = 0
    for c, m, a, r, f in pc["oferta"]["linhas"]:
        if c == codigo and m in meses:
            ag, re_, fa = ag + a, re_ + r, fa + f
    n = len(meses)
    return ent / n, ag / n, re_ / n, fa / n


def demanda_elegivel(filas, coleta, itens):
    """O movimento de cada código da carteira 1 só nas filas que o plano atende.

    O Mapa Social dá entradas e agendamentos por código, com todas as filas do código juntas (emergência, angio
    coronária, a reserva do IEV). A parte das filas do plano nos agendamentos sai das agendadas em 12 meses de cada
    fila; a parte delas no que sobra (entradas − agendamentos) sai do estoque, porque a emergência não acumula fila.
    """
    meta = defaultdict(int)
    for i in itens:
        meta[i["codigo"]] += i["meta"]
    linhas = []
    for codigo in sorted(meta, key=lambda c: -meta[c]):
        fs = [f for f in filas if f["codigo"] == codigo]
        el = [f for f in fs if eh_da_carteira1(f)]
        estoque = sum(f["fila"] for f in fs)
        estoque_el = sum(elegivel_da_fila(f) for f in el)
        fora = defaultdict(int)
        for f in fs:
            if eh_da_carteira1(f):
                fora["reserva do IEV"] += f["fila"] - elegivel_da_fila(f)
            else:
                fora[por_que_fora(f)] += f["fila"]
        ag_t = sum(f["agendadas_12m"] or 0 for f in fs)
        ag_e = sum(f["agendadas_12m"] or 0 for f in el)
        s_ag = ag_e / ag_t if ag_t else 1.0
        s_est = estoque_el / estoque if estoque else 0
        e12, o12, r12, f12 = serie(coleta, codigo, MESES_12)
        saldo = (e12 - o12) * s_est
        obs = [(f["fila"] - FILA_ANTES[f["nome"]][0]) / DIAS_ENTRE_COLETAS * 30.4 for f in el if f["nome"] in FILA_ANTES]
        linhas.append({
            "codigo": codigo, "exame": next(i["descricao_candanga"] for i in itens if i["codigo"] == codigo),
            "meta": meta[codigo], "fila_codigo": estoque, "fila_elegivel": estoque_el,
            "fora": dict(fora), "parte_agendamentos": round(s_ag, 3), "parte_estoque": round(s_est, 3),
            "entram_codigo_mes": round(e12), "agenda_codigo_mes": round(o12), "realiza_codigo_mes": round(r12),
            "entram_elegivel_mes": round(o12 * s_ag + saldo), "ses_agenda_elegivel_mes": round(o12 * s_ag),
            "ses_realiza_elegivel_mes": round(r12 * s_ag), "saldo_elegivel_mes": round(saldo, 1),
            "saldo_codigo_mes": round(e12 - o12, 1),
            "variacao_observada_mes": round(sum(obs)) if obs else None,
            "falta_ses": round(f12 / (r12 + f12), 3) if r12 + f12 else None,
        })
    return linhas


def pedidos_novos_detalhe(itens, dem):
    """Os pedidos novos esperados da carteira 1, um a um: de onde vem o número e o que o recorte elegível diz dele."""
    por = {d["codigo"]: d for d in dem}
    linhas = []
    for i in itens:
        if i["cobertura"] != "crescimento da fila":
            continue
        d = por[i["codigo"]]
        linhas.append({"codigo": i["codigo"], "fila": i["nome"].split(" — ")[0], "meta": i["meta"],
                       "valor": i["valor"], "preco": i["preco"], "saldo_codigo_mes": d["saldo_codigo_mes"],
                       "limite": i["fila"], "saldo_elegivel_8m": round(d["saldo_elegivel_mes"] * MESES),
                       "fila_elegivel_hoje": d["fila_elegivel"], "meta_do_codigo": d["meta"]})
    return linhas


def faltas_e_pedidos(coleta, dem):
    """Exames, tentativas de agenda, faltas, reagendamentos e pedidos consumidos: o que a fonte diz e o que é cenário.

    A fonte dá, por código, a situação de cada agendamento em 12 meses (realizado, falta, cancelado, pendente de
    confirmação). Não dá o que acontece com o pedido depois da falta: se volta à fila, se ganha outro agendamento ou
    se é encerrado. Por isso os pedidos consumidos vão em três cenários de reagendamento, e não como necessidade.
    """
    sit = defaultdict(lambda: defaultdict(int))
    for c, s, n in coleta["por_codigo"]["situacao"]["linhas"]:
        sit[c][s] += n
    linhas = []
    for d in dem:
        c, m = d["codigo"], d["meta"]
        s = sit[c]
        total = sum(s.values())
        real, falta = s["PROCEDIMENTO REALIZADO"], s["PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE"]
        canc = sum(s[k] for k in CANCELADOS)
        pend = s["PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO"]
        f_ses = falta / (real + falta) if real + falta else 0
        tent20 = m / (1 - FALTA_PLANEJAMENTO)
        linhas.append({
            "codigo": c, "exame": d["exame"], "meta": m,
            "ses_agendamentos_12m": total, "ses_realizados": real, "ses_faltas": falta, "ses_cancelados": canc,
            "ses_pendentes_confirmacao": pend, "ses_outros": total - real - falta - canc - pend,
            "falta_ses": round(f_ses, 3), "cancelamento_ses": round(canc / total, 3) if total else None,
            "tentativas_20": round(tent20), "tentativas_falta_ses": round(m / (1 - f_ses)),
            "faltas_20": round(tent20 - m), "pedidos_todos_reagendados": m,
            "pedidos_metade_reagendada": round(m + (tent20 - m) / 2), "pedidos_nenhum_reagendado": round(tent20),
        })
    return linhas


def faltas_na_taxa_da_ses(fal, enc):
    """Os pedidos que o projeto gasta se as faltas dele forem iguais às da SES, exame a exame (pedido do usuário,
    02/11/2026): quantos a mais que a meta e que a premissa de 20%, e quantos faltam nas filas do plano em cada arranjo
    com a SES. Mesma regra de reagendamento da aba Faltas e pedidos: a falta reagendada no mesmo pedido não gasta pedido;
    a fonte não diz quantas são, por isso vão a metade e nenhuma.
    """
    linhas = []
    for f, e in zip(fal, enc):
        m, fs = f["meta"], f["ses_faltas"] / (f["ses_realizados"] + f["ses_faltas"])
        nenhum = m / (1 - fs)
        metade = m + (nenhum - m) / 2
        s, ao_a, maximo = e["ses_agenda_periodo"], e["cenarios"]["a"]["ao_projeto"], e["estoque_inicio"] + e["entradas_periodo"]
        falta_a = max(0, nenhum - ao_a)
        encaminhar = min(s, falta_a)
        linhas.append({"codigo": f["codigo"], "exame": f["exame"], "meta": m, "falta_ses": round(fs, 3),
                       "pedidos_metade_ses": round(metade), "pedidos_nenhum_ses": round(nenhum),
                       "a_mais_que_a_meta": round(nenhum - m), "a_mais_que_20": round(nenhum - f["pedidos_nenhum_reagendado"]),
                       "disponiveis_a": ao_a, "faltam_a_metade": round(max(0, metade - ao_a)), "faltam_a_nenhum": round(falta_a),
                       "ses_agenda_periodo": s, "encaminhar_nenhum": round(encaminhar),
                       "parte_da_agenda_ses": round(encaminhar / s, 3) if s else None,
                       "disponiveis_c": maximo, "faltam_c": round(max(0, nenhum - maximo))})
    return linhas


def encaminhamento(dem):
    """Os três arranjos com a SES, por código, a partir da fila elegível de hoje (não há data de início): (a) a SES
    mantém a oferta; (b) a regulação encaminha ao projeto a parte da demanda que falta, e a SES reduz a própria agenda
    na mesma medida; (c) a SES concentra no projeto o eletivo do código e suspende a própria agenda. Só o recorte
    elegível: emergência, angio coronária, sedação e as reservas do IEV não entram na transferência.

    Pedidos que o projeto consome: entre a meta (toda falta reagendada no mesmo pedido) e meta ÷ (1 − 20%) (nenhuma).
    A demanda transferida não é demanda nova: o aumento líquido de exames na rede é a produção do projeto menos o que
    a SES deixa de realizar.
    """
    linhas = []
    for d in dem:
        m = d["meta"]
        e0 = d["fila_elegivel"]
        n = d["entram_elegivel_mes"] * MESES
        s = d["ses_agenda_elegivel_mes"] * MESES
        realiza_ses = d["ses_realiza_elegivel_mes"] * MESES
        baixo, alto = m, m / (1 - FALTA_PLANEJAMENTO)

        def x_para(pedidos):
            return min(1.0, max(0.0, (pedidos - (e0 + n - s)) / s)) if s else 0.0
        cen = {}
        for nome, x in (("a", 0.0), ("b", x_para(alto)), ("c", 1.0)):
            ao_projeto = max(0, e0 + n - s * (1 - x))
            cen[nome] = {"reducao_ses": round(x, 3), "ses_agenda": round(s * (1 - x)), "ao_projeto": round(ao_projeto),
                         "estoque_final_baixo": round(ao_projeto - alto), "estoque_final_alto": round(ao_projeto - baixo),
                         "aumento_liquido": round(m - realiza_ses * x)}
        linhas.append({"codigo": d["codigo"], "exame": d["exame"], "meta": m, "estoque_inicio": e0,
                       "entradas_periodo": round(n), "ses_agenda_periodo": round(s), "ses_realiza_periodo": round(realiza_ses),
                       "reserva_outros": d["fora"].get("reserva do IEV", 0) + d["fora"].get("tem dono (IEV)", 0),
                       "pedidos_baixo": baixo, "pedidos_alto": round(alto), "vagas": round(alto),
                       "x_minimo": round(x_para(baixo), 3), "cenarios": cen})
    return linhas


def situacao_iev(filas):
    """A situação completa de cada fila que o IEV também pode atender: pedidos e pessoas na fila de hoje, o que ele
    contratou, o que já fez e a regra que vale para o plano 4 (L-008 revista, 02/11/2026)."""
    grupos = [("02.05.02.006-2", "US de articulação, sem as partes moles", lambda f: "PARTES MOLES" not in f["nome"].upper()),
              ("02.05.02.006-2", "US de partes moles", lambda f: "PARTES MOLES" in f["nome"].upper()),
              ("02.05.02.018-6", "US transvaginal", lambda f: True),
              ("02.06.03.003-7", "TC de pelve", lambda f: True),
              ("02.05.02.011-9", "US de próstata transretal", lambda f: True)]
    regra = {"US de articulação, sem as partes moles": "fora inteira: comprometida com a OCI 09.03.01.002-0 do IEV",
             "US de partes moles": "fora inteira: do IEV (usuário, 01/11/2026)",
             "US transvaginal": "4.000 reservados à GIN1 do IEV; o resto entra no plano 4",
             "TC de pelve": "entra, sem os 7 pedidos com o CID da OCI 09.03.01.003-8",
             "US de próstata transretal": "fora: pede outro exame (via transretal)"}
    linhas = []
    for codigo, rotulo, filtro in grupos:
        fs = [f for f in filas if f["codigo"] == codigo and "emergência" not in f["protocolo"] and filtro(f)]
        plano, oci, contratado = QUEM_ATENDE.get(codigo, ("", "", None))
        feito, vigencia = IEV_EXECUTADO.get(codigo, ("", ""))
        linhas.append({"exame": rotulo, "codigo": codigo, "pedidos": sum(f["fila"] for f in fs),
                       "fila_viva": sum(f["fila_viva"] or 0 for f in fs),
                       "pessoas": sum(f["pessoas"] or 0 for f in fs), "convenio": plano, "oci": oci,
                       "contratado": contratado, "feito": feito, "vigencia": vigencia, "regra": regra[rotulo]})
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
# de onde vem a quantidade de OCI contratadas: a planilha de aplicação de cada plano aprovado do IEV
# (estudo/normalizados/pt_ses_0N/planilha.csv, o item e a quantidade)
FONTE_CONTRATADO = {
    "02.05.02.006-2": "pt_ses_02 (030975), item 2.1.2: 12.070 + pt_ses_04 (030977), item 2.2.2: 7.000",
    "02.05.02.018-6": "pt_ses_04 (030977), item 2.1.1: 3.218",
    "02.06.03.003-7": "pt_ses_04 (030977), item 2.2.3: 539 (uma TC por OCI, entre os sete códigos compatíveis)",
    "02.05.02.011-9": "pt_ses_04 (030977), item 2.5.1: 1.015",
    "02.05.01.001-6": "pt_ses_04 (030977), item 2.3.3: 900",
    "02.05.01.003-2": "pt_ses_04 (030977), item 2.3.2: 1.000",
    **{c: "pt_ses_04 (030977), item 2.2.3: 539 (uma TC por OCI, entre os sete códigos compatíveis)"
       for c in IEV_TC_ORTOPEDIA},
}


def com_o_iev(codigo, situacao, quem):
    """O indicativo de quem atende a fila: só o plano 4, os dois juntos, só o IEV ou nenhum."""
    if situacao == "livre":
        return "só o plano 4"
    if situacao == "parcial" and codigo not in PARTE_COM_CID:
        return "só o IEV, por ora: o CID não foi medido, e o plano 4 não usa a fila"
    if situacao == "parcial":
        return ("juntos: 4.000 pedidos ficam com o IEV (GIN1) e o resto com o plano 4" if codigo == "02.05.02.018-6"
                else "juntos: os pedidos com o CID da OCI ficam com o IEV e o resto com o plano 4")
    if quem.startswith("IEV") and "em parte" not in quem:
        return "só o IEV: a fila inteira fica com ele"
    if "em parte" in quem:
        return "o IEV atende só uma parte; o plano 4 não atende (outra equipe)"
    return "nenhum dos dois"


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
            elif codigo in OUTRA_EQUIPE and plano:
                quem, regra = f"{plano}, em parte", f"fora do plano 4 por viabilidade — {motivo}"
            elif "IEV" in motivo or "L-008" in motivo:
                quem, regra = plano, "fila inteira fora do plano 4"
            else:
                quem, regra, oci, contratado = "ninguém", f"fora do plano 4 por viabilidade — {motivo}", "", None
        linhas.append([g["desc"], codigo, situacao, quem, oci, contratado, regra, g["fila"], com_cid, livres,
                       *[meta[k].get(codigo, 0) if situacao != "fora" else 0 for k in range(len(nomes))],
                       FONTE_CONTRATADO.get(codigo, "") if contratado else "", com_o_iev(codigo, situacao, quem)])
    return linhas, nomes


# o que o IEV fez nas três unidades dele, de 29/04 a 26/10/2026 (output/mapeamento_iev_20261026.md, seção 3; coleta do
# agente mapa-social de 26/10, planos/redacao_07/dados/fontes/mapa_social_20261026_iev.md): consulta, agendadas,
# realizadas, faltas (None = não medido) e o contratado
IEV_CONSULTAS = [("ortopedia", 29894, 13818, 11112, "100.525 OCI de ortopedia (quatro OCI, dois convênios)"),
                 ("risco cirúrgico", 2822, 990, 499, "4.647 OCI 09.02.01.001-8"),
                 ("cardiologia adulto", 1138, 300, 314, "1.900 OCI (09.02.01.006-9 e 004-2)"),
                 ("ginecologia", 60, 20, None, "3.218 OCI GIN1"),
                 ("otorrinolaringologia", 80, 28, None, "11.590 OCI de déficit auditivo"),
                 ("urologia", 0, 0, None, "1.015 OCI de próstata")]


def viabilidade_carteira1(itens):
    """Custo e margem de cada fila da carteira 1, com as parcelas à parte e o efeito da falta não reposta.

    Ultrassom feito pelo projeto: a sala com aparelho custa R$ 5.500 por mês, rateados nas 168 horas de exame do mês
    (8 horas por dia útil × 21 dias); o médico, R$ 100 por hora; o insumo, R$ 3 por exame. Falta não reposta deixa a
    sala e o médico parados: a hora deles se divide por menos exames. Tomografia: preço por exame na clínica (cotado),
    que a falta não muda. Premissas; a cotação fica para a etapa de custos.
    """
    juntos = {}
    for i in itens:
        k = (i["nome"].split(" — ")[0], i["codigo"])
        if k in juntos:
            juntos[k]["meta"] += i["meta"]
        else:
            juntos[k] = {**i, "nome": k[0]}
    linhas = []
    for i in sorted(juntos.values(), key=lambda i: (i["modalidade"] != "Ultrassom", i["codigo"], -i["meta"])):
        mins, p = i["minutos"], i["preco"]
        if i["modalidade"] == "Ultrassom":
            sala, medico, insumo = SALA_APARELHO_HORA * mins / 60, MEDICO_HORA * mins / 60, INSUMO
            custo = {r: (sala + medico) / (1 - r) + insumo for r in FALTAS_RESIDUAIS}
            base = "premissa (custo_por_exame_v2)"
        else:
            sala, medico, insumo = None, None, None
            custo = {r: TC_CLINICA for r in FALTAS_RESIDUAIS}
            base = "cotado por exame (rede de TC do ISHP)"
        linhas.append({"codigo": i["codigo"], "fila": i["nome"], "modalidade": i["modalidade"], "meta": i["meta"],
                       "preco": p, "minutos": mins, "sala": round(sala, 2) if sala else None,
                       "medico": round(medico, 2) if medico else None, "insumo": insumo,
                       "custo": {r: round(c, 2) for r, c in custo.items()},
                       "margem": {r: round(p - c, 2) for r, c in custo.items()},
                       "margem_hora": {r: round((p - c) * 60 / mins, 2) for r, c in custo.items()},
                       "base": base})
    return linhas


def revisar_carteira1(filas, coleta, itens):
    """Capacidade por polo, demanda elegível, pedidos novos, faltas, encaminhamento da SES e a situação do IEV para a
    carteira 1 (revisão de 02/11, tarde)."""
    part = participacoes(json.load(open(COLETA_REGIAO, encoding="utf-8")))
    dem = demanda_elegivel(filas, coleta, itens)
    tempos = {}
    for i in itens:
        nome = i["nome"].split(" — ")[0]
        tempos[(i["codigo"], nome)] = [i["codigo"], nome, i["minutos"], i["base_tempo"]]
    fal, enc = faltas_e_pedidos(coleta, dem), encaminhamento(dem)
    return {"participacoes": part,
            "origem_por_fila": [[i["nome"], i["codigo"], i["meta"], i["minutos"],
                                 grupo_regional(i["nome"].split(" — ")[0], i["codigo"])] for i in itens],
            "capacidade": capacidade_por_polo(itens, part), "demanda": dem,
            "pedidos_novos": pedidos_novos_detalhe(itens, dem), "faltas": fal,
            "faltas_ses": faltas_na_taxa_da_ses(fal, enc), "encaminhamento": enc, "iev": situacao_iev(filas), "tempos": list(tempos.values()),
            "viabilidade": viabilidade_carteira1(itens), "iev_consultas": IEV_CONSULTAS,
            "custos": {"sala_mes": 5500, "horas_exame_mes": 168, "medico_hora": MEDICO_HORA, "insumo": INSUMO,
                       "tc_clinica": TC_CLINICA},
            "valor_fila_de_hoje": round(sum(i["valor"] for i in itens if i["cobertura"] != "crescimento da fila"), 2),
            "premissas": {"meses": MESES, "faltas_residuais": FALTAS_RESIDUAIS, "falta_planejamento": FALTA_PLANEJAMENTO,
                          "salas": SALAS_US, "tomografos": TOMOGRAFOS, "polos_com_tomografo": POLOS_COM_TOMOGRAFO,
                          "horas_dia": HORAS_DIA, "horas_de_exame": HORAS_DE_EXAME, "dias_uteis_mes": DIAS_UTEIS_MES}}


FOLGA_REAGENDADA = 0.5    # carteira 6: metade das faltas reagendada no mesmo pedido (premissa, usuário, 02/11/2026)
FOLGA_ENCAMINHADA = 0.2   # carteira 6: a SES encaminha 20% da própria agenda em cada exame (premissa)
FOLGA_TETO_TC = 0.8       # carteira 6: os tomógrafos não passam de 80% da capacidade (cabe 20% de faltas sem reposição)
SUFIXO_ENCAMINHADOS = f" — encaminhados pela SES em {MESES} meses"
SEM_TRANSFONTANELA = {"02.05.02.017-8"}   # carteiras 1 e 6 sem a transfontanela (usuário, 03/11/2026)


def teto_folga(rv):
    """Os exames que cada código aguenta com a falta da SES: pedidos que chegam ÷ pedidos por exame (ver carteira 6)."""
    fal = {f["codigo"]: f for f in rv["faltas"]}
    teto = {}
    for e in rv["encaminhamento"]:
        f = fal[e["codigo"]]
        falta = f["ses_faltas"] / (f["ses_realizados"] + f["ses_faltas"])
        por_exame = 1 + (1 / (1 - falta) - 1) * (1 - FOLGA_REAGENDADA)
        chega = max(0, e["estoque_inicio"] + e["entradas_periodo"] - e["ses_agenda_periodo"]) \
            + FOLGA_ENCAMINHADA * e["ses_agenda_periodo"]
        teto[e["codigo"]] = int(chega / por_exame)
    return teto


def espalhar(itens, teto, horas_tc=None):
    """Completa o valor dos exames da v26 pelos códigos que ainda têm folga até o teto, na proporção da meta de cada um,
    numa linha de pedidos encaminhados pela SES; o resto, menor que um exame por código, vai ao de preço maior que
    caiba. Serve para o valor que sai com a transfontanela (usuário, 03/11/2026). Tira os códigos de SEM_TRANSFONTANELA."""
    itens = [i for i in itens if i["codigo"] not in SEM_TRANSFONTANELA]
    for i in itens:
        i["valor"] = round(i["meta"] * i["preco"], 2)
    total = sum(i["valor"] for i in itens)
    if horas_tc is None:
        horas_tc = sum(i["meta"] * i["minutos"] for i in itens if i["modalidade"] == "Tomografia") / 60
    cap_tc = TOMOGRAFOS * HORAS_DE_EXAME * DIAS_UTEIS_MES * MESES * FOLGA_TETO_TC
    meta, maior = defaultdict(int), {}
    for i in itens:
        meta[i["codigo"]] += i["meta"]
        if i["cobertura"] not in ("crescimento da fila", "encaminhamento da SES") \
                and i["meta"] > maior.get(i["codigo"], {"meta": -1})["meta"]:
            maior[i["codigo"]] = i
    com_folga = [c for c in maior if teto.get(c, 0) > meta[c]]
    peso = sum(meta[c] for c in com_folga)

    def somar(c, q):
        nonlocal total, horas_tc
        f = maior[c]
        ja = next((i for i in itens if i["codigo"] == c and i["cobertura"] == "encaminhamento da SES"), None)
        if ja:
            ja["meta"] += q; ja["fila"] += q; ja["valor"] = round(ja["meta"] * ja["preco"], 2)
        else:
            itens.append({**f, "nome": f"{f['nome']}{SUFIXO_ENCAMINHADOS}", "meta": q, "valor": round(q * f["preco"], 2),
                          "fila": q, "fila_viva": 0, "cobertura": "encaminhamento da SES"})
        total += q * f["preco"]
        meta[c] += q
        if f["modalidade"] == "Tomografia":
            horas_tc += q * f["minutos"] / 60

    def cabe(c):
        f = maior[c]
        q = teto[c] - meta[c]
        if f["modalidade"] == "Tomografia":
            q = min(q, int((cap_tc - horas_tc) * 60 / f["minutos"]))
        return q
    falta_valor = VALOR_EXAMES_V26 - total
    for c in sorted(com_folga, key=lambda c: -meta[c]):
        q = min(cabe(c), int(falta_valor * meta[c] / peso // maior[c]["preco"]),
                int((VALOR_EXAMES_V26 - total) // maior[c]["preco"]))
        if q > 0:
            somar(c, q)
    for c in sorted(com_folga, key=lambda c: -maior[c]["preco"]):
        q = min(cabe(c), int((VALOR_EXAMES_V26 - total) // maior[c]["preco"]))
        if q > 0:
            somar(c, q)
    return itens


def carteira_folga(itens1, rv):
    """Carteira 6: a carteira 1 limitada, código a código, aos pedidos que chegam com a falta da SES, e o valor que sai
    do ultrassom completado com TC encaminhada pela SES (usuário, 02/11/2026).

    Pedidos que chegam = fila de hoje + entradas em 8 meses − agenda da SES + FOLGA_ENCAMINHADA × agenda da SES.
    Pedidos por exame = 1 + (1 ÷ (1 − falta da SES) − 1) × (1 − FOLGA_REAGENDADA). Teto = pedidos ÷ pedidos por exame.
    O corte sai primeiro dos pedidos novos esperados e depois das filas, na proporção. O acréscimo vai, do preço maior
    para o menor, aos códigos com folga até o teto, numa linha própria de pedidos encaminhados pela SES, sem passar de
    FOLGA_TETO_TC nos tomógrafos.
    """
    teto = teto_folga(rv)
    itens = [dict(i) for i in itens1]
    for c, t in teto.items():
        do_codigo = [i for i in itens if i["codigo"] == c]
        corte = sum(i["meta"] for i in do_codigo) - t
        if corte <= 0:
            continue
        for i in sorted(do_codigo, key=lambda i: i["cobertura"] != "crescimento da fila"):
            if i["cobertura"] != "crescimento da fila":
                break
            q = min(corte, i["meta"]); i["meta"] -= q; corte -= q
        base = [i for i in do_codigo if i["cobertura"] != "crescimento da fila"]
        total = sum(i["meta"] for i in base)
        cortes = {id(i): corte * i["meta"] // total for i in base}
        sobra = corte - sum(cortes.values())
        for i in sorted(base, key=lambda i: -i["meta"])[:sobra]:
            cortes[id(i)] += 1
        for i in base:
            i["meta"] -= cortes[id(i)]
    itens = [i for i in itens if i["meta"] > 0]
    for i in itens:
        i["valor"] = round(i["meta"] * i["preco"], 2)
    total = sum(i["valor"] for i in itens)
    horas_tc = sum(i["meta"] * i["minutos"] for i in itens if i["modalidade"] == "Tomografia") / 60
    cap_tc = TOMOGRAFOS * HORAS_DE_EXAME * DIAS_UTEIS_MES * MESES * FOLGA_TETO_TC
    meta = defaultdict(int)
    for i in itens:
        meta[i["codigo"]] += i["meta"]
    maior = {}
    for i in itens:
        if i["cobertura"] != "crescimento da fila" and i["meta"] > maior.get(i["codigo"], {"meta": -1})["meta"]:
            maior[i["codigo"]] = i
    for c in sorted(maior, key=lambda c: -maior[c]["preco"]):
        f = maior[c]
        folga = teto[c] - meta[c]
        if f["modalidade"] == "Tomografia":
            folga = min(folga, int((cap_tc - horas_tc) * 60 / f["minutos"]))
        q = min(folga, int((VALOR_EXAMES_V26 - total) // f["preco"]))
        if q <= 0:
            continue
        itens.append({**f, "nome": f"{f['nome']}{SUFIXO_ENCAMINHADOS}", "meta": q, "valor": round(q * f["preco"], 2),
                      "fila": q, "fila_viva": 0, "cobertura": "encaminhamento da SES"})
        total += q * f["preco"]
        meta[c] += q
        if f["modalidade"] == "Tomografia":
            horas_tc += q * f["minutos"] / 60
    return espalhar(itens, teto, horas_tc)


def escrever_revisao(aba, rv):
    """As abas da revisão de 02/11 (tarde) na planilha completa; a organizada as reapresenta."""
    cp = rv["capacidade"]
    linhas = [["Ultrassom", p, cp["exames_us"][p], cp["horas_us"][p], cp["salas"][p],
               *[u["uso"][p] for u in cp["ultrassom"]], cp["vagas_por_dia_us"][p]] for p in POLOS]
    aba("Capacidade por polo", ["Modalidade", "Polo", "Exames", "Horas de exame", "Salas (das 20)",
                                *[f"Uso, {r:.0%} das faltas sem reposição" for r in FALTAS_RESIDUAIS],
                                "Vagas por dia útil (20% de faltas)"], linhas,
        f"Carteira 1, {MESES} meses. Sala de {HORAS_DIA} horas por dia útil: {HORAS_DE_EXAME:.0f} de exame e o resto para "
        f"preparo, intervalo e manutenção; {DIAS_UTEIS_MES} dias úteis por mês. Polo = Região da unidade solicitante "
        "(coleta de 02/11). Tomógrafos: ver a aba Tomógrafos.")
    aba("Tomógrafos", ["Faltas sem reposição", "Polo", "Carga própria (tomógrafos)", "Recebe de outro polo",
                       "Carga final"],
        [[t["falta_residual"], p, t["carga_propria"][p], t["recebe"].get(p, 0), t["carga_final"].get(p)]
         for t in cp["tomografia"] for p in POLOS],
        "5 tomógrafos (usuário, 02/11): a Leste é atendida na Central e Centro-Sul; o que passa de um tomógrafo vai a "
        "outro polo com folga. Carga 1 = um tomógrafo cheio (8 horas de exame por dia útil).")
    aba("Origem regional", ["Grupo de filas", "Pedidos", *POLOS, "Sem Região (rateado)"],
        [[v["nome"], v["pedidos"], *[round(v["polos"][p], 4) for p in POLOS], v["sem_regiao"]]
         for v in rv["participacoes"].values()],
        "Região de Saúde da unidade solicitante, Mapa Social de 02/11/2026 "
        "(dados/fontes/mapa_social_20261102_regiao.md), só nas filas da carteira 1.")
    aba("Demanda elegível", ["Código", "Exame", "Meta", "Fila do código", "Fila elegível", "Fora do recorte",
                             "Parte das filas do plano nos agendamentos", "Parte das filas do plano no estoque",
                             "Entram por mês (código)", "SES agenda por mês (código)", "Entram por mês (filas do plano)",
                             "SES agenda por mês (filas do plano)", "SES realiza por mês (filas do plano)",
                             "Saldo por mês (filas do plano)", "Variação observada por mês (15/09 a 02/11)",
                             "Falta na SES"],
        [[d["codigo"], d["exame"], d["meta"], d["fila_codigo"], d["fila_elegivel"],
          "; ".join(f"{k}: {v}" for k, v in d["fora"].items() if v), d["parte_agendamentos"], d["parte_estoque"],
          d["entram_codigo_mes"], d["agenda_codigo_mes"], d["entram_elegivel_mes"], d["ses_agenda_elegivel_mes"],
          d["ses_realiza_elegivel_mes"], d["saldo_elegivel_mes"], d["variacao_observada_mes"], d["falta_ses"]]
         for d in rv["demanda"]],
        "O movimento do código (12 meses fechados) levado só às filas que o plano atende. Saldo negativo = a SES agenda "
        "mais do que entra, e a fila cai.")
    aba("Pedidos novos", ["Código", "Fila", "Pedidos novos na carteira 1", "Preço (R$)", "Valor (R$)",
                          "Saldo por mês do código", "Limite (saldo × 8)", "Saldo das filas do plano em 8 meses",
                          "Fila elegível de hoje", "Meta do código"],
        [[p["codigo"], p["fila"], p["meta"], p["preco"], p["valor"], p["saldo_codigo_mes"], p["limite"],
          p["saldo_elegivel_8m"], p["fila_elegivel_hoje"], p["meta_do_codigo"]] for p in rv["pedidos_novos"]],
        "Os pedidos que a carteira 1 conta como entradas futuras, para fechar o valor da v26 depois de usar a fila "
        "elegível de hoje inteira.")
    aba("Faltas e pedidos", ["Código", "Exame", "Meta (exames realizados)", "SES: agendamentos 12 m", "SES: realizados",
                             "SES: faltas", "SES: cancelados", "SES: pendentes de confirmação", "SES: outros",
                             "Falta na SES", "Cancelamento na SES", "Tentativas de agenda (20% de faltas)",
                             "Tentativas (falta da SES)", "Faltas esperadas (20%)",
                             "Pedidos consumidos: toda falta reagendada", "Pedidos: metade reagendada",
                             "Pedidos: nenhuma reagendada"],
        [[f["codigo"], f["exame"], f["meta"], f["ses_agendamentos_12m"], f["ses_realizados"], f["ses_faltas"],
          f["ses_cancelados"], f["ses_pendentes_confirmacao"], f["ses_outros"], f["falta_ses"], f["cancelamento_ses"],
          f["tentativas_20"], f["tentativas_falta_ses"], f["faltas_20"], f["pedidos_todos_reagendados"],
          f["pedidos_metade_reagendada"], f["pedidos_nenhum_reagendado"]] for f in rv["faltas"]],
        "Tentativas = meta ÷ (1 − faltas): são vagas de agenda, não pedidos. A fonte não diz o que acontece com o "
        "pedido depois da falta; por isso os pedidos consumidos vão em três cenários de reagendamento.")
    aba("Faltas na taxa da SES", ["Código", "Exame", "Meta (exames realizados)", "Falta na SES",
                                  "Pedidos: metade das faltas reagendada", "Pedidos: nenhuma falta reagendada",
                                  "A mais que a meta", "A mais que com 20% de faltas",
                                  "Pedidos disponíveis no arranjo a", "Faltam no arranjo a (metade reagendada)",
                                  "Faltam no arranjo a (nenhuma reagendada)", f"SES agenda nessas filas em {MESES} meses",
                                  "Pedidos que a SES teria de encaminhar (nenhuma reagendada)", "Parte da agenda da SES",
                                  "Pedidos disponíveis no arranjo c (fila + entradas)", "Faltam mesmo no arranjo c"],
        [[f["codigo"], f["exame"], f["meta"], f["falta_ses"], f["pedidos_metade_ses"], f["pedidos_nenhum_ses"],
          f["a_mais_que_a_meta"], f["a_mais_que_20"], f["disponiveis_a"], f["faltam_a_metade"], f["faltam_a_nenhum"],
          f["ses_agenda_periodo"], f["encaminhar_nenhum"], f["parte_da_agenda_ses"], f["disponiveis_c"], f["faltam_c"]]
         for f in rv["faltas_ses"]],
        "Se o projeto tiver a mesma falta da SES em cada exame. Pedidos = meta ÷ (1 − falta da SES) se nenhuma falta for "
        "reagendada no mesmo pedido. Arranjo a: a SES mantém a agenda; c: a SES para o eletivo. Controle interno.")
    linhas = []
    for e in rv["encaminhamento"]:
        for k, c in e["cenarios"].items():
            linhas.append([e["codigo"], e["exame"], k, e["meta"], e["estoque_inicio"], e["entradas_periodo"],
                           e["ses_agenda_periodo"], e["reserva_outros"], c["reducao_ses"], c["ses_agenda"],
                           c["ao_projeto"], e["pedidos_baixo"], e["pedidos_alto"], c["estoque_final_baixo"],
                           c["estoque_final_alto"], c["aumento_liquido"], e["vagas"], e["x_minimo"]])
    aba("Encaminhamento SES", ["Código", "Exame", "Cenário", "Meta", "Fila elegível de hoje",
                               f"Entradas elegíveis em {MESES} meses", "SES agenda nessas filas, se mantiver",
                               "Reservado a outro convênio (fila de hoje)", "Redução da agenda da SES",
                               "SES agenda no cenário", "Pedidos que chegam ao projeto", "Pedidos consumidos (mínimo)",
                               "Pedidos consumidos (máximo)", "Estoque final (pior)", "Estoque final (melhor)",
                               "Aumento líquido de exames na rede", "Vagas do projeto (20% de faltas)",
                               "Redução mínima, se toda falta for reagendada"],
        linhas,
        "a: a SES mantém a oferta habitual; b: a regulação encaminha ao projeto a parte que falta, e a SES reduz a agenda "
        "própria na mesma medida; c: a SES concentra o eletivo do código no projeto e suspende a própria agenda. Só as "
        "filas do plano: sem emergência, angio coronária, sedação e reservas. Aumento líquido = produção do projeto − o "
        "que a SES deixa de realizar.")
    aba("IEV", ["Exame", "Código", "Pedidos na fila (sem emergência)", "Fila viva", "Pessoas (soma das filas)",
                "Convênio", "OCI e papel do exame", "OCI contratadas", "O que o IEV fez até 26/10", "Fim da vigência",
                "Regra no plano 4"],
        [[l["exame"], l["codigo"], l["pedidos"], l["fila_viva"], l["pessoas"], l["convenio"], l["oci"], l["contratado"],
          l["feito"], l["vigencia"], l["regra"]] for l in rv["iev"]],
        "As filas que o IEV também pode atender, com o que ele contratou e o que fez (L-008 revista, 02/11/2026).")
    aba("Tempos", ["Código", "Fila", "Minutos", "Base"], rv["tempos"], "O tempo de sala de cada fila da carteira 1.")


def escrever(filas, rumo, cenarios, v26, destino, fontes, executante=None, revisao=None):
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
                                   "Livres para o plano 4", *[f"Na carteira {n.split(':')[0].split(' ')[0]}" for n in nomes],
                                   "De onde vem o número de OCI contratadas", "Quem atende"],
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
    if revisao:
        escrever_revisao(aba, revisao)
    aba("v26 pela Candanga", ["Código", "Descrição Candanga", "Meta v26", "Preço v26 (R$)", "Preço Candanga (R$)",
                              "Valor v26 (R$)", "Valor Candanga (R$)"],
        [[l["codigo"], l["descricao"], l["meta"], l["preco_v26"], l["preco_candanga"], l["valor_v26"],
          l["valor_candanga"]] for l in v26],
        "As metas da v26 assinada com o preço da Portaria 4.282 e com o da Candanga.")
    if executante:
        aba("Quem oferta", ["Código", "Unidade executante", "Tipo", "Agendamentos 12 m fechados",
                            "Média por mês, out. a mar.", "Média por mês, jul. a set.", "Maior mês", "Mês do maior",
                            "Out. 2026 (até 28)", "Nov. 2026 (já agendado)"], executante,
            "Oferta por unidade executante nos 17 códigos da carteira 1 (agendamentos pelo mês em que acontecem; por "
            "código, e não por fila: na TC entra a emergência do mesmo código), nos 12 meses fechados de "
            "out./2025 a set./2026. Serve para separar a oferta que fica (contratado, URD, unidade nova) do mutirão "
            "que acaba (unidade que sobe e volta a zero). Novembro ainda vai receber agendamentos.")
    aba("Fontes", ["Fonte", "Arquivo e localização"], fontes, "Toda conta do estudo sai destes arquivos.")
    wb.save(destino)


def quem_oferta(coleta, codigos):
    """Agendamentos por unidade executante, só nos códigos da carteira 1. O painel dá a unidade por código, e não por
    nome de fila: na TC, a conta inclui a emergência do mesmo código."""
    ex = coleta["por_codigo"]["executante"]
    linhas = [dict(zip(ex["cols"], l)) for l in ex["linhas"]]
    linhas = [l for l in linhas if l["codigo"] in codigos]
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


def carteira1(filas, rumo, coleta):
    """A carteira 1 de 02/11 sem a transfontanela (usuário, 03/11/2026): o valor dela se espalha pelos códigos com folga
    sob a falta da SES (espalhar), como na carteira 6. O resto da carteira fica como estava."""
    itens = carteira(filas, rumo, VALOR_EXAMES_V26, lambda f: "angio coronária" not in f["protocolo"], crescimento=True)
    return espalhar(itens, teto_folga(revisar_carteira1(filas, coleta, itens)))


def main():
    coleta = json.load(open(sys.argv[1], encoding="utf-8"))
    preco = ler_candanga(sys.argv[2])
    filas, rumo = montar(coleta, preco)
    # só as carteiras que chegam ao valor dos exames da v26 (usuário, 02/11/2026)
    cenarios = {
        "1 (escolhida, 02/11; sem a transfontanela, 03/11): parede abdominal no abdômen total, sem angio coronária, com os "
        "pedidos novos esperados": carteira1(filas, rumo, coleta),
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
        executante = quem_oferta(json.load(open(sys.argv[3], encoding="utf-8")),
                                 {i["codigo"] for i in next(iter(cenarios.values()))})
        fontes.append(["Oferta por unidade executante", sys.argv[3]])
    destino = AQUI / "estudo_filas_imagem_20261102.xlsx"
    revisao = revisar_carteira1(filas, coleta, next(iter(cenarios.values())))
    cenarios["6 (folga, 02/11): a carteira 1 limitada aos pedidos que chegam com a falta da SES, metade das faltas "
             "reagendada e 20% da agenda da SES encaminhada; o que sai do ultrassom vira TC"] = carteira_folga(
        next(iter(cenarios.values())), revisao)
    fontes += [["Região de Saúde das filas da carteira 1", str(COLETA_REGIAO.relative_to(AQUI.parent.parent.parent))],
               ["Fila de 15/09 e 05/10 dos onze nomes da v26", "planos/redacao_04/dados/fontes/mapa_social_20261005.md, seção 6"]]
    escrever(filas, rumo, cenarios, v26, destino, fontes, executante, revisao)
    json.dump({"filas": filas, "cenarios": cenarios, "v26": v26, "revisao": revisao}, open(AQUI / "estudo_filas_imagem_20261102.json", "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)
    print(destino)


if __name__ == "__main__":
    main()
