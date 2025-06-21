import flet as ft
from src.utils.logger import logger

def cria_campo_login():
    usuario = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)
    logger.info("Campos de login criados")
    return usuario, senha