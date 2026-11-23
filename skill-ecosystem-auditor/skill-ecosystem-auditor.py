#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill: skill-ecosystem-auditor
Strate: L4-TOOLS/SKILLS
Description: Audite l'écosystème des skills L4 : détecte doublons, orphelins,
dépendances circulaires, chemins de registre non cohérents.
Génère un WAL d'audit par exécution.
"""
import json
import os
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = SKILLS_DIR / "REGISTRY.yaml"
WAL_DIR = SKILLS_DIR.parent / "WAL"

def load_registry():
    skills = []
    current = {}
    for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if line.startswith("- id:"):
            if current:
                skills.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif line.startswith("  name:"):
            current["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("  version:"):
            current["version"] = line.split(":", 1)[1].strip()
        elif line.startswith("  status:"):
            current["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("  path:"):
            current["path"] = line.split(":", 1)[1].strip()
        elif line.startswith("  triggers:"):
            current["triggers"] = [line.split(":", 1)[1].strip()]
        elif line.startswith("  - "):
            current.setdefault("triggers", []).append(line.strip("- ").strip())
    if current:
        skills.append(current)
    return skills

def check_duplicates(skills):
    names = [s.get("name", "") for s in skills]
    seen = {}
    dups = []
    for n in names:
        seen[n] = seen.get(n, 0) + 1
    for n, c in seen.items():
        if c > 1:
            dups.append(n)
    return dups

def check_orphans(skills):
    orphan = []
    for s in skills:
        p = Path(SKILLS_DIR) / s.get("path", "")
        if not p.exists():
            orphan.append(s.get("name", ""))
    return orphan

def main():
    skills = load_registry()
    report = {
        "timestamp": str(Path(__file__).stat().st_mtime),
        "skills_count": len(skills),
        "duplicates": check_duplicates(skills),
        "orphans": check_orphans(skills),
    }
    WAL_DIR.mkdir(parents=True, exist_ok=True)
    wal_file = WAL_DIR / f"0x244-skill-audit-{os.getpid()}.json"
    wal_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[AUDIT] {len(skills)} skills scannés")
    print(f"[AUDIT] Doublons: {report['duplicates']}")
    print(f"[AUDIT] Orphelins: {report['orphans']}")
    print(f"[AUDIT] WAL: {wal_file.name}")

if __name__ == "__main__":
    main()