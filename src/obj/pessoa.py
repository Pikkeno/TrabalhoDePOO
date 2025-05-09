class Pessoa:
    def __init__(self, nome, idm, saldo, score):
        self.nome = nome
        self.idm = idm
        self.saldo = saldo
        self.score = score

    def __str__(self):
        return f"Pessoa(nome={self.nome}, idm={self.idm}, saldo={self.saldo}, score={self.score})"

    def aposta(self, valor_aposta):
        # Implementar lógica para fazer uma aposta
        pass

    def desafiar(self, oponente, valor_aposta):
        # Implementar lógica para desafiar um oponente
        pass