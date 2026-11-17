# A cobertura das filas de imagem fora do plano 4 — emenda de R$ 1.502.687,00

**Controle interno: tem valor em reais; não vai ao documento.**

| | |
|---|---|
| recurso | R$ 1.502.687,00, federal — a mesma emenda do redacao_05 (`estado.yaml`) |
| gestão e apoio | a decidir (trava F-08). Dois cenários: **sem apoio**, e **10%** (R$ 1.352.418,30 para exames), o teto que o usuário fixou para a mesma emenda no redacao_05 |
| fila | Mapa Social, recarga de 15/10/2026 19:32, coleta do agente `mapa-social` (`fontes/mapa_social_20261015.md`, 7/7). **Fila = solicitações (exames), não pessoas** |
| valor | `valor_unitario.md` (Anexo I da Portaria SAES/MS 4.282/2026, a regra do plano 4). Código fora do rol fica sem valor aqui |
| fora por decisão do usuário | ecocardiografia transtorácica e as filas de articulação (15/10/2026); todas as cintilografias (16/10/2026) — seção 0 |
| montado em | 16/10/2026, por `scripts/cobertura.py` |

Tudo abaixo é **CALCULADO**:
- **custo para zerar** = fila × valor de referência; **% do recurso** = custo ÷ R$ 1.502.687,00;
- **atende** = piso(recurso ÷ valor), limitado à fila; o percentual é truncado, e "zera" só quando
  atende a fila inteira;
- **meses para a rede zerar** = fila ÷ agendadas por mês em 2026 (jan–set ÷ 9). Mede o ritmo de
  agendamento de hoje sem contar os pedidos novos: quanto maior, menos a rede dá conta sozinha;
- **zerar** é zerar a fila medida em 15/10/2026. Pedido novo continua entrando.
- **\*** = parte das filas de um código, somada linha a linha: as pessoas podem contar duas vezes,
  a espera média é ponderada pela fila e a mediana não se calcula.

## 0. Fora por decisão do usuário

- 15/10/2026: "Retire Ecocardiografia transtorácica e todos os outros de articulações."
- 16/10/2026: "Retire todos de cintilografia." Sai a medicina nuclear inteira (02.08), inclusive o estudo renal dinâmico e o de fluxo sanguíneo cerebral, que também são cintilográficos. O PET-CT fica: é tomografia.

