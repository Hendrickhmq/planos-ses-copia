# schema.md

Definição dos campos. Alterar aqui **antes** de alterar qualquer arquivo em
`registros/` ou `destilados/`. Revisar depois do segundo plano fichado.

`python verificar_registros.py` confere os `registros/*.csv` contra este arquivo
e contra o disco. As listas de valores dele **espelham** as tabelas daqui: mudou
aqui, muda lá. Erro (id fora do padrão, valor fora da lista, referência para id
que não existe, arquivo que não está onde o registro diz) dá código de saída 1;
o que só uma pessoa pode preencher — URL, data de acesso, conferência — sai como
pendência.

Todo texto em **Unicode composto (NFC)**. O macOS grava nome de arquivo
decomposto, e o nome copiado do Finder para uma célula não casa com o mesmo
arquivo no Windows.

---

## registros/acervo.csv

Todo documento do acervo entra aqui, seja plano, norma ou peça de controle.
O nome evita a colisão com "fonte do direito", que é termo técnico e significa
apenas norma.

| campo | valores / formato |
|---|---|
| `id` | `pt_ses_01` plano, `NM-001` norma, `CT-001` controle, `IT-001` instrumento, `DD-001` dado |
| `tipo` | `plano`, `norma`, `controle`, `instrumento`, `dado` |
| `especie` | ver tabela de espécies abaixo |
| `hierarquia` | 1 a 6, só para `tipo: norma` — ver tabela |
| `titulo` | como consta no documento |
| `orgao` | emissor |
| `instrumento` | `convenio`, `contrato`, `termo_fomento`, `credenciamento`, `-` |
| `base_legal` | dispositivo que rege o instrumento, quando conhecido |
| `processo_sei` | número do processo, quando houver |
| `plano_relacionado` | id do plano a que a peça de controle ou o instrumento se refere |
| `data_doc` | AAAA-MM-DD |
| `situacao` | `vigente`, `revogada`, `alterada`, `a_verificar`, `-`; para plano, `aprovado` |
| `paginas` | inteiro |
| `arquivo` | nome do arquivo local, sem caminho — é também o nome da pasta em `extraidos_normas/` (normas) ou o id em `extraidos/` (planos). Vazio quando o documento não foi baixado. Mora em `planos_aprovados/` (plano), `normas/` (norma), `controle/` (controle e instrumento) ou `registros/fontes/` (dado) |
| `url` | endereço exato de onde foi baixado — obrigatório quando há `arquivo`. A citação do DOU vai no `titulo`, não aqui |
| `data_acesso` | AAAA-MM-DD — quando o arquivo foi baixado daquela URL |
| `acesso` | `integral`, `so_indice`, `restrito` |
| `extracao_conferida` | `sim` / `nao` |

### Espécies e hierarquia

`tipo: norma` — o campo `hierarquia` resolve conflito entre duas linhas do
`obrigacoes.csv`. Número menor vence.

| hierarquia | espécie |
|---|---|
| 1 | `constituicao` |
| 2 | `lei`, `lei_complementar`, `lei_distrital` |
| 3 | `decreto`, `decreto_distrital` |
| 4 | `portaria`, `resolucao`, `portaria_consolidacao` |
| 5 | `instrucao_normativa`, `manual` |
| 6 | `nota_tecnica` |

A escada não distingue portaria de ministro (GM/MS) de portaria de secretaria
(SAES/MS): as duas são `portaria`, nível 4. As duas Portarias GM/MS do acervo
(NM-032 e NM-033) chegaram a ser registradas como `portaria_ministerial`, nível
3 — o nível do decreto —, e voltaram a 4 em 27/09/2026. Se o projeto precisar
que GM vença SAES num conflito, o caminho é abrir um nível aqui, e não pôr a
portaria no degrau do decreto.

`tipo: controle` — sem `hierarquia`. Espécies: `parecer_juridico`,
`parecer_referencial`, `parecer_tecnico`, `acordao`, `decisao`, `checklist`,
`relatorio_preliminar`, `oficio`, `termo_aprovacao`, `notificacao`,
`representacao`.

`representacao` é a peça com que o Ministério Público de Contas leva ao TCDF um
instrumento já celebrado. Não é exigência de aprovação — o plano passou —, mas
mostra o que o controle externo ataca depois dela. Quando só o resumo publicado
pelo órgão está disponível, `acesso: so_indice`.

