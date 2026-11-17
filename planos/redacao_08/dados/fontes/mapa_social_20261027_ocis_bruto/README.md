# Mapa Social, 27/10/2026 12:32:51 — dados brutos da coleta

fila de OCI 09.02.01.001-8 (OCI Avaliação de Risco Cirúrgico); OCI 09.02.01.002-6 (OCI Avaliação Cardiológica); OCI 09.02.01.003-4 (OCI Avaliação Diagnóstica Inicial - Síndrome Coronariana Crônica); OCI 09.02.01.004-2 (OCI Progressão da Avaliação Diagnóstica I - Síndrome Coronariana Crônica); OCI 09.02.01.005-0 (OCI Progressão da Avaliação Diagnóstica II - Síndrome Coronariana Crônica); OCI 09.02.01.006-9 (OCI Avaliação Diagnóstica - Insuficiência Cardíaca); OCI 09.02.01.007-7 (OCI Gestão do Pré-Operatório); OCI P-08 risco cirurgico sem recorte (Consulta de risco cirúrgico sem recorte de CID, para a 007-7 e a 001-8 (P-08)). Resumo em `../mapa_social_20261027_ocis.md`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.

| arquivo | o que é |
|---|---|
| `ordem.json` | a ordem de coleta, gravada pelo líder antes de chamar o agente (hash 1437565671) |
| `motor_parte_N.txt` | a saída do kit do motor, tirada do navegador pela área de transferência: 3 parte(s), cada uma com tamanho e hash djb2 no cabeçalho |
| `motor_20261027.json` | o JSON do motor (`ferramentas/ler_motor.py`): as partes conferidas, os nomes exatos e as datas em DD/MM/AAAA |
| `coleta_20261027.json` | o JSON da coleta no formato do método (`ferramentas/montar_coleta.py`), com as entradas que o montador usou (o enquadramento e a coleta anterior); é o que a conferência lê |
| `montagem.json` | a versão do montador e o hash djb2 de cada arquivo que ele gravou: a conferência K derruba a edição à mão |

Refazer, da raiz do repositório:

```bash
python3 ferramentas/ler_motor.py <esta pasta>
python3 ferramentas/montar_coleta.py <esta pasta>
python3 ferramentas/conferir_coleta.py <a pasta de cima>/mapa_social_20261027_ocis.md
```
