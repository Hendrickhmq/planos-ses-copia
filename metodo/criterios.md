# criterios.md — o que aprova, o que o controle ataca e o que é boa prática

> Gerado por `python3 ferramentas/consultar.py criterios` a partir de `registros/licoes.csv`.
> Não editar à mão: corrigir a lição e gerar de novo.

45 lições: 39 no eixo da administração, 6 no da qualidade. Cada uma é uma regra para o nosso plano, destilada do que os cinco planos aprovados fizeram, do que a norma e o termo exigem e do que o controle externo atacou depois da aprovação.

Como ler:

- **reprova** — a análise da SES-DF ou o termo barram;
- **questiona** — passou na SES-DF, e o controle externo atacou ou atacaria;
- **melhora** — boa prática, que separa o plano excelente do mínimo viável;
- **verificação** — `automática`: o `conferir_plano.py` confere sozinho; `parcial`: confere uma parte e a pergunta cobre o resto; `manual`: só a pergunta;
- **origem** — os registros de onde a lição saiu. `python3 ferramentas/consultar.py <id>` abre cada um, com o que ele cita e quem o cita.

Para um plano em redação: `python3 ferramentas/consultar.py checklist planos/redacao_NN/`.

## Eixo 1 — Administração: o que aprova, o que reprova e o que o controle ataca

### Códigos SIGTAP

**LI-001** · erro · questiona — Escrever cada código SIGTAP - de OCI ou de procedimento avulso - com o dígito verificador certo e, ao lado, o nome exato da tabela, conferidos na ficha da competência vigente.

- Por quê: Três dos cinco aprovados erram código ou nome (09.03.01.004-0 por 004-6; a 004-2 chamada de 'Avaliação Cardiológica'; 09.02.01.001 sem dígito), e o MPCDF repetiu o código errado como prova de sobreposição.
- Verificação: parcial (W) — O nome de cada procedimento fora do grupo 09 confere com a ficha? (a W confere o dígito de todos e o nome só no grupo 09)
- Origem: AC-059, AC-017, AC-058, AC-060, CT-002, DD-003, DD-006

### Valor unitário

**LI-002** · acerto · reprova — Usar como valor unitário o da Tabela SUS Candanga, qualquer que seja a origem do recurso - emenda federal ou distrital -, quando o código estiver no Anexo Único da Deliberação CG-SES 46/2026, na modalidade do objeto (SIA ou SIH), e citar a fonte na coluna de referência da linha. Se o SIGTAP vigente for igual ou maior que o valor do Anexo, vale o SIGTAP vigente. Código fora do Anexo: a tabela do SIGTAP na competência vigente, sem ajuste - o total ambulatorial da OCI, ou o valor do procedimento acrescido do incremento que a portaria dá à habilitação do executor -, e o plano diz que o código não está na Candanga.

- Por quê: Regra do usuário de 01/11/2026: a Tabela SUS Candanga passa a ser a precificação, inclusive com recurso federal. A Lei distrital 7.897/2026 manda financiar a remuneração com recursos de emendas, distritais e federais, e recursos próprios do DF (art. 5º) e veda remuneração em contrato ou convênio em desconformidade com a Candanga (art. 6º); a Deliberação 46/2026 a faz referência remuneratória de contratos, convênios e credenciamentos (art. 3º) e manda remunerar pelo valor do Anexo (art. 5º). O valor do Anexo já contém o SIGTAP: a complementação distrital é a diferença (Deliberação 46/2026, art. 4º, § 5º; Lei 7.897/2026, art. 4º, § 1º), e o reajuste do SIGTAP a reduz (Lei 7.897/2026, art. 4º, § 3º); quando o SIGTAP vigente alcança o Anexo, a complementação é zero e o SIGTAP fica - 12 OCI estão assim em 09/2026 (a coluna alerta da tabela). Até 31/10/2026 a regra era emenda federal, SIGTAP, porque o art. 4º, § 1º, põe o complemento no recurso próprio e as Deliberações CG-SES 17/2022 e 17/2024, art. 3º, vedam o federal nas tabelas diferenciadas anteriores; a Candanga é posterior e diz, no art. 5º, que a emenda federal financia a remuneração. O Anexo Único oficial (SEI 212117347) chegou em 01/11/2026, e o valor dele não é o Valor Máximo da análise comparativa de 06/08/2026: o ultrassom de abdômen total vale R$ 117,51 no Anexo e R$ 334,88 no Máximo. Os aprovados de 2026, anteriores à Candanga, usam a tabela de abril de 2026; a Lei 8.080 manda remunerar pelos valores da direção nacional do SUS, e a GM/MS 12.116/2026 deixou cada ente pagar acima dela.
- Verificação: parcial (V, W) — A linha de cada procedimento cita a fonte do valor - a Tabela SUS Candanga, ou, fora dela, o SIGTAP e, se houver, a portaria do incremento?
- Origem: AC-069, AC-015, OB-003, DD-003, DD-006, NM-092, NM-099, NM-093, NM-095, NM-096, NM-105

