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

class TestEventoCarregarPersistencia(unittest.TestCase):
    def test_carregar_eventos(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "eventos.json"
            original_path = evento_db.DB_PATH
            evento_db.DB_PATH = tmp_path
            try:
                pessoa_controller = PessoaController()
                pessoa_controller.pessoas = []
                p1 = pessoa_controller.criar_pessoa("Alice", "1")
                p2 = pessoa_controller.criar_pessoa("Bob", "2")
                controller = EventoController(DesafioController(), pessoa_controller)
                controller.eventos = []
                evento = controller.criar_evento(p1, p2)
                controller.salvar_eventos()

                novo_controller = EventoController(DesafioController(), pessoa_controller)
                self.assertEqual(len(novo_controller.eventos), 1)
                self.assertEqual(novo_controller.eventos[0].criador.idm, "1")
                self.assertEqual(novo_controller.eventos[0].convidado.idm, "2")
            finally:
                evento_db.DB_PATH = original_path

if __name__ == "__main__":
    unittest.main()