"""
NexusGov - Testes de Centralidade de Intermediação (RF-ANA-02, RNF-02)
"""

import pytest
import networkx as nx
from analytics.graph.centrality import CentralityEngine

def test_betweenness_identifies_bridge_node():
    # Cria duas comunidades (cliques) conectadas por um único nó-ponte "E_ponte"
    g = nx.Graph()

    # Bloco A: 1, 2, 3
    for u in ["E_1", "E_2", "E_3"]:
        for v in ["E_1", "E_2", "E_3"]:
            if u != v:
                g.add_edge(u, v, weight=1.0)

    # Bloco B: 4, 5, 6
    for u in ["E_4", "E_5", "E_6"]:
        for v in ["E_4", "E_5", "E_6"]:
            if u != v:
                g.add_edge(u, v, weight=1.0)

    # Nó intermediário conectando Bloco A e Bloco B
    g.add_edge("E_ponte", "E_1", weight=1.0)
    g.add_edge("E_ponte", "E_4", weight=1.0)

    engine = CentralityEngine()
    centralities = engine.calculate_betweenness(g)

    # O nó "E_ponte" deve ter a maior intermediação (betweenness) de todo o grafo
    assert "E_ponte" in centralities
    max_node = max(centralities, key=centralities.get)
    assert max_node == "E_ponte"
    assert centralities["E_ponte"] > 0.40
