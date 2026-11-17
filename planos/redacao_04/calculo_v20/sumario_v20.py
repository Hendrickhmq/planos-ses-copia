"""Atualiza as paginas do sumario da v20 (o sumario da v6 e texto fixo, sem campo TOC).

uso: sumario_v20.py <docx_descompactado> limpo|marcado <pdf_v6> <pdf_v20_limpo>

A pagina nova de cada titulo = pagina do sumario da v6 + deslocamento medido nos dois PDFs
renderizados pelo LibreOffice. Assim a calibragem do Word, que gerou o sumario da v6, se mantem.
"""
import sys, os, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docxlib import Doc

pasta, modo, pdf6, pdf20 = sys.argv[1:5]
d = Doc(os.path.join(pasta, "word", "document.xml"), marcado=(modo == "marcado"))
LINHA = re.compile(r"^(\d+(?:\.\d+)?\.? .+?)\t(\d+)$")


def paginas(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout)[1])
    return [subprocess.run(["pdftotext", "-layout", "-f", str(k), "-l", str(k), pdf, "-"], capture_output=True,
                           text=True).stdout for k in range(1, n + 1)]


def pagina_do_titulo(pags, titulo):
    alvo = re.sub(r"\s+", " ", titulo).strip()
    for k, txt in enumerate(pags, start=1):
        for ln in txt.splitlines():
            s = re.sub(r"\s+", " ", ln).strip()
            # a linha do proprio sumario termina com o numero da pagina; o titulo no corpo, nao
            if s.startswith(alvo) and not re.fullmatch(r"[ .]*\d{1,3}", s[len(alvo):]):
                return k
    raise ValueError(f"titulo nao achado: {titulo!r}")


p6, p20 = paginas(pdf6), paginas(pdf20)
mudou = 0
for p in d.paragraphs():
    m = LINHA.match(d.text(p))
    if not m:
        continue
    titulo, pag = m[1], int(m[2])
    nova = pag + pagina_do_titulo(p20, titulo) - pagina_do_titulo(p6, titulo)
    if nova != pag:
        txt = d.text(p)
        d.replace(p, str(pag), str(nova), desde=len(txt) - len(str(pag)))
        mudou += 1
d.save()
print(f"sumario: {mudou} paginas atualizadas")
