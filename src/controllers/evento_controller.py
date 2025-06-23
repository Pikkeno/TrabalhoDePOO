from __future__ import annotations
from typing import List

from src.controllers.pessoa_controller import PessoaController
from src.models.evento_competitivo_models import EventoCompetitivo
from src.models.competidor_base import Competidor
from src.models.desafio_models import Desafio
from src.controllers.desafio_controller import DesafioController
from src.models.pessoa_models import Pessoa
from src.utils import evento_db

class EventoController:
    """Gerencia eventos competitivos entre competidores."""

    def __init__(
        self,
        desafio_controller: DesafioController | None = None,
        pessoa_controller: PessoaController | None = None,
    ):
        self.eventos: List[EventoCompetitivo] = []
        self.desafio_controller = desafio_controller or DesafioController()
        self.pessoa_controller = pessoa_controller
        self.carregar_eventos()


    def criar_evento(self, criador: Competidor, convidado: Competidor) -> EventoCompetitivo:
        evento = EventoCompetitivo(criador, convidado)
        self.eventos.append(evento)
        self.salvar_eventos()
        return evento

    def aceitar_evento(self, evento: EventoCompetitivo, usuario: Competidor):
        if evento.convidado != usuario:
            raise ValueError("Apenas o convidado pode aceitar o evento")
        evento.aceitar_convite()
        self.salvar_eventos()

    def recusar_evento(self, evento: EventoCompetitivo, usuario: Competidor):
        """Remove o evento caso o convidado recuse o convite."""
        if evento.convidado != usuario:
            raise ValueError("Apenas o convidado pode recusar o evento")
        if evento in self.eventos:
            self.eventos.remove(evento)
            self.salvar_eventos()

    def adicionar_desafio_ao_evento(
        self,
        evento: EventoCompetitivo,
        descricao: str,
        data_inicio: str,
        data_fim: str,
        valor_aposta: float,
        limite_participantes: int = 2,
    ) -> Desafio:
        if not evento.aceito:
            raise ValueError("Evento ainda nao aceito")
        desafio = self.desafio_controller.criar_desafio(
            len(self.desafio_controller.desafios) + 1,
            descricao,
            data_inicio,
            data_fim,
            valor_aposta,
            limite_participantes,
        )
        evento.adicionar_desafio(desafio)
        self.salvar_eventos()
        return desafio

    def registrar_aposta_evento(self, evento: EventoCompetitivo, competidor: Competidor, valor: float):
        evento.registrar_aposta(competidor, valor)
        self.salvar_eventos()

    def salvar_eventos(self):
        dados = []
        for evento in self.eventos:
            dados.append(
                {
                    "evento_id": evento.evento_id,
                    "criador": getattr(evento.criador, "idm", evento.criador.obter_nome()),
                    "convidado": getattr(evento.convidado, "idm", evento.convidado.obter_nome()),
                    "aceito": evento.aceito,
                    "desafios": [
                        {
                            "id": d.id,
                            "descricao": d.descricao,
                            "data_inicio": d.data_inicio,
                            "data_fim": d.data_fim,
                            "valor_aposta": d.valor_aposta,
                            "limite_participantes": d.limite_participantes,
                            "status": d.status,
                        }
                        for d in evento.desafios
                    ],
                    "apostas": {
                        getattr(c, "idm", c.obter_nome()): v
                        for c, v in evento.apostas.items()
                    },
                }
            )
        evento_db.salvar_dados(dados)

    def carregar_eventos(self):
        for dado in evento_db.carregar_dados():
            criador = self._resolver_competidor(dado.get("criador"))
            convidado = self._resolver_competidor(dado.get("convidado"))
            evento = EventoCompetitivo(
                criador,
                convidado,
                evento_id=dado.get("evento_id"),
            )
            if dado.get("aceito"):
                evento.aceitar_convite()
            for d in dado.get("desafios", []):
                desafio = Desafio(
                    d.get("id"),
                    d.get("descricao"),
                    d.get("data_inicio"),
                    d.get("data_fim"),
                    d.get("valor_aposta"),
                    d.get("limite_participantes", 2),
                )
                desafio.status = d.get("status", "Ativo")
                evento.desafios.append(desafio)
            for competidor_id, valor in dado.get("apostas", {}).items():
                competidor = self._resolver_competidor(competidor_id)
                evento.apostas[competidor] = valor
            self.eventos.append(evento)

    def _resolver_competidor(self, identificador):
        if self.pessoa_controller:
            pessoa = self.pessoa_controller.buscar_por_id(identificador) or self.pessoa_controller.buscar_por_nome(identificador)
            if pessoa:
                return pessoa
        return Pessoa(identificador, identificador)