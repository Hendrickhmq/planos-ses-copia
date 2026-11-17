# Plano 4 com mais TC, só ambulatório — e a queda da mama e da transvaginal

**Controle interno, 01/11/2026.** Este estudo compara duas versões de ajuste do plano 4 (v26,
assinado) à Tabela SUS Candanga, sem nenhuma fila de emergência (D-009) e sem sobreposição
com o IEV e o redacao_07 (L-008). O alvo é o valor dos exames da v26, **R$ 10.636.542,52**,
sem o apoio.

As filas são as da coleta do Mapa Social de 29/10/2026 (`registros/mapa_social/imagem/`). A
conta está em `plano4_mais_tc_ambulatorio_20261101.py`, nesta pasta (roda com `python3 output/plano4_mais_tc_ambulatorio_20261101.py <tabela_sus_candanga.csv>` a partir da raiz).

## 1. Mama e transvaginal: o que fez a fila cair

São os agendamentos por mês (a oferta da rede), com os pedidos que entram e o que aconteceu
com os agendados. Outubro de 2026 vai só até o dia 29. Novembro mostra só o que já estava
agendado em 29/10.

**Ultrassonografia mamária (02.05.02.009-7)**

| mês | pedidos novos | agendamentos | realizados | faltas |
|---|---:|---:|---:|---:|
| out/2024 (Outubro Rosa) | 896 | 329 | 175 | 64 |
| out/2025 (Outubro Rosa) | 941 | 577 | 252 | 118 |
| média de jan a jun/2026 | 961 | 489 | 231 | 93 |
| jul/2026 | 1.058 | 778 | 439 | 173 |
| ago/2026 | 971 | **1.733** | 827 | **609** |
| set/2026 | 926 | **2.821** | 926 | **927** |
| out/2026 (até 29) | 888 | 1.308 | 213 | 217 |
| nov/2026 (já agendado) | — | 756 | — | — |

**Ultrassonografia transvaginal (02.05.02.018-6)**

| mês | pedidos novos | agendamentos | realizados | faltas |
|---|---:|---:|---:|---:|
| média de 2025 | 1.152 | 990 | 441 | 276 |
| média de jan a mai/2026 | 1.310 | 1.189 | 509 | 368 |
| jun/2026 | 1.231 | 1.655 | 741 | 594 |
| jul/2026 | 1.458 | **2.120** | 977 | **845** |
| ago/2026 | 1.480 | 1.861 | 866 | 700 |
| set/2026 | 1.295 | **2.210** | 865 | **755** |
| out/2026 (até 29) | 1.150 | 1.537 | 335 | 279 |
| nov/2026 (já agendado) | — | 678 | — | — |

**O que os números mostram:**

- **Mama: um mutirão, e não o padrão de outros outubros.**
  - A oferta saltou em agosto e teve o pico em setembro, cinco a seis vezes o normal. Começou
    antes de outubro.
  - Nos Outubros Rosa anteriores, a oferta pouco mudou: nada em 2024 e cerca de +35% em 2025.
  - A sua leitura de campanha se sustenta. Foi uma campanha concentrada que começou antes do
    Outubro Rosa e já está diminuindo: novembro tem 756 agendados.
- **Transvaginal: um esforço mais longo.**
  - A oferta subiu de junho a setembro, para cerca de 2.000 por mês, contra cerca de 1.200 no
    começo do ano.
  - Pode ser campanha ou capacidade nova. Os dados por código não dizem qual.
- **Um terço dos chamados faltou** nos meses de pico. Na mama de setembro foram 927 faltas para
  926 realizados.
  - Parte da queda da fila não é exame feito: é pedido que saiu por falta. Essas pacientes
    podem voltar como pedido novo.
- **Os pedidos novos não mudaram:** cerca de 900 por mês na mama e de 1.150 a 1.450 na
  transvaginal.

