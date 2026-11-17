#!/usr/bin/env python3
"""
conferir.py - conferencia de integridade da extracao (extrair_planos.py e
extrair_digitalizados.py) e do tratamento (tratar_planos.py).

Nao altera nada. So le o PDF original, o texto.md e as CSVs, e imprime o
relatorio no stdout.

Uso:
    python conferir.py extraidos/ planos_aprovados/
    python conferir.py extraidos/ planos_aprovados/ --doc pt_ses_01
    python conferir.py extraidos/ planos_aprovados/ --sem-ocr      (so B, C, D, F, I)

Codigo de saida 1 quando alguma verificacao NUMERICA acusa - A com valor so de
um lado, C ou D que nao fecha, I com problema -, para que um script ou a
integracao continua possam parar ali. As de texto (B, E, F, G) sao avisos: o
que elas acusam pede leitura, nao e erro por si.

As letras daqui (A a I) sao as da extracao. As do conferir_plano.py (A a V) sao
outra lista, sobre o plano redigido: a mesma letra nao quer dizer a mesma coisa
nos dois.

Oito verificacoes. A I so tem o que conferir em normalizados/; as outras sete
rodam nos dois lados.

NUMERICAS
  A  LEITURA CRUZADA   renderiza a 300 dpi cada pagina com tabela, roda
                       Tesseract/por e compara os valores monetarios com os da
                       extracao nativa da mesma pagina (texto.md + CSVs).
  B  ESTRUTURA         linhas de largura diferente do cabecalho, linhas vazias,
                       colunas vazias. CSV de uma linha so nao entra no teste de
                       coluna vazia - la toda coluna sem dado e falso positivo.
  C  ARITMETICA        subtotal = soma dos itens do grupo; total geral = soma dos
                       subtotais. Acha o rotulo em QUALQUER coluna, casa
                       "SUBTOTAL" com "sub-total", e ENCADEIA paginas
                       consecutivas, porque a planilha atravessa varias paginas
                       e sai como uma CSV por pagina. Linha so com valor, sem
                       rotulo e sem descricao, e total de rotulo perdido, nao
                       item: le-la como item faz o subtotal seguinte contar o
                       valor duas vezes e acusar diferenca que nao existe.
  D  PRODUTO POR LINHA valor total = produto dos fatores da propria linha
                       (quantidade x frequencia x valor unitario). E o teste mais
                       forte: so fecha se cada numero estiver na coluna certa,
                       entao pega desalinhamento de coluna, que o A nao enxerga.

DE TEXTO
  E  COBERTURA         OCR de TODAS as paginas: das palavras que o OCR viu,
                       quantas existem na extracao nativa? Palavra ausente em
                       >=70% das paginas e timbre (papel timbrado e imagem), nao
                       perda de extracao - sai em lista separada e fora da conta.
  F  ARTEFATOS         quebras hifenizadas de fim de linha e palavras coladas.
                       Nao usa OCR.
  G  ORDEM DE LEITURA  palavras que ocorrem exatamente uma vez nas duas leituras
                       sao ancoras; compara a ordem relativa dos pares. Compara
                       SO contra o texto corrido do texto.md - anexar as CSVs no
                       fim embaralha por construcao e da alarme falso.

DA CONSOLIDACAO
  I  PLANILHA          roda sobre normalizados/<plano>/planilha.csv e confere o
     CONSOLIDADA       que as outras nao alcancam: a consolidacao em si. C e D
                       leem uma CSV por pagina, e cada CSV isolada pode estar
                       perfeita enquanto a juncao entre elas esta errada. Tres
                       partes: numeracao dos itens (buraco = linha perdida,
                       repeticao = linha contada duas vezes), hierarquia
                       fechando ponta a ponta com itens de paginas diferentes no
                       mesmo subtotal, e truncamento - consolidada que nao
                       termina em total geral e cadeia que parou cedo.
                       Sem planilha.csv, a verificacao nao se aplica e diz isso.

O OCR fica em cache fora da pasta do projeto (%TEMP%), indexado pelo sha256 do
PDF: a segunda execucao nao repete o reconhecimento.

Dependencias: pdfplumber, pytesseract, tesseract com idioma 'por'. Com
--sem-ocr o PDF nao e aberto: o numero de paginas sai do meta.yaml ou dos
marcadores de pagina do texto.md.
"""

import argparse
import csv
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from comum import (RE_MOEDA, identificar,
                   preparar_tesseract as _preparar_tesseract, reais,
                   saida_utf8, sem_acento, sha256_arquivo, valor_moeda)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

DPI_OCR = 300

# Palavra ausente nesta fracao das paginas ou mais e timbre, nao perda.
LIMIAR_TIMBRE = 0.70

# Tamanho minimo de palavra considerada nas verificacoes de texto.
MIN_LETRAS = 4

# Minimo de ancoras para a pagina ser mensuravel no teste de ordem. Com 2
# ancoras existe UM par: o escore so pode dar 0% ou 100% e nao mede nada. Com 10
# ancoras sao 45 pares. Paginas quase inteiramente de tabela ficam abaixo disso,
# porque o texto corrido delas foi para as CSVs - e correto que nao pontuem.
MIN_ANCORAS = 10

# Tolerancias em reais.
TOL_EXATA = 0.01
TOL_ARREDONDAMENTO = 1.00


# ----------------------------------------------------------------- numeros ---

# RE_MOEDA e valor_moeda moram no comum.py: o tratamento le dinheiro pela mesma
# regra, e as duas leituras nao podem divergir.

# Numero inteiro puro, para os fatores da linha (quantidade, frequencia).
RE_INTEIRO = re.compile(r"^\d{1,3}(?:\.\d{3})*$|^\d+$")


