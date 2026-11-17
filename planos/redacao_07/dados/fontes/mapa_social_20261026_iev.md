# Mapa Social da Saúde — o que o IEV já agenda e a fila que as OCI de ortopedia dele podem atender, recarga de 26/10/2026 16:32

Coleta do agente `mapa-social` para medir a sobreposição com o **IEV (Instituto Esporte e Vida,
CNPJ 05.117.522/0001-91)** em dois estudos de emenda: cardiologia (R$ 2 mi, redacao_08) e exames de
imagem (R$ 1,5 mi, redacao_07). O IEV tem três convênios com a SES-DF, todos com termo de 29/04/2026:
030975/2026 (DOA, ortopedia, 15 meses), 030976/2026 (DOAR, ortopedia, 13 meses) e 030977/2026 (Fila
Zero, cinco especialidades, 13 meses). Os planos aprovados contratam 100.525 OCI de ortopedia
(09.03.01.001-1 52.786; 002-0 19.070; 003-8 539; 004-6 28.130), 6.547 de cardiologia (001-8 4.647;
006-9 1.000; 004-2 900), 3.218 de saúde da mulher (09.06.01.001-2), 11.590 de déficit auditivo
(09.04.01.001-5 6.250; 002-3 5.340) e 1.015 de próstata (09.01.01.004-9), nos locais Centro Clínico
Sobradinho, Centro Clínico Samambaia e Centro de Imagens Gama.