| código | procedimento | fila | pessoas | custo para zerar |
|---|---|---|---|---|
| 02.05.01.003-2 | Ecocardiografia transtoracica | 16.293 | 16.289 | R$ 2.609.161,02 |
| 02.05.02.006-2 * | US de articulação (as filas de articulação, mão, pé, quadril, tendão) | 10.256 | 10.249 | R$ 1.024.984,64 |
| 02.05.02.006-2 * | US de partes moles e outras regiões (o resto do código da articulação) | 4.225 | 4.224 | R$ 422.246,50 |
| 02.08.01.002-5 | Cintilografia de miocardio p/ avaliacao da perfusao em situacao de estresse (minimo 3 projecoes) | 1.825 | 1.825 | R$ 1.640.200,50 |
| 02.08.05.003-5 | Cintilografia de ossos com ou sem fluxo sanguíneo (corpo inteiro) | 1.688 | 1.688 | R$ 1.289.564,48 |
| 02.08.01.003-3 | Cintilografia de miocardio p/ avaliacao da perfusao em situacao de repouso (minimo 3 projecoes) | 1.505 | 1.505 | R$ 1.325.995,30 |
| 02.06.03.002-9 | Tomografia computadorizada de articulacoes de membro inferior | 241 | 206 | R$ 72.336,15 |
| 02.08.04.010-2 | Estudo renal dinamico c/ ou s/ diuretico | 222 | 222 | fora do rol |
| 02.08.03.001-8 | Cintilografia de paratireoides | 189 | 189 | R$ 184.014,18 |
| 02.08.04.005-6 | Cintilografia renal/renograma (qualitativa e/ou quantitativa) | 167 | 167 | R$ 88.864,04 |
| 02.07.01.002-1 | Ressonancia magnetica de articulacao temporo-mandibular (bilateral) | 127 | 125 | R$ 63.483,49 |
| 02.08.02.003-9 | Cintilografia de glandulas salivares c/ ou s/ estimulo | 122 | 122 | R$ 42.890,32 |
| 02.06.02.001-5 | Tomografia computadorizada de articulacoes de membro superior | 72 | 69 | R$ 21.610,80 |
| 02.04.06.008-7 | Radiografia de articulacao tibio-tarsica | 60 | 40 | fora do rol |
| 02.04.06.006-0 | Radiografia de articulacao coxo-femoral | 56 | 46 | fora do rol |
| 02.08.01.004-1 | Cintilografia de miocardio p/ localizacao de necrose (minimo 3 projecoes ) | 50 | 50 | R$ 33.294,00 |
| 02.08.02.007-1 | Cintilografia p/ estudo de transito gastrico | 34 | 30 | R$ 19.613,92 |
| 02.08.03.002-6 | Cintilografia de tireóide com ou sem captação | 33 | 33 | R$ 5.100,48 |
| 02.08.08.004-0 | Linfocintilografia | 21 | 21 | R$ 11.871,72 |
| 02.08.03.004-2 | Cintilografia p/ pesquisa do corpo inteiro | 10 | 10 | R$ 6.774,00 |
| 02.04.04.003-5 | Radiografia de articulacao escapulo-umeral | 10 | 10 | fora do rol |
| 02.08.05.004-3 | Cintilografia de segmento osseo c/ galio 67 | 10 | 10 | R$ 9.151,00 |
| 02.08.07.004-4 | Cintilografia de pulmao por perfusao (minimo 4 projecoes) | 8 | 8 | R$ 4.176,00 |
| 02.08.02.006-3 | Cintilografia p/ estudo de transito esofagico (semi-solido) | 5 | 5 | R$ 2.707,60 |
| 02.08.02.009-8 | Cintilografia p/ pesquisa de hemorragia digestiva ativa | 5 | 5 | R$ 3.144,60 |
| 02.08.06.003-0 | Estudo de fluxo sanguineo cerebral | 4 | 4 | fora do rol |
| 02.08.07.002-8 | Cintilografia de pulmão p/ pesquisa de aspiração | 3 | 3 | R$ 1.530,12 |
| 02.08.09.001-0 | Cintilografia de corpo inteiro c/ galio 67 p/ pesquisa de neoplasias | 3 | 3 | R$ 2.720,40 |
| 02.08.02.008-0 | Cintilografia p/ pesquisa de diverticulose de meckel | 3 | 3 | R$ 1.378,32 |
| 02.08.02.005-5 | Cintilografia p/ estudo de transito esofagico (liquido) | 3 | 3 | R$ 1.624,56 |
| 02.08.09.002-9 | Cintilografia de glandula lacrimal (dacriocintilografia) | 3 | 3 | R$ 596,07 |
| 02.04.04.002-7 | Radiografia de articulacao acromio-clavicular | 2 | 2 | fora do rol |
| 02.08.02.011-0 | Cintilografia p/ pesquisa de refluxo gastro-esofagico | 2 | 2 | R$ 1.083,04 |
| 02.04.06.007-9 | Radiografia de articulacao sacro-iliaca | 1 | 1 | fora do rol |
| 02.04.04.004-3 | Radiografia de articulacao esterno-clavicular | 1 | 1 | fora do rol |
| 02.04.01.005-5 | Radiografia de articulacao temporo-mandibular bilateral | 1 | 1 | fora do rol |

Fica, com nota: a **TC de face / seios da face / ATM** (02.06.01.004-4, 500 na fila), que é exame de face e seios e só cita a articulação temporo-mandibular no nome.

- 16/10/2026: "Tire partes moles." Sai o resto do código 02.05.02.006-2: partes moles e as outras regiões abaixo.

