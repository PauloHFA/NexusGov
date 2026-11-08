"""
NexusGov - Detecção de Fracionamento de Despesa em Janelas Deslizantes Temporais (RF-ANA-05)
Consulta de Tetos Legais por Vigência Temporal: RF-CFG-02
Critérios de Aceite: CA-ANA-03, CA-ANA-04
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class LegalThresholdRule(BaseModel):
    """Regra de teto legal com vigência temporal (RF-CFG-02 / CA-ANA-04)."""
    modalidade_objeto: str # 'DISPENSA_COMPRAS_SERVICOS' ou 'DISPENSA_OBRAS_ENGENHARIA'
    valor_limite: float
    data_inicio: date
    data_fim: Optional[date] = None # None = vigência aberta
    base_legal: str

    def is_effective_on(self, target_date: date) -> bool:
        if target_date < self.data_inicio:
            return False
        if self.data_fim is not None and target_date > self.data_fim:
            return False
        return True


# Tabela padrão de tetos legais da Nova Lei de Licitações (Lei 14.133/2021 e Decretos Federais)
DEFAULT_LEGAL_THRESHOLDS: List[LegalThresholdRule] = [
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_COMPRAS_SERVICOS",
        valor_limite=50000.00,
        data_inicio=date(2021, 4, 1),
        data_fim=date(2021, 12, 31),
        base_legal="Lei 14.133/2021 Art. 75, II (valor original)"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_OBRAS_ENGENHARIA",
        valor_limite=100000.00,
        data_inicio=date(2021, 4, 1),
        data_fim=date(2021, 12, 31),
        base_legal="Lei 14.133/2021 Art. 75, I (valor original)"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_COMPRAS_SERVICOS",
        valor_limite=54020.41,
        data_inicio=date(2022, 1, 1),
        data_fim=date(2022, 12, 31),
        base_legal="Decreto Federal nº 10.922/2021"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_OBRAS_ENGENHARIA",
        valor_limite=108040.82,
        data_inicio=date(2022, 1, 1),
        data_fim=date(2022, 12, 31),
        base_legal="Decreto Federal nº 10.922/2021"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_COMPRAS_SERVICOS",
        valor_limite=57209.60,
        data_inicio=date(2023, 1, 1),
        data_fim=date(2023, 12, 31),
        base_legal="Decreto Federal nº 11.317/2022"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_OBRAS_ENGENHARIA",
        valor_limite=114416.65,
        data_inicio=date(2023, 1, 1),
        data_fim=date(2023, 12, 31),
        base_legal="Decreto Federal nº 11.317/2022"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_COMPRAS_SERVICOS",
        valor_limite=59906.02,
        data_inicio=date(2024, 1, 1),
        data_fim=None,
        base_legal="Decreto Federal nº 11.871/2023"
    ),
    LegalThresholdRule(
        modalidade_objeto="DISPENSA_OBRAS_ENGENHARIA",
        valor_limite=119812.02,
        data_inicio=date(2024, 1, 1),
        data_fim=None,
        base_legal="Decreto Federal nº 11.871/2023"
    )
]


class ContractPurchaseEntry(BaseModel):
    """Representação de uma compra direta para análise temporal."""
    id: str
    numero_controle_pncp: str
    orgao_id: str
    fornecedor_cnpj: str
    data_contratacao: date
    valor: float
    codigo_catmat: Optional[str] = None
    objeto_descricao: str = ""
    modalidade_objeto: str = "DISPENSA_COMPRAS_SERVICOS"


class SplitWindowFinding(BaseModel):
    """Achado de suspeita de fracionamento de despesa em janela deslizante."""
    orgao_id: str
    fornecedor_cnpj: str
    codigo_catmat: Optional[str]
    tamanho_janela_dias: int
    data_inicio_janela: date
    data_fim_janela: date
    total_contratacoes: int
    soma_valores: float
    teto_legal_vigente: float
    razao_soma_teto: float
    motivo_sinalizacao: str # 'TETO_EXCEDIDO' ou 'REPETICAO_PROXIMA_AO_TETO'
    contratacoes_ids: List[str]
    escore_sinal: float = Field(ge=0.0, le=1.0)


class SplitPurchaseDetector:
    """
    Detector de fracionamento de despesa por janelas deslizantes (30, 60 e 90 dias)
    com consulta determinística a tetos legais vigentes.
    """

    def __init__(
        self,
        threshold_rules: Optional[List[LegalThresholdRule]] = None,
        sliding_windows_days: Tuple[int, ...] = (30, 60, 90),
        k_min_near_limit: int = 3,
        near_limit_ratio: float = 0.80
    ):
        self.threshold_rules = threshold_rules or DEFAULT_LEGAL_THRESHOLDS
        self.windows = sliding_windows_days
        self.k_min = k_min_near_limit
        self.near_limit_ratio = near_limit_ratio

    def get_threshold_for(self, target_date: date, modalidade_objeto: str = "DISPENSA_COMPRAS_SERVICOS") -> float:
        """
        Retorna o teto legal estritamente vigente na data informada (RF-CFG-02 / CA-ANA-04).
        """
        for rule in self.threshold_rules:
            if rule.modalidade_objeto == modalidade_objeto and rule.is_effective_on(target_date):
                return rule.valor_limite
        # Fallback conservador para valor base
        return 50000.00 if "OBRAS" not in modalidade_objeto else 100000.00

    def detect_split_purchases(
        self,
        purchases: List[ContractPurchaseEntry]
    ) -> List[SplitWindowFinding]:
        """
        Agrupa compras por (orgao_id, fornecedor_cnpj, codigo_catmat) e analisa janelas temporais.
        Garante CA-ANA-03: sinaliza janela quando a soma excede o teto ou há >= k compras a 80-100% do teto.
        """
        findings: List[SplitWindowFinding] = []

        # Agrupamento
        groups: Dict[Tuple[str, str, Optional[str]], List[ContractPurchaseEntry]] = {}
        for p in purchases:
            key = (p.orgao_id, p.fornecedor_cnpj, p.codigo_catmat)
            groups.setdefault(key, []).append(p)

        for (orgao, fornecedor, catmat), items in groups.items():
            if len(items) < 2:
                continue

            # Ordena temporalmente
            sorted_items = sorted(items, key=lambda x: x.data_contratacao)

            for win_days in self.windows:
                delta = timedelta(days=win_days)

                for i, start_item in enumerate(sorted_items):
                    win_start = start_item.data_contratacao
                    win_end = win_start + delta

                    # Coleta compras dentro da janela deslizante
                    in_window = [p for p in sorted_items if win_start <= p.data_contratacao <= win_end]
                    if len(in_window) < 2:
                        continue

                    soma_val = sum(p.valor for p in in_window)
                    # Usa o teto da modalidade vigente na data média da janela
                    teto_vigente = self.get_threshold_for(win_start, in_window[0].modalidade_objeto)

                    motivo = None
                    escore = 0.0

                    # Condição 1: soma dos valores excede o teto legal da modalidade na data
                    if soma_val > teto_vigente:
                        motivo = "TETO_EXCEDIDO"
                        excesso_ratio = (soma_val - teto_vigente) / teto_vigente
                        escore = min(1.0, 0.60 + excesso_ratio * 0.40)

                    # Condição 2: >= k compras cada uma entre 80% e 100% do teto
                    compras_quase_teto = [
                        p for p in in_window
                        if (self.near_limit_ratio * teto_vigente) <= p.valor <= teto_vigente
                    ]
                    if len(compras_quase_teto) >= self.k_min:
                        motivo = "REPETICAO_PROXIMA_AO_TETO"
                        escore = max(escore, 0.85)

                    if motivo:
                        finding = SplitWindowFinding(
                            orgao_id=orgao,
                            fornecedor_cnpj=fornecedor,
                            codigo_catmat=catmat,
                            tamanho_janela_dias=win_days,
                            data_inicio_janela=win_start,
                            data_fim_janela=in_window[-1].data_contratacao,
                            total_contratacoes=len(in_window),
                            soma_valores=round(soma_val, 2),
                            teto_legal_vigente=teto_vigente,
                            razao_soma_teto=round(soma_val / teto_vigente, 3),
                            motivo_sinalizacao=motivo,
                            contratacoes_ids=[p.numero_controle_pncp for p in in_window],
                            escore_sinal=round(escore, 3)
                        )
                        findings.append(finding)
                        # Avança para evitar duplicações excessivas da mesma janela
                        break

        return findings
