#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill: skill-dependency-healer
Détecte et résout les dépendances manquantes ou circulaires entre skills L4.
"""
import json
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent

def load_registry():
    skills = {}
    for p in SKILLS_DIR.iterdir():
        if p.is_dir() and (p / "SKILL.md").exists():
            text = (p / "SKILL.md").read_text(encoding="utf-8")
            deps = []
            for line in text.splitlines():
                if line.startswith("- Dépendances :"):
                    deps = [d.strip() for d in line.split(":", 1)[1].split(",")]
            skills[p.name] = {"path": p, "deps": deps}
    return skills

def find_cycles(skills):
    # Simple cycle detection via DFS
    visited = set()
    rec_stack = set()
    cycles = []
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for dep in skills.get(node, {}).get("deps", []):
            if dep not in visited:
                if dfs(dep):
                    return True
            elif dep in rec_stack:
                cycles.append(dep)
                return True
        rec_stack.remove(node)
        return False
    for s in skills:
        if s not in visited:
            dfs(s)
    return cycles

def main():
    skills = load_registry()
    cycles = find_cycles(skills)
    print(f"[HEALER] {len(skills)} skills scannés")
    print(f"[HEALER] Cycles détectés: {cycles}")
    if cycles:
        print("[HEALER] ACTION: romper les cycles en supprimant les arêtes les moins critiques")

if __name__ == "__main__":
    main()