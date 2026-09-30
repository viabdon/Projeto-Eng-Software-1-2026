"""C12 — Receber aviso de nova tarefa. Ver docs/cards/C12.md."""

from datetime import datetime

from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.eventos import TIPOS, registrar_evento
from app.base.relogio import agora


def _resposta(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def configurar_avisos(estado, usuario_id, grupo_id, ativo, tipos):
    """Cria ou atualiza a preferência de avisos do usuário para um grupo."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resposta(False, "Usuário não encontrado.")

    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if grupo is None:
        return _resposta(False, "Grupo não encontrado.")
    if not grupo["ativo"]:
        return _resposta(False, "Notificações não podem ser ativadas em um grupo inativo.")
    if buscar_vinculo(estado, usuario_id, grupo_id) is None:
        return _resposta(False, "É necessário participar do grupo para configurar avisos.")
    if not isinstance(ativo, bool):
        return _resposta(False, "O estado das notificações deve ser ativado ou desativado.")
    if ativo and estado["configuracao"]["bloqueio_notificacoes"]:
        return _resposta(False, "Notificações bloqueadas pela configuração do sistema.")
    if not isinstance(tipos, list):
        return _resposta(False, "Selecione uma lista de tipos de aviso.")
    if any(not isinstance(tipo, str) or tipo not in TIPOS for tipo in tipos):
        return _resposta(False, "Tipo de aviso inválido.")

    tipos_selecionados = list(dict.fromkeys(tipos))
    if ativo and not tipos_selecionados:
        return _resposta(False, "Selecione ao menos um tipo de aviso para ativar.")

    preferencia = next(
        (item for item in estado["preferencias"]
         if item["usuario_id"] == usuario_id and item["grupo_id"] == grupo_id),
        None,
    )
    if preferencia is None:
        preferencia = {
            "id": proximo_id(estado["preferencias"]),
            "usuario_id": usuario_id,
            "grupo_id": grupo_id,
            "ativo": ativo,
            "tipos": tipos_selecionados,
        }
        estado["preferencias"].append(preferencia)
    else:
        preferencia["ativo"] = ativo
        preferencia["tipos"] = tipos_selecionados

    mensagem = "Avisos ativados." if ativo else "Avisos desativados."
    return _resposta(True, mensagem, preferencia)


def listar_avisos(estado, usuario_id):
    """Lista avisos recebidos pelo usuário que ainda participa do grupo."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resposta(False, "Usuário não encontrado.")

    gerar_lembretes(estado)
    grupos_usuario = {
        vinculo["grupo_id"] for vinculo in estado["vinculos"]
        if vinculo["usuario_id"] == usuario_id
    }
    avisos = []
    for evento in estado["eventos"]:
        if evento["grupo_id"] not in grupos_usuario:
            continue
        if usuario_id not in evento["destinatarios"]:
            continue
        lido = any(
            leitura["evento_id"] == evento["id"]
            and leitura["usuario_id"] == usuario_id
            for leitura in estado["leituras"]
        )
        avisos.append({"evento": evento, "lido": lido})

    avisos.sort(
        key=lambda item: (item["evento"]["criado_em"], item["evento"]["id"]),
        reverse=True,
    )
    mensagem = "Avisos listados." if avisos else "Você não tem avisos."
    return _resposta(True, mensagem, avisos)


def marcar_lido(estado, usuario_id, evento_id):
    """Marca como lido um aviso destinado ao usuário, sem duplicar leituras."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resposta(False, "Usuário não encontrado.")
    if isinstance(evento_id, bool) or not isinstance(evento_id, int):
        return _resposta(False, "ID do aviso inválido.")

    evento = buscar_por_id(estado["eventos"], evento_id)
    if evento is None:
        return _resposta(False, "Aviso não encontrado.")
    if usuario_id not in evento["destinatarios"]:
        return _resposta(False, "Este aviso não foi destinado a você.")
    if buscar_vinculo(estado, usuario_id, evento["grupo_id"]) is None:
        return _resposta(False, "É necessário participar do grupo para acessar este aviso.")

    leitura = next(
        (item for item in estado["leituras"]
         if item["evento_id"] == evento_id and item["usuario_id"] == usuario_id),
        None,
    )
    if leitura is not None:
        return _resposta(True, "Aviso já estava marcado como lido.", leitura)

    leitura = {
        "id": proximo_id(estado["leituras"]),
        "evento_id": evento_id,
        "usuario_id": usuario_id,
    }
    estado["leituras"].append(leitura)
    return _resposta(True, "Aviso marcado como lido.", leitura)


def gerar_lembretes(estado):
    """Emite uma vez os lembretes de encontros futuros que ocorrem hoje."""
    instante_atual = agora(estado)
    lembretes = []
    for encontro in estado["encontros"]:
        try:
            inicio = datetime.fromisoformat(encontro["inicio"])
        except (TypeError, ValueError):
            continue
        if inicio.date() != instante_atual.date() or inicio <= instante_atual:
            continue

        grupo = buscar_por_id(estado["grupos"], encontro["grupo_id"])
        if grupo is None or not grupo["ativo"]:
            continue

        chave = "lembrete:" + str(encontro["id"]) + ":" + encontro["inicio"]
        if any(evento["chave"] == chave for evento in estado["eventos"]):
            continue
        destinatarios = [
            vinculo["usuario_id"] for vinculo in estado["vinculos"]
            if vinculo["grupo_id"] == grupo["id"]
        ]
        texto = (
            "Lembrete de encontro: " + grupo["nome"] + " em "
            + encontro["inicio"] + " - " + encontro["local"]
        )
        evento = registrar_evento(
            estado,
            grupo["id"],
            "lembrete_encontro",
            texto,
            destinatarios,
            chave,
        )
        lembretes.append(evento)

    mensagem = "Lembretes gerados." if lembretes else "Nenhum novo lembrete para hoje."
    return _resposta(True, mensagem, lembretes)
