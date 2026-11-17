# comum.md — as regras que valem para as duas trilhas

Valem para o **pré-plano** e para o **plano de trabalho**. Cada trilha tem também as
suas regras próprias, em `pre_plano/` e em `plano/`. Uma regra mora num lugar só: se
está aqui, as trilhas apontam para cá e não a repetem.

As regras são numeradas para serem citadas: "comum, regra 4". Cada uma termina com a
**origem**, o plano e o episódio de onde veio. O caso completo fica no plano de origem.

---

## As fontes e os números

**1. Número não entra por plausibilidade.** Todo número vem do usuário, tem fonte com
data, ou fica como `[preencher]` no lugar exato. O número que o usuário dá é dado. Se
ele não bate com a fonte que se tem, a pergunta é *de que data é a minha fonte*, e não
*de onde ele tirou isso*.
*Origem: redacao_02, acordo de trabalho de 24/08/2026; redacao_03, o R$ 600,11 de 31/08/2026.*

**2. Antes de deduzir, conferir a fonte.** Quando a fonte está a um passo, ler a fonte;
não concluir por dedução nem por caso parecido.
- A **Tabela do SUS muda por portaria** a cada poucos meses. Compilação estadual ou
  agregador servem para achar o procedimento, nunca para fixar o valor vigente.
  Número que não bate com a tabela que se tem pede, antes de tudo, a portaria
  posterior.
- O **âmbito de uma norma** se lê no artigo de âmbito, não se deduz *a contrario*.
- **Antes de mexer em estrutura, conferir o modelo atestado** nos planos aprovados.
- **Nunca reestruturar nem concluir enquanto uma consulta sobre aquilo está rodando.**
- **Dado do proponente tem função.** Dois e-mails, dois CNPJs ou dois telefones podem
  ser dados diferentes com finalidades diferentes: matriz e filial, institucional e
  do representante. Conferir a função no acervo antes de apontar divergência, e só
  levar ao usuário o que o acervo não resolve.

*Origem: redacao_03, 31/08 e 01/09/2026 — o âmbito da IN CGDF 01/2005, o R$ 600,11
tratado como prêmio, a identificação refeita na direção errada; redacao_04, análise
da ISHP de 07/10/2026.*

**3. A ficha do procedimento no SIGTAP é fonte da fase 0.** Idade, sexo, quantidade
máxima, atributos complementares, habilitações e quantidades de compatibilidade só
existem lá. Portaria altera a tabela e nota técnica orienta, mas quem vale é a tabela
vigente na competência. A ficha vira arquivo em
`dados/fontes/sigtap_<código>_<competência>.md` antes de qualquer redação. Ela
descreve o procedimento **no programa federal**: financiamento FAEC, subtipo e
habilitações não viram condição de partida quando a execução é por convênio de emenda.
*Origem: redacao_03, devolutiva de 05/09/2026 (a faixa etária afirmada por analogia).*

**4. Ancoragem e segunda opinião.** Toda decisão do usuário passa por conferência em
fonte independente antes de virar texto. A ordem das fontes, da mais forte para a mais
fraca:

1. **A norma baixada e lida localmente:** `pdftotext` sobre o PDF em
   `biblioteca/normas/`, e também `biblioteca/extraidos_normas/<norma>/tabelas/*.csv`.
   O extrator manda para tabela o que o PDF diagramou em quadro, e há portaria cujo
   artigo alterador mora ali e não no `texto.md`.
2. **A extração dos aprovados:** `grep` em `estudo/normalizados/<plano>/texto.md`.
3. **O NotebookLM do plano:** serve para varrer os aprovados de uma vez e para segunda
   opinião sobre desenho. Resposta sem `sources_used` é indicativa, não transcrição:
   cruzar com 1 ou 2 antes de usar.
4. **Pesquisa na web:** só para achar a fonte, nunca para citar. O que se cita é o
   arquivo baixado.

*Origem: redacao_03, 01/09/2026 — a regra apanhou três erros; o art. 14 da Portaria
1.640/2024 estava numa tabela da extração.*

