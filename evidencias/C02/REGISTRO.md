# Evidências — C02

Status: **cenários locais executados; integração e prints visuais pendentes**.

| Cenário | Esperado | Observado | Resultado | Executor | Data | Commit | Print |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C02-S1 | Três campos persistem na sessão, grupo fica ativo e pesquisável. | `python3 main.py` configurou o grupo 5; a tela mostrou descrição `Revisão de listas`, privacidade `publico`, modalidade `online` e `Ativo: True`. O teste de contrato confirmou o mesmo registro, limite e vínculo preservados. Busca não verificada: C03 ainda está em stub. | Passou localmente; busca e print pendentes | Codex | 2026-09-29 | `af9fc3b` | Pendente: a ferramenta de UI bloqueou acesso ao Terminal por segurança. |
| C02-F1 | Modalidade obrigatória/válida é informada; grupo continua inativo, sem alteração parcial. | A interface rejeitou modalidade vazia e `hibrida` com a mensagem `A modalidade deve ser online ou presencial.`; os testes de contrato confirmaram estado sem alteração. | Passou localmente; print pendente | Codex | 2026-09-29 | `af9fc3b` | Pendente: a ferramenta de UI bloqueou acesso ao Terminal por segurança. |
| C02-F2 | Acesso negado por não ser criador. | Como Bruno (2), a interface mostrou `Somente o criador pode configurar este grupo.`; o teste de contrato confirmou estado sem alteração. | Passou localmente; print pendente | Codex | 2026-09-29 | `af9fc3b` | Pendente: a ferramenta de UI bloqueou acesso ao Terminal por segurança. |

Verificações executadas em Python 3.14.6 porque `python3.12` não está instalado neste ambiente (o alvo do projeto continua sendo Python 3.12). Seis testes temporários de contrato passaram, e os três cenários acima foram percorridos por `python3 main.py` com dados fictícios. A tela de busca do C03 não está implementada nesta branch, então a disponibilidade para pesquisa ainda precisa ser verificada na integração.

Os prints reais ainda precisam ser capturados e anexados ao card original do Trello. A ferramenta de UI recusou abrir o Terminal por segurança; nenhuma imagem foi fabricada ou registrada como evidência.
