"""Carrega dados fictícios; cada execução recebe pasta própria de arquivos."""
import json
import shutil
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def carregar_estado():
    estado = {}
    for arquivo in sorted((RAIZ / "dados").glob("*.json")):
        with arquivo.open(encoding="utf-8") as entrada:
            estado[arquivo.stem] = json.load(entrada)
    runtime = RAIZ / "runtime"
    runtime.mkdir(exist_ok=True)
    sessao = Path(tempfile.mkdtemp(prefix="sessao_", dir=runtime))
    estado["_runtime"] = sessao
    for material in estado["materiais"]:
        destino = sessao / material["caminho"]
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ / "amostras" / material["nome"], destino)
        material["tamanho"] = destino.stat().st_size
    return estado
