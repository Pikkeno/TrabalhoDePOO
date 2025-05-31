
class Desafio:
    def __init__(self, id, descricao, data_inicio, data_fim, valor_aposta):
        self.id = id
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.valor_aposta = valor_aposta
        self.status = "Ativo"  # O status inicial é 'Ativo'
        self.participantes = []  # Lista de participantes
        self.vencedor = None  # Nenhum vencedor até o desafio ser encerrado

    def add_participante(self, participante):
        """
        Adiciona um participante ao desafio.
        """
        if len(self.participantes) < 2:
            self.participantes.append(participante)
            return True
        return False

    def remover_participante(self, participante):
        """
        Remove um participante do desafio.
        """
        if participante in self.participantes:
            self.participantes.remove(participante)
            return True
        return False

    def encerrar_desafio(self, vencedor):
        """
        Encerra o desafio e define um vencedor.
        """
        if len(self.participantes) < 2:
            return False, "Não há participantes suficientes para encerrar o desafio."
        
        self.vencedor = vencedor
        self.status = "Encerrado"
        return True, f"Desafio {self.id} encerrado. O vencedor é {self.vencedor.nome}."

    def recompensa_participantes(self):
        """
        #Recompensa os participantes com base no resultado do desafio.
        """
        if self.status != "Encerrado":
            return False, "O desafio precisa ser encerrado antes de recompensar os participantes."
        
        if self.vencedor:
            # Recompensa o vencedor com o valor da aposta
            self.vencedor.saldo += self.valor_aposta
            return True, f"{self.vencedor.nome} recebeu a recompensa de R${self.valor_aposta}."
        
        return False, "Não há vencedor para recompensar."
