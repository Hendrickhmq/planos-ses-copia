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
