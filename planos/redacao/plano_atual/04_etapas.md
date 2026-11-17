# Seção 4 — Etapas e cronograma físico

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seção 2 · Lacunas: 3 (nenhuma bloqueante)
Vigência: 10 meses · 3 etapas · 14 subetapas

---

## Quadro de etapas

| nº | etapa / subetapa | início | fim | entrega verificável | meta | indicador |
|---|---|---|---|---|---|---|
| **1** | **Pré-produção (implantação operacional)** | mês 1 | mês 1, 2ª semana | **3 polos aptos a operar** | **Meta 2** | IND-03 |
| 1.1 | Organização da estrutura física, equipamentos e insumos nos 3 polos | mês 1 | mês 1 | termo de vistoria por polo | 2 | IND-03 |
| 1.2 | Mobilização e contratação das equipes assistencial, administrativa e de apoio | mês 1 | mês 1 | contratos firmados, por polo e por cargo | 2 | IND-03 |
| 1.3 | Habilitação dos acessos aos sistemas oficiais (SISREG, TrakCare) e validação dos fluxos | mês 1 | mês 1 | acessos ativos, com fluxo testado ponta a ponta | 2 | IND-03 |
| 1.4 | Programação da FPO do executor junto à SES-DF | mês 1 | mês 1 | confirmação de programação do procedimento 09.02.01.002-6 | 2 | IND-03 |
| 1.5 | Publicação das agendas iniciais no SISREG | mês 1 | mês 1 | extrato de vagas ofertadas para a 2ª quinzena | 2 | IND-03, IND-04 |
| **2** | **Execução assistencial** | mês 1, 3ª semana | mês 10 | **35.000 OCI concluídas** | **Meta 1** | IND-01, IND-02 |
| 2.1 | Oferta mensal de horários no SISREG, nos 3 polos | mês 1 | mês 9 | extrato mensal de vagas ofertadas | 1 | IND-04 |
| 2.2 | Consulta de entrada, com usuários encaminhados pela regulação da SES-DF | mês 1, 3ª semana | mês 9 | 35.000 entradas realizadas | 1 | IND-05 |
| 2.3 | Realização dos exames integrantes do pacote | mês 1, 3ª semana | mês 9 | exames vinculados à APAC do usuário | 1 | — |
| 2.4 | Consulta ou teleconsulta de retorno, em até 30 dias da entrada | mês 2 | mês 10 | 35.000 retornos realizados | 1 | IND-07 |
| 2.5 | Busca ativa e reagendamento dos faltosos, nos dois pontos do fluxo | mês 1, 3ª semana | mês 10 | reagendamentos registrados no SISREG | 1 | IND-06 |
| 2.6 | Registro da produção: APAC no SIA/SUS e carga dos formulários nos sistemas oficiais | mês 2 | mês 10 | produção apresentada por competência | 1 | IND-01, IND-08 |
| **3** | **Encerramento e conciliação** | mês 10 | vigência financeira | **execução comprovada e conciliada** | 1 e 2 | IND-02 |
| 3.1 | Conclusão dos pacotes abertos no mês 9 | mês 10 | mês 10 | últimas 4.125 OCI concluídas | 1 | IND-01 |
| 3.2 | Fechamento das últimas competências e conciliação da produção aprovada | mês 10 | vigência financeira | demonstrativo apresentada × aprovada | 1 | IND-01 |
| 3.3 | Relatório final e prestação de contas | vigência financeira | vigência financeira | relatório consolidado → Seção 8 | 1 e 2 | IND-02 |

A subetapa 2.3 não tem indicador próprio: os exames são item do pacote, não
entrega autônoma. Medi-los separadamente seria contar duas vezes a mesma OCI.

---

## Cronograma físico, mês a mês

| | m1 | m2 | m3 | m4 | m5 | m6 | m7 | m8 | m9 | m10 | pós |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** Pré-produção | ▓ | | | | | | | | | | |
| **2** Execução | ▒ | █ | █ | █ | █ | █ | █ | █ | █ | ▒ | |
| 2.2 entradas | ▒ | █ | █ | █ | █ | █ | █ | █ | █ | | |
| 2.4 retornos | | ▒ | █ | █ | █ | █ | █ | █ | █ | █ | |
| **3** Encerramento | | | | | | | | | | █ | █ |
| **entradas** | 2.000 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | — | |
| **OCI concluídas** | — | 2.000 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | 4.125 | |

`▓` meia etapa (2 semanas) · `▒` meia carga · `█` carga cheia

