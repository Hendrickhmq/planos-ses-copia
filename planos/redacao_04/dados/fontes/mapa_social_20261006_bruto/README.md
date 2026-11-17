# Mapa Social, 06/10/2026 — dados brutos da coleta

Saída da Qlik Engine API do painel e o script que monta `../mapa_social_20261006.xlsx`,
coleta feita pelo Claude no navegador embutido. Só contagens agregadas: nenhum CNS, CPF
ou nome de usuário.

| arquivo | o que é | aba da planilha |
|---|---|---|
| `coleta_20261006.json` | fila, pessoas, espera, região, idade, risco, entrantes e pessoas por código | 1 a 4, 6 a 9 |
| `dev_20261006.json` | devolvidas por nome de fila | 10 |
| `montar_20261006.py` | monta a planilha inteira; calcula rateio (5), entrantes (7, 8) e comparação com 05/10 (11) | |
| `entr_rows_20261006.json` | saída intermediária do script: entrantes por nome de fila | 7, 8 e 11 |
