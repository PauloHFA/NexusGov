"""
NexusGov - Testes do Coletor PNCP (RF-ING-01, RF-ING-02, CA-ING-01-A)
"""

import pytest
from pathlib import Path
from ingestion.collectors.pncp import PncpCollector
from ingestion.storage.raw_storage import RawStorageManager

import pytest
from pathlib import Path
from ingestion.collectors.pncp import PncpCollector
from ingestion.storage.raw_storage import RawStorageManager

def test_pncp_collector_parses_and_stores_evidence(tmp_path: Path):
    mock_data = {
        "totalRegistros": 1,
        "totalPaginas": 1,
        "numeroPagina": 1,
        "data": [
            {
                "numeroControlePNCP": "08123456000199-1-000001/2026",
                "anoCompra": 2026,
                "numeroCompra": "00001/2026",
                "modalidadeNome": "Dispensa de Licitação",
                "objetoCompra": "Aquisição emergencial de medicamentos em Patos - PB",
                "valorTotalHomologado": 75000.00,
                "orgaoEntidade": {
                    "cnpj": "08.123.456/0001-99",
                    "razaoSocial": "Prefeitura Municipal de Patos",
                    "esferaId": "MUNICIPAL",
                    "poderId": "EXECUTIVO"
                },
                "unidadeOrgao": {
                    "municipioId": "2510808" # Patos PB
                },
                "itens": [
                    {
                        "numeroItem": 1,
                        "descricao": "Item 1 Medicamento",
                        "quantidade": 100,
                        "valorUnitarioHomologado": 750.0,
                        "valorTotal": 75000.0
                    }
                ]
            }
        ]
    }

    storage = RawStorageManager(base_dir=tmp_path)
    collector = PncpCollector(raw_storage=storage)

    # Executa a coleta síncrona com mock
    results = collector.collect_contratacoes_sync(
        data_inicial="20260901",
        data_final="20260930",
        uf="PB",
        max_paginas=1,
        sync_fetch_fn=lambda url, params: mock_data
    )

    assert len(results) == 1
    c = results[0]
    assert c.numero_controle_pncp == "08123456000199-1-000001/2026"
    assert c.uf == "PB"
    assert c.codigo_ibge_municipio == "2510808"
    assert c.valor_total_homologado == 75000.00
    assert len(c.itens) == 1

    # Confirma que a evidência bruta imutável foi gravada em disco com hash SHA-256
    raw_files = list(tmp_path.rglob("*.json"))
    assert len(raw_files) >= 1
    assert storage.verify_file(raw_files[0]) is True





