"""
NexusGov - Testes de Validação de Esquema de Origem (RF-ING-09)
"""

import pytest
from ingestion.parsers.schema_validator import SchemaValidator, SchemaValidationException

def test_valid_pncp_payload_passes():
    valid = {
        "numeroControlePNCP": "00000000000191-1-000001/2026",
        "orgaoEntidade": {"cnpj": "08123456000199", "razaoSocial": "Prefeitura Municipal de João Pessoa"},
        "anoCompra": 2026,
        "modalidadeNome": "Dispensa de Licitação"
    }
    assert SchemaValidator.validate_pncp_payload(valid) is True

def test_invalid_pncp_payload_raises_exception():
    invalid = {
        "anoCompra": 2026
        # Faltam numeroControlePNCP, orgaoEntidade, modalidadeNome
    }
    with pytest.raises(SchemaValidationException) as exc_info:
        SchemaValidator.validate_pncp_payload(invalid)

    assert "Quebra de esquema no PNCP" in str(exc_info.value)
    assert "numeroControlePNCP" in str(exc_info.value)

def test_csv_column_validation():
    expected = ["col1", "col2", "col3"]
    actual = ["col1", "col2", "col3"]
    assert SchemaValidator.validate_csv_columns(actual, expected, "Teste") is True

    with pytest.raises(SchemaValidationException):
        SchemaValidator.validate_csv_columns(["col1", "col2"], expected, "TesteIncompleto")
