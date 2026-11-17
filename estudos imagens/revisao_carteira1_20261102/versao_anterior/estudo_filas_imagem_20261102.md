# Estudo das filas de imagem para decidir o plano 4 — relatório de decisão

**Controle interno, 02/11/2026; revisto no mesmo dia.** Nada daqui vai ao plano nem aos parceiros sem decisão do
usuário. A nova versão do plano de trabalho vem depois da escolha da carteira.

**O que as revisões de 02/11 mudaram**, por decisão do usuário:
- o redacao_07 está no campo das ideias e não cobre fila;
- o foco é ultrassom e TC; a radiologia fica mapeada, mas fora;
- só entra exame ambulatorial;
- **a US de articulação fica fora inteira:** a fila está comprometida com a OCI 09.03.01.002-0 do IEV;
- **4.000 transvaginais ficam reservadas** para a OCI GIN1 do IEV.

As duas últimas estão registradas na L-008, em `pendencias.md`, com a pergunta a fazer de novo à regulação da SES.

**Os arquivos, nesta pasta:**
- **a planilha única:** `estudo_filas_imagem_20261102.xlsx`, com dez abas: Quem atende o quê, Inventário, Rumo por
  código (com os meses para zerar), Cobertura, Viabilidade, Carteiras, Crescimento e faltas, v26 pela Candanga, Quem
  oferta e Fontes;
- **a cópia organizada, para ler e mostrar:** `estudo_filas_imagem_20261102_organizada.xlsx`. Ela tem o Painel
  (gráficos de onde cai cada pedido de hoje), o Rumo das filas com os 133 códigos de imagem e a situação de cada um
  no plano 4, e a aba Filas, uma linha por fila, com as carteiras que a usam numa coluna só. Rumo, Filas, Quem oferta
  e Viabilidade são tabelas do Excel, com filtro e ordem em cada coluna e um total que muda com o filtro;
- **o script que gera tudo:** `estudo_filas_imagem_20261102.py`;
- **o estudo separado dos outros planos:** `estudo_outros_planos_imagem_20261102.md`, com a planilha dele.

```bash
python3 planos/redacao_04/estudos/estudo_filas_imagem_20261102.py planos/redacao_04/dados/fontes/mapa_social_20261102_imagem_bruto/coleta_20261102.json <tabela_sus_candanga.csv do main> planos/redacao_04/dados/fontes/mapa_social_20261102_executante_bruto/coleta_20261102.json
```

## 1. A decisão em uma página

**Só entram carteiras que chegam ao valor dos exames da v26** (R$ 10.636.542,52; decisão do usuário, 02/11). São
cinco. Todas ficam sem a US de articulação, comprometida com o IEV, e com 4.000 transvaginais reservadas a ele.

| | **1 (recomendada)** | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| o que leva | **parede, sem angio coronária, pedidos novos** | parede e angio coronária | sem parede, com angio coronária e pedidos novos | a v26 como está, mais TC e pedidos novos (parede e angio coronária, como na v26) | a v26 como está, mais TC e pedidos novos, sem angio coronária |
| quando usar | a SES aceita a parede | a SES aceita a parede, e você aceita a angio coronária | a SES não aceita a parede | para mudar o mínimo do texto assinado | idem, sem a angio coronária |
| exames | **79.219** | 76.657 | 76.533 | 75.903 | 78.924 |
| valor dos exames | **R$ 10.636.506,41** | R$ 10.636.499,05 | R$ 10.636.507,81 | R$ 10.636.523,39 | R$ 10.636.529,66 |
| pedidos novos esperados | 1.490 | 0 | 576 | 2.277 | **6.842** |
| códigos | 17 | 17 | 17 | 14 | 14 |
| uso das 13 salas de ultrassom | 137% | 132% | 129% | 126% | 138% |

