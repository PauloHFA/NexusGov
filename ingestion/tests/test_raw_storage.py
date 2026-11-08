"""
NexusGov - Testes de Armazenamento Forense Imutável (RF-ING-02, CA-ING-02, RF-REL-04)
"""

import json
from pathlib import Path
import pytest
from ingestion.storage.raw_storage import RawStorageManager

def test_raw_evidence_sha256_generation_and_storage(tmp_path: Path):
    manager = RawStorageManager(base_dir=tmp_path)
    sample_payload = {
        "numeroControlePNCP": "00000000000191-1-000001/2026",
        "objeto": "Aquisição de computadores para o município de João Pessoa",
        "valor": 150000.00
    }

    evidence = manager.store(
        identifier="TEST_ED_01",
        url_fonte="https://pncp.gov.br/api/consulta/v1/contratacoes/TEST_ED_01",
        competencia="2026-09",
        content=sample_payload,
        uf="PB"
    )

    assert evidence.hash_sha256 is not None
    assert len(evidence.hash_sha256) == 64
    assert evidence.caminho_storage is not None
    assert Path(evidence.caminho_storage).exists()

    # Verifica integridade
    assert manager.verify_file(Path(evidence.caminho_storage)) is True

def test_raw_evidence_tamper_detection(tmp_path: Path):
    """
    Critério de Aceite CA-ING-02:
    Qualquer alteração posterior do payload invalida a verificação forense.
    """
    manager = RawStorageManager(base_dir=tmp_path)
    sample_payload = {"valor": 50000.00, "status": "HOMOLOGADO"}

    evidence = manager.store(
        identifier="TEST_TAMPER_01",
        url_fonte="https://pncp.gov.br/test",
        competencia="2026-09",
        content=sample_payload,
        uf="PB"
    )

    file_path = Path(evidence.caminho_storage)
    assert manager.verify_file(file_path) is True

    # Adulteração maliciosa simulada no arquivo
    file_content = json.loads(file_path.read_text(encoding="utf-8"))
    # Altera um caractere no payload_bruto
    file_content["payload_bruto"] = file_content["payload_bruto"].replace("50000", "99999")
    file_path.write_text(json.dumps(file_content), encoding="utf-8")

    # A verificação DEVE falhar imediatamente
    assert manager.verify_file(file_path) is False
