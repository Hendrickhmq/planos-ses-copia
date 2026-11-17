#!/usr/bin/env python3
"""
conferir_plano.py - conferencia do plano de trabalho redigido.

Nao altera nada. Le plano.md, estado.yaml, dados/*.md e pendencias.md do plano
indicado, recalcula tudo o que o documento afirma e compara.

Uso:
    python3 conferir_plano.py redacao_03/
    python3 conferir_plano.py redacao_03/ --verboso

Vale para QUALQUER plano do projeto. Os parametros que mudam de plano para plano -
recurso, valor unitario, vigencia, meses de producao, dias uteis e nomes dos polos -
sao lidos do estado.yaml do proprio plano; a estrutura das secoes vem de metodo/plano/estrutura.md
na raiz; as normas, de normas/. Nada de um plano especifico e constante aqui.

POR QUE ISTO EXISTE

conferir.py confere EXTRACAO - PDF contra texto.md e CSVs. Aqui o objeto e
outro: o documento que nos escrevemos. O erro que se quer pegar nao e de
leitura, e de coerencia - numero que muda de secao para secao, subtotal que nao
fecha, parametro que o documento afirma e a conta nao sustenta, regra de metodo
violada.

AS VERIFICACOES

NUMERICAS
  A  PRODUTO POR LINHA   valor total de cada linha da planilha = qtd x unitario
                         x meses. Pega numero na coluna errada.
  B  SOMA DOS SUBTOTAIS  subtotal 1.1 = soma das linhas de 1.1; idem 1.2;
                         Meta 1 = 1.1 + 1.2; global = Meta 1 + Meta 2.
  C  FECHAMENTO          recurso - apoio = envelope de producao; o quantitativo
                         e o maior inteiro que cabe; a sobra e menor que um
                         unitario - se nao for, cabia mais uma OCI e a meta esta
                         subdimensionada.
  D  CURVA FISICA        a curva mensal soma o quantitativo; o regime pleno
                         dividido por 21 da as entradas por dia util afirmadas.
  E  RATEIO POR POLO     a soma dos polos = quantitativo; as participacoes
                         recalculadas da fila batem com as publicadas.
  F  DESEMBOLSO          as parcelas somam o global; cada parcela = apoio do
                         periodo + OCI do periodo x unitario; os meses cobertos
                         formam 1..10 sem buraco nem sobreposicao.
  G  CAPACIDADE POR POLO na tabela de capacidade com coluna de total, os polos
                         somam o total. O recalculo a partir dos tempos de sala
                         e de aparelho e do objeto: mora na bateria do plano.

DE COERENCIA
  H  ENTRE ARQUIVOS      os numeros-chave sao identicos em plano.md,
                         estado.yaml, dados/envelope.md e pendencias.md.
  I  FILA EXTERNA        os numeros do Mapa Social no documento batem com os
                         registrados em estado.yaml, e as sete regioes somam.

DE ESTRUTURA E METODO
  J  ESTRUTURA           9 secoes na ordem padrao; subsecoes numeradas em
                         sequencia dentro de cada secao, sem buraco.
  K  FORMA DOS TITULOS   nenhum titulo comeca com Por que / O que / Como /
                         Quando - a regra dos sintagmas nominais.
  L  REGRA DO METODO     o documento nao carrega marcacao de metodo (L-xxx,
                         AC-xxx, DV-xxx, [[lacuna]]), nao escreve "custo
                         acessorio", nao publica percentual de apoio sobre o
                         global, e so tem [preencher] em campo de identificacao.

DE JULGAMENTO — as quatro de 05/09/2026, nascidas da devolutiva do professor
  S  REGUA               meta ou indicador abaixo de 100%, faixa de tolerancia,
                         quadro de pre-condicoes com coluna de comprovacao. Nada
                         disso e exigido por norma e tudo vira obrigacao afericavel.
  T  NUMERO SEM LASTRO   todo percentual e toda medida de tempo, em prosa ou em
                         celula, tem de existir no estado.yaml, em dados/, ou vir de
                         norma citada no mesmo paragrafo. Registro marcado como
                         "premissa" ou "sem fonte" nao serve de lastro, e copia
                         arquivada de plano nao entra no corpus.
  U  AUSENCIA ANUNCIADA  o plano nomeia rubrica que nao tem. E defesa antecipada, e
                         a Q nao alcanca porque esta forma nao usa enfase.
  V  FICHA               idade, quantidade maxima, valor e codigo conferidos contra
                         dados/fontes/sigtap_<codigo>_<competencia>.md. Sem a ficha,
                         FALHA: comum, regra 3, a exige na fase 0.

DO CONTROLE — as duas de 27/09/2026, da leitura dos aprovados contra o SIGTAP e as
representacoes do MPCDF (registros/licoes.csv)
  W  CODIGOS SIGTAP      todo codigo, de OCI ou de procedimento avulso, tem o
                         digito verificador certo; o do grupo 09 existe e esta
                         vigente no catalogo registros/fontes/sigtap_grupo09_<MMAAAA>
                         .csv, o nome escrito ao lado e o da tabela e a linha da
                         planilha traz o valor da tabela.
  X  RUBRICA ATACADA     taxa de administracao; comunicacao sem carater educativo
                         (audiovisual, fotografia, jornalismo, brindes); servico
                         descrito como triagem. Vedadas pelo termo ou atacadas pelo
                         MPCDF nos aprovados.

Saida: uma linha por verificacao, com PASSOU / FALHOU / NAO SE APLICA, e o
detalhe de cada divergencia. Codigo de saida 1 se qualquer uma falhar.

As letras daqui (A a X) sao as do plano redigido. As do conferir.py (A a I) sao
outra lista, sobre a extracao dos aprovados: a mesma letra nao quer dizer a
mesma coisa nos dois.

A estrutura.md e a pasta de normas sao lidas na raiz do projeto, que por padrao e a
pasta acima do plano; --raiz aponta outra (e o que o testar_conferencia_plano.py
usa para conferir uma copia do plano sem copiar o acervo).
"""
from __future__ import annotations
import argparse, importlib.util, math, re, subprocess, sys
from pathlib import Path

import comum
from comum import localizar, reais, saida_utf8, sem_acento

TOL = 0.005          # meio centavo
BASE = None          # diretorio do plano, definido em main()
RAIZ = None          # raiz do projeto
ESTRUTURA = None     # RAIZ/metodo/plano/estrutura.md
NORMAS = None        # RAIZ/normas
UNIT = None          # valor unitario da unidade produzida (plano de unidade unica)
UNITS = []           # valores unitarios declarados (plano de multiplos codigos)
MULTI = False        # True quando o objeto tem mais de um codigo/unitario
METAS_EXEC = [2]     # metas que carregam a execucao assistencial
DIRECAO = "recurso_define_fila"
RECURSO = None       # recurso disponivel
DIAS_UTEIS = 21
POLOS = []
AMBIENTE = []        # verificacoes desligadas pelo ambiente (programa ausente)

def chave(t: str) -> str:
    """minusculas sem acento — o estado.yaml e ASCII e o plano.md nao"""
    return sem_acento(t).strip().strip("*").lower()

# ------------------------------------------------------------- estado.yaml
#
# Leitura sem PyYAML, mas pela ESTRUTURA do arquivo: cada chave do caminho e
# procurada so dentro do bloco da chave anterior (as linhas mais indentadas que
# ela). A versao anterior era uma regex que atravessava o arquivo: faltando
# `valor:` dentro de `valor_unitario:`, ela devolvia o primeiro `valor:` que
# aparecesse depois, de qualquer outra secao.

RE_CHAVE_YAML = re.compile(r'^(\s*)(?:-\s+)?"?([\w.\-]+)"?\s*:(.*)$')
NULOS_YAML = {"null", "~", "none", ""}

def _sem_comentario(v: str) -> str:
    """corta o comentario ' #...' que esta fora de aspas"""
    dentro = None
    for i, c in enumerate(v):
        if c in "\"'":
            if dentro == c:
                dentro = None
            elif dentro is None:
                dentro = c
        elif c == "#" and dentro is None and (i == 0 or v[i - 1].isspace()):
            return v[:i]
    return v

def _indentacao(linha: str) -> int:
    return len(linha) - len(linha.lstrip())

def yaml_valor(txt: str, caminho: str):
    """texto do escalar em 'a.b.c', ou None se a chave nao existe ou abre bloco.

    A primeira chave e procurada no arquivo inteiro, em qualquer nivel - os
    caminhos daqui sao escritos a partir do nome que identifica a chave
    ('valor_unitario.valor'), nao da raiz ('parametros.valor_unitario.valor').
    """
    linhas = txt.splitlines()
    ini, fim, resto = 0, len(linhas), None
    for nome in caminho.split("."):
        achou = None
        for i in range(ini, fim):
            m = RE_CHAVE_YAML.match(linhas[i])
            if m and m.group(2) == nome:
                achou = (i, len(m.group(1)), m.group(3))
                break
        if achou is None:
            return None
        i, ind, resto = achou
        j = i + 1
        while j < len(linhas):
            s = linhas[j].strip()
            if s and not s.startswith("#") and _indentacao(linhas[j]) <= ind:
                break
            j += 1
        ini, fim = i + 1, j
    v = _sem_comentario(resto).strip()
    if not v or v[0] in "|>{[":
        return None
    v = v.strip('"').strip("'")
    return None if v.lower() in NULOS_YAML else v

def escalar(txt, caminho, conv=float):
    """le uma chave aninhada do estado.yaml sem depender de PyYAML"""
    bruto = yaml_valor(txt, caminho)
    if bruto is None:
        return None
    try:
        return conv(bruto)
    except (ValueError, TypeError):
        return None

def parametro(estado, nome, conv=float):
    """o parametro escrito como escalar (vigencia_meses: 12) ou como bloco com
    valor (vigencia_meses: {valor: 10, fonte: ...}) - os dois jeitos aparecem
    nos estado.yaml do projeto, e so o primeiro era lido."""
    v = escalar(estado, nome, conv)
    return v if v is not None else escalar(estado, nome + ".valor", conv)

def carregar_parametros(estado):
    """define os globais a partir do estado.yaml do plano"""
    global UNIT, UNITS, MULTI, METAS_EXEC, DIRECAO, RECURSO, DIAS_UTEIS, POLOS
    UNIT = escalar(estado, "valor_unitario.valor")
    RECURSO = escalar(estado, "origem_recurso.valor")
    du = escalar(estado, "dias_uteis", int)
    if du: DIAS_UTEIS = du
    m = re.search(r"nomes:\s*\[([^\]]+)\]", estado)
    if m:
        POLOS = [chave(x.strip().strip('"')) for x in m.group(1).split(",")]
    # plano de multiplos codigos: o unitario nao e um numero, e um conjunto
    bloco = re.search(r"por_codigo:\s*\n((?:\s+\"[\d.]+-\d\":.*\n)+)", estado)
    if bloco:
        UNITS = sorted({float(x) for x in re.findall(r"unitario:\s*([\d.]+)", bloco.group(1))})
        MULTI = len(UNITS) > 0
    mm = re.search(r"metas_execucao:\s*\[([\d,\s]+)\]", estado)
    if mm:
        METAS_EXEC = [int(x) for x in re.findall(r"\d+", mm.group(1))]
    md = re.search(r"direcao:\s*(\w+)", estado)
    if md: DIRECAO = md.group(1)
    faltas = []
    if UNIT is None and not MULTI:
        faltas.append("parametros.valor_unitario.valor (ou valor_unitario.por_codigo)")
    if RECURSO is None: faltas.append("parametros.origem_recurso.valor")
    return faltas

# ---------------------------------------------------------------- utilidades

def num(txt: str):
    """'1.284.120,10' -> 1284120.10 ; '38,80%' -> 38.80 ; devolve None se nao for numero"""
    if txt is None:
        return None
    t = txt.strip().replace("**", "").replace("*", "").replace("%", "")
    t = re.sub(r"[^\d.,\-]", "", t)
    if not t or t in {"-", "—"}:
        return None
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    else:
        # sem virgula: ponto e separador de milhar quando ha 3 digitos depois
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
            t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None

def perto(a, b, tol=TOL):
    return a is not None and b is not None and abs(a - b) <= tol

def tabelas(md: str):
    """devolve lista de tabelas; cada tabela e lista de linhas; cada linha, lista de celulas"""
    out, atual = [], []
    for linha in md.splitlines():
        s = linha.strip()
        if s.startswith("|") and s.endswith("|"):
            celulas = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in celulas if c):
                continue                      # separador
            atual.append(celulas)
        else:
            if atual:
                out.append(atual)
                atual = []
    if atual:
        out.append(atual)
    return out

def tabela_com(tbs, *termos):
    """primeira tabela cujo texto inteiro contem todos os termos"""
    for t in tbs:
        txt = " ".join(" ".join(l) for l in t).lower()
        if all(x.lower() in txt for x in termos):
            return t
    return None

# ---------------------------------------------------------------- resultado

class R:
    def __init__(self):
        self.itens = []
    def add(self, sigla, nome, ok, detalhes=None, na=False):
        self.itens.append((sigla, nome, ok, detalhes or [], na))
    @property
    def falhou(self):
        return any(not ok and not na for _, _, ok, _, na in self.itens)

# ---------------------------------------------------------------- as verificacoes

def carregar():
    d = {}
    if not (BASE / "plano.md").exists():
        raise SystemExit(f"erro: {BASE}/plano.md nao existe")
    d["plano"] = (BASE / "plano.md").read_text(encoding="utf-8")
    d["estado"] = (BASE / "estado.yaml").read_text(encoding="utf-8")
    d["pend"] = (BASE / "pendencias.md").read_text(encoding="utf-8")
    for nome in ("envelope", "parametros_tecnicos", "valor_unitario", "gestao_no_acervo"):
        p = BASE / "dados" / f"{nome}.md"
        d[nome] = p.read_text(encoding="utf-8") if p.exists() else ""
    d["tbs"] = tabelas(d["plano"])
    return d

