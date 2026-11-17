# Readequação do plano 4 à Candanga: dois cenários pela margem de cada exame

Estudo interno de 09/11/2026, a pedido do usuário, revisto no mesmo dia. Controle interno: a margem não vai ao plano.

**Os dois cenários:**
1. **Cenário 1:** a v26 como está, com as mesmas metas, paga pela Candanga. Só os cerca de R$ 245 mil que sobram são
   readequados.
2. **Cenário 2:** as filas escolhidas de novo, pela margem de cada exame, pela complexidade e pela fila que existe:
   a de hoje e os pedidos novos dos 12 meses.

**Decisões do usuário em 09/11, já na conta:**
- a TC na clínica custa **R$ 175 sem contraste, mais R$ 50 com contraste** (R$ 225);
- a **US pélvica ginecológica** fica fora da conta;
- as **angiotomografias voltam**, menos a de coronárias. Só a coronária pede betabloqueador, controle da frequência e
  ECG; as outras são uma TC com contraste com injeção mais rápida;
- **crianças entram**, sem limite de idade no plano (D-010). As filas infantis de abdômen total, aparelho urinário,
  bolsa escrotal e tireoide voltam à conta.

**Arquivos:**
- `estudo_readequacao_candanga_margem_20261109.xlsx`, com as abas Premissas, Margem por exame, Cenário 1, Cenário 2
  Comparação e Contraste. Tudo é fórmula, e o amarelo é premissa. A planilha está com o médico do ultrassom pago por hora;
- `gerar_readequacao_candanga_margem_20261109.py`, o gerador. As quantidades escolhidas saem dele. Para o médico pago
  por exame, rode com `MEDICO_MODO=exame`.

**Fontes:**
- o estudo das filas de 02/11: as filas, a regra de um pedido, um plano (L-008), os preços da Candanga, os minutos e
  a demanda por código;
- o estudo de 05/11: a v26 pela Candanga, que vale R$ 10.390.824,04, e a sobra;
- o custo v2 de 20/10: a sala, o aparelho, os insumos e o médico por exame;
- o formulário de 09/11: o auxiliar de sala do ultrassom.

---

## Resposta curta

1. **A margem é a folga para executar, e não lucro.** No convênio, o que não se gasta volta como saldo ou vira mais
   exames. Ela mostra quais exames pagam o próprio custo e quais não pagam.
2. **O que cada exame deixa, em % do preço, com o médico pago por hora:**

   | exame | margem | por quê |
   |---|---:|---|
   | US de abdômen superior, bolsa escrotal, aparelho urinário, abdômen total e parede | 50% a 56% | preço bom, 15 a 20 min |
   | Doppler de carótidas | 49% | 20 min |
   | US transvaginal | 46% | 15 min |
   | TC sem contraste (abdômen, pelve, tórax) | 43% | R$ 309,25 menos R$ 175 |
   | US de próstata | 39% | preço baixo |
   | TC de crânio sem contraste e US de tireoide | 30% | preços de R$ 251,29 e R$ 64,07 |
   | **TC com contraste e angiotomografias** | **27%** | R$ 309,25 menos R$ 225 |
   | US de mamas | 17% | a Candanga paga 29% menos que a v26 |
   | TC de face e de crânio com contraste, angio do crânio | 11% a 14% | preço do código menor e o mesmo custo de R$ 225 |
   | **Doppler de membros** | **0,5%** | 40 min de sala e de médico pelo mesmo preço do Doppler de carótidas |

   Nas crianças, a margem é a mesma do exame do adulto.
3. **Com o dinheiro fixo, a margem que importa é a % do preço.** A hora pesa onde ela é escassa, que é no tomógrafo
   com 3 polos.
4. **Cenário 1** (v26 e a sobra): a sobra vai a 2.350 ultrassons a mais, de abdômen superior, aparelho urinário e
   abdômen total. A margem fica em **R$ 3,40 mi (32%)**, mas **R$ 1,14 mi das metas da v26 está em exames sem fila ou
   já descartados** (seção 2).
