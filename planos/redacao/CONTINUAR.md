# CONTINUAR.md — como retomar em outra conversa

Este arquivo existe para que a redação do plano continue em qualquer conversa
nova, sem recontar o histórico. O estado mora nos arquivos, não no chat.

---

## Ordem de leitura, para quem chega

1. `redacao/CONTINUAR.md` — este arquivo. **Começar por aqui.**
2. `redacao/plano_final.md` — **o documento entregável** (20/08/2026).
3. `redacao/pendencias_final.md` — o que falta, com dono e ordem de ataque.
4. `redacao/estado.yaml` — decisões travadas, dados, histórico das versões.

Se for **mudar conteúdo** e não só formato, é preciso mais:

5. `redacao/plano_v3.md` — a fonte de onde o final foi derivado, congelada.
   Antes dela, `redacao/decreto_48727_leitura.md`: o Decreto DF nº 48.727/2026
   é a norma do instrumento.
6. `redacao/regras_oci_cardiologia.md` — as normas lidas no original. **É a
   régua**: onde ela e os planos de referência divergirem, ela vence.
7. `destilados/roteiro.md` · `redacao/duvidas.md` · `redacao/melhorias.md` ·
   `registros/achados.csv` — método, dúvidas abertas e o que ficou de fora.

Versões congeladas em `redacao/`: `plano_v3.md`, `plano_v2.md` e, em `versoes/`,
`plano_v1_2026-08-18.md` e `plano_final_remontagem_2026-08-18.md`. Não editar.

Não é preciso ler `README.md` nem `schema.md`. São do Projeto A (estudo do
corpus). Ler só se a dúvida for de método.

---

## As regras

**1. Nunca inventar número.** Valor de tabela SIGTAP, tamanho de fila, endereço
de polo, base legal: vêm do usuário, ou de fonte citada com URL e data, ou viram
`[[lacuna: LC-xxx]]` no lugar exato onde faltam. Nunca de plausibilidade.

**2. Fronteira anticópia.** Consultar os 4 planos aprovados para **gerar
achado** é o método. Copiar texto deles para o rascunho, não. O que atravessa a
fronteira é a linha de `achados.csv`, nunca o parágrafo.

**3. Nível: mínimo viável.** ~~O rascunho faz o que os 4 aprovados fazem, nada
além.~~ **SUSPENSA em 2026-08-18, a pedido do usuário.** A v2 incorpora
melhorias e, sobretudo, exigências normativas que o corpus não tem. As regras
1 e 2 continuam valendo integralmente — nenhum número foi inventado na v2, e
nenhum parágrafo do corpus foi copiado.

**4. Toda dúvida vira DV-xxx** em `duvidas.md`, com pergunta, por que importa, o
que já se sabe e campo de resposta em branco. Nunca deixar dúvida só no chat.

**5. Toda observação sobre os 4 planos vira AC-xxx** em `achados.csv`, com
evidência em `arquivo:linha`. Classificação: `exigido_norma`, `exigido_parecer`,
`pratica_ses`, `idiossincrasia`. Achado nunca vence norma.

**6. Corrigir em voz alta.** Várias conclusões desta fase foram revistas quando
o dado chegou (a razão fila/meta, o código da OCI no pt_ses_04, a premissa da
DV-003). Rever é o funcionamento normal, e a revisão fica registrada.

---

## Onde paramos — atualizado em 2026-08-20

**O plano final está pronto, em duas versões.**

| arquivo | o que é |
|---|---|
| `redacao/plano_final.md` | **o documento**. 20 seções, 1.837 linhas, sem método |
| `redacao/plano_final.docx` | o mesmo, em Word: capa, sumário automático, rodapé numerado, planilha em paisagem |
| `redacao/pendencias_final.md` | as 49 pendências que saíram do documento, com dono e ordem de ataque |
| `redacao/perguntas_ao_professor.md` | DV-034 a DV-049: o que temos que os 4 aprovados não têm, separado entre norma, tática e peso |
| `redacao/plano_v3.md` | a fonte, **congelada**. Mudança de conteúdo se faz aqui e regenera |

Duas decisões do usuário governam o final, e não devem ser revertidas sem ele:

1. **Campo marcado, sem conteúdo.** Nada de prosa fictícia sobre o proponente. O
   IECC foi removido inteiro; todos os campos de identificação estão em branco.
2. **Fora tudo o que é método.** Sem Anexo I, sem Anexo II, sem `LC-xxx`, sem
   comparação entre versões, sem referência ao corpus ou a `registros/`.

### As cinco que continuam anteriores à assinatura

| id | o que falta | de quem |
|---|---|---|
| **LC-025** | custo unitário real da OCI no DF | proponente |
| **LC-041** | capacidade da rede própria da SES-DF | SES-DF |
| **LC-056** | situação do PAR do DF e prazo do Colegiado | SES-DF |
| **LC-023** | pesquisa de preços própria | proponente |
| **LC-042** | ancoragem no PDS 2024–2027 e na PAS | SES-DF |

Nenhuma se resolve escrevendo. Detalhe e ordem sugerida em `pendencias_final.md`.

### Se precisar regerar o .docx

Não há pandoc nem LibreOffice nesta máquina. O `.docx` sai de um conversor
markdown→docx em node. A cópia que morava aqui (`redacao/md2docx.js`, com a
citação em caixa âmbar) saiu em 27/09/2026 e está no histórico do Git; o
conversor atual é o `md2docx.js` da raiz:

```
npm ci && npm run docx -- redacao/plano_final.md redacao/plano_final.docx --titulo "OCI Avaliação Cardiológica"
```

Ele trata tabelas, blocos de código, o aviso em destaque, capa, sumário e a
seção em paisagem da planilha. Editar o `.md` e rodar de novo — nunca editar o
`.docx` e o `.md` em paralelo.

---

## O primeiro prompt da conversa nova

Copiar e colar:

```
Estou retomando um plano de trabalho de convênio para a SES-DF. O documento
final já existe; o estado inteiro está no repositório. Leia nesta ordem antes
de responder:

1. redacao/CONTINUAR.md       (as regras e onde paramos)
2. redacao/plano_final.md     (o documento entregável)
3. redacao/pendencias_final.md (o que falta, com dono)
4. redacao/estado.yaml        (decisões travadas — não reabrir)

Depois me diga, em poucas linhas: o que está fechado, o que está aberto e o que
bloqueia a assinatura. Não recomece nada que já esteja decidido.

O documento está pronto como peça. O que resta é dado externo, não redação —
e se for preciso mudar conteúdo, muda em plano_v3.md e regera o final.
```
