# coleta/mapa_social.md — a fila do objeto no Mapa Social da Saúde

Vale para as duas trilhas: é a trava F-05 da fase 0 do plano (`../plano/procedimento.md`)
e a justificativa do pré-plano (`../pre_plano/formulario.md`). A fila medida é a
justificativa (`../comum.md`, regra 11), e é daqui que ela sai.

*Origem: as coletas de 15/09, 05/10 e 06/10/2026 do plano 4 e a de 07–08/10/2026 do
redacao_05. Cada uma refez o método à mão, com um script próprio.*

---

## Quem faz o quê

| quem | faz | não faz |
|---|---|---|
| **conversa principal (o líder)** | destrincha o pedido ("tenho R$ 10 mi") em ordens de coleta; grava a `ordem.json` na pasta bruta; lê o que voltou; decide com o usuário; grava o enquadramento do plano | não coleta à mão |
| **agente `mapa-social`** | lê a ordem; abre o painel; carrega o kit do motor e roda a ordem; resolve o imprevisto (recarga no meio, campo que não responde); tira a saída do navegador; roda os três scripts; devolve o que eles imprimem, as lacunas e o que faltou no método | não decide, não interpreta, não escreve resumo, planilha nem script |
| **os scripts** | `ferramentas/mapa_social/motor.js` mede; `ferramentas/ler_motor.py` confere a saída; `ferramentas/montar_coleta.py` monta o JSON da coleta, o `.md`, a planilha, os alarmes e a diferença; `ferramentas/conferir_coleta.py` confere | não acessam o painel, fora o kit |

O agente só busca. A decisão de cada fila é do usuário, na conversa principal, e fica no
enquadramento do plano; o número sai do motor para o disco sem passar pelo modelo, ou
passa conferido por hash.

*Origem: a coleta de 26/10/2026 do redacao_07 (619 linhas no `.md`, 37 mil caracteres de
script feito na hora, uma `decidir()` que copiava decisões do usuário) e a de 22/10/2026
do redacao_08, em que o teto de 50.317 passou 7/7 porque o mesmo agente media e julgava.
Decisão do usuário, 26/10/2026: julgamento no script e na conversa; o agente só busca.*

## A ordem

O líder grava a ordem em `dados/fontes/mapa_social_<AAAAMMDD>[_sufixo]_bruto/ordem.json`
antes de chamar o agente. O agente a confere e a passa ao kit:

```bash
python3 ferramentas/montar_coleta.py --ordem <a pasta bruta>
```

Ordem incompleta faz o agente parar e devolver o que falta, sem medir nada. O hash da
ordem vai na saída do kit, e o `ler_motor.py` derruba a coleta de uma ordem trocada no
meio do caminho.

**Os campos comuns:** `contrato` ("2026-10-27"), `tipo` (`panorama` ou `medicao`),
`plano` (`planos/redacao_NN`), `pedido` (para quê, numa linha), `saida`
(`area_de_transferencia` ou `transcricao`; ver "A saída do navegador"), `janela_viva_meses`
(24) e `dimensoes`, entre `regiao`, `idade`, `cid`, `entrantes`, `ano`, `oferta` e `situacao`.
No panorama, `por_codigo` pede o rumo de cada código (abaixo).

**O panorama** não tem objeto: mede o universo pedido e devolve cada fila (nome exato ×
código) com fila, pessoas, devolvidas, fila viva, espera (média, mediana e máxima),
agendadas em 12 meses, pedido mais antigo e CIDs principais.

```json
{"contrato": "2026-10-27", "tipo": "panorama", "plano": "planos/redacao_NN",
 "pedido": "R$ 10 mi de emenda federal: onde aplicar?", "saida": "area_de_transferencia",
 "janela_viva_meses": 24, "dimensoes": ["regiao"], "minimo": 1,
 "universo": [{"rotulo": "consultas especializadas", "termos": ["CONSULTA"]},
              {"rotulo": "ultrassonografia", "codigos": ["02.05*"]},
              {"rotulo": "tudo", "tudo": true}]}
```

**O rumo por código.** No panorama, `"por_codigo": ["entrantes", "oferta", "situacao"]` mede,
para cada código SIGTAP das filas do universo, os entrantes pelo mês do pedido, a oferta pelo
mês do agendamento (com realizados e faltas) e a situação dos agendamentos em 12 meses. É por
código, e não por fila, porque a rede oferta o exame, e um código junta muitos nomes de fila. O
montador soma as filas de cada código e calcula, nos 12 meses fechados e nos 12 de antes, os
entrantes, a oferta, o saldo por mês, a falta, o maior mês de oferta e a média dos 3 últimos: é
o que mostra a fila que a SES já atende, a que cresce e o esforço que parou.

