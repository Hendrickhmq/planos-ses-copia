# Tomografia em 3 polos e 12 meses: fluxo, tempo, exames por hora e equipe

Estudo interno de 09/11/2026, a pedido do usuário, revisto duas vezes no mesmo dia. Ele faz quatro coisas:
- prepara a consulta ao grupo sobre a mudança de 5 ou 6 polos de tomografia em 8 meses para 3 polos em 12. O
  formulário vai às pessoas que ajudam o projeto na parte assistencial, e não às clínicas, e serve só para entender
  o tempo. O protocolo do contraste fica para um estudo à parte;
- deixa mapeados o fluxo com e sem contraste, onde o paciente fica em cada etapa e quanto cada tomógrafo faz por
  hora, para voltar a eles depois;
- abre o estudo do ultrassom por tipo de exame, com o auxiliar de sala que fica com o médico o exame todo;
- monta a equipe de referência para um tomógrafo e para uma sala de ultrassom funcionarem 10 horas por dia útil, com
  os cargos do plano.

**Base:** carteira 1, com 14.401 TC. Com 10% dos pedidos que podem ir sem contraste convertidos, 12.883 ficam com
contraste. A angiotomografia não aparece à parte: as da carteira contam como TC com contraste comum. Os tempos são os
de referência do estudo de 08/11 até a equipe assistencial responder.

**Liga com:**
- o estudo de 08/11 (contraste: tempo, fluxo e regras), de onde vêm os tempos de cada etapa e as fontes;
- o de 07/11 (12 meses e 3 tomógrafos), que propôs o arranjo dos 3 polos, o fluxo em linha e os tempos do
  ultrassom;
- a v26 (PT v1), 4.15, com a equipe assistencial e as jornadas;
- a análise do despacho GEDIAG (08/11). Ela pede, por polo, o tempo por procedimento, os profissionais por turno e o
  horário (5.11).

**Arquivos:**
- `tempos_e_equipe_tomografia_ultrassom_20261109.xlsx`: o formulário em branco para o grupo, com uma aba de
  tomografia e uma de ultrassom, sem nada interno. Pede só o nome de quem preenche;
- `tempos_e_equipe_tomografia_ultrassom_nossa_referencia_20261109.xlsx`: o mesmo formulário preenchido com a nossa
  referência, com a fonte de cada número na Observação. Vai junto, para comparar (decisão do usuário, 09/11);
- `estudo_tempos_tomografia_3_polos_20261109.xlsx`: o estudo, com as abas Fluxo TC, Por hora, Três polos,
  Ultrassom, Equipe e Respostas. Tudo é fórmula, e o amarelo é premissa ou resposta;
- `gerar_tempos_tomografia_20261109.py`: o gerador das duas.

Nada daqui vai ao plano sem decisão do usuário.

---

## Resposta curta

1. **Mandar a planilha, com uma mensagem curta.**
   - Só a mensagem volta com respostas soltas ("uns 15 minutos"), sem dizer o que entra no tempo, e cada pessoa
     responde de um jeito.
   - A planilha já traz as etapas escritas e separa as que prendem o tomógrafo. É esse o número que decide a
     viabilidade. Quem preenche só digita minutos, e os exames por hora aparecem sozinhos.
   - Para quem estiver só no celular, a mensagem traz as 4 perguntas que mais pesam, para responder ali mesmo.
2. **O radiologista decide o contraste, e o melhor momento é a véspera** (seção 1). O pedido médico indica, e o
   radiologista confirma ao rever o pedido (Parecer CFM 17/2019). Assim, só é puncionado quem vai receber contraste.
3. **A punção antes poupa 5 min de tomógrafo por exame,** mas pede sala de preparo e uma segunda pessoa de
   enfermagem (seção 2). Com 3 polos, é ela que deixa o volume caber.
   - **O paciente passa mais tempo em cadeira ou maca:** 33 min com a punção na mesa (repouso e alta) e 59 com ela
     antes (orientação, punção, espera, repouso e alta).
   - **Isso dá 3 cadeiras ou macas por tomógrafo com a punção na mesa e 5 com ela antes,** com 1 de folga.
