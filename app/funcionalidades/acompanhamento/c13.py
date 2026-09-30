"""C13 — Acessar painel de grupos. Ver docs/cards/C13.md."""

from datetime import datetime

from app.base.consulta import buscar_por_id, buscar_vinculo
from app.base.relogio import agora


def _resposta(ok, mensagem, dados=None):
    return {"ok": ok, "mensagem": mensagem, "dados": dados}


def obter_painel(estado, usuario_id):
    """Retorna grupos do usuário com um resumo pessoal de atividades."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resposta(False, "Usuário não encontrado.")

    instante_atual = agora(estado)
    painel = []
    vinculos_usuario = [
        vinculo for vinculo in estado["vinculos"]
        if vinculo["usuario_id"] == usuario_id
    ]

    for vinculo in vinculos_usuario:
        grupo_id = vinculo["grupo_id"]
        grupo = buscar_por_id(estado["grupos"], grupo_id)
        if grupo is None:
            continue

        atividades = [
            atividade for atividade in estado["atividades"]
            if atividade["grupo_id"] == grupo_id
        ]
        atividades_id = {atividade["id"] for atividade in atividades}
        tarefas_pendentes = sum(
            1 for atribuicao in estado["atribuicoes"]
            if atribuicao["usuario_id"] == usuario_id
            and atribuicao["atividade_id"] in atividades_id
            and atribuicao["status"] == "pendente"
        )

        avisos_nao_lidos = 0
        for evento in estado["eventos"]:
            if evento["grupo_id"] != grupo_id or usuario_id not in evento["destinatarios"]:
                continue
            foi_lido = any(
                leitura["evento_id"] == evento["id"]
                and leitura["usuario_id"] == usuario_id
                for leitura in estado["leituras"]
            )
            if not foi_lido:
                avisos_nao_lidos += 1

        encontros_futuros = [
            encontro for encontro in estado["encontros"]
            if encontro["grupo_id"] == grupo_id
            and datetime.fromisoformat(encontro["inicio"]) > instante_atual
        ]
        proximo_encontro = min(
            encontros_futuros,
            key=lambda encontro: datetime.fromisoformat(encontro["inicio"]),
            default=None,
        )

        materiais_recentes = sorted(
            (material for material in estado["materiais"]
             if material["grupo_id"] == grupo_id),
            key=lambda material: (material["criado_em"], material["id"]),
            reverse=True,
        )[:3]

        painel.append({
            "grupo_id": grupo_id,
            "nome": grupo["nome"],
            "ativo": grupo["ativo"],
            "tarefas_pendentes": tarefas_pendentes,
            "avisos_nao_lidos": avisos_nao_lidos,
            "proximo_encontro": proximo_encontro,
            "materiais_recentes": materiais_recentes,
        })

    if not painel:
        return _resposta(True, "Você ainda não participa de nenhum grupo.", [])
    return _resposta(True, "Meus Grupos", painel)


def sair_grupo(estado, usuario_id, grupo_id):
    """Remove o vínculo atual, sem apagar o histórico do grupo."""
    if buscar_por_id(estado["usuarios"], usuario_id) is None:
        return _resposta(False, "Usuário não encontrado.")
    if buscar_por_id(estado["grupos"], grupo_id) is None:
        return _resposta(False, "Grupo não encontrado.")

    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if vinculo is None:
        return _resposta(False, "Você não participa deste grupo.")

    if vinculo["papel"] == "monitor" and not any(
        outro["grupo_id"] == grupo_id
        and outro["papel"] == "monitor"
        and outro["usuario_id"] != usuario_id
        for outro in estado["vinculos"]
    ):
        return _resposta(False, "O último monitor não pode sair do grupo.")

    estado["vinculos"].remove(vinculo)
    estado["preferencias"] = [
        preferencia for preferencia in estado["preferencias"]
        if not (preferencia["usuario_id"] == usuario_id
                and preferencia["grupo_id"] == grupo_id)
    ]
    return _resposta(True, "Você saiu do grupo.", {"grupo_id": grupo_id})
