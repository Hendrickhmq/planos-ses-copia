# melhorias.md — o que ficou de fora do mínimo viável

O `plano_atual/` é deliberadamente **mínimo viável**: faz o que os quatro planos
aprovados fazem, nada além. Este arquivo guarda o que seria melhor, para não se
perder e para não contaminar o primeiro rascunho.

Cada item traz: o que o corpus faz, o que seria melhor, o que custa fazer.

Quando o `criterios.md` for escrito, **este arquivo é a matéria-prima do eixo 2**
— o que é boa prática, inclusive quando nenhum dos quatro planos faz.

---

## M-01 · Declarar a fonte do recurso · Seção 13

**Corpus:** nenhum dos quatro declara. Zero menção a emenda, dotação, programa de
trabalho, natureza ou elemento de despesa (AC-011). Dizem quanto custa e não
dizem de onde vem.

**Melhor:** declarar a emenda, o exercício, o programa de trabalho e a natureza
de despesa. Quem analisa não precisa buscar no processo, e a vinculação
orçamentária fica auditável no próprio plano.

**Custo:** baixo. Um parágrafo, desde que os dados existam.

---

## M-02 · Resolver o duplo pagamento FAEC × convênio · Seções 1, 5 e 8

**Corpus:** nenhum enfrenta (AC-012). Afirmam financiamento via FAEC com registro
por APAC e, ao mesmo tempo, remuneram a produção pelo convênio, sem dizer como
não se paga duas vezes.

**Melhor:** escrever o mecanismo — não a afirmação de que não ocorre. Se a
produção é faturada, a rotina de conciliação competência a competência; se não é,
o controle que garante o não-faturamento.

**Custo:** alto, e depende de BL-002. É a melhoria de maior valor do arquivo:
resolve a única questão que derruba um plano deste tipo e que nenhum aprovado
responde.

---

## M-03 · Conferir código SIGTAP contra a tabela oficial · todas as seções

**Corpus:** o pt_ses_04, aprovado, tem rótulo e código divergentes em duas de três
linhas de cardiologia (AC-017). Passou.

**Melhor:** conferência de todo código citado contra a SIGTAP vigente, com
registro da competência consultada. A verificação 5 do `validador.py` deve
comparar contra a tabela, não só entre seções do documento.

**Custo:** baixo, e mecanizável.

---

## M-04 · Critério de inclusão por segmento da fila · Seções 2, 7 e 11

**Corpus:** ninguém segmenta. A fila entra como bloco.

**Melhor:** a OCI de entrada só se aplica a quem ainda **não** foi avaliado.
Inscrever quem já foi avaliado e espera só o exame é faturar consulta e retorno
que a pessoa não precisa — superfaturamento sem má-fé, e o caminho natural de
quem precisa bater meta (AC-019). Escrever o critério de inclusão **e** o
mecanismo que o verifica.

**Custo:** médio. Exige a fila segmentada, que só o Complexo Regulador produz.

---

## M-05 · Meta pactuada com apuração intermediária · Seções 2 e 3

**Corpus:** metas com prazo global; apuração concentrada.

**Melhor:** meta com marcos intermediários, para que o descumprimento apareça no
3º mês e não no 9º. Plano de 9 meses cuja primeira aferição real é no fim não tem
como ser corrigido a tempo.

**Custo:** baixo.

---

## M-06 · Justificar o dimensionamento, não só a necessidade · Seção 12

**Corpus:** justificativas descrevem a necessidade e não explicam por que a meta é
aquele número.

**Melhor:** amarrar a meta à fila com o dado, a data de extração e a unidade —
aqui, 36.052 CNS com 777 dias de espera. Este plano já faz isso por construção; o
ponto é não perder na redação final.

**Custo:** zero. Já está feito.

---

## M-07 · Consequência escrita do descumprimento · Seção 7

**Corpus:** monitoramento descreve o envio de relatório, não a análise dele nem o
que acontece se a meta não bater.

**Melhor:** glosa, retenção, notificação e prazo de recuperação, com quem decide
e em quanto tempo.

**Custo:** médio. Toca a minuta do convênio, não só o plano.

---

## M-08 · Prestação de contas física, não só financeira · Seção 8

**Corpus:** comprovação centrada em despesa. Nota fiscal prova gasto, não prova
entrega.

**Melhor:** vincular despesa a item da planilha **e** a produção registrada, com
a APAC como lastro físico.

**Custo:** baixo, e casa com M-02.

---

## M-09 · Risco específico do objeto · Seção 11

