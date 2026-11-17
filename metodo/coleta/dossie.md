# coleta/dossie.md — o dossiê do objeto: qual fila e qual OCI

Vale para as duas trilhas, antes da fase 0: é onde se escolhe o objeto, quando há um
recurso para aplicar. Ele junta as coletas de um objeto num lugar só e separa duas coisas
que não podem se misturar:
- **a conta interna**, com a margem e o mercado;
- **a justificativa pública**, que pode ir à SES e ao documento.

**Quem executa é o assistente, na conversa principal.** Ele chama os agentes
`ficha-sigtap`, `mapa-social` e `precos` e junta o que eles devolvem, porque um agente não
abre outro. O comando `/dossie` (`.claude/commands/dossie.md`) começa por este arquivo.

*Origem: a escolha do objeto do redacao_05 (07–08/10/2026), feita na conversa, com cenários,
a comparação com o mercado e a OCI de nasofaringe escolhida como "a que paga melhor perto
do mercado". O alinhamento com o usuário em 09/10/2026 deu os dois pontos de partida, o
formato, o critério da margem e a regra de que a escolha tem de resistir à SES e aos
órgãos de controle.*

---

## Os dois pontos de partida

| | entra | pergunta |
|---|---|---|
| **escolher a fila** | o recurso: valor e origem | quais filas e quais OCI o recurso atende melhor? |
| **dada a fila** | uma fila do Mapa Social | em que OCI os pacientes dela se enquadram (CID, idade e sexo da ficha)? |

O resultado é o mesmo: uma página por OCI candidata, o comparativo e a justificativa.

**Escolher a fila começa pelo panorama.** O assistente escreve a ordem de panorama do
universo que o recurso pode pagar (o subgrupo, a especialidade ou tudo) e chama o
`mapa-social`. Lê as filas que voltam e escolhe com o usuário as candidatas. Pede ao
`ficha-sigtap` as fichas das OCI delas e só então escreve as ordens de medição, uma por
coleta, com as filas de partida do enquadramento do plano (`mapa_social.md`, "A ordem" e
"O enquadramento do plano"). **Dada a fila**, começa pela ficha e pela ordem de medição.
O panorama mostra as filas; quem as escolhe é o usuário.

*Origem: o agente `mapa-social` passou a só buscar, por ordem de coleta (plano aprovado pelo
usuário em 26/10/2026).*

## O critério

- **Executa-se a OCI de maior margem**, que em geral é a que paga melhor. Com o recurso fixo,
  o que sobra no total depende de quanto do custo a OCI cobre (a **cobertura**: o valor
  dividido pelo mercado mínimo), não da diferença por unidade. Por isso o comparativo segue a
  cobertura. Com um teto igual para todas as OCI, a margem no teto só repetiria a ordem do
  valor. *Origem: piloto do dossiê do redacao_05, 10/10/2026. Pela margem no teto, a
  progressão do déficit auditivo vinha primeiro; pela cobertura, vem a OCI de nasofaringe,
  que o usuário escolheu em 08/10/2026 como "a que paga melhor perto do mercado".*
- **O recurso quase nunca zera a fila.** Por isso se atende o maior número de pessoas da
  fila com a OCI mais cara em que elas se enquadram.
- **Quando o recurso zera uma fila, passa-se à próxima**, numa sequência combinada com a
  SES, que faz a regulação.
- **O dossiê ordena; a escolha é do usuário.**

*Origem: usuário, 09/10/2026.*

## A página de cada OCI

Seis partes, cada uma com a fonte:

| parte | o que tem | de onde |
|---|---|---|
| **1. Ficha** | valor, idade e sexo, CID, composição | `dados/fontes/sigtap_<código>_<MMAAAA>.md` (agente `ficha-sigtap`) |
| **2. Fila** | as pessoas que se enquadram pela **finalidade**, na fila inteira e na viva; o teto, só como referência; os alarmes da coleta; a espera média | a coleta em `dados/fontes/mapa_social_<AAAAMMDD>.md` (agente `mapa-social`) |
| **3. Normas** | o valor pela origem do recurso (LI-002); a última portaria que mudou a OCI, pelo histórico da ficha; o que a vigia trouxe | a ficha, `registros/vigia/` |
| **4. Aprovados** | quem já executa a OCI nos planos aprovados, a que valor e em que quantidade; o apoio de cada um, em percentual do valor global; o que o controle atacou neles | `estudo/normalizados/pt_ses_*/planilha.csv`, o achado AC-075, as peças CT do acervo |
| **5. Custo de executar** | o mercado mínimo e a mediana, a cobertura pela descrição inteira e pelo mínimo da APAC, a margem no teto | `dados/precos.md` (agente `precos`) |
| **6. A conta** | quantas OCI o recurso compra, quantas pessoas da fila isso atende, a parte da fila | abaixo |

**A fila da página é a da finalidade** (`mapa_social.md`, "Os três números"): no JSON da
coleta, `ocis.<código>.finalidade`. A medida padrão é a fila inteira, com a viva ao lado; a
linha `medida` diz qual entra na conta, e trocar pela viva é decisão do usuário. O teto
nunca é a fila da página. Cada alarme da coleta para aquela OCI vai para a linha
`alarmes`, e o que ele pedir de decisão vai para `pendencias.md`: com alarme aberto, o
dossiê ordena, mas não recomenda.

