# Seção 11 — Riscos

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seções 4 e 5 · Lacunas: 1
14 riscos · 8 classificados como altos · 3 categorias

---

## Critério de classificação — escrito, não implícito

Matriz genérica serviria para qualquer convênio. Estes critérios são deste plano:
os limiares de impacto estão em OCI e em reais **deste objeto**.

**Probabilidade**

| grau | critério |
|---|---|
| **alta** | depende de ato de terceiro sem prazo definido, ou já ocorreu em plano do corpus |
| **média** | depende de premissa adotada e não medida |
| **baixa** | depende de evento sob controle direto do executor |

**Impacto**

| grau | critério |
|---|---|
| **alto** | compromete ≥ 3.500 OCI (10% da meta), ou ≥ R$ 1.000.000, ou gera obrigação de devolução |
| **médio** | compromete entre 875 e 3.500 OCI (2,5% a 10%), ou entre R$ 250.000 e R$ 1.000.000 |
| **baixo** | compromete menos de 875 OCI, ou menos de R$ 250.000 |

Os limiares são **convenção declarada** desta análise, não pactuação com o
concedente — o limiar contratual é outro e está em LC-018.

---

## Matriz P × I

| | impacto baixo | impacto médio | impacto alto |
|---|---|---|---|
| **prob. alta** | | R-12 | **R-01 · R-03 · R-06** |
| **prob. média** | R-10 | R-09 · R-13 | **R-02 · R-04 · R-05 · R-07 · R-08 · R-11** |
| **prob. baixa** | | | R-14 |

---

## Quadro de riscos

| id | risco | etapa | categoria | P | I | classe |
|---|---|---|---|---|---|---|
| **R-01** | FPO não programada e acessos não habilitados nas 2 semanas de pré-produção | 1 | execução | alta | alto | **alto** |
| **R-02** | Vagas ofertadas e não preenchidas pela regulação da SES-DF | 2 | execução | média | alto | **alto** |
| **R-03** | A meta exige converter 97,1% da fila; a conversão real fica abaixo | 2 | execução | alta | alto | **alto** |
| **R-04** | Não comparecimento no retorno acima dos 20% adotados | 2 | execução | média | alto | **alto** |
| **R-05** | R$ 200,00 não cobrir o custo assistencial real da OCI | 2 | financiamento | média | alto | **alto** |
| **R-06** | Não mobilizar a equipe assistencial em 2 semanas | 1 | execução | alta | alto | **alto** |
| **R-07** | Capacidade de ecocardiografia insuficiente para ~65/polo/dia útil | 2 | execução | média | alto | **alto** — premissa do proponente: os polos suportam |
| **R-08** | Produção aquém do repassado, gerando obrigação de devolver | 3 | financiamento | média | alto | **alto** |
| **R-09** | Produção apresentada e não aprovada na crítica do SIA | 2 | regulatório | média | médio | médio |
| **R-10** | Produção acima da meta, não remunerada por ser a meta o teto da FPO | 2 | regulatório | média | baixo | baixo |
| **R-11** | Registro documental incompleto: OCI concluída e administrativamente inexistente | 2 | regulatório | média | alto | **alto** |
| **R-12** | Atraso no fechamento de competência e na entrega de bases | 3 | financiamento | alta | médio | médio |
| **R-13** | Indisponibilidade de SISREG, TrakCare ou SIA/SUS | 2 | execução | média | médio | médio |
| **R-14** | Instrumento questionado — convênio em vez de outro regime | — | regulatório | baixa | alto | alto |

Cobertura das três categorias exigidas: **execução** (R-01 a R-04, R-06, R-07,
R-13), **financiamento** (R-05, R-08, R-12) e **regulatório** (R-09 a R-11, R-14).

---

## Os riscos altos, com mitigação, responsável e gatilho

Todo risco alto tem ação **e** responsável. O gatilho diz qual indicador da Seção 3
acusa o risco antes de ele virar prejuízo.

### R-01 · Partida travada — FPO e acessos

