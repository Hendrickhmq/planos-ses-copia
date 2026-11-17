# mapa.md — o percurso inteiro numa página

Uma entidade sem fins lucrativos recebe dinheiro de uma emenda parlamentar, por um
convênio com a SES-DF, para atender gente que está na fila do SUS. O projeto escreve os
documentos que tornam isso possível: o pré-plano e o plano de trabalho.

Esta página é a vista de cima; o cofre de notas começa em [[Início]]. O percurso completo, com a regra e o prazo de cada etapa,
está em `biblioteca/instrumento/fluxo_emenda.md`.

---

## As cinco perguntas de todo projeto

Tudo o que se faz responde a uma delas. Quando travar, volte aqui e veja qual está sem
resposta.

| pergunta | o que decide | módulo |
|---|---|---|
| **Por que uma entidade privada pode atender pelo SUS?** | as condições que a Constituição e a lei põem, e que voltam em todo documento | 1 |
| **De onde vem o dinheiro?** | a regra que vale, o que ele pode pagar, quando chega | 2 e 3 |
| **Por qual instrumento, e por onde ele anda?** | a lei que se cita, o vocabulário, quem analisa e quem aprova | 4 e 5 |
| **Para fazer o quê, para quem?** | a fila, o procedimento, o lugar, a quantidade | 6 |
| **Quanto custa, e fecha?** | o valor de tabela, o custo de executar, o apoio | 7 |

Só depois delas se escreve: o pré-plano (módulo 8) e o plano (módulo 9).

## O percurso

| # | o que acontece | quem faz | o que sai | módulo |
|---|---|---|---|---|
| 1 | A emenda entra na lei orçamentária da União | parlamentar, bancada ou comissão | o recurso, com número e tipo | 3 |
| 2 | O dinheiro vai ao Fundo de Saúde do DF | a ARINS cadastra a proposta do DF; o Ministério da Saúde aprova; o Fundo Nacional paga | recurso na conta do Fundo, com fonte própria | 3 |
| 3 | O parlamentar indica a entidade e o projeto | parlamentar, por ofício à SES-DF | ofício de indicação | 3 e 5 |
| 4 | Escolhe-se o objeto | nós, com a entidade | o dossiê: qual fila, qual procedimento, por quê | 6 e 7 |
| 5 | A SES pede o plano simplificado, e a entidade responde | ARINS pede; nós escrevemos | o pré-plano | 8 |
| 6 | A SES decide se e como fazer | SUCONV e a área técnica | o relatório preliminar e o parecer | 4 e 5 |
| 7 | A entidade apresenta o plano de trabalho, em versões | nós escrevemos; a SES analisa e devolve | o plano aprovado | 9 e 10 |
| 8 | A SES aprova, empenha e assina | quem aprova (ver "Quem é quem"), o Fundo, o Secretário | o termo de convênio, publicado | 5 |
| 9 | A entidade executa | entidade, com a regulação da SES | atendimentos registrados, relatório mensal | 11 |
| 10 | A entidade presta contas | entidade; a SES analisa | prestação parcial a partir do 3º mês e final em 60 dias | 11 |

Os passos 1 e 2 e o passo 3 correm em paralelo, e um não espera o outro: são os "dois
trilhos" do `fluxo_emenda.md`. O Ministério da Saúde nunca lê o plano da entidade.

Por baixo de todos os passos está uma ideia só, a da **[[Complementaridade|complementaridade]]**: a entidade
entra onde a rede pública não dá conta, pelo instrumento certo, pela tabela do SUS e sob
o comando da SES. É o módulo 1, e é por ela que o controle começa a ler.

O controle externo (Ministério Público de Contas, Tribunal de Contas, Controladoria)
pode entrar a qualquer momento depois do passo 8. Já entrou treze dias depois de uma
assinatura. Por isso todo documento se escreve pensando em quem vai lê-lo para atacar.

## Quem é quem

| quem | o que faz no percurso |
|---|---|
| **[[Emenda parlamentar|Parlamentar ou bancada]]** | põe o recurso na lei e indica a entidade |
| **[[Ministério da Saúde|Ministério da Saúde e Fundo Nacional de Saúde]]** | aprovam a proposta do DF e pagam ao Fundo do DF. Não leem o plano da entidade nem pagam a ela |
| **[[ARINS|ARINS]]** | a porta de entrada das emendas na SES-DF: acha o recurso, abre o processo, pede o plano à entidade |
| **[[SUCONV|SUCONV]]** | a Subsecretaria de Convênios e Parcerias. Instrui o convênio: define o instrumento, pede documento, analisa preço e elegibilidade, faz diligência |
| **[[SAIS|Área técnica da SES]]** | dá o parecer assistencial: se o que se propõe faz sentido para a rede. Quase sempre é da SAIS |
| **[[Secretarias executivas|Quem aprova]]** | pela portaria, as secretarias adjuntas (SAA o assistencial, SAG o resto). Nos processos de 2026 assinam as três secretarias executivas. O módulo 5 conta a diferença |
| **[[FSDF|Fundo de Saúde do DF]]** | empenha e paga as parcelas |
| **[[Complexo Regulador|Complexo Regulador]]** | manda o paciente da fila para o atendimento. A entidade não escolhe paciente |
| **[[Partícipes e convenente|Entidade proponente]]** | assina o convênio e responde por ele |
| **[[Executor|Executor]]** | o estabelecimento onde o atendimento acontece. Pode ser a própria entidade ou outro, e isso muda muita coisa (módulo 6) |
| **[[MPCDF|MPCDF, TCDF, CGDF]]** | o controle externo e interno do DF |
| **[[MPDFT|MPDFT]]** | publica o Mapa Social da Saúde, de onde se mede a fila |

O nome por extenso de cada sigla está no `glossario.md`.

## Onde o repositório guarda cada coisa

Está no `README.md`, "Onde está cada coisa". Em uma linha: a regra em `metodo/`, a
consulta em `biblioteca/`, cada projeto em `planos/redacao_NN/`, a base em `registros/`.

Todo registro tem um número, e `python3 ferramentas/consultar.py <número>` abre qualquer
um:

| prefixo | o que é | exemplo |
|---|---|---|
| `NM-` | norma: lei, decreto, portaria | NM-010, o decreto dos convênios de emenda do DF |
| `CT-` | peça de controle: representação, decisão de tribunal | CT-008, a decisão que separa convênio de MROSC |
| `IT-` | instrumento: termo de convênio, apostilamento | IT-001 |
| `DD-` | dado: painel, consulta, tabela | DD-005, o CNES dos executores |
| `OB-` | obrigação: o que o plano precisa conter, e por quê | OB-043 |
| `AC-` | achado: o que se observou nos planos aprovados | AC-077 |
| `LI-` | lição: o que fazer no nosso plano, com a origem | LI-009 |
