# Arquitetura — Comunidade de Estudos

Definida antes do detalhamento das tasks. Fonte: os 14 cards de **Backlog Ready** do [quadro da equipe](https://trello.com/b/I49Fyzvl), consultados em 25/09/2026. A distribuição dos cards está definida em PLANEJAMENTO.md.

## Escolha e limites

Python 3.12, biblioteca padrão, aplicação local com menu de terminal. Não há instalação de bibliotecas. O terminal é a interface mínima para inserir dados, escolher usuários fictícios, visualizar resultados e tirar prints. As regras ficam separadas da interface para que o código possa ser reutilizado.

Os JSONs são fixtures: dados iniciais fictícios carregados na memória ao abrir o programa. O mesmo estado é passado para todos os módulos durante uma execução. Reiniciar limpa as alterações em memória. Não há gravação concorrente em JSON, banco de dados ou múltiplos processos.

O objetivo é planejar e entregar a base para o time implementar os cards. Arquivos com `NotImplementedError` são pontos de implementação, não funcionalidades concluídas. Nenhum card ou teste funcional está marcado como Done nesta entrega.

| Recurso do backlog | Adaptação mínima proposta para esta Sprint |
| --- | --- |
| Usuário autenticado | Seleção de usuário fictício no menu; vínculo e papel continuam sendo validados |
| Tela, aba ou painel | Opção de menu com listagem legível no terminal |
| Armazenamento em nuvem (C10) | Cópia real de arquivo para `runtime/nuvem/` e download para `runtime/downloads/`; indicar “nuvem simulada” |
| IA (C14) | Provedor mock que devolve questões prontas; validar resposta e simular resposta inválida; indicar “IA simulada” |
| Chat (C11) | Histórico em memória e envio sequencial; trocar usuário para demonstrar conversa; sem tempo real |
| Notificações (C12) | Caixa de avisos dentro da aplicação, alimentada imediatamente por eventos locais; sem push ou e-mail |
| Permissão do celular | Flag fictícia de bloqueio de notificações e grupo inativo para simular a exceção |
| Lembretes | Verificação ao abrir a caixa de avisos; sem agendador em segundo plano |

O escopo do MVP utiliza dados mockados e simulações locais. Não alegar IA, nuvem, autenticação ou push reais na apresentação. Se a avaliação exigir essas integrações reais, será necessário rever o escopo; elas não estão nesta Sprint.

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
    grupos/                     Renan: cards C01 e C02
    descoberta/                 Bernardo: cards C03, C04 e C05
    participacao/               Alexandre: card C06
    encontros/                  Alexandre: card C09
    acompanhamento/             Rafael: cards C12 e C13
    materiais/                  Enrique: card C10
    chat/                       Enrique: card C11
    estudos/                    Pablo: cards C07 e C08
    simulados/                  Pablo: card C14
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
- `estado` é um dicionário cujos valores são listas de registros. Os campos e exemplos de acesso estão descritos no guia de implementação.
- Registros são dicionários com campos definidos em `CONTRATOS.md`. Procurar registros com `buscar_por_id` e laços simples.
- Cada função retorna `{"ok": True/False, "mensagem": "...", "dados": ...}`. A interface imprime mensagem e dados de forma legível. `False` representa uma rejeição esperada, não uma exceção de Python.
- Primeiro validar todos os dados e permissões; depois alterar o estado. Uma operação recusada não modifica registros, arquivos ou eventos.
- Cada `tela_cXX.py` pertence ao card correspondente. O menu central já referencia todos os pontos de entrada; não exige edição por cada participante.
- Operações produtoras chamam `registrar_evento` da base. A caixa de avisos lê esses eventos sem importar o módulo que criou a tarefa, encontro ou material. Não há fila, servidor ou processamento assíncrono.
- Módulos podem consultar diretamente coleções estáveis do estado. Chamadas entre cards são restritas aos contratos documentados: filtro após busca e painel abrindo detalhes. As fixtures permitem trabalhar antes desses merges.

## Regras adotadas onde o quadro deixa escolhas abertas

1. O criador entra como monitor do próprio grupo. Os papéis são por grupo, não globais.
2. O card C01 cria grupo inativo, ainda em configuração. O card C02 valida descrição, modalidade e privacidade e o ativa. Isso concilia os critérios de cadastro do C01 com o BDD, que descreve configuração e se sobrepõe ao C02.
3. Modalidades: `online` e `presencial`. Privacidade: `publico` e `privado`. Filtros do C04 usam esses dois campos; não acrescentar localização, reputação ou recomendação.
4. Grupo público aceita entrada imediatamente; grupo privado registra pedido pendente. A tela de aprovação não existe nos 14 cards e fica fora da Sprint. Pendentes não ocupam vaga nem recebem conteúdo de participante.
5. Só monitores publicam materiais e avaliações; membros podem baixar materiais, conversar e criar metas pessoais. Qualquer participante pode marcar encontro e alterar o encontro que criou; outro participante recebe rejeição.
6. Sair do grupo remove o vínculo, mantendo histórico. Impedir saída do último monitor para evitar grupo sem responsável. A interface oferece confirmação simples antes da saída.
7. Não permitir conclusão de atividade após o prazo. Avaliação fica disponível após conclusão individual OU término do prazo; avaliar uma pessoa não conclui a tarefa das demais.
8. Um simulado tem três questões de múltipla escolha; correção simples com número de acertos. Não usar LLM, API paga ou geração de PDF.
9. Materiais aceitam `.txt` e `.pdf`, no máximo 1 MiB por arquivo e 5 MiB por grupo, para dar um limite concreto ao critério de espaço disponível. Não interpretar o conteúdo dos PDFs.
10. O relógio de demonstração é fixo em `2026-09-25 10:00`. Todas as regras de prazo usam `agora(estado)`, evitando fixtures que deixam de funcionar no dia da apresentação.

Essas são decisões do planejamento, não transcrições de requisitos que o Trello não especificou.

## Estratégia para evitar conflitos e espera

Congelar esta base antes de criar branches funcionais. Cada pessoa altera somente os arquivos relacionados no card e na pasta de evidências correspondente. Fixtures pessoais opcionais ficam em `dados_extras/Cxx/` e não mudam o carregador central; para demonstração integrada, Pablo incorpora os dados necessários nas fixtures comuns.

Cards dependentes usam registros prontos durante o desenvolvimento. Um card pode ser desenvolvido em paralelo, mas só vai para Done após testar as ligações com os produtores reais. Ordem de integração e dependências ficam no planejamento. Os 14 cards continuam rastreáveis por ID e link original, sem criar funcionalidades para inflar a contagem.