4. **Cada tomógrafo faz, por hora de exame:**
   - 5,5 exames sem contraste;
   - 3,0 com contraste e a punção na mesa;
   - 4,0 com a punção feita antes;
   - 4,6 com a punção antes e as medidas que agilizam.

   Por hora aberta, descontadas as horas sem exame, são 4,4, 2,4, 3,2 e 3,7. Na carteira, que tem 89% de exames com
   contraste, são 25 exames por dia de 10 horas com a punção na mesa e 33 com ela antes.
5. **Com 3 polos em 12 meses, cada tomógrafo faz 400 TC por mês, ou 19 por dia útil.**
   - Com 6 polos em 8 meses, eram 300; com 5, eram 360. São 33% e 11% a mais por tomógrafo.
   - Cada tomógrafo precisa ficar 7,6 h por dia útil para o projeto com a punção na mesa, ou 5,8 h com ela antes.
     Com 6 h por dia, só cabe a punção antes.
6. **O tomógrafo da clínica é dividido com os pacientes particulares dela.**
   - Na negociação de 08/10, a posição para a Clínica Brasília era 3 turnos de 4 h por semana, cerca de 2,4 h por dia
     útil, para 133 TC por mês da Oeste.
   - Agora, cada tomógrafo precisa de cerca de 3 vezes isso.
7. **A equipe de referência para 10 horas por dia útil** (seção 7):
   - **um tomógrafo:** 3 técnicos em radiologia, porque a lei limita a jornada a 24 h semanais; 2 de enfermagem, ou
     3 com a punção antes; 1 radiologista no horário do contraste; e 2 de recepção por polo;
   - **uma sala de ultrassom:** 2 médicos, 2 auxiliares de sala (um fica com o médico o exame todo e digita o laudo)
     e o pessoal de recepção e preparo do polo.
   - Os cargos são os da v26 (4.15). O auxiliar de sala do ultrassom é função nova.
8. **As pausas da equipe já estão nos 20% de horas sem exame.** Com dois turnos de 5 h, cada turno tem 15 min de
   pausa (CLT, art. 71, § 1º), e o tomógrafo para 30 min por dia, 5% do dia.
   - **Os turnos quase não pedem mais gente:** cada pessoa trabalha menos horas, e o número fica igual.
   - **A exceção é o contraste:** ele ocupa 5,3 h por dia e passa de um turno. Então o radiologista e a 2ª pessoa de
     enfermagem vão de 1 para 2, e o tomógrafo, de 9 para 11 pessoas. Se o contraste couber num turno, voltam a 1.
9. **A troca de roupa passou de 3 para 5 min** (de 3 a 10), porque a fila tem idade mediana de 59 a 61 anos. Ela não
   ocupa o tomógrafo: muda só o tempo do paciente na unidade.

---

## 1. Quem decide se o exame vai com ou sem contraste, e quando

- **O pedido médico indica.** A fila do SISREG separa os pedidos com e sem contraste, como a "TC de abdômen superior
  com contraste".
- **O radiologista decide.** Pelo Parecer CFM 17/2019, a indicação, a dose e a prescrição do contraste são dele.
  - Fazer sem contraste um pedido com contraste não é infração, desde que ele registre o motivo técnico.
  - O médico que pediu não pode impor o contraste.
- **O melhor momento é a véspera.** Ao rever o pedido, o radiologista define o protocolo: com ou sem contraste, as
  fases, o preparo e a pré-medicação de quem já reagiu. Assim:
  - o paciente chega sabendo o que vai fazer;
  - só é puncionado quem vai receber contraste. Com a punção antes, isso é obrigatório.
- **No dia, a triagem pode mudar a decisão.** Diante de alergia prévia, doença renal sem creatinina válida ou
  gestação, o radiologista faz o exame sem contraste ou o devolve à regulação com o motivo (v26, 4.8).
