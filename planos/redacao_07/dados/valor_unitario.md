# Valor de referência por procedimento — o rol de imagem da Portaria SAES/MS 4.282/2026

O valor de referência de cada exame é o valor do Serviço Ambulatorial da Tabela do SUS
acrescido do incremento que o **Anexo I da Portaria SAES/MS nº 4.282, de 19 de junho de
2026**, fixa para o procedimento, com o centavo truncado — a mesma regra do plano 4 e do
redacao_06 (`planos/redacao_06/dados/valor_unitario.md`):

```
valor de referência = valor de tabela × (1 + incremento), truncado na segunda casa
```

- **Fonte:** `biblioteca/normas/SAES 4282-2026 rol imagem e incremento.pdf`, Anexo I (101
  procedimentos). O valor de tabela e o incremento foram lidos do PDF por script em
  15/10/2026, e o valor de referência é **CALCULADO**.
- **Conferência:** os onze códigos do plano 4 dão exatamente os valores de
  `planos/redacao_04/dados/valor_unitario.md` (R$ 99,94, R$ 100,18, R$ 299,44 e R$ 300,10).
- **As Portarias SAES/MS 4.694 e 4.695/2026** levam o rol aos Componentes Ambulatorial e
  Ressarcimento "com os mesmos parâmetros remuneratórios e percentuais de incremento" do
  Anexo I. Só a 4.694 (Componente Ambulatorial, habilitação 38.01) tem prazo: produz efeitos até
  31/12/2026 (art. 6º). A 4.695 (Ressarcimento, 38.06) não tem prazo (art. 8º). *Corrigido em
  16/10/2026, pela leitura das fichas: antes dizia que as duas iam até 31/12/2026.*
- **Exame de imagem fora do rol** (radiografia, mamografia diagnóstica, angiotomografia,
  arteriografia e outros) não tem incremento: o valor é o da Tabela, a conferir na ficha
  do SIGTAP (agente `ficha-sigtap`) se a fila virar candidata.
- **Fica de fora desta tabela** o que o Anexo I traz e não é exame de imagem: endoscopias
  (02.09), cateterismo (02.11), retirada de pólipo (04.07) e sedação (04.17).
- **Ficha do SIGTAP não baixada** (idade, sexo, CID, habilitação): se a fila virar
  candidata, a ficha vem antes do documento.

