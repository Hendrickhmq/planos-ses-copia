# O estudo das filas de imagem — o que se levantou e por que se cortou

**Controle interno: não vai ao documento.**

Emenda de Bancada 71080005 (R$ 1.502.687,00), redacao_07. Este arquivo reúne num lugar só o
caminho de 15 a 20/10/2026: o que o Mapa Social mostrou, o que entrou na carteira do PT
simplificado e por que cada grupo de filas ficou de fora, com quem decidiu e quando. A
planilha `estudo_das_filas.xlsx` traz os 167 códigos, um por linha, com a decisão e o motivo
(filtro na primeira coluna). O script é `scripts/estudo_filas.py`.

## As fontes

| | |
|---|---|
| fila | Mapa Social da Saúde, recarga de 15/10/2026 19:32, coleta do agente `mapa-social` (`fontes/mapa_social_20261015.md`, 7/7). Varredura pelo código SIGTAP nos subgrupos 02.04 a 02.10 e pelo nome: **756 nomes de fila com gente esperando** |
| coleta anterior | a do pré-plano do plano 4, de 09/10/2026 (`planos/redacao_06/dados/fontes/mapa_social_20261009.md`): ultrassom e tomografia, já com as 82 filas do mesmo código do plano 4 |
| valor | `valor_unitario.md`: o rol de imagem da Portaria SAES/MS 4.282/2026, com o incremento |
| preço de mercado | `precos.md` (16/10/2026), só dos códigos que chegaram perto da carteira |
| fichas SIGTAP | `fontes/sigtap_*_102026.md`, os 16 da carteira e a mamografia diagnóstica no texto da ficha da 018-8 |

**Fila** = pedidos pendentes de regulação (três status); devolvidas ficam fora. **Meses para a
rede zerar** = fila ÷ agendamentos por mês em 2026 (jan–set ÷ 9): quanto maior, menos a rede
dá conta sozinha.

## A regra dos cortes (usuário, 20/10/2026)

**A maior parte do que saiu já tem outro projeto lidando com ela, ou vai ter:**
- o **plano 4** de imagem (ISHP, R$ 11,5 mi);
- os convênios do **IEV** (Instituto Esporte e Vida), que têm exames de imagem dentro das OCI:
  - **030975/2026**, ortopedia (DOA), R$ 16,67 mi;
  - **030976/2026**, ortopedia (DOAR), R$ 6,0 mi;
  - **030977/2026**, Fila Zero, cinco especialidades, R$ 9,0 mi.
  
  No Fila Zero, a ecocardiografia transtorácica entra na OCI de insuficiência cardíaca (09.02.01.006-9). A eco de estresse entra na de síndrome coronariana (09.02.01.004-2). O ultrassom de partes moles e a tomografia de articulações ou segmentos entram nas de ortopedia (09.03.01.002-0 e 09.03.01.003-8). Fonte: `registros/fontes/pre_planos_20261007/iev_194448359_plano_detalhado_fila_zero.txt` e o acervo (IT-003 a IT-005).

O resto saiu por outros motivos:
- **cintilografia:** complexa de executar (confirmado: licença da CNEN e da vigilância, equipe certificada, radiofármaco do IPEN);
- **ressonância:** a rede já cuida;
- **fora da Portaria 4.282:** paga mal (confirmado: radiografias de R$ 6,30 a R$ 10,96 na Tabela);
- **fila pequena:** não vale a pena incluir.

## O resumo