**LI-003** · erro · questiona — Tirar valor e nome da tabela vigente, nunca da portaria que criou o procedimento nem de outro plano, e reconferir a ficha perto do protocolo.

- Por quê: O pt_ses_04 citou R$ 435,00 da Portaria 1.822/2024 para uma OCI que vale R$ 840,00 desde pelo menos 01/2025 e trocou os valores de duas OCI cardiológicas; a de câncer gástrico passou de R$ 250,00 a R$ 600,11 em 08/2026.
- Verificação: parcial (V, W) — A ficha do SIGTAP usada é da competência corrente na data do protocolo?
- Origem: AC-014, AC-058, DD-003

### Objeto e unidade de aferição

**LI-004** · acerto · reprova — Descrever o objeto pela unidade que se afere: a OCI como conjunto executado inteiro - a composição do SIGTAP, com todos os secundários e o retorno -, sem triagem nem avaliação simplificada; o exame avulso como exame realizado, laudado e entregue.

- Por quê: É cláusula do termo, idêntica nos cinco convênios, e a origem da frase 'não se caracterizando como triagem' dos planos do ISHP.
- Verificação: parcial (X) — A seção do objeto diz a unidade de aferição e, na OCI, transcreve a composição e diz que ela é executada inteira?
- Origem: OB-047, AC-067, AC-073

**LI-006** · erro · questiona — Declarar o público-alvo com a faixa etária e o sexo da ficha do SIGTAP, sem herdar faixa de outro plano.

- Por quê: O pt_ses_05 escreveu 'a partir de 0 a 8 anos', resto do molde do pt_ses_01 ('a partir de 9 anos'); o MPCDF atacou faixa etária sem justificativa no TF 031000.
- Verificação: parcial (V) — O sexo do público-alvo é o da ficha do SIGTAP?
- Origem: AC-069, CT-004, DD-003

### Enquadramento no CNES

**LI-039** · erro · questiona — Conferir, antes de escrever, o CNES de cada estabelecimento executor contra a ficha de cada procedimento: tipo de estabelecimento, serviço e classificação atendendo SUS, profissional com o CBO exigido vinculado, equipamento e habilitação.

- Por quê: O IEV é, no CNES, consultório isolado que não atende SUS e executa em clínicas de terceiros - o que o MPCDF chamou de quarteirização; nenhum executor dos aprovados tem habilitação, e nenhum plano fala do enquadramento.
- Verificação: manual — O CNES de cada polo tem o serviço, a classificação, o CBO e o equipamento que a ficha de cada procedimento pede, atendendo SUS?
- Origem: AC-077, DD-005, DD-006, CT-002, OB-026

**LI-040** · erro · questiona — Quando o valor do exame levar o incremento da habilitação 38.01, 38.05 ou 38.06, confirmar com a SES-DF que o estabelecimento executor tem ou terá a habilitação - a 38.01 é marcada pelo gestor por ato publicado e exige o Núcleo de Gestão do Cuidado (170/002).

- Por quê: O incremento não é da tabela, é da habilitação (+313% no ultrassom, +116% a +120% na tomografia), e nenhum executor dos aprovados a tem.
- Verificação: manual — O executor tem a habilitação que dá o incremento usado no valor unitário, ou há ato da SES-DF previsto para marcá-la?
- Origem: OB-053, OB-054, AC-077, DD-006

