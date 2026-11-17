#!/usr/bin/env python3
"""
testar_conferencia_plano.py - testa o conferir_plano.py sobre um plano real.

Uso:
    python3 testar_conferencia_plano.py redacao_03/

POR QUE ISTO EXISTE

Suite que passa nao prova nada: prova que nao acusou. Este script injeta um erro
conhecido por vez numa copia do plano, roda a conferencia sobre a copia e exige que
a verificacao correspondente FALHE. Se o erro passar despercebido, quem esta
quebrado e o teste.

As mutacoes sao DERIVADAS DO PROPRIO PLANO - localizam a linha pelo formato, nao
por texto fixo -, de modo que o arnes vale para qualquer plano do projeto.
"""
from __future__ import annotations
import importlib.util, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

from comum import RAIZ

AQUI = Path(__file__).resolve().parent

# ------------------------------------------------------------------ mutadores
# cada um recebe o texto do arquivo e devolve o texto mutado, ou None se nao
# encontrar onde morder. None vira "SEM ANCORA" no relatorio.

def _troca_valor(txt, padrao, delta, grupo=1):
    m = re.search(padrao, txt)
    if not m:
        return None
    bruto = m.group(grupo)
    v = float(bruto.replace(".", "").replace(",", "."))
    novo = f"{v + delta:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    ini, fim = m.span(grupo)
    return txt[:ini] + novo + txt[fim:]

def mut_A(t):   # total de linha da planilha
    return _troca_valor(t, r"\|\s*1\.1\.1\s*\|[^|]*(?:\|[^|]*){5}\|\s*([\d.]+,\d{2})\s*\|", 100)
def mut_B(t):   # subtotal — qualquer etapa, que o plano decide quantas tem
    v = _troca_valor(t, r"subtotal da Etapa [\d.]+\*{0,2}[^|]*(?:\|[^|]*)*?\|\s*\*{0,2}([\d.]+,\d{2})", 1000)
    if v: return v
    # planilha sem linha de subtotal: o TOTAL DA META fecha a etapa
    return _troca_valor(t, r"TOTAL DA META \d\*{0,2}[^|]*(?:\|[^|]*)*?\|\s*\*{0,2}([\d.]+,\d{2})", 1000)
def _linha_item(t, prefixo):
    """a linha da planilha cujo primeiro campo comeca com o prefixo (ex.: '2.1')"""
    for m in re.finditer(r"^\|\s*(\d+(?:\.\d+)+)\s*\|.*$", t, re.M):
        if m.group(1).startswith(prefixo):
            return m
    return None
def mut_C(t):   # quantitativo acima do que o envelope comporta
    if "subtotal da Etapa" not in t:
        # plano em que a fila define o recurso: nao ha piso de divisao a estourar.
        # o que C guarda e o teto do apoio — infla uma linha de apoio ate passar dele
        def triplicar(txt, padrao):
            m = re.search(padrao, txt)
            if not m: return txt, False
            v = float(m.group(1).replace(".", "").replace(",", "."))
            novo = f"{v*3:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
            return txt[:m.start(1)] + novo + txt[m.end(1):], True
        t2, a = triplicar(t, r"TOTAL DA META 1\*{0,2}[^|]*(?:\|[^|]*)*?\|\s*\*{0,2}([\d.]+,\d{2})")
        t2, b = triplicar(t2, r"\|\s*\*{0,2}Meta 1 —[^|]*\|\s*\*{0,2}([\d.]+,\d{2})")
        return t2 if (a or b) else None
    lin = _linha_item(t, "2.1")
    if not lin: return None
    # a quantidade e o maior inteiro sem centavos da linha
    cands = [x for x in re.finditer(r"(?<![\d,.])(\d{1,3}(?:\.\d{3})+|\d+)(?![\d,])", lin.group(0))
             if int(x.group(1).replace(".", "")) > 100]
    if not cands: return None
    alvo = max(cands, key=lambda x: int(x.group(1).replace(".", "")))
    q = int(alvo.group(1).replace(".", ""))
    novo = f"{q + 500:,}".replace(",", ".")
    ini = lin.start() + alvo.start(1)
    return t[:ini] + novo + t[lin.start() + alvo.end(1):]
