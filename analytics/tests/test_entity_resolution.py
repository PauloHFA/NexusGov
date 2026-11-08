"""
NexusGov - Testes de Resolução de Entidades Societárias (RF-ENT-03, RF-ENT-05, CA-ENT-01, SG-05)
"""

import pytest
from analytics.graph.entity_resolution import EntityResolutionEngine

def test_partner_resolution_presumed_identity_and_confidence():
    """
    Critério de Aceite CA-ENT-01:
    Dados dois sócios com mesmo nome e CPF mascarado idêntico,
    o vínculo é criado com confiança < 1,0 e rotulado 'identidade presumida'.
    """
    engine = EntityResolutionEngine(base_confidence_pf=0.80)

    # Sócio com sobrenome comum (Silva) sem outros atributos coincidentes
    partner_silva = engine.resolve_partner_identity(
        nome="João Pedro da Silva",
        cpf_mascarado="***123456**",
        shared_address=False,
        shared_phone_or_email=False
    )

    assert partner_silva.confianca_identidade < 1.0
    assert partner_silva.rotulo_identidade == "identidade presumida"
    # Penalidade por sobrenome comum
    assert partner_silva.confianca_identidade <= 0.60
    assert "SOBRENOME_ALTA_FREQUENCIA" in partner_silva.atributos_compartilhados

def test_partner_confidence_boost_with_shared_attributes():
    engine = EntityResolutionEngine(base_confidence_pf=0.80)

    # Sócio com endereço e telefone compartilhados entre as empresas
    partner_boosted = engine.resolve_partner_identity(
        nome="Severino Ramos de Lucena",
        cpf_mascarado="***987654**",
        shared_address=True,
        shared_phone_or_email=True
    )

    # Confiança deve ser elevada pelo cruzamento de atributos
    assert partner_boosted.confianca_identidade >= 0.90
    assert partner_boosted.confianca_identidade < 1.0 # Nunca 1.0 para PF com CPF mascarado (LGPD)
    assert "ENDERECO_COMPARTILHADO" in partner_boosted.atributos_compartilhados
    assert "CONTATO_COMPARTILHADO" in partner_boosted.atributos_compartilhados

def test_corporate_chains_expansion():
    """Teste de expansão de cadeias societárias multinível (RF-ENT-05)."""
    engine = EntityResolutionEngine()

    empresa_alvo = "08123456000199"
    socios_pj = [("12345678000195", "HOLDING PARTICIPACOES LTDA")]
    pj_qsa_map = {
        "12345678000195": [
            ("s_1", "Carlos Eduardo de Melo", "***555444**")
        ]
    }

    chain_links = engine.resolve_corporate_chains(
        empresa_cnpj=empresa_alvo,
        socios_pj=socios_pj,
        pj_qsa_map=pj_qsa_map,
        max_depth=2
    )

    assert len(chain_links) == 1
    link = chain_links[0]
    assert link.fornecedor_cnpj == empresa_alvo
    assert link.socio_pj_cnpj == "12345678000195"
    assert link.profundidade == 2
    assert link.confianca_acumulada > 0.0
