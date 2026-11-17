# Valor de referência por procedimento

O valor de referência de cada exame é o valor do Serviço Ambulatorial da Tabela do SUS
acrescido do incremento que o **Anexo I da Portaria SAES/MS nº 4.282, de 19 de junho de
2026**, fixa para o procedimento, com o centavo truncado:

```
valor de referência = valor de tabela × (1 + incremento), truncado na segunda casa
```

| código | procedimento | valor de tabela | incremento | produto | valor de referência |
|---|---|---|---|---|---|
| 02.05.02.009-7 | Ultrassonografia mamária bilateral | R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| 02.05.01.004-0 | Ultrassonografia doppler colorido de vasos | R$ 39,60 | 153% | R$ 100,188 | **R$ 100,18** |
| 02.05.02.004-6 | Ultrassonografia de abdômen total | R$ 37,95 | 164% | R$ 100,188 | **R$ 100,18** |
| 02.05.02.018-6 | Ultrassonografia transvaginal | R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| 02.05.02.005-4 | Ultrassonografia de aparelho urinário | R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| 02.05.02.012-7 | Ultrassonografia de tireoide | R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| 02.05.02.010-0 | Ultrassonografia de próstata por via abdominal | R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| 02.05.02.003-8 | Ultrassonografia de abdômen superior | R$ 24,20 | 313% | R$ 99,946 | **R$ 99,94** |
| 02.06.03.001-0 | Tomografia computadorizada de abdômen superior | R$ 138,63 | 116% | R$ 299,4408 | **R$ 299,44** |
| 02.06.03.003-7 | Tomografia computadorizada de pelve, bacia e abdômen inferior | R$ 138,63 | 116% | R$ 299,4408 | **R$ 299,44** |
| 02.06.02.003-1 | Tomografia computadorizada de tórax | R$ 136,41 | 120% | R$ 300,102 | **R$ 300,10** |

São os mesmos do plano 4 (`planos/redacao_04/dados/valor_unitario.md`, fechado em
15/09/2026 contra o Anexo I e conferido em `conferencia_procedimentos.md`).

## Conferido em 09/10/2026

- **As portarias posteriores mantêm o incremento.** As Portarias SAES/MS nº 4.694 e nº
  4.695, de 13 de agosto de 2026 (NM-065 e NM-066), incluem o rol de imagem nos
  Componentes Ambulatorial e Ressarcimento "com os mesmos parâmetros remuneratórios e
  percentuais de incremento previstos no Anexo I da Portaria SAES/MS n.º 4.282".
- **O valor de tabela da competência 09/2026** confere nos dois códigos que estão em
  `registros/fontes/sigtap_enquadramento_092026.csv`: 02.05.01.004-0 a R$ 39,60 (38.01
  +153%) e 02.05.02.003-8 a R$ 24,20 (38.01 +313%).
- **A ficha SIGTAP de cada código não foi baixada**, como no plano 4 (dispensada pelo
  usuário em 17/09/2026). O pré-plano não afirma idade, sexo nem habilitação dos
  procedimentos. Ver `../pendencias.md`.

O contraste de tomografia (02.06.03.004-5, R$ 60,00, Anexo II) não entra como linha: é
custeado dentro do valor do exame, como no plano 4 (L-004 do plano 4).
