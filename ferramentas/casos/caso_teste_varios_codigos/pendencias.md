# Pendências — plano 4, filas de ultrassom e tomografia

Aberto em 15/09/2026. Lacuna tem dono. Decisão tem opções e consequência em reais.

---

## Lacunas

### L-001 — parede abdominal e partes moles · RESOLVIDA NA FONTE

**Fechada em 15/09/2026** com a coleta em `dados/fontes/validacao_ultrassom.md`. O
painel de regulação carrega o código SIGTAP de cada nome interno:

| nome interno | SIGTAP |
|---|---|
| ULTRASONOGRAFIA DE PAREDE ABDOMINAL | **02.05.02.004-6** — abdômen total |
| ECOGRAFIA␣␣DE PARTES MOLES | **02.05.02.006-2** — articulação |

**A parede abdominal cai no mesmo código do abdômen total**, que já estava no objeto:
as duas linhas viram uma, de 13.080 exames. **As partes moles entram como linha
própria**, sob articulação.

**A hipótese que este projeto carregava estava meio certa.** Partes moles em
articulação era o encaixe previsto; parede abdominal estava apontada para abdômen
**superior**, e é abdômen **total** — o que muda o unitário de R$ 99,94 para
R$ 100,18.

### L-002 — angiotomografia de coronárias · RESOLVIDA NA FONTE

**Fechada em 15/09/2026** com a coleta do Mapa Social da Saúde, em
`dados/fontes/mapa_social_tomografia.md`.

O painel de regulação guarda o campo `codigo_sigtap_solicitacao`, e nele
**ANGIOTOMOGRAFIA DAS ARTÉRIAS CORONARIAS ADULTO S/SEDACAO carrega o código
02.06.02.003-1 — TOMOGRAFIA COMPUTADORIZADA DE TÓRAX.**

A SES-DF já fatura o exame assim. Não é analogia deste plano: é o código do próprio
sistema. As 1.397 angiotomografias integram a linha do 02.06.02.003-1, que passa de
3.794 para **5.191 exames**.

**O que isso moveu no plano inteiro:** o objeto vai de 74.054 a **81.546 exames**, a
soma dos procedimentos de R$ 9.814.279,70 a **R$ 10.843.402,74** e o valor global a
**R$ 11.688.862,74**. O apoio, que não mudou de tamanho, caiu de 7,931% para
**7,233%**.

### L-003 — fichas SIGTAP · a parte crítica RESOLVIDA

**A quantidade máxima do 02.05.01.004-0 fechou em 15/09/2026.** A ficha diz 5 por
AIH/competência e acrescenta que **"estas quantidades de procedimento realizado
independem da quantidade de vasos estudados"**.

**Um doppler venoso bilateral de membros inferiores é um registro, não dois.** A linha
de 14.401 exames não dobra, e o risco de R$ 981.062,74 que este arquivo vinha
carregando não existe.

**O que continua aberto**, e não move dinheiro: idade mínima e máxima, sexo,
atributos complementares, CBO e habilitações de cada um dos doze códigos, na
competência vigente. Entram na seção 2 como condição de elegibilidade se alguma for
restritiva.

### L-004 — o contraste de tomografia · decidido fora, dúvida registrada

**Decidido em 15/09/2026: não entra.** A planilha lança apenas o valor do
procedimento declarado na tabela da portaria. O usuário pediu que a dúvida ficasse
registrada, e é o que este item faz.

O 02.06.03.004-5 CONTRASTE PARA TOMOGRAFIA COMPUTADORIZADA é criado pelo Anexo II
da mesma portaria: APAC secundário, R$ 60,00, quantidade máxima 1, compatível com os
treze procedimentos de tomografia do rol (Anexo IV). **Não está no Anexo I e
portanto não tem incremento.**

Onze mil trezentos e vinte e nove dos 13.452 exames de tomografia da fila pedem
contraste. A R$ 60,00 cada, são **R$ 679.740,00**.

**O que decidiu:** a descrição do Anexo II destina o valor "exclusivamente à
composição e ao cálculo dos créditos financeiros no âmbito da modalidade Crédito
Financeiro do Programa Agora Tem Especialistas", e a execução deste plano é por
convênio de emenda, não pelo componente de créditos.

**O que a decisão deixa em pé:** os 12.726 exames continuam exigindo contraste e o
executor continua comprando meio de contraste, agora **dentro do valor unitário do
exame**. Pela referência da própria portaria são R$ 679.740,00 — 6,9% da soma dos
procedimentos, absorvidos. **Isto vai à matriz de riscos da seção 8**, e é o item que
mais pesa lá.

**O que reabriria:** se a SES-DF orientar o registro do secundário na produção deste
convênio, ou se a análise da concedente pedir a composição do insumo, o item volta
com o número já calculado.

### L-005 — a fila por Região de Saúde · RESOLVIDA

**Fechada em 15/09/2026** com a coleta de ultrassonografia, que completou a de
tomografia.