**Por quê.** A curva assume 2 semanas para programar a FPO e habilitar SISREG e
TrakCare. Nenhum dos dois é ato do executor, e nenhum tem prazo conhecido
(LC-015, LC-021). Cada quinzena perdida custa ~240 entradas a mais por mês em
todos os meses seguintes.

**Mitigação.** Solicitar FPO e acessos na assinatura, não na partida; fixar prazo
para os atos da concedente no próprio instrumento; iniciar 1.1, 1.2 e 1.5 em
paralelo, sem esperar 1.3 e 1.4.
**Responsável.** Coordenação do Projeto aciona; concedente executa.
**Gatilho.** IND-03 — 3/3 ao fim da 2ª semana. Menos que isso, a curva desloca.

### R-02 · Vaga ofertada e não regulada

**Por quê.** O executor oferta; quem preenche é o Complexo Regulador. Vaga vazia é
capacidade instalada paga e ociosa, e a causa não é dele.

**Mitigação.** Registrar a oferta mês a mês no SISREG como prova documental;
comunicar formalmente ao concedente a partir da primeira competência com
preenchimento abaixo do ofertado; **pactuar no instrumento o efeito da
sub-regulação sobre a meta** — que é a DV-016, ainda aberta.
**Responsável.** Coordenação do Projeto registra e comunica; concedente responde.
**Gatilho.** IND-04, com a leitura cruzada de IND-01 da Seção 7.

### R-03 · A meta é 97,1% da fila

**Por quê.** 35.000 OCI concluídas sobre 36.052 CNS exige que quase toda a fila
compareça duas vezes. É a premissa mais agressiva do plano.

**Mitigação.** Busca ativa como obrigação, não esforço; teleconsulta de retorno;
levantar o fluxo de novas solicitações e a ordem de encaminhamento (DV-015), que
é o que amplia o denominador.
**Responsável.** Coordenação do Projeto; concedente fornece os dados de contato.
**Gatilho.** IND-02 — se o acumulado descolar da curva por duas competências, a
premissa está errada e o dimensionamento precisa ser revisto, não apenas cobrado.

### R-04 · Falta no retorno acima de 20%

**Por quê.** Os 20% foram medidos na entrada e replicados no retorno sem medição
(LC-014). Falta no retorno custa o **pacote inteiro**, não metade.

**Mitigação.** Agendar o retorno já na consulta de entrada; priorizar OCI em
andamento sobre entrada nova; teleconsulta; busca ativa reiterada.
**Responsável.** Coordenação do Projeto.
**Gatilho.** IND-05, apurado separadamente na entrada e no retorno — é a primeira
medição real desse parâmetro.

### R-05 · R$ 200,00 não cobrir o custo

**Por quê.** O pacote tem duas consultas, ecocardiograma, eletrocardiograma,
radiografia e laboratório. Se o custo real superar o valor de tabela, **a rubrica
de apoio não pode cobrir a diferença** — seria o incremento disfarçado que o teste
da Seção 5 proíbe.

**Mitigação.** Apurar o custo unitário real **antes** de assinar (LC-025). Não há
mitigação depois: é o único risco desta lista que não se administra em execução.
**Responsável.** Proponente, na decisão de aderir.
**Gatilho.** Nenhum indicador acusa — por isso a apuração é prévia.

### R-06 · Mobilizar a equipe em 2 semanas

**Por quê.** O plano exige de 17 a 25 cardiologistas, 6 a 8 por polo, contratados
dentro das 2 semanas de pré-produção (Seção 9).

**Revisto em 2026-08-18, para baixo.** A estimativa anterior — ~45 profissionais —
vinha do parâmetro do pt_ses_04 (8,7 consultas/dia útil), descartado por estar
muito abaixo da jornada ambulatorial praticada. Com 16 a 24 consultas/dia, o
número cai quase pela metade. O risco continua alto pelo **prazo**, não mais pela
escala.

**Mitigação.** Iniciar seleção antes da assinatura; escalonar a entrada em
operação dos polos dentro da própria Etapa 1; ter cadastro reserva.
**Responsável.** Coordenação do Projeto.
**Gatilho.** IND-03.

