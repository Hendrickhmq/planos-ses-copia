# Estudo — o panorama de imagem e o que sobra depois dos descartes

**Controle interno.** Estudo de 27/10/2026 para o redacao_07: Emenda de Bancada do DF 71080005,
R$ 1.502.687,00. Segue o pedido de hoje: o panorama do que podemos atender e, depois, os
descartes, primeiro pelo que outros planos atendem ou vão atender, depois pelo que a SES já dá
conta, olhando o rumo da fila.

**As fontes:**
- **o panorama:** a coleta do agente `mapa-social` de 27/10/2026, recarga das 08:33,
  conferência 9/9 (`planos/redacao_07/dados/fontes/mapa_social_20261027_panorama.md`, na sua
  pasta). Ela tem as filas de imagem com 10 ou mais pedidos e o **rumo de cada código**:
  - os pedidos novos por mês;
  - a oferta pelo mês em que o agendamento acontece;
  - os realizados e as faltas.

  O kit passou a medir essas três coisas hoje, no ramo `melhorias/mapa-social`.
- **a US de articulação completa:** `mapa_social_20261027_articulacao.md` e
  `estudo_us_articulacao_20261027.md`.
- **os outros planos:** o catálogo das OCI (`registros/fontes/sigtap_grupo09_092026.csv`), as fichas das OCI
  de cardiologia do redacao_08 e o enquadramento do plano 4.

**Os termos:** são todos **calculados** sobre a série do motor.
- **Entrantes:** pedidos novos por mês.
- **Oferta:** agendamentos por mês.
- **Saldo:** entrantes menos oferta. Positivo, a fila cresce.
- **Saldo recente:** os entrantes contra a oferta média dos últimos 3 meses fechados (07 a 09/2026).
- **Falta:** faltas ÷ (realizados + faltas), nos 12 meses fechados (10/2025 a 09/2026).

## 1. O universo

| modalidade | filas | fila válida | fila viva | pessoas |
|---|---|---|---|---|
| radiologia (02.04) | 77 | 14.371 | 14.299 | 13.034 |
| ultrassonografia (02.05) | 85 | 100.431 | 75.283 | 80.597 |
| tomografia (02.06) | 75 | 21.097 | 20.867 | 11.461 |
| ressonância (02.07) | 71 | 9.787 | 9.777 | 7.432 |
| medicina nuclear (02.08) | 15 | 5.632 | 5.632 | 4.152 |
| radiologia intervencionista (02.10) | 0 | — | — | — |

São 92 códigos com rumo. A fila por código no panorama soma só as filas com 10 ou mais pedidos:
a US de articulação dá 14.361 aqui e 14.428 na coleta completa.

## 2. Primeiro descarte: o que outros planos atendem ou vão atender

| quem | códigos | fila válida |
|---|---|---|
| **plano 4** (ISHP, R$ 11,5 mi) | US doppler de vasos, abdômen total, mamária, transvaginal, aparelho urinário, tireoide, próstata abdominal, abdômen superior; TC de abdômen superior, tórax e pelve | 66.859 em US e 17.150 em TC |
| **cardiologia** (IEV e redacao_08) | eco transtorácico (OCI 002-6, 003-4, 006-9) e eco de estresse (004-2) | 14.621 |
| **IEV, ortopedia** | radiografias, US de articulação, TC e RM de coluna e articulações, **só no CID das OCI**: a fila de exame quase não tem esse CID, e o IEV não agenda pela fila do exame | não descarta o código |

A **cintilografia de miocárdio** está na OCI 09.02.01.005-0, mas nenhum plano a contratou: ela
fica. As radiografias periapicais (02.04.01.017-9 e 018-7) são de odontologia, outro objeto.

## 3. Segundo descarte: o que a SES já dá conta

