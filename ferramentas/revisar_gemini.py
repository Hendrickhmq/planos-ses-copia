#!/usr/bin/env python3
"""
revisar_gemini.py - roda o revisor do Google (Gemini Notebook) sobre um pacote cego.

Uso:
    python3 revisar_gemini.py <pacote> --saida <rodada>/gemini [--consultas G1,G3,G5,G9,G7]
        [--faturamento] [--obrigacoes fontes/normas/<arquivo>.md]... [--caderno <id>]
    python3 revisar_gemini.py <pacote> --saida <rodada>/gemini --treplica <rodada anterior>

O metodo e metodo/revisao/gemini.md. As perguntas sao os blocos ```prompt``` de
metodo/revisao/perguntas.md, e os blocos proprios do Gemini (instrucao, formato, G4, G6,
G8) ficam em gemini.md: este script nao guarda pergunta. Usa o `nlm` (NotebookLM Tools), ja autenticado.

1. Cria um caderno novo e neutro e sobe o pacote: o documento com o titulo
   "DOCUMENTO EM ANALISE", as fontes com o nome do arquivo. Configura a instrucao.
   (--caderno reaproveita um caderno ja montado por este script, pelo caderno.json.)
2. Roda cada consulta numa conversa nova: G1, G3, G5, G9 e G7; G2 com --faturamento; a G4 uma
   vez por fonte de --obrigacoes, com a consulta restrita a ela.
3. Converte os blocos ### ACHADO para o esquema de achados. O trecho da fonte, quando o
   Gemini cita, vem da propria citacao do caderno (cited_text).
4. Confere as citacoes (conferir_revisao.py) e roda a G6 sobre cada achado cujo trecho
   da fonte nao confere, restrita a fonte citada.

Saida: brutos/<consulta>.json, achados.json, obrigacoes/<fonte>.md e caderno.json.
"""
from __future__ import annotations
import argparse, json, re, subprocess, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from comum import saida_utf8
import conferir_revisao as CR

RAIZ = Path(__file__).resolve().parent.parent
METODO = RAIZ / "metodo" / "revisao" / "gemini.md"
PERGUNTAS = RAIZ / "metodo" / "revisao" / "perguntas.md"
TITULO_DOC = "DOCUMENTO EM ANÁLISE"
CAMPOS = ("classe", "trecho_documento", "fonte", "trecho_fonte", "gravidade", "por_que")


def prompts(caminho: Path = METODO) -> dict[str, str]:
    """As perguntas de perguntas.md, mais os blocos proprios do Gemini (instrucao, formato,
    G4, G6, G8) de gemini.md."""
    saida = {}
    for arq in (PERGUNTAS, caminho):
        txt = arq.read_text(encoding="utf-8")
        saida.update({m.group(1): m.group(2).strip() for m in re.finditer(r"```prompt (\S+)\n(.*?)```", txt, re.S)})
    return saida


class SemResposta(RuntimeError):
    """O caderno nao respondeu. Quando todos os cadernos param ao mesmo tempo, e a cota do
    plano do Gemini, que se renova a cada 5 horas (calibracao de 11/10/2026)."""


def nlm(*args, timeout=900) -> dict:
    erro = ""
    for tentativa in range(3):
        r = subprocess.run(["nlm", *args, "--json"], capture_output=True, text=True, timeout=timeout)
        saida = r.stdout[r.stdout.find("{"):] if "{" in r.stdout else r.stdout
        try:
            d = json.loads(saida)
        except json.JSONDecodeError:
            d = {"bruto": r.stdout}
        if r.returncode == 0 and d.get("status") != "error":
            return d
        erro = d.get("error") or r.stderr[-300:] or r.stdout[-300:]
        time.sleep(10 * (tentativa + 1))
    raise SemResposta(f"nlm {' '.join(args[:2])}: {erro}")


def titulo_da_fonte(rel: str) -> str:
    """O titulo no caderno: sem extensao nem sublinhado. "nome.md" vira, na resposta do
    Google, "[suspicious link removed]" (calibracao de 11/10/2026)."""
    if rel == "documento.md":
        return TITULO_DOC
    return Path(rel).stem.replace("_", " ")


