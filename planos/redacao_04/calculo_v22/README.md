# v22 (07/10/2026) — oito meses, dez polos e gestão nova, sobre a v7 FINAL da equipe

- `calculo_v22.py` — o método da v20/v21 com 8 meses de vigência e de execução (168 dias úteis,
  quatro bimestres), o quadro de gestão novo (R$ 919.640,00) e os dez polos por Região. Salas e
  tomógrafos pela regra dos 80% sobre 1.344 h no período; médicos a 1.200 h no período. Grava `v22.json`.
- `aplicar_v22.py <docx_descompactado> limpo|marcado` — escreve tudo na v7 FINAL numa passada só
  (os dez polos da v21 e o que veio depois); `marcado` gera a cópia com amarelo (entrou) e rosa
  riscado (saiu). Os riscos ficam com a redação da v7, só com números novos.
- `gerar_v22.sh <python_com_lxml> <pasta>` — roda tudo, inclusive o sumário.

As decisões estão em `../estado.yaml`, bloco `v22_20261007`.