- **Pagamento:** o código SUS é o mesmo com ou sem contraste e paga o mesmo (estudo de 07/11).
- **Quanto se converte:** planejamos 10%. Na rotina, a troca fica entre 8,5% e 14% (estudo de 08/11, seção 7).

## 2. Punção na mesa ou punção antes: o que muda

| | punção na mesa | punção antes, numa sala de preparo |
|---|---|---|
| onde | na mesa do tomógrafo, com o paciente deitado | numa sala ao lado, com o paciente sentado |
| o tomógrafo | fica parado durante a punção: 20 min por exame, 3,0 por hora | só posiciona, injeta e adquire: 15 min por exame, 4,0 por hora |
| a veia difícil | para o tomógrafo, às vezes por 15 min | não para o tomógrafo. O enfermeiro tenta com calma, com ultrassom se preciso |
| o paciente | chega cerca de 15 min antes; fica 73 min na unidade | chega cerca de 40 min antes; fica 89 min |
| a enfermagem | 1 pessoa por vez | 2 juntas no horário do contraste |
| cadeira ou maca | 33 min por paciente, no repouso e na alta: 3 por tomógrafo, com 1 de folga | 59 min, também no preparo e na espera: 5 por tomógrafo |
| o espaço | a sala do tomógrafo e a de repouso | também a sala de preparo |
| a decisão do contraste | pode ser tomada na hora | precisa vir antes da punção, senão o paciente é puncionado à toa |
| quando serve | volume baixo, ou unidade sem espaço nem segunda pessoa de enfermagem | volume alto, como os 400 exames por mês de cada tomógrafo com 3 polos |

**Casos:**
- **A fila é oncológica.** Muitos pacientes têm a veia gasta pela quimioterapia, ou o braço da mama operada fora da
  punção. Na mesa, cada um desses para o tomógrafo. Antes, o enfermeiro com ultrassom acerta na primeira tentativa
  cerca de 3 vezes mais (estudo de 08/11).
- **O exame que vira sem contraste no dia.** Com a punção antes, o acesso já feito é retirado. Por isso o
  radiologista decide na véspera.
- **O que a literatura mediu:**
  - em Kingston, cada punção feita na sala custou cerca de 8 min de tomógrafo;
  - em Amsterdam, tirar a punção da sala levou o uso do tomógrafo de 44% para 51% e a espera de 21 para menos de 5
    dias (estudo de 08/11).

## 3. Quantos exames cada tomógrafo faz por hora

Por hora aberta, a conta põe 80% das horas com exame. Os outros 20% são atrasos, encaixes, limpeza e pausas. O
Canadá mediu 2,34 exames por hora aberta (estudo de 08/11).

| fluxo | minutos de tomógrafo | por hora de exame | por hora aberta | por dia (10 h) | por turno (4 h) |
|---|---:|---:|---:|---:|---:|
| sem contraste | 11 | 5,5 | 4,4 | 44 | 17 |
| com contraste, punção na mesa | 20 | 3,0 | 2,4 | 24 | 10 |
| com contraste, punção antes | 15 | 4,0 | 3,2 | 32 | 13 |
| com contraste, punção antes e as medidas que agilizam | 13 | 4,6 | 3,7 | 37 | 15 |
| **carteira 1, punção na mesa** | 19,1 (média) | **3,1** | 2,5 | **25** | 10 |
| **carteira 1, punção antes** | 14,6 (média) | **4,1** | 3,3 | **33** | 13 |

Do melhor ao pior caso, por hora de exame:
- **sem contraste:** de 3,5 a 6,7;
- **com contraste e a punção na mesa:** de 1,8 a 4,0;
- **com contraste e a punção antes:** de 3,2 a 5,5.

O pior caso põe todas as etapas no máximo: punção difícil e exame demorado.

## 4. O fluxo da tomografia, passo a passo

Os minutos abaixo são os centrais. O mínimo, o máximo e a fonte de cada etapa estão na aba 1 da planilha e no estudo
de 08/11 (aba 2).

### A. Sem contraste

