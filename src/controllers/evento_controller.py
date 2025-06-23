from __future__ import annotations
from typing import List

from src.models.evento_competitivo_models import EventoCompetitivo
from src.models.competidor_base import Competidor
from src.models.desafio_models import Desafio
from src.controllers.desafio_controller import DesafioController

class EventoController:
    """Gerencia eventos competitivos entre competidores."""

    def __init__(self, desafio_controller: DesafioController | None = None):
        self.eventos: List[EventoCompetitivo] = []
        self.desafio_controller = desafio_controller or DesafioController()

    def criar_evento(self, criador: Competidor, convidado: Competidor) -> EventoCompetitivo:
        evento = EventoCompetitivo(criador, convidado)
        self.eventos.append(evento)
        return evento

    def aceitar_evento(self, evento: EventoCompetitivo):
        evento.aceitar_convite()

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
        return desafio

    def registrar_aposta_evento(self, evento: EventoCompetitivo, competidor: Competidor, valor: float):
        evento.registrar_aposta(competidor, valor)