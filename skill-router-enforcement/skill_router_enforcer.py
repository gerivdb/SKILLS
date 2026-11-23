#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_router_enforcer.py — Skill Router Enforcement
Gate pre-commit qui vérifie skills-index.json avant toute création de fichier/code.
Interdit la création de code qui duplique un skill existant.
Usage: python skill_router_enforcer.py [--check-only] [--files file1.py...]
"""
import json
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any

SKILLS_INDEX_FILE = Path(__file__).parent.parent / "skills-index.json"
SKILLS_DIR = Path(__file__).parent.parent

# Mots-clés qui déclenchent la vérification de skills existants
TRIGGER_KEYWORDS = {
    "cdp": ["cdp", "chrome devtools", "websocket", "chrome.debugger"],
    "gemini": ["gemini", "google gemini"],
    "deepseek": ["deepseek"],
    "git": ["git ", "git.commit", "git.push", "git.branch", "git.merge", "git.rebase"],
    "skill": ["skill ", "skill.", "skill(", "skill[", "create_skill", "new_skill"],
    "agent": ["agent ", "shard", "sub-agent", "subagent"],
    "git_ops": ["git add", "git commit", "git push", "git pull", "git fetch", "git merge", "git rebase", "git branch", "git checkout", "git stash", "git log", "git diff"],
    "cdp": ["cdp", "chrome.devtools", "websocket", "chrome.debugger", "runtime.enable", "runtime.evaluate", "page.navigate", "input.dispatchkeyevent"],
    "skill_mgmt": ["validate-skill", "index-skills", "skill-feedback", "distill-skill", "skill-feedback"],
    "git_hooks": ["pre-commit", "pre-push", "post-commit", "commit-msg", "husky", ".githooks"],
    "git_worktree": ["worktree", "git worktree"],
    "branch_mgmt": ["branch", "branche", "branching", "merge", "rebase", "cherry-pick"],
    "skill_creation": ["create_skill", "new_skill", "skill.create", "skill.new"],
    "temp_cleanup": ["tempfile", "temp_dir", "cleanup", "tempfile.mkdtemp"],
    "evidence": ["evidence.md", "evidence_", "sha256", "hash ", "hashlib"],
    "adr": ["adr ", "adr.", "architecture decision", "decision record"],
    "git_remote": ["origin", "upstream", "remote", "git remote", "git push", "git fetch"],
    "skill_index": ["skills-index", "skills_index", "skill.index", "skill_index"],
    "citizen": ["citizen", "citizen.", "daemon", "service", "worker", "consumer", "producer"],
    "vex": ["vex.yaml", "vex ", "vex-"],
    "kiva": ["kiva", "kiva.", "kiva-"],
    "cdp_gemini": ["gemini_cdp", "gemini.cdp", "gemini_dialog", "gemini.dialog"],
    "cdp_deepseek": ["deepseek_cdp", "deepseek.cdp", "deepseek_gateway", "deepseek.gateway"],
}

SKILLS_INDEX_FILE = Path(__file__).parent.parent / "skills-index.json"


def load_skills_index() -> Dict[str, Any]:
    """Charge skills-index.json."""
    try:
        with open(SKILLS_INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"skills": {}}


def get_skill_keywords(skill_name: str, skill_info: Dict) -> List[str]:
    """Extrait les mots-clés d'un skill depuis son nom et sa description."""
    keywords = set()
    # Du nom
    for word in re.split(r'[-_\s]', skill_name.lower()):
        if len(word) > 2:
            keywords.add(word)
    # De la description si disponible
    if isinstance(skill_info, dict):
        desc = skill_info.get("description", "")
        for word in re.split(r'[-_\s]', desc.lower()):
            if len(word) > 2:
                keywords.add(word)
    return list(keywords)


def check_skill_coverage(description: str, skills_index: Dict) -> List[Dict]:
    """Vérifie si un skill existant couvre le besoin décrit."""
    matches = []
    desc_lower = description.lower()
    
    skills = skills_index.get("skills", {}) or {}
    for skill_name, skill_info in skills.items():
        skill_keywords = get_skill_keywords(skill_name, skill_info)
        for kw in skill_keywords:
            if len(kw) > 3 and kw in desc_lower:
                matches.append({
                    "skill": skill_name,
                    "matched_keyword": kw,
                    "description": skill_info.get("description", "")[:100] if isinstance(skill_info, dict) else ""
                })
                break
    return matches


def scan_file_for_triggers(filepath: Path) -> List[str]:
    """Scanne un fichier pour détecter les mots-clés déclencheurs."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return []
    
    triggers = []
    content_lower = content.lower()
    for category, keywords in TRIGGER_KEYWORDS.items():
        for kw in keywords:
            if kw in content_lower:
                triggers.append(category)
                break
    return list(set(triggers))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Skill Router Enforcement - Pre-commit gate")
    parser.add_argument("--check-only", action="store_true", help="Ne pas bloquer, juste reporter")
    parser.add_argument("--files", nargs="*", help="Fichiers spécifiques à vérifier")
    parser.add_argument("--description", help="Description du travail prévu (pour check coverage)")
    args = parser.parse_args()

    skills_index = load_skills_index()
    
    if args.description:
        matches = check_skill_coverage(args.description, skills_index)
        if matches:
            print(json.dumps({
                "ok": False,
                "message": "Skills existants couvrent ce besoin",
                "matches": matches
            }, ensure_ascii=False, indent=2))
            return 1
        else:
            print(json.dumps({"ok": True, "message": "Aucun skill existant ne couvre ce besoin"}))
            return 0

    if args.files:
        files = [Path(f) for f in args.files if Path(f).exists()]
    else:
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True, text=True, check=True, timeout=10
            )
            files = [Path(f.strip()) for f in result.stdout.strip().split("\n") if f.strip()]
            files = [f for f in files if f.exists() and f.suffix in [".py", ".ps1", ".sh", ".js", ".ts", ".json", ".yaml", ".yml", ".md"]]
        except subprocess.CalledProcessError:
            files = []

    if not files:
        print(json.dumps({"ok": True, "message": "Aucun fichier à vérifier"}))
        return 0

    skills_index_data = load_skills_index()
    all_issues = []

    for f in files:
        triggers = scan_file_for_triggers(f)
        if triggers:
            for trigger in triggers:
                matches = check_skill_coverage(trigger, skills_index_data)
                if matches:
                    for m in matches:
                        all_issues.append({
                            "file": str(f),
                            "trigger": trigger,
                            "existing_skill": m["skill"],
                            "matched_keyword": m["matched_keyword"],
                            "existing_description": m["description"],
                            "severity": "HIGH"
                        })

    if all_issues:
        print(json.dumps({
            "ok": False,
            "message": "Skills existants détectés pour les modifications proposées",
            "issues": all_issues,
            "recommendation": "Utiliser les skills existants au lieu de créer du code dupliqué"
        }, ensure_ascii=False, indent=2))
        return 1
    
    print(json.dumps({"ok": True, "message": "Aucun conflit avec skills existants"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())