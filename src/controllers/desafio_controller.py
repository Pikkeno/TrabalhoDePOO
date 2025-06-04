# src/controllers/desafio_controller.py
from src.models.desafio_models import Desafio
class DesafioController:
            

    def __init__(self):
        self.desafios = []  # Lista de desafios ativos no sistema

    def criar_desafio(self, id, descricao, data_inicio, data_fim, valor_aposta):
        """
        Cria um novo desafio e adiciona à lista de desafios.
        """
        desafio = Desafio(id, descricao, data_inicio, data_fim, valor_aposta)
        self.desafios.append(desafio)
        return desafio

    def adicionar_participante(self, desafio, participante):
        """
        Adiciona um participante a um desafio específico.
        """
        if desafio.add_participante(participante):
            return f"Participante {participante.nome} adicionado ao desafio {desafio.id}."
        else:
            return "O desafio já tem o número máximo de participantes."

    def remover_participante(self, desafio, participante):
        """
        Remove um participante de um desafio.
        """
        if desafio.remover_participante(participante):
            return f"Participante {participante.nome} removido do desafio {desafio.id}."
        else:
            return f"Participante {participante.nome} não encontrado no desafio {desafio.id}."

    def encerrar_desafio(self, desafio, vencedor):
        """
        Encerra o desafio e define o vencedor.
        """
        sucesso, mensagem = desafio.encerrar_desafio(vencedor)
        return mensagem

    def recompensar_participantes(self, desafio):
        """
        Recompensa os participantes com base no resultado do desafio.
        """
        sucesso, mensagem = desafio.recompensa_participantes()
        return mensagem

    def listar_desafios(self):
        """
        Exibe a lista de desafios ativos.
        """
        return [f"Desafio {desafio.id}: {desafio.descricao} - Status: {desafio.status}" for desafio in self.desafios]
