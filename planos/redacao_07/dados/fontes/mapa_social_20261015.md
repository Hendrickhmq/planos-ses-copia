# Mapa Social da Saúde — varredura das filas de exames de imagem, recarga de 15/10/2026 19:32

Coleta do agente `mapa-social` para o redacao_07 (emenda de cerca de R$ 1,5 milhão para exames
de imagem, aberto em 15/10/2026). **Não há objeto:** o ponto de partida é "escolher a fila"
(`metodo/coleta/dossie.md`), e esta coleta é uma varredura ampla das filas de imagem do SISREG
para comparar candidatas **fora do plano 4** (`planos/redacao_04/`). O plano 4 entra só como
referência e como base do cruzamento de pessoas: os dezesseis nomes de fila do enquadramento
gravado em `planos/redacao_06/dados/fontes/mapa_social_20261009_bruto/coleta_20261009.json`,
nos onze códigos 02.05.01.004-0, 02.05.02.003-8, 02.05.02.004-6, 02.05.02.005-4, 02.05.02.009-7,
02.05.02.010-0, 02.05.02.012-7, 02.05.02.018-6, 02.06.02.003-1, 02.06.03.001-0 e 02.06.03.003-7.
Planilha em `mapa_social_20261015.xlsx`; JSON do motor e script em `mapa_social_20261015_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 15/10/2026 19:32:31 (qLastReloadTime 2026-10-15T22:32:31Z), conferida no início e no fim da coleta |
| Consulta | 15/10/2026 19:35:33 a 19:36:21 (relógio do motor, Brasília); uma medida complementar às 19:53:40, na mesma recarga |
| Solicitação mais recente na base | 15/10/2026 (na coleta de 09/10 era 02/10/2026) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Recorte | todos os anos; universo pelo código SIGTAP da solicitação (subgrupos 02.04, 02.05, 02.06, 02.07, 02.08 e 02.10) e pelo nome da fila; cada conjunto fixo na expressão de conjunto `{1<...>}`, sem depender da tela; sem recorte de CID, porque não há objeto |
| Via | Qlik Engine API do próprio painel (hipercubos de sessão e evaluateEx), no navegador embutido |
| Comparação | coleta de 09/10/2026 do redacao_06 (base de 09/10/2026 11:32), para o mesmo código do plano 4 e para o plano 4 |

**A base recarregou durante a coleta.** O painel foi aberto às 19:25:48 com a base de
15/10/2026 17:33:23; a recarga das 19:32:31 entrou no meio da varredura. Tudo o que está aqui
saiu depois dela, numa ida só (19:35:33 a 19:36:21), com a recarga conferida no início e no fim;
o que foi lido antes foi descartado.

Pessoas = CNS distintos no conjunto: quem espera por mais de um exame conta uma vez. Espera em
dias, calculada no motor sobre os registros do conjunto (não é média das linhas). Agendadas/mês
= agendamentos com data marcada de janeiro a setembro de 2026, divididos por 9 (**calculado**).
"Pessoas já no plano 4" = CNS do conjunto que também têm solicitação na fila dos dezesseis nomes
do plano 4 (`P()` no motor, só a contagem). **Códigos diferentes não se somam como se fossem um
objeto:** os totais por modalidade e do universo servem para dimensionar, não são fila de um
objeto.

---

## 1. Varredura das filas

### 1.1 Como se varreu

- **Pelo código.** O campo `codigo_sigtap_solicitacao` é numérico, sem o zero à esquerda e sem
  pontos (02.05.02.009-7 vem como 205020097, como no JSON de 09/10). O curinga
  `{"204*","205*","206*","207*","208*","210*"}` achou **746 filas** (pares nome de fila ×
  código) com alguém na fila, em **134 códigos**. Ele pega também dois códigos malformados, de
  oito dígitos e sem descrição SIGTAP (20406014 e 20406015), que são radiografias de joelho e de
  pé: ficam na radiologia, com a nota. A faixa numérica do mesmo intervalo não os pegaria.
- **Pelo nome.** Os 1.572 nomes de fila da base, normalizados (sem acento, espaço não separável
  como espaço, maiúsculas), foram procurados pelos termos de imagem (RESSON, RNM, RM, TOMOGRAF,
  TC, ANGIOTOMO, ANGIORRESSON, MAMOGRAF, DENSITOM, RADIOGRAF, RX, RAIO, CINTILOG, PET, ECOGRAF,
  ULTRA, USG, DOPPLER, ECOCARDIO, ELASTOGRAF, ARTERIOGRAF, FLEBOGRAF, UROGRAF, ESOFAGOGRAF,
  HISTEROSSALPINGO, ANGIOGRAF, CONTRAST, GUIADA, IMAGEM e partes do corpo); a descrição SIGTAP da
  solicitação, pelos mesmos termos; e o grupo do painel, pelos grupos de imagem. Fora dos
  subgrupos de imagem, só responderam **dez filas** (seção 1.4): punções e biópsias guiadas por
  imagem, OCT e biometria ultrassônica (oftalmologia), cateterismo e duas filas sem código no
  grupo de radiodiagnóstico. Não apareceu fila de imagem em "campo livre" (02.11.07.003-3).
- **Falsos positivos da busca por nome**, que não entram: consultas de ortopedia por segmento
  (joelho, coluna, quadril, pé, ombro, mão), odontologia, fisioterapia de coluna, pé diabético,
  mapeamento de retina, angioplastias, embolizações e correções endovasculares (04.06,
  terapêuticas; a angioplastia coronariana tem 97 na fila), cateterismo pediátrico, pletismografia
  e core biópsia de mama (fila 0). Lista no JSON e na aba 8.
- **Nome com dois códigos:** "COLUNA TOTAL" tem fila só com 02.04.02.013-1 (o código do ENMG,
  02.11.05.008-3, tem 0); "311. RM DE MAMA BILATERAL" tem fila só com 02.07.02.006-0 (o
  02.07.02.005-1 tem 0). As tabelas `*_ce` do app não têm nenhum código de imagem.
- **Cada fila foi estudada** (fila, pessoas, devolvidas, espera média, mediana e máxima, idade
  mediana, 1ª solicitação na base, fila pedida em 2026, agendadas de janeiro a setembro de 2026,
  os três CIDs principais e as pessoas já na fila do plano 4) e recebeu decisão pela regra pedida
  pela conversa principal, escrita no script da planilha (`decidir()`).

### 1.2 A decisão de cada fila

| categoria | decisão | filas | fila | pessoas | devolvidas | espera média | mediana | pessoas já na fila do plano 4 |
|---|---|---|---|---|---|---|---|---|
| **candidata** — subgrupos de imagem, fora dos onze códigos do plano 4 | a decidir | 611 | **69.675** | 56.722 | 62.342 | 216 | 97 | 10.992 |
| **mesmo código do plano 4** — os onze códigos, fora dos dezesseis nomes, sem resíduo | a decidir, com risco de sobreposição | 57 | **9.502** | 7.176 | 9.844 | 355 | 269 | 2.239 |
| resíduo do mesmo código do plano 4 | fica fora | 31 | 258 (calculado) | — | — | — | — | — |
| resíduo dos outros códigos — nada em 2026 | fica fora | 31 | **66** | 61 | 124 | 1.966 | 857 | 5 |
| outro código com nome de imagem (02.01, 02.11, sem código) | a decidir, à parte | 10 | **5.085** | 4.912 | 2.243 | 214 | 170 | 671 |
| plano 4 — os dezesseis nomes do enquadramento | fora da soma, referência | 16 | **76.037** | 61.310 | 55.428 | 500 | 293 | 61.310 |
| *fora do plano 4 = candidata + mesmo código sem resíduo (universo, não é objeto)* | — | 668 | 79.177 | 62.203 | 72.186 | 232 | 112 | 12.637 |

Linhas do motor (conjuntos), menos o resíduo do mesmo código, que é a diferença entre o
conjunto com e sem resíduo. As regras:
- **plano 4** — os dezesseis nomes do enquadramento: fora da soma, só referência;
- **mesmo código do plano 4** — as filas dos onze códigos fora do enquadramento: a decidir, com a
  nota de sobreposição com a execução do plano 4; as que não tiveram nenhuma solicitação nem
  agendamento em 2026 ficam fora como resíduo (31 filas, entre elas o doppler de carótidas e
  vertebrais antigo, com 190 na fila e nada em 2026);
- **resíduo** — fila de outro código sem nenhuma solicitação (qualquer status) nem agendamento em
  2026: fica fora. São 31 nomes antigos do SISREG, quase todos com uma ou duas solicitações, de
  2007 a 2025;
- **candidata** — todas as outras filas dos subgrupos de imagem: a decidir;
- **outro código** — nome ou código de imagem fora dos subgrupos (02.01, 02.11, sem código): a
  decidir, à parte, porque não é exame de imagem pelo SIGTAP.

"Fora do plano 4" (candidata + mesmo código sem resíduo) é o universo que a emenda pode olhar:
**79.177 na fila e 62.203 pessoas**, das quais 12.637 já estão na fila do plano 4. Só para
dimensionar; não é fila de um objeto.

### 1.3 O estudo das filas

CIDs = os três `codigo_cid_solicitado` com mais solicitações na fila, com a contagem. Espera em
dias. ␣␣ = dois espaços comuns; [NBSP] = espaço não separável (U+00A0); o JSON guarda o nome
exato. A nota "nada da fila pedido em 2026" marca fila viva só por agendamento.

**Mesmo código do plano 4, com 100 ou mais na fila**

| código | nome interno | fila | pessoas | devolv. | espera média / mediana / máx. | idade med. | 1ª solicitação | fila pedida 2026 | agend./mês 2026 (calc.) | já no plano 4 | CIDs principais | decisão — nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) | 1.809 | 1.809 | 326 | 471 / 393 / 1.424 | 63 | 19/10/2022 | 702 | 46 | 1.176 | I70 296; I83 246; I739 222 | a decidir — sobreposição |
| 02.05.02.012-7 | ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE | 801 | 801 | 531 | 438 / 351 / 1.961 | 54 | 19/11/2019 | 365 | 36 | 319 | E07 184; E04 99; E039 86 | a decidir — sobreposição |
| 02.05.02.004-6 | ECOGRAFIA DE ABDOMEN TOTAL INFANTIL | 451 | 451 | 429 | 590 / 360 / 2.061 | 9 | 07/01/2020 | 213 | 89 | 13 | R10 135; E66 56; R104 31 | a decidir — sobreposição |
| 02.05.02.005-4 | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL | 313 | 313 | 650 | 471 / 276 / 2.093 | 8 | 08/01/2020 | 162 | 65 | 34 | N39 36; N390 19; R31 14 | a decidir — sobreposição |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER DE CAROTIDAS E VERTEBRAIS | 190 | 190 | 26 | 954 / 925 / 1.345 | 66 | 08/02/2023 | 0 | 0 | 53 | I10 71; E11 23; I70 19 | fica fora — resíduo: nenhuma solicitação nem agendamento em 2026 (mesmo código do plano 4) |
| 02.05.01.004-0 | ECOGRAFIA TRANSVAGINAL COM DOPPLER | 144 | 144 | 151 | 552 / 478 / 1.379 | 49 | 15/01/2020 | 48 | 12 | 66 | Z014 19; N951 13; R10 10 | a decidir — sobreposição |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) | 144 | 144 | 204 | 165 / 107 / 848 | 56 | 25/10/2022 | 122 | 7 | 40 | I83 23; I82 16; I872 14 | a decidir — sobreposição |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS | 133 | 133 | 0 | 18 / 21 / 43 | 58 | 02/09/2026 | 133 | 0 | 39 | I83 25; I839 16; I87 10 | a decidir — sobreposição |
| 02.06.02.003-1 | TC DO TORAX␣␣ADULTO S/CONTRASTE S/SEDACAO␣␣EMERGENCIA | 888 | 888 | 78 | 341 / 318 / 3.600 | 64 | 06/12/2016 | 412 | 166 | 85 | J18 170; I25 73; C50 36 | a decidir — sobreposição |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.ADULTO␣␣C/CONTRASTE S/SEDACAO␣␣EMERG. | 729 | 729 | 84 | 346 / 344 / 748 | 58 | 29/12/2016 | 324 | 126 | 100 | R10 133; C18 32; C50 29 | a decidir — sobreposição |
| 02.06.03.003-7 | TC DE PELVE OU BACIA ADULTO␣␣C/CONTRASTE␣␣S/SEDACAO EMERG. | 676 | 676 | 67 | 338 / 322 / 748 | 57 | 27/09/2024 | 309 | 111 | 94 | R10 112; Z54 30; C18 28 | a decidir — sobreposição |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.ADULTO␣␣S/CONTRASTE S/SEDACAO␣␣EMERG. | 391 | 391 | 67 | 355 / 344 / 3.600 | 57 | 06/12/2016 | 167 | 61 | 48 | R10 92; N20 22; Z54 11 | a decidir — sobreposição |
| 02.06.03.003-7 | TC DE PELVE OU BACIA ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO EMERG. | 370 | 370 | 63 | 356 / 339 / 3.600 | 57 | 06/12/2016 | 158 | 55 | 43 | R10 84; N20 16; Z54 11 | a decidir — sobreposição |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS[NBSP] ADULTO S/SEDACAO[NBSP] | 331 | 331 | 174 | 200 / 170 / 737 | 65 | 29/01/2024 | 238 | 47 | 82 | I71 118; I35 29; I712 24 | a decidir — sobreposição |
| 02.06.02.003-1 | TC DO TORAX␣␣ADULTO C/CONTRASTE␣␣S/SEDACAO␣␣EMERGENCIA | 309 | 309 | 30 | 340 / 313 / 750 | 59 | 26/09/2024 | 144 | 80 | 43 | C50 16; C53 13; I26 13 | a decidir — sobreposição |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO[NBSP] | 299 | 299 | 143 | 201 / 170 / 737 | 65 | 10/01/2024 | 211 | 37 | 59 | I71 98; I70 19; N180 18 | a decidir — sobreposição |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO | 283 | 283 | 589 | 138 / 115 / 527 | 59 | 29/01/2024 | 247 | 117 | 62 | I26 88; I71 29; I27 18 | a decidir — sobreposição |
| 02.06.03.003-7 | ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO | 248 | 248 | 140 | 209 / 171 / 461 | 57 | 10/01/2024 | 161 | 26 | 55 | I82 32; I71 30; N180 23 | a decidir — sobreposição |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO[NBSP] | 243 | 243 | 128 | 208 / 174 / 526 | 58 | 04/04/2024 | 160 | 25 | 59 | I71 35; N180 23; K55 18 | a decidir — sobreposição |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO | 227 | 227 | 130 | 128 / 107 / 456 | 68 | 24/01/2024 | 202 | 39 | 45 | I65 45; I64 30; I652 25 | a decidir — sobreposição |

**Candidatas com 100 ou mais na fila**

| código | nome interno | fila | pessoas | devolv. | espera média / mediana / máx. | idade med. | 1ª solicitação | fila pedida 2026 | agend./mês 2026 (calc.) | já no plano 4 | CIDs principais | decisão — nota |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | MAMOGRAFIA BILATERAL PARA SCREENING (ROTINA) | 6.274 | 6.274 | 2.233 | 48 / 28 / 2.186 | 54 | 03/01/2020 | 6.213 | 4.275 | 1.118 | Z123 3355; Z12 1313; N63 263 | a decidir — candidata |
| 02.04.06.002-8 | DENSITOMETRIA OSSEA - RADIODIAGNOSTICO | 2.196 | 2.196 | 3.620 | 44 / 35 / 2.158 | 66 | 23/03/2020 | 2.194 | 980 | 444 | M81 786; M810 158; M819 154 | a decidir — candidata |
| 02.04.01.017-9 | RADIOGRAFIA PANORAMICA | 940 | 939 | 2.514 | 32 / 21 / 2.375 | 33 | 17/01/2020 | 936 | 1.302 | 55 | K08 240; K01 169; K081 112 | a decidir — candidata |
| 02.04.01.018-7 | RADIOLOGIA PERIAPICAL - ATÉ 5 INCIDÊNCIAS | 706 | 706 | 621 | 24 / 21 / 65 | 39 | 06/01/2020 | 706 | 769 | 53 | K02 316; K04 119; K08 98 | a decidir — candidata |
| 02.04.03.015-3 | TORAX : PA E PERFIL | 662 | 662 | 187 | 95 / 94 / 206 | 53 | 07/02/2020 | 662 | 1.099 | 78 | R074 37; K80 34; R05 34 | a decidir — candidata |
| 02.04.01.017-9 | RADIOGRAFIA PERIAPICAL DE 6 A 13 INCIDÊNCIAS | 601 | 600 | 227 | 214 / 198 / 535 | 47 | 06/01/2020 | 401 | 49 | 55 | K02 277; K05 85; K04 73 | a decidir — candidata |
| 02.04.03.018-8 | MAMOGRAFIA BILATERAL DIAGNOSTICA | 187 | 187 | 568 | 74 / 23 / 2.170 | 51 | 08/01/2020 | 182 | 407 | 63 | N63 81; Z123 35; Z12 19 | a decidir — candidata |
| 02.04.02.006-9 | COLUNA LOMBO SACRA (AP E PERFIL) | 136 | 136 | 31 | 91 / 79 / 212 | 52,5 | 17/05/2021 | 136 | 64 | 11 | M545 50; M54 31; M549 17 | a decidir — candidata |
| 02.04.01.017-9 | RADIOGRAFIA DE BOCA TOTAL (14 PERIAPICAIS + 4 BITE-WINGS) | 112 | 112 | 210 | 53 / 49 / 147 | 42 | 10/03/2020 | 112 | 45 | 6 | K02 38; K05 35; K08 17 | a decidir — candidata |
| 02.05.01.003-2 | 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 14.646 | 14.646 | 13.100 | 135 / 127 / 521 | 62 | 19/08/2016 | 14.072 | 2.851 | 4.700 | I10 2653; I50 2258; I25 1041 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE PARTES MOLES | 3.108 | 3.107 | 1.470 | 654 / 520 / 5.832 | 51 | 28/10/2010 | 1.093 | 127 | 533 | D17 535; R22 502; K40 153 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | 1.993 | 1.991 | 732 | 556 / 393 / 2.102 | 58 | 23/01/2020 | 708 | 99 | 357 | M75 552; M255 290; M751 266 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | 1.743 | 1.742 | 383 | 509 / 372 / 5.866 | 53 | 24/09/2010 | 712 | 57 | 325 | G56 359; G560 331; M255 176 | a decidir — candidata |
| 02.05.01.003-2 | 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 1.593 | 1.592 | 2.510 | 134 / 136 / 702 | 3 | 23/07/2019 | 1.590 | 505 | 9 | R01 232; Q21 167; R011 131 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | 1.545 | 1.544 | 575 | 535 / 386 / 2.107 | 57 | 06/01/2020 | 567 | 73 | 326 | M75 428; M255 214; M751 185 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | 1.468 | 1.467 | 352 | 491 / 365 / 2.106 | 53 | 09/01/2020 | 609 | 46 | 279 | G56 311; G560 240; M255 141 | a decidir — candidata |
| 02.05.02.008-9 | ULTRA-SONOGRAFIA DO GLOBO OCULAR OU DE ORBITA | 1.272 | 1.272 | 196 | 264 / 266 / 491 | 62 | 17/02/2020 | 676 | 58 | 106 | H25 403; H35 99; H26 73 | a decidir — candidata |
| 02.05.02.007-0 | ECOGRAFIA DE BOLSA ESCROTAL ADULTO | 734 | 734 | 429 | 616 / 517 / 2.099 | 46 | 06/01/2020 | 256 | 45 | 137 | N511 102; K40 73; N51 73 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO JOELHO E ADULTO | 593 | 593 | 84 | 582 / 514 / 2.086 | 56 | 06/01/2020 | 199 | 29 | 100 | M23 123; M255 103; M17 46 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO JOELHO D ADULTO | 586 | 586 | 64 | 571 / 521 / 2.086 | 55 | 13/01/2020 | 194 | 30 | 109 | M23 143; M255 115; M17 54 | a decidir — candidata |
| 02.05.02.016-0 | ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO | 570 | 570 | 829 | 708 / 428 / 2.108 | 24 | 02/01/2020 | 240 | 74 | 113 | R10 78; Z014 36; N946 34 | a decidir — candidata |
| 02.05.02.016-0 | ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL | 433 | 433 | 82 | 464 / 343 / 2.095 | 10 | 24/04/2020 | 199 | 37 | 20 | E30 69; E301 60; E228 43 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO TORNOZELO E ADULTO | 381 | 380 | 122 | 464 / 365 / 2.095 | 55 | 03/02/2020 | 146 | 18 | 94 | M255 64; M722 27; M65 22 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO TORNOZELO D ADULTO | 339 | 339 | 144 | 439 / 331 / 2.044 | 55 | 03/02/2020 | 143 | 21 | 80 | M255 50; M722 25; M25 20 | a decidir — candidata |
| 02.05.02.014-3 | ECOGRAFIA OBSTETRICA | 324 | 324 | 515 | 125 / 65 / 1.924 | 26 | 09/01/2020 | 283 | 254 | 12 | Z34 232; Z35 31; Z36 9 | a decidir — candidata |
| 02.05.02.017-8 | ULTRA-SONOGRAFIA TRANSFONTANELA | 281 | 281 | 201 | 282 / 213 / 1.576 | 0 | 18/02/2020 | 185 | 74 | 3 | P21 42; Q75 30; Q753 20 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE REGIAO INGUINAL DIREITO | 233 | 233 | 16 | 375 / 323 / 1.316 | 51 | 09/03/2023 | 109 | 23 | 25 | K40 152; K409 26; R10 10 | a decidir — candidata |
| 02.05.02.007-0 | ECOGRAFIA DE BOLSA ESCROTAL INFANTIL | 232 | 232 | 71 | 524 / 233 / 2.106 | 3 | 31/01/2020 | 119 | 27 | 10 | Q53 55; N43 29; N433 18 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | 223 | 223 | 70 | 528 / 345 / 2.058 | 52 | 03/02/2020 | 104 | 24 | 42 | M771 42; M255 34; M77 22 | a decidir — candidata |
| 02.05.02.015-1 | ECOGRAFIA␣␣OBSTETRICA: COM DOPPLER COLORIDO | 205 | 205 | 120 | 177 / 141 / 587 | 29 | 09/04/2020 | 161 | 32 | 7 | Z34 81; Z35 47; Z359 23 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | 195 | 195 | 12 | 348 / 275 / 1.421 | 52 | 24/11/2022 | 102 | 18 | 23 | K40 131; K409 17; R10 10 | a decidir — candidata |
| 02.05.02.006-2 | USG MAO DIREITA | 194 | 194 | 30 | 410 / 271 / 1.345 | 56,5 | 23/01/2020 | 99 | 11 | 17 | M653 26; M255 22; M65 20 | a decidir — candidata |
| 02.05.02.002-0 | PAQUIMETRIA ULTRASSONICA | 164 | 164 | 247 | 22 / 19 / 51 | 62,5 | 14/04/2020 | 164 | 167 | 18 | H40 85; H400 22; H18 16 | a decidir — candidata |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DA REGIAO INGUINAL | 159 | 159 | 26 | 448 / 435 / 1.296 | 52 | 29/03/2023 | 54 | 24 | 43 | K40 98; K409 12; K402 5 | a decidir — candidata |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DO PESCOCO | 155 | 155 | 8 | 513 / 486 / 1.347 | 47 | 01/12/2022 | 42 | 4 | 32 | R221 28; R22 15; R59 14 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | 141 | 141 | 59 | 468 / 344 / 2.094 | 51 | 22/01/2020 | 66 | 21 | 27 | M771 21; M255 16; M77 11 | a decidir — candidata |
| 02.05.02.006-2 | USG MAO ESQUERDA | 139 | 139 | 26 | 474 / 385 / 1.345 | 56 | 19/05/2020 | 62 | 10 | 17 | M255 24; M653 18; M713 10 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | 134 | 134 | 1 | 508 / 506 / 904 | 1 | 24/04/2024 | 31 | 0 | 2 | Q76 98; Q05 14; Q760 7 | a decidir — candidata |
| 02.05.02.006-2 | USG QUADRIL | 117 | 117 | 17 | 332 / 265 / 1.346 | 1 | 20/01/2020 | 68 | 7 | 7 | Q65 34; M255 8; M706 6 | a decidir — candidata |
| 02.05.02.006-2 | USG PE DIREITO | 110 | 110 | 21 | 545 / 400 / 1.346 | 53 | 24/01/2020 | 48 | 6 | 20 | M722 21; M72 14; M773 11 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO NAO LISTADA | 107 | 107 | 259 | 893 / 696 / 2.100 | 52 | 02/01/2020 | 18 | 4 | 18 | M65 10; M255 9; M653 7 | a decidir — candidata |
| 02.06.01.005-2 | 119. TC DE PESCOCO ADULTO C/CONTRASTE S/SEDACAO | 491 | 490 | 334 | 118 / 113 / 829 | 61 | 13/01/2020 | 489 | 111 | 381 | C32 41; C73 28; C10 19 | a decidir — candidata |
| 02.06.01.009-5 | TOMOGRAFIA POR EMISSÃO DE PÓSITRONS (PET-CT) | 424 | 424 | 819 | 162 / 128 / 371 | 61 | 11/11/2021 | 301 | 42 | 112 | C34 39; C81 37; C18 33 | a decidir — candidata |
| 02.06.01.007-9 | TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA | 390 | 390 | 80 | 359 / 358 / 752 | 62 | 23/09/2024 | 166 | 92 | 30 | I64 58; R51 32; R41 19 | a decidir — fila de emergência |
| 02.06.01.007-9 | 031. TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO | 380 | 380 | 1.107 | 119 / 112 / 832 | 54 | 02/01/2020 | 374 | 155 | 187 | R51 73; C50 30; C509 14 | a decidir — candidata |
| 02.06.01.007-9 | ANGIOTOMOGRAFIA DO CRANIO ADULTO S/SEDACAO | 336 | 336 | 256 | 69 / 65 / 176 | 58 | 31/01/2024 | 336 | 110 | 45 | I67 54; I671 50; I64 42 | a decidir — candidata |
| 02.06.01.004-4 | TOMOGRAFIA CONE BEAN | 199 | 199 | 196 | 87 / 86 / 265 | 28 | 11/07/2023 | 199 | 27 | 9 | K01 58; K011 50; K04 21 | a decidir — candidata |
| 02.06.01.005-2 | ANGIOTOMOGRAFIA DO PESCOCO ADULTO S/SEDACAO | 162 | 162 | 187 | 94 / 92 / 234 | 66,5 | 02/02/2024 | 162 | 40 | 29 | I64 29; I65 19; I652 17 | a decidir — candidata |
| 02.06.01.007-9 | TC DE CRANIO ADULTO C/CONTRASTE S/SEDACAO EMERGENCIA | 128 | 128 | 10 | 372 / 384 / 751 | 59 | 24/09/2024 | 51 | 39 | 15 | C50 16; I64 10; C79 7 | a decidir — fila de emergência |
| 02.06.01.007-9 | 029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO | 115 | 115 | 760 | 14 / 2 / 307 | 53 | 02/01/2020 | 114 | 769 | 19 | R51 40; G40 6; R55 5 | a decidir — candidata |
| 02.07.01.004-8 | 037. RM DA COLUNA LOMBO-SACRA ADULTO S/CONTRASTE S/SEDACAO | 1.193 | 1.193 | 1.282 | 18 / 16 / 57 | 52 | 06/01/2020 | 1.193 | 1.308 | 169 | M545 436; M54 199; M511 128 | a decidir — candidata |
| 02.07.03.002-2 | 071. RM DE BACIA OU PELVIS ADULTO C/CONTRASTE S/SEDACAO | 1.122 | 1.122 | 674 | 26 / 24 / 80 | 51 | 04/01/2020 | 1.122 | 1.167 | 239 | N80 131; C53 78; C50 70 | a decidir — candidata |
| 02.07.03.001-4 | 055. RM DE ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 657 | 657 | 494 | 24 / 24 / 64 | 59 | 04/01/2020 | 657 | 785 | 149 | C50 73; C18 59; C53 51 | a decidir — candidata |
| 02.07.01.006-4 | 005. RM DE CRANIO ADULTO S/CONTRASTE S/SEDACAO | 588 | 588 | 557 | 19 / 16 / 1.269 | 57 | 06/01/2020 | 587 | 619 | 86 | R51 102; F03 46; G40 42 | a decidir — candidata |
| 02.07.01.006-4 | 007. RM DE CRANIO ADULTO C/CONTRASTE S/SEDACAO | 581 | 581 | 652 | 24 / 22 / 210 | 53 | 04/01/2020 | 581 | 610 | 105 | R51 54; G35 41; C50 39 | a decidir — candidata |
| 02.07.01.003-0 | 021. RM DA COLUNA CERVICAL ADULTO S/CONTRASTE S/SEDACAO | 478 | 477 | 529 | 17 / 16 / 56 | 51 | 12/04/2017 | 478 | 541 | 64 | M542 153; M54 71; M501 26 | a decidir — candidata |
| 02.07.03.003-0 | 133. RM DE JOELHO D ADULTO S/CONTRASTE S/SEDACAO | 476 | 476 | 377 | 18 / 16 / 69 | 52 | 03/01/2020 | 476 | 475 | 78 | M23 104; M255 93; M17 50 | a decidir — candidata |
| 02.07.03.002-2 | 069. RM DE BACIA OU PELVIS ADULTO S/CONTRASTE S/SEDACAO | 446 | 446 | 739 | 17 / 16 / 73 | 45 | 06/01/2020 | 446 | 420 | 60 | N80 98; R10 39; M255 33 | a decidir — candidata |
| 02.07.03.003-0 | 141. RM DE JOELHO E ADULTO S/CONTRASTE S/SEDACAO | 435 | 435 | 384 | 18 / 16 / 56 | 53 | 16/01/2020 | 435 | 454 | 59 | M23 87; M255 74; M17 51 | a decidir — candidata |
| 02.07.02.002-7 | 077. RM DE OMBRO D ADULTO S/CONTRASTE S/SEDACAO | 323 | 323 | 209 | 17 / 16 / 66 | 54 | 09/01/2020 | 323 | 303 | 46 | M75 80; M751 78; M255 30 | a decidir — candidata |
| 02.07.02.002-7 | 085. RM DE OMBRO E ADULTO S/CONTRASTE S/SEDACAO | 226 | 226 | 170 | 17 / 16 / 55 | 57 | 22/01/2020 | 226 | 232 | 36 | M75 62; M751 53; M255 24 | a decidir — candidata |
| 02.07.01.005-6 | 029. RM DA COLUNA DORSAL ADULTO S/CONTRASTE S/SEDACAO | 168 | 168 | 241 | 18 / 16 / 52 | 52 | 16/01/2020 | 168 | 236 | 25 | M54 49; M546 18; M545 13 | a decidir — candidata |
| 02.07.02.001-9 | 264. RM DO CORACAO OU AORTA ADULTO C/CONTRASTE S/SEDACAO | 162 | 162 | 316 | 64 / 58 / 135 | 57 | 14/02/2020 | 162 | 83 | 30 | I50 40; I42 19; I25 11 | a decidir — candidata |
| 02.07.01.001-3 | ANGIORESSONANCIA CEREBRAL ARTERIAL | 161 | 161 | 31 | 40 / 42 / 91 | 52 | 28/04/2023 | 161 | 123 | 34 | I671 31; I64 19; R51 19 | a decidir — candidata |
| 02.07.01.004-8 | 039. RM DA COLUNA LOMBO-SACRA ADULTO C/CONTRASTE S/SEDACAO | 160 | 160 | 304 | 24 / 23 / 56 | 53 | 07/01/2020 | 160 | 196 | 30 | M545 24; M54 14; C61 10 | a decidir — candidata |
| 02.07.01.003-0 | 023. RM DA COLUNA CERVICAL ADULTO C/CONTRASTE S/SEDACAO | 120 | 120 | 183 | 26 / 24 / 55 | 49 | 03/01/2020 | 120 | 145 | 19 | G35 35; C50 6; M542 4 | a decidir — candidata |
| 02.08.01.002-5 | CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | 1.825 | 1.825 | 65 | 276 / 337 / 443 | 66 | 23/06/2025 | 808 | 32 | 383 | I25 576; I20 511; I50 107 | a decidir — candidata |
| 02.08.05.003-5 | CINTILOGRAFIA DE OSSOS C/ OU S/ FLUXO SANGUINEO (CORPO INTEIRO) | 1.688 | 1.688 | 26 | 144 / 125 / 407 | 62 | 25/06/2025 | 1.460 | 130 | 637 | C50 713; C61 348; C509 247 | a decidir — candidata |
| 02.08.01.003-3 | CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | 1.505 | 1.505 | 32 | 281 / 364 / 443 | 66 | 26/06/2025 | 632 | 29 | 303 | I25 468; I20 417; I50 83 | a decidir — candidata |
| 02.08.04.010-2 | CINTILOGRAFIA RENAL DINAMICA (DTPA) | 222 | 222 | 4 | 149 / 155 / 336 | 45,5 | 11/08/2025 | 207 | 11 | 38 | N13 44; N20 37; N18 23 | a decidir — candidata |
| 02.08.03.001-8 | CINTILOGRAFIA DE PARATIREOIDES | 189 | 189 | 10 | 176 / 170 / 386 | 60 | 11/08/2025 | 152 | 17 | 37 | E21 109; N250 17; E210 10 | a decidir — candidata |
| 02.08.04.005-6 | CINTILOGRAFIA RENAL ESTATICA (DMSA) | 167 | 167 | 15 | 94 / 78 / 206 | 44 | 25/08/2025 | 167 | 25 | 32 | N20 37; N13 24; Q62 17 | a decidir — candidata |
| 02.08.02.003-9 | CINTILOGRAFIA DE GLANDULAS SALIVARES C/ OU S/ ESTIMULO | 122 | 122 | 3 | 121 / 103 / 311 | 54,5 | 24/09/2025 | 113 | 5 | 20 | M35 63; M350 40; M32 4 | a decidir — candidata |

**Filas de 10 a 99 na fila** (mesmo código do plano 4, candidatas e resíduo)

| código | nome interno | fila | espera média | idade med. | 1ª solicitação | fila pedida 2026 | agend./mês 2026 (calc.) | já no plano 4 | decisão — nota |
|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS | 89 | 191 | 52 | 05/11/2023 | 64 | 2 | 28 | a decidir — mesmo código do plano 4 |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) | 60 | 243 | 63 | 07/11/2022 | 35 | 7 | 19 | a decidir — mesmo código do plano 4 |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER VENOSO - MIE | 10 | 1.591 | 65 | 03/01/2020 | 0 | 0 | 7 | fica fora — resíduo: nenhuma solicitação nem agendamento em 2026 (mesmo código do plano 4) |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER DE AORTA E VASOS ILIACOS | 10 | 42 | 53 | 05/05/2022 | 10 | 2 | 8 | a decidir — mesmo código do plano 4 |
| 02.05.01.004-0 | ULTRASSONOGRAFIA DAS GLANDULAS PAROTIDAS | 10 | 361 | 51,5 | 28/08/2023 | 6 | 2 | 1 | a decidir — mesmo código do plano 4 |
| 02.05.02.003-8 | ECOGRAFIA DE ABDOMEN SUPERIOR INFANTIL | 19 | 512 | 10 | 27/10/2020 | 11 | 10 | 2 | a decidir — mesmo código do plano 4 |
| 02.05.02.005-4 | ULTRASSONOGRAFIA RENAL | 72 | 611 | 60 | 23/02/2023 | 21 | 2 | 19 | a decidir — mesmo código do plano 4 |
| 02.05.02.012-7 | ECOGRAFIA DE TIREOIDE INFANTIL | 68 | 482 | 11 | 02/02/2021 | 19 | 8 | 2 | a decidir — mesmo código do plano 4 |
| 02.06.02.003-1 | TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 42 | 342 | 3,5 | 03/10/2024 | 15 | 1 | 1 | a decidir — mesmo código do plano 4 |
| 02.06.02.003-1 | TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO␣␣EMERGENCIA | 23 | 326 | 5 | 06/11/2024 | 11 | 1 | 1 | a decidir — mesmo código do plano 4 |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA[NBSP] DAS ARTÉRIAS CORONARIAS INFANTIL S/SEDACAO | 11 | 273 | 7 | 31/01/2025 | 6 | 0 | 0 | a decidir — mesmo código do plano 4 |
| 02.06.03.001-0 | 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 67 | 15 | 54 | 02/01/2020 | 67 | 488 | 15 | a decidir — mesmo código do plano 4 |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.INFANTIL C/CONTRASTE S/SEDACAO␣␣EMERG. | 34 | 324 | 12,5 | 30/10/2024 | 17 | 1 | 2 | a decidir — mesmo código do plano 4 |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO | 32 | 161 | 45 | 17/07/2024 | 25 | 4 | 6 | a decidir — mesmo código do plano 4 |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 14 | 345 | 7,5 | 01/10/2024 | 7 | 1 | 1 | a decidir — mesmo código do plano 4 |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DO SISTEMA PORTA (VASOS HEPÁTICOS) ADULTO S/SEDACAO | 12 | 211 | 45,5 | 28/03/2024 | 7 | 1 | 1 | a decidir — mesmo código do plano 4 |
| 02.06.03.003-7 | 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE␣␣S/SEDACAO | 63 | 16 | 55 | 03/01/2020 | 63 | 485 | 15 | a decidir — mesmo código do plano 4 |
| 02.06.03.003-7 | TC DE PELVE OU BACIA INFANTIL␣␣C/CONTRASTE␣␣S/SEDACAO EMERG. | 30 | 341 | 44 | 08/10/2024 | 14 | 1 | 3 | a decidir — mesmo código do plano 4 |
| 02.06.03.003-7 | TC DE PELVE OU BACIA INFANTIL␣␣S/CONTRASTE␣␣S/SEDACAO EMERG. | 15 | 445 | 39 | 27/12/2024 | 2 | 1 | 0 | a decidir — mesmo código do plano 4 |
| 02.04.01.006-3 | CAVUM - LATERAL | 76 | 95 | 6,5 | 30/09/2020 | 76 | 65 | 0 | a decidir — candidata |
| 02.04.01.006-3 | RADIOGRAFIA DE CAVUM (LATERAL + HIRTZ) | 58 | 101 | 7 | 20/04/2022 | 58 | 141 | 0 | a decidir — candidata |
| 02.04.01.014-4 | SEIOS DA FACE - F.N.+M.N | 14 | 101 | 25,5 | 13/01/2021 | 14 | 72 | 2 | a decidir — candidata |
| 02.04.01.014-4 | SEIOS DA FACE : F.N. + M.N. + LATERAL | 11 | 114 | 45 | 30/06/2021 | 11 | 0 | 1 | a decidir — candidata |
| 02.04.02.003-4 | COLUNA CERVICAL (AP E PERFIL) | 83 | 124 | 57 | 30/09/2020 | 82 | 110 | 11 | a decidir — candidata |
| 02.04.02.003-4 | COLUNA CERVICAL: AP + LATERAL + TO + OBLIQUAS (AP E PERFIL) | 46 | 70 | 56,5 | 02/07/2021 | 46 | 4 | 3 | a decidir — candidata |
| 02.04.02.006-9 | COLUNA LOMBO-SACRA (AP E PERFIL) | 53 | 128 | 56 | 06/05/2021 | 53 | 137 | 0 | a decidir — candidata |
| 02.04.02.006-9 | COLUNA LOMBAR (AP E PERFIL) | 38 | 90 | 59 | 14/07/2020 | 38 | 84 | 1 | a decidir — candidata |
| 02.04.02.006-9 | COLUNA LOMBAR: AP+LATERAL | 38 | 127 | 57 | 13/09/2022 | 38 | 2 | 3 | a decidir — candidata |
| 02.04.02.007-7 | COLUNA LOMBO SACRA COM OBLIQUAS (AP E PERFIL) | 31 | 73 | 54 | 19/07/2021 | 31 | 11 | 4 | a decidir — candidata |
| 02.04.02.009-3 | COLUNA DORSAL : AP + LATERAL | 51 | 118 | 53 | 06/05/2021 | 51 | 4 | 5 | a decidir — candidata |
| 02.04.02.009-3 | COLUNA DORSAL (AP E PERFIL) | 23 | 79 | 58 | 29/09/2020 | 23 | 55 | 4 | a decidir — candidata |
| 02.04.02.009-3 | RADIOGRAFIA DE COLUNA TORACICA LOMBO - SACRA (AP + LATERAL) | 20 | 112 | 51,5 | 10/02/2020 | 20 | 1 | 1 | a decidir — candidata |
| 02.04.02.009-3 | RADIOGRAFIA DE COLUNA TORACICA (AP + LATERAL) | 15 | 112 | 50 | 30/09/2020 | 15 | 30 | 0 | a decidir — candidata |
| 02.04.02.009-3 | COLUNA DORSAL : AP + LATERAL (AP E PERFIL) | 13 | 121 | 52 | 11/10/2022 | 13 | 5 | 0 | a decidir — candidata |
| 02.04.02.010-7 | COLUNA DORSO - LOMBAR PARA ESCOLIOSE (AP E PERFIL) | 17 | 96 | 39 | 24/08/2022 | 17 | 3 | 0 | a decidir — candidata |
| 02.04.02.010-7 | RADIOGRAFIA DE COLUNA TORACO ? LOMBAR | 12 | 89 | 37,5 | 30/09/2022 | 12 | 8 | 2 | a decidir — candidata |
| 02.04.02.013-1 | COLUNA TOTAL | 34 | 12 | 36,5 | 18/04/2022 | 34 | 116 | 4 | a decidir — candidata |
| 02.04.03.017-0 | TORAX:␣␣P.A | 11 | 4.427 | 56 | 09/12/2009 | 3 | 3 | 0 | a decidir — candidata |
| 02.04.04.005-1 | BRACO DIREITO (AP E PERFIL) | 16 | 71 | 48,5 | 09/11/2022 | 16 | 6 | 1 | a decidir — candidata |
| 02.04.04.005-1 | BRACO ESQUERDO (AP E PERFIL) | 15 | 52 | 44 | 16/08/2021 | 15 | 5 | 0 | a decidir — candidata |
| 02.04.04.007-8 | COTOVELO DIREITO (AP E PERFIL) | 22 | 81 | 54,5 | 14/10/2022 | 22 | 9 | 3 | a decidir — candidata |
| 02.04.04.007-8 | COTOVELO ESQUERDO (AP E PERFIL) | 14 | 100 | 45 | 23/10/2020 | 14 | 8 | 0 | a decidir — candidata |
| 02.04.04.009-4 | MAO DIREITA (AP E OBLIQUO) | 75 | 60 | 59 | 02/09/2021 | 75 | 30 | 8 | a decidir — candidata |
| 02.04.04.009-4 | MAO ESQUERDA (AP E OBLIQUO) | 74 | 66 | 58 | 18/11/2021 | 74 | 26 | 8 | a decidir — candidata |
| 02.04.04.009-4 | MAO DIREITA ( DUAS INCIDENCIAS) (AP E OBLIQUO) | 45 | 98 | 59 | 18/11/2021 | 45 | 2 | 2 | a decidir — candidata |
| 02.04.04.009-4 | MAO ESQUERDA ( DUAS INCIDENCIAS) (AP E OBLIQUO) | 33 | 84 | 58 | 16/11/2022 | 33 | 1 | 1 | a decidir — candidata |
| 02.04.04.009-4 | MAO DIREITA ( DUAS INCIDENCIAS) | 23 | 114 | 58 | 17/06/2022 | 23 | 27 | 5 | a decidir — candidata |
| 02.04.04.009-4 | MAO ESQUERDA ( DUAS INCIDENCIAS) | 19 | 112 | 59 | 27/05/2025 | 19 | 26 | 5 | a decidir — candidata |
| 02.04.04.009-4 | RADIOGRAFIA DE MAO | 10 | 66 | 57,5 | 25/05/2022 | 10 | 88 | 1 | a decidir — candidata |
| 02.04.04.010-8 | MAOS E PUNHOS PARA IDADE OSSEA ESQUERDO | 73 | 106 | 9 | 03/01/2020 | 73 | 3 | 1 | a decidir — candidata |
| 02.04.04.010-8 | RADIOGRAFIA DE MAO E PUNHO P/DETERMINACAO DE IDADE OSSEA | 44 | 84 | 9 | 10/02/2020 | 44 | 38 | 0 | a decidir — candidata |
| 02.04.04.010-8 | MAOS E PUNHOS PARA IDADE OSSEA | 25 | 82 | 8 | 02/04/2020 | 25 | 136 | 0 | a decidir — candidata |
| 02.04.04.011-6 | OMBRO DIREITO (AP VERDADEIRO, PERFIL DE ESCAPULAR E AXILAR) | 26 | 107 | 52,5 | 26/01/2021 | 26 | 59 | 0 | a decidir — candidata |
| 02.04.04.011-6 | OMBRO ESQUERDO (AP VERDADEIRO, PERFIL DE ESCAPULAR E AXILAR) | 21 | 129 | 61 | 04/04/2022 | 21 | 47 | 0 | a decidir — candidata |
| 02.04.04.011-6 | RAIO X DE OMBRO DIREITO | 13 | 36 | 60 | 11/05/2022 | 13 | 9 | 0 | a decidir — candidata |
| 02.04.04.011-6 | RAIO X DE OMBRO ESQUERDO | 10 | 52 | 58 | 02/05/2022 | 10 | 5 | 2 | a decidir — candidata |
| 02.04.04.012-4 | PUNHO ESQUERDO: AP + LATERAL + OBLIQUOS | 34 | 94 | 55 | 09/05/2022 | 34 | 2 | 3 | a decidir — candidata |
| 02.04.04.012-4 | PUNHO DIREITO: AP + LATERAL + OBLIQUOS | 32 | 83 | 56,5 | 10/05/2022 | 32 | 2 | 2 | a decidir — candidata |
| 02.04.04.012-4 | PUNHO ESQUERDO: (AP E PERFIL) | 25 | 97 | 59 | 10/12/2020 | 25 | 10 | 1 | a decidir — candidata |
| 02.04.04.012-4 | PUNHO DIREITO: (AP E PERFIL) | 24 | 103 | 59,5 | 22/02/2021 | 24 | 9 | 0 | a decidir — candidata |
| 02.04.06.006-0 | ARTICULACAO COXO-FEMORAL ESQUERDO (AP E PERFIL) | 16 | 88 | 52,5 | 09/11/2022 | 16 | 0 | 1 | a decidir — candidata |
| 02.04.06.006-0 | ARTICULACAO COXO-FEMORAL DIREITO | 14 | 22 | 64 | 11/07/2022 | 14 | 13 | 0 | a decidir — candidata |
| 02.04.06.006-0 | ARTICULACAO COXO-FEMORAL ESQUERDO | 14 | 60 | 61 | 19/09/2022 | 14 | 13 | 1 | a decidir — candidata |
| 02.04.06.008-7 | ARTICULACAO TIBIO-TARSICA ESQUERDO (AP VERDADEIRO E PERFIL) | 28 | 82 | 58 | 10/05/2022 | 28 | 7 | 3 | a decidir — candidata |
| 02.04.06.008-7 | ARTICULACAO TIBIO-TARSICA DIREITO (AP VERDADEIRO E PERFIL) | 22 | 94 | 57 | 24/05/2022 | 22 | 8 | 1 | a decidir — candidata |
| 02.04.06.009-5 | BACIA (AP E FROG) | 53 | 82 | 58 | 05/10/2021 | 53 | 5 | 3 | a decidir — candidata |
| 02.04.06.009-5 | BACIA | 28 | 97 | 57 | 30/09/2020 | 28 | 77 | 5 | a decidir — candidata |
| 02.04.06.010-9 | CALCANEO ESQUERDO (PERFIL E AXIAL) | 27 | 58 | 54 | 03/05/2021 | 27 | 19 | 3 | a decidir — candidata |
| 02.04.06.010-9 | CALCANEO DIREITO (PERFIL E AXIAL) | 24 | 55 | 58 | 01/09/2022 | 24 | 19 | 2 | a decidir — candidata |
| 02.04.06.010-9 | CALCANEO DIREITO | 17 | 51 | 52 | 03/05/2022 | 17 | 2 | 3 | a decidir — candidata |
| 02.04.06.010-9 | CALCANEO ESQUERDO | 11 | 44 | 65 | 24/03/2026 | 11 | 2 | 1 | a decidir — fila aberta em 2026 (desde 24/03/2026) |
| 02.04.06.012-5 | JOELHO ESQUERDO (AP E PERFIL) | 85 | 101 | 58 | 02/02/2021 | 85 | 55 | 6 | a decidir — candidata |
| 02.04.06.012-5 | JOELHO DIREITO (AP E PERFIL) | 84 | 96 | 60,5 | 05/04/2022 | 84 | 60 | 4 | a decidir — candidata |
| 02.04.06.012-5 | JOELHO : AP + LATERAL DIREITO | 70 | 52 | 58 | 27/09/2022 | 70 | 15 | 7 | a decidir — candidata |
| 02.04.06.012-5 | JOELHO : AP + LATERAL ESQUERDO | 51 | 48 | 60 | 10/05/2022 | 51 | 11 | 7 | a decidir — candidata |
| 02.04.06.013-3 | JOELHO OU ROTULA - AP + LAT. + AXIAL DIREITO | 57 | 66 | 53 | 23/08/2022 | 57 | 10 | 4 | a decidir — candidata |
| 02.04.06.013-3 | JOELHO OU ROTULA - AP + LAT. + AXIAL ESQUERDO | 42 | 61 | 53,5 | 29/11/2022 | 42 | 8 | 4 | a decidir — candidata |
| 02.04.06.013-3 | JOELHO OU ROTULA DIREITO - AP + PERFIL + AXIAL | 13 | 54 | 51 | 04/05/2026 | 13 | 16 | 1 | a decidir — fila aberta em 2026 (desde 04/05/2026) |
| 02.04.06.013-3 | JOELHO OU ROTULA ESQUERDO - AP + PERFIL + AXIAL | 11 | 36 | 52 | 20/07/2026 | 11 | 15 | 1 | a decidir — fila aberta em 2026 (desde 20/07/2026) |
| 20406015 (malformado) | RADIOGRAFIA DE PE/DEDOS DO PE | 11 | 107 | 58 | 31/03/2022 | 11 | 101 | 1 | a decidir — candidata |
| 02.04.06.015-0 | PE OU PODODACTILOS DIREITO | 69 | 53 | 50 | 29/09/2020 | 69 | 12 | 2 | a decidir — candidata |
| 02.04.06.015-0 | PE OU PODODACTILOS DIREITO (AP E OBLIQUO) | 67 | 98 | 56 | 29/09/2020 | 67 | 47 | 5 | a decidir — candidata |
| 02.04.06.015-0 | PE OU PODODACTILOS ESQUERDO | 56 | 40 | 54 | 29/09/2020 | 56 | 10 | 6 | a decidir — candidata |
| 02.04.06.015-0 | PE OU PODODACTILOS ESQUERDO (AP E OBLIQUO) | 48 | 124 | 56 | 20/01/2022 | 48 | 49 | 3 | a decidir — candidata |
| 02.04.06.015-0 | PE OU PODODACTILOS | 10 | 154 | 47 | 26/01/2021 | 10 | 1 | 0 | a decidir — candidata |
| 02.04.06.016-8 | PERNA ESQUERDA (AP E PERFIL) | 24 | 82 | 47 | 28/03/2022 | 24 | 12 | 4 | a decidir — candidata |
| 02.04.06.016-8 | PERNA DIREITA (AP E PERFIL) | 22 | 101 | 34 | 03/05/2021 | 22 | 11 | 1 | a decidir — candidata |
| 02.04.06.017-6 | PANORAMICA DE MEMBROS INFERIORES | 14 | 103 | 5,5 | 20/01/2021 | 14 | 1 | 0 | a decidir — candidata |
| 02.05.01.001-6 | 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO | 60 | 24 | 67 | 02/01/2020 | 60 | 63 | 14 | a decidir — candidata |
| 02.05.01.003-2 | 9. ECOCARDIOGRAFIA FETAL | 54 | 23 | 27,5 | 23/04/2020 | 53 | 66 | 5 | a decidir — candidata |
| 02.05.01.005-9 | ECOGRAFIA DOPPLER FLUXO OBSTETRICO | 14 | 98 | 32 | 28/02/2020 | 14 | 1 | 0 | a decidir — candidata |
| 02.05.02.006-2 | USG PE ESQUERDO | 95 | 499 | 54 | 24/01/2020 | 43 | 6 | 18 | a decidir — candidata |
| 02.05.02.006-2 | ULTRASSONOGRAFIA CERVICAL | 89 | 362 | 46 | 16/02/2023 | 44 | 14 | 12 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO COXO-FEMURAL E INFANTIL | 83 | 415 | 1 | 18/02/2021 | 33 | 1 | 1 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO COXO-FEMURAL D INFANTIL | 76 | 362 | 1 | 24/02/2022 | 36 | 1 | 1 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DA REGIAO LOMBAR | 54 | 456 | 2 | 10/10/2023 | 19 | 0 | 6 | a decidir — candidata |
| 02.05.02.006-2 | USG BRACO ESQUERDO | 50 | 1.167 | 61,5 | 12/05/2022 | 4 | 1 | 8 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO COXO-FEMURAL D ADULTO | 48 | 538 | 59 | 16/03/2020 | 21 | 3 | 6 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA PELVICA | 46 | 77 | 45,5 | 18/01/2023 | 46 | 2 | 14 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO COXO-FEMURAL E ADULTO | 40 | 554 | 58 | 05/02/2020 | 22 | 1 | 5 | a decidir — candidata |
| 02.05.02.006-2 | USG BRACO DIREITO | 28 | 990 | 62,5 | 22/09/2020 | 5 | 2 | 6 | a decidir — candidata |
| 02.05.02.006-2 | USG PERNA ESQUERDA | 26 | 532 | 53,5 | 20/10/2020 | 14 | 1 | 4 | a decidir — candidata |
| 02.05.02.006-2 | USB AXILA DIREITA | 23 | 609 | 43 | 06/03/2024 | 2 | 0 | 6 | a decidir — candidata |
| 02.05.02.006-2 | USG AXILA ESQUERDA | 20 | 648 | 54,5 | 25/02/2021 | 0 | 0 | 4 | fica fora — resíduo: nenhuma solicitação nem agendamento em 2026 |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO JOELHO D INFANTIL | 18 | 578 | 13 | 10/02/2020 | 7 | 1 | 1 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | 17 | 409 | 56 | 08/02/2023 | 8 | 1 | 6 | a decidir — candidata |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DO DEDO | 16 | 618 | 59 | 15/06/2023 | 4 | 0 | 2 | a decidir — candidata |
| 02.05.02.006-2 | USG PERNA DIREITA | 16 | 559 | 62,5 | 21/08/2020 | 5 | 0 | 3 | a decidir — candidata |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE ARTICULACAO JOELHO E INFANTIL | 15 | 522 | 12 | 12/03/2021 | 8 | 1 | 0 | a decidir — faixa etária infantil |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DO CALCANEO | 15 | 407 | 53 | 14/02/2023 | 6 | 0 | 6 | a decidir — candidata |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DAS GLANDULAS SUBMANDIBULARES | 12 | 190 | 50 | 07/03/2023 | 9 | 1 | 1 | a decidir — candidata |
| 02.05.02.007-0 | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DA BOLSA ESCROTAL | 18 | 394 | 33,5 | 25/06/2024 | 8 | 0 | 6 | a decidir — candidata |
| 02.05.02.007-0 | ULTRASSONOGRAFIA␣␣COM DOPPLER COLORIDO DOS TESTICULOS | 11 | 368 | 47 | 15/02/2023 | 4 | 0 | 2 | a decidir — candidata |
| 02.05.02.011-9 | ECOGRAFIA␣␣PROSTATA ( VIA TRANSRETAL) | 20 | 121 | 66 | 07/01/2020 | 20 | 0 | 4 | a decidir — candidata |
| 02.05.02.013-5 | ECOGRAFIA DE TORAX (EXTRACARDIACO) ADULTO | 13 | 665 | 57 | 27/01/2020 | 5 | 0 | 2 | a decidir — candidata |
| 02.05.02.014-3 | ECOGRAFIA MORFOLOGICA DO 1° TRIMESTRE | 69 | 252 | 28 | 04/07/2023 | 46 | 3 | 5 | a decidir — candidata |
| 02.05.02.014-3 | ECOGRAFIA OBSTETRICA MORFOLOGICA | 66 | 134 | 27 | 22/08/2007 | 65 | 9 | 1 | a decidir — candidata |
| 02.06.01.001-0 | 007. TC COLUNA CERVICAL ADULTO C/CONTRASTE S/SEDACAO | 69 | 105 | 57 | 10/01/2020 | 69 | 16 | 39 | a decidir — candidata |
| 02.06.01.001-0 | TC␣␣COLUNA CERVICAL ADULTO S/CONTRASTE S/SEDACAO EMERG. | 33 | 278 | 57 | 24/09/2024 | 20 | 10 | 4 | a decidir — fila de emergência |
| 02.06.01.001-0 | TC COLUNA CERVICAL ADULTO C/CONTRASTE S/SEDACAO EMERG. | 21 | 360 | 59 | 21/10/2024 | 10 | 6 | 1 | a decidir — fila de emergência |
| 02.06.01.001-0 | 005. TC COLUNA CERVICAL ADULTO S/CONTRASTE S/SEDACAO | 12 | 12 | 54,5 | 28/01/2020 | 12 | 96 | 2 | a decidir — candidata |
| 02.06.01.002-8 | TC COLUNA LOMBO-SACRA ADULTO S/CONTRASTE S/SEDACAO EMERG. | 54 | 334 | 56,5 | 23/09/2024 | 25 | 16 | 6 | a decidir — fila de emergência |
| 02.06.01.002-8 | 023. TC COLUNA LOMBO-SACRA ADULTO C/CONTRASTE S/SEDACAO | 50 | 118 | 55,5 | 03/01/2020 | 50 | 17 | 21 | a decidir — candidata |
| 02.06.01.002-8 | 021. TC COLUNA LOMBO-SACRA ADULTO S/CONTRASTE S/SEDACAO | 34 | 11 | 54 | 28/01/2020 | 34 | 241 | 4 | a decidir — candidata |
| 02.06.01.002-8 | TC␣␣COLUNA LOMBO-SACRA ADULTO C/CONTRASTE S/SEDACAO EMERG. | 23 | 472 | 59 | 26/09/2024 | 6 | 8 | 0 | a decidir — fila de emergência |
| 02.06.01.003-6 | 015. TC COLUNA DORSAL ADULTO C/CONTRASTE S/SEDACAO | 28 | 124 | 57,5 | 20/05/2020 | 28 | 9 | 13 | a decidir — candidata |
| 02.06.01.003-6 | TC␣␣COLUNA DORSAL␣␣ADULTO S/CONTRASTE S/SEDACAO␣␣EMERG. | 27 | 278 | 55 | 02/10/2024 | 17 | 8 | 1 | a decidir — fila de emergência |
| 02.06.01.003-6 | 013. TC COLUNA DORSAL ADULTO S/CONTRASTE S/SEDACAO | 11 | 7 | 64 | 09/01/2020 | 11 | 75 | 2 | a decidir — candidata |
| 02.06.01.004-4 | 071. TC DE FACE ADULTO C/CONTRASTE S/SEDACAO | 86 | 125 | 58 | 21/01/2020 | 85 | 18 | 34 | a decidir — candidata |
| 02.06.01.004-4 | 079. TC DE SEIOS DE FACE ADULTO C/CONTRASTE S/SEDACAO | 51 | 106 | 56 | 24/04/2020 | 50 | 13 | 20 | a decidir — candidata |
| 02.06.01.004-4 | 095. TC DE MASTOIDES ADULTO C/CONTRASTE S/SEDACAO | 28 | 94 | 54,5 | 13/02/2020 | 28 | 11 | 3 | a decidir — candidata |
| 02.06.01.004-4 | 077. TC DE SEIOS DE FACE ADULTO S/CONTRASTE S/SEDACAO | 22 | 5 | 55,5 | 02/01/2020 | 22 | 188 | 3 | a decidir — candidata |
| 02.06.01.004-4 | 093. TC DE MASTOIDES ADULTO S/CONTRASTE S/SEDACAO | 20 | 5 | 57 | 19/02/2020 | 20 | 109 | 0 | a decidir — candidata |
| 02.06.01.004-4 | TC DE FACE ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO␣␣EMERGENCIA | 17 | 356 | 50 | 08/11/2024 | 7 | 2 | 3 | a decidir — fila de emergência |
| 02.06.01.004-4 | TC DE SEIOS DE FACE␣␣ADULTO S/CONTRASTE S/SEDACAO EMERG. | 13 | 323 | 40 | 05/12/2024 | 5 | 3 | 2 | a decidir — fila de emergência |
| 02.06.01.004-4 | 069. TC DE FACE ADULTO S/CONTRASTE S/SEDACAO | 11 | 4 | 44 | 01/07/2020 | 11 | 56 | 1 | a decidir — candidata |
| 02.06.01.004-4 | TC DE MASTOIDES INFANTIL␣␣S/CONTRASTE S/SEDACAO EMERGENCIA | 11 | 392 | 5 | 18/11/2024 | 4 | 0 | 0 | a decidir — fila de emergência; faixa etária infantil |
| 02.06.01.005-2 | TC␣␣DE PESCOCO ADULTO␣␣C/CONTRASTE / S/SEDACAO␣␣EMERGENCIA | 58 | 354 | 61 | 24/09/2024 | 30 | 9 | 8 | a decidir — fila de emergência |
| 02.06.01.005-2 | TC␣␣DE PESCOCO ADULTO␣␣S/CONTRASTE / S/SEDACAO EMERGENCIA | 29 | 276 | 54 | 14/11/2024 | 18 | 2 | 3 | a decidir — fila de emergência |
| 02.06.01.006-0 | 047. TC DE ORBITAS ADULTO C/CONTRASTE S/SEDACAO | 16 | 85 | 53 | 29/04/2020 | 16 | 7 | 6 | a decidir — candidata |
| 02.06.01.006-0 | TC DE ORBITA INFANTIL C/CONTRASTE␣␣S/SEDACAO␣␣EMERG. | 10 | 343 | 10 | 16/06/2025 | 3 | 0 | 0 | a decidir — fila de emergência; faixa etária infantil |
| 02.06.01.007-9 | TC DE CRANIO INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 66 | 337 | 2 | 16/10/2024 | 29 | 4 | 0 | a decidir — fila de emergência; faixa etária infantil |
| 02.06.01.007-9 | TC DE CRANIO INFANTIL C/CONTRASTE S/SEDACAO EMERGENCIA | 24 | 316 | 7 | 25/03/2025 | 10 | 1 | 0 | a decidir — fila de emergência; faixa etária infantil |
| 02.06.01.007-9 | 025. TC DE CRANIO INFANTIL S/CONTRASTE S/SEDACAO | 11 | 5 | 7 | 24/01/2020 | 11 | 70 | 0 | a decidir — faixa etária infantil |
| 02.06.02.001-5 | ANGIOTOMOGRAFIA DOS MEMBROS SUPERIORES ESQUERDO ADULTO S/SEDACAO | 13 | 204 | 49 | 18/03/2024 | 10 | 2 | 3 | a decidir — candidata |
| 02.06.02.001-5 | TC ARTIC. OMBROS ADULTO S/CONTRASTE␣␣S/SEDACAO EMERG. | 13 | 408 | 51 | 20/10/2024 | 4 | 2 | 2 | a decidir — fila de emergência |
| 02.06.02.001-5 | TC ARTIC. COTOVELOS ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO EMERG. | 11 | 350 | 42 | 25/10/2024 | 4 | 1 | 0 | a decidir — fila de emergência |
| 02.06.02.002-3 | 263. TC DE PE ADULTO S/ CONTRASTE S/ SEDACAO | 23 | 39 | 48 | 24/03/2020 | 23 | 28 | 1 | a decidir — candidata |
| 02.06.02.002-3 | TC DE PERNA D ADULTO C/CONTRASTE␣␣S/SEDACAO␣␣EMERGENCIA | 14 | 359 | 40 | 05/12/2024 | 7 | 3 | 0 | a decidir — fila de emergência |
| 02.06.02.002-3 | 279. TC DE MAO ADULTO S/ CONTRASTE S/ SEDACAO | 13 | 43 | 47 | 05/06/2020 | 13 | 17 | 0 | a decidir — candidata |
| 02.06.02.002-3 | TC DE COXA D␣␣ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO␣␣EMERG. | 12 | 252 | 61,5 | 06/11/2024 | 10 | 1 | 1 | a decidir — fila de emergência |
| 02.06.02.002-3 | TC DE PERNA E␣␣ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO␣␣EMERGENCIA | 12 | 466 | 68,5 | 28/10/2024 | 2 | 1 | 1 | a decidir — fila de emergência |
| 02.06.02.002-3 | TC DE COXA E␣␣ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO␣␣EMERGENCIA | 11 | 272 | 66 | 06/11/2024 | 7 | 1 | 0 | a decidir — fila de emergência |
| 02.06.03.002-9 | ANGIOTOMOGRAFIA DOS MEMBROS INFERIORES DIREITO ADULTO S/SEDACAO | 40 | 230 | 63 | 22/04/2024 | 26 | 5 | 10 | a decidir — candidata |
| 02.06.03.002-9 | ANGIOTOMOGRAFIA DOS MEMBROS INFERIORES ESQUERDO ADULTO S/SEDACAO | 38 | 234 | 62 | 22/04/2024 | 23 | 5 | 8 | a decidir — candidata |
| 02.06.03.002-9 | TC ARTIC.JOELHOS ADULTO S/CONTRASTE S/SEDACAO EMERG. | 37 | 378 | 46 | 27/09/2024 | 15 | 2 | 1 | a decidir — fila de emergência |
| 02.06.03.002-9 | 255. TC DE TORNOZELO ADULTO S/ CONTRASTE S/ SEDACAO | 28 | 44 | 42 | 05/06/2020 | 28 | 28 | 3 | a decidir — candidata |
| 02.06.03.002-9 | TC DE PE ADULTO S/ CONTRASTE S/ SEDACAO | 19 | 399 | 55 | 17/10/2024 | 7 | 2 | 0 | a decidir — candidata |
| 02.06.03.002-9 | TC DE PE ADULTO C/ CONTRASTE S/ SEDACAO | 14 | 423 | 63,5 | 01/11/2024 | 2 | 3 | 1 | a decidir — candidata |
| 02.06.03.002-9 | TC DE TORNOZELO ADULTO S/ CONTRASTE S/ SEDACAO | 12 | 255 | 44 | 10/06/2025 | 6 | 3 | 1 | a decidir — candidata |
| 02.06.03.002-9 | 237. TC ARTIC. JOELHOS ADULTO S/CONTRASTE S/SEDACAO | 10 | 4 | 58,5 | 18/05/2020 | 10 | 66 | 1 | a decidir — candidata |
| 02.06.03.002-9 | 239. TC ARTIC. JOELHOS ADULTO C/CONTRASTE S/SEDACAO | 10 | 89 | 56,5 | 10/03/2020 | 10 | 3 | 3 | a decidir — candidata |
| 02.07.01.001-3 | ANGIORESSONANCIA CEREBRAL VENOSA | 65 | 41 | 47 | 14/04/2023 | 65 | 53 | 12 | a decidir — candidata |
| 02.07.01.001-3 | 300. ANGIORESSONANCIA DE VASOS CERVICAIS | 16 | 38 | 65,5 | 04/03/2020 | 16 | 13 | 3 | a decidir — candidata |
| 02.07.01.001-3 | ANGIORESSONANCIA DO PESCOCO | 16 | 43 | 51 | 10/08/2026 | 16 | 10 | 3 | a decidir — fila aberta em 2026 (desde 10/08/2026) |
| 02.07.01.001-3 | ANGIORESSONANCIA DO ABDOMEN | 11 | 25 | 39 | 14/09/2023 | 11 | 10 | 3 | a decidir — candidata |
| 02.07.01.002-1 | RM DE MASTOIDES ADULTO C/CONTRASTE S/SEDACAO | 48 | 25 | 54 | 30/06/2023 | 48 | 55 | 6 | a decidir — candidata |
| 02.07.01.002-1 | 304. RM DE SEIOS DA FACE ADULTO C/CONTRASTE S/SEDACAO | 30 | 22 | 58 | 10/02/2020 | 30 | 28 | 8 | a decidir — candidata |
| 02.07.01.002-1 | 013. RM DE ATM (BILATERAL) ADULTO␣␣S/CONTRASTE S/SEDACAO | 18 | 20 | 49,5 | 15/01/2020 | 18 | 21 | 6 | a decidir — candidata |
| 02.07.01.002-1 | RM DE MASTOIDES ADULTO S/CONTRASTE S/SEDACAO | 14 | 16 | 53 | 05/07/2023 | 14 | 15 | 0 | a decidir — candidata |
| 02.07.01.003-0 | RM DE PESCOCO ADULTO C/CONTRASTE S/SEDAÇÃO | 78 | 23 | 58 | 24/11/2025 | 78 | 55 | 20 | a decidir — candidata |
| 02.07.01.003-0 | RM DE PESCOCO ADULTO S/CONTRASTE S/SEDAÇÃO | 19 | 26 | 49 | 02/02/2026 | 19 | 11 | 3 | a decidir — fila aberta em 2026 (desde 02/02/2026) |
| 02.07.01.003-0 | RM DE ARTICULACAO COXO-FEMURAL DIREITA C/CONTRASTE S/SEDACAO | 15 | 20 | 56 | 14/11/2020 | 15 | 6 | 4 | a decidir — candidata |
| 02.07.01.003-0 | 022. RM DA COLUNA CERVICAL ADULTO S/CONTRASTE C/SEDACAO | 14 | 29 | 55,5 | 18/01/2020 | 14 | 9 | 3 | a decidir — candidata |
| 02.07.01.003-0 | RM DE ARTICUACAO COXO-FEMURAL ESQUERDA C/CONTRASTE S/SEDACAO | 11 | 24 | 57 | 01/09/2026 | 11 | 6 | 3 | a decidir — fila aberta em 2026 (desde 01/09/2026) |
| 02.07.01.004-8 | 038. RM DA COLUNA LOMBO-SACRA ADULTO S/CONTRASTE C/SEDACAO | 36 | 38 | 52 | 14/01/2020 | 35 | 17 | 2 | a decidir — candidata |
| 02.07.01.004-8 | 033. RM DA COLUNA LOMBO-SACRA INFANTIL S/CONTRASTE S/SEDACAO | 14 | 17 | 27 | 05/02/2020 | 14 | 4 | 0 | a decidir — faixa etária infantil |
| 02.07.01.005-6 | 031. RM DA COLUNA DORSAL ADULTO C/CONTRASTE S/SEDACAO | 87 | 24 | 53 | 09/01/2020 | 87 | 131 | 18 | a decidir — candidata |
| 02.07.01.006-4 | 002. RM DE CRANIO INFANTIL S/CONTRASTE C/SEDACAO | 59 | 111 | 4 | 07/08/2019 | 57 | 77 | 0 | a decidir — faixa etária infantil |
| 02.07.01.006-4 | 001. RM DE CRANIO INFANTIL S/CONTRASTE S/SEDACAO | 36 | 31 | 8 | 07/01/2020 | 36 | 32 | 0 | a decidir — faixa etária infantil |
| 02.07.01.006-4 | 004. RM DE CRANIO INFANTIL C/CONTRASTE C/SEDACAO | 33 | 37 | 2 | 08/08/2019 | 33 | 62 | 0 | a decidir — faixa etária infantil |
| 02.07.01.006-4 | 008. RM DE CRANIO ADULTO C/CONTRASTE C/SEDACAO | 31 | 146 | 53 | 08/01/2020 | 28 | 26 | 2 | a decidir — candidata |
| 02.07.01.006-4 | 006. RM DE CRANIO ADULTO S/CONTRASTE C/SEDACAO | 29 | 54 | 57 | 03/01/2020 | 28 | 24 | 1 | a decidir — candidata |
| 02.07.01.006-4 | 003. RM DE CRANIO INFANTIL C/CONTRASTE S/SEDACAO | 24 | 25 | 12 | 10/01/2020 | 24 | 22 | 0 | a decidir — faixa etária infantil |
| 02.07.01.006-4 | RM DE ORBITAS ADULTO C/CONTRASTE S/SEDAÇÃO | 21 | 18 | 44 | 05/12/2025 | 21 | 25 | 3 | a decidir — candidata |
| 02.07.01.007-2 | RM DE SELA TURCICA ADULTO C/CONTRASTE S/SEDACAO | 80 | 24 | 46 | 11/02/2020 | 80 | 81 | 11 | a decidir — candidata |
| 02.07.01.007-2 | RM DE SELA TURCICA ADULTO S/CONTRASTE S/SEDACAO | 18 | 17 | 43,5 | 05/03/2020 | 18 | 17 | 4 | a decidir — candidata |
| 02.07.01.007-2 | RM DE SELA TURCICA INFANTIL S/CONTRASTE S/SEDACAO | 12 | 23 | 11,5 | 30/01/2020 | 12 | 6 | 0 | a decidir — faixa etária infantil |
| 02.07.01.007-2 | RM DE SELA TURCICA ADULTO C/CONTRASTE C/SEDACAO | 11 | 48 | 51 | 07/01/2020 | 11 | 3 | 0 | a decidir — candidata |
| 02.07.01.007-2 | RM DE SELA TURCICA INFANTIL C/CONTRASTE S/SEDACAO | 10 | 65 | 9 | 20/02/2020 | 9 | 11 | 0 | a decidir — faixa etária infantil |
| 02.07.02.001-9 | 262. RM DO CORACAO OU AORTA ADULTO S/CONTRASTE S/SEDACAO | 80 | 67 | 57 | 09/01/2020 | 80 | 63 | 21 | a decidir — candidata |
| 02.07.02.002-7 | 280. RM DE MAO D ADULTO S/CONTRASTE S/SEDACAO | 62 | 16 | 53,5 | 02/01/2020 | 62 | 34 | 10 | a decidir — candidata |
| 02.07.02.002-7 | 109. RM DE PUNHO D ADULTO S/CONTRASTE S/SEDACAO | 55 | 18 | 52 | 25/05/2020 | 55 | 31 | 6 | a decidir — candidata |
| 02.07.02.002-7 | 117. RM DE PUNHO E ADULTO S/CONTRASTE S/SEDACAO | 48 | 20 | 52 | 16/06/2020 | 48 | 30 | 6 | a decidir — candidata |
| 02.07.02.002-7 | 288. RM DE MAO E ADULTO S/CONTRASTE S/SEDACAO | 46 | 18 | 55 | 13/08/2020 | 46 | 26 | 8 | a decidir — candidata |
| 02.07.02.002-7 | 079. RM DE OMBRO D ADULTO C/CONTRASTE S/SEDACAO | 26 | 27 | 55 | 11/02/2020 | 26 | 18 | 5 | a decidir — candidata |
| 02.07.02.002-7 | 282. RM DE MAO D ADULTO C/CONTRASTE S/SEDACAO | 24 | 26 | 51,5 | 27/01/2020 | 24 | 11 | 0 | a decidir — candidata |
| 02.07.02.002-7 | 221. RM DE COXA E ADULTO S/CONTRASTE S/SEDACAO | 19 | 18 | 49 | 03/01/2020 | 19 | 23 | 1 | a decidir — candidata |
| 02.07.02.002-7 | 231. RM DE PERNA D ADULTO C/CONTRASTE S/SEDACAO | 19 | 20 | 52 | 14/08/2020 | 19 | 17 | 4 | a decidir — candidata |
| 02.07.02.002-7 | 093. RM DE COTOVELO D ADULTO S/CONTRASTE S/SEDACAO | 18 | 14 | 46 | 10/12/2020 | 18 | 19 | 3 | a decidir — candidata |
| 02.07.02.002-7 | 223. RM DE COXA E ADULTO␣␣C/CONTRASTE S/SEDACAO | 18 | 23 | 46 | 05/03/2020 | 18 | 15 | 2 | a decidir — candidata |
| 02.07.02.002-7 | 290. RM DE MAO E ADULTO C/CONTRASTE S/SEDACAO | 18 | 31 | 49,5 | 01/06/2021 | 18 | 10 | 3 | a decidir — candidata |
| 02.07.02.002-7 | 087. RM DE OMBRO E ADULTO C/CONTRASTE S/SEDACAO | 17 | 26 | 56 | 02/01/2020 | 17 | 14 | 4 | a decidir — candidata |
| 02.07.02.002-7 | 237. RM DE PERNA E ADULTO S/CONTRASTE S/SEDACAO | 17 | 18 | 57 | 17/02/2020 | 17 | 25 | 2 | a decidir — candidata |
| 02.07.02.002-7 | 111. RM DE PUNHO D ADULTO C/CONTRASTE S/SEDACAO | 16 | 28 | 47 | 17/11/2020 | 16 | 9 | 0 | a decidir — candidata |
| 02.07.02.002-7 | 181. RM DE BRACO D ADULTO S/CONTRASTE S/SEDACAO | 16 | 16 | 43,5 | 27/02/2020 | 16 | 21 | 3 | a decidir — candidata |
| 02.07.02.002-7 | 213. RM DE COXA D ADULTO S/CONTRASTE S/SEDACAO | 16 | 23 | 48 | 08/01/2020 | 16 | 22 | 4 | a decidir — candidata |
| 02.07.02.002-7 | 239. RM DE PERNA E ADULTO C/CONTRASTE S/SEDACAO | 16 | 24 | 54,5 | 03/01/2020 | 16 | 15 | 3 | a decidir — candidata |
| 02.07.02.002-7 | 101. RM DE COTOVELO E ADULTO S/CONTRASTE S/SEDACAO | 15 | 15 | 48 | 03/09/2021 | 15 | 13 | 1 | a decidir — candidata |
| 02.07.02.002-7 | 119. RM DE PUNHO E ADULTO C/CONTRASTE S/SEDACAO | 15 | 24 | 45 | 13/04/2021 | 15 | 7 | 1 | a decidir — candidata |
| 02.07.02.002-7 | 189. RM DE BRACO E ADULTO S/CONTRASTE S/SEDACAO | 13 | 16 | 44 | 19/02/2020 | 13 | 18 | 2 | a decidir — candidata |
| 02.07.02.002-7 | 215. RM DE COXA D ADULTO C/CONTRASTE S/SEDACAO | 13 | 23 | 50 | 09/03/2020 | 13 | 15 | 1 | a decidir — candidata |
| 02.07.02.002-7 | 078. RM DE OMBRO D ADULTO S/CONTRASTE C/SEDACAO | 12 | 26 | 54 | 14/04/2020 | 12 | 3 | 3 | a decidir — candidata |
| 02.07.02.003-5 | 045. RM DE TORAX ADULTO S/CONTRASTE S/SEDACAO | 38 | 16 | 51 | 17/01/2020 | 38 | 52 | 10 | a decidir — candidata |
| 02.07.02.003-5 | 047. RM DE TORAX ADULTO C/CONTRASTE S/SEDACAO | 34 | 25 | 58 | 14/01/2020 | 34 | 41 | 8 | a decidir — candidata |
| 02.07.02.006-0 | 311. RM DE MAMA BILATERAL | 84 | 21 | 50 | 22/09/2021 | 83 | 162 | 22 | a decidir — candidata |
| 02.07.03.001-4 | 053. RM DE ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 82 | 16 | 49 | 22/04/2019 | 82 | 117 | 12 | a decidir — candidata |
| 02.07.03.002-2 | 067. RM DE BACIA OU PELVIS INFANTIL C/CONTRASTE S/SEDACAO | 22 | 23 | 39,5 | 23/04/2020 | 22 | 9 | 0 | a decidir — faixa etária infantil |
| 02.07.03.002-2 | 072. RM DE BACIA OU PELVIS ADULTO C/CONTRASTE C/SEDACAO | 19 | 116 | 41,5 | 09/01/2020 | 18 | 15 | 2 | a decidir — candidata |
| 02.07.03.003-0 | 149. RM DE TORNOZELO D ADULTO S/CONTRASTE S/SEDACAO | 75 | 18 | 51 | 03/02/2020 | 75 | 57 | 4 | a decidir — candidata |
| 02.07.03.003-0 | 173. RM DE PE E␣␣ADULTO S/CONTRASTE S/SEDACAO | 68 | 15 | 53 | 30/01/2020 | 68 | 61 | 14 | a decidir — candidata |
| 02.07.03.003-0 | 165. RM DE PE D ADULTO S/CONTRASTE S/SEDACAO | 60 | 16 | 52 | 14/01/2020 | 60 | 58 | 10 | a decidir — candidata |
| 02.07.03.003-0 | RM DE ARTICULACAO COXO-FEMURAL ESQUERDA S/ CONTRASTE S/ SEDACAO | 55 | 23 | 53 | 09/11/2020 | 55 | 28 | 8 | a decidir — candidata |
| 02.07.03.003-0 | 157. RM DE TORNOZELO E ADULTO S/CONTRASTE S/SEDACAO | 54 | 17 | 53 | 15/01/2020 | 54 | 54 | 6 | a decidir — candidata |
| 02.07.03.003-0 | RM DE ARTICULACAO COXO -FERMURAL DIREITA S/ CONTRASTE S/ SEDACAO | 50 | 26 | 55 | 27/11/2020 | 50 | 29 | 3 | a decidir — candidata |
| 02.07.03.003-0 | 143. RM DE JOELHO E ADULTO C/CONTRASTE S/SEDACAO | 32 | 27 | 52,5 | 21/10/2020 | 32 | 23 | 5 | a decidir — candidata |
| 02.07.03.003-0 | 135. RM DE JOELHO D ADULTO C/CONTRASTE S/SEDACAO | 31 | 26 | 50 | 20/01/2020 | 31 | 26 | 4 | a decidir — candidata |
| 02.07.03.003-0 | 229. RM DE PERNA D ADULTO S/CONTRASTE S/SEDACAO | 25 | 19 | 42 | 28/02/2020 | 25 | 26 | 4 | a decidir — candidata |
| 02.07.03.003-0 | 175. RM DE PE E ADULTO C/CONTRASTE S/SEDACAO | 23 | 22 | 62 | 10/03/2020 | 23 | 28 | 5 | a decidir — candidata |
| 02.07.03.003-0 | 167. RM DE PE D ADULTO C/CONTRASTE S/SEDACAO | 20 | 26 | 55,5 | 10/03/2020 | 20 | 30 | 3 | a decidir — candidata |
| 02.07.03.003-0 | 138. RM DE JOELHO E INFANTIL S/CONTRASTE S/SEDACAO | 12 | 26 | 12,5 | 04/10/2021 | 12 | 6 | 0 | a decidir — faixa etária infantil |
| 02.07.03.003-0 | 151. RM DE TORNOZELO D ADULTO C/CONTRASTE S/SEDACAO | 10 | 22 | 53 | 28/01/2020 | 10 | 9 | 1 | a decidir — candidata |
| 02.07.03.004-9 | 063. RM DE VIAS BILIARES ADULTO C/CONTRASTE S/SEDACAO | 46 | 27 | 57,5 | 27/03/2020 | 46 | 92 | 6 | a decidir — candidata |
| 02.07.03.004-9 | 061. RM DE VIAS BILIARES ADULTO S/CONTRASTE S/SEDACAO | 39 | 18 | 50 | 29/04/2020 | 39 | 187 | 5 | a decidir — candidata |
| 02.08.01.004-1 | CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE | 50 | 164 | 66,5 | 24/09/2025 | 43 | 1 | 11 | a decidir — candidata |
| 02.08.02.007-1 | CINTILOGRAFIA PARA ESVAZIAMENTO GÁSTRICO (SÓLIDOS/SEMI -SÓLIDOS) | 21 | 105 | 43 | 15/09/2025 | 21 | 1 | 4 | a decidir — candidata |
| 02.08.02.007-1 | CINTILOGRAFIA PARA ESVAZIAMENTO GÁSTRICO ( LIQUIDOS) | 13 | 170 | 57 | 03/10/2025 | 12 | 0 | 4 | a decidir — candidata |
| 02.08.03.002-6 | CINTILOGRAFIA DA TIREOIDE C/ OU S/ CAPTACAO | 33 | 22 | 57 | 08/07/2025 | 33 | 34 | 8 | a decidir — candidata |
| 02.08.03.004-2 | CINTILOGRAFIA P/ PESQUISA DO CORPO INTEIRO | 10 | 8 | 52 | 23/10/2025 | 10 | 9 | 1 | a decidir — candidata |
| 02.08.05.004-3 | CINTILOGRAFIA DE SEGMENTO OSSEO C/ GALIO 67 | 10 | 16 | 64 | 01/09/2026 | 10 | 1 | 7 | a decidir — fila aberta em 2026 (desde 01/09/2026) |
| 02.08.08.004-0 | LINFOCINTILOGRAFIA | 21 | 121 | 53 | 24/09/2025 | 20 | 3 | 9 | a decidir — candidata |
| 02.10.01.001-0 | ANGIOGRAFIA CEREBRAL (4 VASOS) | 11 | 20 | 61 | 09/01/2020 | 11 | 9 | 0 | a decidir — candidata |

**Filas com menos de 10 na fila**, por código. São 395 filas e 1.188 solicitações (soma das
linhas, calculado); cada uma está, com o estudo e a decisão, na aba 5 da planilha e em
`filas` no JSON.

| código | procedimento | filas com menos de 10 | fila (soma das linhas, calc.) | delas, resíduo: filas | resíduo: fila |
|---|---|---|---|---|---|
| 02.04.01.005-5 | Radiografia de articulacao temporo-mandibular bilateral | 1 | 1 | 0 | 0 |
| 02.04.01.006-3 | Radiografia de cavum (lateral + hirtz) | 2 | 9 | 1 | 2 |
| 02.04.01.007-1 | Radiografia de cranio (pa + lateral + oblíqua / bretton + hirtz) | 2 | 10 | 0 | 0 |
| 02.04.01.008-0 | Radiografia de cranio (pa + lateral) | 1 | 6 | 0 | 0 |
| 02.04.01.011-0 | Radiografia de maxilar (pa + obliqua) | 1 | 1 | 0 | 0 |
| 02.04.01.012-8 | Radiografia de ossos da face (mn + lateral + hirtz) | 2 | 5 | 0 | 0 |
| 02.04.01.014-4 | Radiografia de seios da face (fn + mn + lateral + hirtz) | 1 | 9 | 0 | 0 |
| 02.04.01.017-9 | Radiografia panoramica | 1 | 1 | 1 | 1 |
| 02.04.02.003-4 | Radiografia de coluna cervical (ap + lateral + to + obliquas) | 1 | 7 | 0 | 0 |
| 02.04.02.004-2 | Radiografia de coluna cervical (ap + lateral + to / flexao) | 1 | 8 | 0 | 0 |
| 02.04.02.005-0 | Radiografia de coluna cervical funcional / dinamica | 1 | 3 | 0 | 0 |
| 02.04.02.006-9 | Radiografia de coluna lombo-sacra | 2 | 16 | 0 | 0 |
| 02.04.02.007-7 | Radiografia de coluna lombo-sacra (c/ obliquas) | 5 | 26 | 0 | 0 |
| 02.04.02.008-5 | Radiografia de coluna lombo-sacra funcional / dinamica | 2 | 8 | 0 | 0 |
| 02.04.02.010-7 | Radiografia de coluna toraco-lombar | 1 | 2 | 0 | 0 |
| 02.04.02.011-5 | Radiografia de coluna toraco-lombar dinamica | 2 | 13 | 0 | 0 |
| 02.04.02.012-3 | Radiografia de regiao sacro-coccigea | 2 | 2 | 0 | 0 |
| 02.04.03.007-2 | Radiografia de costelas (por hemitorax) | 2 | 13 | 0 | 0 |
| 02.04.03.012-9 | Radiografia de torax (apico-lordortica) | 1 | 3 | 0 | 0 |
| 02.04.03.013-7 | Radiografia de tórax (pa + inspiração + expiração + lateral) | 1 | 7 | 0 | 0 |
| 02.04.03.014-5 | Radiografia de torax (pa + lateral + obliqua) | 1 | 4 | 0 | 0 |
| 02.04.04.001-9 | Radiografia de antebraco | 4 | 17 | 0 | 0 |
| 02.04.04.002-7 | Radiografia de articulacao acromio-clavicular | 2 | 2 | 0 | 0 |
| 02.04.04.003-5 | Radiografia de articulacao escapulo-umeral | 3 | 10 | 0 | 0 |
| 02.04.04.004-3 | Radiografia de articulacao esterno-clavicular | 1 | 1 | 0 | 0 |
| 02.04.04.005-1 | Radiografia de braco | 2 | 2 | 0 | 0 |
| 02.04.04.006-0 | Radiografia de clavicula | 3 | 8 | 0 | 0 |
| 02.04.04.007-8 | Radiografia de cotovelo | 2 | 2 | 0 | 0 |
| 02.04.04.008-6 | Radiografia de dedos da mao | 4 | 10 | 0 | 0 |
| 02.04.04.009-4 | Radiografia de mao | 1 | 9 | 0 | 0 |
| 02.04.04.010-8 | Radiografia de mao e punho (p/ determinacao de idade ossea) | 2 | 9 | 1 | 1 |
| 02.04.04.011-6 | Radiografia de escapula/ombro (tres posicoes) | 3 | 15 | 0 | 0 |
| 02.04.04.012-4 | Radiografia de punho (ap + lateral + obliqua) | 5 | 16 | 0 | 0 |
| 02.04.05.011-1 | Radiografia de abdomen (ap + lateral / localizada) | 2 | 2 | 0 | 0 |
| 02.04.05.013-8 | Radiografia de abdomen simples (ap) | 2 | 6 | 0 | 0 |
| 02.04.05.018-9 | Urografia venosa | 1 | 1 | 1 | 1 |
| 02.04.06.003-6 | Escanometria | 1 | 1 | 0 | 0 |
| 02.04.06.006-0 | Radiografia de articulacao coxo-femoral | 3 | 12 | 0 | 0 |
| 02.04.06.007-9 | Radiografia de articulacao sacro-iliaca | 1 | 1 | 0 | 0 |
| 02.04.06.008-7 | Radiografia de articulacao tibio-tarsica | 4 | 10 | 0 | 0 |
| 02.04.06.010-9 | Radiografia de calcaneo | 3 | 7 | 2 | 2 |
| 02.04.06.011-7 | Radiografia de coxa | 4 | 12 | 0 | 0 |
| 02.04.06.012-5 | Radiografia de joelho (ap + lateral) | 1 | 8 | 0 | 0 |
| 02.04.06.013-3 | Radiografia de joelho ou patela (ap + lateral + axial) | 2 | 3 | 0 | 0 |
| 20406014 (malformado) | (malformado) | 1 | 5 | 0 | 0 |
| 02.04.06.014-1 | Radiografia de joelho ou patela (ap + lateral + obliqua + 3 axiais) | 4 | 22 | 0 | 0 |
| 02.04.06.016-8 | Radiografia de perna | 2 | 14 | 0 | 0 |
| 02.05.01.002-4 | Ecocardiografia transesofagica | 2 | 5 | 1 | 1 |
| 02.05.01.003-2 | Ecocardiografia transtoracica | 4 | 5 | 4 | 5 |
| 02.05.01.004-0 | Ultrassonografia doppler colorido de vasos | 22 | 49 | 20 | 42 |
| 02.05.02.003-8 | Ultrassonografia de abdômen superior | 1 | 1 | 1 | 1 |
| 02.05.02.004-6 | Ultrassonografia de abdomen total | 1 | 3 | 1 | 3 |
| 02.05.02.005-4 | Ultrassonografia de aparelho urinário | 1 | 5 | 1 | 5 |
| 02.05.02.006-2 | Ultrassonografia de articulacao | 20 | 66 | 5 | 15 |
| 02.05.02.009-7 | Ultrassonografia mamaria bilateral | 2 | 2 | 2 | 2 |
| 02.05.02.010-0 | Ultrassonografia de prostata por via abdominal | 1 | 2 | 1 | 2 |
| 02.05.02.012-7 | Ultrassonografia de tireoide | 2 | 4 | 2 | 4 |
| 02.05.02.013-5 | Ultrassonografia de torax (extracardiaca) | 1 | 4 | 0 | 0 |
| 02.05.02.014-3 | Ultrassonografia obstetrica | 1 | 5 | 0 | 0 |
| 02.05.02.016-0 | Ultrassonografia pelvica (ginecologica) | 2 | 2 | 2 | 2 |
| 02.05.02.017-8 | Ultrassonografia transfontanela | 1 | 2 | 1 | 2 |
| 02.05.02.018-6 | Ultrassonografia transvaginal | 1 | 1 | 1 | 1 |
| 02.06.01.001-0 | Tomografia computadorizada de coluna cervical c/ ou s/ contraste | 3 | 6 | 1 | 1 |
| 02.06.01.002-8 | Tomografia computadorizada de coluna lombo-sacra c/ ou s/ contraste | 2 | 5 | 0 | 0 |
| 02.06.01.003-6 | Tomografia computadorizada de coluna toracica c/ ou s/ contraste | 1 | 9 | 0 | 0 |
| 02.06.01.004-4 | Tomografia computadorizada de face / seios da face / articulacoes temp | 18 | 45 | 2 | 3 |
| 02.06.01.005-2 | Tomografia computadorizada do pescoco | 6 | 15 | 0 | 0 |
| 02.06.01.006-0 | Tomografia computadorizada de sela turcica | 8 | 19 | 0 | 0 |
| 02.06.01.007-9 | Tomografia computadorizada do cranio | 6 | 17 | 0 | 0 |
| 02.06.02.001-5 | Tomografia computadorizada de articulacoes de membro superior | 12 | 35 | 0 | 0 |
| 02.06.02.002-3 | Tomografia computadorizada de segmentos apendiculares - (braco, antebr | 29 | 113 | 3 | 3 |
| 02.06.02.003-1 | Tomografia computadorizada de torax | 5 | 14 | 0 | 0 |
| 02.06.03.001-0 | Tomografia computadorizada de abdomen superior | 8 | 14 | 0 | 0 |
| 02.06.03.002-9 | Tomografia computadorizada de articulacoes de membro inferior | 13 | 37 | 2 | 4 |
| 02.06.03.003-7 | Tomografia computadorizada de pelve / bacia / abdomen inferior | 5 | 7 | 0 | 0 |
| 02.07.01.001-3 | Angioressonancia cerebral | 3 | 18 | 0 | 0 |
| 02.07.01.002-1 | Ressonancia magnetica de articulacao temporo-mandibular (bilateral) | 9 | 17 | 0 | 0 |
| 02.07.01.003-0 | Ressonancia magnetica de coluna cervical/pescoço | 10 | 23 | 0 | 0 |
| 02.07.01.004-8 | Ressonancia magnetica de coluna lombo-sacra | 4 | 9 | 0 | 0 |
| 02.07.01.005-6 | Ressonancia magnetica de coluna toracica | 5 | 11 | 0 | 0 |
| 02.07.01.006-4 | Ressonancia magnetica de cranio | 8 | 16 | 1 | 1 |
| 02.07.01.007-2 | Ressonancia magnetica de sela turcica | 2 | 5 | 0 | 0 |
| 02.07.02.001-9 | Ressonancia magnetica de coracao / aorta c/ cine | 5 | 16 | 0 | 0 |
| 02.07.02.002-7 | Ressonancia magnetica de membro superior (unilateral) | 30 | 72 | 0 | 0 |
| 02.07.02.003-5 | Ressonancia magnetica de torax | 3 | 8 | 0 | 0 |
| 02.07.03.001-4 | Ressonancia magnetica de abdomen superior | 4 | 13 | 0 | 0 |
| 02.07.03.002-2 | Ressonancia magnetica de bacia / pelve / abdomen inferior | 2 | 16 | 0 | 0 |
| 02.07.03.003-0 | Ressonancia magnetica de membro inferior (unilateral) | 23 | 66 | 1 | 1 |
| 02.07.03.004-9 | Ressonancia magnetica de vias biliares/colangiorressonancia | 2 | 7 | 0 | 0 |
| 02.08.02.005-5 | Cintilografia p/ estudo de transito esofagico (liquido) | 1 | 3 | 0 | 0 |
| 02.08.02.006-3 | Cintilografia p/ estudo de transito esofagico (semi-solido) | 1 | 5 | 0 | 0 |
| 02.08.02.008-0 | Cintilografia p/ pesquisa de diverticulose de meckel | 1 | 3 | 0 | 0 |
| 02.08.02.009-8 | Cintilografia p/ pesquisa de hemorragia digestiva ativa | 1 | 5 | 0 | 0 |
| 02.08.02.011-0 | Cintilografia p/ pesquisa de refluxo gastro-esofagico | 1 | 2 | 0 | 0 |
| 02.08.06.001-4 | Cintilografia de perfusao cerebral c/ talio (spcto) | 1 | 1 | 1 | 1 |
| 02.08.06.003-0 | Estudo de fluxo sanguineo cerebral | 1 | 4 | 0 | 0 |
| 02.08.07.002-8 | Cintilografia de pulmão p/ pesquisa de aspiração | 1 | 3 | 0 | 0 |
| 02.08.07.004-4 | Cintilografia de pulmao por perfusao (minimo 4 projecoes) | 1 | 8 | 0 | 0 |
| 02.08.09.001-0 | Cintilografia de corpo inteiro c/ galio 67 p/ pesquisa de neoplasias | 1 | 3 | 0 | 0 |
| 02.08.09.002-9 | Cintilografia de glandula lacrimal (dacriocintilografia) | 1 | 3 | 0 | 0 |
| **total** | | 395 | 1188 | 59 | 106 |

### 1.4 Outro código com nome de imagem

| código | nome interno | fila | pessoas | espera média | mediana | fila pedida em 2026 | agendadas/mês 2026 (calc.) | pessoas já no plano 4 | CIDs principais | decisão — nota |
|---|---|---|---|---|---|---|---|---|---|---|
| 02.11.06.028-3 | OCT GLAUCOMA | 2.296 | 2.296 | 218 | 212 | 1.536 | 53 | 296 | H40 1281; H401 421; H400 358 | a decidir — fora dos subgrupos de imagem: exame oftalmológico (02.11.06) |
| 02.11.06.028-3 | OCT | 1.523 | 1.523 | 326 | 349 | 643 | 31 | 192 | H35 560; H36 211; H353 157 | a decidir — fora dos subgrupos de imagem: exame oftalmológico (02.11.06) |
| 02.01.01.047-0 | PUNCAO ASPIRATIVA TIREOIDE TELEGUIADA | 521 | 520 | 86 | 83 | 520 | 48 | 84 | E04 127; E042 87; E041 58 | a decidir — fora dos subgrupos de imagem: punção ou biópsia guiada por imagem (02.01), não é exame de imagem |
| 02.11.06.001-1 | BIOMETRIA ULTRASSONICA | 459 | 459 | 62 | 58 | 459 | 154 | 52 | H25 334; H251 40; H26 29 | a decidir — fora dos subgrupos de imagem: exame oftalmológico (02.11.06) |
| 02.01.01.054-2 | PUNCAO DE MAMA POR AGULHA GROSSA (CORE BIOPSIA) GUIADA POR ULTRASSONOGRAFIA | 198 | 198 | 57 | 43 | 198 | 101 | 44 | N63 137; R92 17; D486 13 | a decidir — fora dos subgrupos de imagem: punção ou biópsia guiada por imagem (02.01), não é exame de imagem |
| 02.01.01.054-2 | PUNCAO DE MAMA POR AGULHA GROSSA (CORE BIOPSIA) GUIADA POR MAMOGRAFIA | 71 | 71 | 66 | 62 | 70 | 19 | 23 | N64 17; N63 13; R92 11 | a decidir — fora dos subgrupos de imagem: punção ou biópsia guiada por imagem (02.01), não é exame de imagem |
| 02.11.02.001-0 | CATETERISMO | 14 | 14 | 1 | 1 | 14 | 641 | 2 | I20 4; I25 3; I21 2 | a decidir — fora dos subgrupos de imagem: cateterismo cardíaco, hemodinâmica (02.11.02) |
| (sem código) | ORGAOS INTERNOS DO TORAX I | 1 | 1 | 122 | 122 | 1 | 0 | 0 | R13 1 | a decidir — fora dos subgrupos de imagem: sem código SIGTAP; grupo radiodiagnóstico do painel |
| (sem código) | ORGAOS INTERNOS DO TORAX II | 1 | 1 | 83 | 83 | 1 | 0 | 0 | R13 1 | a decidir — fora dos subgrupos de imagem: sem código SIGTAP; grupo radiodiagnóstico do painel |
| 02.01.01.058-5 | PUNCAO ASPIRATIVA DE MAMAS POR AGULHA FINA (PAAF) GUIADA POR ULTRASSONOGRAFIA | 1 | 1 | 1 | 1 | 1 | 24 | 0 | N63 1 | a decidir — fora dos subgrupos de imagem: punção ou biópsia guiada por imagem (02.01), não é exame de imagem |

As duas OCT juntas: 3.819 na fila e **3.700 pessoas** (motor). OCT e biometria ultrassônica
são exames de oftalmologia (02.11.06); as punções e biópsias são procedimentos guiados por
imagem (02.01), não exames de imagem. O cateterismo tem fila pequena (14) e muita oferta (641
agendados por mês).

## 2. Fila por código SIGTAP — candidatas

Códigos dos subgrupos de imagem fora dos onze do plano 4, **sem as filas-resíduo**, por
modalidade e em ordem decrescente de fila. Uma linha por código, no motor (pessoas distintas
dentro do código). A linha da modalidade é o conjunto no motor, não a soma das linhas. As
agendadas são por `codigo_sigtap_agendamento` (campo que responde e não está na lista do
método). Todas as linhas e as colunas de idade, 1ª solicitação e resíduo estão na aba 1.

**Radiologia** (57 códigos)

| código | procedimento (SIGTAP) | nomes | fila | pessoas | devolvidas | espera média | mediana | agendadas/mês 2026 (calc.) | pessoas já no plano 4 |
|---|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | 2 | 6.461 | 6.458 | 2.801 | 49 | 28 | 4.682 | 1.180 |
| 02.04.06.002-8 | Densitometria ossea duo-energetica de coluna (vertebras lombares e/ou femur) | 1 | 2.196 | 2.196 | 3.620 | 44 | 35 | 980 | 444 |
| 02.04.01.017-9 | Radiografia panoramica | 3 | 1.653 | 1.638 | 3.003 | 100 | 31 | 1.397 | 115 |
| 02.04.01.018-7 | Radiografia peri-apical interproximal (bite-wing) | 1 | 706 | 706 | 673 | 24 | 21 | 769 | 53 |
| 02.04.03.015-3 | Radiografia de torax (pa e perfil) | 1 | 662 | 662 | 187 | 95 | 94 | 1.099 | 78 |
| 02.04.06.012-5 | Radiografia de joelho (ap + lateral) | 5 | 298 | 209 | 76 | 81 | 69 | 245 | 17 |
| 02.04.04.009-4 | Radiografia de mao | 8 | 288 | 179 | 73 | 82 | 66 | 202 | 18 |
| 02.04.02.006-9 | Radiografia de coluna lombo-sacra | 6 | 281 | 258 | 94 | 105 | 101 | 308 | 15 |
| 02.04.06.015-0 | Radiografia de pe / dedos do pe | 5 | 250 | 183 | 48 | 80 | 56 | 119 | 12 |
| 02.04.04.010-8 | Radiografia de mao e punho (p/ determinacao de idade ossea) | 4 | 150 | 144 | 46 | 94 | 81 | 178 | 1 |
| 02.04.01.006-3 | Radiografia de cavum (lateral + hirtz) | 3 | 141 | 140 | 15 | 99 | 93 | 206 | 0 |
| 02.04.02.003-4 | Radiografia de coluna cervical (ap + lateral + to + obliquas) | 3 | 136 | 136 | 29 | 105 | 91 | 118 | 14 |
| 02.04.04.012-4 | Radiografia de punho (ap + lateral + obliqua) | 9 | 131 | 88 | 45 | 93 | 86 | 88 | 7 |
| 02.04.06.013-3 | Radiografia de joelho ou patela (ap + lateral + axial) | 6 | 126 | 98 | 11 | 62 | 65 | 124 | 7 |
| 02.04.02.009-3 | Radiografia de coluna toracica (ap + lateral) | 5 | 122 | 117 | 40 | 109 | 99 | 95 | 9 |
| 02.04.04.011-6 | Radiografia de escapula/ombro (tres posicoes) | 7 | 85 | 71 | 19 | 97 | 91 | 129 | 2 |
| 02.04.06.010-9 | Radiografia de calcaneo | 5 | 84 | 70 | 13 | 60 | 35 | 74 | 8 |
| 02.04.06.009-5 | Radiografia de bacia | 2 | 81 | 78 | 38 | 87 | 84 | 82 | 8 |
| 02.04.06.008-7 | Radiografia de articulacao tibio-tarsica | 6 | 60 | 40 | 23 | 94 | 84 | 49 | 4 |
| 02.04.06.016-8 | Radiografia de perna | 4 | 60 | 48 | 16 | 93 | 79 | 54 | 5 |
| 02.04.02.007-7 | Radiografia de coluna lombo-sacra (c/ obliquas) | 6 | 57 | 56 | 17 | 94 | 83 | 16 | 5 |
| 02.04.06.006-0 | Radiografia de articulacao coxo-femoral | 6 | 56 | 46 | 13 | 64 | 43 | 55 | 2 |
| 02.04.04.007-8 | Radiografia de cotovelo | 4 | 38 | 28 | 13 | 92 | 70 | 32 | 3 |
| 02.04.01.014-4 | Radiografia de seios da face (fn + mn + lateral + hirtz) | 3 | 34 | 34 | 29 | 112 | 103 | 85 | 3 |
| 02.04.02.013-1 | Radiografia panoramica de coluna total- telespondilografia ( p/ escoliose) | 1 | 34 | 34 | 13 | 12 | 9 | 116 | 4 |
| 02.04.04.005-1 | Radiografia de braco | 4 | 33 | 27 | 5 | 59 | 41 | 22 | 2 |
| 02.04.02.010-7 | Radiografia de coluna toraco-lombar | 3 | 31 | 30 | 8 | 89 | 80 | 38 | 2 |
| 02.04.06.014-1 | Radiografia de joelho ou patela (ap + lateral + obliqua + 3 axiais) | 4 | 22 | 18 | 4 | 99 | 87 | 1 | 1 |
| 02.04.04.001-9 | Radiografia de antebraco | 4 | 17 | 13 | 3 | 109 | 127 | 14 | 2 |
| 02.04.06.017-6 | Radiografia panoramica de membros inferiores | 1 | 14 | 14 | 5 | 103 | 87 | 1 | 0 |
| 02.04.02.011-5 | Radiografia de coluna toraco-lombar dinamica | 2 | 13 | 13 | 2 | 92 | 71 | 2 | 0 |
| 02.04.03.007-2 | Radiografia de costelas (por hemitorax) | 2 | 13 | 12 | 4 | 48 | 15 | 18 | 2 |
| 02.04.06.011-7 | Radiografia de coxa | 4 | 12 | 10 | 6 | 52 | 23 | 15 | 2 |
| 20406015 (malformado) | (sem descrição: código malformado) | 1 | 11 | 11 | 8 | 107 | 101 | 101 | 1 |
| 02.04.03.017-0 | Radiografia de torax (pa) | 1 | 11 | 11 | 7 | 4.427 | 6.038 | 3 | 0 |
| 02.04.01.007-1 | Radiografia de cranio (pa + lateral + oblíqua / bretton + hirtz) | 2 | 10 | 10 | 1 | 74 | 85 | 2 | 1 |
| 02.04.04.008-6 | Radiografia de dedos da mao | 4 | 10 | 10 | 4 | 91 | 73 | 11 | 1 |
| 02.04.04.003-5 | Radiografia de articulacao escapulo-umeral | 3 | 10 | 10 | 2 | 49 | 27 | 9 | 1 |
| 02.04.02.008-5 | Radiografia de coluna lombo-sacra funcional / dinamica | 2 | 8 | 8 | 1 | 88 | 82 | 2 | 0 |
| 02.04.02.004-2 | Radiografia de coluna cervical (ap + lateral + to / flexao) | 1 | 8 | 8 | 4 | 111 | 110 | 4 | 1 |
| 02.04.04.006-0 | Radiografia de clavicula | 3 | 8 | 8 | 4 | 47 | 30 | 8 | 1 |
| 02.04.03.013-7 | Radiografia de tórax (pa + inspiração + expiração + lateral) | 1 | 7 | 7 | 1 | 99 | 80 | 3 | 1 |
| 02.04.05.013-8 | Radiografia de abdomen simples (ap) | 2 | 6 | 6 | 8 | 64 | 27 | 15 | 3 |
| 02.04.01.008-0 | Radiografia de cranio (pa + lateral) | 1 | 6 | 6 | 6 | 63 | 33 | 21 | 0 |
| 02.04.01.012-8 | Radiografia de ossos da face (mn + lateral + hirtz) | 2 | 5 | 5 | 2 | 92 | 86 | 3 | 0 |
| 20406014 (malformado) | (sem descrição: código malformado) | 1 | 5 | 5 | 3 | 79 | 52 | 0 | 1 |
| 02.04.03.014-5 | Radiografia de torax (pa + lateral + obliqua) | 1 | 4 | 4 | 1 | 41 | 49 | 2 | 0 |
| 02.04.03.012-9 | Radiografia de torax (apico-lordortica) | 1 | 3 | 3 | 0 | 37 | 41 | 1 | 1 |
| 02.04.02.005-0 | Radiografia de coluna cervical funcional / dinamica | 1 | 3 | 3 | 0 | 135 | 112 | 1 | 0 |
| 02.04.04.002-7 | Radiografia de articulacao acromio-clavicular | 2 | 2 | 2 | 4 | 111 | 111 | 10 | 0 |
| 02.04.02.012-3 | Radiografia de regiao sacro-coccigea | 2 | 2 | 2 | 5 | 80 | 80 | 10 | 0 |
| 02.04.05.011-1 | Radiografia de abdomen (ap + lateral / localizada) | 2 | 2 | 2 | 2 | 67 | 67 | 1 | 1 |
| 02.04.06.007-9 | Radiografia de articulacao sacro-iliaca | 1 | 1 | 1 | 1 | 65 | 65 | 9 | 0 |
| 02.04.06.003-6 | Escanometria | 1 | 1 | 1 | 2 | 140 | 140 | 21 | 0 |
| 02.04.04.004-3 | Radiografia de articulacao esterno-clavicular | 1 | 1 | 1 | 0 | 134 | 134 | 3 | 0 |
| 02.04.01.011-0 | Radiografia de maxilar (pa + obliqua) | 1 | 1 | 1 | 0 | 140 | 140 | 0 | 0 |
| 02.04.01.005-5 | Radiografia de articulacao temporo-mandibular bilateral | 1 | 1 | 1 | 0 | 27 | 27 | 6 | 0 |
| **radiologia** | **modalidade inteira, no motor** | 168 | **14.471** | **13.126** | 11.065 | 66 | 35 | 11.666 | 1.925 |

**Ultrassonografia** (14 códigos)

| código | procedimento (SIGTAP) | nomes | fila | pessoas | devolvidas | espera média | mediana | agendadas/mês 2026 (calc.) | pessoas já no plano 4 |
|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | Ecocardiografia transtoracica | 3 | 16.293 | 16.289 | 15.977 | 135 | 127 | 3.422 | 4.713 |
| 02.05.02.006-2 | Ultrassonografia de articulacao | 55 | 14.481 | 11.486 | 5.136 | 545 | 400 | 698 | 1.981 |
| 02.05.02.008-9 | Ultrassonografia de globo ocular / orbita (monocular) | 1 | 1.272 | 1.272 | 196 | 264 | 266 | 58 | 106 |
| 02.05.02.016-0 | Ultrassonografia pelvica (ginecologica) | 2 | 1.003 | 994 | 916 | 603 | 380 | 111 | 130 |
| 02.05.02.007-0 | Ultrassonografia de bolsa escrotal | 4 | 995 | 994 | 506 | 588 | 471 | 72 | 155 |
| 02.05.02.014-3 | Ultrassonografia obstetrica | 4 | 464 | 464 | 924 | 144 | 57 | 270 | 18 |
| 02.05.02.017-8 | Ultrassonografia transfontanela | 1 | 281 | 281 | 202 | 282 | 213 | 74 | 3 |
| 02.05.02.015-1 | Ultrassonografia obstetrica c/ doppler colorido e pulsado | 1 | 205 | 205 | 125 | 177 | 141 | 32 | 7 |
| 02.05.02.002-0 | Paquimetria ultrassônica | 1 | 164 | 164 | 247 | 22 | 19 | 167 | 18 |
| 02.05.01.001-6 | Ecocardiografia de estresse | 1 | 60 | 60 | 1.411 | 24 | 23 | 63 | 14 |
| 02.05.02.011-9 | Ultrassonografia de prostata (via transretal) | 1 | 20 | 20 | 133 | 121 | 117 | 0 | 4 |
| 02.05.02.013-5 | Ultrassonografia de torax (extracardiaca) | 2 | 17 | 17 | 13 | 693 | 749 | 0 | 2 |
| 02.05.01.005-9 | Ultrassonografia doppler de fluxo obstetrico | 1 | 14 | 14 | 33 | 98 | 117 | 1 | 0 |
| 02.05.01.002-4 | Ecocardiografia transesofagica | 1 | 4 | 4 | 1.018 | 100 | 6 | 98 | 1 |
| **ultrassonografia** | **modalidade inteira, no motor** | 78 | **35.273** | **31.682** | 26.837 | 335 | 189 | 5.066 | 6.934 |

**Tomografia** (11 códigos)

| código | procedimento (SIGTAP) | nomes | fila | pessoas | devolvidas | espera média | mediana | agendadas/mês 2026 (calc.) | pessoas já no plano 4 |
|---|---|---|---|---|---|---|---|---|---|
| 02.06.01.007-9 | Tomografia computadorizada do cranio | 14 | 1.467 | 1.440 | 2.739 | 197 | 120 | 1.285 | 291 |
| 02.06.01.005-2 | Tomografia computadorizada do pescoco | 10 | 755 | 746 | 657 | 139 | 115 | 209 | 418 |
| 02.06.01.004-4 | Tomografia computadorizada de face / seios da face / articulacoes temporo-mandibulares | 26 | 500 | 488 | 865 | 124 | 90 | 497 | 77 |
| 02.06.01.009-5 | Tomografia por emissão de pósitrons (pet-ct) | 1 | 424 | 424 | 819 | 162 | 128 | 42 | 112 |
| 02.06.03.002-9 | Tomografia computadorizada de articulacoes de membro inferior | 20 | 241 | 206 | 254 | 244 | 164 | 150 | 27 |
| 02.06.02.002-3 | Tomografia computadorizada de segmentos apendiculares - (braco, antebraço, mão, coxa, perna, pé) | 32 | 195 | 157 | 220 | 217 | 146 | 200 | 19 |
| 02.06.01.002-8 | Tomografia computadorizada de coluna lombo-sacra c/ ou s/ contraste | 6 | 166 | 164 | 360 | 221 | 136 | 285 | 31 |
| 02.06.01.001-0 | Tomografia computadorizada de coluna cervical c/ ou s/ contraste | 6 | 140 | 138 | 369 | 179 | 118 | 130 | 46 |
| 02.06.01.003-6 | Tomografia computadorizada de coluna toracica c/ ou s/ contraste | 4 | 75 | 74 | 153 | 199 | 148 | 97 | 16 |
| 02.06.02.001-5 | Tomografia computadorizada de articulacoes de membro superior | 15 | 72 | 69 | 101 | 255 | 179 | 89 | 8 |
| 02.06.01.006-0 | Tomografia computadorizada de sela turcica | 10 | 45 | 43 | 164 | 169 | 122 | 37 | 7 |
| **tomografia** | **modalidade inteira, no motor** | 144 | **4.080** | **3.401** | 6.701 | 178 | 120 | 3.022 | 865 |

**Ressonância magnética** (15 códigos)

| código | procedimento (SIGTAP) | nomes | fila | pessoas | devolvidas | espera média | mediana | agendadas/mês 2026 (calc.) | pessoas já no plano 4 |
|---|---|---|---|---|---|---|---|---|---|
| 02.07.03.002-2 | Ressonancia magnetica de bacia / pelve / abdomen inferior | 6 | 1.625 | 1.616 | 2.050 | 24 | 22 | 1.622 | 300 |
| 02.07.03.003-0 | Ressonancia magnetica de membro inferior (unilateral) | 37 | 1.491 | 1.142 | 1.770 | 19 | 17 | 1.407 | 155 |
| 02.07.01.006-4 | Ressonancia magnetica de cranio | 16 | 1.417 | 1.391 | 4.312 | 30 | 21 | 1.502 | 194 |
| 02.07.01.004-8 | Ressonancia magnetica de coluna lombo-sacra | 8 | 1.412 | 1.409 | 2.210 | 19 | 17 | 1.537 | 201 |
| 02.07.02.002-7 | Ressonancia magnetica de membro superior (unilateral) | 54 | 1.140 | 869 | 1.394 | 19 | 17 | 1.002 | 125 |
| 02.07.01.003-0 | Ressonancia magnetica de coluna cervical/pescoço | 17 | 758 | 742 | 1.210 | 20 | 17 | 788 | 115 |
| 02.07.03.001-4 | Ressonancia magnetica de abdomen superior | 6 | 752 | 749 | 1.096 | 25 | 23 | 921 | 161 |
| 02.07.01.001-3 | Angioressonancia cerebral | 8 | 287 | 220 | 464 | 39 | 42 | 224 | 41 |
| 02.07.01.005-6 | Ressonancia magnetica de coluna toracica | 7 | 266 | 265 | 605 | 20 | 17 | 380 | 45 |
| 02.07.02.001-9 | Ressonancia magnetica de coracao / aorta c/ cine | 7 | 258 | 255 | 728 | 63 | 58 | 157 | 53 |
| 02.07.01.007-2 | Ressonancia magnetica de sela turcica | 7 | 136 | 136 | 361 | 39 | 23 | 129 | 15 |
| 02.07.01.002-1 | Ressonancia magnetica de articulacao temporo-mandibular (bilateral) | 13 | 127 | 125 | 293 | 22 | 21 | 142 | 22 |
| 02.07.03.004-9 | Ressonancia magnetica de vias biliares/colangiorressonancia | 4 | 92 | 91 | 449 | 22 | 22 | 286 | 12 |
| 02.07.02.006-0 | Ressonância magnética da mama | 1 | 84 | 84 | 25 | 21 | 17 | 162 | 22 |
| 02.07.02.003-5 | Ressonancia magnetica de torax | 5 | 80 | 80 | 425 | 21 | 20 | 97 | 18 |
| **ressonância magnética** | **modalidade inteira, no motor** | 196 | **9.925** | **7.343** | 17.460 | 24 | 21 | 10.355 | 1.139 |

**Medicina nuclear** (23 códigos)

| código | procedimento (SIGTAP) | nomes | fila | pessoas | devolvidas | espera média | mediana | agendadas/mês 2026 (calc.) | pessoas já no plano 4 |
|---|---|---|---|---|---|---|---|---|---|
| 02.08.01.002-5 | Cintilografia de miocardio p/ avaliacao da perfusao em situacao de estresse (minimo 3 projecoes) | 1 | 1.825 | 1.825 | 65 | 276 | 337 | 32 | 383 |
| 02.08.05.003-5 | Cintilografia de ossos com ou sem fluxo sanguíneo (corpo inteiro) | 1 | 1.688 | 1.688 | 26 | 144 | 125 | 130 | 637 |
| 02.08.01.003-3 | Cintilografia de miocardio p/ avaliacao da perfusao em situacao de repouso (minimo 3 projecoes) | 1 | 1.505 | 1.505 | 32 | 281 | 364 | 29 | 303 |
| 02.08.04.010-2 | Estudo renal dinamico c/ ou s/ diuretico | 1 | 222 | 222 | 4 | 149 | 155 | 11 | 38 |
| 02.08.03.001-8 | Cintilografia de paratireoides | 1 | 189 | 189 | 10 | 176 | 170 | 17 | 37 |
| 02.08.04.005-6 | Cintilografia renal/renograma (qualitativa e/ou quantitativa) | 1 | 167 | 167 | 15 | 94 | 78 | 25 | 32 |
| 02.08.02.003-9 | Cintilografia de glandulas salivares c/ ou s/ estimulo | 1 | 122 | 122 | 3 | 121 | 103 | 5 | 20 |
| 02.08.01.004-1 | Cintilografia de miocardio p/ localizacao de necrose (minimo 3 projecoes ) | 1 | 50 | 50 | 2 | 164 | 148 | 1 | 11 |
| 02.08.02.007-1 | Cintilografia p/ estudo de transito gastrico | 2 | 34 | 30 | 1 | 130 | 108 | 1 | 8 |
| 02.08.03.002-6 | Cintilografia de tireóide com ou sem captação | 1 | 33 | 33 | 4 | 22 | 21 | 34 | 8 |
| 02.08.08.004-0 | Linfocintilografia | 1 | 21 | 21 | 2 | 121 | 143 | 3 | 9 |
| 02.08.03.004-2 | Cintilografia p/ pesquisa do corpo inteiro | 1 | 10 | 10 | 2 | 8 | 9 | 9 | 1 |
| 02.08.05.004-3 | Cintilografia de segmento osseo c/ galio 67 | 1 | 10 | 10 | 0 | 16 | 13 | 1 | 7 |
| 02.08.07.004-4 | Cintilografia de pulmao por perfusao (minimo 4 projecoes) | 1 | 8 | 8 | 35 | 56 | 12 | 12 | 1 |
| 02.08.02.006-3 | Cintilografia p/ estudo de transito esofagico (semi-solido) | 1 | 5 | 5 | 0 | 178 | 155 | 0 | 0 |
| 02.08.02.009-8 | Cintilografia p/ pesquisa de hemorragia digestiva ativa | 1 | 5 | 5 | 0 | 41 | 43 | 1 | 1 |
| 02.08.06.003-0 | Estudo de fluxo sanguineo cerebral | 1 | 4 | 4 | 0 | 121 | 133 | 1 | 0 |
| 02.08.07.002-8 | Cintilografia de pulmão p/ pesquisa de aspiração | 1 | 3 | 3 | 1 | 23 | 17 | 0 | 0 |
| 02.08.09.001-0 | Cintilografia de corpo inteiro c/ galio 67 p/ pesquisa de neoplasias | 1 | 3 | 3 | 0 | 260 | 226 | 0 | 0 |
| 02.08.02.008-0 | Cintilografia p/ pesquisa de diverticulose de meckel | 1 | 3 | 3 | 0 | 147 | 143 | 0 | 0 |
| 02.08.02.005-5 | Cintilografia p/ estudo de transito esofagico (liquido) | 1 | 3 | 3 | 0 | 277 | 325 | 0 | 0 |
| 02.08.09.002-9 | Cintilografia de glandula lacrimal (dacriocintilografia) | 1 | 3 | 3 | 0 | 45 | 48 | 1 | 1 |
| 02.08.02.011-0 | Cintilografia p/ pesquisa de refluxo gastro-esofagico | 1 | 2 | 2 | 0 | 13 | 13 | 0 | 0 |
| **medicina nuclear** | **modalidade inteira, no motor** | 24 | **5.915** | **4.377** | 204 | 217 | 182 | 314 | 1.182 |

**Radiologia intervencionista** (1 códigos)

| código | procedimento (SIGTAP) | nomes | fila | pessoas | devolvidas | espera média | mediana | agendadas/mês 2026 (calc.) | pessoas já no plano 4 |
|---|---|---|---|---|---|---|---|---|---|
| 02.10.01.001-0 | Angiografia cerebral (4 vasos) | 1 | 11 | 11 | 21 | 20 | 20 | 9 | 0 |
| **radiologia intervencionista** | **modalidade inteira, no motor** | 1 | **11** | **11** | 75 | 20 | 20 | 26 | 0 |

## 3. Por modalidade

Motor, por prefixo do código. Candidatas sem resíduo; mesmo código do plano 4 sem resíduo; plano
4 só como referência. Agendadas/mês das candidatas (calculado).

| modalidade | candidatas: fila | pessoas | espera média | mediana | agendadas/mês (calc.) | mesmo código (sem resíduo): fila | pessoas | espera média | plano 4: fila | pessoas | espera média |
|---|---|---|---|---|---|---|---|---|---|---|---|
| radiologia | **14.471** | 13.126 | 66 | 35 | 11.666 | — | — | — | — | — | — |
| ultrassonografia | **35.273** | 31.682 | 335 | 189 | 5.066 | 4.130 | 4.080 | 446 | 63.960 | 55.512 | 568 |
| tomografia | **4.080** | 3.401 | 178 | 120 | 3.022 | 5.372 | 3.141 | 284 | 12.077 | 6.609 | 139 |
| ressonância magnética | **9.925** | 7.343 | 24 | 21 | 10.355 | — | — | — | — | — | — |
| medicina nuclear | **5.915** | 4.377 | 217 | 182 | 314 | — | — | — | — | — | — |
| radiologia intervencionista | **11** | 11 | 20 | 20 | 26 | — | — | — | — | — | — |
| *todas (universo, não é objeto)* | 69.675 | 56.722 | 216 | 97 | 30.448 | 9.502 | 7.176 | 355 | 76.037 | 61.310 | 500 |

A soma das pessoas das 121 linhas da seção 2 dá 65.289; as candidatas são **56.722 pessoas
distintas**: quem espera dois exames candidatos conta uma vez no motor.

## 4. Mesmo código do plano 4 — diferença para 09/10

As filas dos onze códigos fora dos dezesseis nomes. **Risco de sobreposição:** têm o código dos
exames do plano 4, e parte das pessoas já está na fila dele. Δ = diferença para 09/10
(calculado). A coluna "sem resíduo" tira as filas sem nada em 2026.

| código | procedimento | nomes com fila | fila 09/10 | **fila 15/10** | Δ | pessoas 15/10 | devolvidas | espera média | mediana | pessoas já no plano 4 | sem resíduo: fila | agendadas/mês fora dos nomes do plano 4 (calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | Ultrassonografia doppler colorido de vasos | 32 | 2.570 | **2.647** | 77 | 2.593 | 2.516 | 475 | 370 | 1.425 | 2.406 | 79 |
| 02.06.03.001-0 | Tomografia computadorizada de abdomen superior | 18 | 1.916 | **2.062** | 146 | 1.897 | 2.685 | 270 | 216 | 319 | 2.062 | 822 |
| 02.06.02.003-1 | Tomografia computadorizada de torax | 12 | 1.831 | **1.901** | 70 | 1.813 | 2.674 | 284 | 227 | 271 | 1.901 | 465 |
| 02.06.03.003-7 | Tomografia computadorizada de pelve / bacia / abdomen inferior | 11 | 1.308 | **1.409** | 101 | 1.310 | 1.825 | 306 | 281 | 198 | 1.409 | 696 |
| 02.05.02.012-7 | Ultrassonografia de tireoide | 4 | 858 | **873** | 15 | 873 | 566 | 452 | 368 | 322 | 869 | 45 |
| 02.05.02.004-6 | Ultrassonografia de abdomen total | 2 | 480 | **454** | −26 | 454 | 430 | 597 | 363 | 14 | 451 | 89 |
| 02.05.02.005-4 | Ultrassonografia de aparelho urinário | 3 | 392 | **390** | −2 | 389 | 665 | 511 | 336 | 53 | 385 | 67 |
| 02.05.02.003-8 | Ultrassonografia de abdômen superior | 2 | 19 | **20** | 1 | 20 | 17 | 561 | 214 | 2 | 19 | 10 |
| 02.05.02.009-7 | Ultrassonografia mamaria bilateral | 2 | 2 | **2** | 0 | 2 | 0 | 1.507 | 1.507 | 0 | 0 | 0 |
| 02.05.02.010-0 | Ultrassonografia de prostata por via abdominal | 1 | 2 | **2** | 0 | 2 | 0 | 1.511 | 1.511 | 0 | 0 | 0 |
| 02.05.02.018-6 | Ultrassonografia transvaginal | 1 | 1 | **1** | 0 | 1 | 3 | 3.951 | 3.951 | 0 | 0 | 0 |
| **total (motor)** | | 88 | 9.378 | **9.760** | 382 | 7.408 | 11.381 | 376 | 282 | 2.305 | 9.502 | |

**De 09/10 para 15/10:** 82 → **88 filas**, 9.378 → **9.760 na fila** (+382), 7.156 → **7.408
pessoas** (+252), das quais 2.242 → **2.305** já estão na fila do plano 4. A base ganhou treze
dias de solicitações (de 02/10 para 15/10). Sete filas de TC que tinham fila 0 em 09/10
voltaram com 1 a 3 (TC cardíaca, TC de abdômen superior e de pelve infantis, TC de tórax com
sedação) e uma saiu (052. TC do tórax infantil com contraste e sedação). As maiores altas são
nas TC: abdômen superior +146, pelve +101, tórax +70, com as filas de emergência subindo de 14 a
31 cada; o doppler colorido de vasos aberto em 02/09/2026 passou de 97 para 133. Sem resíduo, o
mesmo código tem **57 filas, 9.502 na fila e 7.176 pessoas**. Diferença fila a fila na aba 9.

## 5. Região de Saúde — medida fila

Região de Saúde da unidade solicitante. URD, Contratado/Credenciado, Serviços Centralizados e
Público – Não SES não são Região de Saúde: são unidades de referência e prestadores que
solicitam direto, e vão à parte. A linha sem região é o campo vazio no painel. Nenhuma linha
foi rateada. Os quinze códigos candidatos de maior fila; pessoas por Região na aba 6 (não somam
o total: quem tem solicitação vinda de duas Regiões conta nas duas).

| código | procedimento | Central | Centro-Sul | Leste | Norte | Oeste | Sudoeste | Sul | URD | Contrat./Cred. | Serv. Centr. | Púb. não SES | **sem região** | **total** | URD + Contrat. (% calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | Ecocardiografia transtoracica | 1.101 | 1.293 | 940 | 1.800 | 1.615 | 2.853 | 1.066 | 2.676 | 2.823 | 0 | 0 | 126 | **16.293** | 33,8% |
| 02.05.02.006-2 | Ultrassonografia de articulacao | 40 | 2.805 | 2.958 | 512 | 1.523 | 4.239 | 2.252 | 0 | 0 | 0 | 0 | 152 | **14.481** | 0,0% |
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | 303 | 1.249 | 1.675 | 333 | 931 | 751 | 593 | 306 | 183 | 0 | 0 | 137 | **6.461** | 7,6% |
| 02.04.06.002-8 | Densitometria ossea duo-energetica de coluna (vertebras lomb | 156 | 221 | 144 | 194 | 256 | 493 | 222 | 308 | 166 | 0 | 0 | 36 | **2.196** | 21,6% |
| 02.08.01.002-5 | Cintilografia de miocardio p/ avaliacao da perfusao em situa | 100 | 162 | 31 | 90 | 115 | 133 | 54 | 250 | 884 | 0 | 0 | 6 | **1.825** | 62,1% |
| 02.08.05.003-5 | Cintilografia de ossos com ou sem fluxo sanguíneo (corpo int | 42 | 10 | 48 | 44 | 133 | 291 | 80 | 705 | 335 | 0 | 0 | 0 | **1.688** | 61,6% |
| 02.04.01.017-9 | Radiografia panoramica | 235 | 158 | 157 | 268 | 418 | 289 | 114 | 2 | 0 | 0 | 0 | 12 | **1.653** | 0,1% |
| 02.07.03.002-2 | Ressonancia magnetica de bacia / pelve / abdomen inferior | 82 | 72 | 98 | 139 | 200 | 373 | 138 | 377 | 131 | 0 | 0 | 15 | **1.625** | 31,3% |
| 02.08.01.003-3 | Cintilografia de miocardio p/ avaliacao da perfusao em situa | 42 | 145 | 12 | 68 | 57 | 73 | 41 | 176 | 886 | 0 | 0 | 5 | **1.505** | 70,6% |
| 02.07.03.003-0 | Ressonancia magnetica de membro inferior (unilateral) | 70 | 170 | 153 | 181 | 210 | 317 | 212 | 133 | 28 | 0 | 0 | 17 | **1.491** | 10,8% |
| 02.06.01.007-9 | Tomografia computadorizada do cranio | 24 | 34 | 106 | 71 | 77 | 673 | 58 | 276 | 111 | 0 | 0 | 37 | **1.467** | 26,4% |
| 02.07.01.006-4 | Ressonancia magnetica de cranio | 70 | 79 | 102 | 116 | 155 | 268 | 117 | 361 | 130 | 0 | 1 | 18 | **1.417** | 34,7% |
| 02.07.01.004-8 | Ressonancia magnetica de coluna lombo-sacra | 46 | 133 | 209 | 168 | 211 | 293 | 131 | 144 | 45 | 0 | 0 | 32 | **1.412** | 13,4% |
| 02.05.02.008-9 | Ultrassonografia de globo ocular / orbita (monocular) | 404 | 24 | 13 | 1 | 7 | 195 | 32 | 573 | 22 | 0 | 0 | 1 | **1.272** | 46,8% |
| 02.07.02.002-7 | Ressonancia magnetica de membro superior (unilateral) | 49 | 99 | 83 | 118 | 146 | 200 | 198 | 202 | 24 | 1 | 0 | 20 | **1.140** | 19,8% |

Por conjunto (motor):

| Região | candidatas | mesmo código do plano 4 | plano 4 | outro código |
|---|---|---|---|---|
| Região Central | 3.134 | 183 | 3.666 | 1.383 |
| Região Centro-Sul | 7.532 | 753 | 6.168 | 86 |
| Região Leste | 8.021 | 980 | 10.441 | 173 |
| Região Norte | 7.343 | 1.228 | 4.506 | 154 |
| Região Oeste | 7.097 | 170 | 4.087 | 340 |
| Região Sudoeste | 14.110 | 4.477 | 23.894 | 453 |
| Região Sul | 6.384 | 802 | 15.232 | 174 |
| URD | 8.650 | 537 | 4.995 | 2.139 |
| Contratado/Credenciado | 6.597 | 498 | 2.293 | 172 |
| Serviços Centralizados | 1 | 0 | 1 | 0 |
| Público - Não SES | 3 | 1 | 1 | 0 |
| **sem região informada** | 803 | 131 | 753 | 11 |
| **total (motor)** | 69.675 | 9.760 | 76.037 | 5.085 |

**Nas cintilografias de miocárdio e de ossos, URD e Contratado/Credenciado pedem de 62% a 71%
da fila** (calculado); na ultrassonografia de articulação e na radiografia panorâmica, quase
nada. A ecocardiografia tem um terço da fila vinda de URD e contratado.

## 6. Plano 4 — referência

Os dezesseis nomes do enquadramento, fora da soma. Δ = diferença para 09/10 (calculado).

| código | nome interno | fila 09/10 | **fila 15/10** | Δ | pessoas 15/10 | espera média | mediana | agendadas/mês 2026 (calc.) |
|---|---|---|---|---|---|---|---|---|
| 02.05.02.009-7 | ECOGRAFIA DE MAMAS - BILATERAL | 13.762 | **13.519** | −243 | 13.498 | 624 | 500 | 918 |
| 02.05.02.004-6 | ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 10.175 | **10.278** | 103 | 10.273 | 531 | 323 | 741 |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 9.930 | **10.001** | 71 | 9.999 | 621 | 569 | 308 |
| 02.05.02.018-6 | ECOGRAFIA TRANSVAGINAL | 9.814 | **9.842** | 28 | 9.841 | 633 | 486 | 1.533 |
| 02.05.01.004-0 | 10. ECODOPPLER DE CAROTIDAS | 4.580 | **4.591** | 11 | 4.591 | 141 | 136 | 690 |
| 02.06.03.001-0 | 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 4.125 | **4.157** | 32 | 4.154 | 122 | 119 | 649 |
| 02.05.02.005-4 | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | 3.899 | **3.820** | −79 | 3.818 | 641 | 426 | 343 |
| 02.06.03.003-7 | 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 3.649 | **3.650** | 1 | 3.649 | 122 | 120 | 556 |
| 02.05.02.010-0 | ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | 3.337 | **3.309** | −28 | 3.303 | 573 | 448 | 356 |
| 02.05.02.004-6 | ULTRASONOGRAFIA DE PAREDE ABDOMINAL | 3.199 | **3.229** | 30 | 3.229 | 596 | 507 | 135 |
| 02.05.02.012-7 | ECOGRAFIA DE TIREOIDE ADULTO | 3.168 | **3.094** | −74 | 3.094 | 474 | 359 | 281 |
| 02.06.02.003-1 | 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 2.466 | **2.471** | 5 | 2.468 | 122 | 115 | 474 |
| 02.05.02.003-8 | ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | 2.271 | **2.276** | 5 | 2.274 | 691 | 611 | 213 |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA[NBSP] DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | 1.475 | **1.506** | 31 | 1.506 | 280 | 252 | 12 |
| 02.06.02.003-1 | 053. TC DO TORAX␣␣ADULTO S/CONTRASTE S/SEDACAO | 26 | **293** | 267 | 293 | 23 | 6 | 1.647 |
| 02.05.02.004-6 | ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 1 | **1** | 0 | 1 | 1.507 | 1.507 | 0 |
| **plano 4 (motor)** | 16 nomes | 75.877 | **76.037** | 160 | 61.310 | 500 | 293 | |

O plano 4 subiu 160 na fila e 178 pessoas. Duas mudanças grandes: a **TC de tórax sem
contraste** passou de 26 para 293 (267 pedidos novos, espera média de 23 dias) e a **mama
bilateral** caiu 243 (13.762 para 13.519). O painel não diz para onde as solicitações saíram.

## 7. O que pesa na escolha

Só os números do painel; a escolha é da conversa principal.

- **Ecocardiografia transtorácica (02.05.01.003-2)** é a maior fila candidata: 16.293 na fila,
  16.289 pessoas, espera média de 135 dias (mediana 127), 3.422 agendadas por mês; 4.713 dessas
  pessoas já estão na fila do plano 4. Três nomes de fila (adulto 14.646, infantil 1.593, fetal
  54). Um terço da fila vem de URD e contratado.
- **Ultrassonografia de articulação (02.05.02.006-2)** tem a espera mais longa entre as grandes:
  14.481 na fila em 55 nomes, 11.486 pessoas, espera média de 545 dias (mediana 400), só 698
  agendadas por mês. Inclui as partes moles (3.108), que saiu do plano 4 em 22/09/2026, ombro
  (3.538 nos dois lados), punho (3.211), joelho (1.179), tornozelo, região inguinal, mão, pé,
  pescoço e quadril infantil.
- **Ultrassonografias de espera longa e pouca oferta:** pélvica ginecológica (1.003, espera média
  603 dias, 111 agendadas por mês), bolsa escrotal (995, 588 dias, 72 por mês), globo ocular
  (1.272, 264 dias, 58 por mês), transfontanela (281, 282 dias).
- **Cintilografias de miocárdio** (estresse 1.825 e repouso 1.505): **1.943 pessoas**, 1.387
  nas duas (motor); espera mediana de 337 e 364 dias e cerca de 30 agendadas por mês em cada uma.
  Os nomes de fila existem desde junho de 2025. A **cintilografia óssea** tem 1.688 (espera
  média 144 dias, 130 por mês); 62% a 71% dessas três filas vêm de URD e contratado.
- **Mamografia (6.461) e densitometria (2.196)** têm fila média, espera curta (49 e 44 dias) e
  oferta grande (4.682 e 980 agendadas por mês): a fila gira.
- **Ressonância:** 9.925 na fila, espera média de 24 dias e 10.355 agendadas por mês; a fila de
  RM no painel anda rápido. As maiores são bacia/pelve (1.625), membro inferior (1.491), crânio
  (1.417) e coluna lombo-sacra (1.412).
- **Tomografia candidata:** 4.080 na fila. TC de crânio (1.467, espera média 197 dias), TC de
  pescoço (755) e **PET-CT** (424, espera média 162 dias, 42 agendadas por mês). As filas de
  emergência de TC fora do plano 4 têm, em geral, espera média acima de 250 dias (a maior, TC de
  crânio adulto sem contraste, 390 na fila e 359 dias).
- **Radiografia** convencional: muitas filas pequenas (168 filas, 14.471 na fila contando
  mamografia e densitometria), espera média curta e muita oferta.
- **Radiologia intervencionista:** só a angiografia cerebral tem fila (11).

## 8. Lacunas

- **Oferta:** as agendadas são contadas pela data marcada do exame (`data_agendamento`, que vai
  até 25/01/2027). O painel não diz quantas foram realizadas.
- **Pessoas entre códigos:** as pessoas de cada código são distintas dentro dele; somar códigos
  conta duas vezes quem espera dois exames (65.289 na soma das linhas contra 56.722 no motor).
  Para um objeto com mais de um código, medir a união no motor.
- **"Pessoas já no plano 4"** mede a mesma pessoa em duas filas, não o mesmo exame; e o painel
  não diz que parte do plano 4 já foi executada.
- **Região:** coletada por código só para os quinze códigos candidatos de maior fila e por
  modalidade; os demais códigos não foram abertos por Região.
- **Idade e sexo:** só a idade mediana por fila e por código; o painel não foi aberto por faixa
  etária nem por sexo, porque não há objeto (OCI com faixa ou sexo pede nova medida).
- **CID:** só os três CIDs principais de cada fila; o recorte por CID de uma OCI pede nova coleta.
- **Valor e OCI:** a coleta não diz se o código cabe numa OCI nem quanto paga (ficha do SIGTAP e
  pesquisa de preços).
- **Códigos malformados:** 20406014 e 20406015 não têm descrição SIGTAP; ficaram na radiologia
  pelo nome (radiografia de joelho e de pé).
- **Espera máxima:** chega a 6.995 dias (ecografia obstétrica morfológica de 2007) e a 7.037 dias
  no resíduo; são registros antigos ainda pendentes, e o painel não diz se são esquecidos.
- **Entrantes:** não coletados, por não terem sido pedidos.
