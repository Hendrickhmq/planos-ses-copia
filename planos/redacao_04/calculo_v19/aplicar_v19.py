"""v19 do plano 4: valor da emenda de bancada (R$ 13.095.449,00), cenario G, apoio com +1 operador
e +2 assistentes, rateio da v18. Uso: aplicar_v19.py <docx_descompactado> limpo|marcado"""
import copy, sys
from pathlib import Path
from lxml import etree

UN = Path(sys.argv[1]); MARCA = sys.argv[2] == "marcado"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XS = "{http://www.w3.org/XML/1998/namespace}space"
q = lambda t: f"{{{W}}}{t}"
ORDER = ["rStyle","rFonts","b","bCs","i","iCs","caps","smallCaps","strike","dstrike","outline","shadow","emboss",
         "imprint","noProof","snapToGrid","vanish","webHidden","color","spacing","w","kern","position","sz","szCs",
         "highlight","u","effect","bdr","shd","fitText","vertAlign","rtl","cs","em","lang","eastAsianLayout"]

def set_rpr(run, tag, val=None, remove=False, attrs=None):
    rpr = run.find(q("rPr"))
    if rpr is None:
        rpr = etree.Element(q("rPr")); run.insert(0, rpr)
    old = rpr.find(q(tag))
    if old is not None: rpr.remove(old)
    if remove: return
    el = etree.Element(q(tag))
    if val is not None: el.set(q("val"), val)
    for k, v in (attrs or {}).items(): el.set(q(k), v)
    pos = len(rpr)
    for i, ch in enumerate(rpr):
        n = etree.QName(ch).localname
        if n in ORDER and ORDER.index(n) > ORDER.index(tag): pos = i; break
    rpr.insert(pos, el)

def runs_of(p): return [(r, "".join(t.text or "" for t in r.findall(q("t")))) for r in p.findall(q("r"))]
def ptext(p): return "".join(t for _, t in runs_of(p))

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

def novo_run(tmpl_rpr, texto, negrito=None):
    r = etree.Element(q("r"))
    if tmpl_rpr is not None: r.append(copy.deepcopy(tmpl_rpr))
    if negrito is False:
        set_rpr(r, "b", remove=True); set_rpr(r, "bCs", remove=True)
    t = etree.SubElement(r, q("t")); t.text = texto; t.set(XS, "preserve")
    set_rpr(r, "strike", remove=True)
    if MARCA: set_rpr(r, "highlight", "yellow")
    else: set_rpr(r, "highlight", remove=True)
    return r

def trocar_em(p, velho, novo):
    tx = ptext(p); assert tx.count(velho) == 1, (velho[:60], tx[:80])
    i = tx.index(velho); sel = isolate(p, i, i + len(velho))
    tmpl = copy.deepcopy(sel[0].find(q("rPr")))
    if MARCA:
        for r in sel:
            set_rpr(r, "highlight", remove=True); set_rpr(r, "strike"); set_rpr(r, "color", "9C0006")
            set_rpr(r, "shd", "clear", attrs={"color": "auto", "fill": "FFC7CE"})
        if novo and not velho.endswith(" ") and not novo.startswith(" "):
            lt = sel[-1].findall(q("t"))[-1]; lt.text = (lt.text or "") + " "; lt.set(XS, "preserve")
        if novo: sel[-1].addnext(novo_run(tmpl, novo))
    else:
        t = sel[0].find(q("t")); t.text = novo; t.set(XS, "preserve")
        for r in sel[1:]: r.getparent().remove(r)

ROOT = None
def paragrafos(): return list(ROOT.iter(q("p")))
def rep(velho, novo):
    alvo = [p for p in paragrafos() if velho in ptext(p)]
    assert len(alvo) == 1, (velho[:60], len(alvo))
    trocar_em(alvo[0], velho, novo)
    return alvo[0]

def inserir_apos(p_ref, texto, antes=False, negrito=None):
    np_ = etree.Element(q("p"))
    ppr = p_ref.find(q("pPr"))
    if ppr is not None: np_.append(copy.deepcopy(ppr))
    r0 = p_ref.find(q("r"))
    np_.append(novo_run(copy.deepcopy(r0.find(q("rPr"))) if r0 is not None else None, texto, negrito))
    (p_ref.addprevious if antes else p_ref.addnext)(np_)

