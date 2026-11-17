# Contraste na tomografia: tempo, fluxo e regras

Estudo interno de 08/11/2026, a pedido do usuário. É uma pesquisa sobre o exame com contraste e uma análise com os
números do plano. A pesquisa cobre:
- quanto tempo ele ocupa o tomógrafo;
- como o usuário anda pelo polo;
- o que as diretrizes e as normas brasileiras exigem;
- o risco do exame;
- quanto dá para fazer sem contraste.

**Bases:**
- **v26 (PT v1):** 13.618 TC, 12.890 com contraste, 6 tomógrafos, 8 meses;
- **carteira 1:** 14.401 TC, 14.053 com contraste, 2.353 angiotomografias, sem coronária.

**Liga com:**
- o estudo de 05/11 (custos e cenários sem contraste);
- o de 07/11 (12 meses, 3 tomógrafos e fluxo em linha);
- a análise do Despacho GEDIAG 218755566 (08/11), que contesta a 4.8 do PT v1.

**Arquivos:**
- `estudo_contraste_fluxo_tempo_20261108.xlsx`, com dez abas. Tudo é fórmula; as células amarelas são premissas, e
  a aba 3 troca a base (v26 ou carteira 1) na célula B4;
- `gerar_estudo_contraste_fluxo_tempo_20261108.py`, o gerador.

Nada daqui vai ao plano sem decisão do usuário.

---

## Resposta curta

1. **Os 20 minutos da v26 estão certos para o contraste com punção na mesa.**
   - Medidos: 17 a 20 min de tomógrafo por exame.
   - Com o acesso feito antes, numa sala de preparo, são 12 a 15 min. Os 13 min do estudo de 07/11 são o piso, e
     **15 é o valor central**.
   - Sem contraste, são 9 a 11 min, e não os 15 da v26.
2. **A produção boa é de cerca de 3 exames por hora por tomógrafo.**
   - O HC-UFMG planeja com 20 min.
   - O pronto-socorro de Boston fez 3,2 exames por hora, perto do máximo de 3,8.
   - O Canadá mediu 3,0 a 3,2, igual com 4 ou 64 canais.
   - O parâmetro do Ministério é de 7.000 exames por ano.
3. **O que trava é o fluxo, não a máquina.**
   - Em Yale, o tomógrafo trabalhou em 31% do tempo; 78% do tempo parado veio de falha no fluxo de usuários.
   - Em Amsterdam, tirar a punção da sala encurtou em 5 min o tempo de atravessamento e levou o uso de 44% a 51%.
4. **A capacidade da v26 se mantém com os tempos medidos.**
   - Em série: 4.493 h, carga de 3,34 tomógrafos de 6.
   - Em linha: 3.397 h e carga de 2,53.
   - No pior caso, com todos os passos no máximo: 7.185 h e carga de 5,35.
   - **Carteira 1 com 3 tomógrafos:** 9,1 meses em série e 6,9 em linha (eram 6,0 com 13 min). No pior caso, 15,3
     meses: não fecha em 12.
5. **Três regras da 4.8 estão fora das diretrizes atuais, e a GEDIAG contestou as três.**
   - **A metformina para todos.** Pelo ACR e pelo ESUR, com filtração de 30 ou mais não se suspende nem se repete a
     creatinina.
   - **O repouso sem tempo mínimo.** As bulas do contraste pedem 30 min.
   - **A triagem renal sem lista nem prazo.**
   - A norma citada para a supervisão, a CFM 2.147/2016, trata do diretor técnico. As que tratam do contraste são o
     **Parecer CFM 17/2019** e a **Resolução CFM 2.107/2014, art. 8º**.
6. **O ACR 2026 é mais estreito do que a análise da GEDIAG supôs.**
   - Pede creatinina de quem tem doença renal ou toma metformina, e o diabetes é opcional.
   - Diz que idade e hipertensão geram falso positivo.
   - **O ESUR 2026 é que é largo:** hipertensão, diabetes e outros, ou todos os usuários, com validade de 3 meses.
   - A escolha decide se a creatinina vale para uma minoria ou para boa parte de uma fila de 60 anos.
