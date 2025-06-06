class Pessoa:
    def __init__(self, nome, idm, saldo=0, score=0, valor_aposta=None, oponente=None):
        """Cria uma nova pessoa.

        Parameters
        ----------
        nome : str
            Nome da pessoa.
        idm : str
            Identificador único da pessoa.
        saldo : int | float
            Saldo inicial disponível.
        score : int
            Score inicial da pessoa.
        valor_aposta : int | float | None, optional
            Valor da aposta atual da pessoa. ``None`` indica que não há aposta registrada.
        oponente : Pessoa | None, optional
            Oponente da pessoa em uma aposta/desafio. ``None`` indica que não há oponente definido.
        """
        self.nome = nome
        self.idm = idm
        self.saldo = max(0, saldo)
        self.score = max(0, score)
        self.valor_aposta = valor_aposta
        self.oponente = oponente

    def __str__(self):
        return f"Pessoa(nome={self.nome}, idm={self.idm}, saldo={self.saldo}, score={self.score})"

    