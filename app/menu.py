from app.funcionalidades.grupos.tela_c27 import executar as tela_c27
from app.funcionalidades.grupos.tela_c28 import executar as tela_c28
from app.funcionalidades.descoberta.tela_c29 import executar as tela_c29
from app.funcionalidades.descoberta.tela_c30 import executar as tela_c30
from app.funcionalidades.descoberta.tela_c31 import executar as tela_c31
from app.funcionalidades.participacao.tela_c32 import executar as tela_c32
from app.funcionalidades.encontros.tela_c37 import executar as tela_c37
from app.funcionalidades.acompanhamento.tela_c09 import executar as tela_c09
from app.funcionalidades.acompanhamento.tela_c33 import executar as tela_c33
from app.funcionalidades.materiais.tela_c36 import executar as tela_c36
from app.funcionalidades.chat.tela_c38 import executar as tela_c38
from app.funcionalidades.estudos.tela_c26 import executar as tela_c26
from app.funcionalidades.estudos.tela_c19 import executar as tela_c19
from app.funcionalidades.simulados.tela_c39 import executar as tela_c39

OPCOES = [
    ("27", "Criar grupo de estudo", tela_c27),
    ("28", "Configurar características do grupo", tela_c28),
    ("29", "Procurar grupos por matéria", tela_c29),
    ("30", "Filtrar grupos encontrados", tela_c30),
    ("31", "Visualizar detalhes do grupo", tela_c31),
    ("32", "Solicitar participação no grupo", tela_c32),
    ("37", "Marcar e alterar horário de encontro", tela_c37),
    ("9", "Receber aviso de nova tarefa", tela_c09),
    ("33", "Acessar painel de grupos", tela_c33),
    ("36", "Upload e Download de material de estudo", tela_c36),
    ("38", "Chat do Grupo", tela_c38),
    ("26", "Definir Tarefas e Metas de Estudo (em um grupo)", tela_c26),
    ("19", "Receber Avaliação e Feedback de Grupos e Monitores", tela_c19),
    ("39", "Simulados gerados por IA", tela_c39),
]


def escolher_usuario(estado):
    while True:
        print("\nUsuários fictícios (seleção simula autenticação):")
        for usuario in estado["usuarios"]:
            print(str(usuario["id"]) + " - " + usuario["nome"])
        valor = input("ID do usuário: ").strip()
        for usuario in estado["usuarios"]:
            if valor == str(usuario["id"]):
                return usuario["id"]
        print("Usuário inválido. Escolha um ID listado.")


def executar(estado):
    print("Comunidade de Estudos — estrutura inicial; funcionalidades pendentes")
    print("Relógio de demonstração: " + estado["configuracao"]["agora"])
    print("Arquivos desta sessão: " + str(estado["_runtime"]))
    try:
        usuario_id = escolher_usuario(estado)
        while True:
            print("\nUsuário atual: " + str(usuario_id))
            for codigo, titulo, funcao in OPCOES:
                print(codigo + " - " + titulo)
            print("U - Trocar usuário | 0 - Sair")
            escolha = input("Opção: ").strip().upper()
            if escolha == "0":
                print("Sessão encerrada. Dados em memória serão reiniciados na próxima execução.")
                return
            if escolha == "U":
                usuario_id = escolher_usuario(estado)
                continue
            encontrada = False
            for codigo, titulo, funcao in OPCOES:
                if escolha == codigo:
                    encontrada = True
                    try:
                        funcao(estado, usuario_id)
                    except NotImplementedError as erro:
                        print(str(erro))
            if not encontrada:
                print("Opção inválida. Escolha um código listado.")
    except (EOFError, KeyboardInterrupt):
        print("\nSessão encerrada.")
