# Estudo 1 — atender por OCI de cardiologia

**Controle interno.** Estudo de 27/10/2026 para o redacao_08: Emenda 41360018/2024, do Senador
Izalci Lucas, individual, federal, ação 2E90, R$ 2.000.000,00; executor Instituto Fazer o Bem,
Faz Bem. O estudo 2, por exames, é `estudo_cardiologia_por_exames_20261027.md`. A escolha é sua.

Refaz o estudo de 26/10 (`estudo_cardiologia_2_milhoes_20261026.md`) com duas coisas novas:
- a procura de portarias que mudaram as OCI ou os valores, até hoje;
- a Tabela SUS Candanga, como base do preço que a SES-DF aceita.

**As fontes:**
- **a fila:** a coleta do Mapa Social de 25/10/2026, `planos/redacao_08/dados/fontes/mapa_social_20261025.md`,
  no ramo `plano_oci_cardiologia`;
- **o valor:** o pacote oficial do SIGTAP da competência 10/2026 (`TabelaUnificada_202610_v2610271043.zip`,
  publicado hoje às 09:44);
- **a Candanga:** `~/Downloads/Tabela_SUS_Candanga___Final_SIA__1_ (2).pdf`, 27 páginas, de
  06/08/2026 (seção 2);
- **o mercado:** `planos/redacao_08/dados/precos.md`, de 22/10/2026, refeito em 25/10 com o mínimo da APAC;
- **o IEV:** o convênio 030977/2026 (pt_ses_04) e o mapeamento de 26/10 (`mapeamento_iev_20261026.md`).

**A conta parte de R$ 1.800.000,00 para produção:** o recurso menos 10% de apoio.

## 1. O que mudou nas normas

**Nas sete OCI de cardiologia, nada mudou depois do que o dossiê já usa.** O valor das sete na
competência 10/2026 é o das fichas de 22/10.

| norma | o que fez | desde | já no projeto? |
|---|---|---|---|
| SAES 4.104/2026 | criou a OCI 09.02.01.007-7, Gestão do Pré-Operatório: R$ 130,00, FAEC, CID principal Z01.8, Z48.8 ou Z48.9 | 06/2026 | sim |
| SAES 4.795/2026 | levou a 005-0 (cintilografia) de R$ 840,00 a R$ 1.879,80 | 09/2026 | sim |
| SAES 5.086/2026 (DOU 20/10) | criou a habilitação 38.14, "Unidade Móvel Cardiologia", da Modalidade 3 do Agora Tem Especialistas | 10/2026 | **não, é nova.** Não serve ao Instituto: só vale para ambulatório móvel sob gestão federal, contratado pela União (art. 2º) |

**Como se procurou:**
- **as Notas Técnicas do SIGTAP** de 06 a 11/2026, no FTP do DATASUS:
  - as de 06 e 07 foram republicadas em 23/10, e as de 09 e 10 em 26/10;
  - a de 11/2026, de 25/10, saiu hoje às 09:31 só com o índice, sem nenhuma alteração listada;
  - o pacote da competência 11/2026 ainda não saiu.
- **o DOU, Seção 1, edição extra e suplemento,** de 09 a 27/10, com `ferramentas/ler_dou.py`:
  10 atos normativos novos. No texto de cada um, só a 5.086 toca cardiologia. A 5.109 é de
  odontologia e oftalmologia; a 5.156, a 5.157 e a 5.158 são de oncologia; a 4.457 e a 5.215,
  de outros procedimentos.

**O que esta procura não fez:** ela não substitui a vigia de normas. A última vigia é de 10/10 e
a do dia 22 não rodou. Ficaram de fora o SINJ, o controle externo e o registro das normas novas
no acervo.

## 2. A Tabela SUS Candanga

**O que é o PDF.** É a "Análise comparativa — Tabela SUS Candanga (SIA)", de 06/08/2026, que
vem antes da Deliberação CG-SES 46, de 21/09/2026. Para cada código, ela põe lado a lado:
- o SIGTAP, sem e com incremento;
- o IVR;
- o PATE;
- a CBHPM;
- a Tabela SUS Paulista;
- as Deliberações da SES-DF;
- o SIGTAP corrigido pelo IPCA.

No fim, dá o valor máximo, o médio e o mediano. O PDF não diz qual dos três é o "Valor Tabela
SUS Candanga" do Anexo Único (Deliberação 46, art. 15, IV). Este estudo usa o **mediano** e mostra
os outros dois.

**O que ela mostra nas OCI:**
- **Ela é o SIGTAP mais 31%, em todas.** Nas OCI só há quatro fontes: o SIGTAP, o IVR e a
  Paulista (as duas a 150% do SIGTAP) e o IPCA. O mediano sai em 130,6% do SIGTAP em cinco das
  seis que ela traz, e em 125% na 005-0. Ela não mede o custo de nenhuma OCI.
- **A 007-7 não está nela:** foi criada em 06/2026, depois da base da análise. Este estudo usa a
  001-8, de mesmo valor (R$ 130,00), no lugar.
- **A 005-0 está com o valor velho:** R$ 840,00, mediano R$ 1.050,00. O SIGTAP de hoje
  (R$ 1.879,80) passa da Candanga, e a atualização do SIGTAP não muda a Candanga sozinha
  (Deliberação 46, art. 5º, § 1º).

**O que ela muda no plano: nada no valor unitário.** A emenda é federal e paga o SIGTAP (LI-002).
A diferença até a Candanga é "complementação distrital" (Deliberação 46, art. 4º, § 5º), paga
pelo DF com recurso próprio (Lei 7.897/2026, art. 4º, § 1º). Por isso a Candanga entra aqui como
custo que a SES reconhece, ao lado do mercado.

