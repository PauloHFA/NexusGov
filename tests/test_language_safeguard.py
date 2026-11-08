"""
Testes automatizados para a Salvaguarda Metodológica SG-01 (Linguagem Neutra)
Garante conformidade com o Artigo 19-B da Resolução TCU nº 367/2024.
"""

from pathlib import Path
from spec.check_language_safeguard import check_language


def test_sg01_language_safeguard_compliance():
    root = Path(__file__).resolve().parent.parent
    assert check_language(root) is True