**Ordem grande, área de transferência.** A medição com dezenas de filas e todas as dimensões,
e o panorama com `por_codigo`, saem com centenas de milhares de caracteres: pela transcrição,
o modelo reescreve tudo (a coleta de 27/10/2026 da US de articulação, 61 filas, saiu em 73 mil
caracteres e quatro partes). Nesses casos a ordem vai com `area_de_transferencia`, avisando o
usuário de que a área de transferência dele será sobrescrita durante a coleta.

O universo vai por código (o subgrupo com curinga, `02.05*`), por termo do nome (cada
palavra casa pelo começo de uma palavra do nome: `RINOLOGIA` não acha `ENDOCRINOLOGIA`)
ou inteiro (`"tudo": true`). `minimo` é a fila mínima para a linha sair.

**A medição** tem objetos, cada um uma OCI ou um exame:

```json
{"contrato": "2026-10-27", "tipo": "medicao", "plano": "planos/redacao_NN", "pedido": "...",
 "saida": "area_de_transferencia", "janela_viva_meses": 24,
 "dimensoes": ["regiao", "idade", "cid", "entrantes", "ano"],
 "objetos": [
  {"id": "09.04.01.003-1", "tipo": "oci", "nome": "...", "ficha": "dados/fontes/sigtap_0904010031_092026.md",
   "codigos": ["02.09.04.004-1", "02.09.04.002-5"],
   "cid_aceito": "codigo_cid_solicitado={\"J3*\"}", "cid_finalidade": "codigo_cid_solicitado={\"J3*\"}",
   "idade": {"min": 0, "max": 130}, "sexo": "ambos",
   "filas": [{"nome": "CONSULTA EM OTORRINOLARINGOLOGIA - GERAL", "papel": "consulta", "entrada": true},
             {"nome": "VIDEOLARINGOSCOPIA", "papel": "exame", "obrigatorio": true}],
   "termos": ["RINOLOGIA"]},
  {"id": "02.04.03.018-8", "tipo": "exame", "nome": "...", "codigos": ["02.04.03.018-8"],
   "filas": [{"nome": "MAMOGRAFIA BILATERAL PARA RASTREAMENTO"}], "sexo": "feminino",
   "recortes": [{"rotulo": "rastreamento", "cid": "codigo_cid_solicitado={\"Z123*\"}"}]}]}
```

- **Na OCI**, tudo é obrigatório: os códigos dos **exames** da composição, o CID aceito e
  o da finalidade, a ficha na pasta do plano, a idade e o sexo da ficha, e as filas de
  partida com o papel. Pelo menos uma fila tem de ser a `entrada` (a consulta de entrada)
  ou `obrigatorio` (um exame obrigatório), porque o núcleo se mede por elas.
- **O código 03.01.01.007-2 não entra** em `codigos`: é o de toda consulta especializada
  do SISREG, e a varredura acharia todas. Na OCI, a consulta se acha pelo CID.
- **As filas de partida vêm do enquadramento do plano** (abaixo). O nome pode ir digitado:
  o kit acha o nome exato do motor, com as grafias que só diferem em espaço, espaço não
  separável ou acento, e o `.md` mostra o pedido ao lado do exato.
- **No exame**, idade, sexo e `recortes` de CID são opcionais.

*Origem: plano aprovado pelo usuário em 26/10/2026; a prova do P3 no painel, 26/10/2026.*

## O enquadramento do plano

`planos/redacao_NN/dados/enquadramento_mapa_social.json` guarda as decisões do usuário
sobre as filas do plano. A conversa principal o escreve, com o sim do usuário; o agente e
os scripts só o leem.

```json
{"atualizado": "DD/MM/AAAA",
 "filas": {"<nome exato>": {"decisao": "entra | fica fora | a decidir", "motivo": "... (usuário, DD/MM/AAAA)",
                            "papel": "exame | consulta", "generica": false}},
 "ocis": {"09.04.01.003-1": {"filas": ["<nome exato>"], "entrada": ["<nome>"], "obrigatorios": ["<nome>"]}}}
```

- A fila sem decisão sai **a decidir**, e a fila nova não entra na soma: entra na
  varredura, com o tamanho, para o usuário decidir.
- A ordem de medição copia daqui as filas de partida de cada OCI, com o papel.
- O montador guarda no JSON da coleta a cópia do enquadramento que usou (`entradas`): a
  coleta se refaz igual mesmo que o enquadramento mude depois.

*Origem: a `decidir()` refeita em cada script de coleta; plano aprovado em 26/10/2026.*

## A fonte