def moedas(texto: str):
    """Todos os valores monetarios de um texto, na ordem em que aparecem."""
    return [valor_moeda(m.group()) for m in RE_MOEDA.finditer(texto)]


def celula_numero(celula: str):
    """(valor, e_moeda) se a celula INTEIRA e um numero; senao None.

    Exigir a celula inteira evita capturar numero solto de dentro de descricao
    ('40h/semanais X 15 MESES' nao vira fator).
    """
    s = celula.strip()
    if not s:
        return None
    limpo = re.sub(r"(?i)^r\$\s*", "", s).strip()
    tinha_cifrao = limpo != s
    if RE_MOEDA.fullmatch(limpo):
        return (valor_moeda(limpo), True)
    if RE_INTEIRO.fullmatch(limpo):
        return (float(limpo.replace(".", "")), tinha_cifrao)
    return None


def perto(a: float, b: float, tol: float = TOL_EXATA) -> bool:
    return abs(a - b) <= tol


# ------------------------------------------------------------------ texto ----

def dobrar(texto: str) -> str:
    """Minuscula e sem acento - a forma dobrada usada nas comparacoes."""
    return sem_acento(texto.lower())


RE_PALAVRA = re.compile(r"[a-z]{%d,}" % MIN_LETRAS)


def palavras(texto: str):
    """Lista de palavras dobradas com MIN_LETRAS ou mais letras, em ordem."""
    return RE_PALAVRA.findall(dobrar(texto))


RE_ROTULO = re.compile(r"[^a-z0-9]")


def rotulo(celula: str) -> str:
    """Forma canonica de rotulo: 'sub-total' e 'SUBTOTAL' viram 'subtotal'."""
    return RE_ROTULO.sub("", dobrar(celula))


# ------------------------------------------------------------- leitura -------

# "<!-- pagina 12 -->" do extrair_planos.py e "<!-- pagina 12 | confianca OCR
# 91.0 -->" do extrair_digitalizados.py. Sem aceitar o segundo, o texto inteiro
# de um documento digitalizado caia na pagina 0 e E e G comparavam o OCR de
# cada pagina contra nada.
RE_PAGINA = re.compile(r"^<!-- pagina (\d+)(?: \|[^>]*)? -->\s*$")
RE_MARCADOR = re.compile(r"^\[\[tabela: p\d+_t\d+\]\].*$")
RE_COMENTARIO = re.compile(r"^<!--.*-->\s*$")


def ler_texto_md(caminho: Path):
    """Devolve {pagina: [(n_linha_no_arquivo, texto)]} do texto corrido.

    Marcadores de tabela e comentarios sao descartados: nao sao texto do
    documento. O cabecalho antes da primeira pagina fica na chave 0.
    """
    paginas = defaultdict(list)
    atual = 0
    for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
        m = RE_PAGINA.match(linha)
        if m:
            atual = int(m.group(1))
            continue
        if RE_MARCADOR.match(linha) or RE_COMENTARIO.match(linha):
            continue
        paginas[atual].append((n, linha))
    return paginas


RE_CSV = re.compile(r"^p(\d+)_t(\d+)\.csv$")


def ler_tabelas(dir_tabelas: Path):
    """Devolve {pagina: [(caminho, [linhas])]} em ordem de pagina e de tabela."""
    por_pagina = defaultdict(list)
    for caminho in sorted(dir_tabelas.glob("*.csv")):
        m = RE_CSV.match(caminho.name)
        if not m:
            continue
        with caminho.open(encoding="utf-8", newline="") as f:
            linhas = list(csv.reader(f))
        por_pagina[int(m.group(1))].append((caminho, linhas))
    return por_pagina


# -------------------------------------------------------------------- ocr ----

def preparar_tesseract():
    """Devolve a funcao de OCR ou None. Nao usa rapidocr: perde acentuacao."""
    pytesseract, _ = _preparar_tesseract()
    if pytesseract is None:
        return None
    return lambda img: pytesseract.image_to_string(img, lang="por")


class OCR:
    """OCR das paginas, com cache em disco FORA da pasta do projeto."""

    def __init__(self, pdf_path: Path, dir_cache: Path, motor):
        self.pdf_path = pdf_path
        self.motor = motor
        self.dir = dir_cache / sha256_arquivo(pdf_path)[:16]
        self.dir.mkdir(parents=True, exist_ok=True)
        self._memo = {}

    def _arquivo(self, pagina: int) -> Path:
        return self.dir / f"p{pagina:03d}_{DPI_OCR}.txt"

    def faltantes(self, paginas):
        return [p for p in paginas if not self._arquivo(p).exists()]

    def carregar(self, paginas, verboso=True):
        """Reconhece o que faltar e guarda tudo em memoria."""
        pendentes = self.faltantes(paginas)
        if pendentes:
            if self.motor is None:
                raise RuntimeError("OCR indisponivel e sem cache.")
            if verboso:
                print(f"   OCR de {len(pendentes)} pagina(s) a {DPI_OCR} dpi "
                      f"(as outras vem do cache)...", flush=True)
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, p in enumerate(pendentes, 1):
                    imagem = pdf.pages[p - 1].to_image(resolution=DPI_OCR).original
                    texto = self.motor(imagem) or ""
                    self._arquivo(p).write_text(texto, encoding="utf-8")
                    if verboso and (i % 5 == 0 or i == len(pendentes)):
                        print(f"      {i}/{len(pendentes)}", flush=True)
        for p in paginas:
            self._memo[p] = self._arquivo(p).read_text(encoding="utf-8")

    def __getitem__(self, pagina: int) -> str:
        return self._memo[pagina]


# --------------------------------------------------------------- documento ---

RE_META_PAGINAS = re.compile(r"^paginas:\s*(\d+)\s*$", re.M)


