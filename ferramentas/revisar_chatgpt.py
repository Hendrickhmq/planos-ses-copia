#!/usr/bin/env python3
"""
revisar_chatgpt.py - roda o revisor do ChatGPT (o Sol, por padrao) sobre um pacote cego.

Uso:
    python3 revisar_chatgpt.py <pacote> --saida <rodada>/chatgpt [--passadas A1,A2,A4] [--modelo gpt-6.1-sol]
    python3 revisar_chatgpt.py <pacote> --saida <rodada>/chatgpt --treplica <rodada anterior>

O metodo e metodo/revisao/chatgpt.md, e as perguntas sao os blocos ```prompt``` de
metodo/revisao/perguntas.md: este script nao guarda pergunta. Cada passada e uma execucao do Codex, em paralelo:
modo nao interativo, sandbox somente leitura, sessao efemera, sem a configuracao do
usuario, sem memoria, plugins, apps e skills, e resposta no esquema de
metodo/revisao/esquemas/.

Na treplica (rodadas 2 e 3), <pacote> e o pacote da versao nova. A <rodada anterior>
traz chatgpt/achados.json (ou o veredito anterior), o documento anterior e resposta.json.
Entram so os achados ainda em discussao.

Saida: <passada>.json e <passada>.log por passada, e achados.json (ou veredito.json)
juntos, com os ids GPT-<passada>-NN.
"""
from __future__ import annotations
import argparse, difflib, json, os, re, shutil, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from comum import saida_utf8

RAIZ = Path(__file__).resolve().parent.parent
METODO = RAIZ / "metodo" / "revisao" / "perguntas.md"
ESQUEMAS = RAIZ / "metodo" / "revisao" / "esquemas"
APP = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
EM_DISCUSSAO = {"nao_resolvido", "contestacao_nao_procede"}


def codex() -> str:
    for c in (os.environ.get("CODEX_BIN"), shutil.which("codex"), APP):
        if c and Path(c).exists():
            return c
    raise SystemExit("Codex nao encontrado: instale o app do ChatGPT ou defina CODEX_BIN")


def prompts(caminho: Path = METODO) -> dict[str, str]:
    """Os blocos ```prompt NOME ... ``` do metodo."""
    txt = caminho.read_text(encoding="utf-8")
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"```prompt (\S+)\n(.*?)```", txt, re.S)}


def comando(pasta: Path, esquema: Path, saida: Path, modelo: str, esforco: str) -> list[str]:
    return [codex(), "exec", "-m", modelo, "-c", f'model_reasoning_effort="{esforco}"',
            "-c", 'web_search="disabled"',
            "--ephemeral", "--ignore-user-config", "--skip-git-repo-check", "-s", "read-only",
            "--disable", "apps", "--disable", "plugins", "--disable", "skill_search",
            "--disable", "memories", "-C", str(pasta), "--output-schema", str(esquema),
            "-o", str(saida), "-"]


def rodar(passada: str, texto: str, pasta: Path, esquema: Path, saida: Path, modelo: str, esforco: str):
    alvo = saida / f"{passada}.json"
    inicio = datetime.now()
    with open(saida / f"{passada}.log", "w", encoding="utf-8") as log:
        r = subprocess.run(comando(pasta, esquema, alvo, modelo, esforco), input=texto, text=True,
                           stdout=log, stderr=subprocess.STDOUT)
    minutos = (datetime.now() - inicio).total_seconds() / 60
    ok = r.returncode == 0 and alvo.exists()
    print(f"  {passada}: {'ok' if ok else 'FALHOU (codigo %d)' % r.returncode} em {minutos:.1f} min")
    return passada, ok


def juntar_achados(saida: Path, passadas: list[str], modelo: str, esforco: str, chave: str = "achados"):
    tudo = {"revisor": "chatgpt", "modelo": modelo, "esforco": esforco,
            "data": datetime.now().isoformat(timespec="minutes"),
            "achados": [], "listas_vazias": {}, "falta_fonte": {}, "falharam": []}
    for p in passadas:
        arq = saida / f"{p}.json"
        if not arq.exists():
            tudo["falharam"].append(p)
            continue
        d = json.loads(arq.read_text(encoding="utf-8"))
        for n, a in enumerate(d.get(chave, []), 1):
            a = {"id": f"GPT-{p}-{n:02d}", "revisor": "chatgpt", "modelo": modelo, "passada": p, **a}
            tudo["achados"].append(a)
        tudo["listas_vazias"][p] = d.get("listas_vazias", [])
        tudo["falta_fonte"][p] = d.get("falta_fonte", [])
        if "vereditos" in d:
            tudo["vereditos"] = d["vereditos"]
    return tudo


