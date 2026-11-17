# Estudo — quantas pessoas cabem, pela porta de entrada

**Controle interno.** Estudo de 27/10/2026 para o redacao_08: Emenda 41360018/2024, do Senador
Izalci Lucas, R$ 2 milhões; executor Instituto Fazer o Bem, Faz Bem. Aplica as decisões do
enquadramento de hoje (`planos/redacao_08/dados/enquadramento_mapa_social.json`) à medição feita
depois delas. A escolha é sua.

**A medição:** `planos/redacao_08/dados/fontes/mapa_social_20261027_porta.md`, recarga do painel
de 27/10/2026 16:32, conferência 10/11.
- O item que caiu (I, os três números) é falha do conferidor. Ele acha a linha da OCI pelos
  últimos cinco caracteres do id, e a "006-9 caso 2 IC ampliada" casou com a linha da "caso 1 IC
  ampliada".
- Conferi as duas linhas no `.md`, e os números batem com o JSON.

**O que ficou de fora:** o risco cirúrgico por estabelecimento. O kit não mede essa dimensão e
precisa de uma mudança.

## 1. Como se conta

Disponíveis em 12 meses = **fila viva − o que o IEV ainda vai fazer + 12 × (o que entra − o que a
rede agenda)**. É a mesma conta da planilha de imagem. No ritmo de hoje, quando a rede agenda
mais do que entra, a parcela do fluxo fica em zero. Nos cenários da seção 3, ela é negativa e a
fila diminui.

**A rede vai em dois ritmos:**
- **hoje:** a média de 07 a 09/2026, com o IEV dentro;
- **antes do IEV:** a média de 10/2025 a 04/2026, ou até 06/2026 no risco cirúrgico, que o IEV
  só começou em 07/2026. É o ritmo para quando o IEV sair (05/2027).

O que a pessoa paga é o SIGTAP:
- 003-4, R$ 270,00;
- 006-9, R$ 350,00;
- 002-6, R$ 200,00;
- 007-7, R$ 130,00.

Os dois casos da porta:
- **caso 1:** só a consulta com o CID;
- **caso 2:** a consulta e os exames obrigatórios com o CID, cada pessoa uma vez. Na linha
  coronária, só o eletrocardiograma e o ergométrico.

## 2. Cada fila

| fila | caso | pessoas (viva) | entram/mês | rede hoje · antes do IEV | o IEV ainda faz | **disponíveis em 12 meses** | falta |
|---|---|---|---|---|---|---|---|
| 003-4 coronária (I20 a I25) | 1 | 2.023 (1.617) | 213 | 206 · 131 | — | **1.692 a 2.596** | 24% |
| 003-4 coronária (I20 a I25) | 2 | 2.816 (2.105) | 372 | 365 · 286 | — | **2.182 a 3.132** | 29% |
| 006-9, I50 | 1 | 2.079 (1.794) | 193 | 143 · 108 | cerca de 760 | 1.626 a 2.055 | 29% |
| 006-9, I50 com I11.0, I13.0 e I13.2 | 1 | 2.120 (1.824) | 196 | 146 · 109 | cerca de 760 | **1.672 a 2.109** | 29% |
| 006-9, ampliada (com I42 e I43) | 1 | 2.280 (1.957) | 208 | 155 · 115 | cerca de 760 | 1.833 a 2.315 | 29% |
| 006-9, I50 | 2 | 4.675 (2.629) | 281 | 205 · 172 | cerca de 760 | 2.784 a 3.178 | 32% |
| 006-9, I50 com I11.0, I13.0 e I13.2 | 2 | 4.734 (2.667) | 286 | 208 · 174 | cerca de 760 | **2.834 a 3.248** | 32% |
| 006-9, ampliada | 2 | 5.162 (2.879) | 309 | 229 · 187 | cerca de 760 | 3.083 a 3.582 | 32% |
| 002-6, pelo eletrocardiograma | — | 345 (227) | 30 | 29 · 14 | — | **234 a 409** | 35% |
| risco cirúrgico inteiro (P-08) | — | 9.654 (8.170) | 704 | 796 · 291 | 1.825 | **6.345 a 11.310** | 38% |

