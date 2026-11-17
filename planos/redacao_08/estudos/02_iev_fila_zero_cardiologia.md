# IEV, Fila Zero — o que ele faz em cardiologia e o erro de valores no plano

**Estudo interno.** Montado em 22/10/2026 com o plano aprovado (`estudo/normalizados/pt_ses_04/`),
o primeiro plano detalhado e o projeto do IEV (`registros/fontes/pre_planos_20261007/`) e as fichas do
SIGTAP de 10/2026 (`../dados/fontes/`).

## 1. O projeto

| | |
|---|---|
| entidade | Instituto Esporte e Vida (IEV), CNPJ 05.117.522/0001-91, Sobradinho/DF |
| convênio | **030977/2026**, "Fila Zero", OCI de várias especialidades (cardiologia, ginecologia, oncologia, ortopedia e otorrino) |
| processo SEI | 00060-00003072/2026-32 |
| valor | R$ 8.998.131,20 |
| vigência | 29/04/2026 a 28/05/2027 (1º apostilamento) |
| onde executa | 3 unidades de atendimento; o IEV é consultório isolado no CNES e executa em clínicas de terceiros, o que o MPCDF chamou de quarteirização (CT-002) |

**A linha do tempo da cardiologia:**
1. **22/12/2025 — o projeto "Atenção Cardiológica em Rede"** (SEI 191061167, 6 páginas): 4.647 da
   001-8, 900 da 004-2, 1.000 da 005-0 e 1.000 da 006-9.
2. **09/02/2026 — o primeiro plano detalhado** (SEI 194448359): a 005-0 sai; ficam três OCI.
3. **29/04/2026 — o plano aprovado** (`pt_ses_04`): as mesmas três, com as quantidades corrigidas
   e os valores ainda trocados (seção 3).

## 2. O que ele faz e quanto

| OCI | quantidade no plano | meta a cada 2 meses | começo e fim das metas |
|---|---:|---:|---|
| 001-8 Avaliação de Risco Cirúrgico | 4.647 | 775 | 25/07/2026 a 25/05/2027 |
| 004-2 Síndrome Coronariana, progressão I | 900 | 150 | idem |
| 006-9 Insuficiência Cardíaca | 1.000 | 167 | idem |
| **total** | **6.547** | | |

O plano diz que são cerca de 546 consultas por mês, com 3 cardiologistas nas 3 unidades e mais
1 cardiologista para o eco de estresse. O laboratório vai a "serviço especializado contratado".

**A demanda que ele disse atender.** O plano do IEV **não cita o tamanho da fila** de
cardiologia: as quantidades são a oferta dele, não a fila. A fila vem da nossa coleta no Mapa
Social (`../dados/fontes/mapa_social_20261022.md`, base de 22/10/2026 08:32).

**A fila contra a oferta do IEV:**

| OCI | pessoas na fila pelo CID da ficha | espera média | o IEV oferece até 05/2027 |
|---|---:|---:|---:|
| 001-8 Risco Cirúrgico | 442 (e 10.041 na consulta de risco cirúrgico sem recorte de CID) | 660 dias (435 na consulta sem recorte) | 4.647 |
| 002-6 Avaliação Cardiológica | 504 | 587 dias | 0 |
| 003-4 Síndrome Coronariana, inicial | 29.111 | 513 dias | 0 |
| 004-2 Síndrome Coronariana, progressão I | 2.119 | 388 dias | 900 |
| 005-0 Síndrome Coronariana, progressão II | 3.413 | 334 dias | 0 |
| 006-9 Insuficiência Cardíaca | 50.317 | 1.002 dias | 1.000 |
| 007-7 Gestão do Pré-operatório | 132 | 250 dias | 0 |

Três leituras:
- **Na 006-9, o IEV atende 2% da fila.** São 1.000 de 50.317 pessoas. A 003-4 e a 006-9 dividem
  quase as mesmas pessoas (28.929 nas duas), quase todas com hipertensão; o que separa as duas é
  o Holter, que tem 36.152 na fila, com pedidos desde 2012.
- **No risco cirúrgico, o pedido não traz o CID da ficha.** A consulta de risco cirúrgico tem
  10.041 pessoas, mas o CID do pedido é o da cirurgia (varizes, vesícula, hérnia, catarata). Só
  56 têm o CID da 001-8. Se essa fila conta para a OCI é decisão nossa e da SES.