def celtxt(tc): return "".join(t.text or "" for t in tc.iter(q("t"))).strip()
def tabela(*cab):
    for tb in ROOT.iter(q("tbl")):
        h = [celtxt(c) for c in tb.find(q("tr")).findall(q("tc"))]
        if all(x in h for x in cab): return tb
    raise KeyError(cab)
def linha(tb, chave, col=0):
    trs = tb.findall(q("tr"))
    if isinstance(chave, int): return trs[chave]
    achou = [tr for tr in trs if len(tr.findall(q("tc"))) > col and celtxt(tr.findall(q("tc"))[col]) == chave]
    assert len(achou) == 1, (chave, len(achou)); return achou[0]
def cel(tb, chave, col, novo, colchave=0):
    tc = linha(tb, chave, colchave).findall(q("tc"))[col]
    p = next(p for p in tc.iter(q("p")) if ptext(p).strip())
    velho = ptext(p)
    if velho.strip() != novo: trocar_em(p, velho, novo)

doc = UN / "word" / "document.xml"
tree = etree.parse(str(doc)); ROOT = tree.getroot()

if len(sys.argv) > 3 and sys.argv[3] == "com_texto":
    # as cinco correcoes de texto de 05/10/2026, para a copia marcada partir da v18
    rep("Emenda parlamentar federal [preencher: autor, número e RP]",
        "Emenda de Bancada do Distrito Federal (RP 7) nº 202571080005, OGU 2025 — propostas nº 36000722999202500 (R$ 1.502.687,00) e nº 36000720055202500 (R$ 11.592.762,00)")
    rep("O acesso venoso e a injeção do meio de contraste são feitos por enfermeiro ou técnico de enfermagem do polo, sob supervisão médica, conforme a Resolução CFM nº 2.147/2016.",
        "O acesso venoso e a injeção do meio de contraste são feitos por enfermeiro, ou por técnico de enfermagem sob supervisão do enfermeiro, e o exame segue sob supervisão do médico radiologista.")
    rep("acesso venoso e injeção, sob supervisão médica (5.5)", "acesso venoso e injeção, sob supervisão do enfermeiro (5.5)")
    rep(" — o que a afasta da leitura de taxa de administração.", ".")
    rep("até 3%, proposto pelo proponente", "até 3%")

# 1.2
rep("R$ 11.391.641,18", "R$ 13.095.356,94")
# 2.2
rep("O objeto é a realização de 78.572 exames", "O objeto é a realização de 88.518 exames")
tb = tabela("código", "procedimento", "exames")
nomes = {celtxt(tr.findall(q("tc"))[0]): celtxt(tr.findall(q("tc"))[1]) for tr in tb.findall(q("tr"))[1:-1]}
ordem = [("02.05.01.004-0","16.244"),("02.05.02.009-7","16.014"),("02.05.02.004-6","14.572"),("02.05.02.018-6","11.528"),
         ("02.06.02.003-1","6.048"),("02.06.03.001-0","5.552"),("02.06.03.003-7","4.759"),("02.05.02.005-4","4.321"),
         ("02.05.02.012-7","3.558"),("02.05.02.010-0","3.468"),("02.05.02.003-8","2.454")]
for i, (c, n) in enumerate(ordem, start=1):
    cel(tb, i, 0, c); cel(tb, i, 1, nomes[c]); cel(tb, i, 2, n)
cel(tb, -1, 2, "88.518")
rep("São 65.120 exames de ultrassonografia e 13.452 de tomografia computadorizada.",
    "São 72.159 exames de ultrassonografia e 16.359 de tomografia computadorizada.")
rep("Os quantitativos por procedimento são os da fila de regulação na data da extração.",
    "Os quantitativos por procedimento somam a fila de regulação na data da extração e parte das solicitações que entram na fila durante a vigência, na forma da subseção 3.1.")
# 3.1
p2 = rep("O convênio resolve a totalidade das 78.572 solicitações.",
         "O convênio resolve a totalidade das 78.572 solicitações da extração e atende mais 9.946 das que entram na fila durante a vigência, 88.518 exames ao todo.")
