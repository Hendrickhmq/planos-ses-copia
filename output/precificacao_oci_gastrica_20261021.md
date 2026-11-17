# Estudo — o que é preciso para precificar a OCI de câncer gástrico e até quanto pagar às clínicas

21/10/2026. **Uso interno do ISHP: não vai ao plano nem às clínicas.** A base é o plano assinado
pelo ISHP em 01/10/2026 (`../dados/ishp_plano_assinado_20261001.pdf`, processo SEI
00060-00367596/2026-59). As contas estão em `teto_oci_20261021.xlsx` (premissas em amarelo) e se
refazem com `calculo/planilha_teto_oci.py`. Os preços, linha a linha, estão em `../dados/precos.md`.

---

## 0. Em uma página

- **Todo o R$ 600,11 é para executar.** O convênio paga R$ 600,11 por OCI concluída, 13.012 OCIs,
  R$ 7.808.631,32. A gestão, a recepção e a prestação de contas são pagas à parte, nas Metas 01 e
  03 (R$ 596.696,76). Nada do valor da OCI precisa sustentar a estrutura do ISHP.
- **O estudo de 20/10 olhou três peças: o exame, o retorno e a biópsia. A OCI tem mais.** Ficavam
  de fora:
  - a consulta inicial;
  - a sedação, que muita clínica cobra à parte, com o anestesiologista;
  - a pinça e o frasco da biópsia, que não são o laboratório;
  - as OCIs que não concluem, que pagam consulta e exame e não recebem.

  No exemplo da planilha, isso soma **R$ 107 por OCI**.
- **O teto técnico é R$ 560,60 por OCI concluída** (93% do valor), com 5% de reserva e R$ 10 de
  custos que ficam com o ISHP. Se a clínica receber na EDA, e não na OCI concluída, cai para
  R$ 532,57.
- **Pelo exame com sedação, cabe até uns R$ 358.** A conta supõe a consulta a R$ 80, o
  anatomopatológico a R$ 60 em 70% das EDAs e o retorno médio a R$ 55. Com biópsia em todas e
  laboratório caro, cai para R$ 270. Para comparar, o SUS paga **R$ 335,00** pelo exame (Tabela
  Regionalizada da SES-DF) e **R$ 350,12** (programa federal).
- **A régua da negociação é o que o SUS já paga por peça.** O Ministério paga ao habilitado no
  Agora Tem Especialistas R$ 350,12 pela EDA e R$ 149,99 pela sedação. Somam R$ 500,11; com
  R$ 100,00 a mais dão os R$ 600,11 da OCI, exatos. Uma clínica habilitada receberia esta mesma
  OCI direto do Ministério, por esse valor.
- **Os 50% do plano 4 não servem aqui.** Seriam R$ 300 pela OCI inteira, menos do que o SUS paga
  só pelo exame. A faixa realista do pacote vai de uns R$ 480 (80%) ao teto de R$ 560.
- **Fazer com equipe própria, como o plano descreve, não cabe com as hipóteses de hoje.** A conta
  dá uns **R$ 671 por OCI**, com estrutura alugada, equipe contratada e anestesiologista por hora em
  cada sala. O que pesa é o médico pago pelas 10 horas do posto. Funciona se a equipe vier da
  clínica, paga por produção.
- **A oferta inicial e o teto são decisão de vocês.** Quando decididos, entram no cabeçalho de
  `../dados/precos.md`.

## 1. O que o plano assinado obriga: a lista para a clínica

É o que a clínica de cada polo precisa ter ou aceitar. Cada linha diz onde está no plano.

