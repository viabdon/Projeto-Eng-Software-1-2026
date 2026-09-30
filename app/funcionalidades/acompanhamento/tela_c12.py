"""Interface de terminal do C12. Proprietário: Rafael Vergolino do Nascimento."""

from app.base.consulta import buscar_por_id, buscar_vinculo
from app.base.eventos import TIPOS
from app.funcionalidades.acompanhamento import c12


_ROTULOS_TIPOS = {
    "nova_tarefa": "Nova tarefa",
    "lembrete_encontro": "Lembrete de encontro",
    "alteracao_encontro": "Alteração de encontro",
    "novo_material": "Novo material",
}


def _ler_id(pergunta):
    try:
        return int(input(pergunta).strip())
    except ValueError:
        print("Informe um ID numérico.")
        return None


def _grupos_usuario(estado, usuario_id):
    grupos = []
    for grupo in estado["grupos"]:
        if buscar_vinculo(estado, usuario_id, grupo["id"]) is not None:
            grupos.append(grupo)
    return grupos


def _escolher_grupo(grupos):
    if not grupos:
        print("Você não participa de nenhum grupo.")
        return None
    for grupo in grupos:
        situacao = "Ativo" if grupo["ativo"] else "Inativo"
        print(f"{grupo['id']} - {grupo['nome']} ({situacao})")
    grupo_id = _ler_id("ID do grupo: ")
    if grupo_id is None:
        return None
    grupo = next((item for item in grupos if item["id"] == grupo_id), None)
    if grupo is None:
        print("Escolha um ID listado.")
    return grupo


def _configurar(estado, usuario_id):
    grupo = _escolher_grupo(_grupos_usuario(estado, usuario_id))
    if grupo is None:
        return

    preferencia = next(
        (item for item in estado["preferencias"]
         if item["usuario_id"] == usuario_id and item["grupo_id"] == grupo["id"]),
        None,
    )
    print("\nTipos de aviso:")
    for indice, tipo in enumerate(TIPOS, start=1):
        selecionado = (
            preferencia is not None
            and tipo in preferencia["tipos"]
            and preferencia["ativo"]
        )
        marca = "[x]" if selecionado else "[ ]"
        print(f"{indice} - {marca} {_ROTULOS_TIPOS[tipo]}")
    print("A - Ativar ou atualizar | D - Desativar | 0 - Voltar")
    acao = input("Opção: ").strip().upper()
    if acao == "0":
        return

    if acao == "D":
        tipos = preferencia["tipos"] if preferencia is not None else []
        resultado = c12.configurar_avisos(
            estado, usuario_id, grupo["id"], False, tipos
        )
        print(resultado["mensagem"])
        return

    if acao != "A":
        print("Escolha A, D ou 0.")
        return

    escolha_tipos = input("Tipos para receber (números separados por vírgula): ").strip()
    tipos = []
    try:
        for item in escolha_tipos.split(","):
            if not item.strip():
                continue
            indice = int(item.strip())
            tipos.append(TIPOS[indice - 1])
    except (ValueError, IndexError):
        print("Tipo inválido. Use os números listados.")
        return

    resultado = c12.configurar_avisos(
        estado, usuario_id, grupo["id"], True, tipos
    )
    print(resultado["mensagem"])


def _mostrar_avisos(estado, usuario_id):
    resultado = c12.listar_avisos(estado, usuario_id)
    print(resultado["mensagem"])
    if not resultado["ok"] or not resultado["dados"]:
        return

    for item in resultado["dados"]:
        evento = item["evento"]
        grupo = buscar_por_id(estado["grupos"], evento["grupo_id"])
        nome_grupo = grupo["nome"] if grupo is not None else "Grupo indisponível"
        status = "Lido" if item["lido"] else "Não lido"
        tipo = _ROTULOS_TIPOS.get(evento["tipo"], evento["tipo"])
        print(
            f"\nAviso #{evento['id']} | {nome_grupo} | {tipo} | "
            f"{evento['criado_em']} | {status}"
        )
        print(evento["texto"])

    evento_id = _ler_id("ID do aviso para marcar como lido (0 para voltar): ")
    if evento_id in (None, 0):
        return
    resposta = c12.marcar_lido(estado, usuario_id, evento_id)
    print(resposta["mensagem"])


def executar(estado, usuario_id):
    """Configura preferências e exibe avisos do usuário."""
    while True:
        print("\nC12 — Avisos de atividades")
        print("1 - Configurar avisos por grupo")
        print("2 - Ver avisos recebidos")
        print("0 - Voltar ao menu principal")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha == "1":
            _configurar(estado, usuario_id)
        elif escolha == "2":
            _mostrar_avisos(estado, usuario_id)
        else:
            print("Opção inválida. Escolha 1, 2 ou 0.")
