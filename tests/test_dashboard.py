import unittest
import types
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

ft_stub = types.SimpleNamespace(
    ListTile=lambda *a, **k: ("ListTile", a, k),
    Text=lambda *a, **k: ("Text", a, k),
    Row=lambda *a, **k: ("Row", a, k),
    TextButton=lambda *a, **k: ("TextButton", a, k),
    ListView=lambda *a, **k: ("ListView", a, k),
    Column=lambda *a, **k: ("Column", a, k),
    Container=lambda *a, **k: ("Container", a, k),
    Tabs=lambda *a, **k: ("Tabs", a, k),
    Tab=lambda *a, **k: ("Tab", a, k),
    IconButton=lambda *a, **k: ("IconButton", a, k),
    Colors=types.SimpleNamespace(GREY_100="", GREY_400="", RED_400=""),
    Icons=types.SimpleNamespace(ARROW_BACK=""),
    MainAxisAlignment=types.SimpleNamespace(START=0, CENTER=0),
)
sys.modules.setdefault("flet", ft_stub)

from src.views.dashboard_view import listar_desafios_por_status
from src.controllers.desafio_controller import DesafioController
from src.controllers.evento_controller import EventoController
from src.controllers.pessoa_controller import PessoaController
from src.models.pessoa_models import Pessoa

class TestDashboardFilter(unittest.TestCase):
    def test_desafio_evento_visivel_para_criador(self):
        pessoa_ctrl = PessoaController()
        p1 = Pessoa("Alice", "1")
        p2 = Pessoa("Bob", "2")
        pessoa_ctrl.pessoas = [p1, p2]

        desafio_ctrl = DesafioController()
        evento_ctrl = EventoController(desafio_ctrl, pessoa_ctrl)
        evento_ctrl.eventos = []
        evento = evento_ctrl.criar_evento(p1, p2)
        evento.aceitar_convite()
        desafio = evento_ctrl.adicionar_desafio_ao_evento(
            evento,
            "corrida",
            "01-01-2030",
            "02-01-2030",
            10,
            2,
        )

        tiles = listar_desafios_por_status(
            desafio_ctrl, "Ativo", p1, evento_ctrl
        )
        self.assertEqual(len(tiles), 1)

if __name__ == "__main__":
    unittest.main()