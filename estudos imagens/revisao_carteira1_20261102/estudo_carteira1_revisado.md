# Carteira 1 — revisão de capacidade, demanda e encaminhamento

Revisão de 02/11/2026, na pasta de trabalho `estudos imagens`. A apresentação principal é `estudo_filas_imagem_20261102_organizada_revisada.xlsx`. Fontes e versões anteriores estão preservadas nesta pasta com hashes. O plano oficial, `estado.yaml` e documentos de outros planos não foram alterados. Sem commit ou envio externo.

## Resultado para decisão

A carteira 1 mantém **79.219 exames e R$ 10.636.506,41 em procedimentos**. Há 23.906,2 horas assistenciais de US e 4.739,0 de TC. A parede abdominal, com 3.304 exames, permanece essencial e sujeita à confirmação expressa da SES sobre enquadramento e faturamento. A angio coronária permanece excluída. A US de articulação fica fora inteira e 4.000 transvaginais ficam reservadas ao IEV, sem liberação automática por prazo presumido.

**Até 20 salas não é um arranjo robusto para a distribuição territorial atual aproximada.** Sem mover demanda, são 21 salas em oito meses ou 23 em sete, mesmo sem perda adicional por faltas. Se 20% das vagas forem perdidas além da disponibilidade operacional de 80%, são 24 e 29 salas. Com 30%, são 29 e 33. O mínimo puramente agregado com 20% de perdas seria 23 e 26, antes de arredondar por polo.

Um teste de 20 salas só cabe em oito meses, com faltas já integralmente absorvidas na eficiência final de 80% ou vagas repostas sem perda adicional, e com remanejamento de 1.371 Dopplers venosos bilaterais do Sul: 915 para Asa Sul e 456 para Ceilândia. O arranjo fica em 3 salas na Asa Sul, 3 em São Sebastião, 3 em Sobradinho, 1 em Ceilândia, 6 em Samambaia e 4 no Gama. Gama e Asa Sul ficam praticamente no teto de agenda. Esse teste matemático depende de deslocamento viável, regulação, equipe e salas confirmadas. Não constitui capacidade instalada nem recomendação territorial aprovada.

## Salas por região de origem e polo de atendimento

| Origem aproximada | Execução proposta | Horas US | 8m sem perda extra | 7m sem perda extra | 8m com 20% extra | 7m com 20% extra |
|---|---|---:|---:|---:|---:|---:|
| Central + Centro-Sul | Asa Sul | 3.421,9 | 3 | 3 | 4 | 4 |
| Leste | São Sebastião | 2.851,7 | 3 | 3 | 3 | 4 |
| Norte | Sobradinho | 2.840,9 | 3 | 3 | 3 | 4 |
| Oeste | Ceilândia | 1.037,7 | 1 | 1 | 1 | 2 |
| Sudoeste | Samambaia | 7.464,0 | 6 | 7 | 7 | 8 |
| Sul | Gama | 6.290,0 | 5 | 6 | 6 | 7 |

As participações por família vêm de **15/09/2026**: fila de US e total de solicitações na TC, transcritos em `calculo_v19/calculo.py`. Protocolos sem equivalente usam o mix regional antigo de 20/10 como premissa. Foram rateadas quantidades inteiras por maiores restos por item, conservando as metas e os tempos. A distribuição de 02/11 está disponível somente para modalidades inteiras, sem cruzamento com elegibilidade e protocolos. Ela inclui URD, credenciados e registros sem região e não foi renormalizada silenciosamente para simular residência. A região do registro precisa ser validada como origem geográfica antes da pactuação.

O total de US equivale a 17,79 salas de 1.344 horas em oito meses antes do arredondamento territorial. Em sete meses, cada sala tem 1.176 horas. Vagas de agenda, horas assistenciais e horas perdidas estão separadas. Os tempos do gerador anterior foram preservados, incluindo 40 minutos para Doppler bilateral de membros. A referência ao CBR 2017 é a atribuição documental herdada e não uma validação clínica nova. Unidade de faturamento bilateral precisa de conferência.

Os 80% têm duas interpretações explicitadas: (1) disponibilidade operacional, com pausas e indisponibilidades, descontando faltas separadamente; (2) eficiência final já com faltas, sem descontá-las novamente. A segunda só é válida se as perdas totais couberem nos 20%. Com faltas de 20%, sobra zero margem para outras perdas; com 30%, eficiência final de 80% requer reposição. As salas não foram ajustadas por redução artificial de tempos.

TC foi dimensionada separadamente, por origem, no arranjo local de seis polos, em `Salas por polo`. No caso de oito meses sem perdas adicionais, são sete tomógrafos locais (dois para a Sudoeste), contra mínimo agregado de quatro. Não foi presumido que os seis equipamentos herdados ou o roteiro antigo estão confirmados. A redistribuição da TC precisa ser pactuada separadamente, com contraste, agenda e prestadores disponíveis.

## O encaminhamento da SES que sustenta as metas

