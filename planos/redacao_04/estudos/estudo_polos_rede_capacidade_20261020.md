# Estudo — o quadro, os 6 polos, a rede e a capacidade (plano 4)

20/10/2026. Uso interno do usuário. A base é a v9 final da equipe, que é a nossa v23, byte a byte. **Nada disto
foi aplicado ao plano ainda.** As contas estão em `calculo_v24/` e se refazem com os scripts (seção 10).

---

## 0. Em uma página

- **Decidido:** o quadro de gestão do cenário 3, com o preço proposto. São R$ 954.560,00 em 8 meses, 8,23% do
  valor global, e 79.152 exames (65.530 de ultrassom e 13.622 de tomografia). Ver D-005 em `pendencias.md`.
- **Arranjo dos documentos de 20/10:** 6 polos, um por Região, com a Central e a Centro-Sul num polo só. Uma
  unidade de ultrassom por polo. Tomografia em 6 polos ou em 5, com a Leste sem tomógrafo.
- **Para fechar com folga:**
  - Samambaia com 6 salas de ultrassom e Gama com 5, no tempo de planejamento;
  - o tempo real por exame de cada clínica;
  - um mínimo de tomografia por clínica perto do volume que ela recebe, e não 400 por mês;
  - começar a produzir no 1º mês.
- **Próximo:** os dois planos. Um com 6 polos de tomografia; outro com 5, sem destacar no texto qual polo fica
  sem. Para onde vai a demanda está na seção 6.

## 1. A base e o que vale

- A "v9 final" da equipe é a `versoes/plano_v23_20261008.docx`. A "quinta versão" que estava em Downloads é a v19.
- Vale o que foi combinado em 20/10/2026: 8 meses, os exames do cenário 3 e 6 polos.
- O plano de execução do ISHP e a apresentação da rede chegaram em 20/10, mas são de antes. Eles falam em 10 meses,
  9 polos de ultrassom e 4 de tomografia, com a tomografia em 6 meses. Servem só pela rede de clínicas (seção 4).

## 2. O quadro de gestão (decidido)

| rubrica | qtd | R$ por mês | de onde vem o preço |
|---|---:|---:|---|
| Direção Executiva de Projeto | 1 | 14.500 | pt_ses_01 (ISHP), item 1.1.1 |
| Coordenação Assistencial | 1 | 10.500 | pt_ses_01, item 1.1.3 |
| Coordenação Administrativa e Financeira | 1 | 8.400 | mercado DF (gerente adm. e fin., CBO 1421-05), dentro da faixa 6.000 a 10.500 dos aprovados |
| Coordenação Operacional | 1 | 8.400 | o mesmo |
| Supervisão de Polo Assistencial (1 para 2 polos) | 3 | 6.155 | pt_ses_01, item 1.1.11 (2 para 4 polos) |
| Operador de registro de sistemas | 8 | 4.300 | pt_ses_02, 03 e 04 (IEV), item 1.3.3 |
| Assistente Administrativo | 6 | 3.200 | IEV; é também o mercado da função de contato e confirmação (R$ 3.156) |
| Assessoria de Prestação de Contas | 1 | 5.455 | pt_ses_01, item 3.1.1 |

A regra de preço, os três cenários e a pesquisa de mercado estão em
`dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx` e em `calculo_v24/README.md`.

## 3. Os 6 polos: por que juntar a Central e a Centro-Sul

São 7 Regiões de Saúde para 6 polos, então duas se juntam. O critério do usuário foi **demanda e proximidade**,
depois **transporte público** e **as clínicas que a rede já tem**.

### 3.1 Demanda por Região (cenário 3)

| Região | exames | % | ultrassom | tomografia |
|---|---:|---:|---:|---:|
| Sudoeste | 26.821 | 33,9% | 21.947 | 4.874 |
| Sul | 16.298 | 20,6% | 14.444 | 1.854 |
| Leste | 12.301 | 15,5% | 10.941 | 1.360 |
| Centro-Sul | 7.730 | 9,8% | 6.795 | 935 |
| Norte | 6.700 | 8,5% | 4.676 | 2.024 |
| Central | 4.706 | 5,9% | 3.187 | 1.519 |
| Oeste | 4.596 | 5,8% | 3.540 | 1.056 |

A fila é a de 15/09/2026, com as participações por Região do próprio plano. A Oeste aparece com pouca demanda para
444 mil habitantes. É o dado que o plano usa desde o início.

### 3.2 Qual dupla junta

Para cada dupla, o polo fica na RA que minimiza exames × km, em linha reta. A conta mede quanto a junção aumenta a
distância e o tamanho do polo novo.

