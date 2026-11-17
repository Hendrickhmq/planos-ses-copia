#!/usr/bin/env python3
"""
conferencia.py - o que ja foi conferido a mao, e se a marcacao ainda vale.

Uso:
    python conferencia.py extraidos/                     status
    python conferencia.py normalizados/                  status do outro lado
    python conferencia.py extraidos_ocr/                 status da leitura por OCR
    python conferencia.py extraidos/ --doc pt_ses_01     so um documento
    python conferencia.py extraidos/ --marcar pt_ses_01 --por HB
    python conferencia.py extraidos/ --marcar pt_ses_01 --por HB \\
        --alvo tabelas/p034_t01.csv --observacao "planilha, paginas 34-54"

POR QUE ISTO EXISTE

O `tabelas_conferidas` morou no meta.yaml ate a quarta geracao do extrator, e
era um bug: o extrair_planos.py monta o meta.yaml do zero e escreve por cima,
com o campo em `false` fixo. Reprocessar um documento - que e o que o README
manda fazer depois de acrescentar um ajuste de pagina - apagava a marcacao sem
dizer nada. Voce conferia 25 tabelas contra o PDF, acrescentava um ajuste numa
delas, rodava `--doc`, e as outras 24 voltavam a constar como nao conferidas.

Preservar o campo no meta.yaml seria pior, nao melhor: o `true` sobreviveria a
uma reextracao que mudou o conteudo, e passaria a afirmar "conferido" sobre
numeros que ninguem viu. Marcacao de conferencia tem que caducar sozinha quando
o conteudo muda.

Por isso o registro e ancorado no HASH do que foi conferido. A linha guarda o
sha256 do conteudo no momento da conferencia; este script recalcula o hash de
agora e compara. Bate, a marcacao VALE. Nao bate, CADUCOU - e nao ha risco de
voce confiar num numero que mudou desde que foi lido.

O ARQUIVO

`registros/conferencia.csv` e dado, como o `correcoes.csv` - uma linha por
(plano, pasta, alvo), com quem conferiu e quando:

    plano, pasta, alvo, sha256, conferido_por, data, resultado, observacao

`pasta` e a pasta conferida: extraidos, extraidos_ocr ou normalizados. O mesmo
plano tem uma leitura em cada uma, com conteudo diferente, e uma marcacao feita
na leitura por OCR nao diz nada sobre a leitura nativa. Sem essa coluna, rodar o
status em `extraidos/` mostrava como CADUCOU a conferencia que tinha sido feita
em `extraidos_ocr/` e continuava valendo la. Linha antiga, sem pasta, e
mostrada em qualquer pasta, com aviso.

`alvo` e o caminho relativo dentro da pasta do documento, ou `*` para o
documento inteiro. Marcar `*` cobre tudo de uma vez e e o caso comum; marcar
arquivo por arquivo serve quando a conferencia foi parcial - "li a planilha, nao
li a matriz de risco".

`resultado` e `ok` ou `com_achado`. `com_achado` significa que a leitura foi
feita e o que sobrou de errado esta em `achados.csv` - o alvo esta conferido,
nao esta correto. Sao coisas diferentes e a distincao importa: defeito do
documento nao deixa de ser conferido por ser defeito.

Marcar de novo o mesmo (plano, pasta, alvo) SUBSTITUI a linha. O registro diz o
estado de agora; a historia fica no Git.

O HASH E O MESMO EM QUALQUER COMPUTADOR

Arquivo de texto (.md, .yaml, .txt) entra no hash com o fim de linha
normalizado para LF. O Git para Windows troca LF por CRLF no checkout, e sem
essa normalizacao a conferencia feita no Mac aparecia como CADUCOU no Windows
sobre conteudo identico. As CSVs entram como estao: o modulo csv as grava com
CRLF em todo sistema, e o .gitattributes impede o Git de mexer nelas.

Sem dependencia externa.
"""

import argparse
import csv
import hashlib
import sys
from collections import namedtuple
from datetime import date
from pathlib import Path

from comum import RAIZ, REGISTROS

REGISTRO = REGISTROS / "conferencia.csv"

CAMPOS = ["plano", "pasta", "alvo", "sha256", "conferido_por", "data",
          "resultado", "observacao"]

# A coluna `pasta` entrou depois; o arquivo sem ela ainda e lido.
CAMPOS_OBRIGATORIOS = [c for c in CAMPOS if c != "pasta"]

Linha = namedtuple("Linha", CAMPOS)

RESULTADOS = ("ok", "com_achado")

DOCUMENTO_INTEIRO = "*"

# O meta.yaml fica FORA do hash do documento inteiro. Ele carrega data_extracao
# e a versao do pdfplumber, entao mudaria a cada rodada mesmo quando o conteudo
# saisse identico - e toda marcacao caducaria por nada. O que se confere e o
# texto e as tabelas.
FORA_DO_HASH = {"meta.yaml", "tratamento.yaml"}

