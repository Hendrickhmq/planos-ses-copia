#!/usr/bin/env python3
"""
verificar_registros.py - os registros/*.csv conferidos contra o schema.md e o disco.

Uso:
    python verificar_registros.py            relatorio
    python verificar_registros.py --erros    so os erros

POR QUE ISTO EXISTE

Os registros sao dado versionado a mao, e o schema.md so vale enquanto alguem
lembra de olhar para ele. Nesta pasta ja apareceram, sem ninguem notar: id fora
do padrao ("Portaria GM/MS 10.297/2026" onde o schema pede NM-xxx), especie que
o schema nao tem, texto de um campo no campo vizinho, nome de arquivo gravado
pelo Mac em Unicode decomposto - que o Windows nao casa com o arquivo do disco -
e quatro normas baixadas para normas/ sem linha no acervo.

DUAS CLASSES

ERRO      o registro contradiz o schema ou o disco: id repetido ou fora do
          padrao, valor fora da lista, referencia para id que nao existe,
          arquivo que nao esta onde o registro diz. Codigo de saida 1.
PENDENTE  falta um dado que so uma pessoa pode dar: a URL de onde a norma foi
          baixada, a data do acesso, a conferencia da extracao. Nao falha - e
          a lista do que fazer, e ninguem a inventa.

As listas de valores aqui ESPELHAM o schema.md. Mudou o schema, muda aqui - e
o schema manda: "alterar aqui antes de alterar qualquer arquivo em registros/".

So biblioteca padrao.
"""

import argparse
import csv
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

from comum import (CONTROLE, EXTRAIDOS, EXTRAIDOS_OCR, NORMAS, PLANOS_APROVADOS,
                   RAIZ, REGISTROS)
REG = REGISTROS

# --------------------------------------------------------- espelho do schema

PADRAO_ID = {
    "plano": r"pt_ses_\d{2}",
    "norma": r"NM-\d{3}",
    "controle": r"CT-\d{3}",
    "instrumento": r"IT-\d{3}",
    "dado": r"DD-\d{3}",
}

HIERARQUIA = {
    "constituicao": 1,
    "lei": 2, "lei_complementar": 2, "lei_distrital": 2,
    "decreto": 3, "decreto_distrital": 3,
    "portaria": 4, "resolucao": 4, "portaria_consolidacao": 4, "deliberacao": 4,
    "instrucao_normativa": 5, "manual": 5,
    "nota_tecnica": 6,
}

ESPECIES = {
    "norma": set(HIERARQUIA),
    "controle": {"parecer_juridico", "parecer_referencial", "parecer_tecnico",
                 "acordao", "decisao", "checklist", "relatorio_preliminar",
                 "oficio", "termo_aprovacao", "notificacao", "representacao"},
    "plano": {"plano_trabalho"},
    "instrumento": {"termo_convenio", "termo_aditivo", "termo_apostilamento"},
    "dado": {"painel", "tabela_comparativa", "planilha", "extracao_sistema"},
}

INSTRUMENTOS = {"convenio", "contrato", "termo_fomento", "credenciamento", "-"}
SITUACOES = {"vigente", "revogada", "alterada", "a_verificar", "aprovado", "-"}
ACESSOS = {"integral", "so_indice", "restrito"}
SIM_NAO = {"sim", "nao"}

# Onde o `arquivo` de cada tipo mora.
# Caminhos relativos a RAIZ, para que o teste possa trocar a RAIZ por uma pasta temporaria.
_rel = lambda p: p.relative_to(RAIZ).as_posix()
PASTA_NORMAS = _rel(NORMAS)
PASTAS_EXTRACAO = (_rel(EXTRAIDOS), _rel(EXTRAIDOS_OCR))
PASTAS_ARQUIVO = {
    "plano": [_rel(PLANOS_APROVADOS)],
    "norma": [PASTA_NORMAS, PASTA_NORMAS + "/_substituidos"],
    "controle": [_rel(CONTROLE)],
    "instrumento": [_rel(CONTROLE)],
    "dado": [_rel(REGISTROS / "fontes")],
}

OBRIGACAO_NATUREZA = {"legal", "infralegal", "interpretativa", "contratual"}
OBRIGACAO_STATUS = {"vigente", "revogado", "inaplicavel", "a_verificar"}
ACHADO_CLASSIFICACAO = {"exigido_norma", "exigido_parecer", "pratica_ses", "idiossincrasia"}
ACHADO_QUALIDADE = {"bom_exemplo", "aceitavel", "falha", "neutro"}