| etapa | quem faz | min | ocupa o tomógrafo? |
|---|---|---:|---|
| recepção: identificação, documento e pedido | recepção | 5 | não |
| conferência: questionário de segurança e gestação | enfermagem ou técnico | 5 | não |
| troca de roupa (há muitos idosos na fila) | paciente | 5 | não |
| exame: posicionar, adquirir as imagens e sair | técnico em radiologia | 9 | **sim** |
| troca de paciente: limpar a mesa e chamar o próximo | técnico em radiologia | 2 | **sim** |
| **tomógrafo** | | **11** | 5,5 por hora |
| **paciente na unidade** | | **26** | |

### B. Com contraste e a punção na mesa (a conta da v26)

Antes do dia, o radiologista revê o pedido e define o protocolo (seção 1).

| etapa | quem faz | min | ocupa o tomógrafo? |
|---|---|---:|---|
| recepção | recepção | 5 | não |
| triagem e termo: alergia, rim, metformina, gestação; leitura e assinatura do termo | enfermagem; médico se preciso | 10 | não |
| troca de roupa (há muitos idosos na fila) | paciente | 5 | não |
| punção na mesa | enfermagem | 7 | **sim** |
| exame: posicionar, ligar à bomba, adquirir as fases e desligar | técnico e enfermagem | 11 | **sim** |
| troca de paciente | técnico em radiologia | 2 | **sim** |
| repouso depois do contraste, com o acesso mantido | enfermagem; radiologista na unidade | 30 | não |
| alta: retirar o acesso e orientar | enfermagem | 3 | não |
| **tomógrafo** | | **20** | 3,0 por hora |
| **paciente na unidade** | | **73** | |

### C. Com contraste e a punção antes (em linha)

Muda em três pontos:
- a punção é feita na sala de preparo, e o paciente espera sentado e pronto;
- o termo é lido em grupo, de 3 a 5 pacientes;
- um ou dois pacientes ficam prontos na porta, para o tomógrafo não parar.

O tomógrafo fica 15 min por exame (13 de exame e 2 de troca), e faz 4,0 por hora. O paciente fica 89 min, porque
chega cerca de 40 min antes. Com as medidas que agilizam, são 13 min e 4,6 por hora (estudo de 08/11, seção 10):
- o pedido revisado na véspera;
- o termo lido no pré-exame;
- a bomba carregada antes de o paciente entrar.

### O que o contraste acrescenta

- **Quatro etapas:** a triagem ampliada com o termo, a punção, a injeção e os 30 min de repouso.
- **Uma pessoa:** a enfermagem.
- **Uma condição de agenda:** o radiologista na unidade durante todo exame com contraste, até a alta (Parecer CFM
  17/2019). Por isso as horas do radiologista contam tanto quanto as do tomógrafo.

## 5. De 5 ou 6 polos em 8 meses para 3 em 12

| | 6 polos, 8 meses | 5 polos, 8 meses | 3 polos, 12 meses |
|---|---:|---:|---:|
| tomógrafo-mês | 48 | 40 | 36 |
| TC por tomógrafo, por mês | 300 | 360 | **400** |
| TC por tomógrafo, por dia útil | 14,3 | 17,1 | **19,0** |
| horas por dia de cada tomógrafo, com a punção na mesa | 5,7 | 6,8 | **7,6** |
| horas por dia, com a punção antes | 4,3 | 5,2 | **5,8** |
| horas por dia, com a punção antes e as medidas | 3,8 | 4,6 | 5,1 |
| horas por dia com radiologista, com a punção na mesa | 5,3 | 6,4 | 7,1 |
| horas por dia com radiologista, com a punção antes | 4,0 | 4,8 | 5,3 |

**Como ler:**
- **A carteira não muda:** são as mesmas 14.401 TC. O que muda é a carga de cada tomógrafo: 33% a mais que com 6
  polos e 11% a mais que com 5.
- **Por dia, 3 polos em 12 meses pesam quase como 5 polos em 8:** 19 TC contra 17.
- **As horas por dia já contam as horas abertas sem exame.**

## 6. O limite: horas por dia contra minutos por exame

Com 3 tomógrafos em 12 meses, e a carteira dividida igual entre eles:

