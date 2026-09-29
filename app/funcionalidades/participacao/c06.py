"""C06 — Solicitar participação no grupo. Ver docs/cards/C06.md."""

from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.relogio import agora


def _resposta(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def solicitar_participacao(estado, usuario_id, grupo_id):
    """Cria uma participação imediata em grupo público ou um pedido privado."""
    usuario = buscar_por_id(estado["usuarios"], usuario_id)
    if usuario is None:
        return _resposta(False, "Usuário não encontrado.")

    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if grupo is None:
        return _resposta(False, "Grupo não encontrado.")
    if not grupo["ativo"]:
        return _resposta(False, "Este grupo está inativo e não aceita participantes.")

    if buscar_vinculo(estado, usuario_id, grupo_id) is not None:
        return _resposta(False, "Você já participa deste grupo.")

    for solicitacao in estado["solicitacoes"]:
        if solicitacao["usuario_id"] == usuario_id and solicitacao["grupo_id"] == grupo_id:
            if solicitacao["status"] == "pendente":
                return _resposta(False, "Já existe uma solicitação pendente para este grupo.")
            if solicitacao["status"] == "aceita":
                return _resposta(False, "Sua solicitação para este grupo já foi aceita.")

    privacidade = grupo["privacidade"]
    if privacidade not in ("publico", "privado"):
        return _resposta(False, "A privacidade do grupo ainda não está configurada.")

    participantes = sum(1 for vinculo in estado["vinculos"]
                        if vinculo["grupo_id"] == grupo_id)
    limite = grupo["limite"]
    if not isinstance(limite, int) or limite <= 0:
        return _resposta(False, "O limite de participantes do grupo é inválido.")
    if participantes >= limite:
        return _resposta(False, "O grupo está lotado e não aceita novas solicitações.")

    status = "aceita" if privacidade == "publico" else "pendente"
    solicitacao = {
        "id": proximo_id(estado["solicitacoes"]),
        "grupo_id": grupo_id,
        "usuario_id": usuario_id,
        "status": status,
        "criado_em": agora(estado).isoformat(timespec="minutes"),
    }
    estado["solicitacoes"].append(solicitacao)

    if status == "aceita":
        estado["vinculos"].append({
            "id": proximo_id(estado["vinculos"]),
            "grupo_id": grupo_id,
            "usuario_id": usuario_id,
            "papel": "membro",
        })
        mensagem = "Participação confirmada no grupo público."
    else:
        mensagem = "Solicitação enviada. Ela está pendente de aprovação e não ocupa uma vaga."

    return _resposta(True, mensagem, solicitacao)
