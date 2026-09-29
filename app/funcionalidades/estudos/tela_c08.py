"""Interface de terminal para avaliações e feedback."""

from app.base.consulta import buscar_por_id
from app.funcionalidades.estudos import c08


def _ler_id(pergunta):
    try:
        return int(input(pergunta).strip())
    except ValueError:
        print("Informe um ID numérico.")
        return None


def _avaliar(estado, usuario_id):
    atribuicao_id = _ler_id("ID da atribuição: ")
    if atribuicao_id is None:
        return

    nota_informada = input("Nota (0 a 10): ").strip().replace(",", ".")
    try:
        nota = float(nota_informada)
    except ValueError:
        nota = nota_informada
    feedback = input("Feedback: ")
    resultado = c08.avaliar(estado, usuario_id, atribuicao_id, nota, feedback)
    print(resultado["mensagem"])
    if resultado["ok"]:
        avaliacao = resultado["dados"]
        print("Avaliação #" + str(avaliacao["id"]) + " para a atribuição #" + str(atribuicao_id))


def _listar(estado, usuario_id):
    resultado = c08.listar_avaliacoes(estado, usuario_id)
    print(resultado["mensagem"])
    if not resultado["ok"]:
        return
    for item in resultado["dados"]:
        avaliacao = item["avaliacao"]
        atividade = item["atividade"]
        indicador = "Nova" if not avaliacao["lida"] else "Lida"
        print(
            "Avaliação #" + str(avaliacao["id"])
            + " — " + atividade["titulo"]
            + " (" + atividade["tipo"] + ")"
            + " | Nota: " + str(avaliacao["nota"])
            + " | " + indicador
        )
        print("Feedback: " + avaliacao["feedback"])
        print("Data: " + avaliacao["criado_em"])


def _ler(estado, usuario_id):
    avaliacao_id = _ler_id("ID da avaliação a abrir: ")
    if avaliacao_id is None:
        return
    resultado = c08.ler_avaliacao(estado, usuario_id, avaliacao_id)
    print(resultado["mensagem"])
    if not resultado["ok"]:
        return
    avaliacao = resultado["dados"]
    atribuicao = buscar_por_id(estado["atribuicoes"], avaliacao["atribuicao_id"])
    atividade = buscar_por_id(estado["atividades"], atribuicao["atividade_id"])
    print("Atividade: " + atividade["titulo"])
    print("Nota: " + str(avaliacao["nota"]))
    print("Feedback: " + avaliacao["feedback"])
    print("Data: " + avaliacao["criado_em"])


def executar(estado, usuario_id):
    """Oferece registro pelo monitor, histórico e leitura pelo participante."""
    while True:
        print("\nC08 — Avaliações e feedback")
        print("1 - Registrar avaliação (monitor)")
        print("2 - Meu histórico de avaliações")
        print("3 - Abrir avaliação")
        print("0 - Voltar ao menu principal")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if escolha == "1":
            _avaliar(estado, usuario_id)
        elif escolha == "2":
            _listar(estado, usuario_id)
        elif escolha == "3":
            _ler(estado, usuario_id)
        else:
            print("Opção inválida. Escolha 1, 2, 3 ou 0.")
