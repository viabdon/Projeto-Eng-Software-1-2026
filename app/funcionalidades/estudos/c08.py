"""C08 — avaliações e feedback das atividades de estudo."""

from datetime import datetime
from math import isfinite

from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.relogio import agora


def _resultado(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def _id_valido(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def avaliar(estado, usuario_id, atribuicao_id, nota, feedback):
    """Registra uma avaliação por atribuição concluída ou com prazo encerrado."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")
    if not _id_valido(atribuicao_id):
        return _resultado(False, "ID da atribuição inválido.")

    atribuicao = buscar_por_id(estado["atribuicoes"], atribuicao_id)
    if atribuicao is None:
        return _resultado(False, "Atribuição não encontrada.")
    atividade = buscar_por_id(estado["atividades"], atribuicao["atividade_id"])
    if atividade is None:
        return _resultado(False, "A atividade desta atribuição não foi encontrada.")
    grupo = buscar_por_id(estado["grupos"], atividade["grupo_id"])
    if grupo is None or not grupo["ativo"]:
        return _resultado(False, "O grupo da atividade não está ativo.")

    vinculo_monitor = buscar_vinculo(estado, usuario_id, grupo["id"])
    if vinculo_monitor is None or vinculo_monitor["papel"] != "monitor":
        return _resultado(False, "Somente um monitor do grupo pode avaliar esta atribuição.")
    if buscar_vinculo(estado, atribuicao["usuario_id"], grupo["id"]) is None:
        return _resultado(False, "A pessoa avaliada não participa mais do grupo.")

    for avaliacao in estado["avaliacoes"]:
        if avaliacao["atribuicao_id"] == atribuicao_id:
            return _resultado(False, "Esta atribuição já foi avaliada.")

    if isinstance(nota, bool) or not isinstance(nota, (int, float)):
        return _resultado(False, "A nota deve ser numérica, de 0 a 10.")
    if not isfinite(nota) or nota < 0 or nota > 10:
        return _resultado(False, "A nota deve estar entre 0 e 10.")
    if not isinstance(feedback, str) or not feedback.strip():
        return _resultado(False, "O feedback é obrigatório.")

    try:
        prazo = datetime.fromisoformat(atividade["prazo"])
        momento = agora(estado)
        if prazo.tzinfo is not None or momento.tzinfo is not None:
            return _resultado(False, "O prazo da atividade deve usar horário local sem fuso.")
    except (TypeError, ValueError, OverflowError):
        return _resultado(False, "O prazo da atividade é inválido.")
    if atribuicao["status"] != "concluida" and momento < prazo:
        return _resultado(False, "Atividade ainda indisponível para avaliação.")

    avaliacao = {
        "id": proximo_id(estado["avaliacoes"]),
        "atribuicao_id": atribuicao_id,
        "monitor_id": usuario_id,
        "nota": nota,
        "feedback": feedback.strip(),
        "criado_em": momento.isoformat(timespec="minutes"),
        "lida": False,
    }
    estado["avaliacoes"].append(avaliacao)
    return _resultado(True, "Avaliação registrada com sucesso.", avaliacao)


def listar_avaliacoes(estado, usuario_id):
    """Mostra somente o histórico da pessoa avaliada."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")

    historico = []
    for avaliacao in estado["avaliacoes"]:
        atribuicao = buscar_por_id(estado["atribuicoes"], avaliacao["atribuicao_id"])
        if atribuicao is None or atribuicao["usuario_id"] != usuario_id:
            continue
        atividade = buscar_por_id(estado["atividades"], atribuicao["atividade_id"])
        if atividade is None:
            continue
        historico.append(
            {"avaliacao": avaliacao, "atividade": atividade, "usuario_id": usuario_id}
        )

    if not historico:
        return _resultado(True, "Ainda não há avaliações para este usuário.", [])
    return _resultado(True, "Histórico de avaliações encontrado.", historico)


def ler_avaliacao(estado, usuario_id, avaliacao_id):
    """Abre o feedback e o marca como lido apenas para o destinatário."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resultado(False, "Usuário não encontrado.")
    if not _id_valido(avaliacao_id):
        return _resultado(False, "ID da avaliação inválido.")

    avaliacao = buscar_por_id(estado["avaliacoes"], avaliacao_id)
    if avaliacao is None:
        return _resultado(False, "Avaliação não encontrada.")
    atribuicao = buscar_por_id(estado["atribuicoes"], avaliacao["atribuicao_id"])
    if atribuicao is None or atribuicao["usuario_id"] != usuario_id:
        return _resultado(False, "Esta avaliação pertence a outro usuário.")

    avaliacao["lida"] = True
    return _resultado(True, "Avaliação aberta e marcada como lida.", avaliacao)
