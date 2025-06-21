class Pessoa:
    def __init__(self, nome, idm, saldo=0, score=0, email=None, senha=None, valor_aposta=None, oponente=None):
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
        email : str | None, optional
            E-mail da pessoa.
        senha : str | None, optional
            Senha da pessoa.
        valor_aposta : int | float | None, optional
            Valor da aposta atual da pessoa. ``None`` indica que não há aposta registrada.
        oponente : Pessoa | None, optional
            Oponente da pessoa em uma aposta/desafio. ``None`` indica que não há oponente definido.
        """
        self.nome = nome
        self.idm = idm
        self._saldo = 0
        self.saldo = saldo
        self._score = 0
        self.score = score
        self.email = email
        self.senha = senha
        self._valor_aposta = None
        self.valor_aposta = valor_aposta
        self.oponente = oponente
        self.amigos = []

        @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = max(0, value)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = max(0, value)

    @property
    def valor_aposta(self):
        return self._valor_aposta

    @valor_aposta.setter
    def valor_aposta(self, value):
        if value is None:
            self._valor_aposta = None
        else:
            self._valor_aposta = max(0, value)

    def __str__(self):
        return (
            f"Pessoa(nome={self.nome}, idm={self.idm}, saldo={self.saldo}, "
            f"score={self.score}, email={self.email})"
        )
    
    def adicionar_amigo(self, amigo):
        """Adiciona uma pessoa à lista de amigos se ainda não estiver presente."""
        if amigo not in self.amigos:
            self.amigos.append(amigo)
            return True
        return False
    