# Mapa Social, 22/10/2026 (recarga 08:32) — dados brutos da coleta

Primeira coleta do redacao_08: a fila das sete OCI de cardiologia (subgrupo 09.02.01) para o
dossiê do objeto. Saída da Qlik Engine API do painel e o script que monta
`../mapa_social_20261022.xlsx`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de
nascimento.

| arquivo | o que é | aba da planilha |
|---|---|---|
| `coleta_20261022.json` | datas, medida da fila (`filtro_fila`), recortes de CID, nomes internos exatos das filas (`nomes_internos`), enquadramento OCI → filas (`enquadramento`), fila a fila por recorte, conjuntos por OCI, Região de Saúde, pessoas em mais de uma OCI, fila por ano, agendadas por unidade executante, unidades privadas, CID principais e a varredura (solicitações e agendamentos) | 1 a 12 |
| `montar_20261022.py` | monta a planilha; não calcula nada, só dispõe os números do motor | |

Rodar de dentro desta pasta: `python3 montar_20261022.py`.

A coleta seguinte parte do `enquadramento` e dos `nomes_internos` do JSON, não do `.md`.
