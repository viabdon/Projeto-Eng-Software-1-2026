# Guia de implementação

1. Ler ARQUITETURA.md, CONTRATOS.md e o arquivo `docs/cards/Cxx.md` correspondente ao card atribuído.
2. Clonar o repositório, abrir a pasta e executar `py -3.12 main.py`. Em Linux/macOS, usar `python main.py` com Python 3.12. Não há pacotes para instalar.
3. Criar uma branch a partir de main atualizada: `git switch main`, `git pull --ff-only`, `git switch -c codex/cxx`. Executar cada comando separadamente e substituir `xx` pelo número do card, de `01` a `14`.
4. Implementar as funções declaradas em `cxx.py`, preservando nomes e parâmetros. Implementar a tela correspondente em `tela_cxx.py`, já vinculada ao menu principal.
5. Executar os cenários do card, registrar resultados e capturar os prints. Incluir no commit apenas os arquivos atribuídos ao card; abrir um PR para main com a identificação do card e dos testes executados.
6. Após revisão e merge, atualizar a base da próxima branch. Centralizar com Pablo as mudanças necessárias no menu, nas fixtures e nos contratos.

## Acesso aos dados

O estado reúne listas de registros. Os campos são acessados pelo nome:

```python
grupo = {"id": 1, "nome": "Python", "ativo": True}
print(grupo["nome"])
grupo["ativo"] = False

grupos = [grupo]
for item in grupos:
    print(item["nome"])
```

Para localizar um registro, utilizar o helper da base:

```python
from app.base.consulta import buscar_por_id

grupo = buscar_por_id(estado["grupos"], grupo_id)
if grupo is None:
    return {"ok": False, "mensagem": "Grupo não encontrado.", "dados": None}
```

Os valores JSON `true`, `false` e `null` são convertidos para `True`, `False` e `None` no carregamento. As funções devem utilizar o estado recebido por parâmetro. Recarregar o JSON a cada chamada apagaria alterações feitas por outro módulo na mesma sessão.

## Separação entre regra e terminal

`cxx.py` valida e altera dados; `tela_cxx.py` utiliza `input()` e `print()`. Exemplo de validação de entrada na tela:

```python
valor = input("ID do grupo: ")
try:
    grupo_id = int(valor)
except ValueError:
    print("O ID deve ser um número inteiro.")
    return

# Chamar a função correspondente ao card e apresentar o resultado.
# resultado = consultar(estado, grupo_id)
# print(resultado["mensagem"])
```

Ao final da operação, a tela retorna ao menu principal. Submenus podem utilizar `while`, `if/elif/else` e uma opção de voltar. Apresentar os dados de forma legível para consulta e registro das evidências.

## Apoio de IA (opcional)

Modelo de instrução para implementação assistida:

> Implementar somente o card Cxx descrito em docs/cards/Cxx.md, seguindo docs/ARQUITETURA.md e docs/CONTRATOS.md. Editar apenas os arquivos atribuídos ao card. Usar Python 3.12 e biblioteca padrão, com if/else, for simples e funções pequenas. Preservar assinaturas e campos. Manter o escopo definido, sem adicionar frameworks, banco ou APIs reais. Executar os cenários possíveis e registrar limitações da verificação. Não inventar prints ou resultados de testes. Encaminhar propostas de alteração dos contratos ao responsável pela integração.

O código gerado deve ser revisado e validado. Dados fictícios não dispensam a implementação das regras: mensagens fixas de sucesso não substituem as operações previstas nos cards.

## Pull request

Incluir ID do card, comportamento entregue, arquivos alterados, cenários executados e caminhos dos prints. Registrar dependências de integração ainda pendentes. O PR pode ser revisado antes da integração final; Done exige validação completa.

Em conflitos de merge, comparar as mudanças dos dois lados e preservar os comportamentos necessários. Arquivos exclusivos por card reduzem a ocorrência de conflitos.