As filas do código 02.05.02.006-2 que saíram em 16/10/2026 (partes moles e outras regiões):

| fila no SISREG | fila | espera média |
|---|---|---|
| ECOGRAFIA  DE PARTES MOLES | 3.108 | 654 |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | 233 | 375 |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | 195 | 348 |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | 159 | 448 |
| ULTRASSONOGRAFIA DO PESCOCO | 155 | 513 |
| ULTRASSONOGRAFIA CERVICAL | 89 | 362 |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | 54 | 456 |
| USG BRACO ESQUERDO | 50 | 1167 |
| ECOGRAFIA PELVICA | 46 | 77 |
| USG BRACO DIREITO | 28 | 990 |
| USG PERNA ESQUERDA | 26 | 532 |
| USB AXILA DIREITA | 23 | 609 |
| ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | 17 | 409 |
| USG PERNA DIREITA | 16 | 559 |
| ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | 12 | 190 |
| USG ANTEBRACO ESQUERDO | 8 | 630 |
| ULTRASSONOGRAFIA DA BACIA | 4 | 595 |
| USG ESTRUTURA SUPERFICIE | 2 | 14 |

## 1. As filas candidatas, código a código (fila de 100 ou mais)

| modalidade | código | procedimento | fila | pessoas | espera média / mediana (dias) | agendadas/mês 2026 | meses para a rede zerar | valor ref. | custo para zerar | % do recurso | sem apoio | com 10% de apoio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| radiologia | 02.04.03.018-8 | Mamografia bilateral para rastreamento | 6.461 | 6.458 | 49 / 28 | 4.682 | 1,4 | R$ 99,90 | R$ 645.453,90 | 43% | zera | zera |
| radiologia | 02.04.06.002-8 | Densitometria ossea duo-energetica de coluna (vertebras lombares e/ou femur) | 2.196 | 2.196 | 44 / 35 | 980 | 2,2 | R$ 220,40 | R$ 483.998,40 | 32% | zera | zera |
| radiologia | 02.04.01.017-9 | Radiografia panoramica | 1.653 | 1.638 | 100 / 31 | 1.397 | 1,2 | fora do rol | | | | |
| ressonância | 02.07.03.002-2 | Ressonancia magnetica de bacia / pelve / abdomen inferior | 1.625 | 1.616 | 24 / 22 | 1.622 | 1,0 | R$ 499,87 | R$ 812.288,75 | 54% | zera | zera |
| ressonância | 02.07.03.003-0 | Ressonancia magnetica de membro inferior (unilateral) | 1.491 | 1.142 | 19 / 17 | 1.407 | 1,1 | R$ 499,87 | R$ 745.306,17 | 50% | zera | zera |
| tomografia | 02.06.01.007-9 | Tomografia computadorizada do cranio | 1.467 | 1.440 | 197 / 120 | 1.285 | 1,1 | R$ 300,11 | R$ 440.261,37 | 29% | zera | zera |
| ressonância | 02.07.01.006-4 | Ressonancia magnetica de cranio | 1.417 | 1.391 | 30 / 21 | 1.502 | 0,9 | R$ 499,87 | R$ 708.315,79 | 47% | zera | zera |
| ressonância | 02.07.01.004-8 | Ressonancia magnetica de coluna lombo-sacra | 1.412 | 1.409 | 19 / 17 | 1.537 | 0,9 | R$ 499,87 | R$ 705.816,44 | 47% | zera | zera |
| ultrassonografia | 02.05.02.008-9 | Ultrassonografia de globo ocular / orbita (monocular) | 1.272 | 1.272 | 264 / 266 | 58 | 22,1 | R$ 99,94 | R$ 127.123,68 | 8% | zera | zera |
| ressonância | 02.07.02.002-7 | Ressonancia magnetica de membro superior (unilateral) | 1.140 | 869 | 19 / 17 | 1.002 | 1,1 | R$ 499,87 | R$ 569.851,80 | 38% | zera | zera |
| ultrassonografia | 02.05.02.016-0 | Ultrassonografia pelvica (ginecologica) | 1.003 | 994 | 603 / 380 | 111 | 9,0 | R$ 99,94 | R$ 100.239,82 | 7% | zera | zera |
| ultrassonografia | 02.05.02.007-0 | Ultrassonografia de bolsa escrotal | 995 | 994 | 588 / 471 | 72 | 13,9 | R$ 99,94 | R$ 99.440,30 | 7% | zera | zera |
| ressonância | 02.07.01.003-0 | Ressonancia magnetica de coluna cervical/pescoço | 758 | 742 | 20 / 17 | 788 | 1,0 | R$ 499,87 | R$ 378.901,46 | 25% | zera | zera |
| tomografia | 02.06.01.005-2 | Tomografia computadorizada do pescoco | 755 | 746 | 139 / 115 | 209 | 3,6 | R$ 300,15 | R$ 226.613,25 | 15% | zera | zera |
| ressonância | 02.07.03.001-4 | Ressonancia magnetica de abdomen superior | 752 | 749 | 25 / 23 | 921 | 0,8 | R$ 499,87 | R$ 375.902,24 | 25% | zera | zera |
| radiologia | 02.04.01.018-7 | Radiografia peri-apical interproximal (bite-wing) | 706 | 706 | 24 / 21 | 769 | 0,9 | fora do rol | | | | |
| radiologia | 02.04.03.015-3 | Radiografia de torax (pa e perfil) | 662 | 662 | 95 / 94 | 1.099 | 0,6 | fora do rol | | | | |
| tomografia | 02.06.01.004-4 | Tomografia computadorizada de face / seios da face / articulacoes temporo-mandibulares | 500 | 488 | 124 / 90 | 497 | 1,0 | R$ 300,15 | R$ 150.075,00 | 10% | zera | zera |
| ultrassonografia | 02.05.02.014-3 | Ultrassonografia obstetrica | 464 | 464 | 144 / 57 | 270 | 1,7 | R$ 99,94 | R$ 46.372,16 | 3% | zera | zera |
| tomografia | 02.06.01.009-5 | Tomografia por emissão de pósitrons (pet-ct) | 424 | 424 | 162 / 128 | 42 | 10,0 | fora do rol | | | | |
| radiologia | 02.04.06.012-5 | Radiografia de joelho (ap + lateral) | 298 | 209 | 81 / 69 | 245 | 1,2 | fora do rol | | | | |
| radiologia | 02.04.04.009-4 | Radiografia de mao | 288 | 179 | 82 / 66 | 202 | 1,4 | fora do rol | | | | |
| ressonância | 02.07.01.001-3 | Angioressonancia cerebral | 287 | 220 | 39 / 42 | 224 | 1,3 | R$ 499,87 | R$ 143.462,69 | 10% | zera | zera |
| ultrassonografia | 02.05.02.017-8 | Ultrassonografia transfontanela | 281 | 281 | 282 / 213 | 74 | 3,8 | R$ 99,94 | R$ 28.083,14 | 2% | zera | zera |
| radiologia | 02.04.02.006-9 | Radiografia de coluna lombo-sacra | 281 | 258 | 105 / 101 | 308 | 0,9 | fora do rol | | | | |
| ressonância | 02.07.01.005-6 | Ressonancia magnetica de coluna toracica | 266 | 265 | 20 / 17 | 380 | 0,7 | R$ 499,87 | R$ 132.965,42 | 9% | zera | zera |
| ressonância | 02.07.02.001-9 | Ressonancia magnetica de coracao / aorta c/ cine | 258 | 255 | 63 / 58 | 157 | 1,6 | R$ 498,52 | R$ 128.618,16 | 9% | zera | zera |
| radiologia | 02.04.06.015-0 | Radiografia de pe / dedos do pe | 250 | 183 | 80 / 56 | 119 | 2,1 | fora do rol | | | | |
| ultrassonografia | 02.05.02.015-1 | Ultrassonografia obstetrica c/ doppler colorido e pulsado | 205 | 205 | 177 / 141 | 32 | 6,3 | R$ 100,18 | R$ 20.536,90 | 1% | zera | zera |
| tomografia | 02.06.02.002-3 | Tomografia computadorizada de segmentos apendiculares - (braco, antebraço, mão, coxa, perna, pé) | 195 | 157 | 217 / 146 | 200 | 1,0 | R$ 300,15 | R$ 58.529,25 | 4% | zera | zera |
| tomografia | 02.06.01.002-8 | Tomografia computadorizada de coluna lombo-sacra c/ ou s/ contraste | 166 | 164 | 221 / 136 | 285 | 0,6 | R$ 300,26 | R$ 49.843,16 | 3% | zera | zera |
| ultrassonografia | 02.05.02.002-0 | Paquimetria ultrassônica | 164 | 164 | 22 / 19 | 167 | 1,0 | fora do rol | | | | |
| radiologia | 02.04.04.010-8 | Radiografia de mao e punho (p/ determinacao de idade ossea) | 150 | 144 | 94 / 81 | 178 | 0,8 | fora do rol | | | | |
| radiologia | 02.04.01.006-3 | Radiografia de cavum (lateral + hirtz) | 141 | 140 | 99 / 93 | 206 | 0,7 | fora do rol | | | | |
| tomografia | 02.06.01.001-0 | Tomografia computadorizada de coluna cervical c/ ou s/ contraste | 140 | 138 | 179 / 118 | 130 | 1,1 | R$ 300,18 | R$ 42.025,20 | 3% | zera | zera |
| radiologia | 02.04.02.003-4 | Radiografia de coluna cervical (ap + lateral + to + obliquas) | 136 | 136 | 105 / 91 | 118 | 1,2 | fora do rol | | | | |
| ressonância | 02.07.01.007-2 | Ressonancia magnetica de sela turcica | 136 | 136 | 39 / 23 | 129 | 1,1 | R$ 499,87 | R$ 67.982,32 | 5% | zera | zera |
| radiologia | 02.04.04.012-4 | Radiografia de punho (ap + lateral + obliqua) | 131 | 88 | 93 / 86 | 88 | 1,5 | fora do rol | | | | |
| radiologia | 02.04.06.013-3 | Radiografia de joelho ou patela (ap + lateral + axial) | 126 | 98 | 62 / 65 | 124 | 1,0 | fora do rol | | | | |
| radiologia | 02.04.02.009-3 | Radiografia de coluna toracica (ap + lateral) | 122 | 117 | 109 / 99 | 95 | 1,3 | fora do rol | | | | |