def contar_paginas(dir_doc: Path, linhas_por_pagina, pdf_path):
    """Numero de paginas sem abrir o PDF quando possivel.

    O meta.yaml do extrator traz o numero; em normalizados/ nao ha meta.yaml, e
    o maior marcador de pagina do texto.md serve. So na falta dos dois o PDF e
    aberto - e so ele exige o pdfplumber.
    """
    meta = dir_doc / "meta.yaml"
    if meta.exists():
        m = RE_META_PAGINAS.search(meta.read_text(encoding="utf-8"))
        if m:
            return int(m.group(1))
    paginas = [p for p in linhas_por_pagina if p > 0]
    if paginas:
        return max(paginas)
    if pdf_path is None or pdfplumber is None:
        return 0
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)


class Documento:
    def __init__(self, doc_id, dir_extraido, pdf_path):
        self.id = doc_id
        self.dir = dir_extraido
        self.pdf = pdf_path
        self.texto_md = dir_extraido / "texto.md"
        self.linhas_por_pagina = ler_texto_md(self.texto_md)
        self.tabelas = ler_tabelas(dir_extraido / "tabelas")
        self.n_paginas = contar_paginas(dir_extraido, self.linhas_por_pagina,
                                        pdf_path)
        self.paginas_com_tabela = sorted(self.tabelas)

    def prosa(self, pagina: int) -> str:
        """Texto corrido da pagina, sem conteudo de tabela."""
        return "\n".join(t for _, t in self.linhas_por_pagina.get(pagina, []))

    def texto_tabelas(self, pagina: int) -> str:
        return "\n".join(
            " ".join(linha)
            for _, dados in self.tabelas.get(pagina, [])
            for linha in dados
        )

    def nativo(self, pagina: int) -> str:
        """Extracao nativa completa da pagina: prosa + tabelas."""
        return self.prosa(pagina) + "\n" + self.texto_tabelas(pagina)

    def rel(self, caminho: Path) -> str:
        try:
            return str(caminho.relative_to(RAIZ)).replace("\\", "/")
        except ValueError:
            return str(caminho)


# ------------------------------------------------------- A leitura cruzada ---

def verificar_A(doc, ocr):
    """Valores monetarios do OCR x da extracao nativa, pagina a pagina."""
    resultado = {"paginas": len(doc.paginas_com_tabela), "so_nativo": [],
                 "so_ocr": []}
    for p in doc.paginas_com_tabela:
        c_nat = Counter(round(v, 2) for v in moedas(doc.nativo(p)))
        c_ocr = Counter(round(v, 2) for v in moedas(ocr[p]))
        for v, n in (c_nat - c_ocr).items():
            resultado["so_nativo"].extend([(p, v)] * n)
        for v, n in (c_ocr - c_nat).items():
            resultado["so_ocr"].extend([(p, v)] * n)
    resultado["divergencias"] = len(resultado["so_nativo"]) + len(resultado["so_ocr"])
    return resultado


# ------------------------------------------------------------ B estrutura ---

def verificar_B(doc):
    """Largura irregular, linha vazia, coluna vazia."""
    res = {"csvs": 0, "largura": [], "linha_vazia": [], "coluna_vazia": [],
           "uma_linha": []}
    for pagina in sorted(doc.tabelas):
        for caminho, dados in doc.tabelas[pagina]:
            res["csvs"] += 1
            if not dados:
                continue
            largura_cab = len(dados[0])
            for i, linha in enumerate(dados):
                if len(linha) != largura_cab:
                    res["largura"].append(
                        (doc.rel(caminho), i + 1, len(linha), largura_cab))
                if all(not c.strip() for c in linha):
                    res["linha_vazia"].append((doc.rel(caminho), i + 1))
            # CSV de uma linha so: qualquer coluna sem dado seria falso positivo,
            # porque nao ha linha de dado nenhuma para preencher a coluna.
            if len(dados) == 1:
                res["uma_linha"].append(doc.rel(caminho))
                continue
            n_col = max(len(l) for l in dados)
            for c in range(n_col):
                if all(c >= len(l) or not l[c].strip() for l in dados):
                    res["coluna_vazia"].append((doc.rel(caminho), c + 1))
    return res


# ---------------------------------------------------- C aritmetica totais ---

def cadeias(doc):
    """Corridas de paginas CONSECUTIVAS com tabela.

    A planilha orcamentaria atravessa varias paginas e sai como uma CSV por
    pagina; sem encadear, o subtotal da pagina 23 nunca acha os itens dele, que
    estao na 22.
    """
    grupos, atual = [], []
    for p in doc.paginas_com_tabela:
        if atual and p == atual[-1] + 1:
            atual.append(p)
        else:
            if atual:
                grupos.append(atual)
            atual = [p]
    if atual:
        grupos.append(atual)
    return grupos


def classificar_rotulo(linha):
    """Procura rotulo de total em QUALQUER coluna, nao so na primeira."""
    for celula in linha:
        r = rotulo(celula)
        if not r:
            continue
        if "subtotal" in r:
            return "subtotal"
        if "totalgeral" in r:
            return "total_geral"
        if r.startswith("total") and len(r) < 40:
            return "total"
    return None


def valor_da_linha(linha):
    """Ultimo valor MONETARIO da linha - a coluna 'Valor Total'."""
    for celula in reversed(linha):
        n = celula_numero(celula)
        if n and n[1]:
            return n[0]
    return None


# Codigo de item da planilha: 1, 1.1, 1.2.3. Nunca leva letra.
RE_CODIGO_ITEM = re.compile(r"^\d+(?:\.\d+)*$")


def tem_texto(linha) -> bool:
    """A linha tem alguma celula de texto, ou so numero e vazio?"""
    return any(c.strip() and celula_numero(c) is None for c in linha)


