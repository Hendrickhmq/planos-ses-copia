# Plano 4 em 12 meses, com 6 polos de ultrassom e 3 de tomografia: o que muda

Estudo interno de 07/11/2026. Ele responde a um pedido da equipe, trazido pelo usuário: passar a execução para 12 meses,
manter 6 polos de ultrassom e pôr a tomografia em 3 polos, para negociar volume com a clínica parceira. O contraste
trouxe um problema de tempo que ainda não estava mapeado.

**Segunda parte, no mesmo dia,** a pedido do usuário:
- a gestão e o apoio ficam no valor de hoje, ou sobem pouco, até 8,5% do valor global, com readequação de salários;
- o fluxo de atendimento de cada procedimento, com o preparo do contraste feito em paralelo;
- os meses que a tomografia leva com 3, 4 ou 5 tomógrafos, lembrando que o radiologista vai fazer sem contraste parte
  dos pedidos com contraste.

**Base de comparação:** a carteira 1, escolhida em 02/11 e revista em 03/11, sem a transfontanela. Ela tem 79.533 exames
pela Candanga, 20 salas e 5 tomógrafos em 8 meses. O quadro de gestão é o da v26 assinada.

**Arquivos:**
- a planilha `estudo_12_meses_3_tomografos_20261107.xlsx`, com dez abas. Tudo nela é fórmula, e as células amarelas são
  premissas que podem ser mudadas;
- o gerador `gerar_estudo_12_meses_3_tomografos_20261107.py`.

Nada daqui vai ao plano sem decisão do usuário.

---

## Resposta curta

1. **Os 4 meses a mais aumentam a gestão em 50%.** Sem readequar, o apoio vai de R$ 956.160 para R$ 1.434.240, e de
   8,25% para 12,37% do valor global.
2. **Para ficar no teto, o custo por mês da gestão precisa cair um terço:**
   - 33,3% para o apoio ficar igual ao de hoje;
   - 31,3% para caber em 8,5%, o que permite R$ 29.225 (+3,1%) a mais que hoje.
3. **Readequar só os salários não serve.** Cortar 31% em todos os cargos (P1) põe 6 dos 8 abaixo do menor preço já
   aprovado pela SES-DF, e os 7 que têm comparação de mercado ficam abaixo dele.
4. **A recomendação (P2) combina menos postos e preços dos aprovados.**
   - O apoio fica em **R$ 978.120 (8,44%)**: R$ 21.960 (+2,3%) a mais que hoje, e 163 exames a menos.
   - O custo por mês cai 31,8%: 21,3% por ter menos postos e 13,3% pela readequação dos salários.
   - Nenhum preço fica abaixo do menor aprovado, e a carga por operador fica abaixo da de hoje.
5. **O fluxo em linha resolve o problema do contraste.** Com o acesso venoso feito numa sala de preparo, e dois pacientes
   prontos à espera, o exame com contraste ocupa o tomógrafo cerca de **13 minutos, e não 20** (35% a menos). O tempo
   real precisa ser medido no mês 1.
6. **Com o fluxo em linha, 3 tomógrafos sobram em 12 meses.** Fazem toda a tomografia em **6 meses**, ou correm os 12
   meses com cerca de **5 horas por dia** cada. No fluxo em série, levam 9,2 meses com 20 minutos por exame e não fecham
   com 30 minutos.
7. **A conversão para sem contraste ajuda pouco no tempo,** de 0,1 a 0,2 mês a cada 10% convertidos, mas poupa contraste,
   punção e risco de reação. O código SUS é o mesmo e paga o mesmo.
8. **No ultrassom, o preparo fora da sala reduz as horas de sala em 18%.** Em 12 meses bastam 13 salas, contra 15 sem
   esse preparo e 20 hoje. A Leste fica no limite com 1 sala; com 2, são 14.