def mut_D(t):   # um mes da curva
    m = re.search(r"\n\| 4 \| ([\d.]+) \| [\d.]+ \|", t)
    if not m:
        # curva por faixa: | 1 a 6 | 6.796 | 40.776 |
        m = re.search(r"\n\| \d+ a \d+ \| ([\d.]+) \| [\d.]+ \|", t)
    if not m:
        # curva por trimestre: | 2º | 4 a 6 | 19.642 |
        m = re.search(r"\n\| \d+º \| \d+ a \d+ \| ([\d.]+) \|", t)
    if not m: return None
    v = int(m.group(1).replace(".", "")) - 100
    return t[:m.start(1)] + f"{v:,}".replace(",", ".") + t[m.end(1):]
def mut_D2(t):  # curva por trimestre desalinhada do desembolso, com a soma preservada
    ms = list(re.finditer(r"\n\| \d+º \| \d+ a \d+ \| ([\d.]+) \|", t))
    if len(ms) < 2: return None
    a, b = ms[0], ms[1]
    va = int(a.group(1).replace(".", "")) - 100
    vb = int(b.group(1).replace(".", "")) + 100
    fmt = lambda v: f"{v:,}".replace(",", ".")
    return t[:a.start(1)] + fmt(va) + t[a.end(1):b.start(1)] + fmt(vb) + t[b.end(1):]
def mut_E(t):   # OCI de um polo
    m = re.search(r"\|\s*[\d.]+\s*\|\s*[\d,]+%\s*\|\s*\*{0,2}([\d.]+)\*{0,2}\s*\|", t)
    if not m:
        # | Ceilandia | Oeste e Sudoeste | 40,56% | **33.073** |
        m = re.search(r"\|[^|\n]+\|[^|\n]+\|\s*[\d,]+%\s*\|\s*\*{0,2}([\d.]{4,})\*{0,2}\s*\|", t)
    if not m: return None
    v = int(m.group(1).replace(".", "")) - 100
    return t[:m.start(1)] + f"{v:,}".replace(",", ".") + t[m.end(1):]
def mut_F(t):   # valor de uma parcela
    return _troca_valor(t, r"\|\s*2\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*\*{0,2}([\d.]+,\d{2})", 10000)
def mut_G(t):   # o total de capacidade deixa de ser a soma dos polos
    m = re.search(r"(\| Exames por dia útil[^|]*\| \*{0,2})(\d+)", t)
    if not m: return None
    return t[:m.end(1)] + str(int(m.group(2)) + 1) + t[m.end(2):]
def mut_I(t):   # uma regiao da fila
    m = re.search(r"\n\| [A-ZÀ-Ü][\wÀ-ü-]+ \| ([\d.]+) \| [\d,]+% \|", t)
    if not m: return None
    v = int(m.group(1).replace(".", "")) + 100
    return t[:m.start(1)] + f"{v:,}".replace(",", ".") + t[m.end(1):]
def mut_J(t):   # subsecao fora de sequencia
    m = re.search(r"^### 5\.4 ", t, re.M)
    return t[:m.start()] + "### 5.9 " + t[m.end():] if m else None
def mut_J2(t):  # secao que nao volta
    m = re.search(r"^### 9\.1 .+$", t, re.M)
    return t[:m.start()] + "### 9.1 Contrapartida" + t[m.end():] if m else None
def mut_K(t):   # titulo que anuncia argumento
    m = re.search(r"^(### 8\.1 )(.+)$", t, re.M)
    return t[:m.start(2)] + "Como esta planilha foi montada" + t[m.end(2):] if m else None
def mut_L(t):   # expressao de metodo no documento
    m = re.search(r"^### 9\.1 .+$", t, re.M)
    return t[:m.end()] + "\n\nO custo acessório foi calculado à parte." + t[m.end():] if m else None
def mut_M(t):   # norma citada sem lastro
    m = re.search(r"(Portaria SAES/MS nº )([\d.]+)", t)
    return t[:m.start(2)] + "9.999" + t[m.end(2):] if m else None
def mut_N(t):   # unitario divergente da fonte
    lin = _linha_item(t, "2.1")
    if lin and "exame" not in lin.group(0).lower():
        lin = _linha_item(t, "4.1") or lin      # plano multi-codigo: execucao na Meta 4
    if not lin: return None
    vals = list(re.finditer(r"([\d.]+,\d{2})", lin.group(0)))
    if len(vals) < 2: return None
    alvo = vals[-2]                      # ... | v. unitario | v. total |
    ini = lin.start() + alvo.start(1)
    return t[:ini] + "610,11" + t[lin.start() + alvo.end(1):]
