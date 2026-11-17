"""O que cada ficha pergunta — fonte única da tela do aplicativo e dos arquivos .md.

Três fichas: "polo" (o prédio, vale para qualquer plano), "US" e "TC" (o exame).
Cada ficha é uma lista de seções; cada seção tem um tipo:

  campos   rótulo → texto curto                  dado: "texto"
  itens    rótulo → situação, observação, foto   dado: {"s": ..., "o": ..., "f": ...}
  lista    tabela de linhas livres               dado: [{coluna: texto}, ...]
  textos   rótulo → texto longo                  dado: "texto"

O identificador de um dado é "<seção>.<item>" (ou só "<seção>" numa lista).
Mudar um rótulo é livre; mudar um identificador deixa órfão o que já foi preenchido.

ESSENCIAL × COMPLEMENTAR. Item essencial é o que viabiliza ou impede o atendimento,
ou entra na gestão de risco do plano: regularidade, acesso de quem não anda, o
aparelho, a equipe, a resposta a intercorrência, a capacidade. O resto é
complementar — marcado com um terceiro elemento na tupla (X) —, fica escondido na
tela até se pedir, não conta no percentual e só sai no .md se for preenchido.
"""

X = True  # marca de item complementar

SITUACOES = [["ok", "ok"], ["ajustar", "ajustar"], ["nao_tem", "não tem"], ["na", "n/a"]]
FAZ = [["sim", "faz"], ["restr", "com restrição"], ["nao", "não faz"]]
FAZ_TC = [["ambos", "sem e com contraste"], ["sem", "só sem contraste"], ["nao", "não faz"]]
PARECER = ["apto", "apto com ajustes", "não apto"]
NIVEL = ["baixa", "média", "alta"]

CATEGORIAS_FOTO = ["01_fachada_acesso", "02_recepcao_espera_fila", "03_banheiros", "04_acessibilidade",
                   "05_salas_exame", "06_sala_troca", "07_equipamentos", "08_apoio", "09_pendencias",
                   "10_documentos"]


def _lista(pares):
    return [{"id": p[0], "rotulo": p[1], **({"extra": True} if len(p) > 2 else {})} for p in pares]


def campos(id_, titulo, pares, dica=""):
    return {"id": id_, "titulo": titulo, "tipo": "campos", "dica": dica, "itens": _lista(pares)}


def itens(id_, titulo, pares, dica="", opcoes=None):
    return {"id": id_, "titulo": titulo, "tipo": "itens", "dica": dica, "itens": _lista(pares),
            "opcoes": opcoes or SITUACOES}


def lista(id_, titulo, pares, dica=""):
    return {"id": id_, "titulo": titulo, "tipo": "lista", "dica": dica, "colunas": _lista(pares)}


def textos(id_, titulo, pares, dica=""):
    return {"id": id_, "titulo": titulo, "tipo": "textos", "dica": dica, "itens": _lista(pares)}


_PENDENCIAS = [("pendencia", "Pendência"), ("quem", "Quem resolve"), ("prazo", "Prazo"),
               ("custo", "Custo estimado"), ("impede", "Impede o início?")]


def separada(s):
    """Seção que não é vistoria: preenche-se e analisa-se à parte (aba própria, fora do percentual)."""
    s["separada"] = True
    return s


def _parecer(rotulo):
    s = campos("parecer", "Parecer", [("parecer", rotulo)])
    s["itens"][0]["opcoes"] = PARECER
    return s


