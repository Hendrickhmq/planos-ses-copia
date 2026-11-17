#!/usr/bin/env python3
"""
tratar_planos.py - tratamento de forma da extracao.

Uso:
    python tratar_planos.py extraidos/ normalizados/
    python tratar_planos.py extraidos/ normalizados/ --doc pt_ses_01
    python tratar_planos.py extraidos/ normalizados/ --correcoes registros/correcoes.csv
    python tratar_planos.py extraidos/ normalizados/ --ocr extraidos_ocr/

Le  extraidos/ + extraidos_ocr/ + registros/correcoes.csv  e escreve  normalizados/.

Tres regras que este script nao viola:

1. `extraidos/` e bruto e so o extrator escreve la. Este script nunca abre
   arquivo de `extraidos/` para escrita.
2. `normalizados/` e derivado e descartavel: apagar a pasta e rodar de novo
   produz os mesmos bytes. Por isso nao entra data, nem hora, nem contagem que
   dependa da ordem do sistema de arquivos - e as saidas de uma rodada anterior
   sao apagadas antes de escrever, senao uma CSV que deixou de existir na
   extracao continuaria aqui.
3. `registros/correcoes.csv` e dado, nao codigo. Correcao de celula mora la,
   com motivo. Defeito do DOCUMENTO nao entra la - vai para achados.csv, e o
   numero errado continua errado em `normalizados/`.

DE ONDE VEM CADA DOCUMENTO

Da pasta `extraidos/`, salvo quando o mesmo id existe em `extraidos_ocr/`. PDF
digitalizado (o pt_ses_05) tem duas leituras: a do extrair_planos.py, que so
consegue texto corrido por OCR de pagina inteira, e a do
extrair_digitalizados.py, que reconstroi a grade e le celula por celula. A
segunda e a que tem tabela, e foi a conferida (registros/conferencia.csv).
Sem ela, a planilha do pt_ses_05 nunca chegava aqui e a verificacao I nao tinha
o que conferir nesse plano. A pasta usada fica registrada no tratamento.yaml.

O que sai em normalizados/<plano>/:

    texto.md          copia byte a byte do texto.md da pasta de origem
    tabelas/*.csv     as mesmas CSVs, tratadas
    planilha.csv      a planilha orcamentaria inteira, consolidada
    tratamento.yaml   o que foi aplicado, para conferencia

O ganho maior e a `planilha.csv`. A planilha orcamentaria atravessa dezenas de
paginas e sai como uma CSV por pagina; consolidada, com `pagina_origem` e
`csv_origem` em cada linha, da para somar, filtrar e ainda voltar ao PDF.

O que o tratamento faz, nesta ordem:

  1. correcoes de celula vindas de correcoes.csv (classe `forma`), casadas por
     arquivo + linha + campo. `linha` e `campo` sao 1-based e se referem a CSV
     da pasta de origem, antes de qualquer remocao de linha - senao a
     coordenada mudaria de significado a cada rodada.

     `linha` 0 e o cabecalho que a extracao nao capturou: as correcoes com
     linha 0 montam uma linha nova, antes da primeira, com os campos dados por
     numero de coluna. E o caso do pt_ses_05, cujo cabecalho da planilha esta
     na pagina 40, fora da grade que o OCR reconstruiu.
  2. cabecalho repetido no meio da planilha: a planilha recomeca com o
     cabecalho quando muda de bloco no Word. Linha identica ao cabecalho, fora
     da primeira, sai.
  3. linha inteiramente vazia: sai.
  4. decimal: celula que e SO um valor monetario e reescrita numa convencao so.
     O pt_ses_01 mistura as duas dentro do mesmo documento (R$ 1.216,00 na
     planilha e R$ 1,216.00 no anexo). O separador decimal e o ultimo que
     aparece - a mesma regra do conferir.py, que le do mesmo comum.py.
  5. consolidacao da planilha, com uma juncao a mais: item cuja descricao vira
     a pagina deixa o rabicho como primeira linha da CSV seguinte, sem codigo
     de item e sem valor. Essa linha e emendada na linha anterior, e as duas
     origens ficam registradas em `csv_origem`.

     Quando a pasta de origem ja traz a planilha costurada
     (`planilha_pNNN-pNNN.csv`, saida do extrair_digitalizados.py), e ela que
     vira a consolidada: a costura ja foi feita pela grade da imagem, e refaze-la
     pelas CSVs por pagina perderia a normalizacao dos codigos de item.

O que o tratamento NAO faz: mexer em numero, quantidade, rotulo ou data. Se a
planilha diz 16 locacoes e o cronograma soma 18, os dois continuam como estao.
Isso e defeito do documento, e vira linha em `registros/achados.csv`.
"""