**A carteira 1 (recomendada): 79.219 exames e R$ 10.636.506,41.** São R$ 36 a menos que o valor da v26.
- O apoio de R$ 956.160,00 fica como está, e o total cabe no recurso.
- **A carteira leva:**
  - toda a fila elegível de hoje de ultrassom e TC, menos a angio coronária;
  - a parede abdominal no código do abdômen total;
  - **1.490 pedidos novos esperados** nas filas que não zeram;
  - o limite dos pedidos novos é o saldo por mês × 8 meses.

**A v26 com mais TC (carteiras 4 e 5), que você pediu para mapear.** A lógica é manter o mix da v26, código por
código, até onde a fila de hoje deixa, e usar o resto do valor em TC.
- **A TC livre acaba antes de fechar o valor.** Faltam R$ 348 mil com a angio coronária e R$ 825 mil sem ela. Por isso
  as duas só chegam ao valor com pedidos novos esperados.
- **A carteira 4 (com a angio coronária, como na v26)** precisa de 2.277 pedidos novos.
- **A carteira 5 (sem a angio coronária)** precisa de 6.842, 9% da carteira. É a que mais depende de pedido que
  ainda não existe.
- **As duas não usam os seis códigos que eram do redacao_07** (crânio e pescoço entram como TC a mais). São as que
  mudam menos o texto assinado.

| código | exame | v26 | **1** | 2 | 3 | 4 | 5 |
|---|---|---:|---:|---:|---:|---:|---:|
| 02.05.01.004-0 | Doppler (carótidas, membros, renais) | 14.508 | **16.770** | 16.770 | 16.770 | 14.508 | 16.884 |
| 02.05.02.004-6 | Abdômen total (com a parede nas carteiras 1, 2, 4 e 5) | 13.166 | **13.651** | 13.651 | 10.347 | 14.160 | 15.296 |
| 02.05.02.009-7 | Mama bilateral | 14.689 | **12.950** | 12.950 | 12.950 | 12.952 | 12.952 |
| 02.05.02.018-6 | Transvaginal (sem os 4.000 do IEV) | 10.541 | **5.294** | 2.690 | 5.294 | 5.294 | 5.294 |
| 02.05.02.005-4 | Aparelho urinário | 3.944 | **4.657** | 4.025 | 4.025 | 4.594 | 4.594 |
| 02.05.02.012-7 | Tireoide | 3.216 | **3.854** | 3.854 | 3.854 | 3.216 | 4.087 |
| 02.05.02.010-0 | Próstata por via abdominal | 3.201 | **2.969** | 2.969 | 2.969 | 2.971 | 3.153 |
| 02.05.02.003-8 | Abdômen superior | 2.261 | **2.327** | 2.213 | 2.247 | 2.343 | 2.343 |
| 02.05.02.007-0 | Bolsa escrotal | — | **1.136** | 934 | 934 | — | — |
| 02.05.02.016-0 | Pélvica | — | **1.014** | 1.014 | 1.014 | — | — |
| 02.05.02.017-8 | Transfontanela | — | **293** | 270 | 293 | — | — |
| 02.06.03.001-0 | TC de abdômen superior | 4.516 | **5.349** | 5.031 | 5.349 | 5.349 | 5.349 |
| 02.06.03.003-7 | TC de pelve | 3.862 | **4.141** | 3.942 | 4.141 | 4.141 | 4.141 |
| 02.06.02.003-1 | TC de tórax, sem a angio coronária (na v26, com ela) | 5.240 | **3.215** | 3.215 | 3.215 | 3.232 | 3.232 |
| 02.06.02.003-1 | Angio coronária (mesmo código da TC de tórax) | (na linha acima) | **—** | 1.532 | 1.532 | 1.544 | — |
| 02.06.01.007-9 | TC de crânio | — | **801** | 801 | 801 | 801 | 801 |
| 02.06.01.005-2 | TC de pescoço | — | **659** | 657 | 659 | 659 | 659 |
| 02.06.01.004-4 | TC de face | — | **139** | 139 | 139 | 139 | 139 |
| | **total** | **79.144** | **79.219** | **76.657** | **76.533** | **75.903** | **78.924** |