# Achado que atravessa varios planos: "pt_ses_01..04".
RE_FAIXA_PLANOS = re.compile(r"(pt_ses_)(\d{2})\.\.(\d{2})")
EXIGENCIA_CUMPRIDA = {"sim", "parcial", "nao"}
CORRECAO_CLASSE = {"forma", "documento"}
CONFERENCIA_RESULTADO = {"ok", "com_achado"}
CONFERENCIA_PASTA = {"extraidos", "extraidos_ocr", "normalizados", ""}
LICAO_EIXO = {"administracao", "qualidade"}
LICAO_TEMA = {"codigos_sigtap", "valor_unitario", "objeto", "enquadramento_cnes", "metas",
              "dimensionamento",
              "custo_apoio", "precos", "sobreposicao", "capacidade_executor", "instrumento",
              "desembolso_vigencia", "faturamento_sus", "controle_social", "riscos",
              "redacao", "uso_do_acervo", "diligencia"}
LICAO_TIPO = {"erro", "acerto"}
LICAO_GRAVIDADE = {"reprova", "questiona", "melhora"}
RE_VERIFICACAO = re.compile(r"manual|(automatica|parcial):([A-Z](?:,[A-Z])*)")


# ------------------------------------------------------------------ apoio

class Relatorio:
    """Erros um a um; pendencias agrupadas pelo que falta, com a lista de ids."""

    def __init__(self):
        self.erros, self.pendentes = [], {}

    def erro(self, onde, msg):
        self.erros.append(f"{onde}: {msg}")

    def pendente(self, id_, msg):
        self.pendentes.setdefault(msg, []).append(id_)


def ler(nome):
    caminho = REG / nome
    if not caminho.exists():
        return None, []
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        return leitor.fieldnames, [(n, l) for n, l in enumerate(leitor, 2)]


def data_valida(txt):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", txt):
        return False
    try:
        date.fromisoformat(txt)
        return True
    except ValueError:
        return False


def nfc(txt):
    return unicodedata.normalize("NFC", txt)


def conferir_texto(rel, onde, linha):
    """Unicode decomposto em qualquer campo: e o que o Mac grava em nome de arquivo."""
    for campo, valor in linha.items():
        if valor and not unicodedata.is_normalized("NFC", valor):
            rel.erro(onde, f"{campo} em Unicode decomposto (NFD) - normalize para NFC")


def ids_unicos(rel, arquivo, linhas, padrao):
    vistos = set()
    for n, l in linhas:
        i = l.get("id", "")
        if not re.fullmatch(padrao, i):
            rel.erro(f"{arquivo}:{n}", f"id '{i}' fora do padrao {padrao}")
        if i in vistos:
            rel.erro(f"{arquivo}:{n}", f"id '{i}' repetido")
        vistos.add(i)
    return vistos


def no_conjunto(rel, onde, campo, valor, permitidos, vazio_ok=False):
    if vazio_ok and not valor:
        return
    if valor not in permitidos:
        rel.erro(onde, f"{campo} '{valor}' fora do schema ({', '.join(sorted(p for p in permitidos if p))})")


# ------------------------------------------------------------------ acervo

def verificar_acervo(rel):
    _, linhas = ler("acervo.csv")
    ids = set()
    arquivos_citados = set()
    for n, l in linhas:
        onde = f"acervo.csv:{n} ({l['id']})"
        conferir_texto(rel, onde, l)
        tipo = l["tipo"]
        if tipo not in PADRAO_ID:
            rel.erro(onde, f"tipo '{tipo}' fora do schema")
            continue
        if not re.fullmatch(PADRAO_ID[tipo], l["id"]):
            rel.erro(onde, f"id fora do padrao de {tipo} ({PADRAO_ID[tipo]})")
        if l["id"] in ids:
            rel.erro(onde, "id repetido")
        ids.add(l["id"])

        no_conjunto(rel, onde, "especie", l["especie"], ESPECIES[tipo])
        if tipo == "norma":
            esperada = HIERARQUIA.get(l["especie"])
            if esperada is not None and l["hierarquia"] != str(esperada):
                rel.erro(onde, f"hierarquia {l['hierarquia'] or '(vazia)'} para "
                               f"'{l['especie']}'; o schema da {esperada}")
        elif l["hierarquia"]:
            rel.erro(onde, "hierarquia so vale para tipo norma")

        no_conjunto(rel, onde, "instrumento", l["instrumento"], INSTRUMENTOS)
        no_conjunto(rel, onde, "situacao", l["situacao"], SITUACOES)
        no_conjunto(rel, onde, "acesso", l["acesso"], ACESSOS, vazio_ok=True)
        no_conjunto(rel, onde, "extracao_conferida", l["extracao_conferida"], SIM_NAO)
        for campo in ("data_doc", "data_acesso"):
            if l[campo] and not data_valida(l[campo]):
                rel.erro(onde, f"{campo} '{l[campo]}' nao e AAAA-MM-DD")
        if l["paginas"] and not l["paginas"].isdigit():
            rel.erro(onde, f"paginas '{l['paginas']}' nao e inteiro")

        arquivo = nfc(l["arquivo"])
        if arquivo:
            arquivos_citados.add(arquivo)
            pastas = PASTAS_ARQUIVO[tipo]
            if not any((RAIZ / p / arquivo).is_file() for p in pastas):
                rel.erro(onde, f"arquivo '{arquivo}' nao esta em {' nem '.join(p + '/' for p in pastas)}")
            url = l["url"]
            if not url:
                rel.pendente(l["id"], "url de onde o arquivo foi baixado")
            elif not url.startswith(("http://", "https://")) and not (RAIZ / url).exists():
                rel.pendente(l["id"], "url que seja endereco (hoje traz a citacao do DOU)")
            if not l["data_acesso"]:
                rel.pendente(l["id"], "data_acesso (quando o arquivo foi baixado)")
            if not l["acesso"]:
                rel.pendente(l["id"], "acesso (integral, so_indice ou restrito)")
            if l["extracao_conferida"] == "nao":
                rel.pendente(l["id"], "extracao_conferida: conferir o texto extraido contra o PDF")

    # PDF baixado sem linha no acervo nao tem proveniencia
    for pdf in sorted((RAIZ / PASTA_NORMAS).glob("*.pdf")):
        if nfc(pdf.name) not in arquivos_citados:
            rel.erro(f"{PASTA_NORMAS}/{nfc(pdf.name)}", "PDF sem linha em acervo.csv")
    return ids


