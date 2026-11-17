# A fila — Mapa Social da Saúde, base recarregada em 09/10/2026 11:32

Solicitações até 02/10/2026. Medida **fila**: os três status (pendente de regulação,
corrigida e reenviada, pendente por fila de espera); devolvidas fora. Os dezesseis nomes
de fila do plano 4, reunidos nos onze códigos do objeto. A coleta é do agente
`mapa-social`, com a varredura das filas, a Região de Saúde e o estudo de cada fila, em
`fontes/mapa_social_20261009.md`.

**É esta a base do `plano_v1_geral.md`** — os números da justificativa saem daqui.

## O que o documento usa

| procedimento | solicitações | pessoas | espera média |
|---|---|---|---|
| Ultrassonografia doppler colorido de vasos | 14.510 | 14.348 | 471 dias |
| Ultrassonografia mamária bilateral | 13.762 | 13.739 | 623 dias |
| Ultrassonografia de abdômen total | 13.375 | 13.108 | 548 dias |
| Ultrassonografia transvaginal | 9.814 | 9.813 | 636 dias |
| Ultrassonografia de aparelho urinário | 3.899 | 3.898 | 640 dias |
| Ultrassonografia de próstata por via abdominal | 3.337 | 3.331 | 583 dias |
| Ultrassonografia de tireoide | 3.168 | 3.168 | 479 dias |
| Ultrassonografia de abdômen superior | 2.271 | 2.269 | 693 dias |
| Tomografia computadorizada de abdômen superior | 4.125 | 4.122 | 128 dias |
| Tomografia computadorizada de tórax | 3.967 | 3.944 | 185 dias |
| Tomografia computadorizada de pelve, bacia e abdômen inferior | 3.649 | 3.647 | 129 dias |
| ultrassonografia, oito procedimentos | 64.136 | 55.608 | 569 dias |
| tomografia computadorizada, três procedimentos | 11.741 | 6.297 | 148 dias |
| objeto, onze procedimentos | 75.877 | 61.132 | 504 dias |

## O recurso contra a fila — CALCULADO

A fila de cada código vezes o valor de referência (`valor_unitario.md`):

| código | fila | valor de referência | valor da fila |
|---|---|---|---|
| 02.05.01.004-0 | 14.510 | R$ 100,18 | R$ 1.453.611,80 |
| 02.05.02.009-7 | 13.762 | R$ 99,94 | R$ 1.375.374,28 |
| 02.05.02.004-6 | 13.375 | R$ 100,18 | R$ 1.339.907,50 |
| 02.05.02.018-6 | 9.814 | R$ 99,94 | R$ 980.811,16 |
| 02.05.02.005-4 | 3.899 | R$ 99,94 | R$ 389.666,06 |
| 02.05.02.010-0 | 3.337 | R$ 99,94 | R$ 333.499,78 |
| 02.05.02.012-7 | 3.168 | R$ 99,94 | R$ 316.609,92 |
| 02.05.02.003-8 | 2.271 | R$ 99,94 | R$ 226.963,74 |
| 02.06.03.001-0 | 4.125 | R$ 299,44 | R$ 1.235.190,00 |
| 02.06.02.003-1 | 3.967 | R$ 300,10 | R$ 1.190.496,70 |
| 02.06.03.003-7 | 3.649 | R$ 299,44 | R$ 1.092.656,56 |
| **fila do objeto** | **75.877** | | **R$ 9.934.787,50** |

- A execução dos exames do pré-plano (R$ 10.673.026,22, `envelope.md`) é 107,4% do valor da
  fila do objeto. Os 79.373 exames do plano 4 são 104,6% das 75.877 solicitações. Por isso
  o documento diz que o recurso alcança o volume **dessas filas**, sem número fechado de
  exames (`metodo/pre_plano/formulario.md`).
- **Com as 82 filas "a decidir" da varredura**, que têm os mesmos códigos (9.378
  solicitações; seção 1 da coleta), o valor sobe para R$ 11.882.537,72, e a execução cobre
  89,8%. Por isso o documento não diz "a fila dos onze procedimentos": diz "essas filas", as
  da tabela. Decisão em aberto: `../pendencias.md`, P-04 e P-05.

## A diferença para a base do plano 4

O plano 4 dimensiona os 79.373 exames pela extração de 10/09/2026 do sistema de regulação
da SES-DF (78.572 solicitações, painel interno) mais 801 entradas. O Mapa Social é a fonte
pública e mede 75.877 em 09/10/2026. O pré-plano cita só o Mapa Social, como o formulário
pede, e não fixa quantidade por procedimento: a do plano 4 é pactuação posterior.

## Conferência cruzada — a coleta da conversa contra a do agente, 09/10/2026

A primeira coleta do dia foi feita na conversa principal, sobre a base das 09:32. O usuário
pediu que a coleta fosse sempre do agente, e o agente refez a coleta sem ler a primeira,
sobre a base das 11:32. A da conversa saiu da pasta; a do agente ficou.

| | conversa (09:32) | agente (11:32) | diferença |
|---|---|---|---|
| objeto, solicitações | 75.870 | 75.877 | +7 |
| objeto, pessoas | 61.127 | 61.132 | +5 |
| ultrassonografia | 64.133 | 64.136 | +3 |
| tomografia | 11.737 | 11.741 | +4 |
| por código | | | de −1 a +2 em cada um |
| espera média, por código e nos conjuntos | | | igual, em dias inteiros |
| Região de Saúde | | | até 4 por linha |
| filas fora do enquadramento | 54 filas, 6.315 (busca pelo nome) | 82 filas do mesmo código, 9.378, mais 20 de outro código | a busca pelo nome perdeu, entre outras, o doppler arterial de MMII (1.781) e as TC de abdômen superior de emergência ("SUPER.", 708 e 374) |

As contagens do objeto batem: a diferença é a recarga das 11:32. **A varredura da conversa
estava incompleta**, porque procurou pelo nome e não pelo código, que é o que o método de
09/10/2026 pede para exame avulso.
