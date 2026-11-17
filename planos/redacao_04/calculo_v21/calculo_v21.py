"""v21 do plano 4 (07/10/2026): dez polos, sem localizacao fixa - so quantos em cada Regiao.

Decisao do usuario: partir dos seis polos da v20 e acrescentar quatro (um na Regiao Sul, um na
Sudoeste, um na Central e um nas Regioes Norte e Leste). Nenhum polo tem localizacao fixada.
Tomografia: so o minimo - pelo menos um polo de cada Regiao (Norte e Leste contadas juntas),
no minimo seis tomografos.

O rateio, as horas, a curva, as parcelas e o apoio sao os da v20 (calculo_v20/v20.json): os
seis territorios sao os mesmos. Muda o que depende do numero de polos.
"""
import os, json, math

AQUI = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(os.path.join(AQUI, "..", "calculo_v20", "v20.json")))

# os seis territorios da v20, na mesma ordem das colunas
REGIAO = {"Ceilândia": "Oeste", "Taguatinga": "Sudoeste", "Sobradinho": "Norte e Leste",
          "Plano Piloto": "Central", "Gama": "Sul", "Guará": "Centro-Sul"}
ORD = [REGIAO[p] for p in V["ORD"]]
POLOS = {"Oeste": 1, "Sudoeste": 2, "Norte e Leste": 2, "Central": 2, "Sul": 2, "Centro-Sul": 1}
assert sum(POLOS.values()) == 10


def por_regiao(chave):
    return {REGIAO[p]: v for p, v in V[chave].items()}


tot, us, tc = por_regiao("tot"), por_regiao("us"), por_regiao("tc")
hus, htc = por_regiao("hus"), por_regiao("htc")
dia_us, dia_tc = por_regiao("dia_us"), por_regiao("dia_tc")
# salas: regra dos 80% da v18-v20, e no minimo uma por polo
salas = {r: max(math.ceil(hus[r] / (252 * 10 * 0.8)), POLOS[r]) for r in ORD}
por_sala = {r: math.ceil(dia_us[r] / salas[r]) for r in ORD}
# medicos de US: horas / 1.800, e no minimo um por sala (um medico por sala durante o exame)
medicos_us = {r: max(math.ceil(hus[r] / 1800), salas[r]) for r in ORD}
radiologistas = {r: math.ceil(htc[r] / 1800) for r in ORD}
tomografos = {r: 1 for r in ORD}                      # minimo: um por Regiao
tecnicos = {r: 3 * tomografos[r] for r in ORD}         # 50 h / 24 h = 2,08 -> 3 por tomografo
enfermagem = {r: 2 * tomografos[r] for r in ORD}       # 50 h / 44 h = 1,14 -> 2 por tomografo
rt = dict(POLOS)                                       # responsavel tecnico medico por polo
retaguarda = dict(POLOS)                               # um por dia util em cada polo
recepcao = {r: 2 * POLOS[r] for r in ORD}              # 2 por polo
# apoio igual ao da v20: um operador por Regiao, assistentes 1/2/2/1/1/1
operadores = {REGIAO[p]: v for p, v in V["operadores"].items()}
assistentes = {REGIAO[p]: v for p, v in V["assistentes"].items()}

out = dict(V)
out.update({"ORD_REGIAO": ORD, "POLOS": POLOS, "tot_r": tot, "us_r": us, "tc_r": tc, "hus_r": hus, "htc_r": htc,
            "dia_us_r": dia_us, "dia_tc_r": dia_tc, "salas_r": salas, "por_sala_r": por_sala,
            "medicos_us_r": medicos_us, "radiologistas_r": radiologistas, "tomografos_r": tomografos,
            "tecnicos_r": tecnicos, "enfermagem_r": enfermagem, "rt_r": rt, "retaguarda_r": retaguarda,
            "recepcao_r": recepcao, "operadores_r": operadores, "assistentes_r": assistentes,
            "mes_us_r": por_regiao("mes_us"), "mes_tc_r": por_regiao("mes_tc")})

if __name__ == "__main__":
    for k in ["POLOS", "salas_r", "por_sala_r", "medicos_us_r", "radiologistas_r", "tomografos_r", "tecnicos_r",
              "enfermagem_r", "rt_r", "retaguarda_r", "recepcao_r", "operadores_r", "assistentes_r"]:
        print(f"{k:16}", out[k], sum(out[k].values()))
    json.dump(out, open(os.path.join(AQUI, "v21.json"), "w"), ensure_ascii=False, indent=1, default=str)
