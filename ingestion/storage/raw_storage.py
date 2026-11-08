"""
NexusGov - Armazenamento de Payload Bruto Imutável com Rastreabilidade SHA-256
Requisito: RF-ING-02, RF-REL-03, RF-REL-04 (Critério de Aceite: CA-ING-02)
"""

from pathlib import Path
from typing import Any, Optional
import json
from ..models.payloads import RawEvidence

class RawStorageManager:
    """
    Gerencia a gravação e validação forense dos payloads brutos imutáveis.
    Organiza arquivos por: base_dir / competencia=YYYY-MM / uf=UF / {hash_sha256}.json
    """

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            # Padrão: data/raw relativo à raiz do repositório
            root = Path(__file__).resolve().parent.parent.parent
            self.base_dir = root / "data" / "raw"
        else:
            self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def store(
        self,
        identifier: str,
        url_fonte: str,
        competencia: str,
        content: Any,
        uf: str = "PB"
    ) -> RawEvidence:
        """
        Armazena o payload bruto com cálculo do hash SHA-256 e gravação imutável em disco.
        """
        evidence = RawEvidence.from_content(
            evidence_id=identifier,
            url_fonte=url_fonte,
            competencia_base=competencia,
            content=content
        )

        partition_dir = self.base_dir / f"competencia={competencia}" / f"uf={uf.upper()}"
        partition_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"{evidence.hash_sha256}.json"
        target_path = partition_dir / file_name

        evidence_metadata = {
            "id": evidence.id,
            "url_fonte": evidence.url_fonte,
            "coletado_em": evidence.coletado_em.isoformat(),
            "competencia_base": evidence.competencia_base,
            "hash_sha256": evidence.hash_sha256,
            "payload_bruto": evidence.payload_bruto
        }

        # Gravação atômica
        temp_path = partition_dir / f".tmp_{file_name}"
        temp_path.write_text(json.dumps(evidence_metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(target_path)

        evidence.caminho_storage = str(target_path.resolve())
        return evidence

    def load(self, target_path: Path) -> RawEvidence:
        """Carrega e desserializa uma evidência a partir do caminho do arquivo."""
        raw_text = Path(target_path).read_text(encoding="utf-8")
        data = json.loads(raw_text)
        return RawEvidence(**data)

    def verify_file(self, target_path: Path) -> bool:
        """
        Confere se o arquivo em disco sofreu qualquer adulteração desde a coleta.
        Garante CA-ING-02 e RF-REL-04.
        """
        if not target_path.exists():
            return False
        evidence = self.load(target_path)
        return evidence.verify_integrity()
