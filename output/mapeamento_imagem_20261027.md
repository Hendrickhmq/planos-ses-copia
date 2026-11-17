# Mapeamento de imagem — o R$ 1,5 milhão da Emenda de Bancada 71080005

**Controle interno.** Documento de 27/10/2026 que reúne o que se sondou para o redacao_07:
- tudo de imagem que tem fila no DF;
- o que se descartou, e por quê;
- o que ficou na carteira;
- o que mais daria para fazer, porque tem fila.

O PT continua como estava: nada daqui foi para o documento.

## 1. O recurso e o objeto

| | |
|---|---|
| Emenda | Bancada do DF 71080005, proposta 36000722999202500, OGU 2025, **federal**, ação 2E90 |
| Valor | **R$ 1.502.687,00**: R$ 150.268,70 de gestão e apoio (10%, decisão de 16/10) e **R$ 1.352.418,30 para exames** |
| Proponente | ISHP (CNES 8078858) |
| Objeto | "Exames de imagem" (Ofício 88/2026 da Bancada). Era otorrino (redacao_05), e a ARINS pediu imagem (Ofício 398/2026, 13/10) |
| Valor por exame | tabela do SIGTAP mais o incremento do Anexo I da Portaria SAES/MS 4.282/2026, truncado no centavo (`dados/valor_unitario.md`). Exame fora do rol da 4.282 paga só a tabela |
| Vigência | 12 meses |
| Instrumento | convênio (serviço assistencial complementar ao SUS) |

## 2. O que se sondou

| quando | o quê | onde está |
|---|---|---|
| 15/10 | primeira coleta das filas de imagem e estudo das filas (16 procedimentos) | `planos/redacao_07/dados/fontes/mapa_social_20261015.md` (ramo `pre-plano-07-imagem-bancada`), `dados/estudo_das_filas.md` |
| 16/10 | fichas do SIGTAP dos 16 procedimentos e pesquisa de preço no DF | `dados/fontes/sigtap_*_102026.md`, `dados/precos.md` |
| 20/10 | carteira de 12 exames, com 4 TC de coluna e segmentos fora (sobreposição com a OCI 003-8 do IEV); mamografia e densitometria de reserva | `cenario_4_espera_longa_com_reserva.xlsx` |
| 26/10 | recoleta das filas de imagem: a TC mistura eletiva, angiotomografia, emergência e cone beam | `mapa_social_20261026.md`, `output/estudo_imagem_1_5_milhao_20261026.md` |
| 26/10 | mapeamento do IEV: o que contratou, onde executa e o que já fez | `mapa_social_20261026_iev.md`, `output/mapeamento_iev_20261026.md` |
| 27/10 | estudo por aparelho e falta | `output/estudo_imagem_por_aparelho_20261027.md` |
| 27/10 | **US de articulação completa**: 61 filas, dentro e fora do CID da OCI do IEV, região, idade, CID, ano, entrantes | `mapa_social_20261027_articulacao.md`, `output/estudo_us_articulacao_20261027.md` |
| 27/10 | **panorama de imagem** com o rumo de cada código: entrantes, oferta pelo mês do agendamento, realizados, faltas, situação | `mapa_social_20261027_panorama.md`, `output/estudo_panorama_imagem_20261027.md` |
| 27/10 | **conta da carteira escolhida** | `planos/redacao_07/cenario_5_ultrassom_com_reserva.xlsx`, `output/estudo_conta_ultrassom_20261027.md` |

As coletas de 26 e 27/10 estão em `planos/redacao_07/dados/fontes/`, na sua pasta. Todas são do
agente `mapa-social` e passaram na conferência. A de 27/10 usa o kit novo (ramo
`melhorias/mapa-social`), que passou a medir a oferta pelo mês do agendamento e as faltas.

## 3. Como ler os números

| termo | o que é |
|---|---|
| **total de solicitações** | os pedidos na lista de espera do SISREG em quatro situações: pendente de regulação, corrigido e reenviado, pendente por fila de espera e devolvido |
| **devolvidas** | pedidos que a regulação devolveu ao médico para completar (falta dado, CID ou justificativa). Não podem ser agendados enquanto não voltam corrigidos |
| **fila** | **total − devolvidas**. Conferido nas 323 filas do panorama: a conta bate em todas |
| **fila viva** | a fila só com os pedidos dos últimos 24 meses (de 27/10/2024 em diante), já sem as devolvidas |
| **entram por mês** | pedidos novos por mês (abertos mais os já agendados, pelo mês do pedido), média de 10/2025 a 09/2026 |
| **rede agenda por mês** | agendamentos pelo mês em que acontecem, média dos 12 meses fechados e dos 3 últimos (07 a 09/2026) |
| **saldo recente** | entram por mês − rede nos 3 últimos meses. Positivo, a fila cresce |
| **estoque** | fila ÷ agendamentos de 12 meses, em anos: abaixo de 0,3, a rede esvazia a fila em poucos meses |
| **falta** | faltas ÷ (realizados + faltas) nos 12 meses fechados, pela situação do agendamento no SISREG |

As **pessoas** não se somam entre exames, porque a mesma pessoa pode esperar mais de um. O
panorama soma por código as filas com 10 ou mais pedidos. A US de articulação tem coleta
completa (14.428 na fila), e o panorama dá 14.361.

## 4. O universo: tudo de imagem que tem fila

| modalidade | filas com 10 ou mais | fila | fila viva | pessoas |
|---|---|---|---|---|
| ultrassonografia (02.05) | 85 | 100.431 | 75.283 | 80.597 |
| tomografia (02.06) | 75 | 21.097 | 20.867 | 11.461 |
| radiologia (02.04) | 77 | 14.371 | 14.299 | 13.034 |
| ressonância (02.07) | 71 | 9.787 | 9.777 | 7.432 |
| medicina nuclear (02.08) | 15 | 5.632 | 5.632 | 4.152 |
| radiologia intervencionista (02.10) | 0 | — | — | — |

Totais do motor, com cada pedido uma vez. São **92 códigos SIGTAP**, e cada um cai num destes grupos:

| grupo | códigos | fila | fila viva |
|---|---|---|---|
| **na carteira ampla: ultrassom** (seção 5) | 6 | 18.320 | 13.688 |
| **na carteira ampla: mamografia e densitometria** (seção 5) | 2 | 9.063 | 9.011 |
| descartado: **plano 4** (6.1) | 11 | 84.009 | 63.444 |
| descartado: **cardiologia** (6.2) | 2 | 14.621 | 14.621 |
| descartado: **IEV, próstata** (6.3) | 1 | 22 | 22 |
| descartado: **a SES dá conta** (6.4) | 51 | 16.288 | 16.204 |
| descartado: **odontologia** (6.5) | 2 | 1.885 | 1.881 |
| fora por decisão: **medicina nuclear e PET-CT** (6.6) | 15 | 5.980 | 5.980 |
| descartado: **filas mínimas de ultrassom** (6.7) | 2 | 29 | 22 |

## 5. A carteira ampla: tudo o que gostaríamos de atender

**A decisão de 27/10/2026:**
- **O PT leva a carteira ampla**, sem carteira e reserva separadas.
- **A ordem de ataque das filas se decide na execução,** ou no plano detalhado, com a fila
  daquele momento.
- **O porquê:** o pré-plano fixa os códigos. O plano detalhado pode usar parte da carteira, mas
  não pode incluir código fora dela. Então a carteira tem de trazer tudo o que talvez se queira
  atacar em 12 meses.

**A ideia continua:**
- um aparelho de ultrassom e um médico, com várias filas. Quando alguém falta, a vaga vai para o
  próximo de qualquer uma delas, e o aparelho não fica parado;
- a menor complexidade vem primeiro.

