# O que os outros planos já contratam — exames, OCI e procedimentos de imagem

**Controle interno, 02/11/2026.** Este estudo é separado do estudo das filas do plano 4. Ele serve para saber
quais filas e públicos já têm dono, e evitar que um pedido entre em dois planos. **Nenhum outro plano será
alterado.**

- **Planilha:** `estudo_outros_planos_imagem_20261102.xlsx`, com cinco abas: Planos aprovados, Imagem nas OCI,
  Transvaginal e GIN1, Nossos planos em elaboração e Fontes.
- **Script:** `estudo_outros_planos_imagem_20261102.py`.

**O que conta como "outro plano":** só os planos aprovados e assinados com a SES-DF que estão no acervo
(`estudo/normalizados`, `registros/acervo.csv`). Os nossos planos em elaboração ficam numa lista à parte e não
cobrem fila nenhuma (seção 4). O redacao_07 está no campo das ideias (usuário, 02/11/2026).

## 1. Os planos aprovados

| plano | convênio | proponente | assinado | o que contrata (Meta 2) | controle externo |
|---|---|---|---|---|---|
| pt_ses_01 | 030989/2026 | ISHP | 29/04/2026 | OCI 09.05.01.003-5, oftalmologia a partir de 9 anos: 36.000, a R$ 160 | Representação 28/2026 no TCDF; a Decisão 1500/2026 pediu esclarecimentos, e o caso foi à pauta de 28/09 |
| pt_ses_02 | 030975/2026 | IEV | 29/04/2026 | OCI de ortopedia 001-1: 38.594; 002-0: 12.070; 004-6: 16.700 | Representação 31/2026; a Decisão 1501/2026 pediu esclarecimentos |
| pt_ses_03 | 030976/2026 | IEV | 29/04/2026 | OCI de ortopedia 004-6: 11.430 | idem |
| pt_ses_04 | 030977/2026 | IEV | 29/04/2026 | 10 OCI: GIN1 3.218; ortopedia 001-1 14.192, 002-0 7.000, 003-8 539; risco cirúrgico 4.647; insuficiência cardíaca 1.000; coronariana 900; déficit auditivo 6.250 e 5.340; próstata 1.015 | idem |
| pt_ses_05 | 031061/2026 | ISHP | 09/07/2026 | OCI 09.05.01.001-9, oftalmologia de 0 a 8 anos: 8.400, a R$ 200 | nenhuma no acervo |

- **As OCI de oftalmologia do ISHP não usam ultrassom nem TC.** A composição delas é consulta, teste ortóptico,
  tonometria, mapeamento de retina e biomicroscopia.
- **O IEV soma 122.895 OCI nos três convênios.**
- **Os termos de fomento (MROSC) do acervo não têm imagem:** IBCS e Instituto Impulsionar (oftalmologia e
  endocrinologia) e ADRA, já encerrado.

## 2. O exame de imagem dentro de cada OCI contratada

**Como ler a tabela:**
- **Obrigatório:** a OCI só se fecha com o exame. Então o número de OCI contratadas é o teto de exames daquele
  código.
- **Compatível:** o exame pode entrar, sem número fixo.
- **Fila:** a de hoje, sem as filas de emergência.

**Ultrassom e TC:**

| exame | OCI (IEV) | papel | OCI contratadas | fila hoje | o que o IEV executou no SISREG (até 26/10) |
|---|---|---|---:|---:|---|
| US de articulação 02.05.02.006-2 | 09.03.01.002-0, ortopedia com US | obrigatório | 19.070 | 14.355 | 642 consultas com CID da OCI, 308 realizadas; **nenhuma US agendada pela fila do exame** |
| US transvaginal 02.05.02.018-6 | 09.06.01.001-2, GIN1 | obrigatório | 3.218 | 9.295 | 60 consultas de ginecologia agendadas, 20 realizadas |
| US de próstata transretal 02.05.02.011-9 | 09.01.01.004-9, próstata | obrigatório | 1.015 | 22 | nenhuma consulta de urologia agendada |
| Eco de estresse 02.05.01.001-6 | 09.02.01.004-2, coronariana | obrigatório | 900 | 66 | entra pela consulta de cardiologia adulto |
| Ecocardiografia 02.05.01.003-2 | 09.02.01.006-9, insuficiência cardíaca | compatível | até 1.000 | 14.601 | idem: 1.138 agendadas para as duas OCI, 300 realizadas |
| TC de coluna, articulações, segmentos e pelve (sete códigos) | 09.03.01.003-8, ortopedia com TC | compatível; a OCI exige uma TC | até 539 no conjunto | 4.476, dos quais 3.954 na pelve | 250 consultas com CID da OCI, 94 realizadas |