def tipo_da_linha(linha):
    """(tipo, rotulo_perdido) da linha na hierarquia da planilha.

    Um caso a mais que o classificar_rotulo sozinho: linha sem codigo de item,
    sem texto nenhum e com valor e um total cujo ROTULO se perdeu na extracao -
    e o caso do pt_ses_04 p050:3, o sub-total da Etapa 2.3, que saiu do PDF como
    ['', '', '', '', '', '', '', 'R$ 1.169.110,00'].

    Sem esse caso a linha e lida como item, e o subtotal seguinte soma o valor
    duas vezes: acusava R$ 2.338.220,00 de diferenca no pt_ses_04, e a
    diferenca nao existia. O que falta ali e a palavra, nao o numero.

    A heuristica e estreita de proposito - exige a linha inteira sem texto - e
    nos quatro planos ela pega exatamente uma linha, nos dois lados.
    """
    tipo = classificar_rotulo(linha)
    if tipo:
        return tipo, False
    if RE_CODIGO_ITEM.fullmatch((linha[0] if linha else "").strip()):
        return "item", False
    if valor_da_linha(linha) is not None and not tem_texto(linha):
        return "subtotal", True
    return "item", False


def escada(linhas):
    """Sobe a hierarquia da planilha. Devolve (testes, rotulos_perdidos).

    `linhas` e uma sequencia de (origem, celulas) na ordem de leitura. O que
    varia entre quem chama e so como as linhas foram reunidas: o C encadeia
    paginas consecutivas de `extraidos/`, o I le a `planilha.csv` ja achatada.
    A escada em si e a mesma, e por isso mora aqui - se as duas divergirem, o
    relatorio passa a afirmar coisas diferentes sobre o mesmo documento.

    `origem` e opaco: quem chama monta a string e o relatorio so imprime.

    Cada teste sai como (nome, origem, declarado, calculado, fonte, n_base),
    com n_base == 0 quando nao havia o que somar - teste nao verificavel, que
    nao e o mesmo que teste que falhou.

    A planilha tem TRES niveis: sub-total de etapa, total de meta e total geral.
    Somar tudo num nivel so faz o total geral contar cada valor duas vezes e
    acusar erro onde nao ha.
    """
    testes, perdidos = [], []
    itens, subtotais, totais = [], [], []
    for origem, celulas in linhas:
        tipo, rotulo_perdido = tipo_da_linha(celulas)
        valor = valor_da_linha(celulas)
        if tipo == "item":
            if valor is not None:
                itens.append(valor)
            continue
        if valor is None:
            continue
        if rotulo_perdido:
            perdidos.append((origem, valor))
        if tipo == "subtotal":
            nome, base, fonte, n_base = ("SUBTOTAL", sum(itens),
                                         "soma dos itens do grupo", len(itens))
            subtotais.append(valor)
            itens = []
        elif tipo == "total":
            # Total de meta fecha contra os subtotais dela; quando a tabela
            # nao tem subtotal nenhum, fecha contra os proprios itens.
            if subtotais:
                base, fonte, n_base = (sum(subtotais), "soma dos subtotais",
                                       len(subtotais))
            else:
                base, fonte, n_base = (sum(itens), "soma dos itens do grupo",
                                       len(itens))
            nome = "TOTAL"
            totais.append(valor)
            subtotais, itens = [], []
        else:
            nome = "TOTAL GERAL"
            if totais:
                base, fonte, n_base = (sum(totais), "soma dos totais de meta",
                                       len(totais))
            elif subtotais:
                base, fonte, n_base = (sum(subtotais), "soma dos subtotais",
                                       len(subtotais))
            else:
                base, fonte, n_base = (sum(itens), "soma dos itens", len(itens))
        testes.append((nome, origem, valor, base, fonte, n_base))
    return testes, perdidos


def contar(testes, res):
    """Distribui os testes entre ok, falha e nao verificavel."""
    for _, _, declarado, calculado, _, n_base in testes:
        if n_base == 0:
            res["nao_verificavel"] += 1
        elif perto(declarado, calculado):
            res["ok"] += 1
        else:
            res["falha"] += 1


def verificar_C(doc):
    res = {"cadeias": [], "ok": 0, "falha": 0, "nao_verificavel": 0,
           "rotulos_perdidos": []}
    for grupo in cadeias(doc):
        linhas = [(f"{doc.rel(caminho)}:{i + 1}", linha)
                  for p in grupo
                  for caminho, dados in doc.tabelas[p]
                  for i, linha in enumerate(dados)]
        if not any(tipo_da_linha(l)[0] != "item" for _, l in linhas):
            continue
        testes, perdidos = escada(linhas)
        res["cadeias"].append({"paginas": (grupo[0], grupo[-1]),
                               "testes": testes})
        res["rotulos_perdidos"].extend(perdidos)
        contar(testes, res)
    return res


# ------------------------------------------------------ D produto da linha ---

def verificar_D(doc):
    """Valor total da linha x produto dos fatores da propria linha."""
    res = {"ok": 0, "falha": 0, "arredondamento": 0, "linhas": []}
    for pagina in sorted(doc.tabelas):
        for caminho, dados in doc.tabelas[pagina]:
            for i, linha in enumerate(dados):
                if classificar_rotulo(linha):
                    continue
                # O codigo do item na primeira coluna nao e fator. "1.1.1" nunca
                # parecia numero, mas o codigo que o OCR le sem os pontos
                # parece: "2141" entrava como inteiro e "1.24" como R$ 1,24, e
                # o produto da linha saia multiplicado pelo codigo.
                codigo = linha[0].strip() if linha else ""
                inicio = 1 if RE_CODIGO_ITEM.fullmatch(codigo) else 0
                nums = [(j, celula_numero(c)) for j, c in enumerate(linha)
                        if j >= inicio]
                nums = [(j, v) for j, v in nums if v]
                if len(nums) < 3:
                    continue
                _, (total, total_moeda) = nums[-1]
                if not total_moeda:
                    continue
                fatores = [v for _, (v, _) in nums[:-1]]
                if not any(m for _, (_, m) in nums[:-1]):
                    continue
                produto = 1.0
                for f in fatores:
                    produto *= f
                diferenca = abs(produto - total)
                if diferenca <= TOL_EXATA:
                    estado = "ok"
                    res["ok"] += 1
                elif diferenca <= TOL_ARREDONDAMENTO:
                    estado = "arredondamento"
                    res["arredondamento"] += 1
                else:
                    estado = "falha"
                    res["falha"] += 1
                res["linhas"].append(
                    (estado, doc.rel(caminho), i + 1, fatores, produto, total))
    return res


