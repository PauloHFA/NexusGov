"""
NexusGov - Detecção de Empresas Recém-Criadas (Pop-up Vendors) (RF-ANA-06)
Metodologia: Seção 4.4 do SRS (Idade do CNPJ, Razão Valor/Capital, Distância Geográfica e CNAE)
"""

from datetime import date
from typing import Dict, Optional
from pydantic import BaseModel, Field
from ingestion.ibge.municipios import IbgeService

class PopupVendorFinding(BaseModel):
    """Achado de empresa recém-criada com incompatibilidade operacional."""
    fornecedor_cnpj: str
    razao_social: str
    data_abertura_cnpj: date
    data_abertura_certame: date
    idade_dias_na_licitacao: int
    capital_social: float
    valor_adjudicado: float
    razao_valor_capital: float
    distancia_sede_orgao_km: Optional[float] = None
    escore_sinal: float = Field(ge=0.0, le=1.0)
    detalhes_sinais: Dict[str, float] = Field(default_factory=dict)


class PopupVendorDetector:
    """
    Detector de empresas recém-nascidas (pop-up vendors) vencedoras de certames vultosos.
    """

    def __init__(self, ibge_service: Optional[IbgeService] = None):
        self.ibge = ibge_service or IbgeService()

    def evaluate_vendor(
        self,
        cnpj: str,
        razao_social: str,
        data_abertura_cnpj: date,
        data_certame: date,
        capital_social: float,
        valor_adjudicado: float,
        municipio_fornecedor_ibge: Optional[str] = None,
        municipio_orgao_ibge: Optional[str] = None
    ) -> PopupVendorFinding:
        """
        Calcula o escore de exposição do eixo de empresas recém-criadas.
        """
        # 1. Idade do CNPJ na data de abertura do certame (em dias)
        delta_dias = (data_certame - data_abertura_cnpj).days
        idade_dias = max(0, delta_dias)

        # Sinal por idade: quanto mais nova a empresa, maior a exposição
        if idade_dias <= 30:
            sinal_idade = 1.00
        elif idade_dias <= 90:
            sinal_idade = 0.80
        elif idade_dias <= 180:
            sinal_idade = 0.50
        elif idade_dias <= 365:
            sinal_idade = 0.25
        else:
            sinal_idade = 0.00

        # 2. Razão entre valor adjudicado e capital social
        cap_safe = max(100.0, capital_social)
        razao_valor_cap = valor_adjudicado / cap_safe

        if razao_valor_cap >= 100.0:
            sinal_capital = 1.00
        elif razao_valor_cap >= 50.0:
            sinal_capital = 0.80
        elif razao_valor_cap >= 20.0:
            sinal_capital = 0.50
        elif razao_valor_cap >= 10.0:
            sinal_capital = 0.25
        else:
            sinal_capital = 0.00

        # 3. Distância geográfica entre fornecedor e órgão
        distancia_km: Optional[float] = None
        sinal_distancia = 0.0

        if municipio_fornecedor_ibge and municipio_orgao_ibge:
            m_forn = self.ibge.get_by_code(municipio_fornecedor_ibge)
            m_org = self.ibge.get_by_code(municipio_orgao_ibge)
            if m_forn and m_org:
                distancia_km = self.ibge.haversine_distance_km(
                    m_forn.latitude, m_forn.longitude,
                    m_org.latitude, m_org.longitude
                )
                # Distância muito elevada para prestação de serviços locais
                if distancia_km >= 1500.0:
                    sinal_distancia = 0.80
                elif distancia_km >= 800.0:
                    sinal_distancia = 0.50
                elif distancia_km >= 400.0:
                    sinal_distancia = 0.20

        # Composição ponderada do sinal deste eixo
        # Pesos: Idade (0.45), Razão Capital (0.40), Distância (0.15)
        peso_idade = 0.45
        peso_cap = 0.40
        peso_dist = 0.15

        escore_eixo = (
            sinal_idade * peso_idade +
            sinal_capital * peso_cap +
            sinal_distancia * peso_dist
        )
        escore_eixo = min(1.0, max(0.0, round(escore_eixo, 3)))

        return PopupVendorFinding(
            fornecedor_cnpj=cnpj,
            razao_social=razao_social,
            data_abertura_cnpj=data_abertura_cnpj,
            data_abertura_certame=data_certame,
            idade_dias_na_licitacao=idade_dias,
            capital_social=capital_social,
            valor_adjudicado=valor_adjudicado,
            razao_valor_capital=round(razao_valor_cap, 2),
            distancia_sede_orgao_km=round(distancia_km, 1) if distancia_km is not None else None,
            escore_sinal=escore_eixo,
            detalhes_sinais={
                "sinal_idade": round(sinal_idade, 2),
                "sinal_capital": round(sinal_capital, 2),
                "sinal_distancia": round(sinal_distancia, 2)
            }
        )
