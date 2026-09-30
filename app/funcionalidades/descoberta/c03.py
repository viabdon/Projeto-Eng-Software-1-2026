"""C03 — Procurar grupos por matéria. Ver docs/cards/C03.md."""


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def buscar_grupos(estado, materia):
    """Busca grupos ativos por matéria, usando comparação sem diferenciar maiúsculas."""
    if not isinstance(estado, dict):
        return _resultado(False, "Estado inválido para a busca.", None)

    if not isinstance(materia, str):
        return _resultado(False, "Informe a matéria para buscar grupos.", None)

    materia_busca = materia.strip().lower()
    if not materia_busca:
        return _resultado(False, "Informe a matéria para buscar grupos.", None)

    grupos = estado.get("grupos", [])
    encontrados = []
    for grupo in grupos:
        if not isinstance(grupo, dict):
            continue
        if not grupo.get("ativo", False):
            continue
        materia_grupo = grupo.get("materia")
        if isinstance(materia_grupo, str) and materia_grupo.strip().lower() == materia_busca:
            encontrados.append(grupo)

    if not encontrados:
        return _resultado(True, "Nenhum grupo encontrado", [])

    return _resultado(
        True,
        f"Foram encontrados {len(encontrados)} grupo(s) para a matéria '{materia.strip()}'.",
        encontrados,
    )
