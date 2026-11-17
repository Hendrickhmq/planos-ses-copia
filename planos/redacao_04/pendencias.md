# Pendências — plano 4, filas de ultrassom e tomografia

Aberto em 15/09/2026. Lacuna tem dono. Decisão tem opções e consequência em reais.

---

## Lacunas

### L-001 — parede abdominal e partes moles · RESOLVIDA NA FONTE

**Fechada em 15/09/2026** com a coleta em `dados/fontes/validacao_ultrassom.md`. O
painel de regulação carrega o código SIGTAP de cada nome interno:

| nome interno | SIGTAP |
|---|---|
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | **02.05.02.004-6** — abdômen total |
| ECOGRAFIA␣␣DE PARTES MOLES | **02.05.02.006-2** — articulação |

**A parede abdominal cai no mesmo código do abdômen total**, que já estava no objeto:
as duas linhas viram uma, de 13.080 exames. **As partes moles entram como linha
própria**, sob articulação.

**A hipótese que este projeto carregava estava meio certa.** Partes moles em
articulação era o encaixe previsto; parede abdominal estava apontada para abdômen
**superior**, e é abdômen **total** — o que muda o unitário de R$ 99,94 para
R$ 100,18.

### L-002 — angiotomografia de coronárias · RESOLVIDA NA FONTE

**Fechada em 15/09/2026** com a coleta do Mapa Social da Saúde, em
`dados/fontes/mapa_social_tomografia.md`.

O painel de regulação guarda o campo `codigo_sigtap_solicitacao`, e nele
**ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO carrega o código
02.06.02.003-1 — TOMOGRAFIA COMPUTADORIZADA DE TÓRAX.**

A SES-DF já fatura o exame assim. Não é analogia deste plano: é o código do próprio
sistema. As 1.397 angiotomografias integram a linha do 02.06.02.003-1, que passa de
3.794 para **5.191 exames**.

**O que isso moveu no plano inteiro:** o objeto vai de 74.054 a **81.546 exames**, a
soma dos procedimentos de R$ 9.814.279,70 a **R$ 10.843.402,74** e o valor global a
**R$ 11.688.862,74**. O apoio, que não mudou de tamanho, caiu de 7,931% para
**7,233%**.

### L-003 — fichas SIGTAP · a parte crítica RESOLVIDA

**A quantidade máxima do 02.05.01.004-0 fechou em 15/09/2026.** A ficha diz 5 por
AIH/competência e acrescenta que **"estas quantidades de procedimento realizado
independem da quantidade de vasos estudados"**.

**Um doppler venoso bilateral de membros inferiores é um registro, não dois.** A linha
de 14.401 exames não dobra, e o risco de R$ 981.062,74 que este arquivo vinha
carregando não existe.

**O que continua aberto**, e não move dinheiro: idade mínima e máxima, sexo,
atributos complementares, CBO e habilitações de cada um dos doze códigos, na
competência vigente. Entram na seção 2 como condição de elegibilidade se alguma for
restritiva.

### L-004 — o contraste de tomografia · decidido fora, dúvida registrada

**Decidido em 15/09/2026: não entra.** A planilha lança apenas o valor do
procedimento declarado na tabela da portaria. O usuário pediu que a dúvida ficasse
registrada, e é o que este item faz.

O 02.06.03.004-5 CONTRASTE PARA TOMOGRAFIA COMPUTADORIZADA é criado pelo Anexo II
da mesma portaria: APAC secundário, R$ 60,00, quantidade máxima 1, compatível com os
treze procedimentos de tomografia do rol (Anexo IV). **Não está no Anexo I e
portanto não tem incremento.**

Onze mil trezentos e vinte e nove dos 13.452 exames de tomografia da fila pedem
contraste. A R$ 60,00 cada, são **R$ 679.740,00**.

