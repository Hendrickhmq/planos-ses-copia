"""Aplica a v26 sobre a v25A (versoes/plano_v25a_20261021.docx, descompactada).

uso: aplicar_v26.py <docx_descompactado> limpo|marcado

Pedido do usuario em 21/10/2026, para enviar o plano a SES-DF (D-008):
- plano de trabalho, nao pre-plano: a capa deixa de se declarar "Pre-Plano de Trabalho encaminhado em atendimento ao
  Oficio n 387/2026"; o 1.7 e a 4.2 dizem "deste plano de trabalho";
- a proposta certa: o Oficio 387/2026 SES/GAB/ARINS e da proposta 36000722999202500 (R$ 1.502.687,00, redacao_07); a
  do plano 4 e a 36000720055202500 (R$ 11.592.762,00), com indicacao do ISHP pelo Oficio 40/2026. Saem as tres
  remissoes ao 387 (capa, 3.3, 3.6 e 4.1);
- convenio (LI-026): o 1.8 com o texto da SUCONV, o mesmo dos pre-planos 05, 06 e 07; a 3.3 sem a alternativa do
  Termo de Fomento (Lei 13.019 e Decreto 37.843); "formalizacao do convenio"; "parceria" sai da prosa do plano.
Numeros nao mudam: e a v25A com outra redacao nesses trechos.
"""
import sys, os
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "calculo_v20"))
from docxlib import Doc, q

pasta, modo = sys.argv[1], sys.argv[2]
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))
# os do 1.7 e da 4.2 mudam junto com o "pré-plano", logo abaixo
FORMALIZA = [p for p in d.paragraphs() if "formalização do instrumento" in d.text(p) and "pré-plano" not in d.text(p)]
assert len(FORMALIZA) == 6, len(FORMALIZA)

# ================= capa =================
d.sub("Pré-Plano de Trabalho encaminhado em atendimento",
      "Pré-Plano de Trabalho encaminhado em atendimento ao Ofício nº 387/2026 – SES/GAB/ARINS, de 2 de outubro de 2026",
      "Plano de Trabalho da Proposta nº 36000720055202500, com indicação do ISHP pelo Ofício nº 40/2026 do Senado "
      "Federal, de 22 de setembro de 2026")

# ================= 1.7 e 1.8 =================
d.sub("O CNES dos estabelecimentos de cada polo de execução não consta deste pré-plano",
      "deste pré-plano e será informado na formalização do instrumento",
      "deste plano de trabalho e será informado na formalização do convênio")
p18 = d.find("o que o enquadra na definição de organização da sociedade civil")
d.set_cell(p18.getparent(), "Sim. O ISHP se enquadra como OSC mas não será utilizado esse normativo por se tratar de um "
                            "convênio. Decreto N.º 48.727, de 09 de junho de 2026")

# ================= 3.3 Modalidade =================
d.sub("O instrumento jurídico da parceria — Termo de Fomento",
      "O instrumento jurídico da parceria — Termo de Fomento, na forma da Lei nº 13.019/2014 e do Decreto Distrital nº "
      "37.843/2016, ou Convênio, na forma da Lei nº 14.133/2021 — será definido pela Subsecretaria de Parcerias e "
      "Convênios (SUCONV) da SES-DF, após a análise deste pré-plano, conforme o item 5 do Ofício nº 387/2026. O plano é "
      "elaborado para custeio da média e alta complexidade (item 3 do mesmo Ofício). Qualquer que seja o instrumento, o "
      "pagamento observa",
      "O instrumento é o convênio, regido pelo Decreto Distrital nº 48.727, de 9 de junho de 2026, por se tratar de "
      "prestação de serviço assistencial complementar ao Sistema Único de Saúde. O plano é elaborado para custeio da "
      "média e alta complexidade, e o pagamento observa")

# ================= 3.6 e 4.1: sem o Ofício 387 =================
d.sub("determina a observância da Portaria GM/MS nº 10.297",
      "O Ofício nº 387/2026 determina a observância da Portaria GM/MS nº 10.297, de 27 de fevereiro de 2026. O art. 7º "
      "da Portaria exige",
      "O plano observa a Portaria GM/MS nº 10.297, de 27 de fevereiro de 2026, cujo art. 7º exige")
d.sub("Nível de atenção. O projeto se situa na Atenção Especializada",
      " indicada no Ofício nº 387/2026 (item 3)", "")

# ================= 4.2 =================
d.sub("o CNES do estabelecimento de cada polo não constam deste pré-plano",
      "deste pré-plano e serão informados na formalização do instrumento",
      "deste plano de trabalho e serão informados na formalização do convênio")

# ================= formalização do convênio (1.9, 3.12, 4.15 e 4.16) =================
for p in FORMALIZA:
    d.replace(p, "formalização do instrumento", "formalização do convênio", count=0)

# ================= "parceria" sai da prosa =================
d.sub("A parceria resolve a totalidade das", "A parceria resolve", "O convênio resolve")
d.sub("a parceria não seleciona usuário", "a parceria não seleciona usuário", "o proponente não seleciona usuário")
d.sub("A parceria não capta demanda própria", "A parceria não capta", "O proponente não capta")
d.sub("não instrumento criado para a parceria", "criado para a parceria", "criado para o convênio")

restos = [d.text(p) for p in d.paragraphs() if any(k in d.text(p) for k in ("pré-plano", "Pré-Plano", "387/2026",
                                                                              "13.019", "37.843", "Termo de Fomento"))]
assert d.marcado or not restos, restos
d.save()

# a propriedade "Assunto" do arquivo citava o Ofício 387
core = os.path.join(pasta, "docProps", "core.xml")
s = open(core, encoding="utf-8").read()
assert "Ofício nº 387/2026 SES/GAB/ARINS" in s
open(core, "w", encoding="utf-8").write(s.replace("Ofício nº 387/2026 SES/GAB/ARINS", "Proposta nº 36000720055202500"))
print(f"{modo}: {len(d.log)} trocas")
