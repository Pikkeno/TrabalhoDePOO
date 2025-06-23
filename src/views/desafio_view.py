import flet as ft
from src.utils.logger import logger

def criar_campos_desafio():
    """Cria e retorna os campos de entrada do formulário de Desafio."""
    descricao = ft.TextField(label="Descrição do Desafio", width=250)
    data_inicio = ft.TextField(label="Data de Início (DD-MM-YYYY)", width=250)
    data_fim = ft.TextField(label="Data de Fim (DD-MM-YYYY)", width=250)
    valor_aposta = ft.TextField(label="Valor da Aposta", value="100", width=250)
    limite_participantes = ft.TextField(label="Limite de Participantes", value="2", width=250)
    logger.info("Campos de desafio criados")
    return descricao, data_inicio, data_fim, valor_aposta, limite_participantes

def mostrar_cadastro_desafio(
    page, pessoa, desafio_controller, equipe_controller, voltar_callback
):
    """Exibe a tela de criação de desafio."""
    page.clean()
    (
        descricao,
        data_inicio,
        data_fim,
        valor_aposta,
        limite_participantes,
    ) = criar_campos_desafio()
    competicao_dropdown = ft.Dropdown(
        label="Tipo de Competição",
        options=[
            ft.dropdown.Option("individual"),
            ft.dropdown.Option("equipe"),
        ],
        value="individual",
        width=250,
    )
    adversarios = ft.TextField(
        label="Adversários (nomes separados por vírgula)", width=250
    )
    equipe_adv = ft.TextField(label="Equipe Adversária", width=250)
    output = ft.Text()

    def criar_desafio(e):
        try:
            desafio = desafio_controller.criar_desafio(
                1,
                descricao.value,
                data_inicio.value,
                data_fim.value,
                int(valor_aposta.value),
                int(limite_participantes.value),
                competicao=competicao_dropdown.value,
                criador=pessoa,
                adversarios=[
                    p
                    for nome in adversarios.value.split(",")
                    if (
                        p := desafio_controller.equipe_controller.pessoa_controller.buscar_por_nome(  # type: ignore
                            nome.strip()
                        )
                    )
                ],
                equipe_adversaria=next(
                    (
                        eq
                        for eq in equipe_controller.equipes
                        if eq.nome == equipe_adv.value
                    ),
                    None,
                ),
            )
        except ValueError as exc:
            output.value = f"Erro ao criar desafio: {exc}"
        else:
            mensagem = desafio_controller.adicionar_participante(desafio, pessoa)
            output.value = (
                f"Desafio criado: {desafio.descricao}\n{mensagem}"
            )
        page.update()
        logger.info("Desafio criado via Flet: %s", descricao.value)

    conteudo = ft.Container(
        ft.Column(
            [
                descricao,
                data_inicio,
                data_fim,
                valor_aposta,
                limite_participantes,
                ft.ElevatedButton(
                    "Criar Desafio",
                    on_click=criar_desafio,
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