9. **Custo de executar:** sobe cerca de R$ 260 mil em 12 meses (salas, aparelhos e recepção), sem contar os itens ainda
   sem preço. O que é pago por exame não muda.

---

## 1. Gestão e apoio em 12 meses, dentro do teto

### 1.1 Os 4 meses a mais, em porcentagem

| | valor | % |
|---|---:|---:|
| meses a mais | 4 | +50% de vigência |
| apoio de hoje, 8 meses | R$ 956.160 | 8,25% do global |
| o mesmo quadro e os mesmos salários por 12 meses | R$ 1.434.240 | +50% sobre hoje |
| custo por mês de hoje | R$ 119.520 | |
| custo por mês que mantém o apoio de hoje | R$ 79.680 | −33,3% |
| custo por mês no teto de 8,5% | R$ 82.115 | −31,3% |
| quanto o teto permite a mais sobre o apoio de hoje | R$ 29.225 | +3,1% |

### 1.2 Os cenários

Os preços são o custo total por mês, com encargos. Por isso férias e 13º proporcionais já estão dentro do preço.

| cenário | postos | por mês | em 12 meses | do global | sobre hoje | exames | carga por operador | abaixo do mercado | abaixo do menor aprovado |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hoje (v26, 8 meses) | 22 + assessoria | R$ 119.520 | R$ 956.160 | 8,25% | — | — | 994 | 4 | 0 |
| A. sem readequar | 22 + assessoria | R$ 119.520 | R$ 1.434.240 | 12,37% | +50,0% | −3.574 | 663 | 4 | 0 |
| P1. o mesmo quadro, salários cortados por igual | 22 + assessoria | R$ 82.115 | R$ 985.385 | 8,50% | +3,1% | −217 | 663 | 7 | 6 |
| **P2. quadro pelo volume, preços dos aprovados** | **16 + assessoria** | **R$ 81.510** | **R$ 978.120** | **8,44%** | **+2,3%** | **−163** | **947** | **4** | **0** |
| P3. salários de hoje, menos postos | 13 + assessoria | R$ 80.510 | R$ 966.120 | 8,33% | +1,0% | −73 | 1.326 | 4 | 0 |

**Como ler as colunas:**
- **exames** é quanto o apoio tira da produção, no valor médio de R$ 133,74 por exame;
- **carga por operador** é em exames por operador de registro por mês;
- **abaixo do mercado** compara com o custo para a empresa, em Brasília, da ocupação que faz o mesmo trabalho
  (salario.com.br, levantado em 20/10). Hoje já são 4 cargos abaixo: Direção, Coordenação Assistencial, Supervisão e
  Assistente.

### 1.3 A P2, cargo a cargo

| cargo | hoje | P2 | de onde vem o preço da P2 |
|---|---|---|---|
| Direção Executiva de Projeto | 1 × R$ 14.500 | 1 × **R$ 10.200** | pt_ses_02, Convênio 030975/2026, IEV, Direção Executiva (16 meses) |
| Coordenação Assistencial | 1 × R$ 10.500 | 1 × **R$ 8.400** | igual à Coordenação Administrativa e Financeira, para a direção continuar acima das coordenações. É o custo de mercado de um gerente (R$ 8.371) e está dentro da faixa de coordenação dos aprovados (R$ 6.000 a R$ 10.500) |
| Coordenação Administrativa e Financeira | 1 × R$ 8.400 | 1 × R$ 8.400 | não muda |
| Supervisão de Polo Assistencial | 3 × R$ 6.155 | **2** × R$ 6.155 | pt_ses_01, Convênio 030989/2026, ISHP. Passa a 1 supervisor para 3 polos; o pt_ses_01 tem 1 para 2 |
| Pré-exame: agenda, contato, confirmação e busca ativa | 5 × R$ 4.300 | **4 × R$ 3.200** | pago pela função de contato, como o Assistente Administrativo do IEV (pt_ses_02, 03 e 04). O mercado de quem faz contato e confirmação por telefone é R$ 3.156. Na P2 o posto passa a se chamar assistente de agendamento, confirmação e busca ativa |
| Pós-exame: TrakCare e APAC | 5 × R$ 4.300 | **3** × R$ 4.300 | pt_ses_02 e 04, IEV, Operador de registro de sistemas |
| Assistente Administrativo (documentação) | 6 × R$ 3.200 | **4** × R$ 3.200 | pt_ses_02, 03 e 04, IEV |
| Assessoria de Prestação de Contas | R$ 5.455 | **R$ 3.700** | pt_ses_05, Convênio 031061/2026, ISHP (leitura por OCR). Em 12 meses dá R$ 44.400, quase o total da v26 (R$ 43.640): o trabalho dela é por prestação de contas, e não por mês |
| **por mês** | **R$ 119.520** | **R$ 81.510** | |