5. **Cenário 2** (escolher de novo), com o médico pago por hora: 79.714 exames e margem de **R$ 3,50 mi (33%)**.
   - Entram toda a TC, as angiotomografias e o ultrassom de adultos e crianças.
   - **O Doppler de membros fica com só 6.112 exames, metade da fila de hoje (12.043).** Pago por hora, ele quase não
     paga o próprio custo, e por isso fica por último.
6. **O que eu escolheria: o cenário 2 com o médico do ultrassom pago por exame** (seção 4).
   - **A margem sobe** para **R$ 3,59 mi (34%)**, e o Doppler de membros vai a 29%.
   - **Entra toda a fila de hoje.** Ficam de fora só a TC de crânio e de face com contraste e a angio do crânio (896
     exames de margem baixa), além de parte dos pedidos novos.
   - **O uso:** salas de ultrassom em 88% e tomógrafos em 70%.

---

## 1. Como a margem foi calculada

**Ultrassom, feito por nós:**
- sala e aparelho, R$ 5.500 por mês, ou R$ 32,74 por hora de exame (custo v2 de 20/10);
- dois auxiliares de sala, R$ 5.918 por mês, ou R$ 35,23 por hora (formulário de 09/11);
- R$ 3 de insumos por exame;
- o médico de duas formas: **R$ 100 por hora** (estudo de 02/11) ou **R$ 33,33 por exame** (modelo do ISHP de 20/10,
  R$ 1.000 por lote de 30).

**Por que a forma de pagar o médico muda tanto:** por hora, o exame longo paga mais médico. O Doppler de membros (40
min) custa R$ 66,67 de médico por hora, e R$ 33,33 por exame. O exame de 15 min faz o contrário: R$ 25 por hora e
R$ 33,33 por exame.

**Tomografia, na clínica:** R$ 175 por exame sem contraste e R$ 225 com contraste (usuário, 09/11).

**Não entram:** a recepção do polo, que não muda com o tipo de exame, e a gestão, que é paga pelo apoio.

**Fila:**
- a fila de hoje é a elegível da coleta de 02/11. Ela já tira a L-008, a coronária, a transfontanela, a pélvica e as
  filas de emergência;
- os pedidos novos em 12 meses são o que entra por mês e a SES não agenda, vezes 12, só quando positivo.

## 2. Cenário 1: a v26 como está, e só a sobra

| | médico por hora | médico por exame |
|---|---:|---:|
| metas da v26 pela Candanga | 79.144 exames | 79.144 exames |
| a sobra vai a | 2.350 US de abdômen superior, urinário e abdômen total | 2.091 US de abdômen total |
| margem | R$ 3,40 mi (32%) | R$ 3,53 mi (33%) |

**Por que a sobra não vai à TC:** a TC com contraste deixa 27% do preço, contra cerca de 50% do ultrassom de abdômen.
Além disso, a hora do tomógrafo é o recurso mais apertado com 3 polos.

**O risco é a base, e não a sobra:**

| linha da v26 | meta | o problema | valor em risco |
|---|---:|---|---:|
| transvaginal | 10.541 | fila disponível de 5.294, sem a reserva da GIN1 | R$ 439 mil |
| mama | 14.689 | fila de 14.134 em 12 meses; a SES fez mutirões | R$ 39 mil |
| angio de coronárias | 1.408 | fora por decisão do usuário (02/11) | R$ 435 mil |
| TC de tórax de emergência | 728 | só ambulatório (D-009) | R$ 225 mil |
| **total** | | | **R$ 1,14 mi** |

Para manter as metas da v26, esses R$ 1,14 mi teriam de ir para outras filas. É o que a carteira 1 já fez.

## 3. Cenário 2: escolher de novo

**A regra:**
1. Primeiro a fila de hoje, da maior para a menor margem.
2. Depois os pedidos novos dos 12 meses, na mesma ordem.
3. Abaixo de 15% de margem, o exame só entra no fim, para fechar o valor.

