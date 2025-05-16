# src/controllers/pessoa_controller.py

from src.models.pessoa import Pessoa

class PessoaController:
    def __init__(self):
        self.pessoas = []  # Lista de pessoas registradas

    def criar_pessoa(self, nome, idm, saldo, score):
        """
        Cria uma nova pessoa e a adiciona à lista de pessoas.
        """
        pessoa = Pessoa(nome, idm, saldo, score)
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

    def desafiar_oponente(self, pessoa, oponente, valor_aposta):
        """
        Faz uma pessoa desafiar outra, verificando se ambos têm saldo suficiente.
        """
        if pessoa.saldo >= valor_aposta and oponente.saldo >= valor_aposta:
            pessoa.saldo -= valor_aposta
            oponente.saldo -= valor_aposta
            return f"{pessoa.nome} desafiou {oponente.nome} para uma aposta de {valor_aposta}. " \
                   f"Saldo de {pessoa.nome}: {pessoa.saldo}, Saldo de {oponente.nome}: {oponente.saldo}"
        else:
            return "Saldo insuficiente para desafiar o oponente."