**Radiologia e ressonância** (mapeadas; fora do foco agora):
- **as OCI de ortopedia 001-1, 002-0, 003-8 e 004-6:** 20 radiografias compatíveis de coluna e membros;
- **a 004-6:** seis ressonâncias compatíveis, com 28.130 OCI contratadas;
- **a 09.02.01.001-8 (risco cirúrgico, 4.647):** a radiografia de tórax.

A lista completa está na aba Imagem nas OCI.

**O que a tabela diz:**
- **O IEV não tira pedido das filas de exame.** A OCI dele entra pela consulta de especialidade, e o exame é feito
  dentro dela. Na US de articulação, os 19.070 exames contratados não passaram pela fila do exame. Ela segue com
  14.355 pedidos, e nenhum foi agendado numa unidade do IEV.
- **Mesmo assim, vale a regra de um pedido, um plano.** Um pedido da fila de exame com o CID da OCI poderia ser
  atendido pelo IEV, se o paciente voltasse pela consulta. O plano 4 tira esses pedidos e fica com o resto.
- **A execução do IEV é baixa.** Em 180 dias, a ortopedia agendou 30% do contratado
  (`output/mapeamento_iev_20261026.md`). Os três convênios estão sob representação no TCDF.

## 3. A transvaginal e a GIN1: medido em 02/11

A OCI GIN1 (09.06.01.001-2) tem a transvaginal como exame obrigatório e aceita 37 CID: C51 a C58, D25, N70 a N77
e N80 a N99. A L-008 não a citava. A medição de hoje passou na conferência (10/10) e está em
`dados/fontes/mapa_social_20261102_gin1.md`.

| fila | pedidos | com CID da GIN1 | parte | na fila viva | CID mais pedidos no recorte |
|---|---:|---:|---:|---:|---|
| ECOGRAFIA TRANSVAGINAL | 9.294 | **3.068** | 33% | 2.162 | N95 1.210, D25 387, N93 365, N92 213, N80 165 |
| USG TRANSVAGINAL | 1 | 0 | — | 0 | — |

- **Com a regra, 6.226 transvaginais ficam livres para o plano 4.**
- **O IEV pode fazer até 3.218 OCI GIN1.** É quase o tamanho do recorte, mas por enquanto quase não executa (20
  consultas realizadas).
- **Os CID mais pedidos fora da GIN1:** Z01 (exame ginecológico, 2.704), R10 (dor abdominal) e Z12 (rastreamento).

## 4. Nossos planos em elaboração: não contam

| pasta | o que é | na cobertura do plano 4 |
|---|---|---|
| redacao_06 | pré-plano do próprio plano 4 | é o próprio plano 4 |
| redacao_07 | pré-plano de imagem da Emenda de Bancada (R$ 1,5 mi): mamografia, densitometria, US e TC de cabeça e pescoço | **não conta: está no campo das ideias (usuário, 02/11/2026)** |
| redacao_08 | OCI de cardiologia do Instituto Fazer o Bem, em estudo (eco, ECG, ergométrico, radiografia) | não conta: fase 0, sem escolha |
| redacao_09 | MROSC de saúde mental infantojuvenil | sem imagem |

**Se o redacao_07 avançar,** ele terá de excluir o que o plano 4 tomar. Pela carteira recomendada, são a US de
bolsa escrotal, a US pélvica, a transfontanela e as TC de pescoço, crânio e face.

## 5. As regras que saem daqui para o plano 4

> **Superada em 02/11 pela seção 7.** Esta seção usa o CID do pedido como fronteira, o que não se sustenta. A regra
> que vale agora: a US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas ao IEV.

1. **Fora inteiras:**
   - **as TC de coluna, articulações e segmentos (522 pedidos):** são compatíveis com a OCI 09.03.01.003-8 (L-008,
     item 2);
   - **as partes moles (3.140):** decisão do usuário de 01/11.
2. **O código fica, sem os pedidos com o CID da OCI:**

| exame | OCI do IEV | pedidos com o CID | parte da fila | medido em |
|---|---|---:|---:|---|
| TC de pelve | 09.03.01.003-8 | 7 | 0,1% | 27/10 |
| US de articulação | 09.03.01.002-0 | 879 | 6% | 26/10 |
| Transvaginal | GIN1 | 3.068 | 33% | 02/11 |

3. **A próstata transretal (22), o eco de estresse e a ecocardiografia** não entram no plano 4, por outro motivo:
   pedem outro exame ou outra equipe.

## 6. A reserva do IEV: o que sobra para o plano 4

> **Superada em 02/11 pela seção 7.** Esta seção usa o CID do pedido como fronteira, o que não se sustenta. A regra
> que vale agora: a US de articulação fica fora inteira, e 4.000 transvaginais ficam reservadas ao IEV.