7. **O repouso de 30 min não ocupa o tomógrafo, mas ocupa poltrona e enfermagem.**
   - Em linha: cerca de 5 poltronas por tomógrafo e 2 pessoas de enfermagem juntas no turno do contraste.
   - Em série: 3 poltronas e 1 pessoa.
8. **O radiologista tem de estar no polo enquanto houver contraste, até a alta (Parecer CFM 17/2019).**
   - Na v26: cerca de 3 h por dia em cada tomógrafo em linha, e 4 h em série.
   - Na carteira 1, com 3 tomógrafos em 12 meses: 4,3 e 5,7 h.
9. **Jejum:** o ACR e o ESUR não pedem. Um ensaio do A.C.Camargo, com 3.206 usuários de centro oncológico, não achou
   diferença nos sintomas. Sem jejum, o contraste não fica preso à manhã.
10. **Risco esperado nas 12.890 TC com contraste da v26:**
    - cerca de 77 reações de tipo alérgico, quase todas leves;
    - cerca de 5 reações graves;
    - de 13 a 155 extravasamentos.
11. **A conversão para sem contraste não fecha a conta.**
    - **Pelo menos 37% das três filas com contraste é câncer**, contando só os 5 CIDs principais. O abdômen pede fase
      portal (CBR).
    - Na rotina, o radiologista muda o contraste de 8,5% a 14% dos pedidos. Taxas de 38% a 61% só apareceram na falta
      de contraste de 2022, com mais exames repetidos.
    - **Planejar 10%.** No teste de 05/11, a TC própria só empata com 57% convertidos.
12. **Dá para agilizar sem equipamento novo** (seção 10, adendo do mesmo dia).
    - Com a punção fora da sala, o usuário pronto na porta, a bomba carregada e o pedido revisado na véspera, o
      exame com contraste ocupa o tomógrafo **13 min, e não 20**.
    - São 4,6 exames por hora, 54% a mais que em série, e o usuário fica cerca de 74 min no polo.
    - O preço é uma sala de preparo com 6 poltronas por tomógrafo, a enfermagem junta no turno do contraste e o
      pré-exame fazendo mais do que confirmar presença.

---

## 1. Quanto tempo o exame ocupa o tomógrafo

| fonte | onde | com contraste | sem contraste | o que mais mostra |
|---|---|---:|---:|---|
| Erdfarb, Forman e Tocino (RSNA 2005; tese de 2006) | Yale, EUA; 225 usuários | 17,1 min (DP 7,4) | 8,6 min (DP 4,2) | tomógrafo ativo em 31% do tempo; 78% do tempo parado por fluxo de usuários |
| Stenson et al. (Am J Emerg Med 2021) | PS de Boston | 12,1 min na sala, todos os exames (mediana) | | mais 3,6 min de sala vazia; 3,2 exames/h, máximo de 3,8 |
| Santos Junior (dissertação, UFMG 2024) | HC-UFMG; acesso feito na sala de preparo | 15 min (10 a 20) | | capacidade calculada com 20 min (3/h); o termo leva 15 min; sem médico à noite, tudo é sem contraste |
| Chang et al. (Kingston, Reino Unido) | auditoria de 1.458 TC | cerca de 8 min por punção feita no serviço | | vagas de 10 min (ambulatório) e 15 (internação e PS) |
| Elkhuizen et al. (Health Care Manage Rev 2007) | AMC, Amsterdam | 5 min a menos com a punção fora da sala | | uso de 44% para 51%; espera pelo exame de 21 para menos de 5 dias |
| Zimmerman et al. (JCCT 2021) | 7 serviços dos EUA | processo inteiro: 37 min (tórax) | | angio de coronárias: 121 min |
| Ministério da Saúde, Parâmetros SUS (NESCON/UFMG) | Brasil | | | 7.000 exames/ano por tomógrafo; no Canadá, 3,0 a 3,2/h com 4 a 64 canais |
| CDA-AMC (2025) | Canadá, 2022 e 2023 | | | 2,34 exames por hora aberta (1,89 a 3,43) |
| v26 / estudo de 07/11 | | 20 / 13 | 15 / 10 | |