def em_discussao(anterior: Path) -> list[dict]:
    """Os achados do ChatGPT que ainda estao em discussao na rodada anterior."""
    achados = json.loads((anterior / "chatgpt" / "achados.json").read_text(encoding="utf-8"))["achados"]
    vered = anterior / "chatgpt" / "veredito.json"
    if vered.exists():
        v = json.loads(vered.read_text(encoding="utf-8"))
        abertos = {x["id"] for x in v.get("vereditos", []) if x["veredito"] in EM_DISCUSSAO}
        achados = [a for a in achados if a["id"] in abertos] + v.get("achados", [])
    return achados


def pasta_treplica(pacote: Path, anterior: Path, destino: Path) -> int:
    shutil.copytree(pacote, destino, dirs_exist_ok=True)
    antes = (anterior / "pacote" / "documento.md").read_text(encoding="utf-8").splitlines(keepends=True)
    depois = (pacote / "documento.md").read_text(encoding="utf-8").splitlines(keepends=True)
    (destino / "mudancas.diff").write_text("".join(difflib.unified_diff(
        antes, depois, "documento_anterior.md", "documento.md")), encoding="utf-8")
    achados = em_discussao(anterior)
    ids = {a["id"] for a in achados}
    resposta = json.loads((anterior / "resposta.json").read_text(encoding="utf-8"))
    resposta["respostas"] = [r for r in resposta["respostas"] if r["id"] in ids]
    (destino / "rodada_anterior").mkdir(exist_ok=True)
    (destino / "rodada_anterior" / "achados.json").write_text(
        json.dumps({"achados": achados}, ensure_ascii=False, indent=2), encoding="utf-8")
    (destino / "rodada_anterior" / "resposta.json").write_text(
        json.dumps(resposta, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(achados)


def main():
    saida_utf8()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pacote")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--passadas", default="A1,A2,A4")
    ap.add_argument("--treplica", help="a pasta da rodada anterior")
    ap.add_argument("--modelo", default="gpt-6.1-sol")
    ap.add_argument("--esforco", default="high")
    args = ap.parse_args()
    pacote, saida = Path(args.pacote).resolve(), Path(args.saida).resolve()
    saida.mkdir(parents=True, exist_ok=True)
    P = prompts()
    if args.treplica:
        with tempfile.TemporaryDirectory(prefix="treplica_") as tmp:
            n = pasta_treplica(pacote, Path(args.treplica).resolve(), Path(tmp))
            if not n:
                print("nada em discussao: a treplica nao roda")
                return
            print(f"treplica: {n} achados em discussao")
            rodar("A5", P["comum"] + "\n\n" + P["A5"], Path(tmp), ESQUEMAS / "veredito.json",
                  saida, args.modelo, args.esforco)
        d = json.loads((saida / "A5.json").read_text(encoding="utf-8"))
        for n_, a in enumerate(d.get("achados_novos", []), 1):
            a.update({"id": f"GPT-A5-{n_:02d}", "revisor": "chatgpt", "passada": "A5"})
        d["achados"] = d.pop("achados_novos", [])
        (saida / "veredito.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"veredito em {saida / 'veredito.json'}")
        return
    passadas = [p.strip() for p in args.passadas.split(",") if p.strip()]
    print(f"ChatGPT ({args.modelo}, esforco {args.esforco}) sobre {pacote}: {', '.join(passadas)}")
    with ThreadPoolExecutor(max_workers=len(passadas)) as ex:
        list(ex.map(lambda p: rodar(p, P["comum"] + "\n\n" + P[p], pacote, ESQUEMAS / "achados.json",
                                    saida, args.modelo, args.esforco), passadas))
    tudo = juntar_achados(saida, passadas, args.modelo, args.esforco)
    (saida / "achados.json").write_text(json.dumps(tudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(tudo['achados'])} achados em {saida / 'achados.json'}"
          + (f"; falharam: {', '.join(tudo['falharam'])}" if tudo["falharam"] else ""))


if __name__ == "__main__":
    main()