# ------------------------------------------------------------ E cobertura ---

def verificar_E(doc, ocr):
    """Das palavras que o OCR viu, quantas existem na extracao nativa?"""
    faltas_por_pagina = {}
    vistas_por_pagina = {}
    ausencias = Counter()
    for p in range(1, doc.n_paginas + 1):
        vistas = set(palavras(ocr[p]))
        nativas = set(palavras(doc.nativo(p)))
        faltando = vistas - nativas
        vistas_por_pagina[p] = vistas
        faltas_por_pagina[p] = faltando
        for w in faltando:
            ausencias[w] += 1

    # Papel timbrado e imagem: as palavras do endereco do proponente faltam em
    # quase toda pagina. Isso e uma perda unica, sistematica, e afunda o recall
    # se entrar na conta como se fossem centenas de perdas independentes.
    corte = LIMIAR_TIMBRE * doc.n_paginas
    timbre = sorted(w for w, n in ausencias.items() if n >= corte)
    set_timbre = set(timbre)

    total = sum(len(v - set_timbre) for v in vistas_por_pagina.values())
    faltas = [(p, w) for p in sorted(faltas_por_pagina)
              for w in sorted(faltas_por_pagina[p]) if w not in set_timbre]
    recall = 1.0 - (len(faltas) / total) if total else 1.0
    return {"recall": recall, "total": total, "faltas": faltas,
            "timbre": timbre, "ausencias": ausencias}


# ------------------------------------------------------------ F artefatos ---

RE_HIFEN = re.compile(r"[A-Za-zÀ-ÿ]{2,}-$")
RE_COLADA = re.compile(r"\b[a-zà-ÿ]{2,}[A-ZÀ-Þ][a-zà-ÿ]{2,}\b")


def verificar_F(doc):
    """Quebra hifenizada de fim de linha e palavra colada. Sem OCR."""
    res = {"hifen": [], "colada": []}
    caminho = doc.rel(doc.texto_md)
    linhas = doc.texto_md.read_text(encoding="utf-8").splitlines()
    for i, linha in enumerate(linhas):
        limpa = linha.rstrip()
        if RE_HIFEN.search(limpa):
            seguinte = next((l.strip() for l in linhas[i + 1:i + 4] if l.strip()), "")
            if seguinte and seguinte[0].islower():
                res["hifen"].append((caminho, i + 1, limpa.split()[-1],
                                     seguinte.split()[0]))
        for m in RE_COLADA.finditer(linha):
            res["colada"].append((caminho, i + 1, m.group()))
    return res


# ------------------------------------------------------- G ordem de leitura ---

def verificar_G(doc, ocr):
    """Ordem relativa das ancoras: palavras unicas nas duas leituras.

    O recall do teste E nao ve embaralhamento - um texto reordenado tem recall
    de 100%. A comparacao e SO contra o texto corrido do texto.md: anexar as
    CSVs no fim embaralha por construcao, porque o OCR le a tabela na posicao
    visual dela, e isso ja produziu alarme falso.
    """
    res = {"paginas": [], "mensuraveis": 0, "perfeitas": 0}
    for p in range(1, doc.n_paginas + 1):
        seq_ocr = palavras(ocr[p])
        seq_nat = palavras(doc.prosa(p))
        uma_ocr = {w for w, n in Counter(seq_ocr).items() if n == 1}
        uma_nat = {w for w, n in Counter(seq_nat).items() if n == 1}
        ancoras = uma_ocr & uma_nat
        if len(ancoras) < MIN_ANCORAS:
            res["paginas"].append((p, None, len(ancoras)))
            continue
        ordem_nat = {w: i for i, w in enumerate(w for w in seq_nat if w in ancoras)}
        so_ocr = [ordem_nat[w] for w in seq_ocr if w in ancoras]
        pares = concordantes = 0
        for i in range(len(so_ocr)):
            for j in range(i + 1, len(so_ocr)):
                pares += 1
                if so_ocr[i] < so_ocr[j]:
                    concordantes += 1
        escore = concordantes / pares if pares else 1.0
        res["mensuraveis"] += 1
        if escore >= 0.9999:
            res["perfeitas"] += 1
        res["paginas"].append((p, escore, len(ancoras)))
    return res


# -------------------------------------------------- I planilha consolidada ---

# Colunas que a consolidacao acrescenta na frente. Saem antes de qualquer conta:
# `pagina_origem` e inteiro e entraria como fator no produto.
COLUNAS_PROCEDENCIA = 2


def ler_planilha(doc):
    """(cabecalho, [(origem, celulas)]) da planilha.csv, sem a procedencia.

    Devolve None quando o arquivo nao existe, e isso nao e erro: a planilha.csv
    nasce no tratamento, entao rodar sobre extraidos/ cai aqui sempre.
    """
    caminho = doc.dir / "planilha.csv"
    if not caminho.exists():
        return None
    with caminho.open(encoding="utf-8", newline="") as f:
        linhas = list(csv.reader(f))
    if len(linhas) < 2:
        return None
    dados = [(l[1] if len(l) > 1 else "", l[COLUNAS_PROCEDENCIA:])
             for l in linhas[1:]]
    return linhas[0][COLUNAS_PROCEDENCIA:], dados


