# Arquitetura — Comunidade de Estudos

Definida antes do detalhamento das tasks. Fonte: os 14 cards de **Backlog Ready** do [quadro da equipe](https://trello.com/b/I49Fyzvl), consultados em 25/09/2026. O arquivo inicialmente fornecido era HTML; a leitura válida foi feita no quadro autenticado. As etiquetas de atribuição anteriores foram desconsideradas, conforme solicitado.

## Escolha e limites

Python 3.12, biblioteca padrão, aplicação local com menu de terminal. Não há instalação de bibliotecas. O terminal é a interface mínima para inserir dados, escolher usuários fictícios, visualizar resultados e tirar prints. As regras ficam separadas da interface para que o código possa ser reutilizado.

Os JSONs são fixtures: dados iniciais fictícios carregados na memória ao abrir o programa. O mesmo estado é passado para todos os módulos durante uma execução. Reiniciar limpa as alterações em memória. Não há gravação concorrente em JSON, banco de dados ou múltiplos processos.

O objetivo é planejar e entregar a base para o time implementar os cards. Arquivos com `NotImplementedError` são pontos de implementação, não funcionalidades concluídas. Nenhum card ou teste funcional está marcado como Done nesta entrega.

| Recurso do backlog | Adaptação mínima proposta para esta Sprint |
| --- | --- |
| Usuário autenticado | Seleção de usuário fictício no menu; vínculo e papel continuam sendo validados |
| Tela, aba ou painel | Opção de menu com listagem legível no terminal |
| Armazenamento em nuvem (#36) | Cópia real de arquivo para `runtime/nuvem/` e download para `runtime/downloads/`; indicar “nuvem simulada” |
| IA (#39) | Provedor mock que devolve questões prontas; validar resposta e simular resposta inválida; indicar “IA simulada” |
| Chat (#38) | Histórico em memória e envio sequencial; trocar usuário para demonstrar conversa; sem tempo real |
| Notificações (#9) | Caixa de avisos dentro da aplicação, alimentada imediatamente por eventos locais; sem push ou e-mail |
| Permissão do celular | Flag fictícia de bloqueio de notificações e grupo inativo para simular a exceção |
| Lembretes | Verificação ao abrir a caixa de avisos; sem agendador em segundo plano |

Essas adaptações se apoiam na autorização do usuário para um MVP com dados mockados. Não alegar IA, nuvem, autenticação ou push reais na apresentação. Se a avaliação exigir essas integrações reais, será necessário rever o escopo; elas não estão nesta Sprint.

## Estrutura e propriedade dos arquivos

```text
Projeto-Eng-Software-1-2026/     nome do repositório e da pasta local
main.py                         entrada: python main.py
app/
  menu.py                       menu central e seleção de usuário
  base/
    dados.py                    carregar JSONs
    consulta.py                 buscar registro e próximo ID
    eventos.py                  registrar aviso e destinatários no momento do evento
    relogio.py                  relógio de demonstração
  funcionalidades/
    grupos/                     Renan: cards 27 e 28
    descoberta/                 Bernardo: cards 29, 30 e 31
    participacao/               Alexandre: card 32
    encontros/                  Alexandre: card 37
    acompanhamento/             Rafael: cards 9 e 33
    materiais/                  Enrique: card 36
    chat/                       Enrique: card 38
    estudos/                    Pablo: cards 26 e 19
    simulados/                  Pablo: card 39
dados/                          fixtures compartilhadas e estáveis
amostras/                       arquivos fictícios de estudo
docs/
  ARQUITETURA.md
  CONTRATOS.md
  PLANEJAMENTO.md
  GUIA-DO-TIME.md
  TESTES.md
  cards/Cxx.md                  uma task detalhada por card original
evidencias/Cxx/                 roteiro e prints por card
runtime/sessao_<id>/             arquivos por execução; ignorado pelo Git
```

Em cada pasta funcional, cada card possui `cXX.py` (regras) e `tela_cXX.py` (entrada e saída). Assim, até cards da mesma pessoa podem ser entregues em branches separadas sem disputar arquivos.

`menu.py`, arquivos de base, contratos e fixtures comuns são integrados por Pablo. Isso é responsabilidade de integração, não um card adicional para a contagem mínima.

## Fluxo e contratos

`main.py → menu.py → tela_cXX.executar(estado, usuario_id) → cXX.função(...)`.

- Funções de negócio recebem `estado` explicitamente. Não usar estado global nem recarregar JSON dentro da operação.
- `estado` é um dicionário cujos valores são listas de registros. O guia explica os poucos acessos necessários; não se espera conhecimento prévio de dicionários.
- Registros são dicionários com campos definidos em `CONTRATOS.md`. Procurar registros com `buscar_por_id` e laços simples.
- Cada função retorna `{"ok": True/False, "mensagem": "...", "dados": ...}`. A interface imprime mensagem e dados de forma legível. `False` representa uma rejeição esperada, não uma exceção de Python.
- Primeiro validar todos os dados e permissões; depois alterar o estado. Uma operação recusada não modifica registros, arquivos ou eventos.
- Cada `tela_cXX.py` pertence ao card correspondente. O menu central já referencia todos os pontos de entrada; não exige edição por cada participante.
- Operações produtoras chamam `registrar_evento` da base. A caixa de avisos lê esses eventos sem importar o módulo que criou a tarefa, encontro ou material. Não há fila, servidor ou processamento assíncrono.
- Módulos podem consultar diretamente coleções estáveis do estado. Chamadas entre cards são restritas aos contratos documentados: filtro após busca e painel abrindo detalhes. As fixtures permitem trabalhar antes desses merges.

## Regras adotadas onde o quadro deixa escolhas abertas

1. O criador entra como monitor do próprio grupo. Os papéis são por grupo, não globais.
2. O card 27 cria grupo inativo, ainda em configuração. O card 28 valida descrição, modalidade e privacidade e o ativa. Isso concilia os critérios de cadastro do 27 com seu BDD, que descreve configuração e se sobrepõe ao 28.
3. Modalidades: `online` e `presencial`. Privacidade: `publico` e `privado`. Filtros do 30 usam esses dois campos; não acrescentar localização, reputação ou recomendação.
4. Grupo público aceita entrada imediatamente; grupo privado registra pedido pendente. A tela de aprovação não existe nos 14 cards e fica fora da Sprint. Pendentes não ocupam vaga nem recebem conteúdo de participante.
5. Só monitores publicam materiais e avaliações; membros podem baixar materiais, conversar e criar metas pessoais. Qualquer participante pode marcar encontro e alterar o encontro que criou; outro participante recebe rejeição.
6. Sair do grupo remove o vínculo, mantendo histórico. Impedir saída do último monitor para evitar grupo sem responsável. A interface oferece confirmação simples antes da saída.
7. Não permitir conclusão de atividade após o prazo. Avaliação fica disponível após conclusão individual OU término do prazo; avaliar uma pessoa não conclui a tarefa das demais.
8. Um simulado tem três questões de múltipla escolha; correção simples com número de acertos. Não usar LLM, API paga ou geração de PDF.
9. Materiais aceitam `.txt` e `.pdf`, no máximo 1 MiB por arquivo e 5 MiB por grupo, para dar um limite concreto ao critério de espaço disponível. Não interpretar o conteúdo dos PDFs.
10. O relógio de demonstração é fixo em `2026-09-25 10:00`. Todas as regras de prazo usam `agora(estado)`, evitando fixtures que deixam de funcionar no dia da apresentação.

Essas são decisões do planejamento, não transcrições de requisitos que o Trello não especificou.

## Estratégia para evitar conflitos e espera

Congelar esta base antes de criar branches funcionais. Cada pessoa altera somente os arquivos relacionados em seu card e sua pasta de evidências. Fixtures pessoais opcionais ficam em `dados_extras/Cxx/` e não mudam o carregador central; para demonstração integrada, Pablo incorpora os dados necessários nas fixtures comuns.

Cards dependentes usam registros prontos durante o desenvolvimento. Um card pode ser desenvolvido em paralelo, mas só vai para Done após testar suas ligações com os produtores reais. Ordem de integração e dependências ficam no planejamento. Os 14 cards continuam rastreáveis por ID e link original, sem criar funcionalidades para inflar a contagem.
