# Estudo — o que fazer com o R$ 1,5 milhão de imagem

**Controle interno.** Estudo de 26/10/2026 para o redacao_07: Emenda de Bancada do DF 71080005,
proposta 36000722999202500, R$ 1.502.687,00, federal, ação 2E90; proponente ISHP; objeto
"Exames de imagem" (Ofício 88/2026 da Bancada). Reabre a carteira do PT simplificado v1: doze
exames, 10% de apoio, 12 meses. A escolha é sua.

**As fontes:**
- **a fila:** coleta nova do Mapa Social, recarga de 26/10/2026 16:32, pelo método de 25/10
  (`planos/redacao_07/dados/fontes/mapa_social_20261026.md`, na sua pasta, conferência 8/8). A
  de 15/10 fica como estava;
- **os valores:** `dados/valor_unitario.md` (tabela mais o incremento do Anexo I da SAES
  4.282/2026);
- **o mercado:** `dados/precos.md` de 16/10/2026, com dez dos doze exames. A densitometria, a US
  obstétrica e a TC de sela não têm preço;
- **o redacao_07:** no ramo `pre-plano-07-imagem-bancada` e no stash de 23/10.

**A conta parte de R$ 1.352.418,30 para exames:** o recurso menos 10% de apoio, como no PT v1.

> **Atualização (26/10/2026, à noite):** o mapeamento do IEV (`mapeamento_iev_20261026.md`, seção
> 4) mostra que o IEV não agendou nenhum exame da fila de US de articulação, e que só 879 dos
> 14.391 pedidos (6,1%) têm CID que a OCI de ortopedia dele aceita. O motivo do corte de 20/10
> não se sustenta: a US de articulação fora do CID da OCI vira candidata ao destino D da sobra.

## 1. O que não muda

- **O ofício.** "Exames de imagem" é largo: qualquer exame de imagem cabe, e o PT v1 segue o
  ofício, como o Ofício 398 da ARINS pediu.
- **O valor.** É a tabela mais o incremento, como no plano 4, por decisão sua de 20/10.
  - O incremento é da habilitação do estabelecimento (LI-040, SES-01): a 38.05 na 4.282, a
    38.01 na 4.694 e a 38.06 na 4.695. O ISHP tem CNES (8078858).
  - A 4.694 (38.01) só vale até 31/12/2026 (art. 6º); a 4.282 e a 4.695 não têm prazo.
  - É um risco da carteira inteira, não de um exame.
- **Os cortes de 15 a 20/10** (`dados/estudo_das_filas.md`): sai o que outro projeto cobre (o
  plano 4 e as OCI do IEV), a cintilografia, a ressonância e o que está fora do rol. A coleta de
  hoje confirma a ressonância: quinze códigos, 9.705 na fila, 126.874 agendadas em 12 meses, e
  estoque abaixo de 0,1 ano em todos.

## 2. O que a fila de hoje mostra

| exame | fila 15/10 → 26/10 | fila viva | espera média 15/10 → 26/10 | agendadas em 12 m | anos de estoque |
|---|---|---|---|---|---|
| US pélvica | 1.005 → 1.025 | 708 | 607 → 606 dias | 1.360 | 0,8 |
| US de bolsa escrotal | 995 → 967 | 623 | 588 → 571 | 916 | 1,1 |
| US transfontanela | 283 → 291 | 262 | 290 → 292 | 826 | 0,4 |
| US de globo ocular | 1.272 → 1.308 | 1.308 | 264 → 267 | 598 | **2,2** |
| TC de crânio | 1.467 → 1.453 | 1.425 | 197 → 206 | 14.949 | 0,1 |
| US obstétrica com doppler | 205 → 169 | 169 | 177 → 196 | 376 | 0,4 |
| TC de sela túrcica | 45 → 48 | 48 | 169 → 169 | 419 | 0,1 |
| US obstétrica | 464 → 487 | 485 | 144 → 145 | 2.957 | 0,2 |
| TC de pescoço | 755 → 779 | 773 | 139 → 139 | 2.432 | 0,3 |
| TC de face, seios e ATM | 503 → 470 | 468 | 126 → 138 | 5.406 | 0,1 |
| mamografia de rastreamento | 6.461 → 6.917 | 6.832 | 49 → 66 | 55.649 | 0,1 |
| densitometria | 2.196 → 2.188 | 2.185 | 44 → 46 | 12.827 | 0,2 |

"Anos de estoque" é a fila ÷ as agendadas em 12 meses (calculado pelo agente).

**Quatro coisas que a coleta de 15/10 não mostrava:**
- **As TC da carteira não são só eletivas.** O código junta três tipos de pedido:

  | TC | eletiva | angiotomografia | emergência |
  |---|---|---|---|
  | crânio | 452 (106 dias) | 382 (75 dias) | 619 (362 dias) |
  | pescoço | 503 (116 dias) | 176 (97 dias) | 100 (330 dias) |
  | face, seios e ATM | 398 (95 dias), com 191 de cone beam | — | 72 (376 dias) |
  | sela túrcica | 27 (80 dias) | — | 21 (284 dias) |

  - **A emergência** é pedido de pronto-atendimento parado há quase um ano, quase todo da
    Região Sudoeste (532 dos 619 do crânio, 95 dos 100 do pescoço). Convênio ambulatorial não
    atende isso.
  - **A cone beam** é tomografia odontológica (CID K01, K04, S02), de outro aparelho.
  - **A angiotomografia** é eletiva, mas pede tomógrafo com bomba injetora. De 61% a 68% dos
    pedidos vêm de URD e contratados.
