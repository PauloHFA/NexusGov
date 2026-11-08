"""
NexusGov - Testes de Cruzamento de Sanções e Vedações Federais (Melhoria 2)
"""

from datetime import date
import pytest
from ingestion.sanctions.cgu_ceis_cnep import SanctionCatalog, SanctionEntry, SanctionType
from analytics.sanctions.sanction_matcher import SanctionMatcher


def test_direct_sanction_match_ceis():
    catalog = SanctionCatalog()
    catalog.add_entry(SanctionEntry(
        id_sancao="SANC_001",
        tipo_cadastro=SanctionType.CEIS,
        cnpj_cpf_sancionado="11.222.333/0001-44",
        nome_razao_social="Empresa Inidônea Alfa Ltda",
        orgao_sancionador="Tribunal de Contas da União",
        fundamentacao_legal="Lei nº 8.666/93 Art. 87, IV",
        data_inicio_sancao=date(2023, 1, 1),
        data_fim_sancao=date(2025, 12, 31),
        ativo=True
    ))

    matcher = SanctionMatcher(catalog)
    finding = matcher.evaluate_supplier(
        cnpj="11222333000144",
        razao_social="Empresa Inidônea Alfa Ltda",
        socios=[],
        data_referencia=date(2024, 6, 1)
    )

    assert finding.tem_impedimento_direto is True
    assert finding.escore_sinal == 1.0
    assert len(finding.sancoes_diretas) == 1
    assert finding.sancoes_diretas[0].tipo_cadastro == SanctionType.CEIS

    # Converte para sinal do IEA
    signal = matcher.to_axis_signal(finding)
    assert signal is not None
    assert signal.eixo == "SANCOES"
    assert signal.nome_sinal == "SANCTION_DIRECT_MATCH"


def test_indirect_partner_sanction_match():
    catalog = SanctionCatalog()
    catalog.add_entry(SanctionEntry(
        id_sancao="SANC_002",
        tipo_cadastro=SanctionType.CNEP,
        cnpj_cpf_sancionado="***.456.789-**",
        nome_razao_social="CARLOS EDUARDO SILVEIRA",
        orgao_sancionador="Controladoria-Geral da União",
        fundamentacao_legal="Lei nº 12.846/2013 Art. 19",
        data_inicio_sancao=date(2023, 5, 10),
        data_fim_sancao=None, # Vigência aberta
        ativo=True
    ))

    matcher = SanctionMatcher(catalog)
    socios = [
        {"cpf_cnpj": "***.456.789-**", "nome": "CARLOS EDUARDO SILVEIRA"},
        {"cpf_cnpj": "***.111.222-**", "nome": "MARIA FERNANDA LIMA"}
    ]

    finding = matcher.evaluate_supplier(
        cnpj="99.888.777/0001-66", # Empresa não está no CEIS
        razao_social="Beta Engenharia e Obras Ltda",
        socios=socios,
        data_referencia=date(2024, 8, 15)
    )

    assert finding.tem_impedimento_direto is False
    assert finding.tem_impedimento_indireto_socio is True
    assert finding.escore_sinal == 0.75
    assert len(finding.sancoes_indiretas_socios) == 1
    assert finding.sancoes_indiretas_socios[0]["socio_nome"] == "CARLOS EDUARDO SILVEIRA"

    signal = matcher.to_axis_signal(finding)
    assert signal is not None
    assert signal.nome_sinal == "SANCTION_INDIRECT_PARTNER_MATCH"