ALIAS_COLUNA = {"quantidade": "qtd", "qtd.": "qtd",
                "valor unitario": "v. unitario", "valor total": "v. total",
                "frequencia": "meses", "un. medida": "un.", "un. de medida": "un."}

def coluna(t, nome):
    """indice da coluna pelo cabecalho, tolerante ao vocabulario do acervo"""
    cab = [ALIAS_COLUNA.get(chave(c), chave(c)) for c in t[0]]
    return cab.index(nome) if nome in cab else None

def linhas_planilha(tbs, marcador):
    """linhas de item da tabela de planilha que contem o marcador; ignora subtotais"""
    t = tabela_com(tbs, marcador, "v. unitário")
    if not t:
        return None, None
    itens, subtotal = [], None
    cab = [c.lower() for c in t[0]]
    try:
        i_q, i_v, i_m, i_t = (cab.index("qtd"), cab.index("v. unitário"),
                              cab.index("meses"), cab.index("v. total"))
    except ValueError:
        return None, None
    for l in t[1:]:
        if len(l) <= i_t:
            continue
        rot = " ".join(l).lower()
        if "subtotal" in rot:
            subtotal = num(l[i_t])
            continue
        q, v, m, tot = num(l[i_q]), num(l[i_v]), num(l[i_m]), num(l[i_t])
        if None in (q, v, tot):
            continue
        itens.append((l[1] if len(l) > 1 else "?", q, v, m, tot))
    return itens, subtotal

def etapas_da_planilha(tbs):
    """toda etapa da planilha, com a meta deduzida do codigo do item.

    Nada de marcador fixo: o plano decide quantas etapas tem. E desde 05/09/2026 a
    planilha e uma tabela so, com as metas como blocos internos — como nos cinco
    aprovados. Cada linha de subtotal fecha uma etapa; o que vier depois abre a
    proxima. Tabela por etapa continua funcionando: e o caso de uma etapa so.
    """
    out = []
    for t in tbs:
        cab = [ALIAS_COLUNA.get(chave(c), chave(c)) for c in t[0]]
        if "qtd" not in cab or "v. unitario" not in cab or "v. total" not in cab:
            continue
        i_q, i_v, i_t = cab.index("qtd"), cab.index("v. unitario"), cab.index("v. total")
        i_m = cab.index("meses") if "meses" in cab else None
        itens, meta = [], None
        def fechar(subtotal):
            nonlocal itens, meta
            if itens:
                out.append({"itens": itens, "subtotal": subtotal, "meta": meta})
            itens, meta = [], None
        for l in t[1:]:
            if len(l) <= i_t:
                continue
            rot = chave(" ".join(l)).replace("-", "")
            if "subtotal" in rot:
                fechar(num(l[i_t])); continue
            if "total da meta" in rot:
                # planilha sem linha de subtotal: o total da meta fecha a etapa
                if itens:
                    fechar(num(l[i_t]))
                continue
            if "total geral" in rot or "valor global" in rot:
                continue
            q, v, tot = num(l[i_q]), num(l[i_v]), num(l[i_t])
            m = num(l[i_m]) if i_m is not None and len(l) > i_m else None
            if None in (q, v, tot):
                continue
            cod = re.match(r"(\d+)\.", l[0].strip().strip("*"))
            if cod and meta is None:
                meta = int(cod.group(1))
            itens.append((l[1] if len(l) > 1 else "?", q, v, m, tot))
        fechar(None)
    return out

def verificar_A(d, r):
    """produto por linha"""
    falhas, n = [], 0
    etapas = etapas_da_planilha(d["tbs"])
    if not etapas:
        falhas.append("nenhuma tabela de planilha encontrada")
    for e in etapas:
        for nome, q, v, m, tot in e["itens"]:
            n += 1
            esperado = q * v * (m if m else 1)
            if not perto(esperado, tot):
                falhas.append(f"{nome[:44]}: {q} x {v} x {m or 1} = {reais(esperado)}, publicado {reais(tot)}")
    r.add("A", f"produto por linha ({n} linhas em {len(etapas)} tabelas)", not falhas, falhas)

def metas_planilha(p: str):
    """{n: total} de cada TOTAL DA META n publicado na planilha.

    Le linha a linha e toma o ULTIMO valor monetario: a planilha pode trazer o
    quantitativo numa coluna intermediaria, e o total da meta e sempre o da direita.
    """
    out = {}
    for linha in p.splitlines():
        m = re.search(r"TOTAL DA META (\d{1,2})", linha)
        if not m:
            continue
        vals = re.findall(r"[\d.]+,\d{2}", linha)
        if vals:
            out[int(m.group(1))] = num(vals[-1])
    return out

def verificar_B(d, r):
    """subtotais, metas e consolidacao"""
    falhas = []
    etapas = etapas_da_planilha(d["tbs"])
    if not etapas:
        r.add("B", "soma dos subtotais", False, ["planilha nao encontrada"]); return
    por_meta = {}
    for e in etapas:
        s = sum(x[4] for x in e["itens"])
        if e["subtotal"] is not None and not perto(s, e["subtotal"]):
            rot = e["itens"][0][0][:30] if e["itens"] else "?"
            falhas.append(f"etapa de '{rot}': linhas somam {reais(s)}, subtotal publicado {reais(e['subtotal'])}")
        if e["meta"] is not None:
            por_meta[e["meta"]] = por_meta.get(e["meta"], 0.0) + s
    metas = metas_planilha(d["plano"])
    for n_meta, s in sorted(por_meta.items()):
        if n_meta in METAS_EXEC and not MULTI:
            continue                       # a meta de execucao se confere pelo quantitativo, abaixo
        if n_meta not in metas:
            falhas.append(f"TOTAL DA META {n_meta} nao encontrado")
        elif not perto(s, metas[n_meta]):
            falhas.append(f"Meta {n_meta}: etapas somam {reais(s)}, publicado {reais(metas[n_meta])}")
    # a meta de execucao e o quantitativo
    qtd = None
    if MULTI:
        # soma das quantidades das linhas das etapas de execucao
        q = 0.0
        for e in etapas:
            if e["meta"] in METAS_EXEC:
                q += sum(x[1] for x in e["itens"])
        qtd = q or None
        if qtd is None:
            falhas.append(f"quantitativo nao encontrado nas etapas das metas {METAS_EXEC}")
    else:
        t2 = tabela_com(d["tbs"], "TOTAL DA META 2")
        if t2:
            for l in t2:
                if "oci" in " ".join(l).lower() and len(l) >= 5:
                    cand = [num(c) for c in l if num(c) and 1000 < num(c) < 1_000_000]
                    if cand: qtd = min(cand)
        if qtd and 2 in metas:
            if not perto(qtd * UNIT, metas[2]):
                falhas.append(f"Meta 2: {qtd:.0f} x {UNIT} = {reais(qtd*UNIT)}, publicado {reais(metas[2])}")
        else:
            falhas.append("Meta 2 ou quantitativo nao encontrado")
    # o rotulo "valor global" na primeira coluna: no modelo da SES (v20 do plano 4) o item "1.4 Valor Total"
    # traz "valor global" e "recurso disponível" no texto da celula, e a tabela de identificacao vinha antes
    rotulo = lambda t: any(l and "valor global" in l[0].lower() for l in t)
    tg = next((t for t in d["tbs"] if rotulo(t) and tabela_com([t], "Recurso disponível")), None) \
        or next((t for t in d["tbs"] if rotulo(t)), None)
    glob = None
    if tg:
        for l in tg:
            if l and "valor global" in l[0].lower():
                glob = next((num(c) for c in reversed(l) if num(c)), None)
            # cada meta da consolidacao tem de bater com o total publicado na planilha
            mm = re.match(r"\**Meta (\d)", l[0].strip())
            if mm:
                v = next((num(c) for c in reversed(l) if num(c)), None)
                n = int(mm.group(1))
                if n in metas and v and not perto(v, metas[n]):
                    falhas.append(f"consolidacao: Meta {n} = {reais(v)}, planilha diz {reais(metas[n])}")
    if glob is None:
        falhas.append("VALOR GLOBAL da consolidacao nao encontrado")
    else:
        soma = sum(metas.values())
        if not perto(soma, glob):
            falhas.append(f"global: soma das metas = {reais(soma)}, publicado {reais(glob)}")
    r.add("B", f"subtotais, metas e consolidacao ({len(metas)} metas)", not falhas, falhas)
    apoio = sum(v for n, v in metas.items() if n not in METAS_EXEC)
    d["_apoio"], d["_qtd"], d["_global"] = apoio, qtd, glob
    d["_exec"] = sum(v for n, v in metas.items() if n in METAS_EXEC)

def verificar_C(d, r):
    """fechamento do envelope"""
    falhas = []
    apoio, qtd, glob = d.get("_apoio"), d.get("_qtd"), d.get("_global")
    if None in (apoio, qtd, glob):
        r.add("C", "fechamento do envelope", False, ["faltam valores da verificacao B"]); return
    if DIRECAO == "fila_define_recurso":
        # a fila e dada e o recurso e a soma: nao ha piso de divisao a conferir.
        # o que se confere e que o global e a soma dos procedimentos com o apoio,
        # e que o apoio cabe no teto declarado.
        #
        # A execucao sai dos TOTAIS DAS METAS de execucao, lidos na planilha - a
        # versao anterior a calculava como global - apoio e depois conferia que
        # execucao + apoio = global, conta que fecha por construcao.
        exec_total = d.get("_exec")
        if not exec_total:
            falhas.append(f"metas de execucao {METAS_EXEC} sem TOTAL DA META na planilha")
        elif not perto(exec_total + apoio, glob):
            falhas.append(f"global {reais(glob)} != execucao {reais(exec_total)} + apoio {reais(apoio)}")
        teto = escalar(d["estado"], "custo_acessorio.teto")
        if teto:
            pct = apoio / glob
            if pct > teto + 1e-6:
                falhas.append(f"apoio {pct*100:.3f}% do global excede o teto de {teto*100:.1f}%")
        if RECURSO and not perto(RECURSO, glob):
            falhas.append(f"origem_recurso.valor {reais(RECURSO)} != global publicado {reais(glob)}")
        r.add("C", f"fechamento do envelope (fila define recurso, apoio {apoio/glob*100:.3f}%)",
              not falhas, falhas)
        return
    if DIRECAO == "recurso_define_meta" and MULTI:
        # o recurso e dado e ha varios unitarios: a meta de cada codigo e inteira, o
        # global nao passa do recurso e a sobra fica abaixo do MENOR unitario - se
        # coubesse mais um exame do codigo mais barato, a meta estaria subdimensionada
        teto = escalar(d["estado"], "custo_acessorio.teto")
        if teto and apoio / glob > teto + 1e-6:
            falhas.append(f"apoio {apoio/glob*100:.3f}% do global excede o teto de {teto*100:.1f}%")
        sobra = RECURSO - glob
        if sobra < -TOL:
            falhas.append(f"global {reais(glob)} excede o recurso {reais(RECURSO)} em {reais(-sobra)}")
        if sobra >= min(UNITS):
            falhas.append(f"sobra {reais(sobra)} >= menor unitario {reais(min(UNITS))}: cabia mais um exame")
        r.add("C", f"fechamento do envelope (recurso define meta, sobra {reais(sobra)}, "
                   f"apoio {apoio/glob*100:.3f}%)", not falhas, falhas)
        return
    env = RECURSO - apoio
    qmax = math.floor(env / UNIT)
    if int(qtd) > qmax:
        falhas.append(f"quantitativo {int(qtd)} excede o que o envelope comporta ({qmax}) — "
                      f"a meta esta acima do recurso")
    sobra = RECURSO - glob
    if sobra < -TOL:
        falhas.append(f"global excede o recurso em {reais(-sobra)}")
    if sobra >= UNIT:
        # regra 2: a meta e o PISO da divisao. Sobra maior que um unitario significa
        # que cabia mais uma unidade e o quantitativo esta subdimensionado.
        falhas.append(f"sobra {reais(sobra)} >= unitario {reais(UNIT)}: o envelope comporta {qmax} "
                      f"e o plano adota {int(qtd)} — a meta e o piso da divisao, nao numero redondo")
    m = re.search(r"Sobra declarada \| ([\d.,]+) \|", d["plano"]) or re.search(r"Diferença não aplicada \| ([\d.,]+) \|", d["plano"])
    if m and not perto(num(m.group(1)), sobra):
        falhas.append(f"sobra declarada {m.group(1)} != calculada {sobra:.2f}")
    r.add("C", f"fechamento do envelope (sobra {reais(sobra)})", not falhas, falhas)

