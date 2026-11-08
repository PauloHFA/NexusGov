"""
NexusGov - Gerador de Dados Sintéticos e Validação Científica (SRS Seção 4.7 / CA-CIE-02)
Gera cenários controlados com cartéis, fracionamentos e empresas recém-criadas
para medição de precisão, revocação e F1 dos detectores.
"""

from datetime import date, timedelta
from typing import Dict, List, Tuple
import numpy as np
from analytics.split.fracionamento import ContractPurchaseEntry

class SyntheticScenarioGenerator:
    """Gerador de dados sintéticos para calibração analítica e testes de propriedades."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def generate_benford_series(self, n: int = 1000, min_val: float = 10.0, max_val: float = 1000000.0) -> List[float]:
        """
        Gera uma série perfeitamente conforme à Lei de Benford através de distribuição log-uniforme.
        MAD esperado: <= 0.006 (Próximo).
        """
        log_min = np.log10(min_val)
        log_max = np.log10(max_val)
        u = self.rng.uniform(log_min, log_max, size=n)
        return [round(float(10.0 ** x), 2) for x in u]

    def generate_anomalous_series(self, n: int = 1000, fixed_digit: int = 7) -> List[float]:
        """
        Gera uma série que viola a Lei de Benford (ex: excesso de valores começando com o mesmo dígito).
        MAD esperado: > 0.015 (Não conforme).
        """
        vals = []
        for _ in range(n):
            # 80% dos números começam com fixed_digit
            if self.rng.random() < 0.80:
                base = fixed_digit * (10 ** self.rng.integers(2, 5))
                offset = self.rng.uniform(0, 99)
                vals.append(round(float(base + offset), 2))
            else:
                vals.append(round(float(self.rng.uniform(100, 50000)), 2))
        return vals

    def generate_synthetic_split_purchases(
        self,
        orgao_id: str = "ORGAO_PB_01",
        fornecedor_cnpj: str = "08123456000199",
        teto: float = 59906.02,
        num_fracionadas: int = 4,
        dias_intervalo: int = 45
    ) -> List[ContractPurchaseEntry]:
        """
        Gera compras propositalmente fracionadas (logo abaixo do teto) para testar CA-ANA-03.
        """
        base_date = date(2024, 6, 1)
        entries: List[ContractPurchaseEntry] = []

        step = dias_intervalo // num_fracionadas
        for i in range(num_fracionadas):
            dt = base_date + timedelta(days=i * step)
            # Valor entre 92% e 98% do teto legal
            val = round(teto * float(self.rng.uniform(0.92, 0.98)), 2)
            entries.append(ContractPurchaseEntry(
                id=f"dispensa_split_{i+1}",
                numero_controle_pncp=f"08123456000199-1-{i+1:06d}/2024",
                orgao_id=orgao_id,
                fornecedor_cnpj=fornecedor_cnpj,
                data_contratacao=dt,
                valor=val,
                codigo_catmat="150645", # Mesmo código CATMAT de materiais
                objeto_descricao="Material de expediente fracionado",
                modalidade_objeto="DISPENSA_COMPRAS_SERVICOS"
            ))

        return entries