### Metas e indicadores

**LI-012** · acerto · reprova — Estruturar as metas para prestação de contas parcial a partir do 3º mês e prever relatórios mensais de atividades.

- Por quê: O termo condiciona as parcelas seguintes à prestação parcial a partir do terceiro mês, em cláusula igual nos cinco convênios; as segundas parcelas do IEV não tinham saído até 25/09/2026.
- Verificação: manual — A primeira apuração cai até o 3º mês, e o plano prevê relatório mensal?
- Origem: OB-043, OB-052, AC-073, AC-076

**LI-007** · erro · questiona — Fazer as metas parciais somarem exatamente o quantitativo contratado, compensando o arredondamento na última parcela.

- Por quê: Nos planos do IEV as parcelas bimestrais não somam o total, e no Fila Zero faltam 790 OCI de otorrino no cronograma; o que se afere na prestação de contas é a parcela datada.
- Verificação: parcial (D) — A soma das metas parciais de cada procedimento é igual ao quantitativo do objeto?
- Origem: AC-053, AC-054

**LI-008** · erro · questiona — Conferir cada data de apuração: dia e mês válidos, dentro da vigência do termo.

- Por quê: O pt_ses_02 foi aprovado com a data 25/19/2026 em três metas.
- Verificação: manual — Todas as datas do quadro de metas existem e caem dentro da vigência?
- Origem: AC-055

**LI-009** · erro · questiona — Publicar a memória de cálculo do quantitativo: a fila regulada dos pacientes da finalidade do objeto, com fonte e data, capacidade instalada e o motivo do número. A fila não é a de todo CID que a APAC aceita: na OCI de CID largo, ela é a dos CID que dão nome à OCI.

- Por quê: A primeira crítica do MPCDF ao pt_ses_01 foi a meta de 36.000 OCI sem memória de cálculo. Numa contratação de médicos pela SES-DF, o TCDF pediu o dimensionamento do déficit e os critérios dos quantitativos, e mandou demonstrar que a contratação é suplementar e subsidiária (Decisão 2445/2026). No redacao_08 (22/10/2026), o capítulo I inteiro deu 50.317 pessoas para a OCI de insuficiência cardíaca, a maior parte com hipertensão: a memória de cálculo que o controle refizesse acharia outro número.
- Verificação: parcial (C, I) — Quem lê o plano consegue refazer a conta que dá o quantitativo?
- Origem: CT-001, AC-070, AC-018, AC-020, CT-012

**LI-011** · erro · questiona — Ligar cada meta ao objeto e dar a cada indicador fórmula, numerador, denominador e fonte, com medida de quantidade e de qualidade, sem repetir o indicador genérico de 'conformidade técnica'.

- Por quê: Os quatro primeiros aprovados têm o mesmo indicador, palavra por palavra, e a seção de parâmetros de aferição do IEV não tem parâmetro nenhum. O TCDF recomendou à SES-DF exigir planos de trabalho com metas ligadas ao objeto e aferíveis em quantidade e em qualidade, num termo de fomento custeado por emenda que acabou em tomada de contas especial (Decisão 2325/2026).
- Verificação: parcial (P, S) — Cada meta mede o objeto, e cada indicador pode ser calculado por terceiro a partir da fonte indicada?
- Origem: AC-036, AC-047, OB-011, CT-009

**LI-013** · acerto · questiona — Usar como meio de verificação os registros oficiais (SISREG, TrakCare, SIA/SUS) somados ao relatório do executor, nunca o relatório sozinho: cada atendimento pago se rastreia até o paciente regulado e o registro no sistema oficial, e o que se paga bate com o que se comprova.