def mut_S2(t):  # condicionante de liberacao criada pelo plano
    m = re.search(r"^### 7\.1 .+$", t, re.M)
    return t[:m.end()] + "\n\nCada parcela é liberada condicionada à comprovação da execução anterior." + t[m.end():] if m else None
def mut_T3(t):  # numero por extenso sem lastro
    if "48 horas" in t:
        return t.replace("48 horas", "onze horas", 1)
    for x in re.finditer(r"\b(dez|doze|seis|quatro|tr[eê]s)\s+(horas|meses|dias)\b", t):
        ini = t.rfind("\n", 0, x.start()) + 1
        if t[ini:ini+1] not in ("|", "#"):
            return t[:x.start(1)] + "dezessete" + t[x.end(1):]
    return None
def mut_S(t):   # indicador pactuado abaixo de 100%
    m = re.search(r"(\| I-0\d \|[^|]*\|[^|]*\| )(100%)( \|)", t)
    return t[:m.start(2)] + "≥ 95%" + t[m.end(2):] if m else None
def mut_T(t):   # medida de tempo em prosa sem lastro em dados/
    m = re.search(r"(\b48)( horas)", t)
    if not m:
        # qualquer medida de tempo dita em prosa, fora de tabela
        for x in re.finditer(r"(?<![\d,.])(\d{1,3}(?:\.\d{3})*)\s+(minutos|horas|dias)\b", t):
            ini = t.rfind("\n", 0, x.start()) + 1
            if t[ini:ini+1] not in ("|", "#"):
                m = x; break
    if not m: return None
    v = int(m.group(1).replace(".", "")) + 7
    novo = f"{v:,}".replace(",", ".")
    return t[:m.start(1)] + novo + t[m.end(1):]
def mut_T2(t):  # premissa em celula de tabela, como os "30% com biopsia" de 03/09
    m = (re.search(r"^\| Chegadas por hora \|.*$", t, re.M)
         or re.search(r"^\| \*{0,2}Tom[óo]grafos\*{0,2} \|.*$", t, re.M))
    return t[:m.end()] + "\n| Rejeição de registro | 43% | 43% | 43% | 43% |" + t[m.end():] if m else None
def mut_U(t):   # anuncia rubrica que o plano nao tem
    # a 9.3 quando existe; senao qualquer subsecao da secao 9 (no plano 4 a devolutiva
    # de 20/09/2026 tirou a 9.3, e a seção 9 ficou com 9.1 e 9.2)
    m = re.search(r"^### 9\.3 .+$", t, re.M) or re.search(r"^### 9\.\d+ .+$", t, re.M)
    return t[:m.end()] + "\n\nNão há rubrica de material de consumo." + t[m.end():] if m else None
def mut_V(t):   # contraria a ficha do procedimento
    return t.replace("**maiores de 18 anos**", "**sem recorte de faixa etária**", 1) \
        if "maiores de 18 anos" in t else None
def mut_W(t):   # digito errado no primeiro codigo SIGTAP (OCI ou exame), como o 004-0 do IEV
    m = re.search(r"(?<![\d.])0[1-9]\.\d{2}\.\d{2}\.\d{3}-(\d)", t)
    return t[:m.start(1)] + str((int(m.group(1)) + 1) % 10) + t[m.end(1):] if m else None
def mut_W2(t):  # valor da tabela trocado na linha da planilha, como a cardiologia do 04
    for m in re.finditer(r"^\|\s*\d+(?:\.\d+)+\s*\|[^\n]*09\.\d{2}\.\d{2}\.\d{3}-\d[^\n]*$", t, re.M):
        v = re.search(r"\|\s*([\d.]+,\d{2})\s*\|", m.group(0))
        if v:
            ini = m.start() + v.start(1)
            return t[:ini] + "1" + t[ini:]
    return None
def mut_X(t):   # comunicacao audiovisual numa linha de apoio, como o 3.1.3 do pt_ses_01
    m = re.search(r"^\|\s*1\.\d+\.\d+\s*\|\s*[^|]+?(?=\s*\|)", t, re.M)
    return t[:m.end()] + " e cobertura audiovisual" + t[m.end():] if m else None
def mut_O(t):   # campo de identificacao repetido em outra secao
    m = re.search(r"^### 4\.1 .+$", t, re.M) or re.search(r"^## 4\. .+$", t, re.M)
    return t[:m.end()] + "\n\n| | |\n|---|---|\n| CNPJ | [preencher] |" + t[m.end():] if m else None