# ------------------------------------------------------------- os outros

def verificar_obrigacoes(rel, ids_acervo):
    _, linhas = ler("obrigacoes.csv")
    ids = ids_unicos(rel, "obrigacoes.csv", linhas, r"OB-\d{3}")
    for n, l in linhas:
        onde = f"obrigacoes.csv:{n} ({l['id']})"
        conferir_texto(rel, onde, l)
        if l["acervo_id"] not in ids_acervo:
            rel.erro(onde, f"acervo_id '{l['acervo_id']}' nao existe em acervo.csv")
        no_conjunto(rel, onde, "natureza", l["natureza"], OBRIGACAO_NATUREZA)
        no_conjunto(rel, onde, "status_vigencia", l["status_vigencia"], OBRIGACAO_STATUS)
        if l["data_verificacao"] and not data_valida(l["data_verificacao"]):
            rel.erro(onde, f"data_verificacao '{l['data_verificacao']}' nao e AAAA-MM-DD")
    return ids


def ids_referidos(acervo_id):
    """'pt_ses_01..04' -> [pt_ses_01, ..., pt_ses_04]; outro id -> [id]."""
    m = RE_FAIXA_PLANOS.fullmatch(acervo_id)
    if not m:
        return [acervo_id]
    ini, fim = int(m.group(2)), int(m.group(3))
    return [f"{m.group(1)}{k:02d}" for k in range(ini, fim + 1)] if ini < fim else [acervo_id]


def verificar_achados(rel, ids_acervo, ids_obrigacoes):
    _, linhas = ler("achados.csv")
    ids = ids_unicos(rel, "achados.csv", linhas, r"AC-\d{3}")
    for n, l in linhas:
        onde = f"achados.csv:{n} ({l['id']})"
        conferir_texto(rel, onde, l)
        faltam = [i for i in ids_referidos(l["acervo_id"]) if i not in ids_acervo]
        if faltam:
            rel.erro(onde, f"acervo_id '{l['acervo_id']}' - nao existe em acervo.csv: {', '.join(faltam)}")
        no_conjunto(rel, onde, "classificacao", l["classificacao"], ACHADO_CLASSIFICACAO)
        no_conjunto(rel, onde, "qualidade", l["qualidade"], ACHADO_QUALIDADE)
        vira = l.get("vira_obrigacao_id", "")
        if vira and vira not in ids_obrigacoes:
            rel.erro(onde, f"vira_obrigacao_id '{vira}' nao existe em obrigacoes.csv")
    return ids


def verificar_exigencias(rel):
    _, linhas = ler("exigencias_resposta.csv")
    ids = ids_unicos(rel, "exigencias_resposta.csv", linhas, r"EX-\d{3}")
    for n, l in linhas:
        onde = f"exigencias_resposta.csv:{n}"
        no_conjunto(rel, onde, "cumprida_integralmente", l["cumprida_integralmente"],
                    EXIGENCIA_CUMPRIDA)
        if l["data_origem"] and not data_valida(l["data_origem"]):
            rel.erro(onde, f"data_origem '{l['data_origem']}' nao e AAAA-MM-DD")
    return ids


def letras_do_conferir_plano():
    """as verificacoes que o conferir_plano.py tem: uma funcao verificar_<letra> cada"""
    caminho = Path(__file__).resolve().parent / "conferir_plano.py"
    if not caminho.exists():
        return None
    return set(re.findall(r"^def verificar_([A-Z])\b", caminho.read_text(encoding="utf-8"), re.M))


