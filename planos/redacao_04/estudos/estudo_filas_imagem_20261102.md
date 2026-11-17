# Estudo das filas de imagem para o plano 4 — a carteira 1 e o que ela exige

**Controle interno, 02/11/2026.** Nada daqui foi aplicado ao plano de trabalho, ao `estado.yaml` nem a outro plano.
Também não foi enviado a parceiros. A nova versão do plano vem depois.

**Os arquivos, nesta pasta:**
- **a planilha para ler e mostrar:** `estudo_filas_imagem_20261102_organizada.xlsx`. Começa pelo Resumo, com as
  respostas, e pelo Enquadramento (siglas, decisões, premissas, tempos, o que confirmar com a SES, metas e
  proteções). Depois vêm Capacidade por polo, Pedidos novos, Encaminhamento SES, Faltas e pedidos, Metas pela falta da SES
  (vagas a agendar por exame e por fila, com a falta de cada código na SES), Filas do plano,
  IEV, Origem regional, Painel, Carteiras por código, Quem atende o quê, Rumo das filas, Filas, Viabilidade (só a
  carteira 1), Quem oferta (só os 17 códigos) e Fontes;
- **a planilha completa:** `estudo_filas_imagem_20261102.xlsx`, com as mesmas contas em colunas cruas;
- **os scripts:**
  - `estudo_filas_imagem_20261102.py` faz as contas;
  - `formatar_estudo_filas_imagem_20261102.py` monta a planilha organizada, sem refazer conta;
- **a versão da manhã, para comparar:** `anterior_20261102_manha/`;
- **o estudo dos outros planos:** `estudo_outros_planos_imagem_20261102.md`.

```bash
git show main:biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv > /tmp/candanga.csv
python3 planos/redacao_04/estudos/estudo_filas_imagem_20261102.py planos/redacao_04/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json /tmp/candanga.csv planos/redacao_04/dados/fontes/mapa_social_20261102_executante_c_bruto/coleta_20261102.json
python3 planos/redacao_04/estudos/formatar_estudo_filas_imagem_20261102.py
```

## 1. Siglas e códigos

| sigla | o que é |
|---|---|
| L-006 | pendência do parque instalado: as salas e os tomógrafos das clínicas ainda não foram confirmados |
| L-007 | pendência da parede abdominal: a SES confirmar, por escrito, que a fila "Ultrassonografia de parede abdominal" é feita e faturada no código do abdômen total (02.05.02.004-6) |
| L-008 | regra "um pedido, um plano": nenhum pedido entra no plano 4 e num convênio do IEV ao mesmo tempo. Revista em 02/11: a US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas ao IEV |
| D-009 | decisão de atender só ambulatório: nenhuma fila de emergência entra |
| LI-002 | regra de preço: vale a Candanga, ou o SIGTAP quando for igual ou maior |
| Candanga | Tabela SUS Candanga: o preço que o DF paga por procedimento |
| IEV | o proponente dos convênios 030975, 030976 e 030977 com a SES, com OCI de ortopedia, ginecologia e outras |
| OCI | Oferta de Cuidados Integrados: pacote do SUS com consulta, exames e retorno, pago de uma vez |
| GIN1 | a OCI de ginecologia (09.06.01.001-2) que o IEV executa; a transvaginal é exame obrigatório dela |
| URD | Unidade de Referência Distrital: serviço de referência do DF inteiro, sem Região de Saúde |
| CBR | Colégio Brasileiro de Radiologia, de onde vêm os tempos de ultrassom (2017) |
| filas do plano | as filas que a carteira 1 atende: sem emergência, angio coronária, sedação, reservas do IEV e filas com menos de 30 pedidos |

## 2. As respostas

**As 20 salas de ultrassom dão conta? Sim, se as faltas forem repostas.**
- **A conta:** com 8 meses de produção e todas as faltas repostas por encaixe, a rede fica em 89%.
- **A folga:** ela aguenta até 11% de faltas sem reposição (10,6%).
- **Sem reposição:** com 10% das faltas sem reposição, fica em 99%, e a Sudoeste e a Sul passam de 100%. Com 20%,
  fica em 112%.

**Como ficam as salas por polo:**

| polo | exames de ultrassom | horas de exame | **salas** | uso, faltas repostas | uso, 10% sem reposição | uso, 20% sem reposição | vagas por dia útil |
|---|---:|---:|---:|---:|---:|---:|---:|
| Oeste | 3.297 | 1.059 | **1** | 79% | 88% | 99% | 25 |
| Sudoeste | 21.873 | 7.712 | **6** | 96% | 106% | 120% | 163 |
| Norte | 5.269 | 3.052 | **3** | 76% | 84% | 95% | 40 |
| Leste | 8.274 | 2.405 | **2** | 89% | 99% | 112% | 62 |
| Central e Centro-Sul | 10.857 | 3.481 | **3** | 86% | 96% | 108% | 81 |
| Sul | 15.562 | 6.327 | **5** | 94% | 105% | 118% | 116 |
| **total** | **65.132** | **24.036** | **20** | **89%** | **99%** | **112%** | **487** |

- **Como as salas foram repartidas:** pelo menos uma por polo, e cada sala a mais vai ao polo mais carregado.
- **O Norte pesa mais do que os exames sugerem.** O Doppler bilateral de membros, de 40 minutos, vem quase todo do
  Norte, da Sul e da Sudoeste. Sozinho, ele ocupa um terço das horas de ultrassom (8.230 de 24.036).
- **Se nenhuma falta for reposta (20%),** bastariam 25 salas.

**Os 5 tomógrafos dão conta? Sim.**
- **O uso:** 71% com as faltas repostas e 89% com 20% sem reposição.
- **Os polos:** a Leste é atendida na Central e Centro-Sul. A Sudoeste pede 1,4 tomógrafo e manda o excedente à Oeste.

**Que encaminhamento da SES sustenta as metas?** A regulação manda ao projeto, exame a exame, a parte que falta. A
SES reduz a própria agenda na mesma medida, sem suspender nada.
- **Quanto:** de 1.762 a 15.529 agendamentos em 8 meses. No pior caso, são 17% da agenda que a SES faz hoje nas filas
  do plano.
