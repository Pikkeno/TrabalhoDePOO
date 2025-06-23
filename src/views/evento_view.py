import flet as ft
from src.utils.logger import logger


def mostrar_cadastro_evento(page, pessoa, pessoa_controller, equipe_controller, evento_controller, voltar_callback):
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

    conteudo = ft.Container(
        ft.Column([
            tipo,
            nome_oponente,
            ft.ElevatedButton(
                "Criar Evento",
                on_click=criar_evento,
                style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
            ),
            output,
            ft.TextButton("Voltar", on_click=voltar_callback),
        ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        border_radius=8,
        bgcolor=ft.Colors.GREY_100,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400),
    )
    page.add(ft.Row([conteudo], alignment=ft.MainAxisAlignment.CENTER))