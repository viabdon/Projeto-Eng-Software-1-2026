"""Interface de terminal do C11. Proprietário: Enrique Araújo."""

from app.base.consulta import buscar_por_id
from app.funcionalidades.chat.c11 import listar_mensagens, enviar_mensagem


def executar(estado, usuario_id):
    """Interface interativa de terminal para envio e visualização de mensagens do chat."""
    print("\n--- C11: Chat do Grupo ---")
    try:
        grupo_id = int(input("Informe o ID do grupo: ").strip())
    except ValueError:
        print("Erro: ID do grupo inválido.")
        return

    # Exibe o histórico de mensagens ao entrar no chat
    resultado_lista = listar_mensagens(estado, usuario_id, grupo_id)
    print(f"\n[{'OK' if resultado_lista['ok'] else 'FALHA'}] {resultado_lista['mensagem']}")

    if not resultado_lista["ok"]:
        return

    print("\n--- Histórico de Mensagens ---")
    mensagens = resultado_lista["dados"]
    if not mensagens:
        print("(Nenhuma mensagem enviada ainda)")
    else:
        for msg in mensagens:
            autor = buscar_por_id(estado["usuarios"], msg["autor_id"])
            nome_autor = autor["nome"] if autor else f"Usuário {msg['autor_id']}"
            print(f"[{msg['criado_em']}] {nome_autor}: {msg['texto']}")

    print("\n------------------------------")
    print("1. Enviar nova mensagem")
    print("0. Voltar")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        texto = input("Digite a sua mensagem: ")
        resultado_envio = enviar_mensagem(estado, usuario_id, grupo_id, texto)
        print(f"\n[{'OK' if resultado_envio['ok'] else 'FALHA'}] {resultado_envio['mensagem']}")

        if resultado_envio["ok"]:
            # Atualiza o histórico após o envio (Subtask C11.4)
            resultado_atualizado = listar_mensagens(estado, usuario_id, grupo_id)
            if resultado_atualizado["ok"]:
                print("\n--- Histórico Atualizado ---")
                for msg in resultado_atualizado["dados"]:
                    autor = buscar_por_id(estado["usuarios"], msg["autor_id"])
                    nome_autor = autor["nome"] if autor else f"Usuário {msg['autor_id']}"
                    print(f"[{msg['criado_em']}] {nome_autor}: {msg['texto']}")