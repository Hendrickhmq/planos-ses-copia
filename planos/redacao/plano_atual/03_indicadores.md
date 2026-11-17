# Seção 3 — Indicadores e meios de verificação

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seção 2 · Lacunas: 4 (nenhuma bloqueante)
Apuração: mensal, por competência · Metas cobertas: 1 e 2
11 indicadores: 3 pactuados, 5 de acompanhamento, 3 qualitativos

---

## Os quatro campos, separados

| conceito | responde | nesta seção |
|---|---|---|
| meta | quanto se entrega | Seção 2 — 35.000 OCI concluídas, 3 polos |
| **indicador** | como se mede | fórmula com numerador e denominador |
| **parâmetro de aferição** | qual valor conta como cumprido | limiar — **decisão pendente**, ver abaixo |
| **meio de verificação** | onde se comprova | sistema oficial, acessível ao concedente |

Contagem não é indicador. "35.000 OCI realizadas" já é a meta; repeti-la na coluna
do indicador é o defeito mais comum do gênero. Toda fórmula abaixo tem
denominador.

---

## Indicadores pactuados — com consequência contratual

| id | meta | indicador (fórmula) | parâmetro de aferição | meio de verificação | apuração |
|---|---|---|---|---|---|
| **IND-01** | 1 | OCI concluídas e **aprovadas** na competência ÷ OCI pactuadas para a competência | `[[lacuna: LC-018]]` | produção aprovada no SIA/SUS, por APAC, competência mensal | mensal |
| **IND-02** | 1 | Σ OCI concluídas até a competência ÷ 35.000 | `[[lacuna: LC-018]]` | consolidação das competências no SIA/SUS | mensal, acumulado |
| **IND-03** | 2 | polos com equipe contratada, agenda publicada no SISREG e FPO programada ÷ 3 | 3/3 — sem tolerância | documentos: contrato de equipe, extrato de agenda no SISREG, confirmação de programação da FPO | única, ao fim da pré-produção |

IND-01 mede ritmo; IND-02 mede se o atraso de uma competência foi recuperado nas
seguintes. Sozinho, o mensal pune oscilação normal; sozinho, o acumulado só
acusa o problema quando não há mais tempo de corrigir. Os dois juntos é que
sustentam a notificação no meio do caminho.

IND-03 não tem tolerância porque não faz sentido operar 2,4 polos: ou o polo está
apto ou não está. É o indicador que dá lastro à 1ª parcela.

---

## Indicadores de acompanhamento — sem consequência contratual

Medem as pontas do fluxo que a meta depende, e que a meta sozinha não distingue.
Entram no relatório mensal, subsidiam a Seção 7 e **não** geram glosa por si.

| id | indicador (fórmula) | por que existe | meio de verificação | apuração |
|---|---|---|---|---|
| **IND-04** | vagas reguladas pela SES-DF ÷ vagas ofertadas pelo executor | é a **prova da ponta do executor**: vaga ofertada e não regulada é capacidade ociosa, e a falha não é dele (DV-016) | SISREG — oferta e regulação no mesmo sistema | mensal |
| **IND-05** | comparecimentos ÷ agendamentos, apurado **separadamente** na entrada e no retorno | mede o que hoje é estimativa: os 20% vêm da entrada e foram replicados no retorno sem medição (LC-014) | SISREG + prontuário TrakCare | mensal |
| **IND-06** | faltosos que compareceram após busca ativa ÷ faltosos do período | a meta assume recuperação do faltoso até a terceira tentativa; sem este indicador a premissa fica indemonstrável | registro de contato do executor **conciliado com** o reagendamento no SISREG | mensal |
| **IND-07** | OCI com retorno em ≤ 30 dias da entrada ÷ OCI com retorno realizado na competência | o ciclo de 30 dias é parâmetro pactuado, não observação — precisa ser aferível | datas de entrada e retorno no prontuário TrakCare | mensal |
| **IND-08** | OCI com registro documental completo ÷ OCI com retorno realizado | conclusão tem duas partes, assistencial e documental; esta mede a segunda | sistemas oficiais de registro | mensal |

