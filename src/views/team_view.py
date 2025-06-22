import flet as ft
from src.utils.logger import logger


def mostrar_gerenciamento_equipes(page, pessoa, equipe_controller, pessoa_controller, voltar_callback):
    """Tela para gerenciar equipes do usuario."""
    page.clean()

    nome_equipe = ft.TextField(label="Nome da Equipe")
    id_membro = ft.TextField(label="ID do Membro")
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

    page.add(
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
                        ft.ElevatedButton("Mostrar Integrantes", on_click=mostrar_integrantes),
                    ]
                ),
                integrantes_list,
                ft.Row(
                    [
                        ft.ElevatedButton("Adicionar Membro", on_click=adicionar_membro),
                        ft.ElevatedButton("Remover Membro", on_click=remover_membro),
                        ft.TextButton("Voltar", on_click=voltar_callback),
                    ]
                ),
                output,
            ]
        )
    )