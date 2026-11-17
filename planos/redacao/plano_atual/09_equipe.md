# Seção 9 — Equipe e estrutura física

Status: `rascunho` · Nível: **mínimo viável** (melhorias em `redacao/melhorias.md`)
Depende de: Seção 4 · Lacunas: 3 · Equipe médica: **17 a 25 cardiologistas**
Carga: ~131 consultas/polo/dia útil · 3 polos · 21 dias úteis/mês

---

## A carga que a equipe tem que suportar

Nada aqui é escolha: tudo sai da curva da Seção 2. Nos meses cheios, 4.125
entradas e 4.125 retornos por mês.

| | mês (3 polos) | mês (por polo) | dia útil (por polo) |
|---|---|---|---|
| consultas de entrada | 4.125 | 1.375 | ~65 |
| consultas de retorno | 4.125 | 1.375 | ~65 |
| **consultas, total** | **8.250** | **2.750** | **~131** |
| ecocardiogramas | 4.125 | 1.375 | ~65 |
| eletrocardiogramas | 4.125 | 1.375 | ~65 |
| radiografias de tórax | 4.125 | 1.375 | ~65 |
| coletas laboratoriais | 4.125 | 1.375 | ~65 |
| agendamentos a gerir | 10.312 | 3.437 | ~164 |
| contatos de busca ativa | ~2.062 | ~687 | ~33 |

**131 consultas por dia útil por polo** é o número que dimensiona esta seção. O
erro fácil seria dimensionar por 65 — só a entrada —, esquecendo que cada usuário
volta. Os contatos de busca ativa saem dos 20% de falta sobre os agendamentos, nos
dois pontos do fluxo.

---

## Equipe assistencial — custeada pela produção

| cargo | quantidade | carga horária | vínculo | onde é custeado |
|---|---|---|---|---|
| Médico cardiologista | **17 a 25** (6 a 8 por polo) | 8h ambulatoriais | `[[lacuna: LC-031]]` | R1 — produção |
| Médico com habilitação em ecocardiografia | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R1 — produção |
| Técnico em enfermagem | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R1 — produção |
| Técnico em radiologia | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R1 — produção |
| Profissional de coleta laboratorial | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R1 — produção |
| Responsável Técnico Assistencial (RQE) | 1 por polo | `[[lacuna]]` | `[[lacuna: LC-031]]` | R1 — produção |

**O quantitativo médico é função de uma variável que só o proponente tem:** quantas
consultas um profissional atende por dia útil. Com 393 consultas/dia úteis a
cobrir nos 3 polos:

| consultas/dia por profissional | profissionais no total | por polo |
|---|---|---|
| 16 — piso da faixa SUS ambulatorial | **~25** | ~8 |
| 20 — meio da faixa | **~20** | ~7 |
| 24 — teto da faixa SUS ambulatorial | **~17** | ~6 |
| *8,7 — parâmetro do pt_ses_04 (AC-016), descartado* | *~45* | *~15* |

**Parâmetro adotado: 16 a 24 consultas por dia útil**, em jornada ambulatorial de
8 horas, com tempo médio de 20 a 30 minutos por consulta — faixa informada pelo
proponente em 2026-08-18 para o setor público/SES-DF. Logo, **17 a 25
cardiologistas no total, 6 a 8 por polo**.

A linha em itálico é o parâmetro que o corpus oferecia e que este plano
**descarta**: 8,7 consultas por dia útil, extraído do pt_ses_04 (AC-016), exigiria
~45 profissionais e está muito abaixo da jornada ambulatorial praticada. Fica
registrado porque a diferença entre 45 e 20 é grande demais para desaparecer sem
explicação — e porque foi ele que sustentou o alerta de mobilização da Seção 11,
que agora cede.

**Proveniência.** A faixa é conhecimento do proponente, sem fonte documental. Não
é medição da operação real, e por isso o dimensionamento final ainda depende da
escala efetiva por turno.

`[[lacuna: LC-029 — escala efetiva por turno e quantitativo final por cargo]]`

**A teleconsulta de retorno é a alavanca.** Metade das 131 consultas diárias é
retorno, e o retorno admite teleconsulta (Seção 2). Isso não reduz o tempo médico,
mas reduz consultório ocupado, deslocamento do usuário e — pelo que a DV-002
aponta — o próprio não comparecimento.

---

## Equipe não assistencial — custeada pelo apoio

| cargo | quantidade | carga horária | vínculo | onde é custeado |
|---|---|---|---|---|
| Recepção e acolhimento | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R2 |
| Agendamento e gestão de agenda no SISREG | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R2 |
| Busca ativa — ~33 contatos/dia útil por polo | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R2 |
| Faturamento e registro de APAC | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R2 |
| Coordenação administrativa do projeto | `[[lacuna: LC-029]]` | `[[lacuna]]` | `[[lacuna: LC-031]]` | R2 |