**Por que esses postos podem cair.** Os exames são os mesmos; em 12 meses, o volume de cada mês cai para 2/3, e os
postos que acompanham o volume caem junto:
- operadores: 10 × 8 meses = 80 operador-mês viram 7 × 12 = 84;
- assistentes: 6 × 8 = 48 viram 4 × 12 = 48.

Direção e coordenações são presença e ficam.

**Por que a P1 não serve.** Ela corta 31% de todos os cargos. Os 7 que têm comparação de mercado ficam abaixo dele, e 6
ficam abaixo do menor preço que a SES-DF já aprovou: a Direção iria a R$ 9.962, o operador a R$ 2.954 e o assistente a R$ 2.198. É difícil
contratar por esses valores, e eles ficam sem procedência no acervo.

**A P3 é o outro extremo.** Ela mantém os salários de hoje e corta postos. Fica em 8,33%, mas a carga por operador sobe
a 1.326 exames por mês. Em 20/10, você achou alta demais a carga de cerca de 1.650.

**Reajuste de salários.** Em 12 meses é mais provável que a data-base caia dentro da vigência. O convênio fixa o custo
por mês, então o aumento fica com o ISHP: cerca de R$ 23 mil na P2, com 5% de reajuste a partir do 7º mês. O mês e o
percentual são premissas a confirmar na convenção coletiva de cada cargo.

## 2. Fluxo de atendimento

A ideia é a mesma no ultrassom e na tomografia: tudo o que não precisa do aparelho acontece fora da sala, antes da
vez do paciente. Assim, quando um paciente sai, o próximo já está pronto. Os minutos estão em amarelo na aba Premissas
e precisam ser medidos no mês 1.

### 2.1 Ultrassom

O CBR 2017 separa o intervalo de agendamento do tempo com o paciente posicionado. A diferença, de 5 minutos por exame,
é a entrada, a troca de roupa, a explicação e a saída. Com o paciente pronto antes da vez, a sala perde só a entrada e
a saída (premissa: 2 minutos).

| grupo de exame | preparo do paciente | o que se faz fora da sala | exames | agenda (CBR) | posicionado (CBR) | sala com preparo fora |
|---|---|---|---:|---:|---:|---:|
| Mama | sem preparo | troca de roupa no vestiário | 12.950 | 20 | 15 | 17 |
| Doppler de membros | sem preparo | tirar meias e a roupa do membro no vestiário | 12.345 | 40 | 30 | 32 |
| Doppler de carótidas e outros vasos | sem preparo; artérias renais e aorta: jejum | — | 4.727 | 20 | 15 | 17 |
| Parede abdominal | sem preparo | — | 3.304 | 20 | 15 | 17 |
| Abdômen total | jejum e bexiga cheia | água na espera; agenda de manhã | 10.347 | 20 | 15 | 17 |
| Abdômen superior | jejum | agenda de manhã | 2.327 | 15 | 10 | 12 |
| Aparelho urinário e rins | bexiga cheia | água na espera, cerca de 1 hora antes | 4.657 | 15 | 10 | 12 |
| Próstata (via abdominal) | bexiga cheia | água na espera | 3.052 | 15 | 10 | 12 |
| Pélvica (ginecológica) | bexiga cheia | água na espera | 1.014 | 15 | 10 | 12 |
| Transvaginal | bexiga vazia; acompanhante | esvaziar a bexiga e trocar de roupa; transdutor desinfetado e capa pronta | 5.294 | 15 | 10 | 12 |
| Tireoide | sem preparo | — | 3.979 | 15 | 10 | 12 |
| Bolsa escrotal | sem preparo; acompanhante | troca de roupa no vestiário | 1.136 | 15 | 10 | 12 |
| **ultrassom** | | | **65.132** | **24.037 h** | | **19.752 h** |

