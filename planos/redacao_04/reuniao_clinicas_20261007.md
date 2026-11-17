# Reunião com o dono das clínicas — ultrassom e tomografia

Preparada em 07/10/2026 sobre o plano v20 (06/10/2026, o texto que está com a equipe).
Uso interno: as partes marcadas **[interno]** não são para dizer na reunião.

---

## 0. Antes de tudo: o desenho que pode e o que não pode

**O que o plano já diz.** Na subseção 4.14: *"A execução assistencial não é
subcontratada. Ela ocorre nos polos do próprio proponente, por equipe própria."* Na
4.2: *"Os exames são realizados na capacidade instalada do proponente."*

**O que o decreto diz.** Decreto DF 48.727/2026, art. 33:

- é vedada a subcontratação total do objeto e a transferência da gestão ou da coordenação (caput);
- subcontratação é contratar terceiros para executar atividades relacionadas ao objeto (§ 1º);
- só se admite subcontratar **em parte, atividades acessórias**, e só se o plano prever (§ 2º);
- remunerar a equipe própria da entidade não é subcontratação (§ 4º).

E o art. 17, I, admite no valor do convênio a **locação de imóveis e equipamentos
destinados ao atendimento**.

**Consequência para a conversa.** A clínica **não** pode ser contratada para fazer
os exames e receber por exame. Isso seria subcontratar o próprio objeto, e o ISHP
ficaria só com a gestão, que é o quadro do risco R-16 (a gestão lida como taxa de
administração).

**O desenho que cabe** é o que o próprio ISHP já usou e teve aprovado nos dois planos
de oftalmologia (Visão Além do Alcance, `pt_ses_01` e `pt_ses_05`):

1. **locação** de espaço (e aqui também de equipamento), por polo e por período, com
   valor tirado de pesquisa de mercado;
2. **profissionais vinculados ao ISHP**, *"ainda que contratados na modalidade de pessoa
   jurídica"*. O aprovado diz que isso *"não caracteriza subcontratação do objeto nem
   transferência da execução assistencial"*;
3. agenda, laudo no TrakCare, registro da produção e coordenação **ficam com o ISHP**.

> Em uma frase: **o ISHP aluga tempo de sala e de equipamento da clínica e opera ali
> com a equipe dele. A clínica não vende exame ao ISHP.**

Essa é a minha leitura do decreto. Quem decide é o jurídico do ISHP e a SUCONV. Mas o
texto do plano já assumiu esse compromisso, e qualquer outro desenho obriga a mudar o
plano.