**O que isso quer dizer para o plano:**
- **Se o esforço parar,** a fila volta a crescer:
  - na mama, uns 450 por mês (900 entram e a oferta normal é de 450);
  - na transvaginal, uns 120 por mês (1.310 entram e a oferta do começo do ano era de 1.190).
- **Se continuar no ritmo de setembro,** as duas filas se esgotam antes ou durante a execução.
- **O dado que decide é quem fez o mutirão.** Se foi uma unidade nova ou contratada, a oferta
  tende a ficar. Se foram as unidades de sempre em regime de campanha, ela tende a voltar.

**Como saber:**
1. **Perguntar à regulação da SES** se houve mutirão ou campanha de mama e de ginecologia
   (julho a outubro de 2026) e se a oferta extra continua em 2027.
2. **Medir os agendamentos por unidade executante e por mês.** O kit do Mapa Social ainda não
   tem essa dimensão (`ferramentas/mapa_social/motor.js`). Acrescentá-la é uma mudança no
   padrão e depende do seu sim.
3. **Recoletar em meados de dezembro,** para ver se novembro e dezembro voltaram ao normal.

### Quem fez o esforço (coleta por unidade executante, 01/11/2026)

O agente `mapa-social` mediu a oferta dos dois códigos por unidade e por mês, numa base
recarregada em 01/11/2026, às 14h31. A conferência passou em 9 de 9. Os arquivos estão em
`planos/redacao_04/dados/fontes/mapa_social_20261101_executante.*`.

**Mama: mutirões em hospitais da SES, já encerrados quase todos.**

| unidade | antes (média por mês) | ago | set | out | nov (já agendado) |
|---|---:|---:|---:|---:|---:|
| HRS (Sobradinho) | 0 | 1.012 | 1.186 | 17 | 0 |
| FHB (serviços centralizados) | 0 | 0 | 718 | 276 | 0 |
| HRAN | 27 | 136 | 200 | 0 | 0 |
| HRPl (Planaltina) | 28 | 23 | 231 | 81 | 2 |
| HRL (Leste) | 46 | 65 | 65 | 313 | **578** |
| as demais | 410 | 497 | 421 | 621 | 176 |
| **total** | **511** | **1.733** | **2.821** | **1.308** | **756** |

**Transvaginal: mutirões em sequência, mais uma unidade nova.**

| unidade | antes (média por mês) | jun | jul | ago | set | out | nov (já agendado) |
|---|---:|---:|---:|---:|---:|---:|---:|
| HRG (Gama) | 19 | 715 | 1.095 | 480 | 9 | 10 | 0 |
| HRAN | 133 | 50 | 90 | 725 | 640 | 96 | 0 |
| HRS, HRPl e FHB | 208 | 129 | 131 | 158 | 1.010 | 264 | 24 |
| Policlínica Ceilândia II | 0 | 243 | 400 | 0 | 58 | 404 | 106 |
| HRL (Leste) | 36 | 38 | 53 | 36 | 59 | 139 | 439 |
| as demais | 871 | 480 | 351 | 462 | 434 | 626 | 109 |
| **total** | **1.267** | **1.655** | **2.120** | **1.861** | **2.210** | **1.539** | **678** |

- **Nenhum contratado ou credenciado aparece.** Todo o esforço foi da rede própria: hospitais
  regionais, URD e serviços centralizados.
- **Na mama, o pico de agosto e setembro foi do HRS, e o de setembro e outubro, da FHB.** Os dois
  partiram de zero e voltaram a zero. Tem a cara de campanha, começando antes do Outubro Rosa. O
  único esforço que segue em novembro é o do HRL (578 já agendados).
- **Na transvaginal, os mutirões vieram em ondas:** o HRG de junho a agosto, o HRAN em agosto e
  setembro, e o HRS, o HRPl e a FHB em setembro. Também há perdas na base. O HRT, que fazia
  cerca de 180 por mês, quase parou desde abril, e o HRC caiu de 240 para menos de 100. A
  Policlínica Ceilândia II é a única oferta nova (desde junho de 2026, irregular).