Os tempos estão em minutos. O preparo é o usual em serviços de imagem, e o responsável técnico de cada polo valida.

**O resultado.** As horas de sala caem 18%. Em 12 meses, a rede precisa de 13 salas, contra 15 sem o preparo fora da
sala:

| polo | Oeste | Sudoeste | Norte | Leste | Central e Centro-Sul | Sul | rede |
|---|---:|---:|---:|---:|---:|---:|---:|
| salas | 1 | 4 | 2 | 1 | 2 | 3 | 13 |

A Leste fica com 98% de uso numa sala só; com 2 salas, a rede fica com 14.

### 2.2 Tomografia: três fluxos

**A. Sem contraste.**

| passo | o que acontece | quem faz | min | ocupa o tomógrafo? |
|---|---|---|---:|---|
| 1. Recepção | identificação, documentos, CPF | secretaria | 5 | não |
| 2. Conferência | gestação, nas usuárias, e termo | enfermagem | 5 | não |
| 3. Troca de roupa | retirada de metais e avental | o paciente, no vestiário | 3 | não |
| 4. Exame | posicionar, adquirir e sair | técnico em radiologia | **10** | **sim** |

A RSNA 2005 mediu 8,6 minutos na sala; a v26 contava 15.

**B. Com contraste em série, tudo na sala (como a v26 conta).**

| passo | o que acontece | quem faz | min | ocupa o tomógrafo? |
|---|---|---|---:|---|
| 1. Recepção | identificação, documentos, CPF | secretaria | 5 | não |
| 2. Triagem | alergia, doença renal, metformina, gestação; termo | enfermagem | 5 | não |
| 3. Troca de roupa | retirada de metais e avental | o paciente | 3 | não |
| 4. Punção e exame | punção na mesa, conexão à bomba, aquisição com fases, desconexão | enfermagem e técnico | **20** | **sim** |
| 5. Repouso | observação depois do contraste | enfermagem | 15 | não |
| 6. Alta | retirada do acesso, orientação da metformina | enfermagem | 3 | não |

**C. Com contraste em linha: o preparo de vários pacientes em paralelo.**

| passo | o que acontece | quem faz | min | ocupa o tomógrafo? |
|---|---|---|---:|---|
| 1. Recepção | identificação, documentos, CPF; o paciente chega cerca de 40 min antes do horário do tomógrafo | secretaria | 5 | não |
| 2. Orientação em grupo | 3 a 5 pacientes juntos: o que é o contraste, o calor na injeção, o repouso, o que avisar | enfermagem | 5 | não |
| 3. Triagem individual | alergia, doença renal (creatinina no TrakCare só para o renal), metformina, gestação; termo | enfermagem | 5 | não |
| 4. Troca de roupa | retirada de metais e avental | o paciente | 3 | não |
| 5. Punção na sala de preparo | cateter, teste com soro e curativo; o paciente fica pronto, sentado | enfermagem | 8 | não |
| 6. Espera pronto | dois pacientes com acesso à espera, para o tomógrafo nunca parar | o paciente | 26 | não |
| 7. Exame | posicionar, conectar à bomba, adquirir com fases, desconectar | técnico em radiologia | **13** | **sim** |
| 8. Repouso | observação, sem tempo mínimo (v26, 4.8) | enfermagem | 15 | não |
| 9. Alta | retirada do acesso, orientação da metformina | enfermagem | 3 | não |

