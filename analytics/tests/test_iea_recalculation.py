"""
NexusGov - Testes de Recálculo Histórico Versionado (RF-ANA-09 / CA-ANA-09)
"""

import pytest
from analytics.iea.engine import IeaEngine, AxisSignal


def test_versioned_historical_recalculation():
    """
    Valida CA-ANA-09:
    Dado uma mudança de pesos de parâmetros (v1.0 vs v1.1),
    Quando um recálculo é solicitado,
    Então os resultados anteriores da v1.0 são mantidos intactos e a nova linha é vinculada à v1.1.
    """
    sinais = [
        AxisSignal(eixo="GRAFO", nome_sinal="COMMUNITY_COVER_BIDDING", intensidade=0.80, peso=1.0, confianca=0.90),
        AxisSignal(eixo="FRACIONAMENTO", nome_sinal="SLIDING_WINDOW_EXCEEDED", intensidade=0.70, peso=1.0, confianca=1.00),
    ]

    # Execução na versão v1.0.0
    engine_v1 = IeaEngine(versao_parametros="v1.0.0")
    res_v1 = engine_v1.calculate_iea("CONTRATACAO_PB_100", sinais)

    assert res_v1.versao_parametros == "v1.0.0"
    score_v1 = res_v1.valor_iea_final

    # Execução com novos pesos em versão v1.1.0 (ex.: peso maior para o eixo GRAFO)
    pesos_v1_1 = {"GRAFO": 2.0, "FRACIONAMENTO": 1.0}
    engine_v1_1 = IeaEngine(versao_parametros="v1.1.0", pesos_customizados=pesos_v1_1)
    res_v1_1 = engine_v1_1.calculate_iea("CONTRATACAO_PB_100", sinais)

    assert res_v1_1.versao_parametros == "v1.1.0"
    score_v1_1 = res_v1_1.valor_iea_final

    # Ambos os cálculos coexistem e registram suas respectivas versões
    assert res_v1.versao_parametros != res_v1_1.versao_parametros
    assert score_v1 != score_v1_1

    # Determinismo estrito bit-a-bit para v1.0.0
    res_v1_repeat = engine_v1.calculate_iea("CONTRATACAO_PB_100", sinais)
    assert res_v1.valor_iea_final == res_v1_repeat.valor_iea_final
