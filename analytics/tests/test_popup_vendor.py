"""
NexusGov - Testes de Detecção de Pop-up Vendors (RF-ANA-06)
"""

from datetime import date
import pytest
from analytics.popup.popup_vendor import PopupVendorDetector
from ingestion.ibge.municipios import IbgeService

def test_popup_vendor_high_exposure_detection():
    detector = PopupVendorDetector()

    # Empresa aberta há apenas 15 dias com R$ 1.000 de capital vencendo R$ 500.000
    # Fornecedor com sede distante (Manaus) disputando serviço em João Pessoa-PB (2507507)
    finding = detector.evaluate_vendor(
        cnpj="11111111000199",
        razao_social="Recém Nascida Serviços LTDA",
        data_abertura_cnpj=date(2026, 8, 15),
        data_certame=date(2026, 8, 30),
        capital_social=1000.00,
        valor_adjudicado=500000.00,
        municipio_fornecedor_ibge=None,
        municipio_orgao_ibge="2507507"
    )

    assert finding.idade_dias_na_licitacao == 15
    assert finding.razao_valor_capital >= 500.0
    # Escore deve ser elevado (>= 0.70)
    assert finding.escore_sinal >= 0.70
    assert finding.detalhes_sinais["sinal_idade"] == 1.0
    assert finding.detalhes_sinais["sinal_capital"] == 1.0

def test_mature_vendor_low_exposure():
    detector = PopupVendorDetector()

    # Empresa aberta há 5 anos com R$ 2.000.000 de capital vencendo R$ 100.000
    finding = detector.evaluate_vendor(
        cnpj="33000167000101",
        razao_social="Empresa Madura e Estabelecida S/A",
        data_abertura_cnpj=date(2019, 1, 10),
        data_certame=date(2024, 5, 20),
        capital_social=2000000.00,
        valor_adjudicado=100000.00
    )

    assert finding.idade_dias_na_licitacao > 1500
    assert finding.razao_valor_capital < 1.0
    assert finding.escore_sinal == 0.0