| horas por dia útil de cada tomógrafo para o projeto | minutos por exame com contraste, no máximo | cabe com a punção na mesa (20 min)? | cabe com a punção antes (15 min)? |
|---:|---:|---|---|
| 4 | 10,0 | não | não |
| 5 | 12,8 | não | não |
| 6 | 15,6 | não | sim |
| 7 | 18,4 | não | sim |
| 8 | 21,2 | sim | sim |
| 9 | 24,1 | sim | sim |
| 10 | 26,9 | sim | sim |

**Meses para fazer toda a TC com 3 tomógrafos:**

| horas por dia | 13 min | 15 min | 17 min | 20 min | 25 min |
|---:|---:|---:|---:|---:|---:|
| 6 | 10,2 | 11,6 | 13,0 | 15,1 | 18,7 |
| 8 | 7,6 | 8,7 | 9,7 | 11,3 | 14,0 |
| 10 | 6,1 | 6,9 | 7,8 | 9,1 | 11,2 |

A matriz completa, de 4 a 10 horas por dia, está na aba 3.

**Como ler:**
- **Com a punção na mesa,** cada tomógrafo precisa de 8 h por dia útil por 12 meses, com o radiologista em quase todo
  esse tempo.
- **Com a punção antes,** bastam 6 h. É o fluxo que o estudo de 07/11 já recomendava.
- **O pior caso do estudo de 08/11** (punção difícil e exame demorado, 34 min de tomógrafo) não cabe nem com 10 h.

## 7. A equipe para 10 horas por dia útil

A conta é: pessoas ao mesmo tempo × horas por dia × 5 dias ÷ jornada semanal, arredondado para cima. Ela não conta
férias nem faltas. Na aba 4, a equipe de cada resposta aparece ao lado.

### Um tomógrafo

| função | ao mesmo tempo | horas por dia | jornada semanal | pessoas |
|---|---:|---:|---:|---:|
| técnico em radiologia | 1 | 10 | 24 (Lei 7.394/1985, art. 14) | **3** (2,08) |
| enfermagem, o dia todo | 1 | 10 | 44 | **2** (1,14) |
| enfermagem, 2ª pessoa no horário do contraste (só com a punção antes) | 1 | 5,3 | 44 | **1** (0,61) |
| radiologista, no horário do contraste | 1 | 5,3 | 34,6 (1.800 h por ano) | **1** (0,77) |
| recepção, por polo | 1 | 10 | 44 | **2** (1,14) |
| **total** | | | | **8 com a punção na mesa; 9 com ela antes** |

**Como ler:**
- **O técnico em radiologia é quem mais pesa.** A lei limita a jornada a 24 h semanais, e 10 h por dia pedem 3
  técnicos. É o que a v26 já tinha (4.15).
- **Com a punção na mesa, o radiologista fica 7,1 h por dia**, ou 1,03 médico: 1 no limite. A v26 tem um médico de
  retaguarda por dia útil em cada polo, que cobre a falta.
- **A 2ª pessoa de enfermagem só entra com a punção antes.** É ela que punciona na sala de preparo enquanto a 1ª
  cuida da triagem, do repouso e da alta (estudo de 08/11, aba 4).

### Uma sala de ultrassom

| função | ao mesmo tempo | horas por dia | jornada semanal | pessoas |
|---|---:|---:|---:|---:|
| médico ultrassonografista | 1 | 10 | 34,6 (1.800 h por ano) | **2** (1,44) |
| auxiliar de sala do ultrassom, com o médico o exame todo | 1 | 10 | 44 | **2** (1,14) |
| pessoal de recepção e preparo, por polo (o mesmo da tomografia, se houver) | 1 | 10 | 44 | **2** (1,14) |

**Como ler:**
- **O médico faz o exame e assina o laudo,** e é um por sala durante o exame (v26, 4.9 e 4.15).
- **O auxiliar de sala fica com o médico o exame todo** (pedido do usuário, 09/11). Ele digita o laudo, ajuda o
  paciente, acompanha o transvaginal e o de próstata (v26, 4.16, g) e limpa o transdutor. É função nova: a v26 não a
  tem, e o custo dela entra no valor do exame.

