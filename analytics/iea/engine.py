"""
NexusGov - Motor de Cálculo do Índice de Exposição a Anomalias (IEA)
Requisitos: RF-ANA-07, RF-CFG-01
Salvaguardas Invioláveis: SG-01, SG-02, SG-03, SG-04, SG-05
Critérios de Aceite: CA-ANA-05, CA-SG-02
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

AVISO_METODOLOGICO_PADRAO = (
    "Aviso Metodológico Obrigatório (SG-03): Os indicadores e pontuações do NexusGov constituem "
    "estritamente triagem estatística e priorização para análise por auditores humanos. "
    "A classificação de exposição não representa emissão de juízo de mérito, prova de irregularidade "
    "ou imputação de conduta, devendo ser interpretada sob o princípio da presunção de inocência."
)

class AxisSignal(BaseModel):
    """Sinal individual normalizado de um dos eixos analíticos."""
    eixo: str           # 'GRAFO', 'BENFORD', 'FRACIONAMENTO', 'POPUP_VENDOR'
    nome_sinal: str     # Ex: 'COMMUNITY_COVER_BIDDING', 'BENFORD_MAD_HIGH', 'SLIDING_WINDOW_EXCEEDED'
    intensidade: float = Field(ge=0.0, le=1.0) # s_i ∈ [0, 1]
    peso: float = Field(gt=0.0)                # w_i
    confianca: float = Field(ge=0.0, le=1.0)   # c_i ∈ [0, 1]
    apenas_homonimia: bool = False             # SG-05
    evidencias: Dict = Field(default_factory=dict)


class IeaComputationResult(BaseModel):
    """Resultado consolidado do IEA com decomposição completa de sinais."""
    contratacao_id: str
    versao_parametros: str
    escore_aritmetico: float = Field(ge=0.0, le=100.0)
    valor_iea_final: float = Field(ge=0.0, le=100.0)
    nivel_risco: str # 'Baixo', 'Médio', 'Elevado'
    truncado_por_salvaguarda: bool = False
    motivo_truncamento: Optional[str] = None
    qtd_eixos_independentes_ativos: int = 0
    decomposicao_sinais: List[AxisSignal]
    aviso_metodologico: str = AVISO_METODOLOGICO_PADRAO


class IeaEngine:
    """
    Motor oficial de cálculo do IEA com aplicação rigorosa das salvaguardas metodológicas.
    Fórmula: IEA = 100 * sum(w_i * s_i * c_i) / sum(w_i)
    """

    DEFAULT_PARAM_VERSION = "v1.0.0"

    # Pesos padrão recomendados pelo SRS (versão v1.0.0)
    DEFAULT_WEIGHTS: Dict[str, float] = {
        "GRAFO": 1.0,
        "BENFORD": 0.8,
        "FRACIONAMENTO": 1.0,
        "POPUP_VENDOR": 0.7
    }

    # Limiares de classificação de risco
    THRESHOLD_MEDIUM = 30.0
    THRESHOLD_HIGH = 60.0

    def __init__(
        self,
        versao_parametros: str = DEFAULT_PARAM_VERSION,
        pesos_customizados: Optional[Dict[str, float]] = None
    ):
        self.versao_parametros = versao_parametros
        self.weights = pesos_customizados or self.DEFAULT_WEIGHTS

    def calculate_iea(
        self,
        contratacao_id: str,
        sinais: List[AxisSignal]
    ) -> IeaComputationResult:
        """
        Calcula o IEA e aplica as salvaguardas invioláveis SG-04 e SG-05.
        Garante CA-ANA-05 (determinismo estrito) e CA-SG-02 (exigência de dois eixos para Elevado).
        """
        if not sinais:
            return IeaComputationResult(
                contratacao_id=contratacao_id,
                versao_parametros=self.versao_parametros,
                escore_aritmetico=0.0,
                valor_iea_final=0.0,
                nivel_risco="Baixo",
                decomposicao_sinais=[]
            )

        # 1. Cálculo da média ponderada dos sinais: sum(w_i * s_i * c_i) / sum(w_i)
        numerador = 0.0
        denominador = 0.0

        eixos_ativos: Dict[str, float] = {}
        homonimia_isolada = False

        for s in sinais:
            w = self.weights.get(s.eixo, s.peso)
            termo = w * s.intensidade * s.confianca
            numerador += termo
            denominador += w

            # Contabiliza eixo ativo se intensidade significativa (s >= 0.35)
            if s.intensidade >= 0.35:
                eixos_ativos[s.eixo] = max(eixos_ativos.get(s.eixo, 0.0), s.intensidade)

            if s.eixo == "GRAFO" and s.apenas_homonimia:
                homonimia_isolada = True

        escore_aritmetico = round((numerador / max(0.0001, denominador)) * 100.0, 2)
        escore_aritmetico = min(100.0, max(0.0, escore_aritmetico))

        # 2. Determinação preliminar do nível de risco
        if escore_aritmetico >= self.THRESHOLD_HIGH:
            nivel = "Elevado"
        elif escore_aritmetico >= self.THRESHOLD_MEDIUM:
            nivel = "Médio"
        else:
            nivel = "Baixo"

        truncado = False
        motivo_truncamento = None
        qtd_eixos_distintos = len(eixos_ativos)

        # 3. Aplicação da Salvaguarda Inviolável SG-04:
        # Nível "Elevado" EXIGE ao menos dois sinais independentes de eixos distintos (CA-SG-02)
        if nivel == "Elevado" and qtd_eixos_distintos < 2:
            nivel = "Médio"
            truncado = True
            motivo_truncamento = (
                "Salvaguarda SG-04 aplicada: classificação rebaixada para 'Médio' pois "
                "o escore elevado decorre de apenas 1 eixo analítico isolado."
            )

        # 4. Aplicação da Salvaguarda Inviolável SG-05:
        # Sinais baseados apenas em homonímia não podem elevar o nível acima de "Médio"
        if nivel == "Elevado" and homonimia_isolada and qtd_eixos_distintos < 3:
            nivel = "Médio"
            truncado = True
            motivo_truncamento = (
                "Salvaguarda SG-05 aplicada: classificação limitada a 'Médio' pois "
                "o vínculo societário fundamenta-se exclusivamente em homonímia/sobrenome presumido."
            )

        return IeaComputationResult(
            contratacao_id=contratacao_id,
            versao_parametros=self.versao_parametros,
            escore_aritmetico=escore_aritmetico,
            valor_iea_final=escore_aritmetico,
            nivel_risco=nivel,
            truncado_por_salvaguarda=truncado,
            motivo_truncamento=motivo_truncamento,
            qtd_eixos_independentes_ativos=qtd_eixos_distintos,
            decomposicao_sinais=sinais
        )
