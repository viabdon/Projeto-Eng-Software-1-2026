"""Interface de terminal do C02. Proprietário: Renan Gomes."""

from app.funcionalidades.grupos.c02 import configurar_grupo


def executar(estado, usuario_id):
    """Coleta as características e apresenta a configuração final."""
    while True:
        print("\n02 - Configurar grupo | 0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha.isdigit():
            escolha = escolha.zfill(2)
        if escolha != "01":
            print("Opção inválida.")
            continue

        valor_grupo = input("ID do grupo: ").strip()
        try:
            grupo_id = int(valor_grupo)
        except ValueError:
            print("O ID deve ser um número inteiro.")
            continue

        descricao = input("Descrição: ")
        print("Privacidade: publico ou privado")
        privacidade = input("Privacidade: ")
        print("Modalidade: online ou presencial")
        modalidade = input("Modalidade: ")
        resultado = configurar_grupo(
            estado, usuario_id, grupo_id, descricao, privacidade, modalidade
        )
        print(resultado["mensagem"])
        if resultado["ok"]:
            grupo = resultado["dados"]
            print("Grupo " + str(grupo["id"]) + ": " + grupo["nome"])
            print("Descrição: " + grupo["descricao"])
            print("Privacidade: " + grupo["privacidade"])
            print("Modalidade: " + grupo["modalidade"])
            print("Ativo: " + str(grupo["ativo"]))