**5. Hierarquia de precedência.** Em conflito entre fontes, vale nesta ordem: a norma
(`registros/obrigacoes.csv`), o critério do professor ou revisor, a resposta a
diligência, a prática observada nos aprovados (`registros/achados.csv`). Entre normas,
vence a de hierarquia maior: constituição, lei, decreto, portaria ou resolução,
instrução normativa, nota técnica.
- **Achado nunca vence norma.** Se três aprovados fazem de um jeito e a norma diz
  outro, a norma manda.
- **Prática observada nunca vira exigência.** Só sobe quando se acha o dispositivo
  que a fundamenta.

*Origem: estudo dos aprovados, agosto de 2026.*

## O que o documento afirma

**6. O documento não cria régua contra o proponente.** Tudo o que se afirma vira
obrigação aferível na prestação de contas. Antes de escrever prazo, faixa de
tolerância, percentual ou quadro de condições com coluna de comprovação, perguntar
**qual norma exige isto**. Sem norma, o conteúdo é controle interno e migra para
`pendencias.md` ou `dados/`; não some. Meta e indicador se pactuam em 100%.
*Origem: redacao_03, devolutiva de 05/09/2026 — falhou oito vezes quando era só uma
pergunta a lembrar; virou a verificação S.*

**7. A citação normativa precisa de motivo.** Duas perguntas, nesta ordem:
- **O que muda no documento se esta citação sair?** Três respostas salvam a citação:
  ela **dá um número** que o documento usa; ela **protege** contra exigência que o
  analista poderia inventar; ela **autoriza** algo que ele estranharia sem âncora.
- **Esta citação entrega a régua para nos medirem?** Norma que obriga o **serviço
  licenciado**, e não o convênio, fica descrita e não citada: o conteúdo operacional
  permanece, o artigo sai.

Cada norma que sobrevive aparece uma vez, na seção que decide; as outras remetem a
ela. Norma que só sustentava uma seção cortada sai junto. Calibragem: os aprovados
citam de zero a duas normas no documento inteiro. Um documento com mais de dez normas
distintas precisa de justificativa de objeto.
*Origem: regra do usuário de 24/08/2026; redacao_02, cortes de 31/08/2026.*

**8. O documento é peça de instrução, não memorial — o teste do leitor.** Quem lê já
sabe fazer o trabalho dele e precisa ser convencido de que a proposta é executável e
o preço é aceitável. Cada parágrafo passa por três perguntas, nesta ordem:

| pergunta | se sim |
|---|---|
| A norma exige que isto conste? | **fica**, e o teste acaba |
| Quem lê sabe disto melhor do que eu, ou é ato dele e não meu? | **sai** |
| Isto cria contra o proponente obrigação, prazo ou fragilidade que nenhuma norma pediu? | **sai do documento** e vai para `pendencias.md` |

**O limite da terceira pergunta não se negocia:** ela retira *declarações sobre
fragilidade*, nunca *conteúdo obrigatório*. A composição do custo fica legível, porque
planilha ilegível é o que dispara a leitura de taxa de administração disfarçada.

