# Mapa Social, 27/10/2026 16:32:47 — dados brutos da coleta

fila de OCI 003-4 caso 1 (OCI 003-4, linha coronária, só a consulta (I20 a I25)); OCI 003-4 caso 2 (OCI 003-4, linha coronária, consulta e obrigatórios da 003-4 (I20 a I25)); OCI 006-9 caso 1 I50 (OCI 006-9, só a consulta (I50)); OCI 006-9 caso 2 I50 (OCI 006-9, consulta e obrigatórios (I50)); OCI 006-9 caso 1 I50 com I11.0, I13.0 e I13.2 (OCI 006-9, só a consulta (I50 com I11.0, I13.0 e I13.2)); OCI 006-9 caso 2 I50 com I11.0, I13.0 e I13.2 (OCI 006-9, consulta e obrigatórios (I50 com I11.0, I13.0 e I13.2)); OCI 006-9 caso 1 IC ampliada (OCI 006-9, só a consulta (IC ampliada)); OCI 006-9 caso 2 IC ampliada (OCI 006-9, consulta e obrigatórios (IC ampliada)); OCI 002-6 pelo ECG (OCI 002-6, a consulta e o eletrocardiograma com Z13.6 ou Z84.8); OCI P-08 risco cirurgico (Consulta de risco cirúrgico inteira, para a 007-7 (P-08)). Resumo em `../mapa_social_20261027_porta.md`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.

| arquivo | o que é |
|---|---|
| `ordem.json` | a ordem de coleta, gravada pelo líder antes de chamar o agente (hash 263537019) |
| `motor_parte_N.txt` | a saída do kit do motor, tirada do navegador pela área de transferência: 3 parte(s), cada uma com tamanho e hash djb2 no cabeçalho |
| `motor_20261027.json` | o JSON do motor (`ferramentas/ler_motor.py`): as partes conferidas, os nomes exatos e as datas em DD/MM/AAAA |
| `coleta_20261027.json` | o JSON da coleta no formato do método (`ferramentas/montar_coleta.py`), com as entradas que o montador usou (o enquadramento e a coleta anterior); é o que a conferência lê |
| `montagem.json` | a versão do montador e o hash djb2 de cada arquivo que ele gravou: a conferência K derruba a edição à mão |

Refazer, da raiz do repositório:

```bash
python3 ferramentas/ler_motor.py <esta pasta>
python3 ferramentas/montar_coleta.py <esta pasta>
python3 ferramentas/conferir_coleta.py <a pasta de cima>/mapa_social_20261027_porta.md
```
