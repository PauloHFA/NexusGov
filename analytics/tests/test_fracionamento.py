"""
NexusGov - Testes de Fracionamento de Despesa e Tetos Legais (RF-ANA-05, RF-CFG-02, CA-ANA-03, CA-ANA-04)
"""

from datetime import date
import pytest
from analytics.split.fracionamento import (
    SplitPurchaseDetector,
    LegalThresholdRule,
    ContractPurchaseEntry
)
from analytics.synthetic.generator import SyntheticScenarioGenerator

def test_split_purchases_sliding_window_ca_ana_03():
    """
    Critério de Aceite CA-ANA-03:
    Dado um fornecedor com 4 dispensas de mesmo CATMAT em 45 dias, cada uma a 95% do teto vigente,
    quando a análise 30-90 dias é executada, então um achado de fracionamento é gerado
    com as 4 contratações listadas e o teto vigente na data de cada uma.
    """
    detector = SplitPurchaseDetector()
    gen = SyntheticScenarioGenerator(seed=42)

    # Gera 4 dispensas em 45 dias a ~95% do teto de compras de 2024 (R$ 59.906,02)
    teto_2024 = 59906.02
    purchases = gen.generate_synthetic_split_purchases(
        orgao_id="PREF_JOAO_PESSOA_PB",
        fornecedor_cnpj="08123456000199",
        teto=teto_2024,
        num_fracionadas=4,
        dias_intervalo=45
    )

    findings = detector.detect_split_purchases(purchases)

    assert len(findings) >= 1
    f = findings[0]
    assert f.fornecedor_cnpj == "08123456000199"
    assert f.total_contratacoes >= 3
    assert f.soma_valores > teto_2024 # A soma excede o teto
    assert f.teto_legal_vigente == teto_2024
    assert f.escore_sinal >= 0.60
    assert len(f.contratacoes_ids) >= 3

def test_legal_thresholds_temporal_validity_ca_ana_04():
    """
    Critério de Aceite CA-ANA-04:
    Dado que o teto muda de valor em uma data X,
    quando contratações anteriores e posteriores a X são avaliadas,
    então cada uma é comparada ao teto vigente em sua data, sem alteração de código.
    """
    detector = SplitPurchaseDetector()

    # Data de 2021 (Lei 14.133 original: R$ 50.000,00)
    teto_2021 = detector.get_threshold_for(date(2021, 6, 1), "DISPENSA_COMPRAS_SERVICOS")
    assert teto_2021 == 50000.00

    # Data de 2022 (Decreto 10.922/2021: R$ 54.020,41)
    teto_2022 = detector.get_threshold_for(date(2022, 6, 1), "DISPENSA_COMPRAS_SERVICOS")
    assert teto_2022 == 54020.41

    # Data de 2023 (Decreto 11.317/2022: R$ 57.209,60)
    teto_2023 = detector.get_threshold_for(date(2023, 6, 1), "DISPENSA_COMPRAS_SERVICOS")
    assert teto_2023 == 57209.60

    # Data de 2024 em diante (Decreto 11.871/2023: R$ 59.906,02)
    teto_2024 = detector.get_threshold_for(date(2024, 6, 1), "DISPENSA_COMPRAS_SERVICOS")
    assert teto_2024 == 59906.02

    # Verifica também obras e serviços de engenharia (2024: R$ 119.812,02)
    teto_obras_2024 = detector.get_threshold_for(date(2024, 6, 1), "DISPENSA_OBRAS_ENGENHARIA")
    assert teto_obras_2024 == 119812.02