**IND-06 e a regra do meio de verificação.** Registro de contato do executor é
autodeclaração e não vale sozinho. Por isso o indicador se apura **conciliado com
o SISREG**: o que prova a busca ativa não é a ligação registrada, é o
reagendamento que apareceu no sistema depois dela. É a mesma lógica do corpus,
que nunca deixa o relatório do executor sem âncora em sistema oficial (AC-038).

---

## Indicadores qualitativos

Acrescentados em 2026-08-17, para atender à estrutura indicada pelo professor —
"indicadores qualitativos e quantitativos". Os oito acima medem volume, prazo e
completude; estes medem **conformidade clínica do que foi entregue**.

| id | indicador (fórmula) | por que existe | meio de verificação | apuração |
|---|---|---|---|---|
| **IND-09** | OCI com avaliação cardiológica completa e conduta definida registrada ÷ OCI concluídas na competência | mede se o pacote entregou desfecho clínico, não só presença nas duas consultas | prontuário TrakCare | mensal |
| **IND-10** | usuários com desfecho registrado — alta, seguimento ou encaminhamento — ÷ OCI concluídas na competência | a OCI é porta de entrada de uma trilha; sem desfecho o usuário volta para a fila de onde saiu | TrakCare + SISREG | mensal |
| **IND-11** | encaminhamentos realizados conforme os critérios regulatórios ÷ encaminhamentos realizados | mede se o egresso da OCI entra na fila certa, e não numa fila nova qualquer | SISREG | mensal |

**Sem consequência contratual**, como os de acompanhamento. É a mesma escolha do
corpus, que trata indicadores desse tipo como gerenciais (AC-037) — com a
diferença de que aqui isso está declarado por decisão, e não usado para esvaziar
o quadro inteiro.

**Ressalva registrada.** IND-09 a IND-11 dependem de o prontuário ter campo
estruturado para conduta e desfecho. Se o registro for texto livre, o indicador
existe no papel e não é apurável. `[[lacuna: LC-028 — confirmar se TrakCare tem
campo estruturado de conduta e desfecho]]`

---

## O parâmetro de aferição — decisão pendente

**Nenhum dos quatro planos aprovados declara limiar numérico.** O pt_ses_02, o 03
e o 04 têm uma seção chamada "Parâmetros de Aferição" que não contém parâmetro
algum: dizem que a aferição é "contínua e sistemática", com base no SISREG e no
TrackCare, e param aí (AC-036). Busca por limiar — `no mínimo N%`, `igual ou
superior a N%`, `N% da meta` — retorna **zero ocorrências nos quatro**. O
pt_ses_01 chega a listar três indicadores percentuais e em seguida os neutraliza:
declara que têm "caráter exclusivamente gerencial", sem criar obrigação (AC-037).

Aqui isso não passa, por uma razão que não é de estilo: **o desembolso é
antecipado**. Como o dinheiro entra antes da despesa, o que se discute na
prestação de contas não é quanto pagar, é **quanto devolver** — e sem limiar
escrito não há critério para decidir se houve descumprimento, nem quanto ele
custa. O limiar é o que separa oscilação normal de inadimplemento.

`[[lacuna: LC-018 — parâmetro de aferição de IND-01 e IND-02, e a consequência
de cada faixa. O proponente não dispõe do número; sai da negociação com a SES ou
da norma distrital. Encaminhado ao professor como DV-018.]]`

O que a decisão precisa fixar, e as opções que fazem sentido dado o desenho:

| | desenho | efeito |
|---|---|---|
| (a) | limiar único mensal — ex.: cumprido se ≥ X% da meta da competência | simples; pune oscilação de agenda que a competência seguinte recuperaria |
| (b) | limiar mensal com **compensação no acumulado** — abaixo do mensal não gera consequência se o acumulado (IND-02) voltar ao patamar em N competências | reconhece que a produção oscila e mantém pressão sobre o resultado; exige definir N |
| (c) | limiar só no acumulado final | não permite notificação no meio do caminho — é a armadilha que a Seção 2 evitou |

Recomendo **(b)**, coerente com IND-01 + IND-02 já estarem separados. Falta o
valor de X e de N, e a consequência de cada faixa — que é conteúdo da Seção 7.

---

## Apresentada, aprovada e o numerador do IND-01

