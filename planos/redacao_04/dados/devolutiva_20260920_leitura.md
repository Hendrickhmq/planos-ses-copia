# devolutiva de 20/09/2026 — leitura antes de alterar

Arquivo: `redacao_04/dados/devolutiva_20260920.docx`
Base marcada: **v7** (`versoes/plano_v7_20260917.docx`) — confirmado pelo diff.

## O que veio

| cor | marcas | significado | fonte do significado |
|---|---|---|---|
| vermelho | 41 | sai do documento | o usuário declarou |
| amarelo | 35 | alterar | o usuário declarou |
| **ciano** | **35** | **desconhecido** | não apareceu na devolutiva de 05/09 |
| **#e6b8af** (salmão) | **8** | **desconhecido** | prima de `#f4cccc`, que em 05/09 era "valor errado" |

Comentários do Word: nenhum. Controle de revisões: desligado.

**Uma edição digitada**, sem cor: `Ultrassonografia de articulação` **`xxxxxxxxxx`**
na tabela da 2.2.

As duas cores desconhecidas caem **exclusivamente sobre tabelas inteiras**, e só sobre
duas: a segunda tabela da 2.2 (8 células = 2 de cabeçalho + 6 de dados) e a tabela
inteira da 6.3 (35 células). A prosa em volta das duas ficou sem marca.

---

## VERMELHO — 41 marcas em 6 blocos

### 1. 2.1, parágrafo da delimitação negativa (1 marca)

> A obrigação do convênio compreende o agendamento, o preparo, a realização do exame,
> o laudo e a entrega do resultado. **Não compreende** consulta de entrada, consulta de
> retorno nem condução do cuidado após a entrega do laudo, que permanecem com a
> unidade solicitante.

O parágrafo existia para separar este objeto do OCI. Cumprida essa função na redação,
ele passa a enunciar o que o convênio **não** faz — e quem lê é o analista.

### 2. 3.4 Dimensionamento, seção inteira (17 marcas: título + tabela)

A tabela-resumo US / TC / execução assistencial / planejamento-gestão-prestação de
contas / valor global. Duas coisas de uma vez: antecipa a seção 9 e **isola numa linha
própria os R$ 845.460,00 de apoio**, que na planilha estão distribuídos entre as Metas
1, 2, 3 e 6. É o mesmo apontamento de 17/09 — *"não precisa deixar esses números
claros, nenhum outro plano faz isso"* —, agora sobre a única tabela que ainda exibia
a separação.

### 3. 3.6, último parágrafo (1 marca)

> Os valores das demais rubricas observam parâmetros de mercado e os princípios da
> economicidade e da razoabilidade, compatíveis com o dimensionamento do objeto.

Afirmação sem conteúdo verificável.

### 4. 9.2 Metodologia de composição de custos, seção inteira (3 marcas)

Explica como a planilha está organizada. Meta-comentário: descreve o quadro em vez de
apresentá-lo. **Nenhum dos cinco aprovados tem seção equivalente** — `grep` por
"composição de custos" em `normalizados/*/texto.md` não retorna nada.

### 5. 9.3 Delimitação das rubricas, seção inteira (15 marcas)

A lista dos nove itens que o valor unitário remunera — equipe assistencial, sala,
contraste, sistema de imagem, imóvel, energia, água, limpeza, vigilância.

Duas razões convergem: **nenhum dos cinco aprovados enumera o que o unitário cobre**
(`grep` por "remunera" / "delimitação das rubricas": zero), e a lista abre à
concedente a composição de um preço que **não é nosso** — é o parâmetro federal da
4.282/2026. Enumerar o conteúdo de um preço que não compomos convida à auditoria de
uma composição que não temos.

### 6. 9.4 Memória de cálculo, título e 3 de 4 parágrafos (4 marcas)

Saem **Postos operacionais**, **Períodos** e **Valores unitários**.
**Fica, sem marca, o parágrafo da Assessoria de Prestação de Contas.**

Isso não é descuido. O pt_ses_05 é o único aprovado que traz memória de cálculo, e
traz **uma por rubrica que precisa se justificar** — locação, sistema e **prestação de
contas** (linhas 878, 938 e 3258 de `normalizados/pt_ses_05/texto.md`). É exatamente
a que ele deixou de pé.

---

## AMARELO — 35 marcas

### Grupo A — a entrega dupla do laudo (8 marcas)

2.3 p104 · 5.8 inteira, título e 4 parágrafos · 5.13 meta qualitativa.

