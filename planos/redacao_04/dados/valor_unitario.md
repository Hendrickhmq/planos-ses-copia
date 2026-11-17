# Os unitários — tabela mais incremento, linha a linha

Fechado em 15/09/2026 contra o Anexo I da Portaria SAES/MS nº 4.282/2026. A
conferência de nome e código está em `conferencia_procedimentos.md`.

## O método

O unitário de cada procedimento é **o valor do Serviço Ambulatorial da Tabela do SUS
acrescido do percentual de incremento que o Anexo I fixa para ele**:

```
unitário = valor de tabela × (1 + incremento)
```

Na ultrassonografia mamária bilateral: R$ 24,20 × (1 + 3,13) = R$ 99,946.

**O centavo se trunca, não se arredonda.** R$ 99,946 vira **R$ 99,94**. É o número
que o usuário fixou em 15/09/2026 e é o critério conservador — o unitário declarado
nunca fica acima do que a fórmula produz. Aplicado às três bases de valor da fila:

| valor de tabela | incremento | produto | unitário declarado |
|---|---|---|---|
| R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| R$ 37,95 | 164% | R$ 100,188 | **R$ 100,18** |
| R$ 39,60 | 153% | R$ 100,188 | **R$ 100,18** |
| R$ 138,63 | 116% | R$ 299,4408 | **R$ 299,44** |
| R$ 136,41 | 120% | R$ 300,102 | **R$ 300,10** |

O incremento é desenho da própria portaria e não composição do plano: ele leva o
ultrassom de região isolada a R$ 100 e a tomografia a R$ 300, qualquer que seja a
base de tabela.

## A planilha por código — ultrassom

**Estado da v8, 22/09/2026.** Oito códigos, 65.120 exames. A ecografia de partes moles
(02.05.02.006-2, 2.974 exames, R$ 297.221,56) saiu do objeto por decisão do usuário —
será contemplada em outra OCI (D-007).

| código | procedimento | tabela | incr. | unitário | exames | valor |
|---|---|---|---|---|---|---|
| 02.05.02.009-7 | ULTRASSONOGRAFIA MAMARIA BILATERAL | R$ 24,20 | 313% | **R$ 99,94** | 14.608 | R$ 1.459.923,52 |
| 02.05.01.004-0 | ULTRASSONOGRAFIA DOPPLER COLORIDO DE VASOS | R$ 39,60 | 153% | **R$ 100,18** | 14.401 | R$ 1.442.692,18 |
| 02.05.02.004-6 | ULTRASSONOGRAFIA DE ABDOMEN TOTAL | R$ 37,95 | 164% | **R$ 100,18** | 13.080 | R$ 1.310.354,40 |
| 02.05.02.018-6 | ULTRASSONOGRAFIA TRANSVAGINAL | R$ 24,20 | 313% | **R$ 99,94** | 10.481 | R$ 1.047.471,14 |
| 02.05.02.005-4 | ULTRASSONOGRAFIA DE APARELHO URINARIO | R$ 24,20 | 313% | **R$ 99,94** | 3.921 | R$ 391.864,74 |
| 02.05.02.012-7 | ULTRASSONOGRAFIA DE TIREOIDE | R$ 24,20 | 313% | **R$ 99,94** | 3.195 | R$ 319.308,30 |
| 02.05.02.010-0 | ULTRASSONOGRAFIA DE PROSTATA POR VIA ABDOMINAL | R$ 24,20 | 313% | **R$ 99,94** | 3.185 | R$ 318.308,90 |
| 02.05.02.003-8 | ULTRASSONOGRAFIA DE ABDOMEN SUPERIOR | R$ 24,20 | 313% | **R$ 99,94** | 2.249 | R$ 224.765,06 |
| | **subtotal** | | | | **65.120** | **R$ 6.514.688,24** |

Dois códigos reúnem mais de um nome de fila: o doppler, com 9.793 dopplers venosos de
membros inferiores e 4.608 ecodopplers de carótidas; e o abdômen total, com 9.959
ecografias de abdômen total e 3.121 de parede abdominal. **A parede abdominal paga
R$ 100,18**, o unitário do código em que a SES-DF a registra — não os R$ 99,94 que
teria como ultrassom de região isolada.

## A planilha por código — tomografia

| código | procedimento | tabela | incr. | unitário | exames | valor |
|---|---|---|---|---|---|---|
| 02.06.03.001-0 | TC DE ABDOMEN SUPERIOR | R$ 138,63 | 116% | **R$ 299,44** | 4.453 | R$ 1.333.406,32 |
| 02.06.03.003-7 | TC DE PELVE / BACIA / ABDOMEN INFERIOR | R$ 138,63 | 116% | **R$ 299,44** | 3.808 | R$ 1.140.267,52 |
| 02.06.02.003-1 | TC DE TÓRAX | R$ 136,41 | 120% | **R$ 300,10** | 5.191 | R$ 1.557.819,10 |
| | **subtotal** | | | | **13.452** | **R$ 4.031.492,94** |

O tórax reúne 3.068 exames com contraste, 726 sem contraste e 1.397 angiotomografias de
coronárias. **O código é o mesmo e o preço é o mesmo**: a SES-DF registra a
angiotomografia sob o 02.06.02.003-1, e é esse o código que a planilha usa.

**O contraste não é faturado e continua sendo prestado.** O 02.06.03.004-5 vale
R$ 60,00, não está no Anexo I e portanto não carrega incremento; a descrição do
Anexo II destina o valor exclusivamente ao cálculo dos créditos financeiros do ATE, e
a execução aqui é por convênio. Os **12.726** exames que pedem contraste — 4.453 de
abdômen superior, 3.808 de pelve e 4.465 de tórax, angiotomografia incluída — somam
**R$ 763.560,00 pela referência da portaria**, custeados dentro do valor unitário.
Matéria da matriz de riscos (R-04); a dúvida fica registrada em L-004.

*Correção de 22/09/2026:* este arquivo e o `estado.yaml` diziam R$ 679.740,00, conta de
11.329 exames feita antes de a angiotomografia ganhar código (L-002). O número nunca
foi ao documento, que cita a contagem de 12.726 e não o valor.

## A soma dos procedimentos

| | exames | valor |
|---|---|---|
| Ultrassom — 8 códigos | 65.120 | R$ 6.514.688,24 |
| Tomografia — 3 códigos | 13.452 | R$ 4.031.492,94 |
| **Soma dos procedimentos** | **78.572** | **R$ 10.546.181,18** |

Média de R$ 134,22 por exame.
