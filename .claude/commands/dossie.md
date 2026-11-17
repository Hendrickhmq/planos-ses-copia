---
description: Monta o dossiê do objeto de um plano — qual fila e qual OCI — chamando os agentes ficha-sigtap, mapa-social e precos, e confere
argument-hint: planos/redacao_NN/ · escolher a fila ou dada a fila · o recurso e a origem · as OCI ou a fila candidatas
---

Monte o dossiê do objeto para: $ARGUMENTS

**O método é `metodo/coleta/dossie.md`.** Leia-o primeiro: este comando não guarda regra.

1. Leia o método e o estado do plano (`estado.yaml`, `dados/`). Falta o recurso, a origem
   ou o apoio? Pergunte ao usuário.
2. Para cada OCI candidata, veja o que já existe e se ainda vale:
   - a ficha da competência vigente em `dados/fontes/`;
   - a coleta da fila pela finalidade, com os alarmes, e o enquadramento do plano
     (`dados/enquadramento_mapa_social.json`) com as decisões do usuário sobre as filas;
   - os preços em `dados/precos.md`, com menos de 180 dias.
3. Chame os agentes para o que falta:
   - para escolher a fila, o `mapa-social` primeiro, com uma ordem de panorama; escolha com
     o usuário as candidatas antes de seguir;
   - o `ficha-sigtap`, porque o CID aceito e o da finalidade vêm da ficha;
   - depois o `mapa-social`, com a ordem de medição gravada na pasta bruta
     (`metodo/coleta/mapa_social.md`, "A ordem"), e o `precos`, em paralelo. O
     `mapa-social` usa o navegador embutido: nunca dois dele ao mesmo tempo.
4. **Leia o que voltou antes de montar.** Os alertas de cada agente vêm primeiro na
   resposta dele. Pergunte, OCI por OCI:
   - a ficha e a coleta usam o mesmo CID da finalidade?
   - o número é de quem precisa da OCI, ou do que ela aceitaria (o teto)?
   - algum alarme da coleta, ou preço fraco, decide a ordem do comparativo?
   O que pedir decisão vai para `pendencias.md` e para a sua resposta, antes do comparativo.
   A fila achada que o usuário decidir vai para o enquadramento do plano, com a data.
5. Monte as páginas, o comparativo e a justificativa no formato do método.
6. Rode `python3 ferramentas/conferir_dossie.py <plano>/dossie/` e corrija até passar.
7. Devolva o comparativo e a justificativa, com os alarmes abertos em cima. **A escolha é
   do usuário.**