| grupo | códigos | nomes de fila | pedidos | decisão | quem e quando |
|---|---|---|---|---|---|
| **0. Entra na carteira** | **12** | 76 | **15.644** | entra | usuário, 16, 19 e 20/10/2026 |
| 1. Plano 4 | 11 | 16 | 76.037 | fora: já é objeto do plano 4 | plano 4 |
| 2. Mesmo código do plano 4 | 11 | 88 | 9.761 | fora: risco de sobreposição | usuário, 16/10/2026 |
| 3. Ecocardiografia | 1 | 3 | 16.293 | fora: na OCI de cardiologia do IEV | usuário, 15/10/2026 |
| 4. Articulações, partes moles e TC de ortopedia | 15 | 171 | 15.628 | fora: nas OCI de ortopedia do IEV | usuário, 15, 16 e 20/10/2026 |
| 5. Cintilografia | 23 | 24 | 5.915 | fora: complexa de executar (CNEN, Anvisa, IPEN) | usuário, 16/10/2026 |
| 6. Ressonância | 14 | 183 | 9.798 | fora: a rede já cuida | usuário, 16/10/2026 |
| 7. Fora do rol da Portaria 4.282 | 53 | 150 | 6.346 | fora: paga mal (radiografias de R$ 6,30 a R$ 10,96) | estudo, 15/10/2026 |
| 8. No rol, fila pequena | 3 | 4 | 51 | fora: não vale a pena | usuário, 20/10/2026 |
| 9. Fora dos subgrupos de imagem | 7 | 10 | 5.085 | fora | estudo, 15/10/2026 |
| 10. Resíduo | 17 | 31 | 66 | fora | estudo, 15/10/2026 |
| **total** | **167** | **756** | **160.624** | | |

Os pedidos são somas por código (cada pedido tem um código só); as pessoas não se somam. O
grupo 2 inclui 258 pedidos em nomes de fila sem movimento em 2026.

## Como se chegou à carteira

| data | o que aconteceu | de onde |
|---|---|---|
| 15/10 | o usuário pede filas de imagem **além do plano 4** para a emenda de R$ 1,5 mi; o agente varre os 756 nomes | `fontes/mapa_social_20261015.md` |
| 15/10 | "pode ser mais de uma fila, onde o valor total chegue a 1,5 milhão" | `estado.yaml` |
| 15/10 | a emenda é a mesma do otorrino (redacao_05); gestão e apoio sem valor: dois cenários, sem apoio e 10% | `estado.yaml` |
| 15/10 | "retire Ecocardiografia transtorácica e todos os outros de articulações" | grupos 3 e 4 |
| 16/10 | "retire todos de cintilografia" | grupo 5 |
| 16/10 | combinação A escolhida: ultrassons de espera longa e o resto em TC de pescoço, crânio e face (e não B, mamografia; C, ressonância; D, o mesmo código do plano 4) | `cobertura.md`, seção 3 |
| 16/10 | "tire partes moles" | grupo 4 |
| 16/10 | "acho bom focarmos em mamografia" e "mamografia primeiro"; 10% de apoio | `cenario_*.xlsx` |
| 19/10 | o Ofício 398 da ARINS pede o PT de **exames de imagem**; a carteira fica com os dez dos cenários e mais seis, para dar abrangência; 12 meses | `plano_v1_geral.md` |
| 20/10 | a regra dos cortes: o que outro projeto já cobre sai. Saem as TC de coluna (cervical, torácica, lombo-sacra) e de segmentos apendiculares, compatíveis com a OCI de ortopedia do IEV: a carteira fica com **doze** | `plano_v1_geral.md` |
| 20/10 | o documento passa a ordenar pela espera e pelo tamanho da fila, com a mamografia e a densitometria por último: a espera curta delas (44 a 49 dias) mostra que a rede dá conta | `plano_v1_geral.md` |
| 20/10 | o cenário de execução: as dez filas de espera longa primeiro; mamografia e densitometria de reserva ("pode deixar as duas de reserva") | `cenario_4_espera_longa_com_reserva.xlsx` |

## 0. O que entra — 12 códigos, 15.644 pedidos

Critério comum: **no rol da Portaria 4.282** (com incremento: R$ 99,90 a R$ 300,26 por exame),
**fora do plano 4** e com **espera longa ou rede que não dá conta**. A quantidade de cada um é
pactuada com a SES; o PT lista a carteira e fixa só o valor.