def mut_P(t):   # meta declarada sem dotacao
    m = re.search(r"^\|\s*\*{0,2}Meta 1\*{0,2}\s*\|", t, re.M)
    return t[:m.start()] + "| **Meta 9** | Meta inventada sem dotacao | 1 | mes 10 |\n" + t[m.start():] if m else None
def mut_P2(t):  # meta qualitativa removida
    # com ou sem negrito: desde a v16 o plano 4 e derivado do docx, sem asteriscos
    novo = re.sub(r"\*{0,2}Meta qualitativa\*{0,2}\s*:", "Compromisso adicional:", t, count=1)
    return novo if novo != t else None
def mut_Q(t):   # voz defensiva no documento
    m = re.search(r"^### 6\.2 .+$", t, re.M)
    return t[:m.end()] + "\n\nO décimo mês não é folga." + t[m.end():] if m else None
def _paragrafo(t, i):
    ini = t.rfind("\n\n", 0, i) + 2
    fim = t.find("\n\n", i)
    return t[ini:fim if fim > 0 else len(t)]

_NORMA = re.compile(r"portaria|nota t[ée]cnica|decreto|resolu[çc][ãa]o|\bRDC\b|\bLei\b|"
                    r"\bart\.|anexo|SIGTAP|tabela federal|componente cr[ée]ditos", re.I)

def mut_R(t):   # valor em reais citado na prosa, divergente da tabela
    for m in re.finditer(r"R\$ ([\d.]+,\d{2})", t):
        ini = t.rfind("\n", 0, m.start()) + 1
        if t[ini:ini + 1] == "|" or _NORMA.search(_paragrafo(t, m.start())):
            continue                       # linha de tabela ou valor que vem de norma
        v = float(m.group(1).replace(".", "").replace(",", "."))
        novo = f"{v + 1000:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        return t[:m.start(1)] + novo + t[m.end(1):]
    return None

def mut_R2(t):  # quantidade citada na prosa com rotulo de item da planilha
    rad = lambda w: w.lower().rstrip("s")
    itens = [l for l in t.splitlines() if re.match(r"\|\s*\d+(\.\d+)+\s*\|", l.strip())]
    # so celulas de texto: numero puro e celula do tipo "10 meses" nao dao rotulo,
    # porque a verificacao R so aceita rotulo vindo do nome do item e da unidade
    celulas = [c.strip() for l in itens for c in l.split("|")]
    celulas = [c for c in celulas
               if c and not re.fullmatch(r"[\d.,]+", c) and not re.match(r"^\d[\d.,]*\s", c)]
    rotulos = {rad(p) for c in celulas for p in re.findall(r"[^\W\d_]{4,}", c)}
    ja_no_texto = set(re.findall(r"\d+", t.replace(".", "")))
    for m in re.finditer(r"(?<![\d,.])(\d{1,3}(?:\.\d{3})+|\d+)\s+\*{0,2}([^\W\d_]{4,})", t):
        ini = t.rfind("\n", 0, m.start()) + 1
        if t[ini:ini + 1] in ("|", "#") or rad(m.group(2)) not in rotulos:
            continue
        v = int(m.group(1).replace(".", ""))
        # o valor injetado nao pode existir no documento NEM ser uma soma plausivel
        # daquele rotulo: em 02/09/2026 este mutador trocou "3 postos" por "17
        # postos" e a verificacao aceitou, com razao — 16 postos da Meta 1 mais 1 da
        # Meta 3 sao 17. Por isso o salto de 100, que nenhuma soma de postos alcanca.
        novo = next((x for x in range(v + 100, v + 500) if str(x) not in ja_no_texto), None)
        if novo is None:
            continue
        return t[:m.start(1)] + f"{novo:,}".replace(",", ".") + t[m.end(1):]
    return None

def mut_R3(t):  # consumo derivado da unidade produzida, na memoria de calculo
    m = re.search(r"(?:s[ãa]o)\s+\w+\s+([^\W\d_]{4,})\s+por\s+([A-ZÀ-Ú]{2,})", t, re.I)
    if not m: return None
    subst = m.group(1).rstrip("s")
    m2 = re.search(rf"(\d{{1,3}}(?:\.\d{{3}})+)\s+{subst}s?\b", t)
    if not m2: return None
    v = int(m2.group(1).replace(".", "")) + 20
    return t[:m2.start(1)] + f"{v:,}".replace(",", ".") + t[m2.end(1):]

def mut_H(t):   # divergencia no estado.yaml (unico que morde outro arquivo)
    m = re.search(r"(valor_global:\s*)(\d+\.\d{2})", t)
    if not m: return None
    v = float(m.group(2)) - 1000
    return t[:m.start(2)] + f"{v:.2f}" + t[m.end(2):]

