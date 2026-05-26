#!/usr/bin/env python3
"""
SKILLS zvec Integration

Indexes all skills in SKILLS registry for semantic discovery.
Usage: python index_skills.py
"""

import json
import sys
from pathlib import Path

# Use repository root as skills_dir (script intended to run from repo root)
skills_dir = Path.cwd()
registry_file = skills_dir / "registry.json"

# allow local shim of ZVecManager in tools.core
sys.path.insert(0, str(Path.cwd()))
try:
    from tools.core.zvec_manager import ZVecManager
except Exception:
    # Minimal fallback shim if missing
    class ZVecManager:
        def __init__(self, data_dir=None):
            if data_dir is None:
                data_dir = Path.cwd() / 'data' / 'zvec'
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.index = []
        def add_text(self, doc_id, text, metadata=None):
            entry = {'id': doc_id, 'text': text, 'metadata': metadata or {}}
            self.index.append(entry)
            out = {'size': len(self.index), 'entries': self.index}
            with open(self.data_dir / 'zvec_index.json', 'w', encoding='utf-8') as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
        def get_stats(self):
            return {'size': len(self.index)}


def index_skills():
    mgr = ZVecManager(data_dir=skills_dir / "data" / "zvec")

    if not registry_file.exists():
        print(f"Registry not found: {registry_file}")
        return

    with open(registry_file, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    skills = registry.get("skills", [])
    indexed = 0

    for skill in skills:
        skill_id = skill.get("name", "")
        description = skill.get("description", "")
        capabilities = skill.get("capabilities", [])

        if not skill_id:
            continue

        content = f"{skill_id} {description} {' '.join(capabilities)}"
        mgr.add_text(skill_id, content, {
            "name": skill_id,
            "description": description,
            "capabilities": capabilities,
            "type": "skill"
        })
        indexed += 1
        print(f"Indexed skill: {skill_id}")

    print(f"\nTotal skills indexed: {indexed}")
    stats = mgr.get_stats()
    print(f"Vector index size: {stats['size']}")


if __name__ == "__main__":
    index_skills()
