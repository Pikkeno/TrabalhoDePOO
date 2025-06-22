import flet as ft
import os
import sys

if __package__ is None:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    

from src.controllers.desafio_controller import DesafioController
from src.controllers.pessoa_controller import PessoaController
from src.controllers.equipe_controller import EquipeController
from src.utils.logger import logger
from src.views.pessoa_view import criar_campos_pessoa
from src.views.desafio_view import criar_campos_desafio
from src.views.login_view import cria_campo_login


def flet_main(page: ft.Page):
    """Configura a tela principal da aplicação."""
    page.title = "Sistema de Desafios"
    logger.info("Iniciando o GymBet com Flet...")

    desafio_controller = DesafioController()
    pessoa_controller = PessoaController()
    equipe_controller = EquipeController()

    usuario_login, senha_login = cria_campo_login()
    login_output = ft.Text()

    def mostrar_cadastro_pessoa(e=None):
        """Exibe a tela de criação de conta."""
        page.clean()
        nome, email, senha = criar_campos_pessoa()
        output = ft.Text()

        def criar_conta(e):
            pessoa = pessoa_controller.registrar_pessoa(
                nome.value,
                None,
                email=email.value,
                senha=senha.value,
            )
            if pessoa is None:
                output.value = "Email ou ID já cadastrado."
                logger.warning(
                    "Tentativa de cadastro com email ou ID duplicado: %s", email.value
                )
            else:
                output.value = f"Conta criada para {pessoa.nome}. "
                logger.info("Conta criada para %s", pessoa.nome)
            page.update()

        page.add(
            ft.Column(
                [
                    nome,
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
            try:
                desafio = desafio_controller.criar_desafio(
                    1,
                    descricao.value,
                    data_inicio.value,
                    data_fim.value,
                    int(valor_aposta.value),
                    int(limite_participantes.value)
                )
            except ValueError as exc:
                output.value = f"Erro ao criar desafio: {exc}"
            else:
                mensagem = desafio_controller.adicionar_participante(desafio, pessoa)
                output.value = (
                    f"Desafio criado: {desafio.descricao}\n"
                    f"{mensagem}"
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
                    ft.TextButton("Voltar", on_click=lambda e: mostrar_pos_login(pessoa)),
                ]
            )
        )

    def listar_desafios_por_status(status: str):
        """Gera uma lista de ListTile para os desafios com o status informado."""
        desafios = [d for d in desafio_controller.desafios if d.status == status]
        if not desafios:
            return [ft.ListTile(title=ft.Text("Nenhum desafio."))]
        return [
            ft.ListTile(
                title=ft.Text(f"Desafio {d.id}"),
                subtitle=ft.Text(d.descricao),
            )
            for d in desafios
        ]

    def mostrar_dashboard(e=None):
        page.clean()

        abertos = ft.ListView(
            controls=listar_desafios_por_status("Ativo"),
            padding=10,
            spacing=10,
        )

        encerrados = ft.ListView(
            controls=listar_desafios_por_status("Encerrado"),
            padding=10,
            spacing=10,
        )

        historico = ft.ListView(
            controls=listar_desafios_por_status("Encerrado"),
            padding=10,
            spacing=10,
        )

        tabs = ft.Tabs(
            expand=1,
            tabs=[
                ft.Tab(text="Abertos", content=abertos),
                ft.Tab(text="Encerrados", content=encerrados),
                ft.Tab(text="Histórico", content=historico),
            ],
        )

        page.add(ft.Container(tabs, padding=20, bgcolor=ft.Colors.GREY_100))
    
    def mostrar_gerenciamento_equipes(pessoa):
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
                            ft.TextButton(
                                "Voltar",
                                on_click=lambda e: mostrar_pos_login(pessoa),
                            ),
                        ]
                    ),
                    output,
                ]
            )
        )
    
    def mostrar_pos_login(pessoa):
        """Tela inicial após o login com opções sociais."""
        page.clean()
        nome_equipe = ft.TextField(label="Nome da Equipe")
        id_amigo = ft.TextField(label="ID do Amigo")
        output = ft.Text()

        def criar_equipe(e):
            equipe_controller.criar_equipe(nome_equipe.value, pessoa)
            output.value = f"Equipe {nome_equipe.value} criada."
            page.update()

        def adicionar_amigo(e):
            output.value = pessoa_controller.adicionar_amigo(pessoa, id_amigo.value)
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text(f"Bem-vindo, {pessoa.nome}!"),
                    nome_equipe,
                    ft.ElevatedButton("Criar Equipe", on_click=criar_equipe),
                    id_amigo,
                    ft.ElevatedButton("Adicionar Amigo", on_click=adicionar_amigo),
                    ft.ElevatedButton(
                        "Gerenciar Equipes",
                        on_click=lambda e: mostrar_gerenciamento_equipes(pessoa),
                    ),
                    ft.ElevatedButton(
                        "Criar Desafio", on_click=lambda e: mostrar_cadastro_desafio(pessoa)
                    ),
                    ft.ElevatedButton(
                        "Ir para Dashboard", on_click=lambda e: mostrar_dashboard()
                    ),
                    output,
                ]
            )
        )
    
    def realizar_login(e):
        pessoa = pessoa_controller.autenticar(
            usuario_login.value,
            senha_login.value,
        )
        if pessoa:
            login_output.value = f"Login de {pessoa.nome}"
            logger.info("Login realizado por %s", pessoa.nome)
            mostrar_pos_login(pessoa)
        else:
            login_output.value = "Credenciais inválidas."
            logger.warning(
                "Falha no login para %s", usuario_login.value
            )

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