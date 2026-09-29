# C02 — Configurar características do grupo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Confirmar e concluir a entrega local do C02, que configura descrição, privacidade e modalidade de um grupo existente, preserva seus demais dados e o ativa.

**Architecture:** Manter a regra de negócio em `c02.py` e a coleta/apresentação no terminal em `tela_c02.py`. A implementação já existe nesta branch; executar verificações de contrato e de interface antes de fazer qualquer correção pontual. Registrar evidências reais no registro do card, sem afirmar integração com módulos que ainda estão em stub.

**Tech Stack:** Alvo do projeto: Python 3.12 e biblioteca padrão (`unittest`); o ambiente atual oferece Python 3.14, então as verificações locais usarão `python3` e registrarão essa diferença.

**Spec:** `docs/cards/C02.md`, com regras comuns em `docs/ARQUITETURA.md`, `docs/CONTRATOS.md`, `docs/GUIA-DO-TIME.md` e `docs/TESTES.md`.

## Global Constraints

- O projeto tem como alvo Python 3.12 e usa somente a biblioteca padrão; como `python3.12` não está instalado neste ambiente, executar verificações locais em Python 3.14 e registrar essa limitação.
- Trabalhar na branch `codex/c02` e usar o grupo 5 existente; não importar C01.
- Alterar apenas `app/funcionalidades/grupos/c02.py`, `app/funcionalidades/grupos/tela_c02.py`, `docs/cards/C02.md` e `evidencias/C02/`; este plano é salvo em `docs/superpowers/plans/` por solicitação do usuário.
- Validar grupo, usuário, autoria, vínculo, descrição, privacidade e modalidade antes de alterar qualquer dado.
- Valores aceitos: privacidade `publico` ou `privado`; modalidade `online` ou `presencial`; configuração válida define `ativo=True`.
- Reconfigurar o registro encontrado sem criar cópia, remover vínculos ou alterar o limite.
- Não marcar integração C01→C02, busca C03, PR, anexos no Trello ou evidências não produzidas como concluídos.

---

## Estrutura de arquivos

- `app/funcionalidades/grupos/c02.py`: regra `configurar_grupo(estado, usuario_id, grupo_id, descricao, privacidade, modalidade)` e retorno padronizado.
- `app/funcionalidades/grupos/tela_c02.py`: submenu, captura dos campos e apresentação da configuração salva.
- `docs/cards/C02.md`: critérios e estado das subtarefas do card.
- `evidencias/C02/REGISTRO.md`: resultado observado, executor, data, commit e caminho de cada evidência real.
- `/tmp/test_c02_card.py`: verificação temporária com `unittest`, fora dos arquivos funcionais atribuídos ao card.

### Task 1: Verificar regra, autorização e preservação dos dados

**Files:**
- Read: `app/funcionalidades/grupos/c02.py`
- Read: `app/base/consulta.py`
- Create temporarily: `/tmp/test_c02_card.py`

**Interfaces:**
- Consumes: `configurar_grupo(estado, usuario_id, grupo_id, descricao, privacidade, modalidade)`.
- Produces: prova local dos retornos padronizados, da validação anterior à mutação e da preservação de limite e vínculos.

- [x] **Step 1: Criar o teste temporário de contrato**