def conferir_sequencia(dados):
    """Buraco e repeticao na numeracao dos itens.

    A planilha numera item dentro de etapa - 1.1.1, 1.1.2, ... e recomeca em
    1.2.1 - entao dentro de cada etapa a ultima componente tem que ser 1, 2, 3,
    sem pulo e sem repeticao.

    E o teste que a aritmetica nao faz. Quando a cadeia da consolidacao para
    cedo, o bloco perdido leva junto o subtotal dele: a soma dos itens que
    sobraram continua fechando com os subtotais que sobraram, e o C nao acusa
    nada. A numeracao acusa.
    """
    por_etapa = defaultdict(list)
    for origem, celulas in dados:
        codigo = (celulas[0] if celulas else "").strip()
        if not RE_CODIGO_ITEM.fullmatch(codigo):
            continue
        partes = codigo.split(".")
        por_etapa[".".join(partes[:-1])].append((int(partes[-1]), codigo, origem))

    buracos, repetidos = [], []
    for etapa, entradas in por_etapa.items():
        numeros = [n for n, _, _ in entradas]
        for n, codigo, origem in entradas:
            if numeros.count(n) > 1:
                repetidos.append((codigo, origem))
        for faltando in sorted(set(range(1, max(numeros) + 1)) - set(numeros)):
            buracos.append(f"{etapa}.{faltando}" if etapa else str(faltando))
    return sorted(buracos), sorted(repetidos)


def verificar_I(doc):
    """Integridade da planilha orcamentaria consolidada."""
    lido = ler_planilha(doc)
    if lido is None:
        return None
    cabecalho, dados = lido

    buracos, repetidos = conferir_sequencia(dados)
    # A MESMA escada do C, sobre a consolidada em vez das CSVs por pagina. E o
    # ponto da verificacao: aqui os itens de um subtotal podem ter vindo de tres
    # paginas diferentes, entao ela fechar prova que as emendas de virada de
    # pagina cairam no lugar certo - coisa que conferir por pagina nao alcanca,
    # porque cada CSV isolada esta certa.
    testes, perdidos = escada(dados)

    # Consolidada que nao termina em total geral e sinal de cadeia interrompida:
    # o tratamento parou de encadear antes do fim da planilha.
    ultimo = next((tipo_da_linha(c)[0] for _, c in reversed(dados)
                   if any(x.strip() for x in c)), None)

    n_itens = sum(1 for _, c in dados
                  if RE_CODIGO_ITEM.fullmatch((c[0] if c else "").strip()))
    res = {"cabecalho": cabecalho, "linhas": len(dados), "itens": n_itens,
           "buracos": buracos, "repetidos": repetidos, "testes": testes,
           "rotulos_perdidos": perdidos, "termina_em": ultimo,
           "ok": 0, "falha": 0, "nao_verificavel": 0}
    contar(testes, res)
    return res


# ------------------------------------------------------------- relatorio -----

def linha_tabela(sigla, nome, veredito, detalhe):
    return f"  {sigla}  {nome:<20} {veredito:<14} {detalhe}"