**Cada um decide a sua parte:** o enquadramento jurídico do instrumento, os documentos
e as normas aplicáveis são da SUCONV; a distribuição das vagas é da regulação. O
documento não argumenta o que é ato de outro.
*Origem: redacao_02, parecer do professor de 31/08/2026 ("ensinando o padre a rezar
missa"); redacao_05, ajustes da SUCONV de 08/10/2026.*

**9. A voz do documento.** O documento declara. Não se defende, não fala de si, não
enfatiza. Toda frase afirma algo sobre o objeto, o executor ou a execução; nunca sobre
o próprio documento, nunca responde a objeção que ninguém fez. Primeira pessoa nunca
aparece ("nós", "nosso", "este plano").

Quatro movimentos que nunca entram:

| movimento | exemplo real, cortado | como se escreve |
|---|---|---|
| **negação defensiva** | *"O décimo mês **não é folga**"* | "O décimo mês é a janela de conclusão das OCI iniciadas no mês 9" |
| **meta-comentário** | *"A distinção entre obrigatório e opcional **não é nossa**"* | "A Nota Técnica nº 3/2025 organiza a composição em duas colunas e coloca o exame na segunda" |
| **ênfase retórica** | *"a razão é substantiva"*, *"cabe em uma frase"*, *"é **exatamente** esse encadeamento"* | corta-se o intensificador e fica a afirmação |
| **confissão de fragilidade** | *"Registre-se, para afastar dúvida na análise"* | afirma-se o fato, sem anunciar que se está afastando dúvida |

Negação **declarativa** é legítima: *"a execução assistencial não é subcontratada"*
afirma o que se faz. Negação **defensiva** responde a uma objeção imaginária. Na
dúvida: alguém fez essa pergunta? Se não, a frase sai.
*Origem: redacao_03, 01–02/09/2026; virou a verificação Q.*

**10. Convênio não contrata serviço.** "Contratar capacidade" de serviço já licenciado
é o que fazem contrato e credenciamento. No convênio, o objeto se **executa**, se
**amplia**, se **realiza na capacidade instalada do proponente**; nunca se compra.
Antes de fechar, procurar `contrat` no documento inteiro.
*Origem: redacao_03, devolutiva de 05/09/2026.*

**11. A fila medida é a justificativa.** Quando o objeto trabalha sobre demanda já
represada no sistema de regulação, a justificativa abre com o número da fila, com
fonte e data da consulta, e para aí. Não se acrescenta revisão de literatura, série
epidemiológica nem argumento de política pública: buscar justificativa adicional
sugere que a demanda precisa de prova, e ela está no painel da própria concedente. O
parágrafo clínico que resta é o mínimo para situar o objeto.
*Origem: redacao_03, setembro de 2026.*

**12. O método fica fora do documento.** Sem `L-xxx`, `AC-xxx`, `DV-xxx`, `LI-xxx`,
`[[lacuna]]`, sem referência ao acervo de planos aprovados, sem a expressão "custo
acessório", sem percentual de apoio sobre o global, sem o motivo interno de uma
escolha.
*Origem: redacao_02; virou a verificação L.*

**13. Fronteira anticópia.** Os planos aprovados geram achado e lição, nunca
parágrafo.
*Origem: estudo dos aprovados, agosto de 2026.*

## Depois de cada mudança

**14. Decisão que muda premissa obriga varredura do documento inteiro.** Quando um
achado altera uma premissa, tudo o que se apoiava nela fica desatualizado no mesmo
instante e em silêncio. Depois de cada achado incorporado ou de cada ajuste devolvido,
varrer o documento atrás do que dependia da premissa antiga. A regra falha justamente
quando a mudança é pequena.
*Origem: redacao_03 — a triagem pela biópsia que só se sabe durante o exame; a curva
sem "e rampa" de 05/09/2026. Virou a verificação R.*

**15. O modelo do proponente e o formulário da SES mandam na estrutura.** O esqueleto
e os blocos de texto podem ser do proponente: quando existe
`biblioteca/proponentes/<nome>/`, parte-se de lá. Quando a SES manda formulário
próprio, o formulário manda na estrutura, e o modelo da casa entra dentro dele. As
regras deste arquivo valem por cima de qualquer bloco: bloco da casa que cria régua
contra o proponente não entra (regra 6).
*Origem: redacao_04 e análise das adições da ISHP, 07/10/2026.*
**Vale o modelo mais recente que a SES mandou.** Ele fica em
`biblioteca/instrumento/modelo_ses/`. Plano que se faz ou se revisa depois de chegar um
modelo novo passa a ele, se for diferente.
*Origem: usuário, 22/10/2026, ao levar ao `main` o modelo de convênio recebido em 21/10/2026
no plano 4: "todo plano que fizermos se for diferente alteramos para o mais recente para
irmos nos adequando".*