MUTACOES = [
    ("A", "total de linha da planilha alterado",            "plano.md",    mut_A),
    ("B", "subtotal de etapa alterado",                     "plano.md",    mut_B),
    ("C", "quantitativo acima do que o envelope comporta",     "plano.md",    mut_C),
    ("D", "um mes da curva alterado",                       "plano.md",    mut_D),
    ("D", "curva desalinhada das parcelas, soma preservada",  "plano.md",    mut_D2,
     lambda t: mut_D2(t) is not None),   # so quando a curva e por trimestre
    ("E", "quantitativo de um polo alterado",               "plano.md",    mut_E),
    ("F", "valor de uma parcela alterado",                  "plano.md",    mut_F),
    ("G", "total de capacidade diferente da soma dos polos", "plano.md",   mut_G,
     lambda t: mut_G(t) is not None),    # so no plano com tabela de capacidade com total
    ("H", "valor global divergente no estado.yaml",         "estado.yaml", mut_H),
    ("I", "uma regiao da fila alterada",                    "plano.md",    mut_I,
     lambda t: mut_I(t) is not None),   # o plano pode nao publicar a fila por regiao
    ("J", "subsecao fora de sequencia",                     "plano.md",    mut_J),
    ("J", "secao que nao volta reintroduzida",              "plano.md",    mut_J2),
    ("K", "titulo que anuncia argumento",                   "plano.md",    mut_K),
    ("L", "expressao de metodo dentro do documento",        "plano.md",    mut_L),
    ("M", "norma citada sem lastro no acervo",              "plano.md",    mut_M),
    ("N", "unitario do plano divergente da fonte",          "plano.md",    mut_N),
    ("O", "campo de identificacao repetido em duas secoes", "plano.md",    mut_O),
    ("P", "meta declarada no texto sem dotacao",            "plano.md",    mut_P),
    ("P", "meta qualitativa ausente",                       "plano.md",    mut_P2),
    ("Q", "voz defensiva dentro do documento",              "plano.md",    mut_Q),
    ("R", "valor em reais da prosa divergente da tabela",   "plano.md",    mut_R,
     lambda t: mut_R(t) is not None),    # o plano pode nao citar valor em reais fora de tabela
    ("R", "quantidade da prosa divergente da planilha",     "plano.md",    mut_R2,
     lambda t: mut_R2(t) is not None),   # o plano pode nao dizer quantidade em prosa
    ("S", "indicador pactuado abaixo de 100%",              "plano.md",    mut_S),
    ("S", "condicionante de liberacao criada pelo plano",   "plano.md",    mut_S2),
    ("T", "medida de tempo em prosa sem lastro",            "plano.md",    mut_T),
    ("T", "numero por extenso sem lastro",                  "plano.md",    mut_T3),
    ("T", "premissa em celula de tabela",                   "plano.md",    mut_T2),
    ("U", "anuncia rubrica que o plano nao tem",            "plano.md",    mut_U),
    ("V", "plano contraria a ficha do procedimento",        "plano.md",    mut_V,
     lambda t: mut_V(t) is not None),   # so quando o plano declara faixa etaria da ficha
    ("W", "digito verificador errado num codigo SIGTAP",    "plano.md",    mut_W,
     lambda t: mut_W(t) is not None),   # so quando o plano cita codigo SIGTAP
    ("W", "valor da tabela trocado na linha da planilha",   "plano.md",    mut_W2,
     lambda t: mut_W2(t) is not None),
    ("X", "comunicacao audiovisual numa linha de apoio",    "plano.md",    mut_X),
    ("R", "consumo derivado divergente do quantitativo",    "plano.md",    mut_R3,
     lambda t: bool(re.search(r"s[ãa]o\s+\w+\s+[^\W\d_]{4,}\s+por\s+[A-ZÀ-Ú]{2,}", t, re.I))),
]