- **O ganho:** a rede faz 70.779 exames a mais, já descontado o que a SES deixa de fazer.
- **Sem esse encaminhamento,** falta pedido em 8 dos 16 exames, mesmo com toda falta reagendada.

## 3. Decisões já tomadas

- **Carteira:** a carteira 1 é a base.
  - São 79.533 exames e R$ 10.636.498,75 de procedimentos pela Candanga.
  - São 65.132 exames de ultrassom e 14.401 de TC, em 16 códigos.
  - **Sem a transfontanela (usuário, 03/11/2026).** Os 293 exames dela (R$ 78.737,89) saíram, e o valor se espalhou
    pelos exames que ainda têm folga sob a falta da SES, na proporção da meta: Doppler +302, tireoide +125, próstata
    +83, TC de abdômen +39, TC de pelve +27, TC de tórax +21, TC de crânio +6 e TC de pescoço +4. São 607 exames
    numa linha de encaminhados pela SES, porque passam da fila de hoje.
  - As carteiras 2 a 5 saem iguais às da manhã de 02/11, item por item.
- **Foco:** ultrassom e TC ambulatoriais. Emergência, radiologia, ressonância e medicina nuclear ficam fora.
- **Equipamentos:** 20 salas de ultrassom e 5 tomógrafos.
- **Prazo:** 8 meses de produção.
- **Angio coronária: não entra.**
  - Ela usa o código da TC de tórax e paga o mesmo, R$ 309,25 pela Candanga.
  - Ocupa o tomógrafo por mais tempo: 30 minutos, contra 20.
  - Só em último caso, para compor valor.
- **Parede abdominal:** é essencial para a proposta e fica na carteira, com 3.304 exames e R$ 388.253,04. A SES ainda
  precisa confirmar (L-007).
- **Custos:** a revisão de custos e a cotação dos médicos ficam para outra etapa.
- **IEV:** a US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas à GIN1 (L-008, seção 10).
- **Filas pequenas:** fila com menos de 30 pedidos não vira item próprio da carteira.

## 4. Premissas de planejamento

**A jornada da sala:**
- Cada sala ou tomógrafo funciona **10 horas por dia útil**.
- **8 horas são de exame.** As outras 2 ficam para preparo, limpeza, intervalo entre pacientes, atraso e manutenção.
- São 21 dias úteis por mês. Em 8 meses, dão 168 dias e **1.344 horas de exame por sala**.

**As faltas:**
- **As 2 horas de folga não cobrem falta.** A falta que não é reposta por encaixe come hora de exame. Por isso o uso
  aparece com 0%, 10% e 20% das faltas sem reposição.
- **Para abrir vagas,** conta-se 20% de faltas.

**Os tempos de sala**, sem nenhuma redução para caber:

| exame | minutos | exames na carteira 1 | horas | de onde vem |
|---|---:|---:|---:|---|
| Doppler bilateral de membros (venoso e arterial, inferiores e superiores) | 40 | 12.345 | 8.230 | CBR 2017, 2 × 20: um lado de cada vez |
| Mama bilateral | 20 | 12.950 | 4.317 | CBR 2017 |
| Abdômen total (adulto e infantil) | 20 | 10.347 | 3.449 | CBR 2017 |
| Parede abdominal (no código do abdômen total) | 20 | 3.304 | 1.101 | CBR 2017 |
| Doppler de carótidas, renais e outros | 20 | 4.727 | 1.576 | CBR 2017 |
| Transvaginal, aparelho urinário, tireoide, próstata, abdômen superior, bolsa escrotal e pélvica | 15 | 21.459 | 5.365 | CBR 2017 |
| TC com contraste (abdômen, pelve, tórax, crânio, pescoço e face) | 20 | 14.053 | 4.684 | intervalo do plano 4 |
| TC sem contraste | 15 | 348 | 87 | intervalo do plano 4 |
| *angio coronária (não entra)* | *30* | — | — | *hipótese* |

O SIGTAP conta o Doppler bilateral como um exame só, mas a sala fica ocupada pelos dois lados.

**A origem dos pedidos:**
- **O que se mediu:** a Região de Saúde da unidade que pediu o exame, no Mapa Social em 02/11, só nas filas da
  carteira 1 (`dados/fontes/mapa_social_20261102_regiao.md`, conferência 10/10).
- **O polo:** o de atendimento é o da Região (v26, 4.2).
- **Os pedidos sem Região** (URD e contratados) se repartem como os outros. Na TC, eles são metade dos pedidos.

**As filas do plano:**
- **O problema:** o Mapa Social dá as entradas e os agendamentos por código, com todas as filas do código juntas,
  inclusive as que o plano não atende (emergência, angio coronária).
- **A conta:** para saber quanto desse movimento é das filas do plano, usa-se a parte delas nos agendamentos dos
  últimos 12 meses.
- **Exemplo:** na TC de tórax, as filas do plano tiveram 88% dos agendamentos. Então 88% da oferta da SES nesse
  código conta como sendo delas.
- **O que sobra** (entradas − agendamentos) se reparte pela fila de hoje, porque a emergência quase não acumula fila.

**Os pedidos novos:** 1.467 exames da carteira 1 são pedidos que ainda vão entrar (seção 6).

## 5. Capacidade por polo

A seção 2 tem o ultrassom. Na tomografia, a carga é contada em tomógrafos: carga 1 é um tomógrafo cheio, com 8 horas
de exame por dia útil.

| polo | exames de TC | horas | carga própria | tem tomógrafo? | carga final, faltas repostas | carga final, 20% sem reposição |
|---|---:|---:|---:|---|---:|---:|
| Oeste | 1.943 | 643 | 0,48 | sim | 0,91 | 1,00 |
| Sudoeste | 5.796 | 1.920 | 1,43 | sim | 1,00 | 1,00 |
| Norte | 1.946 | 645 | 0,48 | sim | 0,48 | 0,60 |
| Leste | 1.079 | 357 | 0,27 | não: vai à Central e Centro-Sul | — | — |
| Central e Centro-Sul | 1.763 | 584 | 0,43 | sim | 0,70 | 1,00 |
| Sul | 1.874 | 621 | 0,46 | sim | 0,46 | 0,84 |
| **total** | **14.401** | **4.770** | **3,55** | **5** | **71%** | **89%** |

