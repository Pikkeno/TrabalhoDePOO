import unittest
import tempfile
import json
from pathlib import Path
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.controllers.evento_controller import EventoController
from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController
from src.utils import evento_db
from src.models.pessoa_models import Pessoa

class TestEventoControllerAceitarPersistencia(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.original_path = evento_db.DB_PATH
        evento_db.DB_PATH = Path(self.tmpdir.name) / "eventos.json"
        self.pessoa_controller = PessoaController()
        self.pessoa_controller.salvar_pessoas = lambda: None
        self.pessoa_controller.pessoas = []
        self.p1 = self.pessoa_controller.criar_pessoa("Alice", "1")
        self.p2 = self.pessoa_controller.criar_pessoa("Bob", "2")
        self.controller = EventoController(DesafioController())
        self.controller.eventos = []

    def tearDown(self):
        evento_db.DB_PATH = self.original_path
        self.tmpdir.cleanup()

    def test_aceitar_evento_persistencia(self):
        evento = self.controller.criar_evento(self.p1, self.p2)
        self.controller.aceitar_evento(evento, self.p2)
        self.assertTrue(evento.aceito)
        self.assertTrue(evento_db.DB_PATH.exists())
        with open(evento_db.DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertTrue(data[0]["aceito"])

    def test_recusar_evento_remove(self):
        evento = self.controller.criar_evento(self.p1, self.p2)
        self.assertIn(evento, self.controller.eventos)
        self.controller.recusar_evento(evento, self.p2)
        self.assertNotIn(evento, self.controller.eventos) 

if __name__ == "__main__":
    unittest.main()