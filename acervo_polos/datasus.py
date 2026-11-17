"""Lê os arquivos mensais do CNES que o DATASUS publica para tabulação.

    python datasus.py 9180168        mostra o que há de um CNES em cada arquivo

Fonte: ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados/ — um arquivo por
UF e mês, público e sem login. Usados aqui, todos do DF:

  EQ  equipamentos           SR  serviços especializados       ST  estabelecimentos

O arquivo .dbc é um DBF com os registros comprimidos (PKWare "implode"). A
descompressão abaixo segue o blast.c de Mark Adler, que acompanha a zlib. Só
biblioteca padrão. O que baixa fica em _cache_cnes/ e não é baixado de novo.
"""
import ftplib
import struct
import sys
from pathlib import Path

SERVIDOR = "ftp.datasus.gov.br"
DIRETORIO = "/dissemin/publicos/CNES/200508_/Dados/"
CACHE = Path(__file__).resolve().parent / "_cache_cnes"

_BASE = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
_EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]
_LITLEN = [11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8, 9, 7, 6, 7, 8, 7, 6,
           55, 8, 23, 24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5, 7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7,
           9, 8, 25, 11, 8, 11, 9, 12, 8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24,
           10, 27, 44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45, 12, 61, 12, 45, 44, 173]
_LENLEN = [2, 35, 36, 53, 38, 23]
_DISTLEN = [2, 20, 53, 230, 247, 151, 248]


def _huffman(rep):
    """Tabela canônica a partir da forma compacta: (contagem por tamanho, símbolos)."""
    tamanhos = []
    for b in rep:
        tamanhos += [b & 15] * ((b >> 4) + 1)
    contagem = [0] * 14
    for t in tamanhos:
        contagem[t] += 1
    simbolos = [s for t in range(1, 14) for s, ts in enumerate(tamanhos) if ts == t]
    return contagem, simbolos


def explodir(dados):
    """Descomprime um fluxo PKWare DCL."""
    lit_cod, len_cod, dist_cod = _huffman(_LITLEN), _huffman(_LENLEN), _huffman(_DISTLEN)
    pos, buf, nbits = 0, 0, 0
    saida = bytearray()

    def bits(n):
        nonlocal pos, buf, nbits
        while nbits < n:
            buf |= dados[pos] << nbits
            pos += 1
            nbits += 8
        v = buf & ((1 << n) - 1)
        buf >>= n
        nbits -= n
        return v

    def decodificar(tabela):
        contagem, simbolos = tabela
        codigo = primeiro = indice = 0
        for tam in range(1, 14):
            codigo |= bits(1) ^ 1
            c = contagem[tam]
            if codigo < primeiro + c:
                return simbolos[indice + codigo - primeiro]
            indice += c
            primeiro = (primeiro + c) << 1
            codigo <<= 1
        raise ValueError("código inválido no arquivo comprimido")

    literal_codificado = bits(8)
    dicionario = bits(8)
    if literal_codificado > 1 or not 4 <= dicionario <= 6:
        raise ValueError("cabeçalho de compressão não reconhecido")
    while True:
        if bits(1):
            s = decodificar(len_cod)
            tam = _BASE[s] + bits(_EXTRA[s])
            if tam == 519:
                return bytes(saida)
            desloc = 2 if tam == 2 else dicionario
            dist = (decodificar(dist_cod) << desloc) + bits(desloc) + 1
            if dist > len(saida):
                raise ValueError("distância além do início")
            ini = len(saida) - dist
            if dist >= tam:
                saida += saida[ini:ini + tam]
            else:
                for i in range(tam):
                    saida.append(saida[ini + i])
        else:
            saida.append(decodificar(lit_cod) if literal_codificado else bits(8))


def ler_dbc(caminho):
    """Devolve (campos, registros) — registros como dicionários de texto já aparado."""
    bruto = Path(caminho).read_bytes()
    tam_cab, tam_reg = struct.unpack_from("<HH", bruto, 8)
    cab = bruto[:tam_cab]
    corpo = explodir(bruto[tam_cab + 4:])  # 4 bytes de CRC entre o cabeçalho e os registros
    campos, p = [], 32
    while p + 32 <= tam_cab and cab[p] != 0x0D:
        campos.append((cab[p:p + 11].split(b"\0")[0].decode("ascii"), cab[p + 16]))
        p += 32
    if sum(t for _, t in campos) + 1 != tam_reg:
        raise ValueError(f"{caminho}: campos não somam o tamanho do registro")
    registros = []
    for ini in range(0, len(corpo) - tam_reg + 1, tam_reg):
        if corpo[ini:ini + 1] == b"*":  # registro apagado
            continue
        r, q = {}, ini + 1
        for nome, t in campos:
            r[nome] = corpo[q:q + t].decode("latin-1").strip()
            q += t
        registros.append(r)
    return [n for n, _ in campos], registros


def baixar_ultimo(tipo, uf="DF"):
    """Baixa o arquivo mais recente do tipo (EQ, SR, ST) e devolve (caminho, 'AAMM').

    Sem rede, usa o mais recente que já estiver em _cache_cnes/.
    """
    CACHE.mkdir(exist_ok=True)
    prefixo = f"{tipo}{uf}"
    try:
        ftp = ftplib.FTP(SERVIDOR, timeout=60)
        ftp.login()
        ftp.cwd(DIRETORIO + tipo)
        nome = sorted(n for n in ftp.nlst() if n.upper().startswith(prefixo) and n.lower().endswith(".dbc"))[-1]
        destino = CACHE / nome
        if not destino.exists():
            parcial = destino.with_suffix(".parcial")
            with open(parcial, "wb") as f:
                ftp.retrbinary("RETR " + nome, f.write)
            parcial.replace(destino)
        ftp.quit()
    except (OSError, ftplib.Error, IndexError):
        locais = sorted(CACHE.glob(prefixo + "*.dbc"))
        if not locais:
            raise
        destino = locais[-1]
    return destino, destino.stem[-4:]


_MEMO = {}


def tabela(tipo):
    """Todos os registros do arquivo mais recente do tipo, e a competência 'MM/AAAA'.

    Guarda em memória: quem roda como servidor não descomprime o mesmo arquivo duas vezes.
    """
    if tipo not in _MEMO:
        caminho, aamm = baixar_ultimo(tipo)
        _, registros = ler_dbc(caminho)
        _MEMO[tipo] = (registros, f"{aamm[2:]}/20{aamm[:2]}")
    return _MEMO[tipo]


def do_cnes(tipo, cnes_procurados):
    """{cnes: [registros]} para os CNES pedidos, e a competência 'MM/AAAA' do arquivo."""
    registros, competencia = tabela(tipo)
    alvo = {str(c).zfill(7) for c in cnes_procurados}
    achado = {c: [] for c in alvo}
    for r in registros:
        c = r.get("CNES", "").zfill(7)
        if c in alvo:
            achado[c].append(r)
    return achado, competencia


if __name__ == "__main__":
    for tipo in ("EQ", "SR", "ST"):
        achado, comp = do_cnes(tipo, sys.argv[1:])
        print(f"== {tipo} — competência {comp}")
        for cnes, regs in achado.items():
            print(f"CNES {cnes}: {len(regs)} linha(s)")
            for r in regs:
                print("  ", {k: v for k, v in r.items() if v})
