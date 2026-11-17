# Mapa Social, 05/10/2026 — dados brutos da coleta

Saída da Qlik Engine API do painel e os scripts que montaram
`../mapa_social_20261005.xlsx`, feitos em três sessões do Claude no navegador embutido.
Só contagens agregadas: nenhum CNS, CPF ou nome de usuário.

| arquivo | o que é | aba da planilha |
|---|---|---|
| `coleta_20261005.json` | fila, pessoas, espera, região e faixa etária por nome de fila | 1 a 6 |
| `rateio.py`, `rateio_out.json` | rateio entre polos calculado a partir da coleta | 5 |
| `xlsx.py` | monta a planilha das abas 1 a 6 | |
| `entrantes_20261005.json`, `entr_rows.json`, `entr.py` | entradas de 2025 e 2026: abertas + agendadas, pela data da solicitação | 7 e 8 |
| `xlsx2.py` | acrescenta as abas 6 a 9 | |
| `dev.json`, `dev.py` | devolvidas por nome de fila | 10 |
