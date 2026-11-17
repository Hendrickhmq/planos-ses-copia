# Estudo — o R$ 1,5 milhão de imagem pelo aparelho

**Controle interno.** Estudo de 27/10/2026 para o redacao_07: Emenda de Bancada do DF 71080005,
R$ 1.502.687,00, federal, proponente ISHP. Segue o estudo de 26/10
(`estudo_imagem_1_5_milhao_20261026.md`) com o critério que você deu hoje:
- o receio de absenteísmo grande;
- o maior número de exames que dividem o mesmo aparelho, para não gerar custo a mais e atender
  mais gente;
- de preferência os de menor complexidade, e os de maior só se for preciso.

Nada disso vai para o PT. O absenteísmo é tratamento interno (decisão sua, 21/10).

**As fontes:**
- **a fila:** a coleta do agente `mapa-social` de 26/10/2026, recarga das 16:32
  (`planos/redacao_07/dados/fontes/mapa_social_20261026.md`, na sua pasta, conferência 8/8);
- **a US de articulação fora do CID da OCI do IEV:** `mapeamento_iev_20261026.md`, seção 4;
- **os valores:** `planos/redacao_07/dados/valor_unitario.md`, a tabela mais o incremento do
  Anexo I da Portaria SAES/MS 4.282/2026, como no PT v1;
- **quem pode fazer cada exame (CBO):** as fichas do SIGTAP de 10/2026 em
  `planos/redacao_07/dados/fontes/`.

**A base da conta é R$ 1.352.418,30 para exames:** o recurso menos os 10% de apoio do PT v1.

## 1. O que é atendimento válido

Cada pedido no SISREG está numa de três situações:

| situação | o que é | entra na conta? |
|---|---|---|
| **devolvido** | o regulador devolveu ao médico que pediu, para completar (falta dado, CID ou justificativa) | **não**: não está apto a agendar. Pode voltar corrigido |
| **fila válida** | pendente de regulação, corrigido e reenviado, ou pendente por fila de espera | **sim** |
| **fila viva** | a fila válida só com os pedidos dos últimos 24 meses (de 26/10/2024 em diante) | sim. É a parte com menos risco de a pessoa já ter feito o exame em outro lugar ou não ser mais achada |

**A fila do estudo de 26/10 já desconta as devolvidas.** Abaixo elas aparecem à parte, para
mostrar o tamanho do desconto, e a conta vai de duas formas: pela fila válida e pela fila viva.

## 2. Exame a exame

"Pendentes" é a fila válida mais as devolvidas (**calculado**). "Estoque" é a fila válida
dividida pelas agendadas em 12 meses, em anos: abaixo de 0,5, a rede já dá conta.

### 2.1 Ultrassom: um aparelho só

| exame | pendentes | devolvidos | % devolvido | **fila válida** | **fila viva** | espera média (dias) | agendadas em 12 m | estoque (anos) | valor | zerar a válida | zerar a viva |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US pélvica | 1.949 | 924 | 47% | **1.025** | **708** | 606 | 1.360 | 0,8 | R$ 99,94 | R$ 102.438,50 | R$ 70.757,52 |
| US de bolsa escrotal | 1.474 | 507 | 34% | **967** | **623** | 571 | 916 | 1,1 | R$ 99,94 | R$ 96.641,98 | R$ 62.262,62 |
| US de globo ocular | 1.506 | 198 | 13% | **1.308** | **1.308** | 267 | 598 | 2,2 | R$ 99,94 | R$ 130.721,52 | R$ 130.721,52 |
| US transfontanela | 493 | 202 | 41% | **291** | **262** | 292 | 826 | 0,4 | R$ 99,94 | R$ 29.082,54 | R$ 26.184,28 |
| US obstétrica | 1.424 | 937 | 66% | **487** | **485** | 145 | 2.957 | 0,2 | R$ 99,94 | R$ 48.670,78 | R$ 48.470,90 |
| US obstétrica com doppler | 316 | 147 | 47% | **169** | **169** | 196 | 376 | 0,4 | R$ 100,18 | R$ 16.930,42 | R$ 16.930,42 |
| US de próstata transretal | 155 | 133 | 86% | **22** | **22** | 120 | 5 | 4,4 | R$ 99,94 | R$ 2.198,68 | R$ 2.198,68 |
| US de tórax | 30 | 13 | 43% | **17** | **8** | 704 | 0 | sem oferta | R$ 99,94 | R$ 1.698,98 | R$ 799,52 |
| Doppler de fluxo obstétrico | 49 | 34 | 69% | **15** | **15** | 102 | 16 | 0,9 | R$ 99,95 | R$ 1.499,25 | R$ 1.499,25 |
| **subtotal, nove exames** | 7.396 | 3.095 | 42% | **4.301** | **3.600** | | | | | **R$ 429.882,65** | **R$ 359.824,71** |
| US de articulação, código inteiro | 19.584 | 5.193 | 27% | 14.391 | 10.396 | 547 | 8.039 | 1,8 | R$ 99,94 | | |
| **· fora do CID da OCI 002-0 do IEV** | | | | **13.512** | **≈ 9.761** | | | | R$ 99,94 | R$ 1.350.389,28 | **≈ R$ 975.514,34** |