| código | procedimento | fila | espera média | meses para a rede zerar | por que entra |
|---|---|---|---|---|---|
| 02.05.02.016-0 | US pélvica (ginecológica) | 1.003 | 603 dias | 9,0 | a maior espera da carteira |
| 02.05.02.007-0 | US de bolsa escrotal | 995 | 588 dias | 13,9 | espera longa |
| 02.05.02.017-8 | US transfontanela | 281 | 282 dias | 3,8 | espera longa; recém-nascido (0 a 4 anos) |
| 02.05.02.008-9 | US de globo ocular / órbita | 1.272 | 264 dias | 22,1 | a rede não dá conta |
| 02.06.01.007-9 | TC de crânio | 1.467 | 197 dias | 1,1 | combinação A |
| 02.05.02.015-1 | US obstétrica com doppler | 205 | 177 dias | 6,3 | espera longa; **não se paga** pelo menor preço do DF (64%) |
| 02.06.01.006-0 | TC de sela túrcica | 45 | 169 dias | 1,2 | abrangência, mesmo tomógrafo |
| 02.05.02.014-3 | US obstétrica | 464 | 144 dias | 1,7 | abrangência, mesmo aparelho |
| 02.06.01.005-2 | TC de pescoço | 755 | 139 dias | 3,6 | combinação A |
| 02.06.01.004-4 | TC de face / seios / ATM | 500 | 124 dias | 1,0 | combinação A |
| 02.04.03.018-8 | Mamografia (rastreamento) | 6.461 | 49 dias | 1,4 | **reserva**: a rede dá conta |
| 02.04.06.002-8 | Densitometria óssea | 2.196 | 44 dias | 2,2 | **reserva**: a rede dá conta |

**Saíram em 20/10/2026** as TC de coluna cervical, torácica e lombo-sacra e a de segmentos
apendiculares (576 pedidos, R$ 172.911,11), que tinham entrado em 19/10 para dar abrangência: são
compatíveis com a OCI de ortopedia 09.03.01.003-8, que o Fila Zero do IEV executa (grupo 4).

**O cenário de execução (usuário, 20/10/2026): as dez filas de espera longa primeiro, mamografia e
densitometria de reserva.**
- **Por quê:** a mamografia (49 dias) e a densitometria (44 dias) têm espera curta, e a rede as
  zeraria em 1 a 2 meses. Pôr o recurso nelas primeiro seria difícil de defender. Ficam na
  carteira para não faltar demanda.
- **A conta, com 10% de apoio:** as dez filas custam R$ 1.252.250,57 para zerar. Do recurso para
  exames (R$ 1.352.418,30) sobram R$ 100.167,73, que vão para a reserva: cerca de 1.002
  mamografias (15% da fila). A densitometria só recebe se a mamografia esvaziar.
- **Por que a reserva quase não será usada:** as dez filas têm 4.546 pedidos feitos em 2026 ainda
  na fila (R$ 914.603,07, uns R$ 96 mil por mês). Esse valor é um indicador e não a medida de
  entrantes, que não foi coletada. Mesmo assim, a demanda nova de pouco mais de um mês já cobre a
  diferença. A reserva serve se a rede esvaziar alguma fila durante a execução.
- **No documento:** a carteira continua com os doze, e a mamografia e a densitometria vêm por
  último. A frase "a programação prioriza as filas de maior espera" diz a ordem sem expor o
  raciocínio (`metodo/pre_plano/procedimento.md`, regra 4); o redacao_05 usou a mesma ideia e a
  SUCONV aceitou.
- **Planilha:** `cenario_4_espera_longa_com_reserva.xlsx`.

## 1. Plano 4 — fora: já é objeto do plano 4

Os 16 nomes de fila do enquadramento do plano 4 (R$ 11,5 mi), em 11 códigos de ultrassom e
tomografia: 76.037 pedidos. As maiores: doppler colorido de vasos (14.592), US mamária (13.519),
US de abdômen total (13.508), US transvaginal (9.842).

## 2. Mesmo código do plano 4 — fora: risco de sobreposição

