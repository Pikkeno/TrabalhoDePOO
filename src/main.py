from src.controllers.cdesafio import DesafioController
from src.controllers.cpessoa import PessoaController


def main():
    # Inicializa os controladores
    desafio_controller = DesafioController()
    pessoa_controller = PessoaController()

    # Exemplo de uso do controlador de pessoas
    pessoa1 = pessoa_controller.criar_pessoa("Alice", "ID123", 1000, 50)
    print(f"Pessoa criada: {pessoa1.nome}, Saldo: {pessoa1.saldo}, Score: {pessoa1.score}")

    # Exemplo de uso do controlador de desafios
    desafio1 = desafio_controller.criar_desafio(1, "Desafio de Apostas", "2023-10-01", "2023-10-31", 100)
    print(f"Desafio criado: {desafio1.descricao}, Data Início: {desafio1.data_inicio}, Data Fim: {desafio1.data_fim}")