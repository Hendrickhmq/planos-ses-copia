#!/usr/bin/env python3
"""
comum.py - o que os scripts do projeto usam igual, num lugar so.

Nao e executavel. Existe porque as mesmas funcoes moravam copiadas em quatro ou
cinco scripts - a leitura de valor monetario, o hash, o reconhecimento do nome
do plano, a procura do Tesseract - e uma correcao feita numa copia nao chegava
nas outras. A leitura de dinheiro em particular TEM de ser a mesma no
tratamento e na conferencia: se as duas lerem numeros diferentes da mesma
celula, a conferencia passa a acusar o tratamento por uma diferenca que so
existe entre as duas copias do codigo.

So biblioteca padrao. O pytesseract e importado so por quem pede OCR.
"""

import hashlib
import re
import shutil
import sys
import unicodedata
from pathlib import Path

# -------------------------------------------------------------- caminhos ---
# Onde mora cada coisa no projeto. Todo script le daqui: mudar uma pasta de
# lugar e mudar uma linha, e nao caçar o nome dela em vinte arquivos.

RAIZ = Path(__file__).resolve().parent.parent      # a pasta acima de ferramentas/

METODO = RAIZ / "metodo"                  # o padrao: vale para todo plano
ESTRUTURA_PLANO = METODO / "plano" / "estrutura.md"   # as tabelas que a verificacao J le
CRITERIOS = METODO / "criterios.md"       # gerado de registros/licoes.csv

CURSO = RAIZ / "curso"                    # a ordem de estudo, a logica e os casos

BIBLIOTECA = RAIZ / "biblioteca"          # material de consulta comum aos planos
NORMAS = BIBLIOTECA / "normas"
EXTRAIDOS_NORMAS = BIBLIOTECA / "extraidos_normas"

PLANOS = RAIZ / "planos"                  # um plano por pasta: redacao_NN/
CASOS = RAIZ / "ferramentas" / "casos"    # planos congelados, so para teste

REGISTROS = RAIZ / "registros"            # a base que liga estudo, biblioteca e metodo

ESTUDO = RAIZ / "estudo"                  # o acervo dos aprovados e sua extracao
PLANOS_APROVADOS = ESTUDO / "planos_aprovados"
EXTRAIDOS = ESTUDO / "extraidos"
EXTRAIDOS_OCR = ESTUDO / "extraidos_ocr"
EXTRAIDOS_CONTROLE = ESTUDO / "extraidos_controle"
NORMALIZADOS = ESTUDO / "normalizados"
CONTROLE = ESTUDO / "controle"
DESTILADOS = ESTUDO / "destilados"


# --------------------------------------------------------------- terminal ---

def saida_utf8():
    """Terminal em UTF-8. No Windows o padrao e cp1252, que nao tem boa parte
    dos simbolos que os relatorios imprimem."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except Exception:
            pass


# ------------------------------------------------------------------ texto ---

def sem_acento(texto: str) -> str:
    """Tira acento e cedilha. Nao mexe em caixa nem em espaco."""
    nfkd = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def nfc(texto: str) -> str:
    """Forma composta do Unicode.

    O macOS grava nome de arquivo em forma DECOMPOSTA ("c" + cedilha
    combinante); o Windows e o Linux, em forma composta. Os dois se imprimem
    igual e sao strings diferentes: comparar sem normalizar fez uma norma que
    estava no disco parecer ausente do acervo.
    """
    return unicodedata.normalize("NFC", texto or "")


def escrever_texto(caminho: Path, texto: str):
    """Grava UTF-8 com LF em qualquer sistema.

    `Path.write_text` em modo texto troca LF por CRLF no Windows, e ai a mesma
    extracao sai com bytes diferentes em cada computador - o hash da
    conferencia caduca e o "reconstroi byte a byte" deixa de valer.
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


# ----------------------------------------------------------------- numeros ---

# Numero monetario estrito: parte inteira, milhares opcionais e DOIS decimais.
# As bordas negativas impedem que CPF (XXX.XXX.XXX-XX), CNPJ (17.517.805/0003-71)
# e codigo SIGTAP (09.03.01.004-0) sejam lidos como dinheiro.
RE_MOEDA = re.compile(r"(?<![\d.,])\d+(?:[.,]\d{3})*[.,]\d{2}(?![\d.,])")


