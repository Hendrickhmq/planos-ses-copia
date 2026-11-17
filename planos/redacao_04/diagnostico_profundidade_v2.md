# Diagnóstico — profundidade e linguagem da v2

Feito em 17/09/2026 a pedido do usuário, **sem alterar o plano**. Mede a v2 contra o
plano 3 e contra os quatro planos aprovados extraídos em `normalizados/`.

---

## 1. A medida que importa não é linha, é prosa

Linha engana: tabela ocupa linha e não é argumento.

| documento | palavras de prosa | palavras em tabela | % em tabela |
|---|---|---|---|
| **plano 4 (v2)** | **2.596** | 3.172 | **55,0%** |
| plano 3 | 3.515 | 2.758 | 43,8% |
| pt_ses_02 (IEV) | 4.801 | — | — |
| pt_ses_03 (IEV) | 4.541 | — | — |
| pt_ses_04 (IEV) | 7.052 | — | — |
| pt_ses_01 (ISHP) | 12.289 | — | — |

*As tabelas dos aprovados foram extraídas para CSV separado, então a coluna de prosa
deles é comparável à minha.*

**O plano tem 74% da prosa do plano 3 e 54% da prosa do menor plano aprovado.** E é o
documento mais tabular do conjunto: mais da metade das suas palavras estão dentro de
grades.

**O usuário está certo, e a palavra certa é essa: é tabular, não é raso em dado.** Os
números estão todos lá. O que falta é o texto que os transforma em decisão.

---

## 2. Onde a rasura está

| seção | prosa v2 | prosa plano 3 | razão |
|---|---|---|---|
| 1. Identificação | 0 | 0 | — |
| 2. Objeto | 259 | 375 | 0,69× |
| 3. Justificativa e dimensionamento | 404 | 455 | 0,89× |
| 4. Proponente | 27 | 66 | `[preencher]` |
| **5. Metodologia** | **839** | **1.707** | **0,49×** |
| 6. Cronograma físico | 303 | 72 | 4,21× |
| 7. Cronograma de desembolso | 156 | 183 | 0,85× |
| 8. Riscos | 393 | 246 | 1,60× |
| **9. Planilha e memória de cálculo** | **215** | **393** | **0,55×** |

**Três seções concentram o problema: 5, 9 e 2.** As seções 6 e 8 já passaram o plano 3.

---

## 3. O padrão do defeito, visto de perto

A seção 5 do plano 3 tem quinze subseções e **a menor delas tem 59 palavras de
prosa**. A minha tem quinze e **quatro estão abaixo de 26**.

| subseção | palavras de prosa |
|---|---|
| 5.3 Confirmação | **19** |
| 5.7 Laudo | **21** |
| 5.6 Realização do exame | **23** |
| 5.9 Busca ativa e reagendamento | **25** |
| 5.4 Recepção e identificação | 49 |
| 5.8 Entrega do resultado | 56 |

**5.6 e 5.7 somam 44 palavras — e são o núcleo do objeto.** O convênio contrata
realizar o exame e laudar; as duas subseções que descrevem esses atos dizem, juntas,
menos do que qualquer subseção do plano 3.

### O mesmo passo, nos dois planos

**Plano 4, subseção 5.2 — 47 palavras de prosa e uma tabela:**

> O usuário é contatado para agendamento e recebe, no mesmo contato, a orientação de
> preparo do exame agendado. O preparo varia por procedimento e é o que determina se o
> exame pode ser realizado na data marcada. [tabela] A orientação é entregue por
> escrito e repetida na confirmação.

**Plano 3, subseção 5.3 — 187 palavras:** diz o mesmo e continua. Diz que a orientação
é verbal *e* escrita; nomeia os dois pontos que decidem se o exame acontece; explica
**por que** a confirmação registra nominalmente o acompanhante — *"é o único momento em
que a ausência ainda pode ser corrigida sem perda de vaga"*; e fecha com o que
acontece quando a condição falha, com a base normativa que o autoriza.

**A diferença não é comprimento. É que a minha prosa afirma e para; a dele afirma e
conclui.** Cada passo do plano 3 responde três perguntas — o que se faz, com que
parâmetro, e o que acontece quando falha. Os meus passos respondem só a primeira, e a
terceira migrou toda para a matriz de riscos.

É a classe 9 da leitura de entrega do `PADRAO.md`: *esta seção diagnostica e não
fecha?*

---

## 4. A seção 3.1 perdeu duas coisas que o plano 3 tem

| | plano 3 | plano 4 |
|---|---|---|
| Fonte nomeada | *"O Mapa Social da Secretaria de Estado de Saúde do Distrito Federal, consultado em 1º de setembro de 2026"* | *"A fila de regulação da Secretaria de Estado de Saúde do Distrito Federal registra, em 10 de setembro de 2026"* — **sem nomear painel ou sistema** |
| Tabela da fila | sim, por Região de Saúde, com a base do rateio explicada ali | **não há tabela** |

**Cinco números vivem só em prosa e não aparecem em nenhuma tabela do plano:** 565
dias, 141 dias, 517, 579 e 66,7%. Todos têm lastro nos arquivos de fonte, nenhum tem
lastro **dentro do documento** — é a classe 2 da leitura de entrega, e a verificação T
existe exatamente para isso.

---

