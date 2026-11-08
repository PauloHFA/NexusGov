"""
NexusGov - Resolução de Entidades Societárias e Confiança Ponderada
Requisitos: RF-ENT-03, RF-ENT-04, RF-ENT-05 (Critérios de Aceite: CA-ENT-01)
Salvaguarda: SG-05 (Proteção contra falsos positivos de homonímia)
"""

from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field
from .normalizer import EntityNormalizer

class ResolvedPartner(BaseModel):
    """Representação de sócio com confiança de identidade."""
    id: str
    nome_normalizado: str
    cpf_mascarado: str
    tipo_pessoa: str = "PF" # 'PF' ou 'PJ'
    confianca_identidade: float = Field(ge=0.0, le=1.0)
    rotulo_identidade: str = "identidade presumida"
    atributos_compartilhados: List[str] = Field(default_factory=list)


class CorporateChainLink(BaseModel):
    """Vínculo em cadeia societária multinível (RF-ENT-05)."""
    fornecedor_cnpj: str
    socio_pj_cnpj: str
    socio_final_id: str
    socio_final_nome: str
    profundidade: int
    confianca_acumulada: float


class EntityResolutionEngine:
    """Motor de resolução de entidades societárias e mitigação de homonímia."""

    # Sobrenomes de altíssima frequência demográfica no Brasil
    HIGH_FREQUENCY_SURNAMES: Set[str] = {
        "SILVA", "SANTOS", "OLIVEIRA", "SOUZA", "SOUSA", "RODRIGUES", "FERREIRA",
        "ALVES", "PEREIRA", "LIMA", "GOMES", "COSTA", "RIBEIRO", "MARTINS",
        "CARVALHO", "ALMEIDA", "LOPES", "SOARES", "FERNANDES", "VIEIRA",
        "BARBOSA", "ROCHA", "DIAS", "NASCIMENTO", "ANDRADE", "MOREIRA", "NUNES"
    }

    def __init__(self, base_confidence_pf: float = 0.80):
        self.base_confidence_pf = base_confidence_pf

    def resolve_partner_identity(
        self,
        nome: str,
        cpf_mascarado: str,
        shared_address: bool = False,
        shared_phone_or_email: bool = False
    ) -> ResolvedPartner:
        """
        Calcula a confiança de identidade do sócio mitigando riscos de homonímia (RF-ENT-03 / CA-ENT-01).
        A confiança nunca atinge 1.0 para PF com CPF mascarado, satisfazendo SG-05.
        """
        nome_norm = EntityNormalizer.normalize_name(nome, is_company=False)
        cpf_clean = (cpf_mascarado or "").strip()

        # Determina se possui sobrenome comum de alto ruído
        tokens = nome_norm.split()
        last_surname = tokens[-1] if tokens else ""
        is_common_surname = last_surname in self.HIGH_FREQUENCY_SURNAMES

        confidence = self.base_confidence_pf
        atributos: List[str] = ["NOME_CPF_MASCARADO"]

        # Fatores de acréscimo de confiança
        if shared_address:
            confidence += 0.10
            atributos.append("ENDERECO_COMPARTILHADO")
        if shared_phone_or_email:
            confidence += 0.08
            atributos.append("CONTATO_COMPARTILHADO")

        # Fator de penalização por homonímia
        if is_common_surname and not (shared_address or shared_phone_or_email):
            confidence -= 0.35
            atributos.append("SOBRENOME_ALTA_FREQUENCIA")

        # Confinamento no intervalo [0.05, 0.95] (PF mascarado nunca é 1.0)
        confidence = max(0.05, min(0.95, round(confidence, 3)))

        rotulo = "identidade presumida" if confidence < 1.0 else "identidade confirmada"
        partner_id = f"socio_{EntityNormalizer.strip_accents(nome_norm).replace(' ', '_')}_{cpf_clean.replace('*', 'X')}"

        return ResolvedPartner(
            id=partner_id,
            nome_normalizado=nome_norm,
            cpf_mascarado=cpf_clean,
            tipo_pessoa="PF",
            confianca_identidade=confidence,
            rotulo_identidade=rotulo,
            atributos_compartilhados=atributos
        )

    def resolve_corporate_chains(
        self,
        empresa_cnpj: str,
        socios_pj: List[Tuple[str, str]], # [(socio_pj_cnpj, socio_pj_nome), ...]
        pj_qsa_map: Dict[str, List[Tuple[str, str, str]]], # socio_pj_cnpj -> [(socio_id, nome, cpf_mascarado), ...]
        max_depth: int = 2
    ) -> List[CorporateChainLink]:
        """
        Expande cadeias societárias onde empresas são sócias de outras empresas (RF-ENT-05).
        """
        links: List[CorporateChainLink] = []

        for pj_cnpj, pj_nome in socios_pj:
            # 1º salto: PJ sócia direta
            beneficiarios = pj_qsa_map.get(pj_cnpj, [])
            for s_id, s_nome, s_cpf in beneficiarios:
                # Confiança diminui a cada salto indireto
                fator_decaimento = 0.85
                resolved = self.resolve_partner_identity(s_nome, s_cpf)
                confianca_final = round(resolved.confianca_identidade * fator_decaimento, 3)

                links.append(CorporateChainLink(
                    fornecedor_cnpj=empresa_cnpj,
                    socio_pj_cnpj=pj_cnpj,
                    socio_final_id=s_id,
                    socio_final_nome=s_nome,
                    profundidade=2,
                    confianca_acumulada=confianca_final
                ))

        return links
