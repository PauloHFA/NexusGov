"""
NexusGov - Validador de Esquema de Origem (RF-ING-09)
Detecta quebras estruturais nas fontes (PNCP ou Receita Federal) e interrompe
a carga emitindo alerta descritivo.
"""

from typing import Any, Dict, List, Set

class SchemaValidationException(Exception):
    """Exceção levantada quando a fonte de dados altera seu esquema."""
    pass

class SchemaValidator:
    """Valida schemas obrigatórios antes da gravação em lote."""

    # Campos mínimos exigidos no payload de contratação do PNCP
    PNCP_REQUIRED_FIELDS: Set[str] = {
        "numeroControlePNCP",
        "orgaoEntidade",
        "anoCompra",
        "modalidadeNome"
    }

    # Colunas esperadas nos arquivos da Receita Federal (Estabelecimentos)
    RECEITA_ESTABELECIMENTOS_COLUMNS: List[str] = [
        "cnpj_basico", "cnpj_ordem", "cnpj_dv", "identificador_matriz_filial",
        "nome_fantasia", "situacao_cadastral", "data_situacao_cadastral",
        "motivo_situacao_cadastral", "nome_cidade_exterior", "pais",
        "data_inicio_atividade", "cnae_fiscal_principal", "cnae_fiscal_secundaria",
        "tipo_logradouro", "logradouro", "numero", "complemento", "bairro",
        "cep", "uf", "municipio", "ddd_1", "telefone_1", "ddd_2", "telefone_2",
        "ddd_fax", "fax", "correio_eletronico", "situacao_especial", "data_situacao_especial"
    ]

    # Colunas esperadas nos arquivos da Receita Federal (Sócios)
    RECEITA_SOCIOS_COLUMNS: List[str] = [
        "cnpj_basico", "identificador_socio", "nome_socio", "cnpj_cpf_socio",
        "qualificacao_socio", "data_entrada_sociedade", "pais", "representante_legal",
        "nome_representante", "qualificacao_representante", "faixa_etaria"
    ]

    @classmethod
    def validate_pncp_payload(cls, payload: Dict[str, Any]) -> bool:
        """Valida se o registro individual do PNCP contém os atributos mandatórios."""
        missing = [f for f in cls.PNCP_REQUIRED_FIELDS if f not in payload]
        if missing:
            raise SchemaValidationException(
                f"Quebra de esquema no PNCP! Campos ausentes: {missing}. Payload: {payload}"
            )
        return True

    @classmethod
    def validate_csv_columns(cls, actual_columns: List[str], expected_columns: List[str], dataset_name: str) -> bool:
        """Valida se a lista de colunas do dump da Receita corresponde ao esperado."""
        if len(actual_columns) != len(expected_columns):
            raise SchemaValidationException(
                f"Esquema incompatível no dump da Receita Federal ({dataset_name})! "
                f"Esperado: {len(expected_columns)} colunas, Recebido: {len(actual_columns)} colunas."
            )
        return True
