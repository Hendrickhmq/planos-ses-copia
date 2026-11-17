# Fonte externa — Manual OCI Cardiologia (SES Sorocaba)

Análise em 2026-08-17. Fonte nova confrontada com o corpus, com o plano em
redação e com a norma federal lida no original.

**O que é.** Manual operacional municipal publicado no BookStack da SES de
Sorocaba (`estante-ses.sorocaba.sp.gov.br`), competência 12/2025, descrevendo
como a Policlínica opera a **OCI 09.02.01.002-6 — Avaliação Cardiológica** no
sistema SIS Sorocaba. É a primeira fonte **operacional** que este projeto tem
sobre o mesmo procedimento do plano em redação.

**Material local:**

| item | onde |
|---|---|
| manual limpo | [`fontes/sorocaba/manual_oci_cardiologia.md`](fontes/sorocaba/manual_oci_cardiologia.md) |
| 37 imagens de tela | `fontes/sorocaba/img/` — duas (`5veimage`, `sb4image`) com o paciente tarjado |
| 4 anexos de teste do município | **fora do repositório** (nome, CPF e CNS de pacientes): `~/Downloads/02-Saude-SUS/OCI-Cardiologia/oci-cardiologia-anexos/` |
| termo de referência de credenciamento de OCI do PMAE (Senhor do Bonfim/BA, PNCP), lido junto com esta fonte | [`fontes/tr_credenciamento_oci_pmae_senhor_do_bonfim_ba.pdf`](fontes/tr_credenciamento_oci_pmae_senhor_do_bonfim_ba.pdf) |
| Portaria SAES/MS 2.331/2024 | `normas/` — **baixada e lida nesta sessão** |
| Portaria SAES/MS 2.930/2025 | `normas/` — **baixada e lida nesta sessão** |
| Portaria SAES/MS 1.822/2024 | raiz do projeto (NM-005) — **lida no original nesta sessão** |

Isso encerra, para três normas, a ressalva do `estado.yaml`: "NENHUMA foi lida no
original nesta sessão".

> **Atualizado.** Uma varredura posterior sobre 16 documentos primários (portarias
> do PMAE, três notas técnicas do DAET e o Manual PMAE do Ministério) confirmou e
> refinou o que está aqui. As regras consolidadas estão em
> [`regras_oci_cardiologia.md`](regras_oci_cardiologia.md); este arquivo trata da
> fonte de Sorocaba.

---

## 1. A régua federal — ficha real da 09.02.01.002-6

Lido no Anexo I da Portaria SAES/MS nº 1.822/2024:

| atributo | valor |
|---|---|
| Descrição | consulta médica especializada, **ecocardiograma**, eletrocardiograma, radiografia de tórax, exames laboratoriais específicos, consulta ou teleconsulta de retorno |
| Instrumento de registro | APAC (procedimento principal) |
| Financiamento | **FAEC** |
| Valor SA | **R$ 200,00** |
| CID-10 | **Sem CID específico** |
| Categoria CBO | 2231 Médicos · 2251 Médicos Clínicos · 2252 Especialidades Cirúrgicas · 2253 Medicina Diagnóstica e Terapêutica |
| Quantidade máxima | 1 |
| Atributos | 009 exige CPF/CNS · 053 PMAE · **054 APAC com validade fixa de 2 competências** |
| Regras condicionadas | **0009 condiciona aos secundários a terem valor zerado** · 0011 condiciona o registro de procedimentos secundários na APAC |
| Habilitação | **38.01 Programa Mais Acesso a Especialistas** |
| Idade mínima | 0 mês na 1.822 — **alterada para 18 anos** pela 2.331/2024, Anexo III |

**Cadeia normativa completa** (todas citadas nos "considerandos" das portarias
lidas — candidatas a NM-008 em diante):

```
GM/MS 1.604/2023   PNAES
GM/MS 3.492/2024   institui o PMAE          ← alterada por GM/MS 5.758/2024
SAES/MS 1.640/2024 operacionalização        ← alterada por SAES/MS 1.976/2024
SAES/MS 1.821/2024 Grupo 09, atributos e regras condicionadas
SAES/MS 1.822/2024 OCI Cardiologia — inclui os procedimentos na Tabela  (NM-005)
SAES/MS 2.331/2024 procedimentos OBRIGATÓRIOS por OCI; idade mínima 18
SAES/MS 2.930/2025 exclui a radiografia de tórax da obrigatoriedade na 002-6
```

Nota de precisão para a Seção 1: o plano escreve que a OCI foi "instituída pela
Portaria SAES/MS nº 1.822/2024". A 1.822 **inclui o procedimento na Tabela**;
quem institui o PMAE é a GM/MS 3.492/2024. E a portaria grafa "Ofertas de
**Cuidados** Integrados", no plural.

