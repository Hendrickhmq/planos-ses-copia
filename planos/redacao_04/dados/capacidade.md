# Capacidade requerida — memória interna

Aberto em 15/09/2026, depois de travada a vigência de 12 meses.

**Os intervalos de agendamento saíram do plano em 17/09/2026**, pela mesma regra da
carga por posto: são premissa sem fonte, e a verificação T os apanhou publicados no
documento. O plano declara as horas de sala e os equipamentos que elas exigem; a
conversão de exame em minuto fica aqui.

**Este arquivo calcula a capacidade que a meta exige, não o parque que o proponente
tem.** O usuário declarou em 15/09/2026 que o proponente já possui ultrassom e
tomógrafo e não conseguiu confirmar quantas salas nem em que turno — L-006. Inventário
não confirmado não se publica; capacidade requerida se calcula e se declara.

**Os tempos de sala abaixo são premissa sem fonte** e continuam precisando de
confirmação.

## As premissas de tempo

| exame | tempo de sala | fonte |
|---|---|---|
| ultrassom de região isolada | 20 min | **premissa, sem fonte** |
| ultrassom com doppler colorido | 30 min | **premissa, sem fonte** |
| tomografia com contraste | 20 min | **premissa, sem fonte** |
| tomografia sem contraste | 15 min | **premissa, sem fonte** |

O doppler pesa mais porque são 14.401 exames a 30 minutos: sozinho, consome 432.030
minutos de sala, 31% de toda a carga de ultrassom.

## A carga

**Revisto em 22/09/2026 (D-007):** sai a ecografia de partes moles, 2.974 exames a
20 minutos. A carga de tomografia não muda.

A execução do objeto requer **28.530 horas** de sala no período: **24.106 horas** de
ultrassonografia e **4.424 horas** de tomografia computadorizada.

| | exames | horas de sala |
|---|---|---|
| Ultrassom | 65.120 | 24.106 h |
| Tomografia | 13.452 | 4.424 h |
| **Total** | **78.572** | **28.530 h** |

## As salas que a vigência exige

Com 12 meses de produção — 252 dias úteis, 6.171 por mês, 294 por dia útil:

| turno | salas de ultrassom | tomógrafos |
|---|---|---|
| turno de 8 horas | 12 | 2 |
| turno de 10 horas | **10** | **2** |
| turno de 12 horas | 8 | 2 |

## O que isto diz sobre os três polos

Os polos são Ceilândia, Sobradinho e Gama, com a cobertura do plano 3.

**A ordem de grandeza é de dez salas de ultrassom e dois tomógrafos em turno de 10 horas.** E os dois números se comportam de modo oposto entre três endereços:

- **Ultrassom distribui.** Dez salas repartidas entre três polos é um arranjo natural,
  e o ultrassom é o exame que o usuário faz perto de casa.
- **Tomografia concentra.** Dois tomógrafos não se espalham por três endereços sem
  ociosidade — 4.424 horas de sala em doze meses são 15,7 horas por dia útil, que um
  aparelho absorve em dois turnos.

**A repartição entre os polos ainda não se calcula**, porque a fila de imagem não veio
aberta por Região de Saúde — L-005. É ela que governa quantas salas cada polo recebe.

## O risco que este arquivo abre

Se o parque real ficar abaixo de dez salas de ultrassom em turno de 10 horas, **a
meta não é executável no ritmo previsto**. É o maior risco de execução do plano e vai
à seção 8 com este número.

## O que falta

| falta | efeito |
|---|---|
| distribuição da fila por Região de Saúde | **L-005** · reparte as salas entre os polos |
| tempos de sala do proponente | substituem as quatro premissas acima |
| turno praticado | escolhe a linha das tabelas acima |
| parque instalado por polo | **L-006** · não se publica; entra como risco |

## Por polo — o que a 6.3 publica (v8, 22/09/2026)

Horas de cada polo = exames rateados procedimento a procedimento × tempo de sala,
arredondadas ao inteiro; o total da tabela é a soma dos polos. Salas =
teto(horas ÷ (252 dias × 10 h × 0,80)) — ocupação máxima de 80% sobre turno de 10 h,
regra que reproduz exatamente os 5 / 4 / 4 da v7.

