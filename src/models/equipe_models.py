class Equipe:
    """Representa um grupo de pessoas."""

    def __init__(self, nome, criador):
        self.nome = nome
        self.integrantes = [criador]

    def adicionar_integrante(self, pessoa):
        if pessoa not in self.integrantes:
            self.integrantes.append(pessoa)
            return True
        return False