---
description: Revisão cega de um plano ou pré-plano — dois subagentes Claude que não conhecem a conversa leem o documento num pacote cego; o assistente confere, responde com fonte e corrige; até três rodadas; na versão final, o Sol (ChatGPT) lê uma vez; o que sobrar vai ao usuário
argument-hint: planos/redacao_NN/ · o documento (plano.md ou o pré-plano) · "final" para a passada do Sol
---

Faça a revisão cega de: $ARGUMENTS

**O método é `metodo/revisao/cega.md`.** O revisor padrão está em `metodo/revisao/claude.md`,
e as perguntas em `metodo/revisao/perguntas.md`. Leia os três primeiro: este comando não
guarda regra.

1. **As baterias da trilha em 100%** (`plano/conferencia.md` ou `pre_plano/conferencia.md`).
   A revisão cega não substitui a bateria.
2. **O pacote** da rodada, em `revisao/AAAAMMDD/r1/pacote`, pelo
   `ferramentas/pacote_revisao.py`. As normas são as que o documento cita, mais as do
   programa e a sanitária do serviço. Se a varredura acusar CPF ou CNS, pare.
3. **O Claude cego:**
   - `revisar_claude.py preparar`, com a pasta cega no scratchpad, fora do repositório, e
     `--faturamento` se o objeto tem APAC.
   - Abra **dois subagentes em segundo plano, em paralelo**, cada um com o texto que a
     ferramenta imprimiu, sem acrescentar nada da conversa, e com `model` e `effort` na
     chamada, os de `claude.md`.
   - Quando os dois terminarem, confira no registro de cada um que nenhum arquivo fora da
     pasta cega foi lido.
   - `revisar_claude.py juntar`.
4. **A conferência por máquina** (`conferir_revisao.py`) no `achados.json`.
5. **A triagem**, achado por achado, contra a fonte primária (comum, regra 4).
   - Escreva o `resposta.json` e o `triagem.md`.
   - Aceitar e contestar exigem fonte.
   - O que bate em decisão travada é `decisao_do_usuario`.
   - O que pede explicação de regra ou condição a comprovar vai para o controle interno, não
     para o documento.
   - Rode `conferir_revisao.py --resposta` até passar.
6. **A correção** do documento pelo que foi aceito, com as baterias da trilha de novo em
   100%.
7. **A rodada 2,** com o pacote do documento corrigido em `r2/pacote`: `preparar
   --treplica <r1>`, dois subagentes e `juntar --treplica`. Confira com `--veredito`.
   Responda o que voltou como `nao_resolvido` ou `contestacao_nao_procede`, corrija, e faça
   a rodada 3 só com isso.
8. **Depois da rodada 3,** o que sobrar vai para `divergencias.md`, com os dois lados e as
   fontes.
9. **Na versão final** (argumento "final", ou quando o usuário disser que o documento vai
   ser entregue):
   - `revisar_chatgpt.py` sobre o pacote da versão final, com o Sol e as perguntas A1, A2 e
     A4;
   - a mesma triagem;
   - se a cota do ChatGPT acabar, diga a hora em que ela volta e pergunte se a entrega
     espera.
10. **Registre o resumo no `estado.yaml`,** sob `revisao_cega`, e devolva ao usuário:
    - o que mudou no documento;
    - o que foi contestado, e com que fonte;
    - as divergências, para ele decidir.

    **A decisão do que fica em divergência é do usuário.**
