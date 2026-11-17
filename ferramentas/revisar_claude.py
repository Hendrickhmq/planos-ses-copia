#!/usr/bin/env python3
"""
revisar_claude.py - prepara e junta a revisao do Claude cego, o revisor padrao.

Uso:
    python3 revisar_claude.py preparar <rodada>/pacote --pasta <pasta cega> [--faturamento]
    python3 revisar_claude.py juntar <pasta cega> --saida <rodada>/claude
    python3 revisar_claude.py preparar <rodada>/pacote --pasta <pasta cega> --treplica <rodada anterior>
    python3 revisar_claude.py juntar <pasta cega> --saida <rodada>/claude --treplica

O metodo e metodo/revisao/claude.md; as perguntas, metodo/revisao/perguntas.md. Este
script nao chama modelo nenhum: quem abre os subagentes e a conversa (comando /revisao),
com o texto que o `preparar` imprime.

  preparar  monta, na pasta cega (fora do repositorio), uma subpasta por revisor:
            contas (A1, A2, A7, A4) e leitura (G1, G2 com --faturamento, G3, G5, G9, G7).
            Cada uma leva o pacote sem o manifesto.json (que diz a origem de cada
            arquivo), perguntas.md com a instrucao comum e as perguntas, esquema.json e
            saida/. A leitura vai sem os planos aprovados. Na treplica, cada subpasta leva
            o documento novo, mudancas.diff, rodada_anterior/ (os achados em discussao e
            a resposta) e a pergunta A5.
  juntar    le saida/*.json das subpastas e grava achados.json (ou veredito.json na
            treplica) com os ids CLC-<pergunta>-NN e CLL-<pergunta>-NN.
"""
from __future__ import annotations
import argparse, difflib, json, re, shutil
from datetime import datetime
from pathlib import Path

from comum import saida_utf8

RAIZ = Path(__file__).resolve().parent.parent
REVISAO = RAIZ / "metodo" / "revisao"
GRUPOS = {"contas": ("CLC", ["A1", "A2", "A7", "A4"]),
          "leitura": ("CLL", ["G1", "G2", "G3", "G5", "G9", "G7"])}
EM_DISCUSSAO = {"nao_resolvido", "contestacao_nao_procede"}


def blocos(arquivo: Path) -> dict[str, str]:
    txt = arquivo.read_text(encoding="utf-8")
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"```prompt (\S+)\n(.*?)```", txt, re.S)}


def copiar_pacote(origem: Path, destino: Path, sem_aprovados: bool):
    def ignorar(pasta, nomes):
        fora = {"manifesto.json"}
        if sem_aprovados and Path(pasta).name == "fontes":
            fora.add("aprovados")
        return [n for n in nomes if n in fora]
    shutil.copytree(origem, destino, ignore=ignorar)


def texto_subagente(pasta: Path, lista: list[str]) -> str:
    modelo = blocos(REVISAO / "claude.md")["subagente"]
    return (modelo.replace("{pasta}", str(pasta)).replace("{perguntas}", "perguntas.md")
            .replace("{lista}", ", ".join(lista)))


def escrever_perguntas(destino: Path, lista: list[str]):
    P = blocos(REVISAO / "perguntas.md")
    partes = ["# Instrução comum\n\n" + P["comum"]] + [f"# Pergunta {q}\n\n" + P[q] for q in lista]
    (destino / "perguntas.md").write_text("\n\n".join(partes) + "\n", encoding="utf-8")


def em_discussao(anterior: Path, sigla: str) -> list[dict]:
    achados = [a for a in json.loads((anterior / "claude" / "achados.json").read_text(encoding="utf-8"))["achados"]
               if a["id"].startswith(sigla + "-")]
    vered = anterior / "claude" / "veredito.json"
    if vered.exists():
        v = json.loads(vered.read_text(encoding="utf-8"))
        abertos = {x["id"] for x in v.get("vereditos", []) if x["veredito"] in EM_DISCUSSAO}
        achados = [a for a in achados if a["id"] in abertos] + [
            a for a in v.get("achados", []) if a["id"].startswith(sigla + "-")]
    return achados