def verificar_D(d, r):
    """curva fisica"""
    falhas = []
    t = tabela_com(d["tbs"], "acumulado", "por dia útil")
    if not t:
        # curva por trimestre: | trimestre | meses | exames |. Cada trimestre tem de
        # bater com os exames do periodo da parcela correspondente - fisico e
        # desembolso sao a mesma curva (devolutiva de 20/09/2026, amarelo na 6.2)
        # o periodo pode ser trimestre, bimestre ou misto ("período", com o tipo no rotulo da linha):
        # plano 4, v22 - oito meses em dois trimestres e um bimestre final
        PERIODO = {"trimestre": 3, "bimestre": 2}
        tq = next((tb for tb in d["tbs"] if tb and len(tb[0]) >= 3
                   and any(k in tb[0][0].lower() for k in list(PERIODO) + ["período", "periodo"])
                   and "exames" in " ".join(tb[0]).lower()), None)
        if tq:
            nome = next((k for k in PERIODO if k in tq[0][0].lower()), "período")
            dur = PERIODO.get(nome)
            falhas, soma, nm, curva = [], 0.0, 0, {}
            for l in tq[1:]:
                if len(l) < 3 or "total" in " ".join(l).lower(): continue
                faixa = re.findall(r"\d+", l[1]); ex = num(l[2])
                if len(faixa) < 2 or ex is None: continue
                a, b = int(faixa[0]), int(faixa[1])
                d_lin = next((v for k, v in PERIODO.items() if k in l[0].lower()), dur)
                if d_lin and b - a + 1 != d_lin:
                    falhas.append(f"{nome} {l[0]} cobre os meses {l[1]}, que nao sao {d_lin}")
                soma += ex; nm += b - a + 1; curva[(a, b)] = ex
            qtd = d.get("_qtd")
            if qtd and not perto(soma, qtd, 0.5):
                falhas.append(f"curva soma {soma:.0f}, quantitativo {int(qtd)}")
            vig = parametro(d["estado"], "vigencia_meses", int)
            if vig and nm != vig:
                falhas.append(f"a curva cobre {nm} meses e a vigencia e de {vig}")
            # a tabela de parcelas pelo CABECALHO: o texto "exames do periodo" pode
            # aparecer em outra tabela (na 6.3 do plano 4 apareceu, em 29/09/2026)
            td = next((tb for tb in d["tbs"] if tb and "parcela" in tb[0][0].lower()
                       and "exames" in " ".join(tb[0]).lower()), None)
            if not td:
                falhas.append(f"curva por {nome} sem tabela de parcelas com exames do periodo")
            else:
                vistos = set()
                for l in td[1:]:
                    if len(l) < 3: continue
                    faixa = re.findall(r"\d+", l[1]); ex = num(l[2])
                    if len(faixa) < 2 or ex is None: continue
                    k = (int(faixa[0]), int(faixa[1])); vistos.add(k)
                    if k not in curva:
                        falhas.append(f"parcela dos meses {l[1]} sem {nome} correspondente na curva")
                    elif not perto(curva[k], ex, 0.5):
                        falhas.append(f"meses {l[1]}: curva {curva[k]:.0f}, parcela {ex:.0f}")
                for k in curva:
                    if k not in vistos:
                        falhas.append(f"{nome} dos meses {k[0]} a {k[1]} sem parcela correspondente")
            r.add("D", f"curva fisica ({len(curva)} {nome}s, soma {soma:.0f}, igual ao desembolso)",
                  not falhas, falhas); return
        # curva por faixa de meses: | meses | exames por mes | subtotal |
        tf = tabela_com(d["tbs"], "exames por mês", "subtotal")
        if tf:
            falhas, soma, nm = [], 0.0, 0
            for l in tf[1:]:
                if len(l) < 3 or "total" in l[0].lower(): continue
                faixa = re.findall(r"\d+", l[0]); porm, sub = num(l[1]), num(l[2])
                if len(faixa) < 2 or porm is None or sub is None: continue
                n = int(faixa[1]) - int(faixa[0]) + 1
                if not perto(n * porm, sub, 0.5):
                    falhas.append(f"meses {l[0]}: {n} x {porm:.0f} = {n*porm:.0f}, publicado {sub:.0f}")
                soma += sub; nm += n
            qtd = d.get("_qtd")
            if qtd and not perto(soma, qtd, 0.5):
                falhas.append(f"curva soma {soma:.0f}, quantitativo {int(qtd)}")
            vig = parametro(d["estado"], "vigencia_meses", int)
            if vig and nm != vig:
                falhas.append(f"a curva cobre {nm} meses e a vigencia e de {vig}")
            r.add("D", f"curva fisica ({nm} meses, soma {soma:.0f})", not falhas, falhas); return
        r.add("D", "curva fisica", False, ["tabela da curva nao encontrada"]); return
    meses, soma = [], 0.0
    for l in t[1:]:
        if len(l) < 3: continue
        mes, oci, ac = num(l[0]), num(l[1]), num(l[2])
        if mes is None or oci is None: continue
        meses.append((mes, oci, ac, num(l[3]) if len(l) > 3 else None))
        soma += oci
    qtd = d.get("_qtd")
    if qtd and not perto(soma, qtd, 0.5):
        falhas.append(f"curva soma {soma:.0f}, quantitativo {int(qtd)}")
    ac = 0.0
    for mes, oci, acpub, dia in meses:
        ac += oci
        if acpub is not None and not perto(ac, acpub, 0.5):
            falhas.append(f"mes {mes:.0f}: acumulado publicado {acpub:.0f}, calculado {ac:.0f}")
        # nao ha fracao de usuario: o por-dia-util publicado e o teto da divisao
        esperado = math.ceil(oci / DIAS_UTEIS)
        if dia is not None and not perto(esperado, dia, 0.5):
            falhas.append(f"mes {mes:.0f}: teto de {oci:.0f}/{DIAS_UTEIS} = {esperado}, publicado {dia}")
    r.add("D", f"curva fisica ({len(meses)} meses, soma {soma:.0f})", not falhas, falhas)

def verificar_E(d, r):
    """rateio por polo contra a fila"""
    falhas = []
    if not POLOS:
        r.add("E", "rateio por polo", True, ["plano sem polos declarados"], na=True); return
    tp = tabela_com(d["tbs"], "solicitações", "participação", "OCI")
    if not tp:
        # rateio publicado so com participacao e quantitativo, sem a coluna de origem
        tq = tabela_com(d["tbs"], "participação", "exames")
        if tq:
            falhas, linhas, soma_q, soma_p = [], [], 0.0, 0.0
            i_p = coluna(tq, "participacao"); i_e = coluna(tq, "exames")
            for l in tq[1:]:
                if i_p is None or i_e is None or len(l) <= max(i_p, i_e): continue
                part, ex = num(l[i_p]), num(l[i_e])
                if part is None or ex is None: continue
                if "total" in " ".join(l).lower():
                    continue
                linhas.append((l[0], part, ex)); soma_q += ex; soma_p += part
            if linhas:
                qtd = d.get("_qtd")
                if qtd and not perto(soma_q, qtd, 0.5):
                    falhas.append(f"exames dos polos somam {soma_q:.0f}, quantitativo {int(qtd)}")
                if not perto(soma_p, 100.0, 0.05):
                    falhas.append(f"participacoes somam {soma_p:.2f}%, esperado 100%")
                for nome, part, ex in linhas:
                    calc = ex / soma_q * 100 if soma_q else 0
                    if not perto(calc, part, 0.02):
                        falhas.append(f"{nome}: {ex:.0f}/{soma_q:.0f} = {calc:.2f}%, publicado {part}%")
                conferidos = d.setdefault("_conferidos", set())
                for _n, part, _e in linhas:
                    conferidos.add((round(part, 2), "%"))
                r.add("E", f"rateio por polo ({len(linhas)} polos)", not falhas, falhas); return
        r.add("E", "rateio por polo", False, ["tabela de distribuicao nao encontrada"]); return
    total_sol, soma_oci, linhas = 0.0, 0.0, []
    for l in tp[1:]:
        if len(l) < 5: continue
        sol, part, oci = num(l[2]), num(l[3]), num(l[4])
        if None in (sol, part, oci): continue
        if "total" in " ".join(l).lower():
            total_sol = sol; continue
        linhas.append((l[0], sol, part, oci)); soma_oci += oci
    if not linhas:
        r.add("E", "rateio por polo", False, ["nenhuma linha de polo lida"]); return
    soma_sol = sum(x[1] for x in linhas)
    if total_sol and not perto(soma_sol, total_sol, 0.5):
        falhas.append(f"solicitacoes somam {soma_sol:.0f}, total publicado {total_sol:.0f}")
    qtd = d.get("_qtd")
    if qtd and not perto(soma_oci, qtd, 0.5):
        falhas.append(f"OCI dos polos somam {soma_oci:.0f}, quantitativo {int(qtd)}")
    base = total_sol or soma_sol
    for nome, sol, part, oci in linhas:
        calc = sol / base * 100
        if not perto(calc, part, 0.02):
            falhas.append(f"{nome}: {sol:.0f}/{base:.0f} = {calc:.2f}%, publicado {part}%")
        # o rateio pode ser arredondado para numero redondo; o que se exige e que
        # a participacao publicada nao se afaste mais de 1 ponto percentual da fila
        if qtd:
            desvio = abs(oci / qtd - sol / base) * 100
            if desvio > 1.0:
                falhas.append(f"{nome}: {oci:.0f}/{qtd:.0f} = {oci/qtd*100:.2f}% "
                              f"contra {sol/base*100:.2f}% da fila — desvio de {desvio:.2f} p.p.")
    conferidos = d.setdefault("_conferidos", set())
    for _n, _sol, part, _oci in linhas:
        conferidos.add((round(part, 2), "%"))
    r.add("E", f"rateio por polo ({len(linhas)} polos)", not falhas, falhas)

def verificar_F(d, r):
    """desembolso"""
    falhas = []
    t = tabela_com(d["tbs"], "parcela", "valor da parcela")
    if not t:
        r.add("F", "desembolso", False, ["tabela de parcelas nao encontrada"]); return
    soma_parc = soma_oci = soma_prod = soma_apoio = 0.0
    meses_vistos, n = [], 0
    for l in t[1:]:
        if len(l) < 6: continue
        if "total" in l[0].lower(): continue
        if not l[0].strip() and not l[1].strip(): continue   # linha de total, sem rotulo
        oci, prod, apoio, val = num(l[2]), num(l[3]), num(l[4]), num(l[5])
        if oci is None: continue
        if None in (prod, apoio, val):
            # parcela com exames e sem valor: antes a comparacao seguia com None
            # e a verificacao inteira caia em "erro na verificacao"
            falhas.append(f"parcela {l[0]}: {oci:.0f} exames e celula de valor sem numero "
                          f"(producao {l[3]!r}, apoio {l[4]!r}, parcela {l[5]!r})")
            continue
        n += 1
        if MULTI:
            # nao ha unitario unico: a producao da parcela tem de cair entre o menor
            # e o maior unitario declarados, multiplicados pelos exames do periodo
            lo, hi = oci * min(UNITS), oci * max(UNITS)
            if not (lo - TOL <= prod <= hi + TOL):
                falhas.append(f"parcela {l[0]}: {oci:.0f} exames produzem entre {reais(lo)} e "
                              f"{reais(hi)} aos unitarios declarados; publicado {reais(prod)}")
        elif not perto(oci * UNIT, prod):
            falhas.append(f"parcela {l[0]}: {oci:.0f} x {UNIT} = {reais(oci*UNIT)}, publicado {reais(prod)}")
        if not perto(prod + apoio, val):
            falhas.append(f"parcela {l[0]}: producao+apoio = {reais(prod+apoio)}, publicado {reais(val)}")
        soma_parc += val; soma_oci += oci; soma_prod += prod; soma_apoio += apoio
        for x in re.findall(r"\d+", l[1]):
            meses_vistos.append(int(x))
    glob, qtd, apoio_t = d.get("_global"), d.get("_qtd"), d.get("_apoio")
    if glob and not perto(soma_parc, glob):
        falhas.append(f"parcelas somam {reais(soma_parc)}, global {reais(glob)}")
    if qtd and not perto(soma_oci, qtd, 0.5):
        falhas.append(f"OCI das parcelas somam {soma_oci:.0f}, quantitativo {int(qtd)}")
    if apoio_t and not perto(soma_apoio, apoio_t):
        falhas.append(f"apoio das parcelas soma {reais(soma_apoio)}, Meta 1 {reais(apoio_t)}")
    # meses: primeiro e ultimo de cada parcela devem encadear 1..10
    if meses_vistos:
        pares = [meses_vistos[i:i+2] for i in range(0, len(meses_vistos), 2)]
        cobertos = []
        for par in pares:
            a = par[0]; b = par[1] if len(par) > 1 else par[0]
            cobertos += list(range(a, b + 1))
        vig = parametro(d["estado"], "vigencia_meses", int)
        if vig is None:
            falhas.append("estado.yaml sem vigencia_meses - os meses das parcelas nao tem contra o que fechar")
            vig = 0
        if sorted(cobertos) != list(range(1, vig + 1)):
            falhas.append(f"meses cobertos pelas parcelas: {sorted(cobertos)} (esperado 1..{vig} sem repeticao)")
    r.add("F", f"desembolso ({n} parcelas)", not falhas, falhas)

# Os tempos que a G usa para recalcular salas, recuperacao, espera e aparelhos.
def verificar_G(d, r):
    """capacidade por polo: na tabela de capacidade com coluna de total, os polos somam o total.

    O recalculo da capacidade a partir dos tempos de sala e de aparelho e do objeto, e
    mora na bateria do plano (planos/redacao_NN/conferencia/verificacoes.py): no
    redacao_03, a +G da endoscopia. Ver metodo/plano/conferencia.md."""
    falhas = []
    # capacidade publicada como | recurso | total | polo | polo | polo |
    tc = tabela_com(d["tbs"], "Exames por dia útil")
    if tc and POLOS:
        cab = [chave(c) for c in tc[0]]
        cols = [i for i, c in enumerate(cab) if c in POLOS]
        i_tot = cab.index("total") if "total" in cab else None
        if len(cols) == len(POLOS) and i_tot is not None:
            n = 0
            for l in tc[1:]:
                if len(l) <= max(cols + [i_tot]): continue
                tot = num(l[i_tot]); vals = [num(l[i]) for i in cols]
                if tot is None or any(v is None for v in vals): continue
                n += 1
                if not perto(sum(vals), tot, 0.5):
                    falhas.append(f"{l[0][:40]}: polos somam {sum(vals):.0f}, total publicado {tot:.0f}")
            r.add("G", f"capacidade por polo ({len(POLOS)} polos, {n} recursos)", not falhas, falhas); return
    if not POLOS:
        r.add("G", "capacidade por polo", True, ["plano sem polos declarados em estado.yaml"], na=True); return
    if (BASE / "conferencia" / "verificacoes.py").exists():
        r.add("G", "capacidade por polo", True,
              ["sem tabela de capacidade com coluna de total; o dimensionamento e da bateria do plano"],
              na=True); return
    r.add("G", "capacidade por polo", False, ["tabela de capacidade por polo nao encontrada"])

