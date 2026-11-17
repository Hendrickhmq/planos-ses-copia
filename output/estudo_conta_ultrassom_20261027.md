# Conta — ultrassom num aparelho só, com mamografia e densitometria de reserva

**Controle interno.** Conta de 27/10/2026 para o redacao_07: Emenda de Bancada do DF 71080005,
R$ 1.502.687,00. A carteira é a que você escolheu hoje:
- a US de articulação fora do CID da OCI do IEV;
- as US pequenas: globo ocular, bolsa escrotal, pélvica, obstétrica e obstétrica com doppler;
- de reserva, a mamografia e depois a densitometria;
- sem as TC.

**A US transfontanela também saiu.** O panorama a pôs entre as que a SES já dá conta: entram
74 pedidos por mês, e a rede agenda 76.

**A planilha:** `planos/redacao_07/cenario_5_ultrassom_com_reserva.xlsx`, na sua pasta, com
fórmulas. Três premissas em amarelo podem mudar, e a planilha recalcula:
- o recurso;
- os 10% de apoio;
- **contar a falta (1 ou 0)**.

**As fontes:**
- **as filas e o rumo:** as coletas do agente `mapa-social` de 27/10/2026, o panorama de imagem e a
  US de articulação completa;
- **os valores:** `dados/valor_unitario.md`, a tabela mais o incremento da Portaria SAES/MS
  4.282/2026;
- **a análise:** `output/estudo_panorama_imagem_20261027.md`.

## 1. As duas formas de contar

| | **contando a falta** (a recomendada) | sem contar a falta |
|---|---|---|
| a base de cada exame | o que se realiza em 12 meses: a fila viva, mais o que entra e a rede não agenda, menos a falta | a fila viva de hoje |
| exames realizados | **13.532** | 13.532 |
| valor pago em exames | **R$ 1.352.326,36** | R$ 1.352.412,40 |
| sobra | R$ 91,94 | R$ 5,90 |
| vagas a agendar (controle interno) | **20.786** | 21.107 |

**O total de exames é o mesmo.** Quase todo exame custa uns R$ 100, então o dinheiro fixa o
número. **O que muda é a mistura:**
- **sem contar a falta,** o ultrassom leva quase tudo e sobram R$ 40 mil para 406 mamografias;
- **mas essa conta não fecha na prática.** Para zerar a fila viva da US de articulação (9.828) com
  33% de falta, é preciso agendar 14.713, e em 12 meses só há 12.744 pessoas disponíveis nessa fila;
- **contando a falta,** o ultrassom fica com o que de fato se realiza, e a reserva entra com
  R$ 257 mil.

## 2. A conta contando a falta

| ordem | exame | fila viva | entram por mês | a rede agenda por mês | disponíveis em 12 meses | falta | realizáveis | **exames** | **valor** | vagas a agendar |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | US de articulação, fora do CID do IEV | 9.828 | 956 | 713 | 12.744 | 33% | 8.512 | **8.512** | R$ 850.689,28 | 12.743 |
| 2 | US de globo ocular | 1.309 | 76 | 63 | 1.465 | 48% | 755 | **755** | R$ 75.454,70 | 1.464 |
| 3 | US de bolsa escrotal | 614 | 95 | 61 | 1.022 | 35% | 668 | **668** | R$ 66.759,92 | 1.022 |
| 4 | US pélvica | 711 | 132 | 132 | 711 | 38% | 440 | **440** | R$ 43.973,60 | 710 |
| 5 | US obstétrica | 495 | 282 | 264 | 711 | 43% | 403 | **403** | R$ 40.275,82 | 711 |
| 6 | US obstétrica com doppler | 169 | 43 | 32 | 301 | 42% | 173 | **173** | R$ 17.331,14 | 300 |
| | **ultrassom** | **13.126** | | | | | | **10.951** | **R$ 1.094.484,46** | **16.950** |
| 7 | mamografia (reserva 1) | 6.880 | 4.707 | 4.336 | 11.332 | 33% | 7.626 | **2.581** | R$ 257.841,90 | 3.836 |
| 8 | densitometria (reserva 2) | 2.131 | 1.171 | 965 | 4.603 | 27% | 3.355 | **0** | — | — |
| | **total** | | | | | | | **13.532** | **R$ 1.352.326,36** | **20.786** |

Com os 10% de apoio (R$ 150.268,70), o total programado é **R$ 1.502.595,06**.

**O que a conta diz:**
- **O ultrassom realiza uns 11 mil exames num aparelho só.** É 81% dos exames e 81% do valor.
- **A articulação é o grosso:** 8.512 exames, 87% da fila viva fora do CID do IEV.
- **As US pequenas zeram ou quase zeram.** A bolsa escrotal e a obstétrica com doppler passam
  de 100% da fila viva, porque contam também quem entra em 12 meses. A US de globo ocular fica
  em 58% e a pélvica em 62%: é a falta que pesa.
- **A mamografia recebe uns R$ 258 mil e faz 2.581 exames,** 38% da fila viva. A fila dela voltou
  a crescer uns 370 por mês.
- **A densitometria não recebe nada nesta ordem.** Se você quiser as duas reservas, dá para
  dividir os R$ 258 mil. Pela metade para cada: uns 1.290 mamografias e 584 densitometrias.

## 3. A premissa da falta

"Realizáveis" supõe que **quem falta não volta à fila**. É a premissa pessimista:
- **se a regulação remarca quem falta,** o ultrassom absorve mais, e a reserva diminui;
- **a falta é a do SISREG em 12 meses** (10/2025 a 09/2026), pela situação do agendamento, e depende
  de a unidade registrar;
- **nada disso vai ao PT:** nem taxa de absenteísmo nem sobre-oferta de vagas (decisão sua, 21/10).
  As 20.786 vagas são para a operação do ISHP.

## 4. O que muda no PT, se for por esta carteira

O PT v1 tem doze códigos:

| sai | entra | fica |
|---|---|---|
| TC de crânio, pescoço, face e sela; US transfontanela | US de articulação (02.05.02.006-2, R$ 99,94, no Anexo I da 4.282) | US pélvica, bolsa escrotal, globo ocular, obstétrica e obstétrica com doppler; mamografia e densitometria |

- **A carteira vai de doze para oito códigos.**
- **A frase "mais da metade da fila" tem de ser refeita:** a fila da articulação muda a conta.
- **A ficha da articulação já existe** (`sigtap_0205020062_102026.md`). Ela não pede CID, e os
  CBO são radiologista e radiologista intervencionista.
- **O preço de mercado da articulação já existe.** O menor no DF é R$ 68,50 (Medprev, Sobradinho),
  e o valor pago é 146% dele. Falta o preço da densitometria e da US obstétrica.
- **A US de articulação foi sua decisão de 15/10 e 16/10.** Ela volta com o mapeamento do IEV de
  26/10 e a coleta completa de 27/10.