| | |
|---|---|
| Painel | Mapa Social da Saúde – Regulamentação (MPDFT) · Lista de Espera – Exames e Consultas |
| Endereço | `https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html` |
| App Qlik | `7edb02fa-f1f5-4ea6-b348-049a4ac2d095` |
| Dados | SISREG/DATASUS |
| Via | a camada de dados do próprio painel (Qlik Engine API), pelo **navegador embutido**, com o kit do motor. Sem leitura de tela e sem exportar pelos ícones |

## O kit do motor

`ferramentas/mapa_social/motor.js` é o único código que fala com o painel. Ele monta as
expressões de conjunto, pagina os hipercubos, mede a ordem e deixa a saída em
`window.__out`, em ASCII, dividida em partes com tamanho e hash djb2.

1. Na página do painel, numa aba própria do navegador embutido, colar o arquivo inteiro no
   `javascript_tool`. Os comentários podem ficar de fora: a assinatura é a do código das
   funções. Depois, `__ms.abrir()` (se o app ainda não está aberto na aba).
2. Conferir `__ms.assinatura()` contra `node ferramentas/mapa_social/motor.js --assinatura`.
   Diferente é kit colado errado: colar de novo.
3. `__ms.rodar(<ordem>)`, com a ordem como o `montar_coleta.py --ordem` a imprime. O kit
   roda em segundo plano; acompanhar com `__ms.estado()` (a cada 20 ou 30 segundos, com
   `await new Promise(r => setTimeout(r, 25000))` na mesma chamada).
4. `estado.erro` diz por que parou:
   - "recarga no meio": a base recarregou entre o começo e o fim. Rodar de novo;
   - "campo que não responde": o kit confere cada campo contra a lista do app antes de
     medir, porque **o motor ignora em silêncio o campo que não existe** e devolve a
     base inteira. A mensagem traz a lista dos campos; registrar e parar.
5. Com o estado "pronto", tirar a saída (abaixo). No fim, a aba fica aberta: com uma aba
   só, fechá-la fecha o navegador embutido.

O que o kit faz, em ordem: confere os campos; lê as datas (recarga, hora da consulta pelo
`Now()`, solicitação mais recente, agendamento mais distante); lista os nomes de fila das
duas tabelas; varre; mede cada objeto (ou o panorama); lê as datas de novo.

- **O `javascript_tool` corta em 45 segundos**: por isso o kit roda em segundo plano, e
  cada chamada só lê o estado.
- **O texto do `javascript_tool` passa pela ferramenta**, que troca o `\u` pelo
  caractere antes de rodar. O kit é ASCII, e a assinatura se calcula sobre a fonte com
  todo caractere fora do ASCII escrito como `\u`: sai igual no node e no navegador.
- Os testes do kit rodam no node, com um motor falso (`ferramentas/testar_motor_js.mjs`,
  `ferramentas/mapa_social/motor_falso.mjs`).

*Origem: o trecho de JavaScript solto que cada coleta refazia (piloto de 08/10/2026); a
prova do P3, 26/10/2026, em que um comentário esquecido dentro de uma função mudou a
assinatura e a conferência pegou.*

## A saída do navegador

Dois caminhos. O líder escolhe na ordem (`saida`).

1. **Área de transferência.** `__ms.preparar(300000)` divide a saída;
   `__ms.botao(i)` põe na página o botão "copiar parte i/n". O agente clica nele com o
   `computer` (um clique de verdade) e grava a parte com
   `pbpaste > <pasta bruta>/motor_parte_i.txt`. O modelo não transcreve número nenhum.
   - O `navigator.clipboard` é negado no painel; o botão usa o `execCommand('copy')`, que
     funciona no clique.
   - O botão **sobrescreve o que o usuário tiver copiado**, e o app avisa o usuário a cada
     cópia feita pela página. Não usar enquanto o usuário trabalha na mesma máquina.
   - Com o painel do navegador escondido, a aba mede 0 × 0 e o botão fica fora da área
     visível: achá-lo com o `find` ("copiar parte") e clicar pela referência.
   - O caminho inverso não funciona: o `cmd+V` do `computer` não cola na página o que o
     `pbcopy` copiou.
2. **Transcrição.** `__ms.preparar(20000)` e, para cada parte, `__ms.parte(i)` lido pelo
   `javascript_tool` e gravado em `motor_parte_i.txt` sem mudar nada: o cabeçalho
   `#ms-parte i/n tamanho=... hash=...` e o texto.

Nos dois caminhos, `python3 ferramentas/ler_motor.py <pasta bruta>` confere o tamanho e
o hash de cada parte e do texto inteiro, a assinatura do kit e o hash da ordem, procura
CPF e CNS, restaura o `{U+XXXX}` e converte as datas seriais. Grava
`motor_<AAAAMMDD>.json`.

*Origem: sondagem de 26/10/2026 (50.042 caracteres pela área de transferência, com o mesmo
hash) e a coleta de 26/10/2026 do redacao_07, transcrita pelo modelo com um hash
improvisado.*