- **A fila viva da US de articulação fora do CID do IEV é estimativa** (**calculado**): os 13.512
  na mesma proporção viva/válida do código inteiro (10.396 de 14.391). A coleta de 26/10 não
  mediu os 879 pedidos no CID da OCI separados pelo ano. Medir isso é uma ordem de coleta
  simples para o agente.
- **A US de articulação** junta articulações (9.952), partes moles (3.117), região inguinal
  (606), pescoço (278) e outras regiões (438), todas pelo código inteiro. Partes moles tem 40%
  de pedido de antes de 26/10/2024.
- **A US de próstata transretal e a de tórax** são filas pequenas que a rede quase não atende
  (5 e 0 agendadas em 12 meses).

### 2.2 Os outros aparelhos

| exame | aparelho | pendentes | devolvidos | % devolvido | **fila válida** | **fila viva** | espera média | agendadas em 12 m | estoque | valor | zerar a válida |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC de crânio | tomógrafo | 4.211 | 2.758 | 65% | **1.453** | **1.425** | 206 | 14.949 | 0,1 | R$ 300,11 | R$ 436.059,83 |
| TC de pescoço | tomógrafo | 1.441 | 662 | 46% | **779** | **773** | 139 | 2.432 | 0,3 | R$ 300,15 | R$ 233.816,85 |
| TC de face, seios e ATM | tomógrafo | 1.351 | 881 | 65% | **470** | **468** | 138 | 5.406 | 0,1 | R$ 300,15 | R$ 141.070,50 |
| TC de sela túrcica | tomógrafo | 213 | 165 | 77% | **48** | **48** | 169 | 419 | 0,1 | R$ 300,11 | R$ 14.405,28 |
| Mamografia de rastreamento | mamógrafo | 9.596 | 2.679 | 28% | **6.917** | **6.832** | 66 | 55.649 | 0,1 | R$ 99,90 | R$ 691.008,30 |
| Densitometria | densitômetro | 5.860 | 3.672 | 63% | **2.188** | **2.185** | 46 | 12.827 | 0,2 | R$ 220,40 | R$ 482.235,20 |

- **Nas TC, a fila válida ainda mistura três tipos de pedido** (estudo de 26/10): eletiva,
  angiotomografia e emergência. Só a eletiva, sem a cone beam odontológica, dá **1.189 exames,
  por R$ 356.859,19**: crânio 452, pescoço 503, face 207 e sela 27. As devolvidas não foram
  medidas por tipo.
- **Os quatro aparelhos da tabela têm estoque de 0,1 a 0,3 ano.** A rede já marca por ano de 3
  a 10 vezes a fila.

## 3. O aparelho e quem opera

| aparelho | exames | o que precisa | quem pode laudar (CBO da ficha) | complexidade |
|---|---|---|---|---|
| **ultrassom com doppler colorido**: convexo, linear de alta frequência, endocavitário e microconvexo | os nove do 2.1 e a US de articulação | um aparelho, quatro transdutores, um médico. Sem radiação, sem contraste, sem preparo na maioria, de 15 a 20 minutos | radiologista em todos. Também: ginecologista e obstetra, clínico e médico de família (pélvica e obstétricas); urologista (bolsa escrotal); oftalmologista (globo ocular). **Transfontanela: só radiologista** | a menor |
| tomógrafo | as quatro TC | sala blindada, técnico em radiologia, contraste. Bomba injetora para a angiotomografia | radiologista | maior |
| mamógrafo | mamografia | sala blindada, técnica em mamografia, controle de qualidade do INCA | radiologista | média |
| densitômetro | densitometria | aparelho próprio | radiologista e outros | média |

**Dois cuidados no ultrassom:**
- **Globo ocular.** A ficha aceita oftalmologista e radiologista, e o exame se faz no aparelho
  geral, com transdutor linear de alta frequência e ajuste oftálmico. Muita clínica usa um
  ecógrafo oftálmico próprio. Confirmar com o ISHP. Se ele não fizer no aparelho geral, este é
  o único exame do bloco que pede outro aparelho.
- **Transfontanela.** É exame de recém-nascido e lactente, até a fontanela fechar, e só
  radiologista lauda. Pede transdutor microconvexo e alguém acostumado a examinar bebê.

## 4. Por que o aparelho único ajuda contra a falta

O convênio paga o exame feito. **A falta não custa dinheiro à SES: custa hora de aparelho
parada ao ISHP**, e esse é o seu receio.
- **Com um aparelho e dez filas**, a vaga de quem falta vai para o próximo de qualquer uma delas.
  A US de articulação, com uns 9.761 pedidos vivos, é o fundo que não acaba em 12 meses.
