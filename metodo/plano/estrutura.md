# plano/estrutura.md — as seções do plano de trabalho

**As tabelas de estrutura abaixo são lidas pela verificação J.** Alterar uma delas é
alterar o padrão: registrar em `../MUDANCAS.md`.

O plano declara qual estrutura segue na chave `estrutura` do `estado.yaml`. Sem a
chave, vale a `padrao`. A estrutura do proponente ou do formulário da SES manda quando
existe (comum, regra 15); as regras de conteúdo deste arquivo valem em qualquer uma.

---

## Estrutura `padrao`

| # | seção | o que absorve |
|---|---|---|
| 1 | Identificação | quadro cadastral do proponente e dados do instrumento |
| 2 | Objeto | composição, unidade de aferição, público-alvo, local de execução |
| 3 | Justificativa e dimensionamento | problema, fila medida, modalidade, dimensionamento, distribuição, economicidade |
| 4 | Proponente | apresentação narrativa |
| 5 | Metodologia e detalhamento das ações | **fluxo → equipe → metas → indicadores**, numeradas 5.1 em diante |
| 6 | Cronograma físico | etapas, curva, capacidade requerida |
| 7 | Cronograma de desembolso | regime, parcelas, ajuste |
| 8 | Riscos | critério e matriz |
| 9 | Planilha e memória de cálculo | composição, delimitação, memória, planilha |

O esqueleto preenchível desta estrutura, seção a seção, é o `modelo.md`.

## Estrutura `formulario_ses_parceria`

O formulário "Plano de Trabalho Simplificado – Modelo Parceria" da SES (SEI 216131719),
pedido pelo Ofício 387/2026 da ARINS. Serve às duas trilhas: o **pré-plano** o preenche
com o mínimo (ver `../pre_plano/formulario.md`); o **plano** o preenche com o conteúdo
de plano detalhado, e então as regras deste arquivo e de `procedimento.md` valem dentro
de cada campo.

| # | seção | o que absorve no plano |
|---|---|---|
| 1 | Informações iniciais | quadro cadastral e dados do instrumento |
| 2 | Objeto | composição, unidade de aferição, público-alvo, local de execução |
| 3 | Justificativa, diagnóstico e contextualização | fila medida, dimensionamento, distribuição |
| 4 | Metodologia | o fluxo, a equipe, o registro da produção |
| 5 | Objetivos | geral e específicos, curtos |
| 6 | Metas e indicadores | metas com dotação, indicadores em 100% |
| 7 | Esboço de cronograma de execução | etapas, curva, capacidade, desembolso |
| 8 | Indicação da aplicação das despesas | planilha e memória de cálculo |
| 9 | Interface com os sistemas da SES-DF | SISREG, TrakCare, registro da produção |

*Origem: redacao_04, a partir da v20 (06/10/2026); o usuário confirmou em 08/10/2026
que o plano 4 é plano, mesmo no formulário.*

## O modelo de plano de trabalho de convênio da SES

Em 21/10/2026 a SES-DF mandou um modelo orientativo de plano de trabalho de convênio, com
o plano de integridade e a lista de habilitação, em `biblioteca/instrumento/modelo_ses/`.
É o modelo mais recente para o plano de convênio (`../comum.md`, regra 15). A estrutura dele
ainda não tem chave própria em `estrutura` nem na verificação J: ganha quando o primeiro
plano for escrito nele.

---

## As regras de conteúdo

**A identificação cadastral fica na primeira seção**, em quadro tabular, como nos cinco
aprovados. A seção do proponente é **narrativa** e não repete os campos, nem traz lista
de pré-condições com coluna de comprovação (comum, regra 6). Natureza jurídica não é
campo da tabela; o CNES não aparece no quadro inicial.
*Origem: redacao_03, 01/09/2026; virou a verificação O.*

**Riscos vêm antes da planilha, e a planilha é a última peça do documento.** É a ordem
dos três planos do IEV e a que o professor exigiu: *"as rubricas de gasto têm que ser
a última coisa do plano de trabalho"*.
*Origem: redacao_03, devolutiva de 05/09/2026.*

**A planilha se organiza por Meta**, não por rubrica nem por polo. Meta 1 —
planejamento, estruturação e gestão; Meta 2 — execução assistencial; Meta 3 —
monitoramento, conclusão e encerramento. **Toda meta declarada no texto tem dotação na
planilha**, e vice-versa.
*Origem: redacao_03; virou a verificação P.*

**O que cada meta carrega:** descrição, **quantitativo aferível** e **prazo**.
Quantitativo que não se conta na prestação de contas não é meta: "3 polos em operação"
e "10 relatórios mensais" contam; "gestão adequada" não.

**A meta qualitativa é obrigatória** e vem logo abaixo da tabela de metas. O art. 7º,
III, do Decreto DF nº 48.727/2026 a exige; a citação sai pelo teste de comum, regra 7,
e a obrigação fica. Ela mede a qualidade da entrega, não o volume.

**Meta e indicador se pactuam em 100%.** Nenhum dos cinco aprovados pactua menos.
Pactuar 95% é pedir 5% de tolerância antes de começar e entregar ao analista o cálculo
da glosa; a diferença entre previsto e executado é o que o ajuste por execução
resolve. Exceção só declarada no `estado.yaml`, em `indicadores_fora_de_100`, com o
motivo. **Indicador que mede gestão interna** (aproveitamento de vaga, distribuição
entre polos) **não é indicador do convênio** e não entra.
*Origem: pt_ses_05 ("Parâmetro de Aferição: 100%"); redacao_03; virou a verificação S.*

**Meta, indicador, parâmetro e meio de verificação são quatro coisas:**

| conceito | pergunta que responde | exemplo |
|---|---|---|
| meta | quanto se compromete a entregar | 4.800 consultas em 12 meses |
| indicador | como se mede o desempenho | consultas realizadas ÷ consultas pactuadas |
| parâmetro de aferição | qual valor conta como cumprido | 100% |
| meio de verificação | onde se comprova | produção aprovada no SIA/SUS, competência mensal |

O defeito mais comum é escrever a meta na coluna do indicador. Indicador sem
denominador é contagem, e contagem já era a meta. O meio de verificação é fonte que
existe e que a concedente acessa: "relatório do proponente" sozinho é
autodeclaração.
*Origem: estudo dos aprovados, agosto de 2026.*

---

## Os títulos

Sintagmas nominais que nomeiam uma peça. Nenhum começa com *Por que*, *O que*, *Como*,
*Quando*, *Quanto* ou *Onde*. O teste é mecânico: **o título nomeia uma coisa, ou
anuncia um argumento?** Anunciando, reescreve-se. No formulário da SES, os títulos de
primeiro nível são os do formulário.
*Origem: redacao_02; virou a verificação K.*

## O que não volta

Base legal como seção · O que não incide · Elegibilidade e habilitação como seção ·
Prestação de contas como seção · Contrapartida · Sumário executivo · Declaração de
fragilidade de qualquer espécie · Origem dos preços linha a linha.
*Origem: redacao_02, cortes de 31/08/2026; virou parte da J.*
