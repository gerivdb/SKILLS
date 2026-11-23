#!/usr/bin/env python3
import json
from pathlib import Path

TOPO_PATH = Path("topology.json")
DISCOVERED_PATH = Path("discovered_repos.json")

with open(TOPO_PATH, "r", encoding="utf-8") as f:
    topo = json.load(f)

with open(DISCOVERED_PATH, "r", encoding="utf-8") as f:
    discovered = json.load(f)

# Arbres déjà dans le graphe
existing_trees = set()
for tree_id in topo.get("trees", {}):
    # L'ID est sous forme T-NOM
    existing_trees.add(tree_id.replace("T-", "").upper())

print(f"Arbres déjà dans le graphe ({len(existing_trees)}):")
for t in sorted(existing_trees):
    print(f"  {t}")

print(f"\nDécouverts dans known_repos ({len(discovered)}):")
remaining = []
for name, info in sorted(discovered.items(), key=lambda x: x[1].get("test_count", 0), reverse=True):
    if name.upper() not in existing_trees:
        remaining.append((name, info["stratum"], info["test_count"]))
        print(f"  {info['stratum']}/{name} ({info['test_count']} tests)")

print(f"\nTotal dépôts restants à cartographier : {len(remaining)}")

# Sauvegarder la liste cible
with open("target_remaining_12.json", "w", encoding="utf-8") as f:
    json.dump(remaining, f, indent=2)