import flet as ft
from src.utils.logger import logger

def criar_campos_pessoa():
    """Cria e retorna os campos de entrada do formulário de Pessoa."""
    nome = ft.TextField(label="Nome")
    idm = ft.TextField(label="IDM")
    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)
    logger.info("Campos de pessoa criados")
    return nome, idm, email, senha
