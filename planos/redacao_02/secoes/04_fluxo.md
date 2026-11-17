# Rodada 4 — Fluxo do atendimento

Texto destinado à **seção 5** do documento remontado. Abaixo da linha dupla, o
fechamento da rodada.

---

## 5. Metodologia e fluxo do atendimento

O ciclo de uma OCI tem **dois contatos**: um comparecimento presencial, em que se
concentram consulta, eletrocardiograma, ecocardiograma e coleta laboratorial, e um **retorno por
teleconsulta**, em que a conduta é definida e a OCI se conclui. A consulta ou
teleconsulta de retorno é parte da composição do procedimento, e não etapa
acessória.

O modelo de **entrada em dia único** é decisão de desenho, e a razão é o segundo
ponto de perda descrito em 5.2: cada comparecimento adicional é uma nova
oportunidade de o ciclo se interromper depois de já ter consumido agenda, equipe e
insumo.

### 5.1 O ciclo, passo a passo

A coluna de setor antecipa a separação que a seção 10 executa: o que é **técnico**
está compreendido no valor unitário do procedimento; o que é **administrativo** e
**financeiro** compõe as despesas de apoio.

| # | passo | setor |
|---|---|---|
| 1 | Recebimento da fila regulada no SISREG | administrativo |
| 2 | Agendamento ativo: contato, oferta de data, confirmação | administrativo |
| 3 | Confirmação prévia, na véspera | administrativo |
| **4** | **Comparecimento à entrada** | **1º ponto de perda** |
| 5 | Recepção: identificação, CNS, conferência do encaminhamento | administrativo |
| 6 | Abertura da APAC e registro do procedimento | administrativo |
| 7 | Preparo e enfermagem | técnico |
| 8 | Consulta especializada em cardiologia | técnico |
| 9 | Eletrocardiograma | técnico |
| 10a | Ecocardiograma transtorácico | técnico |
| 10b | Coleta para exames laboratoriais específicos | técnico |
| 11 | Laudo | técnico |
| 12 | Agendamento da teleconsulta de retorno, ainda no polo | administrativo |
| **13** | **Comparecimento ao retorno** | **2º ponto de perda** |
| 14 | Teleconsulta de retorno, com conduta definida | técnico |
| 15 | Registro do desfecho em campo estruturado | administrativo |
| 16 | Contrarreferência à Atenção Primária ou encaminhamento a nova fila | administrativo |
| 17 | Fechamento e apresentação da APAC na competência | financeiro |
| 18 | Conciliação entre produção apresentada e aprovada | financeiro |
| 19 | Prestação de contas mensal | financeiro |

**Transversais ao ciclo inteiro:** busca ativa do faltoso, sustentação de TI dos
sistemas oficiais, e supervisão de polo.

### 5.2 Os dois pontos de perda, e o dimensionamento que deles decorre

O ciclo se interrompe em dois lugares, e eles não custam a mesma coisa.

**A falta na entrada custa uma vaga.** O horário se perde, o usuário volta à fila
e é reagendado. Nada mais foi consumido.

**A falta no retorno custa a OCI inteira.** Consulta, eletrocardiograma, exames e
laudo já foram executados; sem a teleconsulta de retorno com conduta, nada disso
se converte em OCI concluída. Não é aferível, não é conciliável e não é devido. É
o ponto mais caro do fluxo, e é o que justifica a busca ativa da seção 5.4.

**Dimensionamento.** Adota-se **20% de não comparecimento em cada um dos dois
pontos**:

| ponto | cálculo | horários |
|---|---|---|
| entrada | 35.000 ÷ 0,80 | 43.750 |
| retorno | 35.000 ÷ 0,80 | 43.750 |
| **total** | | **87.500** |

Isto é **dimensionamento de agenda, e não meta**: o compromisso do plano são as
35.000 OCI concluídas da seção 6, não os 87.500 horários. O número existe para que
a estrutura da seção 11 e o custo da seção 10 possam ser dimensionados a partir do
volume real de trabalho, e não de arredondamento.

Os 20% são **premissa declarada**, e não medição: a taxa efetivamente observada na
rede da Secretaria não é dado público. O IND-06 apura a taxa real desde
a primeira competência, separando entrada e retorno; verificando-se taxa
materialmente distinta, a oferta de horários se ajusta sem alteração da meta.

### 5.3 A teleconsulta de retorno

O retorno é, em regra, **por teleconsulta**. Três razões: dispensa o segundo
deslocamento de uma população cuja concentração etária está entre 50 e 75 anos;
encurta o intervalo entre o laudo e a conduta, o que importa porque a conclusão
tem de ocorrer dentro da janela de validade da APAC; e reduz o custo de estrutura
sem reduzir o conteúdo do ato, já que a norma admite expressamente a modalidade.

**O retorno presencial permanece disponível**, e não como exceção burocrática: o
usuário que não dispuser de dispositivo, conexão ou autonomia para a teleconsulta
é atendido presencialmente no polo, sem prejuízo do prazo. A regra é a
teleconsulta; a garantia é a alternativa.

A proporção de usuários sem condição de teleconsulta não é conhecida de antemão;
enquanto não for medida, a estrutura de retorno presencial de cada polo é
dimensionada por margem, e a margem está declarada na seção 11.

### 5.4 Busca ativa

