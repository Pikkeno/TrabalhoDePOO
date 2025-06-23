# src/controllers/desafio_controller.py
from src.interface.desafio_interface import DesafioInterface
from src.models.desafio_models import Desafio
from src.utils.logger import logger
from src.utils import desafio_db
class DesafioController:
            

    def __init__(self, equipe_controller=None):
        self.desafios = []  # Lista de desafios ativos no sistema
        self.equipe_controller = equipe_controller
        self.carregar_desafios()
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
        if not descricao or not str(descricao).strip():
            raise ValueError("Descrição não pode ser vazia")
        if not data_inicio or not str(data_inicio).strip():
            raise ValueError("Data de início não pode ser vazia")
        if not data_fim or not str(data_fim).strip():
            raise ValueError("Data de fim não pode ser vazia")
        if valor_aposta is None or str(valor_aposta).strip() == "":
            raise ValueError("Valor da aposta não pode ser vazio")
        if limite_participantes is None or str(limite_participantes).strip() == "":
            raise ValueError("Limite de participantes não pode ser vazio")
        
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
            
        desafio = Desafio(
            id, descricao, data_inicio, data_fim, valor_aposta, limite_participantes
        )
        self.desafios.append(desafio)
        self.salvar_desafios()
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
    
    def carregar_desafios(self):
        for dado in desafio_db.carregar_dados():
            try:
                desafio = Desafio(
                    dado.get("id"),
                    dado.get("descricao"),
                    dado.get("data_inicio"),
                    dado.get("data_fim"),
                    dado.get("valor_aposta"),
                    dado.get("limite_participantes", 2),
                )
                desafio.status = dado.get("status", "Ativo")
                self.desafios.append(desafio)
            except Exception:
                continue

    def salvar_desafios(self):
        dados = []
        for d in self.desafios:
            dados.append(
                {
                    "id": d.id,
                    "descricao": d.descricao,
                    "data_inicio": d.data_inicio,
                    "data_fim": d.data_fim,
                    "valor_aposta": d.valor_aposta,
                    "limite_participantes": d.limite_participantes,
                    "status": d.status,
                }
            )
        desafio_db.salvar_dados(dados)
