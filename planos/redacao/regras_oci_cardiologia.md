# Regras da OCI 09.02.01.002-6 — fontes primárias

Levantado em 2026-08-17. Tudo aqui foi **lido no original**; os PDFs estão em
`normas/`. Serve como régua para as Seções 1 a 11 e substitui citação de segunda
mão.

## Fontes lidas

| doc | o que resolve |
|---|---|
| GM/MS 3.492/2024 | institui o PMAE; FNS → Fundos; PT 10.302.5118.8585 / PO 0005 FAEC |
| SAES/MS 1.640/2024 | operacionalização; habilitação 38.01; NGC; autonomia do gestor local |
| SAES/MS 1.822/2024 | inclui a OCI Cardiologia na Tabela; ficha completa do 002-6 |
| SAES/MS 2.331/2024 + retificação | procedimentos obrigatórios; idade mínima 18 |
| SAES/MS 2.630/2025 | regra 0012 — financiamento FAEC do secundário |
| SAES/MS 2.930/2025 | exclui a radiografia de tórax da obrigatoriedade |
| SAES/MS 2.747/2025, 2.799/2025, 2.723/2025, 3.200/2025 | alterações posteriores |
| GM/MS 7.701/2025 | programa renomeado "Agora Tem Especialistas" |
| NT 1/2025-DAET | **obrigatórios × opcionais** por OCI |
| NT 2/2025-DAET | metodologia do teto e **distribuição por UF** |
| NT 3/2025-DAET | PAR, habilitação, entes executores, listas de espera |
| **Manual PMAE — Registro da Produção, Controle e Avaliação** (MS, 2025) | preenchimento da APAC, validade, FPO, BPA, indicadores |

---

## 1. O que é obrigatório e o que não é

Da **NT 1/2025**, quadro "LISTA DAS OCIs SEGUNDO O PERFIL DOS COMPONENTES",
combinada com a 2.930/2025:

| | procedimento |
|---|---|
| **obrigatório** | `03.01.01.007-2` consulta médica **ou** `03.01.01.030-7` teleconsulta |
| **obrigatório** | `02.11.02.003-6` eletrocardiograma |
| opcional | `02.04.03.015-3` radiografia de tórax — era obrigatório até a 2.930/2025 |
| opcional | `02.05.01.003-2` **ecocardiografia transtorácica** |
| opcional | exames laboratoriais (14 dosagens + hemograma) |

Piso: **consulta + ECG**. Mínimo de 2 secundários (art. 7º da 2.331).

E o Ministério é explícito sobre o efeito financeiro — NT 1/2025, item 2.1.6:

> "Não há possibilidade de alterar/variar os valores das OCIs para faturamento,
> **ainda que nem todos os procedimentos sejam executados**, sendo esta
> característica uma das inovações do PMAE, saindo do modelo de pagamento por
> procedimento."

E o item 2.1.5 legitima a omissão clínica: um secundário pode não ser necessário
"por já ter sido realizado ou por não haver indicação após avaliação do médico
especialista".

**Consequência para o plano.** O ecocardiograma — que é o filtro da fila e a
justificativa clínica inteira do objeto — é **opcional**, e sua ausência não
reduz o valor. Duas coisas decorrem:

1. O pacote completo é **compromisso do plano de trabalho**, não da norma. O
   plano não pode citar a portaria como fundamento de "OCI concluída = com
   retorno" nem da entrega do eco.
2. A meta de eco **não pode ser 100%** — a norma admite não indicação clínica. O
   indicador correto é percentual com justificativa registrada para a ausência,
   não obrigatoriedade cega.

O próprio MS monitora isso: o Manual lista, entre os indicadores de controle,
"acompanhamento do rol de procedimentos secundários registrados **em relação ao
esperado clinicamente** para cada OCI". O indicador do plano espelha o federal.

---

## 2. Prazo — a regra não é 30 dias, é a competência

Atributo **054 — APAC com validade fixa de 2 competências**. O Manual PMAE dá o
exemplo oficial:

> início da validade 23/01/2025 → fim da validade **no máximo 28/02/2025**.

A validade começa na **data do primeiro procedimento** (a consulta de entrada) e
termina no **último dia da competência seguinte**. Não são 60 dias corridos:

| entrada | prazo final | janela real |
|---|---|---|
| dia 1º | último dia do mês seguinte | ~60 dias |
| dia 15 | último dia do mês seguinte | ~45 dias |
| dia 28 | último dia do mês seguinte | ~31 dias |