| | Ceilândia | Sobradinho | Gama | total |
|---|---|---|---|---|
| exames | 31.183 | 23.527 | 23.862 | 78.572 |
| exames por dia útil (teto de ÷ 252) | 124 | 94 | 95 | 313 |
| horas de ultrassom | 9.176 | 7.066 | 7.864 | 24.106 |
| salas de ultrassom | 5 | 4 | 4 | 13 |
| horas de tomografia | 1.928 | 1.592 | 904 | 4.424 |
| tomógrafos | 1 | 1 | 1 | 3 |

O total de horas de US é a soma dos polos, 24.106; o agregado sem arredondar por polo
seria 24.106,83. A diferença é de arredondamento e não muda sala nenhuma.

## A 6.3 detalhada — v10, 24/09/2026

A devolutiva de 20/09 marcou a tabela da 6.3 em azul: **"precisa de mais
detalhamento"**. O usuário definiu o alcance em 24/09: *"só um plano geral de quantas
salas, quantos exames etc"*. Os parâmetros não mudaram, e salas e tomógrafos continuam
13 e 3.

**Exames por modalidade e polo.** A tomografia de cada polo é o rateio procedimento a
procedimento, arredondado pelos maiores restos até fechar 13.452; a ultrassonografia é
o total do polo menos a tomografia.

| | Ceilândia | Sobradinho | Gama | total |
|---|---|---|---|---|
| ultrassonografia | 25.327 | 18.685 | 21.108 | 65.120 |
| tomografia | 5.856 | 4.842 | 2.754 | 13.452 |
| US por dia útil (teto de ÷ 252) | 101 | 75 | 84 | 260 |
| TC por dia útil (teto de ÷ 252) | 24 | 20 | 11 | 55 |
| exames por sala de US por dia útil (teto) | 21 | 19 | 21 | |

O horário de 10 horas por dia útil é o turno em que a regra das salas foi montada
(ocupação até 80%).

**O que ficou fora, de propósito.** O tempo por exame (20 e 30 minutos) segue sem ir ao
documento. Em 24/09 conferimos a Seção D dos Parâmetros SUS (Portaria GM/MS nº
1.631/2015, NESCON/UFMG 2013), que propõe **40 minutos e 12 exames por equipamento por
dia** no ultrassom: nesse parâmetro seriam **23 salas** (9 / 7 / 7), e não 13. No
tomógrafo, 7.000 exames por equipamento por ano confirmam um por polo. O Quadro 1 do
mesmo documento (UKAS 2008) dá de 15 a 30 minutos por tipo de exame, o que está mais
perto da nossa premissa. O usuário escolheu não entrar em parâmetro. **Se o analista
confrontar com os Parâmetros SUS, é aqui que a conta aparece** — o R-01 continua de pé.

Cópia do documento: `~/.claude/projects/.../tool-results/webfetch-1790272462018-69a8nk.pdf`
(gov.br, "se-o-d-equipamentos.pdf", 93 páginas). Não está em `normas/`.

## v11, 29/09/2026 — a 6.3 escrita

Apontamento do professor em 29/09: *"tabela em azul escrita faltam informações"*. A
tabela ganhou a coluna **como se obtém**, as linhas de exames por mês (teto de ÷ 12),
dias de funcionamento — **252 dias úteis, 12 meses de 21 dias úteis**, de segunda a
sexta-feira — e exames por tomógrafo por dia útil, e um parágrafo polo a polo.

| exames por mês | Ceilândia | Sobradinho | Gama | total |
|---|---|---|---|---|
| ultrassonografia (teto de ÷ 12) | 2.111 | 1.558 | 1.759 | 5.428 |
| tomografia (teto de ÷ 12) | 488 | 404 | 230 | 1.122 |

O tempo por exame segue fora do documento, por decisão do usuário de 24/09.

## Absenteísmo — v16, 01/10/2026

**Taxa adotada: 20%**, a dos dois planos aprovados do ISHP — pt_ses_01 e pt_ses_05,
"Estima-se uma taxa média mínima de 20% de absenteísmo" (normalizados/pt_ses_01/texto.md,
linha 747). Os dois compensam a falta ofertando vagas acima da meta.

A versão da equipe de 01/10 publicava "absenteísmo de até 26,4%", complemento da ocupação
GLOBAL de 73,6%. Por polo a conta não fecha:

