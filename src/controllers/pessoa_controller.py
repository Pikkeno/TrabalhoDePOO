# src/controllers/pessoa_controller.py
from src.models.pessoa_models import Pessoa
from src.utils.logger import logger

class PessoaController:
    def __init__(self):
        self.pessoas = []  # Lista de pessoas registradas
        logger.info("PessoaController iniciado")

    def criar_pessoa(self, nome, idm, email=None, senha=None):
        pessoa = Pessoa(nome, idm, saldo=0, score=0, email=email, senha=senha)
        self.pessoas.append(pessoa)
        logger.info("Pessoa criada: %s", nome)
        return pessoa

    def realizar_aposta(self, pessoa, valor_aposta):
        """
        Faz uma aposta para a pessoa, verificando se o saldo é suficiente.
        """
        if pessoa.saldo >= valor_aposta:
            pessoa.saldo -= valor_aposta  # Deduz o valor da aposta do saldo
            
            logger.info(
                "Aposta de %s realizada no valor de %s. Novo saldo: %s",
                pessoa.nome, valor_aposta, pessoa.saldo
            )
            return f"Aposta de {valor_aposta} realizada por {pessoa.nome}. Novo saldo: {pessoa.saldo}"
        else:
            logger.warning(
                "Saldo insuficiente para %s realizar aposta de %s. Saldo atual: %s",
                pessoa.nome, valor_aposta, pessoa.saldo
            )
            return f"{pessoa.nome} não tem saldo suficiente para fazer essa aposta."


