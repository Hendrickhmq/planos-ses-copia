# Custos e margens do plano 4

Controle interno: nada daqui vai à SES nem ao parceiro sem decisão.

- `final.xlsx` — **a nossa planilha final: a nossa conta, sem a comparação** (11/11). É a coluna "nosso" da planilha
  abaixo, com as trocas do usuário de 11/11: médico R$ 35 no ultrassom sem Doppler e R$ 40 com Doppler (antes R$ 33,33
  nos dois); auxiliar de sala R$ 3.180 por posto (antes R$ 2.959); tomografia R$ 180, mais R$ 50 com contraste (antes
  R$ 175 + R$ 43). Abas:
  - Simulador: uma linha por exame, com quantidade, tipo, preço, minutos e a parte da tomografia feita com contraste
    para trocar; margem por exame (fixo dividido igual e pelo tempo de sala); margem por hora de sala (12/11: a margem
    pelo tempo × exames por hora, como na readequação de 09/11), também com o médico pago a R$ 100 por hora de exame;
    no ultrassom, os exames por hora são a premissa (os minutos saem deles), com os exames por hora para empatar; se o
    valor fecha, se cabe nas salas e o quadro do contraste. Na aba Custos, as salas podem ser fixas ou acompanhar as
    horas de exame (com um uso máximo): aí, mais exames por hora pedem menos salas e baixam o fixo. As quantidades moram aqui: Custos e Volume vão atrás delas. Substitui a aba Margens;
  - Custos: quantidades, valores unitários, custo dos exames, margem, valor a fechar e valor final por exame;
  - Pessoas e Volume, como na planilha abaixo, só com a nossa conta;
  - Médico (12/11, pedido do usuário: a tireoide paga menos que um exame que demora mais): o médico do ultrassom pago
    pelo tempo do exame, valor da hora × minutos de sala do Simulador. Ao lado do pagamento por exame (R$ 35 e R$ 40),
    mostra por exame, por médico (mês e turno de 5 h) e com outros valores da hora (R$ 100, R$ 174,30 do IgesDF). Na
    aba Custos, seção 2, ficam o modo ("pelo tempo" ou "por exame"), o valor da hora e um adicional do Doppler. A
    partida é "pelo tempo" a R$ 101,71 por hora, que mantém o gasto de hoje com médico (R$ 2.749.335 em 27.031 h):
    R$ 25,43 nos exames de 15 min, R$ 33,90 nos de 20 min e R$ 67,81 no Doppler de membros (40 min). A margem do
    conjunto não muda, mas muda por linha: o Doppler de membros vai a −24% e a tireoide a +3% (pelo tempo).

  Gerada por `gerar_custos_e_margens_nosso_20261111.py`, recalculada no LibreOffice do mesmo jeito.
- `final_sebastiao.xlsx` — **a mesma planilha, pelos valores do Sebastião** (12/11): as mesmas abas e os mesmos exames
  da final (carteira v3), com as premissas de `../estudos/planilha_custos_sebastião.xlsx` (ofício de 09/11): 11 salas em
  6 unidades, plantão de 9 h úteis, 1 auxiliar por sala, 1 recepção por unidade a R$ 3.500, sala a R$ 1.500, materiais
  a R$ 3,25, limpeza e gestão por mês da rede, tomografia R$ 175 + R$ 43 e 96% da fila com contraste (93% de toda a
  tomografia). A mais que a final: a garantia de R$ 1.500 por plantão, com o cenário do médico (melhor ou pior) no alto
  do Simulador, e o tempo do estudo dele (70 ultrassons em 9 h) nos minutos de sala. Gerada pelo mesmo script:
  `python3 gerar_custos_e_margens_nosso_20261111.py sebastiao`.
- `custos_e_margens_sebastiao_x_nosso_20261111.xlsx` — **a conta do Sebastião ao lado da nossa** (11/11):
  - aba Comparativo: quantidades de exames, salas, minutos e uso das salas; valores unitários; o custo dos mesmos exames
    pelas duas contas, na rede dele (54.589 ultrassons em 11 salas) e na nossa (carteira v3 em 14 salas), com e sem a
    garantia do médico; e o valor final por exame: ultrassom, Doppler e tomografia com e sem contraste;
  - aba Pessoas: médicos, auxiliares e recepção por sala e por unidade, e o que fica sem preço;
  - aba Volume: o custo por exame do ultrassom conforme o volume, com as salas fixas e com as salas acompanhando o volume;
  - aba Margens: a margem de cada procedimento da carteira v3 pela Candanga, pela conta dele (com e sem a garantia) e
    pela nossa (com o fixo dividido igual e na proporção do tempo de sala).

  Gerada por `gerar_custos_e_margens_sebastiao_x_nosso_20261111.py`; os valores gravados vêm do LibreOffice
  (`soffice --headless --convert-to xlsx`). As fontes são os estudos em `../estudos/`: `planilha_custos_sebastião.xlsx`,
  `roteiro_reuniao_20261110.md`, `estudo_tempos_tomografia_3_polos_20261109.md` e `carteira_final_v3_20261111.xlsx`.
