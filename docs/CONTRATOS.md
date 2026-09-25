# Contratos compartilhados

Leia [arquitetura](ARQUITETURA.md) primeiro. Estes nomes são a base congelada da Sprint. Alterações devem ser centralizadas por Pablo para não quebrar o trabalho das outras pessoas.

## Estado e retornos

`carregar_estado()` devolve um dicionário com uma entrada para cada JSON de `dados/`. Exemplo: `estado["grupos"]` é uma lista; `grupo["nome"]` é o nome de um registro. O estado é o mesmo objeto passado a todas as telas durante a sessão.

As regras retornam `{"ok": True, "mensagem": "...", "dados": registro_ou_lista}` em sucesso, e `{"ok": False, "mensagem": "motivo", "dados": None}` em rejeição. Consulta sem resultados pode retornar sucesso técnico, com lista vazia e mensagem do cenário alternativo. Não confundir cenário de falha do BDD com falha do programa.

IDs são inteiros positivos, exclusivos dentro de cada coleção. `buscar_por_id(lista, id)` retorna registro ou `None`; `proximo_id(lista)` fornece o próximo inteiro. `buscar_vinculo(estado, usuario_id, grupo_id)` retorna vínculo ou `None`.

Textos obrigatórios devem ser tratados com `strip()`. Datas são strings ISO `AAAA-MM-DDTHH:MM`, convertidas com `datetime.fromisoformat` antes de comparar. Todas usam o mesmo horário local de demonstração, sem fuso ou horário de verão. `agora(estado)` é a única fonte de data atual: `2026-09-25T10:00` por padrão.

## Coleções e quem as modifica

As chaves abaixo são obrigatórias. Valores `None` aparecem como `null` nos JSONs. Uma lista vazia `[]` não significa que o contrato ainda está indefinido.

| Coleção | Campos de cada registro | Escrita |
| --- | --- | --- |
| usuarios | id, nome | Base fixa |
| materias | Lista de strings: Python, Matemática | Base fixa |
| grupos | id, nome, materia, objetivo, limite, criador_id, descricao, modalidade, privacidade, ativo | C27 cria; C28 configura |
| vinculos | id, grupo_id, usuario_id, papel (`monitor` ou `membro`) | C27 cria fundador; C32 admite; C33 remove vínculo ao sair |
| solicitacoes | id, grupo_id, usuario_id, status (`pendente` ou `aceita`), criado_em | C32 |
| atividades | id, grupo_id, criador_id, tipo (`tarefa` ou `meta`), escopo (`pessoal` ou `grupo`), titulo, descricao, objetivo, inicio, prazo | C26 |
| atribuicoes | id, atividade_id, usuario_id, status (`pendente` ou `concluida`), concluida_em (string ou None) | C26 |
| avaliacoes | id, atribuicao_id, monitor_id, nota (número 0–10), feedback, criado_em, lida (bool) | C19 |
| preferencias | id, usuario_id, grupo_id, ativo (bool), tipos (lista de strings) | C09; C33 remove ao sair |
| eventos | id, grupo_id, tipo, texto, destinatarios (lista de IDs), criado_em, chave (string única) | Helper da base, chamado pelos produtores |
| leituras | id, evento_id, usuario_id | C09 |
| encontros | id, grupo_id, criador_id, inicio, local | C37 |
| materiais | id, grupo_id, autor_id, nome, caminho (relativo à pasta da sessão), tamanho (bytes), criado_em | C36 |
| mensagens | id, grupo_id, autor_id, texto, criado_em | C38 |
| questoes | id, materia, enunciado, alternativas (lista de textos), correta (`A`, `B` ou `C`) | Fixture do C39 |
| resposta_ia_invalida | Retorno mock propositalmente sem campos obrigatórios | Fixture do C39 |
| simulados | id, usuario_id, materia, questoes (cópia validada), respostas (lista de questao_id/alternativa), status (`aberto` ou `entregue`), acertos (None antes da entrega) | C39 |

`configuracao` é um objeto com `agora`, `bloqueio_notificacoes` e `chat_indisponivel`. `estado["_runtime"]` é um `pathlib.Path` adicionado pelo carregador e não deve ser serializado.

Mesmo quando dois cards escrevem na mesma coleção, eles editam arquivos Python distintos. As alterações de dados ocorrem no programa, não em um JSON compartilhado por todas as branches.

## Saídas de consulta que integram módulos

