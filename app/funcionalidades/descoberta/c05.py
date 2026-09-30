"""C05 — Visualizar detalhes do grupo. Ver docs/cards/C05.md."""

from app.base.consulta import buscar_por_id


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def detalhar_grupo(estado, grupo_id):
    """Retorna os detalhes do grupo e o número de participantes/vagas."""
    if not isinstance(estado, dict):
        return _resultado(False, "Estado inválido para consultar o grupo.", None)

    try:
        grupo_id = int(grupo_id)
    except (TypeError, ValueError):
        return _resultado(False, "ID do grupo inválido.", None)

    grupo = buscar_por_id(estado.get("grupos", []), grupo_id)
    if grupo is None:
        return _resultado(False, "Grupo não encontrado.", None)

    if not grupo.get("ativo", False):
        return _resultado(False, "Grupo indisponível: o grupo está inativo.", None)

    participantes = 0
    for vinculo in estado.get("vinculos", []):
        if isinstance(vinculo, dict) and vinculo.get("grupo_id") == grupo_id:
            participantes += 1

    limite = grupo.get("limite")
    if not isinstance(limite, int) or limite <= 0:
        vagas = 0
    else:
        vagas = limite - participantes
        if vagas < 0:
            vagas = 0

    dados = {
        "id": grupo.get("id"),
        "nome": grupo.get("nome"),
        "materia": grupo.get("materia"),
        "descricao": grupo.get("descricao"),
        "objetivo": grupo.get("objetivo"),
        "modalidade": grupo.get("modalidade"),
        "privacidade": grupo.get("privacidade"),
        "participantes": participantes,
        "limite": limite,
        "vagas": vagas,
    }

    if vagas == 0:
        return _resultado(
            True,
            "Grupo lotado. Não recebe nova participação.",
            dados,
        )

    return _resultado(
        True,
        "Detalhes do grupo consultados com sucesso.",
        dados,
    )
