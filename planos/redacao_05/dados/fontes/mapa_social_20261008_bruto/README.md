# Mapa Social, 08/10/2026 (recarga 21:32) — dados brutos da coleta

Coleta piloto do agente `mapa-social`: a fila das três OCIs de otorrinolaringologia do
pré-plano geral do redacao_05. Saída da Qlik Engine API do painel e o script que monta
`../mapa_social_20261008.xlsx`. Só contagens agregadas: nenhum CNS, CPF ou nome.

| arquivo | o que é | aba da planilha |
|---|---|---|
| `coleta_20261008.json` | fila, pessoas, devolvidas, espera, idade, região, abertas e agendadas por mês, CID principais, expressões usadas e nomes internos das filas | 1 a 4, 6 e 8 |
| `montar_20261008.py` | monta a planilha; soma faixas etárias (5), entrantes (7) e compara com 07/10 e 08/10 07:32 (9) | |

Rodar de dentro desta pasta: `python3 montar_20261008.py`.
