"""
NexusGov - Alerta Preventivo Intra-Dia de Editais Recém-Publicados (Melhoria 1)
Analisa editais imediatamente após publicação no PNCP antes do término da fase de lances.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .event_stream import TenderStreamMessage, TenderEventType


class IntraDayEarlyAlert(BaseModel):
    """Alerta preventivo gerado em tempo real na publicação do edital."""
    alerta_id: str
    numero_controle_pncp: str
    orgao_nome: str
    nivel_prioridade: str # 'Informativo', 'Atenção', 'Prioritário'
    motivo_sinalizacao: str
    dias_para_abertura: Optional[int] = None
    acao_sugerida: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IntraDayAlerter:
    """
    Detector em tempo real de incongruências de prazo e publicidade na fase preparatória/divulgação.
    """

    def __init__(self, dias_minimos_edital: int = 8):
        self.dias_minimos_edital = dias_minimos_edital

    def evaluate_published_tender(self, msg: TenderStreamMessage) -> Optional[IntraDayEarlyAlert]:
        """
        Avalia o edital publicado e gera alerta preventivo caso identificado prazo exíguo ou risco temporal.
        """
        if msg.event_type != TenderEventType.TENDER_PUBLISHED:
            return None

        # 1. Verificação de prazo exíguo de abertura
        if msg.data_abertura_proposta:
            delta = (msg.data_abertura_proposta - msg.timestamp).days
            if delta < self.dias_minimos_edital:
                return IntraDayEarlyAlert(
                    alerta_id=f"ALT_PRAZO_{msg.numero_controle_pncp}",
                    numero_controle_pncp=msg.numero_controle_pncp,
                    orgao_nome=msg.orgao_nome,
                    nivel_prioridade="Atenção",
                    motivo_sinalizacao=f"Prazo de publicidade reduzido ({delta} dias até abertura de propostas)",
                    dias_para_abertura=delta,
                    acao_sugerida="Verificar justificativa legal de urgência ou adequação do prazo nos termos da Lei 14.133/2021"
                )

        # 2. Dispensas de alto valor próximas ao limite
        if "DISPENSA" in msg.modalidade_nome.upper() and msg.valor_estimado >= 50000.0:
            return IntraDayEarlyAlert(
                alerta_id=f"ALT_DISP_{msg.numero_controle_pncp}",
                numero_controle_pncp=msg.numero_controle_pncp,
                orgao_nome=msg.orgao_nome,
                nivel_prioridade="Atenção",
                motivo_sinalizacao="Dispensa direta com valor próximo ao teto legal anual",
                acao_sugerida="Monitorar janela deslizante de 30/60 dias para possíveis contratações correlatas"
            )

        return None
