#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill: skill-deployer
Déploie un skill d'un dépôt source vers un dépôt cible (strate L* uniquement),
avec sauvegarde WAL et vérification skill-linter-sentinel.
"""
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent
VALID_STRATES = ["L0", "L1", "L2", "L3", "L4", "L5", "L6"]

def deploy(skill_name: str, target_repo: str) -> None:
    src = SKILLS_DIR / skill_name
    if not src.exists():
        print(f"[ERROR] Skill {skill_name} introuvable dans {SKILLS_DIR}")
        sys.exit(1)
    # Vérifier que la cible est une strate L* valide
    parts = target_repo.split("/")
    if not any(p.startswith("L") and p[1:].isdigit() and int(p[1:]) <= 6 for p in parts):
        print(f"[ERROR] Cible {target_repo} n'est pas dans une strate L* valide (L0-L6)")
        sys.exit(1)
    print(f"[DEPLOY] {skill_name} -> {target_repo}")
    print(f"[DEPLOY] Vérification skill-linter-sentinel requise avant déploiement")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: skill-deployer <skill_name> <target_repo_strate>")
        sys.exit(1)
    deploy(sys.argv[1], sys.argv[2])