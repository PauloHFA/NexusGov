"""
NexusGov - Modelos de Dados de Ingestão e Evidência Forense
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import hashlib
import json

class RawEvidence(BaseModel):
    """
    Representação de uma evidência bruta coletada (RF-ING-02 / RF-REL-03).
    Garante integridade e cadeia de custódia com hash SHA-256 e timestamp UTC.
    """
    id: str
    url_fonte: str
    coletado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    competencia_base: str # YYYY-MM
    hash_sha256: str
    payload_bruto: str # JSON serializado canônico ou texto bruto
    caminho_storage: Optional[str] = None

    @classmethod
    def from_content(
        cls,
        evidence_id: str,
        url_fonte: str,
        competencia_base: str,
        content: Any,
        caminho_storage: Optional[str] = None
    ) -> "RawEvidence":
        if isinstance(content, (dict, list)):
            serialized = json.dumps(content, ensure_ascii=False, sort_keys=True)
        elif isinstance(content, bytes):
            serialized = content.decode("utf-8", errors="replace")
        else:
            serialized = str(content)

        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        return cls(
            id=evidence_id,
            url_fonte=url_fonte,
            competencia_base=competencia_base,
            hash_sha256=digest,
            payload_bruto=serialized,
            caminho_storage=caminho_storage
        )

    def verify_integrity(self) -> bool:
        """Verifica se o payload atual confere exatamente com o hash SHA-256 armazenado."""
        calculated = hashlib.sha256(self.payload_bruto.encode("utf-8")).hexdigest()
        return calculated == self.hash_sha256


class PncpItem(BaseModel):
    """Item de contratação no PNCP."""
    numero_item: int
    descricao: str
    codigo_catmat_catser: Optional[str] = None
    quantidade: float = 1.0
    unidade_medida: Optional[str] = None
    valor_unitario_estimado: Optional[float] = None
    valor_unitario_homologado: Optional[float] = None
    valor_total: Optional[float] = None
    situacao: Optional[str] = None


class PncpContratacao(BaseModel):
    """Contratação / Edital coletado do PNCP."""
    numero_controle_pncp: str
    orgao_cnpj: str
    orgao_nome: str
    esfera: str = "MUNICIPAL" # MUNICIPAL, ESTADUAL, FEDERAL
    poder: str = "EXECUTIVO"  # EXECUTIVO, LEGISLATIVO, JUDICIARIO
    uf: str                   # ex: 'PB'
    codigo_ibge_municipio: Optional[str] = None
    modalidade_nome: str
    numero_edital: Optional[str] = None
    ano_compra: int
    objeto: str
    valor_total_estimado: Optional[float] = None
    valor_total_homologado: Optional[float] = None
    data_abertura_proposta: Optional[datetime] = None
    data_homologacao: Optional[datetime] = None
    situacao: Optional[str] = None
    url_pncp: Optional[str] = None
    itens: List[PncpItem] = Field(default_factory=list)


class IngestionQualityReport(BaseModel):
    """Relatório de qualidade da carga (RF-ING-08)."""
    lote_id: str
    origem: str # 'PNCP', 'RECEITA_FEDERAL', 'IBGE'
    competencia: str
    uf: str
    total_lidos: int = 0
    total_aceitos: int = 0
    total_rejeitados: int = 0
    total_duplicados_ignorados: int = 0
    tempo_execucao_segundos: float = 0.0
    checksum_arquivos: Dict[str, str] = Field(default_factory=dict)
    erros: List[str] = Field(default_factory=list)
    finalizado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
