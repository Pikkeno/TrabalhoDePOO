import unittest
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.controllers.pessoa_controller import PessoaController


class BasePessoaControllerTest(unittest.TestCase):
    def setUp(self):
        # Start controller without persisting to disk
        self.controller = PessoaController()
        self.controller.salvar_pessoas = lambda: None
        # Ensure clean state
        self.controller.pessoas = []
        self.usuario = self.controller.registrar_pessoa(
            "Alice",
            "1",
            "alice@example.com",
            "senha123",
        )


class TestAutenticarPessoa(BasePessoaControllerTest):
    def test_autenticar_sucesso(self):
        pessoa = self.controller.autenticar("alice@example.com", "senha123")
        self.assertIsNotNone(pessoa)
        self.assertEqual(pessoa.nome, "Alice")

    def test_autenticar_email_errado(self):
        pessoa = self.controller.autenticar("errado@example.com", "senha123")
        self.assertIsNone(pessoa)

    def test_autenticar_senha_errada(self):
        pessoa = self.controller.autenticar("alice@example.com", "senha_errada")
        self.assertIsNone(pessoa)


class TestRegistroDuplicado(BasePessoaControllerTest):
    def test_registrar_idm_existente(self):
        novo = self.controller.registrar_pessoa(
            "Bob",
            "1",
            "bob@example.com",
            "outra",
        )
        self.assertIsNone(novo)
    
    def test_registrar_email_invalido(self):
        with self.assertRaises(ValueError):
            self.controller.registrar_pessoa(
                "Eve",
                "3",
                "email_invalido",
                "senha123",
            )

    def test_registrar_email_existente(self):
        novo = self.controller.registrar_pessoa(
            "Carol",
            "2",
            "alice@example.com",
            "outra",
        )
        self.assertIsNone(novo)

class TestAdicionarAmigo(BasePessoaControllerTest):
    def test_adicionar_amigo_por_nome(self):
        amigo = self.controller.registrar_pessoa(
            "Bob",
            "2",
            "bob@example.com",
            "senha456",
        )
        mensagem = self.controller.adicionar_amigo(self.usuario, "Bob")
        self.assertIn("adicionado como amigo", mensagem)
        self.assertIn(amigo, self.usuario.amigos)

    def test_adicionar_amigo_nao_encontrado(self):
        mensagem = self.controller.adicionar_amigo(self.usuario, "Inexistente")
        self.assertIn("não encontrado", mensagem)

    def test_adicionar_amigo_nome_vazio(self):
        with self.assertRaises(ValueError):
            self.controller.adicionar_amigo(self.usuario, "")

if __name__ == "__main__":
    unittest.main()