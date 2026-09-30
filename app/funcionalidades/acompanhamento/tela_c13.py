"""Interface de terminal do C13. Proprietário: Rafael Vergolino do Nascimento."""

from app.funcionalidades.acompanhamento.c13 import obter_painel, sair_grupo
from app.funcionalidades.descoberta.c05 import detalhar_grupo


def _mostrar_detalhes(grupo):
    print("\nDetalhes do grupo")
    campos = (
        ("nome", "Nome"),
        ("materia", "Matéria"),
        ("descricao", "Descrição"),
        ("objetivo", "Objetivo"),
        ("modalidade", "Modalidade"),
        ("privacidade", "Privacidade"),
    )
    for campo, rotulo in campos:
        valor = grupo.get(campo) or "Não informado"
        print(f"{rotulo}: {valor}")
    print("Situação: " + ("Ativo" if grupo["ativo"] else "Inativo"))


def _selecionar_grupo(painel, entrada):
    try:
        grupo_id = int(entrada)
    except ValueError:
        return None
    return next((grupo for grupo in painel if grupo["grupo_id"] == grupo_id), None)


def executar(estado, usuario_id):
    """Exibe os grupos do usuário e oferece detalhes ou saída do grupo."""
    while True:
        resultado = obter_painel(estado, usuario_id)
        print("\n=== Meus Grupos ===")
        if not resultado["ok"]:
            print(resultado["mensagem"])
            return

        painel = resultado["dados"]
        if not painel:
            print(resultado["mensagem"])
            return

        for grupo in painel:
            situacao = "Inativo" if not grupo["ativo"] else "Ativo"
            print(f"\n{grupo['grupo_id']} - {grupo['nome']} ({situacao})")
            print(f"Tarefas pendentes: {grupo['tarefas_pendentes']}")
            print(f"Avisos não lidos: {grupo['avisos_nao_lidos']}")
            encontro = grupo["proximo_encontro"]
            if encontro is None:
                print("Próximo encontro: nenhum")
            else:
                print(f"Próximo encontro: {encontro['inicio']} - {encontro['local']}")
            materiais = grupo["materiais_recentes"]
            nomes_materiais = ", ".join(material["nome"] for material in materiais)
            print("Materiais recentes: " + (nomes_materiais or "nenhum"))

        escolha = input("\nID para detalhes | S para sair de um grupo | 0 para voltar: ").strip()
        if escolha == "0":
            return
        if escolha.upper() == "S":
            grupo_id_texto = input("ID do grupo para sair: ").strip()
            grupo = _selecionar_grupo(painel, grupo_id_texto)
            if grupo is None:
                print("Escolha um ID de grupo listado no painel.")
                continue
            confirmacao = input(f"Confirma sair de '{grupo['nome']}'? (S/N): ").strip().upper()
            if confirmacao != "S":
                print("Saída cancelada.")
                continue
            resposta = sair_grupo(estado, usuario_id, grupo["grupo_id"])
            print(resposta["mensagem"])
            continue

        grupo = _selecionar_grupo(painel, escolha)
        if grupo is None:
            print("Escolha um ID de grupo listado no painel.")
            continue

        try:
            resposta = detalhar_grupo(estado, grupo["grupo_id"])
        except NotImplementedError:
            grupo_registro = next(
                item for item in estado["grupos"] if item["id"] == grupo["grupo_id"]
            )
            _mostrar_detalhes(grupo_registro)
            continue

        if resposta["ok"]:
            _mostrar_detalhes(resposta["dados"])
            if "participantes" in resposta["dados"]:
                print(f"Participantes: {resposta['dados']['participantes']}")
                print(f"Vagas: {resposta['dados']['vagas']}")
        else:
            print(resposta["mensagem"])
