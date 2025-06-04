import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/controllers')))

from src.models.desafio_models import Desafio
from src.models.pessoa_models import Pessoa

class TestDesafioRecompensa(unittest.TestCase):
    def setUp(self):
        self.p1 = Pessoa('Alice', '1', 100, 0)
        self.p2 = Pessoa('Bernardo', '2', 100, 0)
        self.desafio = Desafio(1, 'Desafio de Teste', '2023-10-01', '2023-10-31', 50)
        self.desafio.add_participante(self.p1)
        self.desafio.add_participante(self.p2)

    def test_recompensa_vencedor(self):

        sucesso_encerrar, _= self.desafio.encerrar_desafio(self.p1)
        self.assertTrue(sucesso_encerrar, "Desafio deveria ser encerrado com sucesso.")

        saldo_anterior = self.p1.saldo
        sucesso, mensagem = self.desafio.recompensa_participantes()

        self.assertTrue(sucesso, "Recompensa deveria ser concedida com sucesso.")
        self.assertEqual(self.p1.saldo, saldo_anterior + self.desafio.valor_aposta, "Saldo do vencedor deveria ser atualizado corretamente.")

    def test_recompensa_sem_encerrar_desafio(self):
        desafio_nao_encerrado = Desafio(2, 'Desafio Não Encerrado', '2023-10-01', '2023-10-31', 50)
        desafio_nao_encerrado.add_participante(self.p1)
        desafio_nao_encerrado.add_participante(self.p2)

        saldo_anterior = self.p1.saldo
        sucesso, mensagem = desafio_nao_encerrado.recompensa_participantes()

        self.assertFalse(sucesso, "Recompensa não deveria ser concedida sem encerrar o desafio.")
        self.assertEqual(mensagem, "O desafio precisa ser encerrado antes de recompensar os participantes.")
        self.assertEqual(self.p1.saldo, saldo_anterior, "Saldo do vencedor não deveria ser alterado.")

if __name__ == '__main__':
    unittest.main()