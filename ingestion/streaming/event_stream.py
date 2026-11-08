"""
NexusGov - Mecanismo de Ingestão em Tempo Real e Streaming de Editais (Melhoria 1)
Implementa mensageria para processamento imediato de avisos de licitação e compras diretas (Kafka / Webhook / AMQP).
"""

from datetime import datetime, date
from enum import Enum
from typing import Callable, Dict, List, Optional, Any
from pydantic import BaseModel, Field
import uuid


class TenderEventType(str, Enum):
    TENDER_PUBLISHED = "TENDER_PUBLISHED"                 # Publicação de novo edital
    PROPOSAL_OPENED = "PROPOSAL_OPENED"                   # Abertura de propostas
    AWARDED = "AWARDED"                                   # Homologação/Adjudicação
    DISPENSATION_AUTHORIZED = "DISPENSATION_AUTHORIZED"   # Autorização de dispensa direta


class TenderStreamMessage(BaseModel):
    """Mensagem de evento em tempo real transmitida via tópico de streaming."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: TenderEventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    numero_controle_pncp: str
    orgao_cnpj: str
    orgao_nome: str
    uf: str
    codigo_ibge_municipio: Optional[str] = None
    objeto: str
    valor_estimado: float
    data_abertura_proposta: Optional[datetime] = None
    modalidade_nome: str
    payload_bruto_hash: str
    dados_extras: Dict[str, Any] = Field(default_factory=dict)


class RealTimeStreamBroker:
    """
    Barramento de eventos em tempo real para orquestração de análises preditivas intra-dia.
    Suporta tópicos pub/sub desacoplados.
    """

    def __init__(self):
        self._subscribers: Dict[TenderEventType, List[Callable[[TenderStreamMessage], None]]] = {
            t: [] for t in TenderEventType
        }
        self._published_history: List[TenderStreamMessage] = []

    def subscribe(self, event_type: TenderEventType, handler: Callable[[TenderStreamMessage], None]) -> None:
        """Registra um consumidor para um determinado tipo de evento."""
        self._subscribers[event_type].append(handler)

    def publish(self, message: TenderStreamMessage) -> None:
        """Publica um evento para todos os consumidores registrados do tópico."""
        self._published_history.append(message)
        handlers = self._subscribers.get(message.event_type, [])
        for handler in handlers:
            handler(message)

    @property
    def total_events_published(self) -> int:
        return len(self._published_history)
