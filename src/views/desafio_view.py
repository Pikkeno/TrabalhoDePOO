import flet as ft
from src.utils.logger import logger

def criar_campos_desafio():
    """Cria e retorna os campos de entrada do formulário de Desafio."""
    descricao = ft.TextField(label="Descrição do Desafio")
    data_inicio = ft.TextField(label="Data de Início (DD-MM-YYYY)")
    data_fim = ft.TextField(label="Data de Fim (DD-MM-YYYY)")
    valor_aposta = ft.TextField(label="Valor da Aposta", value="100")
    limite_participantes = ft.TextField(label="Limite de Participantes", value="2")
    logger.info("Campos de desafio criados")
    return descricao, data_inicio, data_fim, valor_aposta, limite_participantes