## 5. A memória de cálculo encolheu pela metade

**Plano 3, 9.4:** diz onde cada posto está lotado — *"cada polo tem um operador de
registro e dois recepcionistas"* — e **por que** cada grupo atua em 9 ou em 10 meses.

**Plano 4, 9.4:** diz que os doze postos dispõem de 9.072 horas e que *"todos os postos
atuam nos doze meses da vigência"*. Não diz quantos ficam em cada polo.

A subseção 5.10 promete essa lotação — *"se distribuem entre os três polos na proporção
da subseção 3.5"* — e nunca a quantifica.

---

## 6. Uma inconsistência que a leitura apanhou

A tabela da subseção 6.3 traz **"Postos de trabalho custeados pelo convênio · total 14
· Ceilândia 6 · Sobradinho 4 · Gama 4"**.

Os catorze postos são: 1 Coordenação Administrativa, 6 Operadores de registro, 6
Assistentes Administrativos e 1 Coordenação Financeira. **As duas coordenações não são
de polo** — a 5.10 atribui à Coordenação Administrativa a *"supervisão de todos os
passos e redistribuição de agenda entre polos"*, que é função central.

Distribuir só os doze postos de polo na proporção da 3.5 dá 5 · 4 · 4, e não 6 · 4 · 4.
**A linha aloca aos polos dois postos que são centrais.** É a classe 12 — contradição
interna entre duas subseções.

---

## 7. A linguagem

### O que o corpus usa e o plano não

Normalizado por mil palavras:

| termo | plano 4 | plano 3 | corpus aprovado |
|---|---|---|---|
| fluxo | 0,67 | 1,21 | **2,96** |
| regulação | 1,50 | 0,91 | 2,37 |
| SISREG | **0,00** | 0,00 | **1,29** |
| conformidade | 0,00 | 0,00 | 1,88 |
| paciente | **0,00** | 0,61 | 1,43 |
| monitoramento | 0,67 | 0,61 | 1,36 |
| protocolo | 0,17 | 0,15 | 0,49 |

**Duas ausências merecem decisão, não conserto automático:**

**O SISREG não é nomeado.** Os quatro planos aprovados nomeiam o sistema 37 vezes; o
meu diz *"sistemas oficiais de informação do SUS"* em todas as ocorrências. A escolha
genérica protege contra mudança de sistema dentro da vigência; a escolha nominal é a
do acervo e é o que o analista reconhece. **Nunca foi decidida — apenas aconteceu.**

**"Fluxo" aparece um quinto do que aparece no corpus.** O plano descreve passos e quase
nunca nomeia o fluxo que eles formam. Os aprovados falam em fluxo o tempo todo porque é
assim que a concedente lê a operação.

### O que o corpus usa e o plano faz bem em não usar

*Qualidade* (1,15/mil no corpus), *eficiência* (1,08), *conformidade* (1,88),
*transparência* (0,66) e *rastreabilidade* (0,91) não aparecem no plano. **Isso não é
defeito.** São substantivos abstratos que o `PADRAO.md` exclui por serem afirmação
sobre o documento e não sobre o objeto. O plano 3 também não os usa.

### O ritmo da prosa

| | parágrafos | palavras por parágrafo | parágrafos de uma frase |
|---|---|---|---|
| plano 4 | 79 | 32,5 | 57,0% |
| plano 3 | 93 | 38,1 | 48,4% |
| pt_ses_01 | 586 | 21,0 | 92,0% |
| pt_ses_02 | 279 | 17,2 | 81,0% |

Os aprovados escrevem em muitos parágrafos curtos; eu e o plano 3 escrevemos em poucos
e densos. **A diferença de estilo não é defeito — a de volume é.** Setenta e nove
parágrafos contra duzentos e setenta e nove.

---

## 8. Três tabelas nuas

As tabelas das linhas 7, 18 e 477 não têm prosa antes nem depois: são o quadro
cadastral da 1.1, o do instrumento na 1.2 e a matriz de riscos da 8.2. **As duas
primeiras são formulário e estão certas assim.** A matriz de riscos tem a 8.3 logo
abaixo, que a explica — também está certa.

Não há tabela órfã de verdade neste plano.

---

## 9. O que eu faria, em ordem de peso

1. **As quatro subseções-tronco** — 5.3, 5.6, 5.7 e 5.9. Cada uma precisa da terceira
   pergunta: o que acontece quando falha, e por quê. Hoje isso está só na matriz de
   riscos, e a matriz é resumo, não descrição.
2. **5.6 e 5.7 antes de todas.** São o objeto. Quem executa, sob que protocolo, o que
   o laudo contém, e o que se faz com exame inconclusivo.
3. **Uma tabela da fila na 3.1**, com fonte nomeada e data — os cinco números de espera
   e concentração etária ganham lastro dentro do documento.
4. **A lotação por polo na 9.4** — quantos operadores e quantos assistentes em cada um.
5. **A linha de postos da 6.3** — separar as duas coordenações centrais dos doze postos
   de polo.
6. **Decidir o SISREG** — nomear ou não, e registrar a decisão.

**Nada disso muda um número do envelope.** São 2.596 palavras de prosa que precisam
virar algo entre 3.500 e 4.000 — a faixa do plano 3 e dos IEV —, sem tocar em
aritmética.