- **Os 5 tomógrafos** seguem o cenário de 5 polos do estudo de 20/10 (`estudo_polos_rede_capacidade_20261020.md`,
  seção 6).
- **Na TC, metade dos pedidos vem de URD e de contratados,** sem Região. Esses pedidos se repartem como os outros,
  e é a regulação que define o polo deles.

## 6. Pedidos novos

**O que são:** exames da carteira 1 que não estão na fila de hoje. São pedidos que devem entrar nas filas durante os
8 meses. Somam **1.467 exames e R$ 249.460,49**.

**Por que existem:** a fila de hoje das filas do plano, inteira, soma 77.459 exames e R$ 10.387.038,26. Para chegar
ao valor dos exames da v26 (R$ 10.636.542,52), faltavam R$ 249.504,26.

**Como foram contados:**
- só nos exames em que a SES agenda menos do que entra, ou seja, em que a fila cresce;
- em cada um, no máximo o que sobra por mês (entradas − agendamentos da SES no código) × 8 meses;
- primeiro os que rendem mais por hora de sala, até fechar o valor.

| exame | fila | pedidos novos | valor | sobra por mês no código | limite (× 8) | sobra em 8 meses só nas filas do plano | leitura |
|---|---|---:|---:|---:|---:|---:|---|
| Aparelho urinário | adulto | 632 | R$ 57.214,96 | 81,3 | 650 | 650 | cabe |
| TC de abdômen superior | com contraste | 318 | R$ 98.341,50 | 39,8 | 318 | 258 | passa 60 |
| Bolsa escrotal | adulto | 202 | R$ 20.200,00 | 25,2 | 202 | 196 | passa 6 |
| TC de pelve | com contraste | 199 | R$ 61.540,75 | 24,9 | 199 | 156 | passa 43 |
| Abdômen superior | adulto | 114 | R$ 11.544,78 | 14,2 | 114 | 113 | passa 1 |
| TC de pescoço | com contraste | 2 | R$ 618,50 | 0,2 | 2 | 2 | cabe |
| **total** | | **1.467** | **R$ 249.460,49** | | **1.485** | **1.375** | |

**O risco:**
- **Eles só existem se a fila continuar crescendo.** A conta usou o código inteiro; só nas filas do plano, a sobra é
  de 1.375, e não de 1.485.
- **Se a SES atender acima das entradas,** ou se a regulação não mandar esses pedidos ao projeto, eles não chegam.
  Nesse caso vale a tratativa da seção 9.

## 7. Faltas, reagendamentos e baixas

A aba Faltas e pedidos tem a conta por exame.

**O que a fonte dá:** a situação de cada agendamento da SES em 12 meses, por código. Em 155.893 agendamentos dos
códigos da carteira, são:
- 87.661 realizados;
- 45.449 faltas (24% a 44%, conforme o exame);
- 3.366 cancelados;
- 19.050 pendentes de confirmação, sem desfecho registrado.

**O que ela não dá:** o que acontece com o pedido depois da falta. Ele pode voltar à fila, ganhar outro agendamento
ou ser encerrado. Não inventei regra de retorno.

| conceito | carteira 1 | o que é |
|---|---:|---|
| exames realizados | **79.533** | a meta: o que o plano entrega e o que se paga |
| pessoas | cerca de 63.900 | estimativa: na TC, a de abdômen e a de pelve chegam juntas para a mesma pessoa |
| vagas de agenda | 99.419 | meta ÷ (1 − 20%); com a falta de cada exame na SES, seriam 120.712 |
| faltas | 19.886 | vagas − exames, com 20% |
| reagendamentos | de 0 a 19.886 | a fonte não mostra |
| pedidos consumidos | de **79.533 a 99.419** | 79.533 se toda falta for reagendada no mesmo pedido; 99.419 se nenhuma |

**O que muda na leitura:**
- **Vaga não é pedido,** e o reagendamento não é pedido novo.
- **O exame realizado conta uma vez.**
- **Baixa na fila não é exame feito.** O pedido sai da fila quando é agendado, cancelado ou devolvido; só o exame
  realizado resolve.

### 7.1 Com a mesma falta da SES (usuário, 02/11/2026)

A pergunta: se o projeto tiver, em cada exame, a falta que a SES teve nos 12 meses, quantos pedidos a mais ele
precisa? A conta está na tabela 3 da aba Faltas e pedidos e, crua, na aba Faltas na taxa da SES.

**A falta da SES** vai de 25% (Doppler, tireoide) a 44% (transvaginal). Pesada pela meta da carteira 1, dá 34%,
contra os 20% da premissa.

| | metade das faltas reagendada no mesmo pedido | nenhuma reagendada |
|---|---:|---:|
| pedidos que o projeto gasta para 79.533 exames | 100.123 | **120.712** |
| a mais que a meta | 20.590 | **41.179** |
| a mais que com 20% de faltas, no mesmo reagendamento (89.475; 99.419) | 10.648 | **21.293** |
| faltam nas filas do plano, se a SES mantém a agenda (arranjo a) | 16.309, em 15 exames | **36.821, em 16 exames** |
| pedidos que a SES teria de encaminhar ao projeto (arranjo b) | — | **35.635, 39% da agenda dela** |
| faltam mesmo se a SES parar o eletivo (arranjo c) | 0 | **1.186** |

Se toda falta for reagendada no mesmo pedido, a taxa não muda nada: são 79.533 pedidos, como na seção 7.

**Onde aperta, com nenhuma falta reagendada:**
- **Mama:** faltam 7.524 pedidos. A SES teria de passar toda a agenda dela de mama (6.520), e ainda faltariam 1.004.
- **Bolsa escrotal:** faltam 734. Mesmo com toda a agenda da SES (552), faltam 182.
- **Abdômen total, abdômen superior e aparelho urinário:** a SES teria de passar de 72% a 82% da agenda dela.
- **Transvaginal:** faltam 5.017, 43% da agenda da SES, já fora os 4.000 reservados ao IEV.
- **TC:** a SES agenda muito mais do que o projeto pede, e a parte a encaminhar fica abaixo de 35%.

**A leitura:**
- **O número que decide é o reagendamento, não a taxa.** Com a falta da SES, a diferença entre reagendar ou não é de
  41 mil pedidos. A tratativa da seção 9 precisa dizer que o pedido de quem faltou volta ao projeto, e não à fila.