```python
from copy import deepcopy
import unittest

from app.funcionalidades.grupos.c02 import configurar_grupo


def estado_de_teste():
    return {
        "usuarios": [{"id": 1, "nome": "Ana"}, {"id": 2, "nome": "Bruno"}],
        "grupos": [{
            "id": 5, "nome": "Python Rascunho", "materia": "Python",
            "objetivo": "Revisar listas", "limite": 5, "criador_id": 1,
            "descricao": "", "modalidade": "", "privacidade": "", "ativo": False,
        }],
        "vinculos": [{"id": 7, "grupo_id": 5, "usuario_id": 1, "papel": "monitor"}],
    }


class ConfigurarGrupoTests(unittest.TestCase):
    def test_configura_grupo_preservando_limite_e_vinculos(self):
        estado = estado_de_teste()
        vinculos_antes = deepcopy(estado["vinculos"])

        resultado = configurar_grupo(
            estado, 1, 5, " Revisão de listas ", "PUBLICO", "ONLINE"
        )

        self.assertTrue(resultado["ok"])
        self.assertIs(resultado["dados"], estado["grupos"][0])
        self.assertEqual(estado["grupos"][0]["descricao"], "Revisão de listas")
        self.assertEqual(estado["grupos"][0]["privacidade"], "publico")
        self.assertEqual(estado["grupos"][0]["modalidade"], "online")
        self.assertTrue(estado["grupos"][0]["ativo"])
        self.assertEqual(estado["grupos"][0]["limite"], 5)
        self.assertEqual(estado["vinculos"], vinculos_antes)

    def test_reconfigura_grupo_ativo_preservando_membros_e_limite(self):
        estado = estado_de_teste()
        estado["grupos"][0].update({
            "descricao": "Descrição anterior", "modalidade": "online",
            "privacidade": "privado", "ativo": True,
        })
        estado["vinculos"].append({
            "id": 8, "grupo_id": 5, "usuario_id": 2, "papel": "membro",
        })
        vinculos_antes = deepcopy(estado["vinculos"])

        resultado = configurar_grupo(
            estado, 1, 5, "Nova descrição", "publico", "presencial"
        )

        self.assertTrue(resultado["ok"])
        self.assertTrue(estado["grupos"][0]["ativo"])
        self.assertEqual(estado["grupos"][0]["limite"], 5)
        self.assertEqual(estado["vinculos"], vinculos_antes)

    def test_descricao_ou_privacidade_invalida_nao_muda_o_grupo(self):
        for descricao, privacidade in (("", "publico"), ("Descrição", "secreto")):
            with self.subTest(descricao=descricao, privacidade=privacidade):
                estado = estado_de_teste()
                grupo_antes = deepcopy(estado["grupos"][0])

                resultado = configurar_grupo(
                    estado, 1, 5, descricao, privacidade, "online"
                )

                self.assertFalse(resultado["ok"])
                self.assertIsNone(resultado["dados"])
                self.assertEqual(estado["grupos"][0], grupo_antes)

    def test_modalidade_invalida_nao_muda_o_grupo(self):
        for modalidade in ("", "hibrida"):
            with self.subTest(modalidade=modalidade):
                estado = estado_de_teste()
                grupo_antes = deepcopy(estado["grupos"][0])

                resultado = configurar_grupo(
                    estado, 1, 5, "Revisão de listas", "publico", modalidade
                )

                self.assertFalse(resultado["ok"])
                self.assertIsNone(resultado["dados"])
                self.assertEqual(estado["grupos"][0], grupo_antes)

    def test_usuario_que_nao_e_criador_nao_muda_o_grupo(self):
        estado = estado_de_teste()
        grupo_antes = deepcopy(estado["grupos"][0])

        resultado = configurar_grupo(
            estado, 2, 5, "Descrição", "publico", "online"
        )

        self.assertFalse(resultado["ok"])
        self.assertIn("criador", resultado["mensagem"])
        self.assertIsNone(resultado["dados"])
        self.assertEqual(estado["grupos"][0], grupo_antes)

    def test_criador_sem_vinculo_nao_muda_o_grupo(self):
        estado = estado_de_teste()
        estado["vinculos"] = []
        grupo_antes = deepcopy(estado["grupos"][0])

        resultado = configurar_grupo(
            estado, 1, 5, "Descrição", "publico", "online"
        )

        self.assertFalse(resultado["ok"])
        self.assertIn("vínculo", resultado["mensagem"])
        self.assertIsNone(resultado["dados"])
        self.assertEqual(estado["grupos"][0], grupo_antes)


if __name__ == "__main__":
    unittest.main()
```

- [x] **Step 2: Executar os testes de contrato**

Run: `PYTHONPATH="$PWD" python3 /tmp/test_c02_card.py -v`
Expected: 6 testes passam; o sucesso inicial e a reconfiguração ativa preservam limite/vínculos; entradas inválidas, criador sem vínculo e C02-F2 deixam o estado igual ao original.

- [x] **Step 3: Conferir divergências e corrigir somente se necessário**

Os seis testes passaram sem divergência do contrato; nenhuma alteração de produção foi necessária. Se uma verificação posterior apontar regressão, editar somente `app/funcionalidades/grupos/c02.py`, manter a assinatura pública e repetir `PYTHONPATH="$PWD" python3 /tmp/test_c02_card.py -v`.

### Task 2: Verificar a tela e executar os cenários C02-S1, C02-F1 e C02-F2

**Files:**
- Read/Modify if needed: `app/funcionalidades/grupos/tela_c02.py`
- Read: `app/menu.py`
- Read: `dados/grupos.json`, `dados/vinculos.json`, `dados/usuarios.json`

