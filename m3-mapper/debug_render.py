#!/usr/bin/env python3
"""
Debug du render.py - comprendre pourquoi T-JEVX n'apparaît pas dans le document généré.
"""

import json
from pathlib import Path

topo_path = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json")

with open(topo_path, "r", encoding="utf-8") as f:
    topo = json.load(f)

trees = topo.get("trees", {})
print(f"Nombre de trees dans le YAML: {len(trees)}")
for tree_id, tree in trees.items():
    print(f"  Tree: {tree_id} -> {tree.get('name', tree_id)}")
    branches = tree.get("branches", {})
    print(f"    Branches: {len(branches)}")
    for branch_id, branch in branches.items():
        synapses = branch.get("synapses", {})
        print(f"    Branche: {branch_id} -> {branch.get('name', branch_id)} ({len(synapses)} synapses)")
        for syn_id, syn in synapses.items():
            status = syn.get("status", "?")
            print(f"      Synapse: {syn_id} -> {syn.get('name', syn_id)} [{status}]")

# Maintenant vérifier ce que render.py ferait
print("\n--- Simulation du rendu ---")
for tree_id, tree in trees.items():
    tree_name = tree.get("name", tree_id)
    print(f"  Would render tree: {tree_id} -> {tree_name}")