"""
conferencia/verificacoes.py do redacao_03 — a bateria propria deste plano.

O conferir_plano.py carrega este arquivo e roda cada funcao verificar_<nome>(d, r, P),
depois da bateria do padrao. P e o proprio conferir_plano.py em execucao: daqui se usam
as funcoes dele (tabela_com, num, perto, chave, escalar) e os parametros ja lidos
(POLOS). Ver metodo/plano/conferencia.md.

+G  DIMENSIONAMENTO DA ENDOSCOPIA  salas, recuperacao, espera e endoscopios
                                    recalculados dos parametros declarados no
                                    estado.yaml, polo a polo.

Origem: era a verificacao G da ferramenta geral, com as constantes da endoscopia. Saiu
de la na reorganizacao de 08/10/2026: nenhuma formula de um objeto fica na bateria do
padrao.
"""
import math

# Sao parametros deste plano, os de dados/parametros_tecnicos.md, declarados em
# parametros.dimensionamento do estado.yaml.
PARAMETROS_DIMENSIONAMENTO = {
    "horas_sala_dia": "jornada efetiva de sala, em horas por dia util",
    "min_sala_por_paciente": "intervalo de sala por paciente, em minutos",
    "min_recuperacao": "permanencia em recuperacao, em minutos",
    "horas_espera": "permanencia na sala de espera, em horas",
    "pessoas_por_paciente": "pessoas na espera por paciente (usuario e acompanhante)",
    "min_processamento_aparelho": "processamento do aparelho entre usos, em minutos",
}


def parametros_dimensionamento(P, estado):
    """({nome: valor}, [faltando]) de parametros.dimensionamento no estado.yaml"""
    valores, faltando = {}, []
    for nome in PARAMETROS_DIMENSIONAMENTO:
        v = P.escalar(estado, f"dimensionamento.{nome}")
        if v is None:
            faltando.append(nome)
        else:
            valores[nome] = v
    return valores, faltando


def verificar_dimensionamento(d, r, P):
    """+G — dimensionamento da endoscopia, polo a polo"""
    tabela_com, chave, num, perto, POLOS = P.tabela_com, P.chave, P.num, P.perto, P.POLOS
    falhas = []
    t = tabela_com(d["tbs"], "Salas de procedimento", "Endoscópios")
    if not t:
        r.add("+G", "dimensionamento da endoscopia", False,
              ["tabela de capacidade por polo (salas e endoscopios) nao encontrada"]); return
    cab = t[0]
    if not POLOS:
        r.add("+G", "dimensionamento da endoscopia", True, ["plano sem polos declarados em estado.yaml"], na=True); return
    par, faltando = parametros_dimensionamento(P, d["estado"])
    if faltando:
        r.add("+G", "dimensionamento da endoscopia", False,
              [f"estado.yaml sem parametros.dimensionamento.{n} ({PARAMETROS_DIMENSIONAMENTO[n]})"
               for n in faltando]); return
    HORAS, T_SALA = par["horas_sala_dia"], par["min_sala_por_paciente"]
    T_REC, T_PERM = par["min_recuperacao"], par["horas_espera"]
    PESSOAS, T_PROC = par["pessoas_por_paciente"], par["min_processamento_aparelho"]
    cols = [i for i, c in enumerate(cab) if chave(c) in POLOS]
    if len(cols) != len(POLOS):
        achados = [chave(c) for c in cab if chave(c) in POLOS]
        r.add("+G", "dimensionamento da endoscopia", False,
              [f"o estado.yaml declara {len(POLOS)} polos {POLOS} e a tabela de "
               f"capacidade traz {len(cols)} {achados} — cabecalho: {cab}"]); return
    nomes_polo = [cab[i].strip() for i in cols]
    linhas = {l[0].lower(): l for l in t if l}
    def pega(chave):
        for k, l in linhas.items():
            if chave in k:
                return [num(l[i]) if i < len(l) else None for i in cols]
        return None
    entradas = pega("entradas por dia")
    salas = pega("salas de procedimento")
    rec = pega("postos de recuperação")
    esp = pega("lugares na sala de espera")
    endo = pega("endoscópios")
    if not entradas or not salas:
        r.add("+G", "dimensionamento da endoscopia", False, ["linhas de entradas ou salas nao lidas"]); return
    ents = [e for e in entradas if e]
    # exame nao se faz pela metade: a capacidade da sala e o piso da divisao
    cap_sala = math.floor(HORAS * 60 / T_SALA)
    ocup = pega("ocupação média")
    for i, e in enumerate(ents):
        n_calc = math.ceil(e / cap_sala)
        # a sala se confere pelo MINIMO, nao pela igualdade: a folga de ocupacao e
        # deliberada — absorve falta, intercorrencia e o ciclo de processamento. O que
        # amarra o numero publicado e a ocupacao declarada, conferida logo abaixo.
        if salas and i < len(salas) and salas[i] and int(salas[i]) < n_calc:
            falhas.append(f"{nomes_polo[i]}: {e}/{cap_sala} = {e/cap_sala:.2f} -> minimo {n_calc} salas, publicado {int(salas[i])}")
        if ocup and salas and i < len(ocup) and ocup[i] and i < len(salas) and salas[i]:
            calc = e / (int(salas[i]) * cap_sala) * 100
            if not perto(calc, ocup[i], 0.5):
                falhas.append(f"{nomes_polo[i]}: ocupacao {e}/({int(salas[i])}x{cap_sala}) = "
                              f"{calc:.1f}%, publicado {ocup[i]:.0f}%")
        ch = e / HORAS
        n_rec = math.ceil(ch * T_REC / 60)
        if rec and i < len(rec) and rec[i] and int(rec[i]) < n_rec:
            falhas.append(f"{nomes_polo[i]}: recuperacao {ch:.2f}x{T_REC}min = {ch*T_REC/60:.2f} -> minimo {n_rec}, publicado {int(rec[i])}")
        pessoas = ch * T_PERM * PESSOAS
        if esp and i < len(esp) and esp[i] and esp[i] < pessoas:
            falhas.append(f"{nomes_polo[i]}: espera calculada {pessoas:.1f} pessoas > publicado {int(esp[i])} lugares")
        giro = ch * (T_SALA + T_PROC) / 60
        n_endo = math.ceil(giro)
        if endo and i < len(endo) and endo[i] and int(endo[i]) < n_endo:
            falhas.append(f"{nomes_polo[i]}: endoscopios em giro {giro:.2f} -> minimo {n_endo}, publicado {int(endo[i])}")
    # o que a G recalculou nao precisa de lastro em dados/: ja tem lastro em conta
    conferidos = d.setdefault("_conferidos", set())
    # com a unidade junto: 17 entradas por dia nao autoriza um "17%" solto
    for serie, unid in ((entradas, ""), (salas, ""), (rec, ""), (esp, ""),
                        (endo, ""), (ocup, "%")):
        for v in (serie or []):
            if v is not None:
                conferidos.add((round(v, 2), unid))
    r.add("+G", f"dimensionamento da endoscopia ({len(ents)} polos)", not falhas, falhas)