**O que decidiu:** a descrição do Anexo II destina o valor "exclusivamente à
composição e ao cálculo dos créditos financeiros no âmbito da modalidade Crédito
Financeiro do Programa Agora Tem Especialistas", e a execução deste plano é por
convênio de emenda, não pelo componente de créditos.

**O que a decisão deixa em pé:** os 12.726 exames continuam exigindo contraste e o
executor continua comprando meio de contraste, agora **dentro do valor unitário do
exame**. Pela referência da própria portaria são R$ 679.740,00 — 6,9% da soma dos
procedimentos, absorvidos. **Isto vai à matriz de riscos da seção 8**, e é o item que
mais pesa lá.

**O que reabriria:** se a SES-DF orientar o registro do secundário na produção deste
convênio, ou se a análise da concedente pedir a composição do insumo, o item volta
com o número já calculado.

### L-005 — a fila por Região de Saúde · RESOLVIDA

**Fechada em 15/09/2026** com a coleta de ultrassonografia, que completou a de
tomografia.

O rateio foi calculado procedimento a procedimento — a distribuição territorial de
cada um aplicada ao quantitativo daquele procedimento na planilha — e somado:

| polo | participação | exames |
|---|---|---|
| Ceilândia | 40,56% | 33.073 |
| Sobradinho | 29,67% | 24.196 |
| Gama | 29,77% | 24.277 |

**Fora do território, 14,2% do universo** — contra os 44,2% que a tomografia sozinha
sugeria. A ultrassonografia quase não vem de URD nem de contratados, e é 84% do
objeto.

**Gama empatou com Sobradinho.** Só com a tomografia, o Gama aparecia em 21,18%.

### L-006 — o parque instalado não foi confirmado · muda o que a seção 6 declara

**Dono: usuário — não confirmado em 15/09/2026.**

O usuário declarou que o proponente já tem ultrassom e tomógrafo, e não conseguiu
confirmar quantas salas, quantos tomógrafos e em que turno.

**Consequência, e ela é de método:** o plano **não publica inventário de parque
instalado**. A seção 6 declara **capacidade requerida** — as 29.522 horas de sala que
a meta exige, e o número de salas que elas implicam em cada turno. É o que a
estrutura do `PADRAO.md` já chama de capacidade requerida, e é afirmação sobre a
execução, não sobre o patrimônio do proponente.

**O risco fica de pé e vai à seção 8:** se o parque real ficar abaixo de dez salas de
ultrassom em turno de dez horas, a meta de 81.546 exames em doze meses não é
executável no ritmo previsto. É o maior risco de execução do plano.

**Atualização de 02/11/2026, à tarde (usuário):** vão ser 20 salas de ultrassom e 5
tomógrafos, em 8 meses de produção. Pela conta por polo da carteira 1, as 20 salas ficam em 89%
com as faltas repostas e aguentam até 11% de faltas sem reposição; os 5 tomógrafos ficam em
70% (`estudos/estudo_filas_imagem_20261102.md`, seções 2 e 5). As salas e os tomógrafos das
clínicas continuam sem confirmação.

### L-007 — a parede abdominal no código do abdômen total, com a Candanga · ABERTA

**Dono: usuário, com a SES-DF. Aberta em 01/11/2026**, no ajuste de preço do plano 4
para a Tabela SUS Candanga (`output/estudo_imagem_candanga_20261101.md`, seção 6, e
`output/cenario_recomendado_imagem_20261101.md`).

A L-001 mostrou que a SES-DF registra a fila "ULTRASONOGRAFIA DE PAREDE ABDOMINAL" no
**02.05.02.004-6, abdômen total**. O plano 4 (v26, assinado) já a contou assim, a
R$ 100,18. Com a Candanga, o código paga **R$ 117,51**, e a parede vira o exame que
mais rende por hora: R$ 470, com 15 minutos.