**Interfaces:**
- Consumes: `executar(estado, usuario_id)` e a regra `configurar_grupo(...)`.
- Produces: saída observada do submenu, opções permitidas e resultado das entradas dos três cenários do card.

- [x] **Step 1: Executar C02-S1 pela aplicação**

Run: `python3 main.py` com entradas `1`, `02`, `01`, `5`, `Revisão de listas`, `publico`, `online`, `0`, `0`; selecionar Ana e configurar o grupo 5, depois sair do submenu e da sessão.
Expected: mensagem de sucesso, ID `5`, descrição, privacidade, modalidade e estado ativo apresentados; a verificação de contrato confirma que o limite e o vínculo de Ana permanecem.

- [x] **Step 2: Executar C02-F1 com modalidade vazia e inválida**

Em uma sessão limpa, como Ana, tentar configurar grupo `5` com modalidade vazia; repetir a operação com modalidade `hibrida`.
Expected: cada operação informa que a modalidade deve ser `online` ou `presencial`; a verificação de contrato confirma que descrição, privacidade, modalidade e `ativo` não mudaram em cada rejeição.

- [x] **Step 3: Executar C02-F2 como Bruno**

Em uma sessão limpa, selecionar usuário `2`, opção `02`, opção do submenu `01`, grupo `5` e valores válidos para os três campos.
Expected: acesso negado porque somente o criador pode configurar; a verificação de contrato confirma que o registro não mudou.

- [x] **Step 4: Verificar a tela e o tratamento de ID não numérico**

Sem alterações em `tela_c02.py`, C02-S1/F1/F2 foram percorridos pela interface; uma entrada `abc` para ID exibiu `O ID deve ser um número inteiro.` e retornou ao submenu sem traceback.

### Task 3: Registrar os resultados e limites de integração

**Files:**
- Modify: `evidencias/C02/REGISTRO.md`
- Modify: `docs/cards/C02.md`

**Interfaces:**
- Consumes: saída dos testes da Task 1 e dos cenários da Task 2, data local e hash do commit que contém o registro.
- Produces: subtarefas locais atualizadas e tabela com resultados observados, executor, data, commit e evidências realmente capturadas.

- [x] **Step 1: Atualizar o registro com os resultados que foram observados**

Preencher `Observado`, `Resultado`, `Executor`, `Data`, `Commit` e `Print` para cada cenário efetivamente executado. Registrar `pendente` nos campos sem evidência real; não criar capturas simuladas.

- [x] **Step 2: Atualizar somente as subtarefas comprovadas**

Marcar em `docs/cards/C02.md` as subtarefas funcionais e locais que a implementação e as verificações provaram. Deixar C02.7 pendente enquanto PR, integração, cenários integrados e anexos no Trello não tiverem sido feitos.

- [x] **Step 3: Conferir o escopo final e o diff**

Run: `git add docs/superpowers/plans/2026-09-29-c02-configurar-caracteristicas-grupo.md docs/cards/C02.md evidencias/C02/REGISTRO.md`, depois `git diff --cached --check` e `git status --short --branch`.
Expected: branch `codex/c02`, somente arquivos do card e o plano solicitado staged; diff sem erros de whitespace.

- [x] **Step 4: Criar um commit local com o plano e os registros**

Run: `git add docs/superpowers/plans/2026-09-29-c02-configurar-caracteristicas-grupo.md docs/cards/C02.md evidencias/C02/REGISTRO.md` e depois `git commit -m "docs(c02): registrar validacao do card 02"`.
Expected: commit local na branch `codex/c02` contendo apenas o plano solicitado e os registros do C02; o campo `Commit` no registro identifica o commit da implementação que foi testada (`af9fc3b`).

## Revisão do plano

- Cobertura do C02: autorização de criador e vínculo (Task 1), validação dos três campos e atomicidade (Task 1), ativação sem perder membros/limite (Task 1), apresentação de ID/configurações (Task 2), cenários reais e registro de evidências (Tasks 2–3), integração/PR/Trello explicitamente pendentes até ocorrerem (Task 3).
- Busca C03 não pode ser comprovada nesta branch porque `app/funcionalidades/descoberta/c03.py` permanece como stub; o plano verifica `ativo=True` e registra essa limitação sem alegar busca integrada.
- O código desta branch já implementa os comportamentos centrais de C02; mudanças de produção só entram se as verificações apontarem uma divergência específica.
