# Estudo — quem entra em cada OCI de cardiologia, e quantas pessoas sobram

**Controle interno.** Estudo de 27/10/2026 para o redacao_08: Emenda 41360018/2024, do Senador
Izalci Lucas, R$ 2 milhões; executor Instituto Fazer o Bem, Faz Bem. Estuda as cinco decisões
abertas do enquadramento (`planos/redacao_08/dados/enquadramento_mapa_social.json`), mais uma que
apareceu nos números, para fechar quantas pessoas a emenda pode atender. A escolha é sua.

**As fontes:**
- `mapa_social_20261027_ocis.md`: medição de hoje, conferência 11/11;
- `mapeamento_filas_cardiologia_20261027.md`;
- as fichas do SIGTAP de 10/2026, no ramo `plano_oci_cardiologia`.

As pessoas são de 27/10, na idade da ficha; entre parênteses, a fila viva (24 meses).

## 1. A decisão que veio antes das outras: por onde a pessoa entra

A medição separa, em cada OCI, quem espera na **consulta** e quem espera só num **exame**, com o
CID da finalidade:

| OCI | só consulta | só exames | todas as filas |
|---|---|---|---|
| 003-4 coronária, inicial | **1.436** (1.132) | 2.294 (1.997) | 3.644 (3.051) |
| 006-9 insuficiência cardíaca | **2.079** (1.794) | 4.631 (2.963) | 6.461 (4.570) |
| 004-2 e 005-0 coronária, progressão | **2.023** (1.617) | 32 e 1.338 | 2.053 e 3.313 |
| 002-6 avaliação cardiológica | **41** (25) | 377 (275) | 417 (299) |
| 001-8 risco cirúrgico, CID da ficha | **54** (46) | 307 (205) | 358 (248) |
| 007-7 pré-operatório, CID da ficha | **88** (87) | 52 (47) | 136 (130) |
| risco cirúrgico inteiro (P-08) | **9.654** (8.170) | — | 9.654 (8.170) |

As colunas "só consulta" e "só exames" se cruzam: quem espera nas duas conta nas duas.

**Na 003-4, o eco pesa mais que tudo.** Ele é só compatível, não obrigatório, e tem 1.633
pedidos com I20/I25. A consulta adulto tem 1.255, o ergométrico 547, o eletrocardiograma 255 e a
consulta coronária 206.

### Motivos para contar só a consulta

- **É assim que a OCI anda na prática.** O IEV só aparece no SISREG pela consulta de entrada;
  os exames são feitos dentro do pacote (mapeamento de 26/10). Na ortopedia, a OCI dele também
  entra pela consulta, e não pela fila do exame.
- **A OCI começa com a consulta especializada.** Quem espera só um eco ou um eletrocardiograma
  já tem um médico que pediu o exame. Mandá-lo para a OCI é dar-lhe outra consulta e outros
  exames de que talvez não precise.
- **Pegar gente da fila do exame pede que a regulação cancele o pedido e marque a OCI.** É uma
  pergunta à SES do mesmo tipo da P-08, e não há precedente.
- **É o número que se defende.** Quem lê o plano entende "esperam consulta de cardiologia com
  angina", e não estranha.

### Motivos para contar também os exames

- **São pessoas reais, com o CID certo, esperando um pedaço da OCI.** A OCI resolve o exame e
  ainda dá a avaliação.
- **Na 002-6 e na 001-8, a fila é quase toda de exame.** Na 002-6, 377 das 417 pessoas esperam
  um eletrocardiograma com Z13.6 (rastreamento cardiovascular), que é justamente o público dela.
  Pela consulta, sobram 41.
- **O número fica maior,** e a justificativa mais forte.

### A proposta

- **A conta usa a consulta.**
- **Os exames ficam como reserva,** se a SES aceitar converter o pedido, e entram numa pergunta
  junto com a P-08.
- **Na 002-6,** a porta é o eletrocardiograma com Z13.6 ou Z84.8, porque a OCI foi feita para
  esse público. Isso depende da mesma pergunta.

## 2. A consulta adulto (genérica)

Dentro da consulta, quanto vem da adulto e quanto da específica (pedidos com o CID da finalidade):

| OCI | consulta adulto | consulta específica |
|---|---|---|
| 003-4 (I20, I25) | 1.255 | 206 (coronária) |
| 004-2 e 005-0 (I20 a I25) | 1.791 | 273 (coronária) |
| 006-9 (I50) | 1.251 | 895 (insuficiência cardíaca) |