O conjunto completo, com 16 fontes, está na aba 1 da planilha.

**Leitura:**
- **Em série** (punção na mesa), o exame com contraste leva 17 a 20 min. A v26 acerta.
- **Em linha** (acesso feito antes), leva 12 a 15. O valor medido mais próximo do que o plano faria é o do HC-UFMG:
  15 min de média, com o acesso puncionado na sala de preparo.
- **Sem contraste**, leva 9 a 11. A v26 conta 15.
- **O número de canais quase não muda a produção** de exames comuns, porque o preparo pesa mais que a aquisição. Isso
  vale para o Canadá, com 4 a 64 canais.
- **Para a angio de coronárias, o número de canais pesa.** A SCCT pede no mínimo 64. O tomógrafo de 4 canais de
  Sobradinho não serve para ela, e a carteira 1 já tirou a coronária.

## 2. O fluxo do usuário

| fluxo | tomógrafo, min (mín / central / máx) | exames/h | usuário no polo (central) |
|---|---|---:|---:|
| A. Sem contraste | 9 / **11** / 17 | 5,5 | 24 min |
| B. Com contraste em série: punção na mesa (a conta da v26) | 15 / **20** / 34 | 3,0 | 71 min |
| C. Com contraste em linha: punção na sala de preparo | 11 / **15** / 19 | 4,0 | 87 min |
| D. Angio de coronárias, frequência controlada fora da sala | 13 / **20** / 34 | 3,0 | 120 min |

O passo a passo, com quem faz e a fonte de cada número, está na aba 2. O tempo no polo já conta 30 min de repouso.

**O que pesa em cada fluxo:**
- **Em série, a punção na mesa é a parte que mais varia:** cerca de 8 min no relato de Kingston, e mais na veia
  difícil. A fila é oncológica, com veias gastas pela quimioterapia e o braço da mama operada fora da punção. É dela
  que vem o pior caso.
- **Em linha, o tomógrafo ganha, mas o usuário fica mais tempo no polo.** Ele chega cerca de 40 min antes e espera
  pronto, com o acesso feito.
- **Na coronária, o tempo do usuário depende do betabloqueador.** O oral leva cerca de 1 h. Num ensaio de 2011, o
  atendimento levou 120 min com o oral e 35 com o venoso, com o tempo na sala igual.
- **O termo de consentimento leva 15 min** quando o usuário preenche sozinho (HC-UFMG). Lido no contato antes do
  exame e na orientação em grupo, sai do tempo do polo.
- **O contraste oral, se o RT usar no abdômen**, pede de 60 a 90 min de ingestão. No pronto-socorro, tirá-lo
  encurtou a permanência em 97 min (Levenson, 2012). Essa espera fica na sala de preparo, não no tomógrafo.

## 3. Capacidade com os tempos medidos

**v26, 6 tomógrafos, 8 meses, 10 h por dia, 80% com exame, 10% convertidos (aba 3):**

| | v26 como está | em série (central) | em linha (central) | em linha (melhor caso) | em série (pior caso) |
|---|---:|---:|---:|---:|---:|
| horas de tomógrafo | 4.479 | 4.493 | 3.397 | 2.481 | 7.185 |
| uso dos 6 tomógrafos | 55,5% | 55,7% | 42,1% | 30,8% | 89,1% |
| carga, em tomógrafos | 3,33 | 3,34 | 2,53 | 1,85 | 5,35 |
| horas de contraste por dia em cada tomógrafo | 4,3 | 4,1 | 3,0 | 2,2 | 6,6 |

**Carteira 1, 3 tomógrafos, 12 meses:**

| | v26 como está | em série | em linha | melhor caso | pior caso |
|---|---:|---:|---:|---:|---:|
| meses para fazer toda a TC | 9,5 | 9,1 | 6,9 | 5,1 | 15,3 |
| horas de contraste por dia em cada tomógrafo | 6,2 | 5,7 | 4,3 | 3,1 | 9,7 |