O rateio foi calculado procedimento a procedimento — a distribuição territorial de
cada um aplicada ao quantitativo daquele procedimento na planilha — e somado:

| polo | participação | exames |
|---|---|---|
| Ceilândia | 40,56% | 33.073 |
| Sobradinho | 29,67% | 24.196 |
| Gama | 29,77% | 24.277 |

**Fora do território, 14,2% do universo** — contra os 44,2% que a tomografia sozinha
sugeria. A ultrassonografia quase não vem de URD nem de contratados, e é 84% do
objeto.

**Gama empatou com Sobradinho.** Só com a tomografia, o Gama aparecia em 21,18%.

### L-006 — o parque instalado não foi confirmado · muda o que a seção 6 declara

**Dono: usuário — não confirmado em 15/09/2026.**

O usuário declarou que o proponente já tem ultrassom e tomógrafo, e não conseguiu
confirmar quantas salas, quantos tomógrafos e em que turno.

**Consequência, e ela é de método:** o plano **não publica inventário de parque
instalado**. A seção 6 declara **capacidade requerida** — as 29.522 horas de sala que
a meta exige, e o número de salas que elas implicam em cada turno. É o que a
estrutura do `PADRAO.md` já chama de capacidade requerida, e é afirmação sobre a
execução, não sobre o patrimônio do proponente.

**O risco fica de pé e vai à seção 8:** se o parque real ficar abaixo de dez salas de
ultrassom em turno de dez horas, a meta de 81.546 exames em doze meses não é
executável no ritmo previsto. É o maior risco de execução do plano.

---

## Decisões

### D-001 — a direção do dimensionamento · TRAVADA

**Decidida em 15/09/2026: a fila define o valor.** Sem teto prévio. O valor global é
a soma dos procedimentos mais o apoio montado de baixo para cima — R$ 11.688.862,74
com os 81.546 exames de código fechado.

### D-002 — a base dos 8% · TRAVADA

**Decidida em 15/09/2026: por dentro.** Os 8% são do valor global, não da soma dos
procedimentos — o que os torna teto de R$ 942.904,59, resolvida a circularidade. O
apoio realizado ficou em R$ 845.460,00, abaixo dele.

### D-003 — o quadro do apoio · FECHADO

**Decidido em 15/09/2026**, em três rodadas. A equipe é maior do que os três cargos
nomeados; usa os cargos e funções dos planos aprovados; e não passa de 8%. Na última
rodada o usuário fixou os quantitativos: **seis operadores de registro, seis
assistentes administrativos, a diferença para a assessoria e, havendo margem, dois
coordenadores.**

**Os dois últimos pedidos não cabiam juntos** — duas coordenações a R$ 10.500 com a
assessoria ao preço do acervo dão 8,035%. O arranjo adotado mantém os dois
coordenadores e deixa a assessoria no preço do acervo: **Coordenação Administrativa
R$ 10.500, Coordenação Financeira R$ 9.500, seis operadores, seis assistentes e a
Assessoria de Prestação de Contas a R$ 5.455** — R$ 845.460,00 em doze meses,
**7,233% do global**. Todos os cinco preços têm procedência literal no acervo.
Aritmética em `dados/apoio_proposta.md`.

**O que a decisão do usuário mudou nas premissas:** seis operadores comportam 7,35
minutos por registro, contra os 8 minutos que o plano 3 usou. O número de postos veio
dele; o tempo por exame é o que esse número implica.

**A recepção ficou fora**, e a aritmética é que decidiu: o fluxo pede cinco
recepcionistas, R$ 16.000,00 por mês, e a folga até o teto é de R$ 663,00. Ela fica
dentro do valor unitário, que aqui é tabela mais incremento e por isso remunera o
episódio inteiro.

**O que reabriria:** se a análise da concedente entender que recepção e entrega de
laudo são rubrica, o apoio vai a mais de 10% e o teto de 8% é que precisa mudar — não
os postos.

### D-004 — o que mais falta para a fase 0 fechar

Sem lastro, nada disto entra no documento:

| parâmetro | estado |
|---|---|
| proponente — razão social, CNPJ, endereço, CNES | `[preencher]` · o usuário mandou seguir sem, em 15/09/2026 |
| origem do recurso | **emenda parlamentar federal** · falta autor, número e RP |
| vigência em meses | **12** · travado em 15/09/2026 |
| local de execução | **polos múltiplos** · travado em 15/09/2026; falta quantos e quais |
| capacidade instalada | **proponente já possui US e tomógrafo** · travado em 15/09/2026 |
| distribuição da fila por Região de Saúde | `[preencher]` · **L-005** |
| data da extração da fila | **10/09/2026, quinta-feira** · falta o sistema de origem |
| capacidade instalada — salas, equipamentos, turnos | **não confirmável** · **L-006**, e o plano declara capacidade requerida |
| número, nome e cobertura dos polos | **3 — Ceilândia, Sobradinho, Gama** · travado em 15/09/2026 |
| meses de produção dentro da vigência de 12 | `[preencher]` · 11 ou 12 decide a curva |