Mais 46 códigos com menos de 100 na fila (1.241 no total), na planilha da coleta.

## 1a. A ressonância, código a código (todas as filas)

| código | procedimento | fila | pessoas | espera média / mediana (dias) | agendadas/mês 2026 | meses para a rede zerar | custo para zerar |
|---|---|---|---|---|---|---|---|
| 02.07.03.002-2 | Ressonancia magnetica de bacia / pelve / abdomen inferior | 1.625 | 1.616 | 24 / 22 | 1.622 | 1,0 | R$ 812.288,75 |
| 02.07.03.003-0 | Ressonancia magnetica de membro inferior (unilateral) | 1.491 | 1.142 | 19 / 17 | 1.407 | 1,1 | R$ 745.306,17 |
| 02.07.01.006-4 | Ressonancia magnetica de cranio | 1.417 | 1.391 | 30 / 21 | 1.502 | 0,9 | R$ 708.315,79 |
| 02.07.01.004-8 | Ressonancia magnetica de coluna lombo-sacra | 1.412 | 1.409 | 19 / 17 | 1.537 | 0,9 | R$ 705.816,44 |
| 02.07.02.002-7 | Ressonancia magnetica de membro superior (unilateral) | 1.140 | 869 | 19 / 17 | 1.002 | 1,1 | R$ 569.851,80 |
| 02.07.01.003-0 | Ressonancia magnetica de coluna cervical/pescoço | 758 | 742 | 20 / 17 | 788 | 1,0 | R$ 378.901,46 |
| 02.07.03.001-4 | Ressonancia magnetica de abdomen superior | 752 | 749 | 25 / 23 | 921 | 0,8 | R$ 375.902,24 |
| 02.07.01.001-3 | Angioressonancia cerebral | 287 | 220 | 39 / 42 | 224 | 1,3 | R$ 143.462,69 |
| 02.07.01.005-6 | Ressonancia magnetica de coluna toracica | 266 | 265 | 20 / 17 | 380 | 0,7 | R$ 132.965,42 |
| 02.07.02.001-9 | Ressonancia magnetica de coracao / aorta c/ cine | 258 | 255 | 63 / 58 | 157 | 1,6 | R$ 128.618,16 |
| 02.07.01.007-2 | Ressonancia magnetica de sela turcica | 136 | 136 | 39 / 23 | 129 | 1,1 | R$ 67.982,32 |
| 02.07.03.004-9 | Ressonancia magnetica de vias biliares/colangiorressonancia | 92 | 91 | 22 / 22 | 286 | 0,3 | R$ 45.988,04 |
| 02.07.02.006-0 | Ressonância magnética da mama | 84 | 84 | 21 / 17 | 162 | 0,5 | R$ 41.989,08 |
| 02.07.02.003-5 | Ressonancia magnetica de torax | 80 | 80 | 21 / 20 | 97 | 0,8 | R$ 39.989,60 |
| **ressonância, soma das linhas** | 14 códigos | **9.798** | | 24 (ponderada) | 10.213 | 1,0 | **R$ 4.897.377,96** |

