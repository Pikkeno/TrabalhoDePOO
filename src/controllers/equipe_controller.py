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
    
    def adicionar_integrante(self, equipe, pessoa):
        """Adiciona uma pessoa a uma equipe existente."""
        if equipe.adicionar_integrante(pessoa):
            logger.info("%s adicionado à equipe %s", pessoa.nome, equipe.nome)
            return True
        logger.info("%s já faz parte da equipe %s", pessoa.nome, equipe.nome)
        return False

    def remover_integrante(self, equipe, pessoa):
        """Remove uma pessoa da equipe."""
        if equipe.remover_integrante(pessoa):
            logger.info("%s removido da equipe %s", pessoa.nome, equipe.nome)
            return True
        logger.info("%s não encontrado na equipe %s", pessoa.nome, equipe.nome)
        return False

    def entrar_desafio(self, equipe, desafio):
        """Faz a equipe inteira participar de um desafio."""
        if equipe.entrar_desafio(desafio):
            logger.info("Equipe %s entrou no desafio %s", equipe.nome, desafio.id)
            return True
        logger.warning(
            "Equipe %s não pôde entrar no desafio %s por falta de vagas",
            equipe.nome,
            desafio.id,
        )
        return False 