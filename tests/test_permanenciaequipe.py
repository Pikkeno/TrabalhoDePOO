import unittest
import tempfile
import json
from pathlib import Path
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.controllers.equipe_controller import EquipeController
from src.models.pessoa_models import Pessoa
from src.utils import equipe_db

class TestEquipePersistencia(unittest.TestCase):
    def test_criar_equipe_salva_no_arquivo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "equipes.json"
            original_path = equipe_db.DB_PATH
            equipe_db.DB_PATH = tmp_path
            try:
                controller = EquipeController()
                criador = Pessoa("Alice", "1")
                controller.criar_equipe("EquipeX", criador)
                self.assertTrue(tmp_path.exists())
                with open(tmp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.assertEqual(len(data), 1)
                self.assertEqual(data[0]["nome"], "EquipeX")
                self.assertEqual(data[0]["criador"], "1")
            finally:
                equipe_db.DB_PATH = original_path

if __name__ == "__main__":
    unittest.main()