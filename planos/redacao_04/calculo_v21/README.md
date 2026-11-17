# v21 (07/10/2026) — dez polos sem localização fixa, sobre a v7 FINAL da equipe

- `calculo_v21.py` — reaproveita o cálculo da v20 (`../calculo_v20/v20.json`): os seis territórios
  são os mesmos. Acrescenta os polos por Região (1/2/2/2/2/1) e o que depende deles: salas (no mínimo
  uma por polo), médicos de US (no mínimo um por sala), responsável técnico, retaguarda e recepção.
  Tomografia no mínimo um tomógrafo por Região. Grava `v21.json`.
- `aplicar_v21.py <docx_descompactado> limpo|marcado` — troca, na v7 FINAL
  (`../dados/PT_simplificado_exames_de_imagem_v7_FINAL.docx`), as cidades pelas Regiões e escreve o
  número de polos; `marcado` gera a cópia com amarelo (entrou) e rosa riscado (saiu).
- `gerar_v21.sh <python_com_lxml> <pasta>` — roda tudo, inclusive o sumário (`../calculo_v20/sumario_v20.py`).

As decisões estão em `../estado.yaml`, bloco `v21_20261007`.
