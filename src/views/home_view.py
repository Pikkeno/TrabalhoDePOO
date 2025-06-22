import flet as ft
from src.views.team_view import mostrar_gerenciamento_equipes
from src.views.desafio_view import mostrar_cadastro_desafio
from src.views.dashboard_view import mostrar_dashboard
from src.utils.logger import logger


def mostrar_pos_login(page, pessoa, pessoa_controller, equipe_controller, desafio_controller):
    """Tela inicial após o login com opções sociais."""
    page.clean()
    nome_equipe = ft.TextField(label="Nome da Equipe")
    nome_amigo = ft.TextField(label="Nome do Amigo")
    output = ft.Text()

    def criar_equipe(e):
        equipe_controller.criar_equipe(nome_equipe.value, pessoa)
        output.value = f"Equipe {nome_equipe.value} criada."
        page.update()

    def adicionar_amigo(e):
        output.value = pessoa_controller.adicionar_amigo(pessoa, nome_amigo.value)
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(f"Bem-vindo, {pessoa.nome}!"),
                nome_equipe,
                ft.ElevatedButton("Criar Equipe", on_click=criar_equipe),
                nome_amigo,
                ft.ElevatedButton("Adicionar Amigo", on_click=adicionar_amigo),
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
                            desafio_controller,
                        ),
                    ),
                ),
                ft.ElevatedButton(
                    "Criar Desafio",
                    on_click=lambda e: mostrar_cadastro_desafio(
                        page,
                        pessoa,
                        desafio_controller,
                        lambda e: mostrar_pos_login(
                            page,
                            pessoa,
                            pessoa_controller,
                            equipe_controller,
                            desafio_controller,
                        ),
                    ),
                ),
                ft.ElevatedButton(
                    "Ir para Dashboard",
                    on_click=lambda e: mostrar_dashboard(page, desafio_controller),
                ),
                output,
            ]
        )
    )