**A regra do usuário (02/11/2026):** o IEV se comprometeu com uma quantidade num prazo. O que passar disso, com
uma folga de 20% a 30% de faltas, o plano 4 pode pegar.

**Como a conta funciona:**
- **reserva** = OCI que faltam cumprir ÷ (1 − faltas);
- **sobra** = pedidos com o CID da OCI na fila do exame − reserva.

**Duas ressalvas sobre os números:**
- Só os pedidos com o CID da OCI podem virar OCI do IEV. Os que não têm o CID já são livres, com ou sem esta regra.
- Não há como saber quantas OCI o IEV realizou, porque o painel não mostra a APAC. A conta usa as consultas com o
  CID da OCI realizadas no IEV até 26/10. Se ele fez menos OCI que isso, a reserva fica maior.

A aba Reserva do IEV da planilha tem a conta completa.

| exame | OCI | fim da vigência | contratadas | realizadas até 26/10 | faltam | reserva (20% / 30% de faltas) | pedidos com o CID | sobra | sem o CID (já livres) |
|---|---|---|---:|---:|---:|---|---:|---:|---:|
| Transvaginal | GIN1 09.06.01.001-2 | 05/2027 | 3.218 | 20 | 3.198 | 3.998 / 4.569 | 3.068 | **0** | 6.227 |
| US de articulação | 09.03.01.002-0 | 08/2027 e 05/2027 | 19.070 | 308 | 18.762 | 23.452 / 26.803 | 879 | **0** | 13.476 |
| TC de pelve | 09.03.01.003-8 | 05/2027 | 539 | 94 | 445 | 556 / 636 | 7 | **0** | 5.037 |
| Próstata transretal | 09.01.01.004-9 | 05/2027 | 1.015 | 0 | 1.015 | 1.269 / 1.450 | 22 | **0** | 0 |

**Resultado: pela regra, nada sobra.** Em todos os exames, o que o IEV ainda tem a cumprir, mesmo sem a folga de
faltas, é maior que o número de pedidos com o CID dele na fila do exame. Isso confirma o que as carteiras já
fazem: pegam só os pedidos sem o CID, que somam 6.227 na transvaginal, 13.476 na articulação e 5.037 na TC de pelve.

**O prazo muda a conta.**
- **Fim das vigências:**
  - Fila Zero (030977): começou em 25/04/2026, com 13 meses de vigência, e termina por volta de 25/05/2027;
  - DOA (030975): começou em 15/04/2026, com 16 meses, e termina por volta de 15/08/2027.
- **Depois disso, a reserva cai para zero,** e os pedidos com o CID ficam livres.
- **Exemplo:** se o plano 4 começar em 2027 e passar desses meses, os 3.068 pedidos de transvaginal com o CID da
  GIN1 poderiam entrar na segunda metade da execução.
- **O ritmo do IEV mostra que ele não deve cumprir tudo.** Na GIN1, fez 20 consultas em seis meses. Mas o
  compromisso é do convênio, e a regra reserva a quantidade contratada, não o ritmo.

**Origem dos números:**
- **vigência e início:** o item 12 de cada plano;
- **contratadas e realizadas:** `output/ocis_iev_20261027.md` e `output/mapeamento_iev_20261026.md`;
- **pedidos com o CID:** `dados/fontes/mapa_social_20261102_gin1.md` (transvaginal) e `output/mapeamento_iev_20261026.md`
  (articulação e TC de pelve).

## 7. Como avaliar a sobreposição com outro plano: o método

**Por que esta seção existe.** Até 02/11, este estudo tratou o CID do pedido como a fronteira entre o plano 4 e o
IEV: "o pedido com o CID da OCI é do IEV, o resto é livre". Essa fronteira não existe na prática. A conta gerou
números (879, 3.068, sobra zero) que pareciam limites e não eram, e uma confusão que não precisava ter acontecido.
A pergunta certa é outra: **o que o outro plano pode atender, pelo que está escrito nele, e quem decide para onde
vai cada pedido.**

**A ordem certa:**

1. **Ler o texto do outro plano antes de contar qualquer coisa.** Nos itens do objeto, do público-alvo, da porta de
   entrada, dos resultados esperados, das obrigações do executor e dos riscos, responder a quatro perguntas:
   - Quem é o público?
   - De que fila vem o paciente, e quem escolhe essa fila?
   - O plano promete reduzir quais filas?
   - Sob que condição ele cumpre a meta?
2. **Ver a composição da OCI** na Tabela Unificada: o que é exame obrigatório e o que é compatível. O obrigatório é
   o teto de exames daquele código.
