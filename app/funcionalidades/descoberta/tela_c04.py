"""Interface de terminal do C04. Proprietário: Bernardo Lins."""

from app.funcionalidades.descoberta.c04 import filtrar_grupos


def executar(estado, usuario_id):
    """Filtra os resultados da última busca realizada no C03."""
    grupos = estado.get("_ultimo_grupos_encontrados")
    if grupos is None:
        print("Nenhuma busca foi realizada ainda. Use a opção 03 antes do filtro.")
        return

    while True:
        print("\n04 - Filtrar grupos encontrados | 0 - Voltar")
        print("Filtros vazios = mostrar todos os resultados da busca atual.")
        modalidade = input("Modalidade (online/presencial ou vazio): ").strip()
        privacidade = input("Privacidade (publico/privado ou vazio): ").strip()
        resultado = filtrar_grupos(grupos, modalidade, privacidade)
        print(resultado["mensagem"])

        if not resultado["ok"]:
            print("A lista original permanece intacta.")
            continue

        if not resultado["dados"]:
            print("Nenhum grupo corresponde aos filtros aplicados.")
            escolha = input("[0] Voltar | [1] Limpar filtros e mostrar todos: ").strip()
            if escolha == "0":
                return
            if escolha == "1":
                modalidade = ""
                privacidade = ""
                resultado = filtrar_grupos(grupos, modalidade, privacidade)
                print(resultado["mensagem"])
                print("Lista restaurada:")
                for grupo in resultado["dados"]:
                    print(
                        f"- ID {grupo['id']} | {grupo['nome']} | "
                        f"modalidade={grupo.get('modalidade', '')} | "
                        f"privacidade={grupo.get('privacidade', '')}"
                    )
                continue
            continue

        print("Resultados filtrados:")
        for grupo in resultado["dados"]:
            print(
                f"- ID {grupo['id']} | {grupo['nome']} | "
                f"modalidade={grupo.get('modalidade', '')} | "
                f"privacidade={grupo.get('privacidade', '')}"
            )

        escolha = input("[0] Voltar | [1] Limpar filtros e mostrar todos: ").strip()
        if escolha == "0":
            return
        if escolha == "1":
            resultado = filtrar_grupos(grupos, "", "")
            print(resultado["mensagem"])
            print("Lista restaurada:")
            for grupo in resultado["dados"]:
                print(
                    f"- ID {grupo['id']} | {grupo['nome']} | "
                    f"modalidade={grupo.get('modalidade', '')} | "
                    f"privacidade={grupo.get('privacidade', '')}"
                )
            continue
