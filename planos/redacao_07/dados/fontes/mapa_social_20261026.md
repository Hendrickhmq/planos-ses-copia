# Mapa Social da Saúde — filas de exames de imagem para reabrir a carteira do redacao_07, recarga de 26/10/2026 16:32

Recoleta do agente `mapa-social` para o redacao_07: Emenda de Bancada do DF 71080005 (proposta
36000722999202500), R$ 1.502.687,00, federal, ação 2E90, proponente ISHP (Instituto de Saúde
Humanidade e Pesquisa), objeto "Exames de imagem" (Ofício 88/2026 da Bancada; Ofício 398/2026 da
ARINS). **O objeto são exames avulsos, não OCI:** não há CID da OCI nem finalidade de ficha; a
medida é a fila do exame inteira, com qualquer CID, e a fila viva ao lado. Método de 25/10/2026
(`metodo/coleta/mapa_social.md`, ramo `melhorias/agentes`). A coleta de 15/10/2026
(`mapa_social_20261015.md`, ramo `pre-plano-07-imagem-bancada`) não se sobrescreve e foi o ponto
de partida da varredura. Planilha em `mapa_social_20261026.xlsx`; JSON do motor, JSON da coleta
no formato do método e scripts em `mapa_social_20261026_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 26/10/2026 16:32:44 (qLastReloadTime 2026-10-26T19:32:44.246Z), conferida no início e no fim da leitura |
| Consulta | 26/10/2026 16:46:44 a 16:48:33 (relógio do motor, Brasília), numa ida só |
| Solicitação mais recente na base | 26/10/2026 (agendamento mais distante: 27/01/2027; pedido mais antigo da base: 05/07/2007) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | só os pedidos de 26/10/2024 em diante (24 meses contados da solicitação mais recente), `data_solicitacao={">=26/10/2024"}`; conferida contra a soma por ano: 2.620 (2024) + 27.795 (2025) + 95.801 (2026) = 126.216, igual ao motor |
| Agendadas 12 meses | `data_agendamento={">=26/10/2025<=25/10/2026"}`, todos os status do agendamento, pelo código (`codigo_sigtap_agendamento`) ou pelo par nome × código. É a data do atendimento marcado, não a da marcação nem a do exame feito |
| Anos de estoque | fila ÷ agendadas em 12 meses (**calculado**) |
| Recorte | todos os anos na fila inteira; sem recorte de CID; universo `codigo_sigtap_solicitacao={"204*","205*","206*","207*","208*","210*"}` (02.04 a 02.08 e 02.10; o 02.09, endoscopia, fica fora por não ser imagem: 54.445 na fila) e a busca por nome fora dele |
| Via | Qlik Engine API do próprio painel (hipercubos de sessão e evaluateEx), no navegador embutido |
| Comparação | coleta de 15/10/2026 (recarga 19:32:31), código a código e recorte a recorte (seção 4) |

**A base recarregou durante a coleta.** O painel foi aberto às 16:24:21 com a base de 26/10/2026
14:36:46; a recarga das 16:32:44 entrou no meio da transcrição. Tudo o que está aqui saiu depois
dela, numa ida só (16:46:44 a 16:48:33), com a recarga conferida no início e no fim; o que foi
lido antes foi descartado.

Pessoas = CNS distintos no conjunto (quem espera por mais de um exame conta uma vez); só a
contagem sai do motor. Espera em dias, calculada no motor sobre os registros do conjunto (não é
média das linhas). Códigos diferentes não se somam como se fossem um objeto; a união da carteira
foi medida no motor (seção 1.1).

## Alarmes

Dos seis alarmes do método, dois cabem em exame avulso: **estoque** e **fila velha**. Os outros
quatro (CID largo, CID dominante, CID raro, fila genérica) são da OCI e não se aplicam: não há
CID de ficha nem composição. As filas genéricas do universo (os 7 nomes
de ecocardiografia transtorácica e o tórax PA e perfil) estão marcadas no JSON. Limites do método, propostos em
25/10/2026 e ainda a confirmar: estoque acima de 3 anos (ou nenhuma agendada em 12 meses), fila
velha acima de 30% da fila com pedido de antes de 26/10/2024.

Refeitos fila a fila (nome × código) sobre as 684 filas com gente esperando: **126 de
estoque e 85 de fila velha**. A maior parte está em nomes de fila pequenos e antigos (resíduo
de 2007 a 2023, sem pedido em 2026); a lista inteira está na aba 9 da planilha e em `alarmes`
no JSON. Os que pesam na carteira e na tabela de destaque:

**fila velha** — mais de 30% da fila com pedido de antes de 26/10/2024:
- **US pélvica (ginecológica) 02.05.02.016-0** (carteira): 317 de 1.025 (31%), pedido mais antigo de 05/01/2017. Na fila adulto, 234 de 583 (40%).
- **US de bolsa escrotal 02.05.02.007-0** (carteira): 344 de 967 (36%), pedido mais antigo de 27/01/2021. Na fila adulto, 277 de 706 (39%).
- **US de articulação, partes moles** (pode voltar): 1.245 de 3.117 (40%), desde 28/10/2010; joelho E e D adulto, 34% e 35%; "outras regiões", 157 de 438 (36%).
- **Mesmo código do plano 4, enquadramento** (só sobreposição): US mamária 4.446 de 13.182 (34%), transvaginal 3.622 de 9.648 (38%), doppler venoso de MMII 3.984 de 10.019 (40%), aparelho urinário adulto 1.280 de 3.773 (34%), parede abdominal 1.105 de 3.292 (34%), abdômen superior adulto 983 de 2.225 (44%).
- **US de tórax extracardíaca** 02.05.02.013-5 (pode voltar): 9 de 17 (53%).

**estoque** — fila acima de 3 anos de agendamentos, ou sem agendamento em 12 meses:
- **US de próstata transretal 02.05.02.011-9** (pode voltar): 22 na fila e 5 agendadas em 12 meses, **4,4 anos**.
- **US de tórax (extracardíaca) 02.05.02.013-5** (pode voltar): 17 na fila, **nenhuma agendada em 12 meses**.
- **US de articulação, "outras regiões"** (braço, perna, axila, coluna lombar infantil, glândulas, pelve): 438 na fila e 90 agendadas, **4,9 anos**; a fila "ARTICULACAO COLUNA LOMBAR" (infantil, Q76) tem 134 e 4 agendadas (33,5 anos); US do pescoço, 160 e 35 (4,6 anos); coxo-femural infantil E e D, 6,8 e 5,5 anos.
- **Plano 4** (só sobreposição): angiotomografia de coronárias adulto, 1.530 na fila e 137 agendadas, **11,2 anos**; doppler arterial de MMII, 1.790 e 504 (3,6 anos); doppler de carótidas e vertebrais antigo, 190 e nenhuma (só resíduo).
- Fora da tabela de destaque: cintilografia de miocárdio de estresse (1.728 e 365, 4,7 anos) e de repouso (1.489 e 347, 4,3 anos).

Na carteira, nenhum código passa de 3 anos: o maior é a US de globo ocular (1.308 na fila, 598
agendadas, 2,2 anos). O estoque por nome de fila pode exagerar quando a oferta é marcada com
outro nome: nos códigos da tabela de destaque há nomes que só existem na tabela de agendamentos
(aba 12); o número por código é a referência.

**O que o método não resolve e fica para a conversa:**
- **As TC da carteira misturam pronto-atendimento e angiotomografia com o exame eletivo.** TC de
  crânio 1.453 = eletiva 452 (espera média 106 dias) + emergência 619 (362 dias) + angiotomografia
  382 (75 dias); TC de pescoço 779 = 503 + 100 + 176; TC de face 470 = eletiva 398 (das quais 191
  de tomografia cone beam, odontológica) + emergência 72; TC de sela 48 = 27 + 21. Em 15/10 a
  carteira contou o código inteiro. As filas de emergência vêm quase todas da Região Sudoeste
  (532 de 619 na TC de crânio). Marcadas **a decidir**.
- **A mamografia de rastreamento carrega pedido de diagnóstico.** No código 02.04.03.018-8, a fila
  "screening" tem 486 pedidos com queixa ou achado mamário (N60–N64, R92, D24, D48) e 214 com câncer
  de mama (C50); a fila "diagnóstica" tem 192 (101 com queixa). 43 pedidos são de menores de 35
  anos, abaixo da idade da ficha (seção 2).
- **A ecocardiografia caiu 1.577 em onze dias** (16.298 para 14.721), a angiorressonância 144
  (287 para 143), a RM de abdômen 212 e a RM de mama 75 (84 para 9). O painel não diz para onde os
  pedidos saíram.
- **Elastografia hepática 02.05.02.022-4:** nenhum pedido nem agendamento na base, em nenhum status.

## 1. Tabela de destaque

Por código SIGTAP, todos os nomes de fila do código (motor). A espera é a do código inteiro;
dentro do código, os recortes por nome estão em cada subseção. "Pedidos de 2026 na fila" =
fila com `Ano_Solicitacao=2026`.

### 1.1 Carteira atual (doze códigos)

| código | exame | fila | fila viva | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | pedidos de 2026 na fila | agendadas 12 m | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | **6.917** | 6.832 | 6.912 | 2.679 | 66 | 28 | 2.180 | 06/11/2020 | 6.753 | 55.649 | 0,1 | — |
| 02.04.06.002-8 | Densitometria óssea | **2.188** | 2.185 | 2.188 | 3.672 | 46 | 32 | 2.169 | 17/11/2020 | 2.185 | 12.827 | 0,2 | — |
| 02.05.02.016-0 | US pélvica (ginecológica) | **1.025** | 708 | 1.016 | 924 | 606 | 384 | 3.581 | 05/01/2017 | 459 | 1.360 | 0,8 | fila velha |
| 02.05.02.007-0 | US de bolsa escrotal | **967** | 623 | 966 | 507 | 571 | 467 | 2.098 | 27/01/2021 | 382 | 916 | 1,1 | fila velha |
| 02.05.02.008-9 | US de globo ocular / órbita | **1.308** | 1.308 | 1.308 | 198 | 267 | 272 | 502 | 11/06/2025 | 712 | 598 | 2,2 | — |
| 02.05.02.017-8 | US transfontanela | **291** | 262 | 291 | 202 | 292 | 222 | 1.587 | 22/06/2022 | 193 | 826 | 0,4 | — |
| 02.05.02.014-3 | US obstétrica | **487** | 485 | 486 | 937 | 145 | 61 | 7.006 | 22/08/2007 | 422 | 2.957 | 0,2 | — |
| 02.05.02.015-1 | US obstétrica com doppler | **169** | 169 | 169 | 147 | 196 | 152 | 598 | 07/03/2025 | 125 | 376 | 0,4 | — |
| 02.06.01.005-2 | TC de pescoço | **779** | 773 | 770 | 662 | 139 | 116 | 840 | 08/07/2024 | 731 | 2.432 | 0,3 | — |
| 02.06.01.007-9 | TC de crânio | **1.453** | 1.425 | 1.423 | 2.758 | 206 | 129 | 843 | 05/07/2024 | 1.090 | 14.949 | 0,1 | — |
| 02.06.01.004-4 | TC de face / seios / ATM | **470** | 468 | 453 | 881 | 138 | 101 | 843 | 05/07/2024 | 419 | 5.406 | 0,1 | — |
| 02.06.01.006-0 | TC de sela túrcica | **48** | 48 | 46 | 165 | 169 | 128 | 605 | 28/02/2025 | 37 | 419 | 0,1 | — |

**União dos doze no motor:** 16.102 na fila, **15.524 pessoas** (15.286 na fila viva,
14.730 pessoas), das quais **2.708 também esperam na fila do plano 4** (os dezesseis
nomes do enquadramento; mesma pessoa, não o mesmo exame); 98.715 agendadas em 12 meses. **Sem
mamografia e densitometria (os dez):** 6.997 na fila, 6.628 pessoas (5.911
na viva), 1.102 também na fila do plano 4, espera média de 313 dias, 4.570
pedidos de 2026 na fila e 30.239 agendadas em 12 meses.

**Recortes da carteira** — dentro do código, por nome de fila:

| código | recorte (nomes de fila) | nomes | fila | fila viva | pessoas | espera média | mediana | pedido mais antigo | pedidos de 2026 | agendadas 12 m (pelos nomes) | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | MAMOGRAFIA BILATERAL PARA SCREENING (ROTINA) | 1 | **6.725** | 6.641 | 6.724 | 66 | 30 | 06/11/2020 | 6.562 | 50.608 | 0,1 | — |
| 02.04.03.018-8 | MAMOGRAFIA BILATERAL DIAGNOSTICA | 1 | **192** | 191 | 192 | 47 | 21 | 05/11/2021 | 191 | 5.041 | 0,0 | — |
| 02.06.01.007-9 | eletiva | 8 | **452** | 445 | 449 | 106 | 84 | 05/07/2024 | 444 | 11.713 | 0,0 | — |
| 02.06.01.007-9 | emergência | 4 | **619** | 598 | 603 | 362 | 361 | 23/09/2024 | 267 | 1.593 | 0,4 | — |
| 02.06.01.007-9 | angiotomografia | 2 | **382** | 382 | 382 | 75 | 69 | 08/11/2024 | 379 | 1.641 | 0,2 | — |
| 02.06.01.005-2 | eletiva | 2 | **503** | 501 | 502 | 116 | 112 | 08/07/2024 | 501 | 1.826 | 0,3 | — |
| 02.06.01.005-2 | emergência | 4 | **100** | 96 | 98 | 330 | 285 | 24/09/2024 | 54 | 152 | 0,7 | — |
| 02.06.01.005-2 | angiotomografia | 2 | **176** | 176 | 176 | 97 | 91 | 23/02/2026 | 176 | 416 | 0,4 | — |
| 02.06.01.004-4 | eletiva | 14 | **398** | 396 | 390 | 95 | 88 | 05/07/2024 | 396 | 5.064 | 0,1 | — |
| 02.06.01.004-4 | emergência | 15 | **72** | 72 | 63 | 376 | 424 | 08/11/2024 | 23 | 119 | 0,6 | — |
| 02.06.01.006-0 | eletiva | 3 | **27** | 27 | 27 | 80 | 45 | 24/03/2026 | 27 | 228 | 0,1 | — |
| 02.06.01.006-0 | emergência | 7 | **21** | 21 | 20 | 284 | 357 | 28/02/2025 | 10 | 11 | 1,9 | — |

Na TC de face eletiva estão os 191 pedidos de "TOMOGRAFIA CONE BEAN" (espera média 89 dias; CID K01, K04,
S02: odontológica), também **a decidir**. As US da carteira não têm fila de emergência; a US pélvica tem fila
adulto (583, espera média 704 dias) e infantil (440, 468 dias); a bolsa escrotal, adulto (706, 603 dias) e
infantil (234, 491 dias); a obstétrica, a geral (358) e as morfológicas de 1º trimestre (73) e geral (56).

**Idade, onde a ficha restringe** (fichas SIGTAP 10/2026 do redacao_07; nenhuma ficha restringe o sexo desde
05–06/2024, e o sexo não foi aberto):

| código | ficha | nome de fila | fila | na idade da ficha | fora | pessoas na idade | viva na idade |
|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | 35 a 130 anos | MAMOGRAFIA BILATERAL PARA SCREENING (ROTINA) | 6.725 | 6.691 | 34 (abaixo) | 6.690 | 6.613 |
| 02.04.03.018-8 | 35 a 130 anos | MAMOGRAFIA BILATERAL DIAGNOSTICA | 192 | 183 | 9 (abaixo) | 183 | 182 |
| 02.05.01.005-9 | 8 a 60 anos | ECOGRAFIA DOPPLER FLUXO OBSTETRICO | 15 | 15 | 0 (acima) | 15 | 15 |
| 02.05.02.014-3 | 8 a 60 anos | ECOGRAFIA MORFOLOGICA DO 1° TRIMESTRE | 73 | 73 | 0 (acima) | 73 | 73 |
| 02.05.02.014-3 | 8 a 60 anos | ECOGRAFIA OBSTETRICA MORFOLOGICA | 56 | 56 | 0 (acima) | 56 | 55 |
| 02.05.02.014-3 | 8 a 60 anos | ECOGRAFIA OBSTETRICA | 358 | 358 | 0 (acima) | 358 | 357 |
| 02.05.02.015-1 | 8 a 60 anos | ECOGRAFIA␣␣OBSTETRICA: COM DOPPLER COLORIDO | 169 | 169 | 0 (acima) | 169 | 169 |
| 02.05.02.017-8 | 0 a 4 anos | ULTRA-SONOGRAFIA TRANSFONTANELA | 289 | 287 | 2 (acima) | 287 | 261 |
| 02.05.02.017-8 | 0 a 4 anos | ULTRA-SONOGRAFIA TRANSFONTANELAR | 2 | 1 | 1 (acima) | 1 | 0 |

Mamografia na faixa de 50 a 69 anos (a do rastreamento do Ministério; a ficha aceita de 35 em diante):
4.470 da fila "screening" e 101 da "diagnóstica".

**Região de Saúde da unidade solicitante** (fila, na medida da fila; "sem região" é o campo vazio; URD e
contratado não são Região de Saúde e vão à parte; nenhuma linha foi rateada):

| código | exame | Central | Centro-Sul | Leste | Norte | Oeste | Sudoeste | Sul | URD | Contrat./Cred. | outros | **sem região** | total | URD + contrat. (% calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | 467 | 1.487 | 1.790 | 584 | 759 | 596 | 537 | 354 | 215 | 0 | **128** | 6.917 | 8,2% |
| 02.04.06.002-8 | Densitometria óssea | 163 | 244 | 148 | 190 | 256 | 498 | 193 | 295 | 159 | 0 | **42** | 2.188 | 20,7% |
| 02.05.02.016-0 | US pélvica (ginecológica) | 4 | 314 | 410 | 17 | 86 | 56 | 126 | 1 | 1 | 0 | **10** | 1.025 | 0,2% |
| 02.05.02.007-0 | US de bolsa escrotal | 5 | 185 | 135 | 11 | 38 | 514 | 71 | 0 | 0 | 0 | **8** | 967 | 0,0% |
| 02.05.02.008-9 | US de globo ocular / órbita | 424 | 24 | 13 | 2 | 7 | 200 | 32 | 583 | 22 | 0 | **1** | 1.308 | 46,3% |
| 02.05.02.017-8 | US transfontanela | 0 | 104 | 11 | 1 | 0 | 18 | 153 | 0 | 2 | 0 | **2** | 291 | 0,7% |
| 02.05.02.014-3 | US obstétrica | 2 | 3 | 187 | 75 | 47 | 69 | 83 | 0 | 0 | 0 | **21** | 487 | 0,0% |
| 02.05.02.015-1 | US obstétrica com doppler | 0 | 0 | 61 | 1 | 0 | 33 | 62 | 0 | 0 | 0 | **12** | 169 | 0,0% |
| 02.06.01.005-2 | TC de pescoço | 15 | 9 | 13 | 17 | 44 | 162 | 18 | 351 | 145 | 1 | **4** | 779 | 63,7% |
| 02.06.01.007-9 | TC de crânio | 27 | 35 | 102 | 57 | 78 | 670 | 56 | 284 | 110 | 0 | **34** | 1.453 | 27,1% |
| 02.06.01.004-4 | TC de face / seios / ATM | 35 | 12 | 50 | 24 | 72 | 125 | 27 | 98 | 24 | 0 | **3** | 470 | 26,0% |
| 02.06.01.006-0 | TC de sela túrcica | 1 | 0 | 2 | 0 | 4 | 25 | 2 | 8 | 6 | 0 | **0** | 48 | 29,2% |

Nos recortes de TC, a emergência é quase toda da Região Sudoeste:

| código | exame | Central | Centro-Sul | Leste | Norte | Oeste | Sudoeste | Sul | URD | Contrat./Cred. | outros | **sem região** | total | URD + contrat. (% calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.06.01.007-9 | TC de crânio — eletiva | 17 | 19 | 51 | 22 | 51 | 107 | 23 | 108 | 45 | 0 | **9** | 452 | 33,8% |
| 02.06.01.007-9 | TC de crânio — emergência | 0 | 3 | 42 | 5 | 5 | 532 | 2 | 8 | 0 | 0 | **22** | 619 | 1,3% |
| 02.06.01.007-9 | TC de crânio — angiotomografia | 10 | 13 | 9 | 30 | 22 | 31 | 31 | 168 | 65 | 0 | **3** | 382 | 61,0% |
| 02.06.01.005-2 | TC de pescoço — eletiva | 8 | 5 | 10 | 9 | 33 | 51 | 8 | 286 | 91 | 1 | **1** | 503 | 75,0% |
| 02.06.01.005-2 | TC de pescoço — emergência | 0 | 0 | 1 | 1 | 0 | 95 | 0 | 0 | 0 | 0 | **3** | 100 | 0,0% |
| 02.06.01.005-2 | TC de pescoço — angiotomografia | 7 | 4 | 2 | 7 | 11 | 16 | 10 | 65 | 54 | 0 | **0** | 176 | 67,6% |

### 1.2 Os que saíram ou ficaram de fora e podem voltar

Decisão: **a decidir** (reabertura pedida em 26/10/2026), menos os nomes-resíduo (sem pedido nem
agendamento em 2026), que ficam fora. Os motivos de 15 a 20/10 estão em `decidir()` e na aba 7.

| código | exame | fila | fila viva | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | pedidos de 2026 na fila | agendadas 12 m | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | Ecocardiografia transtorácica | **14.721** | 14.716 | 14.716 | 16.413 | 127 | 116 | 6.978 | 19/09/2007 | 14.139 | 40.355 | 0,4 | — |
| 02.05.02.006-2 | US de articulação | **14.391** | 10.396 | 11.435 | 5.193 | 547 | 398 | 6.025 | 29/04/2010 | 5.725 | 8.039 | 1,8 | — |
| 02.05.02.011-9 | US de próstata transretal | **22** | 22 | 22 | 133 | 120 | 104 | 229 | 11/03/2026 | 22 | 5 | 4,4 | estoque |
| 02.05.02.013-5 | US de tórax (extracardíaca) | **17** | 8 | 17 | 13 | 704 | 760 | 1.358 | 06/02/2023 | 7 | 0 | sem agendamento | estoque, fila velha |
| 02.05.01.005-9 | Doppler de fluxo obstétrico | **15** | 15 | 15 | 34 | 102 | 117 | 195 | 14/04/2026 | 15 | 16 | 0,9 | — |
| 02.05.02.022-4 | Elastografia hepática | 0 | 0 | 0 | 0 | — | — | — | — | 0 | 0 | — | sem fila nem agendamento na base |
| 02.06.01.001-0 | TC de coluna cervical | **139** | 136 | 137 | 373 | 189 | 129 | 762 | 24/09/2024 | 112 | 1.478 | 0,1 | — |
| 02.06.01.003-6 | TC de coluna torácica | **79** | 78 | 77 | 154 | 198 | 137 | 754 | 02/10/2024 | 63 | 1.093 | 0,1 | — |
| 02.06.01.002-8 | TC de coluna lombo-sacra | **164** | 157 | 162 | 370 | 230 | 146 | 763 | 23/09/2024 | 115 | 3.182 | 0,1 | — |
| 02.06.02.002-3 | TC de segmentos apendiculares | **219** | 219 | 164 | 223 | 203 | 108 | 728 | 28/10/2024 | 162 | 2.310 | 0,1 | — |
| 02.06.02.001-5 | TC de articulações de membro superior | **71** | 69 | 68 | 101 | 261 | 182 | 736 | 20/10/2024 | 43 | 1.032 | 0,1 | — |
| 02.06.03.002-9 | TC de articulações de membro inferior | **242** | 239 | 206 | 255 | 258 | 185 | 756 | 30/09/2024 | 145 | 1.703 | 0,1 | — |

**Recortes:**

| código | recorte (nomes de fila) | nomes | fila | fila viva | pessoas | espera média | mediana | pedido mais antigo | pedidos de 2026 | agendadas 12 m (pelos nomes) | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | adulto | 1 | **13.373** | 13.373 | 13.373 | 127 | 117 | 12/05/2025 | 12.801 | 33.740 | 0,4 | — |
| 02.05.01.003-2 | infantil | 1 | **1.306** | 1.306 | 1.305 | 107 | 102 | 12/11/2024 | 1.302 | 5.833 | 0,2 | — |
| 02.05.01.003-2 | fetal | 1 | **37** | 37 | 37 | 28 | 10 | 29/12/2025 | 36 | 782 | 0,0 | — |
| 02.05.01.003-2 | outros nomes | 4 | **5** | 0 | 5 | 6.562 | 6.964 | 19/09/2007 | 0 | 0 | sem agendamento | estoque, fila velha |
| 02.05.02.006-2 | articulações | 37 | **9.952** | 7.503 | 7.282 | 525 | 384 | 24/09/2010 | 4.021 | 5.566 | 1,8 | — |
| 02.05.02.006-2 | partes moles | 1 | **3.117** | 1.872 | 3.115 | 652 | 502 | 28/10/2010 | 1.168 | 1.422 | 2,2 | fila velha |
| 02.05.02.006-2 | região inguinal | 3 | **606** | 522 | 542 | 383 | 333 | 24/11/2022 | 285 | 735 | 0,8 | — |
| 02.05.02.006-2 | pescoço e região cervical | 4 | **278** | 218 | 276 | 465 | 409 | 29/04/2010 | 109 | 199 | 1,4 | — |
| 02.05.02.006-2 | outras regiões | 16 | **438** | 281 | 418 | 594 | 550 | 05/08/2022 | 142 | 90 | 4,9 | estoque, fila velha |
| 02.06.01.001-0 | eletiva | 3 | **84** | 84 | 84 | 91 | 82 | 23/02/2026 | 84 | 1.269 | 0,1 | — |
| 02.06.01.001-0 | emergência | 4 | **55** | 52 | 54 | 339 | 292 | 24/09/2024 | 28 | 181 | 0,3 | — |
| 02.06.01.003-6 | eletiva | 4 | **43** | 43 | 42 | 90 | 82 | 25/02/2026 | 43 | 953 | 0,0 | — |
| 02.06.01.003-6 | emergência | 2 | **36** | 35 | 35 | 327 | 278 | 02/10/2024 | 20 | 137 | 0,3 | — |
| 02.06.01.002-8 | eletiva | 4 | **83** | 83 | 83 | 80 | 54 | 25/02/2026 | 83 | 2.872 | 0,0 | — |
| 02.06.01.002-8 | emergência | 3 | **81** | 74 | 79 | 384 | 397 | 23/09/2024 | 32 | 285 | 0,3 | — |
| 02.06.02.002-3 | eletiva | 23 | **119** | 119 | 91 | 88 | 62 | 11/02/2025 | 114 | 2.054 | 0,1 | — |
| 02.06.02.002-3 | emergência | 18 | **100** | 100 | 74 | 341 | 316 | 28/10/2024 | 48 | 181 | 0,6 | — |
| 02.06.02.001-5 | eletiva | 6 | **10** | 10 | 10 | 19 | 7 | 25/08/2026 | 10 | 838 | 0,0 | — |
| 02.06.02.001-5 | emergência | 6 | **37** | 35 | 36 | 378 | 410 | 20/10/2024 | 13 | 64 | 0,6 | — |
| 02.06.02.001-5 | angiotomografia | 3 | **24** | 24 | 22 | 183 | 160 | 07/05/2025 | 20 | 60 | 0,4 | — |
| 02.06.03.002-9 | eletiva | 12 | **99** | 98 | 96 | 222 | 90 | 17/10/2024 | 65 | 1.266 | 0,1 | — |
| 02.06.03.002-9 | emergência | 7 | **56** | 54 | 53 | 384 | 367 | 30/09/2024 | 22 | 53 | 1,1 | — |
| 02.06.03.002-9 | angiotomografia | 2 | **87** | 87 | 57 | 218 | 187 | 07/05/2025 | 58 | 150 | 0,6 | — |

- **Ecocardiografia:** "outros nomes" são quatro filas antigas (2007 a 2013) sem pedido em 2026.
  A eco é fila genérica (pedida para muitos fins: I10, I50, I25 na adulto; R01, Q21 na infantil).
- **US de articulação, por nome:** articulações = ombro, punho, joelho, tornozelo, cotovelo,
  coxo-femural, quadril, mão, pé, dedo, calcâneo, tendão (37 nomes); partes moles = "ECOGRAFIA␣␣DE
  PARTES MOLES"; região inguinal = as três filas de região inguinal; pescoço e região cervical =
  US do pescoço, cervical, doppler de região cervical e o antigo de 2010; outras regiões = braço,
  antebraço, perna, coxa, axila, coluna e região lombar (infantil), glútea, bacia, pelve,
  glândulas submandibulares, estrutura superficial e o doppler de aorta antigo (16 nomes). Os
  nomes de cada recorte estão no JSON (`recortes_por_nome`).
- **TC de coluna, segmentos e articulações:** a eletiva tem espera curta (18 a 222 dias) e muita
  oferta; a emergência espera 327 a 384 dias e vem da Região Sudoeste.

Região de Saúde:

| código | exame | Central | Centro-Sul | Leste | Norte | Oeste | Sudoeste | Sul | URD | Contrat./Cred. | outros | **sem região** | total | URD + contrat. (% calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | Ecocardiografia transtorácica | 1.022 | 1.180 | 867 | 1.646 | 1.486 | 2.581 | 954 | 2.368 | 2.488 | 0 | **129** | 14.721 | 33,0% |
| 02.05.02.006-2 | US de articulação | 62 | 2.823 | 2.707 | 519 | 1.562 | 4.261 | 2.290 | 1 | 6 | 0 | **160** | 14.391 | 0,0% |
| 02.05.02.011-9 | US de próstata transretal | 0 | 0 | 0 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | **0** | 22 | 0,0% |
| 02.05.02.013-5 | US de tórax (extracardíaca) | 0 | 15 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | 17 | 0,0% |
| 02.05.01.005-9 | Doppler de fluxo obstétrico | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 0 | **0** | 15 | 0,0% |
| 02.06.01.001-0 | TC de coluna cervical | 2 | 4 | 14 | 3 | 6 | 56 | 4 | 32 | 17 | 0 | **1** | 139 | 35,3% |
| 02.06.01.003-6 | TC de coluna torácica | 0 | 1 | 6 | 2 | 3 | 37 | 1 | 24 | 5 | 0 | **0** | 79 | 36,7% |
| 02.06.01.002-8 | TC de coluna lombo-sacra | 1 | 4 | 17 | 3 | 7 | 87 | 5 | 33 | 5 | 0 | **2** | 164 | 23,2% |
| 02.06.02.002-3 | TC de segmentos apendiculares | 3 | 6 | 12 | 6 | 6 | 116 | 12 | 49 | 9 | 0 | **0** | 219 | 26,5% |
| 02.06.02.001-5 | TC de articulações de membro superior | 4 | 0 | 1 | 1 | 1 | 44 | 2 | 15 | 2 | 0 | **1** | 71 | 23,9% |
| 02.06.03.002-9 | TC de articulações de membro inferior | 7 | 4 | 16 | 13 | 9 | 122 | 22 | 34 | 14 | 0 | **1** | 242 | 19,8% |

### 1.3 Ressonância (02.07), por código

Na tabela de destaque a pedido; em 16/10 ficou fora (a rede já cuida). Decisão: **a decidir**,
menos os nomes-resíduo.

| código | exame | fila | fila viva | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | pedidos de 2026 na fila | agendadas 12 m | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.07.01.001-3 | Angiorressonância cerebral | **143** | 143 | 112 | 468 | 23 | 24 | 66 | 21/08/2026 | 143 | 2.684 | 0,1 | — |
| 02.07.01.002-1 | RM de ATM | **135** | 135 | 134 | 307 | 24 | 24 | 76 | 11/08/2026 | 135 | 1.706 | 0,1 | — |
| 02.07.01.003-0 | RM de coluna cervical / pescoço | **763** | 760 | 751 | 1.243 | 30 | 24 | 1.715 | 14/02/2022 | 759 | 9.594 | 0,1 | — |
| 02.07.01.004-8 | RM de coluna lombo-sacra | **1.553** | 1.549 | 1.551 | 2.270 | 26 | 21 | 1.720 | 09/02/2022 | 1.549 | 20.121 | 0,1 | — |
| 02.07.01.005-6 | RM de coluna torácica | **286** | 286 | 285 | 616 | 23 | 23 | 66 | 21/08/2026 | 286 | 4.448 | 0,1 | — |
| 02.07.01.006-4 | RM de crânio | **1.345** | 1.343 | 1.325 | 4.391 | 27 | 24 | 1.378 | 17/01/2023 | 1.343 | 17.848 | 0,1 | — |
| 02.07.01.007-2 | RM de sela túrcica | **123** | 123 | 123 | 374 | 25 | 21 | 63 | 24/08/2026 | 123 | 1.592 | 0,1 | — |
| 02.07.02.001-9 | RM de coração / aorta | **246** | 246 | 245 | 736 | 71 | 69 | 146 | 02/06/2026 | 246 | 1.899 | 0,1 | — |
| 02.07.02.002-7 | RM de membro superior | **1.254** | 1.250 | 950 | 1.426 | 27 | 21 | 1.720 | 09/02/2022 | 1.249 | 12.328 | 0,1 | — |
| 02.07.02.003-5 | RM de tórax | **73** | 73 | 73 | 439 | 24 | 20 | 66 | 21/08/2026 | 73 | 1.103 | 0,1 | — |
| 02.07.02.006-0 | RM de mama | **9** | 9 | 9 | 26 | 2 | 3 | 3 | 23/10/2026 | 9 | 1.917 | 0,0 | — |
| 02.07.03.001-4 | RM de abdômen superior | **540** | 540 | 538 | 1.114 | 25 | 27 | 75 | 12/08/2026 | 540 | 10.787 | 0,1 | — |
| 02.07.03.002-2 | RM de bacia / pelve | **1.439** | 1.439 | 1.437 | 2.089 | 27 | 26 | 91 | 27/07/2026 | 1.439 | 19.779 | 0,1 | — |
| 02.07.03.003-0 | RM de membro inferior | **1.684** | 1.682 | 1.303 | 1.816 | 24 | 21 | 1.754 | 06/01/2022 | 1.680 | 17.797 | 0,1 | — |
| 02.07.03.004-9 | RM de vias biliares | **112** | 112 | 111 | 462 | 22 | 18 | 67 | 20/08/2026 | 112 | 3.271 | 0,0 | — |

Soma dos quinze códigos (calculado): 9.705 na fila e 126.874 agendadas em 12 meses. A espera média
vai de 2 a 71 dias; a fila inteira gira em semanas.

Região de Saúde:

| código | exame | Central | Centro-Sul | Leste | Norte | Oeste | Sudoeste | Sul | URD | Contrat./Cred. | outros | **sem região** | total | URD + contrat. (% calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.07.01.001-3 | Angiorressonância cerebral | 7 | 2 | 14 | 20 | 11 | 13 | 8 | 59 | 9 | 0 | **0** | 143 | 47,6% |
| 02.07.01.002-1 | RM de ATM | 10 | 5 | 2 | 7 | 6 | 19 | 18 | 52 | 15 | 0 | **1** | 135 | 49,6% |
| 02.07.01.003-0 | RM de coluna cervical / pescoço | 27 | 65 | 94 | 66 | 80 | 130 | 73 | 149 | 66 | 0 | **13** | 763 | 28,2% |
| 02.07.01.004-8 | RM de coluna lombo-sacra | 51 | 150 | 229 | 199 | 233 | 314 | 144 | 145 | 53 | 0 | **35** | 1.553 | 12,7% |
| 02.07.01.005-6 | RM de coluna torácica | 5 | 17 | 37 | 27 | 25 | 56 | 26 | 67 | 22 | 0 | **4** | 286 | 31,1% |
| 02.07.01.006-4 | RM de crânio | 59 | 85 | 95 | 114 | 163 | 248 | 116 | 342 | 104 | 0 | **19** | 1.345 | 33,2% |
| 02.07.01.007-2 | RM de sela túrcica | 5 | 7 | 7 | 8 | 5 | 22 | 5 | 52 | 12 | 0 | **0** | 123 | 52,0% |
| 02.07.02.001-9 | RM de coração / aorta | 19 | 16 | 7 | 18 | 24 | 35 | 11 | 51 | 64 | 0 | **1** | 246 | 46,7% |
| 02.07.02.002-7 | RM de membro superior | 54 | 119 | 89 | 134 | 153 | 229 | 216 | 218 | 24 | 0 | **18** | 1.254 | 19,3% |
| 02.07.02.003-5 | RM de tórax | 1 | 4 | 11 | 7 | 15 | 8 | 7 | 13 | 5 | 0 | **2** | 73 | 24,7% |
| 02.07.02.006-0 | RM de mama | 0 | 0 | 0 | 0 | 1 | 3 | 2 | 3 | 0 | 0 | **0** | 9 | 33,3% |
| 02.07.03.001-4 | RM de abdômen superior | 32 | 17 | 13 | 40 | 45 | 112 | 45 | 168 | 62 | 0 | **6** | 540 | 42,6% |
| 02.07.03.002-2 | RM de bacia / pelve | 86 | 90 | 106 | 136 | 193 | 325 | 150 | 227 | 108 | 0 | **18** | 1.439 | 23,3% |
| 02.07.03.003-0 | RM de membro inferior | 83 | 192 | 176 | 227 | 221 | 342 | 230 | 152 | 28 | 1 | **32** | 1.684 | 10,7% |
| 02.07.03.004-9 | RM de vias biliares | 22 | 0 | 4 | 9 | 13 | 10 | 13 | 36 | 4 | 1 | **0** | 112 | 35,7% |

### 1.4 Os onze códigos do plano 4 — só a sobreposição

Decisão: **fica fora** (o enquadramento é o objeto do plano 4, ISHP, R$ 11,5 mi; as outras filas
do mesmo código ficaram fora por risco de sobreposição, usuário, 16/10/2026). Por código e, dentro
dele, o enquadramento do plano 4 (os dezesseis nomes gravados em 09/10/2026 no redacao_06) e o que
fica fora dele.

| código | exame | fila | fila viva | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | pedidos de 2026 na fila | agendadas 12 m | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.009-7 | US mamária bilateral | **13.184** | 8.736 | 13.163 | 7.743 | 617 | 500 | 6.123 | 21/01/2010 | 4.987 | 10.379 | 1,3 | fila velha |
| 02.05.02.018-6 | US transvaginal | **9.649** | 6.026 | 9.648 | 8.951 | 640 | 489 | 5.887 | 14/09/2010 | 3.872 | 17.923 | 0,5 | fila velha |
| 02.05.01.004-0 | US doppler colorido de vasos | **16.854** | 12.154 | 15.438 | 5.921 | 479 | 330 | 1.867 | 15/09/2021 | 8.112 | 12.574 | 1,3 | — |
| 02.05.02.004-6 | US de abdômen total | **13.861** | 10.076 | 13.593 | 13.283 | 554 | 373 | 6.118 | 26/01/2010 | 6.177 | 10.647 | 1,3 | — |
| 02.05.02.005-4 | US de aparelho urinário | **4.148** | 2.771 | 4.132 | 4.103 | 626 | 392 | 5.788 | 22/12/2010 | 1.788 | 4.902 | 0,8 | fila velha |
| 02.05.02.012-7 | US de tireoide | **3.857** | 3.099 | 3.824 | 3.327 | 480 | 368 | 7.001 | 27/08/2007 | 1.717 | 3.886 | 1,0 | — |
| 02.05.02.010-0 | US de próstata via abdominal | **3.197** | 2.366 | 3.194 | 2.716 | 581 | 445 | 5.998 | 26/05/2010 | 1.181 | 4.132 | 0,8 | — |
| 02.05.02.003-8 | US de abdômen superior | **2.241** | 1.253 | 2.237 | 1.002 | 678 | 608 | 5.879 | 22/09/2010 | 843 | 2.525 | 0,9 | fila velha |
| 02.06.03.001-0 | TC de abdômen superior | **6.217** | 6.158 | 5.973 | 7.983 | 174 | 140 | 3.611 | 06/12/2016 | 5.340 | 17.776 | 0,3 | — |
| 02.06.03.003-7 | TC de pelve / bacia | **5.030** | 4.976 | 4.885 | 5.557 | 177 | 145 | 3.611 | 06/12/2016 | 4.324 | 14.950 | 0,3 | — |
| 02.06.02.003-1 | TC de tórax | **6.138** | 6.073 | 5.926 | 6.876 | 212 | 159 | 3.611 | 06/12/2016 | 4.618 | 29.933 | 0,2 | — |

| código | recorte (nomes de fila) | nomes | fila | fila viva | pessoas | espera média | mediana | pedido mais antigo | pedidos de 2026 | agendadas 12 m (pelos nomes) | anos de estoque (calc.) | alarmes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.009-7 | enquadramento do plano 4 | 1 | **13.182** | 8.736 | 13.161 | 617 | 500 | 21/01/2010 | 4.987 | 10.379 | 1,3 | fila velha |
| 02.05.02.009-7 | outros fora do enquadramento | 2 | **2** | 0 | 2 | 1.518 | 1.518 | 30/08/2022 | 0 | 0 | sem agendamento | estoque, fila velha |
| 02.05.02.018-6 | enquadramento do plano 4 | 1 | **9.648** | 6.026 | 9.647 | 640 | 489 | 14/09/2010 | 3.872 | 17.923 | 0,5 | fila velha |
| 02.05.02.018-6 | outros fora do enquadramento | 1 | **1** | 0 | 1 | 3.962 | 3.962 | 21/12/2015 | 0 | 0 | sem agendamento | estoque, fila velha |
| 02.05.01.004-0 | enquadramento do plano 4 | 2 | **14.219** | 10.234 | 14.068 | 480 | 322 | 17/10/2022 | 6.933 | 11.676 | 1,2 | — |
| 02.05.01.004-0 | outros fora do enquadramento | 32 | **2.635** | 1.920 | 2.583 | 472 | 361 | 15/09/2021 | 1.179 | 898 | 2,9 | — |
| 02.05.02.004-6 | enquadramento do plano 4 | 3 | **13.400** | 9.783 | 13.141 | 554 | 374 | 26/01/2010 | 5.950 | 9.596 | 1,4 | — |
| 02.05.02.004-6 | outros fora do enquadramento | 2 | **460** | 292 | 460 | 583 | 339 | 22/02/2021 | 226 | 1.051 | 0,4 | fila velha |
| 02.05.02.004-6 | emergência | 1 | **1** | 1 | 1 | 2 | 2 | 25/10/2026 | 1 | 0 | sem agendamento | estoque |
| 02.05.02.005-4 | enquadramento do plano 4 | 1 | **3.773** | 2.493 | 3.771 | 639 | 406 | 22/12/2010 | 1.587 | 4.106 | 0,9 | fila velha |
| 02.05.02.005-4 | outros fora do enquadramento | 3 | **374** | 277 | 373 | 498 | 268 | 21/01/2021 | 200 | 796 | 0,5 | — |
| 02.05.02.005-4 | emergência | 1 | **1** | 1 | 1 | 0 | 0 | 26/10/2026 | 1 | 0 | sem agendamento | estoque |
| 02.05.02.012-7 | enquadramento do plano 4 | 1 | **2.990** | 2.363 | 2.990 | 489 | 369 | 07/01/2021 | 1.321 | 3.365 | 0,9 | — |
| 02.05.02.012-7 | outros fora do enquadramento | 3 | **866** | 736 | 866 | 442 | 360 | 02/06/2021 | 396 | 521 | 1,7 | — |
| 02.05.02.012-7 | emergência | 1 | **1** | 0 | 1 | 7.001 | 7.001 | 27/08/2007 | 0 | 0 | sem agendamento | estoque, fila velha |
| 02.05.02.010-0 | enquadramento do plano 4 | 1 | **3.195** | 2.366 | 3.192 | 580 | 445 | 26/05/2010 | 1.181 | 4.132 | 0,8 | — |
| 02.05.02.010-0 | outros fora do enquadramento | 1 | **2** | 0 | 2 | 1.522 | 1.522 | 23/08/2022 | 0 | 0 | sem agendamento | estoque, fila velha |
| 02.05.02.003-8 | enquadramento do plano 4 | 1 | **2.225** | 1.242 | 2.223 | 679 | 613 | 22/09/2010 | 835 | 2.402 | 0,9 | fila velha |
| 02.05.02.003-8 | outros fora do enquadramento | 2 | **16** | 11 | 16 | 581 | 380 | 25/03/2021 | 8 | 123 | 0,1 | fila velha |
| 02.06.03.001-0 | enquadramento do plano 4 | 1 | **4.131** | 4.116 | 4.127 | 122 | 119 | 05/07/2024 | 4.112 | 8.095 | 0,5 | — |
| 02.06.03.001-0 | outros fora do enquadramento | 4 | **64** | 64 | 64 | 23 | 4 | 15/01/2026 | 64 | 5.614 | 0,0 | — |
| 02.06.03.001-0 | emergência | 4 | **1.166** | 1.122 | 1.064 | 359 | 355 | 06/12/2016 | 513 | 2.246 | 0,5 | — |
| 02.06.03.001-0 | angiotomografia | 7 | **856** | 856 | 797 | 181 | 152 | 07/05/2025 | 651 | 1.510 | 0,6 | — |
| 02.06.03.003-7 | enquadramento do plano 4 | 1 | **3.622** | 3.612 | 3.620 | 123 | 123 | 05/07/2024 | 3.610 | 6.979 | 0,5 | — |
| 02.06.03.003-7 | outros fora do enquadramento | 4 | **63** | 63 | 63 | 30 | 3 | 25/01/2025 | 62 | 5.561 | 0,0 | — |
| 02.06.03.003-7 | emergência | 4 | **1.090** | 1.046 | 991 | 356 | 342 | 06/12/2016 | 482 | 1.995 | 0,5 | — |
| 02.06.03.003-7 | angiotomografia | 2 | **255** | 255 | 255 | 210 | 174 | 17/07/2025 | 170 | 327 | 0,8 | — |
| 02.06.02.003-1 | enquadramento do plano 4 | 3 | **4.164** | 4.151 | 4.133 | 179 | 140 | 11/12/2023 | 3.459 | 24.391 | 0,2 | — |
| 02.06.02.003-1 | outros fora do enquadramento | 3 | **5** | 5 | 5 | 185 | 4 | 25/01/2025 | 4 | 237 | 0,0 | — |
| 02.06.02.003-1 | emergência | 4 | **1.270** | 1.218 | 1.202 | 349 | 329 | 06/12/2016 | 590 | 2.966 | 0,4 | — |
| 02.06.02.003-1 | angiotomografia | 6 | **699** | 699 | 683 | 165 | 136 | 31/01/2025 | 565 | 2.263 | 0,3 | — |

- **Angiotomografia de coronárias:** o SISREG a registra sob 02.06.02.003-1 (TC de tórax). A adulto
  ("ANGIOTOMOGRAFIA[NBSP]␣DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO", com o espaço não separável) está no
  enquadramento do plano 4: 1.530 na fila, espera média de 286 dias, 137 agendadas em 12 meses (11,2
  anos de estoque). A infantil (11 na fila, nenhuma agendada) fica fora do enquadramento, no recorte
  angiotomografia.
- **Fila nova:** "ANGIOTOMOGRAFIA" (sem complemento), 02.06.02.003-1, aberta em 19/10/2026, 3 na fila.
  Não entra em soma nenhuma.
- **Emergência e angiotomografia fora do enquadramento**, nos três códigos de TC do plano 4: tórax
  1.270 + 699, abdômen superior 1.166 + 856, pelve 1.090 + 255.

Região de Saúde:

| código | exame | Central | Centro-Sul | Leste | Norte | Oeste | Sudoeste | Sul | URD | Contrat./Cred. | outros | **sem região** | total | URD + contrat. (% calc.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.009-7 | US mamária bilateral | 1.380 | 518 | 1.974 | 93 | 1.613 | 5.224 | 2.212 | 4 | 3 | 0 | **163** | 13.184 | 0,1% |
| 02.05.02.018-6 | US transvaginal | 98 | 421 | 2.934 | 131 | 162 | 4.380 | 1.432 | 1 | 1 | 0 | **89** | 9.649 | 0,0% |
| 02.05.01.004-0 | US doppler colorido de vasos | 1.011 | 710 | 340 | 4.344 | 563 | 4.000 | 4.666 | 517 | 471 | 0 | **232** | 16.854 | 5,9% |
| 02.05.02.004-6 | US de abdômen total | 722 | 2.283 | 2.018 | 103 | 470 | 4.141 | 3.940 | 7 | 4 | 1 | **172** | 13.861 | 0,1% |
| 02.05.02.005-4 | US de aparelho urinário | 30 | 958 | 652 | 24 | 88 | 1.447 | 894 | 2 | 4 | 0 | **49** | 4.148 | 0,1% |
| 02.05.02.012-7 | US de tireoide | 19 | 722 | 756 | 136 | 125 | 1.096 | 974 | 1 | 4 | 0 | **24** | 3.857 | 0,1% |
| 02.05.02.010-0 | US de próstata via abdominal | 21 | 609 | 701 | 46 | 45 | 580 | 1.177 | 2 | 1 | 0 | **15** | 3.197 | 0,1% |
| 02.05.02.003-8 | US de abdômen superior | 19 | 398 | 128 | 36 | 76 | 1.554 | 24 | 3 | 1 | 0 | **2** | 2.241 | 0,2% |
| 02.06.03.001-0 | TC de abdômen superior | 218 | 101 | 200 | 334 | 326 | 1.995 | 318 | 1.859 | 806 | 0 | **60** | 6.217 | 42,9% |
| 02.06.03.003-7 | TC de pelve / bacia | 158 | 68 | 128 | 280 | 177 | 1.760 | 265 | 1.529 | 629 | 0 | **36** | 5.030 | 42,9% |
| 02.06.02.003-1 | TC de tórax | 243 | 162 | 282 | 347 | 499 | 1.951 | 282 | 1.507 | 827 | 0 | **38** | 6.138 | 38,0% |

## 2. Mamografia 02.04.03.018-8 — rastreamento e diagnóstico

| nome de fila | fila | fila viva | pessoas | devolvidas | espera média | mediana | agendadas 12 m | 35 anos ou mais | menos de 35 | 50 a 69 anos |
|---|---|---|---|---|---|---|---|---|---|---|
| MAMOGRAFIA BILATERAL PARA SCREENING (ROTINA) | **6.725** | 6.641 | 6.724 | 2.135 | 66 | 30 | 50.608 | 6.691 | 34 | 4.470 |
| MAMOGRAFIA BILATERAL DIAGNOSTICA | **192** | 191 | 192 | 544 | 47 | 21 | 5.041 | 183 | 9 | 101 |

**CID solicitado, somado por grupo** (grupo **calculado**; os CID um a um estão na aba 3):

| grupo de CID | screening (rotina) | viva | diagnóstica | viva |
|---|---|---|---|---|
| rastreamento de neoplasia (Z12) | 4.984 | 4.929 | 67 | 66 |
| exame geral ou de rotina (Z00, Z01, Z10, Z13) | 721 | 705 | 5 | 5 |
| queixa ou achado mamário (N60–N64, R92, D24, D48) | 486 | 474 | 101 | 101 |
| câncer de mama (C50, D05) | 214 | 214 | 7 | 7 |
| climatério (N95) | 201 | 201 | 1 | 1 |
| outros | 76 | 75 | 8 | 8 |
| história de câncer ou seguimento (Z80, Z85, Z08) | 43 | 43 | 3 | 3 |
| **total** | **6.725** | 6.641 | **192** | 191 |

- Os CID mais pedidos na fila "screening": Z123 (rastreamento de neoplasia de mama) 3.626, Z12 1.348,
  N63 (nódulo mamário) 256, Z014 (exame ginecológico) 245, Z00 194, C50 150, N95 98, N951 94, N64 93,
  Z01 78, C509 61, Z10 60, N60 53. Na "diagnóstica": N63 68, Z123 41, Z12 26, N64 9, R92 9, C50 7.
- **Rastreamento e diagnóstico se misturam nos dois nomes:** 486 + 214 + 43 = 743 pedidos da fila
  "screening" (11%) têm CID de queixa, câncer ou seguimento; 67 da "diagnóstica" (35%) têm CID de
  rastreamento. O nome da fila não separa a finalidade; o CID separa só em parte (Z00 e Z01 não dizem).
- Em 15/10 eram 187 na "diagnóstica" (81 com N63) e 6.274 na "screening" (263 com N63): a fila
  "screening" subiu 451 e a espera média passou de 48 para 66 dias.
- A Região Leste (1.790) e a Centro-Sul (1.487) pedem quase metade da mamografia (tabela da seção 1.1).


## 3. Varredura das filas

### 3.1 Como se varreu

- **Pelo código.** `codigo_sigtap_solicitacao` é numérico, sem o zero à esquerda e sem pontos
  (02.05.02.009-7 = 205020097). O curinga `{"204*","205*","206*","207*","208*","210*"}` achou **684 filas**
  (pares nome × código) com alguém na fila, em **134 códigos**; em 15/10 eram 746 em 134. Pega também os dois
  códigos malformados de oito dígitos (20406014 e 20406015, radiografias de joelho e de pé). Os
  agendamentos, pelo `codigo_sigtap_agendamento` com os mesmos curingas.
- **Pelo nome.** Os 1.570 nomes de fila da base, normalizados, pelos termos de imagem da coleta de 15/10
  (RESSON, RM, TOMOGRAF, TC, ANGIOTOMO, MAMOGRAF, DENSITOM, RADIOGRAF, RX, RAIO, CINTILOG, PET,
  ECOGRAF, ULTRA, USG, US, DOPPLER, ECOCARD, ELASTOGRAF, ARTERIOGRAF, FLEBOGRAF, UROGRAF, ANGIOGRAF,
  CONTRAST, GUIAD, IMAGEM, OCT, BIOMETRIA) e pelos grupos de imagem do painel
  (`nome_grupo_procedimento_solicitacao`). Fora dos subgrupos só responderam as filas da seção 3.4.
- **Cada fila foi estudada** (fila, viva, pessoas, devolvidas, espera média, mediana e máxima,
  pedido mais antigo, pedidos de 2026, idade mediana, 1ª solicitação na base, agendadas em 12
  meses e no ano, os dez CID principais nos códigos de destaque e três nos demais) e recebeu decisão
  pela regra `decidir()` do `montar_20261026.py`, escrita a partir das decisões do usuário de 15 a
  20/10/2026. A decisão de pôr ou tirar é do usuário.
- **Grafia:** o JSON guarda o nome exato. Seis nomes têm o espaço não separável (U+00A0): as
  angiotomografias de coronárias adulto e infantil, de aorta torácica e abdominal, de abdome superior
  e de pescoço infantil; muitos têm dois espaços seguidos (␣␣ nas tabelas).

### 3.2 A decisão de cada fila

| categoria | decisão | filas | códigos | fila (soma das filas, calc.) | fila viva (calc.) | motivo |
|---|---|---|---|---|---|---|
| carteira | **entra** | 40 | 12 | 14.345 | 13.559 | carteira do pré-plano (usuário, 16, 19 e 20/10/2026); mamografia e densitometria de reserva |
| carteira | **a decidir** | 34 | 5 | 1.750 | 1.724 | emergência, angiotomografia, cone beam e mamografia diagnóstica dentro dos códigos da carteira |
| saíram e podem voltar | **a decidir** | 153 | 11 | 30.032 | 26.031 | reabertura pedida em 26/10/2026 |
| ressonância | **a decidir** | 129 | 15 | 9.703 | 9.690 | na tabela de destaque; em 16/10, fora (a rede já cuida) |
| mesmo código do plano 4, fora do enquadramento | **fica fora** | 56 | 8 | 9.568 | 8.547 | risco de sobreposição com o plano 4 (usuário, 16/10/2026) |
| plano 4 — os dezesseis nomes do enquadramento | **fica fora** | 16 | 11 | 74.549 | 55.122 | objeto do plano 4 |
| cintilografia | **fica fora** | 23 | 22 | 5.610 | 5.610 | complexa de executar: CNEN, vigilância, radiofármaco do IPEN (usuário, 16/10/2026) |
| fora do rol da Portaria 4.282 | **fica fora** | 171 | 61 | 5.899 | 5.886 | sem incremento, só a Tabela: radiografias, PET-CT, eco de estresse e transesofágica, paquimetria, angiografias (estudo, 15/10/2026) |
| resíduo — nenhum pedido nem agendamento em 2026 | **fica fora** | 62 | 24 | 326 | 47 | nomes antigos do SISREG |
| **total** | | 684 | | 151.782 | 126.216 | |

A soma das filas (151.782) passa em 2 do motor (151.780 na fila, 126.216 na viva,
108.860 pessoas): dois pedidos aparecem em dois nomes de fila. Pessoas não se somam entre
categorias.

### 3.3 Filas novas desde 15/10/2026

Vinte e oito pares nome × código que não tinham ninguém na fila em 15/10, todos com 1 a 3 pedidos.
**Nenhuma entra em soma.** As que pesam para a decisão:
- "ANGIOTOMOGRAFIA" (02.06.02.003-1), aberta em 19/10/2026: 3 na fila (I26, I25). Fica fora (mesmo
  código do plano 4).
- "TC␣␣DE SELA TURCICA ADULTO C/CONTRASTE S/SEDACAO␣␣EMERG." (02.06.01.006-0, carteira), 1 pedido de
  15/10/2026: **a decidir** (emergência).
- Três nomes de TC de coluna ("009." e "011. TC COLUNA DORSAL INFANTIL", 02.06.01.003-6; "022. TC COLUNA
  LOMBO-SACRA ADULTO S/CONTRASTE C/SEDACAO", 02.06.01.002-8), com 1 ou 2 pedidos, e seis de TC de
  segmentos apendiculares (braço, antebraço, perna, coxa), com 2 ou 3 pedidos, todos de 20/10/2026 em
  diante: **a decidir** (podem voltar).
- "ECOGRAFIA DE ABDOMEN TOTAL ADULTO EMERGENCIA" e "ECOGRAFIA DO APARELHO URINARIO (RINS, BEXIGA)
  INFANTIL EMERG", 1 pedido cada, de 25 e 26/10/2026: códigos do plano 4.

Saíram da fila desde 15/10 90 nomes dos subgrupos de imagem, com 250 pedidos ao todo, nenhum com mais de
24 (os maiores: RM de crânio infantil com contraste 24, RM de bacia infantil 22, RM de coluna lombo-sacra
infantil 14). A lista sai da comparação de `anterior_20261015_resumo.json` com `coleta_20261026.json`;
a diferença por código e recorte está na aba 10.

### 3.4 Fora dos subgrupos de imagem

| código | nome de fila | fila | fila viva | pessoas | devolvidas | espera média | mediana | decisão — nota |
|---|---|---|---|---|---|---|---|---|
| 02.11.06.028-3 | OCT GLAUCOMA | 2.344 | 2.344 | 2.344 | 1 | 224 | 220 | fica fora — exame oftalmológico (02.11.06) |
| 02.11.06.028-3 | OCT | 1.543 | 1.543 | 1.543 | 414 | 332 | 356 | fica fora — exame oftalmológico (02.11.06) |
| 02.01.01.047-0 | PUNCAO ASPIRATIVA TIREOIDE TELEGUIADA | 521 | 521 | 521 | 90 | 89 | 80 | fica fora — punção guiada por imagem (02.01), não é exame de imagem |
| 02.11.06.001-1 | BIOMETRIA ULTRASSONICA | 484 | 484 | 484 | 341 | 63 | 67 | fica fora — exame oftalmológico (02.11.06) |
| 02.01.01.054-2 | PUNCAO DE MAMA POR AGULHA GROSSA (CORE BIOPSIA) GUIADA POR ULTRASSONOGRAFIA | 221 | 221 | 221 | 185 | 61 | 48 | fica fora — biópsia guiada por imagem (02.01) |
| 02.01.01.054-2 | PUNCAO DE MAMA POR AGULHA GROSSA (CORE BIOPSIA) GUIADA POR MAMOGRAFIA | 74 | 74 | 74 | 64 | 74 | 70 | fica fora — biópsia guiada por imagem (02.01) |
| 02.01.01.058-5 | PUNCAO ASPIRATIVA DE MAMAS POR AGULHA FINA (PAAF) GUIADA POR ULTRASSONOGRAFIA | 5 | 5 | 5 | 131 | 3 | 3 | fica fora — punção guiada por imagem (02.01) |
| 02.01.01.058-5 | PUNCAO ASPIRATIVA DE MAMAS POR AGULHA FINA (PAAF) | 3 | 0 | 3 | 70 | 1.297 | 1.299 | fica fora — punção guiada por imagem (02.01) |
| 02.11.05.008-3 | COLUNA TOTAL | 1 | 0 | 1 | 1 | 2.093 | 2.093 | fica fora — nome de radiografia com o código da eletroneuromiografia (02.11.05); pedido de 2020 |

As agendadas em 12 meses destas filas não foram medidas (a medida saiu zerada por erro de recorte;
lacuna). As duas filas de eletroneuromiografia que dividem o código 02.11.05.008-3 com "COLUNA
TOTAL" não são imagem e não entram.

**Medida complementar** (mesma recarga, consulta de 17:12:50 a 17:13:08): as filas de 15/10 que a
busca por nome desta coleta não apanhou, por não terem termo de imagem no nome.

| código | nome de fila | fila | fila viva | pessoas | devolvidas | espera média | mediana | agendadas 12 m | decisão — nota |
|---|---|---|---|---|---|---|---|---|---|
| (sem código) | ORGAOS INTERNOS DO TORAX I | 1 | 1 | 1 | 6 | 133 | 133 | — | fica fora — sem código SIGTAP; grupo radiodiagnóstico do painel |
| (sem código) | ORGAOS INTERNOS DO TORAX II | 1 | 1 | 1 | 2 | 94 | 94 | — | fica fora — sem código SIGTAP; grupo radiodiagnóstico do painel |
| 02.11.02.002-8 | CATETERISMO CARDIACO EM PEDIATRIA | 2 | 2 | 2 | 12 | 6 | 6 | 85 | fica fora — cateterismo cardíaco, hemodinâmica (02.11.02) |
| 02.11.02.001-0 | CATETERISMO | 11 | 11 | 11 | 878 | 3 | 3 | 7.543 | fica fora — cateterismo cardíaco, hemodinâmica (02.11.02) |

## 4. Comparação com 15/10/2026

Fila e espera média por código, 15/10 (recarga 19:32:31) e 26/10 (recarga 16:32:44). A espera média
de 15/10 por código é a das filas do código ponderada pela fila (**calculado**, exato: cada pedido
tem um nome de fila só); a de 26/10 sai do motor. Δ **calculado**.

| código | exame | papel | fila 15/10 | **fila 26/10** | Δ | espera média 15/10 | **26/10** | Δ espera |
|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | carteira | 6.461 | **6.917** | +456 | 49 | **66** | +16 |
| 02.04.06.002-8 | Densitometria óssea | carteira | 2.196 | **2.188** | −8 | 44 | **46** | +2 |
| 02.05.02.016-0 | US pélvica (ginecológica) | carteira | 1.005 | **1.025** | +20 | 607 | **606** | −1 |
| 02.05.02.007-0 | US de bolsa escrotal | carteira | 995 | **967** | −28 | 588 | **571** | −17 |
| 02.05.02.008-9 | US de globo ocular / órbita | carteira | 1.272 | **1.308** | +36 | 264 | **267** | +4 |
| 02.05.02.017-8 | US transfontanela | carteira | 283 | **291** | +8 | 290 | **292** | +1 |
| 02.05.02.014-3 | US obstétrica | carteira | 464 | **487** | +23 | 144 | **145** | +1 |
| 02.05.02.015-1 | US obstétrica com doppler | carteira | 205 | **169** | −36 | 177 | **196** | +20 |
| 02.06.01.005-2 | TC de pescoço | carteira | 755 | **779** | +24 | 139 | **139** | 0 |
| 02.06.01.007-9 | TC de crânio | carteira | 1.467 | **1.453** | −14 | 197 | **206** | +10 |
| 02.06.01.004-4 | TC de face / seios / ATM | carteira | 503 | **470** | −33 | 126 | **138** | +12 |
| 02.06.01.006-0 | TC de sela túrcica | carteira | 45 | **48** | +3 | 169 | **169** | 0 |
| 02.05.01.003-2 | Ecocardiografia transtorácica | pode voltar | 16.298 | **14.721** | −1.577 | 137 | **127** | −10 |
| 02.05.02.006-2 | US de articulação | pode voltar | 14.516 | **14.391** | −125 | 546 | **547** | +2 |
| 02.05.02.011-9 | US de próstata transretal | pode voltar | 20 | **22** | +2 | 121 | **120** | 0 |
| 02.05.02.013-5 | US de tórax (extracardíaca) | pode voltar | 17 | **17** | 0 | 693 | **704** | +11 |
| 02.05.01.005-9 | Doppler de fluxo obstétrico | pode voltar | 14 | **15** | +1 | 98 | **102** | +4 |
| 02.05.02.022-4 | Elastografia hepática | pode voltar | 0 | **0** | 0 | — | **—** | — |
| 02.06.01.001-0 | TC de coluna cervical | pode voltar | 141 | **139** | −2 | 182 | **189** | +8 |
| 02.06.01.003-6 | TC de coluna torácica | pode voltar | 75 | **79** | +4 | 199 | **198** | −1 |
| 02.06.01.002-8 | TC de coluna lombo-sacra | pode voltar | 166 | **164** | −2 | 221 | **230** | +9 |
| 02.06.02.002-3 | TC de segmentos apendiculares | pode voltar | 198 | **219** | +21 | 219 | **203** | −16 |
| 02.06.02.001-5 | TC de articulações de membro superior | pode voltar | 72 | **71** | −1 | 255 | **261** | +6 |
| 02.06.03.002-9 | TC de articulações de membro inferior | pode voltar | 245 | **242** | −3 | 247 | **258** | +11 |
| 02.07.01.001-3 | Angiorressonância cerebral | ressonância | 287 | **143** | −144 | 39 | **23** | −16 |
| 02.07.01.002-1 | RM de ATM | ressonância | 127 | **135** | +8 | 22 | **24** | +1 |
| 02.07.01.003-0 | RM de coluna cervical / pescoço | ressonância | 758 | **763** | +5 | 20 | **30** | +10 |
| 02.07.01.004-8 | RM de coluna lombo-sacra | ressonância | 1.412 | **1.553** | +141 | 19 | **26** | +7 |
| 02.07.01.005-6 | RM de coluna torácica | ressonância | 266 | **286** | +20 | 20 | **23** | +3 |
| 02.07.01.006-4 | RM de crânio | ressonância | 1.418 | **1.345** | −73 | 30 | **27** | −3 |
| 02.07.01.007-2 | RM de sela túrcica | ressonância | 136 | **123** | −13 | 39 | **25** | −14 |
| 02.07.02.001-9 | RM de coração / aorta | ressonância | 258 | **246** | −12 | 63 | **71** | +8 |
| 02.07.02.002-7 | RM de membro superior | ressonância | 1.140 | **1.254** | +114 | 19 | **27** | +8 |
| 02.07.02.003-5 | RM de tórax | ressonância | 80 | **73** | −7 | 21 | **24** | +3 |
| 02.07.02.006-0 | RM de mama | ressonância | 84 | **9** | −75 | 21 | **2** | −19 |
| 02.07.03.001-4 | RM de abdômen superior | ressonância | 752 | **540** | −212 | 25 | **25** | 0 |
| 02.07.03.002-2 | RM de bacia / pelve | ressonância | 1.625 | **1.439** | −186 | 24 | **27** | +2 |
| 02.07.03.003-0 | RM de membro inferior | ressonância | 1.492 | **1.684** | +192 | 19 | **24** | +5 |
| 02.07.03.004-9 | RM de vias biliares | ressonância | 92 | **112** | +20 | 22 | **22** | 0 |
| 02.05.02.009-7 | US mamária bilateral | plano 4 | 13.521 | **13.184** | −337 | 624 | **617** | −7 |
| 02.05.02.018-6 | US transvaginal | plano 4 | 9.843 | **9.649** | −194 | 633 | **640** | +7 |
| 02.05.01.004-0 | US doppler colorido de vasos | plano 4 | 17.240 | **16.854** | −386 | 471 | **479** | +8 |
| 02.05.02.004-6 | US de abdômen total | plano 4 | 13.962 | **13.861** | −101 | 548 | **554** | +6 |
| 02.05.02.005-4 | US de aparelho urinário | plano 4 | 4.210 | **4.148** | −62 | 629 | **626** | −2 |
| 02.05.02.012-7 | US de tireoide | plano 4 | 3.967 | **3.857** | −110 | 469 | **480** | +11 |
| 02.05.02.010-0 | US de próstata via abdominal | plano 4 | 3.311 | **3.197** | −114 | 574 | **581** | +7 |
| 02.05.02.003-8 | US de abdômen superior | plano 4 | 2.296 | **2.241** | −55 | 690 | **678** | −11 |
| 02.06.03.001-0 | TC de abdômen superior | plano 4 | 6.219 | **6.217** | −2 | 171 | **174** | +3 |
| 02.06.03.003-7 | TC de pelve / bacia | plano 4 | 5.059 | **5.030** | −29 | 173 | **177** | +3 |
| 02.06.02.003-1 | TC de tórax | plano 4 | 6.171 | **6.138** | −33 | 206 | **212** | +7 |

**O que mudou** (onze dias; a base ganhou as solicitações de 16 a 26/10):
- **Carteira:** 15.651 → **16.102** pedidos na soma dos doze códigos (+451, calculado). Quase toda a alta é da
  mamografia (+456; espera média de 49 para 66 dias). Caíram a US obstétrica com doppler (−36), a TC de
  face (−33), a US de bolsa escrotal (−28) e a TC de crânio (−14). A espera média subiu na TC de crânio
  (+10 dias), na TC de face (+12) e na US obstétrica com doppler (+20); a US pélvica e a bolsa escrotal
  seguem acima de 570 dias.
- **Podem voltar:** a ecocardiografia caiu 1.577 (adulto −1.273, infantil −287) e a espera média de 137
  para 127 dias; a US de articulação caiu 125 (articulações −171) e segue em 547 dias; as TC de coluna e
  de articulações variaram de −3 a +4, e a de segmentos apendiculares subiu 21.
- **Ressonância:** caíram RM de abdômen superior (−212), bacia/pelve (−186), angiorressonância (−144),
  RM de mama (−75) e de crânio (−73); subiram membro inferior (+192), coluna lombo-sacra (+141) e membro
  superior (+114). A espera média segue entre 2 e 71 dias.
- **Plano 4:** todos os onze códigos caíram (doppler de vasos −386, US mamária −337, transvaginal −194).
- **Por recorte** (aba 10): na TC de crânio a eletiva caiu 68 e a angiotomografia subiu 43; na mamografia
  a "screening" subiu 451 e a "diagnóstica" 5.

## 5. Lacunas

- **Elastografia hepática 02.05.02.022-4:** nenhum pedido nem agendamento na base; não há o que medir.
- **Sexo:** nenhuma ficha da carteira restringe o sexo (todas "ambos" desde 2024). O campo `sexo_usuario`
  existe na tabela de usuários, mas a associação com as solicitações devolve uma linha vazia maior que o
  total; não foi usado.
- **Idade nos códigos fora da carteira:** as fichas do SIGTAP de ecocardiografia, US de próstata
  transretal, de tórax, doppler de fluxo obstétrico, elastografia, TC de articulações e ressonância não
  estão no redacao_07; a idade da ficha não foi conferida (só a idade mediana por fila e por código).
- **Oferta:** as agendadas são pela data do atendimento marcado (até 27/01/2027); o painel não
  diz quantos exames foram feitos nem quando a vaga foi marcada.
- **Agendadas por nome:** nos códigos de destaque há nomes que só existem na tabela de agendamentos
  (aba 12; por exemplo, 68 nomes na RM de membro superior, 24 na TC de segmentos apendiculares, 23 na TC
  de face). Por nome, o estoque pode sair maior que o real; o número por código é a referência.
- **Pessoas entre códigos:** distintas dentro do código ou do recorte; somar códigos conta duas vezes quem
  espera dois exames. Medida no motor só a união da carteira (seção 1.1).
- **Sobreposição com o plano 4:** medida só para a união da carteira (2.708 pessoas também na fila
  do enquadramento do plano 4); é a mesma pessoa em duas filas, não o mesmo exame.
- **Fora dos subgrupos:** agendadas em 12 meses não medidas (seção 3.4).
- **Região por nome de fila:** só por recorte (abas 6 e 2); por código, todos os códigos com fila (aba 5).
- **Entrantes por mês:** não coletados, por não terem sido pedidos; "pedidos de 2026 na fila" é um
  indicador, não a medida de entrantes.
- **Espera máxima:** chega a 7.006 dias (US obstétrica morfológica de 2007) e a 7.048 em radiografias
  antigas; são registros pendentes de 2007 a 2010 que o painel não diz se valem.
- **02.09 (endoscopia):** fora do universo por não ser imagem.

## 6. Arquivos

- `mapa_social_20261026.md` — este resumo.
- `mapa_social_20261026.xlsx` — treze abas, com uma "Leia-me" (aba 0).
- `mapa_social_20261026_bruto/` — `motor_filas_20261026.txt`, `motor_codigos_20261026.txt` e
  `motor_agregados_20261026.txt` (o texto do motor, conferido por hash djb2); `ler_motor_20261026.py`
  (lê o texto e grava `motor_20261026.json`); `montar_20261026.py` (grava `coleta_20261026.json`, no
  formato do método, e a planilha); `motor_complementar_20261026.json` (a medida complementar das
  17:12, seção 3.4); `anterior_20261015_resumo.json` (o subconjunto da coleta de 15/10 usado na
  comparação); `README.md`.
