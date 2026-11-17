# Rodada 12 — Justificativa e dimensionamento

Texto destinado à **seção 3** do documento remontado. Abaixo da linha dupla, o
fechamento da rodada.

---

## 3. Justificativa e dimensionamento

### 3.1 O problema, e o que o dado disponível mede

A fila de espera regulada por procedimentos cardiológicos para adultos no Distrito
Federal reúne **40.829 solicitações**, correspondentes a **37.731 usuários
distintos**, com **tempo médio de espera de 851,40 dias**.

> Painel de Lista de Espera — Exames e Consultas, da Secretaria de Estado de Saúde
> do Distrito Federal, consultado em 24/08/2026, com filtro de 13 procedimentos
> cardiológicos para adultos.

Oitocentos e cinquenta e um dias são **dois anos e quatro meses**. Não é um número
que precise de adjetivo: uma pessoa encaminhada por sua equipe de Atenção Primária
com suspeita cardiológica espera, em média, mais tempo do que dura o mandato de um
gestor para ser avaliada.

**Quem espera.** A distribuição etária concentra-se entre 50 e 75 anos, com pico na
faixa dos 60 — o perfil em que a doença cardiovascular tem maior prevalência e maior
letalidade evitável. A classificação de risco distribui-se assim:

| classificação | solicitações |
|---|---|
| Prioridade 1 | 3.742 |
| Prioridade 2 | 25.476 |
| Prioridade 3 | 9.378 |
| Prioridade 4 | 2.233 |

**Mais de 29.000 solicitações estão classificadas como prioridade 1 ou 2**, e é
sobre elas que os 851 dias incidem.

**De onde vem a demanda.** A fila distribui-se de forma desigual pelo território:

| Região de Saúde | solicitações |
|---|---|
| Sudoeste | 9.192 |
| Sul | 7.893 |
| Central | 5.902 |
| Norte | 5.520 |
| Centro-Sul | 3.841 |
| Leste | 3.465 |
| Unidade de Referência Distrital | 2.376 |
| Oeste | 1.705 |
| demais origens | 307 |

A soma das origens identificadas é de 40.201 solicitações, **628 a menos que o
total**, diferença que o painel não atribui a região alguma e que fica registrada
como está.

**O que este dado não diz**, e precisa ser dito para que ele não seja usado além do
que suporta: o eixo é a **unidade solicitante**, não a residência do usuário — é
proxy da origem da demanda, não dado de moradia. As 16.391 solicitações devolvidas
estão fora do total, de modo que 40.829 é fila viva. E o painel é uma fotografia:
não informa a **taxa de entrada** de novas solicitações, que é o que determina se a
fila se repõe durante a execução.

### 3.2 Por que a Oferta de Cuidados Integrados, e não a consulta avulsa

O usuário está na fila por uma **consulta**. Uma consulta resolveria o registro da
fila e não resolveria o problema dele: o cardiologista avalia, pede
eletrocardiograma, ecocardiograma e exames laboratoriais, e o usuário volta para
outra fila — a de exames — com um pedido na mão. Quando os exames ficam prontos,
precisa de nova consulta para que alguém os leia e defina conduta. Três filas para
uma pergunta.

A OCI resolve as três de uma vez, e é por isso que ela existe: consulta
especializada, eletrocardiograma, ecocardiograma, exames laboratoriais e **retorno
com conduta definida**, num único ciclo. **É o retorno que retira o usuário da
fila** — por alta, por seguimento na Atenção Primária, ou por encaminhamento
qualificado à fila seguinte, agora com indicação escrita e não com suspeita.

O convênio contrata a **OCI concluída** justamente por isso. Contratar consulta
realizada seria pagar pelo primeiro terço do problema.

### 3.3 O dimensionamento — por que 35.000

O quantitativo não foi arbitrado, e a sua origem é dita sem rodeio: **ele é o que o
recurso custeia**.

| | valor |
|---|---|
| Recurso da emenda | R$ 10.000.000,00 |
| Despesas de apoio (seção 10) | R$ 2.966.419,90 |
| **Disponível para produção** | **R$ 7.033.580,10** |
| ÷ R$ 200,00 por OCI | **35.167,9 OCI** |

O envelope comporta **35.167 OCI**. A fila comporta **37.731 pessoas**. O limite,
portanto, **é o recurso, e não a necessidade**: sobram 2.563 pessoas que este
convênio não alcança, e elas continuam na fila.

