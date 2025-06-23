import flet as ft
import os
import sys

if __package__ is None:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    
from src.controllers.evento_controller import EventoController
from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController
from src.controllers.equipe_controller import EquipeController
from src.utils.logger import logger
from src.views.login_view import mostrar_login


def flet_main(page: ft.Page):
    """Configura a tela principal da aplicação."""
    page.title = "Sistema de Desafios"
    logger.info("Iniciando o GymBet com Flet...")

    
    pessoa_controller = PessoaController()
    equipe_controller = EquipeController(pessoa_controller)
    desafio_controller = DesafioController(equipe_controller)
    evento_controller = EventoController(desafio_controller)

    mostrar_login(page, pessoa_controller, equipe_controller, desafio_controller, evento_controller)
    
if __name__ == "__main__":
        ft.app(target=flet_main)