**Para entrar:**
- **É onde a maior parte espera.** Sem a adulto, a 003-4 cai de 1.436 para cerca de 206 pessoas.
- **O CID já faz o recorte.** Quem está na consulta adulto com I25 espera um cardiologista por
  doença coronária, e a espera média é de 483 dias.
- **O IEV já usa essa fila:** as OCI 006-9 e 004-2 dele entram pela consulta adulto (1.138
  agendadas). É o precedente.

**Para não entrar:**
- **O CID da fila genérica é menos confiável:** quem pede é, em geral, a atenção primária.
- **A mesma pessoa serve a três OCI.** As 1.791 pessoas com I20 a I25 na adulto contam na 004-2 e
  na 005-0, e as 1.255 com I20/I25 estão dentro delas e contam também na 003-4.
- **Na 006-9 e na 004-2, a adulto é a fila em que o IEV pesca.** Ele ainda tem cerca de 760 a
  fazer.

**A proposta: entra, pelo CID da finalidade.**
- Sem ela, a cardiologia fica sem fila.
- A sobreposição se resolve na seção 6, com a pessoa contada uma vez.

## 3. A 003-4: I20 e I25, ou I20 a I25?

O que separa as duas é o grupo I21 a I24:
- I21, infarto agudo;
- I22, infarto recorrente;
- I23, complicações atuais do infarto;
- I24, outras isquêmicas agudas.

Na coleta de 25/10, eram 767 pessoas a mais (4.450 contra 3.683).

**Para incluir:**
- **A ficha aceita** todo o capítulo I. A APAC não cai.
- **Numa fila ambulatorial, I21 costuma ser quem infartou e está em seguimento.** Pela definição
  atual, isso também é síndrome coronariana crônica.

**Para não incluir:**
- **A 003-4 é a "avaliação diagnóstica inicial".** Ela pede ergométrico obrigatório, para quem
  ainda precisa do diagnóstico. Quem infartou já tem o diagnóstico.
- **Para quem infartou, o caminho próprio são as OCI de progressão** (004-2 e 005-0), que aceitam
  I20 a I25 pela ficha.
- **O ergométrico logo depois de um infarto** é decisão do cardiologista, não de protocolo de
  pacote.

**A proposta: I20 e I25.** O grupo I21 a I24 fica para as OCI de progressão.

## 4. A 006-9: I50, ou a insuficiência cardíaca ampliada?

A ampliada junta ao I50:
- I11.0, cardiopatia hipertensiva com insuficiência cardíaca;
- I13.0 e I13.2, cardiopatia e nefropatia hipertensivas com insuficiência cardíaca;
- I42, cardiomiopatias;
- I43, cardiomiopatias em doenças classificadas em outra parte.

Em 25/10, eram 582 pessoas a mais (7.092 contra 6.510).

**Para incluir:**
- **I11.0, I13.0 e I13.2 dizem "com insuficiência cardíaca" no próprio nome.** É o mesmo doente,
  com outro código.
- **A cardiomiopatia pede a mesma investigação:** eco, NT-proBNP, Holter.

**Para não incluir:**
- **A cardiomiopatia (I42, I43) às vezes pede mais do que a OCI tem,** como ressonância ou
  avaliação genética.
- **A 006-9 nem está no caminho A.**

**A proposta:**
- I50 com I11.0, I13.0 e I13.2;
- I42 e I43 de fora;
- a ser medida, se a 006-9 entrar.

## 5. A P-08: a fila de risco cirúrgico na 007-7

**Para entrar:**
- **É a maior fila:** 9.654 pessoas (8.170 na viva). Entram 819 por mês.
- **O precedente existe:** a regulação já manda essa fila, com o CID da cirurgia, para a OCI
  001-8 do IEV (CID mais usado: catarata).
- **A 007-7 se paga** (154% do mínimo do mercado, 116% com cardiologista) e aceita qualquer
  médico.
- **O CID da cirurgia cabe nela:** a 007-7 pede Z01.8, Z48.8 ou Z48.9 como principal e a causa
  associada como secundário (atributo 043).

**Para não entrar:**
- **A concorrência:**
  - o IEV ainda tem 1.825;
  - a HAPVIDA propôs 792 por mês e o Hospital de Ceilândia 115 por mês, no Agora Tem
    Especialistas (posição de 03/09);
  - se os dois começarem, a fila pode sumir antes do nosso convênio.
- **A falta é a maior das OCI:** 38%.
- **O pedido é de "consulta em cardiologia – risco cirúrgico".** A 007-7 é a gestão do
  pré-operatório, mais larga. Se for um clínico quem a faz, a SES pode entender que não é o que
  se pediu. Com cardiologista, não há essa dúvida.