A busca ativa tem posto próprio de propósito: é obrigação escrita (Seção 2), tem
indicador (IND-06) e tem volume calculável — cerca de 2.062 contatos por mês. Sem
alguém responsável por ela, vira intenção.

O faturamento também: quem registra a APAC e acompanha a crítica do SIA é quem
transforma atendimento em produção aprovada, que é o numerador do IND-01.

---

## Estrutura física, por polo

| ambiente | quantidade | observação |
|---|---|---|
| Consultórios para consulta de entrada e retorno | `[[lacuna: LC-030]]` | dimensionar por ~131 consultas/dia útil |
| Sala de ecocardiografia, com equipamento | `[[lacuna: LC-030]]` | ~65 exames/dia útil por polo — provável gargalo |
| Sala de eletrocardiografia | `[[lacuna: LC-030]]` | ~65/dia útil |
| Sala de radiologia | `[[lacuna: LC-030]]` | ~65/dia útil — verificar se o polo tem ou se o exame é referenciado |
| Posto de coleta laboratorial | `[[lacuna: LC-030]]` | ~65/dia útil |
| Recepção e sala de espera | `[[lacuna: LC-030]]` | fluxo de ~164 agendamentos/dia útil |
| Estação de teleconsulta | `[[lacuna: LC-030]]` | reduz consultório ocupado no retorno |

**O ecocardiograma é o gargalo provável.** É o exame mais demorado do pacote e o
que exige equipamento e profissional habilitado ao mesmo tempo. Sessenta e cinco
por dia útil, por polo, é o número a testar contra a capacidade real antes de
assinar. `[[lacuna: LC-030 — estrutura disponível por polo e capacidade diária de
cada ambiente]]`

Todo o material é **locado**, não adquirido (Seção 5).

---

## O espelhamento com a Seção 5 — e o limite dele

A regra é que todo cargo remunerado pelo convênio apareça na planilha, e vice-versa.
Aqui ela vale **inteira para a equipe não assistencial** — cada cargo de R2 tem
linha na planilha, e cada linha de R2 tem cargo aqui.

Para a equipe assistencial ela **não se aplica do mesmo modo**, e isso precisa
estar dito: a rubrica R1 é linha única de produção — 35.000 × R$ 200,00 —, porque
o convênio remunera o procedimento, não os insumos que o compõem. Os cargos
assistenciais existem, são custeados por R1 e estão listados nesta seção para
efeito de dimensionamento, mas não aparecem itemizados na planilha. É a estrutura
do corpus (AC-015), e é coerente com o teste de não-assistencialidade: se o
cardiologista aparecesse como item no apoio, seria incremento disfarçado.

---

## O teste que esta seção existe para fazer

O critério do roteiro é direto: se o objeto são N atendimentos e a equipe não
comporta N, um dos dois está errado. Com as lacunas abertas, o teste ainda não
pode ser feito — mas a conta que ele exige já está montada:

```
393 consultas/dia útil ÷ (consultas por profissional/dia)  =  profissionais necessários
196 ecocardiogramas/dia útil ÷ (exames por sala/dia)       =  salas de eco necessárias
```

Se o resultado da primeira linha for próximo de 45 profissionais, a Seção 11 ganha
um risco de mobilização de porte — 45 cardiologistas contratados em 2 semanas de
pré-produção é premissa forte. E se a capacidade instalada real dos 3 polos não
suportar 65 ecos por dia útil cada, quem cede é a meta, o número de polos ou a
janela — nessa ordem de preferência decrescente.

---

## Lacunas

| id | descrição | como se resolve |
|---|---|---|
| LC-029 | Produtividade real por profissional e por turno, e o quantitativo de cada cargo. | proponente |
| LC-030 | Estrutura disponível por polo e capacidade diária de cada ambiente, com atenção ao eco. | proponente |
| LC-031 | Vínculo de cada cargo — CLT, PJ, cooperativa, credenciamento. | proponente |
| LC-025 | Custo real por OCI — se R$ 200,00 cobre a assistência dimensionada aqui. | proponente, **decide a viabilidade** |

LC-025 vem da Seção 5 e reaparece aqui porque é esta seção que produz o insumo
dela: só depois de saber quantos profissionais e quantas salas é que se sabe
quanto custa uma OCI.

---

## Fundamento

- **OB-004** — Lei 8.080/90, art. 26, §2º: os serviços contratados submetem-se às
  normas técnicas e administrativas e às diretrizes do SUS, o que alcança
  qualificação profissional e responsabilidade técnica. `a_verificar`.
- **OB-007** — Portaria SAES/MS nº 1.822/2024, Anexo: define a composição do
  pacote e, com ela, quais profissionais e ambientes são indispensáveis.
  `a_verificar`, **Anexo não lido**.

Nenhuma lida no original.