def valor_moeda(txt: str) -> float:
    """Converte '4.114.800,00' e '1,216.00' no mesmo numero.

    O separador decimal e o ULTIMO que aparece. O pt_ses_01 mistura as duas
    convencoes dentro do mesmo documento, entao decidir por documento nao
    funciona.
    """
    corte = max(txt.rfind("."), txt.rfind(","))
    inteiro = re.sub(r"[.,]", "", txt[:corte])
    return float(f"{inteiro}.{txt[corte + 1:]}")


def reais(v: float, cifrao: bool = True) -> str:
    """1216.0 -> 'R$ 1.216,00' (ou '1.216,00' sem cifrao)."""
    s = f"{v:,.2f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return f"R$ {s}" if cifrao else s


# ------------------------------------------------------------------ hash -----

def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with Path(caminho).open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


# ------------------------------------------------------------ nome do plano ---

PADRAO_NOME = re.compile(r"^(pt_ses_\d+)\s*[-_ ]+\s*(.+)$", re.IGNORECASE)


def identificar(stem: str):
    """(id, processo) a partir do nome do arquivo: pt_ses_01_030989-2026.

    Nome fora do padrao vira id igual ao nome, sem processo.
    """
    stem = nfc(stem).strip()
    m = PADRAO_NOME.match(stem)
    if m:
        return m.group(1).lower(), m.group(2).strip()
    return stem, ""


# --------------------------------------------------------------- yaml -------

def yaml_simples(meta: dict) -> str:
    """O meta.yaml do extrator: escalar, lista plana e mapa de pagina.

    Aspas e barra invertida dentro de string sao escapadas - nome de arquivo
    com aspas quebrava o YAML antes.
    """
    linhas = []
    for chave, valor in meta.items():
        if isinstance(valor, dict):
            linhas.append(f"{chave}:")
            for k, v in valor.items():
                linhas.append(f"  pagina_{k}: {v}")
        elif isinstance(valor, list):
            linhas.append(f"{chave}: [{', '.join(str(v) for v in valor)}]")
        elif isinstance(valor, bool):
            linhas.append(f"{chave}: {str(valor).lower()}")
        elif isinstance(valor, str):
            escapado = valor.replace("\\", "\\\\").replace('"', '\\"')
            linhas.append(f'{chave}: "{escapado}"')
        else:
            linhas.append(f"{chave}: {valor}")
    return "\n".join(linhas) + "\n"


# ------------------------------------------------------ programas externos ---

# Onde os instaladores do Windows costumam deixar cada programa, para quando
# ele nao estiver no PATH. O Git para Windows traz o pdftotext junto.
LOCAIS_WINDOWS = {
    "tesseract": [r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                  r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"],
    "pdftotext": [r"C:\Program Files\Git\mingw64\bin\pdftotext.exe",
                  r"C:\Program Files\poppler\Library\bin\pdftotext.exe",
                  r"C:\Program Files\poppler\bin\pdftotext.exe"],
}


def localizar(programa: str):
    """Caminho do executavel, pelo PATH ou pelo local usual no Windows."""
    achado = shutil.which(programa)
    if achado:
        return achado
    for candidato in LOCAIS_WINDOWS.get(programa, []):
        if Path(candidato).exists():
            return candidato
    return None


def preparar_tesseract():
    """(pytesseract, descricao) com o idioma 'por', ou (None, "").

    So Tesseract com o pacote 'por'. O rapidocr ficou de fora de proposito:
    reconhece sem acentuacao, e texto sem acento contamina as verificacoes de
    cobertura. Sem OCR a pagina digitalizada fica vazia - melhor que texto
    errado entrando no texto.md.

    A descricao leva a versao do Tesseract: o mesmo PDF sai com OCR diferente
    em versoes diferentes, e o meta.yaml precisa dizer qual leu.
    """
    try:
        import pytesseract
    except ImportError:
        return None, ""
    executavel = localizar("tesseract")
    if executavel is None:
        return None, ""
    pytesseract.pytesseract.tesseract_cmd = executavel
    try:
        if "por" not in pytesseract.get_languages():
            return None, ""
        versao = str(pytesseract.get_tesseract_version()).split()[0]
    except Exception:
        return None, ""
    return pytesseract, f"pytesseract/por, tesseract {versao}"
