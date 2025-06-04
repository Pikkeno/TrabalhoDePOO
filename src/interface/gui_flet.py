import flet as ft
from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController

def flet_main(page: ft.Page):
    page.title = "Sistema de Desafios"

    desafio_controller = DesafioController()
    pessoa_controller = PessoaController()

    nome = ft.TextField(label="Nome")
    idm = ft.TextField(label="IDM")
    saldo = ft.TextField(label="Saldo Inicial", value="1000")
    score = ft.TextField(label="Score Inicial", value="0")

    descricao = ft.TextField(label="Descrição do Desafio")
    data_inicio = ft.TextField(label="Data de Início (YYYY-MM-DD)")
    data_fim = ft.TextField(label="Data de Fim (YYYY-MM-DD)")
    valor_aposta = ft.TextField(label="Valor da Aposta", value="100")
    limite_participantes = ft.TextField(label="Limite de Participantes", value="2")

    output = ft.Text()

    def criar_pessoa_desafio(e):
        pessoa = pessoa_controller.criar_pessoa(
            nome.value,
            idm.value,
            int(saldo.value),
            int(score.value)
        )
        desafio = desafio_controller.criar_desafio(
            1,
            descricao.value,
            data_inicio.value,
            data_fim.value,
            int(valor_aposta.value),
            int(limite_participantes.value)
        )
        mensagem = desafio_controller.adicionar_participante(desafio, pessoa)
        output.value = (
            f"Pessoa criada: {pessoa.nome}\n"
            f"Desafio criado: {desafio.descricao}\n"
            f"{mensagem}"
        )
        page.update()

    page.add(
        ft.Column(
            [
                nome,
                idm,
                saldo,
                score,
                descricao,
                data_inicio,
                data_fim,
                valor_aposta,
                limite_participantes,
                ft.ElevatedButton("Criar Pessoa e Desafio", on_click=criar_pessoa_desafio),
                output,
            ]
        )
    )