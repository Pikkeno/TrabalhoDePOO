from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController


def main():
    # Inicializa os controladores
    desafio_controller = DesafioController()
    pessoa_controller = PessoaController()

    nome = input("Digite seu nome: ")
    idm = input("Digite seu IDM: ")
    saldo = int(input("Digite seu saldo inicial: "))
    score = int(input("Digite seu score inicial: "))

    # Cria uma nova pessoa
    pessoa = pessoa_controller.criar_pessoa(nome, idm, saldo, score)
    print(f"Pessoa criada: {pessoa}")
    # Cria um desafio
    descricao = input("Digite a descrição do desafio: ")
    data_inicio = input("Digite a data de início do desafio (YYYY-MM-DD): ")
    data_fim = input("Digite a data de fim do desafio (YYYY-MM-DD): ")
    valor_aposta = int(input("Digite o valor da aposta: "))
    limite = int(input("Digite o limite de participantes: "))
    desafio = desafio_controller.criar_desafio(
        1, descricao, data_inicio, data_fim, valor_aposta, limite
    )
    print(f"Desafio criado: {desafio.descricao}")
    # Adiciona a pessoa como participante do desafio
    mensagem = desafio_controller.adicionar_participante(desafio, pessoa)
    print(mensagem)

if __name__ == "__main__":
    main()