- **Com metade reagendada,** os pedidos gastos ficam perto da conta de 20% sem reagendamento (100.123 contra 99.419),
  e o arranjo b da seção 9 continua bastando.
- **Com nenhuma reagendada,** só a mama e a bolsa escrotal não fecham com pedido que já existe. Nas duas, a saída é a
  confirmação e o encaixe para baixar a falta, ou remanejar a meta (seção 9, passo 4).
- **Faltar menos que a SES** é o efeito da confirmação ativa e do lembrete, que a SES não faz em toda unidade. Não há
  medida disso aqui: fica como premissa.
- Controle interno: o plano não traz taxa de faltas.

### 7.2 A carteira 6, com folga (usuário, 02/11/2026)

A carteira 1 pede mais pedidos do que chegam em cinco exames de ultrassom. A carteira 6 corrige isso: limita cada
exame aos pedidos que chegam e passa o valor que sobra para a TC, onde a SES agenda muito e uma parte pequena da agenda
dela basta. A função `carteira_folga` do script faz a conta, a partir da carteira 1 (já sem a transfontanela).

**As premissas** (constantes no começo do script):
- metade das faltas reagendada no mesmo pedido;
- a SES encaminha 20% da própria agenda em cada exame;
- a falta é a da SES, exame a exame;
- os tomógrafos não passam de 80% da capacidade.

**A conta, exame a exame:**
- pedidos que chegam = fila de hoje + entradas em 8 meses − agenda da SES + 20% da agenda da SES;
- pedidos por exame = 1 + (1 ÷ (1 − falta da SES) − 1) × 50%;
- teto = pedidos que chegam ÷ pedidos por exame.
- Onde a carteira 1 passa do teto, o corte sai primeiro dos pedidos novos e depois das filas, na proporção.
- O valor que sai vai, do preço maior para o menor, aos códigos com folga até o teto. Fica numa linha própria,
  "encaminhados pela SES".

| exame | carteira 1 | **carteira 6** | diferença |
|---|---:|---:|---:|
| Mama | 12.950 | **11.385** | −1.565 |
| Transvaginal | 5.294 | **4.836** | −458 |
| Aparelho urinário | 4.657 | **4.251** | −406 |
| Abdômen total (com a parede) | 13.651 | **13.305** | −346 |
| Abdômen superior | 2.327 | **2.105** | −222 |
| Bolsa escrotal | 1.136 | **941** | −195 |
| TC de face | 139 | **127** | −12 |
| Pélvica | 1.014 | **1.010** | −4 |
| TC de abdômen superior | 5.388 | **5.737** | +349 |
| TC de pelve | 4.168 | **4.603** | +435 |
| TC de tórax, sem a angio coronária | 3.236 | **3.299** | +63 |
| TC de pescoço | 663 | **696** | +33 |
| Doppler, tireoide, próstata e TC de crânio | 24.910 | **24.910** | 0 |
| **total** | **79.533** | **77.205** | **−2.328** |

**O resultado:**
- **O valor:** R$ 10.636.513,74, R$ 29 abaixo do valor dos exames da v26.
- **Os exames:** 61.936 de ultrassom e 15.269 de TC, em 16 códigos. Ficam na carteira 3.220 de parede, 752 pedidos
  novos e 1.487 exames encaminhados pela SES (977 de TC e 510 de ultrassom).
- **As salas de ultrassom** caem de 89% para 86%, e os tomógrafos sobem de 71% para 75% (rede inteira).
- **Nenhum exame fica sem pedido** com as duas premissas. A carteira 1 pedia que a SES passasse de 72% a 100% da agenda
  em cinco exames.

**Ainda precisa do encaminhamento da SES?** Sim, mesmo na carteira 6. A SES agenda nas mesmas filas: em 8 meses, 90.832
agendamentos, mais do que a fila de hoje (77.459). O que sobra para o projeto, com a agenda dela mantida, não basta em
todo exame. Os pedidos que faltam sem encaminhamento:

| faltas reagendadas no mesmo pedido | carteira 1 | carteira 6 |
|---|---:|---:|
| todas | 1.767, em 8 exames | 2.110, em 6 exames |
| metade (a premissa da 6) | 16.309 | 13.213, cerca de 15% da agenda da SES |
| nenhuma | 36.821 | 32.957 |

- **Com toda falta reagendada,** faltam pedidos na TC de crânio (614), na TC de pelve (501), na transvaginal (486), na
  TC de abdômen (442), na TC de pescoço (39) e na TC de face (28).
- **A carteira 6 pede mais à SES na TC** do que a 1, porque o acréscimo de TC é, por construção, pedido encaminhado. Em
  troca, pede bem menos no ultrassom, onde a agenda da SES é pequena e o pedido dela pesaria mais.
- **Sem nenhum encaminhamento,** uma carteira só fecha o valor se toda falta for reagendada no mesmo pedido: seriam
  cerca de 79.700 exames, com as salas em 91% (113% com 20% das faltas sem reposição). Com metade reagendada e sem
  encaminhamento, falta R$ 1,8 milhão.

## 8. As filas do plano: quanto entra e quanto a SES atende

A aba Filas do plano tem a conta por exame.

- **O tamanho:** no código, são 88.043 pedidos; nas filas do plano, **77.459**.
- **Os maiores cortes:**
  - na TC, a emergência: 1.165 na de abdômen, 1.090 na de pelve e 1.267 na de tórax;
  - na TC de tórax, mais 1.544 de angio coronária;
  - na transvaginal, a reserva do IEV leva 4.000.
- **Onde a SES agenda mais do que entra,** a fila cai: na transvaginal e nas TC de crânio e de face.
- **A fila observada caiu.** A dos mesmos treze nomes medidos em 15/09 caiu cerca de 2.900 pedidos por mês até 02/11,
  inclusive onde a conta de 12 meses diz que cresce. Há saídas além do agendamento, como cancelamento e devolução.
  Por isso a fila se mede de novo quando houver data de início.
- **Agendamento não é exame realizado.** A SES agenda 11.354 exames por mês nessas filas e realiza 6.519.

Os meses para zerar da aba Rumo das filas são projeção, e não previsão.

## 9. Encaminhamento da SES, e o que fazer se faltar fila

