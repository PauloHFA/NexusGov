"""
NexusGov - Testes de Cruzamento de Preços de Referência (RF-ANA-10 / CA-ANA-10)
"""

import pytest
from analytics.price.reference_price import ReferencePriceAnalyzer


def test_reference_price_exceeding_median_by_50_pct():
    """
    Valida CA-ANA-10:
    Dado um catálogo com referencial homologado,
    Quando o valor unitário for superior em mais de 50% à mediana regional,
    Então gera sinal de sobrepreço relativo.
    """
    analyzer = ReferencePriceAnalyzer(limiar_alerta_pct=50.0)

    # Preços históricos de referência com mediana 100.0
    historico = [95.0, 100.0, 102.0, 98.0, 105.0]

    # Item adjudicado a 160.0 (+60% acima da mediana de 100.0)
    finding = analyzer.analyze_item_price(
        item_id="item_01",
        codigo_catmat="12345",
        descricao="Cimento CP-II 50kg",
        valor_unitario=160.0,
        historico_precos_referencia=historico
    )

    assert finding.preco_mediano_referencia == 100.0
    assert finding.desvio_percentual_mediana == 60.0
    assert finding.sinal_sobrepreco_relativo is True
    assert finding.escore_sinal > 0.5


def test_reference_price_within_normal_range():
    """Valida que preços dentro da faixa tolerada não geram sinal de alerta."""
    analyzer = ReferencePriceAnalyzer(limiar_alerta_pct=50.0)
    historico = [100.0, 100.0, 100.0]

    # Preço adjudicado a 110.0 (+10% acima da mediana)
    finding = analyzer.analyze_item_price(
        item_id="item_02",
        codigo_catmat="12345",
        descricao="Cimento CP-II 50kg",
        valor_unitario=110.0,
        historico_precos_referencia=historico
    )

    assert finding.desvio_percentual_mediana == 10.0
    assert finding.sinal_sobrepreco_relativo is False