def rodar(dir_projeto: Path, nome_plano: str):
    """roda a conferencia sobre a copia do plano, com metodo/ e biblioteca/normas/ da raiz.

    A saida e lida em UTF-8 dos dois lados. Com text=True sem encoding, o
    Windows decodificava em cp1252 e a leitura quebrava no primeiro "Á" - ou
    no primeiro simbolo que o cp1252 nao tem, do lado de quem escreve.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(AQUI / "conferir_plano.py"),
                        str(dir_projeto / nome_plano), "--raiz", str(RAIZ)],
                       capture_output=True, encoding="utf-8", errors="replace",
                       env=env)
    v = {}
    for linha in r.stdout.splitlines():
        m = re.match(r"\s{2}(\+?[A-Z][A-Z0-9]*)\s{2}(.+?)\s+(PASSOU|FALHOU|NAO SE APLICA)\s*$", linha)
        if m:
            v[m.group(1)] = m.group(3)
    return v, r.stdout + r.stderr

def montar(td, plano: Path):
    """copia so o plano; metodo/ e biblioteca/normas/ sao lidos da raiz real (--raiz).

    A versao anterior recriava a raiz na pasta temporaria com um link simbolico
    para normas/ - e no Windows criar link simbolico exige administrador ou o
    modo de desenvolvedor, entao a suite inteira parava no primeiro teste.
    """
    proj = Path(td) / "projeto"; proj.mkdir()
    shutil.copytree(plano, proj / plano.name)
    return proj

def mutacoes_do_plano(plano: Path):
    """os erros que so a bateria do plano sabe pegar: MUTACOES em conferencia/mutacoes.py,
    no mesmo formato da lista acima. Ver metodo/plano/conferencia.md."""
    arq = plano / "conferencia" / "mutacoes.py"
    if not arq.exists():
        return []
    spec = importlib.util.spec_from_file_location(f"mutacoes_{plano.name}", arq)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(getattr(mod, "MUTACOES", []))

def main():
    if len(sys.argv) < 2:
        raise SystemExit("uso: python3 testar_conferencia_plano.py redacao_NN/")
    plano = Path(sys.argv[1]).resolve()
    print()
    print(f"TESTE DA CONFERENCIA — {plano.name}")
    print("=" * 78)
    with tempfile.TemporaryDirectory() as td:
        proj = montar(td, plano)
        base_v, saida = rodar(proj, plano.name)
    ruins = [s for s, v in base_v.items() if v == "FALHOU"]
    if not base_v:
        print("  a conferencia nao produziu relatorio legivel:"); print(saida); return 1
    if ruins:
        print(f"  ATENCAO: o estado atual ja falha em {ruins} — corrija antes de testar")
        return 1
    print(f"  linha de base: {len(base_v)} verificacoes, nenhuma falhando")
    print("-" * 78)

    problemas, aplicadas = [], 0
    todas = MUTACOES + mutacoes_do_plano(plano)
    for entrada in todas:
        sigla, desc, arquivo, mutador = entrada[:4]
        # mutacao com predicado so conta quando o plano tem a construcao que ela morde:
        # o redacao_03 perdeu o consumo derivado quando o papel saiu da planilha
        aplica = entrada[4] if len(entrada) > 4 else None
        with tempfile.TemporaryDirectory() as td:
            proj = montar(td, plano)
            alvo = proj / plano.name / arquivo
            txt = alvo.read_text(encoding="utf-8")
            if aplica and not aplica(txt):
                print(f"  {sigla}  {desc:<52} NAO SE APLICA A ESTE PLANO")
                continue
            aplicadas += 1
            novo = mutador(txt)
            if novo is None or novo == txt:
                print(f"  {sigla}  {desc:<52} SEM ANCORA")
                problemas.append(f"{sigla}: nao achou onde injetar o erro em {arquivo}")
                continue
            alvo.write_text(novo, encoding="utf-8")
            v, _ = rodar(proj, plano.name)
            estado = v.get(sigla)
            outras = [x for x, y in v.items() if y == "FALHOU" and x != sigla]
            extra = f"  (tambem: {','.join(sorted(outras))})" if outras else ""
            rotulo = {"FALHOU": "APANHOU", "PASSOU": "PASSOU BATIDO",
                      "NAO SE APLICA": "DESLIGADA NO AMBIENTE", None: "NAO LIDA"}[estado]
            print(f"  {sigla}  {desc:<52} {rotulo}{extra}")
            if estado != "FALHOU":
                problemas.append(f"{sigla}: {rotulo.lower()} — {desc}")

    print("=" * 78)
    if problemas:
        print(f"  {len(problemas)} problema(s) na propria conferencia:")
        for x in problemas:
            print(f"    - {x}")
        return 1
    fora = len(todas) - aplicadas
    resto = f" ({fora} nao se aplica a este plano)" if fora else ""
    print(f"  {aplicadas}/{aplicadas} erros injetados foram apanhados pela verificacao certa{resto}")
    print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