A aba Encaminhamento SES tem a conta por exame. Ela parte da fila de hoje, porque não há data de início, com o
movimento dos últimos 12 meses. Nada foi decidido. Emergência, angio coronária, sedação e as reservas do IEV não
entram.

**De onde vêm os números** (Mapa Social de 02/11, rumo por código; só as filas do plano):
- **Fila de hoje:** 77.459 pedidos esperando.
- **Pedidos que entram em 8 meses:** 97.264. É a média de pedidos novos por mês de out./2025 a set./2026, × 8.
- **O que a SES agenda em 8 meses:** 90.832.
  - Nos 16 códigos, a SES agendou 12.771 exames por mês nesses 12 meses.
  - Fica só a parte das filas do plano: na TC de tórax, 88%; no ultrassom, quase tudo. Dá 11.354 por mês, × 8.
- **O que a SES realiza em 8 meses:** 52.152. São os agendamentos que ficaram como "procedimento realizado": 6.519
  por mês, × 8.
- **Por que realiza só parte do que agenda:** nos 155.893 agendamentos dos 12 meses, a situação é esta:
  - 56% realizados;
  - 29% faltas;
  - 2% cancelados;
  - 12% pendentes de confirmação. A data passou e a unidade não registrou se o exame foi feito. Parte desses pode ter
    sido feita, e o realizado da SES pode estar subestimado.
- **Pedidos que o projeto gasta:**
  - se a falta for reagendada no mesmo pedido, 1 pedido por exame: 79.533;
  - se cada falta gastar o pedido, com 20% de faltas: 99.419.

**Os três arranjos:**
- **a:** a SES mantém a agenda dela;
- **b:** a SES passa ao projeto só o que falta, e deixa de agendar esses pedidos na rede dela;
- **c:** a SES para o eletivo e passa tudo ao projeto.

| | a: a SES mantém a agenda | **b: a SES passa só o que falta** | c: a SES para o eletivo |
|---|---:|---:|---:|
| pedidos que a SES deixa de agendar e passa ao projeto | 0 | **1.762 a 15.529** | 90.832 |
| pedidos disponíveis para o projeto (fila de hoje + entradas − agenda da SES) | 83.891 | 99.419 | 174.723 |
| exames do projeto (meta) | 79.533 | 79.533 | 79.533 |
| pedidos que sobram na fila no fim, com a falta reagendada | 4.358 | 19.886 | 95.190 |
| pedidos que sobram na fila no fim, se a falta gasta o pedido | faltam 15.528 | **0** | 75.304 |
| exames sem pedido suficiente (falta reagendada; falta gasta o pedido) | 8; 17 | **0; 0** | 0; 0 |
| exames a mais na rede (projeto − o que a SES deixa de fazer) | 79.533 | **70.779** | 27.381 |

**Como ler a tabela:**
- **Pedidos que sobram** = pedidos disponíveis − pedidos que o projeto gasta. "Faltam" quer dizer que não há pedido
  para cumprir a meta.
- **O total soma os 16 exames,** mas a sobra de um exame não cobre a falta de outro. Por isso a linha "exames sem
  pedido suficiente".
- **Exames a mais na rede** são os 79.533 do projeto menos o que a SES deixa de fazer por ter cortado a agenda. Ela
  realiza cerca de 56% do que agenda.

**A leitura:**
- **No arranjo a, a SES e o projeto disputam os mesmos pedidos.** Mesmo com toda falta reagendada, falta pedido em 8
  exames: transvaginal (944), TC de crânio (614), TC de abdômen (93), TC de pelve (66), TC de face (40), TC de pescoço
  (6), e 2 pedidos no abdômen superior e na bolsa escrotal.
- **O arranjo b sustenta as metas,** sem a SES suspender nada. Os exames que mais pedem, no pior caso:

  | exame | parte da agenda da SES a encaminhar | agendamentos |
  |---|---:|---:|
  | bolsa escrotal | 52% | 286 |
  | mama | 38% | 2.452 |
  | abdômen superior | 37% | 584 |
  | aparelho urinário | 36% | 1.149 |
  | TC de face | 28% | 75 |
  | Doppler | 26% | 2.140 |
  | próstata | 24% | 661 |

- **O arranjo c não serve na TC.** A SES faz muito mais TC do que o projeto, e suspender a agenda dela tira exames da
  rede: −7.228 na TC de tórax e −3.865 na de crânio.

**Demanda transferida não é demanda nova.** O aumento líquido é a produção do projeto menos o que a SES deixa de fazer.

**Se faltar fila, a tratativa, em ordem:**
1. **Acompanhar:** medir todo mês a fila de cada exame do plano e avisar a SES com antecedência quando uma fila for
   acabar antes da meta.
2. **Pedidos novos:** a regulação manda ao projeto os pedidos que entram nas filas do plano, antes de agendá-los na
   rede própria.
3. **A SES encaminha parte da agenda dela:** deixa de agendar na rede própria a parte da tabela acima e manda esses
   pedidos ao projeto. Não precisa suspender o atendimento.
4. **Remanejar:** se ainda faltar, o quantitativo passa a outro exame do objeto que tenha fila, por termo aditivo,
   como a v26 já prevê.
5. **Último caso:** a angio coronária, só para compor valor.

## 10. Para confirmar com a SES

- **Parede abdominal (L-007):** que a fila de parede abdominal é feita e faturada como abdômen total
  (02.05.02.004-6), por escrito. São 3.304 exames e R$ 388.253,04. A angio coronária não entra no lugar.
- **O encaminhamento e a tratativa da seção 9.**
- **O IEV (L-008):** se a regulação manda às OCI do IEV os pedidos das filas de exame. A situação completa:

| exame | pedidos na fila | pessoas | OCI do IEV que inclui o exame | OCI contratadas | o que o IEV fez até 26/10 | regra no plano 4 |
|---|---:|---:|---|---:|---|---|
| US de articulação (sem partes moles) | 11.215 | 11.208 | 09.03.01.002-0, ortopedia com US (030975 e 030977) | 19.070 | 308 consultas com CID da OCI; nenhuma US pela fila do exame | fora inteira |
| US de partes moles | 3.140 | 3.138 | a mesma | (as mesmas) | idem | fora inteira (usuário, 01/11) |
| US transvaginal | 9.295 | 9.294 | 09.06.01.001-2, GIN1 (030977) | 3.218 | 20 consultas de ginecologia | 4.000 reservados ao IEV; o resto entra |
| TC de pelve | 3.954 | 3.952 | 09.03.01.003-8, ortopedia com TC (030977) | 539 (todas as TC) | 94 consultas com CID da OCI | entra, sem os 7 pedidos com o CID |
| US de próstata transretal | 22 | 22 | 09.01.01.004-9, próstata (030977) | 1.015 | nenhuma consulta de urologia | fora: outro exame |

