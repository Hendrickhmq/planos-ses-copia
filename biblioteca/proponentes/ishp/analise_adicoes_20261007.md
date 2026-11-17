# ISHP — o que a equipe acrescenta aos nossos planos, e de onde vem

Análise de 07/10/2026, feita sobre o plano 4 (ultrassonografia e tomografia). Documento
de trabalho para a agente: explica a lógica das adições da equipe do Instituto de Saúde
Humanidade e Pesquisa (ISHP) e o que o pipeline precisa absorver. **Não é texto de plano.**

## Fontes

| fonte | o que é | onde |
|---|---|---|
| versão da equipe de 01/10/2026 | editada sobre a nossa v15 (Viviane De Marchi) | ramo `plano-04-ultrassom-tomografia`: `redacao_04/dados/terceiros_20261001.docx`, `_texto.md`, `_diff_v15.txt`, `_avaliacao.md` |
| v6 da equipe, 06/10/2026 | a nossa v19 passada para o formulário da SES ("Plano de Trabalho Simplificado — Modelo Parceria", Ofício 387/2026) | ramo do plano 4: `redacao_04/dados/PT_simplificado_exames_de_imagem_v6.docx` |
| pt_ses_01 e pt_ses_05 | os **dois** planos da ISHP aprovados pela SES-DF que estão no acervo (oftalmologia, "Visão Além do Alcance") | `normalizados/pt_ses_01/texto.md`, `normalizados/pt_ses_05/texto.md` |

As devolutivas de 05/09 e 20/09 são do professor, não da ISHP, e não entram aqui. A
`redacao_02/analise_aprovados.md` (31/08) mapeou só o pt_ses_01; o pt_ses_05 é a segunda
referência da casa.

Referências `pt_ses_05:N` apontam para a linha N de `normalizados/pt_ses_05/texto.md`.

---

## 1. As adições têm quatro origens

### 1.1 O modelo da casa — a equipe puxa o nosso texto para os planos que a SES já aprovou

| adição da equipe no plano 4 | de onde vem no aprovado da ISHP |
|---|---|
| Meta 2 em "vagas disponibilizadas à regulação"; o usuário chega já agendado pela regulação e o proponente só faz o contato | fluxo "oferta de vagas ao SISREG → regulação, priorização e agendamento pela SES → comparecimento → atendimento → desfecho" (pt_ses_05:1210) |
| "o projeto não atende demanda espontânea" (9.1 da v6) | "100% dos usuários [...] provenientes do SISREG [...] não sendo admitido atendimento fora do fluxo regulado" (pt_ses_05:1206) |
| a priorização é a do SISREG; o proponente não reclassifica (2.4) | a classificação de risco é da regulação — 12 menções nos dois aprovados |
| recepção confere identidade e autorização, sem triagem clínica (4.7) | "acolhido por equipe de apoio operacional para conferência da autorização regulatória [...] sem realização de triagem clínica" (pt_ses_05:223) |
| RQE para quem executa; responsável técnico médico por polo | execução "exclusivamente por médicos [...] com registro de qualificação de especialista" (pt_ses_05:238); coordenador e responsável técnico nomeado, com RQE anexo (pt_ses_05:260) |
| quadro da equipe assistencial com horas e critério (4.15) | 1.8 Dimensionamento das Equipes: tempo por atendimento × volume = carga médica (pt_ses_05:1701) |
| ordem de resposta aos riscos em cinco passos (7.7) | escada compensatória: remanejamento de quantitativos → ações compensatórias → instrumento de medição de resultados → devolução do não executado (pt_ses_05:2130) |
| absenteísmo e busca ativa (versão de 01/10, "até 26,4%") | "Gestão do Absenteísmo": taxa média mínima de 20% e "oferta de vagas em quantitativo superior à meta" (pt_ses_05:1284, 1290, 1327) |
| endereço e CNES de cada polo informados na formalização (4.2, 1.7) | "a validação definitiva dos pontos de atendimento está condicionada à verificação prévia [...] e à formalização junto à SES" (pt_ses_05:1947) |
| seção 9, Interface com os sistemas da SES-DF | 1.5 Sistemas de Registro e Monitoramento: sistema oficial obrigatório, sistema próprio só complementar (pt_ses_05:1403) |
| "Nota ao item 6.1.2" na planilha | justificativa por item da planilha, para afastar "duplicidade de despesa" (pt_ses_05:999–1001) |
| execução direta, sem subcontratação (4.14) | refrão em cada item: "responsabilidade direta da OSC [...] não implicando terceirização da gestão nem subcontratação do objeto" (pt_ses_05:1176, 1278, 1401) |
| "a curva é reavaliada com o resultado do mês 1" (7.2) | "não sendo adotados parâmetros fixos e engessados de produtividade diária" (pt_ses_05:1397) |