- **O que vem pela frente:**
  - **Mama:** sem os mutirões, a oferta volta a cerca de 500 por mês, contra 913 pedidos novos
    por mês. A fila (12.952 em 01/11) volta a crescer uns 400 por mês e passa a meta da v26
    (14.689) em quatro a cinco meses.
  - **Transvaginal:** entram 1.260 pedidos por mês, e a base perdeu o HRT. A fila (9.295) tende a
    ficar estável ou a crescer pouco, e não chega à meta da v26 (10.541) tão cedo.

## 2. As duas versões, sem emergência

O ponto de partida é o mesmo nas duas. A v26 tem 79.144 exames e pela Candanga vale
R$ 10.390.824,04. Sem a TC de tórax de emergência (728 exames, R$ 225.134,00), ficam
**78.416 exames e R$ 10.165.690,04**. Faltam **R$ 470.852,48** para chegar ao valor de antes.

### Versão pura: o plano assinado como está, e a diferença vira TC

- **Cada meta continua a mesma da v26.** Só o preço muda.
- **A diferença compra 1.522 TC ambulatoriais.** Elas vêm de filas dos mesmos três códigos que
  hoje estão fora do plano: angiotomografias de aorta, tórax, abdômen, pelve, carótidas,
  renais e porta (1.795 pedidos) e TC eletiva sem contraste (283).
- **Resultado:** 79.938 exames e R$ 10.636.368,54.
- **A favor:** é a menor mudança no texto. Mudam os preços, a TC e os totais, e o mix que a
  SES aprovou continua.
- **Contra:** **5.864 exames da meta não estão na fila de hoje.** Eles teriam de vir de pedidos
  novos durante a execução:

| fila | meta da v26 | fila hoje | acima da fila |
|---|---:|---:|---:|
| Mama | 14.689 | 12.941 | 1.748 |
| Transvaginal | 10.541 | 9.286 | 1.255 |
| Doppler de carótidas | 4.674 | 4.137 | 537 |
| Aparelho urinário | 3.944 | 3.671 | 273 |
| Próstata | 3.201 | 2.967 | 234 |
| Tireoide | 3.216 | 2.985 | 231 |
| Abdômen total | 10.028 | 9.887 | 141 |
| Abdômen superior | 2.261 | 2.206 | 55 |
| TC de tórax com contraste | 3.104 | 2.343 | 761 |
| TC de abdômen com contraste | 4.516 | 4.113 | 403 |
| TC de pelve com contraste | 3.862 | 3.636 | 226 |
| **total** | | | **5.864** |

Mais da metade está na mama e na transvaginal, justamente as filas que a SES está atendendo
acima do normal.

### Versão ajustada: nenhuma meta acima da fila de hoje

- **Cada fila do plano fica limitada ao que existe hoje.** Ficam 72.552 exames e
  R$ 9.365.548,98. Faltam **R$ 1.270.993,54**.
- **A falta se cobre nesta ordem,** sempre com filas ambulatoriais e sem sobreposição:

| camada | o que entra | exames | valor | acumulado |
|---|---|---:|---:|---:|
| 1. TC | toda a TC ambulatorial livre nos três códigos (angiotomografias e TC eletiva sem contraste) e 123 angiotomografias de coronárias além da meta | 2.236 | R$ 691.483,00 | R$ 10.057.031,98 |
| 2. US das mesmas filas | o que a fila de hoje tem a mais que a meta (Doppler venoso +209, parede +164) e as mesmas US em criança (abdômen, urinário, tireoide) e a renal | 1.252 | R$ 133.751,48 | R$ 10.190.783,46 |
| 3. Doppler do mesmo código | Doppler arterial de membros inferiores (1.800), de membros superiores, de carótidas e vertebrais, de artérias renais, e o Doppler de tireoide | 3.088 | R$ 315.565,52 | R$ 10.506.348,98 |
| 4. Articulação | US de articulação sem os CID da OCI do IEV (de cerca de 9.197 pedidos) | 1.834 | R$ 130.158,98 | **R$ 10.636.507,96** |

