# Recálculo da v19 (05/10/2026)

- `calculo.py` — o método da v18 reconstruído (rateio por procedimento com os dados de
  15/09, horas de sala por tempo de exame, curva por trimestre, produção por parcela).
  Rodado sozinho, reproduz a v18 ao exame e ao centavo.
- `v19.py` — aplica o cenário G (acréscimo pelas abertas de 2026) e grava `v19.json`.
- `editar_texto.py` — as cinco correções de texto de 05/10 sobre a v18.
- `aplicar_v19.py <docx_descompactado> limpo|marcado [com_texto]` — escreve a v19 no
  docx; `marcado` gera a cópia com amarelo (entrou) e rosa riscado (saiu).

Dependem de `lxml`. O método e as decisões estão em `../estado.yaml`, bloco `v19_20261005`.