import argparse
import csv
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from comum import (EXTRAIDOS_OCR, REGISTROS, RE_MOEDA, escrever_texto, reais, saida_utf8, sem_acento,
                   valor_moeda)

RE_CIFRAO = re.compile(r"(?i)^(r\$)\s*")

RE_CSV = re.compile(r"^p(\d+)_t(\d+)\.csv$")

# Planilha ja costurada pelo extrair_digitalizados.py, de uma pagina a outra.
RE_COSTURADA = re.compile(r"^planilha_p(\d+)-p(\d+)\.csv$")

# Cabecalho da planilha orcamentaria: primeira coluna "Item" e alguma coluna
# "Valor Total". Serve para achar onde a planilha comeca.
RE_ITEM = re.compile(r"(?i)^item$")
RE_VALOR_TOTAL = re.compile(r"(?i)^valor\s*total$")


def dobrar(texto: str) -> str:
    """Minuscula, sem acento e sem espaco - forma usada so em comparacao."""
    return sem_acento(" ".join(texto.split()).lower()).replace(" ", "")


def limpar(celula: str) -> str:
    return " ".join((celula or "").split())


def normalizar_decimal(celula: str):
    """Reescreve a celula que e SO um valor monetario. Devolve (texto, mudou).

    Celula com texto em volta nao e tocada: 'ate 8 (oito) impressoras' nao e
    numero, e '40h/semanais X 15 MESES' tambem nao.
    """
    s = limpar(celula)
    if not s:
        return celula, False
    m = RE_CIFRAO.match(s)
    corpo = s[m.end():] if m else s
    if not RE_MOEDA.fullmatch(corpo):
        return celula, False
    novo = reais(valor_moeda(corpo), cifrao=False)
    if m:
        novo = "R$ " + novo
    return novo, novo != s


# ------------------------------------------------------------- correcoes -----

CAMPOS_CORRECAO = ["plano", "arquivo", "linha", "campo", "valor_novo",
                   "classe", "motivo"]


def ler_correcoes(caminho: Path):
    """{(arquivo, linha): [(campo, valor_novo, motivo)]} da classe forma.

    Classe `documento` e recusada aqui de proposito: defeito do documento nao
    se conserta na copia, se registra em achados.csv.
    """
    if not caminho or not caminho.exists():
        return {}, []
    por_alvo = defaultdict(list)
    recusadas = []
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        faltando = [c for c in CAMPOS_CORRECAO if c not in (leitor.fieldnames or [])]
        if faltando:
            sys.exit(f"{caminho}: faltam as colunas {', '.join(faltando)}")
        for n, linha in enumerate(leitor, 2):
            classe = (linha["classe"] or "").strip().lower()
            if classe != "forma":
                recusadas.append((n, classe, linha["arquivo"]))
                continue
            arquivo = (linha["arquivo"] or "").strip().replace("\\", "/")
            por_alvo[(arquivo, int(linha["linha"]))].append(
                ((linha["campo"] or "").strip(),
                 linha["valor_novo"] or "",
                 (linha["motivo"] or "").strip()))
    return dict(por_alvo), recusadas