**O que o fluxo em linha rende, por tomógrafo:**
- **13 minutos de tomógrafo por exame com contraste, contra 20 em série (35% a menos).** Os 13 minutos são uma
  hipótese: os 8,6 minutos do exame sem contraste medidos na RSNA 2005, mais cerca de 4 minutos de bomba, injeção e
  fases. Não encontrei estudo que meça esse ganho em minutos; é o primeiro número a medir no mês 1.
- **37 exames com contraste por dia, contra 24 em série** (10 horas abertas, 80% delas com exame).
- **Enfermagem:** 4,6 punções por hora ocupam 0,85 pessoa no preparo e na alta. A v26 já prevê 2 pessoas de enfermagem
  por tomógrafo.
- **Espaço:** 4 poltronas na sala de preparo e repouso.
- **Paciente:** fica cerca de 1 hora e 20 minutos no polo, somando a espera pronto.

**Por que o fluxo em linha é viável:**
- **Jejum:** o HC-UFG (Ebserh, 2026) dispensa jejum para tomografia, mesmo com contraste venoso, com base no Colégio
  Americano de Radiologia. Sem jejum, o contraste não fica preso à manhã. A clínica precisa confirmar que segue essa
  orientação.
- **Repouso e creatinina:** a v26 (4.8) já diz que não há tempo mínimo de repouso e que a creatinina só é exigida de
  quem tem doença renal, consultada no TrakCare. Isso tira o repouso e o laboratório de dentro da sala.

**O que a clínica precisa ter para o fluxo em linha:**
- uma sala de preparo com poltronas;
- uma pessoa de enfermagem dedicada à punção e à alta, por tomógrafo;
- a bomba injetora com a seringa pronta antes de o paciente entrar;
- o radiologista no serviço durante as injeções;
- uma agenda em que o paciente com contraste chega 40 minutos antes e o exame sem contraste entra nos intervalos.

## 3. Quantos meses a tomografia leva com 3, 4 ou 5 tomógrafos

A conta já desconta os 10% de pedidos com contraste que o radiologista converte para sem contraste (premissa a medir).
Cada tomógrafo dá 168 horas de exame por mês: 10 horas por dia, 80% delas com exame, em 21 dias úteis.

**Meses para fazer toda a tomografia da carteira 1:**

| tomógrafos | em série, 20 min (v26) | em série, 25 min | em série, 30 min | em linha, 13 min |
|---:|---:|---:|---:|---:|
| 3 | 9,2 | 11,3 | 13,4 | **6,0** |
| 4 | 6,9 | 8,5 | 10,1 | 4,5 |
| 5 | 5,5 | 6,8 | 8,1 | 3,6 |

**Horas por dia que cada tomógrafo precisa abrir para o plano, para fechar em 12 meses:**

| tomógrafos | em série, 20 min | em série, 25 min | em série, 30 min | em linha, 13 min |
|---:|---:|---:|---:|---:|
| 3 | 7,7 | 9,4 | 11,2 | **5,0** |
| 4 | 5,8 | 7,1 | 8,4 | 3,8 |
| 5 | 4,6 | 5,7 | 6,7 | 3,0 |

**Como ler:**
- **3 tomógrafos em série** fecham em 12 meses até cerca de 26 minutos por exame com contraste. Com 30 minutos, não
  fecham.
- **Em linha, 3 tomógrafos sobram.** Ou fazem a tomografia em 6 meses no dia inteiro, ou correm os 12 meses num turno
  de 5 horas por dia. Esse turno pode ser o horário em que o radiologista está presente, o que resolve a janela do
  contraste.