def verificar_H(d, r):
    """coerencia entre arquivos — compara o VALOR DA CHAVE, nao a presenca da string

    A versao anterior procurava o numero em qualquer lugar do estado.yaml, e uma
    frase em prosa citando o valor mascarava divergencia no parametro. Agora le a
    chave e compara numericamente.
    """
    falhas = []
    apoio, qtd, glob = d.get("_apoio"), d.get("_qtd"), d.get("_global")
    chaves = [(["derivados.valor_global"], glob, "valor global"),
              (["derivados.quantitativo_oci", "derivados.quantitativo_exames"], qtd, "quantitativo"),
              (["derivados.apoio_total"], apoio, "apoio total")]
    for caminhos, calculado, rotulo in chaves:
        if calculado is None:
            continue
        declarado = next((escalar(d["estado"], c) for c in caminhos
                          if escalar(d["estado"], c) is not None), None)
        if declarado is None:
            falhas.append("estado.yaml nao declara " + " nem ".join(caminhos))
        elif not perto(declarado, calculado, 0.5):
            falhas.append(f"{rotulo}: plano.md diz {reais(calculado)}, "
                          f"estado.yaml diz {reais(declarado)}")
    # o unitario tem de ser o mesmo nos arquivos que o carregam
    alvos = UNITS if MULTI else ([UNIT] if UNIT else [])
    for nome, texto in [("plano.md", d["plano"]), ("dados/envelope.md", d["envelope"]),
                        ("dados/valor_unitario.md", d["valor_unitario"])]:
        for u in alvos:
            ut = reais(u).replace("R$ ", "")
            # o envelope publica os totais, nao os unitarios linha a linha
            if nome == "dados/envelope.md" and MULTI:
                continue
            if ut not in texto:
                falhas.append(f"unitario {ut} nao aparece em {nome}")
    # e o envelope tem de repetir o global
    if glob and reais(glob).replace("R$ ", "") not in d["envelope"]:
        falhas.append("valor global nao aparece em dados/envelope.md")
    r.add("H", "coerencia entre arquivos", not falhas, falhas)

RE_INTEIRO_SOLTO = re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})+|\d+)(?!\d|[.,]\d)")

def inteiros_do_texto(txt: str):
    """todo numero inteiro do texto, com ou sem ponto de milhar - '11.456' e
    '11456' dao 11456; '600.11' nao da inteiro nenhum."""
    return {int(m.group(1).replace(".", "")) for m in RE_INTEIRO_SOLTO.finditer(txt)}

def verificar_I(d, r):
    """fila do Mapa Social"""
    falhas = []
    t = tabela_com(d["tbs"], "Região de Saúde", "participação")
    if not t:
        r.add("I", "fila externa", True, ["plano sem tabela de fila por regiao"], na=True); return
    regs, total_pub = [], None
    for l in t[1:]:
        if len(l) < 3: continue
        v, p = num(l[1]), num(l[2])
        if v is None: continue
        if "total" in l[0].lower(): total_pub = v; continue
        regs.append((l[0], v, p))
    soma = sum(x[1] for x in regs)
    if total_pub and not perto(soma, total_pub, 0.5):
        falhas.append(f"regioes somam {soma:.0f}, total publicado {total_pub:.0f}")
    base = total_pub or soma
    for nome, v, p in regs:
        if p and not perto(v / base * 100, p, 0.02):
            falhas.append(f"{nome}: {v:.0f}/{base:.0f} = {v/base*100:.2f}%, publicado {p}%")
    # bate com estado.yaml? Numero inteiro, nao pedaco de numero: a busca por
    # substring dava "56" como registrado porque o estado.yaml tinha "1256".
    registrados = inteiros_do_texto(d["estado"])
    for nome, v in [(x[0], x[1]) for x in regs]:
        if int(v) not in registrados:
            falhas.append(f"{nome} = {int(v)} nao consta de estado.yaml")
    # cobertura declarada
    m = re.search(r"correspondem a ([\d,]+)% das solicitações pendentes", d["plano"])
    mp = re.search(r"pendentes_de_regulacao:\s*(\d+)", d["estado"])
    if m and mp and d.get("_qtd"):
        calc = d["_qtd"] / int(mp.group(1)) * 100
        if not perto(calc, num(m.group(1)), 0.02):
            falhas.append(f"cobertura: {int(d['_qtd'])}/{mp.group(1)} = {calc:.2f}%, publicado {m.group(1)}%")
    conferidos = d.setdefault("_conferidos", set())
    for _nome, _v, part in regs:
        if part is not None:
            conferidos.add((round(part, 2), "%"))
    if m:
        conferidos.add((round(num(m.group(1)), 2), "%"))
    r.add("I", f"fila do Mapa Social ({len(regs)} regioes, soma {soma:.0f})", not falhas, falhas)

# ------------------------------------------------------- ancoras no acervo

def citacoes(p: str):
    """(rotulo curto, numero) de cada norma citada no documento"""
    pads = [
        (r"Portaria SAES/MS nº ([\d.]+)", "SAES"),
        (r"Portaria GM/MS nº ([\d.]+)", "GM"),
        (r"RDC ANVISA nº (\d+)", "RDC"),
        (r"RDC nº (\d+)/2013", "RDC"),
        (r"Resolução CFM nº ([\d.]+)", "CFM"),
        (r"Decreto (?:do Distrito Federal |DF )?nº ([\d.]+)", "Decreto DF"),
        (r"Lei nº ([\d.]+)", "Lei"),
        (r"Instrução Normativa CGDF nº (\d+)", "IN CGDF"),
        (r"Nota Técnica nº (\d+)/2025", "NT"),
    ]
    out = set()
    for pad, rot in pads:
        for m in re.finditer(pad, p):
            out.add((rot, m.group(1).replace(".", "")))
    return sorted(out)

# normas que nao precisam de arquivo em normas/: lei federal de conhecimento
# publico e norma cuja copia mora em dados/fontes/
DISPENSADAS = {("Lei", "8080"), ("Lei", "12732"), ("Lei", "13709"),
               ("Lei", "11000"), ("Lei", "3268")}

VOZ_VEDADA = [
    # o plano declara; nao se defende, nao fala de si, nao enfatiza
    (r"\bnoss[ao]s?\b|\bnós\b",                    "primeira pessoa — o plano nao fala de si"),
    (r"\beste plano\b|\besta seção\b|\besta subseção\b|\besta planilha\b",
                                                    "meta-comentario sobre o proprio documento"),
    (r"registre-se|para afastar dúvida|vale (?:dizer|registrar|notar)|cumpre (?:dizer|registrar)",
                                                    "formula que anuncia o proprio texto"),
    (r"não é folga|não é formalismo|não é (?:mera|simples) |não é recomendação|"
     r"não é escolha de conveniência|não é ornamento|não é invenção",
                                                    "negacao defensiva — responde a objecao nao formulada"),
    (r"a razão é substantiva|cabe em uma frase|é isso que|\bjustamente\b",
                                                    "enfase retorica"),
    (r"\bexatamente\b(?! (?:o|a|os|as|no|na) )",     "intensificador"),
    (r"o que .{0,30}não (?:demonstra|prova|garante)|é preciso reconhecer|é forçoso admitir",
                                                    "confissao de fragilidade"),
]

def verificar_Q(d, r):
    """voz do documento: declara, nao se defende"""
    p = re.sub(r"^\|.*$", "", d["plano"], flags=re.M)      # tabelas fora
    falhas = []
    for pad, o_que in VOZ_VEDADA:
        for m in re.finditer(pad, p, re.I):
            ini = max(0, m.start() - 70)
            trecho = re.sub(r"\s+", " ", p[ini:m.end() + 70]).strip()
            falhas.append(f"{o_que}: ...{trecho}...")
    r.add("Q", f"voz do documento ({len(VOZ_VEDADA)} padroes)", not falhas, falhas)

def verificar_M(d, r):
    """toda norma citada tem lastro no acervo"""
    if NORMAS is None or not NORMAS.exists():
        r.add("M", "ancoras no acervo", True, [], na=True); return
    # PDF ou HTML oficial: desde 27/09/2026 o acervo guarda norma publicada em HTML
    # (DOU, Planalto, SINJ), e a M so via PDF - acusava a Portaria SAES 4.795/2026,
    # que estava em biblioteca/normas/ como NM-067
    TIPOS = ("*.pdf", "*.html", "*.htm")
    arquivos = " ".join(f.name for t in TIPOS for f in NORMAS.rglob(t))
    fontes = BASE / "dados" / "fontes"
    if fontes.exists():
        arquivos += " " + " ".join(f.name for t in TIPOS for f in fontes.glob(t))
    colado = re.sub(r"(?<=\d)[._\s](?=\d)", "", arquivos)
    numeros = set(re.findall(r"\d+", colado))
    falhas, ok = [], 0
    for rot, n in citacoes(d["plano"]):
        if (rot, n) in DISPENSADAS:
            ok += 1; continue
        if n in numeros or n.lstrip("0") in numeros:
            ok += 1
        else:
            falhas.append(f"{rot} {n} citado no plano e sem arquivo em normas/")
    r.add("M", f"ancoras no acervo ({ok} normas com lastro)", not falhas, falhas)

SEM_PDFTOTEXT = ("pdftotext nao encontrado - a fonte nao foi lida. Instale o poppler "
                 "(no Windows vem com o Git para Windows) - ver README, Instalacao")

def texto_pdf(caminho: Path):
    """texto do PDF pelo pdftotext -layout, ou None se o programa nao existe.

    Procura tambem no local usual do Windows: o Git para Windows traz o
    pdftotext, mas so o poe no PATH do Git Bash, e fora dele a N passava a
    NAO SE APLICA sem dizer por que.
    """
    exe = localizar("pdftotext")
    if exe is None:
        return None
    return subprocess.run([exe, "-layout", "-enc", "UTF-8", str(caminho), "-"],
                          capture_output=True, encoding="utf-8",
                          errors="replace").stdout

def verificar_N(d, r):
    """o unitario e o codigo da OCI estao na propria portaria baixada"""
    if MULTI:
        return                      # plano de multiplos codigos: ver verificar_N_multi
    if NORMAS is None or not NORMAS.exists():
        r.add("N", "unitario conferido na fonte", True, [], na=True); return
    # a fonte do unitario e apontada pelo proprio estado.yaml
    mm = re.search(r'valor_unitario:[\s\S]{0,400}?fonte:\s*"?[^"\n]*?(\d[\d.]{2,})', d["estado"])
    chave = mm.group(1).replace(".", "") if mm else None
    alvo = None
    for f in NORMAS.glob("*.pdf"):
        if chave and chave in re.sub(r"(?<=\d)[._\s](?=\d)", "", f.name):
            alvo = f
    if alvo is None:
        r.add("N", "unitario conferido na portaria", True,
              ["a fonte do unitario declarada no estado.yaml nao esta em normas/"], na=True); return
    txt = texto_pdf(alvo)
    if txt is None:
        AMBIENTE.append("N")
        r.add("N", "unitario conferido na portaria", True, [SEM_PDFTOTEXT], na=True); return
    falhas = []
    # o que o PLANO afirma, conferido contra a fonte
    # o unitario que o PLANO declara, lido da linha da Meta 2 - nao do estado.yaml
    unit_plano = None
    t2 = tabela_com(d["tbs"], "TOTAL DA META 2")
    i_v = coluna(t2, "v. unitario") if t2 else None
    if t2 and i_v is not None:
        for l in t2:
            if re.match(r"\s*2\.\d", l[0]) and len(l) > i_v:
                unit_plano = num(l[i_v])
    if unit_plano is None:
        falhas.append("nao foi possivel ler o unitario declarado na planilha")
    else:
        if not perto(unit_plano, UNIT):
            falhas.append(f"a planilha declara {reais(unit_plano)} e o estado.yaml, {reais(UNIT)}")
        unit_txt = reais(unit_plano).replace("R$ ", "")
        if unit_txt not in txt:
            falhas.append(f"o plano afirma R$ {unit_txt}; {alvo.name[:34]} nao traz esse valor")
    principal = escalar(d["estado"], "objeto.oci", str)
    if principal and principal not in txt:
        falhas.append(f"codigo {principal} do objeto ausente da fonte do unitario")
    r.add("N", f"unitario conferido na portaria ({alvo.name[:34]})", not falhas, falhas)

