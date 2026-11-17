# proponentes/ — um padrão por proponente

**Decisão de 07/10/2026: proponentes diferentes têm padrões diferentes.**

O padrão (`metodo/`) continua valendo para **todos** os planos no que é regra: número com
fonte, meta no piso, régua contra o proponente, teste da citação, conferência. O que
pode mudar de um proponente para outro é o **esqueleto do documento, os blocos de
texto e a forma como cada proposta é apresentada** — porque cada proponente já tem
planos aprovados pela SES-DF num formato próprio, e a equipe dele devolve o nosso
texto puxado para esse formato.

## Como a agente usa esta pasta

1. Antes da fase 0, identificar o proponente do plano (`estado.yaml`).
2. Se existir `proponentes/<nome>/`, partir dali: a ficha cadastral, o modelo da casa
   e os blocos aceitos. A estrutura `padrao` de `metodo/plano/estrutura.md` é o padrão
   para quem **não** tem pasta própria.
3. Se a SES mandar formulário próprio (como o "Modelo Parceria" do Ofício 387/2026),
   o formulário manda na estrutura, e o modelo da casa entra dentro dele.
4. As regras do padrão valem por cima de qualquer bloco (`metodo/comum.md`, regra 15). Bloco da casa que cria
   prazo, percentual ou pré-condição que norma nenhuma exige não entra (comum, regra 6).

## O que existe

| pasta | situação |
|---|---|
| `ishp/` | análise das adições da equipe feita em 07/10/2026 (`analise_adicoes_20261007.md`). A ficha, o modelo da casa e os blocos estão propostos lá e ainda não foram montados. |

## O que cada pasta de proponente deve ter

| arquivo | conteúdo |
|---|---|
| `ficha.yaml` | dados cadastrais **com a função de cada um** (CNPJ de quem propõe e da matriz, e-mail institucional e do representante, telefones), fonte e data de cada campo |
| `modelo.md` | o esqueleto e os blocos que os planos aprovados do proponente usam, cada bloco com a seção do aprovado de onde vem |
| `blocos_<objeto>.md` | conteúdo técnico aceito pelo usuário para um tipo de objeto, com a decisão que o aprovou |
| `retornos.md` | como a equipe do proponente edita o que mandamos, e o que conferir em cada retorno |