- Por quê: É o desenho dos planos do IEV, e a prestação de contas exige registros de atendimento. O TCDF mandou inspecionar exatamente isto num termo de fomento da SES-DF: a comprovação dos atendimentos, a rastreabilidade dos beneficiários, a aderência aos sistemas oficiais e a compatibilidade entre o pago e o comprovado (Decisão 2426/2026). Num credenciamento de médicos, o TCDF pediu à SES-DF o modelo de execução e fiscalização, com o controle de escalas, de frequência e da produção assistencial (Decisão 2445/2026).
- Verificação: manual — Cada atendimento que o plano paga tem registro oficial e paciente rastreável, e o meio de verificação não é só o relatório do executor?
- Origem: AC-038, AC-025, OB-024, CT-008, CT-012

### Dimensionamento

**LI-014** · erro · questiona — Dimensionar o tempo de atendimento pela composição do procedimento - a OCI inteira; o exame com preparo e laudo -, com fonte; não prometer 12 minutos para consulta com exames.

- Por quê: O MPCDF chamou de 'clinicamente impossível' o parâmetro de 5 atendimentos por hora do pt_ses_01, e o pt_ses_05, assinado depois, o repetiu.
- Verificação: parcial (G, T) — O tempo por atendimento tem fonte e comporta a composição completa do procedimento?
- Origem: CT-001, AC-070, AC-072

**LI-015** · erro · questiona — Fazer as horas profissionais declaradas comportarem a meta: horas vezes atendimentos por hora igual ou maior que o quantitativo.

- Por quê: No pt_ses_05, 1.600 horas a 4 ou 5 atendimentos por hora dão 6.400 a 8.000 atendimentos para uma meta de 8.400.
- Verificação: parcial (G) — Horas vezes produtividade dão, no mínimo, a meta?
- Origem: AC-056

### Custo de apoio

**LI-019** · erro · reprova — Não prever taxa de administração, de gerência ou similar; a gestão entra posto a posto na planilha.

- Por quê: Vedação do termo, igual nos cinco convênios.
- Verificação: automática (X)
- Origem: OB-051, AC-073

**LI-038** · acerto · reprova — Dimensionar o apoio pela folga entre o que o procedimento paga e o que custa executá-lo: o que paga bem leva apoio pequeno; o que paga mal leva mais, com cada linha justificada e sem publicar o percentual no plano.

- Por quê: É o critério que a SES-DF aplica, segundo contato direto do usuário, e os aprovados o seguem: 36,6% de apoio a R$ 129 de valor médio, cerca de 31% entre R$ 160 e R$ 360, e 8% a 8,5% nos nossos de valor alto.
- Verificação: parcial (C) — O peso do apoio é coerente com a folga do procedimento, e a compensação do que paga mal está justificada linha a linha?
- Origem: AC-075, AC-015, CT-002

**LI-017** · erro · questiona — Justificar cada custo fora do valor do procedimento como indispensável ao objeto e não coberto pelo unitário.

- Por quê: O MPCDF comparou os convênios do IEV com o credenciamento, em que a OCI já paga todos os custos: só 63% a 69% do global ia ao atendimento, e a economia seria de mais de R$ 10 milhões.
- Verificação: manual — Para cada linha da Meta 1: por que o valor do procedimento não a cobre?
- Origem: CT-002, AC-071, AC-015, OB-021, OB-022

**LI-018** · erro · questiona — Não pagar apoio assistencial (auxiliar de exame, preparo, apoio ao médico) em rubrica de apoio quando o plano diz que o unitário remunera o atendimento.

- Por quê: O pt_ses_01 tem 12 postos assistenciais na Meta 1 e afirma que os equipamentos da consulta estão 'integralmente contemplados no valor unitário'.
- Verificação: manual — Algum posto da Meta 1 faz parte do atendimento que a OCI já paga?
- Origem: AC-066, AC-009

**LI-020** · erro · questiona — Limitar a comunicação a ação educativa ou informativa prevista no plano; nada de audiovisual, fotografia, jornalismo, brindes ou kits.

- Por quê: O termo só admite publicidade educativa e prevista, e o MPCDF atacou a comunicação audiovisual do pt_ses_01 e os R$ 172.946,00 de mídia e kits do TF 031000.
- Verificação: parcial (X) — Toda comunicação prevista é educativa ou informativa, e está descrita no plano?
- Origem: OB-049, CT-001, CT-004, AC-066, AC-070