def verificar_N_multi(d, r):
    """plano de multiplos codigos: cada codigo, cada valor de tabela e cada incremento
    declarados na composicao do unitario tem de estar na portaria baixada."""
    if not MULTI:
        return
    if NORMAS is None or not NORMAS.exists():
        r.add("N", "composicao conferida na portaria", True, [], na=True); return
    mm = re.search(r'valor_unitario:[\s\S]{0,2500}?\n\s+fonte:\s*"?[^"\n]*?(\d[\d.]{2,})', d["estado"])
    chave_n = mm.group(1).replace(".", "") if mm else None
    alvo = None
    for f in NORMAS.glob("*.pdf"):
        if chave_n and chave_n in re.sub(r"(?<=\d)[._\s](?=\d)", "", f.name):
            alvo = f
    if alvo is None:
        r.add("N", "composicao conferida na portaria", True,
              ["a fonte do unitario declarada no estado.yaml nao esta em normas/"], na=True); return
    txt = texto_pdf(alvo)
    if txt is None:
        AMBIENTE.append("N")
        r.add("N", "composicao conferida na portaria", True, [SEM_PDFTOTEXT], na=True); return
    plano_txt = re.sub(r"[\s\n]+", " ", txt)
    falhas = []
    # os codigos do objeto
    codigos = re.findall(r'"(\d{2}\.\d{2}\.\d{2}\.\d{3}-\d)":', d["estado"])
    # O layout do DOU parte o codigo: "02.06.03.003-" numa celula e o digito
    # verificador depois do nome do procedimento. Nenhum modo do pdftotext o mantem
    # inteiro, e procurar o digito numa janela aceita verificador errado. Entao a
    # fonte confere a RAIZ, que ja distingue procedimento de procedimento, e o digito
    # se confere entre plano.md e estado.yaml, logo abaixo.
    ausentes = [c for c in codigos if c.rsplit("-", 1)[0] not in plano_txt]
    if ausentes:
        falhas.append(f"raiz de codigo ausente da portaria: {', '.join(ausentes)}")
    # o codigo inteiro, com verificador, tem de ser o mesmo nos dois arquivos
    no_plano = set(re.findall(r"\d{2}\.\d{2}\.\d{2}\.\d{3}-\d", d["plano"]))
    so_no_plano = sorted(no_plano - set(codigos))
    if so_no_plano:
        falhas.append(f"codigo no plano.md que o estado.yaml nao declara: {', '.join(so_no_plano)}")
    ausentes = []
    # os pares valor de tabela + incremento da subsecao de composicao
    tc = tabela_com(d["tbs"], "valor de tabela", "incremento")
    n_par = 0
    if tc:
        for l in tc[1:]:
            if len(l) < 2: continue
            tab, inc = num(l[0]), num(l[1])
            if tab is None or inc is None: continue
            n_par += 1
            t_txt = f"{tab:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
            if t_txt not in plano_txt:
                falhas.append(f"valor de tabela R$ {t_txt} nao aparece em {alvo.name[:34]}")
            if f"{inc:.0f}%" not in plano_txt:
                falhas.append(f"incremento {inc:.0f}% nao aparece em {alvo.name[:34]}")
    else:
        falhas.append("tabela de composicao do unitario nao encontrada")
    # cada unitario da planilha tem de ser o produto truncado da composicao da 9.1
    comp = {}
    if tc:
        for l in tc[1:]:
            if len(l) < 3: continue
            tab, inc, un = num(l[0]), num(l[1]), num(l[2])
            if None in (tab, inc, un): continue
            esperado = math.floor(tab * (1 + inc / 100) * 100) / 100
            if abs(esperado - un) > 0.005:
                falhas.append(f"composicao: {tab} + {inc:.0f}% = {esperado:.2f}, publicado {un:.2f}")
            comp[round(un, 2)] = True
    if comp:
        for e in etapas_da_planilha(d["tbs"]):
            if e["meta"] not in METAS_EXEC: continue
            for nome, q, vu, m, tot in e["itens"]:
                if round(vu, 2) not in comp:
                    falhas.append(f"unitario {reais(vu)} da linha '{nome[:38]}' nao sai "
                                  f"da composicao publicada na subsecao de composicao")
    r.add("N", f"composicao conferida na portaria ({len(codigos)} codigos, {n_par} pares, "
          f"{len(comp)} unitarios)", not falhas, falhas)

def verificar_P(d, r):
    """metas: as mesmas no texto e na planilha, com quantitativo e prazo, e a qualitativa"""
    p = d["plano"]
    linhas, texto = {}, set()
    for m in re.finditer(r"\|\s*\*{0,2}Meta (\d)\*{0,2}\s*\|([^\n]*)\|", p):
        n = int(m.group(1))
        celulas = [c.strip() for c in m.group(2).split("|")]
        if len(celulas) >= 2 and len(celulas[0]) > 10:   # e a tabela de metas, nao a consolidacao
            texto.add(n)
            linhas[n] = celulas
    plan = set(metas_planilha(p).keys())
    falhas = []
    if not texto:
        falhas.append("nenhuma meta lida da subsecao de metas")
    so_texto, so_plan = texto - plan, plan - texto
    if so_texto:
        falhas.append(f"meta(s) {sorted(so_texto)} declarada(s) no texto e sem dotacao na planilha")
    if so_plan:
        falhas.append(f"meta(s) {sorted(so_plan)} orcada(s) na planilha e nao declarada(s) no texto")
    # conteudo de cada meta: descricao, quantitativo afericao e prazo
    for n in sorted(linhas):
        cel = linhas[n]
        if len(cel) < 3:
            falhas.append(f"Meta {n}: a linha traz {len(cel)} campos; o padrao pede descricao, quantitativo e prazo")
            continue
        quant, prazo = cel[1], cel[2]
        if not re.search(r"\d", quant):
            falhas.append(f"Meta {n}: quantitativo sem numero afericao — «{quant[:60]}»")
        if not re.search(r"\d|m[eê]s|semana|vig[eê]ncia", prazo, re.I):
            falhas.append(f"Meta {n}: prazo indefinido — «{prazo[:60]}»")
    # a meta qualitativa e obrigatoria
    # a declaracao, nao a mencao: o plano cita "a meta qualitativa da subsecao X" em
    # prosa, e isso mascarava a remocao da propria declaracao
    decl = re.search(r"^\s*\*{0,2}Meta qualitativa\*{0,2}\s*:", p, re.I | re.M)
    if not decl:
        falhas.append("meta qualitativa ausente — exigida pelo art. 7o, III do Decreto DF 48.727/2026")
    r.add("P", f"metas ({sorted(plan)}, conteudo e qualitativa)", not falhas, falhas)

CAMPOS_ID = {
    "cnpj": "CNPJ",
    "endereço": "endereço",
    "endereço da sede": "endereço",
    "representante legal": "representante legal",
    "razão social": "razão social",
    "natureza jurídica": "qualificação da entidade",
    "qualificação": "qualificação da entidade",
    "inscrição no cnes": "CNES",
}

def verificar_O(d, r):
    """campo de identificacao repetido em mais de uma secao"""
    p = d["plano"]
    # mapeia cada posicao do texto para a secao de primeiro nivel
    cortes = [(m.start(), m.group(1)) for m in re.finditer(r"^## (\d+)\. ", p, re.M)]
    def secao_de(pos):
        atual = None
        for ini, n in cortes:
            if ini <= pos: atual = n
            else: break
        return atual
    onde = {}
    for m in re.finditer(r"^\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|", p, re.M):
        rotulo = m.group(1).strip().lower()
        alvo = CAMPOS_ID.get(rotulo)
        if not alvo:
            continue
        onde.setdefault(alvo, set()).add(secao_de(m.start()))
    falhas = []
    for campo, secs in sorted(onde.items()):
        secs = {x for x in secs if x}
        if len(secs) > 1:
            falhas.append(f"'{campo}' aparece como campo nas secoes {sorted(secs)} — identificacao repetida")
    r.add("O", f"identificacao sem repeticao ({len(onde)} campos)", not falhas, falhas)

def estrutura_declarada(estado: str) -> str:
    """a estrutura que o plano segue: a chave `estrutura` na raiz do estado.yaml, ou a padrao.
    O modelo do proponente e o formulario da SES mandam na estrutura (comum, regra 15)."""
    m = re.search(r'^estrutura:\s*"?([A-Za-z0-9_]+)', estado, re.M)
    return m.group(1) if m else "padrao"

def estrutura_padrao(nome="padrao"):
    """le a tabela da estrutura <nome> em metodo/plano/estrutura.md; nao duplica a lista aqui"""
    if ESTRUTURA is None or not ESTRUTURA.exists():
        return None
    txt = ESTRUTURA.read_text(encoding="utf-8")
    m = re.search(r"^#+ Estrutura `" + re.escape(nome) + r"`\s*$", txt, re.M)
    if not m:
        return None
    i = m.start()
    linhas = txt[i:].splitlines()
    # so a PRIMEIRA tabela depois do cabecalho: o arquivo guarda varias estruturas,
    # e uma janela por caracteres engoliria a seguinte (ja aconteceu, com a de 13 secoes)
    fora, dentro = {}, False
    for l in linhas[1:]:
        if l.lstrip().startswith("|"):
            dentro = True
            m = re.match(r"\|\s*\*{0,2}(\d)\*{0,2}\s*\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|", l)
            if m:
                fora[int(m.group(1))] = m.group(2).strip()
        elif dentro:
            break
    return fora or None

def verificar_J(d, r):
    """estrutura conforme a estrutura declarada, travada em metodo/plano/estrutura.md"""
    nome = estrutura_declarada(d["estado"])
    padrao = estrutura_padrao(nome)
    if padrao is None:
        if nome != "padrao":
            r.add("J", "estrutura", False, [f"o estado.yaml declara a estrutura '{nome}', que nao "
                                            "existe em metodo/plano/estrutura.md"]); return
        r.add("J", "estrutura", True, ["estrutura.md nao encontrado ou sem a tabela da estrutura padrao"],
              na=True); return
    igual = lambda t: re.sub(r"\s*[/\-–]\s*", "-", t.strip().lower())
    falhas = []
    secoes = re.findall(r"^## (\d+)\. (.+)$", d["plano"], re.M)
    if len(secoes) != len(padrao):
        falhas.append(f"{len(secoes)} secoes de primeiro nivel, o metodo fixa {len(padrao)}")
    for i, (n, titulo) in enumerate(secoes, 1):
        if int(n) != i:
            falhas.append(f"secao na posicao {i} numerada como {n}")
        esperado = padrao.get(i)
        if esperado and igual(titulo) != igual(esperado):
            falhas.append(f"secao {i}: '{titulo.strip()}' — o metodo fixa '{esperado}'")
    subs = re.findall(r"^### (\d+)\.(\d+) ", d["plano"], re.M)
    if nome != "padrao":
        # no formulario da SES os campos da secao 1 sao linhas numeradas da tabela
        # ("| 1.7 Possui CNES? |"), e a primeira subsecao propria continua a contagem
        # (1.9 no plano 4): as linhas contam na sequencia
        subs = sorted(set(subs) | set(re.findall(r"^\| (\d+)\.(\d+) [^|]", d["plano"], re.M)),
                      key=lambda x: (int(x[0]), int(x[1])))
    por_secao = {}
    for a, b in subs:
        por_secao.setdefault(int(a), []).append(int(b))
    for sec, nums in sorted(por_secao.items()):
        if nums != list(range(1, len(nums) + 1)):
            falhas.append(f"secao {sec}: subsecoes {nums} nao formam sequencia 1..{len(nums)}")
    # secoes que nao voltam (metodo/plano/estrutura.md, "O que nao volta")
    VEDADOS = [(r"base legal", "Base legal como seção"),
               (r"o que n[ãa]o incide", "O que não incide"),
               (r"elegibilidade", "Elegibilidade e habilitação como seção"),
               (r"presta[çc][ãa]o de contas e monitoramento", "Prestação de contas como seção"),
               (r"contrapartida", "Contrapartida"),
               (r"sum[áa]rio executivo", "Sumário executivo")]
    titulos = re.findall(r"^#{2,3} [\d.]+ (.+)$", d["plano"], re.M)
    for t in titulos:
        for pad, veto in VEDADOS:
            if re.search(pad, t, re.I):
                falhas.append(f"seção '{t.strip()}' — «{veto}» não volta (plano/estrutura.md)")
    # na estrutura padrao, a secao 5 e a espinha: fluxo -> equipe -> metas -> indicadores
    t5 = [] if nome != "padrao" else [t for a, b, t in
          [(a, b, t) for a, b, t in re.findall(r"^### (\d+)\.(\d+) (.+)$", d["plano"], re.M)]
          if a == "5"]
    def pos(termo):
        for k, t in enumerate(t5):
            if termo in t.lower(): return k
        return None
    equipe, metas, indic = pos("equipe"), pos("metas"), pos("indicadores")
    if nome != "padrao":
        pass
    elif None in (equipe, metas, indic):
        falhas.append("secao 5 sem subsecao de equipe, metas ou indicadores")
    elif not (equipe < metas < indic):
        falhas.append(f"secao 5 fora da ordem fluxo -> equipe -> metas -> indicadores (posicoes {equipe}, {metas}, {indic})")
    r.add("J", f"estrutura '{nome}' ({len(secoes)} secoes, {len(subs)} subsecoes)", not falhas, falhas)

def verificar_K(d, r):
    """forma dos titulos"""
    proibidos = ("por que", "o que", "como ", "quando ", "quanto ", "onde ")
    falhas = []
    titulos = re.findall(r"^#{2,3} [\d.]+ (.+)$", d["plano"], re.M)
    for t in titulos:
        low = t.lower()
        if any(low.startswith(p) for p in proibidos):
            falhas.append(f"titulo anuncia argumento: '{t}'")
    r.add("K", f"forma dos titulos ({len(titulos)} titulos)", not falhas, falhas)