- **4 ou 5 tomógrafos só se justificam** se a clínica não fizer o fluxo em linha e o exame em série passar de 25
  minutos.

**Volume para negociar, se a tomografia correr os 12 meses:** 400 exames por mês por tomógrafo com 3; 300 com 4; 240
com 5.

**A conversão para sem contraste (3 tomógrafos):**

| parte convertida | em série, 20 min | em linha |
|---:|---:|---:|
| 0% | 9,5 meses | 6,2 meses |
| 10% | 9,2 | 6,0 |
| 20% | 9,0 | 5,9 |
| 30% | 8,8 | 5,7 |

Ela muda pouco o tempo, porque o exame sem contraste também ocupa o tomógrafo: 15 contra 20 minutos em série, 10 contra
13 em linha. O ganho maior é outro: menos contraste, menos punção e menos risco de reação. O código SUS é o mesmo com ou
sem contraste e paga o mesmo; por isso a Meta 5 não muda.

## 4. Custo de executar: o que sobe com os meses e o que não muda

Aqui o ultrassom é feito por nós, com sala e aparelho alugados e médico pago por exame. A tomografia é feita na clínica
parceira, paga por exame. As premissas são as do custo v2 (20/10) e da pesquisa de 05/11. A conta usa as 15 salas da
agenda do CBR; com o preparo em paralelo no ultrassom, são 13 e o custo cai.

| item | como se calcula | hoje (8 meses) | 12 meses | diferença |
|---|---|---:|---:|---:|
| aluguel das salas | salas × meses × R$ 3.000 | R$ 480.000 | R$ 540.000 | +R$ 60.000 |
| aluguel dos aparelhos | salas × meses × R$ 2.500 | R$ 400.000 | R$ 450.000 | +R$ 50.000 |
| custos fixos da sala | salas × meses × R$ 400 | R$ 64.000 | R$ 72.000 | +R$ 8.000 |
| recepção (2 por polo) | 12 × meses × R$ 2.959 | R$ 284.064 | R$ 426.096 | +R$ 142.032 |
| responsável técnico, retaguarda e custos do polo | por polo e por dia | **sem preço** | | +50% |
| médico, insumos, sistema de imagem e energia | por exame ou por hora | R$ 2.532.564 | igual | — |
| tomografia na clínica | exames × R$ 171,44 | R$ 2.468.907 | igual, se o preço não mudar | — |
| **custo de executar** | | **R$ 6.229.535** | **R$ 6.489.567** | **+R$ 260.032** |

**Uma regra de bolso para os itens sem preço:**
- cada R$ 1.000 por mês, por polo, custa R$ 24.000 a mais em 12 meses;
- cada R$ 100 por dia de retaguarda custa R$ 50.400 a mais.

**O custo a mais cabe no valor do exame,** mas folga não é lucro: no convênio, o que não se gasta volta como saldo ou
vira mais exames por aditivo.

**Médicos de ultrassom.** O valor por exame é o mesmo, mas cada médico faz 1/3 menos exames por mês. O risco é o médico
pedir um mínimo por turno.

## 5. Salas de ultrassom, polo a polo

| polo | horas de exame | salas hoje | 12 meses, agenda do CBR | 12 meses, preparo em paralelo | contratos (20/10) |
|---|---:|---:|---:|---:|---|
| Oeste | 1.059 | 1 | 1 | 1 | Ceilândia: 3 (recebe parte da Sudoeste) |
| Sudoeste | 7.712 | 6 | 4 | 4 | Samambaia: 2 |
| Norte | 3.052 | 3 | 2 | 2 | Sobradinho: 2 |
| Leste | 2.405 | 2 | 2 | 1 (98% de uso) | São Sebastião: 2 |
| Central e Centro-Sul | 3.481 | 3 | 2 | 2 | Asa Sul: 3 |
| Sul | 6.327 | 5 | 4 | 3 | Gama: 1 |
| **rede** | **24.036** | **20** | **15** | **13** | **13** |