| dupla | polo novo | km a mais por exame | RA mais longe |
|---|---:|---:|---:|
| Sudoeste + Centro-Sul | 43,7% | 0,8 | 9,4 km |
| Oeste + Sudoeste | 39,7% | 0,8 | 23,3 km |
| Leste + Central | 21,5% | 2,9 | 18,9 km |
| **Central + Centro-Sul** | **15,7%** | **3,2** | **16,7 km** |
| Norte + Leste (como na v9) | 24,0% | 4,4 | 21,8 km |

**As duplas com a Sudoeste saem:** ela já é a maior, e juntar uma vizinha cria um polo com 40% a 44% de tudo.

Com as sedes nas cidades que têm clínica, a distância média por exame fica assim:

| arranjo | km médio | RA mais longe |
|---|---:|---|
| 7 polos (referência) | 4,7 | Brazlândia, 18,7 km de Ceilândia |
| Central + Centro-Sul, sede na Asa Sul | 5,6 | Riacho Fundo II, 21,5 km |
| Central + Centro-Sul, sede no Guará | 5,2 | Brazlândia, 18,7 km |
| Leste + Central | 5,6 | Varjão, 23,7 km de São Sebastião |
| Norte + Leste | 6,6 | Fercal, 34,9 km de São Sebastião |

### 3.3 Transporte público

- **Metrô:** sai da Rodoviária do Plano Piloto, desce pela Asa Sul, passa por Guará, Park Way, Águas Claras,
  Arniqueira e Taguatinga, e se divide em Ceilândia e Samambaia.
- **BRT Sul:** liga Gama e Santa Maria à Rodoviária e ao terminal da Asa Sul.
- **Norte e Leste:** não têm metrô, e os ônibus de lá vão sobretudo ao Plano Piloto. Entre as duas há a linha 511.4
  (Sobradinho–Paranoá). Não há linha direta de Sobradinho a São Sebastião.

Por isso Norte + Leste é o pior arranjo pelo transporte. A Centro-Sul chega ao Plano Piloto de metrô (Guará, Park
Way) ou pelos ônibus da EPIA.

### 3.4 A rede decide

A Centro-Sul é a única Região sem nenhuma clínica, e a Central tem três unidades para a menor demanda do DF.
**Central + Centro-Sul é o único arranjo em que os seis polos têm clínica.** Os outros deixam a Centro-Sul como polo
sem unidade.

## 4. A rede de clínicas

Fonte: as planilhas de CNPJ e CNES do ISHP (Downloads, 20/10/2026).

| Região | ultrassom | tomografia |
|---|---|---|
| Oeste | Ceilândia — Clínica Brasília (CNES 3022870), aguardando aceite | a mesma, R$ 175, aguardando aceite |
| Sudoeste | Samambaia — Med Saúde (CNES 9928200), **fechado** | Taguatinga — Clínica Padrão (CNES 9230149), R$ 165, alinhado |
| Norte | Sobradinho — Clínica Padrão (CNES 9230122), aguardando aceite | a mesma, R$ 165, alinhado |
| Leste | São Sebastião — GPAES/HPAES Hospital Dia (CNES 7379943), aguardando confirmação | — |
| Central | Asa Sul — DaVida (CNES 8177090, SGAS 915); Asa Norte — Dr. Everaldo Maia (CNES 6594948, SCRN 708/709); bairro Sudoeste — Ana Maia (CNES 9010297, CLSW 105) | — |
| Sul | Gama — CIG (CNES 9180168), **proposta aceita**; Santa Maria — Clinisan (CNES 7253451, CL 212) | Gama — CIG, R$ 175, alinhado |
| Centro-Sul | — | — |

**Correção:** a unidade "Sudoeste" do grupo Everaldo Maia fica no bairro Sudoeste, na **Região Central**, conforme a
ficha do CNES. O plano de execução do ISHP a contava na Região Sudoeste e dividia com Samambaia os 21.997
ultrassons de lá. Essa divisão está errada.

**Com 6 unidades de ultrassom:**
- saem a Asa Norte e Santa Maria, que fica de reserva;
- no polo da Central e Centro-Sul fica a DaVida (Asa Sul) ou a Ana Maia (bairro Sudoeste). As duas ficam do lado
  da Centro-Sul, que tem 62% da demanda desse polo. A Asa Norte fica do outro lado do Plano Piloto.

## 5. Ultrassom: o que cada unidade precisa ter, com margem

A regra é a do plano: sala ocupada no máximo 80% de um dia de 10 horas, com o tempo de planejamento por exame
(20 minutos; doppler 30). As faltas (25%, hipótese) não mudam as salas, só as vagas a abrir.

