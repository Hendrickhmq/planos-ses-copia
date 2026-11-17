# Mapa Social, 04/11/2026 14:33:58 — dados brutos da coleta

fila de 1. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO (eco adulto); 2. ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER INFANTIL (eco infantil); 9. ECOCARDIOGRAFIA FETAL (eco fetal); 5. ECOCARDIOGRAFIA DE ESTRESSE ADULTO (eco de estresse); 7. ECOCARDIOGRAFIA TRANSEOFAGICA ADULTO (eco transesofágico adulto). Resumo em `../mapa_social_20261104_eco_filas.md`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.

| arquivo | o que é |
|---|---|
| `ordem.json` | a ordem de coleta, gravada pelo líder antes de chamar o agente (hash 3299284906) |
| `motor_parte_N.txt` | a saída do kit do motor, tirada do navegador pela área de transferência: 1 parte(s), cada uma com tamanho e hash djb2 no cabeçalho |
| `motor_20261104.json` | o JSON do motor (`ferramentas/ler_motor.py`): as partes conferidas, os nomes exatos e as datas em DD/MM/AAAA |
| `coleta_20261104.json` | o JSON da coleta no formato do método (`ferramentas/montar_coleta.py`), com as entradas que o montador usou (o enquadramento e a coleta anterior); é o que a conferência lê |
| `montagem.json` | a versão do montador e o hash djb2 de cada arquivo que ele gravou: a conferência K derruba a edição à mão |

Refazer, da raiz do repositório:

```bash
python3 ferramentas/ler_motor.py <esta pasta>
python3 ferramentas/montar_coleta.py <esta pasta>
python3 ferramentas/conferir_coleta.py <a pasta de cima>/mapa_social_20261104_eco_filas.md
```