---

## 2. O achado central: o piso legal é muito menor que o pacote

A descrição do SIGTAP lista seis componentes. Ela é **finalidade**, não
obrigação. O que é exigível:

- **Art. 7º da 2.331/2024** — no mínimo **2** procedimentos secundários na APAC
  de OCI, sendo um deles obrigatoriamente `03.01.01.007-2 CONSULTA MÉDICA EM
  ATENÇÃO ESPECIALIZADA` **ou** `03.01.01.030-7 TELECONSULTA`.
- **Anexo V da 2.331/2024** — para a 002-6, secundário obrigatório
  `02.11.02.003-6 ELETROCARDIOGRAMA` e `02.04.03.015-3 RADIOGRAFIA DE TÓRAX`.
- **Art. 1º da 2.930/2025** — **exclui a radiografia de tórax** dessa lista.

Piso obrigatório hoje, portanto:

```
ECG  +  1 consulta médica (ou teleconsulta)     = R$ 200,00 pagos
```

**Ecocardiograma, radiografia, laboratório e consulta de retorno são
compatíveis, não obrigatórios.** O Anexo III da 1.822 permite consulta e
teleconsulta na quantidade **2** — o que torna o retorno *possível*, nunca
*devido*. E a regra 0009 zera o valor de todos os secundários: não há qualquer
pressão financeira para executá-los.

**Consequência dura para o plano.** A fila que sustenta a meta foi extraída com
filtro de **solicitação de ecocardiografia** — 36.052 CNS, 777 dias de espera. O
ecocardiograma é a razão clínica inteira do objeto, e é justamente o item que a
norma federal **não** exige. Um executor pode entregar consulta + ECG, faturar
os R$ 200,00 com APAC regular, e a fila continua esperando o eco.

Isso desloca o ônus: **o pacote completo não é garantido pela tabela federal,
tem que ser garantido pelo plano de trabalho.** As decisões já tomadas — "OCI
concluída = fluxo completo até a consulta de retorno" (DV-002) e "não existe
meia OCI" (DV-013) — estão corretas, mas são **compromissos pactuados**, não
decorrência da portaria. O plano não pode citar a norma como fundamento delas.

E Sorocaba é a prova empírica de que o piso é o que se pratica: um município
real executando esta OCI como consulta + ECG, sem eco, sem laboratório e sem
retorno.

**O Ministério diz isso com todas as letras.** NT 1/2025-DAET, item 2.1.6: "Não
há possibilidade de alterar/variar os valores das OCIs para faturamento, ainda
que nem todos os procedimentos sejam executados". Não é brecha — é desenho
declarado do PMAE. E a mesma nota classifica a ecocardiografia transtorácica e os
exames laboratoriais como **opcionais** para a 002-6.

---

## 3. Compatibilidade — o que a fonte nova confirma

| item do plano | situação |
|---|---|
| Composição da OCI transcrita na Seção 1 | **idêntica** à descrição do SIGTAP. Transcrição correta |
| R$ 200,00 | confirmado na 1.822 |
| Registro por APAC no SIA/SUS | confirmado (art. 2º da 1.822) e observado na prática em Sorocaba |
| Financiamento FAEC | confirmado — mantém viva a LC-012 |
| 09.02.01.004-2 é outro procedimento | **confirmado**: é "OCI Progressão da Avaliação Diagnóstica I — Síndrome Coronariana Crônica". AC-017 estava certo, o pt_ses_04 rotulou errado |
| "Não existe meia OCI" (DV-013) | ganha lastro normativo: regra **0009**, secundários com valor zerado |
| "Pacote fechado — nenhum item reaparece como rubrica na Seção 5" | mesma regra 0009 sustenta |
| Ciclo de 30 dias (DV-011) | ganha teto normativo: atributo **054**, APAC com validade fixa de **2 competências** |
| Curva mensal (entradas nos meses 2–8, conclusões 3–9) | compatível com o 054 — defasagem de 1 mês cabe em 2 competências |

---

## 4. O que a norma exige e o plano ainda não tem

