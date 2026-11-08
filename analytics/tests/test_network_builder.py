"""
NexusGov - Testes de Construção de Grafo e Projeção Bipartida (RF-ANA-01)
"""

import pytest
from analytics.graph.network_builder import NetworkBuilder
from analytics.graph.entity_resolution import ResolvedPartner

def test_build_heterogeneous_graph_and_projection():
    builder = NetworkBuilder()

    # Adiciona 3 empresas na Paraíba
    e1 = builder.add_company("08123456000199", "Empresa Alpha Comércio de Medicamentos", uf="PB")
    e2 = builder.add_company("12345678000195", "Beta Distribuidora Hospitalar", uf="PB")
    e3 = builder.add_company("33000167000101", "Gama Serviços Gerais", uf="PB")

    # Sócio compartilhado entre Alpha e Beta
    socio_comum = ResolvedPartner(
        id="socio_carlos_melo",
        nome_normalizado="CARLOS EDUARDO DE MELO",
        cpf_mascarado="***555444**",
        confianca_identidade=0.85
    )
    s_node = builder.add_partner(socio_comum)
    builder.link_company_partner(e1, s_node, confianca=0.85)
    builder.link_company_partner(e2, s_node, confianca=0.85)

    # Endereço compartilhado entre Alpha e Beta em João Pessoa
    addr_node = builder.add_contact_attribute("ENDERECO", "AV EPITACIO PESSOA|100|58000000")
    builder.link_company_contact(e1, addr_node, "ENDERECO")
    builder.link_company_contact(e2, addr_node, "ENDERECO")

    # Edital disputado pelas 3 empresas
    l_node = builder.add_tender("00001/2026", "Aquisição de Insumos", "Prefeitura de João Pessoa", uf="PB")
    builder.link_company_tender(e1, l_node, vencedor=True, valor=150000.0)
    builder.link_company_tender(e2, l_node, vencedor=False, valor=155000.0)
    builder.link_company_tender(e3, l_node, vencedor=False, valor=160000.0)

    # Projeção de coocorrência de empresas
    g_companies = builder.project_company_cooccurrence_graph()

    # Nós de empresas devem existir no grafo projetado
    assert g_companies.has_node(e1)
    assert g_companies.has_node(e2)
    assert g_companies.has_node(e3)

    # Alpha e Beta devem ter aresta direta com acúmulo de pesos (sócio + endereço)
    assert g_companies.has_edge(e1, e2)
    peso_alpha_beta = g_companies[e1][e2]["weight"]
    assert peso_alpha_beta > 1.0 # 0.85 (sócio) + 0.8 (endereço)

    # Gama (e3) não compartilha sócio nem endereço, portanto não deve ter aresta com e1 ou e2
    assert not g_companies.has_edge(e1, e3)
    assert not g_companies.has_edge(e2, e3)
