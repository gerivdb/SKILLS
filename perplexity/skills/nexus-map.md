---
name: nexus-map
description: Universal navigation map for all active gerivdb repos (168 total, geri-cms-* excluded). Use when user mentions
  "where is", "quel repo", "cluster", "liste des repos", "cartographie", "nexus-map".
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---

# NEXUS Map

## Instructions

1. **Identifier la demande** : localisation d'un repo, liste d'un cluster, ou redirection vers un skill spécialisé.
2. **Vérification préalable** : `mcp_github get_file_contents` sur `gerivdb/NEXUS/ECOS_ROOT.json` pour l'état canonique.
3. **Clusters actifs** : intelligence (IRIS, KRONOS, FLUX), swarm (WAZAA, BLO, OPENCLAW-CLI), infra (KIVA, PULSE, ATLAS, FORGE), data (VDB, DATA-MINER, ECOS-VISION), browser (COMET, BIRDY), media (ROCK-REIMS-AGENDA, GVDB-MEDIA), legacy (FERMI-EVER, CodeDB-E5620, LYCOS), piliers (PLIX, GOST, TINA, TRANSCENDANCE, VERSUS, BATVERSE), core (NEXUS, ECOYSTEM, ECOS-CLI, BRAIN, GATEWAY-MANAGER, KIVA-CLI, ONTOLOGY, DevTools, FLUENCE).
4. **Appliquer les tags NEXUS**.
5. **Répondre en français**.

## Règles

- Ne jamais affirmer qu'un repo n'existe pas sans avoir vérifié via MCP GitHub.
- Tout repo hors ECOS_ROOT est `[DÉRIVÉ]` jusqu'à enregistrement NEXUS.
- Les repos geri-cms-* sont exclus de toute analyse.

## Format

- Tableaux pour les clusters.
- Listes pour les repos d'un cluster donné.

## Exemples

- "[Où se trouve la logique de monitoring ?]" → Cluster infra : PULSE (métriques), KIVA (containers), ATLAS (IaC) — vérifier `gerivdb/PULSE`.