| | carga | capacidade (10 h × 252 dias) | com 20% de falta | falta máxima que o polo absorve |
|---|---|---|---|---|
| US Ceilândia | 9.176 h | 12.600 h (5 salas) | 91,0% | 27,2% |
| US Sobradinho | 7.066 h | 10.080 h (4 salas) | 87,6% | 29,9% |
| US Gama | 7.864 h | 10.080 h (4 salas) | 97,5% | **22,0%** |
| TC Ceilândia | 1.928 h | 2.520 h | 95,6% | **23,5%** |
| TC Sobradinho | 1.592 h | 2.520 h | 79,0% | 36,8% |
| TC Gama | 904 h | 2.520 h | 44,8% | 64,1% |

Com 26,4%, o ultrassom do Gama e a tomografia de Ceilândia estouram. Com 20%, todos cabem,
mas o Gama e Ceilândia ficam acima de 95%: é ali que o R-01 mora.

**A fila suporta?** A meta (78.572) é a fila inteira de 10/09/2026. A falta não tira o
usuário da fila — ele é reagendado; quem sai é o que soma três faltas ou não atende em três
dias consecutivos, e o que a validação encerrar. Essa saída só se repõe se a fila receber
solicitações novas durante a vigência. Na tomografia ela recebe: **89% das solicitações
pendentes em 15/09/2026 eram de 2026** (11.732 de 13.125, Mapa Social, filtro Ano = 2026).
No ultrassom a coleta não traz o ano da solicitação, e a espera média de 561 dias indica fila
antiga — é onde a saída pesa. O instrumento para isso é o ajuste da meta por termo aditivo da
2.2.

## v19, 05/10/2026 — os números novos, mesmo método

Recalculado com o método da v18, reproduzido antes ao exame (rateio, horas, curva e
parcelas batem com a v18). Quantidades por nome de fila: o acréscimo de cada código se
reparte entre os seus nomes pelas abertas de 2026; o rateio usa as participações de
15/09/2026, por decisão do usuário (o rateio da fila de 05/10 fica para o redesenho dos
10 pontos de atendimento).

A execução do objeto requer **32.150 horas** de sala no período: **26.760 horas** de
ultrassonografia e **5.390 horas** de tomografia computadorizada.

| | Ceilândia | Sobradinho | Gama | total |
|---|---|---|---|---|
| exames | 35.174 | 26.617 | 26.727 | 88.518 |
| ultrassonografia | 28.054 | 20.729 | 23.376 | 72.159 |
| tomografia | 7.120 | 5.888 | 3.351 | 16.359 |
| horas de ultrassom | 10.189 | 7.855 | 8.716 | 26.760 |
| ocupação em 5/4/4 salas | 80,9% | 77,9% | 86,5% | |
| horas de tomógrafo | 2.349 | 1.939 | 1.102 | 5.390 |
| ocupação do tomógrafo | 93,2% | 76,9% | 43,7% | |

As 13 salas ficam (decisão de 03/10/2026). A regra antiga de ocupação até 80% daria 6/4/5.

**Ponto 4 resolvido pelos números.** As 5.390 horas equivalem a 2,14 tomógrafos em
turno de dez horas. Concentrar em dois polos estoura o tomógrafo do polo receptor em
todas as combinações — a menor é Sobradinho absorvendo o Gama: 1.939 + 1.102 = 3.041 h,
120,7% de 2.520 h. A frase da 6.3 fica, com os números novos.

Curva: 22.127 · 22.128 · 22.131 · 22.132; o trimestre de maior carga dá 352 exames por
dia útil (22.132 ÷ 63). Postos por polo, pela produção e maiores restos: operadores
3/2/2, assistentes 3/2/3.

## v20, 06/10/2026 — seis polos, mesmo método

Os polos passam a seis (decisão do usuário): Ceilândia (Oeste), Taguatinga (Sudoeste),
Sobradinho (Norte e Leste), Plano Piloto (Central), Gama (Sul) e Guará (Centro-Sul). As
participações por procedimento são as de 15/09/2026, as mesmas da v18 e da v19, agora
agrupadas por Região. A Leste fica com Sobradinho, como na v19 e no pt_ses_05.

A execução do objeto requer **28.817 horas** de sala no período: **24.317 horas** de
ultrassonografia e **4.500 horas** de tomografia computadorizada.