def relatar(doc, r):
    print()
    print("=" * 78)
    print(f"  {doc.id}   {doc.n_paginas} paginas, "
          f"{sum(len(v) for v in doc.tabelas.values())} CSVs")
    print("=" * 78)

    if r.get("A"):
        a = r["A"]
        v = "OK" if a["divergencias"] == 0 else f"{a['divergencias']} DIVERG."
        det = (f"{a['paginas']} paginas com tabela; "
               f"{len(a['so_nativo'])} so na extracao, {len(a['so_ocr'])} so no OCR")
        print(linha_tabela("A", "LEITURA CRUZADA", v, det))
    else:
        print(linha_tabela("A", "LEITURA CRUZADA", "-", "nao rodou (--sem-ocr)"))

    b = r["B"]
    n_b = len(b["largura"]) + len(b["linha_vazia"]) + len(b["coluna_vazia"])
    print(linha_tabela(
        "B", "ESTRUTURA", "OK" if n_b == 0 else f"{n_b} avisos",
        f"{len(b['largura'])} linhas fora da largura do cabecalho, "
        f"{len(b['linha_vazia'])} linhas vazias, "
        f"{len(b['coluna_vazia'])} colunas vazias "
        f"({len(b['uma_linha'])} CSVs de 1 linha isentos)"))

    c = r["C"]
    tot_c = c["ok"] + c["falha"]
    print(linha_tabela(
        "C", "ARITMETICA TOTAIS",
        "OK" if c["falha"] == 0 else f"{c['falha']} NAO FECHA",
        f"{c['ok']}/{tot_c} totais fecham, {c['nao_verificavel']} sem itens no "
        f"grupo, {len(c['cadeias'])} cadeia(s)"))

    d = r["D"]
    tot_d = d["ok"] + d["falha"] + d["arredondamento"]
    print(linha_tabela(
        "D", "PRODUTO POR LINHA",
        "OK" if d["falha"] == 0 else f"{d['falha']} NAO FECHA",
        f"{d['ok']}/{tot_d} linhas fecham"
        + (f", {d['arredondamento']} por arredondamento" if d["arredondamento"] else "")))

    if r.get("E"):
        e = r["E"]
        print(linha_tabela(
            "E", "COBERTURA", f"{e['recall'] * 100:.2f}%",
            f"{len(e['faltas'])} palavras de {e['total']} fora do timbre; "
            f"timbre = {len(e['timbre'])} palavras"))
    else:
        print(linha_tabela("E", "COBERTURA", "-", "nao rodou (--sem-ocr)"))

    f = r["F"]
    n_f = len(f["hifen"]) + len(f["colada"])
    print(linha_tabela(
        "F", "ARTEFATOS", "OK" if n_f == 0 else f"{n_f} suspeitas",
        f"{len(f['hifen'])} hifenizacoes, {len(f['colada'])} palavras coladas"))

    if r.get("G"):
        g = r["G"]
        piores = sorted((p, s) for p, s, _ in g["paginas"]
                        if s is not None and s < 0.9999)
        print(linha_tabela(
            "G", "ORDEM DE LEITURA",
            "OK" if not piores else f"{len(piores)} pagina(s)",
            f"{g['perfeitas']}/{g['mensuraveis']} paginas mensuraveis a 100% "
            f"({doc.n_paginas - g['mensuraveis']} sem ancoras suficientes)"))
    else:
        print(linha_tabela("G", "ORDEM DE LEITURA", "-", "nao rodou (--sem-ocr)"))

    i = r.get("I")
    if i is None:
        print(linha_tabela("I", "PLANILHA CONSOLIDADA", "-",
                           "sem planilha.csv (so existe em normalizados/)"))
    else:
        n_seq = len(i["buracos"]) + len(i["repetidos"])
        problema = i["falha"] or n_seq or i["termina_em"] != "total_geral"
        tot_i = i["ok"] + i["falha"]
        print(linha_tabela(
            "I", "PLANILHA CONSOLIDADA",
            "OK" if not problema else f"{i['falha'] + n_seq} PROBLEMA(S)",
            f"{i['itens']} itens em {i['linhas']} linhas; "
            f"{i['ok']}/{tot_i} totais fecham; "
            f"numeracao {'integra' if not n_seq else 'com falha'}"))

    # ------------------------------------------------------------ detalhes ---
    print()
    print("  SUSPEITAS")
    houve = False

    if r.get("A") and r["A"]["divergencias"]:
        houve = True
        print("\n  A - valores que so aparecem de um lado")
        for p, v in r["A"]["so_nativo"][:40]:
            print(f"     pagina {p:>3}  so na extracao nativa: {reais(v)}")
        for p, v in r["A"]["so_ocr"][:40]:
            print(f"     pagina {p:>3}  so no OCR de controle:  {reais(v)}")

    if n_b:
        houve = True
        print("\n  B - estrutura")
        for caminho, n, larg, cab in b["largura"][:30]:
            print(f"     {caminho}:{n}  {larg} colunas, cabecalho tem {cab}")
        for caminho, n in b["linha_vazia"][:20]:
            print(f"     {caminho}:{n}  linha inteiramente vazia")
        for caminho, col in b["coluna_vazia"][:20]:
            print(f"     {caminho}  coluna {col} inteiramente vazia")

    for info in c["cadeias"]:
        print(f"\n  C - cadeia paginas {info['paginas'][0]}-{info['paginas'][1]}")
        for nome, origem, declarado, calculado, fonte, n_itens in info["testes"]:
            if n_itens == 0:
                marca, extra = "?", "  (sem itens no grupo - nao verificavel)"
            elif perto(declarado, calculado):
                marca, extra = "ok", ""
            else:
                marca = "ERRO"
                extra = f"  diferenca {reais(declarado - calculado)}"
                houve = True
            print(f"     {marca:>4}  {origem}  {nome} declarado "
                  f"{reais(declarado)}  x  {fonte} ({n_itens}) "
                  f"{reais(calculado)}{extra}")

    if c["rotulos_perdidos"]:
        # Nao entra em `houve`: o numero esta certo e a conta fecha com ele. O
        # que falta e a palavra, e isso e correcao de FORMA - uma linha em
        # registros/correcoes.csv, nao um achado.
        print("\n  C - totais lidos como tal apesar de o rotulo ter se perdido "
              "na extracao")
        for origem, valor in c["rotulos_perdidos"]:
            print(f"     {origem}  {reais(valor)}  "
                  f"linha sem rotulo e sem descricao; cabe uma linha de "
                  f"classe 'forma' em correcoes.csv")

    ruins = [l for l in d["linhas"] if l[0] != "ok"]
    if ruins:
        houve = True
        print("\n  D - linhas cujo total nao e o produto dos fatores")
        for estado, caminho, n, fatores, produto, total in ruins[:40]:
            fs = " x ".join(f"{f:g}" for f in fatores)
            print(f"     {estado:>14}  {caminho}:{n}  {fs} = {reais(produto)} "
                  f"mas a linha declara {reais(total)}")

    if r.get("E"):
        e = r["E"]
        print("\n  E - timbre detectado automaticamente "
              f"(ausente em >={LIMIAR_TIMBRE:.0%} das paginas, fora da conta)")
        print("     " + (", ".join(e["timbre"]) or "(nenhum)"))
        # Palavra que falta em muita pagina mas nao chega ao limiar tambem cheira
        # a elemento fixo de pagina. Fica so no relatorio, DENTRO da conta do
        # recall - quem decide se e timbre e a conferencia manual.
        limiar_baixo = 0.15 * doc.n_paginas
        quase = sorted(((n, w) for w, n in e["ausencias"].items()
                        if limiar_baixo <= n < LIMIAR_TIMBRE * doc.n_paginas),
                       reverse=True)
        if quase:
            print("     abaixo do limiar, mas recorrentes (seguem NA conta): "
                  + ", ".join(f"{w} ({n}/{doc.n_paginas} pag)" for n, w in quase))
        if e["faltas"]:
            houve = True
            print("\n  E - palavras vistas pelo OCR e ausentes da extracao nativa")
            por_pagina = defaultdict(list)
            for p, w in e["faltas"]:
                por_pagina[p].append(w)
            for p in sorted(por_pagina):
                print(f"     pagina {p:>3}  {', '.join(por_pagina[p])}")

    if n_f:
        houve = True
        print("\n  F - artefatos")
        for caminho, n, a, b2 in f["hifen"][:30]:
            print(f"     {caminho}:{n}  hifenizacao  {a} + {b2}")
        for caminho, n, palavra in f["colada"][:30]:
            print(f"     {caminho}:{n}  palavra colada  {palavra}")

    if r.get("G"):
        piores = [(p, s, a) for p, s, a in r["G"]["paginas"]
                  if s is not None and s < 0.9999]
        if piores:
            houve = True
            print("\n  G - paginas em que a ordem das ancoras discorda")
            for p, s, a in piores:
                print(f"     pagina {p:>3}  {s * 100:.0f}% dos pares na mesma "
                      f"ordem  ({a} ancoras)")

    if i is not None:
        if i["buracos"] or i["repetidos"]:
            houve = True
            print("\n  I - numeracao dos itens")
            for codigo in i["buracos"]:
                print(f"     item {codigo} nao aparece na consolidada - "
                      f"linha perdida entre a extracao e o tratamento")
            for codigo, origem in i["repetidos"]:
                print(f"     item {codigo} aparece mais de uma vez  ({origem})")
        ruins_i = [t for t in i["testes"] if t[5] and not perto(t[2], t[3])]
        if ruins_i:
            houve = True
            print("\n  I - hierarquia da consolidada")
            for nome, origem, declarado, calculado, fonte, n_base in ruins_i:
                print(f"     {origem}  {nome} declarado {reais(declarado)}  x  "
                      f"{fonte} ({n_base}) {reais(calculado)}  "
                      f"diferenca {reais(declarado - calculado)}")
        if i["termina_em"] != "total_geral":
            houve = True
            print("\n  I - a consolidada nao termina em total geral")
            print("     a cadeia do tratamento pode ter parado antes do fim da "
                  "planilha; confira a ultima pagina em normalizados/")
        # Rotulo perdido nao se reporta aqui: o C ja lista, e o escopo dele e
        # maior - todas as tabelas, nao so a planilha.

    if not houve:
        print("     nenhuma.")


