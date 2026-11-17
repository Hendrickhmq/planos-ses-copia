# Mapa Social, 25/10/2026 (recarga 14:31) — dados brutos da coleta

Recoleta da fila das sete OCI de cardiologia (subgrupo 09.02.01) do redacao_08 pelo método de
25/10/2026 (teto, finalidade e núcleo; fila viva de 24 meses; os alarmes), para comparar com a
coleta de 22/10/2026. Saída da Qlik Engine API do painel e o script que monta
`../mapa_social_20261025.xlsx`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de
nascimento.

| arquivo | o que é |
|---|---|
| `motor_20261025.json` | a saída do motor como veio: filas da composição em oito recortes de CID (inteira e viva), CID principais, agendadas em 12 meses, os números de cada OCI (teto, finalidade em 12/24/36 meses, variantes, núcleo), Região de Saúde da finalidade, pessoas em mais de uma OCI, pessoas por ano, a consulta de risco cirúrgico sem recorte |
| `motor_varredura_20261025.json` | a varredura das filas (solicitações e agendamentos), filtrada como diz a nota do arquivo, e o laboratório |
| `coleta_20261025.json` | o mesmo, organizado no formato do método (`filas`, `ocis`, `janela_viva_meses`, `filtro_fila`, `nomes_internos`, `enquadramento`), com os alarmes e a diferença para 22/10; gerado pelo script |
| `montar_20261025.py` | gera `coleta_20261025.json` e a planilha; não calcula número novo, só as razões dos alarmes e a diferença para 22/10 |

Rodar de dentro desta pasta: `python3 montar_20261025.py` (lê também
`../mapa_social_20261022_bruto/coleta_20261022.json`, para a diferença).

A coleta seguinte parte do `enquadramento` e dos `nomes_internos` de `coleta_20261025.json`,
não do `.md`. As cinco angiotomografias com espaço não separável estão com o U+00A0 no lugar
exato (ver a nota de `motor_varredura_20261025.json`).