| unidade | exames em 8 meses | por dia útil | vagas a abrir por dia | salas | salas, se o 1º mês se perder | salas a 12 min por exame (ritmo do ISHP) |
|---|---:|---:|---:|---:|---:|---:|
| Samambaia (Sudoeste) | 21.947 | 131 | 175 | **6** | 7 | 4 |
| Gama (Sul) | 14.444 | 86 | 115 | **5** | 5 | 3 |
| São Sebastião (Leste) | 10.941 | 65 | 87 | 3 | 4 | 2 |
| Asa Sul ou bairro Sudoeste (Central e Centro-Sul) | 9.982 | 59 | 79 | 3 | 4 | 2 |
| Sobradinho (Norte) | 4.676 | 28 | 38 | 2 | 2 | 1 |
| Ceilândia (Oeste) | 3.540 | 21 | 28 | 1 | 2 | 1 |
| **total** | **65.530** | **390** | **522** | **20** | **24** | **13** |

**Leitura:**
- Samambaia e Gama viram as duas unidades grandes. Com as 2 salas do modelo do ISHP, Samambaia não comporta a
  Sudoeste nem a 12 minutos por exame.
- A Clínica Brasília ofereceu em 08/10 um andar com 5 salas em Ceilândia, ao lado da Sudoeste. Pronto e licenciado
  antes da formalização, ele recebe a parte que Samambaia não comportar.

## 6. Tomografia: 6 ou 5 polos (a Leste sem)

### 6.1 Para onde vai a demanda (controle interno)

Sozinha, Taguatinga passaria de um tomógrafo (1,19 de carga). Nos dois cenários, **Samambaia e o Recanto das Emas
vão a Ceilândia**, que estava ociosa: Samambaia fica a 6,7 km de Ceilândia e a 5,8 km de Taguatinga.

No cenário de 5:
- a **Leste vai à Asa Sul**, com ônibus direto ao Plano Piloto: Paranoá a 11,3 km, Jardim Botânico a 11,9 km e
  São Sebastião a 16,5 km;
- o **Itapoã vai a Sobradinho**: 10,8 km, contra 13,3 km da Asa Sul.

A lista RA a RA está na aba "Para onde vai cada RA" da planilha da equipe.

| tomógrafo | 6 polos: por mês | carga | 5 polos: por mês | carga |
|---|---:|---:|---:|---:|
| Ceilândia (Oeste, Samambaia, Recanto das Emas) | 388 | 0,76 | 388 | 0,76 |
| Taguatinga (resto da Sudoeste) | 353 | 0,69 | 353 | 0,69 |
| Central e Centro-Sul (clínica a definir) | 307 | 0,60 | **440** | **0,86** |
| Sobradinho (Norte; no de 5, também o Itapoã) | 253 | 0,50 | 289 | 0,57 |
| Gama (Sul) | 232 | 0,45 | 232 | 0,45 |
| Leste (clínica a definir) | 170 | 0,33 | — | — |
| **total** | **1.703** | **3,32** | **1.703** | **3,33** |

A carga é contada em tomógrafos a 80% de um dia de 10 horas, com o tempo de planejamento (20 minutos com contraste
e 15 sem).

### 6.2 A comparação

| | 6 polos | 5 polos (Leste sem) |
|---|---:|---:|
| distância média até o tomógrafo | 5,7 km | 6,2 km |
| clínicas de tomografia a achar | 2 (Leste e Central/Centro-Sul) | 1 (Central/Centro-Sul) |
| clínica mais carregada | 0,76 | 0,86 |
| volume por clínica (por mês) | 170 a 388 | 232 a 440 |
| mínimos de 400 somados, contra 1.703 de demanda | 2.400 | 2.000 |

**Leitura:**
- **O plano com 6 polos** dá o melhor acesso, mas espalha o volume: três clínicas ficam abaixo de 260 por mês.
  É preciso achar duas clínicas.
- **O plano com 5** custa meio quilômetro a mais na média, dá volumes maiores e exige achar uma clínica só.
- **Nos dois, a Central e Centro-Sul precisa de tomógrafo, e não há nenhum mapeado.** É a primeira coisa a achar.
- **O mínimo de 400 por mês por clínica não fecha.** No cenário de 6, nenhuma clínica chega a 400; no de 5, só a
  Asa Sul. O mínimo que cabe em todas é 170 por mês (6 polos) ou 232 (5 polos). Outra saída é um mínimo pela rede
  inteira.
- Se a tomografia for feita em 6 meses, e não em 8, os volumes por mês sobem um terço.

### 6.3 O que o plano pode dizer no cenário de 5

Dá para não destacar o polo sem tomografia sem escrever nada falso:
- tratar a tomografia como rede do projeto, com a capacidade requerida em tomógrafos no total (a conta pede pelo
  menos 4);
- dividir a Meta 5 por procedimento e por período, não por polo;
- mostrar as linhas de tomografia das tabelas 4.15 e 7.3 só no total;
- a 4.16 (b) já diz "nos polos com tomografia".

