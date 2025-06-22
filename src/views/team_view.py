import flet as ft
from src.utils.logger import logger


def mostrar_gerenciamento_equipes(page, pessoa, equipe_controller, pessoa_controller, voltar_callback):
    """Tela para gerenciar equipes do usuario."""
    page.clean()
    page.title = "Gerenciamento de Equipes"
    page.update()

    nome_equipe = ft.TextField(label="Nome da Equipe", width=250)
    id_membro = ft.TextField(label="ID do Membro", width=250)
    output = ft.Text()
    integrantes_list = ft.ListView(padding=10, spacing=5)

    def listar_equipes_usuario():
        return [eq for eq in equipe_controller.equipes if pessoa in eq.integrantes]

    def mostrar_integrantes(e=None):
        equipe = next((eq for eq in listar_equipes_usuario() if eq.nome == nome_equipe.value), None)
        integrantes_list.controls.clear()
        if equipe:
            for integrante in equipe.integrantes:
                integrantes_list.controls.append(
                    ft.ListTile(title=ft.Text(f"{integrante.nome} ({integrante.idm})"))
                )
        else:
            integrantes_list.controls.append(ft.ListTile(title=ft.Text("Equipe nao encontrada.")))
        page.update()

    def adicionar_membro(e):
        equipe = next((eq for eq in listar_equipes_usuario() if eq.nome == nome_equipe.value), None)
        if not equipe:
            output.value = "Equipe nao encontrada."
        else:
            membro = pessoa_controller.buscar_por_id(id_membro.value)
            if membro is None:
                output.value = "Membro nao encontrado."
            else:
                if equipe_controller.adicionar_integrante(equipe, membro):
                    output.value = f"{membro.nome} adicionado a {equipe.nome}."
                else:
                    output.value = f"{membro.nome} ja esta na equipe."
        mostrar_integrantes()
        page.update()

    def remover_membro(e):
        equipe = next((eq for eq in listar_equipes_usuario() if eq.nome == nome_equipe.value), None)
        if not equipe:
            output.value = "Equipe nao encontrada."
        else:
            membro = pessoa_controller.buscar_por_id(id_membro.value)
            if membro is None:
                output.value = "Membro nao encontrado."
            else:
                if equipe_controller.remover_integrante(equipe, membro):
                    output.value = f"{membro.nome} removido de {equipe.nome}."
                else:
                    output.value = f"{membro.nome} nao esta na equipe."
        mostrar_integrantes()
        page.update()

    conteudo = ft.Container(
        ft.Column(
            [
                ft.Text("Suas Equipes:"),
                ft.ListView(
                    controls=[ft.ListTile(title=ft.Text(eq.nome)) for eq in listar_equipes_usuario()],
                    padding=10,
                    spacing=5,
                ),
                nome_equipe,
                ft.Row(
                    [
                        id_membro,
                        ft.ElevatedButton(
                            "Mostrar Integrantes",
                            on_click=mostrar_integrantes,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE,
                            ),
                        ),
                    ]
                ),
                integrantes_list,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Adicionar Membro",
                            on_click=adicionar_membro,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE,
                            ),
                        ),
                        ft.ElevatedButton(
                            "Remover Membro",
                            on_click=remover_membro,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE,
                            ),
                        ),
                        ft.TextButton("Voltar", on_click=voltar_callback),
                    ]
                ),
                output,
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