- **Depende da SES.**

**A proposta: entra, a decidir pela SES.**
- A pergunta vai junto com a dos exames (seção 1) e a da situação da HAPVIDA e do Hospital de
  Ceilândia.
- A 007-7 é feita por cardiologista.

## 6. Fila inteira ou fila viva

| fila | inteira | viva | o que sai |
|---|---|---|---|
| 003-4, consulta | 1.436 | 1.132 | 21% |
| 006-9, consulta | 2.079 | 1.794 | 14% |
| risco cirúrgico | 9.654 | 8.170 | 15% |

**Pela viva:**
- **Pedido com mais de 2 anos muitas vezes não vale mais:** a pessoa fez em outro lugar, mudou
  ou o quadro mudou.
- **A meta tem de ser realizável.** Recurso mais IEV acima da viva é o que a LI-023 já apontou.

**Pela inteira:**
- **O SISREG ainda os guarda**, e a regulação pode chamá-los.
- **É o número do painel**, que qualquer um confere.

**A proposta:**
- **a conta e a meta pela viva;**
- **a justificativa com os dois:** "X na fila, Y nos últimos 24 meses".

## 7. A sobreposição entre as OCI coronárias

A linha coronária é uma sequência, e não três filas:
- a pessoa faz a 003-4 (avaliação inicial);
- se precisar, segue para a 004-2 (eco de estresse) ou a 005-0 (cintilografia).

As 2.023 pessoas da consulta com I20 a I25 são as mesmas nas três.

**A proposta:**
- cada pessoa conta uma vez, na 003-4 (as I20/I25);
- as de I21 a I24 ficam para a progressão;
- a progressão (004-2, 005-0) não se soma à fila. Ela é o passo seguinte de uma parte de quem
  fez a 003-4.

## 8. Quantas pessoas, com a proposta

Pela consulta, pela fila viva, cada pessoa uma vez, menos o que o IEV ainda vai fazer:

| OCI | pessoas (viva) | menos o IEV | sobram | valor | custo de todas |
|---|---|---|---|---|---|
| 007-7, fila de risco cirúrgico (se a P-08 passar) | 8.170 | 1.825 | **6.345** | R$ 130,00 | R$ 824.850,00 |
| 003-4 coronária, inicial (I20, I25) | 1.132 | — | **1.132** | R$ 270,00 | R$ 305.640,00 |
| 006-9 insuficiência cardíaca (I50) | 1.794 | cerca de 760 | **cerca de 1.034** | R$ 350,00 | R$ 361.900,00 |
| 002-6 avaliação cardiológica, pelo eletrocardiograma | 299 | — | **299** | R$ 200,00 | R$ 59.800,00 |
| **total** | | | **cerca de 8.810** | | **R$ 1.552.190,00** |

**O que isso diz:**
- **Pela consulta, hoje, a fila parada não gasta o recurso.** Sobram R$ 248 mil dos R$ 1,8 milhão
  para produção. O resto tem de vir de quem entra na fila durante o convênio.
  - No risco cirúrgico, entram 819 pessoas por mês.
  - Nas outras, o fluxo da consulta com o CID ainda não foi medido sozinho.
- **O caminho A de hoje cai.** Ele contava 3.683 na 003-4 (todas as filas). Pela consulta, são
  1.132. A diferença (cerca de R$ 690 mil) vai para a 007-7, a 006-9 ou o fluxo.
- **Tudo depende da P-08.** Sem ela, sobram umas 2.465 pessoas (003-4, 006-9 e 002-6) e
  R$ 727 mil de produção. O recurso passaria da fila.
- **E da HAPVIDA e do Hospital de Ceilândia.** Se começarem, a fila do risco cirúrgico encolhe, e
  o resultado vai para o mesmo lugar do "sem a P-08".

## 9. O que falta para fechar o número

1. **Uma medição pela consulta,** para cada OCI e cada alternativa (com e sem a adulto, I20 a
   I25, insuficiência cardíaca ampliada), com:
   - as pessoas uma vez entre as OCI coronárias;
   - **quantas entram por mês só pela consulta**;
   - a falta na consulta.

   Com isso a conta de 12 meses fecha. O kit mede as alternativas como objetos separados.
2. **O risco cirúrgico por estabelecimento,** para ver se a HAPVIDA e o Hospital de Ceilândia já
   aparecem. Esta coleta não separou por unidade.
3. **A pergunta à SES,** com três itens:
   - a P-08;
   - converter pedido de exame em OCI;
   - a situação das duas propostas.