**A leitura:**
- **Na US de articulação,** o IEV contratou mais OCI (19.070) do que a fila inteira (11.215). Até 26/10, não recebeu
  nenhum pedido dela, porque a OCI entra pela consulta de ortopedia.
  - Se a regulação mandar a fila ao IEV, ele tem contrato para atendê-la.
  - Se não mandar, a fila fica sem ninguém.
- **Na transvaginal,** o IEV contratou 3.218 GIN1 e quase não executou. A reserva de 4.000 são essas OCI com folga de
  faltas.
- **A pergunta à regulação, por escrito:** os pedidos das filas de exame vão às OCI do IEV? Com a resposta, a
  articulação pode voltar ao plano, sem os pedidos reservados ao IEV.

## 11. Dados a medir depois (não agora)

- quantos pedidos têm mais de um agendamento, e o que acontece depois da falta;
- a fila do plano de novo, quando houver data de início;
- salas, horário e tempo real por exame de cada clínica (L-006);
- quantos pedidos com mais de 24 meses ainda têm paciente.

## 12. As metas: proposta para avaliar depois, e as proteções

A v26 diz que o convênio "resolve a totalidade das 78.572 solicitações da extração" (3.1). Pela seção 9, isso depende
do que a SES fizer com a própria agenda. A proposta abaixo não foi aplicada ao plano.

- **Objeto:** oferecer à regulação exames de ultrassonografia e de tomografia, dos procedimentos e filas listados no
  plano, para usuários regulados com indicação ambulatorial.
- **Meta de produção:** 79.533 exames realizados e laudados, por procedimento, verificáveis no TrakCare e na APAC.
- **Meta de oferta:** no mínimo 99.419 vagas publicadas à regulação em 8 meses, na curva mensal. A vaga liberada por
  falta volta à regulação no mesmo dia.
- **Demanda:** a que a regulação encaminhar, na ordem que ela define. A execução fica condicionada ao envio regular da
  demanda regulada, como no item 13.7 do plano do IEV.
- **Resultado:** redução da espera e da fila dos procedimentos do objeto, medida pelo Mapa Social no início, no meio e
  no fim. É indicador de acompanhamento, e não promessa de zerar.
- **Remanejamento:** esgotada a demanda de um procedimento, o quantitativo passa a outro do objeto, por termo aditivo.
- **Não sobreposição:** a regulação não encaminha ao convênio pedido vinculado a OCI em execução por outro convênio.
- **Sai do texto:** "resolve a totalidade das N solicitações". A fila apurada fica como justificativa.

**As proteções, para o plano não ter de atender o que não previu:**
- **Lista fechada:** o plano lista os procedimentos e as filas do SISREG que atende, pelo nome e pelo código. Pedido de
  outra fila não entra, mesmo que use um código do objeto.
- **Fora, por escrito:**
  - emergência e urgência, e paciente internado;
  - exame com sedação ou anestesia;
  - angiotomografia de coronárias;
  - ultrassom obstétrico e ecocardiografia;
  - US de articulação e de partes moles, e TC de coluna e de articulações;
  - qualquer exame que peça outro equipamento ou outro especialista.
- **Contraste:** triagem antes do exame (v26, 4.8). Quem não pode receber contraste volta à regulação. O pedido não
  conta na meta nem como falta do projeto.
- **Limite do equipamento:** paciente acima do peso ou do diâmetro que a mesa ou o gantry aceitam, ou que só faria o
  exame sedado, volta à regulação, nas mesmas condições.
- **Crianças:** a carteira tem 1.463 exames de filas infantis (a transfontanela, de recém-nascido e lactente, saiu em
  03/11).
  É preciso decidir se a rede atende criança e a partir de que idade. Se não atender, essas filas saem da lista e o
  valor se remaneja.
- **Devolução:** pedido fora do escopo se devolve à regulação em prazo curto, sem contar na meta e sem penalidade.
- **Teto, e não piso:** o quantitativo de cada procedimento é o máximo a produzir, e não a obrigação de atender toda a
  demanda que chegar. A vaga publicada e não ocupada pela regulação conta na meta de oferta.

## 13. A carteira 1 e as outras, para comparação

| código | exame | v26 | **carteira 1** | fila de hoje (filas do plano) |
|---|---|---:|---:|---:|
| 02.05.01.004-0 | Doppler (carótidas, membros, renais) | 14.508 | **17.072** | 16.770 |
| 02.05.02.004-6 | Abdômen total (com a parede, 3.304) | 13.166 | **13.651** | 13.651 |
| 02.05.02.009-7 | Mama bilateral | 14.689 | **12.950** | 12.950 |
| 02.05.02.018-6 | Transvaginal (sem os 4.000 do IEV) | 10.541 | **5.294** | 5.294 |
| 02.05.02.005-4 | Aparelho urinário | 3.944 | **4.657** | 4.025 |
| 02.05.02.012-7 | Tireoide | 3.216 | **3.979** | 3.854 |
| 02.05.02.010-0 | Próstata por via abdominal | 3.201 | **3.052** | 2.969 |
| 02.05.02.003-8 | Abdômen superior | 2.261 | **2.327** | 2.213 |
| 02.05.02.007-0 | Bolsa escrotal | — | **1.136** | 934 |
| 02.05.02.016-0 | Pélvica | — | **1.014** | 1.014 |
| 02.06.03.001-0 | TC de abdômen superior | 4.516 | **5.388** | 5.031 |
| 02.06.03.003-7 | TC de pelve | 3.862 | **4.168** | 3.942 |
| 02.06.02.003-1 | TC de tórax, sem a angio coronária (na v26, com ela) | 5.240 | **3.236** | 3.215 |
| 02.06.01.007-9 | TC de crânio | — | **807** | 801 |
| 02.06.01.005-2 | TC de pescoço | — | **663** | 657 |
| 02.06.01.004-4 | TC de face | — | **139** | 139 |
| | **total** | **79.144** | **79.533** | **77.459** |

