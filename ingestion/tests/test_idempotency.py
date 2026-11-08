"""
NexusGov - Testes de Idempotência e Relatório de Qualidade (RF-ING-06, RF-ING-08, CA-ING-01)
"""

from pathlib import Path
import pytest
from ingestion.models.payloads import PncpContratacao
from ingestion.storage.idempotent_loader import IdempotentDataLoader

def test_idempotent_load_does_not_duplicate_records(tmp_path: Path):
    loader = IdempotentDataLoader(processed_dir=tmp_path)

    sample_contratacoes = [
        PncpContratacao(
            numero_controle_pncp="08123456000199-1-000001/2026",
            orgao_cnpj="08123456000199",
            orgao_nome="Prefeitura de Campina Grande",
            uf="PB",
            modalidade_nome="Dispensa de Licitação",
            ano_compra=2026,
            objeto="Fornecimento de material de consumo",
            valor_total_homologado=45000.00
        ),
        PncpContratacao(
            numero_controle_pncp="08123456000199-1-000002/2026",
            orgao_cnpj="08123456000199",
            orgao_nome="Prefeitura de Campina Grande",
            uf="PB",
            modalidade_nome="Dispensa de Licitação",
            ano_compra=2026,
            objeto="Serviços de manutenção predial",
            valor_total_homologado=52000.00
        )
    ]

    # Primeira carga
    _, report1 = loader.load_contratacoes(sample_contratacoes, competencia="2026-09", uf="PB")
    assert report1.total_lidos == 2
    assert report1.total_aceitos == 2
    assert report1.total_duplicados_ignorados == 0

    # Segunda carga (mesma competência e mesmos dados) -> Critério de Aceite CA-ING-01
    _, report2 = loader.load_contratacoes(sample_contratacoes, competencia="2026-09", uf="PB")
    assert report2.total_lidos == 2
    assert report2.total_aceitos == 0
    assert report2.total_duplicados_ignorados == 2
