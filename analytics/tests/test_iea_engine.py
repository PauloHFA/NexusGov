"""
NexusGov - Testes do Motor de IEA e Salvaguardas Invioláveis (RF-ANA-07, SG-01 a SG-05, CA-ANA-05, CA-SG-02)
"""

import pytest
from analytics.iea.engine import IeaEngine, AxisSignal

def test_iea_multiaxis_requirement_ca_sg_02():
    """
    Critério de Aceite CA-SG-02 & Salvaguarda Inviolável SG-04:
    Dado um caso com apenas um sinal alto (ex: só Benford),
    quando o IEA é calculado, então o nível máximo é 'Médio'.
    """
    engine = IeaEngine()

    # Caso com APENAS Benford em alta exposição (sinal = 1.0), sem outros eixos
    sinais_um_eixo = [
        AxisSignal(
            eixo="BENFORD",
            nome_sinal="BENFORD_MAD_HIGH",
            intensidade=1.0, # Máxima anomalia em Benford
            peso=0.8,
            confianca=1.0
        )
    ]

    result = engine.calculate_iea(
        contratacao_id="EDITAL_BENFORD_ISOLADO/2026",
        sinais=sinais_um_eixo
    )

    # O escore aritmético é 100, mas o nível DEVE ser truncado em 'Médio'
    assert result.escore_aritmetico == 100.0
    assert result.nivel_risco == "Médio", f"Deveria ter sido truncado para 'Médio', recebido: {result.nivel_risco}"
    assert result.truncado_por_salvaguarda is True
    assert "SG-04" in result.motivo_truncamento

def test_iea_elevated_risk_with_two_independent_axes():
    """Com dois eixos independentes significativos (Grafo + Fracionamento), o nível 'Elevado' é concedido."""
    engine = IeaEngine()

    sinais_multieixo = [
        AxisSignal(
            eixo="GRAFO",
            nome_sinal="COMMUNITY_COVER_BIDDING",
            intensidade=0.85,
            peso=1.0,
            confianca=0.90
        ),
        AxisSignal(
            eixo="FRACIONAMENTO",
            nome_sinal="TETO_EXCEDIDO",
            intensidade=0.90,
            peso=1.0,
            confianca=1.0
        )
    ]

    result = engine.calculate_iea(
        contratacao_id="EDITAL_CARTEL_E_FRACIONAMENTO/2026",
        sinais=sinais_multieixo
    )

    assert result.valor_iea_final >= 60.0
    assert result.nivel_risco == "Elevado"
    assert result.truncado_por_salvaguarda is False
    assert result.qtd_eixos_independentes_ativos == 2

def test_iea_determinism_ca_ana_05():
    """
    Critério de Aceite CA-ANA-05 (Determinismo Estrito):
    Dados os mesmos insumos, a mesma versão de código e parâmetros,
    quando a análise é executada duas vezes,
    então o IEA, os níveis e a composição dos sinais são idênticos.
    """
    engine1 = IeaEngine(versao_parametros="v1.0.0")
    engine2 = IeaEngine(versao_parametros="v1.0.0")

    sinais = [
        AxisSignal(eixo="GRAFO", nome_sinal="COMMUNITY", intensidade=0.6, peso=1.0, confianca=0.8),
        AxisSignal(eixo="POPUP_VENDOR", nome_sinal="RECEM_CRIADA", intensidade=0.7, peso=0.7, confianca=1.0)
    ]

    res1 = engine1.calculate_iea("ED_DET_01", sinais)
    res2 = engine2.calculate_iea("ED_DET_01", sinais)

    assert res1.valor_iea_final == res2.valor_iea_final
    assert res1.nivel_risco == res2.nivel_risco
    assert res1.escore_aritmetico == res2.escore_aritmetico
    assert res1.decomposicao_sinais == res2.decomposicao_sinais

def test_iea_homonymy_safeguard_sg_05():
    """
    Salvaguarda SG-05:
    Sinais baseados apenas em homonímia não elevam o nível acima de 'Médio'.
    """
    engine = IeaEngine()

    sinais_homonimia = [
        AxisSignal(
            eixo="GRAFO",
            nome_sinal="HOMONIMIA_VINCULO",
            intensidade=0.95,
            peso=1.0,
            confianca=0.80,
            apenas_homonimia=True # Sinal baseado puramente em sobrenome
        ),
        AxisSignal(
            eixo="BENFORD",
            nome_sinal="BENFORD_ALERTA",
            intensidade=0.95,
            peso=0.8,
            confianca=1.0
        )
    ]

    res = engine.calculate_iea("ED_HOMONIMIA_01", sinais_homonimia)
    # Escore aritmético > 60, mas truncado para Médio pela regra SG-05
    assert res.escore_aritmetico >= 60.0
    assert res.nivel_risco == "Médio"
    assert res.truncado_por_salvaguarda is True
    assert "SG-05" in res.motivo_truncamento
