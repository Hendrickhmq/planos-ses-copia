#!/usr/bin/env python3
"""
ler_motor.py - le a saida do kit do motor do Mapa Social e grava o JSON do motor.

Uso:
    python3 ferramentas/ler_motor.py planos/redacao_NN/dados/fontes/mapa_social_AAAAMMDD_bruto/

O metodo e metodo/coleta/mapa_social.md ("A saida do navegador"). Le as partes que sairam do
navegador (motor_parte_N.txt, pela area de transferencia ou pela transcricao) e:
  - confere o tamanho e o hash djb2 de cada parte e do texto inteiro;
  - restaura o {U+XXXX} (o espaco nao separavel e todo caractere fora do ASCII);
  - confere a assinatura do kit contra ferramentas/mapa_social/motor.js (pelo node);
  - confere o hash da ordem contra a ordem.json da pasta;
  - procura CPF e CNS;
  - converte as datas seriais e a recarga para o horario de Brasilia;
e grava motor_<AAAAMMDD>.json. Nenhum numero passa do navegador ao disco sem o hash.

Codigo 1 se algo nao bater, com o motivo.
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from comum import saida_utf8

AQUI = Path(__file__).resolve().parent
KIT = AQUI / "mapa_social" / "motor.js"
CABECALHO = re.compile(r"^#ms-parte (\d+)/(\d+) tamanho=(\d+) hash=(\d+) total=(\d+) total_hash=(\d+)$")
CPF = re.compile(r"(?<![\d.])\d{3}\.\d{3}\.\d{3}-\d{2}(?![\d])")
CNS = re.compile(r"(?<![\d.,])[12789]\d{14}(?![\d])")


class ErroMotor(Exception):
    pass


def djb2(s: str) -> int:
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return h


def ascii_kit(s: str) -> str:
    """o mesmo escape do kit (K.ascii): fora do ASCII visivel, e a chave, vira {U+XXXX}"""
    out = []
    for ch in s:
        cp = ord(ch)
        if cp > 0xFFFF:                 # o JS conta em unidades de 16 bits
            cp -= 0x10000
            out.append("{U+%04X}{U+%04X}" % (0xD800 + (cp >> 10), 0xDC00 + (cp & 0x3FF)))
        elif ch == "{" or not 0x20 <= cp <= 0x7E:
            out.append("{U+%04X}" % cp)
        else:
            out.append(ch)
    return "".join(out)


def desfazer(s: str) -> str:
    t = re.sub(r"\{U\+([0-9A-F]{4})\}", lambda m: chr(int(m.group(1), 16)), s)
    return t.encode("utf-16", "surrogatepass").decode("utf-16")


def canonico(ordem) -> str:
    """a ordem como o kit a ve: JSON.stringify, sem espacos, na ordem das chaves"""
    return json.dumps(ordem, ensure_ascii=False, separators=(",", ":"))


def hash_ordem(ordem) -> int:
    return djb2(ascii_kit(canonico(ordem)))


_ASSINATURA = None


def assinatura_kit() -> int:
    """a assinatura do motor.js do repositorio, calculada pelo node como o navegador calcula"""
    global _ASSINATURA
    if _ASSINATURA is None:
        node = shutil.which("node")
        if not node:
            raise ErroMotor("sem o node: a assinatura do kit nao se confere (instale o node)")
        r = subprocess.run([node, str(KIT), "--assinatura"], capture_output=True, text=True)
        if r.returncode:
            raise ErroMotor(f"o node nao leu o kit: {r.stderr.strip()}")
        _ASSINATURA = int(r.stdout.strip())
    return _ASSINATURA


def ler_partes(bruto: Path) -> str:
    """o texto inteiro do motor, conferido parte a parte; ainda com o {U+XXXX}"""
    arqs = sorted(bruto.glob("motor_parte_*.txt"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    if not arqs:
        raise ErroMotor(f"{bruto.name}/ sem as partes (motor_parte_N.txt)")
    pedacos, n_total, total = {}, None, None
    for arq in arqs:
        texto = arq.read_text(encoding="utf-8")
        cab, _, corpo = texto.partition("\n")
        m = CABECALHO.match(cab.strip())
        if not m:
            raise ErroMotor(f"{arq.name}: sem o cabecalho '#ms-parte N/T tamanho=... hash=...'")
        i, n, tam, h, tot, toth = (int(x) for x in m.groups())
        # a transcricao e o pbpaste podem deixar uma quebra de linha no fim
        if len(corpo) > tam and not corpo[tam:].strip():
            corpo = corpo[:tam]
        if len(corpo) != tam or djb2(corpo) != h:
            raise ErroMotor(f"{arq.name}: o texto nao bate com o hash do motor "
                            f"({len(corpo)} caracteres, hash {djb2(corpo)}; o motor disse {tam} e {h})")
        if n_total not in (None, n) or total not in (None, (tot, toth)):
            raise ErroMotor(f"{arq.name}: parte de outra saida (o total nao bate com o das outras partes)")
        n_total, total = n, (tot, toth)
        pedacos[i] = corpo
    faltam = [i for i in range(1, n_total + 1) if i not in pedacos]
    if faltam:
        raise ErroMotor(f"faltam as partes {faltam} de {n_total}")
    texto = "".join(pedacos[i] for i in range(1, n_total + 1))
    if (len(texto), djb2(texto)) != total:
        raise ErroMotor("o texto inteiro nao bate com o hash do motor")
    return texto


def serial_data(v):
    return (date(1899, 12, 30) + timedelta(days=int(v))).strftime("%d/%m/%Y") if isinstance(v, (int, float)) else v


def serial_hora(v):
    if not isinstance(v, (int, float)):
        return v
    d = datetime(1899, 12, 30) + timedelta(seconds=round(v * 86400))
    return d.strftime("%d/%m/%Y %H:%M:%S")


def converter(no, datas: set, horas: set):
    """as datas seriais do motor em DD/MM/AAAA, nas chaves e nas colunas das tabelas"""
    if isinstance(no, dict):
        if isinstance(no.get("cols"), list) and isinstance(no.get("linhas"), list):
            for j, col in enumerate(no["cols"]):
                if col in datas:
                    for linha in no["linhas"]:
                        if j < len(linha):
                            linha[j] = serial_data(linha[j])
        for k, v in no.items():
            if k in datas:
                no[k] = serial_data(v)
            elif k in horas:
                no[k] = serial_hora(v)
            else:
                converter(v, datas, horas)
    elif isinstance(no, list):
        for v in no:
            converter(v, datas, horas)


def brasilia(utc: str) -> str:
    d = datetime.strptime(utc.replace("Z", "+0000"), "%Y-%m-%dT%H:%M:%S.%f%z")
    return (d.astimezone(timezone(timedelta(hours=-3)))).strftime("%d/%m/%Y %H:%M:%S")


def data_da_pasta(bruto: Path) -> str:
    m = re.search(r"mapa_social_(\d{8})", bruto.name)
    if not m:
        raise ErroMotor(f"{bruto.name}: o nome da pasta nao traz a data (mapa_social_AAAAMMDD..._bruto)")
    return m.group(1)


def ler(bruto: Path, conferir_kit: bool = True) -> dict:
    """o JSON do motor a partir das partes, conferido"""
    bruto = Path(bruto)
    texto = ler_partes(bruto)
    for nome, pad in (("CPF", CPF), ("CNS", CNS)):
        if pad.search(texto):
            raise ErroMotor(f"possivel {nome} na saida do motor: a coleta nao pode seguir")
    try:
        motor = json.loads(desfazer(texto))
    except ValueError as e:
        raise ErroMotor(f"a saida do motor nao e JSON: {e}")
    ordem_arq = bruto / "ordem.json"
    if not ordem_arq.exists():
        raise ErroMotor(f"{bruto.name}/ sem a ordem.json")
    ordem = json.loads(ordem_arq.read_text(encoding="utf-8"))
    if motor.get("ordem_hash") != hash_ordem(ordem):
        raise ErroMotor("o kit rodou outra ordem: o hash da ordem que ele recebeu nao e o da ordem.json "
                        f"({motor.get('ordem_hash')} contra {hash_ordem(ordem)})")
    if conferir_kit and (motor.get("kit") or {}).get("assinatura") != assinatura_kit():
        raise ErroMotor("o kit que rodou no painel nao e o ferramentas/mapa_social/motor.js do repositorio "
                        f"(assinatura {(motor.get('kit') or {}).get('assinatura')} contra {assinatura_kit()})")
    converter(motor, set(motor.get("campos_data") or []), set(motor.get("campos_hora") or []))
    for d in (motor.get("datas") or {}).values():
        if isinstance(d, dict) and d.get("recarga_utc"):
            d["recarga_brasilia"] = brasilia(d["recarga_utc"])
    motor["leitura"] = {"partes": len(list(bruto.glob("motor_parte_*.txt"))), "tamanho": len(texto), "hash": djb2(texto)}
    return motor


def gravar(bruto: Path) -> Path:
    bruto = Path(bruto)
    motor = ler(bruto)
    saida = bruto / f"motor_{data_da_pasta(bruto)}.json"
    saida.write_text(json.dumps(motor, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return saida


def main():
    ap = argparse.ArgumentParser(description="le as partes da saida do kit do motor e grava o JSON do motor")
    ap.add_argument("bruto", help="a pasta bruta da coleta, com a ordem.json e as partes")
    args = ap.parse_args()
    saida_utf8()
    try:
        saida = gravar(Path(args.bruto).resolve())
    except ErroMotor as e:
        print(f"FALHOU: {e}")
        return 1
    m = json.loads(saida.read_text(encoding="utf-8"))
    print(f"ok: {saida.name} — {m['leitura']['partes']} parte(s), {m['leitura']['tamanho']} caracteres, "
          f"hash {m['leitura']['hash']}, kit {m['kit']['versao']} conferido, recarga {m['datas']['inicio'].get('recarga_brasilia')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