**A planilha:** `planos/redacao_07/carteira_ampla_imagem.xlsx`, com fórmulas.
- Você escreve a **prioridade** de cada fila, e a conta refaz na hora: o recurso vai na ordem da
  prioridade.
- A fila sem prioridade fica fora da conta, mas continua na lista.
- No resumo, dá para trocar a base da conta: o que se realiza contando a falta, a fila viva ou a
  fila.

| prioridade sugerida | aparelho | código | exame | no mapeamento | fila | fila viva | tabela SIGTAP | incremento | **valor pago por exame** | custo de zerar a fila | custo de zerar a viva |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ultrassom | 02.05.02.006-2 | US de articulação e partes moles, CID não ortopédico (estimado) | entra | 4.361 | 2.948 | R$ 24,20 | 313% | **R$ 99,94** | R$ 435.838,34 | R$ 294.623,12 |
| 2 | ultrassom | 02.05.02.008-9 | US de globo ocular / órbita | entra | 1.309 | 1.309 | R$ 24,20 | 313% | **R$ 99,94** | R$ 130.821,46 | R$ 130.821,46 |
| 3 | ultrassom | 02.05.02.007-0 | US de bolsa escrotal | entra | 958 | 614 | R$ 24,20 | 313% | **R$ 99,94** | R$ 95.742,52 | R$ 61.363,16 |
| 4 | ultrassom | 02.05.02.016-0 | US pélvica (ginecológica) | entra | 1.026 | 711 | R$ 24,20 | 313% | **R$ 99,94** | R$ 102.538,44 | R$ 71.057,34 |
| 5 | ultrassom | 02.05.02.014-3 | US obstétrica | entra | 497 | 495 | R$ 24,20 | 313% | **R$ 99,94** | R$ 49.670,18 | R$ 49.470,30 |
| 6 | ultrassom | 02.05.02.015-1 | US obstétrica com doppler | entra | 169 | 169 | R$ 39,60 | 153% | **R$ 100,18** | R$ 16.930,42 | R$ 16.930,42 |
| 7 | mamógrafo | 02.04.03.018-8 | Mamografia bilateral de rastreamento | entra | 6.931 | 6.880 | R$ 45,00 | 122% | **R$ 99,90** | R$ 692.406,90 | R$ 687.312,00 |
| 8 | densitômetro | 02.04.06.002-8 | Densitometria óssea | entra | 2.132 | 2.131 | R$ 55,10 | 300% | **R$ 220,40** | R$ 469.892,80 | R$ 469.672,40 |
| — | ultrassom | 02.05.02.006-2 | US de articulação, CID ortopédico (estimado) | o IEV consome (27/10/2026); volta se ele não absorver | 9.188 | 6.884 | R$ 24,20 | 313% | **R$ 99,94** | R$ 918.248,72 | R$ 687.986,96 |
| — | tomógrafo | 02.06.01.007-9 | TC de crânio | pode entrar: a rede dá conta hoje | 1.403 | 1.375 | R$ 97,44 | 208% | **R$ 300,11** | R$ 421.054,33 | R$ 412.651,25 |
| — | tomógrafo | 02.06.01.005-2 | TC de pescoço | pode entrar: a rede dá conta hoje | 739 | 733 | R$ 86,75 | 246% | **R$ 300,15** | R$ 221.810,85 | R$ 220.009,95 |
| — | tomógrafo | 02.06.01.004-4 | TC de face / seios da face / ATM | pode entrar: a rede dá conta hoje | 394 | 392 | R$ 86,75 | 246% | **R$ 300,15** | R$ 118.259,10 | R$ 117.658,80 |
| — | tomógrafo | 02.06.01.006-0 | TC de sela túrcica | pode entrar: a rede dá conta hoje | 27 | 27 | R$ 97,44 | 208% | **R$ 300,11** | R$ 8.102,97 | R$ 8.102,97 |
| — | gama-câmara | 02.08.01.002-5 | Cintilografia de miocárdio, estresse | pode entrar: maior complexidade (CNEN) | 1.732 | 1.732 | R$ 408,52 | 120% | **R$ 898,74** | R$ 1.556.617,68 | R$ 1.556.617,68 |
| — | gama-câmara | 02.08.01.003-3 | Cintilografia de miocárdio, repouso | pode entrar: maior complexidade (CNEN) | 1.492 | 1.492 | R$ 383,07 | 130% | **R$ 881,06** | R$ 1.314.541,52 | R$ 1.314.541,52 |
| — | gama-câmara | 02.08.05.003-5 | Cintilografia óssea | pode entrar: maior complexidade (CNEN) | 1.575 | 1.575 | R$ 190,99 | 300% | **R$ 763,96** | R$ 1.203.237,00 | R$ 1.203.237,00 |
| | | | **as 16 linhas (15 códigos)** | | **33.933** | **29.467** | | | | **R$ 7.755.713,23** | **R$ 7.302.056,33** |

- **O recurso para exames cobre 18,5% da fila viva das 16 linhas, em valor.** Só as oito com
  prioridade custariam R$ 1,78 milhão pela fila viva.
- **A US de articulação está dividida pelo CID desde 27/10** (seção 5.6). A parte ortopédica fica
  na lista sem prioridade, porque o IEV vai consumi-la.
- **Saíram da lista por decisão sua (27/10):** a US doppler de fluxo obstétrico, a US de tórax e a
  US transfontanela (seções 6.4 e 6.7).
- **O que fica sem prioridade está na lista para não fechar a porta:**
  - as TC estavam no PT v1. Se a rede deixar de dar conta, como aconteceu com a mamografia, elas
    podem entrar;
  - a medicina nuclear você tirou em 16/10, pela exigência da CNEN.
- **Falta decidir** quais linhas sem prioridade ficam na lista, e se a densitometria entra antes
  da mamografia.
- **Na TC, a fila do código junta eletiva, angiotomografia, emergência e cone beam.** Se a TC
  entrar, a base deve ser só a eletiva.

### 5.1 Ultrassom

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.006-2 | Ultrassonografia de articulacao | 41 | 19.166 | 4.805 | **14.361** | 10.390 | 546 | 956 | 674 | 713 | +244 | 1,8 | 33% | sim, R$ 99,94 |
| 02.05.02.008-9 | Ultrassonografia de globo ocular / orbita (monocular) | 1 | 1.507 | 198 | **1.309** | 1.309 | 268 | 76 | 49 | 63 | +13 | 2,2 | 48% | sim, R$ 99,94 |
| 02.05.02.016-0 | Ultrassonografia pelvica (ginecologica) | 2 | 1.945 | 919 | **1.026** | 711 | 601 | 132 | 116 | 132 | 0 | 0,7 | 38% | sim, R$ 99,94 |
| 02.05.02.007-0 | Ultrassonografia de bolsa escrotal | 3 | 1.461 | 503 | **958** | 614 | 573 | 95 | 70 | 61 | +34 | 1,1 | 35% | sim, R$ 99,94 |
| 02.05.02.014-3 | Ultrassonografia obstétrica | 3 | 1.410 | 913 | **497** | 495 | 143 | 282 | 253 | 264 | +18 | 0,2 | 43% | sim, R$ 99,94 |
| 02.05.02.015-1 | Ultrassonografia obstetrica c/ doppler colorido e pulsado | 1 | 310 | 141 | **169** | 169 | 197 | 43 | 30 | 32 | +11 | 0,5 | 42% | sim, R$ 100,18 |

- **US de articulação.** A rede nunca alcançou a procura em nenhum mês da série, e a fila cresce
  uns 250 por mês. A tabela acima é o código inteiro.
  - **Na conta fica só a parte de CID não ortopédico:** nódulo, lipoma, cisto, hérnia, linfonodo
    e pescoço. São uns 4.361 pedidos na fila e 2.948 na viva (estimativa).
  - **O ortopédico** (uns 9.188 fora do CID da OCI, mais os 879 dentro) **o IEV vai consumir**,
    pela decisão de 27/10 (seção 5.6).
