
from abc import ABC, abstractmethod

class DesafioInterface(ABC):

    @abstractmethod
    def add_participante(self, participante) -> None:
        pass

    @abstractmethod
    def remover_participante(self, participante) -> None:
        pass

    @abstractmethod
    def encerra_desafio(self) -> None:
        pass

    @abstractmethod
    def recompensa_participantes(self) -> None:
        pass
