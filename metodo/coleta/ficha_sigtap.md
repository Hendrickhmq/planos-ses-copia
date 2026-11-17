# coleta/ficha_sigtap.md — a ficha do procedimento no SIGTAP

Vale para as duas trilhas: é a trava F-03 da fase 0 do plano (`../plano/procedimento.md`)
e a fonte do objeto do pré-plano. A ficha é fonte da fase 0 (`../comum.md`, regra 3):
idade, sexo, quantidade máxima, atributos, habilitações e compatibilidades só existem
lá, e quem vale é a tabela vigente na competência.

Quem executa é o agente `ficha-sigtap` (`.claude/agents/ficha-sigtap.md`), ou o
assistente na conversa. O método é este arquivo; o agente não guarda regra.

*Origem: as fichas lidas para o redacao_03 (31/08/2026), o redacao_04 e o redacao_05
(05–07/10/2026), cada uma no seu formato; o erro do R$ 600,11, tratado como prêmio
quando a tabela tinha mudado.*

---

## A fonte

| | |
|---|---|
| Sistema | SIGTAP — Tabela Unificada de Procedimentos do SUS (DATASUS) |
| Entrada | `http://sigtap.datasus.gov.br/tabela-unificada/app/sec/inicio.jsp` |
| Ficha | `http://sigtap.datasus.gov.br/tabela-unificada/app/sec/procedimento/exibir/<código sem pontos>/<MM>/<AAAA>` |
| Histórico | `http://sigtap.datasus.gov.br/tabela-unificada/app/sec/procedimento/exibir/<código sem pontos>` |
| Compatibilidades | menu Compatibilidades, `procedimentoCompativelConsulta.jsp`: código, competência, "Consultar" |
| Via | o **navegador embutido**. Para muitas páginas, `fetch` e `DOMParser` pelo `javascript_tool`, na mesma sessão, é bem mais rápido que navegar página a página. Em 19/10/2026 o `fetch` falhou quase sempre, e a navegação na aba funcionou: se o `fetch` voltar vazio ou com erro, navegar |

**A sessão.** O endereço direto devolve a página inicial se antes não se clicar em
"Acessar a Tabela Unificada" (o link chama `acessar()`, que envia o formulário do usuário
anônimo `publico`). **Depois do clique aparece "403 - Acesso Proibido" no `inicio.jsp`, e
é normal:** a sessão abriu (o menu mostra "Sair"); ir direto ao endereço da ficha. A
sessão expira: repetir o clique antes de cada lote.

**Quando o 403 não abre a sessão** (as páginas seguintes dão 500 ou voltam vazias para o
`inicio.jsp`): abrir o endereço da ficha sem sessão, esperar uns 40 segundos na tela de
entrada e só então clicar em "Acessar a Tabela Unificada". O servidor devolve a própria
ficha. Uma sessão em cada três ainda falha, e algumas servem só para a primeira página:
repetir até a sessão firmar, e então ler o resto em sequência. **Dois agentes no SIGTAP ao
mesmo tempo derrubam a sessão um do outro**, porque as abas do navegador embutido
compartilham o cookie: rodar as leituras em série, ou aceitar reabrir a sessão várias
vezes. *Origem: as leituras de 17 fichas do redacao_07, 15 a 19/10/2026.*

**A competência** é a vigente na data da leitura. **Competência ainda não publicada
devolve 404**, que parece erro de endereço. A lista confiável é a do seletor de
competência (menu Compatibilidades ou formulário da página inicial). Se o documento cita
outra competência, ler as duas e registrar a diferença.

**O pacote oficial da competência.** O FTP do DATASUS publica a Tabela inteira de cada
competência, `TabelaUnificada_<AAAAMM>_v<data>.zip`, na pasta
`ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/`. É a base que o SIGTAP carrega, e
ela sai quando a competência abre, mesmo quando a tela ainda serve a base velha. O
`ferramentas/ler_tabela_unificada.py` baixa o pacote para um cache fora do repositório e lê
dele o valor, a idade, o sexo, a quantidade máxima, o financiamento, o CID principal e as
compatibilidades com o tipo e a quantidade:

```bash
python3 ferramentas/ler_tabela_unificada.py --baixar 102026
python3 ferramentas/ler_tabela_unificada.py 102026 09.02.01.006-9
```

- **Com a tela em dia**, a ficha se lê na tela, e o pacote confere (`conferir_ficha.py`, H).
- **Com a tela parada**, a competência se lê no pacote, e não se reconstitui pelas Notas
  Técnicas. As abas que o pacote não traz (atributos, descrição, histórico) vêm da última
  competência que a tela serve, com a Nota Técnica para o que mudou.
- **A linha da leitura diz de onde veio** a competência: "na tela", "no pacote
  `TabelaUnificada_<AAAAMM>_v<data>.zip`" ou "reconstituída", com o motivo.
