import flet as ft


def criar_campos_desafio():
    """Cria e retorna os campos de entrada do formulário de Desafio."""
    descricao = ft.TextField(label="Descrição do Desafio")
    data_inicio = ft.TextField(label="Data de Início (DD-MM-AAAA)")
    data_fim = ft.TextField(label="Data de Fim (DD-MM-AAAA)")
    valor_aposta = ft.TextField(label="Valor da Aposta", value="100")
    limite_participantes = ft.TextField(label="Limite de Participantes", value="2")
    return descricao, data_inicio, data_fim, valor_aposta, limite_participantes