- sem apoio: o recurso compra 3.006 ressonâncias a R$ 499,87, 30% da fila de ressonância.
- com 10% de apoio: 2.705 ressonâncias, 27% da fila.

A ressonância de ATM (02.07.01.002-1, 127 na fila) saiu com as articulações (seção 0).

## 2. Mesmo código do plano 4, sem resíduo

| código | procedimento | fila | pessoas | espera média / mediana | valor ref. | custo para zerar |
|---|---|---|---|---|---|---|
| 02.05.01.004-0 | Ultrassonografia doppler colorido de vasos | 2.406 | 2.370 | 413 / 322 | R$ 100,18 | R$ 241.033,08 |
| 02.06.03.001-0 | Tomografia computadorizada de abdomen superior | 2.062 | 1.897 | 270 / 216 | R$ 299,44 | R$ 617.445,28 |
| 02.06.02.003-1 | Tomografia computadorizada de torax | 1.901 | 1.813 | 284 / 227 | R$ 300,10 | R$ 570.490,10 |
| 02.06.03.003-7 | Tomografia computadorizada de pelve / bacia / abdomen inferior | 1.409 | 1.310 | 306 / 281 | R$ 299,44 | R$ 421.910,96 |
| 02.05.02.012-7 | Ultrassonografia de tireoide | 869 | 869 | 441 / 366 | R$ 99,94 | R$ 86.847,86 |
| 02.05.02.004-6 | Ultrassonografia de abdomen total | 451 | 451 | 591 / 360 | R$ 100,18 | R$ 45.181,18 |
| 02.05.02.005-4 | Ultrassonografia de aparelho urinário | 385 | 384 | 497 / 323 | R$ 99,94 | R$ 38.476,90 |
| 02.05.02.003-8 | Ultrassonografia de abdômen superior | 19 | 19 | 512 / 197 | R$ 99,94 | R$ 1.898,86 |
| **total** | 57 filas | **9.502** | 7.176 | 355 / 269 | | **R$ 2.023.284,22** |

