import flet as ft

def cria_campo_login():
    usuario = ft.TextField(label="Usuário")
    senha = ft.TextField(label="Senha", password=True)
    return usuario, senha