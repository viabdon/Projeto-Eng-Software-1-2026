# Evidências — C04

Status: **executado com validação automatizada**. Resultado verificado com a suíte de testes do módulo.

| Cenário | Esperado | Observado | Resultado | Executor | Data | Commit | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C04-S1 | Somente grupo 1; limpar filtros restaura grupos 1 e 2. | Filtragem com `online + publico` retornou apenas o grupo 1. A lista original foi preservada. | Sucesso | Copilot | 2026-09-29 | local | Não gerado: execução em terminal de validação |
| C04-F1 | Nenhuma opção compatível, sem reutilizar resultados anteriores. | Requisição de `presencial + publico` retornou lista vazia com sucesso técnico e sem mutação. | Sucesso | Copilot | 2026-09-29 | local | Não gerado: execução em terminal de validação |
| C04-F2 | Filtro inválido recusado, lista original intacta. | Modalidade com valor inválido retornou `ok=False` e manteve a lista original inalterada. | Sucesso | Copilot | 2026-09-29 | local | Não gerado: execução em terminal de validação |

> Evidência anotada a partir da execução do comando `py -3.11 -m unittest discover -s tests -v`, que validou 5 cenários do C03/C04 com sucesso.

Anexar os prints reais também ao card original do Trello; não basta deixar a pasta no GitHub. Usar dados fictícios e evitar credenciais nos prints.
