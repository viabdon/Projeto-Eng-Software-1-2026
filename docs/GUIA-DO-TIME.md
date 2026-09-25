# Guia curto para implementar um card

1. Leia ARQUITETURA.md, CONTRATOS.md e o arquivo `docs/cards/Cxx.md` atribuído a você.
2. Clone o repositório, abra a pasta e execute `py -3.12 main.py`. Em Linux/macOS, use `python main.py` com Python 3.12. Não há pacotes para instalar.
3. Crie sua branch a partir de main atualizada: `git switch main`, `git pull --ff-only`, `git switch -c codex/cxx`. Execute cada comando separadamente.
4. Implemente as funções já declaradas em `cxx.py`, preservando nomes e parâmetros. Implemente sua tela em `tela_cxx.py`; ela já aparece no menu principal.
5. Execute todos os cenários do seu card, registre resultados e tire os prints. Faça commit apenas dos seus arquivos; abra um PR para main e indique o card e testes executados.
6. Após revisão e merge, atualize a base de sua próxima branch. Evite mudar menu, fixtures ou contratos por conta própria: leve a mudança necessária a Pablo.

## Os poucos conceitos de dados necessários

Um dicionário é um registro com campos nomeados. A lista guarda vários registros:

```python
grupo = {"id": 1, "nome": "Python", "ativo": True}
print(grupo["nome"])
grupo["ativo"] = False

grupos = [grupo]
for item in grupos:
    print(item["nome"])
```

No projeto, use os registros que a base já preparou:

```python
from app.base.consulta import buscar_por_id

grupo = buscar_por_id(estado["grupos"], grupo_id)
if grupo is None:
    return {"ok": False, "mensagem": "Grupo não encontrado.", "dados": None}
```

JSON usa `true`, `false` e `null`; depois que o Python carrega o arquivo, eles viram `True`, `False` e `None`. Trabalhe no estado recebido pela função. Recarregar JSON a cada chamada apagaria alterações feitas por outro módulo na mesma sessão.

## Separar regra e terminal

`cxx.py` valida e altera dados; `tela_cxx.py` usa `input()` e `print()`. Uma tela pode seguir esta forma, adaptando a função e os campos ao card:

```python
valor = input("ID do grupo: ")
try:
    grupo_id = int(valor)
except ValueError:
    print("Digite um número inteiro.")
    return

# Chamar aqui a função real do seu card.
# resultado = consultar(estado, grupo_id)
# print(resultado["mensagem"])
```

No fim de uma operação, a tela retorna ao menu principal. Se precisar de submenu, use `while`, `if/elif/else` e opção de voltar. Mostre os dados de modo legível, sem despejar dicionários grandes nos prints de avaliação.

## Uso dos agentes de IA

Copie e adapte este pedido no seu agente:

> Implemente somente o card Cxx descrito em docs/cards/Cxx.md. Leia antes docs/ARQUITETURA.md e docs/CONTRATOS.md. Edite somente os arquivos atribuídos ao card. Use Python 3.12 e biblioteca padrão, com if/else, for simples e funções pequenas. Preserve assinaturas e campos. Não implemente outros cards, não adicione frameworks, banco, API real ou dependências. Explique os acessos a dicionários usados. Execute os cenários possíveis e relate o que não foi executado; não invente prints, testes aprovados ou funcionalidades. Para mudar um contrato, descreva primeiro o motivo ao responsável pela integração.

Verifique o código gerado e tente explicá-lo com suas próprias palavras. Não substituir validações por mensagens de sucesso fixas: dados são fictícios, mas a interação e a regra do card devem funcionar.

## Pull request

Inclua ID do card, comportamento entregue, arquivos alterados, cenários executados e caminhos dos prints. Não afirmar que tudo passou se uma integração depende de outro card. O PR pode ser revisado enquanto a integração final aguarda; Done exige a validação completa.

Em conflito de merge, compare a mudança de ambos os lados. Não resolver aceitando uma versão inteira sem entender, nem usar reset destrutivo para apagar trabalho. Arquivos exclusivos por card reduzem essa situação.