**LI-045** · erro · questiona — Se o plano comprar equipamento ou material permanente, listar cada bem, dizer por que o objeto precisa dele e qual destino ele terá no fim da vigência, sem contradizer a cláusula do termo sobre os bens remanescentes.

- Por quê: A IN CGDF 01/2005 obriga o convênio que adquire equipamento ou material permanente a estipular o destino dos bens remanescentes (arts. 7º, IX, e 24), e a prestação de contas final traz a relação dos bens adquiridos (art. 26, VI). O TCDF mandou a SES-DF conferir, na prestação de contas de um termo de fomento, as despesas com bens permanentes e o destino deles, e evitar cláusulas contraditórias sobre isso (Decisão 2325/2026).
- Verificação: manual — O plano compra bem permanente? Então cada um está listado, justificado e com destino no fim da vigência, igual ao termo?
- Origem: CT-009, NM-011

### Preços e planilha

**LI-021** · erro · questiona — Pesquisar o preço de cada locação e serviço no mercado (portal imobiliário, preço por consultório ou por m², três orçamentos) e deixar o unitário sair da pesquisa, nunca de um total fixado antes, e guardar a memória de cálculo de cada unitário com as fontes, de modo que um terceiro refaça a conta.

- Por quê: O MPCDF estimou sobrepreço de 1.602% nos aluguéis do pt_ses_01, cujos quatro unitários quebrados somam exatamente R$ 515.800,00; no pt_ses_05 a linha do sistema fecha o global em R$ 2.000.000,00. O TCDF mandou a SES-DF instaurar tomada de contas especial por eventual sobrepreço num termo de fomento custeado por emenda federal, com audiência dos responsáveis para multa (Decisão 2325/2026), e cobrou dela, noutra contratação, a memória de cálculo dos preços unitários com as fontes e os documentos dos valores de referência (Decisão 2985/2026).
- Verificação: manual — Cada unitário de apoio tem pesquisa de preço com a fonte guardada, e nenhum total redondo foi fixado antes do unitário?
- Origem: CT-001, AC-070, AC-057, OB-014, CT-009, CT-012

**LI-022** · erro · questiona — Fazer descrição, quantidade e frequência da mesma linha dizerem a mesma coisa, com a frequência acompanhando a vigência.

- Por quê: '12 notebooks' com quantidade 16, 'até 8 impressoras' com 10, internet por 10 meses numa vigência de 9 e 16 locações declaradas contra 18 somadas, todos no pt_ses_01.
- Verificação: parcial (A, R) — Cada linha da planilha tem descrição, quantidade e frequência coerentes?
- Origem: AC-001, AC-002, AC-003, AC-066

### Sobreposição entre convênios

**LI-023** · erro · questiona — Se o proponente tem outro convênio, delimitar objeto, códigos, unidades e equipes de cada um e ratear o custo compartilhado com método declarado.

- Por quê: Os três convênios do IEV pagam a mesma OCI e a limpeza das mesmas unidades (R$ 1.043.460,00 somados), e a gestão só num deles; o MPCDF tratou a coincidência de códigos como prova de identidade de objeto.
- Verificação: manual — O que este convênio paga que nenhum outro do mesmo proponente já paga?
- Origem: CT-002, AC-063, AC-064, AC-071, AC-068

### Capacidade do executor

**LI-025** · acerto · reprova — Relacionar no plano toda obrigação que será subdelegada; sem previsão expressa a subdelegação é vedada, e nunca pode ser da execução inteira.

- Por quê: Cláusula do termo, igual nos cinco convênios, e art. 33 do Decreto 48.727/2026.
- Verificação: manual — Tudo o que será feito por terceiro está listado, e o núcleo assistencial fica com o executor?
- Origem: OB-050, OB-020, AC-073

**LI-024** · erro · questiona — Demonstrar capacidade própria: CNES com profissionais e equipamentos, experiência comprovada nas atividades centrais do objeto, em cada especialidade dele, e, se a execução for em estabelecimento de terceiro, o vínculo formal com ele. A sede e os locais de execução precisam estar em condições de receber a visita da SES-DF.