**Contra os contratos:** Oeste e Sudoeste juntos precisam de 5 salas e têm 5. A Norte fecha. Asa Sul e São Sebastião
têm 1 sala de sobra cada. **O Sul é o problema:** com o preparo em paralelo, faltam 2 salas no Gama. Alugar sala por
turno, onde a carga não enche uma sala, reduz a perda do arredondamento.

## 6. Os 3 polos de tomografia

O arranjo que equilibra os três tomógrafos (no fluxo em série, com 10% de conversão):

| polo de tomografia | Regiões | exames por mês | uso |
|---|---|---:|---:|
| 1, oeste (ex.: Ceilândia) | Oeste e metade da Sudoeste (Samambaia, Recanto das Emas) | 403 | 78% |
| 2, sudoeste e sul (ex.: Taguatinga) | a outra metade da Sudoeste e o Sul | 398 | 77% |
| 3, centro e norte (ex.: Plano Piloto) | Central, Centro-Sul, Leste e Norte | 399 | 77% |

Pôr o terceiro tomógrafo no Gama ou em Sobradinho, no lugar do Plano Piloto, desequilibra a rede se cada Região for
para o polo mais perto: Taguatinga passa de 100%. A coluna D da aba Tomografia deixa testar outro arranjo. As Regiões
sem tomógrafo andam mais, e isso pode aumentar a falta na tomografia.

**Uma questão a mais com o jurídico.** Concentrar a tomografia em 3 unidades de uma clínica, com preço por volume, deixa
mais visível o contrato por exame. Isso pesa na pendência que já está com o jurídico do ISHP: a 4.14 diz que a execução
não é subcontratada.

## 7. O que muda no plano, seção por seção

| seção | hoje (v26) | com a mudança |
|---|---|---|
| 1.9, 5.1, 7.1 | vigência e execução de 8 meses | 12 meses |
| 2.2, 3.1, 6.1 (Metas 2 a 5), 8.2 | 79.533 exames (carteira 1) | cerca de 160 exames a menos com a P2 |
| 3.4, 4.2 | um tomógrafo por polo; a TC de um polo pode ir a outro | TC em 3 polos, com polo de referência para cada Região; sai o argumento de "manter o exame perto da unidade solicitante" |
| 4.3, 4.8 | triagem e acesso venoso no dia, sem dizer onde | acesso venoso na sala de preparo, antes da sala do tomógrafo; orientação em grupo; sem jejum |
| 4.13, 8.2, 8.3 | 22 postos + assessoria por 8 meses | o quadro da P2 por 12 meses; o pré-exame com o nome de assistente de agendamento, confirmação e busca ativa; "8 meses" vira "12 meses" na tabela e na nota da assessoria |
| 4.15 | 24 médicos de US, 7 radiologistas, 18 técnicos, 12 de enfermagem | 16 médicos de US (1.800 h por ano), no mínimo 3 radiologistas, 9 técnicos, 6 de enfermagem; retaguarda por 252 dias úteis; RT e recepção iguais |
| 4.16 (b) e (d) | blindagem, levantamento radiométrico e testes nos polos com TC | só nos 3 polos com TC |
| 5.2, 6.1 | Meta 1: 6 polos por 8 meses; Meta 6: 8 relatórios mensais | 6 polos por 12 meses; 12 relatórios mensais |
| 7.2 | 3/8, 3/8 e 2/8 do quantitativo | 1/4 por trimestre |
| 7.3 | 168 dias úteis; "seis equipamentos para uma carga de 3,33" | 252 dias úteis; 3 tomógrafos; reescrever o parágrafo |
| 7.4, 7.5 | 3 parcelas (3 + 3 + 2 meses) | 4 trimestrais, com uma prestação de contas parcial a mais |
| 7.8, 7.9 | R-01 com seis tomógrafos e oito meses | R-01 com 3 tomógrafos e o fluxo do contraste. R-14 fica mais provável: a tabela pode mudar dentro de 12 meses. Risco novo: deslocamento até as Regiões com TC |
| documento | PT v1 assinado (23/10 e 27/10) | v27, nova assinatura e reenvio à SES, junto com a Candanga |