**Corpus:** matriz genérica, que serviria para qualquer convênio.

**Melhor:** riscos que mencionam a OCI, a fila e o modelo de pagamento —
absenteísmo em fila de 777 dias, cadastro desatualizado, devolução de solicitação
pelo regulador, indisponibilidade de ecocardiografista.

**Custo:** baixo.

---

## M-11 · Base do repasse: produção aprovada, não apresentada · Seções 3, 6 e 8

**Corpus:** nenhum dos quatro distingue os três estados da produção no SIA —
**apresentada**, **orçada** e **aprovada**. Busca por `glosa`, `produção
aprovada`, `produção apresentada`, `rejeitado`: zero ocorrências (AC-024).

**Melhor:** dizer qual estado é a base do repasse, e a rotina quando produção
apresentada não vira aprovada. Pagar por apresentada é pagar por produção que
pode ser rejeitada na crítica.

**Custo:** baixo de escrever, médio de operar — exige conciliação por competência.

---

## M-12 · FPO como pré-requisito de execução · Seções 4, 6 e 11

**Corpus:** nenhum menciona FPO, GEPI, RAAS ou fechamento de competência (AC-026,
AC-027).

**Melhor:** a FPO do estabelecimento é programada **a partir do que foi pactuado
em convênio** — "somente os procedimentos que foram pactuados mediante
contrato/convênio com o gestor, com seu quantitativo correspondente" (AC-028).
Logo:

- A **meta do plano vira o teto de faturamento** do executor. Produção acima do
  programado é apresentada e não aprovada.
- A FPO informa limite **separado por MAC e por FAEC** — é onde se verifica como
  a OCI está custeada.
- A FPO admite **valores a maior** sobre a Tabela SUS. Pagar só o valor de tabela
  é escolha do gestor, e por isso precisa estar escrita, não presumida.

O plano deveria trazer: etapa preliminar de habilitação do CNES e programação da
FPO antes do início da produção; parcelas amarradas ao calendário de fechamento
de competência; e risco de glosa por FPO insuficiente, com mitigação.

**Custo:** baixo de escrever. É a melhoria de melhor relação custo/benefício do
arquivo — evita o modo de falha em que o plano executa e não fatura.

---

## M-13 · Risco nomeado de indisponibilidade de sistema · Seção 11

**Corpus:** matriz genérica; nenhum risco menciona os sistemas de que a execução
depende.

**Melhor:** a produção depende de SISREG, TrakCare e do envio da APAC. O TrakCare
tem histórico público de indisponibilidade total e de disputa contratual com o
fornecedor. Risco específico, verificável, com plano de contingência de registro.

**Custo:** baixo.

---

## M-10 · Não reaproveitar texto entre planos · todo o documento

**Corpus:** pt_ses_02, 03 e 04 repetem parágrafos idênticos, inclusive o mesmo
"2.600 exames cardiológicos", entre objetos diferentes (AC-013).

**Melhor:** óbvio, e listado porque é o vício mais fácil de herdar ao usar o
corpus como referência.

**Custo:** zero. É disciplina.

---

## M-14 · Busca ativa do faltoso como meta pactuada · Seções 2, 3 e 7

**Corpus:** o pt_ses_01 é o único que trata absenteísmo como variável de
dimensionamento (AC-022), e mesmo ele resolve pela oferta — vagas a mais para
compensar a perda. Nenhum dos quatro pactua o que se faz com o usuário que
faltou.

**Melhor:** transformar a busca ativa em meta com indicador próprio — percentual
de faltosos contatados em até N dias, percentual de reagendados, percentual de
reagendados que comparecem. A SES-DF fornece os dados de contato dos pacientes
regulados, então o insumo existe e o resultado é auditável.

**Por que importa mais aqui do que no corpus:** neste plano não há meia OCI. O
usuário que faz a consulta de entrada e some no retorno consome custo e não gera
receita nenhuma. Oferta a mais compensa quem nunca veio; só a busca ativa
recupera quem já entrou no pacote — e é justamente essa a perda cara.

**Custo:** médio. Exige rotina de contato registrada e um campo de desfecho por
usuário faltoso. O mínimo viável fica com a busca ativa descrita no texto, sem
meta e sem indicador.

---

## M-15 · Distribuir a meta por capacidade e população, não por média · Seção 2

**Corpus:** o pt_ses_01 distribui a meta entre polos pelo volume histórico de
demanda por Região de Saúde, com isonomia de acesso declarada como objetivo
(AC-021). É o melhor método do corpus.

