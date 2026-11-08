"""
NexusGov - Testes de Municípios IBGE e Distância Geodésica (RF-ING-07 / Piloto Paraíba)
"""

import pytest
from ingestion.ibge.municipios import IbgeService

def test_ibge_paraiba_municipalities_present():
    ibge = IbgeService()
    
    # João Pessoa (Capital)
    jp = ibge.get_by_code("2507507")
    assert jp is not None
    assert jp.nome == "João Pessoa"
    assert jp.uf == "PB"
    assert jp.latitude == pytest.approx(-7.11532, abs=0.01)

    # Campina Grande
    cg = ibge.get_by_code("2504009")
    assert cg is not None
    assert cg.nome == "Campina Grande"
    assert cg.uf == "PB"

    # Patos
    patos = ibge.get_by_name("Patos", "PB")
    assert patos is not None
    assert patos.codigo_ibge == "2510808"

def test_haversine_distance_paraiba_cities():
    ibge = IbgeService()
    jp = ibge.get_by_code("2507507") # João Pessoa
    cg = ibge.get_by_code("2504009") # Campina Grande

    distancia = ibge.haversine_distance_km(
        jp.latitude, jp.longitude,
        cg.latitude, cg.longitude
    )

    # Distância real aproximada em linha reta é cerca de 112 a 115 km
    assert 110.0 <= distancia <= 120.0