- **O que o IEV já fez.** O painel não diz o convênio, mas duas unidades privadas começaram a
  agendar cardiologia em julho de 2026, quando começam as metas do IEV. O acervo as liga ao IEV:
  - o Centro Clínico e Ecográfico de Sobradinho (CNES 3031543) é unidade de execução do IEV;
  - a Clínica de Imagem Samambaia (0366986) é provável.

  Até 21/10/2026, as duas fizeram 1.937 consultas de risco cirúrgico, com mais 406 marcadas, e
  822 consultas de cardiologia adulto, com mais 73. Nenhum exame de cardiologia foi agendado em
  unidade privada.

**Trabalhar em conjunto para zerar a fila** (ideia do usuário, 22/10/2026). A mesma OCI pode
ser executada pelos dois, se a fila dela for maior que a soma das duas ofertas no período. O que
o nosso plano precisa mostrar:
- a fila da OCI, medida pelo CID;
- o que o IEV atende dela até 05/2027;
- que o que sobra comporta a nossa quantidade.

A regulação da SES distribui os pacientes, e cada um só pode ser faturado uma vez. A regra de
sobreposição do método (LI-023) é para o mesmo proponente com dois convênios. Entre entidades
diferentes, o risco é a SES ou o controle verem duplicidade; o número da fila responde.

## 3. O erro do IEV

**No plano aprovado, as duas OCI do meio estão com nome e valor trocados.** Mostro primeiro o
que diz o SIGTAP e depois o que diz o plano.

| OCI | nome no SIGTAP | valor no SIGTAP |
|---|---|---:|
| 004-2 | Progressão da Avaliação Diagnóstica I – Síndrome Coronariana Crônica | R$ 250,00 |
| 006-9 | Avaliação Diagnóstica – Insuficiência Cardíaca | R$ 350,00 |

**O que o plano aprovado diz:**

| onde | 004-2 | 006-9 |
|---|---|---|
| descrição do serviço (7.3) | "Avaliação Cardiológica", R$ 250,00 | "Progressão do Cuidado Cardiológico", **R$ 435,00** |
| planilha (2.3.2 e 2.3.3) | 900 × **R$ 350,00** = R$ 315.000,00 | 1.000 × **R$ 250,00** = R$ 250.000,00 |
| metas (seção 5) | 900 | 1.000, "OCI em ortopedia de cardiologia" |
| dimensionamento | "1.000 exames de ecocardiografia de estresse" | "900 exames e procedimentos" |

**Os erros, um a um:**
1. **Nomes.**
   - A 004-2 aparece como "Avaliação Cardiológica", que é o nome da 002-6, outra OCI.
   - A 006-9 aparece como "Progressão do Cuidado Cardiológico", que não existe na tabela.
2. **Três valores para a mesma OCI.** A 006-9 vale R$ 435,00 na descrição, R$ 250,00 na
   planilha e R$ 350,00 no SIGTAP. A 004-2 vale R$ 250,00 na descrição, certo, e R$ 350,00 na
   planilha.
3. **A planilha com os valores trocados.**
   - Na 004-2, o plano põe R$ 90.000,00 acima do SIGTAP (900 × R$ 100,00). O recurso federal
     não paga acima da tabela (LI-002).
   - Na 006-9, põe R$ 100.000,00 abaixo (1.000 × R$ 100,00).
   - As duas linhas somam R$ 565.000,00, e o certo seria R$ 575.000,00.
4. **O dimensionamento contradiz as metas.** As quantidades do texto (1.000 eco de estresse para
   a coronariana, 900 para a insuficiência cardíaca) são as do primeiro plano. Nele, a planilha
   tinha a 006-9 com 900 × R$ 250,00 e a 004-2 com 1.000 × R$ 350,00.
5. **Detalhes.**
   - A meta da 006-9 diz "ortopedia de cardiologia".
   - As metas de 2 meses não fecham com o total: 775 × 6 = 4.650 contra 4.647, e 167 × 6 = 1.002
     contra 1.000.

**De onde veio.** No plano de fevereiro, as duas linhas da planilha estavam com as quantidades e
os valores cruzados. A versão aprovada corrigiu as quantidades e deixou os valores. O texto da
seção 7.3 e o dimensionamento não foram revistos junto. Não se sabe se o 1º apostilamento
corrigiu isso.

**O que tiramos disso para os nossos planos:**
- conferir cada código contra a ficha da competência, com o nome, o valor e a composição (a
  verificação W do método e o agente `ficha-sigtap`);
- o mesmo número em todas as seções: descrição, planilha, metas e dimensionamento (a verificação
  R, prosa contra tabela, e a regra 14 de `metodo/comum.md`);
- quando muda uma linha, mudar tudo o que depende dela.
