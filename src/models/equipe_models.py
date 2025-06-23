from .competidor_base import Competidor


class Equipe(Competidor):
    """Representa um grupo de pessoas."""

    def __init__(self, nome, criador):
        self.nome = nome
        self.criador = criador
        self.integrantes = [criador]

    def obter_nome(self) -> str:
        """Retorna o nome da equipe."""
        return self.nome

    def adicionar_integrante(self, pessoa):
        if pessoa not in self.integrantes:
            self.integrantes.append(pessoa)
            return True
        return False

    def remover_integrante(self, pessoa):
        """Remove um integrante da equipe se estiver presente."""
        if pessoa in self.integrantes:
            self.integrantes.remove(pessoa)
            return True
        return False

    def entrar_desafio(self, desafio):
        """Adiciona todos os integrantes ao desafio se houver vagas."""
        if len(desafio.participantes) + len(self.integrantes) > desafio.limite_participantes:
            return False
        for integrante in self.integrantes:
            desafio.add_participante(integrante)
        return True