A busca ativa opera nas duas pontas: **confirmação** antes do horário e
**reagendamento** depois da falta. Os canais são WhatsApp, telefone e mensagem de
texto.

**O que comprova a busca ativa é o reagendamento registrado no SISREG**, não a
ligação anotada em planilha própria. Registro de tentativa é atividade; vaga
reocupada é resultado.

### 5.5 Proteção de dados pessoais

A busca ativa é o ponto do fluxo em que dado pessoal circula fora dos sistemas
oficiais, e por isso a regra vive aqui e não em capítulo apartado.

O tratamento se limita ao **necessário para localizar e reagendar**: nome, contato
e referência do agendamento. Não se transmite por WhatsApp, telefone ou mensagem
qualquer informação sobre condição de saúde, resultado de exame, conduta ou
diagnóstico. A base legal é a execução de política pública de saúde, e a finalidade
é única — o comparecimento.

Os contatos são obtidos do encaminhamento regulado e **não são utilizados para
nenhuma outra finalidade**, nem compartilhados. Encerrado o convênio, os registros
de contato mantidos fora dos sistemas oficiais são eliminados.

---
---

# Fechamento da rodada 4 — não vai para o documento

## Decisões do usuário, 24/08/2026

| pergunta | resposta |
|---|---|
| comparecimentos | **dois contatos**: entrada presencial em dia único + retorno |
| retorno | **teleconsulta**, "quase sempre" |
| quem abre a APAC | **o polo / o profissional** — adotado como **premissa**, e o usuário vai confirmar com o professor |
| canais de busca ativa | WhatsApp, telefone e mensagem |
| absenteísmo | **20%**, fornecido pelo usuário como valor a utilizar; ele declarou não ter a taxa real da SES-DF |

## A coincidência que vale registrar

Os 20% reproduzem exatamente o número do plano anterior: 87.500 horários. Lá o
valor apareceu como "fator 1,25 em dois pontos do fluxo", afirmado sem base — e
1,25 é 1 ÷ 0,80. **O número é o mesmo; o estatuto dele não.** Antes era um fator
sem origem; agora é uma premissa de 20% declarada como premissa, com o indicador
que a corrige a partir da primeira competência.

## O achado desta rodada: a fila quase não tem folga

Com 35.000 OCI concluídas sobre **37.731 pessoas** na fila, a margem é de **2.731
pessoas — 7,2%**.

A conta de 43.750 horários pressupõe que quem falta é reagendado e **acaba
comparecendo**. Se uma parcela dos usuários nunca converte — não atende, mudou de
endereço, não quer mais, já resolveu por outra via —, esses horários não se
convertem em OCI, e a reposição tem de vir de outras pessoas da fila. Só existem
2.731 pessoas de reserva.

Em números: se **mais de 7,2%** dos encaminhados nunca comparecerem, apesar da
busca ativa, a fila atual **não comporta** 35.000 OCI concluídas.

O que salva a conta é o que ainda não está medido: a fila **é reabastecida** ao
longo dos 10 meses. Uma espera média de 851 dias implica entrada contínua de novas
solicitações. Sem a taxa de entrada, porém, isso é raciocínio, não dado — vira
L-017 e vira risco na rodada 11.

## Riscos que esta rodada gera para a rodada 11

1. **Falta no retorno** — perde a OCI inteira depois de todo o custo executado. É
   o risco mais caro do desenho e decorre de decisão da seção 2.
2. **Exaustão da fila** — margem de 7,2% contra taxa de não conversão desconhecida.
3. **Barreira digital na teleconsulta** — população de 50 a 75 anos em regiões
   periféricas; o retorno presencial é a mitigação, e ela tem custo de estrutura.
4. **Entrada em dia único depende de capacidade de exame no mesmo dia** — se o polo
   não fizer ecocardiograma no dia, o modelo de dois contatos vira três.

## Lacunas

| id | o que falta | dono |
|---|---|---|
| **L-017** | taxa de entrada de novas solicitações na fila de cardiologia — decide se a margem de 7,2% é suficiente | SES-DF |
| **L-018** | taxa de não comparecimento observada na rede da SES-DF — os 20% são premissa | SES-DF |
| **L-019** | proporção de usuários sem condição de teleconsulta — dimensiona o retorno presencial | proponente com a SES-DF |
| **L-020** | confirmação de quem autoriza e abre a APAC no DF — adotada a premissa de que é o polo | **DV-051**, ao professor |

## O que esta seção obriga as seguintes a respeitar

1. **Rodada 5 (cronograma)** — a curva mensal tem de distribuir **43.750 entradas**,
   não 35.000, e as conclusões seguem as entradas com a defasagem da janela da APAC.
2. **Rodada 6 (equipe e estrutura)** — cada posto tem de apontar um dos 19 passos.
   Passo sem posto é passo que ninguém executa; posto sem passo é posto que sai. E o
   dimensionamento sai de 43.750 entradas presenciais por ano, não de 35.000.
3. **Rodada 7 (planilha)** — nenhum item do setor técnico entra. A pergunta se aplica
   linha a linha, na seção 10.2. *(A antiga 5.6 foi removida em 25/08/2026 por
   repetir 5.1 e 10.2; o sentido dela ficou numa frase em 5.1.)*
4. **Rodada 11 (riscos)** — os quatro riscos acima, com origem declarada.
