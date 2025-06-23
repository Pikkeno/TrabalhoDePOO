# src/controllers/desafio_controller.py
from src.interface.desafio_interface import DesafioInterface
from src.models.desafio_models import Desafio
from src.utils.logger import logger
class DesafioController:
            

    def __init__(self, equipe_controller=None):
        self.desafios = []  # Lista de desafios ativos no sistema
        self.equipe_controller = equipe_controller
        logger.info("DesafioController iniciado")

    def criar_desafio(
        self,
        id,
        descricao,
        data_inicio,
        data_fim,
        valor_aposta,
        limite_participantes: int = 2,
        competicao: str | None = None,
        criador=None,
        adversarios=None,
        equipe_adversaria=None,
    ):
        """
        Cria um novo desafio e adiciona à lista de desafios.
        """
        if competicao == "individual":
            if not adversarios or len(adversarios) == 0:
                raise ValueError(
                    "Desafio individual requer ao menos um adversário convidado."
                )
        elif competicao == "equipe":
            if criador is None:
                raise ValueError("É necessário informar o criador do desafio.")
            if self.equipe_controller is None:
                raise ValueError(
                    "Um controlador de equipes é necessário para desafios em equipe."
                )
            equipe_usuario = None
            for equipe in self.equipe_controller.equipes:
                if criador in equipe.integrantes:
                    equipe_usuario = equipe
                    break
            if equipe_usuario is None:
                raise ValueError(
                    "Usuário precisa estar vinculado a uma equipe para criar desafio em equipe."
                )
            if equipe_adversaria is None:
                raise ValueError("Selecione uma equipe adversária para o desafio.")
            
        desafio = Desafio(id, descricao, data_inicio, data_fim, valor_aposta,
                          limite_participantes)
        self.desafios.append(desafio)
        logger.info(f"Desafio {id} criado: {descricao}")
        return desafio

    def adicionar_participante(self, desafio, participante):
        """
        Adiciona um participante a um desafio específico.
        """
        if desafio.add_participante(participante):
            logger.info(
                "Participante %s adicionado ao desafio %s.",
                participante.nome, 
                desafio.id,
            )
            return f"Participante {participante.nome} adicionado ao desafio {desafio.id}."
        else:
            logger.warning(
                "O desafio %s ja atingiu o limite de participantes", desafio.id
            )
            return "O desafio já tem o número máximo de participantes."

    def remover_participante(self, desafio, participante):
        """
        Remove um participante de um desafio.
        """
        if desafio.remover_participante(participante):
            logger.info(
                "Participante %s removido do desafio %s.",
                participante.nome, 
                desafio.id,
            )
            return f"Participante {participante.nome} removido do desafio {desafio.id}."
        else:
            logger.warning(
                "Participante %s não encontrado no desafio %s.",
                participante.nome, 
                desafio.id,
            )
            return f"Participante {participante.nome} não encontrado no desafio {desafio.id}."

    def encerrar_desafio(self, desafio, vencedor):
        """
        Encerra o desafio e define o vencedor.
        """
        sucesso, mensagem = desafio.encerrar_desafio(vencedor)
        if sucesso:
            logger.info(
                "Desafio %s encerrado. Vencedor: %s.",
                desafio.id, 
                vencedor.nome,
            )
        else:
            logger.warning(
                "Falha ao encerrar o desafio %s: %s",
                desafio.id,
                mensagem,
            )
        return mensagem
    
    def recompensar_participantes(self, desafio):
        """
        Recompensa os participantes com base no resultado do desafio.
        """
        sucesso, mensagem = desafio.recompensa_participantes()
        if sucesso:
            logger.info(
                "Participantes recompensados no desafio %s.",
                desafio.id,
            )
        else:
            logger.warning(
                "Não foi possível recompensar os participantes do desafio %s: %s",
                desafio.id, 
                mensagem,
            )
        return mensagem

    def listar_desafios(self):
        """
        Exibe a lista de desafios ativos.
        """
        return [f"Desafio {desafio.id}: {desafio.descricao} - Status: {desafio.status}" for desafio in self.desafios]
