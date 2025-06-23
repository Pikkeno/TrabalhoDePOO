from __future__ import annotations
from typing import Dict, List, Optional
from .competidor_base import Competidor
from .desafio_models import Desafio

class EventoCompetitivo:
    """Representa um evento competitivo compartilhado entre dois competidores."""

    def __init__(self, criador: Competidor, convidado: Competidor, evento_id: Optional[str] = None):
        self.evento_id = evento_id or "EVT"  # identificador simples
        self.criador = criador
        self.convidado = convidado
        self.aceito = False
        self.desafios: List[Desafio] = []
        self.apostas: Dict[Competidor, float] = {}

    def aceitar_convite(self):
        """Marca o evento como aceito pelo convidado."""
        self.aceito = True

    def adicionar_desafio(self, desafio: Desafio):
        """Adiciona um desafio ao evento se ele foi aceito."""
        if not self.aceito:
            raise ValueError("O evento precisa ser aceito antes de adicionar desafios.")
        self.desafios.append(desafio)

    def registrar_aposta(self, competidor: Competidor, valor: float):
        """Registra/atualiza o valor apostado por um competidor."""
        if valor < 0:
            raise ValueError("Valor da aposta nao pode ser negativo")
        self.apostas[competidor] = valor