- **A rede dá conta de quase toda a carteira.** Só a US de globo ocular tem estoque longo: 2,2
  anos de agendamentos, com todos os pedidos desde 06/2025. A bolsa escrotal tem 1,1 ano e a US
  pélvica, 0,8. Nas outras, a rede agenda por ano de 2 a 11 vezes a fila. Nos dez exames de
  espera longa, são 30.239 agendamentos em 12 meses para 6.997 na fila.
- **A espera longa da US pélvica e da bolsa escrotal é em parte fila velha.** São 31% e 36% dos
  pedidos de antes de 26/10/2024 (alarme de fila velha). Pela fila viva, as duas caem para 708
  e 623.
- **A mamografia cresceu:** mais 456 pedidos em onze dias, e a espera foi de 49 para 66 dias.
  A rede ainda agenda 55.649 por ano. Na fila de rastreamento, 486 pedidos têm CID de queixa
  mamária e 214 de câncer de mama (C50): são de diagnóstico com o código de rastreamento (P-04).

## 3. Quanto custa zerar

| o que | exames | valor |
|---|---|---|
| as seis US | 4.247 | R$ 424.485,74 |
| TC eletiva, sem a cone beam | 1.189 | R$ 356.859,19 |
| TC, angiotomografia | 558 | R$ 167.468,42 |
| TC, emergência | 812 | R$ 243.696,20 |
| TC, cone beam | 191 | R$ 57.328,65 |
| **os dez, o código inteiro** (a conta do PT v1) | 6.997 | **R$ 1.249.838,20**: sobram R$ 102.580,10 |
| **os dez, eletiva e angiotomografia** | 5.994 | **R$ 948.813,35**: sobram R$ 403.604,95 |
| os dez, só a eletiva | 5.436 | R$ 781.344,93: sobram R$ 571.073,37 |
| mamografia | 6.917 | R$ 691.008,30 |
| densitometria | 2.188 | R$ 482.235,20 |

- **O que muda:** pelo código inteiro, a conta é quase a de 15/10 (R$ 1.252.250,57). Tirando
  a emergência e a cone beam, que um convênio ambulatorial não deveria contar, sobram uns R$ 400
  mil. A reserva do PT v1 deixa de ser de reserva.
- **O PT continua certo.** Ele diz que o recurso alcança "mais da metade da fila desses
  procedimentos" (em valor): é 55,8% pelo código inteiro de hoje e 63,7% sem a emergência e a
  cone beam.

## 4. Para onde vai a sobra

Com a TC eletiva e a angiotomografia, a sobra é de R$ 403.604,95.

| destino | o que compra | a favor | contra |
|---|---|---|---|
| **A. A reserva do PT v1: mamografia, depois densitometria** | 4.040 mamografias, 58% da fila | já está na carteira; a espera subiu para 66 dias; paga 142% do menor preço do DF; 4.470 pedidos na faixa de 50 a 69 anos | a rede agenda 55.649 por ano |
| **B. Os mesmos dez, com quem entra na fila nos 12 meses** | depende da regulação | o mesmo objeto; o PT já diz que a quantidade é pactuada com a SES | os entrantes não foram coletados; a rede já agenda 30.239 por ano |
| C. Eco transtorácico | 2.520 ecos | espera de 127 dias; é exame de imagem do rol | ver abaixo |
| D. US de articulação e partes moles | 4.038 exames | a maior espera fora da carteira: 547 dias, 1,8 ano de estoque, 10.396 pedidos na fila viva | é secundário obrigatório da OCI de ortopedia 09.03.01.002-0 do IEV (Fila Zero e DOA), e a regra dos cortes de 20/10 o tirou |

**O que pesa contra o eco (C):**
- a fila caiu 1.577 pedidos em onze dias (de 16.298 para 14.721);
- a rede agenda 40.355 por ano;
- paga 80% do menor preço do DF;
- você o tirou em 15/10;
- disputa as 1.676 pessoas da OCI 003-4 da cardiologia que esperam eco com I20 ou I25.

## 5. A recomendação

**Manter os doze, sem código novo: nada muda no texto do PT.** A mudança é só na conta interna,
no cenário 4:
1. a TC conta só a eletiva e a angiotomografia, e saem a emergência e a cone beam. A
   angiotomografia fica se as clínicas tiverem tomógrafo com bomba injetora;
2. a sobra, de uns R$ 400 mil, vai primeiro para a mamografia (A). A espera dela já subiu, e o
   exame paga bem;
3. o que a regulação mandar de pedido novo dos dez durante os 12 meses entra antes da reserva
   (B), porque o PT prioriza as filas de maior espera.

**O eco não volta.** A fila dele anda sozinha, e isso vale para as duas emendas: o estudo de
cardiologia também não o recomenda.

**A US de articulação (D) só se você mudar a regra dos cortes.** É a necessidade maior, mas a
mesma fila alimenta a OCI de ortopedia do IEV.

## 6. Se o PT for reenviado

Não mexi no PT. Se ele voltar a ser enviado:
- a tabela da fila pode ir para 26/10/2026;
- falta decidir se a TC aparece pelo código inteiro, como está, ou só com a eletiva e a
  angiotomografia. Só a eletiva e a angiotomografia é mais fiel, mas o crânio cai de 1.453 para
  834 pedidos;
- a frase "mais da metade" vale nas duas contas.

## 7. O que falta

- **O preço** da densitometria, da US obstétrica e da TC de sela (agente `precos`).
- **O preço da angiotomografia**, que deve passar do da TC simples: cotar à parte.
- **Os entrantes** dos dez por mês, que dizem quanto cabe no destino B (agente `mapa-social`).
- **A SES-01:** com a 38.01 indo só até 31/12/2026, perguntar se o valor com incremento vale num
  convênio que comece em 2027.
