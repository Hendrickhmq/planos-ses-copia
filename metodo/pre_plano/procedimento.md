# pre_plano/procedimento.md — como se produz um pré-plano

**O que o pré-plano é.** O Ofício 387/2026 da ARINS pede o "Plano de Trabalho
Simplificado" para **análise inicial** (item 3). Depois dele, a SUCONV define o
instrumento jurídico e pede o que falta, "incluindo o Plano de Trabalho Detalhado"
(item 5). Então **o pré-plano serve para a SES decidir *se* e *como* fazer o
projeto**; *com quem* e *quanto custa cada coisa* ficam para o plano de trabalho.

É outro produto, não uma versão curta do plano. Quem lê é a ARINS e a SUCONV, para
decidir; o plano detalhado vai ser conferido contra ele. Se o documento já instrui um
instrumento decidido, ele é plano, mesmo que use o formulário "Simplificado": ver
`../plano/procedimento.md`. **Quem define a trilha é a finalidade do documento, não o
nome do formulário.**

**Valem também as regras de `../comum.md`.** Este arquivo não as repete.

*Origem: redacao_05 (otorrino, ISHP), 08/10/2026 — a versão final ajustada pela SUCONV
e os cortes do usuário na versão de 12 itens da equipe.*

---

## As regras próprias do pré-plano

**1. O formulário manda.** Entram os campos do modelo da SES, na ordem dele, e só o que
eles pedem. Nada de seção a mais. Campo a campo, em `formulario.md`.

**2. Todo número escrito vira compromisso.** O plano detalhado vai ser conferido contra
o pré-plano. Por isso, o mínimo de números fechados e o máximo de espaço para pactuar
depois. É comum, regra 6, no grau mais forte.

**3. Só o custo assistencial.** A aplicação das despesas mostra o que o procedimento
custa. Gestão e apoio entram numa frase: "completam o Valor Total e serão detalhados no
plano de trabalho".

**4. O raciocínio interno não vai para o papel.** Nem o percentual do custo de apoio,
nem quanto se paga ao prestador, nem o motivo de escolher uma fila. É comum, regra 12.

**5. O que é da SUCONV é da SUCONV.** O enquadramento do instrumento, os documentos e as
normas aplicáveis são ato dela (comum, regra 8). O texto que ela escreve entra
**literal**, sem acertar nem a pontuação.

---

## As fases

| # | fase | entra | sai | pronto quando |
|---|---|---|---|---|
| **0** | Travas | o ofício e o formulário da SES, a emenda, a ficha SIGTAP, a fila | `estado.yaml`, `dados/valor_unitario.md`, `dados/fontes/mapa_social_<data>.md`, `dados/fontes/` | cada código tem ficha da competência vigente (comum, regra 3) e a fila foi coletada pelo método de `../coleta/mapa_social.md` |
| **1** | Decisões do usuário | as travas e o dossiê do objeto (`../coleta/dossie.md`) | o objeto e a versão: geral (vários itens) ou de item único | o usuário escolheu, e a escolha está no `estado.yaml` |
| **2** | Redação | as travas e as decisões | `plano_v<N>_<versão>.md`, campo a campo | todos os campos de `formulario.md` preenchidos, sem "[a preencher]" |
| **3** | Conferência | o documento | o relatório da bateria do pré-plano | a bateria em 100% (`conferencia.md`) |
| **4** | Envio e retorno | o documento conferido | o `.docx` e o `.pdf` enviados, arquivados em `versoes/` | o retorno da SUCONV tratado, como abaixo |

**Na fase 0, a conta se faz inteira**, como no plano (quantitativo no piso, sobra menor
que um unitário), mas fica no `estado.yaml` e em `dados/`: no documento entra só o que
o formulário pede. Os preços do objeto, sem o apoio, saem pelo método de
`../coleta/precos.md`, em `dados/precos.md`, e são controle interno.

**O retorno com ajuste da SUCONV:**
- o texto dela fica literal;
- erro factual se corrige e se avisa. Exemplo de 08/10/2026: voltou "corrigidas e
  enviadas", e o status no SISREG é "corrigida e reenviada";
- quando um ajuste tira uma linha, sai também o que dependia dela (comum, regra 14).
  Fazer o diff contra a versão enviada.

**Ponto de atenção:** o Valor Total da primeira seção menos o valor da aplicação das
despesas revela o custo de apoio por subtração. A SUCONV aceitou assim em 08/10/2026.
Se pedirem para não deixar visível, o Valor Total passa a ser o recurso inteiro.

---

## Onde mora o estado de um pré-plano

```
planos/redacao_NN/
  estado.yaml               proponente, instrumento, recurso, objeto, números, vigência
  pendencias.md             o que falta e o que se decidiu
  dados/valor_unitario.md   o unitário e a portaria que o fixou
  dados/fila.md             a fila do Mapa Social, com a data da base e da consulta
  dados/fontes/             a ficha SIGTAP e as outras fontes
  plano_v<N>_<versão>.md    o documento, uma versão por arquivo
  plano.md                  o plano de trabalho, quando o projeto chega a ele (../plano/)
  versoes/                  o enviado e o devolvido, lado a lado
```

O `.docx` e o `.pdf` saem de `ferramentas/gerar_pre_plano.py`.

**Um projeto, uma pasta.** O pré-projeto, o pré-plano e o plano de trabalho do mesmo
projeto são etapas do mesmo trabalho e ficam na mesma `planos/redacao_NN/`, com a mesma
fase 0 (`dados/`, `dossie/`) e o mesmo `estado.yaml`. O `plano.md` entra ao lado do
pré-plano, e cada um tem a sua conferência. O plano é conferido contra o pré-plano
enviado: objeto, códigos, valor total e metas não podem contradizer o que a SES recebeu.
O `estado.yaml` aponta o enviado em `pre_plano_enviado` (em `versoes/` da mesma pasta), e
a verificação Y confere (`../plano/conferencia.md`).
*Origem: usuário, 22/10/2026, ao abrir o redacao_08: "tudo que for de um projeto deve
ficar junto e não separado, são apenas etapas/coisas diferentes". O plano 4, anterior,
ficou em duas pastas (redacao_04 e redacao_06).*

O modelo pronto de pré-plano é o `planos/redacao_05/plano_v1_geral.md`, na versão que a
SUCONV ajustou.
