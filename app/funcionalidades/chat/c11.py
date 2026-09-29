"""C11 — Chat do Grupo. Ver docs/cards/C11.md."""

from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.relogio import agora


def listar_mensagens(estado, usuario_id, grupo_id):
    """Subtasks C11.1, C11.2 e C11.5: Validações, histórico e indisponibilidade."""
    if estado.get("configuracao", {}).get("chat_indisponivel"):
        return {"ok": False, "mensagem": "O serviço de chat está temporariamente indisponível.", "dados": None}

    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if not grupo or not grupo.get("ativo"):
        return {"ok": False, "mensagem": "Grupo inexistente ou inativo.", "dados": None}

    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if not vinculo:
        return {"ok": False, "mensagem": "Apenas membros do grupo podem visualizar as mensagens do chat.", "dados": None}

    mensagens_grupo = []
    for msg in estado["mensagens"]:
        if msg["grupo_id"] == grupo_id:
            mensagens_grupo.append(msg)

    mensagens_ordenadas = sorted(mensagens_grupo, key=lambda m: m["id"])

    return {"ok": True, "mensagem": "Mensagens listadas com sucesso.", "dados": mensagens_ordenadas}


def enviar_mensagem(estado, usuario_id, grupo_id, texto):
    """Subtasks C11.1, C11.3 e C11.5: Validação de texto, envio e indisponibilidade."""
    if estado.get("configuracao", {}).get("chat_indisponivel"):
        return {"ok": False, "mensagem": "O serviço de chat está temporariamente indisponível.", "dados": None}

    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if not grupo or not grupo.get("ativo"):
        return {"ok": False, "mensagem": "Grupo inexistente ou inativo.", "dados": None}

    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if not vinculo:
        return {"ok": False, "mensagem": "Apenas membros do grupo podem enviar mensagens.", "dados": None}

    texto_limpo = texto.strip() if texto else ""
    if not texto_limpo:
        return {"ok": False, "mensagem": "Não é possível enviar mensagens vazias.", "dados": None}

    nova_mensagem = {
        "id": proximo_id(estado["mensagens"]),
        "grupo_id": grupo_id,
        "autor_id": usuario_id,
        "texto": texto_limpo,
        "criado_em": agora(estado).isoformat(timespec="minutes")
    }

    estado["mensagens"].append(nova_mensagem)

    return {"ok": True, "mensagem": "Mensagem enviada com sucesso.", "dados": nova_mensagem}