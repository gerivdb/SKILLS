#!/usr/bin/env python3
"""
SKILLS Semantic Search

Search skills using zvec vector database.
Usage: python search_skills.py <query>
"""

import sys
from pathlib import Path

sys.path.insert(0, "D:\\DO\\WEB\\TOOLS\\KIVA-CLI")

from tools.core.zvec_manager import ZVecManager


def search_skills(query: str, top_k: int = 5):
    mgr = ZVecManager(data_dir="D:\\DO\\WEB\\TOOLS\\SKILLS\\data\\zvec")
    
    print(f"\nSearching skills for: '{query}'\n")
    print("=" * 60)
    
    results = mgr.search_text(query, top_k)
    
    if not results:
        print("No skills found.")
        return
    
    for i, r in enumerate(results, 1):
        skill_id = r['id']
        score = r['score']
        desc = r.get('metadata', {}).get('description', '')[:100]
        caps = r.get('metadata', {}).get('capabilities', [])
        
        print(f"\n{i}. {skill_id}")
        print(f"   Score: {score:.4f}")
        print(f"   Description: {desc}...")
        if caps:
            print(f"   Capabilities: {', '.join(caps)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_skills.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    search_skills(query)