## A medida

| o quê | expressão ou regra |
|---|---|
| **fila** | `Count(Distinct {1<status_solicitacao_alias={'SOLICITAÇÃO PENDENTE DE REGULAÇÃO','SOLICITAÇÃO CORRIGIDA E REENVIADA PARA REGULAÇÃO','SOLICITAÇÃO PENDENTE DE REGULAÇÃO POR FILA DE ESPERA'}>} contador_solicitacao)` — a medida "Solicitações" do cabeçalho do painel |
| **devolvidas** | `status_solicitacao_alias={'SOLICITAÇÃO DEVOLVIDA PARA COMPLEMENTAÇÃO PELO SOLICITANTE'}`: ficam **fora** da fila e se contam à parte. A "corrigida e reenviada" é ex-devolvida que voltou, e está dentro |
| **total** | `Count(Distinct {1} contador_solicitacao)`, a medida dos gráficos do painel, com as devolvidas. Só para comparar; nunca é a fila |
| **pessoas** | `Count(Distinct {o conjunto da fila} cns_usuario_solicitacao)`: quem espera por mais de um exame conta uma vez |
| **espera** | `Avg`, `Median` e `Max` de `tempo_espera_solicitacao`, em dias, no conjunto da fila. A espera de um conjunto de filas se calcula no motor, sobre os registros, e não como média das linhas |
| **entrantes** | abertas + agendadas, por mês. As abertas são **todos os status** da tabela de solicitações. A data de solicitação de quem já foi agendado é `data_agendamento - tempo_espera_agendamento`; no motor, a dimensão calculada `=Date(MonthStart(data_agendamento - tempo_espera_agendamento),'YYYY-MM')`, com `Ano_Agendamento` restrito aos anos da série na medida |
| **oferta** | os agendamentos pelo **mês em que acontecem** (`=Date(MonthStart(data_agendamento),'YYYY-MM')`), nos 24 meses de calendário dos entrantes e o já marcado para depois, em todas as situações; ao lado, os realizados e as faltas pela situação do agendamento. É a série que mostra o mutirão que acabou: os entrantes contam o agendamento pelo mês do pedido, e o mês recente sai baixo porque o pedido ainda espera |
| **situacao** | os agendamentos dos 12 meses (a janela das agendadas) por `status_solicitacao_agendamento_alias`. A **falta** é faltas ÷ (realizados + faltas), calculada no montador |
| **sem fila de agendamento** | a oferta e a situação de um objeto sem nome na tabela de agendamentos viram lacuna: sem o nome, o conjunto seria a base inteira |
| **recorte** | todos os anos, também para as devolvidas. Cada procedimento entra fixo na expressão de conjunto, `{1<descrição_procedimento_solicitacao={...}>}`, que ignora a seleção da tela |
| **fila viva** | a fila só com as solicitações dos últimos **24 meses**, contados da solicitação mais recente da base: `data_solicitacao={">=DD/MM/AAAA"}` na mesma expressão de conjunto, com a data no formato do campo. Conferir contra a soma por `Ano_Solicitacao`: a viva nunca passa da fila inteira. Sai ao lado da fila inteira, nunca no lugar dela |
| **agendadas em 12 meses** | `data_agendamento` dos 12 meses até a véspera da solicitação mais recente, todos os status, pelo par nome × código da tabela de agendamentos. O par que existe lá sem agendamento na janela dá 0; o que não existe lá fica sem número (a fila pode ter outro nome) |
| **sexo da ficha** | exclui o sexo oposto, e não seleciona o da ficha: `cns_usuario_solicitacao=E({1<sexo_usuario={'MASCULINO'}>} cns_usuario_solicitacao)` para uma ficha feminina. Cerca de 11% da fila não tem sexo ligado, e a seleção os perderia |
| **idade da ficha** | `idade_solicitacao={">=min<=max"}`, a idade na solicitação |
| **sem Região de Saúde** | a diferença de conjuntos `{1<o conjunto> - 1<regiao_saude_solicitante={"*"}>}`. A linha "-" de um hipercubo com dimensão de outra tabela traz a base inteira, e não os sem região |
| **pessoas na união** | de recortes com CIDs diferentes: `{1<...>+1<...>}`. Pessoas nas duas famílias, sem expor CNS: `Sum({1} Aggr({1} If(Count({A})>0 and Count({B})>0,1,0), cns_usuario_solicitacao))` |