_ult = p2.findall(q("r"))[-1]
_ult.addnext(novo_run(copy.deepcopy(_ult.find(q("rPr"))), " O acréscimo se reparte entre os procedimentos na proporção das solicitações de 2026 que continuavam sem agendamento.", negrito=False))
inserir_apos(p2, "A fila se renova durante a execução. No Mapa Social da Saúde, consultado em 5 de outubro de 2026, entraram nas filas desses procedimentos 83.866 solicitações de janeiro a setembro de 2026, e 39.114 delas continuavam sem agendamento — cerca de 4.346 por mês.", antes=True, negrito=False)
# quadro do envelope, como no plano 3: clona a tabela da 1.2 (duas colunas)
modelo = tabela("procedimento", "espera média")
nova = copy.deepcopy(modelo)
trs = nova.findall(q("tr"))
dado_tr, forte_tr = trs[1], trs[-1]
for tr in trs[1:]: nova.remove(tr)
def escrever(tc, texto):
    ps = list(tc.iter(q("p"))); p = ps[0]
    for extra in ps[1:]: extra.getparent().remove(extra)
    rs = p.findall(q("r"))
    tmpl = copy.deepcopy(rs[0].find(q("rPr"))) if rs else None
    for r in rs: p.remove(r)
    p.append(novo_run(tmpl, texto))
linhas = [("composição", "valor"), ("Recurso disponível", "R$ 13.095.449,00"),
          ("Estrutura de gestão e apoio (seção 9)", "R$ 973.860,00"),
          ("Envelope de produção assistencial", "R$ 12.121.589,00"), ("Quantitativo", "88.518 exames"),
          ("Produção assistencial", "R$ 12.121.496,94"), ("Valor global", "R$ 13.095.356,94"),
          ("Diferença não aplicada", "R$ 92,06")]
cab_tr = nova.findall(q("tr"))[0]
for tc, tx in zip(cab_tr.findall(q("tc")), linhas[0]): escrever(tc, tx)
ant = cab_tr
for a, b in linhas[1:]:
    tr = copy.deepcopy(forte_tr if a in ("Quantitativo", "Valor global") else dado_tr)
    for tc, tx in zip(tr.findall(q("tc")), (a, b)): escrever(tc, tx)
    ant.addnext(tr); ant = tr
p2.addnext(nova)
frase = etree.Element(q("p"))
if p2.find(q("pPr")) is not None: frase.append(copy.deepcopy(p2.find(q("pPr"))))
r0 = p2.find(q("r"))
frase.append(novo_run(copy.deepcopy(r0.find(q("rPr"))) if r0 is not None else None,
    "A unidade produzida é indivisível e o valor global não excede o recurso disponível: a diferença, menor que o menor valor unitário, permanece não aplicada.", negrito=False))
nova.addnext(frase)
# 3.4
tb = tabela("polo", "Regiões de Saúde", "participação", "exames")
for polo, pct, ex in (("Ceilândia","39,74%","35.174"),("Sobradinho","30,07%","26.617"),("Gama","30,19%","26.727")):
    cel(tb, polo, 2, pct); cel(tb, polo, 3, ex)
cel(tb, "total", 3, "88.518")
# 5.5
rep("são 12.726 dos 13.452 exames de tomografia do objeto", "são 15.605 dos 16.359 exames de tomografia do objeto")
# 5.10
tb = tabela("postos", "cargo", "atuação")
cel(tb, "Operador de registro de sistemas", 0, "7", colchave=1)
cel(tb, "Assistente Administrativo", 0, "8", colchave=1)
rep("Os seis operadores de registro e os seis assistentes administrativos",
    "Os sete operadores de registro e os oito assistentes administrativos")
tb = tabela("posto", "Ceilândia", "Sobradinho", "Gama", "total")
for k, vals in (("Operador de registro de sistemas", ("3","2","2","7")), ("Assistente Administrativo", ("3","2","3","8")),
                ("por polo", ("6","4","5","15"))):
    for j, v in enumerate(vals, start=1): cel(tb, k, j, v)