**Leitura:**
- **A conclusão de 07/11 fica de pé:** em linha, 3 tomógrafos sobram em 12 meses. Com o tempo central de 15 min, são
  6,9 meses de trabalho, e não 6,0.
- **O risco está no fluxo em série com punção difícil:** no pior caso, a carteira 1 não fecha com 3 tomógrafos.
  O tempo real precisa ser medido no mês 1, como o estudo de 07/11 já pedia.
- **O turno do radiologista é a linha que mais pesa na agenda.** Em linha, cabe num turno de 5 h; em série, quase
  enche o dia.

## 4. As regras que mudam o fluxo

A tabela completa, com o ACR 2026, o ESUR 2026 e as normas brasileiras, está na aba 7.

| tema | v26 (4.8) | o que dizem | sugestão para a próxima versão |
|---|---|---|---|
| jejum | não diz se a TC com contraste pede | ACR e ESUR: não pedir; ensaio do A.C.Camargo: sem diferença | sem jejum, salvo sedação |
| creatinina | só de quem tem doença renal | ACR 2026: doença renal, metformina e, opcional, diabetes; idade e hipertensão dão falso positivo. ESUR 2026: hipertensão, diabetes e outros, ou todos | lista do ACR, com a metformina; o RT decide se segue o ESUR |
| validade da creatinina | "válida", sem prazo | ACR: sem prazo (muitos aceitam 30 dias); ESUR: 3 meses, ou 7 dias se há doença aguda | 90 dias para quem está estável; 7 para doença aguda |
| metformina | todo usuário só reinicia após 48 h e nova creatinina | ACR e ESUR: com filtração de 30 ou mais, não suspende; abaixo de 30 ou com lesão aguda, 48 h e nova dosagem | alinhar; hoje a regra manda todo diabético colher sangue depois |
| observação | "não há tempo mínimo" | bulas: 30 min. ACR: quase toda reação grave em 20 min. ESUR 2026: 30 min com acesso para quem já reagiu. CFM 17/2019: médico no serviço até a alta | 30 min com o acesso mantido; mais para quem já reagiu |
| médico presente | "conforme a Resolução CFM nº 2.147/2016" | Parecer CFM 17/2019: médico no espaço físico durante todo o exame contrastado. CFM 2.107/2014, art. 8º: TC exige especialista local | citar as duas; o turno do contraste é o turno do radiologista |
| quem decide | o radiologista, diante de contraindicação | Parecer CFM 17/2019: indicação, dose e prescrição são do radiologista; fazer sem contraste não é infração, com o motivo registrado | registrar o motivo de cada conversão |
| punção e injeção | enfermagem, com supervisão | conselhos: a enfermagem punciona e injeta; o técnico em radiologia pode injetar pelo acesso feito, mas não punciona | manter; enfermeiro na punção difícil |
| reação anterior | "alergia prévia" | ACR: pré-medicação oral começando 12 h antes, ou venosa de ao menos 4 a 5 h (2 h ou menos não funciona), com 2,1% de reação de escape; ESUR: trocar de contraste e observar 30 min | escrever a conduta: sem contraste, pré-medicação ou hospital |

**Duas correções à análise do despacho GEDIAG (08/11):**
- **A lista de risco renal.** A análise diz que as diretrizes usam idade acima de 60, diabetes, hipertensão,
  metformina e doença renal. Isso é a lista antiga do ACR. O ACR 2026 tirou idade e hipertensão, e o ESUR 2026 pôs a
  hipertensão.
- **O acervo.** As duas diretrizes foram lidas inteiras nesta pesquisa, mas continuam fora do acervo.

## 5. Repouso, poltronas e enfermagem

Conta por tomógrafo, pela lei de Little: usuários ao mesmo tempo = chegadas por hora × horas de permanência (aba 4).

