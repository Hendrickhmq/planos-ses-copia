# metodo/ — o padrão

Vale para **todo** documento que o projeto produz. Melhora a cada plano e a cada
entendimento novo, e cada regra diz de onde veio.

## Primeiro: qual é a trilha

São dois produtos de essência diferente. **Quem define a trilha é a finalidade do
documento, não o nome do formulário.**

| | pré-plano | plano de trabalho |
|---|---|---|
| **para que serve** | para a SES decidir **se e como** fazer | para instruir o instrumento já decidido: **com quem e quanto custa cada coisa** |
| **quem lê** | ARINS e SUCONV, na análise inicial | o parecerista, que verifica se é executável e se o preço é aceitável |
| **estrutura** | o formulário da SES, campo a campo | as 9 seções do padrão, o modelo do proponente ou o formulário da SES |
| **números** | o mínimo: tudo o que se escreve vira compromisso | todos, calculados |
| **custo** | só o assistencial | o assistencial e o apoio, de baixo para cima pelo fluxo |
| **começa por** | `pre_plano/procedimento.md` | `plano/procedimento.md` |

Quando o mesmo projeto tem os dois, eles ficam na mesma pasta, e o plano é conferido contra
o pré-plano enviado (`pre_plano/procedimento.md`, "Um projeto, uma pasta").

## Os arquivos

```
metodo/
  LEIA.md                  este arquivo
  comum.md                 as regras das duas trilhas
  MUDANCAS.md              cada mudança no padrão: data, o que mudou, origem
  criterios.md             as lições do acervo, geradas de registros/licoes.csv — não editar
  pre_plano/
    procedimento.md        o que é, as regras próprias, as fases, o retorno da SUCONV
    formulario.md          o formulário da SES, campo a campo
    conferencia.md         a bateria do pré-plano
  coleta/
    mapa_social.md         a fila do objeto no Mapa Social: a ordem, o kit, a medida, o montador (agente mapa-social)
    ficha_sigtap.md        a ficha do procedimento no SIGTAP: acesso, campos, saída (agente ficha-sigtap)
    normas.md              vigiar, validar e registrar as normas, todo dia 10 (agente normas)
    precos.md              os preços do objeto: valor pela origem do recurso, SES-DF, mercado do DF, conta (agente precos)
    dossie.md              qual fila e qual OCI: junta as coletas, a conta interna e a justificativa pública (comando /dossie)
  plano/
    procedimento.md        as oito fases, as regras próprias, o estado do plano, a triagem
    estrutura.md           as seções (lidas pela verificação J), metas, indicadores, títulos
    modelo.md              o esqueleto preenchível, seção a seção, com os anexos de perguntas
    conferencia.md         as quatro conferências: as duas baterias, o checklist, a revisão cega
    leitura_de_entrega.md  as doze perguntas
  agentes/
    gauntlet.md            melhorar o prompt de um agente por rodadas contra uma referência real (comando /gauntlet)
  revisao/
    cega.md                a revisão cega: quem não conhece a conversa lê o documento num pacote cego (comando /revisao)
    perguntas.md           as perguntas da revisão, as mesmas para qualquer revisor
    claude.md              o revisor padrão: o Claude cego, em dois subagentes (contas e leitura)
    chatgpt.md             o revisor de outra família, uma vez, na versão final: o Sol
    gemini.md              o revisor do Google (Gemini Notebook), opcional, fora do padrão
    esquemas/              os formatos do achado, da resposta e do veredito
```

## Como o padrão muda

**Uma verdade só.** Cada regra mora num lugar. Se vale para as duas trilhas, mora em
`comum.md`; se vale para uma, na pasta dela. Os outros lugares apontam para ela, sem
repetir. A memória do assistente também aponta para cá e não guarda cópia de regra.

**A triagem.** Cada entendimento novo, no momento em que aparece, passa por uma
pergunta: **isto muda como se faz qualquer documento desta trilha?**
- **Sim:** entra aqui, no arquivo certo, com a linha de origem, e se registra em
  `MUDANCAS.md`. Se dá para codificar, vira verificação na bateria da trilha.
- **Só para um tipo de objeto:** vai para `biblioteca/`, no tema, ou para a bateria do
  plano.
- **Não:** fica no `licoes.md` do plano.

**A linha de origem.** Toda regra termina com *Origem: <plano>, <episódio>*. A história
completa fica no plano de origem; aqui fica só a linha, que explica por que a regra
existe sem contar o caso inteiro.

**O padrão se testa.** `ferramentas/testar_padrao.py` confere que o padrão é coerente
consigo mesmo: caminhos citados que existem, regras e verificações citadas que existem,
nenhuma referência ao lugar antigo, cada agente com método e no README.
`ferramentas/testar_atualidade.py` confere que o dado não envelheceu: fichas contra o
catálogo e o acervo, portarias do `estado.yaml` no acervo, vigia de normas recente. Os
dois rodam na suíte.

**O padrão e as ferramentas moram só no `main`.** O ramo de um plano em andamento
guarda só a pasta do plano. Se o plano precisa mudar uma regra ou uma ferramenta, a
mudança vai primeiro para o `main`.
