from src.models.equipe_models import Equipe
from src.utils.logger import logger

class EquipeController:
    def __init__(self):
        self.equipes = []
        logger.info("EquipeController iniciado")

    def criar_equipe(self, nome, criador):
        equipe = Equipe(nome, criador)
        self.equipes.append(equipe)
        logger.info("Equipe criada: %s", nome)
        return equipe
    