Foram modelados os três cenários solicitados, por protocolo: a) manutenção da oferta; b) transferência de 50% da oferta eletiva selecionada atribuída à SES; c) transferência integral desse recorte, reduzindo a oferta correspondente. A produção dos demais prestadores é mantida. Protocolos sem meta própria não têm a oferta suspensa. Emergência, angio coronária, sedação e reservas são excluídas antes da projeção.

**Nas hipóteses do modelo, somente a concentração integral dos protocolos selecionados assegura todo o mix sem remanejamento de metas.** Isso não comprova que tal encaminhamento esteja disponível: a separação entre produção SES e outros convênios no mesmo protocolo não foi medida. A hipótese inicial atribui 100% da produção habitual à parcela transferível, como teto ilustrativo. O percentual é editável e os resultados se alteram quando parte dessa oferta pertence a outros prestadores não transferíveis.

| Cenário | Meses | Espera até início | Estoque inicial | Entradas elegíveis | SES atendida | Projeto possível | Déficit de meta | Estoque final | Aumento líquido rede |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| a | 8 | 0 | 77.981 | 83.906 | 37.928 | 77.614 | 1.605 | 46.345 | 77.614 |
| b | 8 | 0 | 77.981 | 83.906 | 19.927 | 78.871 | 348 | 63.089 | 60.871 |
| c | 8 | 0 | 77.981 | 83.906 | 456 | 79.219 | 0 | 82.212 | 41.748 |
| a | 8 | 2 | 89.175 | 83.906 | 37.523 | 77.300 | 1.919 | 58.257 | 77.300 |
| b | 8 | 2 | 89.175 | 83.906 | 19.523 | 78.871 | 348 | 74.686 | 60.871 |
| c | 8 | 2 | 89.175 | 83.906 | 401 | 79.219 | 0 | 93.460 | 42.097 |
| a | 7 | 0 | 77.981 | 73.417 | 33.238 | 77.771 | 1.448 | 40.390 | 77.771 |
| b | 7 | 0 | 77.981 | 73.417 | 17.487 | 78.871 | 348 | 55.040 | 63.121 |
| c | 7 | 0 | 77.981 | 73.417 | 407 | 79.219 | 0 | 71.773 | 46.388 |
| a | 7 | 2 | 89.175 | 73.417 | 32.834 | 77.457 | 1.762 | 52.301 | 77.457 |
| b | 7 | 2 | 89.175 | 73.417 | 17.084 | 78.871 | 348 | 66.637 | 63.121 |
| c | 7 | 2 | 89.175 | 73.417 | 352 | 79.219 | 0 | 83.021 | 46.737 |

Os totais são pedidos equivalentes de modelagem, arredondados só na apresentação. A coluna de outros convênios/prestadores está na planilha e vale zero na hipótese extrema inicial, **não por medição de ausência**. O estoque final pode crescer mesmo com cumprimento da meta porque a rede reduz a oferta em c. Transferência não cria demanda nova nem equivale a aumento líquido de atendimento. O aumento líquido compara a produção total do cenário com a produção habitual possível sobre o mesmo estoque e entradas.

No cenário b, faltam 348 realizações em quatro protocolos sem contraste. A pactuação pode selecionar percentuais diferentes por protocolo em vez de suspender tudo. Para estes quatro, a proxy sugere transferência mínima superior a 50%:

| Protocolo | Meta | Transferência mínima 8m | Transferência mínima 7m |
|---|---:|---:|---:|
| 109. TC DE PELVE OU BACIA ADULTO S/CONTRASTE  S/SEDACAO | 56 | 94,6% | 94,6% |
| 061. TC DO ABDOMEN SUPERIOR ADULTO S/CONTRASTE S/SEDACAO | 68 | 93,6% | 93,6% |
| 053. TC DO TORAX  ADULTO S/CONTRASTE S/SEDACAO | 180 | 92,0% | 92,0% |
| 029. TC DE CRANIO ADULTO S/CONTRASTE S/SEDACAO | 44 | 91,3% | 91,3% |

Esses percentuais são cenários, sem confirmação de fluxos por protocolo. Não são quantidades comprovadas a contratar. A planilha expõe as frações mínimas para todos os protocolos em `Protocolos`. É preciso pactuar com a regulação: lista eletiva e critérios de elegibilidade, identificação da oferta própria efetivamente transferível, oferta preservada de outros convênios, quantitativo mensal encaminhado, destino após falta/cancelamento, bloqueio de dupla vinculação e remanejamento de metas autorizado. A SES deve confirmar também parede abdominal e unidade de faturamento do Doppler bilateral.

## Faltas, reagendamentos e baixas

A conclusão de **12.884 a 27.004 pedidos novos necessários está superada**. Para 79.219 realizações, meta/(1−faltas) gera cerca de 99.024 tentativas a 20% ou 113.170 a 30%, arredondando no total. Arredondar separadamente por protocolo gera mais vagas. Essas tentativas podem pertencer à mesma solicitação reapresentada, portanto não comprovam pacientes ou pedidos novos. Reagendamento não é entrada e não é realização.

