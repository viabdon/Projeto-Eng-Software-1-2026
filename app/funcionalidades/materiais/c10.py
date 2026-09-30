"""C10 — Upload e Download de material de estudo. Ver docs/cards/C10.md."""

from pathlib import Path
import shutil
from app.base.consulta import buscar_por_id, buscar_vinculo, proximo_id
from app.base.eventos import registrar_evento
from app.base.relogio import agora


def enviar_material(estado, usuario_id, grupo_id, caminho_origem):
    """Subtasks C10.1 a C10.4: Validações, cópia para nuvem e registro de metadados/eventos."""
    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if not grupo or not grupo.get("ativo"):
        return {"ok": False, "mensagem": "Grupo inexistente ou inativo.", "dados": None}

    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if not vinculo or vinculo["papel"] != "monitor":
        return {"ok": False, "mensagem": "Apenas o monitor do grupo pode enviar materiais.", "dados": None}

    origem = Path(caminho_origem)
    if not origem.exists() or not origem.is_file():
        return {"ok": False, "mensagem": "Arquivo de origem não existe ou é inválido.", "dados": None}

    extensao = origem.suffix.lower()
    if extensao not in [".txt", ".pdf"]:
        return {"ok": False, "mensagem": "Extensão não permitida. Envie arquivos .txt ou .pdf.", "dados": None}

    tamanho = origem.stat().st_size
    limite_arquivo = 1 * 1024 * 1024  # 1 MiB
    if tamanho > limite_arquivo:
        return {"ok": False, "mensagem": "O arquivo excede o tamanho máximo permitido de 1 MiB.", "dados": None}

    tamanho_total_grupo = 0
    for mat in estado["materiais"]:
        if mat["grupo_id"] == grupo_id:
            tamanho_total_grupo += mat["tamanho"]

    limite_grupo = 5 * 1024 * 1024  # 5 MiB
    if tamanho_total_grupo + tamanho > limite_grupo:
        return {"ok": False, "mensagem": "Cota máxima de armazenamento do grupo (5 MiB) excedida.", "dados": None}

    novo_id = proximo_id(estado["materiais"])
    nome_original = origem.name
    caminho_relativo = Path("nuvem") / str(grupo_id) / f"{novo_id}_{nome_original}"
    destino_absoluto = estado["_runtime"] / caminho_relativo

    try:
        destino_absoluto.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino_absoluto)
    except OSError:
        return {"ok": False, "mensagem": "Falha de I/O ao copiar o arquivo para o armazenamento simulado.", "dados": None}

    novo_material = {
        "id": novo_id,
        "grupo_id": grupo_id,
        "autor_id": usuario_id,
        "nome": nome_original,
        "caminho": str(caminho_relativo),
        "tamanho": tamanho,
        "criado_em": agora(estado).isoformat(timespec="minutes")
    }
    estado["materiais"].append(novo_material)

    membros_destinatarios = []
    for v in estado["vinculos"]:
        if v["grupo_id"] == grupo_id:
            membros_destinatarios.append(v["usuario_id"])

    registrar_evento(
        estado,
        grupo_id=grupo_id,
        tipo="novo_material",
        texto=f"Novo material disponibilizado: {nome_original}",
        destinatarios=membros_destinatarios,
        chave=f"material:{novo_id}"
    )

    return {"ok": True, "mensagem": "Material enviado com sucesso.", "dados": novo_material}


def listar_materiais(estado, usuario_id, grupo_id):
    """Subtask C10.5: Lista materiais do grupo se o usuário for participante."""
    grupo = buscar_por_id(estado["grupos"], grupo_id)
    if not grupo or not grupo.get("ativo"):
        return {"ok": False, "mensagem": "Grupo inexistente ou inativo.", "dados": None}

    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if not vinculo:
        return {"ok": False, "mensagem": "Apenas membros do grupo podem listar materiais.", "dados": None}

    materiais_grupo = []
    for mat in estado["materiais"]:
        if mat["grupo_id"] == grupo_id:
            materiais_grupo.append(mat)

    return {"ok": True, "mensagem": "Materiais listados com sucesso.", "dados": materiais_grupo}


def baixar_material(estado, usuario_id, material_id):
    """Subtasks C10.5 e C10.6: Baixa material resolvendo o caminho na sessão."""
    material = buscar_por_id(estado["materiais"], material_id)
    if not material:
        return {"ok": False, "mensagem": "Material não encontrado.", "dados": None}

    grupo_id = material["grupo_id"]
    vinculo = buscar_vinculo(estado, usuario_id, grupo_id)
    if not vinculo:
        return {"ok": False, "mensagem": "Apenas participantes do grupo podem baixar o material.", "dados": None}

    origem_absoluta = estado["_runtime"] / material["caminho"]
    if not origem_absoluta.exists() or not origem_absoluta.is_file():
        return {"ok": False, "mensagem": "Arquivo de origem não encontrado no armazenamento.", "dados": None}

    caminho_destino_relativo = Path("downloads") / f"usuario_{usuario_id}" / f"{material['id']}_{material['nome']}"
    destino_absoluto = estado["_runtime"] / caminho_destino_relativo

    try:
        destino_absoluto.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem_absoluta, destino_absoluto)
    except OSError:
        return {"ok": False, "mensagem": "Falha de I/O ao realizar o download do material.", "dados": None}

    return {"ok": True, "mensagem": "Download concluído com sucesso.", "dados": {"caminho": str(destino_absoluto)}}