from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController
from src.utils.logger import logger
import sys

def cli_main():    # Inicializa os controladores
    logger.info("Iniciando o GymBet CLI...")
    desafio_controller = DesafioController()
    pessoa_controller = PessoaController()

    nome = input("Digite seu nome: ")
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    # Cria uma nova pessoa com IDM aleatório
    try:
        pessoa = pessoa_controller.criar_pessoa(nome, email=email, senha=senha)
    except ValueError as exc:
        print(f"Erro ao criar pessoa: {exc}")
        return
    print(f"Pessoa criada: {pessoa}")
 
    # Cria um desafio
    descricao = input("Digite a descrição do desafio: ")
    data_inicio = input("Digite a data de início do desafio (DD-MM-YYYY): ")
    data_fim = input("Digite a data de fim do desafio (DD-MM-YYYY): ")
    valor_aposta = input("Digite o valor da aposta: ")
    limite = input("Digite o limite de participantes: ")

    try:
        desafio = desafio_controller.criar_desafio(
            1, descricao, data_inicio, data_fim, valor_aposta, limite
        )
    except ValueError as exc:
        print(f"Erro ao criar desafio: {exc}")
        return
    else:
        print(f"Desafio criado: {desafio.descricao}")
        # Adiciona a pessoa como participante do desafio
        mensagem = desafio_controller.adicionar_participante(desafio, pessoa)
        print(mensagem)

def main():

    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        try:
            import flet as ft
            from src.interface.gui_flet import flet_main
            logger.info("Iniciando o GymBet com Flet...")   
        except ModuleNotFoundError:
            logger.error(
                "Flet não está instalado. Execute 'pip install flet' para instalar."
            )
            sys.exit(1)
        ft.app(target=flet_main)
    else:
        cli_main()

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.exception("Erro inesperado no GymBet CLI: %s", exc)