def indice_do_campo(campo: str, cabecalho, largura: int):
    """Numero 1-based da coluna, seja pelo numero, seja pelo nome do cabecalho."""
    if campo.isdigit():
        i = int(campo)
        return i if 1 <= i <= largura else None
    alvo = dobrar(campo)
    for i, nome in enumerate(cabecalho, 1):
        if dobrar(nome) == alvo:
            return i
    return None


def aplicar_correcoes(rel, linhas, correcoes, resumo):
    """[(n, celulas)] da CSV, com as correcoes aplicadas.

    `n` e o numero da linha na CSV de origem, 1-based. O cabecalho montado a
    partir das correcoes de linha 0 entra com n = 0 - a coordenada das outras
    linhas nao muda.
    """
    largura = max((len(l) for l in linhas), default=0)
    numeradas = list(enumerate(linhas, 1))

    montado = correcoes.get((rel, 0))
    if montado:
        cabecalho = [""] * largura
        for campo, valor_novo, _ in montado:
            i = int(campo) if campo.isdigit() else None
            if i is None or not 1 <= i <= largura:
                resumo["sem_alvo"].append((rel, 0, campo))
                continue
            cabecalho[i - 1] = valor_novo
            resumo["correcoes"] += 1
        numeradas.insert(0, (0, cabecalho))

    cabecalho = numeradas[0][1] if numeradas else []
    for n, linha in numeradas:
        if n == 0:
            continue
        for campo, valor_novo, _ in correcoes.get((rel, n), []):
            i = indice_do_campo(campo, cabecalho, largura)
            if i is None or i > len(linha):
                resumo["sem_alvo"].append((rel, n, campo))
                continue
            linha[i - 1] = valor_novo
            resumo["correcoes"] += 1
    return numeradas


# --------------------------------------------------------------- tabelas -----

def ler_csv(caminho: Path):
    with caminho.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def escrever_csv(caminho: Path, linhas):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(linhas)


def e_cabecalho_planilha(linha) -> bool:
    celulas = [limpar(c) for c in linha]
    return (any(RE_ITEM.match(c) for c in celulas)
            and any(RE_VALOR_TOTAL.match(c) for c in celulas))


def largura_de(numeradas) -> int:
    return max((len(l) for _, l in numeradas), default=0)


def cadeia_planilha(tabelas):
    """Lista de (pagina, caminho) da planilha orcamentaria, em ordem.

    Comeca na CSV cujo cabecalho e o da planilha e segue enquanto as paginas
    forem consecutivas e houver na pagina alguma CSV da mesma largura. A matriz
    de risco do pt_ses_04 tambem tem 8 colunas, mas fica antes do cabecalho e
    por isso nao entra.
    """
    paginas = sorted(tabelas)
    inicio = None
    for pagina in paginas:
        for caminho, numeradas in tabelas[pagina]:
            if numeradas and e_cabecalho_planilha(numeradas[0][1]):
                inicio = (pagina, caminho, largura_de(numeradas))
                break
        if inicio:
            break
    if not inicio:
        return [], 0

    pagina_ini, caminho_ini, largura = inicio
    cadeia = []
    pagina = pagina_ini
    while pagina in tabelas:
        do_tamanho = [(c, l) for c, l in tabelas[pagina]
                      if l and largura_de(l) == largura
                      and (pagina > pagina_ini or c >= caminho_ini)]
        if not do_tamanho:
            break
        cadeia.extend((pagina, c) for c, _ in do_tamanho)
        pagina += 1
    return cadeia, largura


def e_continuacao(linha) -> bool:
    """Rabicho de item que virou a pagina: sem codigo, sem valor, com texto."""
    celulas = [limpar(c) for c in linha]
    if len(celulas) < 3:
        return False
    return (not celulas[0] and not celulas[-1]
            and any(celulas[1:-1]))


# Codigo de item: so digito e ponto, com pelo menos um ponto (1.2.4, 1.24).
RE_CODIGO = re.compile(r"^\d+(?:\.\d+)+$")


