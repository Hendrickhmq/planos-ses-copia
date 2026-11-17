# Dimensionamento dos postos — memória interna

**Saiu do plano em 05/09/2026** (itens D10 e D11 da devolutiva: o professor marcou as
duas tabelas célula por célula, e a memória contradizia o rearranjo do c29, que dá
três postos ao Gama). Fica aqui pela regra 9 do `PADRAO.md`: o conteúdo migra, não
some.

Base: **75,29 entradas por dia útil** no regime pleno e **jornada efetiva de 6 horas**
por posto.

## No polo, por usuário atendido

| atividade | tempo unitário | fonte |
|---|---|---|
| recepção, conferência da lista do dia, do jejum e do acompanhante; termo de consentimento; ficha da OCI | 8 min | **premissa, sem fonte** |
| entrega do laudo, das orientações e do comprovante do retorno | 4 min | **premissa, sem fonte** |
| abertura da APAC e registro dos secundários | 8 min | **premissa, sem fonte** |
| registro do desfecho e encerramento da APAC | 5 min | **premissa, sem fonte** |
| lançamento do resultado no Sistema de Informação do Câncer, nos 30% com biópsia | 4 min | **premissa dupla** — o tempo e a proporção de biópsias (V-09 diz que ela é desconhecida) |
| crítica e reapresentação de registro rejeitado, nos 10% rejeitados | 10 min | **premissa dupla** — o tempo e a taxa de rejeição |
| **carga por OCI** | **27,2 min** | derivado |

| polo | entradas por dia útil | horas/dia | postos pela carga | postos adotados |
|---|---|---|---|---|
| Ceilândia | 29,19 | 13,23 | 3 | **3** |
| Sobradinho | 29,29 | 13,28 | 3 | **3** |
| Gama | 16,81 | 7,62 | 2 | **3** — por decisão de 05/09/2026: dois recepcionistas em cada polo |

## Na coordenação, para os três polos

| atividade | volume diário | tempo unitário | horas/dia |
|---|---|---|---|
| agendamento do exame e do retorno | 150,58 atos | 4 min | 10,04 |
| confirmação ativa de ambos | 150,58 atos | 1,5 min | 3,76 |
| busca ativa | 30,12 contatos | 5 min | 2,51 |
| reagendamento de falta | 7,53 | 5 min | 0,63 |
| **subtotal — agendamento** | | | **16,94** → **3 postos** |
| conferência do laudo endoscópico e do resultado | 75,29 | 2 min | 2,51 |
| cobrança de laudo de anatomia patológica em atraso | 22,59 | 2 min | 0,75 |
| agendamento e confirmação do retorno em atraso | — | — | ~2,5 |
| **subtotal — laudo e retorno** | | | **5,76** → **1 posto** |

Todos os tempos unitários acima são **premissa nossa**. Nenhum tem fonte em
`dados/`, e foi por isso que a regra 1 do `PADRAO.md` — número não entra por
plausibilidade — foi violada seis vezes na versão de 03/09.

## O que isto sustenta hoje na planilha

- 1.1.3 Assistente de agendamento, confirmação e busca ativa — **3 postos**
- 1.1.4 Assistente de rastreamento de laudo e retorno — **1 posto**

São as duas quantidades que o professor marcou de **azul**. Se a marca significar
"de onde vem este número", a resposta está nesta página — e a resposta é que vem de
premissa nossa, não de fonte.
