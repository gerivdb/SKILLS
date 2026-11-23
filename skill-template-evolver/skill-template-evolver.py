#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill: skill-template-evolver
Fait évoluer le template canonique SKILL.md lorsqu'une nouvelle propriété
est ajoutée à un skill existant. Vérifie que tous les skills respectent
le schéma canonique.
"""
from pathlib import Path
import sys

SKILLS_DIR = Path(__file__).resolve().parent
REQUIRED_KEYS = [
    "## Description",
    "## Déclencheurs",
    "## Règles",
    "## Invariants",
    "## Statut",
]

def check_all():
    missing = []
    for p in SKILLS_DIR.iterdir():
        if p.is_dir() and (p / "SKILL.md").exists():
            text = (p / "SKILL.md").read_text(encoding="utf-8")
            for k in REQUIRED_KEYS:
                if k not in text:
                    missing.append((p.name, k))
    return missing

def main():
    missing = check_all()
    if missing:
        print(f"[EVOLVER] {len(missing)} skills avec clés manquantes:")
        for s, k in missing:
            print(f"  - {s}: {k} manquante")
    else:
        print("[EVOLVER] Tous les skills sont conformes au template canonique")

if __name__ == "__main__":
    main()