- **Com tomógrafo, mamógrafo e densitômetro**, cada um depende só da própria fila. Elas são
  curtas: a rede já esvazia cada uma em 1 a 4 meses. Com falta alta, o aparelho fica parado
  ou disputa paciente com a rede.
- **A fila velha falta mais.** Pedido de antes de 26/10/2024 é de quem pode já ter feito o
  exame, mudado de telefone ou desistido. Por isso a conta pela fila viva é a mais segura.

**A falta medida até hoje** é de consulta, não de exame de imagem, e vem da coleta do IEV de
26/10 (`mapa_social_20261026_iev.md`, seção 2.3), entre os agendamentos com desfecho:

| | realizadas | faltas | falta (calculado) |
|---|---|---|---|
| consultas de ortopedia no IEV | 13.818 | 11.112 | 45% |
| consulta de risco cirúrgico no IEV | 990 | 499 | 34% |
| consulta de cardiologia adulto no IEV | 300 | 314 | 51% |

O painel tem a situação de cada agendamento (realizado, falta do paciente, cancelado), o campo
`status_solicitacao_agendamento_alias`. **O kit de coleta ainda não mede esse campo por exame:
é preciso acrescentá-lo** para saber a falta da US pélvica, da articulação etc.

## 5. Os cenários

| cenário | aparelhos | o que entra | exames | custo | sobra |
|---|---|---|---|---|---|
| **1. Só ultrassom, pela fila viva** | 1 | os nove de US (3.600) + US de articulação fora do CID do IEV (≈ 9.761) | **≈ 13.361** | ≈ R$ 1.335.339,05 | ≈ R$ 17.079,25 |
| **2. Só ultrassom, pela fila válida** | 1 | os nove de US (4.301) + 9.230 US de articulação, 68% dos 13.512 | **13.531** | R$ 1.352.328,85 | R$ 89,45 |
| 3. Ultrassom e TC eletiva, pela fila viva | 2 | os nove de US (3.600) + TC eletiva (1.189) + 6.361 US de articulação | 11.150 | R$ 1.352.402,24 | R$ 16,06 |
| 4. A recomendação de 26/10 | 4 | os dez de espera longa (eletiva e angiotomografia) + 4.040 mamografias | 10.034 | R$ 1.352.418,30 | — |

**O que os números dizem:**
- **Só ultrassom atende mais gente:** uns 13.400 exames contra 10.034, cerca de 3.300 a mais,
  com um aparelho em vez de quatro.
- **Pela fila viva, o dinheiro zera toda a fila viva de ultrassom fora do plano 4 e do IEV.**
  Sobram uns R$ 17 mil, que vão para a fila velha ou para quem entrar nos 12 meses.
- **A TC entra só se for preciso.** O cenário 3 troca 3.400 US de articulação por 1.189
  tomografias, e faz 2.211 exames a menos que o 1. As tomografias são de uma fila que a rede esvazia em cerca de um mês.

## 6. O que muda no PT, se for por ultrassom

- **Saem** as quatro TC, a mamografia e a densitometria.
- **Entram** a US de articulação (02.05.02.006-2), a US de próstata transretal (02.05.02.011-9),
  a US de tórax (02.05.02.013-5) e o doppler de fluxo obstétrico (02.05.01.005-9). Os quatro
  estão no Anexo I da 4.282, com R$ 99,94 e R$ 99,95.
- **Uma decisão sua volta:** a US de articulação saiu em 15/10, e partes moles em 16/10. O
  motivo de 20/10 (a OCI do IEV) não se sustenta (`mapeamento_iev_20261026.md`, seção 4).
  Para não deixar dúvida, ficam fora os 879 pedidos no CID da OCI 002-0.
- **Nenhum código do plano 4 entra** (US mamária, transvaginal, doppler de vasos, abdômen total
  e superior, aparelho urinário, tireoide e próstata abdominal).
- **Vem antes do documento:** as fichas do SIGTAP de três dos códigos novos (próstata transretal,
  tórax e doppler de fluxo obstétrico; a da articulação já existe), o preço do
  mercado dos que não têm, e a revisão cega da versão nova.

## 7. O que falta

- **A falta por exame** no painel: acrescentar a situação do agendamento ao kit e medir os
  nove de US e a articulação em 12 meses.
- **A fila viva da US de articulação fora do CID do IEV**, medida e não estimada (ordem de
  coleta com o recorte de CID).
- **O ISHP:** se faz o globo ocular no aparelho geral, e se tem radiologista para a
  transfontanela.
- **A SES-01:** a habilitação 38.01 (Portaria 4.694) só vai até 31/12/2026. Perguntar se o
  valor com incremento vale num convênio que comece em 2027.