Pessoas únicas, solicitações, tentativas de agendamento, faltas, reagendamentos, cancelamentos, outras baixas e realizações são medidas distintas. A fonte tem pessoas por par/modalidade, pendências por nome e situações/produção agregadas por código. Não tem chave longitudinal que permita reconstruir destinos ou deduplicar pessoas da carteira. Cancelamento de agenda não demonstra cancelamento do pedido. Não foi inventada regra de retorno à fila.

Se a mesma solicitação puder ser reapresentada no prazo, faltas afetam vagas e capacidade, sem necessariamente aumentar demanda única. Se uma falta retirar o pedido da execução sem retorno, a disponibilidade pode cair: nesse cenário extremo, uma tentativa por pedido requer mais solicitações acessíveis, mas a regra e a perda definitiva precisam ser medidas antes de quantificar necessidade de novos pedidos. Baixas administrativas podem reduzir o registro da fila sem resolver a indicação assistencial. Não contam como produção. O modelo começa com baixas e cancelamentos adicionais iguais a zero como hipóteses explícitas, com campos próprios.

## Crescimento, estoques e intervalo até execução

A projeção usa o mesmo inventário elegível da carteira, incluindo nomes pequenos como disponibilidade possível, sem incluí-los artificialmente nas metas. O estoque elegível é **77.981,35 pedidos equivalentes**, frente a 77.976 antes: a diferença vem de filas pequenas e truncamentos por nome. A fração de pelve de 7/5.944 é conservada como premissa legada pendente, sem tratar CID como fronteira. A reserva transvaginal permanece 4.000 no estoque; a aplicação proporcional ao fluxo é apenas hipótese de rateio.

Não há entradas e produção realizada por protocolo no mesmo recorte. Entradas são estimadas pelo fluxo do código vezes a participação elegível no estoque. Produção usa os agendamentos dos nomes multiplicados pela razão realizados/agendados do código e pela fração elegível. As janelas e o mix não são idênticos. Não se pode tratar o fluxo integral do código nem a agenda como produção acessível garantida. A planilha separa fonte, proxy e realização projetada. Os saldos negativos são mantidos e reduzem o estoque quando a rede atende acima das entradas.

Há comparações com zero e dois meses entre coleta e início. O início real permanece desconhecido. Os dados mais recentes de solicitações na recarga de 02/11 vão até 28/10, informação que também afeta o calendário efetivo. A produção anterior ao início é descontada antes da nova execução. Meses para zerar são projeções condicionadas ao saldo e não previsões garantidas. O balanço acumulado não prova disponibilidade mês a mês, acesso geográfico, elegibilidade individual ou conclusão de toda a fila da extração.

## Formulação a avaliar posteriormente

Propõe-se substituir a promessa de zerar a extração por **produção efetivamente realizada de 79.219 exames elegíveis, encaminhados pela regulação, por código e prazo**, com identificação individual, laudo e registro único, sem dupla contagem. A quantidade de vagas ofertadas é indicador separado. Remanejamento só após pactuação prévia e preservando limites e enquadramento. A redução da espera deve ser acompanhada por protocolo, com mediana e P90 medidos na linha de base e nos períodos, antes de fixar percentual de redução. Reagendamentos e baixas administrativas têm indicadores próprios. Esta proposta não altera o texto oficial nesta etapa.

## Registro das mudanças e verificação

- Mantida a carteira 1, com parede e sem angio, em lugar de voltar a discutir carteiras alternativas.
- Substituída a afirmação de 137% sobre 13 salas por cálculo territorial e comparação explícita com até 20.
- Separadas horas realizadas, tempo de agenda e perdas, corrigindo a afirmação antiga de que faltas não mudam salas.
- Retirada a inferência de pedidos novos a partir de tentativas de agenda.
- Substituídos crescimento apenas positivo e oferta agendada por balanços com produção estimada, contração e defasagem.
- Acrescentados cenários de divisão da produção com a SES e distinção entre transferência e expansão líquida da rede.
- Identificadas as distribuições antigas, a parcela sem origem geográfica validada e as pendências de medição.
- Custos e cotação médica não foram reabertos.

Verificação independente: 8395 conferências, 31432 fórmulas e nenhum erro de fórmula Excel identificado. Conferidos meta, valor, horas, arredondamento por polo, balanços de todos os cenários, conservação de horas no remanejo e hashes das cópias e origens. O cálculo independente valida a implementação, não as premissas nem a viabilidade clínica/territorial. As prévias da planilha ficam em `verificacao`.

Para regenerar: executar `scripts/preparar.py`, `scripts/gerar_planilha.mjs` e `scripts/verificar_e_relatar.py`, nesta ordem, com Python/openpyxl de leitura e Node com `@oai/artifact-tool`. Os scripts antigos são evidência preservada, não geradores desta revisão. As fontes já copiadas permitem reproduzir os cálculos sem nova consulta ao painel.