## 3. Combinações (cada fila na ordem; quando uma zera, passa-se à próxima)

Os cinco ultrassons de espera longa (pélvica, bolsa escrotal, globo ocular, transfontanela, obstétrica com doppler) custam R$ 375.423,84 para zerar, 25% do recurso. Toda combinação começa por eles; o que muda é onde vai o resto.

| combinação | cenário | o que atende | filas zeradas | exames | sobra |
|---|---|---|---|---|---|
| A. Ultrassom de espera longa, o resto em tomografia: TC de pescoço → TC de crânio → TC de face/seios | sem apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; TC de pescoço: zera; TC de crânio: zera; TC de face/seios: zera | 8 | 6.478 | R$ 310.313,54 |
| A. Ultrassom de espera longa, o resto em tomografia: TC de pescoço → TC de crânio → TC de face/seios | com 10% de apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; TC de pescoço: zera; TC de crânio: zera; TC de face/seios: zera | 8 | 6.478 | R$ 160.044,84 |
| B. Ultrassom de espera longa, o resto em mamografia → densitometria | sem apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; mamografia: zera; densitometria: 2.186 de 2.196 (99%) | 6 | 12.403 | R$ 14,86 |
| B. Ultrassom de espera longa, o resto em mamografia → densitometria | com 10% de apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; mamografia: zera; densitometria: 1.504 de 2.196 (68%) | 6 | 11.721 | R$ 58,96 |
| C. Ultrassom de espera longa, o resto em ressonância: RM de crânio → RM de coluna lombo-sacra | sem apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; RM de crânio: zera; RM de coluna lombo-sacra: 838 de 1.412 (59%) | 6 | 6.011 | R$ 56,31 |
| C. Ultrassom de espera longa, o resto em ressonância: RM de crânio → RM de coluna lombo-sacra | com 10% de apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; RM de crânio: zera; RM de coluna lombo-sacra: 537 de 1.412 (38%) | 6 | 5.710 | R$ 248,48 |
| D. Só ultrassom: os de espera longa e os do mesmo código do plano 4 fora das filas dele, o resto em TC de pescoço → TC de crânio | sem apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; US doppler (mesmo código do plano 4): zera; US de tireoide (mesmo código do plano 4): zera; US de abdômen total (mesmo código do plano 4): zera; US de aparelho urinário (mesmo código do plano 4): zera; US de abdômen superior (mesmo código do plano 4): zera; TC de pescoço: zera; TC de crânio: zera | 12 | 10.108 | R$ 46.950,66 |
| D. Só ultrassom: os de espera longa e os do mesmo código do plano 4 fora das filas dele, o resto em TC de pescoço → TC de crânio | com 10% de apoio | US pélvica: zera; US de bolsa escrotal: zera; US de globo ocular: zera; US transfontanela: zera; US obstétrica com doppler: zera; US doppler (mesmo código do plano 4): zera; US de tireoide (mesmo código do plano 4): zera; US de abdômen total (mesmo código do plano 4): zera; US de aparelho urinário (mesmo código do plano 4): zera; US de abdômen superior (mesmo código do plano 4): zera; TC de pescoço: zera; TC de crânio: 1.122 de 1.467 (76%) | 11 | 9.763 | R$ 219,91 |