**As etapas 2 e 3 se sobrepõem no mês 10**, de propósito: enquanto os últimos
pacotes se concluem (3.1), a conciliação das competências anteriores já corre
(3.2). Somar as durações como se fossem sequenciais daria 10,5 meses e estouraria
a vigência — a sobreposição é o que faz o cronograma caber.

**A etapa 3 atravessa a fronteira da vigência física.** 3.1 acontece dentro do mês
10; 3.2 e 3.3 correm na vigência financeira, que é posterior e ainda não tem
prazo definido (DV-012). É a distinção que nenhum dos quatro planos aprovados faz
(AC-033).

---

## Verificações da própria seção

**Numeração hierárquica** — sem buraco e sem repetição, o mesmo teste da
verificação I do `conferir.py`:

```
1 → 1.1  1.2  1.3  1.4  1.5
2 → 2.1  2.2  2.3  2.4  2.5  2.6
3 → 3.1  3.2  3.3
```

**Toda meta da Seção 2 aparece em pelo menos uma etapa:**

| meta | etapa |
|---|---|
| Meta 1 — 35.000 OCI concluídas | 2 (integral), 3.1 (último lote) |
| Meta 2 — 3 polos em operação | 1 (integral) |

**Durações dentro da vigência:** a etapa mais longa é a 2, de meia quinzena do
mês 1 ao mês 10 — 9,5 meses de uma vigência de 10.

**Nenhuma etapa de mobilização sem entrega.** É a armadilha clássica: etapa de
partida que não entrega nada e mesmo assim recebe desembolso. A Etapa 1 entrega
3 polos aptos, e cada subetapa tem documento próprio — vistoria, contrato, acesso
ativo, confirmação de FPO, extrato de agenda. É o que dá lastro à 1ª parcela na
Seção 6, e é aferido por IND-03, que não admite tolerância: 3 de 3.

---

## As dependências que não são do executor

Duas subetapas da Etapa 1 dependem de ato da SES-DF, não do proponente:

- **1.3 — habilitação dos acessos** ao SISREG e ao TrakCare. Sem acesso, não há
  como ofertar vaga nem registrar atendimento. Prazo desconhecido
  — `[[lacuna: LC-021]]`, DV-019.
- **1.4 — programação da FPO.** Sem FPO, a produção é registrada e não é
  aprovada. Prazo desconhecido — `[[lacuna: LC-015]]`, DV-004.

**As duas juntas são o risco de partida do plano.** A curva da Seção 2 assume que
2 semanas bastam para as duas. Se não bastarem, a Etapa 1 se estende, a janela de
entrada encolhe e o ritmo mensal sobe — cada quinzena perdida na partida custa
cerca de 240 entradas a mais por mês nos meses seguintes. Vai nomeado na Seção 11,
e é o argumento para que o instrumento fixe prazo para os atos da concedente.

A subetapa 2.2 tem a mesma natureza: o executor oferta a vaga, mas quem a preenche
é a regulação (IND-04, DV-016). A etapa é dele; o insumo dela, não.

---

## Prazo de registro — onde a Etapa 2 realmente termina

A subetapa 2.6 não termina com o retorno: termina com a carga dos formulários, e
é ela que fecha a OCI (Seção 2). Como a produção é entregue por competência,
segundo o cronograma de entrega de bases da SES-DF, o registro do mês 10 cai
depois do mês 10. `[[lacuna: LC-022 — prazo de entrega de bases e de carga dos
formulários. É DV-008.]]`

Consequência para a Seção 6: **a última parcela não pode vencer antes do
fechamento da última competência**, ou remunera produção que ainda não existe
para o sistema.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-015 | Prazo de programação da FPO (subetapa 1.4). | DV-004 |
| LC-021 | Prazo de habilitação dos acessos ao SISREG e ao TrakCare (subetapa 1.3). | DV-019 |
| LC-022 | Prazo de entrega de bases e de carga dos formulários (subetapa 2.6). | DV-008 |

Nenhuma bloqueante. As três são prazos de atos de terceiro, e todas empurram na
mesma direção: se a partida atrasar ou o fechamento demorar, a janela útil
encolhe pelas duas pontas.

---

## Fundamento

- **OB-009** — Manual Operacional da FPO: sustenta a subetapa 1.4 como
  pré-requisito de execução, e não como trâmite paralelo. `a_verificar`.
- **OB-008** — Portaria SAS/MS nº 768/2006: laudo prévio à realização do
  procedimento, o que amarra a ordem entre 2.1, 2.2 e 2.6. `a_verificar`.
- **OB-010** — registro por APAC no SIA/SUS: é o conteúdo da subetapa 2.6.
  `a_verificar`, sem dispositivo identificado.

Nenhuma lida no original.