A meta de **35.000** fica 167,9 OCI abaixo do que o recurso permitiria. A diferença
é deliberada e corresponde exatamente aos **R$ 33.580,10** que a seção 10 declarou
como não aplicados: nenhuma linha da planilha foi esticada para consumir o teto, e
nenhuma meta foi inflada para o mesmo fim.

**Contra a fila, a meta representa 92,8% dos usuários em espera.** É a cobertura
possível, não a cobertura desejável.

**E há um terceiro limite, que não é financeiro.** A seção 11 demonstra que 35.000
OCI em dez meses e três polos exigem **89 entradas completas por polo por dia
útil** no regime pleno — cada uma com consulta, eletrocardiograma, ecocardiograma,
coleta e laudo no mesmo dia. O quantitativo está simultaneamente no limite de três
variáveis: o recurso disponível, a fila existente e a capacidade instalável. Não há
folga em nenhuma das três, e isso está refletido na matriz de riscos.

### 3.4 Por que estes três polos

Com referência distrital, a localização do polo não recorta a população atendida:
decide **quanto o usuário se desloca**. O território se agrupa em quatro arcos:

| arco | Regiões de Saúde | solicitações | polo |
|---|---|---|---|
| sul | Sul + Centro-Sul | 11.734 | **Gama** |
| oeste | Sudoeste + Oeste | 10.897 | **Samambaia** |
| centro-leste | Central + Leste | 9.367 | — |
| norte | Norte | 5.520 | **Sobradinho** |

**Sobradinho** é o único ponto que resolve o arco norte: Planaltina e Fercal não
têm alternativa mais próxima. **Gama** ancora o arco de maior volume, somando Santa
Maria e o Centro-Sul. **Samambaia** foi escolhida sobre Ceilândia porque, dos
10.897 do arco oeste, 9.192 estão no Sudoeste — Ceilândia fica na região de 1.705,
na borda do território, enquanto Samambaia está dentro da maior massa da fila e
continua vizinha de Ceilândia, Taguatinga e Recanto das Emas.

Taguatinga seria ainda mais central e foi descartada por outra razão: é onde a rede
própria da Secretaria concentra maior capacidade especializada, e **complementaridade
não se instala sobre a capacidade existente** — instala-se onde ela falta.

**As Regiões Central e Leste, que somam 9.367 solicitações, não recebem polo.** A
omissão é consequência da mesma razão e fica declarada: é no eixo central que a
rede própria é mais forte. O usuário do Paranoá, do Itapoã e de São Sebastião tem o
maior deslocamento deste desenho, e isso consta da matriz de riscos como risco de
acesso, com a sua ação compensatória.

### 3.5 Economicidade

A economicidade deste plano se demonstra por três vias, e nenhuma delas depende de
adjetivo.

**A primeira é a proporção.** As despesas de apoio somam R$ 2.966.419,90, ou
**29,8% do valor global**. Os 70,2% restantes são produção assistencial, paga por
unidade concluída e aprovada.

**A segunda é a ausência de duplicidade.** Nenhum custo assistencial figura na
planilha: consulta, ecocardiograma, eletrocardiograma, coleta, laudo, insumo e o
próprio parque de equipamentos estão compreendidos no valor unitário do
procedimento, e o teste foi aplicado item a item. O executor não é remunerado duas
vezes pelo mesmo ato, e a seção 10.2 demonstra onde a verificação foi feita.

**A terceira é a rastreabilidade do preço.** Cada valor unitário da planilha declara
a sua origem, linha a linha, e não em nota genérica.

**O que a economicidade ainda não demonstra**, e é dito aqui e não escondido: não há
comparativo com preço de mercado para a cesta de procedimentos, o que impediria
afirmar que R$ 200,00 é vantajoso em relação à contratação avulsa dos mesmos atos.
O levantamento correspondente — tabela de referência de mercado para consulta,
eletrocardiograma, ecocardiograma e exames laboratoriais — é apresentado pelo
proponente na fase de análise técnica.

### 3.6 O que esta justificativa ainda não demonstra

Três demonstrações faltam, e nenhuma delas se resolve escrevendo.

**A complementaridade.** O art. 24 da Lei nº 8.080/1990 admite a participação
complementar da iniciativa privada quando as disponibilidades do Poder Público
forem insuficientes. A fila prova que **falta atendimento**; ela não prova que falta
**ao Estado**. A demonstração exige o número da capacidade instalada da rede própria
da Secretaria e o déficit dela resultante. Esse dado é da concedente, e a sua
apresentação na análise técnica é o que converte a demonstração de necessidade em
demonstração de complementaridade.