**Prioridade do usuário (02/11): não atender a angio coronária.** Ficam de pé as carteiras 1 e 5. A 2, a 3 e a 4
levam a angio e só servem se essa prioridade mudar.

**Por que a carteira 1 continua a recomendada:**
- é a que fecha sem a angio coronária e com poucos pedidos novos (1.490, 2%);
- a carteira 5 também fica sem a angio coronária, mas precisa de 6.842 pedidos novos e deixa de fora a bolsa escrotal,
  a pélvica e a transfontanela, que estão em déficit;
- a parede abdominal (3.304 exames, R$ 388 mil) depende da SES (L-007). Se ela não aceitar, vale a carteira 3.

**As faltas:** com 20% de faltas, a carteira 1 precisa agendar 99.025 vezes para fazer 79.219 exames. A fila
elegível de hoje e o crescimento líquido das filas somam 86.166 pedidos. Os 12.884 que faltam são 12% do que entra
nessas filas em 8 meses. A regulação precisa mandar ao plano essa parte das entradas (seção 3.2).

## 2. As fontes

| o quê | de onde |
|---|---|
| Inventário de todas as filas de imagem | Mapa Social, recarga de 02/11/2026 às 10h31; agente `mapa-social`, conferência 9/9. `dados/fontes/mapa_social_20261102_imagem.*` |
| Oferta por unidade executante | a mesma base, nos cinco códigos de maior peso. `dados/fontes/mapa_social_20261102_executante.*` (9/9) |
| Oferta por unidade: eco transtorácica, globo ocular e bolsa escrotal | recarga das 16h31. `dados/fontes/mapa_social_20261102_executante_b.*` (9/9). O globo ocular só tem o CRDF; a eco é sustentada pelo ICDF (57%); a bolsa escrotal está espalhada em 12 hospitais regionais |
| Transvaginal × CID da GIN1 | recarga das 12h31. `dados/fontes/mapa_social_20261102_gin1.*` (10/10) |
| Preço | o Anexo Único da Candanga (SEI 212117347), modalidade SIA, do `main`; vale o SIGTAP quando é igual ou maior (LI-002) |
| Metas e preços da v26 | `plano.md`, 2.2 e 8.2 |
| Outros planos | `estudo_outros_planos_imagem_20261102.md` (os planos aprovados do acervo) |
| Custo | `custo_por_exame_v2_20261020.xlsx` (premissas) e a rede de TC do ISHP (cotado) |
| Capacidade | `salas_ultrassom_metricas_20261020.xlsx` e `estudo_polos_rede_capacidade_20261020.md` |
| Tempos | CBR 2017 no ultrassom; intervalos do plano 4 na TC (`output/estudo_imagem_candanga_20261101.xlsx`, aba 6) |

Só entram dados agregados, sem CPF nem CNS. As coletas originais estão preservadas nas pastas brutas.

## 3. O inventário e o rumo de cada código

**656 filas de imagem** (nome exato × código), em 133 códigos e sem corte de tamanho. Somar filas não dá pessoas
únicas.

| modalidade | filas | pedidos | na fila viva (24 meses) | pessoas | no estudo |
|---|---:|---:|---:|---:|---|
| Ultrassom | 151 | 99.169 | 74.069 | 79.673 | **foco** |
| Tomografia | 196 | 21.269 | 21.039 | 11.599 | **foco** |
| Radiologia | 174 | 14.093 | 14.022 | 12.748 | mapeada, fora do foco (seção 3.1) |
| Ressonância | 109 | 10.149 | 10.142 | 7.690 | fora: outro equipamento |
| Medicina nuclear | 24 | 5.663 | 5.663 | 4.178 | fora: outro equipamento |
| Radiologia intervencionista | 2 | 9 | 9 | 9 | fora |

**Como ler:**
- A fila são os três status pendentes. As devolvidas ficam ao lado, sem subtrair uma da outra (decisão de 02/11).
- O rumo é **por código**, porque a rede oferta o exame e um código junta muitos nomes de fila. É uma estimativa
  por entradas e agendamentos, e não a queda observada do estoque.
