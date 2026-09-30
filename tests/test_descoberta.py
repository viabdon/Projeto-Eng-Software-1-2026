import unittest

from app.funcionalidades.descoberta.c03 import buscar_grupos
from app.funcionalidades.descoberta.c04 import filtrar_grupos
from app.funcionalidades.descoberta.c05 import detalhar_grupo


class TestDescoberta(unittest.TestCase):
    def setUp(self):
        self.estado = {
            "grupos": [
                {
                    "id": 1,
                    "nome": "Python em Comunidade",
                    "materia": "Python",
                    "modalidade": "online",
                    "privacidade": "publico",
                    "ativo": True,
                },
                {
                    "id": 2,
                    "nome": "Python Presencial",
                    "materia": "Python",
                    "modalidade": "presencial",
                    "privacidade": "privado",
                    "ativo": True,
                },
                {
                    "id": 3,
                    "nome": "Matemática em Dupla",
                    "materia": "Matemática",
                    "modalidade": "online",
                    "privacidade": "publico",
                    "ativo": True,
                },
                {
                    "id": 4,
                    "nome": "Python Arquivado",
                    "materia": "Python",
                    "modalidade": "online",
                    "privacidade": "publico",
                    "ativo": False,
                },
                {
                    "id": 5,
                    "nome": "Python Rascunho",
                    "materia": "Python",
                    "modalidade": "",
                    "privacidade": "",
                    "ativo": False,
                },
            ]
        }

    def test_buscar_grupos_pelo_texto_da_materia(self):
        resultado = buscar_grupos(self.estado, "  python  ")
        self.assertTrue(resultado["ok"])
        self.assertEqual([grupo["id"] for grupo in resultado["dados"]], [1, 2])
        self.assertIn("Python em Comunidade", " ".join(grupo["nome"] for grupo in resultado["dados"]))

    def test_buscar_grupos_retorna_vazio_quando_nao_acha_resultado(self):
        resultado = buscar_grupos(self.estado, "Astronomia")
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["dados"], [])
        self.assertIn("Nenhum grupo encontrado", resultado["mensagem"])

    def test_buscar_grupos_rejeita_entrada_vazia(self):
        resultado = buscar_grupos(self.estado, "   ")
        self.assertFalse(resultado["ok"])
        self.assertIsNone(resultado["dados"])
        self.assertIn("matéria", resultado["mensagem"].lower())

    def test_filtrar_grupos_aplica_modalidade_e_privacidade(self):
        grupos = [
            self.estado["grupos"][0],
            self.estado["grupos"][1],
        ]
        resultado = filtrar_grupos(grupos, "online", "publico")
        self.assertTrue(resultado["ok"])
        self.assertEqual([grupo["id"] for grupo in resultado["dados"]], [1])

    def test_filtrar_grupos_rejeita_modalidade_invalida_sem_mudar_lista(self):
        grupos = [
            self.estado["grupos"][0],
            self.estado["grupos"][1],
        ]
        original = list(grupos)
        resultado = filtrar_grupos(grupos, "hibrida", "publico")
        self.assertFalse(resultado["ok"])
        self.assertIsNone(resultado["dados"])
        self.assertEqual(len(grupos), len(original))
        self.assertEqual(grupos, original)

    def test_detalhar_grupo_retorna_dados_do_grupo_ativo(self):
        estado = {
            "grupos": [
                {"id": 1, "nome": "Python em Comunidade", "materia": "Python", "descricao": "Estudo semanal", "objetivo": "Praticar programação", "modalidade": "online", "privacidade": "publico", "ativo": True, "limite": 5},
                {"id": 3, "nome": "Matemática em Dupla", "materia": "Matemática", "descricao": "Grupo já lotado", "objetivo": "Revisar funções", "modalidade": "online", "privacidade": "publico", "ativo": True, "limite": 2},
            ],
            "vinculos": [
                {"id": 1, "grupo_id": 1, "usuario_id": 1, "papel": "monitor"},
                {"id": 2, "grupo_id": 1, "usuario_id": 2, "papel": "membro"},
                {"id": 3, "grupo_id": 3, "usuario_id": 3, "papel": "monitor"},
                {"id": 4, "grupo_id": 3, "usuario_id": 2, "papel": "membro"},
            ],
        }
        resultado = detalhar_grupo(estado, 1)
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["dados"]["participantes"], 2)
        self.assertEqual(resultado["dados"]["vagas"], 3)
        self.assertEqual(resultado["dados"]["nome"], "Python em Comunidade")

    def test_detalhar_grupo_inativo_e_inexistente_sao_rejeitados(self):
        estado = {
            "grupos": [
                {"id": 4, "nome": "Python Arquivado", "materia": "Python", "descricao": "Grupo inativo", "objetivo": "Revisão encerrada", "modalidade": "online", "privacidade": "publico", "ativo": False, "limite": 3},
            ],
            "vinculos": [{"id": 1, "grupo_id": 4, "usuario_id": 1, "papel": "monitor"}],
        }

        resultado_inativo = detalhar_grupo(estado, 4)
        self.assertFalse(resultado_inativo["ok"])
        self.assertIn("indisponível", resultado_inativo["mensagem"].lower())

        resultado_inexistente = detalhar_grupo(estado, 999)
        self.assertFalse(resultado_inexistente["ok"])
        self.assertIn("não encontrado", resultado_inexistente["mensagem"].lower())

    def test_detalhar_grupo_lotado_informa_zero_vagas(self):
        estado = {
            "grupos": [
                {"id": 3, "nome": "Matemática em Dupla", "materia": "Matemática", "descricao": "Grupo já lotado", "objetivo": "Revisar funções", "modalidade": "online", "privacidade": "publico", "ativo": True, "limite": 2},
            ],
            "vinculos": [
                {"id": 1, "grupo_id": 3, "usuario_id": 3, "papel": "monitor"},
                {"id": 2, "grupo_id": 3, "usuario_id": 2, "papel": "membro"},
            ],
        }
        resultado = detalhar_grupo(estado, 3)
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["dados"]["participantes"], 2)
        self.assertEqual(resultado["dados"]["vagas"], 0)
        self.assertIn("nova participação", resultado["mensagem"].lower())


if __name__ == "__main__":
    unittest.main()