- O FTP republica: em 23/10/2026 saíram de novo os pacotes de 06 a 08/2026. Vale a versão
  mais nova.

*Origem: as fichas do redacao_08, 22/10/2026. A tela parou em 05/2026, e as sete fichas de
10/2026 foram reconstituídas pelas Notas Técnicas com o pacote de 10/2026 no FTP desde
15/10. Conferidas contra ele em 25/10/2026, as sete batiam.*

**Onde fica cada coisa na página:**
- grupo e subgrupo aparecem como "Sub-Grupo" e "Forma de Organização"; o financiamento,
  em "Financiamento" e "Sub-Tipo de Financiamento"; a idade, em "Idade Mínima" e "Idade
  Máxima"; há "Serviço Ambulatorial" e "Total Ambulatorial";
- **CID, CBO, Habilitação e Regra Condicionada ficam em abas**, já carregadas na página
  mas escondidas: o texto visível não mostra o CID. Clicar na aba, ou ler o conteúdo
  escondido. A aba CID tem duas: "CID Principal" e "CID Secundário";
- **os atributos aparecem só em texto**, sem número. O número (072, 054…) vem da
  portaria que criou ou alterou o atributo; escrever de onde veio.

**A composição da OCI não está na ficha: está em Compatibilidades.** Cada linha traz o
secundário, a portaria, o **tipo** ("Obrigatória", "Compatível" ou "Excludente"), a
**quantidade** (0 quer dizer sem limite) e o período ("Desde MM/AAAA" ou "De… até…", com
a portaria de revogação). O valor avulso de cada componente está na ficha dele
(`/exibir/<código>/<MM>/<AAAA>`, Serviço Ambulatorial).

**Armadilha: a consulta de Compatibilidades guarda o estado no servidor.** Depois de
algumas consultas, ela pode devolver o resultado de outro código ou de outra competência,
e o seletor volta a mostrar outra. Consultar um código por vez, voltando ao `inicio.jsp`
e abrindo o menu de novo, ou enviar o formulário por `fetch` com a competência fixada.
**Sempre conferir o código e a competência que aparecem no resultado.**

## O que se lê

Da ficha: grupo e subgrupo, modalidade e complexidade, financiamento, instrumento de
registro (APAC, BPA), sexo, idade mínima e máxima, quantidade máxima, atributos
complementares (com o número e o texto), habilitações, o valor do **Serviço
Ambulatorial** (e o hospitalar e o profissional, se houver), a descrição, a lista de
CID principal e as compatibilidades.

**Da OCI, também a composição:** cada procedimento do conjunto, com código e valor
avulso, e quais são obrigatórios. "E" e "ou" na descrição mudam o objeto: a 003-1 passou
de "videolaringoscopia **e** laringoscopia" a "videolaringoscopia **ou** laringoscopia"
em 09/2026.

**Do histórico:** cada mudança de valor, composição, atributo, regra ou habilitação, com a
competência e a portaria que a fez. A Tabela muda por portaria a cada poucos meses
(`../comum.md`, regra 2).

**A página de histórico não basta.** Ela lista só "competência – Incluído/Alterado –
portaria", sem dizer o que mudou, e **não mostra as mudanças de compatibilidade**: a SAES
2.331/2024, que tornou obrigatórios os exames das OCIs em 01/2025, não aparece nela. O
"o que mudou" sai de duas comparações: a ficha em cada competência do histórico (os
links levam a `/exibir/<código>/<MM>/<AAAA>`) e as datas "Desde" e "até" das
compatibilidades.

## Procurar e validar as portarias

Toda mudança do histórico — valor, composição, atributo, regra, a metodologia inteira —
se valida **no texto da portaria**, não só na página do SIGTAP.

1. **Procurar.** Além das portarias do histórico e das compatibilidades, ler a **Nota
   Técnica CGSI** de cada competência desde a leitura anterior: ela lista todas as
   portarias que alteraram a Tabela naquela competência, procedimento por procedimento.
   É o jeito de achar a portaria que mexeu no código e que o histórico não mostra.
2. **Validar.** Para cada portaria: está em `biblioteca/normas/` com linha no
   `registros/acervo.csv`? O artigo ou o anexo diz exatamente a mudança registrada
   (valor, descrição, atributo, tipo de compatibilidade)? Desde qual competência vale
   ("efeitos a partir da competência seguinte à publicação")?
3. **Registrar.** O histórico da ficha cita a portaria pelo número e diz onde no texto
   está a mudança (art. 1º, Anexo I). Portaria que falta no acervo se aponta; quem
   chama decide baixar e registrar.

*Origem: regra do usuário, 09/10/2026 — "procurar e validar portarias que mudaram os
valores, metodologia, tudo". Na mesma data, a validação no Anexo I da SAES 4.795/2026
corrigiu doze linhas do catálogo do grupo 09.*