1. **Habilitação 38.01 — PMAE.** O procedimento só é faturável em estabelecimento
   habilitado. Sem isso os 3 polos não produzem. Hoje está em
   `melhorias.md:163` ("etapa preliminar de habilitação do CNES e programação da
   FPO"); pertence ao **mínimo viável**, na Meta 3 / Etapa 0, e é candidato a
   lacuna bloqueante — a 1ª parcela se vincula à Meta 3.

2. **Idade mínima 18 anos.** A fila de 36.052 CNS precisa ser refiltrada. Se
   houver menores no estoque, a meta cai. Lacuna nova.

3. **Validade fixa de 2 competências.** Não é só o ciclo de 30 dias: é uma
   janela **por competência**, não uma contagem de dias. Entrada no dia 28
   consome quase toda a primeira competência. Entra na Seção 2 e na Seção 7.

4. **Registro obrigatório de secundários (art. 7º + Anexo V).** A conciliação da
   Seção 8 não é contar APAC — é conferir se cada APAC traz ECG e consulta. É o
   que separa OCI executada de OCI declarada.

5. **Autorização prévia da APAC.** Em Sorocaba há um passo de autorização
   (CREDAC) entre o atendimento e o número da APAC, com trâmite físico. O
   análogo no DF precisa entrar no cronograma — hoje a Seção 6 assume competência
   do SIA sem o lag da autorização.

6. **CBO por categoria de 4 dígitos.** A norma admite 2231/2251/2252/2253 — não
   exige cardiologista. Alivia a Seção 9 no dimensionamento, mas é decisão
   clínica antes de ser administrativa: convém pactuar o cardiologista mesmo
   sendo mais largo o permitido.

7. **Sem CID específico.** Nenhuma restrição federal de CID no principal — a
   fila por ecocardiografia não sofre corte. Mas ver o item 5 abaixo: Sorocaba
   impôs restrição local, e a SES-DF pode fazer o mesmo. Vale confirmar com o
   Complexo Regulador antes de fechar a Seção 2.

---

## 5. Onde Sorocaba diverge da norma federal

| tema | manual de Sorocaba | norma federal |
|---|---|---|
| Nome | "**Operação** de Cuidado Integrado" | "**Oferta** de Cuidados Integrados" |
| CID | só **Z13.6, Z84.8, Z48** | **sem CID específico** — restrição é local, não federal |
| CBO | só **225120** cardiologista | categorias 2231/2251/2252/2253 |
| Secundários | "pelo menos **um** entre consulta e ECG" | **no mínimo 2**, sendo um deles consulta ou teleconsulta (art. 7º), **e** o ECG é obrigatório (Anexo V) |
| Composição | consulta + ECG | seis componentes na descrição; piso de consulta + ECG |
| Retorno | não existe no manual | previsto (consulta/teleconsulta qtd 2), não obrigatório |
| Base citada | "Portaria SAES/MS nº 2.331/2024" | correta, mas **desatualizada**: a 2.930/2025 alterou o Anexo V |
| Habilitação 38.01 | não menciona | exigida |
| Validade de 2 competências | não menciona | atributo 054 |

O resultado prático de Sorocaba (consulta + ECG) **atende** ao piso do art. 7º.
A regra que eles escreveram ("pelo menos um") **não** — uma APAC só com ECG,
seguindo o manual ao pé da letra, é irregular.

**Ressalva importante, apurada depois.** As restrições de CID e de CBO não
contrariam a norma federal: o **art. 21, §2º da Portaria SAES/MS 1.640/2024** dá
ao gestor local autonomia para definir autorizações prévias, regras de bloqueio
de produção e aprovação da produção. Sorocaba está exercendo uma competência que
tem. O que permanece divergente é a regra de secundários ("pelo menos um") e a
ausência de retorno, habilitação e validade de 2 competências no manual.

Para o plano, a leitura muda de sinal: se o gestor local pode restringir, **a
SES-DF também pode** — e uma restrição de CID recortaria a fila elegível.

---

## 6. Contradições internas do manual — com prova nos próprios anexos

Os quatro anexos do capítulo "Fluxo Administrativo" foram baixados e lidos. Eles
contradizem o texto que os cita.

O manual afirma que o teste de homologação foi feito com "**Procedimento único
lançado: 0902010026**" e "**Exclusão de qualquer outro procedimento BPA**".

| anexo | o que mostra |
|---|---|
| `32724812 TESTE SOAP OCI 01` | 17/11/2025 · CID **R69** · profissional **médico gastroenterologista** · procedimento: só a OCI |
| `32724854 TESTE SOAP OCI 02` | 24/11/2025 · CID **I10** · médico cardiologista · procedimentos: **ELETROCARDIOGRAMA + OCI** |

Ou seja: **nenhum dos dois testes usou os 3 CIDs que o manual declara
obrigatórios**; um foi feito por especialidade fora da regra de CBO do próprio
manual; e o segundo lançou dois procedimentos, não um.

**O que o BPA de fato prova.** Parsei `BPA TESTE OCI PA355220.NOV` (layout SIA,
31 linhas). Nenhum dos dois CNS de teste (`700600438874667`, `700001171103403`)
aparece no arquivo. A conclusão do manual está certa — mas o achado é mais forte
e diferente do que ele diz:

> o atendimento não foi ao BPA **mesmo com o ECG lançado junto**.

Isto é: a instrução "exclua todos os procedimentos" **não foi o que se testou**,
e o comportamento observado sugere que o sistema suprime o atendimento inteiro
do BPA quando a OCI está presente. O risco espelhado: qualquer procedimento BPA
legítimo lançado no mesmo atendimento some silenciosamente do faturamento.

**Um achado que o manual não discute.** O procedimento da enfermagem
`03.01.04.007-9` (preparação para ECG) **vai** ao BPA — linhas de 12/11/2025,
CBO 322205, no mesmo arquivo. Como a Escuta Inicial é atendimento separado, ela
não é suprimida. O episódio assistencial gera **BPA (enfermagem) + APAC
(médico)**.

A régua federal existe e é do Manual PMAE (p. 26): atendimentos que geraram
secundários na APAC de OCI "não deverão ser registrados em duplicidade em
qualquer outro instrumento de registro do SIA ou do SIH", e o MS mantém indicador
de duplicidade entre APAC, BPA-I e AIH por CNS/CPF. O preparo para ECG não é
secundário da OCI, então não é duplicidade automática — mas é o ponto exato onde
ela apareceria, e nenhuma linha do manual de Sorocaba trata disso.

**Controle frágil que interessa à Seção 8.** Os secundários da APAC são
digitados à mão pela equipe administrativa — o manual diz textualmente que "o
sistema não os insere automaticamente". A APAC, portanto, **não é prova de que o
eco ou o retorno aconteceram**: é prova de que alguém os digitou. Para a
prestação de contas, isso significa que conciliar APAC contra despesa não basta;
é preciso lastro no prontuário.

**Outras inconsistências de redação:** capítulo 1 desatualizado ("código pendente
de inserção", quando o código já está em uso); ícone chamado "Passou pela escuta"
no capítulo 1 e "Escuta Inicial realizada" no restante; "Gestão da Unidade" no
texto e "Coordenação" na tabela; CID grafado ora `Z136` ora `Z13.6`.

---

## 7. O que fazer, por seção

| seção | ação |
|---|---|
| 1 — Objeto | corrigir a atribuição normativa (1.822 inclui na Tabela; 3.492/2024 institui o PMAE); grafar "Ofertas de Cuidados Integrados" |
| 1 e 2 | **declarar que o pacote completo é compromisso pactuado**, acima do piso federal de consulta + ECG. É o ponto que dá sentido ao valor e protege a fila |
| 2 — Metas | refiltrar a fila por **idade ≥ 18**; reler a janela do ciclo como **2 competências**, não 30 dias corridos |
| 3 — Indicadores | criar indicadores de integralidade: % de OCI com **ecocardiograma** registrado na APAC e % com **retorno** registrado. Sem eles nada distingue o pacote pactuado do piso legal |
| 4 — Etapas | habilitação **38.01** no CNES dos 3 polos como etapa anterior à produção |
| 6 — Desembolso | incluir o lag de autorização da APAC entre atendimento e competência faturada |
| 8 — Prestação de contas | conciliação por composição da APAC (secundários), não só por contagem; lastro no prontuário, porque o secundário é digitado à mão |
| 9 — Equipe | CBO admitido é mais largo que "cardiologista" — decidir e justificar |
| 11 — Riscos | risco de execução do piso legal em lugar do pacote pactuado, com Sorocaba como caso observado |

**Lacunas novas propostas:** idade mínima 18 e o refiltro da fila; habilitação
38.01 nos polos; regra local de CID na SES-DF (existe? o Complexo Regulador
impõe?); prazo de autorização da APAC no DF.

---

## 8. Limites desta análise

- A restrição de CID de Sorocaba pode vir de norma local ou de orientação da
  CREDAC. Não foi localizada em nenhuma das três portarias federais lidas.
- Varri a cadeia normativa até a **2.930/2025**. Não fiz varredura exaustiva de
  portarias de 2025–2026: pode haver alteração posterior. O valor de R$ 200,00
  na competência 04/2026 vem da conferência do SIGTAP já registrada no plano.
- O parse do BPA usou o layout padrão do SIA. Procedimentos, CBOs e datas
  conferem com códigos SIGTAP válidos; os campos de CID e quantidade ficaram
  desalinhados e não foram usados como prova.
- As duas portarias novas estão em `normas/` mas **não foram cadastradas** em
  `acervo.csv` — proponho NM-008 (2.331/2024) e NM-009 (2.930/2025), e mudar
  NM-005 de `a_verificar` para lida no original.
