"""C02 — Configurar características do grupo. Ver docs/cards/C02.md."""

from app.base.consulta import buscar_por_id, buscar_vinculo


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def configurar_grupo(estado, usuario_id, grupo_id, descricao, privacidade, modalidade):
    """Configura as características do grupo e o deixa ativo."""
    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if grupo is None:
        return _resultado(False, "Grupo não encontrado.")
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")
    if grupo["criador_id"] != usuario_id:
        return _resultado(False, "Somente o criador pode configurar este grupo.")
    if buscar_vinculo(estado, usuario_id, grupo_id) is None:
        return _resultado(False, "O criador não possui vínculo com este grupo.")

    descricao = descricao.strip() if isinstance(descricao, str) else ""
    privacidade = privacidade.strip().lower() if isinstance(privacidade, str) else ""
    modalidade = modalidade.strip().lower() if isinstance(modalidade, str) else ""
    if not descricao:
        return _resultado(False, "A descrição é obrigatória.")
    if privacidade not in ("publico", "privado"):
        return _resultado(False, "A privacidade deve ser publico ou privado.")
    if modalidade not in ("online", "presencial"):
        return _resultado(False, "A modalidade deve ser online ou presencial.")

    grupo["descricao"] = descricao
    grupo["privacidade"] = privacidade
    grupo["modalidade"] = modalidade
    grupo["ativo"] = True
    return _resultado(True, "Grupo configurado e ativado.", grupo)
