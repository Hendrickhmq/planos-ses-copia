"""Confere o que foi informado em cadastro.csv contra as bases públicas.

    python validar.py              todos os polos com CNPJ ou CNES preenchido
    python validar.py CIG          só as linhas cuja pasta contém "CIG"

Fontes, ambas abertas e sem login:
  CNPJ  Receita Federal, via brasilapi.com.br (e minhareceita.org, se a primeira falhar)
  CNES  Ministério da Saúde, via apidadosabertos.saude.gov.br
  Equipamentos, serviço 121 e licença sanitária: arquivos mensais do DATASUS (datasus.py)

Grava em cada polo:
  validacao.md              o que confere, o que diverge, o que falta ver à mão
  _consulta/cnpj.json       resposta bruta, para proveniência
  _consulta/cnes.json

Só biblioteca padrão. Não altera polo.md nem cadastro.csv.
"""
import csv
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import datasus

RAIZ = Path(__file__).resolve().parent
CADASTRO = RAIZ / "cadastro.csv"
URLS_CNPJ = ("https://brasilapi.com.br/api/cnpj/v1/{}", "https://minhareceita.org/{}")
URL_CNES = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/{}"
URL_TIPOS = "https://apidadosabertos.saude.gov.br/cnes/tipounidades"

# CNAE da subclasse 8640-2: o que a empresa declara à Receita que faz.
CNAE_MODALIDADE = {
    "TC": (8640204, "8640-2/04 serviços de tomografia"),
    "US": (8640207, "8640-2/07 diagnóstico por imagem sem radiação ionizante"),
}

OK, DIVERGE, ATENCAO, NAO_VISTO = "confere", "DIVERGE", "atenção", "não consultado"

# Códigos da tabela auxiliar do próprio DATASUS (TAB_CNES.zip, equipam2508.cnv e
# S_CLASSEN.dbf), tipo de equipamento 01 — diagnóstico por imagem.
EQUIPAMENTO = {
    "01": "Gama câmara", "02": "Mamógrafo com comando simples", "03": "Mamógrafo com estereotaxia",
    "04": "Raio X até 100 mA", "05": "Raio X de 100 a 500 mA", "06": "Raio X mais de 500 mA",
    "07": "Raio X odontológico", "08": "Raio X com fluoroscopia", "09": "Raio X para densitometria óssea",
    "10": "Raio X para hemodinâmica", "11": "Tomógrafo computadorizado", "12": "Ressonância magnética",
    "13": "Ultrassom doppler colorido", "14": "Ultrassom ecógrafo", "15": "Ultrassom convencional",
    "16": "Processadora de filme para mamografia", "17": "Mamógrafo digital", "18": "PET/CT",
    "19": "Mamógrafo com tomossíntese", "20": "Raio X analógico", "21": "Raio X digital",
    "22": "Raio X telecomandado", "23": "Raio X móvel", "24": "Arco cirúrgico", "25": "Raio X panorâmico",
    "26": "Tomógrafo computadorizado 4 canais", "27": "Tomógrafo computadorizado 16 canais",
    "28": "Tomógrafo computadorizado 32 canais", "29": "Tomógrafo computadorizado 64 canais",
    "30": "Tomógrafo computadorizado 128 canais", "31": "Tomógrafo simulador para radioterapia",
    "32": "Ressonância magnética 0,5 T", "33": "Ressonância magnética 1,5 T",
    "34": "Ressonância magnética 3 T", "35": "Ressonância magnética de campo aberto",
}
CLASSE_121 = {
    "001": "Radiologia", "002": "Ultrassonografia", "003": "Tomografia computadorizada",
    "004": "Ressonância magnética", "006": "Radiologia intervencionista",
    "007": "Radiologia por telemedicina", "008": "Ultrassonografia por telemedicina",
    "009": "Tomografia por telemedicina", "010": "Ressonância por telemedicina",
    "011": "Radiologia intervencionista por telemedicina", "012": "Mamografia",
    "013": "Mamografia por telemedicina",
}
# O que cada modalidade do plano precisa encontrar no CNES do polo.
IMAGEM = {
    "TC": {"nome": "tomografia", "equip": {"11", "26", "27", "28", "29", "30"}, "classe": "003"},
    "US": {"nome": "ultrassonografia", "equip": {"13", "14", "15"}, "classe": "002"},
}


