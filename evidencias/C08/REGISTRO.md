# Evidências — C08

Status: **verificações locais passaram; teste manual e prints ainda pendentes**.

| Cenário | Esperado | Observado | Resultado | Executor | Data | Commit | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C08-S1 | Avaliação salva e associada ao usuário, grupo e atividade corretos. | Chamada local registrou avaliação #1 da atribuição #3, nota 8, feedback informado, monitor Ana, data fixa e `lida=False`. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |
| C08-S2 | Área de tarefas indica Nova avaliação; histórico mostra nota/texto e marca lida após abrir; ao retornar à opção 07 o indicador some. | Integração C07/C08 indicou nova avaliação da atribuição #3 para Bruno; leitura mudou `lida` para `True` e removeu o indicador. A tela C08 foi percorrida com entradas simuladas. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |
| C08-S3 | Avaliação permitida por prazo encerrado; não altera status da atribuição. | Atribuição #4 da meta expirada recebeu nota 7,5 e continuou `pendente`. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |
| C08-S4 | Duas avaliações com as respectivas atividades e feedbacks. | Na mesma instância do estado, o histórico de Bruno continha as avaliações das atribuições #3 e #4. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |
| C08-F1 | Informa que ainda não existe avaliação; não inventa feedback. | Estado inicial devolveu lista vazia e mensagem de ausência de avaliações. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |
| C08-F2 | Somente monitor autorizado pode avaliar. | Bruno não conseguiu avaliar a atribuição #2; a lista de avaliações permaneceu inalterada. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |
| C08-F3 | Atividade ainda indisponível para avaliação; sem registro novo. | Ana não conseguiu avaliar a atribuição #1 pendente com prazo futuro; nenhum registro foi criado. | Passou localmente; print pendente | Codex | 2026-09-29 | Ver commit do C08 | Pendente |

Anexar os prints reais também ao card original do Trello; não basta deixar a pasta no GitHub. Usar dados fictícios e evitar credenciais nos prints.

Verificações locais executadas com Python 3.12.10 e entradas simuladas no terminal. Os cenários manuais e as capturas de tela ainda precisam ser feitos no aplicativo em execução antes de mover o card para Backlog Done.
