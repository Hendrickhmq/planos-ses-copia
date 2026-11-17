"""Refaz, no topo de cada módulo do curso, a lista das notas do cofre que citam o módulo.
Uso: python3 ferramentas/cofre/blocos_dos_modulos.py .   (na raiz do repositório)"""
import re, sys
from pathlib import Path
R=Path(sys.argv[1]); idx={}
for p in (R/"conhecimento").rglob("*.md"):
    t=p.read_text(encoding="utf-8"); fm=t.split("---",2)[1] if t.startswith("---") else ""
    tipo=re.search(r"tipo: (\w+)",fm)
    for m in re.findall(r"\[\[(\d\d)_[a-z_]+\|Módulo \d+\]\]", t):
        idx.setdefault(int(m),[]).append((tipo.group(1) if tipo else "", p.stem))
rot={"conceito":"Conceitos","norma":"Normas","órgão":"Órgãos","caso":"Casos","plano":"Planos"}
for p in sorted((R/"curso/modulos").glob("*.md")):
    n=int(p.name[:2]); t=p.read_text(encoding="utf-8")
    t=re.sub(r"\n\*\*No cofre\.\*\*.*?(?=\n---\n)", "\n", t, flags=re.S).replace("\n\n\n---\n","\n\n---\n")
    grupos=[f"- {r}: "+" · ".join(f"[[{s}]]" for s in sorted({s for tp,s in idx.get(n,[]) if tp==k})) for k,r in rot.items() if any(tp==k for tp,_ in idx.get(n,[]))]
    bloco="**No cofre.** As notas deste módulo, com as definições e os links ([[Início]]):\n\n"+"\n".join(grupos)+"\n"
    i=t.index("\n---\n"); t=t[:i]+"\n"+bloco+t[i:]
    p.write_text(t,encoding="utf-8"); print(p.name[:2], sum(g.count("[[") for g in grupos))