def verificar_licoes(rel, ids_conhecidos):
    _, linhas = ler("licoes.csv")
    ids_unicos(rel, "licoes.csv", linhas, r"LI-\d{3}")
    letras = letras_do_conferir_plano()
    for n, l in linhas:
        onde = f"licoes.csv:{n} ({l['id']})"
        conferir_texto(rel, onde, l)
        no_conjunto(rel, onde, "eixo", l["eixo"], LICAO_EIXO)
        no_conjunto(rel, onde, "tema", l["tema"], LICAO_TEMA)
        no_conjunto(rel, onde, "tipo", l["tipo"], LICAO_TIPO)
        no_conjunto(rel, onde, "gravidade", l["gravidade"], LICAO_GRAVIDADE)
        if not l["regra"].strip() or not l["por_que"].strip():
            rel.erro(onde, "licao sem regra ou sem por_que")
        origem = [i.strip() for i in l["origem"].split(";") if i.strip()]
        if not origem:
            rel.erro(onde, "licao sem origem")
        for i in origem:
            if i not in ids_conhecidos:
                rel.erro(onde, f"origem '{i}' nao existe nos registros")
        m = RE_VERIFICACAO.fullmatch(l["verificacao"])
        if not m:
            rel.erro(onde, f"verificacao '{l['verificacao']}' fora do formato "
                           "manual | automatica:<letras> | parcial:<letras>")
            continue
        if m.group(2) and letras is not None:
            for x in m.group(2).split(","):
                if x not in letras:
                    rel.erro(onde, f"verificacao cita '{x}', que o conferir_plano.py nao tem")
        if m.group(1) != "automatica" and not l["pergunta"].strip():
            rel.erro(onde, "verificacao manual ou parcial sem pergunta")


def verificar_correcoes(rel):
    _, linhas = ler("correcoes.csv")
    for n, l in linhas:
        onde = f"correcoes.csv:{n}"
        no_conjunto(rel, onde, "classe", l["classe"], CORRECAO_CLASSE)
        if not l["arquivo"].startswith(l["plano"] + "/"):
            rel.erro(onde, f"arquivo '{l['arquivo']}' nao e do plano {l['plano']}")
        if not any((RAIZ / pasta / l["arquivo"]).is_file()
                   for pasta in PASTAS_EXTRACAO):
            rel.erro(onde, f"arquivo '{l['arquivo']}' nao existe em {' nem '.join(p + '/' for p in PASTAS_EXTRACAO)}")
        if not l["linha"].isdigit():
            rel.erro(onde, f"linha '{l['linha']}' nao e inteiro >= 0")
        if l["linha"] == "0" and not l["campo"].isdigit():
            rel.erro(onde, "linha 0 (cabecalho montado) pede campo pelo numero da coluna")
        if not l["motivo"].strip():
            rel.erro(onde, "correcao sem motivo")


def verificar_conferencia(rel):
    _, linhas = ler("conferencia.csv")
    for n, l in linhas:
        onde = f"conferencia.csv:{n} ({l['plano']})"
        no_conjunto(rel, onde, "resultado", l["resultado"], CONFERENCIA_RESULTADO)
        no_conjunto(rel, onde, "pasta", l.get("pasta", ""), CONFERENCIA_PASTA)
        if not re.fullmatch(r"[0-9a-f]{64}", l["sha256"]):
            rel.erro(onde, "sha256 invalido")
        if not l["conferido_por"]:
            rel.erro(onde, "marcacao sem dono")
        if not data_valida(l["data"]):
            rel.erro(onde, f"data '{l['data']}' nao e AAAA-MM-DD")


def verificar():
    rel = Relatorio()
    ids_acervo = verificar_acervo(rel)
    ids_obrigacoes = verificar_obrigacoes(rel, ids_acervo)
    ids_achados = verificar_achados(rel, ids_acervo, ids_obrigacoes)
    ids_exigencias = verificar_exigencias(rel)
    verificar_licoes(rel, ids_acervo | ids_obrigacoes | ids_achados | ids_exigencias)
    verificar_correcoes(rel)
    verificar_conferencia(rel)
    return rel


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--erros", action="store_true", help="nao lista as pendencias")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    rel = verificar()
    print(f"ERROS: {len(rel.erros)}")
    for e in rel.erros:
        print(f"  {e}")
    if not args.erros:
        total = sum(len(v) for v in rel.pendentes.values())
        print(f"\nPENDENTES (dado que so uma pessoa pode dar): {total}")
        for msg, ids in rel.pendentes.items():
            print(f"  falta {msg} - {len(ids)}: {', '.join(ids)}")
    return 1 if rel.erros else 0


if __name__ == "__main__":
    sys.exit(main())
