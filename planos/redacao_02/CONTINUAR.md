# CONTINUAR.md — segundo plano de trabalho

Como retomar em qualquer conversa nova, sem recontar histórico. O estado mora nos
arquivos.

---

## Ordem de leitura, para quem chega

0. **`analise_aprovados.md`** — *acrescentado em 31/08/2026, e o mais importante para
   quem chega agora.* O que os cinco planos aprovados de fato fazem, medido: o
   esqueleto deles, a banda real de custo acessório, e a **diligência da SES-DF**
   (Ofício nº 25/2026), que é a única evidência direta do que o analista cobra.
1. **`00_metodo.md`** — o acordo de trabalho: as rodadas, a regra do enxuto, o
   **teste do leitor** (novo, 31/08), o teste da norma citada, as três regras.
2. **`plano.md`** — o documento. **9 seções** (ver a estrutura padrão em `00_metodo.md`).
3. **`pendencias.md`** — os 43 itens que faltam, com dono. **É o único registro
   deles**: a versão de apresentação do documento não carrega marcações
   `[preencher]`.
4. **`estado.yaml`** — decisões travadas, rodada a rodada. **Não reabrir.**
5. **`verificacoes_internas.md`** — V-01 a V-12. O que saiu do documento e continua
   valendo, com dono e momento. **Não é entregue.**

Se for mudar conteúdo: `secoes/NN_*.md` é a fonte. Cada arquivo tem o **texto do
documento acima da linha dupla** e o **fechamento da rodada abaixo** — o fechamento
é método e não entra no documento.

Também no repositório: `duvidas_professor.md` (DV-050 a DV-055), `lacunas.csv`
(L-001 a L-038, com dono e se bloqueia) e `dados/fila_espera.md` (o painel).

---

## Como o documento se monta

`plano.md` é **gerado**, não editado. Mudança de conteúdo se faz no arquivo da
seção e o documento se remonta. A ordem é esta:

| # | seção | vem de |
|---|---|---|
| 1 | Identificação | `14_identificacao.md` |
| 2 | Objeto | `01_objeto.md` |
| 3 | Justificativa e dimensionamento | `12_justificativa.md` |
| 4 | Proponente | `13_proponente.md` |
| 5 | Metodologia e detalhamento das ações | `04_fluxo.md` + `06_equipe.md` + `02_metas.md` + `03_indicadores.md` |
| 6 | Cronograma físico | `05_etapas.md` |
| 7 | Cronograma de desembolso | `08_desembolso.md` |
| 8 | Planilha e memória de cálculo | `07_planilha.md` |
| 9 | Riscos | `11_riscos.md` |

**Atenção:** a seção 5 vem de quatro arquivos, na ordem fluxo → equipe → metas →
indicadores, com as subseções renumeradas 5.1 a 5.19 na remontagem. Os arquivos
`09_contas_monitoramento.md` e `10_contrapartida.md` **não entram mais** no
documento.

`10_contrapartida.md` **não integra o documento** — a seção foi retirada em
24/08/2026. O arquivo fica porque dele saíram o encerramento da L-026 e o achado do
art. 40.

### Regerar o `.docx`

```
npm ci && npm run docx -- redacao_02/plano.md redacao_02/plano.docx
```

(Desde 27/09/2026 o conversor mora na raiz, `md2docx.js`, e le o titulo do
cabecalho de `titulo_documento` no `estado.yaml`.)

O conversor é uma cópia adaptada do de `redacao/`, com os cabeçalhos de tabela
larga do plano novo. Nunca editar o `.docx` e o `.md` em paralelo.

---

## Os números que amarram o documento

Toda conferência aritmética passou em 25/08/2026. Os blocos de autoconferência
foram **retirados do documento** — eles são método, e o documento não os carrega:

```
metas por polo ......... 11.667 + 11.667 + 11.666 = 35.000
entradas efetivas ...... 35.000 (meses 1 a 9)
horários ............... 43.750 entrada + 43.750 retorno = 87.500
apoio por polo/mês ..... R$    96.237,33  (11 postos)
apoio total ............ R$ 2.966.419,90  (29,8% do global)
produção ............... R$ 7.000.000,00  (35.000 x R$ 200,00)
VALOR GLOBAL ........... R$ 9.966.419,90
teto ................... R$ 10.000.000,00 — diferença R$ 33.580,10, declarada
parcelas ............... 4, somando R$ 9.966.419,90
envelope comporta ...... 35.167,9 OCI — a meta fica 167,9 abaixo, = R$ 33.580,10
pico ................... 89,3 entradas completas por polo por dia útil
```

---

## As sete que antecedem a assinatura

Nenhuma se resolve escrevendo. Detalhe em `pendencias.md`.

| o que falta | dono |
|---|---|
| PAR contempla a OCI e admite novo executor | SES-DF |
| Diretriz do Plano Distrital de Saúde e da PAS | SES-DF |
| Capacidade instalada da rede própria da SES-DF | SES-DF |
| Parque de ecocardiografia do executor, por polo | proponente |
| Pesquisa de preços própria | proponente |
| Data prevista de celebração — 2026 é ano eleitoral e último de mandato (V-06 e V-07) | SES-DF |
| Relação nominal das PJs e dos profissionais | proponente |

---

## Seis dúvidas ao professor