## 8. A fila

- **Ritmo:** cerca de 6.600 exames por mês, em vez de 9.900. A fila cai mais devagar, porque as entradas continuam.
- **Pedidos novos:** em 12 meses entram cerca de 1,5 vez os pedidos esperados em 8. As linhas de pedidos novos e
  encaminhados da carteira 1 (2.074 exames) ficam mais seguras.
- **Faltas:** com menos vagas por mês, há mais pacientes na fila para repor cada falta. É controle interno e não vai ao
  plano.

## 9. O que precisa ser decidido

Na ordem em que travam o resto:

1. **O quadro de gestão em 12 meses.** Recomendo a P2. Ela fica em 8,44%, nenhum preço fica abaixo do menor aprovado,
   e a carga por operador fica abaixo da de hoje.
2. **O fluxo da tomografia com contraste na clínica.** Recomendo o fluxo em linha: é ele que faz 3 tomógrafos sobrarem
   em 12 meses. A sala de preparo, a enfermagem e o radiologista durante as injeções devem ir para o contrato.
3. **O tempo real do contraste na clínica,** medido no mês 1 e por escrito: minutos em série e em linha, janela do
   contraste, jejum, creatinina e repouso.
4. **Quais 3 polos de tomografia** e para onde vai cada Região. Escolher pela rede da clínica parceira e testar na
   planilha.
5. **Quanto tempo a tomografia corre.** Recomendo os 12 meses num turno com o radiologista presente. Isso deixa folga
   para remarcação e para falha de equipamento.
6. **Salas de ultrassom.** Recomendo contratar por 12 meses as da coluna do preparo em paralelo, com 2 na Leste (14 no
   total), e negociar sala por turno onde a carga não enche uma sala.
7. **Parcelas.** Recomendo 4 trimestrais, na lógica da v26.
8. **Mês de início e data-base de cada cargo,** para a reserva de reajuste.
9. **Preço da tomografia com volume,** com o contraste incluído e o prazo do laudo no contrato.

**Limite deste estudo:** o mapa da seção 7 parte do texto da v26, e a carteira 1 ainda não foi aplicada ao plano. Os
números de exames das seções valem como ordem de grandeza até a v27 ser montada.

## Fontes

- Preparo de TC e RM do HC-UFG/Ebserh (2026; processo SEI 23760.025096/2025-89), que dispensa o jejum na TC com
  contraste: https://www.gov.br/hubrasil/pt-br/hospitais-universitarios/regiao-centro-oeste/hc-ufg/saude/exames/PREPAROEXAMESDETCERM.26.pdf
- Tempo de sala da tomografia com e sem contraste (Erdfarb et al., RSNA 2005): https://archive.rsna.org/2005/4407929.html
- Tempos do ultrassom (CBR 2017): os mesmos do estudo das filas de 02/11 e do estudo de 05/11.
- Preços de mercado no DF: `dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx`, aba Mercado e aprovados
  (salario.com.br, 20/10/2026).
- Preços dos aprovados: `biblioteca/precos/cargos_no_acervo.md`.
- O ganho de puncionar fora da sala é prática relatada, mas não achei medida em minutos. Dois exemplos: a estação de
  acesso venoso da UMass Memorial
  (https://umassmed.edu/radiology/radnews/2024/spring2024/innovators-of-the-year-award-university-ct-team) e o modelo
  de auditoria do Royal College of Radiologists sobre o tempo de tomógrafo perdido com punção na mesa
  (https://www.rcr.ac.uk/career-development/audit-quality-improvement/auditlive-radiology-templates/inpatient-cannulation-in-ct-how-much-scanner-time-is-lost/).