| | em série | em linha |
|---|---:|---:|
| exames com contraste por hora | 3 | 4 |
| usuários em repouso ao mesmo tempo (30 min) | 1,5 | 2,0 |
| usuários na sala de preparo ao mesmo tempo | 0 | 1,5 |
| **poltronas, com 1 de folga** | **3** | **5** |
| minutos de enfermagem por exame (triagem, termo, punção e alta) | 20 | 19 |
| **enfermagem ocupada ao mesmo tempo** | 1,0 | **1,3** |

**Leitura:**
- **Em linha, a enfermagem vira o gargalo.** As 2 pessoas por tomógrafo da v26 servem, desde que estejam juntas no
  turno do contraste, e não em turnos que se cobrem.
- **O técnico em radiologia pode conectar a bomba ao acesso já feito,** sob supervisão. Isso tira minutos da
  enfermagem.
- **A análise do despacho estimou cerca de 5 poltronas** com 30 min de repouso. A conta confirma.

## 6. Segurança em números

Taxas do ACR 2026 (aba 5):

| | v26 (12.890 com contraste) | carteira 1 (14.053) |
|---|---:|---:|
| reações de tipo alérgico (0,6%) | 77 | 84 |
| reações graves (0,04%) | 5 | 6 |
| extravasamentos (0,1% / 0,3% / 1,2%) | 13 / 39 / 155 | 14 / 42 / 169 |
| reações tardias, de pele (0,5% a 14%) | 64 a 1.805 | 70 a 1.967 |

**Leitura:**
- **A probabilidade por exame é baixa, mas o projeto tem volume.** Algumas reações graves são esperadas. Por isso
  pesam o médico presente, o suporte, o fluxo de transferência e os 30 min de repouso com acesso.
- **No Brasil,** o HCPA registrou 1% de reações leves com contraste não iônico e 2,2% de extravasamento, em internados
  (2007).
- **As reações tardias acontecem em casa.** A orientação de alta precisa dizer o que fazer e para onde ligar.

## 7. Conversão para sem contraste: quanto é realista

**A base legal existe.** Pelo Parecer CFM 17/2019, o radiologista decide o contraste. Fazer sem contraste o pedido
com contraste não é infração, desde que ele registre o motivo técnico, e o solicitante não pode impor o contraste.

**A fila (Mapa Social, 02/11; os 5 CIDs mais frequentes, aba 6):**

| fila | pedidos | câncer nos 5 CIDs | dor abdominal (R10) |
|---|---:|---:|---:|
| TC do abdômen superior com contraste | 4.116 | 35,1% (mama, cólon, reto, estômago) | 7,8% |
| TC de pelve com contraste | 3.639 | 33,9% | 8,4% |
| TC do tórax com contraste | 2.350 | 46,6% (mais pulmão) | — |
| três filas | 10.105 | **37,4%** | 6,2% |

A idade mediana é de 59 a 61 anos. É estadiamento e seguimento de câncer, e o painel não mostra os outros CIDs.

**Por exame:**
- **Tórax:** o CBR faz a TC "geralmente sem contraste". Há espaço para converter no seguimento de nódulo ou metástase
  pulmonar.
- **Abdômen e pelve:** o CBR pede ao menos a fase portal, porque é ela que mostra a metástase no fígado. O espaço é
  pequeno, salvo a dor abdominal com suspeita de cálculo.

**O que a evidência mostra:**

| situação | taxa |
|---|---:|
| rotina: o radiologista muda o uso do contraste, para pôr ou tirar (RSNA 2014, cerca de 220 mil pedidos) | 8,5% |
| rotina: pedidos de TC com contraste do PS mudados ou cancelados (Yale, 2018) | 14% |
| falta de contraste, 2022: abdômen e pelve feitos sem contraste, com mais exames repetidos (Vermont) | 38% a 55% |
| falta de contraste, 2022: queda da TC de tórax com contraste (um sistema dos EUA) | 61% |
| modelo: contraste poupado se toda TC com contraste não essencial fosse sem (JAMA 2022; não mede o dano) | 78% |

**O que cada nível rende na v26:**

