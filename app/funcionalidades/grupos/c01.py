"""C01 — Criar grupo de estudo. Ver docs/cards/C01.md."""

from app.base.consulta import buscar_por_id, proximo_id


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def criar_grupo(estado, usuario_id, nome, materia, objetivo, limite):
    """Cria um grupo inativo e vincula seu criador como monitor."""
    nome = nome.strip() if isinstance(nome, str) else ""
    materia_informada = materia.strip() if isinstance(materia, str) else ""
    objetivo = objetivo.strip() if isinstance(objetivo, str) else ""
    erros = []

    if not nome:
        erros.append("nome obrigatório")
    if not objetivo:
        erros.append("objetivo obrigatório")

    materia_canonica = None
    for item in estado["materias"]:
        if isinstance(item, str) and item.strip().casefold() == materia_informada.casefold():
            materia_canonica = item.strip()
            break
    if materia_canonica is None:
        erros.append("matéria deve estar no catálogo disponível")

    if isinstance(limite, bool) or not isinstance(limite, int) or limite <= 0:
        erros.append("limite deve ser um número inteiro positivo")

    if erros:
        return _resultado(
            False,
            "Grupo não criado. Corrija: " + "; ".join(erros) + ".",
        )

    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")

    grupo = {
        "id": proximo_id(estado["grupos"]),
        "nome": nome,
        "materia": materia_canonica,
        "objetivo": objetivo,
        "limite": limite,
        "criador_id": usuario_id,
        "descricao": "",
        "modalidade": "",
        "privacidade": "",
        "ativo": False,
    }
    vinculo = {
        "id": proximo_id(estado["vinculos"]),
        "grupo_id": grupo["id"],
        "usuario_id": usuario_id,
        "papel": "monitor",
    }
    estado["grupos"].append(grupo)
    estado["vinculos"].append(vinculo)
    return _resultado(
        True,
        "Grupo criado como rascunho. Conclua a configuração na opção 02.",
        grupo,
    )
