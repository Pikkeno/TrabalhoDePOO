import unittest
import os
import sys
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.models.pessoa_models import Pessoa
from src.models.desafio_models import Desafio

class TestPessoaValidations(unittest.TestCase):
    def test_non_negative_properties(self):
        p = Pessoa('Teste', '1', saldo=-10, score=-5, valor_aposta=-20)
        self.assertEqual(p.saldo, 0)
        self.assertEqual(p.score, 0)
        self.assertEqual(p.valor_aposta, 0)

        p.saldo = -50
        p.score = -3
        p.valor_aposta = -100
        self.assertEqual(p.saldo, 0)
        self.assertEqual(p.score, 0)
        self.assertEqual(p.valor_aposta, 0)

        p.valor_aposta = None
        self.assertIsNone(p.valor_aposta)

class TestDesafioValidations(unittest.TestCase):
    def test_limite_participantes_validation(self):
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=2)).strftime('%d-%m-%Y')
        with self.assertRaises(ValueError):
            Desafio(1, 't', inicio, fim, 10, limite_participantes=0)
        d = Desafio(2, 't', inicio, fim, 10)
        with self.assertRaises(ValueError):
            d.limite_participantes = -1

    def test_status_validation(self):
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=2)).strftime('%d-%m-%Y')
        d = Desafio(3, 't', inicio, fim, 10)
        with self.assertRaises(ValueError):
            d.status = 'Pausado'

if __name__ == '__main__':
    unittest.main()