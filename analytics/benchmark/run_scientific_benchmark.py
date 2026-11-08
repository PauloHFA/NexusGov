"""
NexusGov - Validação Científica, Benchmark de Precisão/Revocação e Sensibilidade de Pesos
SRS Seção 4.7, Critérios de Aceite CA-CIE-01 e CA-CIE-02.

Executa:
1. Benchmark de Precisão (>= 80%) e Revocação (>= 85%) em cenários sintéticos controlados.
2. Análise de Sensibilidade de Pesos do IEA: comprova que variação de ±20% nos pesos
   provoca alteração em menos de 10% das classificações de risco ("Baixo", "Médio", "Elevado").
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

from analytics.synthetic.generator import SyntheticScenarioGenerator
from analytics.benford.benford_test import BenfordAnalysisEngine
from analytics.split.fracionamento import SplitPurchaseDetector, ContractPurchaseEntry
from analytics.iea.engine import IeaEngine, AxisSignal

@dataclass
class BenchmarkMetricResult:
    detector: str
    total_samples: int
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    precision: float
    recall: float
    f1_score: float
    passed: bool

@dataclass
class SensitivityAnalysisResult:
    total_evaluations: int
    total_flips: int
    flip_rate: float
    passed: bool

class ScientificBenchmarkRunner:

    def __init__(self, seed: int = 42):
        self.generator = SyntheticScenarioGenerator(seed=seed)
        self.rng = np.random.default_rng(seed)

    def benchmark_benford_detector(self, num_series: int = 200) -> BenchmarkMetricResult:
        """Avalia detector de Benford em séries conformes vs. propositalmente anômalas."""
        tp = fp = tn = fn = 0
        analyzer = BenfordAnalysisEngine()

        for _ in range(num_series // 2):
            # Série conforme (Log-uniforme, negativa para anomalia)
            vals_conforme = self.generator.generate_benford_series(n=400)
            res_conforme = analyzer.test_benford_compliance(vals_conforme)
            if res_conforme.conformidade_mad == "NÃO CONFORME":
                fp += 1
            else:
                tn += 1

            # Série anômala (80% de dígitos 7, positiva para anomalia)
            vals_anomala = self.generator.generate_anomalous_series(n=400, fixed_digit=7)
            res_anomala = analyzer.test_benford_compliance(vals_anomala)
            if res_anomala.conformidade_mad == "NÃO CONFORME":
                tp += 1
            else:
                fn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        return BenchmarkMetricResult(
            detector="Benford (MAD / Chi-Square)",
            total_samples=num_series,
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            passed=(precision >= 0.80 and recall >= 0.85)
        )

    def benchmark_fracionamento_detector(self, num_cases: int = 200) -> BenchmarkMetricResult:
        """Avalia detector de fracionamento em compras regulares vs. fracionadas."""
        tp = fp = tn = fn = 0
        detector = SplitPurchaseDetector()
        teto = 59906.02

        for i in range(num_cases // 2):
            # Caso 1: Regular (Apenas 1 compra dentro do limite, sem reincidência na janela)
            entries_regular = [
                ContractPurchaseEntry(
                    id=f"reg_{i}",
                    numero_controle_pncp=f"08123456000199-1-{i:06d}/2024",
                    orgao_id="ORGAO_PB_01",
                    fornecedor_cnpj=f"081234560001{i%90+10:02d}",
                    data_contratacao=self.generator.generate_synthetic_split_purchases()[0].data_contratacao,
                    valor=round(float(self.rng.uniform(5000, 45000)), 2),
                    codigo_catmat=f"CAT_{i}",
                    objeto_descricao="Serviço regular",
                    modalidade_objeto="DISPENSA_COMPRAS_SERVICOS"
                )
            ]
            res_reg = detector.detect_split_purchases(entries_regular)
            if len(res_reg) > 0:
                fp += 1
            else:
                tn += 1

            # Caso 2: Propositalmente Fracionado (4 compras totalizando > R$ 200k na janela)
            entries_split = self.generator.generate_synthetic_split_purchases(
                orgao_id=f"ORGAO_PB_{i}",
                fornecedor_cnpj=f"081234560001{i%90+10:02d}",
                teto=teto,
                num_fracionadas=4,
                dias_intervalo=45
            )
            res_split = detector.detect_split_purchases(entries_split)
            if len(res_split) > 0:
                tp += 1
            else:
                fn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        return BenchmarkMetricResult(
            detector="Fracionamento (Janelas Deslizantes)",
            total_samples=num_cases,
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            passed=(precision >= 0.80 and recall >= 0.85)
        )

    def analyze_weight_sensitivity(self, num_samples: int = 1000, perturbation: float = 0.20) -> SensitivityAnalysisResult:
        """
        CA-CIE-01: Prova que variação de ±20% nos pesos do IEA altera menos de 10%
        das classificações de risco ('Baixo', 'Médio', 'Elevado').
        """
        base_weights = {
            "GRAFO": 1.0,
            "BENFORD": 0.8,
            "FRACIONAMENTO": 1.0,
            "POPUP_VENDOR": 0.7
        }
        engine_base = IeaEngine(versao_parametros="v1.0.0-base", pesos_customizados=base_weights)

        # Gera perturbações de ±20% nos pesos
        perturbed_weights = {}
        for axis, w in base_weights.items():
            factor = 1.0 + float(self.rng.uniform(-perturbation, perturbation))
            perturbed_weights[axis] = w * factor

        engine_perturbed = IeaEngine(versao_parametros="v1.0.0-pert", pesos_customizados=perturbed_weights)

        flips = 0

        for idx in range(num_samples):
            # Gera sinais cobrindo o espectro
            signals_base = []
            signals_pert = []
            axes = ["GRAFO", "BENFORD", "FRACIONAMENTO", "POPUP_VENDOR"]
            num_active = int(self.rng.integers(1, 4))
            chosen_axes = self.rng.choice(axes, size=num_active, replace=False)

            for ax in chosen_axes:
                intensidade = float(self.rng.uniform(0.1, 1.0))
                confianca = float(self.rng.uniform(0.7, 1.0))

                signals_base.append(AxisSignal(
                    eixo=ax,
                    nome_sinal=f"{ax}_DETECTED",
                    intensidade=intensidade,
                    peso=base_weights[ax],
                    confianca=confianca
                ))

                signals_pert.append(AxisSignal(
                    eixo=ax,
                    nome_sinal=f"{ax}_DETECTED",
                    intensidade=intensidade,
                    peso=perturbed_weights[ax],
                    confianca=confianca
                ))

            res_base = engine_base.calculate_iea(f"c_{idx}", signals_base)
            res_pert = engine_perturbed.calculate_iea(f"c_{idx}", signals_pert)

            if res_base.nivel_risco != res_pert.nivel_risco:
                flips += 1

        flip_rate = flips / num_samples

        return SensitivityAnalysisResult(
            total_evaluations=num_samples,
            total_flips=flips,
            flip_rate=round(flip_rate, 4),
            passed=(flip_rate < 0.10) # Menos de 10% de alteração
        )

def run_all_benchmarks():
    runner = ScientificBenchmarkRunner(seed=42)
    print("=== NexusGov - Validação Científica & Benchmarks Forenses ===")
    
    benford_res = runner.benchmark_benford_detector(num_series=200)
    print(f"\n[1] {benford_res.detector}:")
    print(f"    Precisão: {benford_res.precision * 100:.1f}% (Meta >= 80%)")
    print(f"    Revocação: {benford_res.recall * 100:.1f}% (Meta >= 85%)")
    print(f"    F1-Score: {benford_res.f1_score:.4f}")
    print(f"    Status: {'✅ APROVADO' if benford_res.passed else '❌ REPROVADO'}")

    frac_res = runner.benchmark_fracionamento_detector(num_cases=200)
    print(f"\n[2] {frac_res.detector}:")
    print(f"    Precisão: {frac_res.precision * 100:.1f}% (Meta >= 80%)")
    print(f"    Revocação: {frac_res.recall * 100:.1f}% (Meta >= 85%)")
    print(f"    F1-Score: {frac_res.f1_score:.4f}")
    print(f"    Status: {'✅ APROVADO' if frac_res.passed else '❌ REPROVADO'}")

    sens_res = runner.analyze_weight_sensitivity(num_samples=1000, perturbation=0.20)
    print(f"\n[3] Análise de Sensibilidade de Pesos (CA-CIE-01):")
    print(f"    Perturbação nos pesos: ±20.0%")
    print(f"    Taxa de Reclassificação de Risco: {sens_res.flip_rate * 100:.2f}% (Meta < 10.0%)")
    print(f"    Status: {'✅ APROVADO' if sens_res.passed else '❌ REPROVADO'}")

    return benford_res.passed and frac_res.passed and sens_res.passed

if __name__ == "__main__":
    import sys
    success = run_all_benchmarks()
    sys.exit(0 if success else 1)