| tema | o que o plano diz | seção |
|---|---|---|
| **local** | um polo em Taguatinga e outro no CONIC (Asa Sul); não há execução fora dos dois | 8, 9.1 |
| **forma** | estrutura por locação, cessão ou outro instrumento, formalizado depois do Termo, com **exclusividade das 07h às 17h, de segunda a sexta**, e cláusula de continuidade | 9.1, 9.2 |
| **CNES** | serviço 142-001 (endoscopia); 120-001 (anatomia patológica) no polo ou no laboratório | 2, 9.3 |
| **sanitário** | serviço de endoscopia **tipo III** da RDC 6/2013 (sedação ou anestesia por anestesiologista); alvará e licença da VISA-DF com essa tipificação; plantas pela RDC 50/2002 | 12 |
| **salas** | 2 salas de endoscopia por polo, 25 minutos por exame com a troca, 48 EDAs por dia; o pico previsto é 40,3 | 10.2, 11 |
| **consultórios** | 3 por polo: 2 presenciais e 1 para retorno ou teleconsulta | 11 |
| **SRPA** | 6 leitos ou poltronas por polo, monitor e oxigênio em cada um, 45 minutos de permanência | 11, 14.2 |
| **equipamento** | 6 videoendoscópios e 3 torres por polo (5 em uso, 1 reserva); 2 lavadoras automáticas (DAN); carrinho de emergência, desfibrilador, monitores, bombas | 11, Anexo I.5 |
| **reprocessamento** | área suja e limpa separadas, POP, registro de cada ciclo, teste de estanqueidade (RDC 15/2012) | 12, Anexo I.4 |
| **equipe por polo** | 5 gastroenterologistas, 3 endoscopistas, 3 anestesiologistas (**um por sala**), 3 enfermeiros, 6 técnicos de enfermagem, 3 técnicos de reprocessamento; RT médico e RT de enfermagem | 10.2, 10.4 |
| **biópsia** | indicada em lesão suspeita ou pelo protocolo de Sydney modificado; frasco com formol, etiqueta, envio em até 24 h; nova coleta sem ônus se a amostra vier ruim | 13 |
| **laudo** | laboratório com 120-001, contratado pelo ISHP no mês 1; **laudo em até 15 dias**; ≥ 95% no prazo | 13.3, 13.4, 15 |
| **retorno** | consulta ou teleconsulta (CFM 2.314/2022), com consentimento; **≥ 95% das OCIs com EDA** | 7.1, 15 |
| **segurança** | Plano de Segurança do Paciente por polo; time-out; fluxo de urgência com o SAMU | 14 |
| **calendário** | mês 1 (nov/2026) sem produção; produção de dez/2026 a jul/2027 | 16 |

**Dois pontos para a conversa:**
- **A recepção não entra no preço da clínica.** O plano paga os 6 assistentes administrativos na
  Meta 01, e diz que eles não compõem o valor unitário (10.3). A clínica que cobrar recepção e
  agendamento cobra duas vezes.
- **A exclusividade é o custo grande da clínica.** São 2 salas, 3 consultórios e a SRPA reservados
  10 horas por dia. É também o argumento: a clínica recebe 6.506 OCIs em 8 meses, uns 40 pacientes
  por dia útil.

## 2. A OCI por dentro

### 2.1 As peças que o SUS registra

| peça | código | por OCI | quem faz | SUS avulso | SUS com incremento | varejo no DF |
|---|---|---|---|---|---|---|
| consulta inicial | 03.01.01.007-2 | 1 | gastroenterologista | R$ 10,00 | — | R$ 100 a R$ 1.000; mediana R$ 400 (35 preços) |
| EDA | 02.09.01.003-7 | 1, obrigatória | endoscopista | R$ 48,16 | R$ 350,12 | R$ 500 e R$ 1.100 (só 2 publicados) |
| sedação | 04.17.01.006-0 | 1 | anestesiologista | R$ 15,15 | R$ 149,99 | não publicada à parte |
| anatomopatológico | 02.03.02.003-0 | **1** (mesmo com 2 frascos) | patologista do laboratório | R$ 40,78 | — | sem preço no DF; R$ 91 a R$ 130 por amostra em SP |
| retorno | 03.01.01.007-2 ou 03.01.01.030-7 | 1 (até 2 de cada) | gastroenterologista | R$ 10,00 | — | não publicado |

Fonte: Tabela de 10/2026, arquivo oficial do DATASUS (`../dados/fontes/sigtap_ftp_202610.md`);
incrementos da Portaria SAES/MS 4.282/2026; varejo do Doctoralia e do dr.consulta em 21/10/2026.

