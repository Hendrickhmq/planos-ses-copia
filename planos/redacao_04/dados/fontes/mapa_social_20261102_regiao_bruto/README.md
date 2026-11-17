# Mapa Social, 02/11/2026 18:31:39 — dados brutos da coleta

fila de TC de abdômen superior (tc_abdomen); TC de pelve (tc_pelve); Ultrassonografia transfontanela (transfontanela); TC de pescoço (tc_pescoco); Ultrassonografia de abdômen superior (abdomen_superior); Ultrassonografia de bolsa escrotal (bolsa_escrotal); Ultrassonografia de aparelho urinário (urinario); Ultrassonografia de abdômen total (abdomen_total); Ultrassonografia de parede abdominal (parede); Doppler de carótidas, renais e outros (doppler_outros); Ultrassonografia de próstata por via abdominal (prostata); Ultrassonografia de tireoide (tireoide); Ultrassonografia mamária bilateral (mama); Doppler bilateral de membros (doppler_membros); Ultrassonografia pélvica (pelvica); TC de tórax, sem a angio coronária (tc_torax); TC de crânio (tc_cranio); TC de face (tc_face); Ultrassonografia transvaginal (transvaginal). Resumo em `../mapa_social_20261102_regiao.md`. Só contagens agregadas: nenhum CNS, CPF, nome ou data de nascimento.

| arquivo | o que é |
|---|---|
| `ordem.json` | a ordem de coleta, gravada pelo líder antes de chamar o agente (hash 3216986928) |
| `motor_parte_N.txt` | a saída do kit do motor, tirada do navegador pela área de transferência: 1 parte(s), cada uma com tamanho e hash djb2 no cabeçalho |
| `motor_20261102.json` | o JSON do motor (`ferramentas/ler_motor.py`): as partes conferidas, os nomes exatos e as datas em DD/MM/AAAA |
| `coleta_20261102.json` | o JSON da coleta no formato do método (`ferramentas/montar_coleta.py`), com as entradas que o montador usou (o enquadramento e a coleta anterior); é o que a conferência lê |
| `montagem.json` | a versão do montador e o hash djb2 de cada arquivo que ele gravou: a conferência K derruba a edição à mão |

Refazer, da raiz do repositório:

```bash
python3 ferramentas/ler_motor.py <esta pasta>
python3 ferramentas/montar_coleta.py <esta pasta>
python3 ferramentas/conferir_coleta.py <a pasta de cima>/mapa_social_20261102_regiao.md
```