- A meta passa da fila de hoje nos 1.467 pedidos novos (seção 6) e nos 607 encaminhados pela SES que entraram no lugar
  da transfontanela (seção 3).
- São R$ 10.636.498,75, R$ 44 abaixo do valor da v26. Com o apoio de R$ 956.160,00, cabe no recurso.
- São 65.132 exames de ultrassom e 14.401 de TC. A transfontanela saiu (usuário, 03/11/2026).

**As outras carteiras ficam para comparação.**
- **A 2, a 3 e a 4 levam a angio coronária.** A 3 é a que fica sem a parede.
- **A 5 fica sem a angio,** mas depende de 6.842 pedidos novos e deixa de fora a bolsa escrotal, a pélvica e a
  transfontanela.
- **A 6 é a carteira com folga (seção 7.2):** 77.205 exames, a 1 limitada aos pedidos que chegam com a falta da SES; o
  valor que sai do ultrassom passa para a TC.

Os números delas estão no Resumo e em Carteiras por código.

## 14. As fontes

| o quê | de onde |
|---|---|
| Inventário de todas as filas de imagem, rumo por código e situação dos agendamentos | Mapa Social, recarga de 02/11/2026 às 10h31; agente `mapa-social`, conferência 9/9. `dados/fontes/mapa_social_20261102_imagem.*` |
| Região de Saúde das filas da carteira 1 | Mapa Social, recarga de 02/11/2026 às 18h31; agente `mapa-social`, conferência 10/10. `dados/fontes/mapa_social_20261102_regiao.*` |
| Fila de 15/09 e 05/10 dos onze nomes da v26 | `dados/fontes/mapa_social_20261005.md`, seção 6 |
| Pessoas por pedido | `dados/fontes/mapa_social_20261005.md`, seção 6 |
| Oferta por unidade executante | `dados/fontes/mapa_social_20261102_executante_c.*`, os 17 códigos da carteira 1 (as coletas `_executante` e `_executante_b` da manhã ficam como estavam) |
| Transvaginal × CID da GIN1 | `dados/fontes/mapa_social_20261102_gin1.*` (10/10) |
| Preço | o Anexo Único da Candanga (SEI 212117347), modalidade SIA, do `main`; vale o SIGTAP quando é igual ou maior (LI-002) |
| Metas, preços, polos e capacidade da v26 | `versoes/plano_v26_20261021.md`, 2.2, 3.4, 4.2, 7.3 e 8.2 |
| Outros planos | `estudo_outros_planos_imagem_20261102.md` |
| Tempos | CBR 2017 no ultrassom; intervalos do plano 4 na TC (`output/estudo_imagem_candanga_20261101.xlsx`, aba 6) |
| Rede de clínicas e polos | `estudo_polos_rede_capacidade_20261020.md` |

Só entram dados agregados, sem CPF nem CNS. As coletas originais estão preservadas nas pastas brutas.

## 15. O inventário e o rumo de cada código

**656 filas de imagem** (nome exato × código), em 133 códigos e sem corte de tamanho. Somar filas não dá pessoas
únicas.

| modalidade | filas | pedidos | na fila viva (24 meses) | pessoas | no estudo |
|---|---:|---:|---:|---:|---|
| Ultrassom | 151 | 99.169 | 74.069 | 79.673 | **foco** |
| Tomografia | 196 | 21.269 | 21.039 | 11.599 | **foco** |
| Radiologia | 174 | 14.093 | 14.022 | 12.748 | mapeada, fora do foco |
| Ressonância | 109 | 10.149 | 10.142 | 7.690 | fora: outro equipamento |
| Medicina nuclear | 24 | 5.663 | 5.663 | 4.178 | fora: outro equipamento |
| Radiologia intervencionista | 2 | 9 | 9 | 9 | fora |

**Como ler:**
- A fila são os três status pendentes. As devolvidas ficam ao lado, sem subtrair uma da outra.
- O rumo é por código, por entradas e agendamentos, e não pela queda observada do estoque (para essa, ver a seção 8).

**Só ambulatório.**
- As 86 filas com "EMERG" no nome (4.697 pedidos) ficam fora (D-009).
- A TC com sedação também fica fora.

**As classes,** pelo tempo que a fila leva para zerar no ritmo da SES:
- **capacidade da SES:** zera em até 8 meses;
- **zera devagar:** zera, mas leva mais de 8 meses;
- **esforço pontual:** houve mutirão, e acabado o esforço a fila não zera;
- **déficit persistente:** não zera, ou levaria mais de dois anos no ritmo dos 3 últimos meses;
- **inconclusivo:** os dois ritmos dizem coisas diferentes.

São projeções condicionadas ao ritmo, e não previsões.

| código | fila | entram por mês | oferta por mês (12 m; 3 últimos) | meses para zerar (12 m; 3 últimos) | classe |
|---|---:|---:|---|---|---|
| Doppler 02.05.01.004-0 | 16.844 | 1.359 | 1.053; 1.100 | não zera; não zera | déficit persistente |
| Abdômen total 02.05.02.004-6 | 13.656 | 1.155 | 889; 1.169 | não zera; 981 | déficit persistente |
| Mama 02.05.02.009-7 | 12.952 | 913 | 815; 1.777 | não zera; 15 (só com o mutirão) | esforço pontual |
| Transvaginal 02.05.02.018-6 | 9.295 | 1.260 | 1.467; 2.064 | 45; 12 | zera devagar |
| TC de abdômen superior 02.06.03.001-0 | 6.214 | 1.516 | 1.476; 1.504 | não zera; não zera | déficit persistente |
| TC de tórax 02.06.02.003-1 | 6.043 | 2.488 | 2.463; 2.950 | não zera; 13 | inconclusivo |
| TC de pelve 02.06.03.003-7 | 5.044 | 1.272 | 1.247; 1.309 | não zera; 135 | déficit persistente |
| Aparelho urinário 02.05.02.005-4 | 4.032 | 481 | 400; 470 | não zera; não zera | déficit persistente |
| Tireoide 02.05.02.012-7 | 3.858 | 408 | 299; 309 | não zera; não zera | déficit persistente |
| Próstata 02.05.02.010-0 | 2.971 | 366 | 343; 312 | não zera; não zera | déficit persistente |
| Abdômen superior 02.05.02.003-8 | 2.229 | 224 | 209; 221 | não zera; não zera | déficit persistente |
| TC de crânio 02.06.01.007-9 | 1.428 | 1.141 | 1.276; 1.363 | 11; 6 | zera devagar |
| Pélvica 02.05.02.016-0 | 1.016 | 132 | 116; 132 | não zera; 3.048 | déficit persistente |
| Bolsa escrotal 02.05.02.007-0 | 961 | 95 | 70; 61 | não zera; não zera | déficit persistente |
| TC de pescoço 02.06.01.005-2 | 762 | 201 | 201; 214 | não zera; 59 | déficit persistente |
| TC de face 02.06.01.004-4 | 466 | 430 | 447; 592 | 28; 3 | zera devagar |
| Transfontanela 02.05.02.017-8 | 272 | 74 | 71; 76 | não zera; 103 | déficit persistente |

