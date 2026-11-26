#!/usr/bin/env python3
"""Script: read_external_extensions.py
Rôle : Lire et afficher le registre external_extensions.json de Comet.
Aucune modification du filesystem, lecture seule.
"""
import json
import sys
from pathlib import Path


def main():
    registry_path = sys.argv[1] if len(sys.argv) > 1 else str(
        Path(__file__).parent.parent / "references" / "comet-external-extensions.json"
    )

    registry = Path(registry_path)
    if not registry.exists():
        print(f"ERREUR: Registre introuvable: {registry_path}")
        sys.exit(1)

    with open(registry, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nTotal: {len(data)} extension(s) dans le registre")


if __name__ == "__main__":
    main()