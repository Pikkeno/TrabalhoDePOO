class Pessoa:
    def __init__(self, nome, idm, saldo, score, valor_aposta, oponente):
        self.nome = nome
        self.idm = idm
        self.saldo = saldo
        self.score = score
        self.valor_aposta = valor_aposta
        self.oponente = oponente

    def __str__(self):
        return f"Pessoa(nome={self.nome}, idm={self.idm}, saldo={self.saldo}, score={self.score})"

    