"""
NexusGov - Teste Estatístico de Conformidade à Lei de Benford (RF-ANA-04)
Metodologia: Seção 4.2 do SRS (MAD de Nigrini, KS sobre a mantissa e Benjamini-Hochberg)
Critério de Aceite: CA-ANA-02
"""

import math
from typing import Dict, List, Optional, Sequence, Set, Tuple
import numpy as np

class BenfordResult:
    """Resultado detalhado do teste de Benford."""
    def __init__(
        self,
        aplicavel: bool,
        motivo_inaplicabilidade: Optional[str] = None,
        n_amostras: int = 0,
        ordens_grandeza: float = 0.0,
        mad_nigrini: float = 0.0,
        conformidade_mad: str = "NÃO APLICÁVEL",
        qui_quadrado_stat: float = 0.0,
        qui_quadrado_pvalor: float = 1.0,
        ks_mantissa_stat: float = 0.0,
        ks_mantissa_pvalor: float = 1.0,
        pvalor_ajustado_fdr: Optional[float] = None,
        escore_sinal: float = 0.0, # s_i ∈ [0, 1]
        frequencias_observadas: Optional[Dict[int, float]] = None,
        frequencias_esperadas: Optional[Dict[int, float]] = None
    ):
        self.aplicavel = aplicavel
        self.motivo_inaplicabilidade = motivo_inaplicabilidade
        self.n_amostras = n_amostras
        self.ordens_grandeza = ordens_grandeza
        self.mad_nigrini = mad_nigrini
        self.conformidade_mad = conformidade_mad
        self.qui_quadrado_stat = qui_quadrado_stat
        self.qui_quadrado_pvalor = qui_quadrado_pvalor
        self.ks_mantissa_stat = ks_mantissa_stat
        self.ks_mantissa_pvalor = ks_mantissa_pvalor
        self.pvalor_ajustado_fdr = pvalor_ajustado_fdr
        self.escore_sinal = escore_sinal
        self.frequencias_observadas = frequencias_observadas or {}
        self.frequencias_esperadas = frequencias_esperadas or {}


