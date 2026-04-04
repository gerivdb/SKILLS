#!/usr/bin/env python3
"""
SKILLS zvec Integration

Indexes all skills in SKILLS registry for semantic discovery.
Usage: python index_skills.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, "D:\\DO\\WEB\\TOOLS\\KIVA-CLI")

from tools.core.zvec_manager import ZVecManager


def index_skills():
    skills_dir = Path("D:\\DO\\WEB\\TOOLS\\SKILLS")
    registry_file = skills_dir / "registry.json"
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