# Texto entra no hash com LF; CSV entra byte a byte (ver docstring).
TEXTO_NORMALIZADO = {".md", ".yaml", ".yml", ".txt"}

# Campos que moraram no meta.yaml e nao moram mais. Se aparecerem, o documento
# foi extraido por uma geracao anterior do extrator e o valor ali e ignorado.
CAMPOS_APOSENTADOS = ("tabelas_conferidas", "ocr_revisado", "observacoes")


# ------------------------------------------------------------------ hash -----

def sha256_arquivo(caminho: Path) -> str:
    dados = caminho.read_bytes()
    if caminho.suffix.lower() in TEXTO_NORMALIZADO:
        dados = dados.replace(b"\r\n", b"\n")
    return hashlib.sha256(dados).hexdigest()


def arquivos_do_documento(dir_doc: Path):
    """Conteudo conferivel do documento, em ordem estavel."""
    return sorted(c for c in dir_doc.rglob("*")
                  if c.is_file() and c.name not in FORA_DO_HASH)


def hash_alvo(dir_doc: Path, alvo: str):
    """sha256 do alvo agora, ou None se ele nao existe mais.

    Para o documento inteiro o hash e o do MANIFESTO - cada caminho relativo com
    o hash do seu arquivo, em ordem. Assim ele muda tanto quando um arquivo muda
    quanto quando um arquivo entra ou sai, que e o caso de uma reextracao que
    detecta uma tabela a mais.
    """
    if alvo != DOCUMENTO_INTEIRO:
        caminho = dir_doc / alvo
        return sha256_arquivo(caminho) if caminho.is_file() else None
    arquivos = arquivos_do_documento(dir_doc)
    if not arquivos:
        return None
    h = hashlib.sha256()
    for caminho in arquivos:
        rel = caminho.relative_to(dir_doc).as_posix()
        h.update(f"{rel}\n{sha256_arquivo(caminho)}\n".encode())
    return h.hexdigest()


# --------------------------------------------------------------- registro ----

def nome_da_pasta(dir_base: Path) -> str:
    """'extraidos', 'extraidos_ocr', 'normalizados' - o nome, nao o caminho."""
    return Path(dir_base).resolve().name


def ler_registro(caminho: Path):
    """[Linha], na ordem do arquivo. Linha sem pasta vem com pasta ''."""
    if not caminho.exists():
        return []
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        faltando = [c for c in CAMPOS_OBRIGATORIOS
                    if c not in (leitor.fieldnames or [])]
        if faltando:
            sys.exit(f"{caminho}: faltam as colunas {', '.join(faltando)}")
        return [Linha(*((linha.get(c) or "").strip() for c in CAMPOS))
                for linha in leitor]


def escrever_registro(caminho: Path, linhas):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(CAMPOS)
        escritor.writerows(sorted(linhas, key=lambda l: (l.plano, l.pasta, l.alvo)))


def marcar(dir_base: Path, doc_id: str, alvo: str, por: str, resultado: str,
           observacao: str, caminho_registro: Path):
    dir_doc = dir_base / doc_id
    if not dir_doc.is_dir():
        sys.exit(f"Documento nao encontrado: {dir_doc}")
    atual = hash_alvo(dir_doc, alvo)
    if atual is None:
        sys.exit(f"Alvo nao encontrado ou vazio: {doc_id}/{alvo}")

    pasta = nome_da_pasta(dir_base)
    # Substitui a linha da mesma pasta e tambem a antiga sem pasta: marcar de
    # novo e a forma de migrar uma linha antiga.
    linhas = [l for l in ler_registro(caminho_registro)
              if not (l.plano == doc_id and l.alvo == alvo
                      and l.pasta in (pasta, ""))]
    nova = Linha(doc_id, pasta, alvo, atual, por, date.today().isoformat(),
                 resultado, observacao)
    linhas.append(nova)
    escrever_registro(caminho_registro, linhas)
    try:
        onde = caminho_registro.resolve().relative_to(RAIZ)
    except ValueError:
        onde = caminho_registro          # --registro apontando para fora
    print(f"registrado em {onde}:")
    print(f"   {doc_id}  {pasta}/  {alvo}  {resultado}  por {por}  "
          f"{nova.data}  sha256 {atual[:12]}")


# ----------------------------------------------------------------- status ----

def avisar_meta_antigo(dir_doc: Path):
    """Aviso quando o meta.yaml ainda traz os campos aposentados."""
    meta = dir_doc / "meta.yaml"
    if not meta.exists():
        return []
    texto = meta.read_text(encoding="utf-8")
    return [c for c in CAMPOS_APOSENTADOS if f"{c}:" in texto]


