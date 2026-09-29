"""Interface de terminal do C07."""

from datetime import datetime

from app.base.consulta import buscar_por_id, buscar_vinculo
from app.funcionalidades.estudos import c07


def _ler_id(pergunta):
    valor = input(pergunta).strip()
    try:
        return int(valor)
    except ValueError:
        print("Informe um ID numérico.")
        return None


def _mostrar_grupos(estado, usuario_id):
    grupos = []
    for grupo in estado["grupos"]:
        vinculo = buscar_vinculo(estado, usuario_id, grupo["id"])
        if grupo["ativo"] and vinculo is not None:
            grupos.append(grupo)

    if not grupos:
        print("Não há grupos ativos disponíveis para este usuário.")
        return False

    print("Grupos ativos:")
    for grupo in grupos:
        print(str(grupo["id"]) + " - " + grupo["nome"])
    return True


def _criar(estado, usuario_id):
    if not _mostrar_grupos(estado, usuario_id):
        return
    grupo_id = _ler_id("ID do grupo ativo: ")
    if grupo_id is None:
        return

    print("Tipo: tarefa ou meta")
    tipo = input("Tipo: ").strip()
    print("Escopo: pessoal ou grupo")
    escopo = input("Escopo: ").strip()
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    objetivo = input("Objetivo: ")
    inicio = input("Início (AAAA-MM-DDTHH:MM): ")
    prazo = input("Prazo (AAAA-MM-DDTHH:MM): ")

    resultado = c07.criar_atividade(
        estado,
        usuario_id,
        grupo_id,
        tipo,
        escopo,
        titulo,
        descricao,
        objetivo,
        inicio,
        prazo,
    )
    print(resultado["mensagem"])

    if not resultado["ok"]:
        return

    atividade = resultado["dados"]
    print(
        "Atividade #"
        + str(atividade["id"])
        + " — "
        + atividade["tipo"]
        + " — prazo "
        + atividade["prazo"]
    )

    nomes = []
    for atribuicao in estado["atribuicoes"]:
        if atribuicao["atividade_id"] == atividade["id"]:
            pessoa = buscar_por_id(estado["usuarios"], atribuicao["usuario_id"])
            if pessoa is not None:
                nomes.append(pessoa["nome"])
    print("Atribuída a: " + ", ".join(nomes))

    chave_evento = "atividade:" + str(atividade["id"])
    for evento in estado["eventos"]:
        if evento["chave"] == chave_evento:
            destinatarios = []
            for destinatario_id in evento["destinatarios"]:
                pessoa = buscar_por_id(estado["usuarios"], destinatario_id)
                if pessoa is not None:
                    destinatarios.append(pessoa["nome"])
            if destinatarios:
                print(
                    "Aviso local registrado para: " + ", ".join(destinatarios)
                )
            else:
                print("Aviso local registrado sem destinatários elegíveis.")
            print("Texto do aviso: " + evento["texto"])
            break


def _listar(estado, usuario_id):
    if not _mostrar_grupos(estado, usuario_id):
        return
    grupo_id = _ler_id("ID do grupo ativo: ")
    if grupo_id is None:
        return

    resultado = c07.listar_atividades(estado, usuario_id, grupo_id)
    print(resultado["mensagem"])
    if not resultado["ok"]:
        return

    for item in resultado["dados"]:
        atividade = item["atividade"]
        atribuicao = item["atribuicao"]
        pessoa = buscar_por_id(estado["usuarios"], atribuicao["usuario_id"])
        if pessoa is None:
            nome = "Usuário desconhecido"
        else:
            nome = pessoa["nome"]
        print("\nAtividade #" + str(atividade["id"]) + ": " + atividade["titulo"])
        print("Tipo: " + atividade["tipo"] + " | Escopo: " + atividade["escopo"])
        print("Pessoa: " + nome + " (ID " + str(atribuicao["usuario_id"]) + ")")
        print("Atribuição #" + str(atribuicao["id"]))
        print("Prazo: " + atividade["prazo"])
        print("Status: " + atribuicao["status"])

        prazo = datetime.fromisoformat(atividade["prazo"])
        atual = datetime.fromisoformat(estado["configuracao"]["agora"])
        if atribuicao["status"] == "pendente" and atual >= prazo:
            print("Prazo encerrado; a atividade pode ser avaliada na opção 08.")
        if item["nova_avaliacao"]:
            print("Nova avaliação: abra a opção 08 para ler o feedback.")


def _concluir(estado, usuario_id):
    atribuicao_id = _ler_id("ID da sua atribuição: ")
    if atribuicao_id is None:
        return

    resultado = c07.concluir_atividade(estado, usuario_id, atribuicao_id)
    print(resultado["mensagem"])
    if resultado["ok"]:
        atribuicao = resultado["dados"]
        print(
            "Atribuição #"
            + str(atribuicao["id"])
            + " concluída em "
            + atribuicao["concluida_em"]
            + "."
        )


def executar(estado, usuario_id):
    """Apresenta as operações do card e retorna ao menu principal."""
    while True:
        print("\nC07 — Tarefas e metas de estudo")
        print("1 - Criar tarefa ou meta")
        print("2 - Listar atividades do grupo")
        print("3 - Concluir minha atribuição")
        print("0 - Voltar ao menu principal")
        escolha = input("Opção: ").strip()

        if escolha == "0":
            return
        if escolha == "1":
            _criar(estado, usuario_id)
        elif escolha == "2":
            _listar(estado, usuario_id)
        elif escolha == "3":
            _concluir(estado, usuario_id)
        else:
            print("Opção inválida. Escolha 1, 2, 3 ou 0.")
