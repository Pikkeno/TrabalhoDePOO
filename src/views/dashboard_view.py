import flet as ft
from src.utils.logger import logger


def listar_desafios_por_status(
    desafio_controller, status: str, usuario=None, evento_controller=None
):
    """Gera uma lista de ``ft.ListTile`` para os desafios com o status informado.

    Se ``usuario`` for fornecido, inclui desafios em que o usuário participa ou
    que estejam associados a eventos do qual ele faz parte. Dessa forma, os
    desafios criados dentro de eventos continuam visíveis para seus criadores.
    """

    if usuario is None:
        desafios = [d for d in desafio_controller.desafios if d.status == status]
    else:
        desafios = []
        for desafio in desafio_controller.desafios:
            if desafio.status != status:
                continue

            participa = usuario in getattr(desafio, "participantes", [])
            em_evento = False
            if evento_controller:
                for evento in evento_controller.eventos:
                    if any(d.id == desafio.id for d in evento.desafios) and (
                        evento.criador == usuario or evento.convidado == usuario
                    ):
                        em_evento = True
                        break

            if participa or em_evento:
                desafios.append(desafio)
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
    usuario,
    page,
    voltar_callback,
    dashboard_callback,
):
    """Retorna controles para listar eventos."""
    eventos_usuario = [
        e
        for e in evento_controller.eventos
        if e.criador == usuario or e.convidado == usuario
    ]
    if not eventos_usuario:
        return [ft.ListTile(title=ft.Text("Nenhum evento."))]

    controles = []
    for idx, evento in enumerate(eventos_usuario, start=1):
        titulo = f"Evento {idx}: {evento.criador.obter_nome()} x {evento.convidado.obter_nome()}"
        controles_evento = []
        if evento.convidado == usuario and not evento.aceito:
            controles_evento.append(
                ft.TextButton(
                    "Aceitar",
                    on_click=lambda e, ev=evento: evento_controller.aceitar_evento(ev, usuario),
                )
            )
            controles_evento.append(
                ft.TextButton(
                    "Recusar",
                    on_click=lambda e, ev=evento: evento_controller.recusar_evento(ev, usuario),
                )
            )
        else:
            controles_evento.append(
                ft.TextButton(
                    "Criar Desafio",
                    on_click=lambda e, ev=evento: mostrar_cadastro_desafio_evento(
                        page,
                        usuario,
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
                )
            )

        subtitulo = ft.Text("Aceito" if evento.aceito else "Pendente")
        controles.append(
            ft.ListTile(
                title=ft.Text(titulo),
                subtitle=subtitulo,
                trailing=ft.Row(controles_evento, spacing=10),
            )
        )
    return controles


def mostrar_dashboard(page, usuario, desafio_controller, evento_controller, voltar_callback):    
    page.clean()
    abertos = ft.ListView(
        controls=listar_desafios_por_status(
            desafio_controller,
            "Ativo",
            usuario,
            evento_controller,
        ),
        padding=10,
        spacing=10,
    )

    encerrados = ft.ListView(
        controls=listar_desafios_por_status(
            desafio_controller,
            "Encerrado",
            usuario,
            evento_controller,
        ),
        padding=10,
        spacing=10,
    )

    historico = ft.ListView(
        controls=listar_desafios_por_status(
            desafio_controller,
            "Encerrado",
            usuario,
            evento_controller,
        ),
        padding=10,
        spacing=10,
    )

    eventos_lista = ft.ListView(
        controls=listar_eventos(
            evento_controller,
            desafio_controller,
            usuario,
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