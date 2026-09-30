"""Interface de terminal do C10. Proprietário: Enrique Araújo."""

from pathlib import Path
from app.funcionalidades.materiais.c10 import enviar_material, listar_materiais, baixar_material


def executar(estado, usuario_id):
    """Interface interativa de terminal para upload, listagem e download de materiais."""
    print("\n--- C10: Material de Estudo (Nuvem Simulada) ---")
    print("1. Enviar Material (Monitor)")
    print("2. Listar Materiais do Grupo")
    print("3. Baixar Material")
    print("0. Voltar")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        try:
            grupo_id = int(input("Informe o ID do grupo: ").strip())
        except ValueError:
            print("Erro: ID do grupo inválido.")
            return

        caminho_origem = input("Informe o caminho local do arquivo: ").strip()
        resultado = enviar_material(estado, usuario_id, grupo_id, caminho_origem)
        print(f"\n[{'OK' if resultado['ok'] else 'FALHA'}] {resultado['mensagem']}")
        if resultado["ok"] and resultado["dados"]:
            mat = resultado["dados"]
            print(f"ID: {mat['id']} | Nome: {mat['nome']} | Caminho: {mat['caminho']} | Tamanho: {mat['tamanho']} bytes")

    elif opcao == "2":
        try:
            grupo_id = int(input("Informe o ID do grupo: ").strip())
        except ValueError:
            print("Erro: ID do grupo inválido.")
            return

        resultado = listar_materiais(estado, usuario_id, grupo_id)
        print(f"\n[{'OK' if resultado['ok'] else 'FALHA'}] {resultado['mensagem']}")
        if resultado["ok"] and resultado["dados"]:
            print("\nMateriais encontrados:")
            for mat in resultado["dados"]:
                print(f" - ID: {mat['id']} | Nome: {mat['nome']} | Tamanho: {mat['tamanho']} bytes | Data: {mat['criado_em']}")

    elif opcao == "3":
        try:
            material_id = int(input("Informe o ID do material: ").strip())
        except ValueError:
            print("Erro: ID do material inválido.")
            return

        resultado = baixar_material(estado, usuario_id, material_id)
        print(f"\n[{'OK' if resultado['ok'] else 'FALHA'}] {resultado['mensagem']}")
        if resultado["ok"] and resultado["dados"]:
            caminho_dest = Path(resultado["dados"]["caminho"])
            print(f"Caminho de destino: {caminho_dest}")
            if caminho_dest.exists():
                print(f"Verificação de integridade: Arquivo copiado com sucesso! Tamanho: {caminho_dest.stat().st_size} bytes.")
                try:
                    conteudo_prev = caminho_dest.read_text(encoding="utf-8", errors="ignore")[:100]
                    print(f"Prévia do conteúdo: {conteudo_prev}...")
                except Exception:
                    print("Prévia indisponível (arquivo binário ou ilegível em modo texto).")

    elif opcao == "0":
        return
    else:
        print("Opção inválida.")