## 3. As sete OCI

"Cobre" é o SIGTAP ÷ a base da coluna. O mercado é o mínimo da APAC no DF: os obrigatórios e uma
consulta.

| OCI | SIGTAP | Candanga mediano (médio · máximo) | cobre a Candanga | mínimo da APAC no mercado | cobre o mercado | fila da finalidade (viva 24 m) | o IEV já faz |
|---|---|---|---|---|---|---|---|
| 007-7 pré-operatório | R$ 130,00 | não está; R$ 169,79 pela 001-8 | 77% | R$ 84,45 (clínico) | **154%** | 136 pelo CID; 9.630 na consulta de risco cirúrgico | — |
| 002-6 avaliação cardiológica | R$ 200,00 | R$ 261,22 (255,61 · 300,00) | 77% | R$ 151,00 | **132%** | 420 com 18 anos ou mais | — |
| 005-0 cintilografia | R$ 1.879,80 | R$ 1.050,00 (960,95 · 1.260,00), com o valor velho | 179% | R$ 1.798,00, com preço de São Paulo | 105% | 3.310 (2.911) | — |
| 003-4 coronária, inicial | R$ 270,00 | R$ 352,64 (345,07 · 405,00) | 77% | R$ 301,00 | 90% | 3.683 (3.087) | — |
| 001-8 risco cirúrgico | R$ 130,00 | R$ 169,79 (166,15 · 195,00) | 77% | R$ 151,00 | 86% | 360 com 18+ pelo CID | 4.647 |
| 006-9 insuficiência cardíaca | R$ 350,00 | R$ 457,13 (447,31 · 525,00) | 77% | R$ 522,22 | 67% | 6.510 (4.620) | 1.000 |
| 004-2 eco de estresse | R$ 250,00 | R$ 326,52 (319,51 · 375,00) | 77% | R$ 693,00 | 36% | 2.055 (1.651) | 900 |

## 4. Os caminhos

| caminho | o que compra | unidades | SIGTAP | custo pela Candanga | cobre a Candanga | cobre o mercado | depende de |
|---|---|---|---|---|---|---|---|
| **A. pré-operatório, coronária e avaliação** | 5.550 OCI 007-7, 3.683 OCI 003-4 e 420 OCI 002-6 | 9.653 | R$ 1.799.910,00 | R$ 2.350.820,02 | 77% | **110%** | a P-08 |
| A com 30% de apoio | 3.683 OCI 003-4, 420 OCI 002-6 e 2.473 OCI 007-7 | 6.576 | R$ 1.399.900,00 | R$ 1.828.376,19 | 77% | 101% | a P-08 |
| D. sem a P-08 | 136 OCI 007-7, 3.683 OCI 003-4, 420 OCI 002-6 e 2.011 OCI 006-9 | 6.250 | R$ 1.799.940,00 | R$ 2.350.865,39 | 77% | 81% | nada além do CNES |
| B. insuficiência cardíaca | 5.142 OCI 006-9 | 5.142 | R$ 1.799.700,00 | R$ 2.350.562,46 | 77% | 67% | repete a OCI do IEV na mesma fila |
| C. cintilografia | 957 OCI 005-0 | 957 | R$ 1.798.968,60 | R$ 1.004.850,00 | 179% | 105% | serviço de medicina nuclear, que é de terceiro |

**Como sai cada número:**
- **A:** a fila do risco cirúrgico (9.630) menos as 1.825 OCI 001-8 que o IEV ainda vai atender
  dá cerca de 7.805. Ele já agendou 2.822 das 4.647 (mapeamento de 26/10, seção 6). Depois da
  003-4 e da 002-6, o recurso compra 5.550 OCI 007-7 (R$ 721.500,00), 71% dessa fila.
- **D:** a 007-7 fica só com as 136 pessoas do CID dela; o resto (R$ 703.910,00) compra 2.011
  OCI 006-9.
- **O custo pela Candanga** é a quantidade × o mediano. Na 007-7 vai o mediano da 001-8.

## 5. O que a Candanga mostra nas OCI

- **Ela não escolhe entre as OCI:** todas ficam em 77%, porque ela é o SIGTAP mais 31%. Quem
  decide continua sendo o mercado.
- **Ela dá um teto de negociação que a SES reconhece.** Uma clínica que cobre até R$ 352,64 pela
  003-4 está dentro do que a própria SES considera justo. A cotação de R$ 378,00 da MedicCei
  (APAC num só prestador) passa dele.
- **Ela não paga a diferença.** Pela emenda, a unidade recebe o SIGTAP. A diferença até a
  Candanga é recurso do DF, e o plano não pode prometê-lo.
- **Na 005-0, a Candanga ficou para trás:** o SIGTAP de hoje já é 79% maior que ela.

## 6. A recomendação

**Por OCI, o caminho A continua o melhor.**
- Nenhuma portaria nova mudou as OCI ou os valores dele.
- É o único caminho em que o SIGTAP cobre o mercado (110%).
- Na conta da Candanga ele fica em 77%, como todos.
- Cabe no Ofício 36 como está e não precisa de habilitação.

**Se a P-08 não passar, o D** troca a 007-7 pela 006-9 e cai para 81% do mercado.

**Falta, para fechar:**
1. **a P-08:** a regulação aceita a fila de risco cirúrgico na 007-7?
2. **a cotação da 003-4** por volume, até R$ 352,64, o teto da Candanga;
3. **o CNES do Instituto** (P-03);
4. **o Anexo Único da Candanga:** confirmar com a SES que o valor dele é o mediano da análise,
   e quando sai a versão com a 007-7 e a 005-0 nova.
