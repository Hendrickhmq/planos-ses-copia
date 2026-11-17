# Seção 12 — Justificativa

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seções 1 a 11 · Lacunas: 4
**Duas delas são de mérito, não de preenchimento.** Ver "o que ainda não se demonstra".

---

## Por que agora

A espera média por avaliação cardiológica com solicitação de ecocardiografia no
SUS/DF é de **777,28 dias** — dois anos e um mês. São **36.052 pessoas** na fila,
correspondentes a 42.632 solicitações.

| dado | valor | fonte |
|---|---|---|
| solicitações em espera | 42.632 | Mapa Social da Saúde (MPDFT), filtro ecocardiografia |
| pessoas distintas (CNS) | 36.052 | idem |
| espera média | 777,28 dias | idem |
| data de extração | **16/08/2026** | acervo DD-001 |

Dado com fonte e data, como o critério exige. Cadastrado no acervo como DD-001,
inaugurando o tipo `dado` que faltava ao schema.

Para contexto — e como advertência contra transportar número de uma fonte para
outra: uma reportagem de maio de 2024 registrava fila de 7.485 consultas de
cardiologia adulto com espera média de 147 dias (AC-018). **Os dois números não se
comparam**: aquele mede consulta adulto; este mede solicitações de ecocardiografia.
Citar os dois lado a lado como se fossem a mesma fila é erro, e por isso o plano
usa apenas o segundo (AC-020).

---

## Por que esta população

Usuários do SUS/DF **em espera regulada**, encaminhados pelo Complexo Regulador a
partir das Regiões de Saúde Norte, Sul, Oeste e Sudoeste. Não há captação, seleção
ou triagem pelo executor: quem entra é quem a regulação encaminha, na ordem que
ela define (Seção 2).

Isso importa para a justificativa por um motivo simples: **o plano não escolhe
quem atende**, e portanto não pode ser acusado de selecionar demanda de menor
complexidade — a vedação de mesclagem indevida de filas regionais está observada
por desenho (AC-030).

---

## Por que este objeto

A OCI 09.02.01.002-6 não é uma consulta: é um **pacote** — consulta especializada,
ecocardiograma, eletrocardiograma, radiografia de tórax, exames laboratoriais e
consulta ou teleconsulta de retorno, instituído pela Portaria SAES/MS nº
1.822/2024 no âmbito do Programa Mais Acesso a Especialistas.

A diferença prática, para quem espera há 777 dias, é o **itinerário**. Na oferta
fragmentada, o usuário obtém a consulta, sai com pedido de exame, volta para a
fila do exame, e depois para a fila do retorno — três esperas encadeadas. Na OCI,
o itinerário inteiro se resolve em duas visitas, com prazo pactuado de **até 30
dias** entre elas (Seção 2).

É também por isso que a meta é de OCI **concluída** e não de atendimento
realizado: entregar a primeira consulta e devolver o usuário à fila do exame
reproduziria exatamente o problema que o objeto existe para resolver.

---

## Por que este tamanho — o dimensionamento

Este é o item que o roteiro cobra e que a maioria dos planos não responde:
explicar por que existe demanda não explica por que a meta é 35.000.

```
36.052 pessoas na fila
   └─ 20% de absenteísmo estimado (parâmetro do pt_ses_01, AC-022)
   └─ com reagendamento e busca ativa, até a 3ª tentativa
        1ª rodada: 36.052 agendados → 28.842 comparecem
        2ª rodada:  7.210 agendados →  5.768 comparecem
        3ª rodada:  1.442 agendados →  1.154 comparecem
                                      ─────────────────
                                      35.764 comparecimentos possíveis
   └─ meta pactuada: 35.000
```

**A meta é o rendimento operacional da fila, não um número escolhido.** E a
composição financeira é consequência dele, não causa: 35.000 × R$ 200,00 =
R$ 7.000.000,00, que são 70% do valor global — os 30% restantes custeiam o apoio
não assistencial, item a item, pelo teste da Seção 5.

**A ordem importa e está declarada:** a fila definiu a meta, a meta definiu a
rubrica de produção. Não o contrário. Um plano em que o valor vem primeiro e a
meta é ajustada para caber nele produz exatamente a justificativa que o roteiro
adverte — bem escrita e desligada do resto.

**E a honestidade da conta exige dizer o desconforto dela:** 35.000 sobre 36.052 é
**97,1% da fila**. Isso pressupõe que quase toda pessoa em espera compareça duas
vezes, com busca ativa insistente. É premissa agressiva, está classificada como
risco alto (R-03, Seção 11) e depende de um dado ainda não levantado — o fluxo de
novas solicitações que entra na fila durante a vigência (DV-015). Se esse fluxo
for relevante, o denominador cresce e a meta deixa de exigir conversão quase
total.

