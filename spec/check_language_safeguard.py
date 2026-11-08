"""
NexusGov - Validador da Salvaguarda Metodológica SG-01 (Linguagem Neutra)
Garante que termos acusatórios ou ilícitos não constem no código de produção,
templates de relatórios, documentações de API ou telas.
"""

import sys
import re
from pathlib import Path

# Termos expressamente vedados pela Salvaguarda Metodológica SG-01
FORBIDDEN_TERMS = [
    r"\bfraude\b",
    r"\bfraudes\b",
    r"\bfraudulento\b",
    r"\bfraudulenta\b",
    r"\bcrime\b",
    r"\bcrimes\b",
    r"\bcriminoso\b",
    r"\bcriminosa\b",
    r"\bculpado\b",
    r"\bculpada\b",
    r"\bconluio comprovado\b",
    r"\bilicito comprovado\b",
]

# Diretórios ou arquivos isentos (ex.: arquivos de teste da salvaguarda e o SRS)
EXCLUDED_PATHS = [
    Path("NexusGov — Documento de Requisitos de Software (SRS) e Metodologia.pdf"),
    Path("spec/check_language_safeguard.py"),
    Path("spec/sg/requirements.md"),
    Path("tests/test_language_safeguard.py"),
    Path(".git"),
    Path("venv"),
    Path(".venv"),
    Path("target"),
    Path("node_modules"),
]

def is_excluded(file_path: Path, root: Path) -> bool:
    rel = file_path.relative_to(root)
    for exc in EXCLUDED_PATHS:
        if exc == rel or exc in rel.parents:
            return True
    return False

def check_language(root_dir: Path):
    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_TERMS]
    violations = []

    for ext in ["*.py", "*.java", "*.ts", "*.tsx", "*.sql", "*.html", "*.json"]:
        for file_path in root_dir.rglob(ext):
            if is_excluded(file_path, root_dir):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                for line_no, line in enumerate(content.splitlines(), start=1):
                    for pattern in compiled_patterns:
                        match = pattern.search(line)
                        if match:
                            violations.append({
                                "file": str(file_path.relative_to(root_dir)),
                                "line": line_no,
                                "matched": match.group(0),
                                "snippet": line.strip()
                            })
            except Exception:
                continue

    if violations:
        print(f"❌ VIOLAÇÃO DA SALVAGUARDA SG-01! Termos proibidos detectados:", file=sys.stderr)
        for v in violations:
            print(f"  {v['file']}:{v['line']} -> termo '{v['matched']}' em: \"{v['snippet']}\"", file=sys.stderr)
        print("\nSubstitua por termos autorizados: 'indício', 'exposição', 'sinal', 'anomalia estatística'.", file=sys.stderr)
        return False
    else:
        print("✅ Salvaguarda SG-01 respeitada! Nenhuma linguagem acusatória encontrada.")
        return True

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    success = check_language(root)
    sys.exit(0 if success else 1)
