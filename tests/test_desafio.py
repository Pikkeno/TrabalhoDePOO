import unittest
import sys
import os
import pytest
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from src.models.desafio_models import Desafio
from src.models.pessoa_models import Pessoa

class TestDesafioRecompensa(unittest.TestCase):
    def setUp(self):
        self.p1 = Pessoa('Alice', '1', 100, 0)
        self.p2 = Pessoa('Bernardo', '2', 100, 0)
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')
        self.desafio = Desafio(1, 'Desafio de Teste', inicio, fim, 50)
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
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')
        desafio_nao_encerrado = Desafio(2, 'Desafio Não Encerrado', inicio, fim, 50)
        desafio_nao_encerrado.add_participante(self.p1)
        desafio_nao_encerrado.add_participante(self.p2)

        saldo_anterior = self.p1.saldo
        sucesso, mensagem = desafio_nao_encerrado.recompensa_participantes()

        self.assertFalse(sucesso, "Recompensa não deveria ser concedida sem encerrar o desafio.")
        self.assertEqual(mensagem, "O desafio precisa ser encerrado antes de recompensar os participantes.")
        self.assertEqual(self.p1.saldo, saldo_anterior, "Saldo do vencedor não deveria ser alterado.")

    def test_limite_variavel_participantes(self):
        inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
        fim = (datetime.now() + timedelta(days=30)).strftime('%d-%m-%Y')
        desafio = Desafio(3, 'Equipe Grande', inicio, fim, 50, limite_participantes=3)
        p3 = Pessoa('Carlos', '3', 100, 0)

        self.assertTrue(desafio.add_participante(self.p1), "Deveria permitir adicionar o primeiro participante.")
        self.assertTrue(desafio.add_participante(self.p2), "Deveria permitir adicionar o segundo participante.")
        self.assertTrue(desafio.add_participante(p3), "Deveria permitir adicionar o terceiro participante.") 

        p4 = Pessoa('Diana', '4', 100, 0)
        self.assertFalse(desafio.add_participante(p4), "Não deveria permitir adicionar um quarto participante, excedendo o limite.")

def test_validacao_formato_data():
    """Valida se as datas no modelo de Desafio estão corretas."""
    inicio = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
    fim = (datetime.now() + timedelta(days=2)).strftime('%d-%m-%Y')
    # Formato correto deve funcionar
    try:
        Desafio(4, 'Formato Ok', inicio, fim, 10)
    except ValueError:
        pytest.fail('Datas no formato DD-MM-YYYY deveriam ser aceitas.')

        # Formato incorreto deve lançar erro
    with pytest.raises(ValueError):
        Desafio(5, 'Formato Errado', '2023-10-10', '2023-10-20', 10)
if __name__ == '__main__':
    unittest.main()