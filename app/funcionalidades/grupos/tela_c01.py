"""Interface de terminal do C01. Proprietário: Renan Gomes."""

from app.funcionalidades.grupos.c01 import criar_grupo


def executar(estado, usuario_id):
    """Oferece a criação de um rascunho e informa seu ID."""
    while True:
        print("\n01 - Criar grupo | 0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha.isdigit():
            escolha = escolha.zfill(2)
        if escolha != "01":
            print("Opção inválida.")
            continue

        nome = input("Nome do grupo: ")
        materia = input("Matéria (" + ", ".join(estado["materias"]) + "): ")
        objetivo = input("Objetivo do grupo: ")
        valor_limite = input("Limite de participantes (inclui o criador): ").strip()
        try:
            limite = int(valor_limite)
        except ValueError:
            print("O limite deve ser um número inteiro positivo.")
            continue

        resultado = criar_grupo(estado, usuario_id, nome, materia, objetivo, limite)
        print(resultado["mensagem"])
        if resultado["ok"]:
            print("ID do rascunho: " + str(resultado["dados"]["id"]))