- **Resultado:** 80.962 exames e R$ 10.636.507,96.
- **A favor:** nenhum exame é prometido sem pedido na fila.
- **Contra:** **a TC sozinha não fecha.** Sem emergência, ela cobre R$ 691 mil dos R$ 1,27 mi. O
  resto precisa de exames que não estavam no plano assinado:
  - Doppler arterial;
  - Doppler de membros superiores;
  - Doppler de tireoide;
  - US infantis;
  - um pouco de articulação, que é código novo no plano.
  
  O texto muda mais, e a SES precisa aceitar o mix novo.

### Lado a lado

| | pura | ajustada |
|---|---:|---:|
| exames | 79.938 | 80.962 |
| valor | R$ 10.636.368,54 | R$ 10.636.507,96 |
| TC | 14.412 | 13.736 |
| exames prometidos acima da fila de hoje | 5.864 | 0 |
| exames de filas que não estavam no plano assinado | 1.522 (só TC) | 7.914 (TC, Doppler, infantis, articulação) |
| emergência | nenhuma | nenhuma |
| sobreposição (L-008) | só o filtro de CID na TC de pelve | o filtro na TC de pelve e na articulação |

**A decisão depende da seção 1:**
- Se o mutirão de mama e transvaginal acabou, as filas voltam a crescer e a pura fica de pé
  com os pedidos novos.
- Se a oferta extra ficou, a pura promete o que não vai existir, e a ajustada é a segura.
- Há um meio-termo: a pura com as metas de mama e transvaginal limitadas à fila de hoje. Os
  R$ 229 mil que saem desses dois vão para TC (741). Com as 1.522, são 2.263 TC novas,
  praticamente toda a TC ambulatorial livre (2.236). As 27 que faltam saem do Doppler venoso
  que a fila tem a mais (+209).

**O que a coleta por unidade executante decidiu: a pura, com a transvaginal limitada.**
- **Mama:** os mutirões acabaram, e a fila volta a passar da meta da v26 em quatro a cinco
  meses. A meta de 14.689 fica.
- **Transvaginal:** a fila não deve voltar aos 10.541 tão cedo. A meta cai para a fila de
  hoje, 9.286 (−1.255 exames, −R$ 105.131,35).
- **A diferença vira TC:** faltam R$ 575.983,83, que compram **1.862 TC** ambulatoriais. Elas
  cabem nas 2.236 livres (angiotomografias e TC eletiva sem contraste).
- **Resultado:** **79.023 exames e R$ 10.636.382,19.**
  - O mix do plano assinado continua: muda só a quantidade de transvaginal, e entram as TC.
  - Ainda ficam acima da fila de hoje 4.609 exames. A mama (1.748) volta pela fila; os outros
    (carótidas 537, TC 1.390 e as demais US, 934) dependem dos pedidos novos. No ultrassom eles
    estão estáveis ou crescendo (o Doppler, uns 260 por mês). Na TC de tórax, a SES vem
    atendendo acima do que entra (−460 por mês nos últimos três meses), e é ali que mora o risco
    dessas metas.

## 3. Os cuidados das duas

- **A parede abdominal (L-007)** está nas duas: 3.138 na pura e 3.302 na ajustada.
- **As angiotomografias** pedem tomógrafo multicorte, bomba injetora e protocolo vascular. O
  plano assinado já tinha a de coronárias, então o equipamento já é exigido.
- **A coleta é de 29/10.** As filas mudam, e a medição final se faz de novo, com a exclusão
  de emergência e de sobreposição na ordem de coleta.