def tratar_linhas(numeradas, assinatura_cabecalho, resumo):
    """Remove linha vazia e cabecalho repetido; normaliza decimal.

    A primeira coluna e a do codigo do item e fica fora da normalizacao
    decimal quando e so digito e ponto: o OCR le "1.2.4" como "1.24", que tem
    cara de R$ 1,24, e a normalizacao o reescrevia como "1,24" - um codigo
    virava dinheiro e passava a entrar como fator na verificacao D.
    """
    saida = []
    for k, (n, linha) in enumerate(numeradas):
        if all(not limpar(c) for c in linha):
            resumo["linhas_vazias"] += 1
            continue
        if (k > 0 and assinatura_cabecalho
                and [dobrar(c) for c in linha] == assinatura_cabecalho):
            resumo["cabecalho_repetido"] += 1
            continue
        nova = []
        for j, celula in enumerate(linha):
            if j == 0 and RE_CODIGO.fullmatch(limpar(celula)):
                nova.append(celula)
                continue
            texto, mudou = normalizar_decimal(celula)
            resumo["decimais"] += 1 if mudou else 0
            nova.append(texto)
        saida.append((n, nova))
    return saida


def limpar_saida(destino: Path):
    """Apaga o que uma rodada anterior escreveu e esta rodada vai reescrever.

    Sem isso, CSV que sumiu da extracao - reprocessada com outro ajuste, a
    numeracao tNN mudou - continuava em normalizados/ e contaminava a
    conferencia, e o "apagar e reconstruir da igual" deixava de ser verdade.
    """
    for antiga in (destino / "tabelas").glob("*.csv"):
        antiga.unlink()
    for nome in ("planilha.csv", "tratamento.yaml"):
        (destino / nome).unlink(missing_ok=True)