**O que a tabela mostra:**
- **Na 003-4, o I21 a I24 pesa.** Pela consulta, com I20 e I25, eram 1.436 pessoas (medição das
  OCI de hoje). Com I20 a I25, são 2.023: 587 a mais.
- **Na 006-9, as três versões do CID ficam perto:**
  - I11.0, I13.0 e I13.2 juntam só 41 pessoas (2.079 a 2.120);
  - as cardiomiopatias, mais 160 (até 2.280).
- **No caso 2 da 006-9, quase metade da fila é velha:** 2.046 das 4.675 pessoas só têm pedido de
  antes de 2024, sobretudo no Holter. A fila viva cresce menos (de 1.794 para 2.629).
- **O risco cirúrgico depende de quem mais vai atender** (seção 3).

## 3. O risco cirúrgico em três cenários

| cenário | rede por mês | disponíveis em 12 meses |
|---|---|---|
| o IEV termina as 1.825 e sai; ninguém entra no lugar | 291 | **cerca de 11.300** |
| entra só o Hospital de Ceilândia (115 por mês) | 406 | cerca de 9.900 |
| entra só a HAPVIDA (792 por mês) | 1.083 | cerca de 1.800 |
| entram os dois (907 por mês) | 1.198 | **cerca de 400** |

A rede de hoje (796 por mês) é a do IEV no auge, e ela acaba com o contrato dele. As duas
propostas são da planilha do Agora Tem Especialistas de 03/09/2026: aprovadas, sem data de início.

## 4. O total

Com a versão do meio da 006-9 (I50 com I11.0, I13.0 e I13.2). A primeira linha de cada caso é
com a rede no ritmo de hoje; a segunda, com a rede como antes do IEV.

| caso | com a P-08 | pessoas | custo pelo SIGTAP | o recurso (R$ 1,8 milhão) |
|---|---|---|---|---|
| 1 | sim | 9.943 | R$ 1.913.690,00 | **falta R$ 114 mil** |
| 1 | sim | 16.424 | R$ 2.990.948,00 | falta R$ 1,19 milhão |
| 1 | **não, ou com a HAPVIDA e Ceilândia** | 3.598 a 4.015 | R$ 1,09 a 1,14 milhão | **sobram R$ 660 a 710 mil** |
| 2 | sim | 11.595 | R$ 2.452.690,00 | falta R$ 653 mil |
| 2 | não | 5.250 | R$ 1.627.840,00 | sobram R$ 172 mil |

**O que isso diz:**
- **Com a P-08, o recurso é o limite, nos dois casos.** A emenda não atende tudo o que há, e a
  ordem de prioridade decide quem fica.
- **Sem a P-08, ou se a HAPVIDA e o Hospital de Ceilândia começarem, a fila é o limite no caso
  1.** Sobram R$ 660 a 710 mil, que só o caso 2 (os exames obrigatórios) ou outra linha usaria.
- **O caso 2 só vale se a SES aceitar converter pedido de exame em OCI.** Sem isso, a conta é a
  do caso 1.
- **A falta não entra na meta** (sua decisão de 21/10). Na execução, ela decide a agenda: com 38%
  no risco cirúrgico, cada 100 realizadas pedem uns 160 agendamentos.

## 5. O que falta

1. **A SES,** com quatro perguntas:
   - a P-08;
   - converter pedido de exame em OCI (o caso 2 e a porta da 002-6);
   - quando começam a HAPVIDA e o Hospital de Ceilândia;
   - o que o IEV ainda vai fazer na 006-9 e na 004-2.
2. **A versão do CID da 006-9:** a diferença entre as três é de 41 a 201 pessoas.
3. **O risco cirúrgico por estabelecimento:** pede incluir no kit a dimensão do estabelecimento.
4. **O conferidor:** o item I tem de achar a linha pelo id inteiro, e não pelos últimos cinco
   caracteres.
5. **A planilha da carteira,** como a de imagem, com a prioridade de cada linha e os cenários do
   risco cirúrgico.
