import unittest
import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.controllers.pessoa_controller import PessoaController
from src.controllers.equipe_controller import EquipeController
from src.utils import equipe_db
from src.models.pessoa_models import Pessoa
from src.models.desafio_models import Desafio

class TestEquipeController(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.original_path = equipe_db.DB_PATH
        equipe_db.DB_PATH = Path(self.tmpdir.name) / "equipes.json"
        self.pessoa_controller = PessoaController()
        self.pessoa_controller.salvar_pessoas = lambda: None
        self.pessoa_controller.pessoas = []
        self.p1 = self.pessoa_controller.criar_pessoa('Alice', '1')
        self.p2 = self.pessoa_controller.criar_pessoa('Bob', '2')
        self.p3 = self.pessoa_controller.criar_pessoa('Carol', '3')
        self.controller = EquipeController(self.pessoa_controller)
        self.controller.salvar_equipes = lambda: None
        self.controller.equipes = []
        self.controller = EquipeController()
        self.equipe = self.controller.criar_equipe('TimeA', self.p1)

    def tearDown(self):
        equipe_db.DB_PATH = self.original_path
        self.tmpdir.cleanup()

    def test_criar_equipe_nome_vazio(self):
        with self.assertRaises(ValueError):
            self.controller.criar_equipe('', self.p1)
    
    def test_criar_equipe_nome_duplicado_mesmo_usuario(self):
        self.controller.criar_equipe('Repetida', self.p1)
        with self.assertRaises(ValueError):
            self.controller.criar_equipe('Repetida', self.p1)

    def test_adicionar_remover_integrante(self):
        self.assertTrue(self.controller.adicionar_integrante(self.equipe, self.p2))
        self.assertIn(self.p2, self.equipe.integrantes)
        # Adicionar novamente deve retornar False
        self.assertFalse(self.controller.adicionar_integrante(self.equipe, self.p2))
        self.assertTrue(self.controller.remover_integrante(self.equipe, self.p2))
        self.assertNotIn(self.p2, self.equipe.integrantes)
        # Remover novamente deve retornar False
        self.assertFalse(self.controller.remover_integrante(self.equipe, self.p2))

    def test_adicionar_remover_por_nome(self):
        self.assertTrue(
            self.controller.adicionar_integrante_por_nome(self.equipe, 'Bob')
        )
        self.assertIn(self.p2, self.equipe.integrantes)
        # Repetido deve retornar False
        self.assertFalse(
            self.controller.adicionar_integrante_por_nome(self.equipe, 'Bob')
        )
        self.assertTrue(
            self.controller.remover_integrante_por_nome(self.equipe, 'Bob')
        )
        self.assertNotIn(self.p2, self.equipe.integrantes)
        self.assertFalse(
            self.controller.remover_integrante_por_nome(self.equipe, 'Bob')
        )

    def test_entrar_desafio(self):
        self.controller.adicionar_integrante(self.equipe, self.p2)
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=2)).strftime('%d-%m-%Y')
        desafio = Desafio(1, 'Teste', inicio, fim, 10, limite_participantes=3)
        self.assertTrue(self.controller.entrar_desafio(self.equipe, desafio))
        self.assertIn(self.p1, desafio.participantes)
        self.assertIn(self.p2, desafio.participantes)

        equipe2 = self.controller.criar_equipe('TimeB', self.p3)
        # Ainda há 1 vaga para Carol
        self.assertTrue(self.controller.entrar_desafio(equipe2, desafio))
        self.assertIn(self.p3, desafio.participantes)

        # Nova equipe excederia o limite
        p4 = Pessoa('Dave', '4')
        equipe3 = self.controller.criar_equipe('TimeC', p4)
        self.assertFalse(self.controller.entrar_desafio(equipe3, desafio))
        self.assertNotIn(p4, desafio.participantes)

if __name__ == '__main__':
    unittest.main()