O SIA classifica a produção em **apresentada**, **orçada** e **aprovada**.
Nenhum dos quatro planos usa esse vocabulário; busca por `glosa` retorna zero
(AC-024). A diferença não é semântica: produção apresentada e não aprovada é
atendimento feito que o sistema não reconhece — e a FPO é justamente onde isso é
barrado (AC-028, OB-009).

O IND-01 usa **produção aprovada** no numerador, por ser a única que sobrevive à
crítica do SIA. Mas o executor precisa registrar as duas, porque a diferença é o
que se discute: se a apresentada é alta e a aprovada é baixa, o problema é de
faturamento, não de assistência, e o tratamento é outro.

`[[lacuna: LC-019 — o que a prestação de contas cobra, apresentada ou aprovada, e
o destino da diferença. É DV-003, aberta ao professor.]]`

Fica ainda uma dependência prática: **quem enxerga a produção aprovada.** Se o
executor só souber o resultado da crítica pela SES, o indicador existe mas ele
não pode se antecipar. `[[lacuna: LC-020]]`, DV-017.

---

## Periodicidade, e o descompasso com o desembolso

Apuração **mensal, por competência** — a mesma unidade em que o SIA processa e em
que a Seção 8 concilia.

**A apuração é mensal; o desembolso será trimestral** (estrutura do professor,
registrada em 2026-08-17). São compatíveis: o roteiro exige que a apuração não
seja mais lenta que o desembolso, e aqui ela é três vezes mais rápida. Cada
parcela trimestral terá três competências apuradas por trás.

O que ainda não fecha: a competência do mês N não é apurável dentro do mês N. A
base é entregue, processada e criticada depois, segundo o cronograma de
fechamento da SES-DF, que ainda não foi levantado (DV-008). Consequência direta
para a Seção 6: **a parcela vinculada à competência N vence necessariamente
depois da apuração dela** — é a verificação 4 do `validador.py`, e é o defeito que
o AC-027 aponta no corpus, onde nenhum plano amarra desembolso a fechamento de
competência.

Com desembolso antecipado a ordem se inverte: a parcela vem antes, e o que vem
depois é a conciliação. O que a Seção 6 tem que garantir é que **cada parcela
tenha uma competência apurada antes da parcela seguinte** — caso contrário o
convênio acumula repasse sem lastro aferido.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-018 | Parâmetro de aferição de IND-01 e IND-02: o limiar, a janela de compensação e a consequência de cada faixa. O proponente não dispõe do número. | **DV-018, → professor** |
| LC-019 | Se a prestação de contas cobra produção apresentada ou aprovada, e o destino da diferença. | DV-003 |
| LC-020 | Se o executor tem acesso próprio ao resultado da crítica do SIA. | DV-017 |
| LC-028 | Se o TrakCare tem campo estruturado de conduta e desfecho, sem o que IND-09 a IND-11 não são apuráveis. | proponente / SES |

Nenhuma bloqueante. As fórmulas, os meios de verificação e a periodicidade estão
fechados; o que falta é o limiar e o vocabulário da conciliação.

---

## Dúvidas

- **DV-003** — apresentada ou aprovada na prestação de contas. `→ professor`
- **DV-008** — cronograma de fechamento de competência da SES-DF. `aberta`
- **DV-016** — vaga ofertada e não regulada: efeito sobre a meta. Sustenta IND-04.
- **DV-017** — acesso do executor ao resultado da crítica do SIA. `→ professor`
- **DV-018** — o limiar de aferição e a consequência de cada faixa. `→ professor`

---

## Fundamento

- **OB-008** — Portaria SAS/MS nº 768/2006: laudo emitido por profissional de
  nível superior **previamente** à realização do procedimento. É a autorização
  prévia — o "A" de APAC — e condiciona o que o IND-01 consegue contar.
  `a_verificar`.
- **OB-010** — registro da produção por APAC no SIA/SUS, com procedimento
  principal e secundários. Meio de verificação de IND-01, IND-02 e IND-08.
  `a_verificar`, ainda **sem dispositivo identificado**.
- **OB-009** — Manual Operacional da FPO: é contra ela que o SIA valida antes de
  aprovar. Sustenta a escolha de "aprovada" no numerador do IND-01.
  `a_verificar`.

Nenhuma lida no original.