POLO = [
    campos("ident", "Identificação", [
        ("nome_fantasia", "Nome fantasia"), ("razao_social", "Razão social"), ("cnpj", "CNPJ"),
        ("cnes", "CNES"), ("endereco", "Endereço completo e CEP"), ("regiao", "Setor / Região de Saúde"),
        ("telefone", "Telefone do polo"), ("email", "E-mail do polo"),
        ("contato_polo", "Quem atende a gente no polo (nome, cargo, celular)"),
        ("responsavel", "Responsável legal pelo estabelecimento"),
        ("resp_tecnico", "Responsável técnico (nome e registro no conselho)"),
        ("horario", "Dias e horário de funcionamento"),
        ("atende_sus", "Já atende SUS ou tem contrato com a SES-DF? Em quê? (conflito de agenda)"),
        ("site", "Site", X),
    ]),
    campos("visita", "Visita", [
        ("data", "Data da visita"), ("quem_visitou", "Quem visitou"), ("quem_recebeu", "Quem recebeu (nome e cargo)"),
    ]),
    itens("doc", "Regularidade", [
        ("contrato_social", "Contrato social com a última alteração e cartão do CNPJ com CNAE de saúde"),
        ("socios", "Quadro de sócios sem vínculo com dirigentes da entidade nem com servidores públicos"),
        ("alvara", "Alvará ou licença de funcionamento no endereço visitado"),
        ("licenca_sanitaria", "Licença sanitária vigente, com ultrassonografia e tomografia entre as atividades"),
        ("bombeiros", "Vistoria do Corpo de Bombeiros"),
        ("cnes_atualizado", "CNES com o endereço visitado e os aparelhos cadastrados"),
        ("crm", "Registro da clínica no CRM-DF e responsável técnico médico com CRM e RQE"),
        ("pgrss", "Plano de gerenciamento de resíduos de serviços de saúde (PGRSS)"),
        ("manutencao", "Contrato de manutenção preventiva dos aparelhos, com tempo de resposta"),
        ("disponibilidade", "Declaração de disponibilidade: salas, equipamentos e horários"),
        ("vinculo", "Vínculo formal com a entidade proponente (contrato, termo de cessão)"),
    ], dica="Sem estes o polo não pode atender. Na observação, o número e a validade: a SES-DF devolve "
            "processo com documento vencido. Pedir cópia e guardar em Fotos › documentos."),
    itens("acess", "Acessibilidade", [
        ("rampa", "Entrada em nível ou com rampa"),
        ("portas", "Portas largas o bastante para cadeira de rodas (entrada, salas, banheiro)"),
        ("elevador", "Mais de um pavimento? Elevador ou plataforma até a sala de exame"),
        ("corredores", "Caminho livre da entrada à sala para cadeira de rodas e maca"),
        ("banheiro_pcd", "Banheiro acessível"),
        ("cadeira_rodas", "Cadeira de rodas disponível no polo"),
        ("desembarque", "Carro ou ambulância consegue parar na porta"),
        ("transporte", "Distância do ponto de ônibus ou do metrô"),
        ("vaga_pcd", "Vaga reservada para PcD e idoso", X), ("estacionamento", "Estacionamento", X),
        ("balcao", "Balcão de recepção com trecho rebaixado", X), ("piso_tatil", "Piso tátil e sinalização", X),
        ("assento_obeso", "Assento para pessoa obesa", X), ("fachada", "Fachada identificada e visível da rua", X),
    ], dica="Quem não anda, usa cadeira ou chega de maca consegue ser atendido? A maior parte da fila tem 60 anos ou mais."),
    itens("recep", "Recepção, espera e fila", [
        ("postos", "Postos de atendimento na recepção (quantos)"),
        ("assentos", "Assentos na espera (quantos), contando acompanhantes"),
        ("mesma_entrada", "Mesma entrada e mesma recepção para o paciente do SUS e o particular"),
        ("fila", "Onde a fila se forma e quantas pessoas cabem sem ir para a rua"),
        ("bebedouro", "Bebedouro"),
        ("chamada", "Organização da chamada (senha, painel, voz)", X),
        ("preferenciais", "Assentos preferenciais", X),
        ("espera_separada", "Espera separada para o nosso público", X),
        ("clima", "Climatização e ventilação", X), ("acompanhante", "Espaço para acompanhante e criança", X),
        ("espera_externa", "Área externa coberta para quem espera abrir", X),
    ], dica="A recepção aguenta o volume do plano somado ao movimento próprio do polo?"),
    lista("banheiros", "Banheiros", [
        ("onde", "Banheiro (onde fica)"), ("publico", "Público (pacientes / equipe)"),
        ("cabines", "Qtd. de cabines"), ("acessivel", "Acessível"), ("conservacao", "Estado de conservação"),
        ("fraldario", "Fraldário", X), ("foto", "Foto", X),
    ]),
    lista("salas", "Salas — inventário do polo", [
        ("sala", "Sala"), ("uso", "Uso hoje"), ("disponivel", "Disponível para nós? (dias e turnos)"),
        ("falta", "O que falta para usar"),
        ("tamanho", "Tamanho aprox.", X), ("pia", "Pia", X), ("clima", "Climatização", X), ("foto", "Foto", X),
    ], dica="Todas as salas, não só as do exame. É daqui que sai a resposta sobre ampliar."),
    itens("seg", "Segurança e continuidade", [
        ("carrinho", "Carrinho de emergência e desfibrilador"),
        ("saida", "Saída de emergência sinalizada e desobstruída"),
        ("extintores", "Extintores dentro da validade"),
        ("gerador", "Gerador ou nobreak (o que acontece se faltar luz)"),
        ("registro", "Internet estável e computador na recepção e nas salas (registro no TrakCare no mesmo dia)"),
        ("adm", "Lugar para a nossa equipe: dois postos de recepção e um de gestão"),
        ("dados", "Quem acessa os dados dos pacientes e por qual meio a clínica faz contato com eles"),
        ("residuos", "Coleta de resíduos de serviço de saúde contratada"),
        ("oxigenio", "Oxigênio (cilindro ou rede)", X), ("vigilancia", "Vigilância (câmeras, porteiro)", X),
        ("laudo", "Sala de laudo", X),
        ("internet", "Internet (operadora, redundância)", X), ("copa", "Copa e banheiro da equipe", X),
        ("dml", "Depósito de material de limpeza e abrigo de resíduos", X),
        ("limpeza", "Limpeza (própria ou terceirizada, frequência)", X),
    ], dica="O que protege o paciente numa intercorrência e o que mantém o atendimento de pé."),
    textos("ampl", "Ampliação", [
        ("ociosas", "Salas ociosas ou subutilizadas"),
        ("ativar", "O que precisa ser feito para ativá-las (obra, equipamento, mobília, pessoal)"),
        ("turnos", "Turnos livres (noite, sábado, domingo)"),
        ("limite", "Limite que não dá para vencer (elétrica, espaço, contrato de locação, vizinhança)", X),
    ]),
    lista("riscos", "Riscos para o atendimento", [
        ("risco", "Risco"), ("probabilidade", "Probabilidade (baixa, média, alta)"),
        ("impacto", "Impacto (baixo, médio, alto)"), ("mitigacao", "O que reduz ou contorna"),
    ], dica="O que pode impedir ou interromper o atendimento neste polo. Alimenta a matriz de risco do plano."),
    lista("pendencias", "Precisa arrumar", _PENDENCIAS),
    textos("sint", "Síntese", [
        ("pronto", "Já está pronto"), ("nao_comporta", "Não pode ou não comporta"),
        ("obs", "Observações de quem visitou"),
    ]),
    _parecer("Parecer do polo"),
]