def preparar(pacote: Path, pasta: Path, faturamento: bool, treplica: Path | None) -> list[tuple[str, str]]:
    if pasta.exists() and any(pasta.iterdir()):
        raise SystemExit(f"a pasta cega ja existe e nao esta vazia: {pasta}")
    if RAIZ in pasta.resolve().parents:
        raise SystemExit("a pasta cega tem de ficar fora do repositorio (no scratchpad)")
    textos = []
    for grupo, (sigla, lista) in GRUPOS.items():
        destino = pasta / grupo
        destino.mkdir(parents=True)
        copiar_pacote(pacote, destino / "pacote", sem_aprovados=(grupo == "leitura"))
        (destino / "saida").mkdir()
        if treplica:
            achados = em_discussao(treplica, sigla)
            if not achados:
                shutil.rmtree(destino)
                continue
            ids = {a["id"] for a in achados}
            resp = json.loads((treplica / "resposta.json").read_text(encoding="utf-8"))
            resp["respostas"] = [r for r in resp["respostas"] if r["id"] in ids]
            ant = destino / "pacote" / "rodada_anterior"
            ant.mkdir()
            (ant / "achados.json").write_text(json.dumps({"achados": achados}, ensure_ascii=False, indent=2), encoding="utf-8")
            (ant / "resposta.json").write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")
            antes = (treplica / "pacote" / "documento.md").read_text(encoding="utf-8").splitlines(keepends=True)
            depois = (pacote / "documento.md").read_text(encoding="utf-8").splitlines(keepends=True)
            (destino / "pacote" / "mudancas.diff").write_text("".join(difflib.unified_diff(
                antes, depois, "documento_anterior.md", "documento.md")), encoding="utf-8")
            lista = ["A5"]
            shutil.copy(REVISAO / "esquemas" / "veredito.json", destino / "esquema.json")
        else:
            if grupo == "leitura" and not faturamento:
                lista = [q for q in lista if q != "G2"]
            shutil.copy(REVISAO / "esquemas" / "achados.json", destino / "esquema.json")
        escrever_perguntas(destino, lista)
        textos.append((grupo, texto_subagente(destino, lista)))
    return textos


def juntar(pasta: Path, saida: Path, treplica: bool) -> dict:
    saida.mkdir(parents=True, exist_ok=True)
    tudo = {"revisor": "claude_cego", "data": datetime.now().isoformat(timespec="minutes"),
            "achados": [], "listas_vazias": {}, "falta_fonte": {}, "faltam": []}
    if treplica:
        tudo["vereditos"] = []
    for grupo, (sigla, _) in GRUPOS.items():
        destino = pasta / grupo
        if not destino.exists():
            continue
        lista = re.findall(r"^# Pergunta (\S+)", (destino / "perguntas.md").read_text(encoding="utf-8"), re.M)
        for q in lista:
            arq = destino / "saida" / f"{q}.json"
            if not arq.exists():
                tudo["faltam"].append(f"{grupo}/{q}")
                continue
            d = json.loads(arq.read_text(encoding="utf-8"))
            novos = d.get("achados_novos" if treplica else "achados", [])
            for n, a in enumerate(novos, 1):
                tudo["achados"].append({"id": f"{sigla}-{q}-{n:02d}", "revisor": "claude_cego",
                                        "grupo": grupo, "passada": q, **a})
            if treplica:
                tudo["vereditos"] += d.get("vereditos", [])
            tudo["listas_vazias"][f"{grupo}/{q}"] = d.get("listas_vazias", [])
            tudo["falta_fonte"][f"{grupo}/{q}"] = d.get("falta_fonte", [])
    nome = "veredito.json" if treplica else "achados.json"
    (saida / nome).write_text(json.dumps(tudo, ensure_ascii=False, indent=2), encoding="utf-8")
    return tudo


def main():
    saida_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="acao", required=True)
    p = sub.add_parser("preparar")
    p.add_argument("pacote")
    p.add_argument("--pasta", required=True)
    p.add_argument("--faturamento", action="store_true")
    p.add_argument("--treplica")
    j = sub.add_parser("juntar")
    j.add_argument("pasta")
    j.add_argument("--saida", required=True)
    j.add_argument("--treplica", action="store_true")
    args = ap.parse_args()
    if args.acao == "preparar":
        textos = preparar(Path(args.pacote).resolve(), Path(args.pasta).resolve(), args.faturamento,
                          Path(args.treplica).resolve() if args.treplica else None)
        for grupo, texto in textos:
            print(f"===== subagente: {grupo} =====\n{texto}\n")
        if not textos:
            print("nada em discussao: a treplica nao roda")
    else:
        tudo = juntar(Path(args.pasta).resolve(), Path(args.saida).resolve(), args.treplica)
        print(f"{len(tudo['achados'])} achados" + (f", {len(tudo['vereditos'])} vereditos" if args.treplica else "")
              + (f"; faltam: {', '.join(tudo['faltam'])}" if tudo["faltam"] else ""))


if __name__ == "__main__":
    main()