| | rotina, 10% | ampliada, 20% | crise, 50% |
|---|---:|---:|---:|
| exames convertidos | 1.148 | 2.296 | 5.741 |
| horas de tomógrafo poupadas, em série (9 min cada) | 172 | 344 | 861 |
| horas poupadas, em linha (4 min cada) | 77 | 153 | 383 |
| reações de tipo alérgico evitadas | 7 | 14 | 34 |
| margem da TC própria, teste de 05/11 | −R$ 929.616 | −R$ 732.355 | −R$ 140.573 |

**Leitura:**
- **Planejar 10%,** que é o que o estudo de 07/11 já usava. Tratar 20% como teto razoável, puxado pelo tórax.
- **50% ou mais é cenário de falta de contraste,** com mais exames repetidos.
- **No teste de 05/11,** com os valores sugeridos da planilha de custos, a TC própria só empata com **57%
  convertidos**. A conversão poupa contraste, punção e reação, mas não fecha a conta. O custo tem de cair por outro
  lado: preço do contraste, aluguel ou a clínica parceira.

## 8. O que medir no mês 1

Por polo e por tomógrafo, por escrito:

1. tempo de tomógrafo por exame, da entrada à saída, com contraste, sem contraste e angio;
2. tempo de troca entre usuários e as horas paradas à espera de usuário;
3. punção difícil: mais de duas tentativas, ou feita pelo enfermeiro;
4. parte dos pedidos com contraste feita sem contraste, com o motivo;
5. reações por gravidade e extravasamentos, por 1.000 injeções;
6. usuários que precisaram de creatinina e os que chegaram sem ela;
7. tempo do usuário no polo, da chegada à alta.

## 9. O que precisa ser decidido

Na ordem em que travam o resto:

1. **A nova 4.8**, que responde ao despacho:
   - sem jejum;
   - a lista de risco renal e a validade da creatinina;
   - a metformina pelo ACR e pelo ESUR;
   - 30 min de repouso com o acesso mantido;
   - as normas do CFM certas;
   - a conduta na reação anterior.

   O RT de cada clínica precisa assinar o POP.
2. **ACR ou ESUR na triagem renal.** O ACR deixa a creatinina para uma minoria. O ESUR a estende a boa parte da fila,
   com custo de laboratório.
3. **O fluxo da TC com contraste:** em linha (sala de preparo, 5 poltronas e 2 de enfermagem juntas no turno) ou em
   série.
4. **O tempo por procedimento para o Anexo,** que o despacho pede (5.6 e 5.11): 11 min sem contraste, 15 com
   contraste em linha (ou 20 em série) e o mesmo para a angiotomografia. É valor de planejamento até a medida do mês 1.
5. **A premissa de conversão:** 10% para planejar, e não contar com ela para fechar o custo.
6. **Pôr o ACR 2026 e o ESUR 2026 no acervo**, para a próxima versão citar.

## 10. Adendo, no mesmo dia: o que muda no fluxo com contraste e o que agiliza

Pergunta do usuário, depois da primeira entrega: o que muda no fluxo com contraste e o que pode ser feito para
agilizar. As medidas, o ganho e a fonte de cada uma estão na aba 8; o fluxo E da aba 2 aplica todas.

### 10.1 O que o contraste acrescenta

| | sem contraste | com contraste |
|---|---|---|
| triagem | questionário e gestação | mais alergia, rim, metformina e termo de consentimento |
| creatinina | não | de quem tem risco, pela lista do RT, consultada antes do dia |
| acesso venoso | não | punção pela enfermagem, cateter 20G ou maior |
| tomógrafo | 11 min | 20 em série, 15 em linha, 13 com as medidas |
| depois do exame | sai | 30 min de repouso com o acesso; alta com orientação sobre reação tardia |
| médico | | radiologista no polo durante todo o exame, até a alta (Parecer CFM 17/2019) |
| usuário no polo | 24 min | de 71 a 87 min |

São quatro passos a mais (triagem ampliada, punção, injeção e repouso), uma pessoa a mais (a enfermagem) e uma
condição de agenda (o radiologista presente).

### 10.2 O fluxo com as medidas