**Rascunho atual:** média aritmética — 11.667, 11.667 e 11.666. Divide igual
porque o dado por região ainda não chegou.

**Melhor:** ponderar por capacidade instalada de cada polo, população da região
de referência e volume de fila. A chave do pt_ses_01 mostra a distorção que a
média ignora: Sudoeste + Oeste concentra 49% da demanda.

**Custo:** baixo depois que a fila por Região de Saúde chegar. Enquanto não
chegar, a média é honesta e a cláusula de ajuste pelo SISREG a protege.

---

## M-16 · Vigência de 10 meses — INCORPORADA AO PLANO em 2026-08-17 · Seções 2, 4 e 13

**Corpus:** três dos quatro planos declaram vigência um mês maior que o período
assistencial — 16 para 15, 13 para 12 (AC-035) — e abrem com pré-produção de 2
semanas (AC-034). O corpus compra o tempo de partida esticando a vigência.

**Rascunho atual:** vigência de 9 meses travada, com o mês de implantação saindo
de dentro dela. A janela assistencial cai para 8 meses e o ritmo sobe de 4.375
para 5.000 entradas/mês — 833 a mais por mês, todo mês.

**Melhor:** pedir 10 meses de vigência, sendo o mês 1 de pré-produção e 9 de
assistência. Alinha com a prática do corpus, devolve o ritmo ao patamar
dimensionado e não muda meta, valor nem objeto.

**Custo:** nenhum no papel; depende de o prazo da emenda e do processo
comportarem 10 meses.

**Decisão (2026-08-17):** adotada, com pré-produção de 2 semanas em vez de 1 mês.
Deixou de ser melhoria e virou desenho do plano — entradas caem de 5.000 para
4.125/mês e a carga por polo de ~159 para ~131 consultas/dia útil. Mantida aqui
como registro da origem da decisão.

---

## M-17 · Proteção do dado pessoal no relatório mensal · Seções 7 e 8

**Corpus:** os planos 02, 03 e 04 preveem relatório mensal com "relação analítica
de pacientes atendidos, com telefone e datas de procedimentos" (AC-038). Nenhum
diz como esse dado trafega, quem o acessa, por quanto tempo é retido ou o que
acontece com ele ao fim do convênio.

**Neste plano o volume é maior:** além do relatório, o executor recebe da SES-DF
os dados de contato dos faltosos para a busca ativa — que é obrigação escrita, não
cortesia. São dados de saúde de até 36 mil pessoas, em posse de entidade privada.

**Melhor:** declarar a base legal do tratamento, o canal de transmissão, quem tem
acesso, o prazo de retenção e a destinação dos dados ao término do convênio.

**Custo:** baixo no papel, real na operação. Fora do mínimo viável porque nenhum
dos quatro aprovados faz — mas é o item deste arquivo com maior chance de virar
exigência antes dos outros.

---

## M-17 · Itemizar a rubrica de produção por despesa · Seções 5, 8 e 9

**Corpus:** o pt_ses_01 traz a produção como linha única — 36.000 × R$ 160,00 —
sem itemizar o que ela custeia (AC-015). Os quatro fazem igual.

**Rascunho atual:** mesma coisa. R1 é uma linha, 35.000 × R$ 200,00.

**A alternativa, se a prestação de contas exigir despesa comprovada:** itemizar R1
por natureza de gasto — médico cardiologista, médico ecocardiografista, técnicos de
enfermagem, radiologia e coleta, responsável técnico, exames laboratoriais
terceirizados, locação de ecocardiógrafo, eletrocardiógrafo e equipamento de
radiologia, insumos assistenciais. Quantidades e frequências já estão calculadas na
Seção 9 e na Seção 2; faltariam apenas os valores unitários.

**Vantagem colateral:** resolve onde mora o **equipamento médico**. Hoje ele não
cabe no apoio, porque o teste de não-assistencialidade o proíbe, e não aparece em
R1, porque R1 não é itemizada. Com R1 itemizada, ele tem lugar próprio.

**Custo:** alto, e não é de trabalho — é de argumento. Itemizar a produção expõe a
composição de custo do procedimento, que é justamente o que a remuneração por
tabela dispensa, e desmonta o "sem incremento" da Seção 1.

**Gatilho:** só entra se a DV-023 reformulada responder que a comprovação de R1 é
por documento fiscal vinculado a item da planilha. Enquanto a produção aprovada no
SIA/SUS bastar como lastro, fica fora.