### O ultrassom por tipo de exame

A aba 4 da planilha tem os 12 tipos de exame da carteira 1 (65.132 exames), cada um com o preparo, o tempo de sala
do CBR 2017 e as horas de sala. As respostas entram ali, uma tabela por pessoa, com cinco partes por exame: o preparo
fora da sala, a entrada e o posicionamento, o exame, o fechamento do laudo e a saída com a limpeza do transdutor.

| exame | exames | minutos de sala (CBR) | por hora | horas de sala |
|---|---:|---:|---:|---:|
| mamas (as duas) | 12.950 | 20 | 3,0 | 4.317 |
| Doppler de membros (os dois lados, um de cada vez) | 12.345 | 40 | 1,5 | 8.230 |
| Doppler de carótidas e outros vasos | 4.727 | 20 | 3,0 | 1.576 |
| parede abdominal | 3.304 | 20 | 3,0 | 1.101 |
| abdômen total | 10.347 | 20 | 3,0 | 3.449 |
| abdômen superior | 2.327 | 15 | 4,0 | 582 |
| aparelho urinário e rins | 4.657 | 15 | 4,0 | 1.164 |
| próstata (via abdominal) | 3.052 | 15 | 4,0 | 763 |
| pélvica (ginecológica) | 1.014 | 15 | 4,0 | 254 |
| transvaginal | 5.294 | 15 | 4,0 | 1.324 |
| tireoide | 3.979 | 15 | 4,0 | 995 |
| bolsa escrotal | 1.136 | 15 | 4,0 | 284 |
| **total** | **65.132** | | | **24.037** |

**Como ler:**
- **O Doppler de membros é 19% dos exames e um terço das horas de sala.** É o tempo que mais pesa conferir.
- **Na rede, as 24.037 horas dão 11,9 salas em 12 meses** (10 h por dia, 80% com exame), sem arredondar por polo.
  Arredondando polo a polo, o estudo de 07/11 achou 15 salas, ou 13 com o preparo fora da sala.
- **A diferença entre o tempo de sala e o do exame (5 min no CBR) é entrada, explicação e saída.** Com o auxiliar
  digitando o laudo durante o exame, parte do fechamento do laudo sai do fim. As respostas vão dizer quanto.

### As pausas e os turnos

- **CLT, art. 71:** acima de 6 h de trabalho, o intervalo é de 1 a 2 h; de 4 a 6 h, é de 15 min.
- **Os 20% de horas sem exame já incluem as pausas.** Uma hora parada por dia é 10% de um dia de 10 h: metade desses
  20%.
- **Com dois turnos de 5 h** (manhã e tarde, pedido do usuário), cada turno tem 15 min de pausa. Se o tomógrafo para
  nelas, são 30 min por dia, ou 5% do dia. Ninguém precisa cobrir.

**Os turnos pedem mais gente?** Quase não. Cada pessoa trabalha menos horas (25 h por semana, em vez de 44), e o
número de pessoas fica igual em quase todo cargo (aba 5, seção 4):

| função | jornada cheia, com revezamento | dois turnos de 5 h |
|---|---:|---:|
| técnico em radiologia | 3 | 3 (a lei limita a 24 h: 4 turnos por pessoa) |
| enfermeiro ou técnico de enfermagem, o dia todo | 2 | 2 |
| 2ª pessoa de enfermagem, no horário do contraste (punção antes) | 1 | **2** |
| médico radiologista, no horário do contraste | 1 | **2** |
| pessoal de recepção e preparo, por polo | 2 | 2 |
| **tomógrafo** | **9** | **11** |
| médico ultrassonografista | 2 | 2 |
| auxiliar de sala do ultrassom | 2 | 2 |

**Onde cresce:** o contraste ocupa 5,3 h por dia em cada tomógrafo (3 polos, punção antes). Isso passa de um turno, e
o radiologista e a 2ª pessoa de enfermagem precisam estar nos dois. **Se o contraste couber num turno de 5 h**, os
dois voltam a 1 cada. Com a punção antes e as medidas que agilizam, o contraste ocupa 4,6 h por dia e cabe.