**Antes do dia, no pré-exame que a v26 já tem (4.5 e 4.6):**
1. o operador lê o termo com o usuário, aplica o questionário (alergia, rim, metformina, gestação) e avisa que não
   há jejum;
2. o pré-exame consulta a creatinina no TrakCare de quem tem risco e pede o exame que faltar;
3. na véspera, o radiologista define o protocolo de cada pedido: com ou sem contraste, fases, contraste oral, e
   pré-medicação de quem já reagiu.

**No dia:**
1. o usuário com contraste chega 40 min antes do horário do tomógrafo; o sem contraste, 15;
2. a recepção só identifica, porque o cadastro foi conferido na véspera;
3. orientação em grupo e assinatura do termo;
4. troca de roupa e punção na sala de preparo, com o enfermeiro na veia difícil;
5. espera pronto: um ou dois usuários puncionados na porta do tomógrafo;
6. exame, com a bomba carregada antes de o usuário entrar e o técnico em radiologia conectando ao acesso;
7. 30 min de repouso com o acesso, em poltrona fora da sala de preparo;
8. alta, com a retirada do acesso e a orientação por escrito.

**Na abertura:** a sala de preparo abre de 30 a 40 min antes do tomógrafo, para os dois primeiros usuários já
entrarem puncionados.

### 10.3 O ganho

Base v26, premissas da aba 3 (aba 8):

| | em série (a conta da v26) | em linha | em linha, com as medidas |
|---|---:|---:|---:|
| minutos de tomógrafo por exame com contraste | 20 | 15 | **13** |
| exames com contraste por hora | 3,0 | 4,0 | **4,6** |
| exames com contraste por dia, por tomógrafo | 24 | 32 | 37 |
| tempo do usuário no polo | 71 min | 87 min | 74 min |
| carga da v26, em tomógrafos | 3,34 | 2,53 | 2,27 |
| carteira 1 com 3 tomógrafos, em meses | 9,1 | 6,9 | 6,1 |
| poltronas por tomógrafo | 3 | 5 | 6 |
| enfermagem ocupada ao mesmo tempo | 1,0 | 1,3 | 1,2 |

**Leitura:**
- **O tomógrafo ganha 54%** (de 3 para 4,6 exames por hora).
- **O usuário fica quase o mesmo tempo no polo** que em série, porque o que sai do dia vai para o pré-exame.
- **O que se paga:** mais poltronas, mais enfermagem junta no turno e mais trabalho no pré-exame.

### 10.4 As medidas, pelo tamanho do ganho

**No tempo de tomógrafo:**
- **punção fora da sala:** −5 min por exame. Em Amsterdam, o uso do tomógrafo foi de 44% para 51%. Em Kingston, cada
  punção na sala custou cerca de 8 min;
- **usuário pronto e bomba carregada:** −2 min. Sem usuário pronto a cada intervalo, o máximo não sai (Stenson). Em
  Yale, 78% do tempo parado veio do fluxo;
- **primeiro horário pronto:** em Manchester, a primeira hora rendia 1,6 exame contra 5,7 nas outras. Num serviço dos
  EUA, o início no horário passou de 11% para 82%;
- **duas pessoas de enfermagem juntas no turno do contraste:** em linha, há de 1,2 a 1,3 pessoa ocupada o tempo todo.

**No tempo do usuário e no exame perdido:**
- **pedido revisado antes do dia:** em Temple, revisar os pedidos 3 dias antes, juntar os formulários e refazer a
  agenda levou o tempo da chegada ao exame de 3,1 h para 1,1 h, com 19% mais exames por dia. No HC-UFMG, o usuário
  esperava de 15 a 30 min a decisão do médico sobre o contraste;
- **termo e questionário no pré-exame:** −7 a −10 min no dia. No HC-UFMG, o termo leva 15 min;
- **sem jejum:** a v26 (4.5) diz que o preparo errado é a causa mais frequente de exame não feito. Tirar o jejum da
  TC tira uma das causas;