**A ancoragem no planejamento.** O art. 6º, II da Portaria GM/MS nº 10.297/2026 faz
da coerência com o Plano de Saúde e a Programação Anual de Saúde **requisito de
elegibilidade ao recebimento**, e não critério de mérito. A identificação da
diretriz, do objetivo e da meta do Plano Distrital de Saúde 2024–2027 e da
Programação Anual de Saúde em que este objeto se ancora compete à Secretaria, e
antecede o recebimento do recurso — se o planejamento distrital ainda não o
contemplar, a adequação corre pelo rito ordinário, com prazo próprio.

**A reposição da fila.** O dimensionamento pressupõe que os usuários encaminhados e
não comparecidos sejam substituídos por outros da mesma fila. A margem entre a fila
e a meta é de 2.731 pessoas — 7,2%. Se a taxa de não conversão superar esse
percentual, a fila atual não comporta 35.000 OCI concluídas, e a reposição depende
da entrada de novas solicitações, que o painel não informa. A taxa de entrada mensal
na fila de cardiologia é informação da Secretaria, e a sua obtenção antes da
celebração é o que permite dimensionar essa margem com segurança.

---
---

# Fechamento da rodada 12 — não vai para o documento

## Decisões do usuário, 24/08/2026

| pergunta | resposta |
|---|---|
| dizer que o quantitativo foi fixado pelo teto financeiro | **sim** |
| fonte para comparativo de preço de mercado | não tem |
| novidade sobre PDS/PAS ou capacidade da rede própria | nada novo |

## A decisão que mais fortalece a seção

Dizer abertamente que **o limite é o recurso, e não a fila**, é o que torna esta
justificativa diferente de uma peça retórica. E a conta fecha nos dois sentidos, o
que é raro:

```
envelope comporta ......... 35.167,9 OCI
meta ...................... 35.000,0 OCI
diferença ..................... 167,9 OCI  x R$ 200,00 = R$ 33.580,10
                                                          ↑
                       exatamente o valor que a seção 10 declarou não aplicado
```

O número que a planilha deixou sobrando e o número que a meta deixou de comprometer
**são o mesmo número, visto de dois lados**. Isso não foi construído: apareceu
quando as duas contas foram feitas de forma independente, e é a melhor evidência de
que nenhuma delas foi ajustada para fechar a outra.

## A armadilha que o roteiro nomeia, e como escapamos dela

*"Justificativa que é a única seção bem escrita do plano costuma indicar que o resto
foi preenchido para caber num valor já decidido."*

Escrita em décimo segundo lugar, esta seção **não introduz nenhum número novo**.
Cada afirmação dela aponta para uma conta feita em outra rodada: a fila veio do
painel na rodada 4, o apoio da planilha na rodada 7, o 89 do cronograma na rodada 5,
os arcos da rodada 1, os 29,8% da rodada 7. É verificável por cruzamento interno, o
que é o oposto de retórica.

## O que ficou escrito como ausência

Quatro `[preencher]` nesta seção, e três deles são de **mérito**, não de formulário:

| o que falta | por que importa | lacuna |
|---|---|---|
| capacidade da rede própria | sem ela a fila prova que falta atendimento, não que falta **ao Estado** — e complementaridade é o fundamento constitucional do instrumento | L-004 |
| ancoragem no PDS/PAS | é **elegibilidade ao recebimento**, não mérito | L-003 |
| taxa de entrada na fila | decide se a margem de 7,2% se sustenta | L-017 |
| comparativo de preço de mercado | é a única via de economicidade que não temos | L-038 (nova) |

A seção 3.6 existe para dizer isso dentro do documento. Um plano que afirma
complementaridade sem o dado da rede própria está afirmando o que não sabe; este diz
o que sabe e nomeia o que falta, no lugar exato onde faltaria.

## O que esta seção obriga as seguintes a respeitar

1. **Rodada 13 (proponente e condições de partida)** — a complementaridade é
   argumento de justificativa, mas a **habilitação** que a viabiliza é condição de
   partida. As duas se encontram lá.
2. **Rodada 14 (base legal)** — art. 24 da Lei nº 8.080/1990 e art. 6º, II da
   Portaria GM/MS nº 10.297/2026 estão citados aqui com função; na base legal
   entram como espinha, sem repetição do argumento.