### R-07 · Gargalo do ecocardiograma

**Por quê.** ~65 exames por polo por dia útil, com equipamento e profissional
habilitado ao mesmo tempo. É o item mais provável de não escalar.

**Mitigação.** Verificar capacidade instalada por polo antes de assinar (LC-030);
dimensionar salas e turnos pelo pico, não pela média; considerar redistribuição
entre polos, que a cláusula de ajuste do SISREG permite sem alterar o global.
**Responsável.** Coordenação do Projeto e Responsável Técnico Assistencial.
**Gatilho.** IND-07 — ciclo acima de 30 dias é o primeiro sintoma de fila interna
de exame.

### R-08 · Devolução

**Por quê.** O desembolso é antecipado. Produção aprovada abaixo do repassado vira
obrigação de devolver — o risco migrou do repasse para a devolução.

**Mitigação.** Escada de consequências da Seção 7, que permite corrigir antes do
encerramento; conciliação mensal de apresentada contra aprovada; limiar e janela
de compensação pactuados (LC-018).
**Responsável.** Coordenação do Projeto; concedente decide.
**Gatilho.** IND-01 e IND-02, competência a competência.

### R-11 · Registro documental incompleto

**Por quê.** A OCI só está concluída quando os formulários sobem. Sem registro,
ela é clinicamente concluída e administrativamente inexistente: não conta, não
concilia, não paga.

**Mitigação.** Posto de faturamento e registro de APAC com responsável nomeado
(Seção 9); conferência entre retornos realizados e OCI registradas na mesma
competência.
**Responsável.** Coordenação do Projeto.
**Gatilho.** IND-08 — a diferença entre retornos realizados e registros completos
é o tamanho exato do risco materializado.

### R-14 · Questionamento do instrumento

**Por quê.** A escolha do convênio é premissa do exercício, apoiada na prática
atual da SES-DF (BL-001). Premissa, não certeza — e a situação da secretaria pode
mudar.

**Mitigação.** Fundamentar a Seção 13 na camada distrital e no art. 199, §1º da CF,
com as normas conferidas no original antes de citar.
**Responsável.** Proponente, com assessoria jurídica.
**Gatilho.** Nenhum indicador — é risco de análise, não de execução.

---

## Riscos que este plano não corre, por decisão

Registrado porque seção de riscos boa também diz o que foi eliminado no desenho:

- **Duplo pagamento FAEC × convênio** — o fluxo é cadeia, não duplicidade: o
  executor é remunerado uma vez, pelo convênio (BL-002).
- **Destinação de bem permanente ao fim do convênio** — todo o apoio material é
  locado, não adquirido (Seção 5).
- **Inadimplência de contrapartida** — não há contrapartida (Seção 10).
- **Seleção de demanda** — o executor não capta nem escolhe usuário; toda entrada
  vem da regulação (Seção 2).

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-038 | Classificação de R-05 e R-07 depende de dados que ainda não existem: a probabilidade atribuída é provisória e cai — ou sobe — quando LC-025 e LC-030 chegarem. | proponente |

---

## Fundamento

> ⚠️ **BL-003, aberta em 2026-08-17.** O Decreto DF nº 37.843/2016 é decreto de
> parceria (MROSC), e este plano o usa como camada distrital de um **convênio**.
> Enquanto BL-003 não se resolver, OB-006 é fundamento **em disputa**: o argumento
> do desembolso antecipado segue de pé pela prática do corpus (AC-032), mas pode
> perder o dispositivo. Ver `estado.yaml` e DV-025.


- **OB-006** — Decreto DF nº 37.843/2016, art. 33: liberação conforme cronograma
  de desembolso. Sustenta R-08, que é risco de devolução e não de repasse.
  `a_verificar`, conhecido por citação no corpus (AC-010).
- **OB-009** — Manual Operacional da FPO. Sustenta R-01, R-09 e R-10.
  `a_verificar`.

Nenhuma lida no original.
