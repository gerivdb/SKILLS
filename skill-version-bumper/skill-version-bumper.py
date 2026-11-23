#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill: skill-version-bumper
Incrémente les numéros de version V-4D (Major.Minor.Patch.Micro-Delta)
dans SKILL.md et REGISTRY.yaml.
"""
import sys
from pathlib import Path

def bump(skill_name: str, level: str = "micro") -> None:
    skills_dir = Path(__file__).resolve().parent
    skill_path = skills_dir / skill_name / "SKILL.md"
    if not skill_path.exists():
        print(f"[ERROR] Skill {skill_name} non trouvé")
        sys.exit(1)
    text = skill_path.read_text(encoding="utf-8")
    # Incrémente version: 1.0.0 -> 1.0.1 (patch) ou 1.0.0 -> 1.1.0 (minor)
    m = re.search(r"version:\s*v?(\d+)\.(\d+)\.(\d+)", text)
    if not m:
        print(f"[ERROR] Pas de version trouvée dans {skill_path}")
        sys.exit(1)
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if level == "major":
        major += 1; minor = 0; patch = 0
    elif level == "minor":
        minor += 1; patch = 0
    else:
        patch += 1
    new_ver = f"{major}.{minor}.{patch}"
    text = re.sub(r"version:\s*v?\d+\.\d+\.\d+", f"version: {new_ver}", text)
    skill_path.write_text(text, encoding="utf-8")
    print(f"[VERSION] {skill_name}: {major}.{minor}.{patch} ({level})")

import re
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: skill-version-bumper <skill_name> <major|minor|patch>")
        sys.exit(1)
    bump(sys.argv[1], sys.argv[2])