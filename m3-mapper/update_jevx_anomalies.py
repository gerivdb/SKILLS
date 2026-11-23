#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mettre à jour le topology.json avec les anomalies JEVX qualifiées
et préparer le sweep complet des 115 dépôts restants.
"""

import json
from pathlib import Path

TOPO_PATH = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json")

with open(TOPO_PATH, "r", encoding="utf-8") as f:
    topo = json.load(f)

# 1. Mettre à jour kiva_kix_service_health (déjà BLOCKED, préciser la raison)
topo["trees"]["T-JEVX"]["branches"]["B-JEVX-KIVA"]["synapses"]["kiva_kix_service_health"].update({
    "status": "BLOCKED",
    "error_class": "Service_Unavailable",
    "evidence": "Ollama non installé sur ENV2. /health répond 200 mais /v1/systemone retourne 422.",
    "evidence_full": "JEVX démarre et répond sur 8080/health (200 OK). /v1/systemone retourne 422 Unprocessable Entity car Ollama (modèle upstream) n'est pas installé sur ENV2.",
    "timestamp": "2026-11-21T02:45:00Z",
    "script": "tests/test_kix_integration.py::test_kix_service_health",
    "conclusion": "JEVX démarre mais dépend d'Ollama qui n'est pas installé sur ENV2. Impossible de tester /v1/systemone sans Ollama."
})

# 2. Mettre à jour core_hallucination_gold_set (déjà BLOCKED, préciser la raison)
topo["trees"]["T-JEVX"]["branches"]["B-JEVX-CORE"]["synapses"]["core_hallucination_gold_set"] = {
    "status": "BLOCKED",
    "error_class": "Service_Unavailable",
    "evidence": "JEVX /v1/systemone retourne 422 - Ollama upstream non disponible sur ENV2.",
    "evidence_full": "POST /v1/systemone retourne 422 Unprocessable Entity. Cause probable : absence du modèle upstream Ollama (gemma3:1b) sur ENV2.",
    "timestamp": "2026-11-21T02:45:00Z",
    "script": "tests/test_hallucination_gold_set.py::test_hallucination_gold_set",
    "conclusion": "Impossible de tester l'hallucination sans Ollama démarré sur ENV2."
}

# 3. Ajouter la synapse pour le blocage de collecte pytest (test_jevx_in_mox_crosslinks.py)
topo["trees"]["T-JEVX"]["branches"]["B-JEVX-STUDY"]["synapses"]["jevx_mox_crosslinks_collection_blocked"] = {
    "status": "DEAD_END",
    "error_class": "SyntaxError",
    "evidence": "sys.exit(0) appelé dans test_jevx_in_mox_crosslinks.py ligne 17, bloquant la collecte pytest pour tous les tests du fichier (12 items collectés, 2 erreurs de collecte).",
    "evidence_full": "pytest collection échoue car test_jevx_in_mox_crosslinks.py ligne 17 contient sys.exit(0) au lieu d'une assertion. pytest ne peut pas collecter les autres tests du fichier.",
    "timestamp": "2026-11-21T02:45:00Z",
    "script": "tests/test_jevx_in_mox_crosslinks.py::test_jevx_in_mox_crosslinks",
    "conclusion": "Bug de code de test : sys.exit(0) appelé au lieu d'une assertion. Empêche la collecte de tous les tests du fichier."
}

with open(TOPO_PATH, "w", encoding="utf-8") as f:
    json.dump(topo, f, ensure_ascii=False, indent=2)

print("topology.json mis à jour avec les 3 anomalies JEVX qualifiées.")
print()
# Recalculer les métadonnées
total_synapses = 0
total_validated = 0
total_dead = 0
total_blocked = 0
for tree in topo["trees"].values():
    for branch in tree.get("branches", {}).values():
        for syn in branch.get("synapses", {}).values():
            total_synapses += 1
            st = syn.get("status")
            if st == "VALIDATED_PATH":
                total_validated += 1
            elif st == "DEAD_END":
                total_dead += 1
            elif st == "BLOCKED":
                total_blocked += 1

topo["metadata"] = {
    "total_trees": len(topo["trees"]),
    "total_branches": sum(len(t.get("branches", {})) for t in topo["trees"].values()),
    "total_synapses": total_synapses,
    "validated_paths": total_validated,
    "dead_ends": total_dead,
    "blocked": total_blocked,
    "last_updated_utc": "2026-11-21T02:45:00Z",
    "generator": "m3_mapper_engine_v1"
}

with open(TOPO_PATH, "w", encoding="utf-8") as f:
    json.dump(topo, f, ensure_ascii=False, indent=2)

print(f"  Trees: {topo['metadata']['total_trees']}")
print(f"  Branches: {topo['metadata']['total_branches']}")
print(f"  Synapses: {total_synapses}")
print(f"  Validés: {total_validated}")
print(f"  Impasses: {total_dead}")
print(f"  Bloqués: {total_blocked}")