"""Apoio simples para trabalhar com listas de registros."""

def buscar_por_id(registros, registro_id):
    for registro in registros:
        if registro["id"] == registro_id:
            return registro
    return None


def proximo_id(registros):
    maior = 0
    for registro in registros:
        if registro["id"] > maior:
            maior = registro["id"]
    return maior + 1


def buscar_vinculo(estado, usuario_id, grupo_id):
    for vinculo in estado["vinculos"]:
        if vinculo["usuario_id"] == usuario_id and vinculo["grupo_id"] == grupo_id:
            return vinculo
    return None