- Por quê: A COASIS registrou o IEV no CNES como consultório isolado e o MPCDF tratou a execução em clínicas de terceiros como quarteirização; o ISHP foi atacado por CNPJ distrital recente e sem experiência comprovada. Numa parceria custeada por emenda, o TCDF só deixou a SES-DF seguir depois que ela comprovou a experiência prévia da entidade nas atividades centrais do projeto e a capacidade técnica dos profissionais de cada especialidade, com o relatório da visita à sede e ao local de execução (Decisões 1636 e 2509/2026).
- Verificação: manual — O CNES do executor mostra a equipe e os equipamentos que o plano usa, e há prova de experiência em cada especialidade do objeto?
- Origem: CT-001, CT-002, AC-070, AC-071, OB-026, CT-011

### Instrumento, base legal e recurso

**LI-027** · acerto · reprova — Declarar a fonte do recurso: emenda, número, autor e funcional programática.

- Por quê: Nenhum dos quatro primeiros aprovados diz de onde vem o dinheiro, e as portarias das emendas exigem coerência com o Plano de Saúde e funcional própria.
- Verificação: manual — O plano identifica a emenda e a funcional que o custeiam?
- Origem: AC-011, OB-030, OB-037, OB-040

**LI-028** · acerto · reprova — Prever a publicação, em sítio próprio, dos valores recebidos e aplicados da emenda.

- Por quê: A portaria das emendas obriga a entidade privada sem fins lucrativos a publicar os valores.
- Verificação: manual — O plano prevê onde e quando os valores da emenda serão publicados?
- Origem: OB-038

**LI-043** · erro · reprova — Em ano eleitoral, conferir com a SES-DF, antes da assinatura, da liberação e de qualquer divulgação, as restrições da Lei 9.504 que o Decreto 48.727 manda observar.

- Por quê: O art. 40 do Decreto 48.727/2026 submete celebração, liberação e divulgação dos convênios às regras eleitorais; o art. 73, VI, da Lei 9.504 restringe publicidade institucional e transferências nos três meses anteriores ao pleito.
- Verificação: manual — A assinatura, as parcelas e a divulgação do convênio caem no período eleitoral, e a SES-DF se manifestou sobre isso?
- Origem: OB-028, NM-010, NM-076

**LI-026** · erro · questiona — Escolher o instrumento pelo objeto. Serviço assistencial complementar ao SUS (OCI, exame, consulta, procedimento) é convênio, com o vocabulário e a base legal dele (Lei 14.133/2021, Decreto 44.330/2023, Decreto 48.727/2026), nunca MROSC (OSC, parceria, termo de fomento, Decreto 37.843/2016). O MROSC cabe à promoção da saúde, sem prestação direta de serviço assistencial.

- Por quê: O MPCDF sustenta que o MROSC não se aplica a serviço complementar ao SUS, e a própria SES-DF o reconheceu em nota técnica; os planos do ISHP ainda citam o Decreto 37.843. Em 10/08/2026 o TCDF determinou à SES-DF o instrumento do art. 199, § 1º, da Constituição para a prestação direta de serviços assistenciais complementares ao SUS e a alertou a não usar a Lei 13.019 nesses ajustes (Decisão 2426/2026). A promoção da saúde segue pelo MROSC (usuário, 10/10/2026).
- Verificação: manual — O objeto é serviço assistencial? Então o plano usa o vocabulário e a base legal do convênio; se for promoção da saúde, o MROSC cabe.
- Origem: CT-004, AC-045, AC-062, OB-041, OB-005, CT-008

**LI-042** · acerto · questiona — Documentar a origem do recurso antes de fechar o cronograma: número e tipo da emenda, o ofício de indicação à SES-DF (e a ata, se for de bancada ou de comissão) e a confirmação da ARINS de que o recurso está no FSDF, em que fonte específica e programa de trabalho, e se o crédito adicional já entrou no orçamento do Fundo.

