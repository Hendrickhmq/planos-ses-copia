# Tabela SUS Candanga

O Anexo Único da Deliberação CG-SES-DF 46/2026 (DODF 178, de 24/09/2026; Lei distrital
7.897/2026): a Tabela SUS Candanga oficial, com código, descrição, modalidade e Valor Tabela
SUS Candanga (art. 15). É a "Tabela - SES/SECCIC" do processo SEI 00060-00238687/2026-88,
documento 212117347, assinado em 24/08/2026, 57 páginas, recebida do usuário em 01/11/2026.

| arquivo | o que é |
|---|---|
| `Anexo Unico Tabela SUS Candanga SEI 212117347.pdf` | o PDF do SEI, a fonte |
| `tabela_sus_candanga.csv` | a tabela para busca e para os agentes |
| `tabela_sus_candanga.xlsx` | a mesma tabela para a equipe, com filtro e a aba "Leia" |
| `analise_comparativa_20260806/` | o estudo da SES que precedeu o Anexo (abaixo) |

São 2.952 linhas: 840 SIA, 1.895 SIH, 187 OPME e 30 medicamentos. O Anexo repete quatro
itens nas páginas 55 e 56, com o mesmo valor; a tabela fica com a primeira linha.

Gerados por `ferramentas/extrair_candanga.py`. Quando sair versão nova, rodar de novo:

```
python3 ferramentas/extrair_candanga.py "<pdf>" biblioteca/precos/tabela_sus_candanga/
```

## Como buscar

Pelo código de 10 dígitos, sem pontos:

```
grep 0205020046 biblioteca/precos/tabela_sus_candanga/tabela_sus_candanga.csv
```

Pelo nome, sem acento e em maiúsculas, como o SIGTAP escreve
(`grep -i "ULTRASSONOGRAFIA DE ABDOMEN"`). Os nomes das OCI têm acento.

## As colunas

| coluna | o que é |
|---|---|
| `codigo`, `codigo_sigtap` | o código, sem e com pontos |
| `procedimento` | a descrição do Anexo |
| `modalidade` | SIA, SIH, OPME ou Medicamento |
| `valor` | o Valor Tabela SUS Candanga |
| `sigtap_vigente`, `alerta` | nas OCI, o SIGTAP de 09/2026 do catálogo (`registros/fontes/sigtap_grupo09_092026.csv`) e o aviso de quando ele é igual ou maior que o valor do Anexo |
| `pagina` | a página do PDF, para a citação |

## Qual valor usar

Desde 01/11/2026, o valor unitário dos planos é o da Candanga, **na emenda federal e na
distrital** (lição LI-002, trava F-04). O valor do Anexo é o que a SES-DF paga: ele já contém
o SIGTAP, e a complementação distrital é a diferença (Deliberação 46/2026, art. 4º, § 5º).
Três cuidados:

1. **A modalidade.** O mesmo código pode vir no SIA e no SIH, e 116 códigos têm valor
   diferente em cada uma. Use a do objeto: exame e OCI de ambulatório são SIA.
2. **O SIGTAP vigente.** Se ele for igual ou maior que o valor do Anexo, a complementação é
   zero e vale o SIGTAP (Lei 7.897/2026, art. 4º, §§ 1º e 3º). Nas OCI a coluna `alerta`
   marca as 12 que estão assim em 09/2026; por exemplo, a 09.04.01.003-1 vale R$ 255,61 no
   Anexo e R$ 393,55 no SIGTAP. Nos outros grupos, a ficha vigente
   (`metodo/coleta/ficha_sigtap.md`) diz o SIGTAP.
3. **Código fora do Anexo.** Vale o SIGTAP da ficha (e o incremento da portaria, no exame), e
   a citação diz que o código não está na Candanga.

A citação:

> 02.05.02.004-6 Ultrassonografia de abdômen total: R$ 117,51 — Tabela SUS Candanga, Anexo
> Único da Deliberação CG-SES 46/2026 (SEI 212117347), SIA, p. 5

## A análise comparativa de 06/08/2026

`analise_comparativa_20260806/` guarda o PDF que a SES-DF distribuiu antes do Anexo
("ANÁLISE COMPARATIVA - TABELA SUS CANDANGA (SIA)", 843 procedimentos ambulatoriais, com
SIGTAP, IVR, PATE, CBHPM, Tabela SUS Paulista, Deliberações e IPCA por linha) e a tabela
tirada dele. De 27/10 a 31/10/2026 o método usou o **Valor Máximo** dessa análise como se
fosse a Candanga, e ele não é: o ultrassom de abdômen total vale R$ 334,88 no Máximo e
R$ 117,51 no Anexo. As referências da análise servem só como comparação de mercado.

## A conferência da extração

O extrator lê cada página duas vezes, pela tabela e pelo texto corrido, e para se a contagem
de códigos não bater, se faltar valor ou se a modalidade for outra. Em 01/11/2026 as 57
páginas bateram.
