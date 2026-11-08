"""
NexusGov - Validador de Rastreabilidade SDD (Spec-Driven Development)
Verifica a integridade entre a matriz de requisitos e os documentos em spec/.
"""

import json
import sys
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent.parent
    matrix_file = root_dir / "spec" / "matrix.json"

    if not matrix_file.exists():
        print(f"ERRO: Matriz não encontrada em {matrix_file}", file=sys.stderr)
        sys.exit(1)

    with open(matrix_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    requirements = data.get("requirements", [])
    print(f"--- NexusGov SDD Traceability Validator ---")
    print(f"Projeto: {data.get('project')} v{data.get('version')}")
    print(f"Escopo Piloto: {data.get('pilot_scope', {}).get('estado')} ({data.get('pilot_scope', {}).get('uf')})")
    print(f"Total de Requisitos Catalogados: {len(requirements)}\n")

    errors = []
    status_counts = {}
    priority_counts = {}

    for req in requirements:
        req_id = req.get("id")
        spec_path = root_dir / req.get("spec_file", "")
        priority = req.get("priority", "Unknown")
        status = req.get("status", "Unknown")

        status_counts[status] = status_counts.get(status, 0) + 1
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

        if not spec_path.exists():
            errors.append(f"[{req_id}] Arquivo de especificação não encontrado: {req.get('spec_file')}")
            continue

        spec_content = spec_path.read_text(encoding="utf-8")
        if req_id not in spec_content:
            errors.append(f"[{req_id}] ID não referenciado no arquivo de especificação {req.get('spec_file')}")

    print("Distribuição por Prioridade:")
    for p, count in sorted(priority_counts.items()):
        print(f"  - {p}: {count}")

    print("\nDistribuição por Status:")
    for s, count in sorted(status_counts.items()):
        print(f"  - {s}: {count}")

    if errors:
        print("\nFalhas de rastreabilidade encontradas:", file=sys.stderr)
        for err in errors:
            print(f"  ❌ {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n✅ Matriz de rastreabilidade 100% íntegra!")

if __name__ == "__main__":
    main()