## O que sai

```
dados/fontes/sigtap_<código sem pontos>_<MMAAAA>.md
```

No formato da ficha da 003-1 do `redacao_05`:

1. **Título:** `# SIGTAP <código com pontos e dígito> — <nome da tabela>`.
2. **A linha da leitura:** "Lido em <dd/mm/aaaa> na Tabela Unificada (competência
   <MM/AAAA>)."
3. **A tabela da ficha**, com as linhas: Grupo / subgrupo · Modalidade / complexidade ·
   Financiamento · Instrumento · Sexo / idade · Quantidade máxima · Atributos ·
   Habilitações · Regras condicionadas · CBO · **Serviço Ambulatorial** · Descrição ·
   CID principal. Financiamento FAEC se escreve com a ressalva "(só referência: a emenda
   não paga por FAEC)"; habilitações, com a ressalva de que descrevem o programa federal
   e não são condição do proponente.
4. **Os componentes**, quando for OCI: uma tabela com componente, tipo na OCI,
   quantidade, desde e valor avulso. A soma dos avulsos não entra.
5. **`## Histórico`**: competência, portaria (com onde no texto está a mudança), mudança,
   inclusive as de compatibilidade.
6. **`## CID para o Mapa Social`**: a faixa da ficha convertida na expressão do painel,
   para a coleta (`mapa_social.md`), em **duas linhas**:

   ```
   | | expressão |
   |---|---|
   | aceito | `codigo_cid_solicitado={"I*"}` |
   | finalidade | `codigo_cid_solicitado={"I50*"}` (proposta: a insuficiência cardíaca do nome da OCI; decisão do usuário) |
   ```

   - **aceito** é a lista da ficha inteira: o que a APAC aceita;
   - **finalidade** são os CID da lista que dão nome à OCI. Ela sai da descrição e do nome
     da OCI, nunca de fora da lista, e é proposta: quem decide é o usuário. Quando a lista
     já é a finalidade (I20 a I25 na síndrome coronariana), as duas linhas são iguais, e a
     ficha diz isso;
   - **CID largo**: quando o aceito cobre um capítulo inteiro ou mais de 20 categorias, a
     seção diz "CID largo" e por quê. A coleta não pode tratar esse CID como demanda.

   *Origem: o redacao_08, 22/10/2026. A ficha da 006-9 já dizia, numa nota, que o recorte
   da insuficiência cardíaca seria I50; a coleta usou o capítulo inteiro e deu 50.317
   pessoas.*

## O que a ficha não decide

- **A demanda.** O CID principal é o que a APAC aceita, não quem precisa da OCI. Quem
  mede a fila é a coleta, pela finalidade (`mapa_social.md`, "Os três números").

- **Condição de partida.** Financiamento FAEC, teto do programa e habilitação descrevem
  o procedimento no programa federal; não viram exigência do proponente quando a
  execução é por convênio de emenda (`biblioteca/instrumento/convenio_ses_df.md`).
- **O valor unitário com incremento.** Se uma portaria fixa incremento, a ficha registra a
  portaria; a conta vai para `dados/valor_unitario.md`, na conversa principal.

## A portaria

A portaria que fez a última mudança tem de estar em `biblioteca/normas/` com linha no
`registros/acervo.csv`. Se não estiver, dizer. O site da Imprensa Nacional (in.gov.br)
recusa o navegador embutido; o `curl` no terminal baixa.

## O catálogo do grupo 09

`registros/fontes/sigtap_grupo09_<MMAAAA>.csv` é o catálogo das OCIs que a verificação W
usa. A ficha lida é mais nova que ele: **se o valor, a idade ou a composição divergem,
o catálogo está desatualizado**, e a linha dele se corrige pela ficha, com a portaria
validada no texto. O nome do catálogo diz a competência, mas não a data em que foi
tirado: a linha DD-003 do `acervo.csv` registra isso. O de 09/2026 foi tirado antes da
SAES 4.795/2026 e corrigido por ela em 09/10/2026.

## Conferência

```bash
python3 ferramentas/conferir_ficha.py planos/redacao_NN/dados/fontes/sigtap_<código>_<MMAAAA>.md
```

Confere o nome do arquivo, a linha da leitura, os campos da tabela, o histórico, a
expressão de CID, que toda portaria citada no histórico está no acervo (pelo número e pelo
ano, como o nome do arquivo em `biblioteca/normas/` traz) e, para OCI, o
valor contra o catálogo do grupo 09. Com o pacote da competência no cache, confere a ficha
contra ele: valor, idade, o CID do pacote dentro da expressão aceita e, na OCI, os
obrigatórios e os compatíveis (H). Nas fichas lidas a partir de 25/10/2026, a linha da
leitura diz de onde veio a competência (B), e a seção de CID traz o aceito, a finalidade
e, se for o caso, "CID largo" (E).
