"""Entrada do protótipo. Execute a partir da raiz: python main.py."""
from app.base.dados import carregar_estado
from app.menu import executar

if __name__ == "__main__":
    executar(carregar_estado())
