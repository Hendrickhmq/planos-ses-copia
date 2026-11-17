# Como a OCI de cardiologia é paga e como ela muda

**Estudo interno, para entender o objeto.** Não vai ao documento. Montado em 22/10/2026 com
as fichas do SIGTAP da competência 10/2026 (`../dados/fontes/sigtap_09020100*_102026.md`) e as
regras lidas em agosto (`planos/redacao/regras_oci_cardiologia.md`).

## 1. O que é uma OCI

A **Oferta de Cuidados Integrados** é um **pacote**. A SES paga um valor fixo por paciente que
completa um cuidado, e não cada exame em separado. O registro é uma APAC: o procedimento
principal é a OCI, e os exames e consultas feitos entram como secundários, com valor zero.

Dentro do pacote há dois tipos de item:
- **obrigatório:** sem ele a OCI não fecha (na 002-6, o eletrocardiograma);
- **compatível:** pode entrar, se o médico indicar (na 002-6, o ecocardiograma e os exames de
  laboratório).

Três regras mudam tudo na conta:
- **O mínimo da APAC:** pelo menos dois secundários, e um deles é consulta ou teleconsulta
  (SAES 2.331/2024, art. 7º).
- **O valor não varia com o que se fez.** A Nota Técnica 1/2025 do Ministério diz que o valor
  da OCI não muda para o faturamento, mesmo que nem todos os itens sejam feitos (item 2.1.6). O
  item 2.1.5 aceita que um exame não seja feito por já ter sido feito antes ou por falta de
  indicação.
- **O CID decide quem entra.** Cada OCI aceita só os pacientes com os CID da ficha. É por isso
  que a fila de cada OCI se mede pelo CID (`metodo/coleta/mapa_social.md`).

## 2. As sete, lado a lado

| OCI | valor do pacote | obrigatórios | soma avulsa no SIGTAP* | pacote ÷ avulso | CID | o IEV executa? |
|---|---:|---|---:|---:|---|---|
| 001-8 Risco Cirúrgico | R$ 130,00 | eletrocardiograma | R$ 72,27 | 1,8 | Z13.6, Z84.8 | **sim**, 4.647 |
| 002-6 Avaliação Cardiológica | R$ 200,00 | eletrocardiograma | R$ 130,63 | 1,5 | Z13.6, Z84.8 | não |
| 003-4 Síndrome Coronariana Crônica, inicial | R$ 270,00 | eletrocardiograma e teste ergométrico | R$ 160,63 | 1,7 | I00 a I99 | não |
| 004-2 Síndrome Coronariana, progressão I | R$ 250,00 | eco de estresse | R$ 175,00 | 1,4 | I20 a I25 | **sim**, 900 |
| 005-0 Síndrome Coronariana, progressão II | R$ 1.879,80 | as duas cintilografias (estresse e repouso) | R$ 801,59 | 2,3 | I20 a I25 | não |
| 006-9 Insuficiência Cardíaca | R$ 350,00 | eletrocardiograma, teste ergométrico, Holter e BNP | R$ 217,63 | 1,6 | I00 a I99 | **sim**, 1.000 |
| 007-7 Gestão do Pré-operatório | R$ 130,00 | nenhum | R$ 80,77 | 1,6 | Z01.8, Z48.8, Z48.9 | não |

\* O que somariam, pela tabela do SUS, todos os itens que cabem na OCI comprados um a um, com
as consultas contadas uma vez por encontro. Os valores avulsos são os da ficha de cada
componente.

O que a tabela mostra:
- **O pacote paga de 1,4 a 2,3 vezes a tabela dos itens.** A OCI foi desenhada para isso: é o
  incentivo do programa.
- **O mínimo custa pouco.** Na 002-6, consulta mais eletrocardiograma somam R$ 15,15 na
  tabela, e a OCI paga R$ 200,00. O ecocardiograma é compatível: só entra se o médico indicar.
- **Seis das sete são de adulto** (18 a 130 anos). A 007-7 vai de 0 a 130.
- **Todas pedem médico** (CBO das famílias 2231 a 2253). A 001-8, desde 06/2025, só aceita
  cardiologista (CBO 225120).

