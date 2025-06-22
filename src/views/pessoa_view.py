import flet as ft
from src.utils.logger import logger

def criar_campos_pessoa():
    """Cria e retorna os campos de entrada do formulário de Pessoa."""
    nome = ft.TextField(label="Nome")
    email = ft.TextField(label="Email")
    senha = ft.TextField(label="Senha", password=True)
    logger.info("Campos de pessoa criados")
    return nome, email, senha

def mostrar_cadastro_pessoa(page, pessoa_controller, voltar_callback):
    """Exibe a tela de criação de conta."""
    page.clean()
    nome, email, senha = criar_campos_pessoa()
    output = ft.Text()

    def criar_conta(e):
        pessoa = pessoa_controller.registrar_pessoa(
            nome.value,
            None,
            email=email.value,
            senha=senha.value,
        )
        if pessoa is None:
            output.value = "Email ou ID já cadastrado."
            logger.warning(
                "Tentativa de cadastro com email ou ID duplicado: %s", email.value
            )
        else:
            output.value = f"Conta criada para {pessoa.nome}. "
            logger.info("Conta criada para %s", pessoa.nome)
        page.update()

    page.add(
        ft.Column(
            [
                nome,
                email,
                senha,
                ft.ElevatedButton("Criar Conta", on_click=criar_conta),
                output,
                ft.TextButton("Voltar", on_click=voltar_callback),
            ]
        )
    )