- `buscar_grupos(estado, materia)` e `filtrar_grupos(grupos_encontrados, modalidade, privacidade)` retornam `dados` como lista de registros de grupos. Filtro recebe exatamente a lista da busca. Não mudar seus registros.
- `detalhar_grupo(estado, grupo_id)` retorna em `dados`: id, nome, materia, descricao, objetivo, modalidade, privacidade, participantes, limite, vagas. Grupo inativo/inexistente retorna rejeição; lotado retorna detalhes com vagas=0 e mensagem de indisponibilidade para entrada.
- `obter_painel(estado, usuario_id)` retorna lista de objetos: grupo_id, nome, ativo, tarefas_pendentes (inteiro, inclui metas), avisos_nao_lidos (inteiro), proximo_encontro (registro ou None), materiais_recentes (lista de até três registros). Ordenar os materiais por criado_em decrescente e desempatar por ID decrescente.
- `listar_atividades` retorna lista de objetos com atividade, atribuicao e nova_avaliacao (bool: existe avaliação não lida dessa atribuição). Um membro vê as próprias atribuições; monitor vê as do grupo. A tela deve deixar claro a quem pertence cada atribuição e indicar novo feedback ao destinatário, orientando abrir a opção 19 para ler.
- `listar_avaliacoes` retorna lista de objetos com avaliacao, atividade e usuario_id. É o histórico do usuário atual, com nota/feedback e indicador de leitura.
- `listar_avisos` retorna lista de objetos com evento e lido (bool), apenas para destinatário que ainda tenha vínculo. Grupo inativo pode ter histórico, mas não pode habilitar novos avisos.
- `listar_materiais` e `listar_mensagens` retornam listas de seus registros. Arquivos e mensagens privados exigem vínculo atual.
- `baixar_material` retorna `dados={"caminho": str(destino)}` após verificar a cópia; `entregar` retorna o simulado com acertos preenchidos.
- Outras criações/edições retornam o registro criado/alterado. `concluir_atividade` retorna a atribuição; `sair_grupo` retorna `dados={"grupo_id": grupo_id}`. O retorno não substitui a alteração no estado compartilhado.

## Eventos, avisos e integração sem espera

O helper `registrar_evento(estado, grupo_id, tipo, texto, destinatarios, chave)` já está disponível. Ele registra o evento imediatamente, ignora repetições da mesma chave e aplica preferências no instante da emissão. O chamador deve validar sua operação e o grupo antes de usá-lo.

Sem preferência cadastrada, considerar todos os quatro tipos habilitados. C09 pode criar preferência explícita para desativar ou escolher tipos. O helper captura IDs elegíveis; alterações posteriores na preferência não reentregam eventos antigos. Leituras ficam em uma coleção separada para não modificar o aviso dos outros.

| Produtor | Tipo | Destinatários | Chave |
| --- | --- | --- | --- |
| C26 após criar tarefa ou meta | nova_tarefa | Pessoas atribuídas, ainda participantes | `atividade:<id>` |
| C36 após copiar material e salvar metadados | novo_material | Todos os membros atuais | `material:<id>` |
| C37 após alteração efetiva de encontro | alteracao_encontro | Todos os membros atuais | `encontro:<id>:alteracao:<numero>` |
| C09 ao abrir avisos no dia de encontro futuro | lembrete_encontro | Todos os membros atuais | `lembrete:<id>:<inicio>` |

Para C37, obter o número de alteração contando eventos existentes daquele encontro e acrescentando 1. Não emitir quando data/local não mudarem. Não usar só o minuto da alteração como chave, pois duas edições podem ocorrer no mesmo minuto.

Aviso de avaliação é o campo `lida=False` no histórico C19, não um quinto tipo de notificação. C33 lê eventos e leituras existentes; C09 gera os lembretes ao abrir a caixa. Sem push no sistema operacional.

## Arquivos e isolamento da sessão

O carregador cria `runtime/sessao_<identificador>/`, expõe esse diretório em `_runtime` e copia o material inicial para a nuvem simulada. As pastas `nuvem/` e `downloads/` ficam dentro dele. Reiniciar cria outra pasta; não apagar recursivamente diretórios para reiniciar um teste. Todo `runtime/` é ignorado pelo Git.

C36 deve armazenar caminhos relativos à pasta da sessão; só copiar para dentro dela e usar `Path(caminho_origem).name` ao montar o nome do destino. O nome original pode vir de um caminho absoluto informado voluntariamente pelo usuário. Não enviar arquivos privados nos testes: usar `amostras/`.

## Fixtures para começar sem esperar outra pessoa

| Item | Conteúdo útil |
| --- | --- |
| Ana, ID 1 | Monitora/criadora dos grupos 1, 4 e 5 |
| Bruno, ID 2 | Membro dos grupos 1 e 3 |
| Carla, ID 3 | Monitora dos grupos 2 e 3; não participa do grupo 1 |
| Diego, ID 4 | Não participa de grupo algum no início |
| Grupo 1 | Python, online, público, ativo; 2 de 5 vagas ocupadas |
| Grupo 2 | Python, presencial, privado, ativo; 1 de 3 vagas ocupadas |
| Grupo 3 | Matemática, online, público, ativo; lotado, 2 de 2 |
| Grupo 4 | Inativo, usado para falhas |
| Grupo 5 | Rascunho pronto para C28 configurar |
| Atividade 1 / atribuições 1 e 2 | Tarefa futura pendente de Bruno e Ana |
| Atividade 2 / atribuição 3 | Tarefa concluída por Bruno, ainda não avaliada |
| Atividade 3 / atribuição 4 | Meta expirada de Bruno, ainda pendente e sem avaliação |
| Evento 1 | Aviso de tarefa para Ana e Bruno, não lido |
| Encontro 1 | Grupo 1, criador Bruno, 25/09/2026 às 14h, Sala 10 |
| Material 1 | Texto fictício do grupo 1, copiado ao iniciar |
| Questões 1–3 | Python, respostas corretas A, B e C |

Para simular as flags de falha, alterar `estado["configuracao"]` apenas na sessão de teste via console Python, ou usar uma cópia local do JSON sem incluí-la no commit. A receita exata está em TESTES.md.
