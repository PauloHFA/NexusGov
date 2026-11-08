"""
NexusGov - Testes de Risco de Certame (RC) e Controle por Grafo Nulo (RF-ANA-03, CA-ANA-01)
"""

import pytest
import networkx as nx
from analytics.graph.network_builder import NetworkBuilder
from analytics.graph.entity_resolution import ResolvedPartner
from analytics.graph.leiden_detector import LeidenCommunityDetector
from analytics.graph.null_graph import TenderGraphRiskEngine

def test_synthetic_cartel_detection_ca_ana_01():
    """
    Critério de Aceite CA-ANA-01:
    Dado um conjunto com 5 empresas compartilhando 2 sócios e disputando licitações,
    quando o grafo é analisado, então as 5 pertencem à mesma comunidade e o RC supera 'Médio' (>= 0.30).
    """
    builder = NetworkBuilder()

    # 5 empresas sintéticas
    companies = []
    for i in range(1, 6):
        node = builder.add_company(f"1111111100010{i}", f"Fornecedor Coligado {i} LTDA", uf="PB")
        companies.append(node)

    # 2 sócios compartilhados entre as 5 empresas
    s1 = builder.add_partner(ResolvedPartner(
        id="socio_1", nome_normalizado="MARCOS ANTONIO DE SOUZA",
        cpf_mascarado="***111222**", confianca_identidade=0.85
    ))
    s2 = builder.add_partner(ResolvedPartner(
        id="socio_2", nome_normalizado="JOSE CARLOS PEREIRA",
        cpf_mascarado="***333444**", confianca_identidade=0.85
    ))

    # Vincula os 2 sócios compartilhados a todas as 5 empresas do cartel (conforme CA-ANA-01)
    for c in companies:
        builder.link_company_partner(c, s1, confianca=0.85)
        builder.link_company_partner(c, s2, confianca=0.85)

    # 10 outras empresas independentes no mercado local da Paraíba (universo nulo)
    other_companies = []
    for i in range(10, 20):
        c_ind = builder.add_company(f"999999990001{i}", f"Empresa Independente {i}", uf="PB")
        other_companies.append(c_ind)

    # Projeção de coocorrência de empresas
    g_companies = builder.project_company_cooccurrence_graph()

    # Detecção de comunidades via Leiden
    detector = LeidenCommunityDetector(seed=42)
    partition = detector.detect_communities(g_companies)

    # Verifica se as 5 empresas coligadas pertencem à MESMA comunidade
    comm_0 = partition.get_community(companies[0])
    for c in companies[1:]:
        assert partition.get_community(c) == comm_0, f"Empresa {c} deveria estar na comunidade {comm_0}"

    # Avaliação de risco do edital disputado pelas 5 empresas coligadas
    risk_engine = TenderGraphRiskEngine(seed=42)
    result = risk_engine.calculate_tender_rc(
        edital_id="EDITAL_001/2026",
        licitantes_cnpjs=companies,
        g_companies=g_companies,
        partition=partition
    )

    # O RC do certame deve superar o limiar "Médio" (>= 0.30)
    assert result.pares_coligados == 10 # 5 * 4 / 2 = 10 pares todos conectados
    assert result.rc_bruto >= 0.50
    assert result.rc_ajustado >= 0.30
    assert result.nivel_risco in ("Médio", "Elevado")
