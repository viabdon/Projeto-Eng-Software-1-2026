"""Interface de terminal do C06. Proprietário: Alexandre Scalercio."""

from app.funcionalidades.participacao.c06 import solicitar_participacao


def _ler_id(pergunta):
    valor = input(pergunta).strip()
    try:
        return int(valor)
    except ValueError:
        print("Informe um ID numérico.")
        return None


def _mostrar_grupos(estado):
    print("\nGrupos disponíveis para consulta:")
    for grupo in estado["grupos"]:
        participantes = sum(1 for vinculo in estado["vinculos"]
                            if vinculo["grupo_id"] == grupo["id"])
        ativo = "ativo" if grupo["ativo"] else "inativo"
        print(
            "ID " + str(grupo["id"]) + " — " + grupo["nome"]
            + " | " + grupo["privacidade"]
            + " | " + str(participantes) + "/" + str(grupo["limite"])
            + " participantes | " + ativo
        )


def executar(estado, usuario_id):
    """Permite solicitar participação e mostra o efeito sobre as vagas."""
    while True:
        print("\n06 — Participação em grupo")
        print("1 - Solicitar participação")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()

        if escolha == "0":
            return
        if escolha != "1":
            print("Opção inválida. Escolha 1 ou 0.")
            continue

        _mostrar_grupos(estado)
        grupo_id = _ler_id("ID do grupo: ")
        if grupo_id is None:
            continue

        resultado = solicitar_participacao(estado, usuario_id, grupo_id)
        print(resultado["mensagem"])
        if resultado["ok"]:
            grupo = next(
                (item for item in estado["grupos"] if item["id"] == grupo_id),
                None,
            )
            if grupo is not None:
                participantes = sum(
                    1 for vinculo in estado["vinculos"]
                    if vinculo["grupo_id"] == grupo_id
                )
                print(
                    "Participantes: " + str(participantes)
                    + "/" + str(grupo["limite"])
                )
            print("Status da solicitação: " + resultado["dados"]["status"])
