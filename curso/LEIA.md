# curso/ — aprender a fazer o que o projeto faz

O repositório é organizado para **consultar**: cada regra num lugar, com a origem. Quem
chega não sabe por onde começar, o que depende do quê, nem por que a regra existe. O
curso é a ordem de leitura, a lógica e os casos.

**Para quem é.** Quem vai fazer a parte técnica com o projeto: escolher o objeto, ver a
fila, consultar o CNES, montar o pré-plano e o plano, conferir. Trabalha com o Claude e
com este repositório.

**O curso é interno.** Ele conta o que se discutiu por dentro: preço, margem, erro
nosso. Nada dele vai a documento que sai para a SES.

---

## Como se estuda

```
/aula 1
```

O comando `/aula` (`.claude/commands/aula.md`) conduz um módulo: explica, pergunta, passa
o exercício, corrige mostrando a fonte e anota onde a pessoa parou. Também dá para ler o
módulo direto, em `curso/modulos/`.

Comece pelo `mapa.md`, que é o percurso inteiro numa página, e deixe o `glossario.md`
aberto ao lado.

**O cofre do Obsidian.** Os conceitos, as normas, os órgãos, os casos e os planos estão em
notas ligadas entre si e a cada módulo, na pasta `conhecimento/`. Abra a raiz do repositório
como cofre no Obsidian e comece pela nota [[Início]]. Cada módulo abre com a lista das notas
dele. As notas definem e apontam; a regra continua em `metodo/`.

## As sete partes de todo módulo

| parte | o que traz |
|---|---|
| **Para que serve** | o que a pessoa passa a conseguir fazer sozinha |
| **A lógica** | o porquê, em linguagem simples |
| **Pode e não pode** | pode, não pode, por quê e onde está escrito |
| **O caso** | o que aconteceu de verdade: o que se pensou, o que estava errado, como se descobriu, o que mudou |
| **Leia na fonte** | os arquivos e as normas, na ordem de leitura |
| **Faça** | exercício com dado real do repositório |
| **Confira** | as perguntas que é preciso saber responder, e o que conta como resposta certa |

## Os módulos

A ordem de estudo é a da tabela. **Os módulos 1 a 5 são a base:** a lei, o dinheiro, o
instrumento e o caminho dentro da SES. Sem eles, o resto vira receita. Os módulos 6 a 10
e o 12 são o trabalho do dia a dia.

| nº | módulo | o caso que ensina | situação |
|---|---|---|---|
| 0 | O mapa: o percurso inteiro, quem faz o quê, as siglas | — | `mapa.md` e `glossario.md` |
| 1 | As leis do SUS e a complementaridade: por que uma entidade privada pode atender pelo SUS, e em que condições | o termo de fomento que o Tribunal mandou virar convênio; a norma que juramos que não valia | **escrito** (`modulos/01_as_leis_do_sus_e_a_complementaridade.md`) |
| 2 | Como o SUS organiza e paga: MAC, FAEC, teto, a tabela, a OCI, a regulação, o CNES | a emenda que não paga por FAEC | **escrito** (`modulos/02_como_o_sus_organiza_e_paga.md`) |
| 3 | O dinheiro da emenda: do orçamento da União ao Fundo; os tipos de emenda; o que ela paga e o que não paga; as parcelas | os pagamentos dos cinco convênios de 2026, mês a mês | **escrito** (`modulos/03_o_dinheiro_da_emenda.md`) |
| 4 | O instrumento: convênio, MROSC, contrato; o decreto do DF; o que o termo obriga | o decreto errado em que penduramos dez obrigações | **escrito** (`modulos/04_o_instrumento.md`) |
| 5 | O fluxo por dentro da SES: quem pede, quem analisa, quem aprova, em que ordem, o que volta | a regra que dizia uma coisa e o processo que mostrava outra; o parecer favorável que não era aprovação | **escrito** (`modulos/05_o_fluxo_por_dentro_da_ses.md`) |
| 6 | Escolher o objeto: a fila, a ficha, o CNES, a sobreposição, o dossiê | os 50.317 da cardiologia e o dossiê do otorrino | **escrito** (`modulos/06_escolher_o_objeto.md`) |
| 7 | O preço: a tabela que vale, o mercado, a margem, o apoio | o valor errado de tabela e o apoio como valor fixo | **escrito** (`modulos/07_o_preco.md`) |
| 8 | O pré-plano: o formulário campo a campo; todo número vira compromisso | o pré-plano do otorrino e o retorno da SUCONV | **escrito** (`modulos/08_o_pre_plano.md`) |
| 9 | O plano: as 9 seções, a meta no piso, a planilha de baixo para cima | um plano da primeira à última versão; os erros dos cinco aprovados | **escrito** (`modulos/09_o_plano.md`) |
| 10 | Conferir e revisar: as baterias, a revisão cega, a leitura de entrega | uma leitura hostil que achou o que as baterias não acharam | **escrito** (`modulos/10_conferir_e_revisar.md`) |
| 11 | Depois da assinatura: execução, prestação de contas, controle externo | o termo que acabou em tomada de contas especial | **escrito** (`modulos/11_depois_da_assinatura.md`) |
| 12 | A oficina: agentes, comandos, ramos, pastas, o que nunca entra | um projeto de treino de ponta a ponta | **escrito** (`modulos/12_a_oficina.md`) |