## 8. O que o formulário pergunta

É uma planilha por pessoa, com duas abas. Serve só para entender o tempo e a equipe.

**Tomografia:**
1. os minutos de cada etapa, sem e com contraste, e onde o paciente fica em cada uma;
2. **as duas punções, cada uma na sua linha:** na mesa, que ocupa o tomógrafo, e antes, na sala de preparo, que não
   ocupa, com a espera do paciente pronto. As contas saem para os dois jeitos: minutos de tomógrafo, exames por hora,
   minutos em cadeira ou maca e tempo do paciente na unidade;
3. o repouso depois do contraste, numa maca ou cadeira da sala de repouso;
4. a equipe que a pessoa montaria para um tomógrafo funcionar 10 horas por dia útil, com os cargos do plano e as
   jornadas; como cobriria as 10 horas (dois turnos de 5 h ou jornada cheia com revezamento); e as pausas.

**Ultrassom:**
1. os minutos das cinco partes de cada um dos 12 tipos de exame;
2. a equipe de uma sala por 10 horas, com o auxiliar de sala, e a formação que se pede dele.

**O que saiu:** o protocolo do contraste (jejum, creatinina e quando se decide), que vai para um estudo à parte; a
pergunta de exames por turno; a angiotomografia; e as perguntas de clínica (poltronas, bomba injetora, canais, horas
do aparelho).

**O que não se conta na equipe:** o médico de retaguarda e o responsável técnico do polo, a supervisão de polo, o
pré-exame, o pós-exame e o assistente administrativo. Já estão no projeto (v26, 4.15, e o quadro P2 de 07/11).

**Em branco e preenchido:** vão as duas versões. A preenchida traz a nossa referência com as fontes e um aviso de
que serve para comparar; a resposta vem na em branco. A referência pode puxar a resposta, e por isso a Observação de
cada linha pede o que for diferente.

**O que a versão preenchida usa:**
- na TC, os minutos centrais da seção 4. Como o exame com contraste tem uma linha só, ela usa os 11 min da punção na
  mesa: com a punção antes, o tomógrafo fica 13 min, que é o valor com as medidas que agilizam. Medido com o acesso
  feito antes, o exame vai de 12 a 15 min, e a Observação diz isso;
- no ultrassom, o exame é o tempo do CBR com o paciente posicionado; a diferença até a agenda, de entrada e saída,
  vai 60% para a entrada e 40% para a saída (estimativa nossa); o laudo fica dentro do exame, com o auxiliar
  digitando; o preparo da bexiga cheia é de 60 min;
- na equipe, a referência da seção 7, com a jornada e a conta de cada cargo.

### A mensagem

Versão final de 09/11. Vai só a planilha em branco; a de referência fica para depois, para não influenciar as
respostas (decisão do usuário). As idades são a mediana de cada fila no Mapa Social (coleta de 02/11,
`../dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json`, campo `idade_mediana`).

> Pessoal, preciso da ajuda de vocês.
>
> Vamos tentar executar o plano de imagem com 6 polos de ultrassom e 3 de tomografia, em 12 meses. Antes eram 5 ou 6
> polos de tomografia em 8 meses. Com menos tomógrafos, cada um vai atender mais pacientes por dia. Por isso quero
> fazer um estudo de quanto tempo leva, em média, cada procedimento, para sermos mais assertivos.
>
> Mando uma planilha com duas abas, uma de tomografia e uma de ultrassom. As etapas já estão escritas: é só colocar
> os minutos aproximados de cada uma, pela experiência de vocês. No fim de cada aba, pergunto também que equipe vocês
> montariam para um tomógrafo e para uma sala de ultrassom funcionarem 10 horas por dia. Se não souberem alguma
> parte, podem deixar em branco.
>
> Algumas informações sobre os pacientes da fila, que ajudam a pensar no tempo:
> - A fila é mais velha. Na tomografia com contraste (abdômen, pelve e tórax), metade dos pacientes tem 59 anos ou
>   mais. No ultrassom, a idade mediana é de 65 anos na próstata, 64 no Doppler de carótidas, 63 no Doppler arterial
>   de membros e 58 no venoso.
> - Quase 9 em cada 10 pedidos de tomografia chegam com contraste. Isso não deve se manter: a fila está muito
>   "suja", e o radiologista vai readequar os pedidos, fazendo sem contraste os que não precisam.
> - São só exames ambulatoriais, sem urgência.
> - Pode entrar uma parte de crianças no ultrassom (abdômen, pelve, aparelho urinário e bolsa escrotal), com idade
>   mediana de 3 a 11 anos.
>
> Se conseguirem me devolver até sexta (13/11), já consigo fechar a conta. Obrigado!

