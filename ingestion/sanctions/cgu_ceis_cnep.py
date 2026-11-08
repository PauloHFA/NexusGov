"""
NexusGov - Importador e Estruturador de Sanções e Vedações Federais (Melhoria 2)
Fontes Públicas Oficiais:
- CEIS: Cadastro Nacional de Empresas Inidôneas e Suspensas (CGU)
- CNEP: Cadastro Nacional de Empresas Punidas (Lei Anticorrupção nº 12.846/2013)
- CEPIM: Cadastro de Entidades Privadas Sem Fins Lucrativos Impedidas
- TCU: Relação de Responsáveis com Contas Julgadas Irregulares / Inidôneos
"""

from datetime import date
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from analytics.graph.normalizer import EntityNormalizer


class SanctionType(str, Enum):
    CEIS = "CEIS"
    CNEP = "CNEP"
    CEPIM = "CEPIM"
    TCU_INIDONEO = "TCU_INIDONEO"


class SanctionEntry(BaseModel):
    """Registro individual de sanção ou impedimento de licitar."""
    id_sancao: str
    tipo_cadastro: SanctionType
    cnpj_cpf_sancionado: str
    nome_razao_social: str
    orgao_sancionador: str
    fundamentacao_legal: str
    data_inicio_sancao: date
    data_fim_sancao: Optional[date] = None # None = vigência indeterminada ou até cumprimento
    ativo: bool = True

    def is_active_on(self, target_date: date) -> bool:
        if target_date < self.data_inicio_sancao:
            return False
        if self.data_fim_sancao is not None and target_date > self.data_fim_sancao:
            return False
        return self.ativo


class SanctionCatalog:
    """Catálogo indexado de sanções para consulta de alta performance."""

    def __init__(self):
        self._by_document: Dict[str, List[SanctionEntry]] = {}

    def add_entry(self, entry: SanctionEntry) -> None:
        clean_doc = EntityNormalizer.validate_and_clean_cnpj(entry.cnpj_cpf_sancionado)[1] if len(entry.cnpj_cpf_sancionado.replace(".", "").replace("/", "").replace("-", "")) == 14 else entry.cnpj_cpf_sancionado.strip()
        if clean_doc not in self._by_document:
            self._by_document[clean_doc] = []
        self._by_document[clean_doc].append(entry)

    def find_active_sanctions(self, cnpj_or_cpf: str, reference_date: date) -> List[SanctionEntry]:
        clean_doc = EntityNormalizer.validate_and_clean_cnpj(cnpj_or_cpf)[1] if len(cnpj_or_cpf.replace(".", "").replace("/", "").replace("-", "")) == 14 else cnpj_or_cpf.strip()
        entries = self._by_document.get(clean_doc, [])
        return [e for e in entries if e.is_active_on(reference_date)]

    @property
    def total_entries(self) -> int:
        return sum(len(v) for v in self._by_document.values())
