# v20 (06/10/2026) — Ofício 40 e seis polos, sobre a v6 da equipe

- `calculo_v20.py` — o método da v19 (`../calculo_v19/calculo.py`) com o recurso de
  R$ 11.592.762,00, o apoio da opção C (R$ 922.260,00) e seis polos; grava `v20.json`.
- `aplicar_v20.py <docx_descompactado> limpo|marcado` — escreve os valores e os polos na
  v6 (`../dados/PT_simplificado_exames_de_imagem_v6.docx`); `marcado` gera a cópia com
  amarelo (entrou) e rosa riscado (saiu).
- `sumario_v20.py` — o sumário da v6 é texto fixo; atualiza as páginas pelo deslocamento
  medido no LibreOffice entre a v6 e a v20.
- `docxlib.py` — troca de texto dentro do parágrafo preservando o run, clonagem de linha
  e de coluna de tabela, marcas da cópia.
- `gerar_v20.sh <python_com_lxml> <pasta>` — roda tudo e gera `v20_limpo.docx` e
  `v20_marcado.docx`. Precisa de `lxml`, `soffice` e `pdftotext`/`pdfinfo`.

As decisões e o método estão em `../estado.yaml`, bloco `v20_20261006`.
