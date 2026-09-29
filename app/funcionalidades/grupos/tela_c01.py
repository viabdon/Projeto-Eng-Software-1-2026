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

        while True:
            nome = input("Nome do grupo: ").strip()
            if nome:
                break
            print("Informe o nome do grupo.")

        while True:
            materia = input("Matéria (" + ", ".join(estado["materias"]) + "): ").strip()
            materia_valida = False
            for item in estado["materias"]:
                if materia.casefold() == item.strip().casefold():
                    materia = item
                    materia_valida = True
                    break
            if materia_valida:
                break
            print("Escolha uma matéria disponível no catálogo.")

        while True:
            objetivo = input("Objetivo do grupo: ").strip()
            if objetivo:
                break
            print("Informe o objetivo do grupo.")

        while True:
            valor_limite = input("Limite de participantes (inclui o criador): ").strip()
            try:
                limite = int(valor_limite)
            except ValueError:
                limite = 0
            if limite > 0:
                break
            print("O limite deve ser um número inteiro positivo.")

        resultado = criar_grupo(estado, usuario_id, nome, materia, objetivo, limite)
        print(resultado["mensagem"])
        if resultado["ok"]:
            print("ID do rascunho: " + str(resultado["dados"]["id"]))