| código | exame | fila | entrantes por mês | oferta por mês | saldo | saldo recente | falta |
|---|---|---|---|---|---|---|---|
| 02.07 (todos) | **ressonância** | 9.787 | — | — | negativo em todos | — | 22% a 30% |
| 02.07.03.003-0 | · RM de membro inferior | 1.694 | 1.208 | 1.537 | −329 | +25 | 24% |
| 02.07.01.004-8 | · RM de coluna lombo-sacra | 1.570 | 1.317 | 1.744 | −428 | — | 22% |
| 02.06.01.007-9 | TC de crânio | 1.403 | 1.141 | 1.276 | −135 | −222 | 34% |
| 02.06.01.004-4 | TC de face, seios e ATM | 394 | 430 | 447 | −17 | −162 | 27% |
| 02.06.01.005-2 | TC de pescoço | 739 | 201 | 201 | 0 | −13 | 36% |
| 02.06.01.006-0 | TC de sela túrcica | 27 | 31 | 35 | −4 | −11 | 28% |
| 02.06.01.001-0/2-8/3-6, 02.06.02.002-3, 02.06.03.002-9 | TC de coluna, de pé e angiotomografia de membro inferior | 620 | — | — | −5 a −35 | — | 25% a 30% |
| 02.04 | radiografias (tórax, coluna, membros) | 14.371 | — | — | +2 a +17, sobre ofertas grandes | — | 18% a 26% |
| 02.05.02.017-8 | US transfontanela | 282 | 74 | 71 | +3 | −3 | 42% |

- **A ressonância não precisa de nós.** A oferta dobrou em 2026: a RM de membro inferior foi de
  8.139 para 18.442 agendamentos em 12 meses, e a de coluna lombo-sacra de 9.170 para 20.932. A
  fila cai em todos os códigos.
- **As TC da carteira atual também não.** A fila do crânio cai uns 135 por mês. Pescoço, face e
  sela estão em equilíbrio ou caindo. As quatro TC podem sair do PT.
- **Radiografia, transfontanela e paquimetria:** a rede agenda em poucos meses o que entra.

## 4. O que sobra, pelo rumo

### 4.1 Menor complexidade (ultrassom, mamografia, densitometria)

| código | exame | fila | fila viva | entrantes por mês | oferta por mês | oferta, 3 últimos meses | saldo recente | estoque (anos) | falta |
|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.006-2 | **US de articulação** | 14.361 | 10.390 | 956 | 674 | 713 | **+244** | 1,8 | 33% |
| 02.04.03.018-8 | **mamografia de rastreamento** | 6.931 | 6.880 | 4.707 | 4.533 | 4.336 | **+371** | 0,1 | 33% |
| 02.04.06.002-8 | **densitometria** | 2.132 | 2.131 | 1.171 | 1.095 | 965 | **+206** | 0,2 | 27% |
| 02.05.02.008-9 | US de globo ocular | 1.309 | 1.309 | 76 | 49 | 63 | +13 | 2,2 | **48%** |
| 02.05.02.007-0 | US de bolsa escrotal | 958 | 614 | 95 | 70 | 61 | +34 | 1,2 | 35% |
| 02.05.02.016-0 | US pélvica | 1.026 | 711 | 132 | 116 | 132 | 0 | 0,7 | 38% |
| 02.05.02.014-3 | US obstétrica | 497 | 495 | 282 | 253 | 264 | +18 | 0,2 | 43% |
| 02.05.02.015-1 | US obstétrica com doppler | 169 | 169 | 43 | 30 | 32 | +11 | 0,5 | 42% |

**O rumo de cada um, mês a mês:**
- **US de articulação: falta oferta o tempo todo.** A rede agenda de 480 a 965 por mês, e entram
  de 750 a 1.190. Nunca houve mês que virasse a fila: ela cresce uns 250 a 280 por mês.
- **Mamografia: houve esforço, ele parou, e a fila voltou a crescer.** A oferta subiu de 12/2025 a
  04/2026, de 4.500 a 6.700 por mês, com o pico em 03/2026. Caiu para uns 3.600 de 05 a 07/2026,
  abaixo dos 4.500 a 4.700 que entram. Voltou a 4.400–5.000 em 08 a 10/2026. A fila foi de
  6.461 (15/10) para 6.931 (27/10).
- **Densitometria: o mesmo desenho.** O esforço foi de 09 a 12/2025, com 1.400 a 1.500 por mês.
  Em 2026 a oferta ficou entre 770 e 1.230, e entram de 1.000 a 1.460. A fila cresce uns 200
  por mês.
