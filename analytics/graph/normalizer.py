"""
NexusGov - Normalizador Canônico de CNPJ, Nomes, Endereços e Contatos
Requisitos: RF-ENT-01, RF-ENT-02 (Critérios de Aceite: CA-ENT-01-A, CA-ENT-02)
"""

import re
import unicodedata
from typing import Optional, Tuple

class EntityNormalizer:
    """Normaliza atributos cadastrais para resolução de entidades e construção de grafos."""

    CORPORATE_SUFFIXES = [
        r"\bLTDA\b", r"\bLIMITADA\b",
        r"\bME\b", r"\bMICROEMPRESA\b",
        r"\bEPP\b", r"\bEMPRESA DE PEQUENO PORTE\b",
        r"\bEIRELI\b",
        r"\bS/?A\b", r"\bSOCIEDADE ANONIMA\b",
        r"\bS/?S\b", r"\bSOCIEDADE SIMPLES\b",
        r"\bCIA\b", r"\bCOMPANHIA\b",
        r"\bSOCIEDADE UNIPESSOAL\b"
    ]

    STREET_PREFIXES = {
        r"\bAVENIDA\b": "AV",
        r"\bAV\.\b": "AV",
        r"\bRUA\b": "RUA",
        r"\bR\.\b": "RUA",
        r"\bTRAVESSA\b": "TRAV",
        r"\bTRAV\.\b": "TRAV",
        r"\bPRACA\b": "PRACA",
        r"\bP[CÇ]\.\b": "PRACA",
        r"\bALAMEDA\b": "AL",
        r"\bAL\.\b": "AL",
        r"\bRODOVIA\b": "ROD",
        r"\bROD\.\b": "ROD"
    }

    @staticmethod
    def strip_accents(text: str) -> str:
        """Remove diacríticos e acentos via decomposição NFKD."""
        if not text:
            return ""
        nfkd = unicodedata.normalize("NFKD", text)
        return "".join([c for c in nfkd if not unicodedata.combining(c)])

    @classmethod
    def validate_and_clean_cnpj(cls, raw_cnpj: str) -> Tuple[bool, str]:
        """
        Valida e normaliza CNPJ para 14 dígitos usando o algoritmo Módulo 11 (RF-ENT-01).
        Retorna (is_valid, cleaned_cnpj).
        """
        digits = re.sub(r"\D", "", raw_cnpj or "")
        if len(digits) != 14:
            return False, digits

        # CNPJs com todos os dígitos repetidos são inválidos
        if len(set(digits)) == 1:
            return False, digits

        # Validação do primeiro dígito verificador
        weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma1 = sum(int(digits[i]) * weights1[i] for i in range(12))
        resto1 = soma1 % 11
        dv1 = 0 if resto1 < 2 else 11 - resto1
        if int(digits[12]) != dv1:
            return False, digits

        # Validação do segundo dígito verificador
        weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma2 = sum(int(digits[i]) * weights2[i] for i in range(13))
        resto2 = soma2 % 11
        dv2 = 0 if resto2 < 2 else 11 - resto2
        if int(digits[13]) != dv2:
            return False, digits

        return True, digits

    @classmethod
    def normalize_name(cls, name: str, is_company: bool = False) -> str:
        """
        Normaliza nomes de pessoas físicas ou empresariais:
        Remove acentos, converte para maiúsculas, limpa partículas societárias e pontuações.
        """
        if not name:
            return ""

        text = cls.strip_accents(name).upper().strip()

        if is_company:
            for pattern in cls.CORPORATE_SUFFIXES:
                text = re.sub(pattern, " ", text)

        # Remove pontuações e caracteres não alfanuméricos exceto espaços
        text = re.sub(r"[^A-Z0-9\s]", " ", text)
        # Normaliza múltiplos espaços
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @classmethod
    def normalize_address(
        cls,
        logradouro: str,
        numero: str,
        cep: str,
        bairro: Optional[str] = None
    ) -> str:
        """
        Gera chave canônica de endereço (RF-ENT-02).
        Ex: "AV EPITACIO PESSOA|100|58000000"
        """
        log_clean = cls.strip_accents(logradouro or "").upper().strip()
        for pattern, repl in cls.STREET_PREFIXES.items():
            log_clean = re.sub(pattern, repl, log_clean)

        log_clean = re.sub(r"[^A-Z0-9\s]", " ", log_clean)
        log_clean = re.sub(r"\s+", " ", log_clean).strip()

        # Extrai o número predial principal antes do complemento (ex: "100 - Sala 10" -> "100")
        num_raw = cls.strip_accents(numero or "").strip().upper()
        letters_only = re.sub(r"[^A-Z]", "", num_raw)
        if not num_raw or letters_only in ("SN", "S", "SEM", "SEMNUMERO"):
            num_clean = "SN"
        else:
            tokens = re.split(r"[\s,\-/]", num_raw)
            num_clean = re.sub(r"[^A-Z0-9]", "", tokens[0] if tokens else "")
            if not num_clean:
                num_clean = "SN"

        cep_clean = re.sub(r"\D", "", cep or "")
        return f"{log_clean}|{num_clean}|{cep_clean}"

    @classmethod
    def normalize_phone(cls, ddd: Optional[str], phone: Optional[str]) -> str:
        """Normaliza telefone para formato numérico canônico: DDD + Número (RF-ENT-02)."""
        ddd_clean = re.sub(r"\D", "", ddd or "")
        phone_clean = re.sub(r"\D", "", phone or "")

        # Remove eventual zero à esquerda do DDD
        if ddd_clean.startswith("0") and len(ddd_clean) > 2:
            ddd_clean = ddd_clean[1:]

        if not phone_clean:
            return ""

        return f"{ddd_clean}{phone_clean}"

    @classmethod
    def normalize_email(cls, email: Optional[str]) -> str:
        """Normaliza e-mail para comparação."""
        if not email:
            return ""
        return email.strip().lower()