A mensagem e as duas planilhas não trazem preço, volume por clínica nem nada interno.

## 9. Quando as respostas chegarem

1. **Onde pôr:**
   - os minutos da TC vão na aba 1, bloco D, colunas E a G;
   - os do ultrassom, na aba 4, seção 2, uma tabela por pessoa;
   - a equipe, as pausas e as observações, na aba 6.
2. **O que olhar:**
   - na aba 2, seção 3, os exames por hora de cada resposta com as duas punções, e as cadeiras ou macas;
   - na aba 4, seção 1, as horas de sala do ultrassom pela média das respostas, contra o CBR;
   - na aba 5, a equipe de cada pessoa ao lado da referência, e as pausas.
3. **Os pontos de corte da TC, com 1/3 da carteira em cada polo:** o exame com contraste cabe em até 15,6 min de
   tomógrafo com 6 h por dia, em até 21,2 com 8 h e em até 26,9 com 10 h. Na prática:
   - menos de 8 h por dia não fecha com a punção na mesa;
   - menos de 6 h por dia não fecha nem com a punção antes.
4. **O tomógrafo de 4 canais:** o rascunho do Anexo põe um em Sobradinho. Se ele ficar entre os 3, o tempo dele
   precisa ser conferido à parte, porque é mais lento nas fases do contraste.

## Fontes

- `estudo_contraste_fluxo_tempo_20261108.md` e `.xlsx`: os tempos de cada etapa (aba 2), a carteira 1 (aba 3), a
  enfermagem do repouso (aba 4) e as medidas que agilizam (aba 8 e seção 10), com as 49 fontes.
- `estudo_12_meses_3_tomografos_20261107.md`: o arranjo dos 3 polos, com 403, 398 e 399 TC por mês, o fluxo em linha
  e os tempos do ultrassom pelo CBR 2017 (seção 2.1).
- `../plano.md` (v26), 4.8, 4.9, 4.15 e 4.16 (g): a triagem do contraste, a equipe, as jornadas e o acompanhante.
- `analise_despacho_gediag_20261108.md`: o que o despacho pede por polo (5.8, 5.9 e 5.11) e o tomógrafo de 4 canais.
- `../negociacao_clinicas_20261008.md`: os 3 turnos de 4 h por semana na Oeste.
- Parecer CFM 17/2019: o radiologista decide o contraste e fica na unidade durante o exame, até a alta (link no
  estudo de 08/11).
- Lei 7.394/1985, art. 14: a jornada de 24 h semanais do técnico em radiologia (no acervo, citada na v26, 4.15).
- CLT, art. 71: o intervalo para repouso e alimentação.

**Limites:**
- Os tempos de referência combinam medidas e estimativas. O tempo real é o da equipe assistencial, e depois o do mês 1.
- A parte de cada tomógrafo é 1/3 da carteira. Ela muda se a regulação repartir as Regiões de outro jeito.
- A equipe não conta férias nem faltas. A enfermagem do ultrassom, de 1 para 2 salas, é estimativa.
- A conta é de exames feitos. As faltas se cobrem com mais agendados por turno, como na negociação de 08/10. A falta
  que não se cobre vira hora parada, e os 80% de horas com exame só a absorvem em parte. É controle interno e não vai
  ao plano.