_CAB = campos("cab", "Vistoria", [("plano", "Plano"), ("data", "Data da vistoria"), ("quem", "Quem vistoriou")])

US = [
    _CAB,
    textos("resumo", "Resumo em uma linha", [
        ("resumo", "O que faremos aqui, quantas salas prontas, quantas podem ser ativadas e sob que condição"),
    ]),
    lista("salas_us", "Salas de ultrassom", [
        ("sala", "Identificação da sala no polo"), ("aparelho", "Aparelho (marca, modelo, ano)"),
        ("doppler", "Doppler colorido"), ("endocavitario", "Transdutor endocavitário"),
        ("pia", "Pia para higiene das mãos na sala"), ("banheiro", "Banheiro anexo ou a poucos passos"),
        ("privacidade", "Privacidade (porta que fecha, biombo ou cortina)"),
        ("cadeirante", "Entra cadeira de rodas e dá para transferir à maca"),
        ("convexo", "Transdutor convexo"), ("linear", "Transdutor linear (mama e tireoide)"),
        ("maca", "Maca: altura regulável e peso que suporta"), ("clima", "Climatização"),
        ("tamanho", "Tamanho aproximado", X),
        ("manutencao", "Última manutenção e contrato de manutenção", X),
        ("escada", "Escada de dois degraus", X), ("luz", "Luz regulável ou penumbra", X),
        ("laudo", "Computador, impressora e sistema de laudo", X), ("foto", "Foto", X),
    ], dica="Uma linha por sala."),
    itens("preparo", "Preparo e higiene", [
        ("troca", "Sala ou cabine de troca"),
        ("banheiro", "Banheiro para esvaziar ou encher a bexiga perto da sala"),
        ("agua", "Bebedouro perto das salas (exames com bexiga cheia)"),
        ("desinfeccao", "Desinfecção do transdutor endocavitário entre pacientes: como e com que produto"),
        ("acompanhante", "Espaço para acompanhante nos exames transvaginal e de próstata"),
        ("gel", "Gel, papel-lençol, preservativo de transdutor: quem fornece"),
        ("pertences", "Local para guardar pertences", X), ("avental", "Avental ou lençol descartável", X),
        ("espera_interna", "Espera interna para quem já trocou", X),
        ("descarte", "Descarte de resíduos na sala", X),
    ]),
    itens("exames", "O que o polo faz e o que não faz", [
        ("abdome", "Abdome total e superior"), ("rins", "Rins e vias urinárias"),
        ("pelvica", "Pélvica e transvaginal"), ("obstetrica", "Obstétrica"), ("mamaria", "Mamária"),
        ("tireoide", "Tireoide e cervical"), ("prostata", "Próstata"),
        ("partes_moles", "Partes moles e articulações"), ("doppler", "Doppler vascular"),
        ("pediatrica", "Pediátrica"),
    ], opcoes=FAZ),
    campos("equipe", "Equipe", [
        ("medicos", "Médicos que executam (quantos, especialidade)"),
        ("vinculo_cnes", "Estão vinculados ao CNES deste polo?"),
        ("cessao", "O polo cede a equipe ou só o espaço e o aparelho?"),
        ("laudo", "Laudo: na hora ou em quantos dias"),
        ("pacs", "Onde as imagens ficam guardadas, por quanto tempo, e se há acesso remoto para laudo"),
        ("apoio", "Apoio na sala (técnico de enfermagem, auxiliar)", X),
    ]),
    itens("cnes", "CNES", [
        ("servico", "Serviço 121/002 — ultrassonografia, com marca SUS"),
        ("equip", "Aparelhos de ultrassom cadastrados (quantos constam × quantos existem)"),
        ("cbo", "Profissionais com o CBO exigido pela ficha do procedimento"),
    ]),
    separada(campos("capac", "Ultrassom", [
        ("meta", "Meta do plano para este polo (ultrassons por dia útil e salas estimadas)"),
        ("salas", "Salas existentes e quantas ficariam com o plano"),
        ("turnos", "Dias da semana e turnos disponíveis (o plano prevê 10 h por dia útil)"),
        ("tempo", "Tempo real por exame (simples / com Doppler)"),
        ("por_hora", "Exames por hora por sala (declarado pelo polo)"),
        ("ocupado", "Quanto já está ocupado com a demanda própria do polo"),
        ("liquida", "Capacidade mensal líquida para o plano"),
        ("mensal", "Capacidade mensal bruta = salas × horas/mês × exames/hora", X),
    ])),
    textos("ampl", "Ampliação para ultrassom", [
        ("salas", "Salas que podem virar sala de ultrassom e o que falta em cada uma"),
        ("turno", "Turno extra possível"),
    ]),
    lista("pendencias", "Pendências desta modalidade", _PENDENCIAS),
    _parecer("Parecer para ultrassom"),
]