Em `duvidas_professor.md`, continuando a numeração do plano anterior.

| id | pergunta |
|---|---|
| DV-050 | o que a SES-DF aceita como meta qualitativa |
| DV-051 | quem autoriza e abre a APAC no DF |
| DV-052 | equipe 100% PJ é "equipe própria" para o art. 33, §4º |
| DV-053 | qual dispositivo disciplina a antecipação de parcela |
| DV-054 | custo acessório quando a produção fica abaixo: despesa ou proporção |
| DV-055 | prestação de contas informatizada ou convencional (art. 30) |

---

## As regras, que continuam valendo

1. **Número não entra por plausibilidade.** Vem do usuário, tem fonte com data, ou
   é `[preencher]` no lugar exato.
2. **Total nunca fecha por ajuste.** A soma dá o que dá; a sobra fica declarada.
3. **Dependência de fonte única é controle interno.** Alterada em 31/08/2026.
   10 das 21 linhas (47,6%) se apoiam numa referência só — rastreadas em
   `verificacoes_internas.md`, V-08, onde definem a prioridade da pesquisa de
   preços. **Não vai ao documento.**
4. **Norma citada precisa de motivo.** *O que muda no plano se esta citação sair?*
5. **Fronteira anticópia.** Os quatro planos aprovados geram achado — em
   `registros/achados.csv`, AC-047 a AC-051 —, nunca parágrafo.
6. **Fora do documento tudo o que é método.** Sem `L-xxx`, sem `AC-xxx`, sem
   referência ao corpus. Verificado: zero ocorrências em `plano.md`.


---

## Rodada de 31/08/2026 — o que mudou, e vale para o próximo plano

**Parecer do professor.** O plano de trabalho é peça de instrução processual, não
memorial: quem lê é o parecerista, e tudo que se afirma vira obrigação aferível na
prestação de contas. Saíram 4.5, 4.6, 4.7, 10.4, o bullet da rastreabilidade, a
coluna "origem" da planilha e o risco da restrição eleitoral. **Nada foi apagado** —
migrou para `verificacoes_internas.md`. O critério está em `00_metodo.md`, no
**teste do leitor**.

**A IN CGDF nº 01/2005 INCIDE.** Corrigido pelo usuário. O gatilho é o art. 1º da
própria IN — transferência oriunda de dotação dos Orçamentos Fiscal e da Seguridade
Social —, não a origem federal ou distrital do recurso. Ver V-12. Três consequências
em aberto: o Anexo I (formulário), a declaração de não-mora do art. 2º, VIII, e o
motivo pelo qual a contrapartida fica fora.

**O acervo virou cinco planos, e dois modelos.**

| plano | proponente | produto | unitário | acessório % |
|---|---|---|---|---|
| pt_ses_01 | ISHP | consulta oftalmológica | 160,00 | 32,49% |
| pt_ses_02 | IEV | OCIs ortopedia | 100–150 | 30,65% |
| pt_ses_03 | IEV | OCI ortopedia | — | 31,41% |
| pt_ses_04 | IEV | OCIs multi | 130–350 | 36,57% |
| pt_ses_05 | ISHP | OCI oftalmologia | **200,00** | 16,00% ¹ |

¹ complementa estrutura existente — classe diferente. **A banda de quem levanta
estrutura é 30,65% a 36,57%.**

**Três achados que mudam como se monta a planilha:**

1. Nenhum dos cinco escreve "custo acessório" nem publica percentual. Todos itemizam
   tudo; nenhum calcula a razão.
2. Os dois modelos organizam a planilha por **Meta** — o apoio aparece como Meta 01
   (Planejamento e Estruturação) e Meta 03 (Monitoramento e Encerramento), isto é,
   como entrega, não como overhead.
3. A SES-DF abriu diligência contra o ISHP por **falta de detalhamento de rubrica**
   (material de consumo, sem itens e valores unitários). O crivo do analista é
   discriminação, não austeridade — café e açúcar estão em planilha aprovada.

## Extração de PDF digitalizado

`extrair_planos.py` resolve PDF nativo. Para **digitalizado** use
`extrair_digitalizados.py`, que lê a grade em pixel e faz OCR célula a célula:

```
python3 extrair_digitalizados.py planos_aprovados/ extraidos_ocr/ --doc pt_ses_NN
```

Ele recorta o timbre por coordenada (detectado por constância entre páginas, e a
amostra tem de vir só de páginas com grade) e **costura a tabela partida pela
paginação** num CSV único. No pt_ses_05: 0 → 17 tabelas, confiança 86,5 → 93,2, e a
planilha `planilha_p041-p053.csv` fecha em quatro níveis somando os itens lidos.

## O que ficou em aberto para a próxima conversa

- **O alvo de custo acessório** — o usuário ia definir. A derivação corre custo real
  → percentual, nunca o contrário (regras 1 e 2).
- **O Anexo I da IN** — formulário de 4 folhas. Os planos do ISHP começam por
  formulário e seguem em narrativa; os do IEV não. Confirmar com o professor.
- **A poda estrutural** — 1.2, 1.3, 4.2 a 4.4 e a seção 12 não existem em nenhum
  aprovado. É o maior corte ainda disponível.
- **Nossa rubrica de material de consumo** (uma linha, R$ 10.500 de papel) está
  exposta à mesma diligência que o ISHP levou.