Filas fora do enquadramento do plano 4, mas com os mesmos 11 códigos: 9.761 pedidos, R$ 2,05 mi
para zerar. As maiores: doppler (2.647, espera de 475 dias, que inclui o doppler arterial de
membros inferiores), TC de abdômen superior (2.062), de tórax (1.901) e de pelve (1.409), estas
com as filas de emergência e as angiotomografias. As esperas são longas (270 a 597 dias), mas o
ISHP já recebe pelo plano 4 para estes códigos: os órgãos de controle podem ler como o mesmo
objeto pago duas vezes. As TC de emergência são pedidos de pronto-atendimento. A combinação D,
que as usava, não foi escolhida.

## 3. Ecocardiografia — fora: está na OCI de cardiologia do IEV

| código | fila | espera média | rede zera em | custo para zerar |
|---|---|---|---|---|
| 02.05.01.003-2 ecocardiografia transtorácica | 16.293 | 135 dias | 4,8 meses | R$ 2,6 mi (174% do recurso) |

A maior fila de imagem fora do plano 4. O IEV já a executa no Fila Zero (OCI 09.02.01.006-9,
insuficiência cardíaca). Além disso, a espera é curta, a rede agenda 3.422 por mês e o custo
passa do recurso inteiro. A eco de estresse e a transesofágica estão fora do rol.

## 4. Articulações, partes moles e TC de ortopedia — fora: estão nas OCI de ortopedia do IEV

| código | o que é | fila | espera média |
|---|---|---|---|
| 02.05.02.006-2 | US de articulação: as filas de ombro, punho, joelho, tornozelo, cotovelo, quadril, mão, pé e tendão (10.256), retiradas em 15/10, e as de partes moles e outras regiões (4.225: partes moles 3.108, região inguinal 587, pescoço e cervical 261 e outras), retiradas em 16/10 | 14.481 | 545 dias |
| 02.06.03.002-9 e 02.06.02.001-5 | TC de articulações de membro inferior e superior | 313 | 244 e 255 dias |
| 02.07.01.002-1 | RM de ATM | 127 | 22 dias |
| 02.06.01.001-0, 003-6, 002-8 e 02.06.02.002-3 | TC de coluna cervical, torácica e lombo-sacra e de segmentos apendiculares: entraram em 19/10 e saíram em 20/10 | 576 | 179 a 221 dias |
| sete códigos de 02.04 | radiografias de articulação (fora do rol) | 131 | — |

O código 02.05.02.006-2 tem a maior espera depois da US pélvica e a rede levaria 21 meses para
zerá-lo. No plano 4, partes moles saiu em 22/09/2026 "para ser contemplada em outra OCI" (D-007),
e o código é componente da OCI de ortopedia 09.03.01.002-0, que o IEV executa (Fila Zero e DOA). A TC de face/seios/ATM ficou: é exame
de face e seios.

## 5. Cintilografia (medicina nuclear) — fora: complexa de executar (confirmado em 20/10)

Toda a medicina nuclear (02.08), 23 códigos e 5.915 pedidos, inclusive o estudo renal dinâmico e
o de fluxo cerebral. As maiores: miocárdio de estresse (1.825) e de repouso (1.505), que se pedem
em par (1.387 pessoas nas duas), e óssea (1.688). A rede não dá conta delas (13 a 57 meses), mas
exigem serviço de medicina nuclear e radiofármaco, valem de R$ 154 a R$ 1.103 por exame, e 62% a
71% dos pedidos vêm de unidades de referência e contratados. A de miocárdio está na OCI de
cardiologia 09.02.01.005-0 (R$ 1.879,80), que o IEV não executa. 

**O que a pesquisa mostrou (20/10/2026)** — a cintilografia é a modalidade mais exigente da lista.
As normas não estão no acervo; as fontes são as páginas oficiais abaixo.