### 1.2 O formulário novo da SES (Ofício 387/2026, "Modelo Parceria")

Não são escolhas da ISHP — são respostas ao formulário: campos 1.1 a 1.8 (inclusive "O
Instituto enquadra-se como OSC, nos termos do MROSC?"), seção 5 Objetivos, 3.6
compatibilidade com a Portaria GM/MS 10.297/2026 (arts. 6º e 7º), nível de atenção,
instrumento a definir pela SUCONV, capa de "Pré-Plano". O vocabulário "OSC" é da SES: os
aprovados da ISHP já se chamavam "PLANO DE TRABALHO — CONVÊNIO" e traziam "DADOS E
INFORMAÇÕES DA OSC".

**Falta no repositório:** o Ofício 387/2026 e o formulário em branco. Sem eles não se
separa o que é campo do formulário do que a equipe acrescentou.

### 1.3 Experiência de operação em imagem

A ISHP opera centro de diagnóstico e de imagem (Casa de Saúde São Bento, tabela de
realizações da v6). Daí vêm o protocolo de contraste (termo de consentimento, estado
gestacional, carro de emergência com lista, SBV, SAMU, metformina 48 h, repouso sem tempo
mínimo), o laudo de ultrassonografia no mesmo ato, a RDC Anvisa 611/2022 em sete itens, as
24 h semanais do técnico em radiologia (Lei 7.394/1985), a retaguarda presencial e o
telelaudo só como contingência. Nada disso está nos aprovados, que são de oftalmologia — é
conhecimento de operação. O usuário aceitou quase tudo na v18 (02–03/10).

### 1.4 Instinto de proteção do executor

Tolerância de 10% compensada em três meses, "solicitação encerrada não conta como meta não
cumprida", validação da fila pelo proponente nos meses 1 e 2, campanhas de comunicação em
massa, I-07 "proposto pelo proponente". Saíram todos na v18 pela regra 9 do `PADRAO.md`.

**O ponto que importa:** o modelo aprovado da casa **já tem as formas de proteção que a
SES aceita** — escada compensatória com anuência da SES, oferta de vagas acima da meta,
produtividade como referência e não como parâmetro fixo, prazo de contingência
(pt_ses_05:1651). A agente oferece essas e barra as inventadas.

---

## 2. Como a equipe edita — o que mais pesa para o pipeline

- **Ela mantém um texto-mestre próprio e cola por cima do nosso.** O parágrafo do
  contraste da v6 é idêntico, palavra por palavra, ao da versão de 01/10
  (`terceiros_20261001_texto.md:283`), e desfez a correção da v19 (Res. CFM 2.147/2016 de
  volta — ela trata de diretor técnico, não de injeção de contraste). A frase da
  angiotomografia de coronárias, que entrou no retorno de 02/10, sumiu da 4.4 — e as
  coronárias estão dentro do 02.06.02.003-1.
- **A reversão acontece só nos trechos que a equipe escreveu.** As nossas correções em
  trechos nossos sobreviveram (I-07, frase da tomografia, "taxa de administração").
- **Ao trocar o esqueleto, as remissões são renumeradas à mão.** Três erros na v6:
  Meta 3 → 8.2 (era 9.2), R-15 → 8.3 (era 9.3), etapa 10 → 4.12 (era 4.11). Nenhuma das
  22 verificações do `conferir_plano.py` apanhou.

**Consequência:** todo retorno da equipe passa por diff em três vias — a última versão que
enviamos × a versão anterior da equipe × a nova — para separar acréscimo, reversão e
renumeração. E as remissões passam a ser conferidas.

---

## 3. Dados do proponente — cada um tem uma função

Não são divergências; a ficha guarda cada dado com a sua função:

| dado | função | fonte |
|---|---|---|
| CNPJ 17.517.805/0003-71 | filial de Brasília — **quem propõe** | v6 1.2 e 1.9; pt_ses_05 |
| CNPJ 17.517.805/0001-00 | matriz, Rio de Janeiro (Estatuto, art. 2º) | v6 1.9 |
| contato@institutosaudehumanidade.org.br | e-mail institucional (campo 1.5 do formulário) | v6 1.5 |
| direcao@ e presidencia@ | e-mails do representante legal; direcao@ também no rodapé institucional | pt_ses_05:27–29; pt_ses_01:28; rodapé da v6 |
| (21) 6447-1834 | telefone da matriz | v6 1.6 |
| celular do representante | contato direto do representante legal | pt_ses_05 (quadro da OSC) |
| representante | Diretor-Presidente; representa ativa e passivamente e assina (Estatuto art. 32, b e j); mandato de quatro anos (art. 29, § 1º) | v6 1.9 |
| Estatuto | AGE de 26/08/2025, registro de 03/09/2025, matrícula 287491 | v6 1.8 |
| tempo de atuação | calcular pela fundação (14/01/2013) na data do plano — não fixar "13 anos" | v6 3.10 |

O conteúdo institucional (histórico, estrutura, organograma, filosofia, realizações,
aptidão) entrou no corpo porque o **nosso** esqueleto pedia "4. Proponente — [preencher]".
Os aprovados da casa não trazem isso no corpo: marcam **"[x] Portfólio da OSC"** como anexo
(pt_ses_05:50; pt_ses_01:53). No formulário da SES, a equipe pôs em 3.7 a 3.12.

---

## 4. O que o modelo da casa tem e a v20 ainda não tem

Lacunas que a agente cobriria — não são perguntas ao usuário:

1. **RA por polo.** O pt_ses_05 lista as Regiões Administrativas de cada Região em cada
   polo (pt_ses_05:1901 em diante); a v20 só nomeia as Regiões. Com seis polos, ganha clareza.
2. **Contratação PJ não é subcontratação.** pt_ses_05:1842 — "ainda que contratados na
   modalidade de pessoa jurídica [...] não caracteriza subcontratação". A 4.14 da v20 diz
   "equipe própria", o que fica frágil se os radiologistas forem PJ.
3. **Nota técnica de regulação da especialidade.** pt_ses_05:290 cita a Nota Técnica da
   Regulação da Oftalmologia da SES (SEI 194347375). A v20 não cita documento de regulação
   de exames de imagem da SES.
4. **Produtividade como referência.** A 7.3 publica exames por dia e por sala sem a
   ressalva que o modelo da casa faz (pt_ses_05:376).
5. **Absenteísmo — divergência deliberada.** A casa declara 20% e oferta vagas acima da
   meta; a v20 não usa taxa e fixa vagas = exames (79.357), por decisão do usuário de
   02/10/2026. A agente registra como decisão, não como lacuna.

---

## 5. O que entra no pipeline

| # | peça | situação |
|---|---|---|
| 1 | `proponentes/ishp/ficha.yaml` — dados com função, fonte e data (tabela 3) | a montar |
| 2 | `proponentes/ishp/modelo.md` — os blocos da tabela 1.1, cada um com a linha do aprovado | a montar |
| 3 | `proponentes/ishp/blocos_imagem.md` — o conteúdo de 1.3 aceito na v18–v20, com a decisão | a montar |
| 4 | `PADRAO.md` — formas de proteção permitidas (1.4) e proibidas; portaria por tipo de emenda (bancada: 8.283/2025; a 10.297 só quando o ofício pedir); lista de citações erradas conhecidas, começando pela CFM 2.147/2016 | a montar |
| 5 | `proponentes/ishp/retornos.md` + verificação de remissões + diff em três vias (seção 2) | a montar |
| 6 | formulário da SES como segunda estrutura no `PADRAO.md`, com a verificação J seguindo a estrutura escolhida | depende do Ofício 387 e do formulário em branco |

**Recomendação:** quando o proponente for a ISHP, a agente parte do modelo da casa como
esqueleto; o `PADRAO.md` vale para números, régua e citações.