# 5.13
tb = tabela("meta", "descrição", "quantitativo", "prazo")
cel(tb, "Meta 2", 2, "88.518 solicitações da fila agendadas")
cel(tb, "Meta 3", 2, "88.518 exames registrados nos sistemas oficiais")
cel(tb, "Meta 4", 2, "72.159 exames"); cel(tb, "Meta 5", 2, "16.359 exames")
rep("31.183 exames em Ceilândia, 23.527 em Sobradinho e 23.862 no Gama",
    "35.174 exames em Ceilândia, 26.617 em Sobradinho e 26.727 no Gama")
# 5.16
tb = tabela("posto assistencial", "total", "registro exigido e critério")
for j, v in enumerate(("16","6","5","5"), start=1): cel(tb, "Médico — ultrassonografia", j, v)
for j, v in enumerate(("5","2","2","1"), start=1): cel(tb, "Médico radiologista — tomografia", j, v)
rep("horas de sala da tomografia 1.928, 1.592 e 904 ÷ 1.800 h anuais (1,07; 0,88; 0,50)",
    "horas de sala da tomografia 2.349, 1.939 e 1.102 ÷ 1.800 h anuais (1,30; 1,08; 0,61)")
rep("as 24.106 horas de sala (9.176 em Ceilândia, 7.066 em Sobradinho e 7.864 no Gama)",
    "as 26.760 horas de sala (10.189 em Ceilândia, 7.855 em Sobradinho e 8.716 no Gama)")
rep("6 médicos em Ceilândia (9.176 ÷ 1.800 = 5,1), 4 em Sobradinho (7.066 ÷ 1.800 = 3,9) e 5 no Gama (7.864 ÷ 1.800 = 4,4), 15 no total",
    "6 médicos em Ceilândia (10.189 ÷ 1.800 = 5,7), 5 em Sobradinho (7.855 ÷ 1.800 = 4,4) e 5 no Gama (8.716 ÷ 1.800 = 4,8), 16 no total")
# 6.2
tb = tabela("trimestre", "meses", "exames")
for k, v in (("1º","22.127"),("2º","22.128"),("3º","22.131"),("4º","22.132"),("total","88.518")): cel(tb, k, 2, v)
# 6.3
rep("de 19.648 exames, corresponde a 312 exames por dia útil", "de 22.132 exames, corresponde a 352 exames por dia útil")
rep("requer 28.530 horas de sala no período — 24.106 de ultrassonografia e 4.424 de tomografia computadorizada",
    "requer 32.150 horas de sala no período — 26.760 de ultrassonografia e 5.390 de tomografia computadorizada")
tb = tabela("recurso", "total", "Ceilândia", "Sobradinho", "Gama", "como se obtém")
cap = {"Exames no período": ("88.518","35.174","26.617","26.727"),
       "de ultrassonografia": ("72.159","28.054","20.729","23.376"),
       "de tomografia computadorizada": ("16.359","7.120","5.888","3.351"),
       "Exames por mês — ultrassonografia": ("6.014","2.338","1.728","1.948"),
       "Exames por mês — tomografia computadorizada": ("1.365","594","491","280"),
       "Exames por dia útil — ultrassonografia": ("288","112","83","93"),
       "Exames por dia útil — tomografia computadorizada": ("67","29","24","14"),
       "Exames por sala de ultrassonografia por dia útil": (None,"23","21","24"),
       "Horas de sala de ultrassonografia": ("26.760","10.189","7.855","8.716"),
       "Exames por tomógrafo por dia útil": (None,"29","24","14"),
       "Horas de tomógrafo": ("5.390","2.349","1.939","1.102"),
       "Postos de trabalho lotados no polo": ("15","6","4","5")}
for k, vals in cap.items():
    for j, v in enumerate(vals, start=1):
        if v is not None: cel(tb, k, j, v)