3. **Ver a quantidade e o prazo:** quantas OCI foram contratadas, quando começa e quando termina a vigência.
4. **Ver a execução no SISREG** (Mapa Social): por qual fila o executor recebe pacientes e quanto já fez. Isso
   mostra como a regulação opera hoje, e não o que ela pode fazer amanhã.
5. **Só então medir por CID,** como estimativa do tamanho do público, e nunca como limite.

**Por que o CID não é fronteira:**
- A OCI se fatura com o CID que o médico do executor registra na APAC, e ele pode ser outro que o do pedido no
  SISREG.
- Quem escolhe de qual fila sai o paciente é a regulação da SES, e não o executor nem o CID.

**A regra que decorre daí (usuário, 02/11/2026):**
- **A fila é comprometida com o outro plano** quando o texto dele permite atendê-la e a quantidade contratada
  alcança o tamanho dela. É o caso da US de articulação: 19.070 OCI 002-0 contra 14.355 pedidos.
- **Quando a quantidade contratada é menor que a fila,** reserva-se a ela a quantidade que falta cumprir, com uma
  folga de 20% a 30% de faltas. É o caso da transvaginal: 3.218 OCI GIN1, com 4.000 pedidos reservados.
- **O que passar disso fica para o plano 4.**
- **O prazo também conta.** Depois do fim da vigência do outro plano, a reserva acaba.

## 8. Como o IEV escreveu o plano, e o que levar para a nova versão do plano 4

**O plano do IEV (pt_ses_02, 030975; o pt_ses_04, 030977, segue o mesmo modelo) é escrito de forma abrangente:**

| item do plano do IEV | o que diz, em resumo | o efeito |
|---|---|---|
| 5. Objeto | OCI de ortopedia para usuários regulados pela SES/DF, com a realização integrada de radiografia, ultrassom e ressonância | não amarra a uma fila |
| 5.2 Resultados esperados | "Redução do tempo de espera nas filas reguladas para exames de radiografia, ultrassom e ressonância magnética" | reivindica também as filas de exame, não só a de consulta |
| 6.1 Público-alvo | usuários regulados pela SES/DF "encaminhados para avaliação diagnóstica ortopédica"; no 030977, "inseridos na fila regulatória" | qualquer fila regulada serve |
| 6.1 Seleção | "exclusivamente por meio do sistema de regulação", sem captação própria | a escolha da fila é da SES |
| 7 Obrigações | recebe "exclusivamente as demandas encaminhadas pela SES/DF", e o encerramento no sistema garante a "atualização contínua da fila" | idem |
| 13.7 Riscos | "a execução do projeto está condicionada ao envio regular, contínuo e suficiente da demanda regulada" | protege o executor se a SES não mandar paciente |
| Metas | quantidade de OCI, sem número de fila a zerar | nenhuma promessa sobre o estoque |

**Como a v26 do plano 4 está escrita, para comparar:**
- **1.4:** a meta é a "fila de regulação na data da extração" mais uma parte das entradas. A 3.1 diz que o convênio
  "resolve a totalidade das 78.572 solicitações da extração".
- **4.1:** o público é o usuário "com solicitação de exame de ultrassonografia ou de tomografia computadorizada
  pendente de agendamento na fila de regulação".
- **O que já é igual ao IEV:**
  - a seleção só pela regulação, sem captação própria (4.1 e 4.5);
  - o risco de a demanda regulada não chegar (R-07);
  - o remanejamento entre procedimentos quando uma fila se esgota (1.4).

**O que levar para a nova versão** (para decidir; o texto do plano não foi alterado):
1. **Público-alvo amplo, como o do IEV:** usuários regulados pela SES-DF com indicação de exame de ultrassonografia
   ou de tomografia, encaminhados pela regulação. Sem amarrar a uma fila nem a uma extração.
2. **A meta como capacidade oferecida à regulação,** e não como estoque a zerar. Sai o "resolve a totalidade das N
   solicitações"; a fila apurada fica como justificativa, e não como compromisso.
3. **Uma cláusula de não sobreposição que põe a decisão na SES:** a regulação não encaminha ao convênio solicitação
   já vinculada a OCI em execução por outro convênio. É simétrico ao que o IEV escreveu, e protege os dois lados
   diante do TCDF.
4. **A execução condicionada ao envio da demanda regulada,** como o 13.7 do IEV, e não só como risco (R-07).
5. **Resultados esperados por fila, sem número fechado:** "redução do tempo de espera nas filas reguladas de
   ultrassonografia e tomografia", como o IEV fez com as dele.

Escrito assim, o plano 4 fica no mesmo pé que o IEV: os dois atendem a demanda que a regulação mandar, e quem
evita a sobreposição é a SES. Uma promessa de zerar uma fila que outro plano também pode atender deixa de existir.