*Origem: o dossiê do redacao_08, 22/10/2026: os 50.317 do teto da insuficiência cardíaca
foram para a página, para a conta ("o IEV é 2% da fila") e para a justificativa ("mais de
50 mil pessoas").*

**A conta:**
- **o recurso para produção** é o recurso menos o apoio. O apoio é o do plano, se já
  decidido, ou o teto dele (trava F-08);
- **OCI que o recurso compra** = piso de `(recurso − apoio) ÷ valor` (`../plano/procedimento.md`,
  regra 1);
- **pessoas atendidas** = o menor entre as OCI que o recurso compra e as pessoas que se
  enquadram;
- **parte da fila** = pessoas atendidas ÷ pessoas que se enquadram, em percentual inteiro;
- **sobra do recurso** = recurso para produção − pessoas atendidas × valor. Quando a OCI zera
  a fila, a sobra é o que fica para a próxima.

Cada OCI se calcula como se levasse o recurso inteiro. A combinação de OCI, com a sequência
entre as filas, se decide depois do comparativo.

## O comparativo

`dossie/comparativo.md`: uma linha por OCI.
- **A ordem:** a maior cobertura primeiro. No empate, vem primeiro o maior valor.
- **O cabeçalho diz:**
  - o ponto de partida;
  - o recurso, com o valor e a origem;
  - o apoio considerado e de onde ele vem;
  - a data.

## A justificativa pública

`dossie/justificativa.md` é o texto que pode ir à SES e ao documento. Ele se apoia em:
- a fila medida (`../comum.md`, regra 11);
- a espera;
- a linha de cuidado completa da OCI para aqueles CID (LI-004);
- a prioridade da SES;
- a sequência proposta: "atender a fila X pelos pacientes que se enquadram na OCI Y, na
  ordem da regulação".

**A fila da justificativa é a da página**, a da finalidade. O teto não entra, nem como
"mais de N mil": ele mede o que a OCI aceitaria, não quem espera por ela.

**A justificativa não fala do que se recebe nem do que se paga.** Não traz valor em reais,
margem, mercado, oferta, teto nem cobertura, e não cita plataforma de preço. Também não
traz código do método (`LI-`, `AC-`...), porque ela pode ir ao documento (`../comum.md`,
regra 12). Concentrar
numa OCI se explica pela necessidade dos pacientes, não pelo que ela paga.

*Origem: usuário, 09/10/2026: a escolha tem de resistir à SES e aos órgãos de controle,
"que é o mais perigoso".*

## O que sai

```
planos/redacao_NN/dossie/
  comparativo.md       controle interno
  <código>.md          uma página por OCI, com o código sem pontos (0904010031.md); controle interno
  justificativa.md     o que pode ir a fora
```

A página:

```
# Dossiê — 09.04.01.003-1 OCI <nome>

**Controle interno: não vai ao documento.**

## 1. Ficha

| | |
|---|---|
| valor | R$ 393,55 |
| idade e sexo | ambos · 0 meses a 130 anos |
| CID | J30 a J39 |
| composição | consulta especializada e videolaringoscopia ou laringoscopia |
| fonte | `dados/fontes/sigtap_0904010031_092026.md` |

## 2. Fila

| | |
|---|---|
| medida | finalidade, fila inteira |
| pessoas que se enquadram | 3.459 |
| fila viva | (a coleta de 08/10/2026 é anterior à fila viva) |
| teto (referência) | 3.459 |
| alarmes | nenhum |
| espera média | 520 dias |
| fonte | `dados/fontes/mapa_social_20261008.md` |

## 3. Normas
## 4. Aprovados
## 5. Custo de executar

| | |
|---|---|
| mercado mínimo | R$ 395,50 |
| mercado mediana | R$ 700,00 |
| cobertura | 100% |
| cobertura (mínimo da APAC) | 100% |
| margem no teto | R$ 196,77 |
| fonte | `dados/precos.md` |

## 6. A conta

| | |
|---|---|
| recurso | R$ 1.502.687,00 |
| apoio | R$ 123.600,00 |
| OCI que o recurso compra | 3.504 |
| pessoas atendidas | 3.459 |
| parte da fila | 100% |
| sobra do recurso | R$ 17.797,55 |
```

O comparativo:

```
# Dossiê — <tema>: comparativo

**Controle interno: não vai ao documento.**

Ponto de partida: escolher a fila · Recurso: R$ 1.502.687,00, federal · Apoio: R$ 123.600,00 (decisão do usuário em 08/10/2026) · Montado em DD/MM/AAAA

| código | OCI | valor | mercado mínimo | cobertura | margem no teto | pessoas que se enquadram | OCI que o recurso compra | pessoas atendidas | parte da fila | sobra do recurso |
|---|---|---|---|---|---|---|---|---|---|---|
```

## Conferência

```bash
python3 ferramentas/conferir_dossie.py planos/redacao_NN/dossie/
```

| | confere |
|---|---|
| A | a pasta: o comparativo com o ponto de partida, o recurso e a origem, o apoio e a data; uma página por OCI do comparativo; a justificativa |
| B | as seis partes de cada página. A ficha, a coleta e o `precos.md` citados existem, e o número de pessoas está na coleta; na coleta com o JSON de 25/10/2026, ele é a finalidade (inteira ou viva, como a `medida` diz), e cada alarme da OCI está na linha `alarmes` |
| C | o valor da página pela origem do recurso: o da ficha na emenda federal; a Tabela SUS Candanga na distrital |
| D | o custo de executar igual ao do `dados/precos.md` |
| E | a conta: o piso da divisão, o menor entre as OCI e as pessoas, a parte da fila, a sobra do recurso |
| F | o comparativo igual às páginas, e na ordem da cobertura |
| G | a justificativa sem valor em reais, margem, mercado, oferta, teto, cobertura, plataforma de preço nem código do método, e com a fonte da fila; sem o número do teto, quando ele é maior que a finalidade |
| H | a marca de controle interno no comparativo e nas páginas, e não na justificativa |
