# Mapa Social, 28/10/2026 (recarga 08:33) — dados brutos da coleta

Coleta do agente `mapa-social` para o estudo de estruturação do redacao_09: a demanda
regulada dos ambulatórios de saúde mental infantojuvenil (COMPP e Adolescentro). Saída da
Qlik Engine API do painel e o script que monta `../mapa_social_20261028.xlsx`. Só
contagens agregadas: nenhum CNS, CPF ou nome.

| arquivo | o que é |
|---|---|
| `coleta_20261028.json` | datas, medida da fila (`filtro_fila`), enquadramento com os nomes internos exatos das filas e a decisão de cada uma, estudo de cada fila, varredura por CID F em menores de 18, Região de Saúde, CID principais, classificação de risco, uniões no motor, abertas e agendadas por mês, agendadas por status, unidades executantes e solicitantes |
| `montar_20261028.py` | monta a planilha; a única conta fora do motor é a soma abertas + agendadas da aba 6 (entrantes), marcada como calculada |

Rodar de dentro desta pasta: `python3 montar_20261028.py`.

O nome `­ CONSULTA EM PSICOLOGIA` começa por um hífen discricionário (U+00AD), gravado
como `­` no JSON. `CONSULTA EM REABILITACAO INTELECTUAL  - ADULTO` tem dois espaços.
