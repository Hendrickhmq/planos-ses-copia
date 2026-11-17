# estudos/ — estudos internos do plano 4

Uso interno do usuário. Nada daqui vai ao plano nem aos parceiros sem decisão dele.

- `estudo_polos_rede_capacidade_20261020.md` — o quadro decidido, por que juntar a Central e a Centro-Sul (demanda,
  distância, transporte e a rede de clínicas), a rede com CNES, o ultrassom com margem, a tomografia em 6 e em 5 polos
  (a Leste sem) e o que falta confirmar.
- `custo_por_exame_v2_20261020.xlsx` — **a versão para decidir:** quanto custa executar o plano em três cenários (tudo
  nas clínicas; ultrassom feito por nós nos 6 polos; misto, com os polos escolhidos na planilha), com o ultrassom e a
  tomografia polo a polo, a equipe e as premissas numa aba só. Gerada por
  `../calculo_v24/planilha_cenarios_execucao.py`.
- `salas_ultrassom_metricas_20261020.xlsx` — se as 13 salas do documento da equipe de 20/10 (Projeto Zero Fila | USG,
  quantitativo revisado) aguentam: a rede em 11 cenários (tempo por exame, faltas, salas fechadas, 7 meses), cada
  unidade pela fila do plano e pela população do documento, e a tabela de sensibilidade. Gerada por
  `../calculo_v24/planilha_salas_metricas.py`.
- `custo_por_exame_v1_20261020.xlsx` — a primeira versão, guardada como estava: ultrassom pela execução própria, tomografia
  pelas clínicas, a comparação da tomografia com equipe própria e a conta por polo em duas contas. Gerada por
  `../calculo_v24/planilha_custo_por_exame.py`.
- `estudo_filas_imagem_20261102.md` e `.xlsx` — **o estudo das filas de imagem para escolher a carteira do plano 4** pela
  Candanga: o inventário de todas as filas de imagem (coleta de 02/11/2026), o rumo de cada código, quem sustenta a oferta,
  a cobertura dos outros planos (L-008, IEV, redacao_07), a viabilidade e as carteiras comparadas com a v26 e com a
  recomendação de 01/11. Gerado por `estudo_filas_imagem_20261102.py` (o `.json` ao lado é a saída intermediária).
- `estudo_outros_planos_imagem_20261102.md` e `.xlsx` — **o que os planos aprovados já contratam** (os cinco convênios
  do acervo: oftalmologia do ISHP e as OCI do IEV), com quantidades, o exame de imagem de cada OCI e a medida da
  transvaginal com os CID da GIN1. Os nossos planos em elaboração ficam à parte e não contam. Gerado por
  `estudo_outros_planos_imagem_20261102.py`.
- `estudo_filas_imagem_20261102_organizada.xlsx` — **a cópia organizada da planilha do estudo das filas, para ler e
  mostrar:** resumo das carteiras, carteiras por código, quem atende o quê, rumo das filas, fila por fila, viabilidade, quem
  oferta, inventário e fontes. Gerada por `formatar_estudo_filas_imagem_20261102.py` a partir da planilha completa; não
  refaz conta.