def montar_caderno(pacote: Path, saida: Path, P: dict) -> dict:
    man = json.loads((pacote / "manifesto.json").read_text(encoding="utf-8"))
    titulo = f"Análise — {man['titulo']} — {datetime.now():%d/%m/%Y %H:%M}"
    nb = nlm("notebook", "create", titulo)["notebook_id"]
    fontes = {}

    def subir(item):
        rel = item["arquivo"]
        nome = titulo_da_fonte(rel)
        r = nlm("source", "add", nb, "--file", str(pacote / rel), "--title", nome, "--wait")
        print(f"  fonte: {nome}", flush=True)
        return r["source_id"], {"arquivo": rel, "titulo": nome}

    # os aprovados ficam fora: com eles no caderno, o Gemini toma um aprovado pelo documento
    # em analise e responde sem citar (calibracao de 11/10/2026). A estrutura contra os
    # aprovados e a A7, do Claude cego.
    arquivos = [a for a in man["arquivos"] if not a["arquivo"].startswith("fontes/aprovados/")]
    with ThreadPoolExecutor(max_workers=4) as ex:
        fontes.update(ex.map(subir, arquivos))
    subprocess.run(["nlm", "chat", "configure", nb, "--goal", "custom", "--prompt", P["instrucao"],
                    "--response-length", "longer"], capture_output=True, text=True, check=True)
    cad = {"notebook_id": nb, "titulo": titulo, "fontes": fontes}
    (saida / "caderno.json").write_text(json.dumps(cad, ensure_ascii=False, indent=2), encoding="utf-8")
    return cad


def sem_aprovados(cad: dict) -> list[str]:
    """As fontes do caderno menos os aprovados, para a restricao mecanica."""
    return [k for k, v in cad["fontes"].items() if not v["arquivo"].startswith("fontes/aprovados/")]


def consultar(cad: dict, texto: str, fontes: list[str] | None = None) -> dict:
    """Uma conversa nova, sempre com --source-ids. No formato rigido o caderno quase nunca
    devolve a marca de citacao; a prova e mecanica, pelo trecho literal (conferir_revisao)."""
    fontes = fontes or sem_aprovados(cad)
    return nlm("notebook", "query", cad["notebook_id"], texto, "--new-conversation", "--timeout", "600",
               "--source-ids", ",".join(fontes))


def blocos(resposta: str, marca: str) -> list[dict]:
    """Os blocos ### MARCA de uma resposta, campo: valor."""
    saida = []
    # o titulo do bloco vem como "### ACHADO", "**### ACHADO**" ou "**ACHADO**"
    for bloco in re.split(rf"^[\s*#]*{marca}[\s*:]*$", resposta, flags=re.M)[1:]:
        item, campo = {}, None
        for linha in bloco.splitlines():
            if re.match(r"^[\s*]*VAZIO\s*:", linha):   # a linha de lista vazia fecha o bloco
                campo = None
                continue
            m = re.match(r"^\s*[*-]?\s*\**([a-z_]+)\**\s*:\s*(.*)$", linha)
            if m and m.group(1) in CAMPOS + ("dispositivo", "transcricao", "id", "veredito", "trecho"):
                campo = m.group(1)
                item[campo] = m.group(2).strip()
            elif campo and linha.strip():
                item[campo] += " " + linha.strip()
        saida.append(item)
    return saida


def limpar(t: str) -> str:
    t = re.sub(r"\[\d+(?:\s*[,-]\s*\d+)*\]", "", t or "").strip()
    return t.strip().strip('"“”').strip()


def converter(cad: dict, consulta: str, bruto: dict) -> list[dict]:
    titulo_para_arq = {v["titulo"]: v["arquivo"] for v in cad["fontes"].values()}
    resposta = bruto.get("answer", "")
    refs = {str(r["citation_number"]): r for r in bruto.get("references", [])}
    achados = []
    for n, b in enumerate(blocos(resposta, "ACHADO"), 1):
        fonte_tit = limpar(b.get("fonte", "")).strip("*")
        arq = titulo_para_arq.get(fonte_tit) or next(
            (a for t, a in titulo_para_arq.items() if fonte_tit and (fonte_tit in t or t in fonte_tit)), None)
        trecho_fonte = limpar(b.get("trecho_fonte", ""))
        # a fonte pela marca de citacao: primeiro as do trecho_fonte, depois as do bloco
        # inteiro; vale a primeira que nao e o proprio documento
        marcas = re.findall(r"\[(\d+)", b.get("trecho_fonte", "")) + re.findall(
            r"\[(\d+)", " ".join(str(v) for v in b.values()))
        citado = None
        for m in marcas:
            r = refs.get(m)
            arq_r = cad["fontes"].get(r["source_id"], {}).get("arquivo") if r else None
            if arq_r and arq_r != "documento.md" and (arq is None or arq_r == arq):
                arq, citado = arq_r, r.get("cited_text")
                break
        achados.append({
            "id": f"GEM-{consulta}-{n:02d}", "revisor": "gemini", "passada": consulta,
            "classe": limpar(b.get("classe", "")), "secao": "",
            "trecho_documento": limpar(b.get("trecho_documento", "")),
            "fonte_arquivo": arq, "trecho_fonte": trecho_fonte or None,
            "citacao_do_caderno": citado, "conta": None,
            "gravidade": limpar(b.get("gravidade", "")) or "diligencia",
            "por_que": limpar(b.get("por_que", "")),
            "sem_marca_de_citacao": not bruto.get("sources_used"),
        })
    return achados


