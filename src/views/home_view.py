import flet as ft
from src.views.team_view import mostrar_gerenciamento_equipes
from src.views.desafio_view import mostrar_cadastro_desafio
from src.views.dashboard_view import mostrar_dashboard
from src.views.evento_view import mostrar_cadastro_evento
from src.utils.logger import logger


def mostrar_pos_login(
    page,
    pessoa,
    pessoa_controller,
    equipe_controller,
    evento_controller,
    desafio_controller,
    voltar_callback,
):
    """Tela inicial após o login com opções sociais."""
    page.clean()
    dashboard_callback = lambda e: mostrar_dashboard(
        page,
        desafio_controller,
        evento_controller,
        lambda e: mostrar_pos_login(
            page,
            pessoa,
            pessoa_controller,
            equipe_controller,
            evento_controller,
            desafio_controller,
            voltar_callback,
        ),
    )
    nome_equipe = ft.TextField(label="Nome da Equipe", width=250)
    nome_usuario_amigo = ft.TextField(label="Nome de Usuário do Amigo", width=250)
    output = ft.Text()

    def criar_equipe(e):
        try:
            equipe_controller.criar_equipe(nome_equipe.value, pessoa)
        except Exception as exc:  # noqa: BLE001
            output.value = f"Erro ao criar equipe: {exc}"
            logger.error("Falha ao criar equipe: %s", exc)
        else:
            output.value = f"Equipe {nome_equipe.value} criada."
            logger.info("Equipe criada: %s", nome_equipe.value)
        page.update()

    def adicionar_amigo(e):
        try:
            output.value = pessoa_controller.adicionar_amigo(
                pessoa, nome_usuario_amigo.value
            )
        except Exception as exc:  # noqa: BLE001
            output.value = f"Erro ao adicionar amigo: {exc}"
            logger.error("Falha ao adicionar amigo: %s", exc)
        page.update()

    conteudo = ft.Container(
        ft.Column(
            [
                ft.Text(
                    f"Bem-vindo, {pessoa.nome}!",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    [
                        ft.Text(f"Saldo: {pessoa.saldo}"),
                        ft.Text(f"Score: {pessoa.score}"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                nome_equipe,
                ft.ElevatedButton(
                    "Criar Equipe",
                    on_click=criar_equipe,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
                nome_usuario_amigo,
                ft.ElevatedButton(
                    "Adicionar Amigo",
                    on_click=adicionar_amigo,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
                ft.ElevatedButton(
                    "Gerenciar Equipes",
                    on_click=lambda e: mostrar_gerenciamento_equipes(
                        page,
                        pessoa,
                        equipe_controller,
                        pessoa_controller,
                        lambda e: mostrar_pos_login(
                            page,
                            pessoa,
                            pessoa_controller,
                            equipe_controller,                            
                            evento_controller,
                            desafio_controller,
                            voltar_callback,

                        ),
                        dashboard_callback,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
                ft.ElevatedButton(
                    "Criar Desafio",
                    on_click=lambda e: mostrar_cadastro_desafio(
                        page,
                        pessoa,
                        desafio_controller,
                        equipe_controller,
                        lambda e: mostrar_pos_login(
                            page,
                            pessoa,
                            pessoa_controller,
                            equipe_controller,
                            evento_controller,
                            desafio_controller,
                            voltar_callback,
                        ),
                        dashboard_callback,
                        individual_only=True,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE,
                    ),
                ),
                ft.ElevatedButton(
                    "Criar Evento Competitivo",
                    on_click=lambda e: mostrar_cadastro_evento(
                        page,
                        pessoa,
                        pessoa_controller,
                        equipe_controller,
                        evento_controller,
                        lambda e: mostrar_pos_login(
                            page,
                            pessoa,
                            pessoa_controller,
                            equipe_controller,
                            evento_controller,
                            desafio_controller,
                            voltar_callback,
                        ),
                        dashboard_callback,
                    ),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
                ),
                ft.ElevatedButton(
                    "Ir para Dashboard",
                    on_click=lambda e: mostrar_dashboard(
                        page,
                        desafio_controller,
                        evento_controller,
                        lambda e: mostrar_pos_login(
                            page,
                            pessoa,
                            pessoa_controller,
                            equipe_controller,
                            evento_controller,
                            desafio_controller,
                            voltar_callback,
                        ),
                    ),
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
    page.update()