**Por que ainda é dúvida:** o exame não é o mesmo. O abdômen total examina fígado, vias
biliares, pâncreas, rins e aorta; a parede abdominal examina só a parede (hérnia,
nódulo). O SIGTAP não tem código para a parede, e a SES usa o do abdômen total. Os 15
minutos são analogia com estruturas superficiais, porque o CBR não cita parede
abdominal.

**O que está em jogo:** 3.303 pedidos pendentes, R$ 388.135,53.

| se a SES… | a parede paga | efeito | compensação |
|---|---:|---:|---|
| confirmar o abdômen total | R$ 117,51 | nenhum | — |
| pedir o código de articulação (estrutura superficial) | R$ 70,97 | −R$ 153.721,62 | +1.330 Doppler de membros |
| não aceitar a parede no plano | — | −R$ 388.135,53 | +3.357 Doppler de membros |
| aceitar no plano e a auditoria glosar depois | R$ 0 | até −R$ 388.135,53, com o exame já feito | nenhuma |

**A tratativa:**
1. Pedir à SES-DF confirmação **por escrito** (e-mail ou despacho no SEI) de que a fila
   "Ultrassonografia de parede abdominal" é executada e faturada no 02.05.02.004-6, como
   ela a registra no SISREG, ao valor da Candanga.
2. No texto do plano, escrever o enquadramento às claras: a fila, o código e que o
   registro é o da SES-DF. Não esconder a parede dentro do abdômen total.
3. Guardar a resposta em `recebidos/`, numa subpasta própria, e fechar esta lacuna com
   a data e o documento.

**Sem a confirmação, a parede sai do plano** e o Doppler de membros sobe de 5.870 para
9.227 exames. O valor total continua fechando: a fila do Doppler de membros é de 12.041.

**Atualização de 02/11/2026, à tarde (usuário):** a parede abdominal é essencial para a
viabilidade da proposta e fica na carteira 1 (3.304 exames, R$ 388.253,04), com esta
confirmação pendente. A saída sem parede não é caminho principal, e a angio coronária não
entra no lugar. Se houver obstáculo, a reposição é decisão do usuário
(`estudos/estudo_filas_imagem_20261102.md`, seções 6 e 13).

### L-008 — um pedido, um plano: nenhuma sobreposição com o IEV e o redacao_07 · REGRA

**Aberta em 01/11/2026. Decisão do usuário: a sobreposição "não pode acontecer".** No
ajuste para a Candanga, o cenário ampliado de 01/11 usava filas que já têm dono. A regra
vale para qualquer cenário deste plano:

1. **Por código: as filas da carteira do redacao_07 (Emenda de Bancada) ficam fora.**
   - **Ultrassom:** bolsa escrotal 02.05.02.007-0, pélvica 02.05.02.016-0, globo ocular
     02.05.02.008-9, transfontanela 02.05.02.017-8, obstétrica 02.05.02.014-3 e obstétrica
     com Doppler 02.05.02.015-1.
   - **Tomografia:** pescoço 02.06.01.005-2, crânio 02.06.01.007-9, face/seios/ATM
     02.06.01.004-4 e sela túrcica 02.06.01.006-0.
   - **Outros:** mamografia e densitometria.
   - **A recíproca já vale:** o redacao_07 não usa código do plano 4
     (`planos/redacao_07/estado.yaml`, `fora_do_plano_4`).
2. **Pelas OCI de ortopedia do IEV:**
   - **Ficam fora inteiras:** as TC de coluna (02.06.01.001-0, 002-8 e 003-6), de
     articulações de membro superior e inferior (02.06.02.001-5 e 02.06.03.002-9) e de
     segmentos apendiculares (02.06.02.002-3). Elas são compatíveis com a OCI 09.03.01.003-8,
     e o redacao_07 já as tirou por decisão do usuário de 20/10/2026.
   - **A TC de pelve (02.06.03.003-7) também é compatível com a 09.03.01.003-8.** Ela fica
     no plano, mas sem os pedidos com CID da OCI. Em 27/10 eram 7 em 5.944 pedidos de TC
     (`output/mapeamento_iev_20261026.md`).
   - **Se a US de articulação (02.05.02.006-2) voltar ao plano,** entra sem os pedidos com
     CID da OCI 09.03.01.002-0: cerca de 781 em 27/10.