O plano diz que o exame só se considera executado quando o laudo é entregue ao usuário
**e** encaminhado à unidade solicitante; que *"as duas entregas são distintas e nenhuma
substitui a outra"*; faz disso a unidade de aferição; faz disso meta qualitativa a
**100%**; e cria o I-03 para medir.

**O pedido original dizia "e/ou"**: *"o encaminhamento do resultado para o paciente
e/ou para a unidade que fez o pedido do exame"*. São quatro camadas de obrigação
construídas sobre uma alternativa — régua contra o proponente, e a mais cara delas,
porque a segunda entrega depende de um destinatário que não é nosso.

### Grupo B — o enquadramento do preço (3 marcas)

3.3 p164 e p165 · 3.6 p212.

São os parágrafos **reescritos na v7**, depois da conferência do NotebookLM: o
incremento como parâmetro de custo, o Componente Créditos Financeiros, a compensação
tributária, e *"É esse o valor praticado, sem acréscimo próprio, sem índice e sem
recomposição"*.

O plano levanta, contra si, uma objeção que o analista não levantou — e ainda renuncia
a índice e a recomposição que norma nenhuma proibiu. **É aqui que a revisão de preço
pedida antes da devolutiva e a marcação do professor se encontram.**

### Grupo C — o usuário que falha (6 marcas)

5.2 (fragmento: *"o que determina se o exame pode ser realizado na data marcada"*) ·
5.3 (fragmento: *"O usuário que não confirma"*) · 5.7 exame inconclusivo ·
5.9 p258 (fragmento) e p260 · 2.4 p109.

Parágrafos que descrevem modos de falha: não confirma, não comparece, não é
localizado, não retira, exame inconclusivo. Note que em 5.2, 5.3 e 5.9 ele grifou
**só o trecho condicional**, não o parágrafo — a rotina fica, a moldura negativa sai.

### Grupo D — consequência forçada pelo vermelho (1 marca)

5.10 p307: *"...são remunerados pelo valor unitário do exame, **na forma da subseção
9.3**"*. A 9.3 morre no vermelho; a remissão morre junto. Marcação internamente
coerente.

### Grupo E — blocos inteiros (17 marcas)

- **6.2 Curva de produção** (13): título, prosa e tabela. O físico está em semestres
  (1 a 6 / 7 a 12) e o desembolso da 7.2 está em **trimestres**. Duas réguas para o
  mesmo período.
- **7.3 Ajuste por execução** (3): o ajuste na parcela subsequente, a devolução do
  saldo, e a atuação da Coordenação Financeira até a prestação de contas final.
  Mecânica de devolução que o plano se impõe.
- **2.5 p121** (1): remete à 6.3 — a tabela que está em ciano.
- **3.2 título** (1): *"O percurso que a fila trava"*. É o único título do plano com
  verbo e figura. O acervo titula por substantivo: "Organização da Execução",
  "Registro do Desfecho Assistencial", "Dimensionamento das Equipes".

---

## A edição digitada: `xxxxxxxxxx` em "Ultrassonografia de articulação"

Cai sobre a única das doze linhas cujo nome **não corresponde a fila nenhuma**.

`dados/conferencia_procedimentos.md`, linha 32: a fila é `ECOGRAFIA␣␣DE PARTES MOLES`,
2.974 solicitações, marcada **"nome diferente — não existe na tabela"**. Os 2.974
exames da linha "articulação" são **integralmente** partes moles. Não há fila de
articulação.

E o plano trata isso numa frase solta **fora** da tabela de indicações reunidas:

> A ultrassonografia de partes moles é registrada sob o código 02.05.02.006-2.

A frase lê ao contrário: faz partes moles parecer um acréscimo àquele código, quando é
o seu conteúdo inteiro. Quem confrontar o plano com a fila não encontra "articulação"
em lugar nenhum.

---

## O que não dá para ler sem perguntar

1. **Ciano, 35 marcas** — a tabela inteira da 6.3 (capacidade requerida: exames por dia
   útil, horas de sala, salas, horas de tomógrafo, tomógrafos, postos por polo).
   Não apareceu na devolutiva de 05/09.
2. **Salmão `#e6b8af`, 8 marcas** — a tabela das indicações reunidas na 2.2. Em 05/09
   o tom vizinho `#f4cccc` queria dizer "valor errado, corrija"; não é o mesmo tom.
3. ~~**`xxxxxxxxxx`**~~ — **resolvido em 22/09/2026:** o procedimento sai do plano, porque será
   contemplado em outra OCI. Aplicado na v8 (D-007), antes do vermelho e do amarelo.

`PADRAO.md`, regra da devolutiva: cor desconhecida se pergunta, não se adivinha.
Em 05/09 `#2e74b5` passou por três trechos e foi adivinhada errada.
