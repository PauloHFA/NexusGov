"""
Testes automatizados para validação científica e critérios de aceite CA-CIE-01 e CA-CIE-02.
"""

from analytics.benchmark.run_scientific_benchmark import ScientificBenchmarkRunner

def test_ca_cie_02_benford_precision_recall_benchmark():
    runner = ScientificBenchmarkRunner(seed=42)
    res = runner.benchmark_benford_detector(num_series=100)
    assert res.precision >= 0.80, f"Precisão abaixo da meta: {res.precision}"
    assert res.recall >= 0.85, f"Revocação abaixo da meta: {res.recall}"
    assert res.passed is True

def test_ca_cie_02_fracionamento_precision_recall_benchmark():
    runner = ScientificBenchmarkRunner(seed=42)
    res = runner.benchmark_fracionamento_detector(num_cases=100)
    assert res.precision >= 0.80, f"Precisão abaixo da meta: {res.precision}"
    assert res.recall >= 0.85, f"Revocação abaixo da meta: {res.recall}"
    assert res.passed is True

def test_ca_cie_01_iea_weight_sensitivity_stability():
    runner = ScientificBenchmarkRunner(seed=42)
    # Variação de ±20% nos pesos
    res = runner.analyze_weight_sensitivity(num_samples=500, perturbation=0.20)
    assert res.flip_rate < 0.10, f"Taxa de reclassificação superior a 10%: {res.flip_rate}"
    assert res.passed is True