`tipo: plano` — espécie `plano_trabalho`. Sem `hierarquia`.

`tipo: instrumento` — sem `hierarquia`. Espécies: `termo_convenio`,
`termo_aditivo`, `termo_apostilamento`.

`tipo: dado` — sem `hierarquia`. Espécies: `painel`, `tabela_comparativa`,
`planilha`, `extracao_sistema`. É fonte de número (a fila do Mapa Social, um
comparativo de preços), não norma nem peça de controle: vale como lastro de
quantidade, nunca como fundamento de exigência.

O instrumento não é norma nem peça de controle, e por isso não cabia em nenhum
dos três tipos anteriores. Norma vale para todo mundo; peça de controle opina
sobre um caso; o instrumento **obriga os dois partícipes daquele convênio**, e é
de onde saem as linhas de `obrigacoes.csv` com `natureza: contratual` — que já
existia no schema sem ter documento de origem possível no acervo.

Consequência para a precedência: obrigação contratual não entra na escada de
`hierarquia`, porque não é norma. Ela vincula quem assinou, e só. Quando uma
cláusula do termo contraria norma vigente, vence a norma; quando ela apenas
acrescenta, vale como está. O termo é também onde se descobre **o que o plano
não precisa dizer** — a declaração de ausência de contrapartida do convênio
031061/2026 mora na Cláusula Sétima do termo, não no plano de trabalho.

Nota: `situacao` descreve a vigência da **norma**. Não confundir com
`status_vigencia` do `obrigacoes.csv`, que descreve se **aquela exigência
específica** já foi conferida. Uma norma vigente pode ter exigência ainda
`a_verificar`.

---

## registros/obrigacoes.csv

O que o plano **precisa** conter, por força de norma ou de entendimento.
Nunca receba linha vinda de observação de plano — para isso existe `achados.csv`.

| campo | valores / formato |
|---|---|
| `id` | `OB-001` |
| `acervo_id` | id em `acervo.csv` |
| `dispositivo` | artigo, inciso, item |
| `exigencia` | uma frase, no imperativo |
| `secao_afetada` | seção do plano onde se cumpre |
| `natureza` | `legal`, `infralegal`, `interpretativa`, `contratual` |
| `status_vigencia` | `vigente`, `revogado`, `inaplicavel`, `a_verificar` |
| `data_verificacao` | AAAA-MM-DD |
| `observacao` | livre |

Regra: preencher `status_vigencia` como `a_verificar` no momento da anotação e
validar em bloco depois. O custo de anotar na hora é zero; o de reencontrar é alto.

`inaplicavel` é o caso em que o dispositivo existe e está vigente, mas não rege o
instrumento em questão — norma de outro regime. A linha fica no arquivo, com a
procedência preservada, e não pode ser usada como fundamento enquanto não receber
nova âncora.

---

## registros/achados.csv

O que você **observou** nos planos. Observação não é norma.

| campo | valores / formato |
|---|---|
| `id` | `AC-001` |
| `acervo_id` | id do plano; achado que atravessa planos usa a faixa `pt_ses_01..04` |
| `secao` | seção onde apareceu |
| `achado` | uma frase descritiva |
| `classificacao` | `exigido_norma`, `exigido_parecer`, `pratica_ses`, `idiossincrasia` |
| `qualidade` | `bom_exemplo`, `aceitavel`, `falha`, `neutro` (observação sem juízo — "nenhum dos quatro menciona contrapartida") |
| `vira_obrigacao_id` | id em `obrigacoes.csv`, se virou obrigação |

`classificacao` é o campo que impede canonizar vício de repetição: três planos
fazerem a mesma coisa não significa nada até se saber se é norma ou hábito.

---

## registros/licoes.csv

O que **fazer no nosso plano**, destilado de achados, obrigações, exigências e
peças de controle. Achado é observação sobre plano alheio; lição é regra para o
nosso, com a origem e o modo de conferir. É daqui que se gera o `criterios.md`
(`python consultar.py criterios`) — editar a lição, nunca o `criterios.md`.