- **US de globo ocular.** Tem o maior estoque (2,2 anos). Começou oferta nova em 05/2026, ainda
  irregular. Quase metade dos agendados falta. A ficha aceita oftalmologista ou radiologista.
- **US de bolsa escrotal.** A oferta caiu (de 968 para 834 por ano), e a fila cresce uns 30 por mês.
- **US pélvica.** A fila está parada e é antiga: 31% dos pedidos são de antes de 10/2024.
- **US obstétrica e obstétrica com doppler.** As filas são pequenas e crescem pouco. Juntas, têm
  muitas devolvidas: 1.054 contra 666 na fila.

### 5.2 Mamografia e densitometria

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | 2 | 9.611 | 2.680 | **6.931** | 6.880 | 56 | 4.707 | 4.533 | 4.336 | +371 | 0,1 | 33% | sim, R$ 99,90 |
| 02.04.06.002-8 | Densitometria ossea duo-energetica de coluna (vertebras lombares e/ou  | 1 | 5.804 | 3.672 | **2.132** | 2.131 | 44 | 1.171 | 1.095 | 965 | +206 | 0,2 | 27% | sim, R$ 220,40 |

- **Mamografia.** Houve esforço: de 12/2025 a 04/2026 a rede agendou de 4.500 a 6.700 por mês,
  com o pico em 03/2026. A oferta caiu para uns 3.600 de 05 a 07/2026, e a fila voltou a crescer:
  6.461 (15/10), 6.917 (26/10), 6.931 (27/10).
- **Densitometria.** O mesmo desenho: o esforço foi de 09 a 12/2025, com uns 1.450 por mês. Em
  2026 a oferta ficou em uns 950, e a fila cresce uns 200 por mês.

### 5.3 Um exemplo: a conta pela prioridade sugerida

A conta conta a falta: a base de cada exame é a fila viva, mais o que entra e a rede não agenda,
menos a falta, supondo que quem falta não volta. É a planilha da carteira ampla como sai, e ela
substitui o `cenario_5_ultrassom_com_reserva.xlsx`, que fica como registro.

| prioridade | exame | fila | fila viva | exames | valor por exame | **valor pago** | pela tabela | pelo incremento | vagas a agendar |
|---|---|---|---|---|---|---|---|---|---|
| 1 | US de articulação e partes moles, CID não ortopédico (estimado) | 4.361 | 2.948 | 2.554 | R$ 99,94 | **R$ 255.246,76** | R$ 61.806,80 | R$ 193.439,96 | 3.824 |
| 2 | US de globo ocular | 1.309 | 1.309 | 755 | R$ 99,94 | **R$ 75.454,70** | R$ 18.271,00 | R$ 57.183,70 | 1.464 |
| 3 | US de bolsa escrotal | 958 | 614 | 668 | R$ 99,94 | **R$ 66.759,92** | R$ 16.165,60 | R$ 50.594,32 | 1.022 |
| 4 | US pélvica | 1.026 | 711 | 440 | R$ 99,94 | **R$ 43.973,60** | R$ 10.648,00 | R$ 33.325,60 | 710 |
| 5 | US obstétrica | 497 | 495 | 403 | R$ 99,94 | **R$ 40.275,82** | R$ 9.752,60 | R$ 30.523,22 | 711 |
| 6 | US obstétrica com doppler | 169 | 169 | 173 | R$ 100,18 | **R$ 17.331,14** | R$ 6.850,80 | R$ 10.480,34 | 300 |
| 7 | mamografia | 6.931 | 6.880 | 7.626 | R$ 99,90 | **R$ 761.837,40** | R$ 343.170,00 | R$ 418.667,40 | 11.332 |
| 8 | densitometria | 2.132 | 2.131 | 415 | R$ 220,40 | **R$ 91.466,00** | R$ 22.866,50 | R$ 68.599,50 | 570 |
| | **total** | **17.383** | **15.257** | **13.034** | | **R$ 1.352.345,34** | **R$ 489.531,30** | **R$ 862.814,04** | **19.933** |

- **Do valor pago, R$ 489.531,30 (36%) é a tabela SIGTAP e R$ 862.814,04 (64%) é o incremento**
  do Anexo I da Portaria SAES/MS 4.282/2026. Sem o incremento, cada exame valeria a tabela:
  R$ 24,20 no ultrassom, R$ 45,00 na mamografia e R$ 55,10 na densitometria. Por isso a pendência
  da SES-01 (seção 9) pesa: a 4.694, que dá o incremento à habilitação 38.01, vai só até 31/12/2026.
- **O ultrassom faz 38% dos exames** (4.993). A mamografia faz 7.626, toda a parte realizável
  dela em 12 meses, e a densitometria entra com 415.
- **O total cai de 13.532 para 13.034** porque a densitometria custa R$ 220,40. A sobra é de
  R$ 72,96, e o total programado, com o apoio, é R$ 1.502.614,04.
- **Antes da divisão,** com a articulação inteira (fora do CID da OCI), eram 8.512 exames de
  articulação, 2.581 mamografias e nenhuma densitometria (13.532 exames).
- **As vagas a agendar são para a operação do ISHP.** Não vão ao PT (absenteísmo é tratamento
  interno, decisão de 21/10).

### 5.4 A US de articulação e o IEV: quem pega o quê

**O que o IEV contratou.** A OCI 09.03.01.002-0, "avaliação diagnóstica em ortopedia com recursos
de radiologia e ultrassonografia". Os planos dele a chamam de "ultrassom de partes moles".
- **O pacote, a R$ 140:** consulta de ortopedia, radiografias compatíveis, a US (código
  02.05.02.006-2, secundário obrigatório) e a teleconsulta de retorno.
- **A quantidade:** 12.070 OCI no DOA (pt_ses_02, convênio 030975) e 7.000 no Fila Zero
  (pt_ses_04, 030977). São 19.070.
- **Os 32 CID da ficha** são problemas de tendão, ligamento e sinóvia (a membrana da articulação):
  - **tenossinovite e sinovite:** M65 e as subcategorias M65.0, M65.1, M65.2 (tendinite
    calcificada), M65.4 (De Quervain), M65.8 e M65.9. **O dedo em gatilho (M65.3) não está na lista**;
    - a sinovite transitória (M67.3), a sinovite nas infecções (M68.0), a sinovite crepitante da
      mão e do punho (M70.0) e a sinovite vilonodular (M12.2);
  - **ruptura espontânea de tendão ou sinóvia** (M66) e **de ligamento do joelho** (M23.6);
  - a lista inteira, com os nomes, está em `output/ocis_iev_20261027.md`;
  - **ruptura traumática de ligamento:** cotovelo (S53.2 e S53.3), punho (S63.3), tornozelo e pé
    (S93.2);
  - **osteonecrose** (M87 e M90.3 a M90.5);
  - **I23.4 e I51.1:** ruptura de cordoalha tendínea, que é do coração. Parece erro da ficha, pela
    palavra "tendínea".

**"Partes moles" quer dizer duas coisas diferentes:**
- **no plano do IEV,** são os tecidos moles em volta da articulação (tendão, ligamento, sinóvia), o
  que o ortopedista examina;
- **na fila "ECOGRAFIA DE PARTES MOLES" do SISREG,** são caroços debaixo da pele: nódulo, lipoma,
  cisto, hérnia e linfonodo.

As duas se faturam pelo mesmo código, 02.05.02.006-2, mas não são a mesma demanda.

**Como o paciente chega ao IEV.** Pela fila de **consulta de ortopedia** do SISREG. A US é feita
dentro do pacote e não passa pela fila do exame. Desde o termo (29/04/2026) até 26/10:
- 642 consultas de ortopedia no IEV com CID da 002-0, das quais 308 realizadas;
- **nenhum agendamento da fila de US de articulação** nas três unidades do IEV.

**O que pegaríamos.** A **fila do exame**: pedidos de US que um médico já fez, quase todos da
atenção primária e dos ambulatórios das regiões (só 7 de 14.428 vêm de URD ou contratado). Só os
pedidos fora dos 32 CID da 002-0:

| grupo de filas | fila | no CID do IEV (fica com ele) | **fora do CID (nosso)** | fora, viva |
|---|---|---|---|---|
| articulações (ombro, punho, joelho, tornozelo, cotovelo, quadril, mão, pé) | 9.979 | 781 | **9.195** | 6.974 |
| **partes moles** | 3.124 | 70 | **3.053** | 1.837 |
| região inguinal | 608 | 0 | **608** | 524 |
| pescoço e região cervical | 279 | 0 | **279** | 219 |
| outras regiões (braço, perna, axila, glúteo, glândulas) | 438 | 28 | **410** | 274 |
| **total** | **14.428** | **879** | **13.545** (mais 4 sem CID) | **9.828** |

**A fila de partes moles, em detalhe** ("ECOGRAFIA DE PARTES MOLES"):
- **O tamanho:** 3.124 na fila, 1.878 na viva, 1.456 devolvidas, espera média de 651 dias, e
  pedido desde 2010.
- **O que é do IEV:** 70 pedidos, com M65 (69) e M70 (1). Ficam fora da nossa conta.
- **O resto, 3.053 pedidos, não é ortopedia:**
  - nódulo ou tumefação (R22, 767) e lipoma (D17, 665);
  - cisto de pele (L72, 206) e hérnia inguinal (K40, 190);
  - linfonodo aumentado (R59, 135) e bursopatia (M71, 103);
  - E88 (86), L98 (83), M79 (60) e M72 (39).

  **A OCI do IEV não aceita nenhum desses CID:** é demanda de clínica, cirurgia geral e
  dermatologia, sem outra porta.

**Por que não atrapalha o IEV nem a gente:**
1. **A porta é outra.** O IEV recebe pela consulta de ortopedia; nós, pela fila do exame já
   pedido.
2. **O CID é outro.** Os 879 pedidos com CID da 002-0 ficam fora da nossa conta: quem se
   enquadra na OCI dele continua dele.
3. **A cobrança é outra.** O IEV fatura a APAC da OCI (R$ 140, com consulta, radiografia e US).
   Nós faturamos o procedimento 02.05.02.006-2 (R$ 99,94). Cada um paga o que executou.
4. **A fila não é dele.** Com o IEV funcionando desde 04/2026, o IEV não agendou nenhum exame dela,
   e ela cresce uns 250 por mês.
5. **Ajuda os dois lados.** O paciente que chega à ortopedia do IEV com a US já feita pela nossa
   fila adianta a avaliação dele. E a fila que atendemos deixa de pressionar a ortopedia.

**O risco que sobra: a mesma pessoa nas duas portas.**
- **Como acontece:** quem tem pedido antigo de US na fila do exame e também vai à consulta de
  ortopedia do IEV, que agendou 29.894 consultas desde 04/2026.
- **Os casos:**
  - **o CID está na 002-0:** o IEV faz a US no pacote, e o pedido antigo continua na fila;
  - **ombro (M75):** é o maior grupo da nossa fila, com 2.195 pedidos, e o CID mais comum nas
    consultas do IEV, com 5.414. A 002-0 não o aceita, mas a OCI de ressonância (004-6) aceita
    M75.0 a M75.3. A pessoa pode fazer a RM no IEV e ainda esperar a US na nossa fila.
- **Ainda não se mediu** quantas pessoas estão nas duas portas. O CNS fica dentro do motor, e a
  medida cruzada entre a fila do exame e o agendamento no IEV precisa ser testada no painel.
- **Como evitar:**
  - a regulação confere o histórico antes de agendar (o SISREG mostra) e baixa o pedido de quem
    já fez o exame ou a RM na OCI;
  - pedir à SES essa regra na formalização.

### 5.5 As partes moles do IEV: quanto vai executar e quanto já executou

**O contratado na OCI 09.03.01.002-0**, nos planos aprovados:

| convênio | plano | início e vigência | OCI 002-0 | valor (R$ 140 cada) |
|---|---|---|---|---|
| 030975, DOA | pt_ses_02, item 2.1.2 | 15/04/2026, 16 meses | 12.070 | R$ 1.689.800,00 |
| 030977, Fila Zero | pt_ses_04, item 2.2.2 | 25/04/2026, 13 meses | 7.000 | R$ 980.000,00 |
| **total** | | | **19.070** | **R$ 2.669.800,00** |

**As metas, de dois em dois meses** (tabelas de metas dos dois planos):

| apuração | DOA | Fila Zero | acumulado |
|---|---|---|---|
| 25/07/2026 | 1.609 | 1.167 | 2.776 |
| 25/09/2026 | 1.609 | 1.167 | **5.552** |
| 25/11/2026 | 1.609 | 1.167 | 8.328 |
| 25/01/2027 | 1.609 | 1.167 | 11.104 |
| 25/03/2027 | 1.609 | 1.167 | 13.880 |
| 25/05/2027 | 1.609 | 1.167 | 16.656 |
| 25/08/2027 | 2.414 (em 3 meses) | — | 19.070 |

- **O ritmo contratado é de uns 1.390 OCI por mês** (805 do DOA e 583 do Fila Zero).
- **Até 25/09/2026 venceram metas de 5.552 OCI.**
- **O pagamento vai por parcelas da meta,** não por OCI feita: 25% na assinatura e 15% a cada
  período. Pelo cronograma, até hoje caberiam à 002-0 uns **R$ 1,21 milhão** (calculado, pela
  parte dela em cada convênio):
  - 40% do DOA, R$ 675.920,00;
  - 55% do Fila Zero, R$ 539.000,00.

  Não conferi no Portal da Transparência se as parcelas saíram.

**O que se vê executado:**

| fonte | o que mostra | até |
|---|---|---|
| **SISREG** (Mapa Social, coleta do IEV de 26/10) | 29.894 consultas de ortopedia agendadas no IEV desde 29/04, com 13.818 realizadas e 11.112 faltas. **Com CID da lista da 002-0: 642 agendadas e 308 realizadas.** Nenhum exame da fila de US de articulação agendado nas unidades do IEV | 26/10/2026 |
| **SIA/SUS** (TabNet do DATASUS, produção ambulatorial do DF) | **nenhuma OCI 002-0, nem de outra OCI de ortopedia, apresentada ou aprovada no DF.** No grupo 09 só aparecem o risco cirúrgico (1.932 aprovadas de 12/2025 a 07/2026) e três OCI de otorrino | processamento de 07/2026 |

As consultas do TabNet estão em `planos/redacao_07/dados/fontes/tabnet_sia_20261027/`.

**O que isso diz:**
- **Pelo CID do pedido, o IEV teria feito no máximo umas 308 OCI 002-0 até 26/10.** Isso é 6% das
  5.552 da meta vencida em 25/09, num ritmo de uns 60 por mês contra 1.390 contratados.
- **O número é um indicativo, não a produção.** O CID da APAC é o que o ortopedista registra na
  consulta, que pode não ser o do pedido. O painel não mostra a APAC.
- **O SIA ainda não mostra nada, por um de três motivos:**
  - a APAC da OCI só fecha depois da consulta de retorno, e a ortopedia do IEV começou a
    agendar entre 21/05 e 08/06/2026;
  - o SIA vai só até 07/2026;
  - a produção do convênio pode não ser faturada no SIA. O plano diz que o registro é no
    TrackCare e no SISREG.
- **Para saber o executado de verdade,** é preciso o relatório de monitoramento da SES ou a
  prestação de contas do IEV, no processo SEI de cada convênio.

**Pela ficha da OCI, nada muda no desenho.** Mas o IEV vai consumir tudo o que é ortopédico, e
não só o CID da OCI (você, 27/10): isso muda a conta, na seção 5.6.
- **A fila com CID da 002-0 é pequena:**
  - na fila de consulta, 642 agendamentos com esse CID em seis meses;
  - na fila do exame, 879 pedidos.

  Mesmo que o IEV ou a SES queiram puxar gente da fila do exame para cumprir a meta, só esses
  879 se enquadram, e eles já estão fora da nossa conta.
- **Fora do CID, o IEV não pode faturar a 002-0.** Os 13.545 pedidos que pegaríamos não servem
  para a meta dele.
- **Se o IEV não cumprir a 002-0, quem decide é a SES:** remanejar quantidade, cobrar ou
  devolver. A nossa conta não depende disso.
- **Para comparar, a rede do DF produz uns 1.200 exames de US de articulação por mês no SIA**
  (14.987 de 08/2025 a 07/2026, todas as naturezas jurídicas). O número passa dos ~700 agendados
  pelo SISREG porque inclui o ambulatório dos hospitais, que não passa pela fila.

### 5.6 O IEV consome tudo o que é ortopédico: o que muda para nós

**A premissa (você, 27/10/2026):** tudo o que for ortopédico na fila de US de articulação o IEV
vai consumir, e não só os 32 CID da OCI 002-0. Faz sentido: o IEV já é a porta da ortopedia no DF.
- Ficou com 81% das consultas de ortopedia agendadas desde 29/04.
- 76,5% delas têm CID fora das listas das OCI.

**Como separei** (estimativa, **calculada**). Contei como ortopédico o CID dos capítulos M
(osteomuscular), S e T (trauma), mais o túnel do carpo e as mononeuropatias de membro (G56–G57) e
as malformações de quadril, pé e coluna (Q65–Q79).
- Classifiquei os 10 CID mais pedidos de cada uma das 61 filas, fora do CID da OCI. Eles cobrem
  86% dos pedidos.
- No resto de cada fila, apliquei a mesma proporção.
- Os 4 pedidos sem CID ficaram na parte não ortopédica.

| grupo de filas | fora do CID da OCI | ortopédico (vai ao IEV) | **não ortopédico (nosso)** | o que é o nosso |
|---|---|---|---|---|
| articulações (ombro, punho, joelho…) | 9.195 | ~8.690 (95%) | ~505 | o pouco sem CID de osso ou tendão |
| partes moles | 3.053 | ~265 (9%) | **~2.790** | nódulo, lipoma, cisto de pele, hérnia, linfonodo |
| região inguinal | 608 | ~1 | **~607** | hérnia inguinal |
| pescoço e região cervical | 279 | ~16 | **~263** | pescoço, linfonodo, tireoide |
| outras regiões | 410 | ~220 (55%) | ~190 | axila, glândulas, glúteo |
| **total** | **13.545** | **~9.188** (fila viva ~6.884) | **~4.357** (fila viva ~2.944) | |

Somados os 4 sem CID, a parte não ortopédica fica em **4.361 na fila e 2.948 na viva**. A
ortopédica fica em 9.188 na fila e 6.884 na viva; com os 879 do CID da OCI, são 10.067 pedidos.

**Na planilha da carteira ampla, a US de articulação virou duas linhas:**
- **CID não ortopédico, prioridade 1.**
- **CID ortopédico, sem prioridade:** "o IEV consome; volta se ele não absorver".
- O total, as devolvidas, os pedidos novos e a oferta do código foram divididos na proporção da
  fila: 30,2% para a parte não ortopédica. A falta é a do código inteiro, 33%.

**O que muda:**
1. **A articulação na conta cai de 8.512 para uns 2.554 exames.**
2. **A mamografia passa a ser zerada** na parte realizável em 12 meses (7.626), e a densitometria
   entra (415). O total de exames fica em 13.034.
3. **O ultrassom deixa de ser o centro:** 38% dos exames, contra 81% antes.
   - O argumento de um aparelho só com muitas filas perde força. Quem segura o volume é a
     mamografia, com uns 640 exames por mês.
   - O ISHP precisa de mamógrafo com essa capacidade.
4. **O fundo de fila contra a falta muda de lugar.** A mamografia tem fila funda, que cresce uns
   370 por mês; o ultrassom, sem o ortopédico, tem uns 2.900 na fila viva.
5. **A divisão com o IEV fica limpa:** ele com o ortopédico, nós com o resto, separados pelo
   CID. É fácil de dizer à SES, e o risco da mesma pessoa nas duas portas (seção 5.4) quase some.

**O que não muda:**
- **O código 02.05.02.006-2 continua na carteira,** porque cobre as partes moles e a região
  inguinal.
- **A parte ortopédica fica na carteira ampla, sem prioridade.** Pode voltar por dois caminhos:
  - **o IEV não absorve:** ele realizou 14% da ortopedia em seis meses, e a 002-0 anda a uns 60
    OCI por mês contra 1.390 contratados (seção 5.5);
  - **os convênios acabam:** o Fila Zero termina em 05/2027 e o DOA em 08/2027. Se o nosso
    começar em 2027, essa demanda volta antes do fim dele.
- **Os outros exames não são ortopédicos:** globo ocular, bolsa escrotal, pélvica, obstétricas,
  mamografia e densitometria. As TC e RM de ortopedia já estavam fora.

**Para o número exato:**
- **a fila e a fila viva:** uma coleta com o recorte ortopédico e não ortopédico pelo CID, que o
  kit já faz;
- **os pedidos novos e a oferta por recorte:** o kit ainda não filtra o objeto pelo CID, e eles
  seguem divididos por proporção.

## 6. O que se descartou, e por quê

### 6.1 O plano 4 atende

O plano 4 (ISHP, R$ 11,5 mi, US e TC) tem esses códigos. Em 16/10 você decidiu que o código
inteiro fica fora, e não só o enquadramento dele, pelo risco de sobreposição.

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.004-0 | Ultrassonografia doppler colorido de vasos | 11 | 21.379 | 4.622 | **16.757** | 12.097 | 477 | 1.359 | 1.053 | 1.100 | +259 | 1,3 | 25% | sim, R$ 100,18 |
| 02.05.02.004-6 | Ultrassonografia de abdomen total | 3 | 27.156 | 13.279 | **13.877** | 10.097 | 554 | 1.155 | 889 | 1.169 | -14 | 1,3 | 37% | sim, R$ 100,18 |
| 02.05.02.009-7 | Ultrassonografia mamaria bilateral | 1 | 20.922 | 7.734 | **13.188** | 8.737 | 617 | 914 | 815 | 1.777 | -863 | 1,4 | 38% | sim, R$ 99,94 |
| 02.05.02.018-6 | Ultrassonografia transvaginal | 1 | 18.593 | 8.949 | **9.644** | 6.043 | 638 | 1.260 | 1.467 | 2.064 | -803 | 0,6 | 43% | sim, R$ 99,94 |
| 02.06.03.001-0 | Tomografia computadorizada de abdomen superior | 11 | 13.514 | 7.342 | **6.172** | 6.113 | 175 | 1.516 | 1.476 | 1.504 | +12 | 0,3 | 36% | sim, R$ 299,44 |
| 02.06.02.003-1 | Tomografia computadorizada de tórax | 10 | 11.015 | 5.054 | **5.961** | 5.896 | 218 | 2.488 | 2.463 | 2.950 | -462 | 0,2 | 33% | sim, R$ 300,10 |
| 02.06.03.003-7 | Tomografia computadorizada de pelve / bacia / abdomen inferior | 7 | 9.967 | 4.950 | **5.017** | 4.963 | 178 | 1.272 | 1.247 | 1.309 | -37 | 0,3 | 34% | sim, R$ 299,44 |
| 02.05.02.005-4 | Ultrassonografia de aparelho urinario | 3 | 8.257 | 4.103 | **4.154** | 2.782 | 624 | 481 | 400 | 470 | +11 | 0,9 | 32% | sim, R$ 99,94 |
| 02.05.02.012-7 | Ultrassonografia de tireoide | 3 | 7.190 | 3.327 | **3.863** | 3.107 | 477 | 408 | 299 | 309 | +99 | 1,1 | 24% | sim, R$ 99,94 |
| 02.05.02.010-0 | Ultrassonografia de prostata por via abdominal | 1 | 5.849 | 2.715 | **3.134** | 2.354 | 579 | 366 | 343 | 312 | +54 | 0,8 | 29% | sim, R$ 99,94 |
| 02.05.02.003-8 | Ultrassonografia de abdomen superior | 2 | 3.244 | 1.002 | **2.242** | 1.255 | 678 | 224 | 209 | 221 | +2 | 0,9 | 33% | sim, R$ 99,94 |

Várias dessas filas crescem: doppler de vasos, abdômen total, tireoide e aparelho urinário. Se o
plano 4 não as absorver, voltam a ser candidatas (seção 7).

### 6.2 A cardiologia atende

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.003-2 | Ecocardiografia transtoracica | 3 | 30.997 | 16.446 | **14.551** | 14.551 | 123 | 3.582 | 3.364 | 3.571 | +11 | 0,4 | 26% | sim, R$ 160,14 |
| 02.05.01.001-6 | 5. ecocardiografia de estresse adulto | 1 | 1.507 | 1.437 | **70** | 70 | 26 | 71 | 63 | 70 | +2 | 0,1 | 47% | não |

- **Eco transtorácico.** Está nas OCI 002-6, 003-4 e 006-9. O IEV executa a 006-9 no Fila
  Zero, e o redacao_08 estuda as outras.
- **Eco de estresse.** Está na OCI 004-2, que o IEV executa.
- **O eco também saiu por si.** A fila caiu 1.577 pedidos em onze dias (de 15/10 a 26/10), e o
  saldo recente é quase zero (+11 por mês).

### 6.3 O IEV atende

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.02.011-9 | Ultrassonografia de prostata (via transretal) | 1 | 155 | 133 | **22** | 22 | 121 | 4 | 0 | 0 | +4 | 5,5 | 0% | sim, R$ 99,94 |

A US de próstata transretal está na OCI 09.01.01.004-9 (progressão do câncer de próstata), que o
IEV executa no Fila Zero (1.015 OCI). A fila é mínima, e a ficha de 10/2026 confirma que a US transretal é o exame obrigatório
da OCI. **A parte ortopédica da US de articulação também vai ao IEV** (seção 5.6). As radiografias e as
TC e RM de coluna e membros já estavam fora, porque a rede dá conta delas (seção 6.4).

### 6.4 A SES já dá conta

| código | exame | fila | fila viva | por que a SES dá conta (calculado) |
|---|---|---|---|---|
| 02.04.03.015-3 | Torax : pa e perfil | 645 | 645 | a rede agenda em 0,6 mês o que está na fila; saldo de 45/mês sobre 1.065 de oferta |
| 02.04.04.009-4 | Mao esquerda (ap e obliquo) | 307 | 307 | a rede agenda em 1,4 meses o que está na fila; saldo de 20/mês sobre 203 de oferta |
| 02.04.06.012-5 | Joelho direito (ap e perfil) | 292 | 292 | a rede agenda em 1,2 meses o que está na fila; saldo de 30/mês sobre 235 de oferta |
| 02.04.02.006-9 | Coluna lombo sacra (ap e perfil) | 284 | 284 | a rede agenda em 1,0 mês o que está na fila; saldo de 38/mês sobre 288 de oferta |
| 02.04.06.015-0 | Pe ou pododactilos direito | 246 | 246 | a oferta recente (153/mês) passou a procura (139/mês) |
| 02.04.01.006-3 | Cavum - lateral | 135 | 135 | a rede agenda em 0,6 mês o que está na fila; saldo de 1/mês sobre 216 de oferta |
| 02.04.04.010-8 | Maos e punhos para idade ossea esquerdo | 135 | 135 | a oferta recente (189/mês) passou a procura (176/mês) |
| 02.04.02.003-4 | Coluna cervical (ap e perfil) | 133 | 132 | a rede agenda em 1,1 meses o que está na fila; saldo de 20/mês sobre 104 de oferta |
| 02.04.02.009-3 | Coluna dorsal : ap + lateral | 128 | 128 | a rede agenda em 1,3 meses o que está na fila; saldo de 13/mês sobre 89 de oferta |
| 02.04.06.013-3 | Joelho ou rotula - ap + lat. + axial direito | 116 | 116 | a rede agenda em 1,0 mês o que está na fila; saldo de 23/mês sobre 107 de oferta |
| 02.04.04.012-4 | Punho esquerdo: ap + lateral + obliquos | 110 | 110 | a rede agenda em 1,3 meses o que está na fila; saldo de 15/mês sobre 80 de oferta |
| 02.04.06.010-9 | Calcaneo esquerdo (perfil e axial) | 80 | 80 | a rede agenda em 1,1 meses o que está na fila; saldo de 14/mês sobre 66 de oferta |
| 02.04.06.009-5 | Bacia (ap e frog) | 77 | 77 | a rede agenda em 1,0 mês o que está na fila; saldo de 10/mês sobre 78 de oferta |
| 02.04.04.011-6 | Ombro direito (ap verdadeiro, perfil de escapular e axilar) | 61 | 61 | a rede agenda em 0,5 mês o que está na fila; saldo de 15/mês sobre 117 de oferta |
| 02.04.06.006-0 | Articulacao coxo-femoral direito | 48 | 48 | a rede agenda em 0,8 mês o que está na fila; saldo de 6/mês sobre 52 de oferta |
| 02.04.06.008-7 | Articulacao tibio-tarsica esquerdo (ap verdadeiro e perfil) | 44 | 44 | a rede agenda em 0,8 mês o que está na fila; saldo de 11/mês sobre 41 de oferta |
| 02.04.02.007-7 | Coluna lombo sacra com obliquas (ap e perfil) | 42 | 42 | a rede agenda em 2,3 meses o que está na fila; saldo de 7/mês sobre 15 de oferta |
| 02.04.06.016-8 | Perna direita (ap e perfil) | 41 | 41 | a oferta recente (55/mês) passou a procura (56/mês) |
| 02.04.04.007-8 | Cotovelo direito (ap e perfil) | 35 | 35 | a rede agenda em 1,1 meses o que está na fila; saldo de 7/mês sobre 29 de oferta |
| 02.04.02.010-7 | Coluna dorso - lombar para escoliose (ap e perfil) | 29 | 29 | a fila cai: entram 39 e a rede agenda 38 por mês |
| 02.04.04.005-1 | Braco direito (ap e perfil) | 26 | 26 | a rede agenda em 1,2 meses o que está na fila; saldo de 3/mês sobre 20 de oferta |
| 02.04.01.014-4 | Seios da face - f.n.+m.n | 25 | 25 | a fila cai: entram 88 e a rede agenda 90 por mês |
| 02.04.06.017-6 | Panoramica de membros inferiores | 14 | 14 | a rede agenda em 18,7 meses o que está na fila; saldo de 2/mês sobre 0 de oferta |
| 02.05.02.017-8 | Ultrassonografia transfontanela | 282 | 255 | a oferta recente (76/mês) passou a procura (74/mês) |
| 02.05.02.002-0 | Paquimetria ultrassonica | 134 | 134 | a fila cai: entram 151 e a rede agenda 170 por mês |
| 02.06.01.007-9 | Tomografia computadorizada do crânio | 1.403 | 1.375 | a fila cai: entram 1.141 e a rede agenda 1.276 por mês |
| 02.06.01.005-2 | Tomografia computadorizada do pescoco | 739 | 733 | a fila cai: entram 201 e a rede agenda 201 por mês |
| 02.06.01.004-4 | Tomografia computadorizada de face / seios da face / articulacoes temp | 394 | 392 | a fila cai: entram 430 e a rede agenda 447 por mês |
| 02.06.03.002-9 | Tomografia computadorizada de articulacoes de membro inferior | 200 | 198 | a fila cai: entram 126 e a rede agenda 142 por mês |
| 02.06.01.002-8 | Tomografia computadorizada de coluna lombo- sacra c/ ou s/ contraste | 145 | 138 | a fila cai: entram 235 e a rede agenda 270 por mês |
| 02.06.01.001-0 | Tomografia computadorizada de coluna cervical c/ ou s/ contraste | 128 | 125 | a fila cai: entram 114 e a rede agenda 124 por mês |
| 02.06.02.002-3 | Tomografia computadorizada de segmentos apendiculares (braço, antebraç | 90 | 90 | a fila cai: entram 183 e a rede agenda 194 por mês |
| 02.06.01.003-6 | Tomografia computadorizada de coluna toracica c/ ou s/ contraste | 57 | 56 | a fila cai: entram 86 e a rede agenda 91 por mês |
| 02.06.02.001-5 | Tomografia computadorizada de articulacoes de membro superior | 38 | 36 | a fila cai: entram 79 e a rede agenda 85 por mês |
| 02.06.01.006-0 | Tomografia computadorizada de sela turcica | 27 | 27 | a fila cai: entram 31 e a rede agenda 35 por mês |
| 02.07.03.003-0 | Ressonancia magnetica de membro inferior (unilateral) | 1.694 | 1.693 | a fila cai: entram 1.208 e a rede agenda 1.537 por mês |
| 02.07.01.004-8 | Ressonancia magnetica de coluna lombo-sacra | 1.570 | 1.568 | a fila cai: entram 1.316 e a rede agenda 1.744 por mês |
| 02.07.03.002-2 | Ressonancia magnetica de bacia / pelve / abdomen inferior | 1.423 | 1.423 | a fila cai: entram 1.511 e a rede agenda 1.693 por mês |
| 02.07.01.006-4 | Ressonancia magnetica de cranio | 1.333 | 1.333 | a fila cai: entram 1.318 e a rede agenda 1.559 por mês |
| 02.07.02.002-7 | Ressonancia magnetica de membro superior (unilateral) | 1.209 | 1.208 | a fila cai: entram 849 e a rede agenda 1.055 por mês |
| 02.07.01.003-0 | Ressonancia magnetica de coluna cervical/pescoço | 750 | 749 | a fila cai: entram 664 e a rede agenda 820 por mês |
| 02.07.03.001-4 | Ressonancia magnetica de abdomen superior | 522 | 522 | a fila cai: entram 862 e a rede agenda 900 por mês |
| 02.07.01.005-6 | Ressonancia magnetica de coluna toracica | 286 | 286 | a fila cai: entram 319 e a rede agenda 377 por mês |
| 02.07.02.001-9 | Ressonancia magnetica de coracao / aorta c/ cine | 246 | 246 | a fila cai: entram 103 e a rede agenda 161 por mês |
| 02.07.01.002-1 | Ressonancia magnetica de articulacao temporo- mandibular (bilateral) | 123 | 123 | a fila cai: entram 119 e a rede agenda 153 por mês |
| 02.07.01.007-2 | Ressonancia magnetica de sela turcica | 121 | 121 | a fila cai: entram 108 e a rede agenda 145 por mês |
| 02.07.01.001-3 | Angioressonancia cerebral | 115 | 115 | a fila cai: entram 164 e a rede agenda 232 por mês |
| 02.07.03.004-9 | Ressonancia magnetica de vias biliares / colangioressonância | 109 | 109 | a fila cai: entram 271 e a rede agenda 274 por mês |
| 02.07.02.003-5 | Ressonancia magnetica de torax | 74 | 74 | a fila cai: entram 85 e a rede agenda 91 por mês |
| 02.07.02.006-0 | Ressonância magnética da mama | 12 | 12 | a rede agenda em 0,1 mês o que está na fila; saldo de 22/mês sobre 140 de oferta |
| 20406015 | Radiografia de pe/dedos do pe | 11 | 11 | a fila cai: entram 99 e a rede agenda 104 por mês |

- **A ressonância.** A oferta dobrou em 2026 (a RM de membro inferior foi de 8.139 para 18.442
  agendamentos em 12 meses), e a fila cai em todos os códigos.
- **As TC da carteira antiga** (crânio, pescoço, face e sela). A fila cai ou está em equilíbrio.
  - O código mistura pedido eletivo com angiotomografia, emergência e cone beam odontológica
    (estudo de 26/10). A emergência é de pronto-atendimento, quase toda da Região Sudoeste, e
    convênio ambulatorial não a atende.
  - As TC de coluna e de segmentos tinham saído em 20/10 pela OCI 003-8 do IEV. Também caem.
- **As radiografias.** A rede esvazia cada fila em poucos meses.
- **A US transfontanela.** Entra o mesmo que a rede agenda.

### 6.5 Outro objeto: odontologia

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.04.01.017-9 | Radiografia periapical de 6 a 13 incidências | 3 | 4.214 | 3.027 | **1.187** | 1.183 | 123 | 1.364 | 1.353 | 1.618 | -254 | 0,1 | 46% | não |
| 02.04.01.018-7 | Radiologia periapical - até 5 incidências | 1 | 1.333 | 635 | **698** | 698 | 24 | 588 | 699 | 634 | -46 | 0,1 | 56% | não |

São radiografias de dente: o objeto é saúde bucal, não exame de imagem médica. A cone beam da
TC de face (191 pedidos em 26/10) é o mesmo caso.

### 6.6 Maior complexidade: medicina nuclear e PET-CT

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.08.01.002-5 | Cintilografia de miocardio p/ avaliacao da perfusao em situacao de est | 1 | 1.881 | 149 | **1.732** | 1.732 | 290 | 106 | 31 | 40 | +66 | 4,6 | 44% | sim, R$ 898,74 |
| 02.08.05.003-5 | Cintilografia de ossos com ou sem fluxo sanguíneo (corpo inteiro) | 1 | 1.604 | 29 | **1.575** | 1.575 | 146 | 207 | 124 | 218 | -11 | 1,1 | 46% | sim, R$ 763,96 |
| 02.08.01.003-3 | Cintilografia de miocardio p/ avaliacao da perfusao em situacao de rep | 1 | 1.526 | 34 | **1.492** | 1.492 | 287 | 84 | 30 | 39 | +45 | 4,2 | 42% | sim, R$ 881,06 |
| 02.06.01.009-5 | Tomografia por emissão de pósitrons (pet-ct) | 1 | 1.229 | 851 | **378** | 378 | 185 | 94 | 48 | 44 | +50 | 0,7 | 45% | não |
| 02.08.04.010-2 | Cintilografia renal dinamica (dtpa) | 1 | 236 | 4 | **232** | 232 | 154 | 26 | 12 | 13 | +13 | 1,6 | 51% | não |
| 02.08.04.005-6 | Cintilografia renal/renograma (qualitativa e/ou quantitativa) | 1 | 190 | 15 | **175** | 175 | 101 | 34 | 31 | 27 | +7 | 0,5 | 46% | sim, R$ 532,12 |
| 02.08.03.001-8 | Cintilografia de paratireoides | 1 | 161 | 10 | **151** | 151 | 146 | 20 | 18 | 14 | +6 | 0,7 | 49% | sim, R$ 973,62 |
| 02.08.02.003-9 | Cintilografia de glandulas salivares c/ ou s/ estímulo | 1 | 61 | 3 | **58** | 58 | 66 | 12 | 5 | 10 | +3 | 0,9 | 59% | sim, R$ 351,56 |
| 02.08.01.004-1 | Cintilografia de miocardio p/ localizacao de necrose (minimo 3 projeço | 1 | 52 | 2 | **50** | 50 | 176 | 5 | 1 | 0 | +5 | 3,9 | 73% | sim, R$ 665,88 |
| 02.08.02.007-1 | Cintilografia p/ estudo de transito gastrico | 2 | 35 | 1 | **34** | 34 | 142 | 4 | 2 | 1 | +3 | 1,8 | 44% | sim, R$ 576,88 |
| 02.08.03.002-6 | Cintilografia de tireóide com ou sem captação | 1 | 30 | 4 | **26** | 26 | 17 | 29 | 37 | 48 | -19 | 0,1 | 40% | sim, R$ 154,56 |
| 02.08.03.004-2 | Cintilografia p/ pesquisa do corpo inteiro | 1 | 27 | 2 | **25** | 25 | 11 | 11 | 10 | 16 | -5 | 0,2 | 31% | sim, R$ 677,40 |
| 02.08.08.004-0 | Linfocintilografia | 1 | 24 | 2 | **22** | 22 | 127 | 3 | 3 | 4 | -1 | 0,6 | 51% | sim, R$ 565,32 |
| 02.08.05.004-3 | Cintilografia de segmento osseo c/ galio 67 | 1 | 16 | 0 | **16** | 16 | 19 | 1 | 1 | 1 | 0 | 1,2 | 57% | sim, R$ 915,10 |
| 02.08.07.004-4 | Cintilografia de pulmao por perfusao (minimo 4 projecoes) | 1 | 49 | 35 | **14** | 14 | 42 | 5 | 12 | 7 | -3 | 0,1 | 61% | sim, R$ 522,00 |

Você tirou a medicina nuclear em 16/10. Ela exige licença da CNEN, rejeito radioativo,
radiofármaco do IPEN e vigilância sanitária própria. A cintilografia renal dinâmica e o PET-CT
estão fora do rol da 4.282 e pagariam só a tabela. **Mesmo assim, aqui está o maior déficit
de imagem do DF** (seção 7).

### 6.7 Filas mínimas

| código | exame | filas | total | devolvidas | **fila** | fila viva | espera média (dias) | entram/mês | rede agenda/mês (12 m) | rede, 3 últimos meses | saldo recente/mês | estoque (anos) | falta | no rol da 4.282 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.05.01.005-9 | Ultrassonografia doppler de fluxo obstetrico | 1 | 50 | 34 | **16** | 16 | 96 | 2 | 1 | 0 | +2 | 0,9 | 60% | sim, R$ 99,95 |
| 02.05.02.013-5 | Ultrassonografia de torax (extracardiaca) | 1 | 25 | 12 | **13** | 6 | 676 | 1 | 0 | 0 | +1 | sem oferta | — | sim, R$ 99,94 |

O doppler de fluxo obstétrico e a US de tórax caberiam no mesmo aparelho de ultrassom, mas a
procura é de 1 a 2 pedidos por mês. **Ficam fora da carteira ampla, por decisão sua (27/10).** A US
transfontanela também saiu: a rede agenda o que entra (seção 6.4).

## 7. O que mais daria para fazer, porque tem fila

Fora da carteira, estas filas têm demanda que a rede não atende. Servem para esta emenda, se a
carteira mudar, ou para as próximas:

| o quê | fila | por que tem espaço | o que pesa contra |
|---|---|---|---|
| **cintilografia de miocárdio** (02.08.01.002-5 e 003-3) | 3.224 | a rede faz 1 de cada 3 pedidos novos; 4 a 5 anos de estoque; é a OCI 09.02.01.005-0, que ninguém contratou | CNEN, radiofármaco, falta de 42% a 44%; maior complexidade |
| **cintilografia óssea** (02.08.05.003-5) | 1.575 | a procura dobrou em um ano (de 107 para 207 por mês) | a oferta subiu junto nos últimos meses; CNEN |
| **PET-CT** (02.06.01.009-5) | 378 | a oferta caiu à metade (de 126 para 48 por mês) | fora do rol da 4.282 (só a tabela); alto custo; 851 devolvidas |
| **US doppler de vasos** (02.05.01.004-0) | 16.757 | a maior fila de imagem; cresce uns 260 a 300 por mês; 1,3 ano de estoque | código do plano 4 |
| **US de abdômen total** (02.05.02.004-6) | 13.877 | cresce uns 266 por mês (12 meses); 1,3 ano | código do plano 4; a oferta recente alcançou a procura |
| **US de tireoide** (02.05.02.012-7) | 3.863 | cresce uns 100 por mês | código do plano 4 |
| **eco transtorácico** (02.05.01.003-2) | 14.551 | fila grande, 16.446 devolvidas | OCI da cardiologia; a fila caiu 1.577 em onze dias de outubro, e o saldo recente é quase zero |
| **US de articulação no CID do IEV** | 879 | fila parada também | é a OCI do IEV |
| **doppler de fluxo obstétrico e US de tórax** | 29 | cabem no aparelho da carteira | filas mínimas |

## 8. A falta em toda a imagem

| modalidade | falta nos códigos com fila |
|---|---|
| radiologia | 14% a 27% nas radiografias; mamografia, 33%; periapical, 46% a 56%; panorâmica de membros inferiores, 71% (14 na fila) |
| ressonância | 19% a 30% (RM de coração, 42%) |
| tomografia | 25% a 36% |
| ultrassom | 24% a 48% (globo ocular, 48%; obstétricas, 42% a 43%); doppler de fluxo obstétrico, 60% (16 na fila) |
| medicina nuclear | 31% a 73% |

**Nos ultrassons da carteira, 1 em cada 3 agendados falta, ou mais.** Por isso a conta usa a
falta, e as vagas a agendar passam de 20 mil para 13.532 exames realizados. A falta depende de a
unidade executora registrar o realizado e a falta no SISREG.

## 9. O que falta

- **Decidir a carteira ampla:** se as TC e as cintilografias, hoje sem prioridade, ficam na lista,
  e a ordem sugerida.
- **A versão nova do PT com a carteira ampla:**
  - a lista de códigos;
  - a frase de que a quantidade de cada um se pactua com a SES conforme a fila;
  - a frase "mais da metade da fila" refeita.
- **Pedir à SES o relatório de execução dos convênios do IEV** (030975 e 030977): quantas OCI 002-0
  foram feitas e com que CID (seção 5.5).
- **Confirmar com a SES e a regulação** que o ortopédico da fila de US de articulação vai ao IEV,
  e medir a divisão exata pelo CID (seção 5.6).
- **Medir as pessoas nas duas portas:** a fila de US de articulação contra a consulta de ortopedia
  no IEV (seção 5.4).
- **O preço de mercado** da densitometria e da US obstétrica (agente `precos`).
- **Confirmar com o ISHP:** se faz a US de globo ocular no aparelho geral, e se tem radiologista para
  as US que só ele pode laudar.
- **A SES-01:** a habilitação 38.01 (Portaria 4.694) só vai até 31/12/2026. Perguntar se o valor
  com incremento vale num convênio que comece em 2027.
- **Juntar ao main** o kit novo do Mapa Social (oferta, situação, rumo por código), hoje sem
  commit no ramo `melhorias/mapa-social`.
