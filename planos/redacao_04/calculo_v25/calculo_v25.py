"""v25 do plano 4 (21/10/2026): o calculo da v24 com o quadro de gestao decidido em 21/10/2026.

Decisoes do usuario (21/10/2026), depois da orientacao do professor:
- a conta fica com seis polos de tomografia (a da v24A); tentar cinco so na execucao;
- quadro: Direcao Executiva, Coordenacao Assistencial e Coordenacao Administrativa e Financeira (sai a Operacional),
  tres supervisores de polo a 6.155 (um para dois polos), dez operadores de registro (cinco no pre-exame, cinco no
  pos-exame), seis assistentes administrativos (um por polo) e a assessoria, por 8 meses.

O metodo e o da v24 (calculo_v24.py), que roda aqui com o quadro novo; grava v25.json nesta pasta.
"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
V24 = os.path.join(AQUI, "..", "calculo_v24")
sys.path.insert(0, V24)
QUADRO_V25 = [("Direção Executiva de Projeto", 1, "14500.00", 1, "1.1.1"),
              ("Coordenação Assistencial", 1, "10500.00", 1, "1.1.2"),
              ("Supervisão de Polo Assistencial", 3, "6155.00", 1, "1.1.3"),
              ("Operador de registro de sistemas — pré-exame", 5, "4300.00", 2, "2.1.1"),
              ("Operador de registro de sistemas — pós-exame", 5, "4300.00", 3, "3.1.1"),
              ("Coordenação Administrativa e Financeira", 1, "8400.00", 6, "6.1.1"),
              ("Assessoria de Prestação de Contas", 1, "5455.00", 6, "6.1.2"),
              ("Assistente Administrativo", 6, "3200.00", 6, "6.1.3")]

src = open(os.path.join(V24, "calculo_v24.py"), encoding="utf-8").read()
assert "q = quadro(PROPOSTO, True, 8)" in src and 'os.path.join(AQUI, "v24.json")' in src
src = (src.replace("q = quadro(PROPOSTO, True, 8)", "q = QUADRO_V25")
          .replace('os.path.join(AQUI, "v24.json")', "SAIDA_V25")
          .replace('"_calculo_v24_tmp.py"', '"_calculo_v25_tmp.py"'))
exec(compile(src, "calculo_v24 (quadro da v25)", "exec"),
     {"__file__": os.path.join(V24, "calculo_v24.py"), "__name__": "__main__", "QUADRO_V25": QUADRO_V25,
      "SAIDA_V25": os.path.join(AQUI, "v25.json")})
