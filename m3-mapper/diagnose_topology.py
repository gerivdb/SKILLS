#!/usr/bin/env python3
"""Diagnostic rapide du topology.json."""

import json
from pathlib import Path

TOPO_PATH = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json")

with open(TOPO_PATH, "r", encoding="utf-8") as f:
    topo = json.load(f)

trees = topo.get("trees", {})
print("Nombre de trees :", len(trees))
print("IDs des trees :", list(trees.keys()))
print()

total_synapses = 0
total_validated = 0
total_dead = 0
total_blocked = 0

for tree_id, tree in trees.items():
    branches = tree.get("branches", {})
    tree_synapses = 0
    tree_validated = 0
    tree_dead = 0
    tree_blocked = 0

    for branch_id, branch in branches.items():
        synapses = branch.get("synapses", {})
        for syn_id, syn in synapses.items():
            tree_synapses += 1
            status = syn.get("status", "UNKNOWN")
            if status == "VALIDATED_PATH":
                tree_validated += 1
            elif status == "DEAD_END":
                tree_dead += 1
            elif status == "BLOCKED":
                tree_blocked += 1

    total_synapses += tree_synapses
    total_validated += tree_validated
    total_dead += tree_dead
    total_blocked += tree_blocked

    print(f"  Tree {tree_id}: {tree.get('name', tree_id)}")
    print(f"    Branches : {len(branches)}")
    print(f"    Synapses : {tree_synapses} (validés: {tree_validated}, impasses: {tree_dead}, bloqués: {tree_blocked})")

print()
print("=" * 60)
print("TOTAUX CALCULÉS À PARTIR DES DONNÉES")
print("=" * 60)
print(f"  Total trees      : {len(trees)}")
print(f"  Total synapses   : {total_synapses}")
print(f"  Total validés    : {total_validated}")
print(f"  Total impasses   : {total_dead}")
print(f"  Total bloqués    : {total_blocked}")

meta = topo.get("metadata", {})
print()
print("=" * 60)
print("MÉTADONNÉES ACTUELLES DANS LE FICHIER")
print("=" * 60)
for k, v in meta.items():
    print(f"  {k}: {v}")

print()
print("=" * 60)
print("ÉCARTS DÉTECTÉS")
print("=" * 60)
meta_trees = meta.get("total_trees", 0)
meta_syn = meta.get("total_synapses", 0)
meta_val = meta.get("validated_paths", 0)
meta_dead = meta.get("dead_ends", 0)
meta_block = meta.get("blocked", 0)

print(f"  Trees : déclaré={meta_trees}, calculé={len(trees)}, écart={meta_trees - len(trees)}")
print(f"  Synapses : déclaré={meta_syn}, calculé={total_synapses}, écart={meta_syn - total_synapses}")
print(f"  Validés : déclaré={meta_val}, calculé={total_validated}, écart={meta_val - total_validated}")
print(f"  Impasses : déclaré={meta_dead}, calculé={total_dead}, écart={meta_dead - total_dead}")
print(f"  Bloqués : déclaré={meta_block}, calculé={total_blocked}, écart={meta_block - total_blocked}")