| código | procedimento | modalidade | valor de tabela | incremento | valor de referência | no plano 4 |
|---|---|---|---|---|---|---|
| 02.04.03.018-8 | MAMOGRAFIA BILATERAL PARA RASTREAMENTO | radiologia | R$ 45,00 | 122% | **R$ 99,90** |  |
| 02.04.06.002-8 | DENSITOMETRIA OSSEA DUO-ENERGETICA DE COLUNA (VERTEBRAS LOMBARES E/OU FÊMUR) | radiologia | R$ 55,10 | 300% | **R$ 220,40** |  |
| 02.05.01.003-2 | ECOCARDIOGRAFIA TRANSTORACICA | ultrassonografia | R$ 67,86 | 136% | **R$ 160,14** |  |
| 02.05.01.004-0 | ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS | ultrassonografia | R$ 39,60 | 153% | **R$ 100,18** | sim |
| 02.05.01.005-9 | ULTRASSONOGRAFIA DOPPLER DE FLUXO OBSTETRICO | ultrassonografia | R$ 42,90 | 133% | **R$ 99,95** |  |
| 02.05.02.003-8 | ULTRASSONOGRAFIA DE ABDOMEN SUPERIOR | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** | sim |
| 02.05.02.004-6 | ULTRASSONOGRAFIA DE ABDOMEN TOTAL | ultrassonografia | R$ 37,95 | 164% | **R$ 100,18** | sim |
| 02.05.02.005-4 | ULTRASSONOGRAFIA DE APARELHO URINARIO | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** | sim |
| 02.05.02.006-2 | ULTRASSONOGRAFIA DE ARTICULACAO | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.007-0 | ULTRASSONOGRAFIA DE BOLSA ESCROTAL | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.008-9 | ULTRASSONOGRAFIA DE GLOBO OCULAR / ORBITA (MONOCULAR) | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.009-7 | ULTRASSONOGRAFIA MAMARIA BILATERAL | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** | sim |
| 02.05.02.010-0 | ULTRASSONOGRAFIA DE PROSTATA POR VIA ABDOMINAL | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** | sim |
| 02.05.02.011-9 | ULTRASSONOGRAFIA DE PROSTATA (VIA TRANSRETAL) | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.012-7 | ULTRASSONOGRAFIA DE TIREOIDE | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** | sim |
| 02.05.02.013-5 | ULTRASSONOGRAFIA DE TORAX (EXTRACARDIACA) | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.014-3 | ULTRASSONOGRAFIA OBSTÉTRICA | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.015-1 | ULTRASSONOGRAFIA OBSTETRICA C/ DOPPLER COLORIDO E PULSADO | ultrassonografia | R$ 39,60 | 153% | **R$ 100,18** |  |
| 02.05.02.016-0 | ULTRASSONOGRAFIA PELVICA (GINECOLOGICA) | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.017-8 | ULTRASSONOGRAFIA TRANSFONTANELA | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.05.02.018-6 | ULTRASSONOGRAFIA TRANSVAGINAL | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** | sim |
| 02.05.02.022-4 | ELASTOGRAFIA HEPÁTICA ULTRASSÔNICA | ultrassonografia | R$ 24,20 | 313% | **R$ 99,94** |  |
| 02.06.01.001-0 | TOMOGRAFIA COMPUTADORIZADA DE COLUNA CERVICAL C/ OU S/ CONTRASTE | tomografia | R$ 86,76 | 246% | **R$ 300,18** |  |
| 02.06.01.002-8 | TOMOGRAFIA COMPUTADORIZADA DE COLUNA LOMBO- SACRA C/ OU S/ CONTRASTE | tomografia | R$ 101,10 | 197% | **R$ 300,26** |  |
| 02.06.01.003-6 | TOMOGRAFIA COMPUTADORIZADA DE COLUNA TORACICA C/ OU S/ CONTRASTE | tomografia | R$ 86,76 | 246% | **R$ 300,18** |  |
| 02.06.01.004-4 | TOMOGRAFIA COMPUTADORIZADA DE FACE / SEIOS DA FACE / ARTICULACOES TEMPORO-MANDIBULARES | tomografia | R$ 86,75 | 246% | **R$ 300,15** |  |
| 02.06.01.005-2 | TOMOGRAFIA COMPUTADORIZADA DO PESCOCO | tomografia | R$ 86,75 | 246% | **R$ 300,15** |  |
| 02.06.01.006-0 | TOMOGRAFIA COMPUTADORIZADA DE SELA TURCICA | tomografia | R$ 97,44 | 208% | **R$ 300,11** |  |
| 02.06.01.007-9 | TOMOGRAFIA COMPUTADORIZADA DO CRÂNIO | tomografia | R$ 97,44 | 208% | **R$ 300,11** |  |
| 02.06.02.001-5 | TOMOGRAFIA COMPUTADORIZADA DE ARTICULACOES DE MEMBRO SUPERIOR | tomografia | R$ 86,75 | 246% | **R$ 300,15** |  |
| 02.06.02.002-3 | TOMOGRAFIA COMPUTADORIZADA DE SEGMENTOS APENDICULARES (BRAÇO, ANTEBRAÇO, MÃO, COXA, PERNA, PE) | tomografia | R$ 86,75 | 246% | **R$ 300,15** |  |
| 02.06.02.003-1 | TOMOGRAFIA COMPUTADORIZADA DE TÓRAX | tomografia | R$ 136,41 | 120% | **R$ 300,10** | sim |
| 02.06.03.001-0 | TOMOGRAFIA COMPUTADORIZADA DE ABDOMEN SUPERIOR | tomografia | R$ 138,63 | 116% | **R$ 299,44** | sim |
| 02.06.03.002-9 | TOMOGRAFIA COMPUTADORIZADA DE ARTICULACOES DE MEMBRO INFERIOR | tomografia | R$ 86,75 | 246% | **R$ 300,15** |  |
| 02.06.03.003-7 | TOMOGRAFIA COMPUTADORIZADA DE PELVE / BACIA / ABDOMEN INFERIOR | tomografia | R$ 138,63 | 116% | **R$ 299,44** | sim |
| 02.07.01.001-3 | ANGIORESSONANCIA CEREBRAL | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.01.002-1 | RESSONANCIA MAGNETICA DE ARTICULACAO TEMPORO- MANDIBULAR (BILATERAL) | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.01.003-0 | RESSONANCIA MAGNETICA DE COLUNA CERVICAL/PESCOÇO | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.01.004-8 | RESSONANCIA MAGNETICA DE COLUNA LOMBO-SACRA | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.01.005-6 | RESSONANCIA MAGNETICA DE COLUNA TORACICA | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.01.006-4 | RESSONANCIA MAGNETICA DE CRANIO | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.01.007-2 | RESSONANCIA MAGNETICA DE SELA TURCICA | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.02.001-9 | RESSONANCIA MAGNETICA DE CORACAO / AORTA C/ CINE | ressonância magnética | R$ 361,25 | 38% | **R$ 498,52** |  |
| 02.07.02.002-7 | RESSONANCIA MAGNETICA DE MEMBRO SUPERIOR (UNILATERAL) | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.02.003-5 | RESSONANCIA MAGNETICA DE TORAX | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.02.006-0 | RESSONÂNCIA MAGNÉTICA DA MAMA | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.03.001-4 | RESSONANCIA MAGNETICA DE ABDOMEN SUPERIOR | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.03.002-2 | RESSONANCIA MAGNETICA DE BACIA / PELVE / ABDOMEN INFERIOR | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.03.003-0 | RESSONANCIA MAGNETICA DE MEMBRO INFERIOR (UNILATERAL) | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.03.004-9 | RESSONANCIA MAGNETICA DE VIAS BILIARES / COLANGIORESSONÂNCIA | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.07.03.005-7 | RESSONÂNCIA MAGNÉTICA MULTIPARAMÉTRICA DA PRÓSTATA | ressonância magnética | R$ 268,75 | 86% | **R$ 499,87** |  |
| 02.08.01.001-7 | CINTILOGRAFIA DE CORACAO C/ GALIO 67 | medicina nuclear | R$ 457,55 | 100% | **R$ 915,10** |  |
| 02.08.01.002-5 | CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE ESTRESSE (MINIMO 3 PROJECOES) | medicina nuclear | R$ 408,52 | 120% | **R$ 898,74** |  |
| 02.08.01.003-3 | CINTILOGRAFIA DE MIOCARDIO P/ AVALIACAO DA PERFUSAO EM SITUACAO DE REPOUSO (MINIMO 3 PROJECOES) | medicina nuclear | R$ 383,07 | 130% | **R$ 881,06** |  |
| 02.08.01.004-1 | CINTILOGRAFIA DE MIOCARDIO P/ LOCALIZACAO DE NECROSE (MINIMO 3 PROJEÇOES) | medicina nuclear | R$ 166,47 | 300% | **R$ 665,88** |  |
| 02.08.01.005-0 | CINTILOGRAFIA P/ AVALIACAO DE FLUXO SANGUINEO DE EXTREMIDADES | medicina nuclear | R$ 114,02 | 300% | **R$ 456,08** |  |
| 02.08.01.006-8 | CINTILOGRAFIA P/ QUANTIFICACAO DE SHUNT EXTRACARDIACO | medicina nuclear | R$ 142,57 | 300% | **R$ 570,28** |  |
| 02.08.01.007-6 | CINTILOGRAFIA SINCRONIZADA DE CAMARAS CARDIACAS EM SITUACAO DE ESFORCO | medicina nuclear | R$ 214,85 | 300% | **R$ 859,40** |  |
| 02.08.01.008-4 | CINTILOGRAFIA SINCRONIZADA DE CAMARAS CARDIACAS EM SITUACAO DE REPOUSO (VENTRICULOGRAFIA) | medicina nuclear | R$ 176,72 | 300% | **R$ 706,88** |  |
| 02.08.02.001-2 | CINTILOGRAFIA DE FIGADO E BACO (MINIMO 5 IMAGENS) | medicina nuclear | R$ 133,26 | 300% | **R$ 533,04** |  |
| 02.08.02.002-0 | CINTILOGRAFIA DE FIGADO E VIAS BILIARES | medicina nuclear | R$ 187,93 | 300% | **R$ 751,72** |  |
| 02.08.02.003-9 | CINTILOGRAFIA DE GLANDULAS SALIVARES C/ OU S/ ESTÍMULO | medicina nuclear | R$ 87,89 | 300% | **R$ 351,56** |  |
| 02.08.02.005-5 | CINTILOGRAFIA P/ ESTUDO DE TRANSITO ESOFAGICO (Líquido) | medicina nuclear | R$ 135,38 | 300% | **R$ 541,52** |  |
| 02.08.02.006-3 | CINTILOGRAFIA P/ ESTUDO DE TRANSITO ESOFAGICO (SEMI-SOLIDO) | medicina nuclear | R$ 135,38 | 300% | **R$ 541,52** |  |
| 02.08.02.007-1 | CINTILOGRAFIA P/ ESTUDO DE TRANSITO GASTRICO | medicina nuclear | R$ 144,22 | 300% | **R$ 576,88** |  |
| 02.08.02.008-0 | CINTILOGRAFIA P/ PESQUISA DE DIVERTICULOSE DE MECKEL | medicina nuclear | R$ 114,86 | 300% | **R$ 459,44** |  |
| 02.08.02.009-8 | CINTILOGRAFIA P/ PESQUISA DE HEMORRAGIA DIGESTIVA ATIVA | medicina nuclear | R$ 157,23 | 300% | **R$ 628,92** |  |
| 02.08.02.010-1 | CINTILOGRAFIA P/ PESQUISA DE HEMORRAGIA DIGESTIVA NAO ATIVA | medicina nuclear | R$ 310,82 | 200% | **R$ 932,46** |  |
| 02.08.02.011-0 | CINTILOGRAFIA P/ PESQUISA DE REFLUXO GASTRO- ESOFÁGICO | medicina nuclear | R$ 135,38 | 300% | **R$ 541,52** |  |
| 02.08.02.012-8 | IMUNO-CINTILOGRAFIA (ANTICORPO MONOCLONAL) | medicina nuclear | R$ 1.103,26 | sem incremento | **R$ 1.103,26** |  |
| 02.08.03.001-8 | CINTILOGRAFIA DE PARATIREOIDES | medicina nuclear | R$ 324,54 | 200% | **R$ 973,62** |  |
| 02.08.03.002-6 | CINTILOGRAFIA DE TIREÓIDE COM OU SEM CAPTAÇÃO | medicina nuclear | R$ 77,28 | 100% | **R$ 154,56** |  |
| 02.08.03.003-4 | CINTILOGRAFIA DE TIREOIDE C/ TESTE DE SUPRESSAO / Estímulo | medicina nuclear | R$ 107,30 | 300% | **R$ 429,20** |  |
| 02.08.03.004-2 | CINTILOGRAFIA P/ PESQUISA DO CORPO INTEIRO | medicina nuclear | R$ 338,70 | 100% | **R$ 677,40** |  |
| 02.08.04.002-1 | CINTILOGRAFIA DE RIM C/ GALIO 67 | medicina nuclear | R$ 457,55 | 100% | **R$ 915,10** |  |
| 02.08.04.003-0 | CINTILOGRAFIA DE TESTICULO E BOLSA ESCROTAL | medicina nuclear | R$ 108,94 | 300% | **R$ 435,76** |  |
| 02.08.04.005-6 | CINTILOGRAFIA RENAL/RENOGRAMA (QUALITATIVA E/OU QUANTITATIVA) | medicina nuclear | R$ 133,03 | 300% | **R$ 532,12** |  |
| 02.08.04.006-4 | CISTOCINTILOGRAFIA DIRETA | medicina nuclear | R$ 122,97 | 300% | **R$ 491,88** |  |
| 02.08.04.007-2 | CISTOCINTILOGRAFIA INDIRETA | medicina nuclear | R$ 144,50 | 300% | **R$ 578,00** |  |
| 02.08.05.001-9 | CINTILOGRAFIA DE ARTICULACOES E/OU EXTREMIDADES E/OU OSSO | medicina nuclear | R$ 180,32 | 300% | **R$ 721,28** |  |
| 02.08.05.003-5 | CINTILOGRAFIA DE OSSOS COM OU SEM FLUXO SANGUÍNEO (CORPO INTEIRO) | medicina nuclear | R$ 190,99 | 300% | **R$ 763,96** |  |
| 02.08.05.004-3 | CINTILOGRAFIA DE SEGMENTO OSSEO C/ GALIO 67 | medicina nuclear | R$ 457,55 | 100% | **R$ 915,10** |  |
| 02.08.06.001-4 | CINTILOGRAFIA DE PERFUSAO CEREBRAL C/ TALIO (SPCTO) | medicina nuclear | R$ 438,01 | 100% | **R$ 876,02** |  |
| 02.08.06.002-2 | CISTERNOCINTILOGRAFIA (INCLUINDO PESQUISA E/OU AVALIACAO DO TRANSITO LIQUORICO) | medicina nuclear | R$ 205,34 | 300% | **R$ 821,36** |  |
| 02.08.07.001-0 | CINTILOGRAFIA DE PULMAO C/ GALIO 67 | medicina nuclear | R$ 457,55 | 100% | **R$ 915,10** |  |
| 02.08.07.002-8 | CINTILOGRAFIA DE PULMÃO P/ PESQUISA DE ASPIRAÇÃO | medicina nuclear | R$ 127,51 | 300% | **R$ 510,04** |  |
| 02.08.07.003-6 | CINTILOGRAFIA DE PULMAO POR INALACAO (MINIMO 2 PROJECOES) | medicina nuclear | R$ 127,12 | 300% | **R$ 508,48** |  |
| 02.08.07.004-4 | CINTILOGRAFIA DE PULMAO POR PERFUSAO (MINIMO 4 PROJECOES) | medicina nuclear | R$ 130,50 | 300% | **R$ 522,00** |  |
| 02.08.08.001-5 | CINTILOGRAFIA DE SISTEMA RETICULO-ENDOTELIAL (MEDULA OSSEA) | medicina nuclear | R$ 112,61 | 300% | **R$ 450,44** |  |
| 02.08.08.004-0 | LINFOCINTILOGRAFIA | medicina nuclear | R$ 141,33 | 300% | **R$ 565,32** |  |
| 02.08.09.001-0 | CINTILOGRAFIA DE CORPO INTEIRO C/ GALIO 67 P/ PESQUISA DE NEOPLASIAS | medicina nuclear | R$ 906,80 | sem incremento | **R$ 906,80** |  |
| 02.08.09.002-9 | CINTILOGRAFIA DE GLANDULA LACRIMAL (DACRIOCINTILOGRAFIA) | medicina nuclear | R$ 66,23 | 200% | **R$ 198,69** |  |
| 02.08.09.003-7 | CINTILOGRAFIA DE MAMA (BILATERAL) | medicina nuclear | R$ 289,43 | 200% | **R$ 868,29** |  |
| 05.01.08.009-0 | ULTRASSONOGRAFIA DE ORGAO TRANSPLANTADO | ultrassonografia | R$ 12,00 | 300% | **R$ 48,00** |  |
