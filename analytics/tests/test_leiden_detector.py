"""
NexusGov - Testes de Detecção de Comunidades via Algoritmo de Leiden (RF-ANA-02, CA-ANA-02-A)
"""

import pytest
import networkx as nx
from analytics.graph.leiden_detector import LeidenCommunityDetector

def test_leiden_community_detection_determinism():
    """
    Critério de Aceite CA-ANA-02-A:
    Executar Leiden com semente fixa deve produzir resultados estritamente determinísticos.
    """
    # Constrói grafo de teste com duas comunidades distintas interligadas
    # Comunidade A: nós 0, 1, 2, 3
    # Comunidade B: nós 4, 5, 6, 7
    g = nx.Graph()
    # Comunidade 1 (clique)
    for i in range(4):
        for j in range(i + 1, 4):
            g.add_edge(f"E_{i}", f"E_{j}", weight=2.0)

    # Comunidade 2 (clique)
    for i in range(4, 8):
        for j in range(i + 1, 8):
            g.add_edge(f"E_{i}", f"E_{j}", weight=2.0)

    # Ponte fraca entre as duas comunidades
    g.add_edge("E_3", "E_4", weight=0.1)

    detector1 = LeidenCommunityDetector(seed=42)
    detector2 = LeidenCommunityDetector(seed=42)

    res1 = detector1.detect_communities(g)
    res2 = detector2.detect_communities(g)

    # Mesma partição exata bit-a-bit
    assert res1.node_to_community == res2.node_to_community
    assert res1.modularity == res2.modularity
    assert res1.num_communities == 2

    # Verifica se os nós da comunidade 1 estão todos agrupados juntos
    c0 = res1.get_community("E_0")
    for i in range(1, 4):
        assert res1.get_community(f"E_{i}") == c0

    # Verifica se a comunidade 2 é diferente da comunidade 1
    c1 = res1.get_community("E_4")
    assert c1 != c0
    for i in range(5, 8):
        assert res1.get_community(f"E_{i}") == c1