p = [p for p in paragrafos() if ptext(p).startswith("Ceilândia realiza, por dia útil")]; assert len(p) == 1
trocar_em(p[0], ptext(p[0]), "Ceilândia realiza, por dia útil, 112 exames de ultrassonografia em cinco salas e 29 de tomografia computadorizada em um tomógrafo. Sobradinho realiza 83 exames de ultrassonografia em quatro salas e 24 de tomografia em um tomógrafo. O Gama realiza 93 exames de ultrassonografia em quatro salas e 14 de tomografia em um tomógrafo. Os três polos funcionam dez horas por dia útil; Ceilândia tem seis postos de gestão e apoio lotados, Sobradinho quatro e o Gama cinco.")
rep("de 260 exames de ultrassonografia e 55 de tomografia por dia útil, excede os 312",
    "de 288 exames de ultrassonografia e 67 de tomografia por dia útil, excede os 352")
rep("Aos doze postos lotados nos polos", "Aos quinze postos lotados nos polos")
rep("A carga agregada de 4.424 horas equivale a 1,76 tomógrafo", "A carga agregada de 5.390 horas equivale a 2,14 tomógrafos")
# 7.2
tb = tabela("parcela", "meses", "exames do período", "valor da parcela")
par = {"1": ("22.127","3.029.974,76","243.465,00","3.273.439,76"), "2": ("22.128","3.030.274,20","243.465,00","3.273.739,20"),
       "3": ("22.131","3.030.574,02","243.465,00","3.274.039,02"), "4": ("22.132","3.030.673,96","243.465,00","3.274.138,96")}
for k, vals in par.items():
    for j, v in enumerate(vals, start=2): cel(tb, k, j, v)
for j, v in enumerate(("88.518","12.121.496,94","973.860,00","13.095.356,94"), start=2): cel(tb, -1, j, v)
# 8.2 e 8.3
rep("ritmo de 312 exames por dia útil", "ritmo de 352 exames por dia útil")
rep("é de 78.572 solicitações, igual ao quantitativo pactuado na data da extração,",
    "é de 78.572 solicitações na data da extração, e o quantitativo pactuado de 88.518 inclui 9.946 exames das solicitações que entram na fila durante a vigência, na forma da mesma subseção,")
rep("uma carga de 1,76", "uma carga de 2,14")
rep("A meta de 78.572 exames em doze meses", "A meta de 88.518 exames em doze meses")
rep("insumo de 12.726 dos 13.452 exames de tomografia", "insumo de 15.605 dos 16.359 exames de tomografia")
# 9.2
tb = tabela("#", "item", "referência", "qtd", "v. total")
pl = {"2.1.1": ("8", "307.200,00"), "3.1.1": ("7", "361.200,00"),
      "4.1.1": ("16.014","1.600.439,16"), "4.1.2": ("16.244","1.627.323,92"), "4.1.3": ("14.572","1.459.822,96"),
      "4.1.4": ("11.528","1.152.108,32"), "4.1.5": ("4.321","431.840,74"), "4.1.6": ("3.558","355.586,52"),
      "4.1.7": ("3.468","346.591,92"), "4.1.8": ("2.454","245.252,76"),
      "5.1.1": ("5.552","1.662.490,88"), "5.1.2": ("4.759","1.425.034,96"), "5.1.3": ("6.048","1.815.004,80")}
for k, (qq, vt) in pl.items(): cel(tb, k, 4, qq); cel(tb, k, 7, vt)
for k, qq, vt in (("TOTAL DA META 2","8","307.200,00"),("TOTAL DA META 3","7","361.200,00"),
                  ("TOTAL DA META 4","72.159","7.218.966,30"),("TOTAL DA META 5","16.359","4.902.530,64")):
    cel(tb, k, 4, qq, colchave=1); cel(tb, k, 7, vt, colchave=1)
cel(tb, "TOTAL GERAL", 7, "13.095.356,94", colchave=1)
tb = tabela("meta", "valor")
for k, v in (("Meta 2 — Gestão da fila","307.200,00"),("Meta 3 — Registro da produção","361.200,00"),
             ("Meta 4 — Execução assistencial em ultrassonografia","7.218.966,30"),
             ("Meta 5 — Execução assistencial em tomografia computadorizada","4.902.530,64"),("VALOR GLOBAL","13.095.356,94")):
    cel(tb, k, 1, v)

tree.write(str(doc), xml_declaration=True, encoding="UTF-8", standalone=True)
print("ok", "marcado" if MARCA else "limpo")