class BenfordAnalysisEngine:
    """
    Motor analítico da Lei de Benford com salvaguardas de aplicabilidade estritas:
    Exige n >= 300 e amplitude >= 2 ordens de grandeza.
    """

    # Distribuição teórica do primeiro dígito significativo: P(d) = log10(1 + 1/d)
    BENFORD_PROBABILITIES: Dict[int, float] = {
        d: math.log10(1.0 + 1.0 / d) for d in range(1, 10)
    }

    # Limiares de conformidade MAD de Nigrini (SRS seção 4.2)
    MAD_CLOSE = 0.006      # <= 0.006: Próximo (Conforme)
    MAD_ACCEPTABLE = 0.012 # 0.006 a 0.012: Aceitável
    MAD_MARGINAL = 0.015   # 0.012 a 0.015: Marginal
    # > 0.015: Não conforme

    def __init__(self, catmat_exclusion_set: Optional[Set[str]] = None):
        self.catmat_exclusion = catmat_exclusion_set or set()

    @staticmethod
    def chi2_pvalue_8df(chi2: float) -> float:
        """
        Calcula o p-valor exato da distribuição Qui-Quadrado para 8 graus de liberdade (k=8).
        Fórmula analítica exata da função gama incompleta regularizada para k=8:
        P(X >= x) = exp(-x/2) * (1 + x/2 + x^2/8 + x^3/48)
        """
        if chi2 <= 0.0:
            return 1.0
        h = chi2 / 2.0
        poly = 1.0 + h + (h ** 2) / 2.0 + (h ** 3) / 6.0
        return float(math.exp(-h) * poly)

    @staticmethod
    def kolmogorov_smirnov_uniform(mantissas: np.ndarray) -> Tuple[float, float]:
        """
        Calcula a estatística D de Kolmogorov-Smirnov e p-valor contra Uniforme(0, 1).
        """
        n = len(mantissas)
        if n == 0:
            return 0.0, 1.0

        y = np.sort(mantissas)
        i = np.arange(1, n + 1)
        d_plus = np.max(i / n - y)
        d_minus = np.max(y - (i - 1) / n)
        d = float(max(d_plus, d_minus))

        # Fórmula assintótica de Marsaglia / Stephens para p-valor de KS
        z = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * d
        p = 0.0
        for j in range(1, 101):
            term = 2.0 * ((-1) ** (j - 1)) * math.exp(-2.0 * (j ** 2) * (z ** 2))
            p += term
            if abs(term) < 1e-12:
                break
        p = max(0.0, min(1.0, p))
        return d, p

    def test_benford_compliance(
        self,
        valores: Sequence[float],
        catmat_codes: Optional[Sequence[Optional[str]]] = None
    ) -> BenfordResult:
        """
        Executa o teste de Benford completo sobre a lista de valores (preços/itens/contratações).
        Garante CA-ANA-02: se n < 300, marca categoricamente como 'não aplicável'.
        """
        valid_values: List[float] = []
        for i, val in enumerate(valores):
            if val is None or val <= 0.0 or math.isnan(val) or math.isinf(val):
                continue
            if catmat_codes and i < len(catmat_codes) and catmat_codes[i] in self.catmat_exclusion:
                continue
            valid_values.append(float(val))

        n = len(valid_values)

        # Regra de aplicabilidade 1: n >= 300
        if n < 300:
            return BenfordResult(
                aplicavel=False,
                motivo_inaplicabilidade=f"Amostra insuficiente (n = {n} < 300)",
                n_amostras=n,
                conformidade_mad="NÃO APLICÁVEL",
                escore_sinal=0.0
            )

        arr = np.array(valid_values, dtype=np.float64)
        val_min = np.min(arr)
        val_max = np.max(arr)

        if val_min <= 0.0 or val_max <= val_min:
            return BenfordResult(
                aplicavel=False,
                motivo_inaplicabilidade="Amplitude nula ou valores não estritamente positivos",
                n_amostras=n,
                conformidade_mad="NÃO APLICÁVEL",
                escore_sinal=0.0
            )

        ordens_grandeza = math.log10(val_max / val_min)

        # Regra de aplicabilidade 2: amplitude >= 2 ordens de grandeza
        if ordens_grandeza < 2.0:
            return BenfordResult(
                aplicavel=False,
                motivo_inaplicabilidade=f"Amplitude insuficiente ({ordens_grandeza:.2f} < 2.0 ordens de grandeza)",
                n_amostras=n,
                ordens_grandeza=round(ordens_grandeza, 2),
                conformidade_mad="NÃO APLICÁVEL",
                escore_sinal=0.0
            )

        # 1. Extração do primeiro dígito significativo d ∈ {1..9}
        first_digits = []
        for v in arr:
            s = f"{v:.10e}"
            first_digits.append(int(s[0]))

        counts = {d: 0 for d in range(1, 10)}
        for d in first_digits:
            if 1 <= d <= 9:
                counts[d] += 1

        obs_freq = {d: counts[d] / n for d in range(1, 10)}
        exp_freq = self.BENFORD_PROBABILITIES
        exp_counts = {d: n * exp_freq[d] for d in range(1, 10)}

        # 2. Cálculo do MAD de Nigrini: sum(|Obs - Exp|) / 9
        mad = sum(abs(obs_freq[d] - exp_freq[d]) for d in range(1, 10)) / 9.0

        if mad <= self.MAD_CLOSE:
            conformidade = "PRÓXIMO"
            escore_sinal = 0.0
        elif mad <= self.MAD_ACCEPTABLE:
            conformidade = "ACEITÁVEL"
            escore_sinal = 0.20
        elif mad <= self.MAD_MARGINAL:
            conformidade = "MARGINAL"
            escore_sinal = 0.50
        else:
            conformidade = "NÃO CONFORME"
            escore_sinal = 1.0

        # 3. Teste Qui-Quadrado (8 graus de liberdade)
        chi2_stat = sum(((counts[d] - exp_counts[d]) ** 2) / exp_counts[d] for d in range(1, 10))
        chi2_pval = self.chi2_pvalue_8df(chi2_stat)

        # 4. Kolmogorov-Smirnov sobre a mantissa contínua: mantissa = log10(x) mod 1
        mantissas = np.mod(np.log10(arr), 1.0)
        ks_stat, ks_pval = self.kolmogorov_smirnov_uniform(mantissas)

        return BenfordResult(
            aplicavel=True,
            n_amostras=n,
            ordens_grandeza=round(ordens_grandeza, 2),
            mad_nigrini=round(mad, 5),
            conformidade_mad=conformidade,
            qui_quadrado_stat=round(chi2_stat, 4),
            qui_quadrado_pvalor=round(chi2_pval, 6),
            ks_mantissa_stat=round(ks_stat, 5),
            ks_mantissa_pvalor=round(ks_pval, 6),
            escore_sinal=escore_sinal,
            frequencias_observadas={d: round(obs_freq[d], 4) for d in range(1, 10)},
            frequencias_esperadas={d: round(exp_freq[d], 4) for d in range(1, 10)}
        )

    @staticmethod
    def apply_fdr_correction(p_values: List[float], alpha: float = 0.05) -> List[float]:
        """Aplica correção de Benjamini-Hochberg (FDR) sobre múltiplos testes simultâneos."""
        if not p_values:
            return []
        m = len(p_values)
        indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])

        adjusted = [0.0] * m
        min_so_far = 1.0

        for rank, (orig_idx, p_val) in reversed(list(enumerate(indexed_p, start=1))):
            adj = min(1.0, (p_val * m) / rank)
            min_so_far = min(min_so_far, adj)
            adjusted[orig_idx] = round(min_so_far, 6)

        return adjusted