def sim_nao(v):
    return "sim" if v == "1" else "não"


def conferir_imagem(cnes, mods, imagem, nota):
    """Equipamento, serviço 121 e habilitação do polo. Devolve as linhas do relatório."""
    if imagem.get("erro"):
        nota(NAO_VISTO, "Imagem no CNES", f"arquivos do DATASUS não baixaram ({imagem['erro']}); rodar de novo")
        return []
    chave = cnes.zfill(7)
    eq = [r for r in imagem["EQ"].get(chave, []) if r.get("TIPEQUIP") == "01"]
    sr = [r for r in imagem["SR"].get(chave, []) if r.get("SERV_ESP") == "121"]

    for m in mods:
        regra = IMAGEM[m]
        meus = [r for r in eq if r.get("CODEQUIP") in regra["equip"]]
        uso = sum(int(r.get("QT_USO") or 0) for r in meus)
        if not uso:
            nota(DIVERGE, f"Equipamento de {regra['nome']}", "nenhum em uso cadastrado no CNES")
        else:
            sus = any(r.get("IND_SUS") == "1" for r in meus)
            det = "; ".join(f"{r.get('QT_USO')} × {EQUIPAMENTO.get(r.get('CODEQUIP'), r.get('CODEQUIP'))}" for r in meus)
            nota(OK if sus else ATENCAO, f"Equipamento de {regra['nome']}",
                 f"{det} — {'disponível' if sus else 'NÃO marcado como disponível'} para o SUS")
        serv = [r for r in sr if r.get("CLASS_SR") == regra["classe"]]
        if not serv:
            nota(DIVERGE, f"Serviço 121/{regra['classe']} {regra['nome']}", "não cadastrado no CNES")
        else:
            sus = any(r.get("AMB_SUS") == "1" for r in serv)
            nota(OK if sus else ATENCAO, f"Serviço 121/{regra['classe']} {regra['nome']}",
                 f"cadastrado, ambulatorial {'SUS' if sus else 'só NÃO SUS — falta a marca SUS'}")

    L = ["", f"## Diagnóstico por imagem no CNES — competência {imagem['competencia']}", "",
         "Arquivos mensais do DATASUS. Mudança feita no CNES depois dessa competência ainda não aparece aqui.", "",
         "| equipamento | existentes | em uso | disponível SUS |", "|---|---|---|---|"]
    L += [f"| {EQUIPAMENTO.get(r.get('CODEQUIP'), 'código ' + r.get('CODEQUIP', '?'))} | {r.get('QT_EXIST')} | "
          f"{r.get('QT_USO')} | {sim_nao(r.get('IND_SUS'))} |" for r in sorted(eq, key=lambda r: r.get("CODEQUIP", ""))]
    if not eq:
        L.append("| nenhum equipamento de imagem cadastrado | | | |")
    L += ["", "| serviço 121 — classificação | ambulatorial SUS | ambulatorial não SUS | próprio ou terceirizado |",
          "|---|---|---|---|"]
    L += [f"| {r.get('CLASS_SR')} {CLASSE_121.get(r.get('CLASS_SR'), '')} | {sim_nao(r.get('AMB_SUS'))} | "
          f"{sim_nao(r.get('AMB_NSUS'))} | {'próprio' if r.get('CARACTER') == '1' else 'terceirizado'} |"
          for r in sorted(sr, key=lambda r: r.get("CLASS_SR", ""))]
    if not sr:
        L.append("| serviço 121 não cadastrado | | | |")
    est = imagem["ST"].get(chave, [{}])[0] if imagem["ST"].get(chave) else {}
    if est.get("ALVARA"):
        d = est.get("DT_EXPED", "")
        data = f"{d[6:8]}/{d[4:6]}/{d[:4]}" if len(d) == 8 else "sem data"
        orgao = {"1": "SES", "2": "SMS"}.get(est.get("ORGEXPED"), "órgão não informado")
        L += ["", f"Licença sanitária declarada no CNES: nº {est['ALVARA']}, expedida em {data} ({orgao}). "
                  "O CNES não traz a validade — conferir no documento."]
    return L


def digitos(s):
    return re.sub(r"\D", "", s or "")


def sem_acento(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"[^A-Z0-9 ]", " ", "".join(c for c in s if not unicodedata.combining(c)).upper())


