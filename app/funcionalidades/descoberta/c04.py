"""C04 — Filtrar grupos encontrados. Ver docs/cards/C04.md."""


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def filtrar_grupos(grupos_encontrados, modalidade, privacidade):
    """Filtra a lista de grupos por modalidade e privacidade sem alterar a original."""
    if grupos_encontrados is None:
        grupos_encontrados = []
    try:
        grupos = list(grupos_encontrados)
    except TypeError:
        return _resultado(False, "Lista de grupos inválida.", None)

    modalidade_texto = modalidade.strip().lower() if isinstance(modalidade, str) else ""
    privacidade_texto = privacidade.strip().lower() if isinstance(privacidade, str) else ""

    if modalidade_texto and modalidade_texto not in {"online", "presencial"}:
        return _resultado(
            False,
            "Modalidade inválida. Use online, presencial ou deixe em branco para todos.",
            None,
        )

    if privacidade_texto and privacidade_texto not in {"publico", "privado"}:
        return _resultado(
            False,
            "Privacidade inválida. Use publico, privado ou deixe em branco para todos.",
            None,
        )

    filtrados = []
    for grupo in grupos:
        if not isinstance(grupo, dict):
            continue
        if modalidade_texto and grupo.get("modalidade", "").strip().lower() != modalidade_texto:
            continue
        if privacidade_texto and grupo.get("privacidade", "").strip().lower() != privacidade_texto:
            continue
        filtrados.append(grupo)

    if not filtrados:
        return _resultado(True, "Nenhum grupo encontrado com os filtros aplicados.", [])

    return _resultado(True, "Grupos filtrados com sucesso.", filtrados)
