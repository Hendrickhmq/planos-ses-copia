"""
conferencia/mutacoes.py do redacao_03 — os erros que so a bateria deste plano sabe pegar.

O testar_conferencia_plano.py junta esta lista a dele: cada erro e injetado numa copia
do plano, e a verificacao da sigla tem de falhar. Mesmo formato da lista geral:
(sigla, descricao, arquivo, mutador[, se_aplica]). Ver metodo/plano/conferencia.md.

Origem: eram as mutacoes da G na lista geral, ate a reorganizacao de 08/10/2026.
"""
import re


def salas_abaixo(t):
    """salas do primeiro polo uma abaixo do que as entradas exigem"""
    m = re.search(r"(\| Salas de procedimento \| \*{0,2})(\d)", t)
    if not m:
        return None
    return t[:m.end(1)] + str(int(m.group(2)) - 1) + t[m.end(2):]


def parametro_ausente(t):
    """parametro de dimensionamento apagado do estado.yaml"""
    m = re.search(r"^\s*min_sala_por_paciente:.*\n", t, re.M)
    return t[:m.start()] + t[m.end():] if m else None


MUTACOES = [
    ("+G", "salas de um polo abaixo do necessario", "plano.md", salas_abaixo),
    ("+G", "parametro de dimensionamento ausente", "estado.yaml", parametro_ausente),
]