def tratar_documento(doc_id, dir_doc: Path, destino: Path, correcoes,
                     rotulo_fonte: str = "extraidos/"):
    """Trata um documento inteiro. Devolve o resumo do que foi aplicado."""
    resumo = {"csvs": 0, "correcoes": 0, "cabecalho_repetido": 0,
              "linhas_vazias": 0, "decimais": 0, "emendas": 0,
              "planilha_linhas": 0, "planilha_csvs": 0, "sem_alvo": [],
              "costurada": ""}

    destino.mkdir(parents=True, exist_ok=True)
    limpar_saida(destino)
    shutil.copyfile(dir_doc / "texto.md", destino / "texto.md")

    # ------------------------------------------------- leitura e correcao ---
    tabelas = defaultdict(list)
    costuradas = []
    for caminho in sorted((dir_doc / "tabelas").glob("*.csv")):
        m = RE_CSV.match(caminho.name)
        mc = RE_COSTURADA.match(caminho.name)
        if not (m or mc):
            continue
        rel = f"{doc_id}/tabelas/{caminho.name}"
        numeradas = aplicar_correcoes(rel, ler_csv(caminho), correcoes, resumo)
        if m:
            tabelas[int(m.group(1))].append((caminho, numeradas))
        else:
            costuradas.append((int(mc.group(1)), int(mc.group(2)), caminho,
                               numeradas))

    cadeia, largura_planilha = cadeia_planilha(tabelas)
    da_planilha = set(cadeia)
    cabecalho_planilha = None
    assinatura_cabecalho = []
    if cadeia:
        pagina, caminho = cadeia[0]
        primeira = next(l for c, l in tabelas[pagina] if c == caminho)
        cabecalho_planilha = [limpar(c) for c in primeira[0][1]]
        # A repeticao do cabecalho no meio da planilha costuma vir com a quebra
        # de palavra em coluna diferente da primeira ("Frequê ncia" numa,
        # "Frequênci a" noutra). A comparacao ignora espaco e acento, senao a
        # repeticao passa batida so por causa de onde o Word quebrou a palavra.
        assinatura_cabecalho = [dobrar(c) for c in cabecalho_planilha]

    # ------------------------------------------------------- tratamento ----
    tratadas = {}
    for pagina in sorted(tabelas):
        for caminho, numeradas in tabelas[pagina]:
            resumo["csvs"] += 1
            assinatura = (assinatura_cabecalho
                          if (pagina, caminho) in da_planilha else [])
            saida = tratar_linhas(numeradas, assinatura, resumo)
            tratadas[caminho] = saida
            escrever_csv(destino / "tabelas" / caminho.name,
                         [linha for _, linha in saida])

    # ------------------------------------------------------ consolidacao ---
    consolidada, cabecalho = [], None
    if costuradas:
        # A planilha ja veio costurada pela grade da imagem: e ela a
        # consolidada. Uma so por documento - mais de uma seria ambiguidade
        # que o tratamento nao tem como decidir sozinho.
        if len(costuradas) > 1:
            sys.exit(f"{doc_id}: mais de uma planilha costurada em {dir_doc}")
        ini, fim, caminho, numeradas = costuradas[0]
        resumo["csvs"] += 1
        primeira = numeradas[0][1] if numeradas else []
        if not e_cabecalho_planilha(primeira):
            sys.exit(f"{doc_id}: {caminho.name} nao comeca pelo cabecalho da "
                     f"planilha (Item ... Valor Total). Registre o cabecalho "
                     f"como linha 0 em correcoes.csv.")
        largura_planilha = largura_de(numeradas)
        cabecalho_planilha = [limpar(c) for c in primeira]
        assinatura = [dobrar(c) for c in cabecalho_planilha]
        saida = tratar_linhas(numeradas, assinatura, resumo)
        escrever_csv(destino / "tabelas" / caminho.name,
                     [linha for _, linha in saida])
        cabecalho = ["pagina_origem", "csv_origem"] + cabecalho_planilha
        for n, linha in saida[1:]:
            celulas = list(linha) + [""] * (largura_planilha - len(linha))
            consolidada.append([f"{ini}-{fim}", f"{caminho.name}:{n}"]
                               + celulas[:largura_planilha])
        resumo["planilha_csvs"] = fim - ini + 1
        resumo["costurada"] = caminho.name
    elif cadeia:
        cabecalho = ["pagina_origem", "csv_origem"] + cabecalho_planilha
        for k, (pagina, caminho) in enumerate(cadeia):
            # Rabicho so existe na virada de PAGINA: segunda CSV da mesma
            # pagina comeca linha nova, nao continua a anterior.
            vira_pagina = k > 0 and cadeia[k - 1][0] != pagina
            for n, linha in tratadas[caminho]:
                origem = f"{caminho.name}:{n}"
                if vira_pagina and n == 1 and consolidada and e_continuacao(linha):
                    anterior = consolidada[-1]
                    for i, celula in enumerate(linha):
                        if limpar(celula):
                            j = i + 2
                            anterior[j] = (anterior[j] + " " + limpar(celula)).strip()
                    anterior[1] = anterior[1] + ";" + origem
                    resumo["emendas"] += 1
                    continue
                if [dobrar(c) for c in linha] == assinatura_cabecalho:
                    continue
                celulas = list(linha) + [""] * (largura_planilha - len(linha))
                consolidada.append([str(pagina), origem] + celulas[:largura_planilha])
        resumo["planilha_csvs"] = len(cadeia)

    if cabecalho:
        escrever_csv(destino / "planilha.csv", [cabecalho] + consolidada)
        resumo["planilha_linhas"] = len(consolidada)

    # ------------------------------------------------------- tratamento.yaml
    linhas_yaml = [
        f'id: "{doc_id}"',
        f'fonte: "{rotulo_fonte}"',
        f"csvs_tratadas: {resumo['csvs']}",
        f"correcoes_aplicadas: {resumo['correcoes']}",
        f"cabecalhos_repetidos_removidos: {resumo['cabecalho_repetido']}",
        f"linhas_vazias_removidas: {resumo['linhas_vazias']}",
        f"decimais_normalizados: {resumo['decimais']}",
        f"planilha_csvs_de_origem: {resumo['planilha_csvs']}",
        f"planilha_linhas: {resumo['planilha_linhas']}",
        f"planilha_linhas_emendadas: {resumo['emendas']}",
    ]
    if resumo["costurada"]:
        linhas_yaml.append(f'planilha_costurada_na_extracao: "{resumo["costurada"]}"')
    linhas_yaml += [
        f'origem: "{rotulo_fonte} (bruto) + registros/correcoes.csv"',
        'derivado: "apagar esta pasta e rodar tratar_planos.py reproduz byte a byte"',
    ]
    escrever_texto(destino / "tratamento.yaml", "\n".join(linhas_yaml) + "\n")
    return resumo


