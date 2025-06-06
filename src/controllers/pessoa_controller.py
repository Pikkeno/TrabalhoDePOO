# src/controllers/pessoa_controller.py

from src.models.pessoa_models import Pessoa

class PessoaController:
    def __init__(self):
        self.pessoas = []  # Lista de pessoas registradas

    def criar_pessoa(self, nome, idm, saldo=0, score=0):
        """
        Cria uma nova pessoa e a adiciona à lista de pessoas.
        """
        pessoa = Pessoa(nome, idm)
        self.pessoas.append(pessoa)
        return pessoa

    def realizar_aposta(self, pessoa, valor_aposta):
        """
        Faz uma aposta para a pessoa, verificando se o saldo é suficiente.
        """
        if pessoa.saldo >= valor_aposta:
            pessoa.saldo -= valor_aposta  # Deduz o valor da aposta do saldo
            return f"Aposta de {valor_aposta} realizada por {pessoa.nome}. Novo saldo: {pessoa.saldo}"
        else:
            return f"{pessoa.nome} não tem saldo suficiente para fazer essa aposta."