TC = [
    _CAB,
    textos("resumo", "Resumo em uma linha", [
        ("resumo", "O que faremos aqui, quantos tomógrafos em operação, se faz contraste e do que a ampliação depende"),
    ]),
    lista("tomografos", "Tomógrafo", [
        ("modelo", "Marca, modelo e ano"), ("canais", "Número de canais"), ("peso_mesa", "Peso máximo da mesa"),
        ("injetora", "Bomba injetora de contraste"),
        ("manutencao", "Contrato de manutenção (com quem, quanto tempo leva para consertar)"),
        ("pacs", "PACS: tempo de guarda, acesso remoto para laudo, entrega (filme, CD, portal)"),
        ("abertura", "Diâmetro da abertura", X), ("parada", "Última parada e por quanto tempo", X),
        ("foto", "Foto", X),
    ], dica="Uma linha por aparelho."),
    itens("protecao", "Proteção radiológica — documentos", [
        ("licenca", "Licença sanitária cobrindo o serviço de radiodiagnóstico"),
        ("blindagem", "Projeto de blindagem aprovado pela vigilância sanitária (RDC 611/2022)"),
        ("radiometrico", "Laudo de levantamento radiométrico da sala"),
        ("qualidade", "Laudos dos testes de constância e de controle de qualidade (IN 93/2021)"),
        ("programa", "Plano de proteção radiológica e protocolos de aquisição"),
        ("supervisor", "Supervisor de proteção radiológica (nome e registro)"),
        ("dosimetria", "Dosímetros individuais da equipe"),
    ], dica="Pedir cópia ou fotografar. Sem eles o serviço não está regular. Na observação, a data ou a validade."),
    itens("sala", "Sala de exame", [
        ("comando", "Sala de comando separada, com visor para a sala de exame"),
        ("sinalizacao", "Sinalização de radiação e luz vermelha na porta"),
        ("porta_maca", "Porta e caminho largos o bastante para maca e cadeira de rodas"),
        ("epi", "Aventais e protetores plumbíferos"),
        ("troca", "Sala ou cabine de troca"),
        ("voz", "Comunicação por voz com o paciente", X), ("clima", "Climatização da sala", X),
        ("armario", "Armário com chave para pertences e objetos metálicos", X),
        ("avental", "Avental descartável", X), ("espera_interna", "Espera interna para quem já trocou", X),
        ("banheiro", "Banheiro próximo à sala de exame", X),
    ]),
    itens("contraste", "Contraste e intercorrência", [
        ("faz", "O polo faz exame com contraste venoso?"),
        ("fornece", "Quem fornece o meio de contraste e onde ele fica guardado"),
        ("medico", "Médico presente durante exame contrastado"), ("enfermagem", "Enfermagem para punção"),
        ("preparo", "Local para a punção venosa"),
        ("observacao", "Espaço de repouso e observação depois do contraste"),
        ("carrinho", "Carrinho de emergência: lacre, lista de conferência, medicamentos na validade "
                     "(adrenalina, anti-histamínico, corticoide, broncodilatador)"),
        ("oxigenio", "Desfibrilador, oxigênio e monitor"),
        ("protocolo", "Protocolo de reação adversa escrito"),
        ("triagem", "Triagem (alergia, função renal, gestação) e termo de consentimento"),
        ("remocao", "Caminho livre para a maca do SAMU e serviço de urgência mais próximo"),
        ("sedacao", "Faz sedação? Atende criança?", X),
    ], dica="O maior risco assistencial da tomografia: quase todas as do plano usam contraste iodado."),
    itens("exames", "O que o polo faz e o que não faz", [
        ("cranio", "Crânio"), ("face", "Face, seios da face, pescoço"), ("torax", "Tórax"),
        ("abdome", "Abdome superior"), ("pelve", "Pelve"), ("coluna", "Coluna"),
        ("articulacoes", "Articulações e membros"), ("angio", "Angiotomografia"),
        ("coronarias", "Angiotomografia de coronárias (1.408 no plano, registradas como tórax)"),
    ], opcoes=FAZ_TC),
    campos("equipe", "Equipe", [
        ("tecnicos", "Técnicos e tecnólogos em radiologia (quantos, por turno)"),
        ("radiologistas", "Médicos radiologistas (quantos; presenciais ou laudo a distância)"),
        ("enfermagem", "Enfermagem"), ("vinculo_cnes", "Estão vinculados ao CNES deste polo?"),
        ("cessao", "O polo cede a equipe ou só o espaço e o aparelho?"),
        ("laudo", "Laudo: em quantos dias"),
    ]),
    itens("cnes", "CNES", [
        ("servico", "Serviço 121/003 — tomografia, com marca SUS"),
        ("equip", "Tomógrafo cadastrado como equipamento em uso"),
        ("cbo", "Profissionais com o CBO exigido pela ficha do procedimento"),
    ]),
    separada(campos("capac", "Tomografia", [
        ("meta", "Meta do plano para este polo (tomografias por dia útil)"),
        ("turnos", "Dias da semana e turnos disponíveis (o plano prevê 10 h por dia útil)"),
        ("tempo", "Tempo real por exame (sem contraste / com contraste)"),
        ("por_hora", "Exames por hora (sem contraste / com contraste)"),
        ("ocupado", "Quanto já está ocupado com a demanda própria do polo"),
        ("liquida", "Capacidade mensal líquida para o plano"),
        ("mensal", "Capacidade mensal bruta = horas/mês × exames/hora", X),
    ])),
    textos("ampl", "Ampliação para tomografia", [
        ("turno", "Turno extra possível (noite, fim de semana)"),
        ("contraste", "O que falta para passar a fazer contraste, se hoje não faz"),
        ("segundo", "Há espaço e carga elétrica para um segundo aparelho?", X),
    ]),
    lista("pendencias", "Pendências desta modalidade", _PENDENCIAS),
    _parecer("Parecer para tomografia"),
]