| | Ceilândia | Taguatinga | Sobradinho | Plano Piloto | Gama | Guará | total |
|---|---|---|---|---|---|---|---|
| exames | 4.610 | 26.888 | 19.050 | 4.721 | 16.336 | 7.752 | 79.357 |
| participação | 5,81% | 33,88% | 24,01% | 5,95% | 20,59% | 9,77% | |
| ultrassonografia | 3.549 | 21.993 | 15.652 | 3.195 | 14.474 | 6.813 | 65.676 |
| tomografia | 1.061 | 4.895 | 3.398 | 1.526 | 1.862 | 939 | 13.681 |
| horas de ultrassom | 1.322 | 7.934 | 5.860 | 1.269 | 5.529 | 2.403 | 24.317 |
| salas (teto de h ÷ 2.016) | 1 | 4 | 3 | 1 | 3 | 2 | 14 |
| ocupação das salas | 52% | 79% | 78% | 50% | 73% | 48% | |
| horas de tomógrafo | 353 | 1.609 | 1.116 | 503 | 612 | 307 | 4.500 |
| ocupação do tomógrafo | 14% | 64% | 44% | 20% | 24% | 12% | |

Salas pela regra dos 80% por polo, a mesma que deu 5/4/4 na v18 (24.106 h). Com seis
polos o arredondamento de cada um soma uma sala: 14. Um tomógrafo por polo, como na v19:
seis equipamentos para uma carga de 1,79 tomógrafo (4.500 ÷ 2.520 h). A frase da 7.3 sobre
concentrar a tomografia em dois polos sai: com seis polos ela ficou falsa — os 4.500 h
cabem em dois equipamentos (2.250 h cada, 89% de 2.520 h).

Curva: 19.834 · 19.839 · 19.841 · 19.843; o trimestre de maior carga dá 315 exames por
dia útil (19.843 ÷ 63). A soma das capacidades diárias dos polos, 265 de ultrassonografia
e 58 de tomografia, passa dos 315 porque cada polo arredonda para cima.

## v21, 07/10/2026 — dez polos, sem localização fixa

Pedido de 10 polos. Decisão do usuário: partir dos seis da v20 e acrescentar quatro — um na
Sul, um na Sudoeste, um na Central e um na Norte e Leste — sem fixar a localização de
nenhum. O plano diz só quantos polos há em cada Região. Os seis territórios são os da v20,
então o rateio, as horas, a curva e as parcelas não mudam.

| | Oeste | Sudoeste | Norte e Leste | Central | Sul | Centro-Sul | total |
|---|---|---|---|---|---|---|---|
| polos | 1 | 2 | 2 | 2 | 2 | 1 | 10 |
| exames | 4.610 | 26.888 | 19.050 | 4.721 | 16.336 | 7.752 | 79.357 |
| horas de ultrassom | 1.322 | 7.934 | 5.860 | 1.269 | 5.529 | 2.403 | 24.317 |
| salas (80%, no mínimo uma por polo) | 1 | 4 | 3 | 2 | 3 | 2 | 15 |
| médicos de US (h ÷ 1.800, no mínimo um por sala) | 1 | 5 | 4 | 2 | 4 | 2 | 18 |
| tomógrafos (mínimo) | 1 | 1 | 1 | 1 | 1 | 1 | 6 |

A Central sobe de uma para duas salas e de um para dois médicos: são dois polos, e cada um
precisa de sala e de médico. As outras Regiões com dois polos já tinham salas para os dois.

**Tomografia: só o mínimo.** O ideal, para o usuário, é um tomógrafo por polo, mas o plano não
se compromete com isso: diz que a tomografia é feita em pelo menos um polo de cada Região (as
Regiões Norte e Leste contadas juntas, como na v20), com no mínimo seis tomógrafos para a carga
de 1,79. É o que os aprovados fazem — o pt_ses_02 do IEV escreve "no mínimo 3 unidades". A equipe
de tomografia (radiologistas, técnicos e enfermagem) é a da v20, por tomógrafo.

Responsável técnico e médico de retaguarda seguem um por polo (10 e 10 por dia útil); recepção,
dois por polo (20). Tudo no valor unitário.

