import flet as ft
from src.utils.logger import logger
from src.views.pessoa_view import mostrar_cadastro_pessoa
from src.views.home_view import mostrar_pos_login

def cria_campo_login():
    usuario = ft.TextField(label="Email", width=250)
    senha = ft.TextField(label="Senha", password=True, width=250)
    logger.info("Campos de login criados")
    return usuario, senha


def realizar_login(
    page,
    pessoa_controller,
    usuario_login,
    senha_login,
    login_output,
    equipe_controller,
    desafio_controller,
):
    pessoa = pessoa_controller.autenticar(
        usuario_login.value,
        senha_login.value,
    )
    if pessoa:
        login_output.value = f"Login de {pessoa.nome}"
        logger.info("Login realizado por %s", pessoa.nome)
        mostrar_pos_login(
            page,
            pessoa,
            pessoa_controller,
            equipe_controller,
            desafio_controller,
            lambda e: mostrar_login(
                page,
                pessoa_controller,
                equipe_controller,
                desafio_controller,
            ),
        )
    else:
        login_output.value = "Credenciais inválidas."
        logger.warning(
            "Falha no login para %s", usuario_login.value
        )
    page.update()


def mostrar_login(
    page,
    pessoa_controller,
    equipe_controller,
    desafio_controller,
    voltar_callback=None,
):
    usuario_login, senha_login = cria_campo_login()
    login_output = ft.Text()
    page.clean()
    controles = [
        usuario_login,
        senha_login,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Entrar",
                    on_click=lambda e: realizar_login(
                        page,
                        pessoa_controller,
                        usuario_login,
                        senha_login,
                        login_output,
                        equipe_controller,
                        desafio_controller,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
                ft.TextButton(
                    "Criar conta",
                    on_click=lambda e: mostrar_cadastro_pessoa(
                        page,
                        pessoa_controller,
                        lambda e: mostrar_login(
                            page,
                            pessoa_controller,
                            equipe_controller,
                            desafio_controller,
                        ),
                    ),
                    
                ),
            ]
            
    ),
        login_output,
    ]

    if voltar_callback is not None:
        controles.append(ft.TextButton("Voltar", on_click=voltar_callback))

    conteudo = ft.Container(
        ft.Column(
            controles,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        border_radius=8,
        bgcolor=ft.Colors.GREY_100,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400),
    )

    page.add(ft.Row([conteudo], alignment=ft.MainAxisAlignment.CENTER))