def documentos(pasta: Path):
    if not pasta or not pasta.is_dir():
        return {}
    return {d.name: d for d in sorted(pasta.iterdir())
            if d.is_dir() and (d / "texto.md").exists()}


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("extraidos")
    ap.add_argument("normalizados")
    ap.add_argument("--doc", action="append",
                    help="so este id (pode repetir); padrao: todos")
    ap.add_argument("--correcoes", default=str(REGISTROS / "correcoes.csv"))
    ap.add_argument("--ocr", default=str(EXTRAIDOS_OCR),
                    help="pasta do extrair_digitalizados.py; o documento que "
                         "existir la vem de la (padrao: estudo/extraidos_ocr)")
    args = ap.parse_args()

    saida_utf8()

    origem = Path(args.extraidos)
    destino = Path(args.normalizados)
    if not origem.is_dir():
        sys.exit(f"Pasta nao encontrada: {origem}")

    correcoes, recusadas = ler_correcoes(Path(args.correcoes))
    for n, classe, arquivo in recusadas:
        print(f"AVISO {args.correcoes}:{n} classe '{classe}' ignorada "
              f"({arquivo}). So classe 'forma' entra aqui; defeito do "
              f"documento vai para achados.csv.")

    fontes = documentos(origem)
    pasta_ocr = Path(args.ocr) if args.ocr else None
    for doc_id, dir_doc in documentos(pasta_ocr).items():
        fontes[doc_id] = dir_doc

    ids = sorted(fontes)
    if args.doc:
        pedidos = {d.lower() for d in args.doc}
        ids = [i for i in ids if i in pedidos]
        if not ids:
            sys.exit("Nenhum documento corresponde a --doc")

    destino.mkdir(parents=True, exist_ok=True)
    for doc_id in ids:
        dir_doc = fontes[doc_id]
        rotulo = dir_doc.parent.name + "/"
        print(f"-> {doc_id}" + (f"   (de {rotulo})" if dir_doc.parent != origem else ""))
        resumo = tratar_documento(doc_id, dir_doc, destino / doc_id, correcoes,
                                  rotulo)
        print(f"   {resumo['csvs']} CSVs; {resumo['correcoes']} correcao(oes), "
              f"{resumo['cabecalho_repetido']} cabecalho(s) repetido(s), "
              f"{resumo['linhas_vazias']} linha(s) vazia(s), "
              f"{resumo['decimais']} decimal(is) normalizado(s)")
        if resumo["costurada"]:
            print(f"   planilha.csv: {resumo['planilha_linhas']} linhas da "
                  f"planilha costurada {resumo['costurada']}")
        elif resumo["planilha_csvs"]:
            print(f"   planilha.csv: {resumo['planilha_linhas']} linhas de "
                  f"{resumo['planilha_csvs']} CSVs, "
                  f"{resumo['emendas']} emendada(s) na virada de pagina")
        else:
            print("   planilha orcamentaria nao localizada - sem planilha.csv")
        for rel, n, campo in resumo["sem_alvo"]:
            print(f"   AVISO correcao sem alvo: {rel}:{n} campo '{campo}'")

    print("\nProximo passo: conferir.py nos dois lados e comparar - "
          "o que sobrar em normalizados/ e defeito do documento.")


if __name__ == "__main__":
    main()
