# Validação dos 11 procedimentos de ultrassonografia — Lista de Espera SUS-DF

Coleta recebida do usuário em **15/09/2026**, arquivada em
`validacao_ultrassom_20260915.xlsx`. Mesma origem da coleta de tomografia: Mapa Social
da Saúde (MPDFT), dados do SISREG/DATASUS, extração pela Qlik Engine API, base
carimbada em 15/09/2026 13:32:28, todos os anos.

**Medida usada: `Solicitações`** — os três status de fila. É a medida certa, e a
coleta a declara no cabeçalho.

---

## 1. L-001 resolvida — os dois nomes sem código têm código

| nome interno no SISREG | SIGTAP | descrição |
|---|---|---|
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | **02.05.02.004-6** | ULTRASSONOGRAFIA DE ABDOMEN TOTAL |
| ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL *(variante, 1 solicitação)* | **02.05.02.004-6** | ULTRASSONOGRAFIA DE ABDOMEN TOTAL |
| ECOGRAFIA␣␣DE PARTES MOLES *(espaço duplo no nome)* | **02.05.02.006-2** | ULTRASSONOGRAFIA DE ARTICULAÇÃO |

**A parede abdominal é faturada como abdômen total** — o mesmo código da *Ecografia de
abdômen total adulto*, que já estava no objeto. As duas linhas da planilha colapsam
numa só, de 13.080 exames.

**As partes moles são faturadas como ultrassonografia de articulação**, código que o
objeto ainda não usava. Entra como linha própria, de 2.974 exames.

**Os oito códigos que o plano já usava conferem 100% com o painel.**

### O efeito no unitário

Parede abdominal deixa de valer R$ 99,94 e passa a valer **R$ 100,18** — o
02.05.02.004-6 tem base de tabela de R$ 37,95 com incremento de 164%, não R$ 24,20
com 313%.

## 2. A quantidade máxima do doppler — a maior sensibilidade aberta, fechada

> SIGTAP: 5 por AIH/competência, e **"ESTAS QUANTIDADES DE PROCEDIMENTO REALIZADO,
> INDEPENDEM DA QUANTIDADE DE VASOS ESTUDADOS"**.

**Um doppler venoso bilateral de membros inferiores é um registro, não dois.** A linha
de 14.401 exames não dobra, e o risco de R$ 981.062,74 que este projeto vinha
carregando não existe.

## 3. Espera da fila — os onze procedimentos

| procedimento | solicitações | média, em dias | mediana, em dias |
|---|---|---|---|
| Ecografia de mamas bilateral | 14.396 | 624,1 | 517,1 |
| Ecografia transvaginal | 10.383 | 593,0 | 433,1 |
| Ecografia de abdômen total adulto | 9.912 | 532,1 | 328,1 |
| Doppler venoso MMII bilateral | 9.824 | 609,6 | 564,0 |
| Ecodoppler de carótidas | 4.537 | 139,6 | 131,1 |
| Ecografia do aparelho urinário | 3.914 | 630,9 | 459,1 |
| Ecografia de próstata via abdominal | 3.243 | 578,0 | 460,1 |
| Ecografia de tireoide adulto | 3.216 | 486,7 | 386,1 |
| Ultrassonografia de parede abdominal | 3.142 | 584,9 | 504,0 |
| Ecografia de partes moles | 2.992 | 663,1 | 547,1 |
| Ecografia de abdômen superior adulto | 2.276 | 684,3 | 579,5 |
| **objeto de ultrassonografia** | **67.836** | **565,1** | |

A maior espera média do conjunto é a da ecografia de abdômen superior adulto, com
**684 dias**; a menor é a do ecodoppler de carótidas, com **140 dias**. O conjunto da
ultrassonografia espera **565 dias** e o da tomografia, **141 dias**.

**A média está sempre acima da mediana** — a fila tem cauda longa. O ecodoppler de
carótidas é o oposto do conjunto: 140 dias contra 565, e nenhum registro com mais de
dois anos.