| campo | valores / formato |
|---|---|
| `id` | `LI-001` |
| `eixo` | `administracao` (o que aprova, reprova ou o controle ataca) ou `qualidade` (boa prática) — os dois eixos do `criterios.md` |
| `tema` | `codigos_sigtap`, `valor_unitario`, `objeto`, `enquadramento_cnes`, `metas`, `dimensionamento`, `custo_apoio`, `precos`, `sobreposicao`, `capacidade_executor`, `instrumento`, `desembolso_vigencia`, `faturamento_sus`, `controle_social`, `riscos`, `redacao`, `uso_do_acervo`, `diligencia` |
| `tipo` | `erro` (o que evitar) ou `acerto` (o que repetir) |
| `gravidade` | `reprova` (a análise da SES-DF ou o termo barram), `questiona` (passou na SES-DF e o controle externo atacou, ou atacaria), `melhora` (boa prática) |
| `regra` | uma frase no imperativo, sobre o nosso plano |
| `por_que` | a evidência, em uma ou duas frases |
| `origem` | ids que sustentam a lição, separados por `; ` — `AC`, `OB`, `CT`, `EX`, `IT`, `NM`, `DD` |
| `verificacao` | `automatica:<letras>` quando verificações do `conferir_plano.py` cobrem a regra; `parcial:<letras>` quando cobrem parte e a pergunta cobre o resto; `manual` |
| `pergunta` | a pergunta que se faz ao plano antes do protocolo — obrigatória em `parcial` e `manual` |

A letra citada em `verificacao` tem de existir como `verificar_<letra>` no
`conferir_plano.py`, e todo id de `origem` tem de existir nos registros.

---

## registros/exigencias_resposta.csv

Cadeia causal entre o que foi exigido e como o proponente respondeu. Só se
preenche com acesso ao inteiro teor do processo.

| campo | valores / formato |
|---|---|
| `id` | `EX-001` |
| `documento_origem` | id/protocolo da peça que exigiu |
| `data_origem` | AAAA-MM-DD |
| `versao_alvo` | versão do plano que respondeu |
| `secao` | seção alterada |
| `exigencia` | o que foi cobrado |
| `texto_antes` | resumo ou trecho curto |
| `texto_depois` | resumo ou trecho curto |
| `cumprida_integralmente` | `sim`, `parcial`, `nao` |

---

## registros/correcoes.csv

Correção de **forma**, célula a célula, lida pelo `tratar_planos.py`. Defeito do
documento não entra aqui — vai para `achados.csv`.

| campo | valores / formato |
|---|---|
| `plano` | id do plano |
| `arquivo` | `<plano>/tabelas/<csv>`, relativo a `extraidos/` ou a `extraidos_ocr/` |
| `linha` | 1-based, na CSV de origem. **0** é o cabeçalho que a extração não capturou: as linhas 0 de um arquivo montam uma linha nova antes da primeira |
| `campo` | número da coluna (1-based) ou nome do cabeçalho; na linha 0, só número |
| `valor_novo` | o texto certo |
| `classe` | `forma` (aplicada) ou `documento` (recusada, com aviso) |
| `motivo` | obrigatório — de onde se sabe o valor certo |

---

## registros/conferencia.csv

O que foi conferido à mão, ancorado no sha256 do conteúdo — ver `conferencia.py`.
Escrito pelo script, não à mão.

| campo | valores / formato |
|---|---|
| `plano` | id do plano |
| `pasta` | `extraidos`, `extraidos_ocr` ou `normalizados` — a leitura conferida |
| `alvo` | caminho dentro da pasta do plano, ou `*` para o documento inteiro |
| `sha256` | hash do conteúdo no momento da conferência |
| `conferido_por` | iniciais |
| `data` | AAAA-MM-DD |
| `resultado` | `ok` ou `com_achado` |
| `observacao` | livre |

---

## destilados/fichas/pt_ses_XX.md

Uma ficha por plano, arquivo separado. Campos mínimos:

```
## Identificação
id, proponente, objeto, instrumento, base legal, processo SEI,
vigência, valor global, fonte de recurso, nº de páginas

## Estrutura
seções presentes, na ordem em que aparecem, com nº de páginas de cada

## Conteúdo por seção
justificativa | objetivos | metas | indicadores | cronograma |
orçamento | monitoramento | contrapartida | equipe | anexos
  - o que traz
  - como está expresso (quantificado? verificável? datado?)

## Qualidade
- pontos fortes
- fragilidades
- o que um analista rigoroso questionaria

## Achados registrados
ids gerados em achados.csv
```

Regra de ouro da ficha: distinguir **meta**, **indicador**, **parâmetro de
aferição** e **meio de verificação**. Plano ruim confunde os quatro.