**Os campos que responderam até hoje:**
- solicitação: `descrição_procedimento_solicitacao` (1.571 nomes em 26/10/2026),
  `codigo_sigtap_solicitacao` (o código sem pontos e sem o zero da frente: 204030188),
  `descricao_sigtap_solicitacao`, `codigo_cid_solicitado`, `CID_solicitacao`,
  `status_solicitacao_alias`, `contador_solicitacao`, `cns_usuario_solicitacao`,
  `tempo_espera_solicitacao`, `regiao_saude_solicitante`, `data_solicitacao`,
  `idade_solicitacao` (a idade na solicitação, não a de hoje), `Ano_Solicitacao`,
  `Mes_Solicitacao` (texto: 'jan', 'fev'…);
- agendamento: `descrição_procedimento_agendamento` (2.247 nomes em 26/10/2026),
  `CID_agendamento`, `contador_agendamento`, `data_agendamento`, `tempo_espera_agendamento`,
  `Ano_Agendamento`, `codigo_sigtap_agendamento` (o mesmo código da solicitação para o mesmo
  nome de fila; conta as agendadas por código sem passar pelo nome da fila — coleta de
  15/10/2026 do redacao_07), `status_solicitacao_agendamento_alias` (a situação do
  agendamento: 'PROCEDIMENTO REALIZADO', 'PROCEDIMENTO NÃO REALIZADO POR FALTA DO PACIENTE',
  'PROCEDIMENTO AGENDADO PENDENTE DE CONFIRMAÇÃO', 'SOLICITAÇÃO AUTORIZADA PELA REGULAÇÃO' e
  três de cancelamento — coleta do IEV de 26/10/2026);
- usuário: `sexo_usuario`, com 'FEMININO' e 'MASCULINO', ligado às solicitações pela
  tabela de ligação (sondagem de 26/10/2026). A mesma tabela tem `no_usuario`, o nome, e o
  app tem telefones: **nunca saem**.

Um hipercubo devolve no máximo 10.000 células por página: com 16 colunas, 625 linhas. O kit
pagina; a lista das filas com duas colunas cabe numa página só. Acima do limite, o motor
responde "Result too large".

Se um nome não responder, o kit para e lista os campos do app; registrar o nome novo aqui.

*Origem: sondagem do painel, 26/10/2026 (sexo, devolvidas, paginação, campo que não existe,
linha sem região).*

## O recorte do objeto

- **Procedimento avulso** (exame, consulta): pelo nome da fila no SISREG
  (`descrição_procedimento_solicitacao`), conferido contra o `codigo_sigtap_solicitacao`.
- **OCI:** nenhuma fila do SISREG carrega o código da OCI. A demanda está nas filas dos
  procedimentos da composição, e o **critério é o CID da solicitação**
  (`codigo_cid_solicitado`) contra os CID da ficha do SIGTAP (`../comum.md`, regra 3). A
  ficha já traz as expressões prontas, na seção "CID para o Mapa Social"
  (`ficha_sigtap.md`). A fila sem o CID da ficha fica fora, com o motivo.

**O CID da ficha é o que a APAC aceita, não quem precisa da OCI.** Na otorrino os dois
quase coincidem: H60 a H95 em audiometria e BERA. Na cardiologia, não: a ficha da
insuficiência cardíaca aceita o capítulo I inteiro, e o ECG e o Holter são pedidos para
quase tudo. A união das filas da composição com o capítulo I deu 50.317 pessoas, a maior
parte com hipertensão, e com I50 a fila ficava em poucos milhares. Por isso cada OCI sai
com três números:

| número | recorte | para quê |
|---|---|---|
| **teto** | o CID aceito pela ficha, na união das filas da composição | referência: o máximo que a OCI aceitaria. Nunca é a fila do dossiê nem da justificativa |
| **finalidade** | o CID da finalidade, os da ficha que dão nome à OCI (I50 na insuficiência cardíaca), na união das filas da composição | **a fila da OCI**: as pessoas que se enquadram, no dossiê e na justificativa |
| **núcleo** | o CID da finalidade só na consulta de entrada da OCI (a fila `entrada` da ordem), ou em quem espera todos os exames obrigatórios ao mesmo tempo (as filas `obrigatorio`), o que for maior; a coleta diz qual | o piso: quem certamente precisa do percurso inteiro |

Cada um sai em pessoas, com a fila inteira e a **fila viva** lado a lado, e **dentro da
idade e do sexo da ficha** (`idade_solicitacao`, a idade na solicitação): a 001-8 e a
002-6, de 18 anos em diante, tinham 441 e 502 pessoas pelo CID e 360 e 420 na idade. O CID
da finalidade vem da ficha (linha "finalidade") e é decisão do usuário. Quando a ficha não
o separa, ou a lista é estreita, a finalidade é igual ao teto e a coleta diz isso. Quando a
composição tem exames e consultas, a finalidade sai também só nos exames e só nas consultas.

