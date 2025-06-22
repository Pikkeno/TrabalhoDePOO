import flet as ft
from src.utils.logger import logger


def listar_desafios_por_status(desafio_controller, status: str):
    """Gera uma lista de ListTile para os desafios com o status informado."""
    desafios = [d for d in desafio_controller.desafios if d.status == status]
    if not desafios:
        return [ft.ListTile(title=ft.Text("Nenhum desafio."))]
    return [
        ft.ListTile(title=ft.Text(f"Desafio {d.id}"), subtitle=ft.Text(d.descricao))
        for d in desafios
    ]


def mostrar_dashboard(page, desafio_controller):
    page.clean()
    abertos = ft.ListView(
        controls=listar_desafios_por_status(desafio_controller, "Ativo"),
        padding=10,
        spacing=10,
    )

    encerrados = ft.ListView(
        controls=listar_desafios_por_status(desafio_controller, "Encerrado"),
        padding=10,
        spacing=10,
    )

    historico = ft.ListView(
        controls=listar_desafios_por_status(desafio_controller, "Encerrado"),
        padding=10,
        spacing=10,
    )

    tabs = ft.Tabs(
        expand=1,
        tabs=[
            ft.Tab(text="Abertos", content=abertos),
            ft.Tab(text="Encerrados", content=encerrados),
            ft.Tab(text="Histórico", content=historico),
        ],
    )

    page.add(ft.Container(tabs, padding=20, bgcolor=ft.Colors.GREY_100))