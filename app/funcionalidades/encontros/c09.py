"""C09 — Marcar e alterar horário de encontro. Ver docs/cards/C09.md."""

from datetime import datetime

from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.eventos import registrar_evento
from app.base.relogio import agora


def _resposta(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def _validar_inicio(estado, inicio):
    if not isinstance(inicio, str) or not inicio.strip():
        return None, "Informe a data e a hora do encontro."
    texto = inicio.strip()
    try:
        momento = datetime.fromisoformat(texto)
    except ValueError:
        return None, "Data/hora inválida. Use o formato AAAA-MM-DDTHH:MM."

    if momento.tzinfo is not None or momento.isoformat(timespec="minutes") != texto:
        return None, "Use o formato local AAAA-MM-DDTHH:MM, por exemplo 2026-09-26T14:00."
    if momento <= agora(estado):
        return None, "A data e a hora do encontro devem ser futuras."
    return momento, None


def _validar_local(local):
    if not isinstance(local, str) or not local.strip():
        return None, "Informe o local ou o link da reunião."
    return local.strip(), None


def _grupo_para_participante(estado, usuario_id, grupo_id):
    usuario = buscar_por_id(estado["usuarios"], usuario_id)
    if usuario is None:
        return None, "Usuário não encontrado."

    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if grupo is None:
        return None, "Grupo não encontrado."
    if not grupo["ativo"]:
        return None, "Este grupo está inativo."
    if buscar_vinculo(estado, usuario_id, grupo_id) is None:
        return None, "Você precisa participar do grupo para acessar seus encontros."
    return grupo, None


def marcar_encontro(estado, usuario_id, grupo_id, inicio, local):
    """Marca encontro futuro para um grupo do qual o usuário participa."""
    grupo, erro = _grupo_para_participante(estado, usuario_id, grupo_id)
    if erro:
        return _resposta(False, erro)

    momento, erro = _validar_inicio(estado, inicio)
    if erro:
        return _resposta(False, erro)
    local_validado, erro = _validar_local(local)
    if erro:
        return _resposta(False, erro)

    encontro = {
        "id": proximo_id(estado["encontros"]),
        "grupo_id": grupo["id"],
        "criador_id": usuario_id,
        "inicio": momento.isoformat(timespec="minutes"),
        "local": local_validado,
    }
    estado["encontros"].append(encontro)
    return _resposta(True, "Encontro marcado com sucesso.", encontro)


def _registrar_alteracao(estado, encontro):
    prefixo = "encontro:" + str(encontro["id"]) + ":alteracao:"
    quantidade = sum(
        1 for evento in estado["eventos"]
        if evento["tipo"] == "alteracao_encontro"
        and evento["chave"].startswith(prefixo)
    )
    numero = quantidade + 1
    destinatarios = [
        vinculo["usuario_id"] for vinculo in estado["vinculos"]
        if vinculo["grupo_id"] == encontro["grupo_id"]
    ]
    texto = (
        "O encontro " + str(encontro["id"]) + " foi alterado para "
        + encontro["inicio"] + " em " + encontro["local"] + "."
    )
    return registrar_evento(
        estado,
        encontro["grupo_id"],
        "alteracao_encontro",
        texto,
        destinatarios,
        prefixo + str(numero),
    )


def alterar_encontro(estado, usuario_id, encontro_id, inicio, local):
    """Altera data/hora e local somente para quem criou o encontro."""
    encontro = buscar_por_id(estado["encontros"], encontro_id)
    if encontro is None:
        return _resposta(False, "Encontro não encontrado.")

    grupo, erro = _grupo_para_participante(
        estado, usuario_id, encontro["grupo_id"]
    )
    if erro:
        return _resposta(False, erro)
    if encontro["criador_id"] != usuario_id:
        return _resposta(False, "Somente quem criou o encontro pode alterá-lo.")

    momento, erro = _validar_inicio(estado, inicio)
    if erro:
        return _resposta(False, erro)
    local_validado, erro = _validar_local(local)
    if erro:
        return _resposta(False, erro)

    novo_inicio = momento.isoformat(timespec="minutes")
    if encontro["inicio"] == novo_inicio and encontro["local"] == local_validado:
        return _resposta(
            True,
            "Os dados informados já são os atuais; nenhum evento de alteração foi criado.",
            encontro,
        )

    encontro["inicio"] = novo_inicio
    encontro["local"] = local_validado
    evento = _registrar_alteracao(estado, encontro)
    return _resposta(
        True,
        "Encontro atualizado. Evento de alteração registrado (ID "
        + str(evento["id"]) + ").",
        encontro,
    )