- A falta (faltas ÷ realizados + faltas) serve ao estudo e não vai ao plano: o absenteísmo é tratamento interno.

**Só ambulatório.**
- As 86 filas com "EMERG" no nome (4.697 pedidos, quase todas de TC) ficam fora (D-009).
- Conferi os nomes: nenhuma fila de urgência, internado ou pronto-socorro ficou sem essa marca.
- A TC com sedação fica fora porque pede anestesia.

**A regra das classes**, revista em 02/11, considera **quanto tempo a fila leva para zerar**. Não basta a oferta
cobrir o que entra.
- **O cálculo:** meses para zerar = fila ÷ (oferta por mês − entradas por mês), no ritmo dos 12 meses e no dos 3
  últimos. Se a oferta não passa das entradas, a fila não zera.
- **As classes:**
  - **capacidade da SES:** a SES zera a fila no ritmo dos 12 meses dentro do prazo do plano (8 meses);
  - **zera devagar:** zera, mas leva mais que 8 meses;
  - **esforço pontual:** mutirão (o maior mês passa de 2,5 vezes a média do ano), e, acabado o esforço, a fila não
    zera;
  - **déficit persistente:** não zera, ou levaria mais de dois anos mesmo no ritmo dos 3 últimos meses;
  - **inconclusivo:** não zera no ritmo dos 12 meses, mas zeraria em até dois anos no dos 3 últimos.

| código | fila | entram por mês | oferta por mês (12 m; 3 últimos) | meses para zerar (12 m; 3 últimos) | estoque em meses de oferta | classe |
|---|---:|---:|---|---|---:|---|
| Doppler 02.05.01.004-0 | 16.844 | 1.359 | 1.053; 1.100 | não zera; não zera | 16,0 | déficit persistente |
| Abdômen total 02.05.02.004-6 | 13.656 | 1.155 | 889; 1.169 | não zera; 981 | 15,4 | déficit persistente |
| Mama 02.05.02.009-7 | 12.952 | 913 | 815; 1.777 | não zera; 15 (só com o mutirão) | 15,9 | esforço pontual |
| Transvaginal 02.05.02.018-6 | 9.295 | 1.260 | 1.467; 2.064 | **45; 12** | 6,3 | **zera devagar** |
| TC de abdômen superior 02.06.03.001-0 | 6.214 | 1.516 | 1.476; 1.504 | não zera; não zera | 4,2 | déficit persistente |
| TC de tórax 02.06.02.003-1 | 6.043 | 2.488 | 2.463; 2.950 | não zera; 13 | 2,5 | inconclusivo |
| TC de pelve 02.06.03.003-7 | 5.044 | 1.272 | 1.247; 1.309 | não zera; 135 | 4,0 | déficit persistente |
| Aparelho urinário 02.05.02.005-4 | 4.032 | 481 | 400; 470 | não zera; não zera | 10,1 | déficit persistente |
| Tireoide 02.05.02.012-7 | 3.858 | 408 | 299; 309 | não zera; não zera | 12,9 | déficit persistente |
| Próstata 02.05.02.010-0 | 2.971 | 366 | 343; 312 | não zera; não zera | 8,7 | déficit persistente |
| Abdômen superior 02.05.02.003-8 | 2.229 | 224 | 209; 221 | não zera; não zera | 10,6 | déficit persistente |
| TC de crânio 02.06.01.007-9 | 1.428 | 1.141 | 1.276; 1.363 | **11; 6** | 1,1 | **zera devagar** |
| Pélvica 02.05.02.016-0 | 1.016 | 132 | 116; 132 | não zera; 3.048 | 8,8 | déficit persistente |
| Bolsa escrotal 02.05.02.007-0 | 961 | 95 | 70; 61 | não zera; não zera | 13,8 | déficit persistente |
| TC de pescoço 02.06.01.005-2 | 762 | 201 | 201; 214 | não zera; 59 | 3,8 | déficit persistente |
| TC de face 02.06.01.004-4 | 466 | 430 | 447; 592 | **28; 3** | 1,0 | **zera devagar** |
| Transfontanela 02.05.02.017-8 | 272 | 74 | 71; 76 | não zera; 103 | 3,8 | déficit persistente |

