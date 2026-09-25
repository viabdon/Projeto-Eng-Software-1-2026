from app.funcionalidades.grupos.tela_c01 import executar as tela_c01
from app.funcionalidades.grupos.tela_c02 import executar as tela_c02
from app.funcionalidades.descoberta.tela_c03 import executar as tela_c03
from app.funcionalidades.descoberta.tela_c04 import executar as tela_c04
from app.funcionalidades.descoberta.tela_c05 import executar as tela_c05
from app.funcionalidades.participacao.tela_c06 import executar as tela_c06
from app.funcionalidades.encontros.tela_c09 import executar as tela_c09
from app.funcionalidades.acompanhamento.tela_c12 import executar as tela_c12
from app.funcionalidades.acompanhamento.tela_c13 import executar as tela_c13
from app.funcionalidades.materiais.tela_c10 import executar as tela_c10
from app.funcionalidades.chat.tela_c11 import executar as tela_c11
from app.funcionalidades.estudos.tela_c07 import executar as tela_c07
from app.funcionalidades.estudos.tela_c08 import executar as tela_c08
from app.funcionalidades.simulados.tela_c14 import executar as tela_c14

OPCOES = [
    ("01", "Criar grupo de estudo", tela_c01),
    ("02", "Configurar características do grupo", tela_c02),
    ("03", "Procurar grupos por matéria", tela_c03),
    ("04", "Filtrar grupos encontrados", tela_c04),
    ("05", "Visualizar detalhes do grupo", tela_c05),
    ("06", "Solicitar participação no grupo", tela_c06),
    ("07", "Definir Tarefas e Metas de Estudo (em um grupo)", tela_c07),
    ("08", "Receber Avaliação e Feedback de Grupos e Monitores", tela_c08),
    ("09", "Marcar e alterar horário de encontro", tela_c09),
    ("10", "Upload e Download de material de estudo", tela_c10),
    ("11", "Chat do Grupo", tela_c11),
    ("12", "Receber aviso de nova tarefa", tela_c12),
    ("13", "Acessar painel de grupos", tela_c13),
    ("14", "Simulados gerados por IA", tela_c14),
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
            if escolha.isdigit():
                escolha = escolha.zfill(2)
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
