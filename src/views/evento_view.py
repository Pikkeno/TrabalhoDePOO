import flet as ft
from src.utils.logger import logger
from src.views.desafio_view import criar_campos_desafio

def mostrar_cadastro_evento(
    page,
    pessoa,
    pessoa_controller,
    equipe_controller,
    evento_controller,
    voltar_callback,
    dashboard_callback=None,
):
    page.clean()
    tipo = ft.Dropdown(label="Tipo", options=[ft.dropdown.Option("individual"), ft.dropdown.Option("equipe")], value="individual", width=250)
    nome_oponente = ft.TextField(label="Oponente", width=250)
    output = ft.Text()

    def criar_evento(e):
        try:
            if tipo.value == "individual":
                convidado = pessoa_controller.buscar_por_nome(nome_oponente.value)
            else:
                convidado = next((eq for eq in equipe_controller.equipes if eq.nome == nome_oponente.value), None)
            if not convidado:
                output.value = "Oponente nao encontrado"
                page.update()
                return
            evento_controller.criar_evento(pessoa if tipo.value == "individual" else next(eq for eq in equipe_controller.equipes if pessoa in eq.integrantes), convidado)
            output.value = "Evento criado e convite enviado"
        except StopIteration:
            output.value = "Voce nao pertence a nenhuma equipe"
        page.update()
        logger.info("Evento competitivo criado")

    controles = [
        tipo,
        nome_oponente,
        ft.ElevatedButton(
            "Criar Evento",
            on_click=criar_evento,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
        ),
        output,
        ft.TextButton("Voltar", on_click=voltar_callback),
    ]

    if dashboard_callback:
        controles.append(
            ft.TextButton("Voltar ao Dashboard", on_click=dashboard_callback)
        )

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


def mostrar_eventos(page, evento_controller, voltar_callback, dashboard_callback=None):
    """Exibe os eventos existentes com opcao de adicionar desafios."""
    page.clean()

    def abrir_criar_desafio(evento):
        return lambda e: mostrar_cadastro_desafio_evento(
            page,
            evento,
            evento_controller,
            lambda e: mostrar_eventos(
                page,
                evento_controller,
                voltar_callback,
                dashboard_callback,
            ),
            dashboard_callback,
        )

    lista_eventos = []
    if not evento_controller.eventos:
        lista_eventos.append(ft.ListTile(title=ft.Text("Nenhum evento.")))
    else:
        for idx, evento in enumerate(evento_controller.eventos, start=1):
            titulo = f"Evento {idx}: {evento.criador.obter_nome()} x {evento.convidado.obter_nome()}"
            subtitulo = ft.Text("Aceito" if evento.aceito else "Pendente")
            botao = ft.TextButton("Criar Desafio", on_click=abrir_criar_desafio(evento))
            lista_eventos.append(
                ft.ListTile(title=ft.Text(titulo), subtitle=subtitulo, trailing=botao)
            )

    controles = [
        ft.ListView(controls=lista_eventos, padding=10, spacing=10),
        ft.TextButton("Voltar", on_click=voltar_callback),
    ]

    if dashboard_callback:
        controles.append(
            ft.TextButton("Voltar ao Dashboard", on_click=dashboard_callback)
        )

    page.add(ft.Column(controles))


def mostrar_cadastro_desafio_evento(
    page,
    evento,
    evento_controller,
    voltar_callback,
    dashboard_callback=None,
):
    """Mostra formulario para criar desafio dentro de um evento."""
    page.clean()

    (
        descricao,
        data_inicio,
        data_fim,
        valor_aposta,
        limite_participantes,
    ) = criar_campos_desafio()
    output = ft.Text()

    def criar(e):
        try:
            desafio = evento_controller.adicionar_desafio_ao_evento(
                evento,
                descricao.value,
                data_inicio.value,
                data_fim.value,
                float(valor_aposta.value),
                int(limite_participantes.value),
            )
            output.value = f"Desafio {desafio.id} criado"  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            output.value = str(exc)
        page.update()

    controles = [
        descricao,
        data_inicio,
        data_fim,
        valor_aposta,
        limite_participantes,
        ft.ElevatedButton(
            "Criar Desafio",
            on_click=criar,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
        ),
        output,
        ft.TextButton("Voltar", on_click=voltar_callback),
    ]

    if dashboard_callback:
        controles.append(
            ft.TextButton("Voltar ao Dashboard", on_click=dashboard_callback)
        )

    page.add(
        ft.Column(
            controles,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )