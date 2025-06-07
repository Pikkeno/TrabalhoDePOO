import flet as ft
import os
import sys

if __package__ is None:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController
from src.views.pessoa_view import criar_campos_pessoa
from src.views.desafio_view import criar_campos_desafio
from src.views.login_view import cria_campo_login

def flet_main(page: ft.Page):
    """Configura a tela principal da aplicação."""
    page.title = "Sistema de Desafios"

    desafio_controller = DesafioController()
    pessoa_controller = PessoaController()

    usuario_login, senha_login = cria_campo_login()
    login_output = ft.Text()

    def mostrar_cadastro_pessoa(e=None):
        """Exibe a tela de criação de conta."""
        page.clean()
        nome, idm, email, senha = criar_campos_pessoa()
        descricao, data_inicio, data_fim, valor_aposta, limite_participantes = criar_campos_desafio()
        output = ft.Text()

        def criar_conta(e):
            pessoa = pessoa_controller.criar_pessoa(
                nome.value,
                idm.value,
                email=email.value,
                senha=senha.value,
            )
            output.value = f"Conta criada para {pessoa.nome}"
            mostrar_cadastro_desafio(pessoa)

        page.add(
            ft.Column(
                [
                    nome,
                    idm,
                    email,
                    senha,
                    ft.ElevatedButton("Criar Conta", on_click=criar_conta),
                    output,
                    ft.TextButton("Voltar", on_click=lambda e: mostrar_login()),
                ]
            )
        )

    def mostrar_cadastro_desafio(pessoa):
        """Exibe a tela de criação de desafio."""
        page.clean()
        descricao, data_inicio, data_fim, valor_aposta, limite_participantes = criar_campos_desafio()
        output = ft.Text()

        def criar_desafio(e):
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
                f"Desafio criado: {desafio.descricao}\n"
                f"{mensagem}"
            )
            page.update()

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
                    ft.TextButton("Voltar", on_click=lambda e: mostrar_cadastro_pessoa()),
                ]
            )
        )

    def realizar_login(e):
        # Funcionalidade de login simplificada
        login_output.value = f"Login de {usuario_login.value}"

        page.update()
    def mostrar_login():
        page.clean()
        page.add(
            ft.Column(
                [
                    usuario_login,
                    senha_login,
                    ft.Row(
                        [
                            ft.ElevatedButton("Entrar", on_click=realizar_login),
                            ft.TextButton("Criar conta", on_click=mostrar_cadastro_pessoa),
                        ]
                    ),
                    login_output,
                ]
            )
        )

    mostrar_login()

if __name__ == "__main__":
    ft.app(target=flet_main)