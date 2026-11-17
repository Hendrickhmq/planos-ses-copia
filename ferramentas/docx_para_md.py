import sys, zipfile, re, xml.etree.ElementTree as ET
W="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
def txt(el):
    out=[]
    for n in el.iter():
        if n.tag==W+"t": out.append(n.text or "")
        elif n.tag==W+"tab": out.append("\t")
        elif n.tag==W+"br": out.append("\n")
        elif n.tag==W+"drawing": out.append("[IMAGEM]")
    return "".join(out)
z=zipfile.ZipFile(sys.argv[1]); body=ET.fromstring(z.read("word/document.xml")).find(W+"body")
out=[]
for el in body:
    if el.tag==W+"p":
        st=el.find(W+"pPr/"+W+"pStyle"); st=st.get(W+"val") if st is not None else ""
        t=txt(el).strip()
        if not t: continue
        if re.search(r"t[ií]?t?ulo1|Heading1",st,re.I): out.append("## "+t)
        elif re.search(r"t[ií]?t?ulo2|Heading2",st,re.I): out.append("### "+t)
        else: out.append(("- " if el.find(W+"pPr/"+W+"numPr") is not None else "")+t)
    elif el.tag==W+"tbl":
        rows=[]
        for k,tr in enumerate(el.findall(W+"tr")):
            cells=[txt(tc).strip().replace("\n"," ") for tc in tr.findall(W+"tc")]
            rows.append("| "+" | ".join(cells)+" |")
            if k==0: rows.append("|"+"---|"*len(cells))
        out.append("\n".join(rows))
md="\n\n".join(out)
md=re.sub(r"^Plano de Trabalho\n\n","# Plano de Trabalho\n\n",md,count=1)
print(md)
