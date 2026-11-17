"""v19, parte de texto: troca trechos dentro dos runs existentes, sem marcação.
O trecho antigo vira o texto novo no primeiro run que o contém; os demais runs do
trecho são removidos. A formatação é a do primeiro run."""
import copy, sys
from pathlib import Path
from lxml import etree

UN = Path(sys.argv[1])
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XS = "{http://www.w3.org/XML/1998/namespace}space"
q = lambda t: f"{{{W}}}{t}"

def runs_of(p):
    return [(r, "".join(t.text or "" for t in r.findall(q("t")))) for r in p.findall(q("r"))]

def ptext(p):
    return "".join(t for _, t in runs_of(p))

def explode(p):
    for r in p.findall(q("r")):
        if len(r.findall(q("t"))) < 2: continue
        rpr = r.find(q("rPr")); groups, cur = [], []
        for ch in [c for c in r if c is not rpr]:
            if etree.QName(ch).localname == "t" and any(etree.QName(c).localname == "t" for c in cur):
                groups.append(cur); cur = []
            cur.append(ch)
        groups.append(cur); at = r
        for g in groups:
            nr = etree.Element(q("r"))
            if rpr is not None: nr.append(copy.deepcopy(rpr))
            for ch in g: nr.append(ch)
            at.addnext(nr); at = nr
        r.getparent().remove(r)

def isolate(p, start, end):
    explode(p)
    for cut in (start, end):
        pos = 0
        for r, txt in runs_of(p):
            if pos < cut < pos + len(txt):
                t = r.find(q("t")); right = copy.deepcopy(r)
                t.text, right.find(q("t")).text = txt[:cut - pos], txt[cut - pos:]
                t.set(XS, "preserve"); right.find(q("t")).set(XS, "preserve")
                r.addnext(right); break
            pos += len(txt)
    sel, pos = [], 0
    for r, txt in runs_of(p):
        if txt and pos >= start and pos + len(txt) <= end: sel.append(r)
        pos += len(txt)
    return sel

def trocar(root, velho, novo, tirar_realce=False):
    alvo = [p for p in root.iter(q("p")) if velho in ptext(p)]
    assert len(alvo) == 1, (velho[:50], len(alvo))
    p = alvo[0]; i = ptext(p).index(velho)
    sel = isolate(p, i, i + len(velho))
    t = sel[0].find(q("t")); t.text = novo; t.set(XS, "preserve")
    if tirar_realce:
        rpr = sel[0].find(q("rPr"))
        if rpr is not None:
            for h in rpr.findall(q("highlight")): rpr.remove(h)
    for r in sel[1:]:
        r.getparent().remove(r)
    assert novo in ptext(p)

doc = UN / "word" / "document.xml"
tree = etree.parse(str(doc)); root = tree.getroot()

# 1.2 - origem do recurso (o campo ciano "[preencher...]" deixa de existir)
alvo = [p for p in root.iter(q("p")) if ptext(p).startswith("Emenda parlamentar federal [preencher")]
assert len(alvo) == 1
p = alvo[0]; velho = ptext(p)
sel = isolate(p, 0, len(velho))
t = sel[0].find(q("t"))
t.text = ("Emenda de Bancada do Distrito Federal (RP 7) nº 202571080005, OGU 2025 — propostas "
          "nº 36000722999202500 (R$ 1.502.687,00) e nº 36000720055202500 (R$ 11.592.762,00)")
t.set(XS, "preserve")
rpr = sel[0].find(q("rPr"))
if rpr is not None:
    for h in rpr.findall(q("highlight")): rpr.remove(h)
for r in sel[1:]: r.getparent().remove(r)

# ponto 1 - 5.5 e 5.16
trocar(root, "O acesso venoso e a injeção do meio de contraste são feitos por enfermeiro ou técnico de enfermagem do polo, sob supervisão médica, conforme a Resolução CFM nº 2.147/2016.",
       "O acesso venoso e a injeção do meio de contraste são feitos por enfermeiro, ou por técnico de enfermagem sob supervisão do enfermeiro, e o exame segue sob supervisão do médico radiologista.")
trocar(root, "acesso venoso e injeção, sob supervisão médica (5.5)",
       "acesso venoso e injeção, sob supervisão do enfermeiro (5.5)")
# ponto 2 - 8.3
trocar(root, "e o plano não publica percentual sobre o valor global — o que a afasta da leitura de taxa de administração.",
       "e o plano não publica percentual sobre o valor global.")
# ponto 3 - I-07
trocar(root, "até 3%, proposto pelo proponente", "até 3%")

tree.write(str(doc), xml_declaration=True, encoding="UTF-8", standalone=True)
print("ok")