**Não pode escrever** que todo polo ou toda Região tem tomografia. A 7.3 da v23 diz "≥ 1 por Região", e isso sai.
Na formalização, a SES recebe o CNES e o equipamento de cada polo (4.16, f).

## 7. O que precisa estar confirmado para fechar com tranquilidade

1. **Salas de ultrassom** em cada unidade, pelo menos as da seção 5 (o ideal é a coluna do 1º mês perdido), com 10
   horas por dia. Samambaia e Gama primeiro.
2. **Tempo real por exame** em cada clínica, que substitui a premissa e pode reduzir as salas.
3. **Agenda com uns 25% a mais de vagas** do que os exames, para cobrir as faltas.
4. **Início no 1º mês.** O plano produz desde o mês 1; um mês de mobilização sobe a carga em uns 14%.
5. **Uma clínica de tomografia na Central e Centro-Sul**, nos dois cenários, e outra na Leste no cenário de 6.
6. **Mínimos de tomografia** somados abaixo da demanda mensal, perto do volume de cada clínica.
7. **Contraste incluído no preço** da tomografia (95% dos exames).

## 8. Perguntas para a pessoa responsável

Estão na aba "Perguntas" da planilha da equipe, por clínica, com coluna para a resposta:
- salas e horário de Samambaia, Gama, São Sebastião e Asa Sul ou bairro Sudoeste;
- DaVida ou Ana Maia;
- tomógrafo na Central e Centro-Sul e na Leste;
- capacidade e mínimo de cada tomógrafo;
- o andar de 5 salas em Ceilândia;
- tempo por exame;
- contraste no preço;
- início no 1º mês.

## 9. Pontos de atenção

- **O formato dos contratos e a 4.14.** A tomografia está negociada por exame (R$ 165 a R$ 175, contraste incluído),
  e o ultrassom por aluguel com plantão médico. Comprar o exame da clínica não bate com a 4.14 ("a execução
  assistencial não é subcontratada", "por equipe própria") nem com o art. 33 do Decreto 48.727/2026. O ponto ficou
  em aberto na reunião de 07/10 (seção 0) e na negociação de 08/10. A palavra é do jurídico do ISHP, antes do
  protocolo.
- **O plano de execução do ISHP** fala em 10 meses, com o 1º de mobilização e a tomografia em 6 meses. O plano tem 8
  meses, com produção desde o 1º.
- **Os preços do quadro vêm de planos sob representação.** O pt_ses_01 e os três do IEV estão sob representação do
  MPCDF no TCDF (CT-001 a CT-005). O que defende cada rubrica é a atribuição escrita.
- **A Coordenação Assistencial** precisa dizer que coordena e que o responsável técnico de cada polo executa, pago
  pelo valor do exame (LI-018).
- **O pré-plano (redacao_06)** ainda usa o apoio da v23 (R$ 919.640,00). Falta decidir se acompanha.

## 10. Arquivos e como refazer

- `calculo_v24/cenarios_quadro.py` → `cenarios_quadro.json`: os seis cenários do quadro.
- `calculo_v24/planilha_cenarios_quadro.py` → `dados/quadro_gestao_cenarios_e_precificacao_20261020.xlsx`.
- `calculo_v24/polos_capacidade.py` → `polos_capacidade.json`. Inclui:
  - o rateio nas 7 Regiões com os exames do cenário 3;
  - as duplas de Regiões;
  - os 6 polos;
  - a tomografia em 6 e em 5 polos, RA a RA.

  A população e a posição das RAs vêm de `dados/polos_de_imagem_no_df_v20.html`.
- `calculo_v24/planilha_equipe_polos.py` → `dados/rede_imagem_6_polos_20261020.xlsx`: a planilha da equipe. Não
  cita versão, seção nem custo de gestão.

Fontes da web (acesso em 20/10/2026):
- [salario.com.br](https://www.salario.com.br/), páginas de Brasília/DF por CBO (lista na planilha do quadro);
- [ficha CNES da Ana Maia](https://cnes2.datasus.gov.br/Mod_Conjunto.asp?VCo_Unidade=5300109010297), e as da DaVida,
  da Everaldo Maia (Asa Norte) e da Clinisan;
- metrô: [QuintoAndar](https://www.quintoandar.com.br/guias/?p=2461265) e [Sou Brasília](https://soubrasilia.com/metro-df-horario-linhas-tarifa/);
- BRT Sul: [Jornal de Brasília](https://jornaldebrasilia.com.br/brasilia/expresso-df-reduzira-tempo-de-viagem-do-gama-e-de-santa-maria-a-brasilia/);
- linha 511.4: [Jornal de Brasília](https://jornaldebrasilia.com.br/brasilia/regioes-ganham-mais-cinco-linhas-de-onibus/).
