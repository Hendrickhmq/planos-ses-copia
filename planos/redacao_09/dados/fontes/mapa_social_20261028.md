# Mapa Social da Saúde — saúde mental infantojuvenil (COMPP e Adolescentro), coleta de 28/10/2026

Estudo de estruturação do redacao_09. O objeto não é procedimento SIGTAP nem OCI: não há
ficha nem lista de CID, e o recorte é pelo nome da fila no SISREG. A pergunta: que filas
reguladas levam aos ambulatórios de saúde mental infantojuvenil da atenção secundária, o
COMPP (até 11 anos e 11 meses) e o Adolescentro (12 a 17 anos e 11 meses), para
transtornos moderados (NT SEI-GDF nº 1/2018 - SES/SAIS/COASIS/DISSAM).

| campo | conteúdo |
|---|---|
| Fonte | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas · `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` · app Qlik `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` · dados SISREG/DATASUS |
| Última recarga da base | 28/10/2026 08:33:57 (qLastReloadTime 2026-10-28T11:33:57.238Z) |
| Consulta | 28/10/2026 10:13:20 a 10:24:12 (relógio do motor), sem recarga no meio |
| Solicitação mais recente na base | 27/10/2026 (agendamento mais distante: 04/02/2027) |
| Medida | **fila** = os três status: pendente de regulação, corrigida e reenviada para regulação, pendente de regulação por fila de espera. Devolvidas para complementação ficam fora e são contadas à parte |
| Recorte | todos os anos; cada fila fixa na expressão de conjunto pelo nome exato (`descrição_procedimento_solicitacao`) |
| Via | Qlik Engine API pelo navegador embutido; sem leitura de tela e sem exportação |

Pessoas = CNS distintos no conjunto (quem espera em mais de uma fila conta uma vez); só a
contagem sai do motor. Espera em dias, calculada no motor sobre os registros. Idade = idade
na solicitação (`idade_solicitacao`), não a de hoje.

## Resposta curta

O painel **tem** as filas desse caminho, com nome próprio desde dezembro de 2025:
`CONSULTA EM SAUDE MENTAL - PEDIATRIA` e `CONSULTA EM SAUDE MENTAL - ADOLESCENTE`
(as duas no código 03.01.01.004-8). Juntas, **4.377 pedidos na fila, 4.373 pessoas**,
espera mediana de 193,7 dias. Antes delas a demanda corria numa fila genérica,
`CONSULTA DE PROFISSIONAIS DE NIVEL SUPERIOR NA ATENCAO ESPECIALIZADA (EXCETO MEDICO)`,
que parou de receber pedidos em 27/11/2025 e ainda guarda 2.209 pedidos (a decidir).

O painel **não mostra** o COMPP nem o Adolescentro como unidade que atende essas filas: os
agendamentos saem com executante "CRDF" (Complexo Regulador), e 57 da fila pediátrica no
CRETEA. A ligação com os dois serviços se apoia no nome da fila, na faixa etária, no perfil
de CID e no COMPP como unidade solicitante. Não é registro direto (ver Lacunas).

## Varredura das filas

Procurou-se: (1) nomes de fila com PSIQ, PSICO, NEURO, MENTAL, COMPP, ADOLES, INFANT,
JUVENIL, AUTIS, TEA, TDAH, CAPS, COMPORT, APRENDIZ, FONO, PEDIAT, HEBIAT, DESENVOLV, TERAPIA
OCUP e ORIENTA entre as 1.577 combinações nome × código da base; (2) tudo o que tem COMPP ou
Adolescentro como unidade executante; (3) todas as filas da base com CID F e idade abaixo de
18 anos na fila (aba 2 da planilha).