# ------------------------------------------------------------------ main -----

from comum import RAIZ  # noqa: E402 - so para mostrar caminhos relativos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("extraidos")
    ap.add_argument("planos")
    ap.add_argument("--doc", action="append",
                    help="so este id (pode repetir); padrao: todos")
    ap.add_argument("--sem-ocr", action="store_true",
                    help="pula A, E e G")
    ap.add_argument("--cache", default=None,
                    help="pasta do cache de OCR; padrao: %%TEMP%%/conferir_ocr")
    args = ap.parse_args()

    saida_utf8()

    dir_extraidos = Path(args.extraidos).resolve()
    dir_planos = Path(args.planos).resolve()
    # O cache fica FORA da pasta do projeto de proposito.
    dir_cache = Path(args.cache) if args.cache else Path(tempfile.gettempdir()) / "conferir_ocr"

    if not args.sem_ocr and pdfplumber is None:
        sys.exit("Falta o pdfplumber para o OCR de controle. Rode: "
                 "pip install -r requirements.txt  (ou use --sem-ocr)")

    pdfs = {identificar(pdf.stem)[0]: pdf
            for pdf in sorted(dir_planos.glob("*.pdf"))}

    ids = args.doc or sorted(d.name for d in dir_extraidos.iterdir() if d.is_dir())
    motor = None if args.sem_ocr else preparar_tesseract()
    if not args.sem_ocr and motor is None:
        print("AVISO: Tesseract/por indisponivel. Sem cache, A, E e G nao rodam.\n")

    acusados = []
    for doc_id in ids:
        dir_doc = dir_extraidos / doc_id
        if not (dir_doc / "texto.md").exists():
            continue
        pdf = pdfs.get(doc_id)
        if pdf is None and not args.sem_ocr:
            print(f"AVISO: PDF de {doc_id} nao encontrado em {dir_planos}")
            continue
        print(f"-> {doc_id}", flush=True)
        doc = Documento(doc_id, dir_doc, pdf)

        r = {"B": verificar_B(doc), "C": verificar_C(doc), "D": verificar_D(doc),
             "F": verificar_F(doc), "I": verificar_I(doc)}
        if not args.sem_ocr:
            ocr = OCR(doc.pdf, dir_cache, motor)
            try:
                ocr.carregar(range(1, doc.n_paginas + 1))
                r["A"] = verificar_A(doc, ocr)
                r["E"] = verificar_E(doc, ocr)
                r["G"] = verificar_G(doc, ocr)
            except RuntimeError as erro:
                print(f"   {erro}")
        relatar(doc, r)
        siglas = numericas_que_acusam(r)
        if siglas:
            acusados.append(f"{doc_id} ({', '.join(siglas)})")

    print()
    if acusados:
        print(f"Verificacao numerica acusou em: {'; '.join(acusados)}")
        return 1
    print("Nenhuma verificacao numerica acusou.")
    return 0


def numericas_que_acusam(r):
    """Siglas das verificacoes numericas que acusaram - decidem o codigo de saida."""
    siglas = []
    if r.get("A") and r["A"]["divergencias"]:
        siglas.append("A")
    if r["C"]["falha"]:
        siglas.append("C")
    if r["D"]["falha"]:
        siglas.append("D")
    i = r.get("I")
    if i is not None and (i["falha"] or i["buracos"] or i["repetidos"]
                          or i["termina_em"] != "total_geral"):
        siglas.append("I")
    return siglas


if __name__ == "__main__":
    sys.exit(main())