**A Tabela Regionalizada da SES-DF** paga R$ 335,00 pela EDA. É a tabela da contratação
complementar de terapia intensiva (Deliberação CG-SES 24/2024, republicada pela 16/2025), mas é o
número que a SES-DF já aceita para o exame.

### 2.2 O que vem embutido (o plano põe tudo no unitário, seção 19.3)

- honorários das consultas, do endoscopista e do anestesiologista;
- enfermagem, técnicos e reprocessamento;
- RT médico e de enfermagem;
- sedativos, medicamentos de emergência, pinça, formol, frascos;
- saneantes e testes da DAN;
- equipamento e manutenção;
- aluguel, energia, climatização e limpeza dos polos;
- prontuário e TI;
- seguro de responsabilidade civil e treinamentos (ACLS, segurança do paciente).

**O plano declara que nada disso se cobra à parte.** O preço da clínica tem de cobrir o que ela
traz, e o ISHP fica com o que ela não traz (premissa "custos que ficam com o ISHP", R$ 10 por OCI
na planilha).

### 2.3 Por que as três peças do estudo de 20/10 não bastavam

Na aba B, com os preços de exemplo:

| | R$ por OCI concluída |
|---|---|
| exame com sedação | 400,00 |
| retorno médio (metade presencial, metade teleconsulta) | 55,00 |
| biópsia (70% × R$ 60) | 42,00 |
| **as três peças** | **497,00** |
| **o custo completo** | **604,47** |
| **o que ficava de fora** | **107,47** |

O que fica de fora:
- **a consulta inicial**, R$ 80;
- **as OCIs que não concluem.** Com 95% de conclusão, cada 100 OCIs pagas exigem 105 consultas e
  105 exames, e as 5 que sobram não recebem. São uns R$ 27 por OCI.

A sedação e a pinça à parte estão em zero no exemplo. Se a clínica as cobrar fora do exame, entram
por cima.

## 3. O dinheiro

| | valor | fonte |
|---|---|---|
| por OCI concluída | R$ 600,11 | plano, 19.2, item 2.1.1 |
| total da Meta 02 | R$ 7.808.631,32 | 13.012 × R$ 600,11 |
| por polo, se a divisão for meio a meio | R$ 3.904.315,66 (6.506 OCIs) | a divisão real segue a regulação (9.1) |
| mês de pico (1.774 OCIs) | R$ 1.064.595,14 | plano, 16.3 |
| gestão e prestação de contas, à parte | R$ 596.696,76 | Metas 01 e 03 |
| parcelas trimestrais | R$ 1.959.021,55 · R$ 3.150.239,90 · R$ 3.296.066,63 | plano, 20 |

**Quatro regras que viram risco de dinheiro:**
1. **Só conta a OCI concluída** (7.2): consulta, EDA, biópsia quando indicada, laudo, retorno e
   desfecho registrado. A OCI sem retorno não conta para a meta, e o percentual mínimo e a glosa
   vêm do instrumento (15).
2. **A APAC vale duas competências** (atributo 054, `../dados/parametros_tecnicos.md`, item 7).
   O exame no fim do mês deixa pouco tempo para o laudo e o retorno. Laudo atrasado derruba a OCI.
3. **Nova coleta sem ônus** (13.5): se a amostra vier ruim, repete-se o exame sem receber de novo.
4. **Só 15 CIDs abrem a OCI** (C16, D00, D13, D37, K20 a K23, K25 a K31; Tabela do SUS,
   `../dados/fontes/sigtap_ftp_202610.md`). Quem chega com anemia, perda de peso, disfagia ou
   sangramento como CID principal não fecha a APAC.

É por isso que o jeito de pagar a clínica importa tanto quanto o preço (seção 4).

## 4. Três formas de contratar, e o teto de cada uma

As premissas são as da aba Premissas:

| premissa | valor | de onde vem |
|---|---|---|
| EDAs com biópsia | 70% | hipótese |
| anatomopatológico por paciente | R$ 60 | hipótese |
| retorno por teleconsulta | 50% | hipótese |
| OCIs que concluem | 95% | o indicador do plano |
| reserva do ISHP | 5% | decisão de vocês |
| custos que ficam com o ISHP | R$ 10 por OCI | hipótese |