**O que muda com o tempo para zerar:**
- **A transvaginal não está tranquila.** A oferta passa das entradas, mas no ritmo dos 12 meses a fila levaria
  **45 meses** para zerar. Só cai para 12 meses no ritmo dos mutirões de jun. a set., que já acabaram.
- **Nenhuma fila da carteira zera dentro do prazo do plano no ritmo da SES.**
  - As mais próximas são a TC de crânio (11 meses) e a de face (28).
  - A TC de tórax e a de pelve, que pareciam "fluxo coberto", não zeram: a oferta empata com a entrada, e o estoque
    fica parado.
- **O estoque em meses de oferta** é a fila dividida pela oferta mensal da SES, ou seja, quantos meses de toda a
  produção da SES ela representa.
  - No ultrassom, a fila equivale a 9 a 16 meses de produção.
  - Na TC, a 1 a 4 meses.

**O que isso diz para o plano:**
- **No ultrassom, a fila é estoque que cresce.** Zerar a fila tem efeito real, e ela volta devagar.
- **Na TC, a SES empata com a entrada,** sustentada pelo CRDF e por dois contratados, o HUB e o ICDF. O estoque de 2 a
  4 meses fica parado. O plano tira esse estoque, e ele não volta enquanto a oferta da SES se mantiver.
- **Os dois riscos:**
  - a SES atender parte do estoque antes do início do plano; medir de novo na fase 0;
  - faltar pedido para repor as faltas (seção 3.2).

### 3.2 Quanto cada fila cresce, e se dá para repor as faltas

Controle interno. O plano não traz taxa de faltas: o absenteísmo é tratamento interno. A aba Crescimento e faltas tem
a conta por código, para a carteira 1.

**A conta:**
- **Para fazer a meta com faltas,** é preciso agendar meta ÷ (1 − faltas).
- **Os pedidos disponíveis** são a fila elegível de hoje mais o **crescimento líquido** em 8 meses, ou seja, o que
  entra além do que a SES agenda.
- **O que faltar** precisa vir das **entradas do período**: a regulação mandar ao plano parte dos pedidos novos, em
  vez de agendá-los na rede própria.

| | com 20% de faltas | com 30% de faltas |
|---|---:|---:|
| meta da carteira 1 | 79.219 | 79.219 |
| agendamentos necessários | 99.025 | 113.170 |
| pedidos disponíveis (fila elegível 77.976 + crescimento líquido 8.255) | 86.166 | 86.166 |
| **faltam** | **12.884** | **27.004** |
| parte das entradas do período (108.116 em 8 meses) | **12%** | **25%** |

| código | meta | cresce em 8 meses (líquido) | entram em 8 meses | faltas na SES | parte das entradas a pedir (20%; 30%) |
|---|---:|---:|---:|---:|---|
| Doppler | 16.770 | 2.447 | 10.871 | 25% | 15%; 43% |
| Abdômen total | 13.651 | 2.129 | 9.241 | 37% | 14%; 40% |
| **Mama** | 12.950 | 790 | 7.307 | **38%** | **33%; 65%** |
| TC de abdômen superior | 5.349 | 318 | 12.125 | 36% | 11%; 19% |
| Transvaginal | 5.294 | 0 | 10.082 | **43%** | 13%; 22% |
| Aparelho urinário | 4.657 | 651 | 3.848 | 32% | 30%; 51% |
| TC de pelve | 4.141 | 199 | 10.174 | 34% | 10%; 17% |
| Tireoide | 3.854 | 871 | 3.266 | 24% | 3%; 24% |
| TC de tórax | 3.215 | 201 | 19.903 | 33% | 3%; 6% |
| Próstata | 2.969 | 182 | 2.929 | 29% | 19%; 37% |
| Abdômen superior | 2.327 | 114 | 1.789 | 33% | 32%; 55% |
| Bolsa escrotal | 1.136 | 201 | 757 | 35% | 34%; 61% |
| Pélvica | 1.014 | 127 | 1.053 | 38% | 12%; 29% |
| TC de crânio | 801 | 0 | 9.131 | 34% | 2%; 4% |
| TC de pescoço | 659 | 2 | 1.608 | 36% | 10%; 17% |
| Transfontanela | 293 | 23 | 589 | 42% | 12%; 21% |
| TC de face | 139 | 0 | 3.443 | 27% | 0%; 0% |