| fila (nome no SISREG) | código | fila | pessoas | devolvidas | espera média | mediana | máxima | pedido mais antigo | idade na fila | CID F | decisão |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CONSULTA EM SAUDE MENTAL - PEDIATRIA | 03.01.01.004-8 | 1.503 | 1.503 | 507 | 224,8 | 181,7 | 1.596,8 | 14/06/2022 | 1.503 de 0–11 | 1.355 | **entra** |
| CONSULTA EM SAUDE MENTAL - ADOLESCENTE | 03.01.01.004-8 | 2.874 | 2.870 | 191 | 286,1 | 199,1 | 1.294,8 | 12/04/2023 | 869 de 0–11; 1.959 de 12–17; 46 de 18+ | 2.576 | **entra** |
| CONSULTA DE PROFISSIONAIS DE NIVEL SUPERIOR NA ATENCAO ESPECIALIZADA (EXCETO MEDICO) | 03.01.01.004-8 | 2.209 | 2.209 | 1.667 | 694,1 | 638,8 | 1.825,9 | 28/10/2021 | 1.190 de 0–11; 649 de 12–17; 370 de 18+ | 1.960 | **a decidir** |
| CONSULTA EM NEUROLOGIA PEDIATRICA | 03.01.01.007-2 | 6.203 | 6.203 | 3.743 | 329,6 | 318,2 | 896,8 | 14/05/2024 | 4.854 de 0–11; 1.301 de 12–17; 48 de 18+ | 4.217 | fica fora |
| CONSULTA EM NEUROLOGIA - PEDIATRIA | 03.01.01.007-2 | 6 | 6 | 2 | 988,1 | 978,7 | 1.489,7 | 29/09/2022 | 6 de 0–11 | 6 | fica fora |
| CONSULTA EM PSIQUIATRIA - PEDIATRICA | 03.01.01.007-2 | 1 | 1 | 0 | 798,9 | 798,9 | 798,9 | 20/08/2024 | 1 de 0–11 | 0 | fica fora |
| CONSULTA EM PSICOLOGIA - INFANTIL | 03.01.01.004-8 | 1 | 1 | 319 | 2.790,6 | 2.790,6 | 2.790,6 | 08/03/2019 | 1 de 12–17 | 1 | fica fora |
| CONSULTA EM PSICOLOGIA - PEDIATRICA | 03.01.01.007-2 | 1 | 1 | 0 | 1.643,9 | 1.643,9 | 1.643,9 | 28/04/2022 | 1 de 12–17 | 1 | fica fora |
| CONSULTA EM PSICOLOGIA | 03.01.01.004-8 | 2.463 | 2.463 | 198 | 920,6 | 936,6 | 2.393,7 | 08/04/2020 | 37 de 12–17; 2.426 de 18+ | 2.125 | fica fora |
| ­CONSULTA EM PSICOLOGIA (com U+00AD no início) | 03.01.01.004-8 | 3.427 | 3.427 | 869 | 1.119,5 | 1.149,7 | 2.393,7 | 08/04/2020 | 3 de 0–11; 3.424 de 18+ | 3.070 | fica fora |
| CONSULTA EM PSIQUIATRIA - GERAL | 03.01.01.007-2 | 12.147 | 12.131 | 8.954 | 810,0 | 621,8 | 2.932,9 | 17/10/2018 | 1 de 12–17; 12.146 de 18+ | 11.118 | fica fora |
| CONSULTA EM PSIQUIATRIA - PERINATAL | 03.01.01.007-2 | 971 | 971 | 163 | 234,1 | 235,9 | 475,6 | 09/07/2025 | 27 de 12–17; 944 de 18+ | 683 | fica fora |
| CONSULTA EM HEBIATRIA | 03.01.01.007-2 | 0 | 0 | 10 | — | — | — | — | — | 0 | fica fora |
| CONSULTA EM REABILITACAO INTELECTUAL - INFANTIL | 03.01.01.004-8 | 15.082 | 14.932 | 778 | 555,8 | 548,0 | 1.362,6 | 03/02/2023 | 13.143 de 0–11; 1.938 de 12–17; 1 de 18+ | 14.097 | fica fora |
| CONSULTA EM REABILITACAO INTELECTUAL  - ADULTO (dois espaços) | 03.01.01.004-8 | 2.587 | 2.580 | 143 | 430,2 | 411,7 | 1.685,9 | 17/03/2022 | 1.111 de 12–17; 1.476 de 18+ | 2.280 | fica fora |
| CONSULTA EM FONOAUDIOLOGIA - LINGUAGEM | 03.01.01.004-8 | 10.684 | 10.682 | 1.308 | 556,7 | 498,9 | 1.771,6 | 21/12/2021 | 8.847 de 0–11; 1.600 de 12–17; 237 de 18+ | 9.078 | fica fora |
| CONSULTA EM FONOAUDIOLOGIA INFANTIL | 03.01.01.004-8 | 1.059 | 1.059 | 168 | 478,2 | 443,0 | 1.302,9 | 04/04/2023 | 1.059 de 0–11 | 914 | fica fora |
| CONSULTA EM TERAPIA OCUPACIONAL - REABILITACAO INFANTIL | 03.01.01.004-8 | 966 | 966 | 102 | 719,8 | 799,6 | 1.539,0 | 11/08/2022 | 876 de 0–11; 90 de 12–17 | 805 | fica fora |
| CONSULTA EM PEDIATRIA - ESTIMULACAO PRECOCE | 03.01.01.006-4 | 114 | 114 | 23 | 402,0 | 258,7 | 1.568,7 | 12/07/2022 | 114 de 0–11 | 37 | fica fora |

