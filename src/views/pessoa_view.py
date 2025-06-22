import flet as ft
from src.utils.logger import logger

def criar_campos_pessoa():
    """Cria e retorna os campos de entrada do formulário de Pessoa."""
    nome = ft.TextField(label="Nome", width=250)
    email = ft.TextField(label="Email", width=250)
    senha = ft.TextField(label="Senha", password=True, width=250)
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

    conteudo = ft.Container(
        ft.Column(
            [
                nome,
                email,
                senha,
                ft.ElevatedButton(
                    "Criar Conta",
                    on_click=criar_conta,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
                output,
                ft.TextButton("Voltar", on_click=voltar_callback),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        border_radius=8,
        bgcolor=ft.Colors.GREY_100,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400),
    )

    page.add(ft.Row([conteudo], alignment=ft.MainAxisAlignment.CENTER))

