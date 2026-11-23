#!/usr/bin/env python3
"""
Découvre automatiquement les dépôts avec tests d'intégration.
"""

import json
from pathlib import Path

SEARCH_ROOT = Path("D:/DO/WEB/TOOLS")
TARGET_STRATA = ["L0-CANON", "L1-INFRA", "L2-PLATFORM", "L3-CITIZENS", "L4-TOOLS"]

def discover_repos():
    repos = {}
    for stratum in TARGET_STRATA:
        stratum_path = SEARCH_ROOT / stratum
        if not stratum_path.exists():
            continue

        for repo_dir in stratum_path.iterdir():
            if not repo_dir.is_dir():
                continue

            repo_name = repo_dir.name
            tests_dir = repo_dir / "tests"

            if not tests_dir.exists():
                continue

            test_files = [f for f in tests_dir.glob("test_*.py") if f.is_file()]

            if len(test_files) > 0:
                repos[repo_name] = {
                    "path": str(repo_dir),
                    "stratum": stratum,
                    "test_count": len(test_files),
                    "test_files": [f.name for f in test_files]
                }

    return repos

if __name__ == "__main__":
    repos = discover_repos()
    print(f"Découverts {len(repos)} dépôts avec tests :\n")
    for name, info in sorted(repos.items(), key=lambda x: x[1]['test_count'], reverse=True):
        print(f"  {info['stratum']}/{name}: {info['test_count']} tests")

    Path("discovered_repos.json").write_text(json.dumps(repos, indent=2))
    print(f"\nSauvegardé dans discovered_repos.json")
