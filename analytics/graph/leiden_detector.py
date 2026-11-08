"""
NexusGov - Detecção Determinística de Comunidades via Algoritmo de Leiden
Requisito: RF-ANA-02 (Critério de Aceite: CA-ANA-02-A)
ADR: ADR-003 (Adoção do Algoritmo de Leiden para Comunidades Conectadas)
"""

from typing import Dict, List, Optional, Tuple
import networkx as nx
import igraph as ig
import leidenalg

class CommunityPartitionResult:
    """Resultado da partição de comunidades com métricas estruturais."""
    def __init__(
        self,
        node_to_community: Dict[str, int],
        modularity: float,
        num_communities: int,
        community_sizes: Dict[int, int]
    ):
        self.node_to_community = node_to_community
        self.modularity = modularity
        self.num_communities = num_communities
        self.community_sizes = community_sizes

    def get_community(self, node_id: str) -> Optional[int]:
        return self.node_to_community.get(node_id)

    def share_same_community(self, node_u: str, node_v: str) -> bool:
        comm_u = self.get_community(node_u)
        comm_v = self.get_community(node_v)
        if comm_u is None or comm_v is None:
            return False
        return comm_u == comm_v


class LeidenCommunityDetector:
    """
    Detector de comunidades pelo algoritmo de Leiden com garantia matemática de
    subgrafos conexos e reprodutibilidade estrita bit-a-bit via semente fixa (seed=42).
    """

    def __init__(self, seed: int = 42, resolution: float = 1.0):
        self.seed = seed
        self.resolution = resolution

    def detect_communities(self, g_nx: nx.Graph) -> CommunityPartitionResult:
        """
        Executa a detecção de comunidades sobre o grafo NetworkX ponderado de empresas.
        Garante CA-ANA-02-A: execuções repetidas com a mesma semente geram a mesma partição.
        """
        if len(g_nx.nodes) == 0:
            return CommunityPartitionResult({}, 0.0, 0, {})

        if len(g_nx.edges) == 0:
            # Sem arestas: cada nó é sua própria comunidade isolada
            node_map = {n: i for i, n in enumerate(g_nx.nodes)}
            sizes = {i: 1 for i in range(len(g_nx.nodes))}
            return CommunityPartitionResult(node_map, 0.0, len(g_nx.nodes), sizes)

        # Mapeamento biunívoco de nós NetworkX (strings) para índices inteiros igraph
        node_list = list(g_nx.nodes)
        node_to_idx = {n: i for i, n in enumerate(node_list)}
        idx_to_node = {i: n for i, n in enumerate(node_list)}

        # Constrói grafo igraph correspondente
        g_ig = ig.Graph()
        g_ig.add_vertices(len(node_list))

        edges = []
        weights = []
        for u, v, d in g_nx.edges(data=True):
            edges.append((node_to_idx[u], node_to_idx[v]))
            weights.append(float(d.get("weight", 1.0)))

        g_ig.add_edges(edges)
        g_ig.es["weight"] = weights

        # Executa o algoritmo de Leiden com semente fixa
        partition = leidenalg.find_partition(
            g_ig,
            leidenalg.ModularityVertexPartition,
            weights="weight",
            seed=self.seed
        )

        modularity = g_ig.modularity(partition.membership, weights=weights)

        node_to_community: Dict[str, int] = {}
        community_sizes: Dict[int, int] = {}

        for idx, comm_id in enumerate(partition.membership):
            original_node = idx_to_node[idx]
            node_to_community[original_node] = comm_id
            community_sizes[comm_id] = community_sizes.get(comm_id, 0) + 1

        return CommunityPartitionResult(
            node_to_community=node_to_community,
            modularity=round(modularity, 4),
            num_communities=len(set(partition.membership)),
            community_sizes=community_sizes
        )
