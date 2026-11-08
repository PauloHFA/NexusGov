"""
NexusGov - Cruzamento com Preços de Referência e Detecção de Sobrepreço Relativo (RF-ANA-10)
Critério de Aceite: CA-ANA-10
Compara valor unitário adjudicado com a mediana regional de bancos de preços de referência.
"""

from typing import Dict, List, Optional
import numpy as np
from pydantic import BaseModel, Field


class ItemPriceFinding(BaseModel):
    item_id: str
    codigo_catmat: str
    descricao: str
    valor_unitario_adjudicado: float
    preco_mediano_referencia: float
    desvio_percentual_mediana: float
    sinal_sobrepreco_relativo: bool
    escore_sinal: float = Field(ge=0.0, le=1.0)


class ReferencePriceAnalyzer:
    """
    Analisa itens adjudicados frente a preços medianos regionais por código CATMAT.
    """

    def __init__(self, limiar_alerta_pct: float = 50.0):
        # Limiar de desvio relativo (padrão 50% acima da mediana per CA-ANA-10)
        self.limiar_alerta_pct = limiar_alerta_pct

    def analyze_item_price(
        self,
        item_id: str,
        codigo_catmat: str,
        descricao: str,
        valor_unitario: float,
        historico_precos_referencia: List[float]
    ) -> ItemPriceFinding:
        """
        Executa o cruzamento estatístico e sinaliza desvios > 50% sobre a mediana regional.
        """
        if not historico_precos_referencia or len(historico_precos_referencia) == 0:
            mediana = valor_unitario
        else:
            mediana = float(np.median(historico_precos_referencia))

        if mediana > 0:
            desvio_pct = ((valor_unitario - mediana) / mediana) * 100.0
        else:
            desvio_pct = 0.0

        sinal = desvio_pct > self.limiar_alerta_pct

        if desvio_pct <= 0:
            escore = 0.0
        elif desvio_pct >= 100.0:
            escore = 1.0
        else:
            escore = round(desvio_pct / 100.0, 3)

        return ItemPriceFinding(
            item_id=item_id,
            codigo_catmat=codigo_catmat,
            descricao=descricao,
            valor_unitario_adjudicado=valor_unitario,
            preco_mediano_referencia=mediana,
            desvio_percentual_mediana=round(desvio_pct, 2),
            sinal_sobrepreco_relativo=sinal,
            escore_sinal=escore
        )