3. **As partes moles ficam fora inteiras** (02.05.02.006-2, fila "ECOGRAFIA DE PARTES
   MOLES"): são do IEV, por decisão do usuário.
4. **A cardiologia (redacao_08) não se sobrepõe:** as OCI 09.02.01.002-6, 003-4 e 007-7
   usam eco, ECG, teste ergométrico e radiografia, e nenhuma usa US ou TC deste plano.
5. **Como se garante:**
   - A ordem de coleta da nova medição leva a exclusão por código e por CID.
   - A meta de cada fila é a fila **sem** esses pedidos.
   - O enquadramento do plano (`dados/enquadramento_mapa_social.json`) marca as filas
     excluídas, com o motivo.
   - Antes do protocolo, conferir as filas deste plano contra as do redacao_07 e as do IEV.
     Nenhum nome de fila pode aparecer nos dois.

**Revista em 02/11/2026, por decisão do usuário** (estudo das filas de imagem,
`estudos/estudo_filas_imagem_20261102.md` e `estudos/estudo_outros_planos_imagem_20261102.md`):

- **O item 1 deixa de valer.** O redacao_07 está no campo das ideias e não cobre fila. Só
  contam os planos aprovados. Se o redacao_07 avançar, ele exclui o que o plano 4 tomar.
- **A US de articulação (02.05.02.006-2) fica fora inteira:** fila comprometida com o IEV.
  - O plano do IEV (pt_ses_02) põe entre os objetivos reduzir as filas reguladas de exame de
    ultrassom.
  - A regulação da SES pode encaminhar pedidos da fila do exame às 19.070 OCI 09.03.01.002-0.
  - O CID registrado na APAC pode ser outro que o do pedido.
  - Até 26/10, nenhum agendamento dessa fila tinha ido ao IEV, mas isso é como a regulação vem
    operando, e não uma regra.
- **Na transvaginal, 4.000 pedidos ficam reservados para a OCI GIN1 do IEV** (3.218 OCI, com
  folga de faltas). A medição de 02/11 achou 3.068 pedidos com os 37 CID da GIN1. O plano 4
  conta só com o resto da fila.
- **A TC de pelve continua no plano,** sem os pedidos com CID da OCI 09.03.01.003-8 (7 em 02/11).
- **A perguntar de novo à regulação da SES:** os pedidos das filas de exame (US de
  articulação e transvaginal) são encaminhados às OCI do IEV? Na primeira conversa, a SES pediu
  para evitar a sobreposição. Com a resposta por escrito, a articulação pode voltar ao plano,
  sem os pedidos reservados ao IEV.

---

## Decisões

### D-001 — a direção do dimensionamento · TRAVADA

**Decidida em 15/09/2026: a fila define o valor.** Sem teto prévio. O valor global é
a soma dos procedimentos mais o apoio montado de baixo para cima — R$ 11.688.862,74
com os 81.546 exames de código fechado.

### D-002 — a base dos 8% · TRAVADA

**Decidida em 15/09/2026: por dentro.** Os 8% são do valor global, não da soma dos
procedimentos — o que os torna teto de R$ 942.904,59, resolvida a circularidade. O
apoio realizado ficou em R$ 845.460,00, abaixo dele.

### D-003 — o quadro do apoio · SUBSTITUÍDA PELA D-005 (20/10/2026)

**Decidido em 15/09/2026**, em três rodadas. A equipe é maior do que os três cargos
nomeados; usa os cargos e funções dos planos aprovados; e não passa de 8%. Na última
rodada o usuário fixou os quantitativos: **seis operadores de registro, seis
assistentes administrativos, a diferença para a assessoria e, havendo margem, dois
coordenadores.**

**Os dois últimos pedidos não cabiam juntos** — duas coordenações a R$ 10.500 com a
assessoria ao preço do acervo dão 8,035%. O arranjo adotado mantém os dois
coordenadores e deixa a assessoria no preço do acervo: **Coordenação Administrativa
R$ 10.500, Coordenação Financeira R$ 9.500, seis operadores, seis assistentes e a
Assessoria de Prestação de Contas a R$ 5.455** — R$ 845.460,00 em doze meses,
**7,233% do global**. Todos os cinco preços têm procedência literal no acervo.
Aritmética em `dados/apoio_proposta.md`.

**O que a decisão do usuário mudou nas premissas:** seis operadores comportam 7,35
minutos por registro, contra os 8 minutos que o plano 3 usou. O número de postos veio
dele; o tempo por exame é o que esse número implica.

**A recepção ficou fora**, e a aritmética é que decidiu: o fluxo pede cinco
recepcionistas, R$ 16.000,00 por mês, e a folga até o teto é de R$ 663,00. Ela fica
dentro do valor unitário, que aqui é tabela mais incremento e por isso remunera o
episódio inteiro.

**O que reabriria:** se a análise da concedente entender que recepção e entrega de
laudo são rubrica, o apoio vai a mais de 10% e o teto de 8% é que precisa mudar — não
os postos.

### D-005 — o quadro de gestão da v24 · DECIDIDO

**Decidido em 20/10/2026: o cenário 3, com o preço proposto.** Direção Executiva, três
coordenações (Administrativa e Financeira, Operacional e Assistencial), três supervisores de
polo, oito operadores de registro, seis assistentes e a assessoria de prestação de contas:
R$ 954.560,00 em 8 meses, **8,23% do valor global**, 79.152 exames.

**O que a decisão mudou:** o apoio passa do teto de 8% da D-002, e fica na faixa de 8% a
8,5% do LI-038. A fila extraída fica inteira; o acréscimo além dela cai de 801 para 580
exames. As coordenações Administrativa e Financeira e Operacional vão a R$ 8.400, o custo
de mercado no DF; as outras seis rubricas ficam com o preço de hoje.

**Os outros cenários, para registro:** 2 coordenações e 10 operadores dariam 8,10%; 3
coordenações e 6 operadores, 7,64%. O usuário achou 6 operadores carga alta demais.

**Onde está:** os números no bloco `v24_em_preparo_20261020` do `estado.yaml`; a regra de
preço e os arquivos em `calculo_v24/README.md`; a planilha em
`dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx`. Ainda não foi ao plano: faltam
os polos e a tomografia.

### D-006 — os seis polos e os dois planos de tomografia · DECIDIDO

**Decidido em 20/10/2026.** Seis polos, um por Região de Saúde, com a Central e a Centro-Sul num polo comum. Os
critérios foram demanda, distância, transporte público e a rede de clínicas que já existe, e o estudo está em
`estudos/estudo_polos_rede_capacidade_20261020.md`. Há uma unidade de ultrassom por polo. A tomografia sai em dois planos:

- **v24a**, nos seis polos, um tomógrafo por polo, com o excedente da Sudoeste absorvido no polo da Oeste;
- **v24b**, em rede, sem número de tomógrafos nem distribuição por polo. Internamente são cinco polos, e a Leste fica
  sem.

Os operadores ficam divididos: 4 no pré-exame e 4 no pós-exame. Os assistentes passam a apoio administrativo e
documental.

**O que falta confirmar com a rede**, a confirmar pela equipe com a planilha `dados/rede_imagem_6_polos_20261020.xlsx`:
- as salas de Samambaia (6) e do Gama (5);
- o tempo real por exame;
- uma clínica de tomografia na Central e Centro-Sul, e outra na Leste no plano A;
- o mínimo por clínica.

**Em aberto no texto:** a 4.14 diz que a execução não é subcontratada, mas a tomografia está negociada por exame. Fica
com o jurídico do ISHP.

### D-009 — só ambulatório: nenhuma fila de emergência · DECIDIDO

**Decidido em 01/11/2026 pelo usuário**, no ajuste de preço para a Candanga: "não podemos atender emergência,
apenas ambulatório".

- **O que sai da v26:** a fila "TC DO TORAX ADULTO S/CONTRASTE S/SEDACAO EMERGENCIA", com 728 exames.
  Ela vale R$ 218.472,80 pela Portaria (R$ 300,10) e R$ 225.134,00 pela Candanga (R$ 309,25). Era a única fila de
  emergência do plano.
- **O que não entra como complemento:** nenhuma fila com "EMERG" no nome. Nos três códigos de TC do plano, são
  2.626 pedidos (29/10/2026): abdômen e pelve, com e sem contraste, e tórax com contraste.
- **O que sobra de TC ambulatorial** nos três códigos, fora das filas do plano: 2.113 pedidos. São
  angiotomografias (aorta, tórax, abdômen, pelve, carótidas, renais e porta) e TC eletiva sem contraste. Somam-se
  123 de angiotomografia de coronárias além da meta da v26. As filas com sedação também ficam fora.
- **Consequência:** sem emergência, a diferença de preço não cabe inteira em TC se cada meta ficar limitada à fila
  de hoje. As duas versões estão em `output/plano4_mais_tc_ambulatorio_20261101.md`.

### D-010 — crianças entram, sem limite de idade no plano · DECIDIDO

**Decidido em 09/11/2026 pelo usuário:** "vamos atender crianças também, não acho que seja um problema. No plano vamos
deixar abrangente, sem restringir idade."

- **O que entra:** as filas infantis de ultrassom que já estavam na carteira 1. São abdômen total (452), aparelho
  urinário (276), bolsa escrotal (234) e tireoide (60). A pélvica infantil fica fora junto com a de adulto (decisão
  de 09/11).
- **O que não muda:** a transfontanela segue fora (saiu em 03/11, a pedido do usuário).
- **No texto:** o plano não restringe idade. Fecha a dúvida aberta no estudo das filas de 02/11 (seção 12).
- **Na mesma conversa:** a TC na clínica a R$ 175, mais R$ 50 com contraste; a US pélvica ginecológica fora da conta;
  as angiotomografias de volta, menos a de coronárias. A conta está em
  `estudos/estudo_readequacao_candanga_margem_20261109.md`.

### D-011 — o Doppler de membros dos dois lados só entra se contar como dois exames · CONDIÇÃO

**Dito pelo usuário em 10/11/2026,** na revisão dos exames candidatos: o Doppler de membros dos dois lados só vale a
pena se pagar o dobro de um Doppler comum, ou seja, se for possível lançar dois exames por pedido.

- **Por quê:** ele ocupa a sala e o médico por 40 minutos pelo mesmo preço do Doppler de carótidas, de 20 minutos
  (R$ 115,61). Com o médico pago por hora, a margem é de 0,5%
  (`estudos/estudo_readequacao_candanga_margem_20261109.md`).
- **O que a ficha diz hoje:** o bilateral é um exame só. A descrição do 02.05.01.004-0 diz que a quantidade
  "independe da quantidade de vasos estudados", e nenhuma regra trata de lado (L-003 e
  `dados/fontes/sigtap_0205010040_102026.md`). A ficha admite até 5 registros por paciente por competência, mas como
  teto, e não como regra de multiplicar. Quem aceita ou não dois registros no mesmo dia é o gestor e a auditoria.
- **O que falta para a condição valer:** a SES dizer por escrito que o pedido da fila "Doppler venoso — MMII
  (bilateral)" pode ser registrado como dois procedimentos. Sem isso, o exame fica fora.
- **Se a SES aceitar:** cada pedido passa a valer R$ 231,22, e a fila de 12.043 pedidos (02/11) consome o dobro do
  valor.

### D-012 — a carteira final, exame a exame · EM DECISÃO

**Aberta em 10/11/2026.** O usuário revê os 27 exames candidatos da planilha de 09/11
(`estudos/estudo_readequacao_candanga_margem_20261109.xlsx`, aba 1) e decide um a um. Filas da coleta de 02/11.

| # | exame | fila | decisão | motivo |
|---|---|---:|---|---|
| 10 | Doppler de membros, os dois lados | 12.043 | condicionado | só se contar como dois exames (D-011) |
| 19 | TC de pescoço com contraste | 479 | **entra** | mesmo preço e custo das TC grandes; perfil oncológico |
| 20 | Angiotomografias, sem coronárias e sem crânio | 1.962 | **sai** | dá muito trabalho (usuário). Muda a decisão de 09/11, registrada na D-010, de que elas voltavam |
| 25 | TC de face e seios da face com contraste | 139 | **sai** | não vale executar: margem de 13%, fila pequena |
| 26 | TC de crânio com contraste | 372 | **sai** | não vale executar: margem de 10%; a SES agenda 1.909 por ano |
| 27 | Angiotomografia do crânio | 385 | **sai** | não vale executar: margem de 10% e a maior exigência |
| — | US de articulação, só o que nunca vira OCI de ortopedia: partes moles, região inguinal, pescoço e cervical, axila e as filas infantis de quadril de bebê e coluna lombar (as de joelho, punho, tornozelo e cotovelo infantis são ortopedia e ficam fora) | 4.557 (02/11) | **entra** | 11/11: a OCI 09.03.01.002-0 do IEV é de ortopedia, e nódulo, lipoma, hérnia e displasia do quadril não são. Muda a decisão de 01/11 de que as partes moles eram do IEV (L-008, item 3). As filas de articulação de adulto (ombro, punho, joelho, tornozelo, cotovelo, mão, pé) seguem fora |
| — | US pélvica ginecológica, adulto e infantil | 1.014 | **fora** | 11/11, confirma a decisão de 09/11: a Candanga paga R$ 43,41 e o exame de 15 min custa R$ 44,99 (médico por hora), então cada exame dá prejuízo; com o médico por exame, o prejuízo cresce. A fila inteira vale só R$ 44 mil. A infantil é quase toda de puberdade precoce (E30) e pede prática com criança |

Os demais candidatos seguem em aberto.

### D-008 — a v26: plano de trabalho de convênio, da proposta certa · DECIDIDO

**Decidido em 21/10/2026**, para enviar o plano à SES-DF. O usuário pediu: o 1.8 com o texto da SUCONV, a proposta
certa, plano de trabalho e não pré-plano, as adequações para convênio e, se preciso, o Ofício 40.

- **a proposta:** o Ofício 387/2026 SES/GAB/ARINS, que a capa citava desde a v6 da equipe, é da proposta
  36000722999202500 (R$ 1.502.687,00, a do `redacao_07`). A do plano 4 é a 36000720055202500 (R$ 11.592.762,00), com
  indicação do ISHP pelo Ofício 40/2026 (`dados/fontes/oficios_bancada_20260922/`). A capa passa a citar a proposta e
  o Ofício 40; saem as remissões ao 387 na 3.3, na 3.6 e na 4.1. Ofício da ARINS próprio desta proposta não há no
  acervo (P-02 do `redacao_06`);
- **convênio (LI-026):** o 1.8 com o texto que a SUCONV escreveu no pré-plano de otorrino (`redacao_05`), o mesmo dos
  pré-planos 06 e 07; a 3.3 diz que o instrumento é o convênio, pelo Decreto 48.727/2026, sem a alternativa do Termo
  de Fomento; "formalização do convênio" no lugar de "formalização do instrumento"; "parceria" sai da prosa (fica só
  no nome do modelo da SES e no histórico do ISHP, na 3.11);
- **números:** nenhum muda.

**Onde está:** `calculo_v26/` (`aplicar_v26.py`, `gerar_v26.sh`); `versoes/plano_v26_20261021`; cópia marcada sobre a
v25A em `dados/v26_marcado_20261021.docx`. Ainda falta, pelo modelo de convênio de 21/10 (`recebidos/`), o que o LEIA
de lá lista: partícipes, acompanhamento, processo SEI, versão e data, LGPD e o mapa de riscos do Anexo XXIII.

### D-007 — o quadro de 21/10 e a v25A · DECIDIDO

**Decidido em 21/10/2026**, depois da orientação do professor, que achou que três coordenações não se justificam com
supervisores de polo e que a conta deve ficar com seis polos de tomografia (cinco, se for o caso, só na execução):

- **quadro:** Direção Executiva, Coordenação Assistencial e Coordenação Administrativa e Financeira (sai a
  Operacional), três supervisores de polo a R$ 6.155 (um para dois polos), dez operadores de registro (cinco no
  pré-exame, cinco no pós-exame), seis assistentes e a assessoria: R$ 956.160,00 em 8 meses, 8,25% do valor global,
  79.144 exames. Com seis supervisores ou com três coordenações, o quadro passa do teto de 8,5%;
- **funções:** a Assistencial assume polos, agendas, redistribuição entre polos, supervisores e o pré-exame; a
  Administrativa e Financeira, o pós-exame e os assistentes, com as atribuições do pt_ses_01 (ISHP, Convênio
  030989/2026, item 1.1.2) e do pt_ses_02 (IEV, Convênio 030975/2026, itens 1.1.2, 1.1.4 e 1.1.5);
- **texto:** o polo de cada solicitação é definido pela regulação da SES-DF, em regra pela Região da unidade
  solicitante (é o campo `regiao_saude_solicitante` do Mapa Social), e não pelo domicílio; a ultrassonografia em horas,
  sem salas por polo (as salas saem do tempo real de cada polo, conferido no mês 1); sem o parágrafo de absenteísmo,
  que é tratamento interno; linguagem revista; remissões "(subseção X)";
- **tomografia:** a v25A, com seis tomógrafos dimensionados um por polo e a regra da 4.2 que deixa a tomografia de um
  polo ser feita em outro polo da rede. A v25B, que só publica a carga de 3,33, fica em `versoes/` como alternativa.

**Onde está:** `calculo_v25/` (`calculo_v25.py`, `aplicar_v25.py`, `gerar_v25.sh`, `registrar_v25.py`);
`versoes/plano_v25a_20261021` e `_v25b_`; cópias marcadas sobre a v24A em `dados/v25a_marcado_20261021.docx` e `_v25b_`.

### D-004 — o que mais falta para a fase 0 fechar

Sem lastro, nada disto entra no documento:

| parâmetro | estado |
|---|---|
| proponente — razão social, CNPJ, endereço, CNES | `[preencher]` · o usuário mandou seguir sem, em 15/09/2026 |
| origem do recurso | **emenda parlamentar federal** · falta autor, número e RP |
| vigência em meses | **12** · travado em 15/09/2026 |
| local de execução | **polos múltiplos** · travado em 15/09/2026; falta quantos e quais |
| capacidade instalada | **proponente já possui US e tomógrafo** · travado em 15/09/2026 |
| distribuição da fila por Região de Saúde | `[preencher]` · **L-005** |
| data da extração da fila | **10/09/2026, quinta-feira** · falta o sistema de origem |
| capacidade instalada — salas, equipamentos, turnos | **não confirmável** · **L-006**, e o plano declara capacidade requerida |
| número, nome e cobertura dos polos | **3 — Ceilândia, Sobradinho, Gama** · travado em 15/09/2026 |
| meses de produção dentro da vigência de 12 | `[preencher]` · 11 ou 12 decide a curva |
