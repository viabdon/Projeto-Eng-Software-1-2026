"""Interface de terminal do C03. Proprietário: Bernardo Lins."""

from app.funcionalidades.descoberta.c03 import buscar_grupos
from app.funcionalidades.descoberta.c04 import filtrar_grupos
from app.funcionalidades.descoberta.c05 import detalhar_grupo


def executar(estado, usuario_id):
    """Coleta a matéria, busca grupos e oferece filtros e ações secundárias."""
    while True:
        print("\n03 - Procurar grupos por matéria | 0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha.isdigit():
            escolha = escolha.zfill(2)
        if escolha != "03":
            print("Opção inválida.")
            continue

        materia = input("Matéria: ").strip()
        resultado = buscar_grupos(estado, materia)
        print(resultado["mensagem"])

        if not resultado["ok"]:
            continue

        grupos = resultado["dados"]
        estado["_ultimo_grupos_encontrados"] = grupos

        if not grupos:
            continue

        print("Resultados:")
        for grupo in grupos:
            print(
                f"- ID {grupo['id']} | {grupo['nome']} | "
                f"modalidade={grupo.get('modalidade', '')} | "
                f"privacidade={grupo.get('privacidade', '')}"
            )

        while True:
            print("Ações: [1] Filtrar resultados | [2] Consultar detalhes (C05) | [0] Voltar")
            acao = input("Escolha: ").strip()
            if acao == "0":
                break
            if acao == "1":
                modalidade = input("Modalidade (online/presencial ou vazio): ").strip()
                privacidade = input("Privacidade (publico/privado ou vazio): ").strip()
                filtrado = filtrar_grupos(grupos, modalidade, privacidade)
                print(filtrado["mensagem"])
                if not filtrado["ok"]:
                    continue
                if not filtrado["dados"]:
                    print("Nenhum grupo corresponde aos filtros informados.")
                    continue
                print("Grupos filtrados:")
                for grupo in filtrado["dados"]:
                    print(
                        f"- ID {grupo['id']} | {grupo['nome']} | "
                        f"modalidade={grupo.get('modalidade', '')} | "
                        f"privacidade={grupo.get('privacidade', '')}"
                    )
                valor_id = input("Selecionar ID para consultar detalhes (vazio para voltar): ").strip()
                if not valor_id:
                    continue
                try:
                    grupo_id = int(valor_id)
                except ValueError:
                    print("ID inválido.")
                    continue
                if any(grupo["id"] == grupo_id for grupo in filtrado["dados"]):
                    print("C05 - Visualizar detalhes do grupo: pendente de implementação.")
                else:
                    print("ID informado fora dos resultados filtrados.")
            elif acao == "2":
                valor_id = input("ID do grupo para consultar detalhes: ").strip()
                try:
                    grupo_id = int(valor_id)
                except ValueError:
                    print("ID inválido.")
                    continue
                resultado_detalhe = detalhar_grupo(estado, grupo_id)
                print(resultado_detalhe["mensagem"])
                if not resultado_detalhe["ok"]:
                    continue
                dados = resultado_detalhe["dados"]
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
            else:
                print("Opção inválida.")

            # Permite continuar consultando a mesma busca sem recomeçar o fluxo principal.
            voltar = input("Digitar 0 para voltar ao menu do C03 ou Enter para continuar: ").strip()
            if voltar == "0":
                break
