# Mapa Social da Saúde — fila dos onze procedimentos de imagem, recarga de 09/10/2026 11:32

Coleta do agente `mapa-social` para o pré-plano de exames de imagem (redacao_06), feita de
forma independente para comparar com a coleta da conversa principal do mesmo dia (recarga
das 09:32). **É a coleta do pré-plano desde 09/10/2026**: as duas bateram, e esta tem a
varredura pelo código que o método pede; a comparação está em `../fila.md`. Objeto:
onze procedimentos de ultrassonografia e tomografia em dezesseis nomes de fila do SISREG;
a ecografia de partes moles (02.05.02.006-2), fora do objeto desde 22/09/2026, vem à parte,
fora da soma. O enquadramento (nome interno exato e grupo de cada fila) é o da coleta de
06/10/2026 do plano 4 (`planos/redacao_04/dados/fontes/mapa_social_20261006_bruto/coleta_20261006.json`),
e os dezessete nomes responderam com a grafia gravada. Planilha em
`mapa_social_20261009.xlsx`; JSON do motor e script em `mapa_social_20261009_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 09/10/2026 11:32:55 (qLastReloadTime 2026-10-09T14:32:55Z) |
| Consulta | 09/10/2026 11:40:44 a 12:07:23 (relógio do motor, Brasília); a recarga foi conferida às 11:53:57 e às 12:07:23, sem mudança |
| Solicitação mais recente na base | 02/10/2026 (na coleta de 06/10 era 30/09/2026) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Recorte | todos os anos; cada nome de fila fixo na expressão de conjunto `{1<...>}`, sem depender da tela; procedimento avulso, sem recorte de CID |
| Via | Qlik Engine API do próprio painel (hipercubos de sessão e evaluateEx), no navegador embutido |
| Comparação | coleta de 06/10/2026 do plano 4 (base de 06/10/2026 21:32) |

Pessoas = CNS distintos no conjunto: quem espera por mais de um exame conta uma vez. Espera
em dias, calculada no motor sobre os registros do conjunto (não é média das linhas).

O método mudou às 11:45 de hoje, durante esta coleta (regra do usuário: a varredura vem
antes de tudo e cada fila achada se estuda e recebe decisão). A seção 1 segue a regra nova.

---

## 1. Varredura das filas

A varredura segue a regra do método de 09/10/2026 (`metodo/coleta/mapa_social.md`): para
exame avulso, todas as filas com o código SIGTAP do exame, depois as de nome parecido com
outro código e as variantes e faixas etárias do mesmo nome. Cada fila achada foi estudada
(fila, pessoas, devolvidas, espera, idade, CIDs principais, desde quando existe e oferta
pelas agendadas por mês) e recebeu decisão. O campo de grupo do painel não serve de
"segmento": o ecodoppler de carótidas está no grupo de ecocardiografia, e doze transvaginais
estão em "grupo não relacionado".

**O que não é "entra" fica fora da soma.** A decisão segue uma regra só, escrita no script
da planilha (`decidir()`): o enquadramento entra; partes moles fica fora (22/09/2026); fila
de outro código SIGTAP fica fora, porque o objeto são os onze códigos, e só entraria se o
objeto mudasse; fila do mesmo código fora do enquadramento fica **a decidir**, porque fila
nova não entra na soma sem decisão da conversa principal.

| decisão | filas | fila | de onde |
|---|---|---|---|
| **entra** — enquadramento | 16 | **75.877** | motor (conjunto do objeto) |
| fica fora — partes moles, desde 22/09/2026 | 1 | 3.116 | motor |
| fica fora — outro código SIGTAP, nome parecido | 20 | 17.538 | soma das linhas (calculado) |
| **a decidir** — mesmo código, fora do enquadramento | 82 | **9.378** | motor; a soma das linhas dá 9.380 porque duas solicitações estão em dois nomes |
| só registro — nome parecido em outra modalidade (ressonância, radiografia, cintilografia, punção, consulta) | 51 | — | aba 9 |

As 82 filas "a decidir", por tipo (soma das linhas, calculado):

| tipo | filas | fila | o que é |
|---|---|---|---|
| fila de emergência | 12 | 3.399 | TC de tórax, abdômen superior e pelve "EMERG.", adulto (3.245) e infantil (154) |
| outro doppler com o mesmo código | 8 | 3.006 | doppler arterial de MMII (1.781), doppler de tireoide (784), transvaginal com doppler, MMSS, artérias renais e outros |
| outro exame com o código de doppler | 1 | 9 | ultrassonografia das parótidas |
| angiotomografia | 8 | 1.602 | aorta torácica, aorta abdominal, pelve, abdome superior, pulmonar, carótidas e vertebrais, renais, porta |
| faixa etária infantil | 15 | 908 | abdômen total infantil (477), aparelho urinário infantil (315), tireoide infantil (70) e TC infantis |
| fila parada | 1 | 190 | doppler de carótidas e vertebrais: nada novo nem agendado em 2026 |
| fila aberta em 2026 | 2 | 98 | doppler colorido de vasos (97, desde 02/09/2026) e doppler de órgão (1) |
| variante de nome | 1 | 72 | ultrassonografia renal |
| resíduo | 30 | 70 | nomes antigos do SISREG, quase todos de 2022, sem solicitação nem agendamento em 2026 |
| variante de contraste ou sedação | 4 | 26 | TC de abdômen superior e de pelve sem contraste ou com sedação |

Subtotais do motor, por código, das filas "a decidir":

| código | nomes com fila | fila | pessoas | devolvidas | espera média | mediana | pessoas já na fila do objeto | pessoas fora dela |
|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | 32 | 2.570 | 2.514 | 2.544 | 484 | 378 | 1.389 | 1.125 |
| 02.05.02.012-7 | 4 | 858 | 858 | 576 | 457 | 379 | 328 | 530 |
| 02.05.02.004-6 | 2 | 480 | 480 | 434 | 582 | 353 | 14 | 466 |
| 02.05.02.005-4 | 3 | 392 | 391 | 673 | 534 | 386 | 57 | 334 |
| 02.05.02.003-8 | 2 | 19 | 19 | 17 | 584 | 225 | 2 | 17 |
| 02.05.02.009-7 | 2 | 2 | 2 | 0 | 1.501 | 1.501 | 0 | 2 |
| 02.05.02.010-0 | 1 | 2 | 2 | 0 | 1.504 | 1.504 | 0 | 2 |
| 02.05.02.018-6 | 1 | 1 | 1 | 3 | 3.945 | 3.945 | 0 | 1 |
| **ultrassonografia** | **47** | **4.323** | **4.244** | 4.247 | 496 | 375 | 1.784 | 2.460 |
| 02.06.03.001-0 | 14 | 1.916 | 1.755 | 2.722 | 285 | 241 | 291 | 1.464 |
| 02.06.02.003-1 | 12 | 1.831 | 1.749 | 2.708 | 289 | 232 | 254 | 1.495 |
| 02.06.03.003-7 | 9 | 1.308 | 1.212 | 1.845 | 323 | 307 | 174 | 1.038 |
| **tomografia** | **35** | **5.055** | **2.956** | 7.275 | 297 | 259 | 473 | 2.483 |
| **total "a decidir"** | **82** | **9.378** | **7.156** | 11.522 | 389 | 305 | 2.242 | **4.914** |

"Pessoas já na fila do objeto" = CNS da varredura que também têm solicitação na fila dos
dezesseis nomes (`P()` sobre o conjunto do objeto, no motor). Objeto e "a decidir" juntos,
no motor: **85.255 solicitações e 66.046 pessoas** (61.132 + 4.914). Só para dimensionar;
não é a fila do objeto.

### 1.1 O estudo das filas do enquadramento

Agendadas por mês = agendamentos marcados de janeiro a setembro de 2026, divididos por 9
(calculado); a data de agendamento do painel é a data marcada. CIDs = os três
`codigo_cid_solicitado` com mais solicitações na fila, com a contagem.

| código | nome interno | fila | idade mediana | 1ª solicitação na base | fila pedida em 2026 | CIDs principais na fila | agendadas/mês 2026 (calc.) | decisão |
|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 9.930 | 58 | 17/10/2022 | 2.819 | I83 3389; I839 1636; I872 1351 | 308 | **entra** |
| 02.05.01.004-0 | 10. ECODOPPLER DE CAROTIDAS | 4.580 | 64 | 17/01/2019 | 4.327 | I10 1003; I50 377; I25 372 | 690 | **entra** |
| 02.05.02.003-8 | ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | 2.271 | 55 | 22/09/2010 | 769 | K76 359; K760 264; R10 246 | 213 | **entra** |
| 02.05.02.004-6 | ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 10.175 | 55 | 05/07/2007 | 4.605 | R10 2401; K76 912; K80 655 | 741 | **entra** |
| 02.05.02.004-6 | ULTRASONOGRAFIA DE PAREDE ABDOMINAL | 3.199 | 51 | 15/08/2019 | 1.085 | K42 753; K40 712; K46 418 | 135 | **entra** |
| 02.05.02.004-6 | ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 1 | 54 | 30/08/2022 | 0 | N18 1 | 0 | **entra** |
| 02.05.02.005-4 | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | 3.899 | 57 | 28/10/2010 | 1.436 | N20 627; N18 375; N40 259 | 343 | **entra** |
| 02.05.02.009-7 | ECOGRAFIA DE MAMAS - BILATERAL | 13.762 | 48 | 30/07/2007 | 4.777 | N63 3668; Z123 1824; N64 1443 | 918 | **entra** |
| 02.05.02.010-0 | ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | 3.337 | 65 | 26/05/2010 | 1.076 | N40 1951; Z125 182; N41 129 | 356 | **entra** |
| 02.05.02.012-7 | ECOGRAFIA DE TIREOIDE ADULTO | 3.168 | 55 | 29/07/2019 | 1.310 | E07 532; E04 296; E039 236 | 281 | **entra** |
| 02.05.02.018-6 | ECOGRAFIA TRANSVAGINAL | 9.814 | 49 | 03/09/2010 | 3.677 | Z014 2397; N95 776; R10 498 | 1.533 | **entra** |
| 02.06.02.003-1 | 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 2.466 | 61 | 03/01/2020 | 2.453 | C50 436; C18 226; C509 142 | 474 | **entra** |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA[NBSP]␣DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | 1.475 | 63 | 16/08/2024 | 789 | I20 393; I25 339; I50 106 | 12 | **entra** |
| 02.06.02.003-1 | 053. TC DO TORAX␣␣ADULTO S/CONTRASTE S/SEDACAO | 26 | 68 | 02/01/2020 | 22 | C50 4; R91 2; C16 2 | 1.647 | **entra** |
| 02.06.03.001-0 | 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 4.125 | 58 | 02/01/2020 | 4.106 | C50 591; C18 342; R10 236 | 649 | **entra** |
| 02.06.03.003-7 | 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 3.649 | 59 | 02/01/2020 | 3.632 | C50 503; C18 324; R10 227 | 556 | **entra** |
| 02.05.02.006-2 | ECOGRAFIA␣␣DE PARTES MOLES | 3.116 | 51 | 28/10/2010 | 1.044 | D17 533; R22 503; K40 151 | 127 | **fica fora** (22/09/2026) |

### 1.2 A decidir — filas do mesmo código com 50 ou mais na fila

| código | nome interno | fila | pessoas | espera média / mediana | idade mediana | 1ª solicitação na base | fila pedida em 2026 | CIDs principais na fila | agendadas/mês 2026 (calc.) | decisão — nota |
|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMII (BILATERAL) | 1.781 | 1.781 | 472 / 393 | 63 | 19/10/2022 | 674 | I70 292; I83 243; I739 222 | 46 | a decidir — outro doppler com o mesmo código |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER DE CAROTIDAS E VERTEBRAIS | 190 | 190 | 947 / 918 | 66 | 08/02/2023 | 0 | I10 71; E11 23; I70 19 | 0 | a decidir — fila parada: sem solicitação nova nem agendamento em 2026 |
| 02.05.01.004-0 | ECOGRAFIA TRANSVAGINAL COM DOPPLER | 139 | 139 | 566 / 472 | 49 | 15/01/2020 | 43 | Z014 19; N951 13; Z12 10 | 12 | a decidir — outro doppler com o mesmo código |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMSS ( BILATERAL) | 135 | 135 | 170 / 108 | 55 | 25/10/2022 | 113 | I83 21; I82 15; I872 12 | 7 | a decidir — outro doppler com o mesmo código |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS | 97 | 97 | 17 / 16 | 56 | 02/09/2026 | 97 | I83 21; I839 13; I872 5 | 0 | a decidir — fila aberta em 2026 (desde 02/09/2026) |
| 02.05.01.004-0 | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE ARTERIAS RENAIS | 87 | 87 | 189 / 156 | 52 | 05/11/2023 | 62 | I10 35; I15 17; N18 7 | 2 | a decidir — outro doppler com o mesmo código |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER ARTERIAL - MMSS (BILATERAL) | 67 | 67 | 236 / 238 | 63 | 07/11/2022 | 41 | I83 5; I10 4; I771 4 | 7 | a decidir — outro doppler com o mesmo código |
| 02.05.02.004-6 | ECOGRAFIA DE ABDOMEN TOTAL INFANTIL | 477 | 477 | 576 / 353 | 9 | 07/01/2020 | 221 | R10 144; E66 57; R104 42 | 89 | a decidir — faixa etária infantil, mesmo código |
| 02.05.02.005-4 | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) INFANTIL | 315 | 315 | 502 / 334 | 8 | 08/01/2020 | 147 | N39 34; N390 20; R32 16 | 65 | a decidir — faixa etária infantil, mesmo código |
| 02.05.02.005-4 | ULTRASSONOGRAFIA RENAL | 72 | 72 | 605 / 510 | 60 | 23/02/2023 | 21 | N20 11; N18 7; R31 6 | 2 | a decidir — variante de nome, mesmo código |
| 02.05.02.012-7 | ULTRA-SONOGRAFIA DOPPLER DE TIREOIDE | 784 | 784 | 441 / 357 | 54 | 19/11/2019 | 348 | E07 181; E04 95; E039 86 | 36 | a decidir — outro doppler com o mesmo código |
| 02.05.02.012-7 | ECOGRAFIA DE TIREOIDE INFANTIL | 70 | 70 | 496 / 492 | 12 | 02/02/2021 | 16 | E039 12; E038 9; E07 8 | 8 | a decidir — faixa etária infantil, mesmo código |
| 02.06.02.003-1 | TC DO TORAX␣␣ADULTO S/CONTRASTE S/SEDACAO␣␣EMERGENCIA | 857 | 857 | 347 / 332 | 64 | 06/12/2016 | 381 | J18 165; I25 68; C50 36 | 166 | a decidir — fila de emergência, mesmo código |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS[NBSP]␣ADULTO S/SEDACAO[NBSP] | 329 | 329 | 199 / 169 | 65 | 24/01/2024 | 236 | I71 118; I35 29; I712 22 | 47 | a decidir — angiotomografia, mesmo código |
| 02.06.02.003-1 | TC DO TORAX␣␣ADULTO C/CONTRASTE␣␣S/SEDACAO␣␣EMERGENCIA | 295 | 295 | 350 / 338 | 59 | 26/09/2024 | 130 | C50 16; C53 13; I26 13 | 80 | a decidir — fila de emergência, mesmo código |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA DO TORAX OU PULMONAR ADULTO S/SEDACAO | 264 | 264 | 142 / 115 | 60 | 29/01/2024 | 228 | I26 81; I71 29; I27 17 | 117 | a decidir — angiotomografia, mesmo código |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.ADULTO␣␣C/CONTRASTE S/SEDACAO␣␣EMERG. | 708 | 708 | 350 / 349 | 58 | 29/12/2016 | 303 | R10 133; C18 30; Z54 29 | 126 | a decidir — fila de emergência, mesmo código |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.ADULTO␣␣S/CONTRASTE S/SEDACAO␣␣EMERG. | 374 | 374 | 365 / 359 | 57 | 06/12/2016 | 150 | R10 86; N20 20; Z54 11 | 61 | a decidir — fila de emergência, mesmo código |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS ADULTO S/SEDACAO[NBSP] | 289 | 289 | 204 / 179 | 65 | 10/01/2024 | 201 | I71 93; N180 18; I70 18 | 37 | a decidir — angiotomografia, mesmo código |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DO ABDOME SUPERIOR ADULTO S/SEDACAO[NBSP] | 232 | 232 | 214 / 183 | 58 | 04/04/2024 | 149 | I71 35; N180 23; K55 17 | 25 | a decidir — angiotomografia, mesmo código |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DAS ARTERIAS CAROTIDAS E VERTEBRAIS ADULTO S/SEDACAO | 208 | 208 | 136 / 114 | 68 | 24/01/2024 | 183 | I65 45; I64 25; I652 23 | 39 | a decidir — angiotomografia, mesmo código |
| 02.06.03.003-7 | TC DE PELVE OU BACIA ADULTO␣␣C/CONTRASTE␣␣S/SEDACAO EMERG. | 657 | 657 | 342 / 326 | 57 | 27/09/2024 | 290 | R10 112; Z54 30; C50 26 | 111 | a decidir — fila de emergência, mesmo código |
| 02.06.03.003-7 | TC DE PELVE OU BACIA ADULTO␣␣S/CONTRASTE␣␣S/SEDACAO EMERG. | 354 | 354 | 365 / 349 | 57 | 06/12/2016 | 142 | R10 79; N20 15; Z54 11 | 55 | a decidir — fila de emergência, mesmo código |
| 02.06.03.003-7 | ANGIOTOMOGRAFIA DA PELVE ADULTO S/SEDACAO | 237 | 237 | 214 / 192 | 57 | 10/01/2024 | 150 | I82 31; I71 30; N180 23 | 26 | a decidir — angiotomografia, mesmo código |

### 1.3 A decidir — filas do mesmo código com menos de 50 na fila

| código | nome interno | fila | espera média | idade mediana | 1ª solicitação na base | fila pedida em 2026 | agendadas jan–set/2026 | nota |
|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER VENOSO - MIE | 10 | 1.584 | 64 | 03/01/2020 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER DE AORTA E VASOS ILIACOS | 9 | 40 | 54 | 05/05/2022 | 9 | 20 | outro doppler com o mesmo código |
| 02.05.01.004-0 | ULTRASSONOGRAFIA DAS GLANDULAS PAROTIDAS | 9 | 395 | 49 | 28/08/2023 | 5 | 18 | outro exame com o código de doppler |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER VENOSO - MID | 8 | 1.544 | 61 | 03/01/2020 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER DE ARTERIA␣␣AORTA␣␣ABDOMINAL | 4 | 15 | 46 | 17/11/2022 | 4 | 15 | outro doppler com o mesmo código |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER DE CAROTIDAS E VERTEBRAIS | 4 | 1.644 | 72 | 03/03/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER COLORIDO DE UM VASO | 3 | 1.501 | 56 | 24/02/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I D | 3 | 1.512 | 78 | 27/07/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MID | 3 | 1.512 | 78 | 27/07/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER ARTERIAL- M I E | 2 | 1.499 | 71 | 08/01/2020 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER ARTERIAL- M I D | 2 | 1.514 | 55 | 06/01/2020 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRASSONOGRAFIA DOPPLER ARTERIAL MEMBRO SUPERIOR E | 2 | 1.501 | 54 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | DOPPLER VENOSO DE MI | 2 | 1.501 | 76 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | DOPPLER ARTERIAL DE MI | 2 | 1.501 | 76 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER DE ARTERIAS VERTEBRAIS | 2 | 1.423 | 59 | 14/10/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER ARTERIAL- M S D | 1 | 1.620 | 66 | 04/08/2020 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ECOGRAFIA DOPPLER COLORIDO DE ORGAO | 1 | 119 | 52 | 11/06/2026 | 1 | 0 | fila aberta em 2026 (desde 11/06/2026) |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER COLORIDO DE DOIS VASOS | 1 | 1.676 | 41 | 18/02/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER DE CAROTIDAS | 1 | 1.613 | 36 | 16/03/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DE BOLSA ESCROTAL COM DOPPLER | 1 | 1.501 | 21 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER ARTERIAL-M I E | 1 | 1.501 | 78 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER VENOSO - MIE | 1 | 1.501 | 78 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER - ARTERIAS RENAIS | 1 | 1.534 | 48 | 27/07/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA␣␣DOPPLER COLORIDO DE ORGAO OU ESTRUTURA ISO | 1 | 1.501 | 78 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.01.004-0 | ULTRA-SONOGRAFIA DOPPLER - CERVICAL | 1 | 1.359 | 67 | 19/01/2023 | 0 | 0 | resíduo |
| 02.05.02.003-8 | ECOGRAFIA DE ABDOMEN SUPERIOR INFANTIL | 18 | 533 | 10 | 27/10/2020 | 10 | 92 | faixa etária infantil |
| 02.05.02.003-8 | ULTRA-SONOGRAFIA DE ABDOMEN SUPERIOR | 1 | 1.501 | 74 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.02.004-6 | ULTRA-SONOGRAFIA DE ABDOMEN TOTAL | 3 | 1.501 | 26 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.02.005-4 | ULTRA-SONOGRAFIA␣␣DO APARELHO URINARIO (RINS, BEXIGA) | 5 | 1.509 | 64 | 27/07/2022 | 0 | 0 | resíduo |
| 02.05.02.009-7 | ULTRA-SONOGRAFIA DE MAMAS (BILATERAL) | 1 | 1.501 | 18 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.02.009-7 | ULTRA-SONOGRAFIA DOPPLER DE MAMAS | 1 | 1.501 | 67 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.02.010-0 | ULTRA-SONOGRAFIA DE PROSTATA (VIA ABDOMINAL) | 2 | 1.504 | 82 | 23/08/2022 | 0 | 0 | resíduo |
| 02.05.02.012-7 | ULTRA-SONOGRAFIA DE TIREOIDE | 3 | 1.501 | 76 | 30/08/2022 | 0 | 0 | resíduo |
| 02.05.02.012-7 | ECOGRAFIA DE TIREOIDE ADULTO EMERGENCIA | 1 | 6.983 | 58 | 27/08/2007 | 0 | 0 | resíduo |
| 02.05.02.018-6 | USG TRANSVAGINAL | 1 | 3.945 | 33 | 21/12/2015 | 0 | 0 | resíduo |
| 02.06.02.003-1 | TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO EMERGENCIA | 41 | 343 | 3 | 03/10/2024 | 14 | 8 | emergência (infantil) |
| 02.06.02.003-1 | TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO␣␣EMERGENCIA | 23 | 320 | 5 | 06/11/2024 | 11 | 11 | emergência (infantil) |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA[NBSP]␣DAS ARTÉRIAS CORONARIAS INFANTIL S/SEDACAO | 10 | 293 | 8 | 31/01/2025 | 5 | 0 | faixa etária infantil |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA DA AORTA TORÁCICA E SEUS RAMOS INFANTIL S/SEDACAO | 7 | 182 | 16 | 18/04/2024 | 5 | 8 | faixa etária infantil |
| 02.06.02.003-1 | 049. TC DO TORAX INFANTIL S/CONTRASTE S/SEDACAO | 2 | 165 | 15 | 31/03/2020 | 2 | 113 | faixa etária infantil |
| 02.06.02.003-1 | 051. TC DO TORAX INFANTIL C/CONTRASTE S/SEDACAO | 1 | 622 | 70 | 14/01/2020 | 0 | 44 | faixa etária infantil |
| 02.06.02.003-1 | ANGIOTOMOGRAFIA DO TORAX OU PULMONAR INFANTIL S/SEDACAO | 1 | 242 | 17 | 27/05/2025 | 1 | 14 | faixa etária infantil |
| 02.06.02.003-1 | 052. TC DO TORAX INFANTIL C/CONTRASTE C/SEDACAO | 1 | 36 | 1 | 14/02/2020 | 1 | 20 | faixa etária infantil |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.INFANTIL C/CONTRASTE S/SEDACAO␣␣EMERG. | 33 | 327 | 13 | 30/10/2024 | 16 | 13 | emergência (infantil) |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS ADULTO S/SEDACAO | 31 | 160 | 46 | 17/07/2024 | 24 | 33 | angiotomografia |
| 02.06.03.001-0 | TC DO ABDOMEN SUPER.INFANTIL S/CONTRASTE S/SEDACAO EMERG. | 14 | 339 | 8 | 01/10/2024 | 7 | 11 | emergência (infantil) |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DO SISTEMA PORTA (VASOS HEPÁTICOS) ADULTO S/SEDACAO | 12 | 226 | 46 | 28/03/2024 | 7 | 8 | angiotomografia |
| 02.06.03.001-0 | 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 10 | 76 | 58 | 02/01/2020 | 10 | 4.388 | variante sem contraste |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DA AORTA ABDOMINAL E DOS SEUS RAMOS INFANTIL S/SEDACAO | 2 | 285 | 38 | 22/06/2025 | 1 | 3 | faixa etária infantil |
| 02.06.03.001-0 | 060. TC DO ABDOMEN SUPERIOR INFANTIL C/CONTRASTE C/SEDACAO | 1 | 267 | 14 | 03/03/2020 | 1 | 13 | faixa etária infantil |
| 02.06.03.001-0 | ANGIOTOMOGRAFIA DAS ARTÉRIAS RENAIS INFANTIL S/SEDACAO | 1 | 296 | 11 | 07/07/2025 | 0 | 2 | faixa etária infantil |
| 02.06.03.001-0 | 064. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE C/SEDACAO | 1 | 199 | 69 | 02/01/2020 | 1 | 23 | variante com sedação |
| 02.06.03.003-7 | TC DE PELVE OU BACIA INFANTIL␣␣C/CONTRASTE␣␣S/SEDACAO EMERG. | 29 | 346 | 44 | 08/10/2024 | 13 | 13 | emergência (infantil) |
| 02.06.03.003-7 | 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE␣␣S/SEDACAO | 14 | 60 | 67 | 03/01/2020 | 14 | 4.362 | variante sem contraste |
| 02.06.03.003-7 | TC DE PELVE OU BACIA INFANTIL␣␣S/CONTRASTE␣␣S/SEDACAO EMERG. | 14 | 470 | 47 | 27/12/2024 | 1 | 8 | emergência (infantil) |
| 02.06.03.003-7 | 108. TC DE PELVE OU BACIA INFANTIL C/CONTRASTE␣␣C/SEDACAO | 1 | 267 | 14 | 01/07/2020 | 1 | 5 | faixa etária infantil |
| 02.06.03.003-7 | 112. TC DE PELVE OU BACIA ADULTO C/CONTRASTE C/SEDACAO | 1 | 622 | 70 | 02/01/2020 | 0 | 21 | variante com sedação |
| 02.06.03.003-7 | ANGIOTOMOGRAFIA DA PELVE INFANTIL S/SEDACAO | 1 | 27 | 0 | 12/09/2026 | 1 | 1 | faixa etária infantil |

Todas "a decidir". As notas curtas resumem a da planilha ("resíduo" = nome antigo, sem
solicitação nem agendamento em 2026).

### 1.4 Fica fora — nome parecido, outro código SIGTAP

| código | nome interno | fila | pessoas | espera média | idade mediana | 1ª solicitação na base | agendadas/mês 2026 (calc.) |
|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO | 14.651 | 14.650 | 139 | 62 | 19/08/2016 | 2.851 |
| 02.05.01.003-2 | 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL | 1.593 | 1.591 | 142 | 4 | 23/07/2019 | 505 |
| 02.05.01.003-2 | ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO | 2 | 2 | 6.943 | 89 | 03/10/2007 | 0 |
| 02.05.01.003-2 | ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER ADULTO EMERGENCIA | 1 | 1 | 6.960 | 61 | 19/09/2007 | 0 |
| 02.05.01.003-2 | ECOCARDIOGRAFIA BI-DIMENSIONAL SEM DOPPLER INFANTIL | 1 | 1 | 6.954 | 36 | 25/09/2007 | 0 |
| 02.05.01.005-9 | ECOGRAFIA DOPPLER FLUXO OBSTETRICO | 12 | 12 | 106 | 32 | 28/02/2020 | 1 |
| 02.05.02.006-2 | ECOGRAFIA PELVICA | 45 | 45 | 72 | 48 | 18/01/2023 | 2 |
| 02.05.02.006-2 | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DE REGIAO CERVICAL | 17 | 17 | 403 | 56 | 08/02/2023 | 1 |
| 02.05.02.006-2 | DOPPLER DE AORTA E ILIACA | 6 | 6 | 1.505 | 62 | 05/08/2022 | 0 |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DA BACIA | 4 | 4 | 589 | 60 | 02/03/2023 | 0 |
| 02.05.02.007-0 | ULTRASSONOGRAFIA COM DOPPLER COLORIDO DA BOLSA ESCROTAL | 16 | 16 | 436 | 36 | 25/06/2024 | 0 |
| 02.05.02.007-0 | ULTRASSONOGRAFIA␣␣COM DOPPLER COLORIDO DOS TESTICULOS | 11 | 11 | 362 | 47 | 15/02/2023 | 0 |
| 02.05.02.011-9 | ECOGRAFIA␣␣PROSTATA ( VIA TRANSRETAL) | 21 | 21 | 110 | 66 | 07/01/2020 | 0 |
| 02.05.02.013-5 | ECOGRAFIA DE TORAX (EXTRACARDIACO) ADULTO | 12 | 12 | 713 | 58 | 27/01/2020 | 0 |
| 02.05.02.013-5 | ECOGRAFIA DE TORAX (EXTRACARDIACO) INFANTIL | 4 | 4 | 777 | 5 | 04/05/2022 | 0 |
| 02.05.02.015-1 | ECOGRAFIA␣␣OBSTETRICA: COM DOPPLER COLORIDO | 191 | 191 | 183 | 29 | 09/04/2020 | 32 |
| 02.05.02.016-0 | ECOGRAFIA PELVICA (GINECOLOGICA) - ADULTO | 527 | 527 | 763 | 24 | 02/01/2020 | 74 |
| 02.05.02.016-0 | ECOGRAFIA PELVICA (GINECOLOGICA) - INFANTIL | 422 | 422 | 470 | 10 | 24/04/2020 | 37 |
| 02.05.02.016-0 | ULTRA-SONOGRAFIA PELVICA | 1 | 1 | 1.501 | 4 | 30/08/2022 | 0 |
| 02.05.02.016-0 | USG PELVICA | 1 | 1 | 3.564 | 43 | 05/01/2017 | 0 |

Motivo, para todas: código SIGTAP fora dos onze do objeto; só entram se o objeto mudar. Dois
casos são o "nome parecido com outro código" que o método manda procurar: o **doppler de
aorta e ilíaca** e o **doppler de região cervical** estão registrados com o código de
ultrassonografia de articulação (02.05.02.006-2), o das partes moles, e não com o de doppler.

### 1.5 O que pesa na decisão

- **TC de emergência:** seis filas adultas, 3.245 na fila (soma das linhas, calculado), com o
  mesmo código das eletivas do objeto e espera média de 342 a 365 dias, mais que o dobro da
  eletiva (128). Os CIDs são de pronto-atendimento (R10 dor abdominal, J18 pneumonia).
- **Doppler arterial de MMII** (1.781, CIDs I70, I83, I73) e **doppler de tireoide** (784)
  têm o código do doppler e da tireoide do objeto. No doppler, 1.389 das 2.514 pessoas da
  varredura já estão na fila do objeto.
- **Duas filas de doppler fora do padrão:** "ULTRA-SONOGRAFIA DOPPLER COLORIDO DE VASOS" foi
  aberta em 02/09/2026, tem 97 na fila, espera de 17 dias, nenhum agendamento e os mesmos
  CIDs do doppler venoso de MMII (I83): pode ser fila nova ou recriada para o mesmo exame. A
  "ULTRA-SONOGRAFIA␣␣DOPPLER DE CAROTIDAS E VERTEBRAIS" (190, desde 02/2023, espera de 947
  dias) não recebeu solicitação nem agendamento em 2026, e o último agendamento é de
  09/01/2025: parece a fila antiga das carótidas, parada.
- **Angiotomografias:** oito filas adultas, 1.602. A de carótidas e vertebrais (208) é
  registrada com o código de TC de abdômen superior (02.06.03.001-0), como a de coronárias
  (do objeto) é com o de tórax.
- **Infantis:** abdômen total infantil (477, idade mediana 9), aparelho urinário infantil
  (315, idade mediana 8,5) e tireoide infantil (70) têm o código do objeto e espera média de
  496 a 576 dias.
- **Sem contraste, a rede absorve:** as filas de TC sem contraste têm fila pequena e muita
  oferta — tórax sem contraste (do objeto) 26 na fila e 14.827 agendamentos de janeiro
  a setembro de 2026; abdômen superior sem contraste 10 e 4.388; pelve sem contraste 14 e
  4.362.
- **Resíduos:** trinta nomes antigos do SISREG, 70 solicitações, quase todas de 2022, sem
  nada em 2026.

**Contexto, fora da soma e fora do critério:** os outros códigos dos mesmos subgrupos SIGTAP
(02.05.01, 02.05.02, 02.06.02, 02.06.03). Os maiores são a ecocardiografia transtorácica
(02.05.01.003-2, 16.275 na fila), que não é segmento do objeto, e a ultrassonografia de
articulação (02.05.02.006-2, 11.275 em 59 nomes, sem contar partes moles), que é o código das
partes moles. Seguem globo ocular (1.271), bolsa escrotal (1.106), pélvica ginecológica (951)
e obstétrica (425). Tabela na aba 7. Os grupos 4 e 5 de tomografia do painel, inteiros, têm
19.898 na fila e 10.521 pessoas (19.762 em 06/10). As 51 filas de nome parecido em outras
modalidades (aba 9) ficam fora por não serem ultrassom nem tomografia; as maiores são a consulta de
ginecologia por dor pélvica (977), a ressonância de bacia com contraste (912) e a radiografia
de tórax (659).

## 2. Fila por código SIGTAP

Só os nomes de fila do enquadramento. Δ = diferença para 06/10.

| código | procedimento | nomes | fila | **pessoas** | devolvidas | espera média | mediana | máxima | Δ fila | Δ pessoas |
|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.009-7 | Ultrassonografia mamária bilateral | 1 | 13.762 | **13.739** | 7.760 | 623 | 506 | 6.105 | +24 | +24 |
| 02.05.02.018-6 | Ultrassonografia transvaginal | 1 | 9.814 | **9.813** | 8.947 | 636 | 494 | 5.869 | −137 | −137 |
| 02.05.02.004-6 | Ultrassonografia de abdômen total | 3 | 13.375 | **13.108** | 13.005 | 548 | 364 | 6.100 | +48 | +48 |
| 02.05.01.004-0 | Ultrassonografia doppler colorido de vasos | 2 | 14.510 | **14.348** | 3.346 | 471 | 298 | 1.453 | +71 | +69 |
| 02.05.02.005-4 | Ultrassonografia de aparelho urinário | 1 | 3.899 | **3.898** | 3.440 | 640 | 443 | 5.770 | +12 | +12 |
| 02.05.02.012-7 | Ultrassonografia de tireoide | 1 | 3.168 | **3.168** | 2.727 | 479 | 368 | 2.101 | +18 | +18 |
| 02.05.02.010-0 | Ultrassonografia de próstata por via abdominal | 1 | 3.337 | **3.331** | 2.713 | 583 | 464 | 5.980 | +12 | +12 |
| 02.05.02.003-8 | Ultrassonografia de abdômen superior | 1 | 2.271 | **2.269** | 1.026 | 693 | 603 | 5.861 | −5 | −5 |
| 02.06.03.001-0 | Tomografia computadorizada de abdômen superior | 1 | 4.125 | **4.122** | 5.322 | 128 | 128 | 826 | +30 | +30 |
| 02.06.03.003-7 | Tomografia computadorizada de pelve / bacia / abdômen inferior | 1 | 3.649 | **3.647** | 3.737 | 129 | 128 | 841 | +11 | +11 |
| 02.06.02.003-1 | Tomografia computadorizada de tórax | 3 | 3.967 | **3.944** | 4.193 | 185 | 150 | 1.033 | +39 | +37 |
| | **ultrassonografia** | 11 | **64.136** | **55.608** | 42.964 | 569 | 413 | 6.105 | +43 | +42 |
| | **tomografia** | 5 | **11.741** | **6.297** | 13.252 | 148 | 135 | 1.033 | +80 | +60 |
| | **objeto** | 16 | **75.877** | **61.132** | 56.216 | 504 | 309 | 6.105 | +123 | +94 |

As linhas de conjunto saem do motor, não da soma das linhas: as pessoas são CNS distintos no
conjunto. Na tomografia, **3.500 pessoas** esperam TC de abdômen superior e TC de pelve ao
mesmo tempo (eram 3.488 em 06/10); por isso 11.741 solicitações são de 6.297 pessoas.

*Fora do objeto, à parte:* partes moles (`ECOGRAFIA␣␣DE PARTES MOLES`, 02.05.02.006-2) tem
**3.116** na fila, 3.115 pessoas, 1.492 devolvidas, espera média de 661 dias e mediana de
541. Ultrassonografia com partes moles: 67.252 na fila e 58.216 pessoas; 507 pessoas da fila
de partes moles já estão na fila de ultrassonografia do objeto.

## 3. Fila a fila

| | fila (nome curto) | nome interno no SISREG | SIGTAP | fila | pessoas | devolvidas | espera média | mediana | máxima | fila 06/10 | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US | Mama bilateral | ECOGRAFIA DE MAMAS - BILATERAL | 02.05.02.009-7 | 13.762 | 13.739 | 7.760 | 623 | 506 | 6.105 | 13.738 | +24 |
| US | Transvaginal | ECOGRAFIA TRANSVAGINAL | 02.05.02.018-6 | 9.814 | 9.813 | 8.947 | 636 | 494 | 5.869 | 9.951 | −137 |
| US | Abdômen total | ECOGRAFIA DE ABDOMEN TOTAL ADULTO | 02.05.02.004-6 | 10.175 | 10.170 | 11.702 | 534 | 332 | 6.100 | 10.134 | +41 |
| US | Doppler MMII | ULTRA-SONOGRAFIA DOPPLER VENOSO - MMII ( BILATERAL) | 02.05.01.004-0 | 9.930 | 9.928 | 600 | 622 | 571 | 1.453 | 9.902 | +28 |
| US | Carótidas | 10. ECODOPPLER DE CAROTIDAS | 02.05.01.004-0 | 4.580 | 4.580 | 2.746 | 144 | 137 | 568 | 4.537 | +43 |
| US | Aparelho urinário | ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA) ADULTO | 02.05.02.005-4 | 3.899 | 3.898 | 3.440 | 640 | 443 | 5.770 | 3.887 | +12 |
| US | Tireoide | ECOGRAFIA DE TIREOIDE ADULTO | 02.05.02.012-7 | 3.168 | 3.168 | 2.727 | 479 | 368 | 2.101 | 3.150 | +18 |
| US | Próstata | ECOGRAFIA DE PROSTATA ( VIA ABDOMINAL ) | 02.05.02.010-0 | 3.337 | 3.331 | 2.713 | 583 | 464 | 5.980 | 3.325 | +12 |
| US | Parede abdominal | ULTRASONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | 3.199 | 3.199 | 1.303 | 595 | 507 | 2.429 | 3.192 | +7 |
| US | Parede abdominal (variante) | ULTRA-SONOGRAFIA DE PAREDE ABDOMINAL | 02.05.02.004-6 | 1 | 1 | 0 | 1.501 | 1.501 | 1.501 | 1 | 0 |
| US | Abdômen superior | ECOGRAFIA DE ABDOMEN SUPERIOR ADULTO | 02.05.02.003-8 | 2.271 | 2.269 | 1.026 | 693 | 603 | 5.861 | 2.276 | −5 |
| TC | TC abdômen sup. c/contraste | 063. TC DO ABDOMEN SUPERIOR ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.001-0 | 4.125 | 4.122 | 5.322 | 128 | 128 | 826 | 4.095 | +30 |
| TC | TC pelve c/contraste | 111. TC DE PELVE OU BACIA ADULTO C/CONTRASTE S/SEDACAO | 02.06.03.003-7 | 3.649 | 3.647 | 3.737 | 129 | 128 | 841 | 3.638 | +11 |
| TC | TC tórax c/contraste | 055. TC DO TORAX ADULTO C/CONTRASTE S/SEDACAO | 02.06.02.003-1 | 2.466 | 2.463 | 1.881 | 129 | 128 | 893 | 2.448 | +18 |
| TC | Angiotomografia de coronárias | ANGIOTOMOGRAFIA[NBSP]␣DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO | 02.06.02.003-1 | 1.475 | 1.475 | 139 | 279 | 253 | 659 | 1.460 | +15 |
| TC | TC tórax s/contraste | 053. TC DO TORAX␣␣ADULTO S/CONTRASTE S/SEDACAO | 02.06.02.003-1 | 26 | 26 | 2.173 | 200 | 87 | 1.033 | 20 | +6 |
| fora | Partes moles | ECOGRAFIA␣␣DE PARTES MOLES | 02.05.02.006-2 | 3.116 | 3.115 | 1.492 | 661 | 541 | 5.825 | 3.104 | +12 |

␣␣ = dois espaços comuns; [NBSP]␣ = espaço não separável (U+00A0) seguido de espaço comum.
O JSON guarda o nome exato. A variante da parede abdominal é uma solicitação só, de
30/08/2022. A espera máxima de 5.770 a 6.105 dias (mama, transvaginal, abdômen total e
superior, aparelho urinário, próstata, partes moles) vem de solicitações de 2010 ainda na
fila; a mediana é a medida mais estável.

## 4. Por Região de Saúde — medida fila

Região de Saúde da unidade solicitante. URD, Contratado/Credenciado e Público – Não SES não
são Região de Saúde: são unidades de referência e prestadores que solicitam direto. A linha
sem região é o campo vazio no painel. Nenhuma linha foi rateada. As pessoas por Região não
somam o total: quem tem solicitação vinda de duas Regiões conta nas duas.

| Região | ultrassonografia | tomografia | **objeto — fila** | % da fila (calculado) | objeto — pessoas | partes moles (fora) |
|---|---|---|---|---|---|---|
| Central | 2.967 | 486 | 3.453 | 4,6% | 3.156 | 3 |
| Centro-Sul | 5.927 | 213 | 6.140 | 8,1% | 5.459 | 287 |
| Leste | 10.680 | 429 | 11.109 | 14,6% | 8.842 | 605 |
| Norte | 3.575 | 782 | 4.357 | 5,7% | 3.945 | 97 |
| Oeste | 3.324 | 869 | 4.193 | 5,5% | 3.760 | 244 |
| Sudoeste | 21.571 | 2.124 | 23.695 | 31,2% | 19.773 | 1.695 |
| Sul | 14.334 | 692 | 15.026 | 19,8% | 12.431 | 155 |
| URD | 589 | 4.369 | 4.958 | 6,5% | 2.529 | 0 |
| Contratado/Credenciado | 493 | 1.714 | 2.207 | 2,9% | 1.325 | 0 |
| Público – Não SES | 1 | 0 | 1 | 0,0% | 1 | 0 |
| **sem região informada** | **675** | **63** | **738** | 1,0% | 656 | 30 |
| **total** | **64.136** | **11.741** | **75.877** | 100% | 61.132 | 3.116 |

**Na tomografia, URD e Contratado/Credenciado são 6.083 das 11.741 solicitações (51,8%,
calculado)**; na ultrassonografia, 1.082 de 64.136 (1,7%).

Por código, na fila:

| Região | 02.05.02.009-7 | 02.05.02.018-6 | 02.05.02.004-6 | 02.05.01.004-0 | 02.05.02.005-4 | 02.05.02.012-7 | 02.05.02.010-0 | 02.05.02.003-8 | 02.06.03.001-0 | 02.06.03.003-7 | 02.06.02.003-1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Central | 1.333 | 0 | 607 | 1.012 | 0 | 10 | 1 | 4 | 163 | 129 | 194 |
| Centro-Sul | 509 | 397 | 2.061 | 573 | 817 | 582 | 606 | 382 | 55 | 44 | 114 |
| Leste | 2.525 | 3.166 | 2.244 | 239 | 811 | 569 | 898 | 228 | 131 | 92 | 206 |
| Norte | 17 | 62 | 53 | 3.334 | 22 | 60 | 16 | 11 | 265 | 253 | 264 |
| Oeste | 1.649 | 436 | 366 | 605 | 59 | 109 | 50 | 50 | 261 | 165 | 443 |
| Sudoeste | 5.431 | 4.328 | 4.080 | 3.397 | 1.339 | 838 | 594 | 1.564 | 789 | 685 | 650 |
| Sul | 2.131 | 1.328 | 3.800 | 4.104 | 806 | 980 | 1.156 | 29 | 247 | 239 | 206 |
| URD | 10 | 1 | 5 | 569 | 1 | 0 | 1 | 2 | 1.596 | 1.464 | 1.309 |
| Contratado/Credenciado | 0 | 0 | 1 | 492 | 0 | 0 | 0 | 0 | 595 | 558 | 561 |
| Público – Não SES | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **sem região informada** | 157 | 96 | 158 | 185 | 44 | 19 | 15 | 1 | 23 | 20 | 20 |
| **total** | 13.762 | 9.814 | 13.375 | 14.510 | 3.899 | 3.168 | 3.337 | 2.271 | 4.125 | 3.649 | 3.967 |

Fila por nome de fila e Região na aba 4 da planilha.

## 5. Diferença para 06/10 — CALCULADO

| | 06/10 (base 21:32) | **09/10 (base 11:32)** | Δ |
|---|---|---|---|
| solicitação mais recente na base | 30/09/2026 | **02/10/2026** | +2 dias |
| ultrassonografia — fila | 64.093 | **64.136** | +43 |
| ultrassonografia — pessoas | 55.566 | **55.608** | +42 |
| tomografia — fila | 11.661 | **11.741** | +80 |
| tomografia — pessoas | 6.237 | **6.297** | +60 |
| objeto — fila | 75.754 | **75.877** | +123 |
| objeto — pessoas | 61.038 | **61.132** | +94 |
| objeto — devolvidas | 56.239 | 56.216 | −23 |
| espera média — ultrassonografia | 568 | 569 | +1 |
| espera média — tomografia | 147 | 148 | +1 |

A base ganhou dois dias de solicitações (1º e 2/10). As filas sobem de 6 a 43, menos a de
abdômen superior (−5), a variante da parede abdominal (0) e a transvaginal; a espera média
sobe cerca de um dia. **A exceção é a transvaginal: 137 a menos na fila (9.951 para
9.814), com as devolvidas paradas (8.949 para 8.947)**; a queda está na Região Sudoeste (−77)
e na Oeste (−70). O painel não diz para onde as 137 foram. A TC de tórax sem contraste passou
de 20 para 26, e a espera média dela caiu de 256 para 200 dias com as seis entradas novas.
Diferença fila a fila, por código e por Região na aba 8.

## 6. Lacunas

- **Para onde saíram as 137 transvaginais:** o painel não guarda o histórico de status da
  solicitação; só a comparação entre coletas mostra a saída, não o destino.
- **Outubro incompleto:** a solicitação mais recente é de 02/10/2026, uma semana antes da
  consulta. A base só tem os dois primeiros dias do mês.
- **"Mesmos segmentos":** o painel não tem campo de segmento, e o grupo de procedimento não
  serve (seção 1). A varredura usou o código SIGTAP e o nome; outro critério (por exemplo, o
  subgrupo SIGTAP inteiro) daria outro tamanho, e a aba 7 traz esse contexto.
- **Espera máxima:** 6.105 dias na mama; são solicitações de 2010 ainda pendentes. O painel
  não diz se são registros esquecidos ou espera real.
- **Oferta:** as agendadas são contadas pela data marcada do exame (`data_agendamento`, que
  vai até 2027). O painel não diz quantas foram realizadas.
- **Duas solicitações em dois nomes** na varredura (9.378 no motor, 9.380 na soma das
  linhas): o painel não mostra quais, sem expor o registro. No objeto, nenhuma.
- **Idade e entrantes:** entrantes não coletados, por não serem pedidos (o pré-plano não
  dimensiona produção mensal). A idade aparece só como mediana por fila, no estudo da
  varredura que o método pede; o pré-plano não afirma faixa etária.