### A. Pacote: a clínica entrega a OCI inteira

| | por OCI |
|---|---|
| teto, pagando por OCI concluída | **R$ 560,60** |
| teto, pagando por OCI iniciada (na EDA) | R$ 532,57 |

| oferta | preço | fica com o ISHP por OCI | no total |
|---|---|---|---|
| 70% | R$ 420,08 | R$ 180,03 | R$ 2.342.589 |
| 80% | R$ 480,09 | R$ 120,02 | R$ 1.561.726 |
| 85% | R$ 510,09 | R$ 90,02 | R$ 1.171.295 |
| 90% | R$ 540,10 | R$ 60,01 | R$ 780.863 |
| 95% | R$ 570,10 | R$ 30,01 | passa do teto |

"Fica com o ISHP" é antes da reserva e dos custos do ISHP dentro da OCI. **Pagar por OCI
concluída passa à clínica o risco do retorno e do laudo**, e é o que mais protege. Pagar na EDA
deixa o risco com o ISHP.

### B. Por componente: cada peça com seu preço

Serve quando a clínica cota peça por peça, que é o mais comum.

**A pergunta que a aba responde:** dados os preços da consulta, do anatomopatológico e do retorno,
até quanto se paga pelo exame com sedação?

Com os preços de exemplo, até **R$ 358,32**. A tabela mostra como isso cai com a biópsia:

| biópsia nas EDAs | AP a R$ 40,78 (SIGTAP) | AP a R$ 60 | AP a R$ 91 | AP a R$ 130 |
|---|---|---|---|---|
| 40% | R$ 384,01 | R$ 376,32 | R$ 363,92 | R$ 348,32 |
| 70% | R$ 371,78 | R$ 358,32 | R$ 336,62 | R$ 309,32 |
| 100% (Sydney em todas) | R$ 359,54 | R$ 340,32 | R$ 309,32 | R$ 270,32 |

**O que a tabela ensina:**
- **o preço do anatomopatológico pesa mais do que a taxa de biópsia.** Fechar o laboratório **por
  paciente**, perto do SIGTAP, protege o teto do exame;
- **cada R$ 10 a mais na consulta inicial tira R$ 10 do exame.** Cada R$ 10 a mais no retorno
  médio tira R$ 9,50.

### C. Estrutura alugada e equipe própria: o desenho literal do plano

O ISHP aluga a estrutura e contrata a equipe da seção 10.2. Os médicos são pagos por hora de
posto (custo para a empresa do CAGED pelo salario.com.br, convertido em hora). A enfermagem é CLT
pelos 9 meses. Os insumos, o laboratório e o equipamento são hipóteses.

| bloco | por OCI concluída |
|---|---|
| médicos (gastro, endoscopista, anestesiologista) | R$ 324,24 |
| enfermagem e reprocessamento | R$ 98,87 |
| insumos, pinça e anatomopatológico | R$ 155,79 |
| equipamento (4 conjuntos de vídeo e 4 DAN) | R$ 49,80 |
| estrutura (2 polos) | R$ 27,67 |
| outros | R$ 15,00 |
| **total** | **R$ 671,37** |

São **R$ 110,76 acima do teto.** Com o resto como está, nem com aluguel zero caberia.

**Por que fica caro:**
- **o anestesiologista fica na sala as 10 horas.** São R$ 105 por OCI só dele;
- **o gastroenterologista tem 3 postos** para consultas que ocupam 78% deles (plano, 10.2).

O médico pago por produção, ou a equipe da própria clínica, tira esse custo ocioso. **Esta aba é
ordem de grandeza**: o equipamento, a pinça e os insumos não têm preço publicado e precisam de
cotação.

### O formato do contrato

O preço se negocia por OCI ou por peça. **O contrato se escreve como o plano descreve:**
- locação ou cessão da estrutura de cada polo, com exclusividade e continuidade (9.2);
- os profissionais contratados pelo ISHP, no regime que ele definir (10.2);
- o laboratório de anatomia patológica contratado pelo ISHP (13.3).