Na D, as filas do mesmo código do plano 4 trazem o risco de sobreposição: são os procedimentos que o plano 4 já paga ao ISHP.

## 4. A combinação escolhida — mamografia primeiro, depois a combinação A, com o preço de mercado

Escolhas do usuário em 16/10/2026 (`estado.yaml`). Mercado do DF e cobertura de `precos.md` (16/10/2026); "valor ÷ mediana" é CALCULADO aqui.

| ordem | exame | fila | espera média | a rede zera em | valor | custo para zerar | mercado DF: mínimo / mediana (preços) | cobertura | valor ÷ mediana |
|---|---|---|---|---|---|---|---|---|---|
| 1 | mamografia | 6.461 | 49 dias | 1 mês | R$ 99,90 | R$ 645.453,90 | a pesquisar | | |
| 2 | US pélvica | 1.003 | 603 dias | 9 meses | R$ 99,94 | R$ 100.239,82 | R$ 80,00 / R$ 104,00 (7) | 125% | 96% |
| 3 | US de bolsa escrotal | 995 | 588 dias | 14 meses | R$ 99,94 | R$ 99.440,30 | R$ 90,00 / R$ 120,00 (11) | 111% | 83% |
| 4 | US de globo ocular | 1.272 | 264 dias | 22 meses | R$ 99,94 | R$ 127.123,68 | R$ 73,00 / R$ 261,50 (2) | 137% | 38% |
| 5 | US transfontanela | 281 | 282 dias | 4 meses | R$ 99,94 | R$ 28.083,14 | R$ 90,00 / R$ 104,00 (5) | 111% | 96% |
| 6 | US obstétrica com doppler | 205 | 177 dias | 6 meses | R$ 100,18 | R$ 20.536,90 | R$ 156,00 / R$ 237,00 (4) | 64% | 42% |
| 7 | TC de pescoço | 755 | 139 dias | 4 meses | R$ 300,15 | R$ 226.613,25 | R$ 245,00 / R$ 522,50 (2) | 123% | 57% |
| 8 | TC de crânio | 1.467 | 197 dias | 1 mês | R$ 300,11 | R$ 440.261,37 | R$ 245,00 / R$ 522,50 (2) | 122% | 57% |
| 9 | TC de face/seios | 500 | 124 dias | 1 mês | R$ 300,15 | R$ 150.075,00 | R$ 245,00 / R$ 450,00 (3) | 123% | 67% |