| | médico por hora (a planilha) | médico por exame (recomendado) |
|---|---:|---:|
| exames | 79.714 | 80.875 |
| margem | R$ 3,50 mi (33%) | R$ 3,59 mi (34%) |
| Doppler de membros | 6.112, metade da fila de hoje | 12.043, toda a fila de hoje |
| TC de crânio e de face com contraste, angio do crânio | 896, por último | fora |
| pedidos novos que entram | 9.200 | 5.326 |
| uso das salas de ultrassom (14 salas) | 78% | 88% |
| uso dos 3 tomógrafos | 79% | 70% |

**Como ler:**
- **A demanda que pode entrar mal passa do valor.** Por isso não dá para escolher só o que paga bem: a escolha é o
  que fica por último.
- **Com o médico pago por hora,** o último da fila é o Doppler de membros, e metade da fila dele fica de fora. É a
  maior fila depois da mama, e a SES vai perguntar por ela.
- **Com o médico pago por exame,** o Doppler de membros paga o próprio custo e entra inteiro. O que fica de fora são
  896 TC de margem baixa e parte dos pedidos novos (abdômen superior, urinário, próstata, tireoide, mama e Doppler).

## 4. O que eu escolheria

**O cenário 2 com o médico do ultrassom pago por exame:**
1. **Entra toda a fila de hoje,** de adultos e crianças, menos 896 TC de margem baixa.
2. **Não promete exame sem fila** e respeita as decisões já tomadas: sem emergência, sem coronária, sem pélvica e sem
   sobreposição com o IEV.
3. **Tem a maior margem das opções:** R$ 3,59 mi (34%).

**Com estes cuidados:**
- **O pagamento por exame precisa ser aceito pelos médicos,** inclusive no Doppler de membros, que leva 40 min. Se
  eles pedirem mais pelo Doppler, a conta volta para perto do médico por hora.
- **A TC de crânio e de face com contraste e a angio do crânio** deixam de 11% a 14%. Se a SES pedir, entram no lugar
  de pedidos novos.
- **Os pedidos novos são controle interno.** O plano não promete pedido novo, e, se a SES continuar com mutirões, eles
  não vêm.

## 4.1 E se nem todo pedido com contraste for feito com contraste (aba 5)

O radiologista vai readequar os pedidos, porque a fila está muito "suja". Cada exame feito sem contraste:
- **paga o mesmo,** porque o código é o mesmo;
- **custa R$ 50 a menos** na clínica;
- **ocupa o tomógrafo 11 min, e não 20.**

Os pedidos que podem ir sem contraste são o abdômen, a pelve, o tórax, o pescoço, o crânio e a face. As
angiotomografias não vão sem contraste. Valores com o médico pago por hora:

| feito com contraste | cenário 1: exames sem contraste | cenário 1: margem | cenário 2: exames sem contraste | cenário 2: margem | cenário 2: uso dos tomógrafos |
|---:|---:|---:|---:|---:|---:|
| 100% | 0 | R$ 3,40 mi (32%) | 0 | R$ 3,50 mi (33%) | 79% |
| 90% | 1.148 | R$ 3,45 mi | 1.187 | R$ 3,56 mi | 76% |
| 80% | 2.296 | R$ 3,51 mi | 2.374 | R$ 3,62 mi | 74% |
| 70% | 3.445 | R$ 3,57 mi | 3.561 | R$ 3,68 mi | 71% |
| 60% | 4.593 | R$ 3,62 mi | 4.748 | R$ 3,74 mi | 68% |
| 50% | 5.741 | R$ 3,68 mi (35%) | 5.935 | R$ 3,80 mi (36%) | 65% |