E a **apresentação** da APAC também tem que ocorrer dentro das 2 competências.

**Consequência.** O parâmetro "ciclo de 30 dias" protege a maior parte dos casos
mas não todos: entrada em 30/01 com retorno em 01/03 perde a APAC. A regra
operacional correta para a Seção 7 é **"o retorno ocorre até o último dia da
competência seguinte à da entrada"**, o que obriga a encurtar o ciclo para quem
entra no fim do mês. Isso é agendamento, não meta — mas tem efeito financeiro.

---

## 3. OCI não concluída — o plano está mais duro que a norma

Manual PMAE, p. 26:

> "No caso de a OCI não ser concluída [...] (por exemplo, se não forem realizados
> todos os procedimentos obrigatórios de uma OCI **ou se o prazo para conclusão
> da OCI não for cumprido**), os procedimentos eventualmente realizados
> **poderão ser registrados e apresentados em BPA-I**".

Dois efeitos:

- **O gatilho de perda da APAC é duplo**: faltar procedimento obrigatório, ou
  estourar o prazo. Faltar o *opcional* não bloqueia nada.
- A decisão registrada como "OCI iniciada e não finalizada é **custo sem
  contrapartida**" precisa ser reescrita. No SIA há recuperação residual em
  BPA-I, a valor de tabela MAC, por fora do FAEC. O que é verdade — e é o que o
  plano quer dizer — é que **não conta para a Meta 1 e não é paga pelo
  convênio**. A formulação atual afirma mais do que a norma sustenta.

---

## 4. Vedação de duplicidade — Sorocaba está certa, e agora há fonte

Manual PMAE, p. 26:

> "Os atendimentos realizados, que gerarem registro de procedimentos secundários
> em APAC de OCI, **não deverão ser registrados em duplicidade** em qualquer
> outro instrumento de registro do SIA ou do SIH".

Mais: estabelecimentos do Programa devem usar **BPA-I** para o que é de fora do
programa e **evitar BPA-C**. E há indicador federal de "percentual de registros
em BPA-C, por executor" e de "verificação de duplicidade entre secundários em
APAC, BPA-I e AIH, por CNS/CPF".

Isso valida a instrução de Sorocaba de zerar os procedimentos do atendimento —
e transforma o achado do BPA de teste em ponto de controle do plano: o executor
não pode faturar em BPA nada que já esteja como secundário na APAC.

---

## 5. Condições de partida que o plano ainda não tem

**Habilitação 38.01 — e o PAR antes dela.** NT 3/2025, item 4.1:

> "A execução das OCIs, com devido financiamento federal, pode ser iniciada
> **após a publicação da portaria de aprovação do PAR e após a habilitação dos
> estabelecimentos de saúde**".

E o Manual: o registro em APAC "só é possível por estabelecimentos de saúde com
o cadastro da habilitação devidamente realizado".

A habilitação é **descentralizada**: o gestor habilita por ato normativo próprio
e insere no CNES (art. 6º, §3º da 1.640). Boa notícia — não depende de edital
federal. Mas o estabelecimento tem de ser **integrante do PAR**, e no DF a
pactuação é por **Resolução do Colegiado de Gestão do Distrito Federal** (NT 3,
item 3.11), não CIB/CIR.

**NGC — Núcleo de Gestão do Cuidado.** Obrigatório em todo estabelecimento
executor de OCI: CNES serviço **170**, classificação **002**, equipe mínima de
pelo menos 1 profissional de nível superior (Anexo da 1.640; art. 7º). Finalidade
normativa: monitorar tempo e qualidade das OCIs e **assegurar a transição do
cuidado para a Atenção Primária**. O plano não tem NGC nem transição para a APS
— são Seção 9 e Seção 7, e são exigência, não melhoria.

**Relação de entes executores com limite orçamentário.** NT 3, item 5.1: a
relação vai ao InvestSUS "com a indicação do **limite orçamentário total de cada
um dos executores**", sem extrapolar o limite da UF (art. 9º, IV da 3.492
alterada pela 5.758/2024). O envio "é condicionante ao fluxo de validação das
OCIs e o devido pagamento correspondente".

**FPO — aba FAEC.** Manual, cap. 6: **todos** os procedimentos da OCI, principais
e secundários, devem ser programados na **aba FAEC** da FPO desde a competência
03/2025 (regra 0012 da 2.630/2025). A programação é também física. Secundário
executado fora do PMAE continua MAC, aba MAC.

