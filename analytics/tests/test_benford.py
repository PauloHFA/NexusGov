"""
NexusGov - Testes da Lei de Benford (RF-ANA-04, CA-ANA-02)
"""

import pytest
from analytics.benford.benford_test import BenfordAnalysisEngine
from analytics.synthetic.generator import SyntheticScenarioGenerator

def test_benford_inapplicable_small_sample_ca_ana_02():
    """
    Critério de Aceite CA-ANA-02 (Parte 1):
    Dado um conjunto com 150 valores (n < 300),
    quando o teste é solicitado, então o resultado é categoricamente
    'não aplicável' e nenhum achado é gerado.
    """
    engine = BenfordAnalysisEngine()
    gen = SyntheticScenarioGenerator(seed=42)
    small_series = gen.generate_benford_series(n=150)

    result = engine.test_benford_compliance(small_series)

    assert result.aplicavel is False
    assert "n = 150 < 300" in result.motivo_inaplicabilidade
    assert result.conformidade_mad == "NÃO APLICÁVEL"
    assert result.escore_sinal == 0.0

def test_benford_conforming_large_sample_ca_ana_02():
    """
    Critério de Aceite CA-ANA-02 (Parte 2):
    Dado um conjunto com 5.000 valores gerados conforme Benford,
    então MAD <= 0.006 e nenhum achado de não conformidade é gerado.
    """
    engine = BenfordAnalysisEngine()
    gen = SyntheticScenarioGenerator(seed=42)
    benford_series = gen.generate_benford_series(n=5000, min_val=10.0, max_val=10000000.0)

    result = engine.test_benford_compliance(benford_series)

    assert result.aplicavel is True
    assert result.n_amostras == 5000
    assert result.ordens_grandeza >= 2.0
    assert result.mad_nigrini <= 0.006, f"MAD {result.mad_nigrini} deveria ser <= 0.006"
    assert result.conformidade_mad == "PRÓXIMO"
    assert result.escore_sinal == 0.0

def test_benford_anomalous_detection():
    """Testa rejeição e sinalização de anomalia quando a distribuição viola Benford."""
    engine = BenfordAnalysisEngine()
    gen = SyntheticScenarioGenerator(seed=42)
    anomalous_series = gen.generate_anomalous_series(n=1000, fixed_digit=7)

    result = engine.test_benford_compliance(anomalous_series)

    assert result.aplicavel is True
    assert result.mad_nigrini > 0.015, f"MAD {result.mad_nigrini} deveria ser > 0.015"
    assert result.conformidade_mad == "NÃO CONFORME"
    assert result.escore_sinal == 1.0
    assert result.qui_quadrado_pvalor < 0.01

def test_benford_fdr_correction():
    """Testa correção de Benjamini-Hochberg (FDR) em múltiplos testes."""
    p_vals = [0.001, 0.008, 0.039, 0.045, 0.50]
    adj_vals = BenfordAnalysisEngine.apply_fdr_correction(p_vals)
    assert len(adj_vals) == len(p_vals)
    # Valores ajustados devem ser monotonamente maiores ou iguais aos originais
    for orig, adj in zip(p_vals, adj_vals):
        assert adj >= orig
