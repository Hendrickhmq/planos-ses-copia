"""Edicao de docx por XML (lxml) para a v20: troca de texto dentro de paragrafos preservando a
formatacao do run, clonagem de linha e de coluna de tabela, e modo marcado (amarelo = entrou;
riscado, fundo FFC7CE e letra 9C0006 = saiu), na convencao das copias marcadas v18 e v19."""
import copy
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W}


def q(tag):
    return f"{{{W}}}{tag}"


CONTENT = {q("t"), q("tab"), q("br"), q("cr"), q("noBreakHyphen"), q("softHyphen"), q("sym"),
           q("drawing"), q("fldChar"), q("instrText"), q("lastRenderedPageBreak"), q("footnoteReference")}


class Doc:
    def __init__(self, path, marcado=False):
        self.path = path
        self.tree = etree.parse(path)
        self.root = self.tree.getroot()
        self.body = self.root.find(q("body"))
        self.marcado = marcado
        self.log = []

    def save(self):
        self.tree.write(self.path, xml_declaration=True, encoding="UTF-8", standalone=True)

    # ---------- leitura ----------
    def paragraphs(self):
        return list(self.body.iter(q("p")))

    def tables(self):
        return list(self.body.iter(q("tbl")))

    @staticmethod
    def runs(p):
        return [r for r in p.iter(q("r")) if r.getparent().tag != q("rPr")]

    @staticmethod
    def run_text(r):
        s = []
        for ch in r:
            if ch.tag == q("t"):
                s.append(ch.text or "")
            elif ch.tag == q("tab"):
                s.append("\t")
        return "".join(s)

    def runs_all(self, el):
        """todos os runs de texto dentro de um elemento (linha de tabela, celula)"""
        return [r for r in el.iter(q("r")) if r.getparent().tag != q("rPr")]

    def text(self, p):
        return "".join(self.run_text(r) for r in self.runs(p))

    def find(self, contains, nth=None, within=None):
        base = within if within is not None else self.body
        hits = [p for p in base.iter(q("p")) if contains in self.text(p)]
        if nth is None:
            if len(hits) != 1:
                raise ValueError(f"{len(hits)} paragrafos com {contains!r}")
            return hits[0]
        return hits[nth]

    def table_with(self, contains):
        hits = [t for t in self.tables() if any(contains in self.text(p) for p in t.iter(q("p")))]
        if len(hits) != 1:
            raise ValueError(f"{len(hits)} tabelas com {contains!r}")
        return hits[0]

    # ---------- normalizacao de runs ----------
    def _explode(self, p):
        """um filho de conteudo por run; w:t longo fica inteiro"""
        for r in self.runs(p):
            kids = [ch for ch in r if ch.tag != q("rPr")]
            if len(kids) <= 1:
                continue
            rpr = r.find(q("rPr"))
            parent = r.getparent()
            idx = parent.index(r)
            for k, ch in enumerate(kids):
                nr = etree.Element(q("r"))
                if rpr is not None:
                    nr.append(copy.deepcopy(rpr))
                nr.append(copy.deepcopy(ch))
                parent.insert(idx + 1 + k, nr)
            parent.remove(r)

    @staticmethod
    def _set_t(t, s):
        t.text = s
        if s != s.strip() or "  " in s:
            t.set(f"{{{XML_NS}}}space", "preserve")
        else:
            t.attrib.pop(f"{{{XML_NS}}}space", None)

    def _split(self, r, at):
        """parte o run de texto r na posicao at; devolve (esq, dir)"""
        t = r.find(q("t"))
        s = t.text or ""
        if at <= 0 or at >= len(s):
            return None
        nr = copy.deepcopy(r)
        self._set_t(t, s[:at])
        self._set_t(nr.find(q("t")), s[at:])
        r.addnext(nr)
        return r, nr

    def _isolate(self, p, start, end):
        """runs que cobrem exatamente [start, end) do texto do paragrafo"""
        self._explode(p)
        pos = 0
        for r in self.runs(p):
            n = len(self.run_text(r))
            if r.find(q("t")) is not None:
                if pos < start < pos + n:
                    self._split(r, start - pos)
                    return self._isolate(p, start, end)
                if pos < end < pos + n:
                    self._split(r, end - pos)
                    return self._isolate(p, start, end)
            pos += n
        out, pos = [], 0
        for r in self.runs(p):
            n = len(self.run_text(r))
            if pos >= start and pos + n <= end and n:
                out.append(r)
            pos += n
        return out

    # ---------- marcas ----------
    @staticmethod
    def _rpr(r):
        rpr = r.find(q("rPr"))
        if rpr is None:
            rpr = etree.Element(q("rPr"))
            r.insert(0, rpr)
        return rpr

    ORDER = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline",
             "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing",
             "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText",
             "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"]

    def _put(self, rpr, tag, attrs):
        old = rpr.find(q(tag))
        if old is not None:
            rpr.remove(old)
        el = etree.Element(q(tag))
        for k, v in attrs.items():
            el.set(q(k), v)
        rank = self.ORDER.index(tag)
        for i, ch in enumerate(rpr):
            name = etree.QName(ch).localname
            if name in self.ORDER and self.ORDER.index(name) > rank:
                rpr.insert(i, el)
                return
        rpr.append(el)

    def mark_new(self, r):
        if self.marcado:
            self._put(self._rpr(r), "highlight", {"val": "yellow"})

    def mark_old(self, r):
        rpr = self._rpr(r)
        self._put(rpr, "strike", {"val": "1"})
        self._put(rpr, "color", {"val": "9C0006"})
        self._put(rpr, "shd", {"val": "clear", "color": "auto", "fill": "FFC7CE"})
        h = rpr.find(q("highlight"))
        if h is not None:
            rpr.remove(h)

    # ---------- edicao ----------
    def replace(self, p, old, new, count=1, desde=0):
        """troca old por new no paragrafo p (count ocorrencias; 0 = todas), a partir do caractere desde"""
        done = 0
        start_from = desde
        while True:
            txt = self.text(p)
            i = txt.find(old, start_from)
            if i < 0:
                break
            rs = self._isolate(p, i, i + len(old))
            if not rs:
                raise ValueError(f"nao isolou {old!r}")
            if self.marcado:
                if new:
                    nr = copy.deepcopy(rs[0])
                    for ch in [c for c in nr if c.tag != q("rPr")]:
                        nr.remove(ch)
                    t = etree.SubElement(nr, q("t"))
                    self._set_t(t, new)
                    self.mark_new(nr)
                    rs[-1].addnext(nr)
                for r in rs:
                    self.mark_old(r)
                extra = 0
                t = rs[-1].find(q("t"))
                if new and t is not None and not (t.text or "").endswith(" "):
                    self._set_t(t, (t.text or "") + " ")   # espaco riscado entre o que sai e o que entra
                    extra = 1
                start_from = i + len(old) + extra + len(new)
            else:
                first = rs[0]
                self._set_t(first.find(q("t")), new)
                for r in rs[1:]:
                    r.getparent().remove(r)
                if not new:
                    first.getparent().remove(first)
                start_from = i + len(new)
            done += 1
            if count and done >= count:
                break
        if done == 0:
            raise ValueError(f"{old!r} nao encontrado em {self.text(p)[:90]!r}")
        self.log.append((old, new, done))
        return done

    def sub(self, contains, old, new, count=1, nth=None, within=None):
        return self.replace(self.find(contains, nth=nth, within=within), old, new, count)

    def set_cell(self, tc, new, novo=False):
        """texto inteiro da celula (primeiro paragrafo); novo=True marca tudo como entrou"""
        ps = tc.findall(q("p"))
        p = ps[0]
        for extra in ps[1:]:
            tc.remove(extra)
        old = self.text(p)
        if novo:
            rs = self.runs(p)
            if not rs:
                r = etree.SubElement(p, q("r"))
                etree.SubElement(r, q("t"))
                rs = [r]
            self._explode(p)
            rs = [r for r in self.runs(p) if r.find(q("t")) is not None] or self.runs(p)
            self._set_t(rs[0].find(q("t")), new)
            for r in rs[1:]:
                r.getparent().remove(r)
            self.mark_new(rs[0])
        elif old != new:
            if old:
                self.replace(p, old, new)
            else:
                r = etree.SubElement(p, q("r"))
                self._set_t(etree.SubElement(r, q("t")), new)
                self.mark_new(r)

    # ---------- tabelas ----------
    @staticmethod
    def rows(tbl):
        return tbl.findall(q("tr"))

    @staticmethod
    def cells(tr):
        return tr.findall(q("tc"))

    def clone_row(self, tbl, i, after=None):
        rows = self.rows(tbl)
        nr = copy.deepcopy(rows[i])
        (rows[after] if after is not None else rows[i]).addnext(nr)
        return nr

    def insert_columns(self, tbl, src, after, n, widths=None):
        """insere n colunas copiadas da coluna src depois da coluna after; widths = largura de
        todas as colunas finais (dxa), aplicada no tblGrid e em cada tcW"""
        for tr in self.rows(tbl):
            cs = self.cells(tr)
            anchor = cs[after]
            for k in range(n):
                nc = copy.deepcopy(cs[src])
                anchor.addnext(nc)
                anchor = nc
        grid = tbl.find(q("tblGrid"))
        cols = grid.findall(q("gridCol"))
        anchor = cols[after]
        for k in range(n):
            g = copy.deepcopy(cols[src])
            anchor.addnext(g)
            anchor = g
        if widths:
            self.set_widths(tbl, widths)

    def set_widths(self, tbl, widths):
        grid = tbl.find(q("tblGrid"))
        for g, wd in zip(grid.findall(q("gridCol")), widths):
            g.set(q("w"), str(wd))
        for tr in self.rows(tbl):
            for tc, wd in zip(self.cells(tr), widths):
                tcpr = tc.find(q("tcPr"))
                tcw = tcpr.find(q("tcW")) if tcpr is not None else None
                if tcw is not None:
                    tcw.set(q("w"), str(wd))
                    tcw.set(q("type"), "dxa")
        tblw = tbl.find(q("tblPr")).find(q("tblW"))
        if tblw is not None:
            tblw.set(q("w"), str(sum(widths)))
            tblw.set(q("type"), "dxa")