**Revisão de 07/10/2026 — tomografia em letras miúdas.** A pedido do usuário, o documento não
mostra mais a carga de 1,79 tomógrafo (4.2, 7.3 e R-08) e diz "pelo menos um" polo com tomografia
por Região. Na 7.3, a linha dos tomógrafos fica "pelo menos 6" e "≥ 1" por Região, e sai a linha
"Exames por tomógrafo por dia útil", que dependia de haver exatamente um por Região. A carga
continua aqui como controle interno: 4.500 h ÷ 2.520 h = 1,79.

## v22, 07/10/2026 — oito meses

Oito meses de 21 dias úteis: **168 dias úteis**. Um médico, a 1.800 h anuais, dá **1.200 horas**
nos oito meses. Sala e tomógrafo, a 80% de 10 h por dia útil, dão 1.344 h no período.

A execução do objeto requer **28.822 horas** de sala: **24.321 horas** de ultrassonografia e
**4.501 horas** de tomografia computadorizada (4.501 ÷ 1.680 h = carga de **2,68** tomógrafos).

| | Oeste | Sudoeste | Norte e Leste | Central | Sul | Centro-Sul | total |
|---|---|---|---|---|---|---|---|
| polos | 1 | 2 | 2 | 2 | 2 | 1 | 10 |
| exames | 4.611 | 26.894 | 19.054 | 4.722 | 16.339 | 7.753 | 79.373 |
| horas de ultrassom | 1.322 | 7.936 | 5.861 | 1.269 | 5.530 | 2.403 | 24.321 |
| salas (h ÷ 1.344, no mínimo uma por polo) | 1 | 6 | 5 | 2 | 5 | 2 | 21 |
| médicos de US (h ÷ 1.200, no mínimo um por sala) | 2 | 7 | 5 | 2 | 5 | 3 | 24 |
| horas de tomógrafo | 353 | 1.609 | 1.117 | 503 | 612 | 307 | 4.501 |
| tomógrafos (h ÷ 1.344, no mínimo um) | 1 | 2 | 1 | 1 | 1 | 1 | 7 |
| ocupação dos tomógrafos | 21% | 48% | 66% | 30% | 36% | 18% | |
| radiologistas (h ÷ 1.200, no mínimo um por tomógrafo) | 1 | 2 | 1 | 1 | 1 | 1 | 7 |

Curva em quatro bimestres: 19.841 · 19.841 · 19.843 · 19.848; o bimestre de maior carga dá
**473 exames** por dia útil (19.848 ÷ 42). A soma das capacidades diárias das Regiões, 395 de
ultrassonografia e 86 de tomografia, passa dos 473. Técnicos em radiologia 21 e enfermagem 14
(3 e 2 por tomógrafo); recepção 20, responsáveis técnicos 10 e retaguarda 10 por dia útil (por polo).

**Revisão de 07/10/2026 — dois trimestres e um bimestre.** O usuário corrigiu os quatro bimestres: as
parcelas são duas trimestrais e a última bimestral. Cada procedimento se reparte em três oitavos por
trimestre e dois oitavos no bimestre final: 29.760 · 29.764 · 19.849 exames, cerca de 472 a 473 por dia
útil em todos os períodos. O de maior carga é o bimestre final, de 42 dias úteis, com **473 exames** por dia útil
(19.849 ÷ 42). O apoio acompanha os meses: 344.865,00 · 344.865,00 · 229.910,00.


## v24, 20/10/2026 — seis polos, dois cenários de tomografia

Seis polos, um por Região de Saúde, com a Central e a Centro-Sul num polo comum (estudo de 20/10/2026 em
`../estudos/estudo_polos_rede_capacidade_20261020.md`). O método é o da v22: participações por procedimento de 15/09/2026,
agora nas sete Regiões e somadas nos polos. Sala e tomógrafo a 80% de 10 h por dia útil: 1.344 h no período; médico,
1.200 h.

A execução do objeto requer **28.742 horas** de sala: **24.261 horas** de ultrassonografia e
**4.481 horas** de tomografia computadorizada (4.481 ÷ 1.344 h = carga de **3,33** equipamentos).

