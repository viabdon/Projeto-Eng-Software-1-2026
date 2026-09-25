# Testes manuais e evidências

Os cenários por card estão em `docs/cards/`; as tabelas para resultados estão em `evidencias/Cxx/REGISTRO.md`. Todos começam como **não executado**. Testar a estrutura inicial não substitui testar o sistema após implementação.

## Preparação reproduzível

Executar `py -3.12 main.py`, selecionar o usuário fictício informado e escolher o número do card no menu. Para recomeçar um cenário independente, sair com 0 e abrir novamente. O relógio de demonstração fica em 25/09/2026 às 10h. Cada execução cria uma pasta própria em runtime; a localização aparece ao iniciar.

Para cenários que pedem continuidade (por exemplo criar uma avaliação e depois consultá-la), manter a mesma sessão e usar U para trocar usuário. Reiniciar apagaria a avaliação em memória.

Para ativar falhas simuladas sem editar fixtures compartilhadas, abrir `py -3.12` na raiz do projeto e executar:

```python
from app.base.dados import carregar_estado
from app.menu import executar
estado = carregar_estado()
estado["configuracao"]["chat_indisponivel"] = True
executar(estado)
```

Para bloqueio de notificações, usar `estado["configuracao"]["bloqueio_notificacoes"] = True` antes de executar. Ao voltar do menu, desligar a flag e chamar executar de novo para verificar recuperação na mesma sessão. O card C14 terá uma opção própria de simular retorno inválido.

Para testar limite de upload, gerar um arquivo fictício de 1 MiB + 1 byte usando o console Python, sem depender de arquivo pessoal:

```python
from pathlib import Path
Path("runtime").mkdir(exist_ok=True)
Path("runtime/grande.txt").write_bytes(b"a" * (1024 * 1024 + 1))
```

Para cota de grupo cheia, no estado isolado de teste definir `estado["materiais"][0]["tamanho"] = 5 * 1024 * 1024` antes de chamar executar. Isso simula a cota já ocupada; deve ser identificado no registro como pré-condição mockada, não como cinco megabytes realmente enviados.

## O que capturar

1. Identificação do cenário e usuário fictício.
2. Entrada usada, opção de menu e resultado na tela; usar duas imagens se não couber.
3. No sucesso com criação/edição, consulta posterior mostrando o registro.
4. Na falha, a mensagem correta e, quando necessário, a consulta que prova ausência de alteração indevida.
5. Em upload/download, mostrar caminho e arquivo local com conteúdo. Em aviso, capturar criação e recebimento na mesma sessão.

Salvar `Cxx-S1.png`, `Cxx-F1.png` etc. na pasta do card; preencher observado, resultado (passou/falhou), executor, data e commit. No Windows, a Ferramenta de Captura pode registrar o terminal. Os prints serão produzidos pelo time após implementar, nunca fabricados a partir deste roteiro.

Um cenário de falha passa quando a aplicação trata corretamente a entrada inválida/indisponibilidade. Se aparecer traceback inesperado ou sucesso sem operação real, o teste falhou. Busca sem resultados é o cenário alternativo pedido no BDD, mesmo que tecnicamente retorne `ok=True`.

## Fluxos integrados antes de encerrar a Sprint

| Fluxo | Sequência na mesma sessão | Verificação |
| --- | --- | --- |
| Grupo até participação | Ana cria C01 → configura C02 → Diego busca C03, filtra C04, consulta C05 e entra C06 → abre painel C13 | Mesmo ID e campos; membro conta uma vez; painel mostra nova participação |
| Atividade até feedback | Ana cria coletiva C07 → Bruno vê aviso C12/painel C13 → conclui a atribuição C07 → Ana avalia C08 → Bruno consulta C08 | Aviso real, prazo correto, conclusão individual e feedback associado à pessoa correta |
| Encontros e avisos | Bruno altera encontro 1 no C09 → Ana abre C12 → Bruno abre C13 | Novo horário/local no painel e aviso único; desativados não recebem |
| Material compartilhado | Ana envia arquivo C10 → Bruno vê C12 e C13 → baixa C10 | Mesmo material, arquivo de destino verificável e aviso sem duplicação |
| Chat e perda de acesso | Bruno envia C11 → Ana lê → Bruno sai C13 → Bruno tenta abrir C11 e baixar C10 | Histórico preservado; acesso de ex-membro negado |
| Grupo privado | Diego solicita grupo 2 C06 e tenta participar de recursos | Pedido pendente confirmado; sem vínculo, conteúdo de participante continua indisponível |
| Simulado | Bruno gera C14, responde e entrega; depois inicia outro em modo inválido | Primeiro retorna resultado, segundo é recusado sem simulado parcial |

Cada responsável executa os testes do card atribuído; Pablo coordena os fluxos integrados com os envolvidos. Compartilhar as imagens pertinentes entre os registros sem afirmar que um único print comprova operações que não aparecem nele.

## Backlog Done

Conferir: critérios atendidos, PR integrado, testes de sucesso e falha executados, tabelas preenchidas e **prints anexados ao card original no Trello**. Um link para o repositório sozinho não satisfaz a exigência de anexar prints. O plano não altera o quadro automaticamente.
