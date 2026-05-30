---
name: swarm-cli
description: Swarm, bus ternaire and governance CLI expert for WAZAA, OPENCLAW-CLI, BLO, GOVERNANCE-HUB. Use when user mentions
  "WAZAA", "OPENCLAW", "BLO", "GOVERNANCE-HUB", "bus ternaire", "swarm", "φ-CPS", "TritRegistry".
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---

# Swarm CLI

## Instructions

1. **Identifier la demande** : bus ternaire WAZAA, commandes OPENCLAW, conformité φ-CPS, audit gouvernance.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/WAZAA`, `gerivdb/BLO` ou `gerivdb/GOVERNANCE-HUB` selon le contexte.
3. **Lire `SCOPE.yaml`** et les primitives TritRegistry avant de générer des commandes.
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Ne pas inventer de primitives WAZAA-243 sans les avoir lues dans le code.
- La conformité φ-CPS est calculée via GOVERNANCE-HUB, jamais estimée manuellement.
- Les événements BLO doivent être tracés dans bloom.db avant clôture.

## Format

- Code fences pour les commandes OPENCLAW et WAZAA.
- Tableaux pour les audits de conformité φ-CPS.

## Exemples

- "[Auditer la conformité φ-CPS du dernier sprint]" → Lire `GOVERNANCE-HUB/audits/`, calculer score composite, afficher tableau par repo.