**Zona cinzenta, para levar ao jurídico se aparecer:**
- se ele exigir que o **técnico dele** opere o tomógrafo, a locação passa a incluir quem
  realiza o exame (4.9: *"A tomografia computadorizada é realizada por técnico em
  radiologia"*). Isso se aproxima de subcontratação. A saída dos aprovados é o técnico
  ser contratado pelo ISHP, mesmo que seja a mesma pessoa;
- se os médicos forem contratados **pela PJ da clínica** e não pela PJ de cada médico,
  quem executa é a clínica.

---

## 1. Abertura — o que dizer no primeiro minuto

> "O ISHP vai executar, com recurso de emenda da bancada do DF repassado pela
> Secretaria de Saúde, cerca de 79 mil exames de ultrassom e tomografia em 12 meses,
> para pacientes que estão na fila da regulação do DF. Hoje a espera média do ultrassom
> passa de um ano e meio. O paciente vem pela regulação da Secretaria: a gente abre a
> agenda e a regulação preenche. Não é credenciamento no SUS. A clínica não fatura
> nada no SUS. O que buscamos é **alugar horário de sala e de equipamento** nas suas
> unidades, para a nossa equipe operar, e eventualmente contratar profissionais que
> já trabalham com vocês."

**Traduções para não se perder no jargão:**

| em vez de | diga |
|---|---|
| convênio / emenda de bancada | recurso federal destinado pelos parlamentares do DF, repassado pela SES ao ISHP |
| regulação / SISREG | a Secretaria manda o paciente; a gente não capta paciente |
| unidade de aferição | o exame só conta quando o laudo está lançado no sistema da Secretaria (TrakCare) |
| capacidade instalada | salas, aparelhos e horários disponíveis |
| prestação de contas | toda despesa precisa de contrato, nota fiscal e pagamento pela conta do convênio |

---

## 2. Números para levar

### O projeto

| item | valor | fonte no plano |
|---|---|---|
| fila na extração de 10/09/2026 | 78.572 pedidos (65.120 US · 13.452 TC) | 3.1 |
| espera média | ultrassom 561 dias · tomografia 141 dias | 3.1 (Mapa Social, 15/09/2026) |
| novos pedidos que seguem sem agenda | cerca de 4.346 por mês em 2026 | 3.1 |
| exames do projeto | **79.357** (65.676 US · 13.681 TC) | 2.2 |
| prazo | 12 meses, produção a partir do mês 1 | 7.1 |
| recurso | R$ 11.592.762,00, pago pelo Ministério da Saúde ao Fundo de Saúde do DF em 05/03/2026 | 1.9; `estado.yaml` |
| funcionamento | 10 horas por dia útil, segunda a sexta, 252 dias úteis | 7.3 |
| ritmo de pico | 315 exames por dia útil no conjunto | 7.3 |

**Os exames, pelo que pedem do equipamento:**

| exame | quantidade | o que exige |
|---|---|---|
| US mamária bilateral | 14.719 | transdutor linear |
| US doppler colorido de vasos (MMII e carótidas) | 14.547 | doppler colorido |
| US abdômen total | 13.198 | convexo |
| US transvaginal | 10.563 | transdutor endocavitário; acompanhante |
| US aparelho urinário · tireoide · próstata · abdômen superior | 3.953 · 3.224 · 3.207 · 2.265 | linear (tireoide); convexo |
| TC tórax | 5.258 | **inclui 1.413 angiotomografias de coronárias** |
| TC abdômen superior · pelve | 4.540 · 3.883 | |
| TC com contraste iodado | 12.953 das 13.681 | bomba injetora; enfermagem; carro de emergência |

A angiotomografia de coronárias chega pela regulação com o código de TC de tórax e é
paga como TC de tórax (R$ 300,10). Em geral ela exige tomógrafo de 64 canais ou mais
com sincronização ao ECG. **Confirmar com o radiologista e perguntar se o tomógrafo
dele faz.**

### Por polo — o que precisaríamos da clínica em cada região

| polo (Região) | US/mês | TC/mês | horas de sala US por dia útil | horas de tomógrafo por dia útil | salas US no plano | tomógrafo |
|---|---|---|---|---|---|---|
| Ceilândia (Oeste) | 296 | 89 | 5,2 | 1,4 | 1 | 1 |
| Taguatinga (Sudoeste) | 1.833 | 408 | 31,5 | 6,4 | 4 | 1 |
| Sobradinho (Norte e Leste) | 1.305 | 284 | 23,3 | 4,4 | 3 | 1 |
| Plano Piloto (Central) | 267 | 128 | 5,0 | 2,0 | 1 | 1 |
| Gama (Sul) | 1.207 | 156 | 21,9 | 2,4 | 3 | 1 |
| Guará (Centro-Sul) | 568 | 79 | 9,5 | 1,2 | 2 | 1 |
| **total** | **5.476** | **1.144** | | | **14** | **6** |

**O argumento comercial está na coluna do tomógrafo.** Fora Taguatinga e Sobradinho,
o projeto usa o tomógrafo **1 a 2,5 horas por dia**. Não queremos o equipamento dele
o dia inteiro, só uma faixa de horário. A carga total é 1,79 tomógrafo; o plano mantém
seis só para que o exame fique perto da casa do paciente.

As horas vêm de tempos de sala que ainda não têm fonte (US 20 min, doppler 30 min,
TC 20 min com contraste e 15 min sem contraste — `dados/capacidade.md`). O tempo real
da clínica corrige essas horas.

### Dinheiro

- **Valor por exame pago pelo convênio ao ISHP** (é público, Portaria SAES/MS
  4.282/2026): ultrassom R$ 99,94 (doppler e abdômen total R$ 100,18); tomografia
  R$ 299,44 (tórax R$ 300,10). Se ele perguntar, explique que esse valor **paga o
  exame inteiro**: médico, técnico, enfermagem, contraste, laudo, registro e estrutura.
  Não é o valor que vai para a clínica.
- **Como o dinheiro anda:** quatro parcelas trimestrais de cerca de R$ 2,9 milhões. A
  primeira sai na celebração e as demais no início de cada trimestre, então **o ISHP
  recebe antes de produzir** e consegue pagar a locação em dia. A produção que faltar
  num trimestre é descontada da parcela seguinte (7.6).
- Todo pagamento sai da **conta específica do convênio**, com contrato e nota fiscal
  (art. 19 e 28 do decreto). A SES pode **visitar a clínica** em fiscalização (art. 24).

**[interno] Teto da negociação.** Com os tempos acima, cada hora de sala de US produz
cerca de **R$ 270** de receita para o convênio e cada hora de tomógrafo cerca de
**R$ 911** (Meta 4 ÷ 24.317 h; Meta 5 ÷ 4.500 h). Dessa receita saem o médico, o técnico,
a enfermagem, o contraste (cerca de R$ 60 por exame na referência da tabela, em 12.953
exames) **e** a locação. O preço da hora que ele pedir precisa caber nisso com folga.
A infraestrutura fica dentro do valor unitário porque a margem de gestão é de 7,96%
(memória "a margem decide onde a infraestrutura aparece"). Não existe rubrica separada
de locação para empurrar o custo.

**[interno] Receita aproximada por polo** (unitário médio, R$ 100,04 US e R$ 299,69 TC):
Ceilândia R$ 673 mil · Taguatinga R$ 3,67 mi · Sobradinho R$ 2,58 mi · Plano Piloto
R$ 777 mil · Gama R$ 2,01 mi · Guará R$ 963 mil, no ano.

---

## 3. O que a unidade da clínica precisa ter

O plano (4.8, 4.9 e 4.16) já promete isto, e tudo será exigido **na formalização**:

- [ ] CNES do estabelecimento e **licença sanitária** vigente
- [ ] responsável técnico médico e **supervisor de proteção radiológica** (RDC Anvisa 611/2022)
- [ ] plano de proteção radiológica; **testes de constância** e controle de qualidade do tomógrafo, com laudos
- [ ] **contrato de manutenção preventiva** dos aparelhos, com tempo de resposta
- [ ] especificação dos equipamentos: canais do tomógrafo; transdutores linear e endocavitário; doppler colorido
- [ ] sistema de imagem (PACS) que guarde as imagens para o laudo e para consulta
- [ ] carro de emergência, oxigênio e medicamentos para reação a contraste, durante todo o horário
- [ ] espaço de repouso depois do contraste; desinfecção do transdutor endocavitário; acompanhante no transvaginal e na próstata
- [ ] médicos de US com **RQE em ultrassonografia**; radiologista com RQE para a TC

---

## 4. Perguntas para fazer (fecham a pendência L-006, parque não confirmado)

1. **Em que regiões ficam as unidades?** O plano tem seis polos: Ceilândia,
   Taguatinga, Sobradinho, Plano Piloto, Gama e Guará.
2. Quantas salas de ultrassom em cada unidade, e com quais transdutores? Tem doppler colorido?
3. Tomógrafo: quantos canais? Tem bomba injetora? Faz angiotomografia de coronárias?
4. **Quais horários ficam ociosos** (dias e turnos) em cada unidade?
5. **Quanto tempo de sala vocês usam por exame**: US simples, doppler, TC com e sem contraste?
6. Ele prefere cobrar **por hora, por turno ou por mês**? O que entra no preço (limpeza, energia, manutenção, insumos)?
7. Os médicos e técnicos dele aceitariam ser contratados **diretamente pelo ISHP** (CLT ou PJ do próprio profissional)?
8. A clínica tem PACS que o radiologista do ISHP possa acessar? Faz telelaudo?
9. Já atende SUS ou tem algum contrato com a SES-DF? Isso pode gerar conflito de agenda ou de interesse.

---

## 5. O que **não** dizer nem prometer

- **"Vamos contratar seus exames" / "pagar por exame à clínica" / "credenciar"**.
  Isso é o desenho vedado da seção 0.
- **"O ISHP fica com 8%"** ou **"taxa de administração"**. A gestão é paga posto a
  posto (coordenação, assistentes, operadores, prestação de contas), não como percentual.
- **Data de início.** Ela depende da análise da SES (SUCONV) e da celebração do instrumento.
- **Exclusividade ou contrato fechado.** O ISHP precisa escolher o fornecedor por
  procedimento análogo à licitação, com os princípios de impessoalidade e economicidade
  (IN CGDF 01/2005, art. 25, parágrafo único). A proposta dele entra como uma das
  cotações da pesquisa de mercado.
- **Volume garantido.** O paciente vem da regulação. A meta pode migrar entre exames
  por termo aditivo (2.2), e a parcela é ajustada pela produção (7.6). O contrato de
  locação deve acompanhar isso, com horas ajustáveis e prazo atrelado à vigência.
- **"A clínica escolhe ou indica paciente".** Não escolhe nem indica. O plano diz que a
  parceria não capta demanda própria (4.4).

---

## 6. O que sair da reunião com

- [ ] **proposta comercial por escrito**: preço da hora ou do turno de sala de US e de
      tomógrafo, por unidade, dizendo o que está incluso. Ela serve de cotação.
- [ ] **declaração de disponibilidade**: unidades, salas, equipamentos e horários. Ela
      sustenta a Meta 1 e a 4.16, alínea (f).
- [ ] cópias de CNES, licença sanitária, especificação dos equipamentos e laudos de testes de constância
- [ ] os tempos de sala por exame que a clínica pratica

---

## 7. Depois da reunião — o que pode mudar no plano

- **Se as unidades não coincidirem com os seis polos**, o rateio, as salas e as
  equipes se refazem com `calculo_v20/` (3.4, 4.2, 4.13, 4.15, 7.3). Mudar o plano
  depois de aprovado exige aprovação prévia da SES e, quando exigível, anuência do autor
  da emenda (decreto, art. 14).
- **Se o desenho for locação**, o plano precisa dizer que a estrutura dos polos,
  própria ou locada, é remunerada dentro do valor unitário. O art. 16 pede o custo
  acessório expressamente previsto no plano. Hoje a 4.2 fala só em "capacidade instalada
  do proponente". A 4.14 continua de pé.
- **Tempos de sala reais** da clínica substituem as quatro premissas de `dados/capacidade.md`.
- **[interno] CNES — pergunta em aberto para o faturamento e o jurídico:** em que
  estabelecimento o exame é registrado na APAC, se a sala e o equipamento estão
  cadastrados no CNES da clínica? Resolver antes de assinar a locação.
