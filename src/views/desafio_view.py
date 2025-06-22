import flet as ft
from src.utils.logger import logger

def criar_campos_desafio():
    """Cria e retorna os campos de entrada do formulário de Desafio."""
    descricao = ft.TextField(label="Descrição do Desafio")
    data_inicio = ft.TextField(label="Data de Início (DD-MM-YYYY)")
    data_fim = ft.TextField(label="Data de Fim (DD-MM-YYYY)")
    valor_aposta = ft.TextField(label="Valor da Aposta", value="100")
    limite_participantes = ft.TextField(label="Limite de Participantes", value="2")
    logger.info("Campos de desafio criados")
    return descricao, data_inicio, data_fim, valor_aposta, limite_participantes

def mostrar_cadastro_desafio(page, pessoa, desafio_controller, voltar_callback):
    """Exibe a tela de criação de desafio."""
    page.clean()
    (
        descricao,
        data_inicio,
        data_fim,
        valor_aposta,
        limite_participantes,
    ) = criar_campos_desafio()
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

    page.add(
        ft.Column(
            [
                descricao,
                data_inicio,
                data_fim,
                valor_aposta,
                limite_participantes,
                ft.ElevatedButton("Criar Desafio", on_click=criar_desafio),
                output,
                ft.TextButton("Voltar", on_click=voltar_callback),
            ]
        )
    )