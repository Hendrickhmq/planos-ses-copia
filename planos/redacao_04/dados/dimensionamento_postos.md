# Dimensionamento dos postos — memória interna

**Saiu do plano em 17/09/2026**, por decisão do usuário: *"não precisa deixar esses
números claros, nenhum outro plano faz isso"*. Fica aqui pela regra 9 do `PADRAO.md` —
o conteúdo migra, não some.

**O acervo confirma a decisão.** Três dos quatro planos aprovados não trazem uma única
ocorrência de carga por posto, tempo por tarefa ou jornada efetiva; o pt_ses_01 traz
duas. E no plano 3 as duas tabelas de dimensionamento de posto **saíram em 05/09/2026**,
depois de o professor marcá-las célula por célula — é o mesmo defeito, pela segunda vez.

O que o plano publica agora é a **lotação**, como faz a subseção 9.4 do plano 3: quantos
postos, de que cargo, em cada polo. A derivação fica aqui.

## A base

| parâmetro | valor | fonte |
|---|---|---|
| Exames do objeto | 81.546 | planilha de 10/09/2026 |
| Dias úteis na vigência | 252 | 12 meses × 21 |
| Jornada efetiva por posto | 6 h | **premissa, sem fonte** — é a do plano 3 |
| Postos por função | 6 | decisão do usuário em 15/09/2026 |

Seis postos × 6 h × 252 dias = **9.072 horas** por função, o que dá **6 minutos e 41
segundos por exame** sobre os 81.546 do objeto.

## Como os doze postos foram repartidos

A carga de cada polo é proporcional à sua produção:

| polo | exames | carga em postos | postos adotados |
|---|---|---|---|
| Ceilândia | 33.073 | 2,43 | **2** |
| Sobradinho | 24.196 | 1,78 | **2** |
| Gama | 24.277 | 1,79 | **2** |
| **total** | **81.546** | **6,00** | **6** |

Vale para as duas funções — registro e agendamento —, e dá a lotação de quatro postos
por polo que a subseção 5.10 publica.

**O arredondamento não é para cima aqui, e não podia ser.** A soma é exatamente seis, e
arredondar Ceilândia para três exigiria tirar um posto de outro polo. Pelo maior resto,
os seis se repartem 2 · 2 · 2.

## O que isso implica, e que o documento não diz

| polo | minutos por exame que dois postos comportam |
|---|---|
| Sobradinho | 7,50 |
| Gama | 7,47 |
| **Ceilândia** | **5,49** |

**Ceilândia opera sem folga.** Responde por 40,56% da produção e recebe um terço dos
postos, porque seis não se dividem em 2,43 · 1,78 · 1,79. A compensação é a
redistribuição de carga entre polos pela Coordenação Administrativa, que o documento
declara sem publicar o número que a motiva.

**É o ponto a reabrir se o quantitativo de postos mudar.** Sete operadores em vez de
seis levariam Ceilândia a 8,23 minutos e o apoio a 7,64% do global — dentro do teto de
8%, na aritmética de `apoio_proposta.md`.

## v19, 05/10/2026

+1 operador e +2 assistentes (decisão do usuário): 7 operadores e 8 assistentes para
88.518 exames. Repartidos pela produção de cada polo, por maiores restos:

| polo | exames | operadores | assistentes |
|---|---|---|---|
| Ceilândia | 35.174 | 3 (2,78) | 3 (3,18) |
| Sobradinho | 26.617 | 2 (2,10) | 2 (2,41) |
| Gama | 26.727 | 2 (2,11) | 3 (2,42) |
| **total** | **88.518** | **7** | **8** |

Com 6 h efetivas por posto e 252 dias, os 7 operadores dão 10.584 h, ou 7,2 minutos por
exame; os 8 assistentes, 12.096 h, ou 8,2 minutos — mais que os 6min41s da v18.

## v20, 06/10/2026 — seis polos

Opção C (decisão do usuário): 6 operadores e 8 assistentes para 79.357 exames.

| polo | exames | operadores | assistentes |
|---|---|---|---|
| Ceilândia | 4.610 | 1 | 1 |
| Taguatinga | 26.888 | 1 | 2 |
| Sobradinho | 19.050 | 1 | 2 |
| Plano Piloto | 4.721 | 1 | 1 |
| Gama | 16.336 | 1 | 1 |
| Guará | 7.752 | 1 | 1 |
| **total** | **79.357** | **6** | **8** |

Um operador por polo: o texto da v6 põe um operador de registro dedicado em cada polo
(R-11) e faz o registro no polo, pelo operador ali lotado (9.2). Um assistente por polo, e
os dois restantes pela produção, por maiores restos (2 × participação: Taguatinga 0,68,
Sobradinho 0,48, Gama 0,41) — decisão do usuário em 06/10/2026. A primeira repartição, só
pelos restos (0/3/2/0/2/1), deixava Ceilândia e o Plano Piloto sem assistente. Com 6 h
efetivas por posto e 252 dias, os 6 operadores dão 9.072 h, ou 6,9 minutos por exame; os
8 assistentes, 12.096 h, ou 9,1 minutos.

## v21, 07/10/2026 — dez polos

O apoio não muda: 6 operadores e 8 assistentes, R$ 922.260,00. As colunas passam de polo a
Região: um operador por Região (R-11 e 9.2 dizem agora "em cada Região"), assistentes 1/2/2/1/1/1.
Um operador por polo daria 10 operadores e R$ 1.128.660,00 (9,74% do global), acima do teto de 8%
(R$ 927.420,96). Com um operador para dois polos, a 9.2 perdeu a frase "Os dados não transitam
entre unidades antes de serem lançados".

## v22, 07/10/2026 — oito meses, gestão com os nomes da ISHP

Direção Executiva de Projeto, Coordenação Operacional e Coordenação Administrativa e Financeira, com
os nomes e preços do pt_ses_01 (ISHP); assessoria; 10 operadores e 10 assistentes, um de cada por
polo. A parte técnica fica com um dos dez responsáveis técnicos de polo, no valor unitário. Com 6 h
efetivas por posto e 168 dias, os 10 assistentes dão 10.080 h, ou 7,6 minutos por exame (79.373); os
10 operadores, 10.080 h, também 7,6 minutos.