**Motivo de cada decisão:**
- **Entram** as duas filas de saúde mental: o nome e a faixa etária batem com o COMPP
  (pediatria, só 0–11) e o Adolescentro; o CID é quase todo F (90% e 90%); o COMPP é
  solicitante na fila do adolescente (150 pedidos na fila e 525 agendados). Começaram a ser
  agendadas em 01/12/2025, no mesmo dia em que a fila genérica parou.
- **A decidir**, a fila `NIVEL SUPERIOR (EXCETO MEDICO)`: é a fila anterior do mesmo
  caminho (89% CID F, 83% com menos de 18 anos, o COMPP solicitante de 1.642 dos 13.930
  agendamentos, último pedido em 27/11/2025, último agendamento em 01/12/2025). O que resta
  nela são 2.209 pedidos antigos, mediana de 638,8 dias, e 1.667 devolvidas. Pode ser
  estoque herdado da mesma demanda ou resto que não migrou. **Não entra na soma**: vai como
  achado. Só 90 pessoas estão nela e numa das filas novas.
- **Ficam fora:** neurologia pediátrica (consulta médica de neuropediatria; o CID F é
  frequente, mas é outro serviço e outro executante); psiquiatria e psicologia pediátricas
  e infantis (filas extintas ou de um pedido só); psicologia e psiquiatria gerais e
  perinatal (adultos); hebiatria (sem fila); reabilitação intelectual, fonoaudiologia,
  terapia ocupacional e estimulação precoce (reabilitação e desenvolvimento, rede
  CER/TEA, fora do ambulatório de transtorno moderado).

**O que o painel registra no COMPP e no Adolescentro como executante** (todos os anos):
no COMPP, eletroencefalograma (3.390 agendados, até 12/12/2023), audiometria até 7 anos
(115, 2016–2017), neurologia adulto (200, até 24/11/2023) e geriatria (92, até 30/03/2021);
no Adolescentro, dermatologia (1.454, 2020), urologia (125, 2020) e neurologia pediátrica
(12, 2016). Nenhuma consulta de saúde mental.

## O núcleo: as duas filas de saúde mental

| | SAUDE MENTAL - PEDIATRIA | SAUDE MENTAL - ADOLESCENTE | as duas (motor) |
|---|---|---|---|
| fila (pedidos) | 1.503 | 2.874 | 4.377 |
| pessoas | 1.503 | 2.870 | 4.373 |
| devolvidas (fora da fila) | 507 | 191 | 698 |
| espera média (dias) | 224,8 | 286,1 | 265,0 |
| espera mediana (dias) | 181,7 | 199,1 | 193,7 |
| espera máxima (dias) | 1.596,8 | 1.294,8 | 1.596,8 |
| pedido mais antigo na fila | 14/06/2022 | 12/04/2023 | 14/06/2022 |
| pessoas de 0 a 11 anos | 1.503 | 867 | 2.370 |
| pessoas de 12 a 17 anos | 0 | 1.957 | 1.957 |
| pessoas de 18 anos ou mais | 0 | 46 | 46 |
| pedidos com CID F | 1.355 | 2.576 | — |
| agendados desde 01/12/2025 | 924 (867 CRDF, 57 CRETEA) | 2.216 (CRDF) | — |

Nenhuma pessoa está nas duas filas ao mesmo tempo. Com a fila genérica (a decidir), o
conjunto das três no motor seria 6.586 pedidos, 6.492 pessoas (3.519 de 0–11, 2.560 de
12–17, 413 de 18+), mediana de 337,9 dias.

**Classificação de risco (pedidos na fila):**

| | Prioridade 1 | Prioridade 2 | Prioridade 3 | Prioridade 4 |
|---|---|---|---|---|
| SAUDE MENTAL - PEDIATRIA | 4 | 1.238 | 180 | 81 |
| SAUDE MENTAL - ADOLESCENTE | 595 | 2.047 | 159 | 73 |
| NIVEL SUPERIOR (a decidir) | 242 | 1.840 | 92 | 35 |

**CID principais (pedidos na fila):**
- PEDIATRIA: F84 320, F840 219, F90 151, F900 149, F913 57, F81 41, F98 38, F41 36.
- ADOLESCENTE: F84 340, F900 292, F90 275, F840 177, F41 176, F411 118, F98 105, F32 99.
- NIVEL SUPERIOR: F84 328, F90 257, F840 190, F900 181, F81 128, F41 103, F80 71.

O espectro autista (F84) e o TDAH (F90) são a maior parte nas duas filas. Na do adolescente
aparecem também ansiedade (F41) e depressão (F32).

### Região de Saúde (do solicitante), na medida da fila