## 3. Quando a OCI "paga bem"

A tabela do SUS não é o custo. **O custo é o mercado**: quanto custa, no DF, a consulta com
cardiologista, o ecocardiograma, o eco de estresse, a cintilografia e o Holter. Por isso, se a
OCI paga bem depende de duas coisas:
1. **O exame caro é obrigatório ou opcional?**
   - Na 004-2, o eco de estresse é obrigatório, e o pacote é R$ 250,00.
   - Na 002-6, o eco é opcional: se metade dos pacientes precisar, o custo médio cai.
2. **Quanto o exame caro custa no mercado do DF.**

O dossiê mede isso pela **cobertura**: o valor da OCI dividido pelo menor preço de mercado do
pacote. A pesquisa de preços está em `../dados/precos.md` (agente `precos`, em andamento em
22/10/2026), e a comparação em `../dossie/comparativo.md`.

## 4. Como a OCI muda

**Quem muda é o Ministério, por portaria da SAES/MS**, com vigência numa competência (o mês da
tabela). O histórico de cada ficha diz o que mudou. Nas sete de cardiologia:

| quando | portaria | o que mudou |
|---|---|---|
| 07/2024 | SAES 1.822/2024 | cria as OCI de cardiologia |
| 01/2025 | SAES 2.331/2024 | idade mínima 18 anos; define os obrigatórios; a 005-0 vai a R$ 840,00 |
| 02/2025 | SAES 2.630/2025 | tira os compatíveis repetidos |
| 04/2025 | SAES 2.723/2025 | passa a exigir o CPF do paciente |
| 07/2025 | SAES 2.930/2025 | a radiografia de tórax sai da 002-6 |
| 09/2025 | SAES 3.199 e 3.200/2025 | as habilitações do Agora Tem Especialistas |
| 04/2026 | SAES 3.958/2026 | a APAC deixa de ter validade fixa de 2 competências |
| 06/2026 | SAES 4.104/2026 | cria a 007-7, Gestão do Pré-operatório |
| 09/2026 | SAES 4.795/2026 | **a 005-0 sobe de R$ 840,00 para R$ 1.879,80** |

Algumas mudanças aparecem só nas **Notas Técnicas mensais da CGSI**, sem portaria nova:
- a 001-8 restrita ao cardiologista (NT 06/2025);
- a troca de um CID na 002-6 (NT 12/2024);
- a correção do nome "coronariana" (NT 02/2025).

**Onde acompanhar:**
- **a ficha e o histórico:** no SIGTAP (`sigtap.datasus.gov.br`). Em 22/10/2026 o site estava
  parado na competência 05/2026; a 10/2026 está no FTP do DATASUS;
- **as Notas Técnicas mensais:** no FTP do DATASUS;
- **a vigia do projeto:** roda todo dia 10 e registra em `registros/vigia/` (agente `normas`).

**O que a mudança faz com o plano:**
- o valor de referência é o da ficha da competência vigente, com a portaria que o fixou
  (`metodo/comum.md`, regras 1 a 3);
- se o valor sobe depois do envio, como a 005-0 em 09/2026, o plano enviado continua com o
  valor velho até ser corrigido;
- se a OCI é do recurso federal, o convênio não paga acima do SIGTAP (LI-002).

## 5. Palavras que aparecem nas fichas

| palavra | o que é |
|---|---|
| competência | o mês da tabela do SUS (10/2026 = outubro de 2026) |
| APAC | a autorização de procedimento ambulatorial, onde a OCI é registrada |
| FAEC | o fundo federal que paga a OCI no programa; a emenda não paga por ele |
| CID | o código da doença ou do motivo da consulta |
| CBO | o código da ocupação do profissional (225120 = cardiologista) |
| habilitação 38.01 a 38.06 | a marca do programa federal no CNES; descreve o programa, não é exigência do proponente |
| incremento | o acréscimo sobre a tabela que algumas habilitações dão a exames avulsos (eco, cintilografia); na OCI não há |
