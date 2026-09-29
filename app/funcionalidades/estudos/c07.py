"""C07 — Definir tarefas e metas de estudo em um grupo."""

from datetime import datetime

from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.eventos import registrar_evento
from app.base.relogio import agora


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def _texto(valor):
    if isinstance(valor, str):
        return valor.strip()
    return ""


def _converter_data(valor, campo, erros):
    """Converte uma data ISO e registra uma mensagem clara se for inválida."""
    texto = _texto(valor)
    if not texto:
        erros.append(campo + " obrigatório")
        return None

    try:
        data = datetime.fromisoformat(texto)
    except (TypeError, ValueError, OverflowError):
        erros.append(campo + " deve usar o formato AAAA-MM-DDTHH:MM")
        return None

    if data.tzinfo is not None:
        erros.append(campo + " deve usar o horário local sem fuso")
        return None
    if data.isoformat(timespec="minutes") != texto:
        erros.append(campo + " deve usar o formato AAAA-MM-DDTHH:MM")
        return None
    return data


def _buscar_grupo_e_vinculo(estado, usuario_id, grupo_id):
    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if grupo is None:
        return None, None, _resultado(False, "Grupo não encontrado.")
    if not grupo["ativo"]:
        return None, None, _resultado(False, "O grupo está inativo.")

    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if vinculo is None:
        return None, None, _resultado(
            False, "É necessário participar do grupo para acessar as atividades."
        )
    return grupo, vinculo, None


def criar_atividade(
    estado,
    usuario_id,
    grupo_id,
    tipo,
    escopo,
    titulo,
    descricao,
    objetivo,
    inicio,
    prazo,
):
    """Cria a atividade e uma atribuição independente para cada participante."""
    erros = []

    tipo = _texto(tipo).casefold()
    escopo = _texto(escopo).casefold()
    titulo = _texto(titulo)
    descricao = _texto(descricao)
    objetivo = _texto(objetivo)

    if tipo not in ("tarefa", "meta"):
        erros.append("tipo deve ser tarefa ou meta")
    if escopo not in ("pessoal", "grupo"):
        erros.append("escopo deve ser pessoal ou grupo")
    if not titulo:
        erros.append("título obrigatório")
    if not descricao:
        erros.append("descrição obrigatória")
    if not objetivo:
        erros.append("objetivo obrigatório")

    inicio_data = _converter_data(inicio, "início", erros)
    prazo_data = _converter_data(prazo, "prazo", erros)

    if prazo_data is not None:
        if prazo_data <= agora(estado):
            erros.append("prazo deve ser futuro")
        if inicio_data is not None and prazo_data <= inicio_data:
            erros.append("prazo deve ser posterior ao início")

    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        erros.append("usuário não encontrado")

    _, vinculo, erro_grupo = _buscar_grupo_e_vinculo(
        estado, usuario_id, grupo_id
    )
    if erro_grupo is not None:
        erros.append(erro_grupo["mensagem"].rstrip("."))
    elif escopo == "grupo" and vinculo["papel"] != "monitor":
        erros.append("somente um monitor pode criar atividade coletiva")

    if erros:
        return _resultado(
            False,
            "Atividade não criada. Corrija: " + "; ".join(erros) + ".",
        )

    destinatarios = []
    if escopo == "pessoal":
        destinatarios.append(usuario_id)
    else:
        for vinculo_atual in estado["vinculos"]:
            if vinculo_atual["grupo_id"] == grupo_id:
                pessoa_id = vinculo_atual["usuario_id"]
                if pessoa_id not in destinatarios:
                    destinatarios.append(pessoa_id)

    atividade = {
        "id": proximo_id(estado["atividades"]),
        "grupo_id": grupo_id,
        "criador_id": usuario_id,
        "tipo": tipo,
        "escopo": escopo,
        "titulo": titulo,
        "descricao": descricao,
        "objetivo": objetivo,
        "inicio": inicio_data.isoformat(timespec="minutes"),
        "prazo": prazo_data.isoformat(timespec="minutes"),
    }

    novas_atribuicoes = []
    proximo_atribuicao_id = proximo_id(estado["atribuicoes"])
    for pessoa_id in destinatarios:
        atribuicao = {
            "id": proximo_atribuicao_id,
            "atividade_id": atividade["id"],
            "usuario_id": pessoa_id,
            "status": "pendente",
            "concluida_em": None,
        }
        novas_atribuicoes.append(atribuicao)
        proximo_atribuicao_id += 1

    # Alterar o estado somente depois que todas as validações forem aprovadas.
    estado["atividades"].append(atividade)
    for atribuicao in novas_atribuicoes:
        estado["atribuicoes"].append(atribuicao)

    nome_tipo = "tarefa" if tipo == "tarefa" else "meta"
    texto_evento = "Nova " + nome_tipo + ": " + titulo
    registrar_evento(
        estado,
        grupo_id,
        "nova_tarefa",
        texto_evento,
        destinatarios,
        "atividade:" + str(atividade["id"]),
    )
    return _resultado(True, "Atividade criada e atribuída com sucesso.", atividade)


