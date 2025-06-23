from abc import ABC, abstractmethod

class Competidor(ABC):
    """Interface para entidades que podem competir em desafios."""

    @abstractmethod
    def obter_nome(self) -> str:
        """Retorna o nome do competidor."""
        raise NotImplementedError