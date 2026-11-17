# A fila — Mapa Social da Saúde, base recarregada em 15/10/2026 19:32

Solicitações até 15/10/2026. Medida **fila**: os três status (pendente de regulação,
corrigida e reenviada, pendente por fila de espera); devolvidas fora. Por código SIGTAP,
somando todos os nomes de fila do SISREG com aquele código. A coleta é do agente
`mapa-social`, em `fontes/mapa_social_20261015.md` (conferência 7/7).

**É esta a base do `plano_v1_geral.md`.** A carteira passou de dez para dezesseis procedimentos em
19/10/2026 e para doze em 20/10/2026, quando saíram as TC de coluna (cervical, torácica,
lombo-sacra) e de segmentos apendiculares, que se sobrepõem às OCI de ortopedia do IEV (usuário).

## O que o documento usa

| código | procedimento | solicitações | pessoas | espera média |
|---|---|---|---|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | 6.461 | 6.458 | 49 dias |
| 02.04.06.002-8 | Densitometria óssea | 2.196 | 2.196 | 44 dias |
| 02.05.02.016-0 | Ultrassonografia pélvica (ginecológica) | 1.003 | 994 | 603 dias |
| 02.05.02.007-0 | Ultrassonografia de bolsa escrotal | 995 | 994 | 588 dias |
| 02.05.02.008-9 | Ultrassonografia de globo ocular / órbita | 1.272 | 1.272 | 264 dias |
| 02.05.02.017-8 | Ultrassonografia transfontanela | 281 | 281 | 282 dias |
| 02.05.02.014-3 | Ultrassonografia obstétrica | 464 | 464 | 144 dias |
| 02.05.02.015-1 | Ultrassonografia obstétrica com doppler | 205 | 205 | 177 dias |
| 02.06.01.005-2 | Tomografia computadorizada do pescoço | 755 | 746 | 139 dias |
| 02.06.01.007-9 | Tomografia computadorizada do crânio | 1.467 | 1.440 | 197 dias |
| 02.06.01.004-4 | Tomografia computadorizada de face / seios da face / ATM | 500 | 488 | 124 dias |
| 02.06.01.006-0 | Tomografia computadorizada de sela túrcica | 45 | 43 | 169 dias |

As pessoas não se somam entre códigos: a mesma pessoa pode esperar mais de um exame.

## Por modalidade — CALCULADO

**Fora do documento desde 20/10/2026:** a média de exames diferentes esconde a variação
(usuário: a linha de 405 dias "não faz sentido"). O documento ordena os dezesseis pela espera
média e, no empate, pelo tamanho da fila. Fica aqui só como registro.

Solicitações somadas por código (cada solicitação tem um código só). A espera média do grupo é a média
das esperas de cada código ponderada pela fila, que é a média sobre as solicitações do grupo. Pessoas
não se somam, e a linha do grupo fica sem elas.

| grupo | solicitações | espera média (calculada) | o documento diz |
|---|---|---|---|
| mamografia e densitometria óssea | 8.657 | 47,74 dias | 48 dias |
| ultrassonografia, seis procedimentos | 4.220 | 404,68 dias | 405 dias |
| tomografia computadorizada, oito procedimentos | 3.343 | 174,22 dias | 174 dias |
| carteira, dezesseis procedimentos | 16.220 | 166,67 dias | 167 dias |

Mamografia e densitometria = 8.657 de 16.220 = 53,4% das solicitações.

## O recurso contra a fila — CALCULADO

| | valor |
|---|---|
| valor das doze filas (fila × valor de referência, `valor_unitario.md`) | R$ 2.381.702,87 |
| execução dos exames (recurso − 10% de gestão e apoio) | R$ 1.352.418,30 |
| execução ÷ valor das filas | 56,8% |
| pedidos atendidos ÷ pedidos das doze filas (15.644), na ordem de cada cenário com 10% de apoio | cenário 1: 11.321 (72,4%); cenário 2: 8.080 (51,6%); cenário 3: 11.721 (74,9%) |
| o que o documento diz | "mais da metade": 56,8% do valor, e de 51,6% a 74,9% dos pedidos conforme a ordem |

Por código: mamografia R$ 645.453,90; densitometria R$ 483.998,40; os cinco ultrassons
R$ 375.423,84; as três tomografias R$ 816.949,62 (detalhe em `cobertura.md`). Os seis que
entraram em 19/10/2026: a TC de sela túrcica R$ 13.504,95 e a US obstétrica R$ 46.372,16 ficam;
as quatro TC que saíram em 20/10/2026 somavam R$ 172.911,11.

## O cenário de execução — CALCULADO (usuário, 20/10/2026)

As dez filas de espera longa primeiro, na ordem da espera; mamografia e densitometria de reserva.

| | valor |
|---|---|
| as dez filas, para zerar | R$ 1.252.250,57 |
| recurso para exames (10% de apoio) | R$ 1.352.418,30 |
| diferença, para a reserva | R$ 100.167,73: cerca de 1.002 mamografias (15% da fila) |
| pedidos feitos em 2026 ainda na fila das dez | 4.546, R$ 914.603,07 (uns R$ 96 mil por mês) — indicador, não a medida de entrantes |

Detalhe em `estudo_das_filas.md` e `../cenario_4_espera_longa_com_reserva.xlsx`.

## A mamografia

O código 02.04.03.018-8 é de rastreamento (ficha `fontes/sigtap_0204030188_102026.md`). Os
6.461 somam dois nomes do SISREG registrados com ele: "MAMOGRAFIA BILATERAL PARA SCREENING
(ROTINA)", 6.274, e "MAMOGRAFIA BILATERAL DIAGNOSTICA", 187. O documento usa o total do
código, como a fila está registrada; o enquadramento de cada pedido é da regulação e do
plano detalhado.