**O que a tabela mostra:**
- **As faltas da SES estão entre 24% e 43%.** Os 20% a 30% de referência são otimistas para mama, transvaginal e
  abdômen total.
- **Na TC, repor as faltas é fácil:** entram muitos pedidos (12 a 20 mil por código em 8 meses). Basta a regulação
  mandar de 2% a 19% deles.
- **No ultrassom de região isolada (mama, urinário, abdômen superior, bolsa escrotal), é difícil.** Com 30% de
  faltas, a regulação teria de mandar mais da metade do que entra. Com faltas altas, a meta dessas filas fica acima
  do que a fila sustenta.
- **A mama é o caso mais apertado:** 38% de faltas na SES e só 790 de crescimento líquido. Para cumprir 12.950, com
  faltas de 30%, a regulação teria de mandar 65% dos pedidos novos.
- **O que fazer com isso, internamente:**
  - a confirmação na véspera e a busca ativa, que já estão no plano;
  - **combinar com a regulação, no mês 1, que as vagas liberadas por falta voltem para a fila do mesmo exame;**
  - deixar a mama e o ultrassom de região isolada com a meta mais perto do que a fila sustenta. Se for preciso, a
    sobra vai para a TC, que tem pedido de sobra.

### 3.1 Radiologia: mapeada, sem ataque agora

São 172 filas e 14.077 pedidos, sem nenhuma fila de emergência. A aba Inventário tem todas, e a aba Rumo por
código traz a classe de cada código.

| código | exame | fila | classe |
|---|---|---:|---|
| 02.04.03.018-8 | Mamografia bilateral para rastreamento | 6.630 | déficit persistente |
| 02.04.06.002-8 | Densitometria óssea | 2.178 | déficit persistente |
| 02.04.01.017-9 | Radiografia panorâmica (odontológica) | 1.169 | inconclusivo |
| 02.04.01.018-7 | Radiologia periapical (odontológica) | 659 | capacidade da SES |
| 02.04.03.015-3 | Radiografia de tórax | 648 | déficit persistente |
| demais | 167 filas de radiografia simples, de 1 a 314 pedidos cada | 2.793 | — |

- **A mamografia e a densitometria são a demanda que pesa,** quase toda recente.
- **Se um dia entrarem no plano 4,** pedem mamógrafo e densitômetro nos polos: é outro equipamento, e outra conta
  de capacidade.

**As filas pequenas.** Filas livres com menos de 30 pedidos não viram item próprio na carteira. São 57 filas e
250 pedidos de ultrassom e TC, quase todas variantes de nome de um código que já está no plano. Elas aparecem como
"Livre, fila pequena" na aba Filas.

## 4. Cobertura: o que já tem dono

O estudo separado (`estudo_outros_planos_imagem_20261102.md`) lista o que cada plano aprovado contrata, com as
quantidades e a reserva do IEV.

**A aba "Quem atende o quê", a primeira da planilha, junta tudo por código:**
- a situação: livre, parcial ou fora;
- quem atende hoje e quanto contratou;
- a regra para o plano 4;
- os pedidos livres;
- quanto entra em cada carteira.

**Em ultrassom e TC, ficam fora ou divididos por ter dono:**

| motivo | pedidos |
|---|---:|
| **US de articulação: comprometida com a OCI 09.03.01.002-0 do IEV** (L-008 revista, 02/11) | 11.215 |
| D-009: emergência | 4.697 |
| L-008: partes moles (IEV) | 3.140 |
| L-008: TC de coluna, articulações e segmentos (OCI 09.03.01.003-8 do IEV) | 522 |
| **Transvaginal: 4.000 dos 9.295 reservados para a OCI GIN1 do IEV** | 4.000 |
| TC de pelve: os pedidos com CID da OCI 09.03.01.003-8 | 5 a 7 |

