"""Interface de terminal do C05. Proprietário: Bernardo Lins."""

from app.funcionalidades.descoberta.c05 import detalhar_grupo


def executar(estado, usuario_id):
    """Coleta o ID do grupo e exibe os dados do grupo."""
    while True:
        print("\n05 - Visualizar detalhes do grupo | 0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha.isdigit():
            escolha = escolha.zfill(2)
        if escolha != "05":
            print("Opção inválida.")
            continue

        valor = input("ID do grupo: ").strip()
        try:
            grupo_id = int(valor)
        except ValueError:
            print("O ID deve ser um número inteiro.")
            continue

        resultado = detalhar_grupo(estado, grupo_id)
        print(resultado["mensagem"])
        if not resultado["ok"]:
            continue

        dados = resultado["dados"]
        print(f"ID: {dados['id']}")
        print(f"Nome: {dados['nome']}")
        print(f"Matéria: {dados['materia']}")
        print(f"Descrição: {dados['descricao']}")
        print(f"Objetivo: {dados['objetivo']}")
        print(f"Modalidade: {dados['modalidade']}")
        print(f"Privacidade: {dados['privacidade']}")
        print(f"Participantes: {dados['participantes']}")
        print(f"Limite: {dados['limite']}")
        print(f"Vagas: {dados['vagas']}")