FICHAS = {"polo": POLO, "US": US, "TC": TC}
TITULOS = {"polo": "Polo", "US": "Vistoria — Ultrassonografia", "TC": "Vistoria — Tomografia Computadorizada"}
ARQUIVOS = {"polo": "polo.md", "US": "vistoria_US.md", "TC": "vistoria_TC.md"}


def catalogo(ficha):
    """{identificador: (tipo, rótulo, seção)} — tudo o que existe para preencher numa ficha."""
    cat = {}
    for s in FICHAS[ficha]:
        if s["tipo"] == "lista":
            cat[s["id"]] = ("lista", s["titulo"], s)
        else:
            tipo = {"campos": "campo", "textos": "texto", "itens": "item"}[s["tipo"]]
            for i in s["itens"]:
                cat[f"{s['id']}.{i['id']}"] = (tipo, i["rotulo"], s)
    return cat


def _cheio(tipo, v):
    if tipo == "item":
        return bool(isinstance(v, dict) and (v.get("s") or v.get("o")))
    if tipo == "lista":
        return bool(v and any(any(str(c).strip() for c in l.values()) for l in v))
    return bool(str(v or "").strip())


def preenchimento(ficha, dados):
    """(preenchidos, total) entre os itens essenciais da vistoria — uma lista conta como um."""
    feitos = total = 0
    for s in FICHAS[ficha]:
        if s.get("separada"):
            continue
        if s["tipo"] == "lista":
            total += 1
            feitos += _cheio("lista", dados.get(s["id"]))
            continue
        tipo = "item" if s["tipo"] == "itens" else "campo"
        for i in s["itens"]:
            if not i.get("extra"):
                total += 1
                feitos += _cheio(tipo, dados.get(f"{s['id']}.{i['id']}"))
    return feitos, total


