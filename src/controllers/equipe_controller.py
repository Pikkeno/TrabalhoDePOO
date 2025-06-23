from src.models.equipe_models import Equipe
from src.utils import equipe_db
from src.utils.logger import logger
from src.controllers.pessoa_controller import PessoaController


class EquipeController:
    _default_pessoa_controller = None
    
    def __init__(self, pessoa_controller=None):
        if pessoa_controller is None:
            if EquipeController._default_pessoa_controller is None:
                pessoa_controller = PessoaController()
            else:
                pessoa_controller = EquipeController._default_pessoa_controller
        else:
            EquipeController._default_pessoa_controller = pessoa_controller

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
        dados = []
        for eq in self.equipes:
            dados.append({
                "nome": eq.nome,
                "criador": eq.criador.idm,
                "integrantes": [p.idm for p in eq.integrantes],
            })
        equipe_db.salvar_dados(dados)

    def criar_equipe(self, nome, criador):
        if not nome or nome.strip() == "":
            raise ValueError("Nome da equipe não pode ser vazio")
        equipe = Equipe(nome, criador)
        self.equipes.append(equipe)
        self.salvar_equipes()
        logger.info("Equipe criada: %s", nome)
        return equipe
    
    def adicionar_integrante(self, equipe, pessoa):
        """Adiciona uma pessoa a uma equipe existente."""
        if equipe.adicionar_integrante(pessoa):
            self.salvar_equipes()
            logger.info("%s adicionado à equipe %s", pessoa.nome, equipe.nome)
            return True
        logger.info("%s já faz parte da equipe %s", pessoa.nome, equipe.nome)
        return False


    def adicionar_integrante_por_nome(self, equipe, nome_usuario: str):
        """Adiciona um integrante procurando pelo nome de usuário."""
        if self.pessoa_controller is None:
            return False
        pessoa = self.pessoa_controller.buscar_por_nome(nome_usuario)
        if not pessoa:
            logger.info("Usuário %s não encontrado", nome_usuario)
            return False
        return self.adicionar_integrante(equipe, pessoa)

    def remover_integrante(self, equipe, pessoa):
        """Remove uma pessoa da equipe."""
        if equipe.remover_integrante(pessoa):
            self.salvar_equipes()
            logger.info("%s removido da equipe %s", pessoa.nome, equipe.nome)
            return True
        logger.info("%s não encontrado na equipe %s", pessoa.nome, equipe.nome)
        return False
    
    def remover_integrante_por_nome(self, equipe, nome_usuario: str):
        """Remove um integrante procurando pelo nome de usuário."""
        if self.pessoa_controller is None:
            return False
        pessoa = self.pessoa_controller.buscar_por_nome(nome_usuario)
        if not pessoa:
            logger.info("Usuário %s não encontrado", nome_usuario)
            return False
        return self.remover_integrante(equipe, pessoa)

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