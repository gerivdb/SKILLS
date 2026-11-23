#!/usr/bin/env python3
"""
Debug du render.py - comprendre pourquoi seuls T-EXT et T-ID sont générés.
"""

import json
from pathlib import Path

topo_path = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json")

with open(topo_path, "r", encoding="utf-8") as f:
    topo = json.load(f)

# Simuler exactement ce que fait render.py
lines = []
lines.append("# Test de rendu")
lines.append("")

trees = topo.get("trees", {})
print(f"Nombre de trees à rendre: {len(trees)}")

for tree_id, tree in trees.items():
    print(f"  Rendu de l'arbre: {tree_id} -> {tree.get('name', tree_id)}")
    tree_name = tree.get("name", tree_id)
    tree_desc = tree.get("description", "")
    lines.append(f"## 🌳 M3 Tree : {tree_name}")
    if tree_desc:
        lines.append(f"\n*{tree_desc}*\n")
    lines.append("| Branche | Synapse | Statut | Preuve |")
    lines.append("|---------|---------|--------|--------|")

    branches = tree.get("branches", {})
    for branch_id, branch in branches.items():
        branch_name = branch.get("name", branch_id)
        synapses = branch.get("synapses", {})
        first_syn = True
        for syn_id, syn in synapses.items():
            syn_name = syn.get("name", syn_id)
            status = syn.get("status")
            emoji = {"VALIDATED_PATH": "✅", "DEAD_END": "❌", "BLOCKED": "🛑", "FRAGILE_DEBT": "⚠️", None: "❓"}.get(status, "❓")
            evidence = syn.get("evidence", "")
            script = syn.get("script", "")

            branch_cell = f"**{branch_name}**" if first_syn else ""
            first_syn = False

            line = f"| {branch_cell} | {syn_name} | {emoji} {status} | {evidence} |"
            if script:
                line = line.rstrip(" |") + f" | `{script}` |"
            lines.append(line)
    lines.append("")

print(f"\nNombre total de lignes générées: {len(lines)}")
print("Premières 50 lignes:")
for i, line in enumerate(lines[:50]):
    print(f"  {i}: {line}")