def cnpj_valido(c):
    if len(c) != 14 or len(set(c)) == 1:
        return False
    for n in (12, 13):
        pesos = list(range(n - 7, 1, -1)) + list(range(9, 1, -1))
        resto = sum(int(d) * p for d, p in zip(c[:n], pesos)) % 11
        if int(c[n]) != (0 if resto < 2 else 11 - resto):
            return False
    return True


def fmt_cnpj(c):
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}" if len(c) == 14 else c


def baixar(url):
    """Devolve (dados, erro). Nunca levanta: rede fora do ar vira linha no relatório."""
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "validar-polos/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 - qualquer falha de rede é reportada, não fatal
        return None, type(e).__name__


def nomes_parecidos(a, b):
    """Metade das palavras significativas de um nome aparece no outro."""
    ruido = {"LTDA", "ME", "EPP", "SA", "DE", "DA", "DO", "E", "CLINICA", "CENTRO", "POLO"}
    pa = {p for p in sem_acento(a).split() if p not in ruido}
    pb = {p for p in sem_acento(b).split() if p not in ruido}
    if not pa or not pb:
        return None
    return len(pa & pb) >= max(1, min(len(pa), len(pb)) // 2)


def ler_cadastro():
    texto = CADASTRO.read_text(encoding="utf-8-sig")
    sep = ";" if texto.splitlines()[0].count(";") >= texto.splitlines()[0].count(",") else ","
    return list(csv.DictReader(texto.splitlines(), delimiter=sep))


def validar(linha, tipos, imagem):
    pasta = RAIZ / linha["pasta"].strip()
    cnpj, cnes = digitos(linha.get("cnpj")), digitos(linha.get("cnes"))
    cep_inf = digitos(linha.get("cep"))
    nome_inf = (linha.get("nome_informado") or "").strip()
    mods = [m for m in re.split(r"[ ,/e]+", (linha.get("modalidades") or "").upper()) if m in CNAE_MODALIDADE]
    achados = []  # (resultado, item, detalhe)
    rf = ms = None
    secao_imagem = []

    def nota(res, item, det=""):
        achados.append((res, item, det))

    # --- Receita Federal ---
    if not cnpj:
        nota(NAO_VISTO, "CNPJ", "não informado no cadastro.csv")
    elif not cnpj_valido(cnpj):
        nota(DIVERGE, "CNPJ", f"{fmt_cnpj(cnpj)} tem dígito verificador inválido — erro de digitação")
    else:
        # Duas cópias da mesma base da Receita, com os mesmos campos: uma falha, tenta a outra.
        for url in URLS_CNPJ:
            rf, erro = baixar(url.format(cnpj))
            if rf and rf.get("razao_social"):
                break
            rf = None
        if not rf:
            nota(ATENCAO if erro == "HTTP 404" else NAO_VISTO, "CNPJ na Receita",
                 "não encontrado em nenhuma das duas cópias da base — conferir no site da Receita"
                 if erro == "HTTP 404" else f"consulta falhou ({erro}); rodar de novo")
    if rf:
        sit = rf.get("descricao_situacao_cadastral", "")
        nota(OK if sit == "ATIVA" else DIVERGE, "Situação cadastral", f"{sit} desde {rf.get('data_situacao_cadastral')}")
        nome_rf = f"{rf.get('razao_social')} / {rf.get('nome_fantasia') or 'sem fantasia'}"
        if nome_inf:
            p = nomes_parecidos(nome_inf, nome_rf)
            nota(OK if p else ATENCAO, "Nome × Receita", f"informado \"{nome_inf}\"; Receita: {nome_rf}")
        if cep_inf:
            igual = cep_inf == digitos(rf.get("cep"))
            nota(OK if igual else DIVERGE, "CEP × Receita", f"informado {cep_inf}; Receita {digitos(rf.get('cep'))}")
        cnaes = {rf.get("cnae_fiscal")} | {c.get("codigo") for c in rf.get("cnaes_secundarios") or []}
        for m in mods:
            cod, desc = CNAE_MODALIDADE[m]
            nota(OK if cod in cnaes else ATENCAO, f"CNAE para {m}",
                 f"{desc}: {'consta' if cod in cnaes else 'NÃO consta entre as atividades declaradas'}")

    # --- CNES ---
    if not cnes:
        nota(NAO_VISTO, "CNES", "não informado no cadastro.csv")
    else:
        ms, erro = baixar(URL_CNES.format(cnes))
        if erro or not (ms or {}).get("codigo_cnes"):
            nota(DIVERGE if erro in (None, "HTTP 404") else NAO_VISTO, "CNES",
                 f"{cnes} não encontrado" if erro in (None, "HTTP 404") else f"consulta falhou ({erro}); rodar de novo")
            ms = None
    if ms:
        cnpj_ms = digitos(ms.get("numero_cnpj")) or digitos(ms.get("numero_cnpj_entidade"))
        if cnpj:
            nota(OK if cnpj == cnpj_ms else DIVERGE, "CNPJ × CNES",
                 f"informado {fmt_cnpj(cnpj)}; o CNES {cnes} está no CNPJ {fmt_cnpj(cnpj_ms) or 'vazio'}")
        nome_ms = f"{ms.get('nome_razao_social')} / {ms.get('nome_fantasia')}"
        if nome_inf:
            p = nomes_parecidos(nome_inf, nome_ms)
            nota(OK if p else ATENCAO, "Nome × CNES", f"informado \"{nome_inf}\"; CNES: {nome_ms}")
        if cep_inf:
            igual = cep_inf == digitos(ms.get("codigo_cep_estabelecimento"))
            nota(OK if igual else DIVERGE, "CEP × CNES",
                 f"informado {cep_inf}; CNES {digitos(ms.get('codigo_cep_estabelecimento'))}")
        if rf and digitos(rf.get("cep")) != digitos(ms.get("codigo_cep_estabelecimento")):
            nota(ATENCAO, "CEP Receita × CNES",
                 f"Receita {digitos(rf.get('cep'))}; CNES {digitos(ms.get('codigo_cep_estabelecimento'))} — endereços diferentes")
        if ms.get("codigo_motivo_desabilitacao_estabelecimento"):
            nota(DIVERGE, "CNES ativo", f"desabilitado, motivo {ms['codigo_motivo_desabilitacao_estabelecimento']}")
        sus = ms.get("estabelecimento_faz_atendimento_ambulatorial_sus")
        nota(OK if sus == "SIM" else ATENCAO, "Atendimento ambulatorial SUS", f"CNES declara: {sus}")
        atual = ms.get("data_atualizacao") or ""
        velho = atual and (date.today() - date.fromisoformat(atual[:10])).days > 180
        nota(ATENCAO if velho else OK, "Atualização do CNES", f"{atual}{' — há mais de seis meses' if velho else ''}")
    if cnes:
        secao_imagem = conferir_imagem(cnes, mods, imagem, nota)

    # --- relatório ---
    pasta.mkdir(parents=True, exist_ok=True)
    bruto = pasta / "_consulta"
    bruto.mkdir(exist_ok=True)
    for nome, dados in (("cnpj", rf), ("cnes", ms)):
        if dados:
            (bruto / f"{nome}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    L = [f"# Validação cadastral — {nome_inf or pasta.name}", "",
         f"Consulta de {date.today():%d/%m/%Y}. Gerado por `validar.py`; rodar de novo sobrescreve.", "",
         "## Conferência", "", "| resultado | item | detalhe |", "|---|---|---|"]
    L += [f"| {'**' + r + '**' if r == DIVERGE else r} | {i} | {d} |" for r, i, d in achados]
    if rf:
        socios = "; ".join(f"{s.get('nome_socio')} ({s.get('qualificacao_socio')})" for s in rf.get("qsa") or [])
        L += ["", "## Receita Federal", "", "| campo | valor |", "|---|---|",
              f"| CNPJ | {fmt_cnpj(cnpj)} ({rf.get('descricao_identificador_matriz_filial')}) |",
              f"| Razão social | {rf.get('razao_social')} |",
              f"| Nome fantasia | {rf.get('nome_fantasia') or '—'} |",
              f"| Natureza jurídica | {rf.get('natureza_juridica')} |",
              f"| Início de atividade | {rf.get('data_inicio_atividade')} |",
              f"| Endereço | {rf.get('descricao_tipo_de_logradouro') or ''} {rf.get('logradouro')}, {rf.get('numero')}, "
              f"{rf.get('complemento') or ''} — {rf.get('bairro')}, {rf.get('municipio')}/{rf.get('uf')}, CEP {rf.get('cep')} |",
              f"| Atividade principal | {rf.get('cnae_fiscal')} {rf.get('cnae_fiscal_descricao')} |",
              f"| Quadro societário | {socios or '—'} |",
              "", "Atividades secundárias:", ""]
        L += [f"- {c.get('codigo')} {c.get('descricao')}" for c in rf.get("cnaes_secundarios") or []]
    if ms:
        tipo = ms.get("codigo_tipo_unidade")
        L += ["", "## CNES", "", "| campo | valor |", "|---|---|",
              f"| CNES | {ms.get('codigo_cnes')} |",
              f"| Razão social | {ms.get('nome_razao_social')} |",
              f"| Nome fantasia | {ms.get('nome_fantasia')} |",
              f"| CNPJ no CNES | {fmt_cnpj(digitos(ms.get('numero_cnpj')))} |",
              f"| Tipo de estabelecimento | {tipo} {tipos.get(tipo, '')} |",
              f"| Endereço | {ms.get('endereco_estabelecimento')}, {ms.get('numero_estabelecimento')} — "
              f"{ms.get('bairro_estabelecimento')}, CEP {ms.get('codigo_cep_estabelecimento')} |",
              f"| Telefone / e-mail | {ms.get('numero_telefone_estabelecimento')} / {ms.get('endereco_email_estabelecimento')} |",
              f"| Gestão | {ms.get('tipo_gestao')} ({ms.get('descricao_esfera_administrativa')}) |",
              f"| Turno | {ms.get('descricao_turno_atendimento')} |",
              f"| Ambulatorial SUS | {ms.get('estabelecimento_faz_atendimento_ambulatorial_sus')} |",
              f"| Última atualização | {ms.get('data_atualizacao')} |"]
    L += secao_imagem
    L += ["", "## O que estas bases não respondem", "",
          "Conferir na ficha completa do CNES (cnes.datasus.gov.br, busca pelo número):", "",
          "- [ ] profissionais vinculados, com o CBO que o procedimento exige",
          "- [ ] se o equipamento cadastrado é o mesmo visto na visita (marca, modelo, quantidade)", "",
          "Pedir cópia ao polo e guardar em `fotos/10_documentos/` — não há consulta pública aberta:", "",
          "- [ ] licença sanitária, cobrindo radiodiagnóstico se houver tomografia",
          "- [ ] licença de funcionamento (alvará)",
          "- [ ] vistoria do Corpo de Bombeiros",
          "- [ ] certidão do responsável técnico no conselho", ""]
    (pasta / "validacao.md").write_text("\n".join(L), encoding="utf-8", newline="\n")
    return achados


_TIPOS = {}


def carregar_tipos():
    """Código → nome do tipo de estabelecimento. Uma consulta por execução."""
    if not _TIPOS:
        dados, _ = baixar(URL_TIPOS)
        itens = dados.get("tipos_unidade", dados) if isinstance(dados, dict) else dados or []
        _TIPOS.update({t.get("codigo_tipo_unidade"): t.get("descricao_tipo_unidade", "")
                       for t in itens if isinstance(t, dict)})
    return _TIPOS


def carregar_imagem(procurados):
    """Equipamentos, serviços e cadastro dos CNES pedidos, dos arquivos mensais do DATASUS."""
    imagem = {}
    try:
        for tipo in ("EQ", "SR", "ST"):
            imagem[tipo], imagem["competencia"] = datasus.do_cnes(tipo, procurados)
    except Exception as e:  # noqa: BLE001 - sem os arquivos, o resto da validação segue
        imagem = {"erro": f"{type(e).__name__}: {e}"}
    return imagem


def main():
    filtro = sem_acento(sys.argv[1]) if len(sys.argv) > 1 else ""
    linhas = [l for l in ler_cadastro()
              if (digitos(l.get("cnpj")) or digitos(l.get("cnes"))) and filtro in sem_acento(l["pasta"])]
    if not linhas:
        print("Nenhuma linha do cadastro.csv com CNPJ ou CNES preenchido" + (f" para '{sys.argv[1]}'." if filtro else "."))
        return
    tipos = carregar_tipos()
    imagem = carregar_imagem([digitos(l.get("cnes")) for l in linhas if digitos(l.get("cnes"))])
    for l in linhas:
        achados = validar(l, tipos, imagem)
        print(f"\n{l['pasta']}")
        for r, i, d in achados:
            print(f"  [{r:^14}] {i}: {d}")
        print(f"  -> {l['pasta']}/validacao.md")


if __name__ == "__main__":
    main()
