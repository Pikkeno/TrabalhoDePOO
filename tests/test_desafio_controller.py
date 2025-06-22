import unittest
import os
import sys
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.controllers.desafio_controller import DesafioController
from src.models.pessoa_models import Pessoa

class TestDesafioController(unittest.TestCase):
    def setUp(self):
        self.controller = DesafioController()
        self.p1 = Pessoa('Alice', '1', 100, 0)
        self.p2 = Pessoa('Bob', '2', 100, 0)
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')
        self.desafio = self.controller.criar_desafio(1, 'Desafio de Teste', inicio, fim, 50)
        self.controller.adicionar_participante(self.desafio, self.p1)
        self.controller.adicionar_participante(self.desafio, self.p2)

    def test_encerrar_desafio_success(self):
        mensagem = self.controller.encerrar_desafio(self.desafio, self.p1)
        self.assertEqual(self.desafio.status, 'Encerrado')
        self.assertEqual(self.desafio.vencedor, self.p1)
        self.assertIn('Desafio 1 encerrado', mensagem)

    def test_recompensar_participantes_success(self):
        self.controller.encerrar_desafio(self.desafio, self.p1)
        saldo_anterior = self.p1.saldo
        mensagem = self.controller.recompensar_participantes(self.desafio)
        self.assertEqual(self.p1.saldo, saldo_anterior + self.desafio.valor_aposta)
        self.assertIn('recebeu a recompensa', mensagem)

if __name__ == '__main__':
    unittest.main()