| exigência | o que é | fonte |
|---|---|---|
| **duas licenças** | Autorização de Operação da CNEN **e** licença da vigilância sanitária do DF; obra ou reforma com projeto aprovado pelas duas antes | RDC Anvisa 38/2008; guia da CNEN "Licenciamento e Controle de Instalações de Medicina Nuclear", v. 2.0, set/2023 |
| **equipe mínima** | titular legal perante a CNEN, médico nuclear como responsável técnico e supervisor de proteção radiológica **certificado pela CNEN**; mudança na equipe comunicada à CNEN em até 30 dias | Norma CNEN NN 3.05 (Resolução CNEN/CD 159/2013) |
| **radiofármaco** | o gerador de tecnécio-99m vem do IPEN, único fornecedor nacional, com desabastecimentos relatados pelo setor e um incidente no Centro de Radiofarmácia em maio/2026 | reportagens (Olhar Digital, jun/2026; Anaemn; SBMN e Abdan ao Senado) |
| **controle de qualidade** | testes obrigatórios dos eluatos do gerador, dos radiofármacos e da gama-câmara | RDC Anvisa 38/2008 |
| **rejeito e proteção** | rejeito radioativo, blindagem e monitoração sob a NN 3.05 | Norma CNEN NN 3.05 |

Para um convênio de 12 meses, isso quer dizer que **só uma clínica que já tem serviço de medicina
nuclear licenciado** poderia executar: não dá para montar. A execução fica presa ao fornecimento
do IPEN, que o proponente não controla. Confirma a avaliação do usuário.