Esta tabela é do código inteiro. Só nas filas do plano, ver a seção 8.

**A radiologia fica mapeada, sem ataque agora:** 172 filas e 14.077 pedidos, puxados pela mamografia de rastreamento
(6.630) e pela densitometria (2.178). Se um dia entrar, pede outro equipamento.

## 16. Cobertura: o que já tem dono

O estudo separado (`estudo_outros_planos_imagem_20261102.md`) tem o detalhe. A aba Quem atende o quê junta tudo por
código.

| motivo | pedidos |
|---|---:|
| **US de articulação: comprometida com a OCI 09.03.01.002-0 do IEV** (L-008 revista) | 11.215 |
| D-009: emergência | 4.697 |
| L-008: partes moles (IEV) | 3.140 |
| L-008: TC de coluna, articulações e segmentos (OCI 09.03.01.003-8) | 522 |
| **Transvaginal: 4.000 dos 9.295 reservados para a OCI GIN1 do IEV** | 4.000 |
| TC de pelve: os pedidos com CID da OCI 09.03.01.003-8 | 7 |

**Outra equipe ou outro equipamento:** 17.274 pedidos.
- ecocardiografia (14.669);
- US de globo ocular (1.316);
- obstétricas (561);
- PET-CT (379);
- TC cone beam (195);
- paquimetria (144);
- TC com sedação (10).

**O redacao_07 não cobre fila** (está no campo das ideias). Se avançar, exclui o que o plano 4 tomar.

## 17. Viabilidade

A aba Viabilidade tem a margem por hora de cada fila. **Os custos ficam para outra etapa** (decisão de 02/11). A
margem serve só para tirar da carteira o exame que não paga a hora de sala.
- Todo exame da carteira 1 tem margem por hora positiva nas premissas da `custo_por_exame_v2`.
- As mais baixas: o Doppler de membros (40 minutos), a pélvica e a mama.

## 18. Pendências que podem mudar o resultado

| # | pendência | o que muda | quem decide |
|---|---|---|---|
| 1 | **L-007:** a parede abdominal no abdômen total | sem ela, sai uma peça essencial (3.304 exames, R$ 388 mil); a reposição é decisão do usuário, sem angio coronária | SES, por escrito |
| 2 | **O encaminhamento da seção 9** | sem ele, falta pedido em 8 exames mesmo com toda falta reagendada | regulação da SES |
| 3 | **O reagendamento depois da falta** | os pedidos consumidos vão de 79.533 a 99.419; com a falta da SES, até 120.712 (seção 7.1) | medir depois e pactuar |
| 4 | **A reposição das faltas por encaixe** | sem ela, a Sudoeste e a Sul passam de 100% das salas com 10% das faltas sem reposição | operação do projeto |
| 5 | **Crianças** | 1.463 exames de filas infantis dependem de a rede atender criança | usuário e clínicas |
| 6 | **A articulação e a transvaginal com o IEV** (L-008) | com a confirmação, a articulação volta (cerca de 10 mil exames) | regulação da SES |
| 7 | **As salas e os tomógrafos reais** (L-006) | o tempo real por exame de cada clínica decide | clínicas |
| 8 | **Contraste 02.06.03.004-5** fora da Candanga | nenhum adicional; a cotação da TC já inclui o contraste | SES |

## 19. Melhorias na planilha (usuário, 02/11/2026)

O usuário pediu para melhorar cinco abas da planilha organizada: Encaminhamento SES, Faltas e pedidos, Rumo das
filas, Filas e Viabilidade. As cinco foram refeitas. Também entraram:
- um quadro "Como ler" na aba Capacidade por polo;
- as consultas que o IEV fez, na aba IEV;
- a consulta ao CNES das unidades do IEV.

O que mudou em cada uma, e as decisões que continuam com o usuário, estão em `melhorias_planilha_20261102.md`.

**Viabilidade, em uma linha:** todo exame da carteira tem sobra positiva com as faltas repostas. Com 20% das faltas
sem reposição, a pélvica fica negativa, e o Doppler de membros quase zera. Os custos continuam premissas, para a etapa
de custos.

## 20. O que este estudo não fez, e o histórico

- Não mudou o plano, o `estado.yaml` nem o enquadramento.
- Não reabriu custos nem a cotação dos médicos.
- Não fez commit.
- Não mexeu no redacao_06, no redacao_07 nem em outro plano.

**O que a revisão da tarde de 02/11 deixou para trás** (a versão da manhã está em `anterior_20261102_manha/`):
- **"As 13 salas ficam em 137%":** a conta era da rede inteira, sem polo. Agora são 20 salas e 5 tomógrafos, polo a
  polo.
- **"Faltam 12.884 a 27.004 pedidos para repor as faltas":** a conta lia cada vaga como um pedido novo e usava o fluxo
  do código inteiro. Agora os pedidos consumidos ficam entre 79.533 e 99.419.
- **O crescimento das filas pelo código inteiro, só o positivo:** agora a conta usa só as filas do plano, com a queda
  onde a SES agenda mais do que entra.
- **A Região por fila de 05/10, usada como aproximação:** foi trocada pela coleta de 02/11.
- **7 meses, data de início, mutirões e o polo dos pedidos sem Região:** saíram por decisão do usuário.