- Por quê: O Ministério aprova a proposta do ente e paga ao Fundo; o plano da entidade só a SES-DF analisa, e o recurso costuma já estar no FSDF quando a entidade é indicada. Os termos do ISHP e do IEV repartem uma emenda de bancada de 2025, re-indicada por ofício de fevereiro de 2026, e nenhum cita o ofício nem a ata que a LC 210/2024 exige. Pela Portaria SES-DF 98/2025, o recurso recebido só vira dotação empenhável depois do crédito adicional no orçamento do Fundo.
- Verificação: manual — O plano cita o número da emenda e o ofício de indicação (ou a ata), e a ARINS confirmou que o recurso está no FSDF, com o crédito adicional aberto?
- Origem: AC-078, CT-001, NM-074, NM-054, NM-032, NM-085, NM-086

### Desembolso e vigência

**LI-029** · erro · reprova — Copiar do termo o valor global, a vigência e a data de início, usar o mesmo valor, ao centavo, na planilha, no quadro de metas e no cronograma, e conferir o plano contra o termo assim que ele sair.

- Por quê: O plano do DOA ficou R$ 2.000,00 abaixo do termo, com um mês a mais de vigência e início antes da assinatura; o pt_ses_05 declara 8 meses e o termo, 7; e a SES-DF pagou a 1ª parcela do DOA e do Fila Zero pelo valor do plano e do quadro de metas, não pelo do termo.
- Verificação: manual — Valor, vigência e início do plano são os do termo?
- Origem: AC-074, AC-061, AC-006, AC-076, EX-001

**LI-030** · acerto · reprova — Datar o primeiro desembolso logo após a assinatura, nunca antes dela, e as parcelas seguintes em consonância com as metas e a prestação parcial.

- Por quê: A SES-DF apostilou os três termos do IEV para dizer isso, e o termo do ISHP de julho já nasceu com a regra; os planos do IEV datavam a 1ª parcela de 24/04, antes da assinatura, e ela saiu em 15/05.
- Verificação: manual — A primeira parcela sai na assinatura, e as demais seguem as metas?
- Origem: IT-006, IT-007, IT-008, OB-042, OB-015, EX-003, AC-032, AC-076

### Registro e faturamento no SUS

**LI-032** · erro · questiona — Dizer como a produção vai ao SIA/SUS pelo instrumento da ficha (APAC da OCI com principal e secundários; BPA ou APAC do exame), que só a produção aprovada conta e como se evita pagamento em duplicidade entre FAEC e convênio.

- Por quê: Nenhum aprovado trata glosa, FPO, competência ou duplo pagamento; o pt_ses_02 tem a melhor redação sobre registro por APAC.
- Verificação: manual — O plano explica o caminho da APAC até a produção aprovada e o que impede pagar duas vezes?
- Origem: AC-012, AC-023, AC-024, AC-026, AC-027, AC-028, OB-009, OB-010, DD-006

### Controle social

**LI-033** · erro · questiona — Registrar a ciência ou deliberação do Conselho de Saúde do DF e a coerência com o Plano de Saúde e a Programação Anual.

- Por quê: O MPCDF apontou a falta de oitiva do Conselho nos três convênios do IEV, e a coerência com o Plano de Saúde é requisito de elegibilidade da emenda.
- Verificação: manual — Há registro do Conselho de Saúde e da coerência com o PDS e a PAS?
- Origem: CT-002, OB-030

### Redação

**LI-035** · erro · questiona — Não reaproveitar texto de outro projeto: experiência prévia, números, equipamentos e exames que o objeto não tem.

- Por quê: Parágrafos idênticos com o mesmo número em três planos do IEV; o DOA prevê assistentes para tomografia que não contrata; o pt_ses_05 herdou faixa etária do pt_ses_01; e os termos da própria SES-DF saíram com cláusula de oftalmologia em ortopedia.
- Verificação: manual — Cada número e cada exame citado pertence a este objeto?
- Origem: AC-013, AC-065, AC-069, AC-073

### Uso do acervo

**LI-036** · erro · questiona — Não copiar parâmetro de plano aprovado sem ver se ele está entre os atacados pelo controle externo.

- Por quê: Quatro dos cinco aprovados estão sob representação do MPCDF no TCDF, e os cinco vêm de só dois proponentes.
- Verificação: manual — Algum parâmetro copiado de um aprovado foi atacado nas peças CT-001 a CT-004?
- Origem: AC-070, AC-071, AC-049, CT-001, CT-002

