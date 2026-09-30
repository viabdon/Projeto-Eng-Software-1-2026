# Evidências — C03

Status: **executado com validação automatizada**. Resultado verificado com a suíte de testes do módulo.

| Cenário | Esperado | Observado | Resultado | Executor | Data | Commit | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C03-S1 | Grupos ativos 1 e 2 aparecem; 4 e 5 não aparecem. | Busca por `python` retornou somente os grupos 1 e 2, filtrando os inativos. | Sucesso | Copilot | 2026-09-29 | local | Não gerado: execução em terminal de validação |
| C03-F1 | Mensagem Nenhum grupo encontrado; sem traceback e sem lista antiga. | Resultado retornou `ok=True`, `dados=[]` e mensagem `Nenhum grupo encontrado`. | Sucesso | Copilot | 2026-09-29 | local | Não gerado: execução em terminal de validação |
| C03-F2 | Mensagem solicitando matéria; nenhuma mutação. | Entrada vazia retornou `ok=False`, `dados=None` e mensagem solicitando a matéria. | Sucesso | Copilot | 2026-09-29 | local | Não gerado: execução em terminal de validação |

> Evidência anotada a partir da execução do comando `py -3.11 -m unittest discover -s tests -v`, que validou 5 cenários do C03/C04 com sucesso.

Anexar os prints reais também ao card original do Trello; não basta deixar a pasta no GitHub. Usar dados fictícios e evitar credenciais nos prints.