**Por que a articulação é tratada como comprometida:**
- **O plano do IEV (pt_ses_02) põe entre os objetivos reduzir as filas reguladas de exame de ultrassom.**
- **Quem escolhe a fila é a regulação.** Ela pode mandar um pedido da fila do exame para uma das 19.070 OCI
  09.03.01.002-0; a OCI faz consulta, exame e retorno.
- **O CID não é barreira.** A APAC sai com o CID que o médico do IEV registra, que pode ser outro que o do pedido.
- **Até 26/10, nenhum agendamento da fila do exame tinha ido ao IEV.** Mas isso é como a regulação vem operando, e
  não uma regra.
- A SES pediu para evitar a sobreposição. A pergunta fica anotada para ser feita de novo.

**Outra equipe ou outro equipamento**, e não por ter dono, ficam fora 17.274 pedidos:
- ecocardiografia (14.669);
- US de globo ocular (1.316);
- obstétricas (561), porque o exame tem o prazo da gestação;
- PET-CT (379);
- TC cone beam (195), que é odontológica;
- paquimetria (144);
- TC com sedação (10), que pede anestesia.

**O redacao_07 não cobre mais nada.** Os códigos que ele tinha separado voltam a ser elegíveis, menos as
obstétricas e o globo ocular. Se ele avançar, terá de excluir o que o plano 4 tomar.

## 5. Viabilidade: preço, custo, tempo e capacidade

A aba Viabilidade tem a conta de cada fila. Os parâmetros:
- **Ultrassom feito por nós:** médico a R$ 100 por hora e sala com aparelho a R$ 5.500 por mês, em 168 horas
  (premissas da `custo_por_exame_v2`), mais R$ 3 de insumo (hipótese). Dá R$ 36,18 por exame de 15 minutos e
  R$ 47,25 por exame de 20.
- **Tomografia na clínica:** R$ 171,44 por exame, com o contraste incluído (cotado na rede de TC do ISHP, de R$ 165
  a R$ 175) contra R$ 251,29 a R$ 309,25 pela Candanga.

**Todo exame da carteira tem margem por hora positiva.**
- **As melhores:** a transfontanela (R$ 505 por hora), as carótidas (R$ 205 por hora) e a transvaginal (R$ 190
  por hora).
- **As mais baixas, que entram pela necessidade da fila e não pelo rendimento:**
  - o Doppler de membros: R$ 36 por hora, porque ocupa a sala 40 minutos;
  - a pélvica: R$ 29 por hora, porque paga R$ 43,41;
  - a mama: R$ 71 por hora.
- **Na TC,** a margem vai de R$ 80 por exame (crânio) a R$ 138 (tórax, abdômen, pelve e pescoço).

**Capacidade em 8 meses, a 80% de 10 horas por dia útil:**

| | v26 | **carteira 1** | carteira 2 | carteira 3 | carteira 4 | carteira 5 | com 13 salas e 6 tomógrafos |
|---|---:|---:|---:|---:|---:|---:|---:|
| horas de ultrassom | 24.260 | **23.906** | 23.009 | 22.576 | 21.933 | 24.159 | 17.472 h → a carteira 1 usa **137%** |
| horas de tomógrafo | 4.478 | **4.739** | 5.332 | 5.505 | 5.517 | 4.745 | 8.064 h → a carteira 1 usa 59% |

- **O ultrassom da carteira 1 exige um pouco menos que a v26,** e o limite já era conhecido:
  - nos tempos do plano, as 13 salas fechadas não bastam; o estudo das salas pede 19;
  - nos 13 minutos do documento da equipe, bastam;
  - o tempo real de cada clínica é o que decide.
