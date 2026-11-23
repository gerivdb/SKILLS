#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mettre à jour le topology.json avec les résultats réels des tests JEVX.
"""

import json
from pathlib import Path

TOPO_PATH = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json")

with open(TOPO_PATH, "r", encoding="utf-8") as f:
    topo = json.load(f)

# Mettre à jour les synapses avec les résultats réels des tests

# kiva_kix_service_health : JEVX répond sur 8080/health → VALIDATED_PATH
topo["trees"]["T-JEVX"]["branches"]["B-JEVX-KIVA"]["synapses"]["kiva_kix_service_health"] = {
    "status": "VALIDATED_PATH",
    "error_class": None,
    "evidence": "Port 8080 répond, /health retourne 200 {\"status\":\"ok\"}.",
    "evidence_full": "Chromium CDP 9222 et JEVX 8080 sont opérationnels. Le endpoint /health retourne {\"status\":\"ok\"}.",
    "timestamp": "2026-11-21T02:15:00Z",
    "script": "tests/test_jevx_live.py::test_health (test en direct)",
    "conclusion": "JEVX est démarré et répond sur le port 8080."
}

# kiva_model_selector : Ollama non démarré → reste BLOCKED
topo["trees"]["T-JEVX"]["branches"]["B-JEVX-KIVA"]["synapses"]["kiva_model_selector"] = {
    "status": "BLOCKED",
    "error_class": "Service_Unavailable",
    "evidence": "Ollama non démarré sur le port 11434. Aucun modèle disponible.",
    "evidence_full": "Ollama n'est pas démarré. Le test model_selector ne peut pas s'exécuter sans serveur Ollama.",
    "timestamp": "2026-11-21T02:10:00Z",
    "script": "tests/test_kix_integration.py::test_model_selector",
    "conclusion": "Ollama non démarré. À démarrer pour test complet."
}

# core_hallucination_gold_set : JEVX répond mais 422 sur /v1/systemone
topo["trees"]["T-JEVX"]["branches"]["B-JEVX-CORE"]["synapses"]["core_hallucination_gold_set"] = {
    "status": "BLOCKED",
    "error_class": "Service_Unavailable",
    "evidence": "JEVX répond sur 8080 mais /v1/systemone retourne 422 (format de requête).",
    "evidence_full": "JEVX démarre et répond sur 8080 (/health: 200 OK). POST /v1/systemone retourne 422 Unprocessable Entity, probablement un problème de format de requête dans le script de test ou dans le handler du serveur.",
    "timestamp": "2026-11-21T02:10:00Z",
    "script": "tests/test_hallucination_gold_set.py, tests/test_jevx_live.py",
    "conclusion": "JEVX démarré mais /v1/systemone retourne 422. À investiguer : format de requête ou handler du serveur."
}

with open(TOPO_PATH, "w", encoding="utf-8") as f:
    json.dump(topo, f, ensure_ascii=False, indent=2)

print("topology.json mis à jour avec les résultats réels des tests JEVX.")