O plano diz que o ISHP não transfere a responsabilidade à locadora nem a terceiros (seção 1, último
parágrafo; seção 8).

Se a clínica traz a equipe, o arranjo que casa com o plano tem duas partes:
- a clínica é a locadora da estrutura;
- os médicos dela são contratados pelo ISHP como pessoa jurídica, por produção.

O jurídico e o financeiro do ISHP precisam ver como isso aparece na prestação de contas da Meta 02.

## 5. A biópsia

- **Quantas EDAs terão biópsia.** O plano biopsia lesão suspeita, úlcera, metaplasia ou displasia,
  ou segue o protocolo de Sydney modificado (13.1). Com Sydney de rotina, chega perto de 100%.
  Pedir à clínica a taxa que ela tem em EDA diagnóstica. A planilha usa 70% e mostra de 40% a 100%.
- **Dois custos diferentes:**
  - a **coleta** (pinça, frasco, formol, etiqueta), na sala;
  - o **anatomopatológico** (processamento e laudo), no laboratório.

  Muita clínica põe a coleta no exame; o laboratório cobra à parte.
- **Por frasco ou por paciente.** O SUS paga um anatomopatológico por OCI, e o Sydney usa dois
  frascos (antro e corpo). O laboratório que cobra por frasco dobra o custo: **negociar por
  paciente.**
- **Prazo.** Laudo em até 15 dias, com prioridade para suspeita de neoplasia (13.4), e penalidade no
  contrato. É o laudo que segura o retorno dentro das duas competências.

## 6. O retorno

- **Presencial ou teleconsulta.** O plano admite os dois (7.1); a teleconsulta precisa de
  consentimento e da plataforma (CFM 2.314/2022). A planilha usa metade de cada.
- **Pagar o retorno só quando acontece.** É o retorno que conclui a OCI. Pagar a consulta inicial e
  o exame sem amarrar o retorno é o jeito de ter custo sem receita.
- **O mesmo gastroenterologista da consulta inicial** pode fazer o retorno. O plano conta 15
  minutos de retorno contra 20 da consulta inicial (10.2): o retorno pode valer menos.

## 7. O que perguntar a cada clínica

1. Quanto pela OCI inteira, concluída, com tudo da seção 2.2? E quanto por peça: consulta inicial,
   EDA com sedação, retorno presencial, teleconsulta?
2. A sedação é por anestesiologista e está no preço do exame, ou é cobrada à parte?
3. A pinça, o formol e o frasco estão no exame?
4. O anatomopatológico: laboratório próprio ou parceiro, com 120-001 no CNES? Preço por paciente ou
   por frasco? Prazo do laudo?
5. Qual a taxa de biópsia em EDA diagnóstica?
6. Tem CNES 142-001 e alvará da VISA-DF com endoscopia tipo III? Quantas salas, endoscópios,
   lavadoras e leitos de SRPA?
7. Aceita exclusividade das 07h às 17h, de segunda a sexta, por 9 meses?
8. Os médicos são da clínica? Aceitam contratação pelo ISHP como pessoa jurídica, por produção?
9. Aceita receber por OCI concluída (com o retorno feito)? Se não, aceita reter parte até o retorno?
10. Quem responde pela nova coleta quando a amostra vier ruim, e pela intercorrência?
11. A recepção e o agendamento ficam com a equipe do ISHP: o preço já sai sem eles?

## 8. O que falta para fechar o preço

- **As cotações das clínicas** de Taguatinga e do CONIC, pelas perguntas da seção 7. Com elas, a aba
  B da planilha dá o teto do exame na hora.
- **O preço de um laboratório do DF** com 120-001, por paciente.
- **A decisão da oferta inicial e do teto** (em % ou em reais), da reserva e do jeito de pagar
  (OCI concluída ou peça a peça).
- **O estudo que vocês fizeram em 20/10.** Não está no repositório nem nas conversas gravadas deste
  projeto. Se trouxer números de clínica, eles entram na aba B no lugar dos exemplos.
- **A ficha de 10/2026 pela tela do SIGTAP**, quando o site voltar (agente `ficha-sigtap`). Os
  valores já vieram do arquivo oficial da Tabela.