A mamografia vem primeiro e custa R$ 645.453,90 para zerar (43% do recurso). O resto segue a ordem da combinação A: os cinco ultrassons, depois TC de pescoço, de crânio e de face/seios. As outras variantes ficam como registro.

| variante | cenário | filas zeradas | exames | onde para | sobra |
|---|---|---|---|---|---|
| **a escolhida: mamografia primeiro, depois a A** | sem apoio | 7 | 11.822 | TC de crânio: 850 de 1.467 (57%) | R$ 102,51 |
| **a escolhida: mamografia primeiro, depois a A** | com 10% de apoio | 7 | 11.321 | TC de crânio: 349 de 1.467 (23%) | R$ 188,92 |
| A3. A → mamografia | sem apoio | 8 | 9.584 | mamografia: 3.106 de 6.461 (48%) | R$ 24,14 |
| A3. A → mamografia | com 10% de apoio | 8 | 8.080 | mamografia: 1.602 de 6.461 (24%) | R$ 5,04 |
| A, sem a sobra | sem apoio | 8 | 6.478 | TC de face/seios: zera | R$ 310.313,54 |
| A, sem a sobra | com 10% de apoio | 8 | 6.478 | TC de face/seios: zera | R$ 160.044,84 |
| A1. A + as outras tomografias (segmentos apendiculares, colunas, sela túrcica) → US obstétrica → mamografia | sem apoio | 14 | 8.339 | mamografia: 776 de 6.461 (12%) | R$ 2,92 |
| A1. A + as outras tomografias (segmentos apendiculares, colunas, sela túrcica) → US obstétrica → mamografia | com 10% de apoio | 11 | 7.011 | Tomografia computadorizada de coluna cervical c/ ou s/ contraste: 97 de 140 (69%) | R$ 41,47 |
| A2. A + os ultrassons do mesmo código do plano 4, fora das filas dele (doppler → tireoide → abdômen total → aparelho urinário) | sem apoio | 9 | 9.577 | US de tireoide (mesmo código do plano 4): 693 de 869 (79%) | R$ 22,04 |
| A2. A + os ultrassons do mesmo código do plano 4, fora das filas dele (doppler → tireoide → abdômen total → aparelho urinário) | com 10% de apoio | 8 | 8.075 | US doppler (mesmo código do plano 4): 1.597 de 2.406 (66%) | R$ 57,38 |

Na A2, as filas do mesmo código do plano 4 trazem o risco de sobreposição. As filas das variantes, fora da A, ainda não têm ficha nem preço.
