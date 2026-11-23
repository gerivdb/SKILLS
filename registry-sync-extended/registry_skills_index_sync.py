#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_skills_index_sync.py — Registry Sync Extended pour skills-index.json
Vérifie la cohérence entre skills-index.json et les skills réels sur disque.
Usage: python registry_skills_index_sync.py [--fix] [--check-only]
"""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

SKILLS_DIR = Path(__file__).parent.parent
SKILLS_INDEX_FILE = SKILLS_DIR / "skills-index.json"


def scan_skills_directory() -> Dict[str, Dict]:
    """Scanne le répertoire SKILLS pour trouver tous les skills valides."""
    skills = {}
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        # Lire le frontmatter du SKILL.md
        try:
            content = skill_md.read_text(encoding="utf-8")
            if content.startswith("---"):
                # Parser le frontmatter YAML basique
                lines = content.split("\n")
                frontmatter = {}
                in_fm = False
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if ":" in line:
                        key, val = line.split(":", 1)
                        frontmatter[key.strip()] = val.strip().strip('"')
                frontmatter["path"] = str(skill_dir.relative_to(SKILLS_DIR))
                skills[skill_dir.name] = frontmatter
        except Exception:
            pass
    return skills


def load_skills_index() -> Dict:
    """Charge skills-index.json."""
    try:
        with open(SKILLS_INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"skills": {}}


def save_skills_index(index: Dict):
    """Sauvegarde skills-index.json."""
    index["generated_at_utc"] = datetime.utcnow().isoformat() + "Z"
    with open(SKILLS_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def check_skills_index_drift() -> Dict:
    """Vérifie la dérive entre skills-index.json et les skills réels."""
    disk_skills = scan_skills_directory()
    index = load_skills_index()
    index_skills = index.get("skills", {}) or {}
    
    # Skills sur disque mais pas dans l'index
    missing_in_index = set(disk_skills.keys()) - set(index_skills.keys())
    # Skills dans l'index mais plus sur disque
    extra_in_index = set(index_skills.keys()) - set(disk_skills.keys())
    # Skills communs - vérifier si frontmatter a changé
    common = set(disk_skills.keys()) & set(index_skills.keys())
    changed = []
    for skill in common:
        disk_fm = disk_skills[skill]
        index_fm = index_skills[skill]
        # Comparer champs clés
        for key in ["version", "status", "intent_hash", "date"]:
            if disk_fm.get(key) != index_fm.get(key):
                changed.append({
                    "skill": skill,
                    "field": key,
                    "disk": disk_fm.get(key),
                    "index": index_fm.get(key)
                })
    
    return {
        "missing_in_index": list(missing_in_index),
        "extra_in_index": list(extra_in_index),
        "changed": changed,
        "total_disk": len(disk_skills),
        "total_index": len(index_skills)
    }


def sync_skills_index() -> Dict:
    """Met à jour skills-index.json avec les skills du disque."""
    disk_skills = scan_skills_directory()
    index = load_skills_index()
    index["skills"] = disk_skills
    index["source_repo"] = str(SKILLS_DIR)
    save_skills_index(index)
    return {"ok": True, "synced": len(disk_skills), "message": "skills-index.json synchronisé"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Registry Sync Extended - skills-index.json drift check")
    parser.add_argument("--fix", action="store_true", help="Synchroniser l'index avec le disque")
    parser.add_argument("--check-only", action="store_true", help="Vérifier seulement, ne pas modifier")
    args = parser.parse_args()

    if args.check_only or (not args.fix and not args.check_only):
        drift = check_skills_index_drift()
        result = {
            "ok": len(drift["missing_in_index"]) == 0 and len(drift["extra_in_index"]) == 0 and len(drift["changed"]) == 0,
            "drift": drift
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    
    if args.fix:
        result = sync_skills_index()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 1
    
    print(json.dumps({"ok": False, "error": "Specify --fix or --check-only"}))
    return 1


if __name__ == "__main__":
    sys.exit(main())