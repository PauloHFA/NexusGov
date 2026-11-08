"""
NexusGov - Cálculo de Centralidade (Betweenness Centrality)
Requisito: RF-ANA-02, RNF-02
"""

from typing import Dict, Optional
import networkx as nx

class CentralityEngine:
    """Calcula métricas de centralidade estrutural para identificar nós-ponte."""

    def __init__(self, sample_threshold: int = 300, sample_k: int = 100, seed: int = 42):
        self.sample_threshold = sample_threshold
        self.sample_k = sample_k
        self.seed = seed

    def calculate_betweenness(self, graph: nx.Graph, weight_attr: Optional[str] = "weight") -> Dict[str, float]:
        """
        Calcula betweenness centrality para os nós do grafo.
        Aplica amostragem (Brandes k-pivot) para grafos que excedam sample_threshold.
        """
        num_nodes = len(graph.nodes)
        if num_nodes <= 2:
            return {n: 0.0 for n in graph.nodes}

        # Converte peso de afinidade em distância: d = 1.0 / weight
        # Nós com maior peso têm menor distância no caminho mínimo
        dist_graph = nx.Graph()
        dist_graph.add_nodes_from(graph.nodes(data=True))
        for u, v, d in graph.edges(data=True):
            w = max(0.001, float(d.get(weight_attr or "weight", 1.0)))
            dist_graph.add_edge(u, v, distance=1.0 / w)

        if num_nodes > self.sample_threshold:
            k = min(self.sample_k, num_nodes)
            centralities = nx.betweenness_centrality(
                dist_graph,
                k=k,
                normalized=True,
                weight="distance",
                seed=self.seed
            )
        else:
            centralities = nx.betweenness_centrality(
                dist_graph,
                normalized=True,
                weight="distance"
            )

        return {k: round(v, 5) for k, v in centralities.items()}