Método de 25/10/2026 (`metodo/coleta/mapa_social.md`, ramo `melhorias/agentes`). Fichas das OCI pelo
pacote oficial da Tabela 10/2026 (`ferramentas/ler_tabela_unificada.py`, TabelaUnificada_202610_v2610261600).
A coleta de imagem de hoje (`mapa_social_20261026.md`, mesma recarga) não se sobrescreve; os números
de fila que as duas têm em comum batem (US de articulação 14.391, RM e TC por código). Planilha em
`mapa_social_20261026_iev.xlsx`; texto e JSON do motor, JSON da coleta e script em
`mapa_social_20261026_iev_bruto/`.

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera e Solicitações Agendadas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 26/10/2026 16:32:44 (qLastReloadTime 2026-10-26T19:32:44.246Z), conferida no início e no fim |
| Consulta | 26/10/2026, de 17:33 a 17:46 (relógio do motor, Brasília) |
| Solicitação mais recente na base | 26/10/2026 (agendamento mais distante: 27/01/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Fila viva | pedidos de 26/10/2024 em diante (24 meses contados da solicitação mais recente) |
| Agendadas 12 m | `data_agendamento` de 26/10/2025 a 25/10/2026, todos os status |
| Agendamentos do IEV | `data_agendamento` de 29/04/2026 em diante (o termo), todos os status, nas três unidades identificadas na seção 1; "de 26/10 em diante" = o que já está marcado de hoje até 26/11/2026 |
| Recorte das OCI | `codigo_cid_solicitado` igual a um dos CID principais da ficha (lista exata, sem curinga: "M15" é a categoria sem subitem, como o SISREG a grava); idade da ficha 0 a 130 anos, ambos os sexos, sem recorte de idade |
| Via | Qlik Engine API do próprio painel (hipercubos de sessão e evaluateEx), no navegador embutido; só contagens |

Pessoas = CNS distintos no conjunto, contados no motor; nenhum CNS sai do painel. Espera em dias,
calculada no motor sobre os registros do conjunto.

## Alarmes

Calculados pelo JSON da coleta (`coleta_iev_20261026.json`, chave `alarmes`); limites do método,
propostos em 25/10/2026 e ainda a confirmar.

- **CID largo** nas quatro OCI de ortopedia: **09.03.01.001-1** aceita 94 códigos em 15 categorias
  (M15–M19, M91–M96, Q65–Q66 e M124, M250); **09.03.01.002-0**, 32 códigos em 14 categorias;
  **09.03.01.003-8**, 46 códigos em 26 categorias; **09.03.01.004-6**, 57 códigos em 20 categorias. A
  ficha não traz CID da finalidade: a finalidade é igual ao teto, e um recorte mais estreito é decisão
  do usuário. O teto é o máximo que a APAC aceitaria, não a fila de quem precisa da OCI.
- **CID raro** em três delas: na união das filas da composição (exame + radiografias + consultas de
  ortopedia), o CID da ficha pega **1.493 de 62.714** solicitações na **002-0** (2,4%), **397 de
  54.267** na **003-8** (0,7%) e **1.831 de 55.302** na **004-6** (3,3%). Na 001-1, 4.845 de 48.323
  (10,0%): não dispara. A demanda que essas OCI atendem está com outro CID: M75 (ombro), M54 e M51
  (coluna), M23 (menisco), M25. O próprio IEV agenda **76% das suas consultas de ortopedia (22.856 de
  29.894) com CID fora das quatro listas** (seção 2.5).
- **Fila genérica**: CONSULTA EM ORTOPEDIA E TRAUMATOLOGIA (6.794 na fila; marcada genérica por esta
  coleta: é a consulta geral da especialidade) e CONSULTA EM ORTOPEDIA - GERAL (2 na fila) estão na
  composição das quatro OCI (001-1, 002-0, 003-8, 004-6) como consulta de entrada. Só contam pela
  finalidade, e a decisão de pô-las na OCI é do usuário.
- **Estoque** (fila acima de 3 anos de agendamentos, ou nenhum agendamento em 12 meses): 44 filas da
  composição. As que pesam: **CONSULTA EM ORTOPEDIA - COLUNA, 23.634 na fila e 5.135 agendadas em 12
  meses (4,6 anos)**; CONSULTA EM ORTOPEDIA - PEDIATRIA, 2.363 e 542 (4,4 anos). Na US de articulação,
  nomes pequenos: coluna lombar infantil 134 e 4 (33,5 anos), região lombar 55 e 3 (18,3), pescoço 160
  e 35 (4,6), coxo-femural infantil E 82 e 12 (6,8) e D 77 e 14 (5,5), braço E 50 e 10 (5,0). As outras
  36 têm menos de 50 na fila (aba 26 da planilha).
- **Fila velha** não dispara em nenhuma das quatro OCI (fora da janela viva: 001-1 9%, 002-0 19%,
  003-8 18%, 004-6 2% das pessoas). Na fila inteira, sem recorte de CID, ela aparece: consulta de
  coluna, 11.316 de 23.634 pedidos (48%) de antes de 26/10/2024, o mais antigo de 08/04/2022; US de
  partes moles, 1.245 de 3.117 (40%), desde 28/10/2010; US de articulação no código, 3.995 de 14.391
  (28%).
- **CID dominante** não se calcula: o CID da finalidade é igual ao aceito.

**O que o método não resolve:**
- **O painel não traz o convênio.** As três unidades do IEV saíram do nome, do tipo, da data e do que
  agendam (seção 1).
- **Nas unidades do IEV o SISREG só mostra a consulta de entrada.** Nenhuma US de articulação,
  tomografia, radiografia, eco, ergométrico, Holter, audiometria ou consulta de urologia foi agendada
  nelas. A RM agendada em Sobradinho e no Gama vem de antes do termo (2025 e 2019) e não cresceu depois
  dele. O painel não mede o que o IEV entrega em exame: o exame da OCI é feito dentro do pacote, sem
  agendamento regulado.
- **O CID do agendamento não é o CID da APAC.** O painel não traz a APAC; não se sabe quantas das
  13.818 consultas de ortopedia realizadas viraram OCI nem com que CID.

## 1. As unidades do IEV

| código no painel | nome no painel / no SISREG | tipo | primeiro agendamento | primeira consulta das especialidades do IEV | agendamentos de 29/04/2026 em diante | de 26/10 em diante | filas | certeza |
|---|---|---|---|---|---|---|---|---|
| 0366986 | CLINICA DE IMAGEM SAMAMBAIA / **CENTRO CLINICO SAMAMBAIA** | Privado | 03/06/2026 | 03/06/2026 (ombro) | 16.171, todos de consulta | 1.536 | 10 | **alta**: o nome é o do local do plano, começou depois do termo e só agenda consultas de ortopedia, cardiologia, ginecologia e otorrino |
| 3031543 | Centro Clinico Ecografico Sobrainho / **CENTRO CLINICO E ECOGRAFICO** | Privado | 18/09/2025 (RM) | 21/05/2026 (ombro) | 14.994: 10.710 consultas + 4.284 RM | 1.151 | 196 | **alta para as consultas**; a RM vem de antes do termo e não se atribui ao convênio |
| 9180168 | CIG - CENTRO DE IMAGENS GAMA / **CIG CENTRO DE IMAGENS GAMA** | Contratado/Credenciado | 29/08/2019 (RM) | 08/06/2026 (ombro) | 10.388: 7.113 consultas de ortopedia + 3.275 RM | 695 | 226 | **média-alta para as consultas de ortopedia**: o tipo é o do credenciamento antigo de RM; a consulta de ortopedia é nova e repete o desenho das outras duas |

As três começam a agendar consulta de ortopedia entre 21/05 e 08/06/2026; nenhuma outra unidade do DF
começou a agendar consulta de ortopedia depois do termo (com 30 agendamentos ou mais). A RM das duas que já agendavam não muda
com o termo: em Sobradinho, 1.015 a 1.639 por mês de out/2025 a fev/2026 e 422 a 962 de mai a
out/2026; no Gama, 655 a 757 por mês de out/2025 a mai/2026 e 274 a 645 de jun a out/2026 (aba 25).

**Descartadas:** NOVA SAUDE SOBRADINHO (4294491, "Não Relacionado - Base SES"): só RM, desde
08/09/2025, nenhuma consulta (3.018 desde 29/04). As outras 14 unidades "Privado" com agendamento na
base não agendam ortopedia, cardiologia, ginecologia nem otorrino (seção 7).

## 2. O que o IEV agendou (parte A)

### 2.1 Por grupo e por mês, nas três unidades

Abril = 29 e 30/04; novembro = só o que já está marcado (até 26/11/2026); outubro inclui o marcado de
26 a 31/10.

| grupo | abr | mai | jun | jul | ago | set | out | nov | **desde 29/04** | **de 26/10 em diante** |
|---|---|---|---|---|---|---|---|---|---|---|
| consultas de ortopedia | 0 | 596 | 5.064 | 9.440 | 3.892 | 2.716 | 7.353 | 833 | **29.894** | **2.159** |
| cardiologia: risco cirúrgico | 0 | 0 | 0 | 615 | 240 | 362 | 1.127 | 478 | **2.822** | **720** |
| cardiologia: adulto | 0 | 0 | 0 | 61 | 150 | 233 | 454 | 240 | **1.138** | **316** |
| ginecologia (geral) | 0 | 0 | 0 | 60 | 0 | 0 | 0 | 0 | **60** | 0 |
| otorrinolaringologia (geral) | 0 | 0 | 0 | 80 | 0 | 0 | 0 | 0 | **80** | 0 |
| ressonância 02.07 (Sobradinho e Gama, contrato anterior) | 120 | 1.564 | 1.209 | 1.491 | 1.567 | 740 | 843 | 25 | 7.559 | 187 |
| US de articulação, tomografia, radiografia | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| eco, ergométrico, Holter, ECG | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| audiometria, urologia, próstata | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |

Consultas de ortopedia por unidade e mês: Samambaia jun 2.018, jul 4.891, ago 2.130, set 1.357, out
2.978, nov 397 (13.771); Sobradinho mai 596, jun 2.129, jul 2.506, ago 777, set 554, out 2.163, nov 285
(9.010); Gama jun 917, jul 2.043, ago 985, set 805, out 2.212, nov 151 (7.113). Os meses vêm em blocos
(joelho em julho, coluna em setembro e outubro): é agenda aberta em mutirão, não fluxo contínuo.

### 2.2 Por unidade e nome de fila

| fila | Samambaia | Sobradinho | Gama | **total desde 29/04** | de 26/10 em diante | primeiro agendamento |
|---|---|---|---|---|---|---|
| CONSULTA EM ORTOPEDIA - JOELHO | 5.318 | 4.048 | 1.429 | **10.795** | 286 | 08/06/2026 |
| CONSULTA EM ORTOPEDIA - OMBRO | 3.905 | 2.091 | 2.140 | **8.136** | 377 | 21/05/2026 |
| CONSULTA EM ORTOPEDIA - COLUNA | 1.794 | 1.132 | 1.451 | **4.377** | 652 | 02/09/2026 |
| CONSULTA EM ORTOPEDIA - PE/TORNOZELO | 1.575 | 992 | 1.557 | **4.124** | 312 | 02/07/2026 |
| CONSULTA EM ORTOPEDIA - QUADRIL | 698 | 376 | 306 | **1.380** | 161 | 25/08/2026 |
| CONSULTA EM ORTOPEDIA E TRAUMATOLOGIA | 481 | 370 | 228 | **1.079** | 368 | 19/08/2026 |
| CONSULTA EM ORTOPEDIA - PEDIATRIA | 0 | 1 | 2 | 3 | 3 | 03/11/2026 |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO | 1.654 | 1.168 | 0 | **2.822** | 720 | 03/07/2026 |
| CONSULTA EM CARDIOLOGIA - ADULTO | 636 | 502 | 0 | **1.138** | 316 | 20/07/2026 |
| CONSULTA EM GINECOLOGIA - GERAL | 30 | 30 | 0 | 60 | 0 | 23/07/2026 |
| CONSULTA EM OTORRINOLARINGOLOGIA - GERAL | 80 | 0 | 0 | 80 | 0 | 21/07/2026 |
| RM, todos os códigos (por código na aba 2) | 0 | 4.284 | 3.275 | 7.559 | 187 | 2019 e 2025 |
| · RM nos seis códigos compatíveis com a 004-6 | 0 | 2.656 | 2.418 | 5.074 | — | — |

### 2.3 Situação dos agendamentos (desde 29/04/2026)

| grupo | realizado | falta do paciente | agendado, pendente de confirmação | autorizado pela regulação | cancelado | total |
|---|---|---|---|---|---|---|
| consultas de ortopedia | 13.818 | 11.112 | 2.802 | 1.857 | 305 | 29.894 |
| cardiologia: risco cirúrgico | 990 | 499 | 658 | 651 | 24 | 2.822 |
| cardiologia: adulto | 300 | 314 | 163 | 309 | 52 | 1.138 |
| ginecologia | 20 | 17 | 23 | 0 | 0 | 60 |
| otorrino | 28 | 52 | 0 | 0 | 0 | 80 |

Na ortopedia, 11.112 faltas para 13.818 realizadas (45% dos agendamentos com desfecho).

### 2.4 O que o IEV agendou × o que contratou (calculado)

| objeto | contratado (OCI, planos aprovados) | consultas agendadas no IEV desde 29/04 | das quais de 26/10 em diante | realizadas | exames da OCI agendados no SISREG |
|---|---|---|---|---|---|
| ortopedia, quatro OCI, dois convênios | 100.525 | 29.894 | 2.159 | 13.818 | nenhum (RM das unidades é contrato anterior) |
| cardiologia, três OCI | 6.547 | 3.960 | 1.036 | 1.290 | nenhum |
| saúde da mulher 09.06.01.001-2 | 3.218 | 60 | 0 | 20 | nenhum |
| déficit auditivo 09.04.01.001-5 e 002-3 | 11.590 | 80 (otorrino) | 0 | 28 | nenhuma audiometria |
| próstata 09.01.01.004-9 | 1.015 | 0 | 0 | 0 | nenhum |

Do termo a hoje passaram 180 dias, perto de seis dos 13 a 15 meses. A consulta agendada é a porta de
entrada da OCI (a ficha admite até duas consultas por OCI); o painel não diz quantas consultas viraram
OCI. O painel não separa DOA de DOAR.

### 2.5 CID nos agendamentos do IEV

**Consultas de ortopedia (29.894):** M75 5.414, M23 3.237, M25 3.044, M54 2.740, M17 2.568, S83 1.164,
M51 1.123, M19 972, M77 755, M79 615, M22 581, M16 538. Pela lista de CID de cada OCI:

| lista | consultas de ortopedia no IEV com CID da lista | das quais realizadas |
|---|---|---|
| 09.03.01.001-1 | 4.440 | 2.325 |
| 09.03.01.002-0 | 642 | 308 |
| 09.03.01.003-8 | 250 | 94 |
| 09.03.01.004-6 | 1.955 | 944 |
| em alguma das quatro | 7.038 (23,5%) | 3.580 |
| **em nenhuma** | **22.856 (76,5%)** | 10.238 |

Por fila: ombro, M75 em 5.293 de 8.136 (a 004-6 só aceita M750–M753); joelho, M23 3.143, M17 2.451,
M25 1.556, S83 1.141 de 10.795; coluna, M54 2.291 e M51 1.014 de 4.377.

**Risco cirúrgico (2.822):** H25 catarata 888, Z13 489, Z10 210, K80 75, H02 72, K42 57, Z48 52, K43
52, K40 52, H11 51, N40 43, H33 41. **Cardiologia adulto (1.138):** I10 349, I50 206, I25 113, I49 70,
I21 61, I20 46, I48 42.

**US de articulação:** nenhum agendamento nas unidades do IEV; não há CID para dar.

### 2.6 O peso do IEV na consulta de ortopedia do DF

| mês de 2026 | jan | fev | mar | abr | mai | jun | jul | ago | set | out | nov |
|---|---|---|---|---|---|---|---|---|---|---|---|
| todas as unidades | 774 | 992 | 1.541 | 1.214 | 1.905 | 6.116 | 10.406 | 5.046 | 3.947 | 8.329 | 1.153 |
| unidades do IEV | 0 | 0 | 0 | 0 | 596 | 5.064 | 9.440 | 3.892 | 2.716 | 7.353 | 833 |

De 29/04/2025 a 28/04/2026 o DF agendou 12.704 consultas de ortopedia (todos os nomes "CONSULTA EM
ORTOPEDIA ..."); de 29/04/2026 em diante, 37.032, das quais **29.894 no IEV (81%)**. Em 12 meses
(26/10/2025 a 25/10/2026), 40.728, das quais 27.735 no IEV (68%).

## 3. A fila que as OCI de ortopedia do IEV podem atender (parte B)

### 3.1 Os três números, em pessoas

Teto = CID aceito da ficha na união das filas da composição que existem no SISREG (o exame que dá nome
à OCI, as radiografias compatíveis e as consultas de ortopedia). A ficha não separa o CID da
finalidade: a finalidade é igual ao teto. Núcleo = o CID na consulta de entrada ou em quem espera o
exame obrigatório, o que for maior (só a 002-0 tem exame obrigatório, a US de articulação).

| OCI | CID aceito | CID da finalidade | teto | teto viva | finalidade | finalidade viva | núcleo | núcleo viva | espera média (finalidade) |
|---|---|---|---|---|---|---|---|---|---|
| 09.03.01.001-1 radiologia | 94 códigos: M124, M15–M19, M250, M91–M95, M960, Q65–Q66 | igual ao teto | 4.636 | 4.217 | 4.636 | 4.217 | 4.505 | 4.085 | 311 |
| 09.03.01.002-0 radiologia e US | 32 códigos: I234, I511, M122, M236, M65, M66, M673, M680, M700, M87, M903–M905, S532, S533, S633, S932 | igual ao teto | 1.225 | 986 | 1.225 | 986 | 651 | 438 | 457 |
| 09.03.01.003-8 radiologia e TC | 46 códigos: D169, D480, M162, M241, M403, M42, M432, M532, M861–M864, M918, M94, Q65, Q67, Q76, S134, S336, S430–S434, S480, S730, S780, S930, T09, T902–T932 | igual ao teto | 389 | 319 | 389 | 319 | 380 | 310 | 419 |
| 09.03.01.004-6 radiologia e RM | 57 códigos: C40–C41, D16, D169, D480, M111, M112, M224, M236, M241, M42, M750–M753, M91–M94, Q773, Q776, Q78, S532, S533, S633, S833, S932 | igual ao teto | 1.720 | 1.692 | 1.720 | 1.692 | 1.532 | 1.505 | 161 |

Núcleo: 001-1, 003-8 e 004-6 pela consulta de entrada (na 003-8 a TC com o CID tem 6 pessoas; na
004-6 a RM com o CID tem 188); 002-0 pela US de articulação com o CID (651; a consulta tem 579).
**União dos quatro tetos: 7.551 pessoas (6.816 na fila viva).** Menores de 18 anos no teto: 567,
19, 111 e 57 (pé torto e displasia de quadril, Q65–Q66, na pediatria). Sem recorte de CID, as mesmas
filas têm 44.679, 54.491, 49.693 e 49.182 pessoas.

### 3.2 09.03.01.002-0 — US de articulação 02.05.02.006-2, todos os nomes

O código inteiro: **14.391 na fila**, 10.396 na viva, **11.435 pessoas** (8.088 na viva), 5.193
devolvidas, espera média de 547 dias, mediana 398, máxima 6.025, pedido mais antigo de 29/04/2010,
5.725 pedidos de 2026 na fila, 8.039 agendadas em 12 meses (**nenhuma nas unidades do IEV**; nenhuma
em unidade "Privado" desde 29/04).

| recorte | fila | fila viva | pessoas | pessoas viva | devolvidas | espera média | mediana | máxima |
|---|---|---|---|---|---|---|---|---|
| **no CID da 002-0** | **879 (6,1%)** | 601 | **651** | 438 | 345 | 613 | 425 | 2.117 |
| fora do CID da 002-0 | 13.512 (93,9%) | 9.795 | — | — | 4.848 | — | — | — |

**Por nome de fila** (fila de 30 ou mais; os outros 31 nomes somam 273):

| nome no SISREG | fila | viva | pessoas | devolvidas | espera média | mediana | pedido mais antigo | no CID 002-0 | viva no CID | agendadas 12 m |
|---|---|---|---|---|---|---|---|---|---|---|
| ECOGRAFIA DE PARTES MOLES | 3.117 | 1.872 | 3.115 | 1.456 | 652 | 502 | 28/10/2010 | 70 | 40 | 1.422 |
| ECOGRAFIA DE ARTICULACAO OMBRO D ADULTO | 1.959 | 1.456 | 1.957 | 743 | 559 | 392 | 12/01/2021 | 130 | 79 | 1.178 |
| ECOGRAFIA DE ARTICULACAO PUNHO D ADULTO | 1.691 | 1.293 | 1.690 | 380 | 512 | 370 | 24/09/2010 | 165 | 123 | 704 |
| ECOGRAFIA DE ARTICULACAO OMBRO E ADULTO | 1.526 | 1.168 | 1.525 | 585 | 536 | 384 | 07/01/2021 | 98 | 60 | 843 |
| ECOGRAFIA DE ARTICULACAO PUNHO E ADULTO | 1.459 | 1.150 | 1.458 | 347 | 495 | 369 | 08/01/2021 | 156 | 112 | 605 |
| ECOGRAFIA DE ARTICULACAO JOELHO E ADULTO | 590 | 388 | 590 | 69 | 582 | 504 | 28/01/2021 | 10 | 4 | 315 |
| ECOGRAFIA DE ARTICULACAO JOELHO D ADULTO | 551 | 359 | 551 | 63 | 593 | 544 | 28/01/2021 | 7 | 5 | 332 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO E ADULTO | 374 | 304 | 373 | 118 | 468 | 366 | 19/01/2021 | 51 | 42 | 224 |
| ECOGRAFIA DE ARTICULACAO TORNOZELO D ADULTO | 333 | 273 | 333 | 139 | 442 | 332 | 11/03/2021 | 48 | 37 | 238 |
| ECOGRAFIA DE REGIAO INGUINAL DIREITO | 241 | 213 | 241 | 16 | 373 | 321 | 09/03/2023 | 0 | 0 | 259 |
| ECOGRAFIA DE ARTICULACAO COTOVELO D ADULTO | 215 | 156 | 215 | 72 | 524 | 297 | 25/02/2021 | 21 | 18 | 260 |
| ECOGRAFIA DE REGIÃO INGUINAL ESQUERDO | 201 | 179 | 201 | 12 | 348 | 273 | 24/11/2022 | 0 | 0 | 216 |
| USG MAO DIREITA | 196 | 163 | 196 | 31 | 416 | 278 | 08/02/2023 | 31 | 25 | 133 |
| ULTRASSONOGRAFIA DA REGIAO INGUINAL | 164 | 130 | 164 | 26 | 441 | 437 | 29/03/2023 | 0 | 0 | 260 |
| ULTRASSONOGRAFIA DO PESCOCO | 160 | 119 | 160 | 8 | 508 | 478 | 06/02/2023 | 0 | 0 | 35 |
| ECOGRAFIA DE ARTICULACAO COTOVELO E ADULTO | 143 | 111 | 143 | 59 | 463 | 317 | 20/01/2021 | 10 | 9 | 220 |
| USG MAO ESQUERDA | 142 | 108 | 142 | 27 | 475 | 365 | 08/02/2023 | 9 | 7 | 112 |
| ECOGRAFIA DE ARTICULACAO COLUNA LOMBAR | 134 | 93 | 134 | 1 | 519 | 517 | 24/04/2024 | 0 | 0 | 4 |
| USG QUADRIL | 120 | 107 | 120 | 18 | 335 | 273 | 07/02/2023 | 6 | 4 | 93 |
| USG PE DIREITO | 114 | 74 | 114 | 20 | 541 | 400 | 07/02/2023 | 7 | 4 | 63 |
| USG PE ESQUERDO | 99 | 71 | 98 | 29 | 493 | 391 | 08/02/2023 | 5 | 4 | 62 |
| ULTRASSONOGRAFIA CERVICAL | 99 | 85 | 99 | 39 | 336 | 175 | 16/02/2023 | 0 | 0 | 151 |
| ECOGRAFIA DE ARTICULACAO NAO LISTADA | 96 | 52 | 96 | 262 | 924 | 626 | 14/01/2021 | 12 | 9 | 51 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E INFANTIL | 82 | 67 | 82 | 12 | 414 | 391 | 07/08/2023 | 1 | 1 | 12 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D INFANTIL | 77 | 68 | 77 | 12 | 360 | 319 | 25/04/2024 | 1 | 1 | 14 |
| ULTRASSONOGRAFIA DA REGIAO LOMBAR | 55 | 45 | 55 | 7 | 459 | 408 | 10/10/2023 | 0 | 0 | 3 |
| USG BRACO ESQUERDO | 50 | 7 | 50 | 10 | 1.178 | 1.356 | 08/02/2023 | 15 | 1 | 10 |
| ECOGRAFIA PELVICA | 46 | 46 | 46 | 15 | 88 | 82 | 13/05/2026 | 3 | 3 | 21 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL D ADULTO | 46 | 36 | 46 | 26 | 557 | 371 | 02/02/2021 | 2 | 2 | 26 |
| ECOGRAFIA DE ARTICULACAO COXO-FEMURAL E ADULTO | 38 | 27 | 38 | 27 | 543 | 235 | 18/02/2021 | 2 | 1 | 14 |

Os nomes exatos (alguns com espaço duplo, como "ECOGRAFIA␣␣DE PARTES MOLES") estão em
`nomes_internos` no JSON. O código também guarda filas que não são de articulação (região inguinal,
pescoço, cervical, pélvica, glândulas submandibulares, doppler de aorta): entram pelo código, como foi
pedido, e ficam fora pelo CID.

**O que fica fora da lista da 002-0, pelos grupos de CID que mais pesam** (fila do código inteiro):

| grupo de CID | fila | fila viva | pessoas | no CID da 002-0 |
|---|---|---|---|---|
| M75 ombro (tendinite, bursite, manguito) | 2.189 | 1.666 | 1.852 | 0 |
| M25 outros transtornos articulares | 1.750 | 1.298 | 1.293 | 0 |
| G56 túnel do carpo | 1.351 | 1.060 | 926 | 0 |
| R22 e D17 nódulo e lipoma | 1.686 | 1.019 | 1.674 | 0 |
| K40 hérnia inguinal | 673 | 522 | 621 | 0 |
| M71 bursopatias (cisto de Baker) | 538 | 283 | 494 | 0 |
| M79 partes moles | 461 | 360 | 362 | 0 |
| M23 transtornos internos do joelho (a ficha só aceita M236) | 395 | 238 | 319 | 0 |
| Q65 e Q76 (criança; estão na 001-1 e na 003-8) | 288 | 230 | 246 | 0 |
| M65 sinovite e tenossinovite | 963 | 675 | 714 | **865** (98 com subcategoria que a ficha não lista) |

Os nove grupos fora da lista e a parte de M65 fora dela somam 9.429 das 13.512 solicitações fora.
Outros: R52 244, L72 221, M77 205, M72 200, R59 190, M13 156, M17 125 (aba 13).

### 3.3 09.03.01.004-6 — ressonância (seis códigos compatíveis)

| código | exame | fila | viva | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | no CID 004-6 | pessoas no CID | agendadas 12 m | das quais nas unidades do IEV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.07.01.003-0 | coluna cervical / pescoço | 763 | 760 | 751 | 1.243 | 30 | 24 | 1.715 | 14/02/2022 | 1 | 1 | 9.594 | 1.486 |
| 02.07.01.004-8 | coluna lombo-sacra | 1.553 | 1.549 | 1.551 | 2.270 | 26 | 21 | 1.720 | 09/02/2022 | 2 | 2 | 20.121 | 3.288 |
| 02.07.01.005-6 | coluna torácica | 286 | 286 | 285 | 616 | 23 | 23 | 66 | 21/08/2026 | 1 | 1 | 4.448 | 671 |
| 02.07.02.002-7 | membro superior | 1.254 | 1.250 | 950 | 1.426 | 27 | 21 | 1.720 | 09/02/2022 | 185 | 153 | 12.328 | 2.028 |
| 02.07.03.002-2 | bacia / pelve / abdômen inferior | 1.439 | 1.439 | 1.437 | 2.089 | 27 | 26 | 91 | 27/07/2026 | 4 | 4 | 19.779 | 2.533 |
| 02.07.03.003-0 | membro inferior | 1.684 | 1.682 | 1.303 | 1.816 | 25 | 21 | 1.754 | 06/01/2022 | 43 | 31 | 17.797 | 2.848 |
| **os seis** | | **6.979** | 6.966 | **5.334** | 9.459 | 26 | 24 | 1.754 | | **236 (3,4%)** | **188** | 84.067 | 12.854 |

A RM anda: 84.067 agendadas em 12 meses para 6.979 na fila, espera média de 26 dias. As 12.854 nas
unidades do IEV são da RM que Sobradinho e o Gama já faziam antes do termo. Fora da lista: M54 1.592,
M25 606, M23 438, M75 436 (179 dentro, M750–M753), M51 350, N80 314, M79 171, R10 165, M17 163.

### 3.4 09.03.01.003-8 — tomografia (sete códigos compatíveis)

| código | exame | fila | viva | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | no CID 003-8 | agendadas 12 m | nas unidades do IEV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 02.06.01.001-0 | coluna cervical | 139 | 136 | 137 | 373 | 189 | 129 | 762 | 24/09/2024 | 0 | 1.478 | 0 |
| 02.06.01.002-8 | coluna lombo-sacra | 164 | 157 | 162 | 370 | 230 | 146 | 763 | 23/09/2024 | 1 | 3.182 | 0 |
| 02.06.01.003-6 | coluna torácica | 79 | 78 | 77 | 154 | 198 | 137 | 754 | 02/10/2024 | 0 | 1.093 | 0 |
| 02.06.02.001-5 | articulações de membro superior | 71 | 69 | 68 | 101 | 261 | 182 | 736 | 20/10/2024 | 0 | 1.032 | 0 |
| 02.06.02.002-3 | segmentos apendiculares | 219 | 219 | 164 | 223 | 203 | 108 | 728 | 28/10/2024 | 3 | 2.310 | 0 |
| 02.06.03.002-9 | articulações de membro inferior | 242 | 239 | 206 | 255 | 258 | 185 | 756 | 30/09/2024 | 1 | 1.703 | 0 |
| 02.06.03.003-7 | pelve / bacia / abdômen inferior | 5.030 | 4.976 | 4.885 | 5.557 | 177 | 145 | 3.611 | 06/12/2016 | 2 | 14.950 | 0 |
| **os sete** | | **5.944** | 5.874 | **5.406** | 7.033 | 184 | 146 | 3.611 | | **7 (0,1%)**, 6 pessoas | 25.748 | 0 |

Dos 5.944, 5.030 são TC de pelve (C50 667, R10 563, C18 405: oncologia e abdômen). Nos seis códigos
de coluna e membros, 914 na fila e 5 com o CID da ficha; parte deles é das filas "EMERG." de
pronto-atendimento (aba 18).

### 3.5 09.03.01.001-1 — consultas de ortopedia (todos os nomes "CONSULTA EM ORTOPEDIA ...")

| nome no SISREG | fila | viva | pessoas | devolvidas | espera média | mediana | pedido mais antigo | no CID 001-1 | agendadas 12 m | das quais no IEV | % IEV | agendadas 29/04/2025–28/04/2026 | desde 29/04/2026 | no IEV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COLUNA | 23.634 | 12.318 | 23.634 | 3.835 | 703 | 693 | 08/04/2022 | 469 | 5.135 | 3.725 | 73% | 1.359 | 5.191 | 4.377 |
| JOELHO | 8.054 | 8.052 | 8.054 | 1.710 | 263 | 236 | 08/12/2020 | 2.298 | 11.257 | 10.509 | 93% | 781 | 11.185 | 10.795 |
| E TRAUMATOLOGIA | 6.794 | 6.337 | 6.786 | 5.195 | 264 | 173 | 11/07/2023 | 746 | 7.165 | 711 | 10% | 5.971 | 4.787 | 1.079 |
| OMBRO | 2.375 | 2.375 | 2.375 | 393 | 128 | 102 | 07/07/2025 | 65 | 8.665 | 7.759 | 90% | 1.066 | 8.606 | 8.136 |
| PEDIATRIA | 2.363 | 1.795 | 2.363 | 265 | 508 | 433 | 07/11/2022 | 543 | 542 | 0 | 0% | 568 | 274 | 3 |
| MAO | 1.813 | 1.813 | 1.813 | 213 | 186 | 174 | 17/06/2025 | 83 | 1.300 | 0 | 0% | 1.324 | 634 | 0 |
| PE/TORNOZELO | 746 | 746 | 746 | 363 | 101 | 76 | 09/07/2025 | 73 | 4.463 | 3.812 | 85% | 674 | 4.409 | 4.124 |
| QUADRIL | 683 | 683 | 683 | 178 | 147 | 147 | 17/11/2025 | 320 | 1.802 | 1.219 | 68% | 532 | 1.719 | 1.380 |
| TUMORES | 6 | 6 | 6 | 68 | 11 | 12 | 09/10/2026 | 0 | 228 | 0 | 0% | 257 | 124 | 0 |
| GERAL | 2 | 0 | 2 | 0 | 2.580 | 2.580 | 15/08/2019 | 0 | 0 | 0 | — | 0 | 0 | 0 |
| ADULTO - OSTEOPOROSE | 0 | 0 | 0 | 145 | — | — | — | 0 | 171 | 0 | 0% | 172 | 103 | 0 |
| GERAL - PEDIATRIA | 0 | 0 | 0 | 1 | — | — | — | 0 | 0 | 0 | — | 0 | 0 | 0 |
| **todas** | **46.470** | 34.125 | **43.702** | 12.366 | 485 | 350 | | **4.597** (4.505 pessoas) | 40.728 | **27.735** | **68%** | 12.704 | 37.032 | 29.894 |

O IEV pega o joelho, o ombro e o pé quase inteiros, e a fila deles caiu para meses: joelho 8.054 com
espera média de 263 dias, ombro 2.375 com 128, pé 746 com 101. A fila grande é a **coluna, 23.634
(51% da fila de consulta de ortopedia)**, onde o IEV só entrou em setembro e o CID quase nunca é da
001-1 (M54 e M51: lombalgia e disco). Nas consultas, o CID da 001-1 pega 4.597 de 46.470 (9,9%):
M17 joelho (1.979 na fila de joelho), M19, M16 quadril, e Q66 e Q65 na pediatria.

**Radiografias compatíveis (20 códigos, nas quatro OCI):** 1.853 na fila, 1.850 na viva (três
pedidos antigos, de 2007 e 2023), 18.581 agendadas em 12 meses, nenhuma nas unidades do IEV; com o CID da 001-1, 248; da 002-0, 9; da 003-8, 7; da 004-6, 27 (aba 19).

## 4. Cardiologia (parte C)

A fila pelo CID foi medida em 25/10 (`planos-ses_plano_oci_cardiologia/planos/redacao_08/dados/fontes/mapa_social_20261025.md`)
e não se refaz. Aqui, só o que as unidades do IEV agendaram.

| fila | unidade | jul | ago | set | out | nov (marcado) | **desde 29/04** | de 26/10 em diante | primeiro | último marcado |
|---|---|---|---|---|---|---|---|---|---|---|
| RISCO CIRURGICO | Samambaia | 615 | 120 | 176 | 482 | 261 | **1.654** | 503 | 03/07/2026 | 23/11/2026 |
| RISCO CIRURGICO | Sobradinho | 0 | 120 | 186 | 645 | 217 | **1.168** | 217 | 24/08/2026 | 17/11/2026 |
| ADULTO | Samambaia | 30 | 90 | 90 | 306 | 120 | **636** | 196 | 20/07/2026 | 26/11/2026 |
| ADULTO | Sobradinho | 31 | 60 | 143 | 148 | 120 | **502** | 120 | 27/07/2026 | 05/11/2026 |
| **as duas filas** | | 676 | 390 | 595 | 1.581 | 718 | **3.960** | **1.036** | | |

O Gama não agenda cardiologia. Nenhum ECG, eco, ergométrico, Holter ou cintilografia foi agendado nas
três unidades. No DF, o IEV ficou com 615 de 1.039 consultas de risco cirúrgico agendadas em julho,
1.127 de 1.299 em outubro e 478 de 571 em novembro; na consulta adulto, 454 de 774 em outubro (aba 9).
Situação: risco cirúrgico 990 realizadas, 499 faltas; adulto 300 e 314. CID: seção 2.5 (H25 catarata
lidera o risco cirúrgico; I10 e I50 a consulta adulto). Contratado nas três OCI de cardiologia: 6.547.

## 5. Varredura das filas

Feita na tabela de solicitações, com a lista de CID de cada OCI na medida, sobre todas as filas: a
001-1 aparece em 198 filas (8.909 solicitações com o CID), a 002-0 em 105 (2.520), a 003-8 em 119 (940)
e a 004-6 em 123 (4.489). As 25 maiores de cada uma estão na aba 24.

**Entra** (composição da ficha, pelo CID):

| fila | papel | OCI | por quê |
|---|---|---|---|
| US de articulação 02.05.02.006-2, os 61 nomes com fila | exame obrigatório | 002-0 | pedido do usuário: todos os nomes do código; os não articulares ficam fora pelo CID |
| RM 02.07.01.003-0, 004-8, 005-6, 02.07.02.002-7, 02.07.03.002-2, 003-0 (82 nomes com fila) | exame compatível | 004-6 | compatíveis na ficha |
| TC 02.06.01.001-0, 002-8, 003-6, 02.06.02.001-5, 002-3, 02.06.03.002-9, 003-7 (108 nomes) | exame compatível | 003-8 | compatíveis na ficha |
| radiografias, 20 códigos (87 nomes) | exame compatível | as quatro | compatíveis na ficha |
| CONSULTA EM ORTOPEDIA - COLUNA, JOELHO, OMBRO, PE/TORNOZELO, QUADRIL, MAO, PEDIATRIA, TUMORES | consulta | as quatro | consulta 03.01.01.007-2, compatível; a pediatria entra porque a ficha vai de 0 a 130 anos |

**A decidir** (fora da soma até a conversa principal decidir):

| fila | tamanho | estudo |
|---|---|---|
| CONSULTA EM ORTOPEDIA E TRAUMATOLOGIA | 6.794 na fila, 6.786 pessoas, 5.195 devolvidas, espera 264 dias; com CID 746 (001-1), 156, 62, 300 | **fila genérica**: está no teto acima, marcada; só a finalidade a levaria à OCI |
| CONSULTA EM ORTOPEDIA - GERAL | 2 na fila (2019) | fila genérica, resíduo |
| **CONSULTA EM REUMATOLOGIA - GERAL** (achado novo) | 12.083 na fila; com CID 614 (001-1), 39 (002-0), 7 (003-8), 23 (004-6) | consulta médica 03.01.01.007-2, compatível pelo código; a ficha é de ortopedia; **não somada** |

**Fica fora:**

| fila | com o CID da OCI | motivo |
|---|---|---|
| CONSULTA EM FISIOTERAPIA/REABILITACAO ORTOPEDICA/REUMATOLOGICA (24.234 na fila) | 2.200 (001-1), 498 (002-0), 85 (003-8), 1.394 (004-6) | 03.01.01.004-8, não é consulta médica nem compõe a OCI |
| CONSULTA EM TERAPIA OCUPACIONAL - ORTOPEDIA MMSS (3.316) | 96, 297, 26, 478 | idem |
| CONSULTA EM ACUPUNTURA (4.757) | 153 (001-1), 57 (002-0), 95 (004-6) | não é ortopedia |
| CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO (9.712) | 58 (001-1), 32 (004-6) | cardiologia |
| US de articulação com CID de outra OCI | ombro D e E 268 + 194 (004-6); joelho 71 + 67 (001-1); coxo-femural infantil 50 + 48 (001-1) e 48 + 45 (003-8); coluna lombar 101 (003-8) | a US não compõe a 001-1, a 003-8 nem a 004-6 |
| RM de joelho com CID da 001-1 (M17) | 95 + 87 | a RM não compõe a 001-1, e a 004-6 não aceita M17 |
| eletroneuromiografia, cintilografia óssea, genética, neurologia | 6 a 15 cada | não compõem |

## 6. Por Região de Saúde — medida fila, pessoas

Região da unidade solicitante. URD e Contratado/Credenciado não são Região de Saúde. A linha sem
região fica à parte, sem rateio; as linhas não somam o total (quem tem pedido de duas regiões conta
nas duas).

| Região | US articulação | US no CID 002-0 | consultas de ortopedia | consultas no CID 001-1 | RM (6 códigos) | RM no CID 004-6 | TC (7 códigos) | TC no CID 003-8 | união dos quatro tetos |
|---|---|---|---|---|---|---|---|---|---|
| Central | 50 | 0 | 2.498 | 208 | 256 | 2 | 173 | 0 | 296 |
| Centro-Sul | 2.212 | 221 | 3.948 | 327 | 465 | 17 | 82 | 0 | 791 |
| Leste | 2.165 | 180 | 5.580 | 522 | 585 | 11 | 180 | 1 | 900 |
| Norte | 421 | 20 | 5.489 | 550 | 617 | 31 | 298 | 0 | 920 |
| Oeste | 1.302 | 49 | 6.042 | 595 | 719 | 13 | 203 | 1 | 957 |
| Sudoeste | 3.740 | 88 | 9.872 | 950 | 1.101 | 31 | 1.896 | 3 | 1.593 |
| Sul | 1.440 | 93 | 6.415 | 579 | 602 | 32 | 301 | 0 | 915 |
| URD | 1 | 0 | 1.674 | 178 | 677 | 47 | 1.598 | 1 | 267 |
| Contratado/Credenciado | 6 | 0 | 762 | 76 | 229 | 2 | 650 | 0 | 96 |
| Serviços Centralizados / Público não SES | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| **sem região informada** | **129** | **1** | **1.888** | **533** | **89** | **2** | **40** | **0** | **852** |

## 7. As outras unidades do tipo "Privado"

Agendamentos de 29/04/2026 em diante (por mês, aba 11). Nenhuma agenda ortopedia, cardiologia,
ginecologia ou otorrino.

| unidade (código) | o que agenda | desde 29/04 | de 26/10 em diante |
|---|---|---|---|
| CLINICA SANTA RITA CEMTRA (9530827) e PoliCl Sta Rita (5814413) | consulta de oftalmologia geral, desde 25 e 28/05/2026 | 19.212 + 19.584 | 467 + 1.270 |
| HODF (0255416) | oftalmologia, catarata pré-operatório | 1.052 | 45 |
| CENTRO CLINICO JARDIM BOTANICO (9710248) | catarata pré-operatório (até 21/08/2026) | 413 | 0 |
| Hosp Anchieta (3030121) | RM | 2.585 | 91 |
| Infinita (6490883) e Rio Preto / Infinita Assistência (7719531) | RM | 2.745 + 1.761 | 46 + 49 |
| RA ED Prime (0242047) e Sabin Vega (9411887) | mamografia de rastreamento | 959 + 40 | 0 |
| Radiologia Anchieta / Sabin (3098230) | core biópsia de mama guiada por US | 30 | 0 |
| Aliança (9024654, 7025378) e Cettro (9626670) | oncologia e radioterapia | 58 + 71 + 45 | 0 |
| OFTALMED (9896791) | nada desde 29/04 | 0 | 0 |

## 8. Diferença para coletas anteriores

Não há coleta anterior deste recorte (sobreposição com o IEV). Duas comparações:
- **Coleta de imagem de hoje** (`mapa_social_20261026.md`, mesma recarga): US de articulação 14.391,
  10.396 viva, 11.435 pessoas, 547 dias; RM e TC por código: os mesmos números.
- **Coleta de cardiologia de 22/10/2026** (redacao_08, seção 6): nas duas unidades privadas, risco
  cirúrgico 1.937 até 21/10 + 406 marcadas = 2.343; hoje, 2.822 de 29/04 a 23/11 (+479). Consulta
  adulto 822 + 73 = 895; hoje 1.138 (+243). A diferença é agenda nova de outubro e novembro e a
  recarga; o desenho é o mesmo. A 22/10 não sabia que as consultas de ortopedia das duas eram as
  mesmas do Gama nem o peso delas no DF.

## 9. Lacunas

- **Convênio e CNES:** o painel dá código, nome curto e tipo da unidade, não o convênio. Os códigos
  0366986, 3031543 e 9180168 têm a forma de CNES; confirmar no CNES ou com a SES que são do IEV.
- **Exame feito dentro da OCI:** não passa pelo SISREG nas unidades do IEV; o painel não mede a US,
  a RM, a TC, a radiografia nem os exames cardiológicos que o IEV entrega.
- **APAC e CID da OCI:** o painel não traz a APAC; não se sabe quantas consultas viraram OCI, nem com
  que CID, nem quantas OCI de cada código.
- **DOA × DOAR:** o painel não separa os dois convênios de ortopedia; a divisão 38.594 + 14.192 (e as
  outras) não se verifica aqui.
- **RM de Sobradinho e do Gama:** contrato anterior ao termo; não dá para separar uma eventual RM do
  IEV dentro dela.
- **Data:** é a do atendimento marcado, não a do dia da marcação; "de 26/10 em diante" é o que já está
  na agenda até 26/11/2026.
- **CID de três caracteres:** a lista da ficha tem a categoria sem subitem (M15, M16, M65, Q65...);
  contou-se igual. Subcategoria que a ficha não lista ficou fora (98 pedidos de M65 na US).
- **Idade:** a ficha vai de 0 a 130 anos; sem recorte. É a idade na solicitação.
- **Entrantes por mês:** não coletados (a pergunta é de sobreposição, não de dimensionamento).
- **Motivo das devolvidas e das faltas:** o painel não traz.
