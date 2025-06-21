from src.models.pessoa_models import Pessoa
from src.utils.logger import logger
from src.utils import json_db
import uuid

class PessoaController:
    def __init__(self):
        self.pessoas = []  # Lista de pessoas registradas
        self.carregar_pessoas()
        logger.info("PessoaController iniciado")

    def carregar_pessoas(self):
        """Carrega os dados de pessoas do arquivo JSON."""
        for dado in json_db.carregar_dados():
            pessoa = Pessoa(
                dado.get("nome"),
                dado.get("idm"),
                saldo=dado.get("saldo", 0),
                score=dado.get("score", 0),
                email=dado.get("email"),
                senha=dado.get("senha"),
            )
            self.pessoas.append(pessoa)

    def salvar_pessoas(self):
        """Persiste os dados atuais das pessoas no arquivo JSON."""
        dados = [
            {
                "nome": p.nome,
                "idm": p.idm,
                "saldo": p.saldo,
                "score": p.score,
                "email": p.email,
                "senha": p.senha,
            }
            for p in self.pessoas
        ]
        json_db.salvar_dados(dados)

    def criar_pessoa(self, nome, idm=None, email=None, senha=None):
        if idm is None:
            # Gera um IDM único e aleatório
            while True:
                novo_id = uuid.uuid4().hex
                if not self.buscar_por_id(novo_id):
                    idm = novo_id
                    break
        elif self.buscar_por_id(idm):
            raise ValueError("IDM já existente")
        
        pessoa = Pessoa(nome, idm, saldo=0, score=0, email=email, senha=senha)
        self.pessoas.append(pessoa)
        logger.info("Pessoa criada: %s", nome)
        return pessoa
    
    def registrar_pessoa(self, nome, idm, email, senha):
        """Registra uma pessoa garantindo unicidade de IDM ou email."""
        if self.buscar_por_id(idm) or any(p.email == email for p in self.pessoas):
            logger.warning("Tentativa de cadastro duplicado: %s", idm)
            return None
        pessoa = self.criar_pessoa(nome, idm, email=email, senha=senha)
        self.salvar_pessoas()
        return pessoa
    
    def buscar_por_id(self, idm):
        """Retorn a uma pessoa pelo IDM."""
        for pessoa in self.pessoas:
            if pessoa.idm == idm:
                return pessoa
        return None
    
    def autenticar(self, email, senha):
        """Retorna a pessoa autenticada ou None se falhar."""
        for pessoa in self.pessoas:
            if pessoa.email == email and pessoa.senha == senha:
                return pessoa
        return None
    
    def adicionar_amigo(self, pessoa, id_amigo):
        """Adiciona um amigo"""
        amigo = self.buscar_por_id(id_amigo)
        if not amigo:
            return "Amigo não encontrado."
        if pessoa.adicionar_amigo(amigo):
            return f"{amigo.nome} adicionado como amigo."
        return f"{amigo.nome} já é amigo."
    

    def realizar_aposta(self, pessoa, valor_aposta):
        """
        Faz uma aposta para a pessoa, verificando se o saldo é suficiente.
        """
        if pessoa.saldo >= valor_aposta:
            pessoa.saldo -= valor_aposta  # Deduz o valor da aposta do saldo
            
            logger.info(
                "Aposta de %s realizada no valor de %s. Novo saldo: %s",
                pessoa.nome, valor_aposta, pessoa.saldo
            )
            return f"Aposta de {valor_aposta} realizada por {pessoa.nome}. Novo saldo: {pessoa.saldo}"
        else:
            logger.warning(
                "Saldo insuficiente para %s realizar aposta de %s. Saldo atual: %s",
                pessoa.nome, valor_aposta, pessoa.saldo
            )
            return f"{pessoa.nome} não tem saldo suficiente para fazer essa aposta."