Isso dimensiona a FPO do plano: não são 35.000 linhas. São 35.000 principais
**mais** os secundários — até 70.000 consultas (a compatibilidade admite qtd 2),
35.000 ECG, e o que se pactuar de eco, RX e laboratório. É a resposta operacional
a DV-004 e parte de LC-015.

---

## 6. Financiamento — LC-009 e BL-002 resolvidas por fonte

- **Art. 24 da 1.640/2024:** "As OCI serão financiadas com recursos do **FAEC**,
  mediante produção devidamente apresentada e aprovada no SIA/SUS." → LC-009
  ("FAEC ou teto MAC") está respondida: **é FAEC**, e o pagamento é por produção
  aprovada.
- **Art. 19 da 3.492/2024:** orçamento do MS, PT 10.302.5118.8585, PO 0005 FAEC.
- **Art. 18 da 3.492/2024:** o FNS transfere aos **Fundos de Saúde** estaduais,
  municipais e do DF. → é exatamente a cadeia de BL-002, agora com dispositivo:
  MS → Fundo de Saúde do DF → convênio → executor. A conclusão do plano estava
  certa; faltava a citação.

**O teto, com número.** NT 2/2025, Anexo II — distribuição per capita do PMAE por
UF, ano 2025, sobre R$ 2.400.000.000,00 nacionais:

> **Distrito Federal — população 3.094.325 — R$ 34.813.717,40**

Esse é o envelope do DF para **todo o PMAE**: cardiologia, ortopedia, oncologia,
otorrino e oftalmologia somadas. A produção do plano — 35.000 × R$ 200,00 =
R$ 7.000.000,00 — equivale a **20,1% do envelope anual inteiro do DF**,
concentrada numa única OCI e num único executor, em 9 meses.

Não inviabiliza: o convênio paga o executor com a emenda, e o teto limita o
ressarcimento FAEC ao Fundo. Mas é o número que faltava para a Seção 11 e para
DV-001 — e é grande o bastante para exigir conversa com o Grupo Condutor do PAR
antes de fechar a meta. **Ressalva:** é a distribuição de 2025; a de 2026 precisa
ser conferida.

---

## 7. Regra local — a base normativa da divergência de Sorocaba

**Art. 21, §2º da 1.640/2024:** "Os gestores locais têm autonomia para definir os
processos necessários à(s): I - autorizações prévias para realização dos
procedimentos; II - definição de regras locais para bloqueios de produção
assistencial; e III - aprovação da produção assistencial."

É o que autoriza Sorocaba a restringir CID e CBO sem contrariar a norma federal.
Consequência para o plano: **a SES-DF pode impor regras locais equivalentes** —
CID, CBO, autorização prévia, bloqueios. Isso é pergunta obrigatória ao Complexo
Regulador antes de fechar a Seção 2, porque uma restrição de CID muda a fila
elegível.

---

## 8. Correções de nomenclatura para o plano

| onde | está | deveria |
|---|---|---|
| Seção 1 | "OCI instituída pela Portaria SAES/MS 1.822/2024" | a 1.822 **inclui na Tabela**; quem institui o PMAE é a **GM/MS 3.492/2024** |
| Seção 1 | "Ofertas de Cuidado Integrado" | "Ofertas de **Cuidados** Integrados" |
| geral | "Programa Mais Acesso a Especialistas" | desde 2025 o guarda-chuva é **"Agora Tem Especialistas"** (GM/MS 7.266 e 7.701/2025); o PMAE segue como **Componente Ambulatorial**. A habilitação 38.01 mantém o nome antigo |

---

## 9. O que ficou em aberto

- **Anexos I e II da 2.630/2025 e Anexo da 2.799/2025** são tabelas em imagem —
  não extraí. Podem ter excluído compatibilidades da 002-6. Conferir no SIGTAP.
- **Anexo I da NT 2/2025** (produção física estimada por OCI e por UF) também é
  imagem. É lá que está a estimativa de OCI cardiológica para o DF — o número
  que se compara diretamente com as 35.000.
- **Distribuição 2026** do PMAE por UF: não localizada.
- **Painel Infosaúde PMAE da SES-DF** (`info.saude.df.gov.br`) existe e não foi
  aberto. Deve trazer PAR e produção do DF.
- Regra local de CID/CBO no DF: não pesquisada.