def provar(cad: dict, pacote: Path, achados: list[dict], P: dict, saida: Path):
    """G6: para o achado cujo trecho da fonte nao confere, a transcricao restrita a fonte."""
    arq_para_id = {v["arquivo"]: k for k, v in cad["fontes"].items()}
    for a in achados:
        if a.get("citacao") != "fonte: trecho não encontrado" or not a.get("fonte_arquivo"):
            continue
        sid = arq_para_id.get(a["fonte_arquivo"])
        if not sid:
            continue
        try:
            r = consultar(cad, P["G6"].replace("{afirmacao}", a["por_que"]), [sid])
        except SemResposta:
            a["prova"] = "G6 sem resposta (cota?)"
            continue
        (saida / "brutos" / f"G6_{a['id']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
        resp = r.get("answer", "")
        if "NAO_HA" in resp:
            a["prova"] = "a fonte não sustenta (G6)"
            continue
        refs = [x.get("cited_text") for x in r.get("references", []) if x.get("source_id") == sid]
        texto_fonte = (pacote / a["fonte_arquivo"]).read_text(encoding="utf-8")
        candidatos = [limpar(resp)] + [c for c in refs if c]
        prova = next((c for c in candidatos if CR.existe(c, texto_fonte)), None)
        if prova:
            a["trecho_fonte"], a["prova"] = prova, "G6: trecho literal achado"
        else:
            a["prova"] = "G6: sem trecho literal"


def main():
    saida_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pacote")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--consultas", default="G1,G3,G5,G9,G7")
    ap.add_argument("--faturamento", action="store_true")
    ap.add_argument("--obrigacoes", action="append", default=[])
    ap.add_argument("--caderno", help="reaproveitar o caderno de uma saida anterior (caderno.json)")
    ap.add_argument("--treplica", help="a pasta da rodada anterior")
    ap.add_argument("--reconverter", action="store_true",
                    help="reler brutos/ com o leitor atual, sem consultar o caderno de novo")
    args = ap.parse_args()
    pacote, saida = Path(args.pacote).resolve(), Path(args.saida).resolve()
    (saida / "brutos").mkdir(parents=True, exist_ok=True)
    P = prompts()
    if args.reconverter:
        cad = json.loads((saida / "caderno.json").read_text(encoding="utf-8"))
        achados = []
        for c in [c.strip() for c in args.consultas.split(",")] + (["G2"] if args.faturamento else []):
            arq = saida / "brutos" / f"{c}.json"
            if arq.exists():
                achados += converter(cad, c, json.loads(arq.read_text(encoding="utf-8")))
        dados = {"revisor": "gemini", "caderno": cad["notebook_id"],
                 "data": datetime.now().isoformat(timespec="minutes"), "achados": achados}
        CR.conferir_achados(pacote, dados)
        provar(cad, pacote, achados, P, saida)
        CR.conferir_achados(pacote, dados)
        (saida / "achados.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{len(achados)} achados relidos em {saida / 'achados.json'}")
        return
    if args.caderno:
        cad = json.loads(Path(args.caderno).read_text(encoding="utf-8"))
        (saida / "caderno.json").write_text(json.dumps(cad, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print("montando o caderno")
        cad = montar_caderno(pacote, saida, P)
    if args.treplica:
        treplica(cad, pacote, Path(args.treplica).resolve(), saida, P)
        return
    consultas = [c.strip() for c in args.consultas.split(",") if c.strip()]
    if args.faturamento and "G2" not in consultas:
        consultas.insert(1, "G2")
    achados = []
    falharam = []
    for c in consultas:
        inicio = time.time()
        try:
            bruto = consultar(cad, P[c] + "\n\n" + P["formato"])
        except SemResposta as e:
            falharam.append(c)
            print(f"  {c}: SEM RESPOSTA ({e}); siga com o resto e rode de novo quando a cota voltar")
            continue
        (saida / "brutos" / f"{c}.json").write_text(json.dumps(bruto, ensure_ascii=False, indent=2), encoding="utf-8")
        novos = converter(cad, c, bruto)
        achados += novos
        print(f"  {c}: {len(novos)} achados em {(time.time() - inicio) / 60:.1f} min")
    arq_para_id = {v["arquivo"]: k for k, v in cad["fontes"].items()}
    (saida / "obrigacoes").mkdir(exist_ok=True)
    for rel in args.obrigacoes:
        try:
            bruto = consultar(cad, P["G4"], [arq_para_id[rel]])
        except SemResposta as e:
            falharam.append(f"G4 {Path(rel).stem}")
            print(f"  G4 {Path(rel).stem}: SEM RESPOSTA ({e})")
            continue
        nome = Path(rel).stem
        (saida / "brutos" / f"G4_{nome}.json").write_text(json.dumps(bruto, ensure_ascii=False, indent=2), encoding="utf-8")
        itens = blocos(bruto.get("answer", ""), "OBRIGACAO")
        texto = (pacote / rel).read_text(encoding="utf-8")
        linhas = [f"# Obrigações — {nome}", "", "| dispositivo | transcrição | literal na fonte |", "|---|---|---|"]
        for i in itens:
            tr = limpar(i.get("transcricao", ""))
            linhas.append(f"| {limpar(i.get('dispositivo', ''))} | {tr.replace('|', '/')} | "
                          f"{'sim' if CR.existe(tr, texto) else 'NÃO'} |")
        (saida / "obrigacoes" / f"{nome}.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
        print(f"  G4 {nome}: {len(itens)} obrigações")
    dados = {"revisor": "gemini", "caderno": cad["notebook_id"],
             "data": datetime.now().isoformat(timespec="minutes"), "achados": achados, "falharam": falharam}
    CR.conferir_achados(pacote, dados)
    provar(cad, pacote, achados, P, saida)
    CR.conferir_achados(pacote, dados)
    (saida / "achados.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(achados)} achados em {saida / 'achados.json'}"
          + (f"; sem resposta: {', '.join(falharam)}" if falharam else ""))


def treplica(cad: dict, pacote: Path, anterior: Path, saida: Path, P: dict):
    achados = json.loads((anterior / "gemini" / "achados.json").read_text(encoding="utf-8"))["achados"]
    vered = anterior / "gemini" / "veredito.json"
    if vered.exists():
        v = json.loads(vered.read_text(encoding="utf-8"))
        abertos = {x["id"] for x in v["vereditos"] if x["veredito"] in ("nao_resolvido", "contestacao_nao_procede")}
        achados = [a for a in achados if a["id"] in abertos]
    resp = {r["id"]: r for r in json.loads((anterior / "resposta.json").read_text(encoding="utf-8"))["respostas"]}
    achados = [a for a in achados if a["id"] in resp]
    if not achados:
        print("nada em discussao: a treplica nao roda")
        return
    texto = "\n\n".join(
        f"ACHADO {a['id']} ({a['classe']}): {a['por_que']}\nTrecho do documento anterior: \"{a['trecho_documento']}\"\n"
        f"RESPOSTA ({resp[a['id']]['status']}): {resp[a['id']]['nota']}"
        + (f"\nFonte citada pelo proponente: {resp[a['id']]['fonte_arquivo']}: \"{resp[a['id']]['trecho_fonte']}\""
           if resp[a["id"]].get("trecho_fonte") else "")
        for a in achados)
    bruto = consultar(cad, P["G8"].replace("{achados_e_respostas}", texto))
    (saida / "brutos" / "G8.json").write_text(json.dumps(bruto, ensure_ascii=False, indent=2), encoding="utf-8")
    vereditos = [{"id": limpar(b.get("id", "")), "veredito": limpar(b.get("veredito", "")),
                  "trecho": limpar(b.get("trecho", "")) or None, "por_que": limpar(b.get("por_que", ""))}
                 for b in blocos(bruto.get("answer", ""), "VEREDITO")]
    (saida / "veredito.json").write_text(json.dumps({"vereditos": vereditos, "achados": []},
                                                    ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(vereditos)} vereditos em {saida / 'veredito.json'}")


if __name__ == "__main__":
    main()