Fontes: [NN 3.05](https://www.gov.br/cnen/pt-br/acesso-rapido/normas/grupo-3/ansn-3-05-requisitos-de-seguranca-e-protecao-radiologica-para-servicos-de-medicina-nuclear.pdf),
[Resolução CNEN/CD 159/2013](https://www.gov.br/cnen/pt-br/acesso-a-informacao/atos-normativos-cnen/comissao_deliberativa/resolucoes/2013/rs_cnencd_159_2013.pdf),
[guia de licenciamento da CNEN](https://appasp2019.cnen.gov.br/seguranca/orientacoes/images/cnen/documentos/drs/orientacoes/Licenciamento-e-Controle-de-Instalaes-Medicina-Nuclear-set2023.pdf),
[RDC Anvisa 38/2008](https://vigilanciasanitaria.prefeitura.rio/wp-content/uploads/sites/84/2023/05/4.ResolucaoRDCANVISAn38de2008.pdf),
[Olhar Digital, jun/2026](https://olhardigital.com.br/2026/06/12/ciencia-e-espaco/incidente-no-ipen-o-que-e-o-tecnecio-que-abastece-2-milhoes-de-exames-por-ano-no-brasil/),
[Viva/Anaemn](https://viva.com.br/saude-e-bem-estar/setor-de-medicina-nuclear-alerta-governo-sobre-falta-de-insumos.html),
[DGABC, SBMN e Abdan](https://www.dgabc.com.br/Noticia/3768537/sbmn-e-abdan-apelam-ao-senado-por-recursos-para-o-ipen). O PET-CT, que é tomografia, ficou no
grupo 7.

## 6. Ressonância — fora: a rede já cuida

| código | fila | espera média | rede zera em |
|---|---|---|---|
| RM de bacia/pelve | 1.625 | 24 dias | 1,0 mês |
| RM de membro inferior | 1.491 | 19 dias | 1,1 mês |
| RM de crânio | 1.417 | 30 dias | 0,9 mês |
| RM de coluna lombo-sacra | 1.412 | 19 dias | 0,9 mês |
| RM de membro superior | 1.140 | 19 dias | 1,1 mês |
| outros 9 códigos | 2.713 | 20 a 63 dias | — |
| **14 códigos** | **9.798** | **24 dias** | **cerca de 1 mês** |

A rede agenda por mês o tamanho da fila inteira (10.213 por mês). O recurso compraria 3.006
ressonâncias a R$ 499,87, mas mudaria pouco a espera. O IEV também tem convênio de ressonância
em ortopedia (OCI 09.03.01.004-6). A combinação C, que as usava, não foi
escolhida.

## 7. Fora do rol da Portaria 4.282 — fora: paga mal (confirmado em 20/10)

53 códigos, 6.346 pedidos, todos sem incremento: a emenda pagaria só a Tabela. O valor foi lido
no SIGTAP, competência 10/2026, em 20/10/2026. Nenhum dos onze maiores tem habilitação nem
incremento, nem pela 4.282 nem pelas Portarias 3.992 e 3.935/2026.

| código | exame | fila | espera média | valor SIGTAP | o que pesa |
|---|---|---|---|---|---|
| 02.04.01.017-9 | Radiografia panorâmica | 1.653 | 100 dias | R$ 9,03 | paga mal |
| 02.04.01.018-7 | Radiografia periapical (bite-wing) | 706 | 24 dias | **revogado desde 08/2020** | os sucessores (02.04.01.021-7 e 022-5) são da Atenção Básica, sem valor na Tabela (R$ 0,00); a fila usa código antigo |
| 02.04.03.015-3 | Radiografia de tórax (PA e perfil) | 662 | 95 dias | R$ 9,50 | paga mal; espera curta |
| 02.06.01.009-5 | PET-CT | 424 | 162 dias | **R$ 2.107,22** | alta complexidade; só por APAC e só três indicações (câncer de pulmão não pequenas células, metástase hepática de colorretal, linfomas). Paga bem, mas é serviço raro e a fila custaria R$ 893 mil |
| 02.04.06.012-5 | Radiografia de joelho | 298 | 81 dias | R$ 6,78 | paga mal |
| 02.04.04.009-4 | Radiografia de mão | 288 | 82 dias | R$ 6,30 | paga mal |
| 02.04.02.006-9 | Radiografia de coluna lombo-sacra | 281 | 105 dias | R$ 10,96 | paga mal |
| 02.04.06.015-0 | Radiografia de pé / dedos | 250 | 80 dias | R$ 6,78 | paga mal |
| 02.05.02.002-0 | Paquimetria ultrassônica | 164 | 22 dias | R$ 14,81 | paga mal; espera curta |
| 02.05.01.001-6 | Ecocardiografia de estresse | 60 | 27 dias | R$ 330,00 (SA R$ 165,00 + SH R$ 165,00) | alta complexidade; está na OCI de cardiologia do IEV (09.02.01.004-2) |
| 02.04.03.003-0 | Mamografia (diagnóstica) | — | — | R$ 22,50 | paga mal; os pedidos estão na fila da 018-8 |

**Conclusão:** as radiografias pagam de R$ 6,30 a R$ 10,96, e a mamografia diagnóstica, R$ 22,50.
Com o incremento, um ultrassom da carteira paga R$ 99,94. Nenhuma clínica faz exame por esse
valor de Tabela, e a espera delas já é curta. O PET-CT é a exceção: paga bem, mas é de alta
complexidade, com indicação restrita e pouco serviço habilitado. A eco de estresse já está no IEV.
A fonte é a leitura do agente `ficha-sigtap` em 20/10/2026, sem ficha gravada (só o valor).

## 8. No rol, fila pequena — fora: não vale a pena incluir

US de próstata transretal (20), US de tórax extracardíaca (17) e doppler de fluxo obstétrico (14):
estão no rol, mas a fila é pequena: não vale a pena incluir (usuário, 20/10/2026).

## 9. Fora dos subgrupos de imagem — fora

Achados pela busca por nome, com código fora de 02.04 a 02.10. O maior é a **tomografia de
coerência óptica (OCT)**, 02.11.06.028-3: 3.819 pedidos, 261 dias de espera, a rede levaria 45
meses. É exame oftalmológico, não está no rol da 4.282 e não é exame de imagem da emenda. Os
outros: biópsia de tireoide por agulha fina (521), biometria ultrassônica (459), biópsia guiada
por tomografia (269), cateterismo (14).

## 10. Resíduo — fora

17 códigos, 66 pedidos em nomes antigos do SISREG, sem nenhum pedido nem agendamento em 2026.