### Diligência da SES-DF

**LI-037** · acerto · reprova — Antecipar o que a análise da SES-DF costuma pedir: material de consumo item a item com memória mensal, cronograma de desembolso no Anexo I, locação como custo incremental e sistema já existente em vez de contratação nova.

- Por quê: É o que o Ofício 25/2026 cobrou do ISHP no pt_ses_05, a única diligência do acervo.
- Verificação: manual — O plano já traz o que a diligência do pt_ses_05 pediu?
- Origem: AC-068, EX-001, EX-002, EX-003, EX-004, EX-005

**LI-044** · erro · questiona — Fazer cada reapresentação do plano substituir a anterior por inteiro: número da versão e data no documento, o que mudou dito no ofício e uma só versão valendo no processo.

- Por quê: O TCDF recomendou à SES-DF evitar a proliferação de versões dos planos de trabalho, num termo de fomento custeado por emenda que acabou em tomada de contas especial por eventual sobrepreço (Decisão 2325/2026). Com duas versões no processo, não se sabe qual meta e qual preço valem.
- Verificação: manual — O plano traz versão e data, o ofício diz o que mudou, e só esta versão vale no processo?
- Origem: CT-009

## Eixo 2 — Qualidade: o que é boa prática

### Objeto e unidade de aferição

**LI-005** · acerto · melhora — Definir quando a unidade está concluída - a OCI com secundários e retorno, o exame com o laudo entregue - e contar na meta só a concluída.

- Por quê: Nenhum aprovado define conclusão; sem a regra não se sabe o que se paga nem o que se afere.
- Verificação: manual — O plano diz o que é uma unidade concluída e conta só essas?
- Origem: AC-031, OB-047

### Metas e indicadores

**LI-010** · acerto · melhora — Distribuir a meta entre polos pela demanda regulada de cada Região de Saúde, com a conta publicada, e vedar seleção de demanda fora do SISREG.

- Por quê: O pt_ses_01 é o único com distribuição espacial proporcional à fila e com vedação expressa de mesclar filas regionais.
- Verificação: parcial (E) — A participação de cada polo sai da fila por região, e a conta está no plano?
- Origem: AC-021, AC-030

### Dimensionamento

**LI-016** · acerto · melhora — Tratar absenteísmo como variável de dimensionamento, ofertando vagas acima da meta de atendimentos realizados.

- Por quê: Só o pt_ses_01 faz isso, com taxa estimada de 20%.
- Verificação: manual — A oferta de vagas cobre a meta depois do absenteísmo esperado?
- Origem: AC-022

### Desembolso e vigência

**LI-031** · acerto · melhora — Separar pré-produção, produção e encerramento dentro da vigência, com a execução física, retorno incluído, terminando antes do fim do termo.

- Por quê: Os planos do IEV abrem com duas a quatro semanas de implantação e fecham com quatro de avaliação; nenhum aprovado distingue vigência física de financeira.
- Verificação: manual — A última OCI, com retorno, termina dentro da vigência?
- Origem: AC-033, AC-034, AC-035

**LI-041** · erro · melhora — Tratar o atraso da parcela seguinte como risco com medida: prestação parcial pronta no 3º mês e cronograma físico que não pare se a parcela atrasar um período.

- Por quê: As segundas parcelas dos três convênios do IEV não saíram até 25/09/2026, 40 a 70 dias depois da data prevista.
- Verificação: manual — O plano diz o que acontece com a execução se a parcela seguinte atrasar um período?
- Origem: AC-076, OB-043

### Riscos

**LI-034** · acerto · melhora — Montar a matriz de risco com probabilidade vezes impacto que fecha na aritmética, e uma escada de consequência para o descumprimento (remanejamento, compensação, devolução).

- Por quê: A matriz P x I dos planos do IEV não fecha, e o pt_ses_01 tem a única escada de consequência do acervo.
- Verificação: manual — Nível = P x I em todas as linhas, e o plano diz o que acontece se a meta não for cumprida?
- Origem: AC-051, AC-040, AC-042
