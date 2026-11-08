"""
NexusGov - Testes de Normalização de CNPJ, Nomes, Endereços e Contatos (RF-ENT-01, RF-ENT-02)
"""

import pytest
from analytics.graph.normalizer import EntityNormalizer

def test_cnpj_validation_valid():
    # CNPJs oficiais e matematicamente válidos
    valid_cnpjs = [
        "00.000.000/0001-91", # Banco do Brasil
        "33.000.167/0001-01", # Petrobras
        "00.394.460/0058-87", # Ministério da Fazenda
        "00.394.460/0001-41"  # Receita Federal
    ]
    for c in valid_cnpjs:
        is_valid, cleaned = EntityNormalizer.validate_and_clean_cnpj(c)
        assert is_valid is True, f"CNPJ {c} deveria ser válido"
        assert len(cleaned) == 14

def test_cnpj_validation_invalid():
    # CNPJs com dígitos verificadores incorretos ou repetidos
    invalid_cnpjs = [
        "12.345.678/0001-00", # DV errado
        "00.000.000/0000-00", # Repetido
        "11.111.111/1111-11", # Repetido
        "12345",              # Tamanho insuficiente
        ""
    ]
    for c in invalid_cnpjs:
        is_valid, _ = EntityNormalizer.validate_and_clean_cnpj(c)
        assert is_valid is False, f"CNPJ {c} deveria ser inválido"

def test_name_normalization_person_and_company():
    # Pessoa Física: preserva nome limpo e sem acento
    nome_pf = "José da Silva Souza Júnior"
    pf_clean = EntityNormalizer.normalize_name(nome_pf, is_company=False)
    assert pf_clean == "JOSE DA SILVA SOUZA JUNIOR"

    # Pessoa Jurídica: remove partículas societárias (LTDA, ME, EPP, S/A, etc.)
    nome_pj = "Construtora Epitácio Pessoa & Filhos LTDA - EPP"
    pj_clean = EntityNormalizer.normalize_name(nome_pj, is_company=True)
    assert pj_clean == "CONSTRUTORA EPITACIO PESSOA FILHOS"

def test_address_normalization_canonical_key():
    # Normaliza variações de prefixo de logradouro e número
    addr1 = EntityNormalizer.normalize_address(
        logradouro="Avenida Presidente Epitácio Pessoa",
        numero="100 - Sala 10",
        cep="58.000-000"
    )
    addr2 = EntityNormalizer.normalize_address(
        logradouro="Av. Pres. Epitacio Pessoa",
        numero="100",
        cep="58000000"
    )

    # Ambos devem canonizar para o mesmo CEP e número
    assert addr1.endswith("|100|58000000")
    assert addr2.endswith("|100|58000000")

    # Tratamento de sem número
    addr_sn = EntityNormalizer.normalize_address("Rua das Flores", "S/N", "58000-001")
    assert addr_sn.endswith("|SN|58000001")

def test_phone_normalization():
    # Normaliza telefones da Paraíba (DDD 83)
    p1 = EntityNormalizer.normalize_phone("083", "3211-0000")
    p2 = EntityNormalizer.normalize_phone("83", "32110000")
    assert p1 == "8332110000"
    assert p2 == "8332110000"