**A espera máxima não vai ao documento.** Seis dos onze procedimentos trazem máximos
acima de 5.800 dias, cerca de dezesseis anos, e a própria coleta adverte que pode ser
resíduo de base.

### A armadilha da medida, de novo

| recorte | solicitações | espera média |
|---|---|---|
| três status de fila | 67.836 | **565,1 dias** |
| todos os status | 112.507 | 945,1 dias |
| só as devolvidas | 44.671 | 1.502,7 dias |

## 4. Classificação de risco — todas as prioridades

| prioridade | solicitações | participação | espera média |
|---|---|---|---|
| Prioridade 1 | 1.376 | 2,03% | 108 dias |
| Prioridade 2 | 29.149 | 42,97% | 320 dias |
| Prioridade 3 | 25.751 | 37,96% | 788 dias |
| Prioridade 4 | 11.560 | 17,04% | 741 dias |

Nenhuma solicitação do objeto está sem classificação.

**A escada de espera não é monotônica** — a Prioridade 3 espera mais que a 4 no
agregado, e o inverso ocorre em sete dos onze procedimentos.

**Duas filas concentram 77% de toda a Prioridade 4** — transvaginal, com 49,6% do
próprio volume, e mama bilateral, com 26,0%. São as duas filas de rastreamento, e a
coleta levanta a hipótese de que a classificação 4 seja ausência de classificação na
origem, não baixa prioridade clínica.

**Por isso a classificação de risco não vai ao documento.** Publicar que 17% do objeto
é Prioridade 4 é entregar ao analista um argumento contra a urgência do convênio, com
base num dado que a própria fonte diz não saber ler.

## 4-A. Perfil etário

| recorte | valor |
|---|---|
| Faixa de concentração | 40 a 69 anos — 45.263 solicitações, **66,7%** do objeto |
| Pico por faixa decenal | 50 a 59 anos — 17.036 solicitações, 25,1% |
| Pico por idade simples | 51 anos — 1.751 solicitações |

## 5. Rateio entre os polos — o objeto inteiro

Calculado procedimento a procedimento: a distribuição territorial de cada um aplicada
ao quantitativo daquele procedimento na planilha do objeto, e somada.

| polo | Regiões de Saúde | participação | exames |
|---|---|---|---|
| Ceilândia | Oeste e Sudoeste | **40,56%** | 33.073 |
| Sobradinho | Norte, Leste e Central | **29,67%** | 24.196 |
| Gama | Sul e Centro-Sul | **29,77%** | 24.277 |
| **total** | | **100%** | **81.546** |

**Fora do território, 14,2% do universo** — bem menos que os 44,2% da tomografia,
porque a ultrassonografia quase não vem de URD nem de contratados.

O rateio da tomografia sozinha dava Gama em 21,18%. Com a ultrassonografia dentro,
**Gama empata com Sobradinho**.

## 6. Divergências contra a planilha do objeto

O painel de 15/09 e a planilha de 10/09 não batem exame a exame — a base é
reprocessada diariamente.

| procedimento | planilha | painel 15/09 | |
|---|---|---|---|
| Mama bilateral | 14.608 | 14.396 | −212 |
| Transvaginal | 10.481 | 10.383 | −98 |
| Abdômen total | 9.959 | 9.912 | −47 |
| Doppler MMII | 9.793 | 9.824 | +31 |
| Carótidas | 4.608 | 4.537 | −71 |
| Aparelho urinário | 3.921 | 3.914 | −7 |
| Tireoide | 3.195 | 3.216 | +21 |
| Próstata | 3.185 | 3.243 | +58 |
| Parede abdominal | 3.121 | 3.143 | +22 |
| Partes moles | 2.974 | 2.992 | +18 |
| Abdômen superior | 2.249 | 2.276 | +27 |

**Prevalece a planilha**, por decisão do usuário em 15/09/2026. O painel entra para
código, espera e rateio — não para quantidade.
