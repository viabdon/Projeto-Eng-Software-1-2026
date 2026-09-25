"""Relógio fixo e explícito para testes manuais reproduzíveis."""
from datetime import datetime


def agora(estado):
    return datetime.fromisoformat(estado["configuracao"]["agora"])