def _cel(v):
    return str(v or "").replace("|", "/").replace("\r", "").replace("\n", " ").strip()


def render_md(ficha, dados, nome_polo):
    """A ficha da vistoria como Markdown, sem as seções separadas. Sem data nem hora: mesmo dado, mesmos bytes."""
    return _md(f"{TITULOS[ficha]} — {nome_polo}", [(s, dados) for s in FICHAS[ficha] if not s.get("separada")])


def render_capacidade_md(dados_por_ficha, nome_polo):
    """As seções separadas (capacidade e meta) de todas as modalidades do polo, num arquivo só."""
    return _md(f"Capacidade e metas — {nome_polo}",
               [(s, d) for ficha, d in dados_por_ficha.items() for s in FICHAS[ficha] if s.get("separada")])


def _md(titulo, secoes):
    """Item complementar só aparece se foi preenchido."""
    L = [f"# {titulo}", "",
         "Gerado pelo aplicativo a partir de `dados.json`. Editar pelo aplicativo; o que for "
         "escrito aqui à mão se perde no próximo salvamento.", ""]
    for n, (s, dados) in enumerate(secoes, 1):
        L += [f"## {n}. {s['titulo']}", ""]
        if s.get("dica"):
            L += [s["dica"], ""]
        if s["tipo"] == "lista":
            linhas = dados.get(s["id"]) or [{}]
            cols = [c for c in s["colunas"] if not c.get("extra") or any(_cel(l.get(c["id"])) for l in linhas)]
            if len(cols) > 8:  # larga demais: uma coluna por linha, um atributo por linha da tabela
                L += ["| item | " + " | ".join(f"{k + 1}" for k in range(len(linhas))) + " |",
                      "|---|" + "---|" * len(linhas)]
                L += [f"| {c['rotulo']} | " + " | ".join(_cel(l.get(c["id"])) for l in linhas) + " |" for c in cols]
            else:
                L += ["| " + " | ".join(c["rotulo"] for c in cols) + " |", "|" + "---|" * len(cols)]
                L += ["| " + " | ".join(_cel(l.get(c["id"])) for c in cols) + " |" for l in linhas]
            L.append("")
            continue
        tipo = "item" if s["tipo"] == "itens" else "campo"
        visiveis = [i for i in s["itens"]
                    if not i.get("extra") or _cheio(tipo, dados.get(f"{s['id']}.{i['id']}"))]
        if s["tipo"] == "campos":
            L += ["| campo | valor |", "|---|---|"]
            L += [f"| {i['rotulo']} | {_cel(dados.get(s['id'] + '.' + i['id']))} |" for i in visiveis]
        elif s["tipo"] == "itens":
            rot = dict(s["opcoes"])
            L += ["| item | situação | observação | foto |", "|---|---|---|---|"]
            for i in visiveis:
                v = dados.get(f"{s['id']}.{i['id']}") or {}
                L.append(f"| {i['rotulo']} | {rot.get(v.get('s'), '')} | {_cel(v.get('o'))} | {_cel(v.get('f'))} |")
        else:
            for i in visiveis:
                L += [f"**{i['rotulo']}**", "", str(dados.get(f"{s['id']}.{i['id']}") or "").strip() or "—", ""]
            L.pop()
        L.append("")
    return "\n".join(L)
