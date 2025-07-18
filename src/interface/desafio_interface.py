from abc import ABC, abstractmethod

class DesafioInterface(ABC):

    @abstractmethod
    def criar_desafio(self, id, descricao, data_inicio, data_fim, valor_aposta) -> None:
        pass

    @abstractmethod
    def add_participante(self, participante) -> None:
        pass

    @abstractmethod
    def remover_participante(self, participante) -> None:
        pass

    @abstractmethod
    def encerrar_desafio(self) -> None:
        pass

    @abstractmethod
    def recompensa_participantes(self) -> None:
        pass