---

## Por que três polos, e por que 10 meses

**Três polos**, com meta dividida por média aritmética — 11.667, 11.667 e 11.666 —
e distribuição declarada como estimativa referencial, ajustável pela dinâmica das
filas no SISREG sem alteração do quantitativo global (AC-021, AC-030). O
refinamento por capacidade instalada e população é melhoria registrada, não
promessa desta versão (M-15).

**Dez meses**: 2 semanas de pré-produção, entradas até o mês 9 e conclusões até o
mês 10. A vigência é maior que a janela assistencial porque a OCI só fecha no
retorno — quem entra no mês 9 conclui no mês 10. É a mesma lógica que três dos
quatro planos aprovados adotam ao declarar vigência um mês maior que o período de
atendimento (AC-035).

---

## O que esta justificativa ainda não demonstra

Duas exigências de mérito, ambas em aberto. Nenhuma se resolve escrevendo melhor.

**1 · A insuficiência da rede própria.** A Lei nº 8.080/1990, art. 24, admite o
recurso a serviços privados quando as disponibilidades do SUS forem insuficientes
para garantir a cobertura assistencial (OB-002). **Fila comprova demanda; não
comprova insuficiência.** Para satisfazer o dispositivo é preciso demonstrar o que
a rede própria da SES-DF consegue produzir em avaliação cardiológica e
ecocardiografia, e o quanto disso fica descoberto.
`[[lacuna: LC-041 — capacidade instalada própria da SES-DF e o déficit
resultante]]`

Enquanto isso não existir, esta seção justifica a **necessidade** e não a
**complementaridade** — que é o fundamento constitucional do instrumento.

**2 · A ancoragem no planejamento vigente.** O roteiro exige vínculo com
instrumento de planejamento — Plano Distrital de Saúde e Programação Anual de
Saúde. Nenhum dos dois foi consultado.
`[[lacuna: LC-042 — diretriz, objetivo e meta do PDS 2024–2027 e da PAS vigente
em que este objeto se ancora]]`, DV-024.

---

## Economicidade

O mesmo pacote de procedimentos é remunerado no DF entre R$ 410,00 e R$ 560,00
pelos convênios de saúde com base na CBHPM, e entre R$ 810,00 e R$ 1.370,00 no
particular. A OCI paga **R$ 200,00** — de 36% a 49% do valor praticado pelos
convênios (DD-002, Seção 5).

O argumento é de economicidade, não de qualidade: o SUS contrata o mesmo
itinerário diagnóstico por menos da metade do preço de mercado. A ressalva
metodológica está na Seção 5 e vale repetir aqui — **isto compara remuneração,
não custo**, e não demonstra por si que o valor cobre a execução.

---

## Nota de método

Esta seção foi escrita **por último**, depois das onze anteriores, e não usa
nenhum número que já não estivesse em outra seção. Todos os valores citados aqui
são rastreáveis: a fila e a espera vêm da Seção 1, o rendimento e a meta da Seção
2, os polos da Seção 2, a vigência das Seções 2 e 4, a composição financeira da
Seção 5, o risco de conversão da Seção 11.

O registro é deliberado. A armadilha nomeada no roteiro é a justificativa ser a
única seção bem escrita do plano — sinal de que o resto foi preenchido para caber
num valor já decidido. Aqui ela é a última, é a mais dependente e não introduz
fato novo.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-041 | Capacidade instalada própria da SES-DF e o déficit resultante. **Mérito.** | SES-DF / Complexo Regulador |
| LC-042 | Diretriz, objetivo e meta do PDS 2024–2027 e da PAS em que o objeto se ancora. **Mérito.** | DV-024 |
| LC-016 | Fluxo de novas solicitações entrando na fila — alivia os 97,1%. | DV-015 |

---

## Fundamento

- **OB-002** — Lei nº 8.080/1990, art. 24: serviços privados apenas quando as
  disponibilidades do SUS forem insuficientes. É o dispositivo que LC-041 atende,
  e o mais exigente desta seção. `a_verificar`.
- **OB-001** — CF/1988, art. 199, §1º: participação **complementar**. A palavra
  complementar é o que transforma LC-041 de conveniência em requisito.
  `a_verificar`.
- **OB-007** — Portaria SAES/MS nº 1.822/2024: institui a OCI e sustenta o
  argumento do itinerário integrado. `a_verificar`, **Anexo não lido**.

Nenhuma lida no original.
