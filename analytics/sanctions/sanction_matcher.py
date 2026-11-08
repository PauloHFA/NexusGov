"""
NexusGov - Motor de Cruzamento com Bases de Sanções e Vedações (Melhoria 2)
Verifica impedimentos diretos (CNPJ) e indiretos (Sócios e Coligadas sancionadas).
Salvaguarda SG-01: Linguagem neutra e indiciária, fundamentada em certidões públicas.
"""

from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from ingestion.sanctions.cgu_ceis_cnep import SanctionCatalog, SanctionEntry
from analytics.iea.engine import AxisSignal


class SanctionEvaluationFinding(BaseModel):
    """Achado de conformidade cadastral quanto a sanções administrativas ou judiciais."""
    fornecedor_cnpj: str
    razao_social: str
    tem_impedimento_direto: bool = False
    tem_impedimento_indireto_socio: bool = False
    sancoes_diretas: List[SanctionEntry] = Field(default_factory=list)
    sancoes_indiretas_socios: List[Dict] = Field(default_factory=list)
    escore_sinal: float = Field(ge=0.0, le=1.0)
    descricao_indicio: str


class SanctionMatcher:
    """
    Cruza fornecedores e quadro de sócios (QSA) com o catálogo de sanções CEIS, CNEP, CEPIM e TCU.
    """

    def __init__(self, catalog: SanctionCatalog):
        self.catalog = catalog

    def evaluate_supplier(
        self,
        cnpj: str,
        razao_social: str,
        socios: List[Dict[str, str]], # Lista de dicts com 'cpf_cnpj' e 'nome'
        data_referencia: date
    ) -> SanctionEvaluationFinding:
        """
        Avalia o fornecedor quanto a sanções vigentes diretas e indiretas (societárias).
        """
        # 1. Verificação Direta da Pessoa Jurídica
        sancoes_diretas = self.catalog.find_active_sanctions(cnpj, data_referencia)
        tem_direto = len(sancoes_diretas) > 0

        # 2. Verificação Indireta via Sócios / Administradores
        sancoes_indiretas = []
        for socio in socios:
            socio_doc = socio.get("cpf_cnpj", "")
            if socio_doc:
                s_ativas = self.catalog.find_active_sanctions(socio_doc, data_referencia)
                if s_ativas:
                    sancoes_indiretas.append({
                        "socio_nome": socio.get("nome", ""),
                        "socio_doc": socio_doc,
                        "sancoes": s_ativas
                    })

        tem_indireto = len(sancoes_indiretas) > 0

        # Cálculo do escore indiciário
        if tem_direto:
            escore = 1.00 # Impedimento direto vigente
            desc = f"Identificado registro de impedimento vigente no cadastro oficial ({sancoes_diretas[0].tipo_cadastro.value}) para o CNPJ."
        elif tem_indireto:
            escore = 0.75 # Sócio possui sanção em nome próprio ou coligada
            desc = "Identificado sócio ou administrador com registro de sanção vigente em bases públicas oficiais."
        else:
            escore = 0.00
            desc = "Nenhum registro de sanção ativa localizado para a pessoa jurídica ou seu quadro societário."

        return SanctionEvaluationFinding(
            fornecedor_cnpj=cnpj,
            razao_social=razao_social,
            tem_impedimento_direto=tem_direto,
            tem_impedimento_indireto_socio=tem_indireto,
            sancoes_diretas=sancoes_diretas,
            sancoes_indiretas_socios=sancoes_indiretas,
            escore_sinal=escore,
            descricao_indicio=desc
        )

    def to_axis_signal(self, finding: SanctionEvaluationFinding) -> Optional[AxisSignal]:
        """Converte o achado de sanção em um sinal de eixo para o motor IEA."""
        if finding.escore_sinal == 0:
            return None

        nome_sinal = "SANCTION_DIRECT_MATCH" if finding.tem_impedimento_direto else "SANCTION_INDIRECT_PARTNER_MATCH"
        return AxisSignal(
            eixo="SANCOES",
            nome_sinal=nome_sinal,
            intensidade=finding.escore_sinal,
            peso=1.2, # Peso relevante para vedações legais
            confianca=1.00 if finding.tem_impedimento_direto else 0.85,
            apenas_homonimia=False,
            evidencias={"descricao": finding.descricao_indicio}
        )