- **A tomografia tem folga.** Os exames novos (crânio, pescoço e face) cabem nos mesmos tomógrafos.
- **Custo e tempo:** o ultrassom usa premissas, e o tempo é o intervalo mínimo do CBR, de 2017. A tomografia usa
  preço cotado.

## 6. As carteiras comparadas

As cinco estão na seção 1, com a tabela por código. As saídas, se uma pendência mudar:
- **A SES aceita a parede, e você não quer a angio coronária:** carteira 1.
- **A SES aceita a parede, e você aceita a angio coronária:** carteira 2. Fecha só com a fila de hoje.
- **A SES não aceita a parede:** carteira 3. Precisa da angio coronária.
- **Você prefere mudar o mínimo do texto assinado:** carteira 4, com a angio coronária. A 5 fica sem ela, mas depende
  de 6.842 pedidos novos.
- **A regulação confirma por escrito que a fila de US de articulação não vai para o IEV:** a articulação volta (cerca
  de 10 mil exames e R$ 728 mil), e qualquer carteira fecha com menos pedidos novos.

**O efeito esperado sobre a demanda, na carteira 1:**
- **Ultrassom:** zera a fila elegível de hoje em todos os códigos menos a transvaginal, que fica com a reserva do IEV.
  Doppler, mama, abdômen e as regiões isoladas voltam a crescer depois, porque a SES não dá conta delas.
- **Tomografia:** zera o estoque eletivo de abdômen, pelve, tórax (sem a angio coronária), crânio, pescoço e parte da
  face.

## 7. Pendências que podem mudar a escolha

| # | pendência | o que muda | quem decide |
|---|---|---|---|
| 1 | **L-007:** a parede abdominal no código do abdômen total | sem ela, vale a carteira 3, que precisa da angio coronária | SES, por escrito |
| 2 | **A articulação e a transvaginal com o IEV** (L-008 revista) | com a confirmação da regulação, a articulação volta, e a reserva da transvaginal pode cair para os 3.068 com CID | regulação da SES, perguntar de novo |
| 3 | **A angio coronária** | decidido em 02/11: a prioridade é não atender. Sem a parede, a única carteira sem angio é a 5 | usuário |
| 4 | **Os 1.490 pedidos novos da carteira 1** | se as filas crescerem menos, a meta fica acima da fila; é medir na fase 0 e no meio da execução | medição |
| 5 | **Os seis códigos novos** (os que eram do redacao_07) mudam o mix aprovado pela SES | é mais texto a explicar na nova versão | usuário e SES |
| 6 | **Pedidos antigos:** 22% da meta da carteira 1 está fora da fila viva |
| 6b | **As faltas:** com 20% a 30%, a carteira 1 precisa de 12.884 a 27.004 pedidos além da fila e do crescimento líquido | a regulação mandar de 12% a 25% das entradas; na mama e no ultrassom de região isolada, mais da metade | regulação, no mês 1 | parte não acha paciente; a busca ativa já está no plano | medir na fase 0 |
| 7 | **As salas de ultrassom:** a carteira 1 usa 137% das 13 salas nos tempos do plano | igual à v26; o tempo real das clínicas decide | negociação |
| 8 | **O custo do ultrassom é premissa,** e a margem do Doppler de membros e da pélvica é fina | se o médico não aceitar, cai a quantidade desses exames | cotação |
| 9 | **Contraste 02.06.03.004-5** fora da Candanga | nenhum adicional presumido; a cotação da TC já inclui o contraste | SES |
| 10 | **A coleta é de 02/11.** Na TC a fila é fluxo, e a SES pode reduzir o estoque antes do início | as metas de TC | recoletar na fase 0 |

**A readequação da pasta `estudos imagens` (02/11, de manhã)** subtraiu as devolvidas da fila e chegou a saldos
negativos. Este estudo não usa aquela conta: a fila e as devolvidas ficam lado a lado.

## 8. O que este estudo não fez

- Não mudou o plano, o `estado.yaml`, a L-008 nem o enquadramento: a carteira é do usuário.
- Não fez commit.
- Não mexeu no redacao_07 nem em outro plano.