def status(dir_base: Path, ids, caminho_registro: Path):
    """Imprime o estado de cada documento. Devolve True se algo caducou."""
    pasta = nome_da_pasta(dir_base)
    por_plano = {}
    outras_pastas = {}
    for linha in ler_registro(caminho_registro):
        if linha.pasta in (pasta, ""):
            por_plano.setdefault(linha.plano, []).append(linha)
        else:
            outras_pastas.setdefault(linha.plano, set()).add(linha.pasta)

    houve_caduco = houve_sem_pasta = False
    for doc_id in ids:
        dir_doc = dir_base / doc_id
        print(f"\n{doc_id}")

        arquivos = arquivos_do_documento(dir_doc)
        marcados = por_plano.get(doc_id, [])
        if not marcados:
            print(f"   NUNCA CONFERIDO   {len(arquivos)} arquivo(s)")
            if doc_id in outras_pastas:
                print(f"   (ha conferencia em {', '.join(sorted(outras_pastas[doc_id]))}/"
                      f" - outra leitura do mesmo plano)")
        cobertos = set()
        for l in marcados:
            agora = hash_alvo(dir_doc, l.alvo)
            if agora is None:
                estado = "ALVO SUMIU"
            elif agora == l.sha256:
                estado = "vale"
                cobertos.add(l.alvo)
            else:
                estado = "CADUCOU"
                houve_caduco = True
            if not l.pasta:
                houve_sem_pasta = True
            rotulo = "documento inteiro" if l.alvo == DOCUMENTO_INTEIRO else l.alvo
            print(f"   {estado:<11} {rotulo:<30} {l.resultado:<11} "
                  f"{l.data}  {l.conferido_por}"
                  + (" [sem pasta]" if not l.pasta else "")
                  + (f"   {l.observacao}" if l.observacao else ""))

        # Listar arquivo por arquivo so faz sentido quando a conferencia foi
        # parcial de proposito. Se existe linha para o documento inteiro, ela ja
        # conta a historia - inclusive quando caducou, e ai dizer "sem marcacao"
        # dos mesmos arquivos seria enganoso: eles foram conferidos, o que
        # aconteceu e que o conteudo mudou depois.
        tem_linha_do_documento = any(l.alvo == DOCUMENTO_INTEIRO for l in marcados)
        if marcados and not tem_linha_do_documento:
            faltam = [c.relative_to(dir_doc).as_posix() for c in arquivos
                      if c.relative_to(dir_doc).as_posix() not in cobertos]
            if faltam:
                print(f"   sem marcacao: {len(faltam)} arquivo(s) - "
                      + ", ".join(faltam[:4])
                      + (" ..." if len(faltam) > 4 else ""))

        aposentados = avisar_meta_antigo(dir_doc)
        if aposentados:
            print(f"   AVISO o meta.yaml ainda traz {', '.join(aposentados)} - "
                  f"campo aposentado, o valor ali e ignorado. Some na proxima "
                  f"extracao deste documento.")

    if houve_caduco:
        print("\nCADUCOU significa que o conteudo mudou depois da conferencia. "
              "Reconfira e marque de novo - o valor antigo nao vale mais.")
    if houve_sem_pasta:
        print("\n[sem pasta] e linha anterior a coluna `pasta`: nao se sabe em "
              "qual leitura foi feita. Marcar de novo, na pasta certa, a migra.")
    return houve_caduco


# ------------------------------------------------------------------ main -----

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base", help="extraidos/, extraidos_ocr/ ou normalizados/")
    ap.add_argument("--doc", action="append",
                    help="so este id (pode repetir); padrao: todos")
    ap.add_argument("--marcar", metavar="ID",
                    help="registra a conferencia deste documento")
    ap.add_argument("--alvo", default=DOCUMENTO_INTEIRO,
                    help="caminho dentro da pasta do documento; "
                         f"padrao {DOCUMENTO_INTEIRO} (documento inteiro)")
    ap.add_argument("--por", help="quem conferiu; obrigatorio com --marcar")
    ap.add_argument("--resultado", default="ok", choices=RESULTADOS,
                    help="ok, ou com_achado quando o que sobrou foi para "
                         "achados.csv")
    ap.add_argument("--observacao", default="")
    ap.add_argument("--registro", default=str(REGISTRO))
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    base = Path(args.base)
    if not base.is_dir():
        sys.exit(f"Pasta nao encontrada: {base}")
    caminho_registro = Path(args.registro)

    if args.marcar:
        if not args.por:
            sys.exit("--marcar exige --por: marcacao sem dono nao serve de nada")
        marcar(base, args.marcar, args.alvo, args.por, args.resultado,
               args.observacao, caminho_registro)
        return 0

    ids = sorted(d.name for d in base.iterdir()
                 if d.is_dir() and (d / "texto.md").exists())
    if args.doc:
        pedidos = {d.lower() for d in args.doc}
        ids = [i for i in ids if i in pedidos]
        if not ids:
            sys.exit("Nenhum documento corresponde a --doc")
    return 1 if status(base, ids, caminho_registro) else 0


if __name__ == "__main__":
    sys.exit(main())