def verificar_L(d, r):
    """regra do metodo"""
    falhas = []
    p = d["plano"]
    for padrao, o_que in [(r"\[\[lacuna", "marcacao [[lacuna]]"),
                          (r"\bL-\d{3}\b", "id de lacuna L-xxx"),
                          (r"\bAC-\d{3}\b", "id de achado AC-xxx"),
                          (r"\bDV-\d{3}\b", "id de duvida DV-xxx"),
                          (r"\bV-\d{2}\b", "id de verificacao V-xx"),
                          (r"custo acess[oó]rio", "a expressao 'custo acessorio'"),
                          (r"pt_ses_\d", "referencia ao corpus")]:
        for m in re.finditer(padrao, p, re.I):
            ini = max(0, m.start() - 40)
            falhas.append(f"{o_que}: ...{p[ini:m.end()+40]}...".replace("\n", " "))
    # percentual de apoio sobre o global
    apoio, glob = d.get("_apoio"), d.get("_global")
    if apoio and glob:
        forma = f"{apoio/glob*100:.2f}".replace(".", ",") + "%"
        for m in re.finditer(re.escape(forma), p):
            ini = max(0, m.start() - 160)
            viz = p[ini:m.end() + 160].lower()
            if any(x in viz for x in ("apoio", "gestão", "acessório", "global")):
                falhas.append(f"percentual de apoio sobre o global publicado: {forma}")
    # [preencher] so em campo de identificacao
    for m in re.finditer(r"\[preencher[^\]]*\]", p):
        ini = p.rfind("\n", 0, m.start())
        linha = p[ini+1:p.find("\n", m.end())].strip()
        ok = linha.startswith("|") or linha.startswith("[preencher")
        if not ok:
            falhas.append(f"[preencher] fora de campo de identificacao: {linha[:70]}")
    r.add("L", "regra do metodo", not falhas, falhas)

# --------------------------------------------------------- prosa contra tabela

# As verificacoes A, B e C conferem tabela contra tabela. Nenhuma confere o que o
# texto AFIRMA contra o que a tabela TRAZ — e foi por essa fresta que passaram, em
# 02/09/2026, "104 resmas" (a planilha diz 105), "9 postos" (a planilha tem 11) e
# "a diferenca de R$ 3.020,00" (a tabela diz 19,45). Todas nasceram de uma mudanca
# de premissa que a planilha acompanhou e a prosa nao. E a regra 14 de metodo/comum.md
# virada em maquina.

PALAVRA_NUM = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4,
               "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
               "onze": 11, "doze": 12}

# rotulos curtos demais ou vazios de sentido nao viram ancora
VAZIAS = {"para", "por", "com", "dos", "das", "nos", "nas", "que", "este", "esta",
          "cada", "todo", "toda", "pelo", "pela", "sobre", "entre", "mais", "meta",
          "etapa", "item", "total", "valor", "unitario", "mese", "quando", "outro"}

NORMA_NO_PARAGRAFO = re.compile(
    r"portaria|nota t[ée]cnica|decreto|resolu[çc][ãa]o|instru[çc][ãa]o normativa|"
    r"\bRDC\b|\bLei\b|\bart\.|anexo|SIGTAP|tabela federal|componente cr[ée]ditos", re.I)

def radical(w: str) -> str:
    """singular aproximado, sem acento — 'postos' e 'posto' viram a mesma chave.

    A versao anterior cortava "es" antes de "s", e por isso "exames" virava "exam"
    enquanto "exame" continuava "exame": a planilha e a prosa nunca se encontravam,
    e a verificacao R.2 do plano 4 nao conferia uma unica quantidade. Em portugues o
    plural em "es" so vale depois de r, z, s, l ou n — depois de vogal o plural e
    so "s".
    """
    w = chave(w)
    if len(w) <= 4:
        return w
    if w.endswith(("oes", "aes")):
        return w[:-3] + "ao"
    if w.endswith("ais"):
        return w[:-3] + "al"
    if w.endswith("eis"):
        return w[:-3] + "el"
    if w.endswith("es") and w[-3] in "rzsln":
        return w[:-2]
    if w.endswith("s"):
        return w[:-1]
    return w

def paragrafos_de_prosa(md: str):
    """texto corrido apenas: sem tabela, sem citacao recuada, sem titulo"""
    paras, atual = [], []
    for linha in md.splitlines():
        s = linha.strip()
        if not s or s.startswith(("|", ">", "#", "---")):
            if atual:
                paras.append(" ".join(atual)); atual = []
            continue
        atual.append(s)
    if atual:
        paras.append(" ".join(atual))
    return paras

def numeros_das_tabelas(tbs):
    return {round(v, 2) for t in tbs for l in t for c in l
            if (v := num(c)) is not None}

def itens_de_planilha(tbs):
    """(nome, unidade, qtd, v_unitario, indice_da_tabela) de cada linha de item"""
    out = []
    for i, t in enumerate(tbs):
        cab = [chave(c) for c in t[0]]
        if "qtd" not in cab or "v. unitario" not in cab:
            continue
        i_q, i_v = cab.index("qtd"), cab.index("v. unitario")
        i_n = cab.index("item") if "item" in cab else 1
        i_u = cab.index("un.") if "un." in cab else None
        for l in t[1:]:
            if len(l) <= max(i_q, i_v):
                continue
            rot = chave(" ".join(l[:2]))
            if re.search(r"\bsubtotal\b|total da meta|total geral|valor global|^total\b", rot):
                continue                      # subtotal, TOTAL DA META, consolidacao
            q = num(l[i_q])
            if q is None:
                continue
            nome = l[i_n] if len(l) > i_n else ""
            un = chave(l[i_u]) if i_u is not None and len(l) > i_u else ""
            out.append((nome, un, q, num(l[i_v]), i))
    return out

def trecho(p, i, raio=55):
    return "..." + p[max(0, i - raio):i + raio].strip() + "..."

def verificar_R(d, r):
    """prosa contra tabela"""
    falhas, n = [], 0
    paras = paragrafos_de_prosa(d["plano"])
    tab = numeros_das_tabelas(d["tbs"])
    itens = itens_de_planilha(d["tbs"])

    # R.1 — todo valor em reais citado no texto sai de uma tabela, de um parametro
    #       do estado.yaml ou de uma norma citada no mesmo paragrafo
    for p in paras:
        da_norma = bool(NORMA_NO_PARAGRAFO.search(p))
        for m in re.finditer(r"R\$\s*([\d.]{1,12},\d\d)", p):
            v = num(m.group(1))
            if v is None:
                continue
            n += 1
            if any(perto(v, x) for x in (UNIT, RECURSO)):
                continue
            if any(perto(v, x) for x in tab):
                continue
            if da_norma:
                continue
            falhas.append(f"R$ {m.group(1)} nao aparece em nenhuma tabela nem vem de "
                          f"norma citada: {trecho(p, m.start())}")

    # R.2 — quantidade dita com o rotulo de um item ou de uma unidade da planilha
    aceito = {}
    def registrar(rot, valor):
        k = radical(rot)
        if len(k) < 4 or k in VAZIAS:
            return
        aceito.setdefault(k, set()).add(valor)
    somas = {}
    for nome, un, q, _, i_tab in itens:
        rotulos = [un] if un else []
        rotulos += re.findall(r"[^\W\d_]{4,}", chave(nome))
        for rot in rotulos:
            registrar(rot, q)
            k = radical(rot)
            somas.setdefault(k, {}).setdefault(i_tab, 0.0)
            somas[k][i_tab] += q
    for k, por_tabela in somas.items():            # subtotal por tabela e soma geral
        if k in aceito:
            aceito[k] |= set(por_tabela.values())
            aceito[k].add(sum(por_tabela.values()))
    for p in paras:
        for m in re.finditer(r"(?<![\d,.])(\d{1,3}(?:\.\d{3})+|\d+)\s+\*{0,2}([^\W\d_]{4,})", p):
            v, k = num(m.group(1)), radical(m.group(2))
            if v is None or k not in aceito:
                continue
            n += 1
            if any(perto(v, x, 0.5) for x in aceito[k]):
                continue
            # subtotal, rateio por polo, curva e capacidade publicam quantidades que
            # nao sao quantidade de item e sao corretas: o que a R.2 persegue e a
            # prosa que ficou para tras de uma mudanca, e essa nao esta em tabela
            # nenhuma do documento
            if any(perto(v, x, 0.5) for x in tab):
                continue
            esperados = ", ".join(f"{x:g}" for x in sorted(aceito[k]))
            falhas.append(f"'{m.group(0).strip()}' no texto; a planilha traz {esperados} "
                          f"para esse rotulo: {trecho(p, m.start())}")

    # R.3 — consumo derivado da unidade produzida: 'x xis por UNIDADE' obriga o total
    un_prod = next((un for _, un, _, vu, _ in itens if vu and perto(vu, UNIT) and un), None)
    qtd = d.get("_qtd")
    if un_prod and qtd:
        alvo = "|".join(PALAVRA_NUM)
        for p in paras:
            cp = chave(p)
            for m in re.finditer(rf"(\d+|{alvo})\s+([^\W\d_]{{4,}})\s+por\s+{re.escape(un_prod)}\b", cp):
                f = PALAVRA_NUM.get(m.group(1)) or num(m.group(1))
                k = radical(m.group(2))
                if not f or k in VAZIAS:
                    continue
                esperado = f * qtd
                for p2 in paras:
                    for m2 in re.finditer(rf"(?<![\d,.])(\d{{1,3}}(?:\.\d{{3}})+|\d{{3,}})\s+{k}s?\b",
                                          chave(p2)):
                        n += 1
                        if perto(num(m2.group(1)), esperado, 0.5):
                            continue
                        falhas.append(f"'{m2.group(0)}' no texto; {f:g} por {un_prod.upper()} x "
                                      f"{int(qtd)} = {esperado:.0f}: {trecho(p2, m2.start())}")

    r.add("R", f"prosa contra tabela ({n} numeros conferidos)", not falhas, falhas)

# ---------------------------------------------------------------- S, T, U, V
# As quatro verificacoes de 05/09/2026. Nasceram da devolutiva do professor sobre o
# redacao_03: das doze classes de erro que ela revelou, seis ja estavam escritas no
# padrao e voltaram assim mesmo. Regra que so existe como texto e cumprida
# enquanto alguem lembra dela. Estas quatro cobrem as tres classes que mais se
# repetiram, mais a que custou o unico erro de fato do documento.

PORTAO_CRIADO = [
    (r"condicionad[ao]s?\s+[àa]?\s*(?:comprova|apresenta|entrega)", "condicionante de liberacao criada pelo plano"),
    (r"\b(?:quando|caso|se)\b[^.]{0,40}\bexced(?:er|a)\b", "gatilho por prazo criado pelo plano"),
    (r"sob pena de", "sancao que o plano se impoe"),
]

REGUA_PROSA = [
    (r"(?:no m[íi]nimo|pelo menos|ao menos)\s+\d+(?:[,.]\d+)?\s*%", "meta graduada em prosa"),
    (r"≥\s*\d+(?:[,.]\d+)?\s*%", "meta com piso"),
    (r"±\s*\d+(?:[,.]\d+)?\s*%", "faixa de tolerancia"),
]

def verificar_S(d, r):
    """regua contra o proponente: compromisso graduado, faixa de tolerancia,
    quadro de pre-condicoes. Nada disso e exigido por norma, e tudo vira obrigacao
    afericavel na prestacao de contas — metodo/comum.md, regra 6."""
    falhas = []
    p = d["plano"]

    # 1. a meta de cada indicador e 100%, como nos aprovados
    # a tabela de indicadores pelo CABECALHO, e a coluna do percentual por tres nomes:
    # "parametro de afericao" (os aprovados), "parametro" (o modelo.md e o pre-plano) e
    # "meta" (o redacao_03). No modelo.md a coluna "meta" diz a QUAL meta o indicador
    # pertence: vale a primeira que traz percentual. Ate 08/10/2026 a S nao via a coluna
    # "parametro" - o pre-plano podia pactuar 95% sem acusar.
    t, i_m = None, None
    for tb in d["tbs"]:
        if not tb or "indicador" not in [chave(c) for c in tb[0]]:
            continue
        for nome in ("parametro de afericao", "parametro", "meta"):
            i = coluna(tb, nome)
            if i is not None and any(len(l) > i and "%" in l[i] for l in tb[1:]):
                t, i_m = tb, i
                break
        if t:
            break
    if t:
        # excecao so DECLARADA no estado.yaml, com motivo — como a ficha dispensada da V.
        # Em 01/10/2026 o usuario manteve o I-07 do plano 4 em 3% de proposito.
        exc = {}
        mb = re.search(r"^indicadores_fora_de_100:\s*\n((?:[ \t]+.*\n?)+)", d["estado"], re.M)
        if mb:
            for mi in re.finditer(r"^\s+(I-\d+):\s*\"?(.+?)\"?\s*$", mb.group(1), re.M):
                if len(mi.group(2).strip()) > 10:
                    exc[mi.group(1)] = mi.group(2).strip()
        if i_m is not None:
            for l in t[1:]:
                if len(l) <= i_m:
                    continue
                cel = chave(l[i_m])
                if "%" not in cel:
                    continue
                if l[0].strip().strip("*") in exc:
                    continue
                if num(cel) is not None and not perto(num(cel), 100.0, 0.001):
                    falhas.append(f"indicador '{l[1][:38] if len(l) > 1 else l[0]}': meta {l[i_m].strip()} — "
                                  f"meta e indicador se pactuam em 100%")

    # 2. prosa que gradua compromisso
    prosa = re.sub(r"^\|.*$", "", p, flags=re.M)
    for pad, o_que in REGUA_PROSA:
        for m in re.finditer(pad, prosa, re.I):
            ctx = re.sub(r"\s+", " ", prosa[max(0, m.start() - 60):m.end() + 40]).strip()
            falhas.append(f"{o_que}: ...{ctx}...")

    # 3. condicionante e gatilho que o PLANO cria contra si — a 7.1 dizia "cada
    #    parcela e liberada condicionada a comprovacao", que ninguem exigiu dela.
    #    Norma citada no mesmo paragrafo absolve: ai a condicao e da norma, nao nossa.
    for par in paragrafos_de_prosa(p) + [" ".join(l) for t in d["tbs"] for l in t]:
        if NORMA_NO_PARAGRAFO.search(par):
            continue
        for pad, o_que in PORTAO_CRIADO:
            for m in re.finditer(pad, par, re.I):
                ctx = re.sub(r"\s+", " ", par[max(0, m.start() - 60):m.end() + 60]).strip()
                falhas.append(f"{o_que}: ...{ctx}...")

    # 4. quadro de pre-condicoes — a 4.2 que saiu em 05/09/2026
    for t in d["tbs"]:
        cab = " ".join(chave(c) for c in t[0])
        if "comprova" in cab:
            falhas.append(f"tabela com coluna de comprovacao — quadro de pre-condicoes: {t[0]}")

    r.add("S", "regua contra o proponente", not falhas, falhas)