def listar_atividades(estado, usuario_id, grupo_id):
    """Lista tarefas do membro ou atribuições do grupo para o monitor."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")

    grupo, vinculo, erro = _buscar_grupo_e_vinculo(estado, usuario_id, grupo_id)
    if erro is not None:
        return erro

    eh_monitor = vinculo["papel"] == "monitor"
    atividades = []
    for atividade in estado["atividades"]:
        if atividade["grupo_id"] != grupo["id"]:
            continue

        for atribuicao in estado["atribuicoes"]:
            if atribuicao["atividade_id"] != atividade["id"]:
                continue
            if not eh_monitor and atribuicao["usuario_id"] != usuario_id:
                continue

            nova_avaliacao = False
            for avaliacao in estado["avaliacoes"]:
                if (
                    avaliacao["atribuicao_id"] == atribuicao["id"]
                    and not avaliacao["lida"]
                    and atribuicao["usuario_id"] == usuario_id
                ):
                    nova_avaliacao = True
                    break

            atividades.append(
                {
                    "atividade": atividade,
                    "atribuicao": atribuicao,
                    "nova_avaliacao": nova_avaliacao,
                }
            )

    if not atividades:
        return _resultado(True, "Não há atividades para exibir neste grupo.", [])
    return _resultado(True, "Atividades do grupo listadas.", atividades)


def concluir_atividade(estado, usuario_id, atribuicao_id):
    """Conclui apenas a atribuição do usuário e antes do prazo final."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")
    if isinstance(atribuicao_id, bool) or not isinstance(atribuicao_id, int):
        return _resultado(False, "ID da atribuição inválido.")

    atribuicao = buscar_por_id(estado["atribuicoes"], atribuicao_id)
    if atribuicao is None:
        return _resultado(False, "Atribuição não encontrada.")
    if atribuicao["usuario_id"] != usuario_id:
        return _resultado(False, "Só é possível concluir a própria atribuição.")
    if atribuicao["status"] != "pendente":
        return _resultado(False, "A atribuição não está pendente.")

    atividade = buscar_por_id(estado["atividades"], atribuicao["atividade_id"])
    if atividade is None:
        return _resultado(False, "A atividade desta atribuição não foi encontrada.")

    _, _, erro = _buscar_grupo_e_vinculo(
        estado, usuario_id, atividade["grupo_id"]
    )
    if erro is not None:
        return erro

    erros_data = []
    prazo_data = _converter_data(atividade["prazo"], "prazo", erros_data)
    if prazo_data is None:
        return _resultado(
            False,
            "Atribuição não concluída. O prazo cadastrado é inválido.",
        )
    if agora(estado) >= prazo_data:
        return _resultado(
            False,
            "Período encerrado. A atribuição continua pendente.",
        )

    atribuicao["status"] = "concluida"
    atribuicao["concluida_em"] = agora(estado).isoformat(timespec="minutes")
    return _resultado(True, "Atividade concluída com sucesso.", atribuicao)
