"""Interface de terminal do C09. Proprietário: Alexandre Scalercio."""

from app.base.consulta import buscar_por_id
from app.funcionalidades.encontros.c09 import alterar_encontro, marcar_encontro


def _ler_id(pergunta):
    valor = input(pergunta).strip()
    try:
        return int(valor)
    except ValueError:
        print("Informe um ID numérico.")
        return None


def _mostrar_grupos(estado, usuario_id):
    print("\nGrupos:")
    for grupo in estado["grupos"]:
        if not grupo["ativo"]:
            continue
        participa = any(
            vinculo["grupo_id"] == grupo["id"]
            and vinculo["usuario_id"] == usuario_id
            for vinculo in estado["vinculos"]
        )
        if participa:
            print("ID " + str(grupo["id"]) + " — " + grupo["nome"])


def _mostrar_encontros(estado, usuario_id):
    print("\nEncontros dos seus grupos:")
    encontrados = False
    for encontro in estado["encontros"]:
        participa = any(
            vinculo["grupo_id"] == encontro["grupo_id"]
            and vinculo["usuario_id"] == usuario_id
            for vinculo in estado["vinculos"]
        )
        if not participa:
            continue
        grupo = buscar_por_id(estado["grupos"], encontro["grupo_id"])
        nome_grupo = grupo["nome"] if grupo is not None else "Grupo " + str(encontro["grupo_id"])
        print(
            "ID " + str(encontro["id"]) + " — " + nome_grupo
            + " | " + encontro["inicio"] + " | " + encontro["local"]
        )
        encontrados = True
    if not encontrados:
        print("Nenhum encontro dos seus grupos foi encontrado.")


def executar(estado, usuario_id):
    """Oferece criação, consulta e alteração de encontros."""
    while True:
        print("\n09 — Encontros")
        print("1 - Marcar encontro")
        print("2 - Listar e alterar encontro")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()

        if escolha == "0":
            return
        if escolha == "1":
            _mostrar_grupos(estado, usuario_id)
            grupo_id = _ler_id("ID do grupo: ")
            if grupo_id is None:
                continue
            inicio = input("Data e hora (AAAA-MM-DDTHH:MM): ").strip()
            local = input("Local ou link: ").strip()
            resultado = marcar_encontro(
                estado, usuario_id, grupo_id, inicio, local
            )
            print(resultado["mensagem"])
            if resultado["ok"]:
                encontro = resultado["dados"]
                print(
                    "Encontro ID " + str(encontro["id"]) + ": "
                    + encontro["inicio"] + " | " + encontro["local"]
                    + " | criado pelo usuário " + str(encontro["criador_id"])
                )
            continue

        if escolha == "2":
            _mostrar_encontros(estado, usuario_id)
            encontro_id = _ler_id(
                "ID do encontro para alterar (será validado): "
            )
            if encontro_id is None:
                continue
            inicio = input("Nova data e hora (AAAA-MM-DDTHH:MM): ").strip()
            local = input("Novo local ou link: ").strip()
            resultado = alterar_encontro(
                estado, usuario_id, encontro_id, inicio, local
            )
            print(resultado["mensagem"])
            if resultado["ok"]:
                encontro = resultado["dados"]
                print(
                    "Encontro ID " + str(encontro["id"]) + ": "
                    + encontro["inicio"] + " | " + encontro["local"]
                )
                prefixo = "encontro:" + str(encontro["id"]) + ":alteracao:"
                eventos = [
                    evento for evento in estado["eventos"]
                    if evento["tipo"] == "alteracao_encontro"
                    and evento["chave"].startswith(prefixo)
                ]
                if eventos:
                    evento = max(eventos, key=lambda item: item["id"])
                    print(
                        "Destinatários elegíveis do aviso: "
                        + str(evento["destinatarios"])
                    )
            continue

        print("Opção inválida. Escolha 1, 2 ou 0.")