## De onde sai cada módulo

O que já está escrito no repositório, e que o módulo aponta sem copiar:

| nº | no repositório |
|---|---|
| 1 | NM-001, NM-002, NM-077, NM-078 e NM-079 (a Constituição e as leis do SUS); OB-001 a OB-004; `biblioteca/instrumento/guia-entidades-sem-fins-lucrativos.md`; CT-008 e CT-012; `metodo/comum.md`, regras 5, 7, 8 e 11 |
| 2 | `biblioteca/instrumento/convenio_ses_df.md` ("O financiamento"), `biblioteca/instrumento/enquadramento_cnes.md`, `metodo/coleta/ficha_sigtap.md` |
| 3 | `biblioteca/instrumento/fluxo_emenda.md` (seções 1 e 3), `biblioteca/instrumento/guia-entidades-sem-fins-lucrativos.md`, NM-032, NM-054, NM-074, DD-004 e DD-007 |
| 4 | `biblioteca/instrumento/convenio_ses_df.md`, NM-010, NM-011, LI-026, CT-008, `registros/obrigacoes.csv`, `PLANEJADO.md` (item 10) |
| 5 | `biblioteca/instrumento/fluxo_emenda.md` (seção 2), `biblioteca/instrumento/convenio_ses_df.md` ("O rito"), `metodo/LEIA.md`, NM-013, NM-086, `registros/fontes/pre_planos_20261007/` |
| 6 | `metodo/coleta/dossie.md`, `metodo/coleta/mapa_social.md`, `metodo/coleta/ficha_sigtap.md`, `biblioteca/instrumento/enquadramento_cnes.md`, `planos/redacao_05/dossie/` |
| 7 | `metodo/coleta/precos.md`, `biblioteca/precos/`, LI-002, LI-038, `metodo/plano/procedimento.md` (travas F-04, F-08 e F-10) |
| 8 | `metodo/pre_plano/`, `planos/redacao_05/` |
| 9 | `metodo/plano/`, `metodo/comum.md`, `metodo/criterios.md`, `estudo/README.md` |
| 10 | `metodo/plano/conferencia.md`, `metodo/plano/leitura_de_entrega.md`, `metodo/revisao/cega.md` |
| 11 | `biblioteca/instrumento/fluxo_emenda.md` (seções 3 e 4), `registros/obrigacoes.csv`, CT-009, `PLANEJADO.md` (item 7) |
| 12 | `README.md`, `.claude/agents/`, `.claude/commands/`, `metodo/coleta/` |

A lógica e o caso de cada módulo saem das conversas em que o assunto foi discutido e
do que o usuário mandou para tirar dúvida. O garimpo segue as regras abaixo.

## As regras do curso

**1. O curso não guarda regra.** A regra mora em `metodo/`, e o fato sobre o instrumento,
em `biblioteca/`. O módulo aponta para lá e escreve só o que lá não existe: a lógica, o
caso e o exercício. Se o garimpo achar um fato novo sobre o instrumento, ele vai para a
`biblioteca/`, e o módulo aponta.

**2. Conversa é pista, não verdade.** O que se concluiu numa conversa antiga se confere
contra o estado atual do `metodo/`, da `biblioteca/` e da norma. Onde divergir, vale o
repositório, e a correção vira parte do caso.

**3. O caso conta o erro.** O que ensina a julgar é ver o que parecia certo e não era. O
caso diz o que se pensou, o que estava errado, como se descobriu e o que passou a valer,
com a data e o número.

**4. Nada de paciente.** Nenhum CPF, CNS, nome ou registro de atendimento entra no curso,
nem em exemplo.

**5. Dúvida sem resposta vira melhoria.** O que o módulo não responde vai para
`duvidas.md`, com a data e o módulo. É a fila de melhoria do curso.

## Como o curso muda

- Quando uma regra do `metodo/` muda, o módulo que aponta para ela é relido.
- `python3 ferramentas/testar_curso.py` confere que todo caminho e todo registro citado
  existe, que cada módulo tem as sete partes e que não há dado de paciente.
- Módulo novo ou caso trocado se registra em `metodo/MUDANCAS.md`, como toda mudança.

*Origem: pedido do usuário em 15/11/2026, para formar a pessoa que vai fazer a parte
técnica; item 6 do `PLANEJADO.md`, de 07/10/2026.*
