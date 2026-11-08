"""
NexusGov - Cálculo de Risco por Licitação (RC) e Controle por Grafo Nulo (RF-ANA-03)
Critério de Aceite: CA-ANA-01
"""

from typing import Dict, List, Optional, Set, Tuple
import numpy as np
import networkx as nx
from .leiden_detector import CommunityPartitionResult

class TenderRiskResult:
    """Resultado do risco de cartel/coocorrência em um certame."""
    def __init__(
        self,
        edital_id: str,
        total_licitantes: int,
        pares_totais: int,
        pares_coligados: int,
        rc_bruto: float,
        rc_esperado_nulo: float,
        rc_ajustado: float,
        detalhes_pares: List[Dict]
    ):
        self.edital_id = edital_id
        self.total_licitantes = total_licitantes
        self.pares_totais = pares_totais
        self.pares_coligados = pares_coligados
        self.rc_bruto = rc_bruto
        self.rc_esperado_nulo = rc_esperado_nulo
        self.rc_ajustado = rc_ajustado
        self.detalhes_pares = detalhes_pares

    @property
    def nivel_risco(self) -> str:
        if self.rc_ajustado >= 0.60:
            return "Elevado"
        elif self.rc_ajustado >= 0.30:
            return "Médio"
        return "Baixo"


class TenderGraphRiskEngine:
    """
    Calcula o coeficiente de risco RC de uma licitação ponderado por comunidade e atributos,
    comparando contra um modelo nulo para mitigar falsos positivos em mercados concentrados.
    """

    def __init__(self, num_null_permutations: int = 50, seed: int = 42):
        self.num_null = num_null_permutations
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def calculate_tender_rc(
        self,
        edital_id: str,
        licitantes_cnpjs: List[str],
        g_companies: nx.Graph,
        partition: CommunityPartitionResult
    ) -> TenderRiskResult:
        """
        Calcula o risco RC bruto e ajustado pelo modelo nulo para os licitantes do certame.
        """
        licitantes_nodes = [
            f"E_{cnpj}" if not cnpj.startswith("E_") else cnpj
            for cnpj in licitantes_cnpjs
        ]
        # Filtra apenas licitantes presentes no grafo
        licitantes_presentes = [n for n in licitantes_nodes if g_companies.has_node(n)]
        n = len(licitantes_presentes)

        if n < 2:
            return TenderRiskResult(
                edital_id=edital_id,
                total_licitantes=n,
                pares_totais=0,
                pares_coligados=0,
                rc_bruto=0.0,
                rc_esperado_nulo=0.0,
                rc_ajustado=0.0,
                detalhes_pares=[]
            )

        total_pares = (n * (n - 1)) // 2
        pares_coligados = 0
        soma_pesos = 0.0
        detalhes: List[Dict] = []

        for i in range(n):
            for j in range(i + 1, n):
                u, v = licitantes_presentes[i], licitantes_presentes[j]
                same_community = partition.share_same_community(u, v)
                has_direct_edge = g_companies.has_edge(u, v)
                direct_weight = g_companies[u][v].get("weight", 0.0) if has_direct_edge else 0.0

                if same_community or has_direct_edge:
                    pares_coligados += 1
                    # Peso combinado: comunidade base (0.5) + aresta direta ponderada
                    score_par = min(1.0, (0.5 if same_community else 0.0) + direct_weight * 0.5)
                    soma_pesos += score_par
                    detalhes.append({
                        "empresa_1": u,
                        "empresa_2": v,
                        "mesma_comunidade": same_community,
                        "vinculo_direto": has_direct_edge,
                        "peso_aresta": direct_weight,
                        "escore_par": round(score_par, 4)
                    })

        rc_bruto = soma_pesos / total_pares

        # Modelo Nulo: calcula a expectativa de coligação aleatória no grafo
        rc_esperado_nulo = self._estimate_null_baseline(licitantes_presentes, g_companies, partition)

        # Ajuste pelo modelo nulo: isola o excesso de concentração além do esperado aleatoriamente
        denominador = max(0.001, 1.0 - rc_esperado_nulo)
        rc_ajustado = max(0.0, (rc_bruto - rc_esperado_nulo) / denominador)
        rc_ajustado = min(1.0, round(rc_ajustado, 4))

        return TenderRiskResult(
            edital_id=edital_id,
            total_licitantes=n,
            pares_totais=total_pares,
            pares_coligados=pares_coligados,
            rc_bruto=round(rc_bruto, 4),
            rc_esperado_nulo=round(rc_esperado_nulo, 4),
            rc_ajustado=rc_ajustado,
            detalhes_pares=detalhes
        )

    def _estimate_null_baseline(
        self,
        licitantes: List[str],
        g_companies: nx.Graph,
        partition: CommunityPartitionResult
    ) -> float:
        """
        Estima a expectativa de coligação aleatória permutando aleatoriamente as comunidades dos nós.
        """
        all_nodes = list(g_companies.nodes)
        if len(all_nodes) <= len(licitantes):
            # Mercado pequeno demais (quase todos os nós licitam): expectativa intrínseca do grafo
            num_edges = len(g_companies.edges)
            max_edges = (len(all_nodes) * (len(all_nodes) - 1)) / 2
            return num_edges / max_edges if max_edges > 0 else 0.0

        all_communities = [partition.get_community(n) for n in all_nodes]
        k = len(licitantes)
        total_pairs = (k * (k - 1)) / 2

        null_scores = []
        for _ in range(min(20, self.num_null)):
            # Amostra aleatória de comunidades do universo geral do grafo
            sampled_comms = self.rng.choice(all_communities, size=k, replace=False)
            colligated = sum(
                1 for i in range(k) for j in range(i + 1, k)
                if sampled_comms[i] == sampled_comms[j]
            )
            null_scores.append(colligated / total_pairs)

        return float(np.mean(null_scores)) if null_scores else 0.0