- **creatinina só para quem tem risco, e metformina sem exame depois;**
- **agenda em blocos:** contraste no turno do radiologista; sem contraste e reserva nos intervalos. A agenda de 5 em
  5 min do HC-UFMG enchia a recepção;
- **contraste oral só quando o radiologista pedir:** −60 a −90 min no polo.

**Para sustentar o ritmo:**
- **veia difícil com enfermeiro e ultrassom:** acerto na primeira tentativa cerca de 3 vezes mais provável
  (meta-análise de 2023). A fila é oncológica;
- **técnico em radiologia conectando a bomba;**
- **poltronas suficientes para o repouso de 30 min;**
- **medir desde o mês 1.**

### 10.5 O que a v26 já tem e o que falta

**Já tem:**
- o contato depois do agendamento e a confirmação na véspera (4.5 e 4.6);
- a creatinina consultada no TrakCare (4.8);
- 2 pessoas de enfermagem por tomógrafo (7.1).

**Falta:**
- dizer que o pré-exame lê o termo e aplica o questionário;
- o protocolo do radiologista na véspera;
- "sem jejum";
- a sala de preparo com poltronas e os 30 min de repouso;
- a enfermagem junta no turno do contraste;
- a agenda em blocos no turno do radiologista.

**Onde entra na próxima versão:** na 4.5, na 4.6, na 4.8 e no quadro de equipe. O despacho já pede tempo por
procedimento e profissionais por turno (5.11).

## Fontes

A lista completa, com 49 fontes e o modo como cada uma foi lida, está na aba Fontes. As principais:

- ACR Manual on Contrast Media, 2026: https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/Contrast-Manual
- ESUR Contrast Media Safety Committee Guidelines 2026: https://www.esur.org/esur-guidelines-2026/
- Parecer CFM 17/2019: https://cbr.org.br/wp-content/uploads/2023/08/Parecer-CFM-de-2019-no-17_Uso-de-contraste.pdf
- Parecer jurídico do CBR sobre a prescrição de contraste (cita a Resolução CFM 2.107/2014, art. 8º):
  https://cbr.org.br/wp-content/uploads/2026/04/Parecer-sobre-Responsabilidade-pela-Prescricao-de-Meios-de-Contraste-para-Exames-de-Imagem.pdf
- CBR, Protocolos iniciais de TC (2021): https://cbr.org.br/wp-content/uploads/2022/03/Protocolos-de-Tomografia-Computadorizada-1.pdf
- Santos Junior, Lean na TC do HC-UFMG (2024): https://repositorio.ufmg.br/handle/1843/81992
- Erdfarb et al., RSNA 2005: https://archive.rsna.org/2005/4407929.html
- Elkhuizen et al., AMC Amsterdam (2007): https://research.utwente.nl/en/publications/applying-the-variety-reduction-principle-to-management-of-ancilla/
- Ministério da Saúde, Parâmetros SUS, Seção D: https://www.gov.br/saude/pt-br/acesso-a-informacao/gestao-do-sus/programacao-regulacao-controle-e-financiamento-da-mac/programacao-assistencial/arquivos/se-o-d-equipamentos.pdf
- CDA-AMC, exames de TC por hora no Canadá (2025): https://canjhealthtechnol.ca/index.php/cjht/article/view/CM0028
- Barbosa et al., jejum no A.C.Camargo (AJR 2018): https://doi.org/10.2214/AJR.17.19061
- Coser et al., contraste e lesão renal (Radiol Bras 2021): https://www.scielo.br/j/rb/a/3jKDntc59srhJjTshYX9jVP/?lang=en
- Davenport et al., JAMA 2022: https://jamanetwork.com/journals/jama/fullarticle/2793384
- Fila: `../dados/fontes/mapa_social_20261102_imagem.md` (coleta de 02/11/2026).

**Limites:**
- Parte das fontes de tempo foi lida só pelo resumo; a aba Fontes diz qual.
- Os tempos de Stenson, Kingston e Vermont vieram de trechos e notícias, não do artigo inteiro.
- Os minutos de cada passo do fluxo combinam medidas e estimativas. O tempo real é o do mês 1.