- **US de globo ocular: começou oferta nova em 2026.** Até 04/2026 eram 10 a 40 por mês. Depois
  vieram 110 (05), 140 (06), 30, 102 e 58. Os entrantes caem, de 1.115 para 917 por ano. Quase
  metade dos agendados falta.
- **US pélvica: a fila está parada.** Agora a rede agenda o mesmo que entra. A fila é antiga:
  31% de antes de 10/2024.
- **US de bolsa escrotal: a oferta caiu.** Foi de 968 para 834 por ano, e a fila cresce uns 30
  por mês.

### 4.2 Maior complexidade (medicina nuclear), se for preciso

| código | exame | fila | entrantes por mês | oferta por mês | saldo recente | estoque (anos) | falta |
|---|---|---|---|---|---|---|---|
| 02.08.01.002-5 | cintilografia de miocárdio, estresse | 1.732 | 106 | 31 | +66 | **4,6** | 44% |
| 02.08.01.003-3 | cintilografia de miocárdio, repouso | 1.492 | 84 | 30 | +45 | **4,2** | 42% |
| 02.08.05.003-5 | cintilografia óssea | 1.575 | 207 | 124 | −11 | 1,1 | 46% |
| 02.06.01.009-5 | PET-CT | 378 | 94 | 48 | +50 | 0,7 | 45% |

- **A cintilografia de miocárdio é o maior déficit do panorama:** a rede faz 1 de cada 3 pedidos
  novos.
- **A cintilografia óssea:** a procura dobrou, e a oferta subiu junto nos últimos meses.
- **O PET-CT:** a oferta caiu à metade, de 1.512 para 578 por ano.
- **A medicina nuclear saiu em 16/10 por decisão sua.** Ela exige licença da CNEN, rejeito
  radioativo e radiofármaco do IPEN.

## 5. A falta

**A falta é alta em toda a imagem:** de 18% na radiografia a 59% na cintilografia de glândulas
salivares. Nos candidatos de ultrassom, vai de 33% a 48%. Ela depende de a unidade executora
registrar no SISREG o realizado e a falta.

**O que isso faz com a conta** (estimativa, **calculada**):
1. Para fazer os ~13.400 exames do cenário só de ultrassom com 1 falta a cada 3, é preciso marcar
   uns 20.600.
2. Nos sete ultrassons candidatos, há gente para uns 18.700 em 12 meses:
   - a fila viva, 13.943;
   - mais os pedidos novos, 19.896;
   - menos o que a rede já agenda, 15.156.
3. **Ficam faltando uns 1.900 pacientes.** Por isso a reserva é necessária, e a mamografia e a
   densitometria, que voltaram a crescer, a preenchem.

Nada disso vai para o PT: o absenteísmo é tratamento interno (decisão sua, 21/10).

## 6. O que a análise sugere

**Uma carteira que caiba num aparelho de ultrassom, com a reserva de mamografia e densitometria:**
- **o fundo da carteira:** a US de articulação fora do CID do IEV, pela fila viva, 9.828;
- **as filas pequenas de US:** globo ocular, bolsa escrotal, pélvica, obstétrica e obstétrica com
  doppler. Todas cabem no mesmo aparelho;
- **a reserva:** mamografia e densitometria, que tiveram esforço, perderam força e voltaram a
  crescer. Elas pedem mamógrafo e densitômetro, que são outros aparelhos;
- **saem:** as quatro TC (a SES dá conta), a ressonância e a transfontanela (equilíbrio), e o que
  é do plano 4 e da cardiologia;
- **se precisar de maior complexidade:** a cintilografia de miocárdio, o maior déficit do
  panorama, com a ressalva da CNEN.

## 7. Lacunas

- A falta depende do registro da unidade executora no SISREG, e o painel não diz se cada unidade
  registra.
- O painel não diz quem executou cada agendamento: o esforço de 2026 na mamografia e na RM não
  tem dono identificado.
- O panorama corta as filas com menos de 10 pedidos, e a soma por código pode ficar um pouco
  abaixo da medição completa.
- A US de próstata transretal ficou fora do panorama (22 pedidos), e falta confirmar na ficha
  da OCI 004-9 se a US de próstata é a transretal.
