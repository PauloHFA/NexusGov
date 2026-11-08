"""
NexusGov - Construtor de Grafo Heterogêneo e Projeção Bipartida (RF-ANA-01)
Modelo: V = {E, S, L, A} (Empresas, Sócios, Licitações, Atributos de Contato)
"""

from typing import Any, Dict, List, Optional, Set, Tuple
import networkx as nx
from .normalizer import EntityNormalizer
from .entity_resolution import ResolvedPartner

class NetworkBuilder:
    """
    Constrói o grafo heterogêneo multidimensional e projeta o grafo de coocorrência de empresas.
    """

    def __init__(
        self,
        weight_partner: float = 1.0,
        weight_address: float = 0.8,
        weight_phone: float = 0.6,
        weight_email: float = 0.7,
        weight_tender: float = 1.0
    ):
        self.w_partner = weight_partner
        self.w_address = weight_address
        self.w_phone = weight_phone
        self.w_email = weight_email
        self.w_tender = weight_tender

        # Grafo heterogêneo
        self.graph = nx.Graph()

    def add_company(self, cnpj: str, razao_social: str, uf: str = "PB", municipio_ibge: Optional[str] = None):
        """Adiciona nó de Empresa (E)."""
        clean_cnpj = EntityNormalizer.validate_and_clean_cnpj(cnpj)[1]
        node_id = f"E_{clean_cnpj}"
        self.graph.add_node(
            node_id,
            node_type="E",
            cnpj=clean_cnpj,
            label=EntityNormalizer.normalize_name(razao_social, is_company=True),
            uf=uf,
            municipio_ibge=municipio_ibge
        )
        return node_id

    def add_partner(self, resolved_partner: ResolvedPartner):
        """Adiciona nó de Sócio (S)."""
        node_id = f"S_{resolved_partner.id}"
        self.graph.add_node(
            node_id,
            node_type="S",
            label=resolved_partner.nome_normalizado,
            cpf_mascarado=resolved_partner.cpf_mascarado,
            confianca=resolved_partner.confianca_identidade,
            rotulo=resolved_partner.rotulo_identidade
        )
        return node_id

    def add_tender(self, numero_controle_pncp: str, objeto: str, orgao_nome: str, uf: str = "PB"):
        """Adiciona nó de Licitação / Contratação (L)."""
        node_id = f"L_{numero_controle_pncp}"
        self.graph.add_node(
            node_id,
            node_type="L",
            numero_controle=numero_controle_pncp,
            label=f"Edital {numero_controle_pncp}",
            objeto=objeto,
            orgao=orgao_nome,
            uf=uf
        )
        return node_id

    def add_contact_attribute(self, attr_type: str, canonical_value: str):
        """Adiciona nó de Atributo de Contato (A) - ex: endereço canônico, telefone."""
        node_id = f"A_{attr_type}_{canonical_value}"
        self.graph.add_node(
            node_id,
            node_type="A",
            attr_type=attr_type,
            label=canonical_value
        )
        return node_id

    def link_company_partner(self, company_node: str, partner_node: str, confianca: float = 1.0):
        """Cria aresta E-S ponderada pelo grau de confiança da identidade."""
        peso = self.w_partner * confianca
        self.graph.add_edge(company_node, partner_node, edge_type="E-S", weight=peso)

    def link_company_contact(self, company_node: str, contact_node: str, attr_type: str):
        """Cria aresta E-A (endereço, telefone, e-mail)."""
        if attr_type == "ENDERECO":
            peso = self.w_address
        elif attr_type == "TELEFONE":
            peso = self.w_phone
        else:
            peso = self.w_email
        self.graph.add_edge(company_node, contact_node, edge_type=f"E-A_{attr_type}", weight=peso)

    def link_company_tender(self, company_node: str, tender_node: str, vencedor: bool = False, valor: float = 0.0):
        """Cria aresta E-L (participação em certame)."""
        self.graph.add_edge(
            company_node,
            tender_node,
            edge_type="E-L",
            weight=self.w_tender,
            vencedor=vencedor,
            valor=valor
        )

    def project_company_cooccurrence_graph(self) -> nx.Graph:
        """
        Projeta o grafo heterogêneo em um grafo de coocorrência de empresas (G_E).
        Duas empresas são ligadas se compartilham sócio ou atributo de contato,
        preservando o peso acumulado das relações.
        """
        g_companies = nx.Graph()

        # Seleciona nós de empresas
        company_nodes = [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == "E"]
        for cn in company_nodes:
            g_companies.add_node(cn, **self.graph.nodes[cn])

        # Para cada atributo intermediário (Sócio ou Atributo A), conecta os pares de empresas
        intermediate_nodes = [
            n for n, d in self.graph.nodes(data=True)
            if d.get("node_type") in ("S", "A")
        ]

        for inter in intermediate_nodes:
            vizinhos = [v for v in self.graph.neighbors(inter) if self.graph.nodes[v].get("node_type") == "E"]
            if len(vizinhos) < 2:
                continue

            # Para todos os pares de empresas ligadas a esse intermediário
            for i in range(len(vizinhos)):
                for j in range(i + 1, len(vizinhos)):
                    u, v = vizinhos[i], vizinhos[j]
                    w_u = self.graph[u][inter].get("weight", 1.0)
                    w_v = self.graph[v][inter].get("weight", 1.0)
                    # Peso da ligação entre u e v através de inter
                    edge_w = (w_u + w_v) / 2.0

                    if g_companies.has_edge(u, v):
                        g_companies[u][v]["weight"] += edge_w
                        g_companies[u][v]["sources"].append(inter)
                    else:
                        g_companies.add_edge(u, v, weight=edge_w, sources=[inter])

        return g_companies
