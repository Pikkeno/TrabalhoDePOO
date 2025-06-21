import unittest
from unittest import mock
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

import main

class TestCliMainInvalidDate(unittest.TestCase):
    def test_criar_desafio_data_invalida(self):
        entradas = [
            'Alice',            # nome
            'alice@example.com', # email
            'senha123',         # senha
            'Teste',            # descricao
            '2023-01-01',       # data_inicio invalida
            '2023-01-31',       # data_fim invalida
            '50',               # valor_aposta
            '2'                 # limite
        ]
        with mock.patch('builtins.input', side_effect=entradas):
            with mock.patch('builtins.print') as mock_print:
                main.cli_main()
        saida = "\n".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn('Erro ao criar desafio', saida)

if __name__ == '__main__':
    unittest.main()