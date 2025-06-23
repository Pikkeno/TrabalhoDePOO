from src.models.equipe_models import Equipe
from src.utils import equipe_db
from src.utils.logger import logger


class EquipeController:
    def __init__(self, pessoa_controller=None):
        self.equipes = []
        self.pessoa_controller = pessoa_controller
        self.carregar_equipes()
        logger.info("EquipeController iniciado")

    def carregar_equipes(self):
        if self.pessoa_controller is None:
            return
        for dado in equipe_db.carregar_dados():
            criador = self.pessoa_controller.buscar_por_id(dado.get("criador"))
            if not criador:
                continue
            equipe = Equipe(dado.get("nome"), criador)
            for idm in dado.get("integrantes", []):
                pessoa = self.pessoa_controller.buscar_por_id(idm)
                if pessoa and pessoa not in equipe.integrantes:
                    equipe.integrantes.append(pessoa)
            self.equipes.append(equipe)

    def salvar_equipes(self):
        if self.pessoa_controller is None:
            return
        dados = []
        for eq in self.equipes:
            dados.append({
                "nome": eq.nome,
                "criador": eq.criador.idm,
                "integrantes": [p.idm for p in eq.integrantes],
            })
        equipe_db.salvar_dados(dados)

    def criar_equipe(self, nome, criador):
        equipe = Equipe(nome, criador)
        self.equipes.append(equipe)
        self.salvar_equipes()
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
            self.salvar_equipes()
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