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


from src.views.evento_view import mostrar_cadastro_desafio_evento


def listar_eventos(
    evento_controller,
    desafio_controller,
    page,
    voltar_callback,
    dashboard_callback,
):
    """Retorna controles para listar eventos."""
    if not evento_controller.eventos:
        return [ft.ListTile(title=ft.Text("Nenhum evento."))]

    controles = []
    for idx, evento in enumerate(evento_controller.eventos, start=1):
        titulo = f"Evento {idx}: {evento.criador.obter_nome()} x {evento.convidado.obter_nome()}"
        subtitulo = ft.Text("Aceito" if evento.aceito else "Pendente")
        controles.append(
            ft.ListTile(
                title=ft.Text(titulo),
                subtitle=subtitulo,
                trailing=ft.TextButton(
                    "Criar Desafio",
                    on_click=lambda e, ev=evento: mostrar_cadastro_desafio_evento(
                        page,
                        ev,
                        evento_controller,
                        lambda e: mostrar_dashboard(
                            page,
                            desafio_controller,
                            evento_controller,
                            voltar_callback,
                        ),
                        dashboard_callback,
                    ),
                ),
            )
        )
    return controles


def mostrar_dashboard(page, desafio_controller, evento_controller, voltar_callback):    
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

    eventos_lista = ft.ListView(
        controls=listar_eventos(
            evento_controller,
            desafio_controller,
            page,
            voltar_callback,
            voltar_callback,
        ),
        padding=10,
        spacing=10,
    )

    tabs = ft.Tabs(
        expand=1,
        tabs=[
            ft.Tab(text="Abertos", content=abertos),
            ft.Tab(text="Encerrados", content=encerrados),
            ft.Tab(text="Histórico", content=historico),
            ft.Tab(text="Eventos", content=eventos_lista),
        ],
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [ft.IconButton(ft.Icons.ARROW_BACK, on_click=voltar_callback)],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(tabs, padding=20, bgcolor=ft.Colors.GREY_100),
                ft.TextButton("Voltar", on_click=voltar_callback),
            ]
        )
    )