**Como ler:**
- **Cada 10 pontos a menos de contraste somam cerca de R$ 60 mil de margem** e poupam cerca de 175 horas de tomógrafo.
- **O que mais muda é o turno do radiologista.** No cenário 2, as horas de contraste por dia em cada tomógrafo caem de
  6,5 (100%) para 3,3 (50%), sem contar as angiotomografias. Abaixo de 5 h, o contraste cabe num turno, e a 2ª pessoa
  de enfermagem e o 2º radiologista deixam de ser necessários (estudo de tempos de 09/11).
- **As quantidades não mudam:** o preço é o mesmo, então a readequação não abre espaço para mais exames, só folga.
- **O realista:** na rotina, o radiologista muda o contraste de 8,5% a 14% dos pedidos (90%). Uma fila "suja" pode dar
  mais; 50% só apareceu na falta de contraste de 2022, com mais exames repetidos. Cerca de 37% da fila é câncer, que
  pede fase com contraste (estudo de 08/11).

## 4.2 Exame a exame (aba 6)

O cenário 2 no formato do cenário 1, com a diferença de cada exame (médico pago por hora):

| | cenário 1 | cenário 2 | diferença |
|---|---:|---:|---:|
| **o que sai** | | | |
| US transvaginal | 10.541 | 5.294 | −5.247 (a v26 passa da fila sem a reserva da GIN1) |
| Doppler de membros | 9.834 | 6.112 | −3.722 (por último com o médico por hora) |
| angio de coronárias | 1.408 | 0 | −1.408 |
| TC de tórax sem contraste, emergência | 728 | 0 | −728 |
| TC de tórax com contraste | 3.104 | 2.510 | −594 |
| US de mamas | 14.689 | 14.134 | −555 |
| US de aparelho urinário | 4.999 | 4.723 | −276 |
| **o que entra** | | | |
| angiotomografias (sem coronárias) | 0 | 2.347 | +2.347 |
| US de abdômen total | 11.202 | 13.088 | +1.886 |
| US de tireoide | 3.216 | 5.099 | +1.883 |
| Doppler de carótidas | 4.674 | 5.756 | +1.082 |
| crianças (abdômen, urinário, escrotal, tireoide) | 0 | 1.022 | +1.022 |
| US de bolsa escrotal | 0 | 994 | +994 |
| TC de pescoço, crânio e face; TC sem contraste | 0 | 1.338 | +1.338 |
| **total** | **81.494** | **79.714** | **−1.780** |

O valor fica quase igual (diferença de R$ 39), e a margem sobe R$ 109 mil. O cenário 2 tem menos exames porque troca
ultrassom barato (transvaginal, Doppler de membros) por TC, que custa três vezes mais.

## 5. Os três lado a lado (médico pago por hora; entre parênteses, por exame)

| | cenário 1: v26 e a sobra | cenário 2: escolher de novo | carteira 1 (em vigor) |
|---|---:|---:|---:|
| exames | 81.494 (81.236) | 79.714 (80.875) | 79.533 |
| margem | R$ 3,40 mi, 32% (R$ 3,53 mi) | R$ 3,50 mi, 33% (R$ 3,59 mi) | R$ 3,18 mi, 30% (R$ 3,41 mi) |
| uso das salas de ultrassom | 85% (85%) | 78% (88%) | 85% |
| uso dos 3 tomógrafos | 77% (77%) | 79% (70%) | 79% |
| exames sem fila ou já descartados | R$ 1,14 mi | nenhum | pélvica |

**Limites:**
- Os custos do ultrassom são premissas de 20/10 e 02/11. Os da planilha de 05/11 ainda estão em branco: com eles, a
  margem muda, mas a ordem dos exames muda pouco.
- O valor dos exames é o da v26. Com o quadro P2 de 12 meses, ele cai para R$ 10.614.642, cerca de R$ 22 mil a
  menos: sai um pouco do último bloco.
- A tomografia usa 20 min com contraste. Com a punção antes, o uso dos tomógrafos cai (estudo de 09/11).
- Nas crianças, o tempo é o do adulto. Se a equipe assistencial disser que leva mais, a margem delas cai um pouco.