| Região de Saúde | PEDIATRIA fila | PEDIATRIA pessoas | ADOLESCENTE fila | ADOLESCENTE pessoas | as duas, fila (motor) | as duas, pessoas (motor) |
|---|---|---|---|---|---|---|
| Central | 36 | 36 | 278 | 278 | 314 | 314 |
| Centro-Sul | 133 | 133 | 263 | 262 | 396 | 395 |
| Leste | 175 | 175 | 442 | 442 | 617 | 617 |
| Norte | 273 | 273 | 454 | 452 | 727 | 725 |
| Oeste | 370 | 370 | 513 | 513 | 883 | 883 |
| Sudoeste | 349 | 349 | 572 | 572 | 921 | 921 |
| Sul | 134 | 134 | 290 | 289 | 424 | 423 |
| URD (referência distrital) | 5 | 5 | 18 | 18 | 23 | 23 |
| Contratado/Credenciado | 0 | 0 | 1 | 1 | 1 | 1 |
| **sem região** | 28 | 28 | 43 | 43 | 71 | 71 |
| **total** | 1.503 | 1.503 | 2.874 | 2.870 | 4.377 | 4.373 |

A linha "sem região" é solicitante sem Região de Saúde no painel: não foi rateada. A
mediana de espera e as devolvidas por região estão na aba 4 da planilha.

### Entrantes e oferta por mês (calculado: abertas + agendadas pelo mês da solicitação)

| mês | PEDIATRIA entrantes | PEDIATRIA agendadas no mês | ADOLESCENTE entrantes | ADOLESCENTE agendadas no mês |
|---|---|---|---|---|
| 2025-12 | 93 | 106 | 136 | 156 |
| 2026-01 | 156 | 57 | 241 | 295 |
| 2026-02 | 115 | 82 | 321 | 154 |
| 2026-03 | 161 | 82 | 375 | 251 |
| 2026-04 | 109 | 73 | 300 | 240 |
| 2026-05 | 145 | 83 | 201 | 165 |
| 2026-06 | 177 | 111 | 187 | 165 |
| 2026-07 | 211 | 52 | 245 | 245 |
| 2026-08 | 211 | 111 | 295 | 170 |
| 2026-09 | 244 | 53 | 287 | 215 |
| 2026-10 (incompleto) | 168 | 84 | 214 | 158 |

Entrantes = pedidos abertos (todos os status da tabela de solicitações) + agendados, pelo
mês da solicitação; a soma é calculada fora do motor. "Agendadas no mês" = agendamentos
pelo mês do agendamento, do motor. As filas carregam pedidos com data de 2022 a 2025, mas
nenhum agendamento antes de 01/12/2025. Por isso a série útil começa em dezembro de 2025. A
série desde 2021, com a fila genérica, está na aba 6.

## Lacunas

1. **O executante não aparece.** Os agendamentos das duas filas saem com executante "CRDF"
   (Complexo Regulador em Saúde do DF, CNES 3044432), e 57 da pediátrica no CRETEA. O
   painel não diz quantos foram atendidos no COMPP, no Adolescentro ou em outro serviço.
   A ligação da fila com os dois serviços se apoia no nome, na idade, no CID e no COMPP
   como solicitante. Não é registro direto.
2. **Moderado ou grave:** o painel não separa a gravidade da NT 1/2018. A classificação de
   risco do SISREG (acima) é prioridade de regulação, não gravidade clínica.
3. **Idade na fila do adolescente:** 869 pedidos (867 pessoas) têm de 0 a 11 anos na
   solicitação, e 46 têm 18 ou mais. O painel não diz se é erro de encaminhamento, idade
   limítrofe ou outra regra de entrada.
4. **Demanda fora do SISREG:** acesso direto, CAPSi e retornos internos dos serviços não
   passam por estas filas e não aparecem no painel.
5. **A fila genérica (a decidir):** não se sabe se os 2.209 pedidos ainda vivos nela são da
   mesma demanda e devem migrar, ou resto de outras especialidades não médicas. 370 deles
   são de adultos.
6. Não há coleta anterior deste objeto: sem coluna de diferença.

## Arquivos

- `mapa_social_20261028.xlsx`: Leia-me; 1 varredura das filas; 2 varredura CID F em
  menores de 18 (todas as filas da base); 3 uniões no motor; 4 Região de Saúde; 5 CID
  principais; 5b classificação de risco; 6 entrantes e oferta (calculado); 7 agendadas por
  status; 8 a 11 unidades executantes e solicitantes.
- `mapa_social_20261028_bruto/`: `coleta_20261028.json` (saída do motor, medida da fila e
  nomes internos exatos), `montar_20261028.py` e `README.md`.