POR_EXTENSO = {
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5,
    "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12,
    "treze": 13, "catorze": 14, "quatorze": 14, "quinze": 15, "dezesseis": 16,
    "dezessete": 17, "dezoito": 18, "dezenove": 19, "vinte": 20, "trinta": 30,
    # ordinais: "a partir do decimo dia", "excede cinco dias uteis"
    "primeiro": 1, "segundo": 2, "terceiro": 3, "quarto": 4, "quinto": 5,
    "sexto": 6, "setimo": 7, "oitavo": 8, "nono": 9, "decimo": 10, "vigesimo": 20,
}

UNIDADES = [(r"%", "%"),
            (r"minutos?|min\b", "min"),
            (r"horas?\b", "hora"),
            (r"dias?\b", "dia"),
            (r"m[êe]s(?:es)?\b", "mes"),
            (r"compet[êe]ncias?", "competencia")]

def verificar_T(d, r):
    """numero sem lastro: todo percentual e toda medida de tempo dita em PROSA tem
    de existir no estado.yaml, em dados/, ou vir de norma citada no mesmo paragrafo.
    Foi assim que 30% de biopsia, 10% de rejeicao e seis tempos unitarios entraram no
    documento como se fossem dado — metodo/comum.md, regra 1."""
    # copia arquivada de plano NAO e fonte: o numero validaria a si mesmo
    def e_registro(f):
        n = f.name.lower()
        return not (n.startswith(("enviado", "plano")) or "devolutiva" in n)
    # o "@" separa os arquivos e nao pertence a janela de separadores de
    # perto_da_unidade: sem ele, um numero no fim de um arquivo casava com a unidade
    # no inicio do seguinte e fabricava lastro que nao existe
    corpus = chave(d["estado"])
    if BASE is not None and (BASE / "dados").exists():
        for f in sorted(BASE.joinpath("dados").rglob("*.md")):
            if e_registro(f):
                corpus += "\n@\n" + chave(f.read_text(encoding="utf-8"))
    # prosa E celula de tabela: os tempos unitarios que causaram o estrago em 03/09
    # — "8 min", "nos 30% com biopsia" — moravam em celula, nao em paragrafo
    trechos = list(paragrafos_de_prosa(d["plano"]))
    for t in d["tbs"]:
        # o 100% da coluna de parametro de um indicador e a propria regra (metodo/comum.md,
        # regra 6), nao numero que peca fonte: no pre-plano, sem esse 100% no estado.yaml,
        # a T acusava cada indicador
        cab = [chave(c) for c in t[0]] if t else []
        regra_100 = ({i for i, c in enumerate(cab) if c in ("parametro de afericao", "parametro", "meta")}
                     if "indicador" in cab else set())
        for linha in t:
            for i_cel, cel in enumerate(linha):
                if i_cel in regra_100 and cel.strip().strip("*") == "100%":
                    continue
                # nao basta filtrar por digito: "cinco dias uteis" nao tem nenhum
                if cel and re.search(r"[a-zA-Z%]", cel):
                    trechos.append(cel)
    falhas, n = [], 0
    for par in trechos:
        da_norma = bool(NORMA_NO_PARAGRAFO.search(par))
        for pad, canon in UNIDADES:
            # numero em digito e numero por extenso — "cinco dias uteis" e "decimo dia"
            # passavam batido ate 05/09/2026, quando a fase 7 os encontrou lendo
            achados = list(re.finditer(r"(?<![\d,.])(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s*(" + pad + r")", par, re.I))
            palavras = "|".join(POR_EXTENSO)
            achados += [m for m in re.finditer(r"\b(" + palavras + r")\s+(" + pad + r")", chave(par), re.I)]
            for m in achados:
                bruto = m.group(1)
                if not re.match(r"[\d]", bruto):
                    bruto = str(POR_EXTENSO[chave(bruto)])
                n += 1
                if da_norma:
                    continue
                # separador de milhar e decimal variam entre as fontes: 1.581, 1581, 52,14
                alvo = "".join("[.,]?" if c in ".," else re.escape(c) for c in bruto)
                # o numero tem de aparecer COLADO na mesma unidade em alguma fonte.
                # Janela larga nao serve: em 05/09/2026 um "17%" injetado passou
                # batido porque o estado.yaml tinha "10,21% com 17 pessoas" a 40
                # caracteres de distancia.
                # o padrao da unidade entra em grupo: "minutos?|min\b" sem parenteses
                # quebrava a ancora e o regex virava "qualquer 'min' no corpus", o que
                # dava lastro de graca a todo numero em minutos
                perto_da_unidade = re.compile(
                    r"(?<![\d])" + alvo + r"(?![\d])[\s*_ºoª°.\-]{0,3}(?:" + pad + r")", re.I)
                achado = perto_da_unidade.search(corpus)
                if achado:
                    ini = corpus.rfind("\n", 0, achado.start()) + 1
                    fim = corpus.find("\n", achado.end())
                    linha_fonte = corpus[ini:fim if fim > 0 else len(corpus)]
                    if re.search(r"premissa|sem fonte", linha_fonte):
                        falhas.append(f"'{m.group(0).strip()}' so tem registro marcado como "
                                      f"premissa sem fonte — regra 1: {trecho(par, m.start())}")
                    continue
                v = num(bruto)
                if v is not None and (round(v, 2), canon if canon == "%" else "") in d.get("_conferidos", set()):
                    continue        # numero que outra verificacao ja recalculou
                falhas.append(f"'{m.group(0).strip()}' sem lastro em estado.yaml, dados/ "
                              f"ou norma no paragrafo: {trecho(par, m.start())}")
    r.add("T", f"numero sem lastro ({n} medidas em prosa)", not falhas, falhas)


AUSENCIA_ANUNCIADA = [
    (r"n[ãa]o h[áa][^.]{0,80}?(?:rubrica|linha pr[óo]pria|linha na planilha|linha de)", "anuncia rubrica ausente"),
    (r"n[ãa]o (?:t[êe]m|tem) linha pr[óo]pria", "anuncia rubrica ausente"),
    (r"\bsem linha pr[óo]pria\b", "anuncia rubrica ausente"),
    (r"\bsem rubrica\b", "anuncia rubrica ausente"),
    (r"\bn[ãa]o (?:custeia|aluga|paga|prev[êe])\b", "anuncia despesa que nao faz"),
]

def verificar_U(d, r):
    """negacao de ausencia: o plano nomeia rubrica que NAO tem. E defesa antecipada —
    nenhum dos cinco aprovados escreve o que nao tem, e a verificacao Q nao alcanca
    esta forma porque ela nao usa enfase, usa inventario."""
    falhas = []
    prosa = re.sub(r"^\|.*$", "", d["plano"], flags=re.M)
    for pad, o_que in AUSENCIA_ANUNCIADA:
        for m in re.finditer(pad, prosa, re.I):
            ctx = re.sub(r"\s+", " ", prosa[max(0, m.start() - 70):m.end() + 70]).strip()
            falhas.append(f"{o_que}: ...{ctx}...")
    r.add("U", f"negacao de ausencia ({len(AUSENCIA_ANUNCIADA)} padroes)", not falhas, falhas)


def verificar_V(d, r):
    """ficha do procedimento: idade, sexo, quantidade maxima e valor conferidos
    contra dados/fontes/sigtap_*.md. A regra 3 de metodo/comum.md exige a ficha na fase 0 —
    foi a leitura da Nota Tecnica no lugar da ficha que pos 'sem recorte de faixa
    etaria' num procedimento de 18 a 130 anos."""
    if escalar(d["estado"], "ficha_sigtap.situacao", str) == "dispensada":
        r.add("V", "ficha do procedimento (dispensada no estado.yaml, com motivo)",
              True, ["a dispensa e decisao registrada em parametros.ficha_sigtap — "
                     "metodo/comum.md, regra 3, pede a ficha na fase 0"], na=True); return
    fichas = sorted((BASE / "dados" / "fontes").glob("sigtap_*.md")) if BASE else []
    if not fichas:
        r.add("V", "ficha do procedimento", False,
              ["nenhuma ficha em dados/fontes/sigtap_<codigo>_<competencia>.md — "
               "metodo/comum.md, regra 3: a ficha se consulta na fase 0"]); return
    ficha = chave(fichas[-1].read_text(encoding="utf-8"))
    p, falhas = d["plano"], []

    def campo(rotulo):
        m = re.search(r"\|\s*" + rotulo + r"\s*\|\s*([^|]+)\|", ficha)
        return m.group(1).strip() if m else None

    idade_min, idade_max = campo("idade minima"), campo("idade maxima")
    if idade_min:
        v = num(idade_min)
        if re.search(r"sem recorte de faixa et[áa]ria|faixa et[áa]ria n[ãa]o se aplica", p, re.I):
            falhas.append(f"o plano diz 'sem recorte de faixa etaria' e a ficha fixa idade minima de {v:.0f} anos")
        elif v and v > 0 and not re.search(rf"(?<!\d){v:.0f}\s*anos", p):
            falhas.append(f"a ficha fixa idade minima de {v:.0f} anos e o plano nao a declara")
    if idade_max and num(idade_max) and num(idade_max) < 130:
        v = num(idade_max)
        if not re.search(rf"(?<!\d){v:.0f}\s*anos", p):
            falhas.append(f"a ficha fixa idade maxima de {v:.0f} anos e o plano nao a declara")

    qmax = campo("quantidade maxima")
    if qmax and num(qmax) and num(qmax) != 1:
        falhas.append(f"quantidade maxima da ficha e {qmax} — conferir a unidade de afericao do plano")

    if UNIT and reais(UNIT).replace("R$ ", "") not in ficha:
        falhas.append(f"o unitario {reais(UNIT)} nao aparece na ficha {fichas[-1].name}")

    codigo = escalar(d["estado"], "objeto.oci", str)
    if codigo and chave(codigo) not in ficha:
        falhas.append(f"o codigo {codigo} do objeto nao aparece na ficha {fichas[-1].name}")

    r.add("V", f"ficha do procedimento ({fichas[-1].name})", not falhas, falhas)


# ---------------------------------------------------------------- W, X
# As duas de 27/09/2026, nascidas da leitura dos cinco planos aprovados contra o
# SIGTAP e contra as representacoes do MPCDF (registros/licoes.csv: as licoes com
# verificacao W ou X). Tres dos cinco aprovados erram codigo ou nome de OCI, e o MPCDF usou o
# codigo errado como prova; e as rubricas que o controle atacou sao reconheciveis
# pelo nome.

# Qualquer grupo da tabela: OCI (09) e procedimento avulso (02 diagnostico, 03 clinico...).
# O digito se confere em todos; o catalogo, por ora, so tem o grupo 09.
RE_CODIGO_SIGTAP = re.compile(r"(?<![\d.])(0[1-9]\.\d{2}\.\d{2}\.\d{3})(?:-(\d))?(?![\d])")
# escrito corrido, so o do grupo 09: dez digitos soltos de outro grupo podem ser qualquer coisa
RE_CODIGO_OCI_CORRIDO = re.compile(r"(?<!\d)(09\d{8})(?!\d)")
RE_ITEM_PLANILHA = re.compile(r"^\|\s*\*{0,2}\d+(?:\.\d+)+\*{0,2}\s*\|")
RE_DINHEIRO = re.compile(r"(?<![\d.,])\d{1,3}(?:\.\d{3})*,\d{2}(?!\d)")
PALAVRAS_VAZIAS = {"oci", "para", "com", "das", "dos", "partir"}

def digito_sigtap(nove: str) -> int:
    """modulo 11 com pesos 10 a 2; resto 0 ou 1 da digito 0. Confere os 49 codigos
    do grupo 09 na competencia 09/2026 e os 101 do rol de imagem da Portaria SAES/MS
    4.282/2026 (grupos 02 e 03)."""
    d = 11 - sum(int(c) * p for c, p in zip(nove, range(10, 1, -1))) % 11
    return 0 if d >= 10 else d

def catalogo_sigtap():
    """o catalogo mais recente de registros/fontes/sigtap_grupo09_<MMAAAA>.csv"""
    import csv
    arquivos = sorted((RAIZ / "registros" / "fontes").glob("sigtap_grupo09_*.csv"),
                      key=lambda f: (f.stem[-4:], f.stem[-6:-4]))
    if not arquivos:
        return None, {}
    with arquivos[-1].open(encoding="utf-8", newline="") as f:
        return arquivos[-1], {l["codigo"]: l for l in csv.DictReader(f)}

def palavras(t: str):
    return {w for w in re.findall(r"[a-z0-9]{4,}", chave(t)) if w not in PALAVRAS_VAZIAS}

