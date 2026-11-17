"""v23 (08/10/2026): a 4.16 com a sugestao da equipe, sem detalhar sala nem gerar obrigacao de obra.

- alinea (b): o projeto de blindagem aprovado e o laudo de levantamento radiometrico dos polos com
  tomografia passam a ser apresentados na formalizacao, junto com a licenca sanitaria. So dos polos com
  tomografia: o servico de ultrassonografia nao tem projeto de blindagem (RDC 611/2022, art. 8o, par. unico);
- alinea (h), nova: conformidade dos tomografos com a IN Anvisa 93/2021 e da estrutura fisica de cada polo
  com a RDC Anvisa 50/2002, no que couber a cada modalidade.

Aplica sobre a v22 descompactada; o modo marcado mostra so o que a v23 muda em relacao a v22.
uso: aplicar_v23.py <docx_v22_descompactado> limpo|marcado
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "calculo_v20"))
from docxlib import Doc, q  # noqa: E402

pasta, modo = sys.argv[1:3]
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))

# (b) acrescimo depois de "licenca sanitaria de cada polo", sem riscar o que ja estava
B_ANCORA = "licença sanitária de cada polo"
B_NOVO = (" e, nos polos com tomografia, projeto de blindagem aprovado pela vigilância sanitária e laudo de"
          " levantamento radiométrico,")
pb = d.find("(b)\t" + B_ANCORA)
i = d.text(pb).index(B_ANCORA) + len(B_ANCORA)
rs = d._isolate(pb, i - len("polo"), i)
nr = copy.deepcopy(rs[-1])
for ch in [c for c in nr if c.tag != q("rPr")]:
    nr.remove(ch)
t = nr.makeelement(q("t"))
nr.append(t)
d._set_t(t, B_NOVO)
d.mark_new(nr)
rs[-1].addnext(nr)

# (g) deixa de ser a ultima alinea: ponto final vira ponto e virgula
G = "(g)\tdesinfecção do transdutor endocavitário entre usuários"
pg = d.find(G)
ph = copy.deepcopy(pg)                      # copia antes de marcar a (g)
txt = d.text(pg)
d.replace(pg, ".", ";", desde=len(txt) - 1)

# (h) nova, com a formatacao da (g)
H = ("conformidade dos tomógrafos com a Instrução Normativa Anvisa nº 93, de 27 de maio de 2021, e da"
     " estrutura física de cada polo com a RDC Anvisa nº 50, de 21 de fevereiro de 2002, no que couber"
     " a cada modalidade.")
r = d.runs(ph)[0]
ts = r.findall(q("t"))
d._set_t(ts[0], "(h)")
d._set_t(ts[1], H)
d.mark_new(r)
pg.addnext(ph)

d.save()
print(f"v23 {modo}: (b) acrescida, (g) com ponto e virgula, (h) nova")
