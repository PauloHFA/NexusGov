"""
NexusGov - Testes de Streaming em Tempo Real e Alertas Preventivos Intra-Dia (Melhoria 1)
"""

from datetime import datetime, timedelta
import pytest
from ingestion.streaming.event_stream import (
    RealTimeStreamBroker,
    TenderStreamMessage,
    TenderEventType
)
from ingestion.streaming.intra_day_alerter import IntraDayAlerter


def test_real_time_stream_broker_pub_sub():
    broker = RealTimeStreamBroker()
    received_events = []

    broker.subscribe(TenderEventType.TENDER_PUBLISHED, lambda msg: received_events.append(msg))

    msg = TenderStreamMessage(
        event_type=TenderEventType.TENDER_PUBLISHED,
        numero_controle_pncp="08778268000160-1-000010/2024",
        orgao_cnpj="08778268000160",
        orgao_nome="Prefeitura de João Pessoa",
        uf="PB",
        objeto="Reforma de Posto de Saúde",
        valor_estimado=250000.0,
        modalidade_nome="Pregão Eletrônico",
        payload_bruto_hash="a1b2c3d4e5"
    )

    broker.publish(msg)

    assert len(received_events) == 1
    assert received_events[0].numero_controle_pncp == "08778268000160-1-000010/2024"
    assert broker.total_events_published == 1


def test_intra_day_alerter_flag_short_deadline():
    alerter = IntraDayAlerter(dias_minimos_edital=8)
    now = datetime.utcnow()

    # Publicado hoje, com abertura em 3 dias (prazo exíguo)
    msg = TenderStreamMessage(
        event_type=TenderEventType.TENDER_PUBLISHED,
        timestamp=now,
        data_abertura_proposta=now + timedelta(days=3),
        numero_controle_pncp="2504009-1-000020/2024",
        orgao_cnpj="08778268000160",
        orgao_nome="Prefeitura de Campina Grande",
        uf="PB",
        objeto="Aquisição emergencial de medicamentos",
        valor_estimado=180000.0,
        modalidade_nome="Pregão Eletrônico",
        payload_bruto_hash="hash123"
    )

    alert = alerter.evaluate_published_tender(msg)
    assert alert is not None
    assert alert.nivel_prioridade == "Atenção"
    assert "Prazo de publicidade reduzido" in alert.motivo_sinalizacao
    assert alert.dias_para_abertura == 3