| | Oeste | Sudoeste | Norte | Leste | Central e Centro-Sul | Sul | total |
|---|---|---|---|---|---|---|---|
| exames | 4.596 | 26.821 | 6.700 | 12.301 | 12.436 | 16.298 | 79.152 |
| participação | 5,81% | 33,89% | 8,46% | 15,54% | 15,71% | 20,59% |  |
| ultrassonografia | 3.540 | 21.947 | 4.676 | 10.941 | 9.982 | 14.444 | 65.530 |
| plano B: ultrassonografia do polo, sobre o total | 4,47% | 27,73% | 5,91% | 13,82% | 12,61% | 18,25% | tomografia na rede: 17,21% |
| tomografia | 1.056 | 4.874 | 2.024 | 1.360 | 2.454 | 1.854 | 13.622 |
| horas de ultrassom | 1.318 | 7.917 | 2.147 | 3.700 | 3.661 | 5.518 | 24.261 |
| salas (h ÷ 1.344, no mínimo uma) | 1 | 6 | 2 | 3 | 3 | 5 | 20 |
| médicos de US (h ÷ 1.200, no mínimo um por sala) | 2 | 7 | 2 | 4 | 4 | 5 | 24 |
| horas de tomógrafo | 351 | 1.602 | 664 | 448 | 807 | 609 | 4.481 |
| carga de tomografia (h ÷ 1.344) | 0,26 | 1,19 | 0,49 | 0,33 | 0,60 | 0,45 | 3,33 |

**Plano A (seis polos com tomografia).** Um tomógrafo por polo, seis no total. A Sudoeste passa de um equipamento
(1,19); o proponente libera no polo da Oeste (0,26) a agenda do excedente. Radiologistas pelas horas de cada polo, no
mínimo um por tomógrafo: 1, 2, 1, 1, 1 e 1 = 7; técnicos 18 e enfermagem 12 (3 e 2 por tomógrafo).

**Plano B (tomografia em rede).** O documento não diz quantos tomógrafos nem onde: publica a carga (3,33),
as 4.481 horas, os 13.622 exames e os radiologistas da rede (4.481 ÷ 1.200 = 3,73, no mínimo
4). A 3.4 reparte a ultrassonografia por polo e põe a tomografia numa linha da rede, as duas sobre o total (participações acima); a Meta 4 se reparte por polo. Uso
interno: cinco polos com tomografia, a Leste sem; a distribuição RA a RA está em `../calculo_v24/polos_capacidade.json`.

Curva: 29.677 · 29.682 · 19.793; o bimestre final dá **472 exames** por dia útil
(19.793 ÷ 42). A soma das capacidades diárias dos polos, 393 de ultrassonografia
e 86 de tomografia (plano A; 82 na rede, plano B), passa dos 472
porque cada número arredonda para cima. Postos lotados: um assistente administrativo por polo (6); os operadores, a
direção e as coordenações atuam de forma centralizada.


## v25, 21/10/2026 — o quadro de 21/10 e a capacidade em horas

Mesmo método da v24. A execução do objeto requer **28.738 horas** de sala: **24.260 horas** de ultrassonografia e
**4.478 horas** de tomografia computadorizada (4.478 ÷ 1.344 h = carga de **3,33** equipamentos).

| | Oeste | Sudoeste | Norte | Leste | Central e Centro-Sul | Sul | total |
|---|---|---|---|---|---|---|---|
| exames | 4.595 | 26.818 | 6.699 | 12.300 | 12.436 | 16.296 | 79.144 |
| ultrassonografia | 3.539 | 21.946 | 4.676 | 10.940 | 9.982 | 14.443 | 65.526 |
| tomografia | 1.056 | 4.872 | 2.023 | 1.360 | 2.454 | 1.853 | 13.618 |
| horas de ultrassom | 1.318 | 7.917 | 2.147 | 3.700 | 3.661 | 5.517 | 24.260 |
| horas de tomógrafo | 351 | 1.601 | 663 | 448 | 806 | 609 | 4.478 |
| exames por dia útil, ultrassom | 22 | 131 | 28 | 66 | 60 | 86 | 393 |
| exames por dia útil, tomografia | 7 | 29 | 13 | 9 | 15 | 12 | 85 |

O texto passa a publicar a capacidade da ultrassonografia em horas, sem número de salas por polo (usuário, 21/10/2026):
o número de salas de cada polo sai do tempo de exame praticado nele, conferido no mês 1. Variante A: seis tomógrafos,
um por polo no dimensionamento, com a tomografia de um polo podendo ser feita em outro da rede. Variante B: o texto
não diz quantos tomógrafos, só a carga de 3,33 equipamentos, que a rede atende com folga; radiologistas da rede
4.478 ÷ 1.200 = 3,73 (no mínimo 4).
