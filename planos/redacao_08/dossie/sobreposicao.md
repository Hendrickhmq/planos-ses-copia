# Sobreposição — o que já está em andamento em cardiologia no DF

**Controle interno: não vai ao documento.**

Pedido do usuário, 22/10/2026: estudar as OCI e a fila "além de projetos já em andamento para
nada se sobrepor". Consulta de 22/10/2026.

## 1. Convênios da SES-DF publicados

A página de convênios da SUCONV (`saude.df.gov.br/convenios-suconv`) lista seis. **Só um tem
cardiologia:** o **030977/2026, do IEV** (CNPJ 05.117.522/0001-91), "Fila Zero", multiespecialidades,
R$ 8.998.131,20, vigente de 29/04/2026 a 28/05/2027 (1º apostilamento). O objeto cita "OCI em
Cardiologia; OCI em Ginecologia; OCI em Oncologia; OCI em Ortopedia e; OCI em Otorrinolaringologia".

As OCI de cardiologia dele, pela planilha do plano aprovado (`estudo/normalizados/pt_ses_04/planilha.csv`,
itens 2.3.1 a 2.3.3):

| OCI | quantidade | valor no plano do IEV | valor no SIGTAP (10/2026) |
|---|---:|---:|---:|
| 09.02.01.001-8 Avaliação de Risco Cirúrgico | 4.647 | R$ 130,00 | R$ 130,00 |
| 09.02.01.006-9 Avaliação Diagnóstica - Insuficiência Cardíaca | 1.000 | R$ 250,00 | R$ 350,00 |
| 09.02.01.004-2 Progressão da Avaliação Diagnóstica I - Síndrome Coronariana Crônica | 900 | R$ 350,00 | R$ 250,00 |

O plano do IEV troca os valores da 006-9 e da 004-2 entre si, e as fichas de 10/2026 confirmam
a troca: as duas linhas somam R$ 565.000,00 no plano e dariam R$ 575.000,00 pelo SIGTAP. O caso
inteiro está em `../estudos/02_iev_fila_zero_cardiologia.md`.

Os outros cinco convênios não têm cardiologia: APAE 031636/2026 (reabilitação), ISHP 030989/2026 e
031061/2026 (oftalmologia), IEV 030975/2026 e 030976/2026 (ortopedia).

## 2. O pré-projeto do IEV

O projeto "Atenção Cardiológica em Rede" do IEV (22/12/2025,
`registros/fontes/pre_planos_20261007/iev_191061167_projeto_cardiologia.pdf`) pedia também a
**09.02.01.005-0** (progressão II, 1.000), que não entrou no plano aprovado.

## 3. Os nossos planos

Os do ISHP não têm OCI de cardiologia:
- plano 4 (redacao_04, ultrassom e tomografia): o único exame vascular é o doppler de vasos
  (02.05.01.004-0);
- redacao_07 (exames de imagem): a ecocardiografia transtorácica ficou fora por decisão do
  usuário (15/10/2026).

## 4. O que isso diz para a escolha

- **Mesma OCI, mesma fila.** As três do IEV tiram pacientes da fila de cardiologia até 05/2027.
  Para não sobrepor: preferir as OCI que o IEV não executa (002-6, 003-4, 005-0, 007-7) ou, se for
  uma das três, descontar da fila o que o IEV atende no período.
- **Limite da consulta.** Só se vê o que foi publicado. Pré-planos e pedidos de outras entidades
  em análise na ARINS não aparecem; vale perguntar à ARINS quando houver contato (P-04).