*Origem: a coleta do redacao_08, 22/10/2026 (OCI de cardiologia), e o diagnóstico de
25/10/2026: o agente seguiu o método, e o método tratava o CID aceito como demanda.*

**O CID muda de formato entre as tabelas.** `codigo_cid_solicitado` vem sem ponto
("H903", "J35"); `CID_solicitacao` e `CID_agendamento` vêm com o nome ("H91 - OUTRAS
PERDAS DE AUDICAO"). A faixa da ficha vira expressão de conjunto com curinga; na tabela de
agendamentos, o kit põe o curinga em todo valor:

| faixa da ficha | expressão |
|---|---|
| H60 a H95 | `codigo_cid_solicitado={"H6*","H7*","H8*","H90*","H91*","H92*","H93*","H94*","H95*"}` |
| J30 a J39 | `codigo_cid_solicitado={"J3*"}` |

**A varredura vem antes de tudo, em toda coleta.** O objetivo é conhecer **todas** as
filas que uma OCI ou um exame atende, e não só as da coleta anterior ou as que o nome
sugere. A demanda do objeto se espalha por filas de nomes, códigos e faixas etárias
diferentes, e fila que não se procura não aparece.

| objeto | como o kit varre |
|---|---|
| **OCI** | todas as filas, na tabela de solicitações e na de agendamentos, com o CID aceito e o da finalidade; mais as filas dos códigos dos exames da composição e as de nome parecido com as filas de partida ou com os `termos`. Inclui as filas de consulta, não só as de exame |
| **exame avulso** | todas as filas com o `codigo_sigtap_solicitacao` do exame; as de nome parecido com as filas de partida (o nome contido no outro: as variantes e faixas etárias do mesmo nome) e as dos `termos` (a audiometria do SISREG vem registrada como campo livre, 02.11.07.003-3) |

**Cada fila encontrada se estuda:** fila, pessoas, devolvidas, espera, os CIDs
principais, a idade, desde quando existe (fila só de 2026 pode ser fila recriada), a
oferta (agendadas em 12 meses) e, na OCI, quantos pedidos dela têm o CID do objeto. E
recebe a decisão do enquadramento: **entra**, **fica fora** (com o motivo) ou **a decidir**.
Tudo vai para a seção "Varredura das filas" do resumo.

No resumo, a fila achada **só pelo CID** aparece quando o CID aceito do objeto é pelo
menos 5% dos pedidos dela (`LIM_VARREDURA` do `conferir_coleta.py`); as outras ficam no
JSON e na planilha, contadas numa linha. Na otorrino, J30–J39 aparece em 120 filas, a
maioria com 0,1% dos pedidos (Holter, endoscopia digestiva); acima de 5% ficaram 34, entre
elas a consulta para respirador bucal (91%) e a de rinologia (93%).

*Origem: regra do usuário, 09/10/2026, depois de a coleta piloto achar duas filas de
consulta da 003-1 que as coletas anteriores não tinham listado; o limite de 5%, prova do P3,
26/10/2026.*

**As quatro regras do enquadramento:**
1. **Fila nova não entra na soma sem decisão**: vai para a varredura, como "a decidir",
   com o estudo dela.
2. **A mesma fila em duas OCIs** (a consulta de otorrino geral, com CIDs diferentes)
   conta em cada uma pelo seu CID. O resumo diz quantas pessoas estão nas duas.
3. **O enquadramento mora no plano** (`dados/enquadramento_mapa_social.json`, acima): o
   nome interno exato de cada fila, a decisão, o papel da fila e quais filas vão em cada
   OCI. A ordem seguinte parte dele, e não do `.md`.
4. **Fila genérica só entra pelo CID da finalidade, e nunca como "entra" sem decisão.**
   Genérica é a fila pedida para muitos fins: eletrocardiograma, raio-X de tórax, Holter,
   ecocardiograma, laboratório, e a consulta geral ou "adulto" da especialidade. No teto
   ela aparece, marcada; na finalidade, só com o CID da finalidade; e a decisão de pô-la
   na OCI é "a decidir" até o usuário dizer.

**Armadilhas já vistas:**
- **Grafia: nunca digitar o nome da fila na expressão.** O kit lista os nomes pelo
  hipercubo, normaliza só para procurar e usa na expressão o texto exato que o motor
  devolveu. Já apareceram: espaço não separável seguido de espaço comum (angiotomografia de
  coronárias); espaços duplos e nome sem acento ("VIDEOENDOSCOPIA␣␣NASAL␣␣FLEXIVEL",
  "CONSULTA EM␣␣RINOLOGIA"); travessão U+2013 e "ATÉ" com acento (audiometria e BERA). O
  `.md` escreve o nome bonito e mostra o exato na seção "Nomes internos"; o JSON guarda o
  exato.
- **O código da fila não é o código do exame:** as filas de audiometria do SISREG são
  registradas como 02.11.07.003-3 (campo livre), não como o exame da OCI.
- **Região:** parte da fila vem de unidade de referência distrital ou de contratado, sem
  Região de Saúde. Na tomografia do plano 4 era mais da metade. Mostrar essa parte em
  linha própria; nunca ratear em silêncio.
- **Fuso:** o `qLastReloadTime` vem em UTC; a recarga das 01:32 UTC é 22:32 em Brasília
  do dia anterior. O cabeçalho do painel ("Atualizado em") junta a data em UTC com a hora
  de Brasília: dizia 27/10/2026 22:32:42 para a recarga de 26/10/2026 22:32:42. A data da
  coleta é a do kit, nunca a da tela.
- **Um dia muda pouco:** a recarga atualiza status e completa o fim do mês. Comparar com a
  coleta anterior antes de concluir que a fila andou.
- **A base recarrega até duas vezes por dia** (14:36, 16:32 e 22:32 em 26/10/2026). A
  coleta com recarga no meio não vale: o kit para.

## Os alarmes

O número do painel é exato, mas pode não ser a fila do objeto. Antes de devolver, a
coleta se pergunta se aquele número é de quem precisa do objeto. Seis sinais dizem que
talvez não seja:

| alarme | quando | o que fazer |
|---|---|---|
| **CID largo** | o CID aceito pela ficha cobre um capítulo inteiro (`"I*"`) ou mais de 20 categorias | calcular a finalidade; o teto não vai ao dossiê |
| **CID dominante** | numa fila do teto, um só CID (três caracteres) de fora da finalidade passa de 30% das solicitações | dizer qual e quanto (I10 em 88% do ECG com CID do capítulo I) |
| **CID raro** | a finalidade de uma OCI pega menos de 5% das filas da composição | a demanda pode estar com outro CID (o da cirurgia, no risco cirúrgico): levar a fila sem recorte como "a decidir" |
| **fila velha** | mais de 30% das pessoas da finalidade só têm pedido de antes da janela da fila viva | pôr a viva ao lado, e dizer desde quando há pedido |
| **estoque** | numa fila do objeto, a fila passa de 3 anos de agendamentos (fila ÷ agendadas em 12 meses > 3), ou não houve agendamento em 12 meses | dizer quantos anos: a fila não anda, e parte dos pedidos pode não valer mais |
| **fila genérica** | uma fila genérica está na composição da OCI (regra 4 do enquadramento) | dizer qual, e que ela só conta pela finalidade |

Quem calcula é o `conferir_coleta.py` (`alarmes()`), e o montador usa a mesma função: os
limites moram num lugar só. O alarme não muda o número: põe ao lado dele o que o usuário
precisa saber para decidir. Vai para a seção "Alarmes" do resumo e para o topo da resposta
do agente. Sem alarme, a seção diz "nenhum". No panorama, os alarmes não se aplicam.

*Limites propostos em 25/10/2026 (30%, 5%, 24 meses, 3 anos), a confirmar pelo usuário.
Na coleta de cardiologia de 22/10/2026, os seis disparavam, e nenhum estava no topo.*

## O que sai

```
dados/fontes/mapa_social_<AAAAMMDD>.md        o resumo que o documento usa
dados/fontes/mapa_social_<AAAAMMDD>.xlsx      a planilha, uma aba por tabela, com uma "Leia-me"
dados/fontes/mapa_social_<AAAAMMDD>_bruto/
  ordem.json              a ordem do líder
  motor_parte_N.txt       a saída do kit, como saiu do navegador
  motor_<AAAAMMDD>.json   o JSON do motor (ler_motor.py)
  coleta_<AAAAMMDD>.json  o JSON da coleta (montar_coleta.py), com as entradas que usou
  montagem.json           a versão do montador e o hash de cada arquivo que ele gravou
  README.md               o que tem a pasta
```

Quando já existe coleta do mesmo dia, a ordem nova vai com sufixo
(`mapa_social_<AAAAMMDD>_<sufixo>_bruto/`), e nada se sobrescreve.

**Quem escreve tudo é o montador:**

```bash
python3 ferramentas/montar_coleta.py <a pasta bruta>
```

Ele lê a ordem, o JSON do motor, o enquadramento do plano e a coleta anterior mais recente
da mesma pasta (ou a de `--anterior`), e imprime a resposta que o agente devolve: alarmes,
datas, tabela curta, achados fora do enquadramento com o tamanho, as filas que o enquadramento
deixou a decidir, lacunas. **Nenhum número
calculado se mistura aos do motor**: o que o montador calcula (anos de estoque, a parte de
uma fila no CID, os entrantes, a diferença) diz "calculado".

O `.md` abre com uma tabela que traz **obrigatoriamente**:

| campo | o que é |
|---|---|
| Fonte | o painel e o endereço |
| Última recarga da base | data e hora do `qLastReloadTime`, em Brasília |
| Consulta | data e hora da consulta, do começo ao fim, pelo relógio do motor |
| Solicitação mais recente na base | a maior data de solicitação |
| Medida | "fila", com os três status, e as devolvidas fora |

Logo depois, as seções **"Alarmes"** e **"Lacunas"**. Na OCI, **a tabela dos três números**,
uma linha por OCI, com o cabeçalho:

```
| OCI | CID aceito | CID da finalidade | teto | teto viva | finalidade | finalidade viva | núcleo | núcleo viva | espera média (finalidade) |
```

Depois: os exames; as filas do objeto, sem recorte e por recorte de CID; a **"Varredura
das filas"**, com o estudo e a decisão de cada uma; a Região de Saúde, com a linha sem
região; idade, CID, ano, entrantes, oferta e situação, quando pedidos; no panorama com `por_codigo`, o "Rumo por código"; a diferença para a coleta anterior; e
os nomes internos. No panorama, cada universo sai em três tabelas: por pessoas, as 20 de
maior espera média e as 20 de mais anos de estoque. O panorama mostra; não ordena para
escolher nem recomenda.

**O JSON da coleta** (`coleta_<AAAAMMDD>.json`) guarda, além da medida (`filtro_fila`) e
dos nomes internos (`nomes_internos`), o que a conferência usa para refazer os alarmes:

```json
{
  "metodo": "2026-10-27", "tipo": "medicao", "janela_viva_meses": 24,
  "filas": {
    "<nome interno exato>": {
      "papel": "exame", "generica": true, "objetos": ["09.02.01.006-9"],
      "fila": 36152, "fila_viva": 10639, "agendadas_12m": 2735,
      "recortes": {
        "teto 09.02.01.006-9": {"fila": 25259, "fila_viva": 10639, "cid_principais": [["I10", 6365], ["I49", 3862]]}
      }
    }
  },
  "ocis": {
    "09.02.01.006-9": {
      "cid_aceito": "codigo_cid_solicitado={\"I*\"}", "cid_finalidade": "codigo_cid_solicitado={\"I50*\"}",
      "recorte_teto": "teto 09.02.01.006-9", "recorte_finalidade": "finalidade 09.02.01.006-9",
      "filas": ["<nome interno exato>"],
      "teto": {"pessoas": 50317, "pessoas_viva": 0},
      "finalidade": {"pessoas": 0, "pessoas_viva": 0},
      "nucleo": {"pessoas": 0, "pessoas_viva": 0, "como": "consulta de entrada"}
    }
  },
  "exames": {}, "varredura": [], "dimensoes": {}, "lacunas": [], "alarmes": [],
  "entradas": {"enquadramento": {}, "anterior": null}
}
```

`fila` é sem recorte de CID; `cid_principais`, os dez CID mais pedidos no recorte, pela
categoria (os três primeiros caracteres: a dimensão `=Left(codigo_cid_solicitado,3)`).

## O que nunca sai do painel

**Só contagens agregadas.** Nenhum CNS, CPF, nome, telefone ou data de nascimento de
usuário vai para o `.md`, a planilha ou o JSON. O kit nunca põe esses campos em dimensão,
e o hipercubo que precisa do CNS para contar pessoas devolve a contagem, não a lista. O
`ler_motor.py` procura CPF e CNS na saída antes de gravar.

## Conferência

```bash
python3 ferramentas/conferir_coleta.py planos/redacao_NN/dados/fontes/mapa_social_<AAAAMMDD>.md
```

Confere os campos obrigatórios, a pasta bruta, a seção de varredura das filas, e procura
CNS e CPF no `.md` e na pasta bruta. Nas coletas a partir de 25/10/2026, também **refaz os
alarmes pelo JSON** e exige cada um na seção "Alarmes" (H), e exige na OCI a tabela dos três
números, igual ao JSON (I). Nas coletas a partir de 27/10/2026, e nas que têm a `ordem.json`:
- **J, a ordem:** está na pasta bruta, completa, é a que o kit rodou (hash), e cada
  objeto, dimensão e universo pedido tem número ou lacuna com motivo;
- **K, montado:** o `.md`, o README e os dois JSON são os que os scripts gravaram (o hash
  de cada um no `montagem.json`), e, na mesma versão do montador, a coleta se refaz
  inteira das partes que saíram do navegador e dá o mesmo texto. A edição à mão derruba a
  coleta.

Em 100% antes de o número entrar no documento. A conferência não diz se o número é o certo:
diz se o resumo mostra o que o número esconde e se ninguém mexeu nele depois do motor. A
decisão continua do usuário.
