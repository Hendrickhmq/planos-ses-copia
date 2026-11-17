# Filas de raio-X e escolha de carteira

Estudo em 11/11/2026. Fonte quantitativa: extração preservada do Mapa Social/MPDFT, SISREG/DATASUS, recarga 02/11/2026 10:31:47, solicitações até 28/10/2026. A página consultada hoje informa recarga 11/11/2026 00:32:28, mas os filtros mudaram durante a consulta e não foi possível validar um recorte estável de raio-X. Portanto, os números deste relatório NÃO são uma atualização integral de hoje.

## Parecer

Priorizar cotação de tórax PA/perfil, joelho AP/lateral, coluna lombossacra e pé/dedos em serviço já instalado. Mãos têm volume, mas tarifa menor; punho, cervical e coluna torácica são complementos. Não há custo contratado de raio-X neste estudo: a ordem indica atratividade para cotar, não margem comprovada. Examinar demanda regulada disponível e cobertura de outros contratos/OCI antes de definir metas.

## Demanda e referência de receita

Na classificação Radiologia do inventário: 3.458 pedidos, sendo 3.442 solicitados nos últimos 24 meses. Não são pessoas únicas. Mamografia, densitometria e imagem odontológica foram classificadas separadamente. O valor bruto teórico de todo este estoque é R$ 102.678,64, multiplicando quantidade pela referência Candanga; não é receita garantida nem orçamento aprovado.

| Procedimento agrupado por código cadastrado | Código | Pedidos | Últimos 24 meses | Referência Candanga R$ |
|---|---|---:|---:|---:|
| RADIOGRAFIA DE TORAX (PA E PERFIL) | 0204030153 | 648 | 648 | 29,95 |
| RADIOGRAFIA DE MAO | 0204040094 | 314 | 314 | 20,48 |
| RADIOGRAFIA DE JOELHO (AP + LATERAL) | 0204060125 | 309 | 309 | 30,32 |
| RADIOGRAFIA DE COLUNA LOMBO-SACRA | 0204020069 | 293 | 293 | 32,84 |
| RADIOGRAFIA DE PE / DEDOS DO PE | 0204060150 | 252 | 252 | 30,32 |
| RADIOGRAFIA DE MAO E PUNHO (P/ DETERMINACAO DE IDADE OSSEA) | 0204040108 | 144 | 143 | 28,49 |
| RADIOGRAFIA DE CAVUM (LATERAL + HIRTZ) | 0204010063 | 144 | 142 | 24,92 |
| RADIOGRAFIA DE COLUNA CERVICAL (AP + LATERAL + TO + OBLIQUAS) | 0204020034 | 141 | 140 | 30,86 |
| RADIOGRAFIA DE PUNHO (AP + LATERAL + OBLIQUA) | 0204040124 | 129 | 129 | 31,06 |
| RADIOGRAFIA DE COLUNA TORACICA (AP + LATERAL) | 0204020093 | 128 | 128 | 34,60 |
| RADIOGRAFIA DE JOELHO OU PATELA (AP + LATERAL + AXIAL) | 0204060133 | 123 | 123 | 31,50 |
| RADIOGRAFIA DE CALCANEO | 0204060109 | 89 | 87 | 24,31 |
| RADIOGRAFIA DE ESCAPULA/OMBRO (TRES POSICOES) | 0204040116 | 83 | 83 | 29,76 |
| RADIOGRAFIA DE BACIA | 0204060095 | 76 | 76 | 30,58 |
| RADIOGRAFIA DE ARTICULACAO COXO-FEMORAL | 0204060060 | 63 | 63 | 32,47 |
| RADIOGRAFIA DE COLUNA LOMBO-SACRA (C/ OBLIQUAS) | 0204020077 | 60 | 60 | 45,98 |
| RADIOGRAFIA DE ARTICULACAO TIBIO-TARSICA | 0204060087 | 55 | 55 | 28,85 |
| RADIOGRAFIA DE PERNA | 0204060168 | 55 | 55 | 32,79 |

O lote inicial sugerido soma 1.502 pedidos e R$ 46.039,24 de receita bruta teórica. É um lote pontual; o estoque não comprova fluxo mensal para sustentar investimento novo. Cotar preço integral com execução, incidências, laudo, entrega e repetições. A diferença entre tarifa e cotação ainda precisa cobrir custos próprios, faltas e despesas administrativas.

Validar nomes e incidências: há grafias diferentes sob o mesmo código e protocolos locais que não coincidem integralmente com o nome oficial. O quadro soma pedidos por código, sem deduplicar pessoas entre filas. Não cobrar por incidência adicional sem previsão do instrumento. A ordem é de composição operacional e econômica; a prioridade assistencial cabe à regulação.

## Alternativas de radiologia

Na mesma fotografia, densitometria tem 2.178 pedidos a R$ 220,00 (R$ 479.160 brutos teóricos) e mamografia reúne 6.630 pedidos a R$ 100,00 (R$ 663.000). Merecem cotação separada com prestador e equipamentos próprios; maior tarifa não demonstra maior margem. Em mamografia, conferir a distinção entre diagnóstico e rastreamento, pois os nomes locais compartilham o código de rastreamento na base.

## Fontes e limites

- Painel oficial: https://paineis-ext.mpdft.mp.br/extensions/mapasauderegulamentacao/mapasauderegulamentacao.html
- Extração local: tmp/estudo-integrado/fontes/mapa_social_20261102_inventario_bruto/motor_20261102.json; classificação: tmp/estudo-integrado/classificacao.json.
- Referência por código: ../outputs/estudo_imagem_candanga_20261101/tabela_oficial_sia.json. Valores conferidos também no arquivo da Tabela Candanga SIA, campo deliberações.
- A remuneração efetiva depende do instrumento aplicável. Não somar SIGTAP novamente à referência Candanga. Não foram verificados custo contratado, margem líquida ou disponibilidade de agenda.
