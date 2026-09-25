"""Contrato comum dos produtores. Não substitui a caixa de avisos do C12."""
from app.base.consulta import proximo_id, buscar_vinculo
from app.base.relogio import agora

TIPOS = ["nova_tarefa", "lembrete_encontro", "alteracao_encontro", "novo_material"]


def registrar_evento(estado, grupo_id, tipo, texto, destinatarios, chave):
    """Após operação válida, salva aviso uma vez e captura destinatários elegíveis.

    Quem chamar já deve ter validado a operação de negócio e o grupo ativo.
    Ausência de preferência significa habilitado para todos os tipos.
    """
    if tipo not in TIPOS:
        raise ValueError("Tipo de evento fora do contrato")
    for evento in estado["eventos"]:
        if evento["chave"] == chave:
            return evento
    elegiveis = []
    for usuario_id in destinatarios:
        permitido = buscar_vinculo(estado, usuario_id, grupo_id) is not None
        for preferencia in estado["preferencias"]:
            if preferencia["usuario_id"] == usuario_id and preferencia["grupo_id"] == grupo_id:
                permitido = permitido and preferencia["ativo"] and tipo in preferencia["tipos"]
        if estado["configuracao"]["bloqueio_notificacoes"]:
            permitido = False
        if permitido and usuario_id not in elegiveis:
            elegiveis.append(usuario_id)
    evento = {"id": proximo_id(estado["eventos"]), "grupo_id": grupo_id,
              "tipo": tipo, "texto": texto, "destinatarios": elegiveis,
              "criado_em": agora(estado).isoformat(timespec="minutes"), "chave": chave}
    estado["eventos"].append(evento)
    return evento
