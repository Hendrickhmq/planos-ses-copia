#!/usr/bin/env python3
"""
testar_tudo.py - todas as conferencias do projeto, numa chamada.

Uso:
    python testar_tudo.py                 suites, planos e registros (~5 s)
    python testar_tudo.py --mutacoes      mais o arnes de mutacao dos planos (~30 s)

Roda, nesta ordem, e para no fim com um quadro do que passou:

  1. as suites de teste (testar_*.py, e a do kit do Mapa Social no node), cada uma no seu processo;
  2. a conferencia de cada plano redigido que segue o contrato do estado.yaml,
     secao 11 - o redacao_02 e anterior ao contrato e fica de fora, dizendo;
  3. a conferencia numerica da extracao tratada (conferir.py sobre
     normalizados/, sem OCR);
  4. os registros contra o schema (verificar_registros.py, so erros), e o
     criterios.md em dia com registros/licoes.csv (consultar.py criterios --conferir);
  5. com --mutacoes, o testar_conferencia_plano.py em cada plano: injeta um erro
     conhecido por vez e exige que a verificacao certa o apanhe.

Codigo de saida 1 se qualquer passo falhar. E o que a integracao continua do
GitHub roda a cada envio (.github/workflows/testes.yml).
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from comum import CASOS, NORMALIZADOS, PLANOS, PLANOS_APROVADOS, RAIZ

AQUI = Path(__file__).resolve().parent     # os scripts rodam daqui

SUITES = ["testar_conferencia.py", "testar_conferir.py", "testar_conferir_plano.py",
          "testar_tratar.py", "testar_registros.py", "testar_devolutiva.py",
          "testar_consultar.py", "testar_extrair_html.py", "testar_conferir_coleta.py",
          "testar_conferir_ficha.py", "testar_padrao.py",
          "testar_ler_dou.py", "testar_atualidade.py", "testar_conferir_precos.py", "testar_conferir_dossie.py", "testar_ler_controle.py",
          "testar_revisao.py", "testar_motor_js.mjs", "testar_ler_motor.py", "testar_montar_coleta.py",
          "testar_curso.py"]


def planos_com_contrato():
    """planos/redacao_NN/ e ferramentas/casos/caso_teste_*/ com plano.md e as chaves
    que o conferir_plano.py exige. Devolve os caminhos relativos a raiz."""
    planos, fora = [], []
    for d in sorted(PLANOS.glob("redacao_*")) + sorted(CASOS.glob("caso_teste_*")):
        estado = d / "estado.yaml"
        if not (d / "plano.md").exists() or not estado.exists():
            continue
        texto = estado.read_text(encoding="utf-8")
        if re.search(r"^\s+origem_recurso:", texto, re.M) and \
                re.search(r"^\s+valor_unitario:", texto, re.M):
            planos.append(d.relative_to(RAIZ).as_posix())
        else:
            fora.append(d.relative_to(RAIZ).as_posix())
    return planos, fora


def pre_planos():
    """os pre-planos: planos/redacao_NN/plano_v*.md. A pasta do projeto pode ter o
    plano.md ao lado (metodo/pre_plano/procedimento.md, "Um projeto, uma pasta").
    Devolve os caminhos relativos a raiz."""
    docs = []
    for d in sorted(PLANOS.glob("redacao_*")):
        if not (d / "estado.yaml").exists():
            continue
        docs += [f.relative_to(RAIZ).as_posix() for f in sorted(d.glob("plano_v*.md"))]
    return docs


# fontes de plano encerrado anteriores ao metodo da coleta: ficam fora, com o motivo
ANTERIORES_AO_METODO = {
    "planos/redacao_03/dados/fontes/sigtap_0901010073_082026.md":
        "ficha de 31/08/2026, anterior a metodo/coleta/ficha_sigtap.md",
}


def fontes_dos_planos():
    """(conferencia, arquivo) de cada ficha, coleta, pesquisa de precos e dossie dos planos"""
    out = []
    for d in sorted(PLANOS.glob("redacao_*")):
        for f in sorted((d / "dados" / "fontes").glob("sigtap_*.md")):
            out.append(("conferir_ficha.py", f))
        for f in sorted((d / "dados" / "fontes").glob("mapa_social_*.md")):
            out.append(("conferir_coleta.py", f))
        if (d / "dados" / "precos.md").exists():
            out.append(("conferir_precos.py", d / "dados" / "precos.md"))
        if (d / "dossie").is_dir():
            out.append(("conferir_dossie.py", d / "dossie"))
    return [(c, f.relative_to(RAIZ).as_posix()) for c, f in out]


def rodar(rotulo, argumentos):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    inicio = time.time()
    # o kit do motor do Mapa Social e JavaScript: a suite dele roda no node
    cmd = ["node", "--test"] + argumentos if argumentos[0].endswith(".mjs") else [sys.executable] + argumentos
    r = subprocess.run(cmd, cwd=AQUI, env=env,
                       capture_output=True, encoding="utf-8", errors="replace")
    segundos = time.time() - inicio
    ok = r.returncode == 0
    print(f"  {'ok   ' if ok else 'FALHA'}  {rotulo:<52} {segundos:5.1f} s", flush=True)
    if not ok:
        saida = (r.stdout + r.stderr).strip().splitlines()
        for linha in saida[-25:]:
            print(f"         | {linha}")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mutacoes", action="store_true",
                    help="roda tambem o arnes de mutacao dos planos (lento)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    resultados = []
    print("\nSuites")
    for suite in SUITES:
        resultados.append(rodar(suite, [suite]))

    planos, fora = planos_com_contrato()
    print("\nPlanos redigidos (conferir_plano.py)")
    for plano in planos:
        resultados.append(rodar(f"conferir_plano.py {plano}/",
                                ["conferir_plano.py", str(RAIZ / plano) + "/"]))
    for plano in fora:
        print(f"  -      {plano}/ anterior ao contrato do estado.yaml (metodo/plano/procedimento.md)")

    pps = pre_planos()
    print("\nPre-planos (conferir_pre_plano.py)")
    for doc in pps:
        resultados.append(rodar(f"conferir_pre_plano.py {doc}",
                                ["conferir_pre_plano.py", str(RAIZ / doc)]))

    print("\nFontes dos planos (ficha, coleta, precos, dossie)")
    for conferencia, arq in fontes_dos_planos():
        if arq in ANTERIORES_AO_METODO:
            print(f"  -      {arq}: {ANTERIORES_AO_METODO[arq]}")
            continue
        resultados.append(rodar(f"{conferencia} {arq}", [conferencia, str(RAIZ / arq)]))

    print("\nExtracao tratada e registros")
    resultados.append(rodar("conferir.py normalizados/ --sem-ocr",
                            ["conferir.py", str(NORMALIZADOS) + "/", str(PLANOS_APROVADOS) + "/",
                             "--sem-ocr"]))
    resultados.append(rodar("verificar_registros.py --erros",
                            ["verificar_registros.py", "--erros"]))
    resultados.append(rodar("consultar.py criterios --conferir",
                            ["consultar.py", "criterios", "--conferir"]))

    if args.mutacoes:
        print("\nMutacoes (testar_conferencia_plano.py)")
        for plano in planos:
            resultados.append(rodar(f"testar_conferencia_plano.py {plano}/",
                                    ["testar_conferencia_plano.py", str(RAIZ / plano) + "/"]))
        for doc in pps:
            resultados.append(rodar(f"testar_conferencia_pre_plano.py {doc}",
                                    ["testar_conferencia_pre_plano.py", str(RAIZ / doc)]))

    falhas = resultados.count(False)
    print(f"\n{len(resultados) - falhas}/{len(resultados)} passaram"
          + ("" if args.mutacoes else "  (sem as mutacoes - use --mutacoes)"))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