def verificar_W(d, r):
    """codigos SIGTAP do plano. Em todos, de OCI ou de procedimento avulso: digito
    verificador. Nos do grupo 09, contra o catalogo: existencia, revogacao, nome
    escrito ao lado do codigo e valor na linha da planilha. Pega o 09.03.01.004-0 dos
    pt_ses_02 e 03, o 09.02.01.001 sem digito e a troca de nomes e valores das OCI
    cardiologicas do pt_ses_04 (AC-017, AC-058, AC-059). O valor do exame avulso nao
    se confere aqui: e tabela mais incremento, e quem o confere e a N."""
    p = d["plano"]
    codigos = [(m.start(), m.group(1), m.group(2)) for m in RE_CODIGO_SIGTAP.finditer(p)]
    for m in RE_CODIGO_OCI_CORRIDO.finditer(p):
        c = m.group(1)
        codigos.append((m.start(), f"{c[:2]}.{c[2:4]}.{c[4:6]}.{c[6:9]}", c[9]))
    if not codigos:
        r.add("W", "codigos SIGTAP", True, ["o plano nao cita codigo SIGTAP"], na=True); return
    fonte, cat = catalogo_sigtap()
    if not cat and any(b.startswith("09.") for _, b, _ in codigos):
        r.add("W", "codigos SIGTAP", False,
              ["catalogo registros/fontes/sigtap_grupo09_<MMAAAA>.csv ausente"]); return
    falhas, vistos = [], set()
    for pos, base, dv in sorted(codigos):
        certo = digito_sigtap(base.replace(".", ""))
        rotulo = f"{base}-{dv}" if dv else base
        if dv is None:
            falhas.append(f"{base} sem digito verificador — e {base}-{certo}")
            continue
        if int(dv) != certo:
            falhas.append(f"{rotulo}: digito verificador errado — e {base}-{certo}")
            continue
        if not base.startswith("09."):
            continue                      # fora do catalogo: so o digito
        linha = cat.get(rotulo)
        if linha is None:
            if rotulo not in vistos:
                falhas.append(f"{rotulo} nao existe no grupo 09 do SIGTAP ({fonte.name})")
            vistos.add(rotulo); continue
        if linha["situacao"].startswith("revogado") and rotulo not in vistos:
            falhas.append(f"{rotulo} {linha['situacao']}")
        vistos.add(rotulo)
        # o nome escrito logo depois do codigo ("09.02.01.004-2 — Avaliacao ...")
        depois = re.split(r"[\n|]", p[pos + len(rotulo):pos + len(rotulo) + 160])[0]
        m = re.match(r"\s*\**\s*[–—:-]\s*(.+)", depois)
        # o nome acaba na primeira virgula: "09.05.01.003-5 – OCI, integrante da
        # Tabela..." nao da nome nenhum, e "... Gastrico, concluida na forma" da so o nome
        nome = re.split(r"[,;.(]", m.group(1))[0] if m else ""
        if palavras(nome):
            esperado = palavras(linha["nome"])
            if esperado and len(esperado & palavras(nome)) / len(esperado) < 0.5:
                falhas.append(f"{rotulo} escrito como '{nome.strip()[:60]}' — no SIGTAP e "
                              f"'{linha['nome']}'")
    # valor na linha da planilha que carrega o codigo
    for l in p.splitlines():
        if not RE_ITEM_PLANILHA.match(l):
            continue
        for m in RE_CODIGO_SIGTAP.finditer(l):
            linha = cat.get(f"{m.group(1)}-{m.group(2)}")
            valores = RE_DINHEIRO.findall(l)
            if linha and linha["valor_total_ambulatorial"] and valores \
                    and linha["valor_total_ambulatorial"] not in valores:
                falhas.append(f"planilha: {m.group(0)} sem o valor da tabela "
                              f"(R$ {linha['valor_total_ambulatorial']}) na linha")
    n = len({b for _, b, _ in codigos})
    r.add("W", f"codigos SIGTAP ({n} distintos" + (f"; grupo 09 contra {fonte.name})" if fonte else ")"),
          not falhas, falhas)


RUBRICA_ATACADA = [
    (r"taxa de (?:administra[çc][ãa]o|ger[êe]ncia)",
     "taxa de administracao ou gerencia — vedada pelo termo (clausula 9.2, VII; OB-051)"),
    ((r"audiovisual|fotogr[áa]fic|jornal[íi]stic|videomaker|social\s*m[íi]dia|"
      r"assessoria de imprensa|camisetas?|brindes?|kits? de acolhimento"),
     ("comunicacao sem carater educativo — termo 9.2, VIII (OB-049); o MPCDF atacou no "
      "030989 e no TF 031000")),
    (r"\btriagem\b(?!\s+qualificada)",
     "atendimento descrito como triagem — o termo veda (clausula 4.1.2.3; OB-047)"),
]

def secao(md: str, n: int) -> str:
    """o texto da secao de primeiro nivel n, ate a seguinte"""
    m = re.search(rf"^## {n}\. .*$", md, re.M)
    if not m:
        return ""
    fim = re.search(r"^## \d+\. ", md[m.end():], re.M)
    return md[m.end(): m.end() + fim.start()] if fim else md[m.end():]

RE_CODIGO = re.compile(r"\b\d{2}\.\d{2}\.\d{2}\.\d{3}-\d\b")
RE_REAIS = re.compile(r"R\$\s*([\d.]+,\d{2})")

def verificar_Y(d, r):
    """o plano contra o pre-plano enviado, quando o projeto tem os dois.

    O pre-plano foi a SES antes, e o plano detalhado e conferido contra ele: objeto,
    codigos, valor total e producao nao podem contradizer o que foi enviado
    (metodo/pre_plano/procedimento.md). O estado.yaml aponta o enviado em
    `pre_plano_enviado` (caminho a partir da raiz do projeto). Divergencia decidida se
    declara em `pre_plano_divergencias`, com motivo - como a ficha dispensada da V."""
    m = re.search(r'^pre_plano_enviado:\s*"?([^"\n#]+?)"?\s*(?:#.*)?$', d["estado"], re.M)
    if not m:
        r.add("Y", "contra o pre-plano enviado", True, ["o estado.yaml nao aponta pre-plano enviado"],
              na=True); return
    arq = RAIZ / m.group(1).strip()
    if not arq.exists():
        r.add("Y", "contra o pre-plano enviado", False, [f"pre-plano enviado nao encontrado: {m.group(1)}"]); return
    pp = arq.read_text(encoding="utf-8")
    aceitas = set()
    mb = re.search(r"^pre_plano_divergencias:\s*\n((?:[ \t]+.*\n?)+)", d["estado"], re.M)
    if mb:
        for mi in re.finditer(r"^\s+(codigos|valor_total|producao):\s*\"?(.+?)\"?\s*$", mb.group(1), re.M):
            if len(mi.group(2).strip()) > 10:
                aceitas.add(mi.group(1))
    falhas = []
    novos = sorted(set(RE_CODIGO.findall(d["plano"])) - set(RE_CODIGO.findall(pp)))
    if novos and "codigos" not in aceitas:
        falhas.append(f"codigos do plano que o pre-plano nao trazia: {', '.join(novos)}")
    total = None
    for t in tabelas(secao(pp, 1)):
        for l in t:
            if l and re.search(r"valor total", l[0], re.I):
                vs = RE_REAIS.findall(" ".join(l[1:]))
                total = num(vs[0]) if vs else None
    glob = d.get("_global")
    if total is None:
        falhas.append("Valor Total nao encontrado na primeira secao do pre-plano")
    elif glob and not perto(glob, total) and "valor_total" not in aceitas:
        falhas.append(f"valor global do plano {reais(glob)}, Valor Total do pre-plano {reais(total)}")
    aplic = sum(num(v) for t in tabelas(secao(pp, 8)) for l in t[1:] if l
                for v in RE_REAIS.findall(l[-1])[:1])
    prod = d.get("_exec")
    if aplic and prod and not perto(prod, aplic) and "producao" not in aceitas:
        falhas.append(f"producao assistencial do plano {reais(prod)}, aplicacao das despesas do "
                      f"pre-plano {reais(aplic)}")
    det = f"{arq.name}" + (f"; divergencias declaradas: {', '.join(sorted(aceitas))}" if aceitas else "")
    r.add("Y", f"contra o pre-plano enviado ({det})", not falhas, falhas)

def verificar_X(d, r):
    """rubrica vedada pelo termo de convenio ou atacada pelo controle externo, na
    linha da planilha. A taxa de administracao vale em qualquer lugar do texto."""
    falhas = []
    for l in d["plano"].splitlines():
        if not RE_ITEM_PLANILHA.match(l):
            continue
        for pad, o_que in RUBRICA_ATACADA:
            m = re.search(pad, l, re.I)
            if m:
                falhas.append(f"{o_que}: ...{l[max(0, m.start() - 50):m.end() + 30].strip()}...")
    prosa = re.sub(r"^\|.*$", "", d["plano"], flags=re.M)
    for m in re.finditer(RUBRICA_ATACADA[0][0], prosa, re.I):
        ctx = re.sub(r"\s+", " ", prosa[max(0, m.start() - 60):m.end() + 30]).strip()
        falhas.append(f"{RUBRICA_ATACADA[0][1]}: ...{ctx}...")
    r.add("X", "rubrica vedada ou atacada pelo controle", not falhas, falhas)


def verificacoes_do_plano():
    """as funcoes verificar_<nome>(d, r, P) de planos/redacao_NN/conferencia/verificacoes.py.

    A bateria do plano confere o que so aquele objeto tem. Ela recebe este modulo como P,
    para usar as mesmas funcoes de leitura e os parametros ja carregados. Ver
    metodo/plano/conferencia.md."""
    arq = BASE / "conferencia" / "verificacoes.py"
    if not arq.exists():
        return []
    spec = importlib.util.spec_from_file_location(f"bateria_{BASE.name}", arq)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [f for n, f in vars(mod).items() if n.startswith("verificar_") and callable(f)]

def main():
    global BASE, RAIZ, ESTRUTURA, NORMAS
    ap = argparse.ArgumentParser(description="confere um plano de trabalho do projeto")
    ap.add_argument("plano", help="diretorio do plano, por exemplo redacao_03/")
    ap.add_argument("--verboso", action="store_true")
    ap.add_argument("--raiz", help="raiz do projeto, onde estao metodo/ e "
                                   "biblioteca/normas/; padrao: a raiz do repositorio")
    args = ap.parse_args()
    saida_utf8()
    BASE = Path(args.plano).resolve()
    RAIZ = Path(args.raiz).resolve() if args.raiz else comum.RAIZ
    ESTRUTURA = RAIZ / comum.ESTRUTURA_PLANO.relative_to(comum.RAIZ)
    NORMAS = RAIZ / comum.NORMAS.relative_to(comum.RAIZ)
    d = carregar()
    faltas = carregar_parametros(d["estado"])
    if faltas:
        raise SystemExit("erro: estado.yaml sem " + ", ".join(faltas) +
                         " — ver metodo/plano/procedimento.md, as chaves do estado.yaml")
    r, rp = R(), R()          # a bateria do padrao e a do plano
    P = sys.modules[__name__]
    for f in (verificar_A, verificar_B, verificar_C, verificar_D, verificar_E,
              verificar_F, verificar_G, verificar_H, verificar_I, verificar_J,
              verificar_K, verificar_L, verificar_M, verificar_N, verificar_N_multi,
              verificar_O, verificar_P,
              verificar_Q, verificar_R, verificar_S, verificar_T,
              verificar_U, verificar_V, verificar_W, verificar_X, verificar_Y):
        try:
            f(d, r)
        except Exception as e:
            # verificar_N_multi e da N: a sigla e o que vem depois de "verificar_"
            r.add(f.__name__.split("_")[1], f.__name__, False, [f"erro na verificacao: {e!r}"])
        if f is verificar_G:
            # a bateria do plano roda aqui, logo depois da G e antes da T: o que ela
            # recalcula (a capacidade, no redacao_03) e lastro para os numeros da prosa
            for fp in verificacoes_do_plano():
                try:
                    fp(d, rp, P)
                except Exception as e:
                    rp.add("+?", fp.__name__, False, [f"erro na verificacao do plano: {e!r}"])
    print()
    print(f"CONFERENCIA DO PLANO — {BASE.name}")
    cab = (f"{len(UNITS)} unitarios de {reais(min(UNITS))} a {reais(max(UNITS))}"
           if MULTI else f"unitario {reais(UNIT)}")
    print(f"  {cab} · recurso {reais(RECURSO)} · {DIAS_UTEIS} dias uteis · "
          f"polos: {', '.join(POLOS) if POLOS else 'sitio unico'}")
    def bloco(itens):
        for sigla, nome, ok, det, na in itens:
            veredito = "NAO SE APLICA" if na else ("PASSOU" if ok else "FALHOU")
            print(f"  {sigla}  {nome:<46} {veredito}")
            if det and (not ok or args.verboso):
                for x in det[:20]:
                    print(f"        - {x}")
                if len(det) > 20:
                    print(f"        ... e mais {len(det)-20}")
    padrao, do_plano = r.itens, rp.itens
    print("=" * 78)
    bloco(padrao)
    if do_plano:
        print("-" * 78)
        print("  BATERIA DO PLANO — conferencia/verificacoes.py")
        bloco(do_plano)
    print("=" * 78)
    passou = lambda itens: sum(1 for _, _, ok, _, na in itens if ok and not na)
    todos = padrao + do_plano
    print(f"  {passou(todos)}/{len(todos)} verificacoes passaram"
          + (f" — padrao {passou(padrao)}/{len(padrao)}, plano {passou(do_plano)}/{len(do_plano)}"
             if do_plano else ""))
    if AMBIENTE:
        # NAO SE APLICA por falta de programa nao e o mesmo que nao se aplicar ao
        # plano: a verificacao existe e nao rodou.
        print(f"  AVISO: {', '.join(sorted(set(AMBIENTE)))} nao rodou neste computador - "
              f"{SEM_PDFTOTEXT}")
    print()
    return 1 if (r.falhou or rp.falhou) else 0

if __name__ == "__main__":
    sys.exit(main())
