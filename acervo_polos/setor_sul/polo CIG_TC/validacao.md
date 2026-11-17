# Validação cadastral — CIG CENTRO DE IMAGENS GAMA

Consulta de 16/11/2026. Gerado por `validar.py`; rodar de novo sobrescreve.

## Conferência

| resultado | item | detalhe |
|---|---|---|
| confere | Situação cadastral | ATIVA desde 2016-05-23 |
| confere | Nome × Receita | informado "CIG CENTRO DE IMAGENS GAMA"; Receita: CIG - CENTRO DE IMAGENS GAMA LTDA / CIG-CENTRO DE IMAGENS GAMA |
| **DIVERGE** | CEP × Receita | informado 72425132; Receita 72425100 |
| confere | CNAE para TC | 8640-2/04 serviços de tomografia: consta |
| confere | CNPJ × CNES | informado 24.857.885/0001-08; o CNES 9180168 está no CNPJ 24.857.885/0001-08 |
| confere | Nome × CNES | informado "CIG CENTRO DE IMAGENS GAMA"; CNES: CIG CENTRO DE IMAGENS GAMA LTDA / CIG CENTRO DE IMAGENS GAMA |
| confere | CEP × CNES | informado 72425132; CNES 72425132 |
| atenção | CEP Receita × CNES | Receita 72425100; CNES 72425132 — endereços diferentes |
| atenção | Atendimento ambulatorial SUS | CNES declara: NAO |
| atenção | Atualização do CNES | 2025-09-03 — há mais de seis meses |
| atenção | Equipamento de tomografia | 1 × Tomógrafo computadorizado 4 canais — NÃO marcado como disponível para o SUS |
| atenção | Serviço 121/003 tomografia | cadastrado, ambulatorial só NÃO SUS — falta a marca SUS |

## Receita Federal

| campo | valor |
|---|---|
| CNPJ | 24.857.885/0001-08 (MATRIZ) |
| Razão social | CIG - CENTRO DE IMAGENS GAMA LTDA |
| Nome fantasia | CIG-CENTRO DE IMAGENS GAMA |
| Natureza jurídica | Sociedade Empresária Limitada |
| Início de atividade | 2016-05-23 |
| Endereço | QUADRA QUADRA 10, 02, LOTE 16 E 17 LOJA 01 E — SETOR OESTE (GAMA), BRASILIA/DF, CEP 72425100 |
| Atividade principal | 8640207 Serviços de diagnóstico por imagem sem uso de radiação ionizante, exceto ressonância magnética |
| Quadro societário | ELTON GONCALVES MONTIJO (Sócio); HUGO HOLANDA DE SOUZA (Sócio-Administrador); JOSE WANDERLEY MONTEIRO (Sócio); MARCELO RODRIGUES PINTO DE OLIVEIRA (Sócio); RAFAEL GUSTAVO DOS SANTOS OLIVEIRA (Sócio) |

Atividades secundárias:

- 8640204 Serviços de tomografia
- 8640205 Serviços de diagnóstico por imagem com uso de radiação ionizante, exceto tomografia
- 8640206 Serviços de ressonância magnética

## CNES

| campo | valor |
|---|---|
| CNES | 9180168 |
| Razão social | CIG CENTRO DE IMAGENS GAMA LTDA |
| Nome fantasia | CIG CENTRO DE IMAGENS GAMA |
| CNPJ no CNES | 24.857.885/0001-08 |
| Tipo de estabelecimento | 36 CLINICA/CENTRO DE ESPECIALIDADE |
| Endereço | QUADRA 10 LOTE 16 E 17 LOJA 01 E 02, S/N — SETOR OESTE GAMA, CEP 72425132 |
| Telefone / e-mail | 61 35486162 / DIRETORIA@CENTRODEIMAGENSGAMA.COM.BR |
| Gestão | E (ESTADUAL) |
| Turno | ATENDIMENTOS NOS TURNOS DA MANHA E A TARDE |
| Ambulatorial SUS | NAO |
| Última atualização | 2025-09-03 |

## Diagnóstico por imagem no CNES — competência 09/2026

Arquivos mensais do DATASUS. Mudança feita no CNES depois dessa competência ainda não aparece aqui.

| equipamento | existentes | em uso | disponível SUS |
|---|---|---|---|
| Raio X para densitometria óssea | 1 | 1 | não |
| Ultrassom ecógrafo | 3 | 3 | não |
| Mamógrafo digital | 1 | 1 | não |
| Raio X analógico | 1 | 1 | não |
| Tomógrafo computadorizado 4 canais | 1 | 1 | não |
| Ressonância magnética 0,5 T | 2 | 2 | sim |

| serviço 121 — classificação | ambulatorial SUS | ambulatorial não SUS | próprio ou terceirizado |
|---|---|---|---|
| 001 Radiologia | não | sim | próprio |
| 002 Ultrassonografia | não | sim | próprio |
| 003 Tomografia computadorizada | não | sim | próprio |
| 004 Ressonância magnética | sim | sim | próprio |
| 012 Mamografia | não | sim | próprio |

Licença sanitária declarada no CNES: nº 00060-00062439/2021-45, expedida em 17/09/2025 (SES). O CNES não traz a validade — conferir no documento.

## O que estas bases não respondem

Conferir na ficha completa do CNES (cnes.datasus.gov.br, busca pelo número):

- [ ] profissionais vinculados, com o CBO que o procedimento exige
- [ ] se o equipamento cadastrado é o mesmo visto na visita (marca, modelo, quantidade)

Pedir cópia ao polo e guardar em `fotos/10_documentos/` — não há consulta pública aberta:

- [ ] licença sanitária, cobrindo radiodiagnóstico se houver tomografia
- [ ] licença de funcionamento (alvará)
- [ ] vistoria do Corpo de Bombeiros
- [ ] certidão do responsável técnico no conselho
