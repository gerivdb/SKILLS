---
name: antigravity-brain-visualizer
description: Visualiseur web interactif pour traces d'exécution d'agents Antigravity, indexant SQLite et diffs de code. Pattern inspiré de https://github.com/glaforge/antigravity-brain-visualizer
version: 1.0.0
intent_hash: 0xSKILL_ANTIGRAVITY_BRAIN_VISUALIZER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/glaforge/antigravity-brain-visualizer
source_url: https://github.com/glaforge/antigravity-brain-visualizer
path: antigravity-brain-visualizer
---

# Antigravity Brain Visualizer — Skill KiloCode

## Objectif

Fournir une référence canonique pour le visualiseur web interactif de traces d'exécution d'agents Antigravity, indexant SQLite et diffs de code. Adapté à ENV2 pour la visualisation des traces d'exécution et des diffs de code sans serveur externe.

## Déclencheur

Ce skill s'active quand :
- Il faut visualiser des traces d'exécution d'agents Antigravity
- Des diffs de code doivent être indexés et visualisés via SQLite
- Une interface web locale légère est nécessaire pour l'analyse des traces
- L'environnement ENV2 nécessite un visualiseur sans serveur externe

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `trace_db_path` | string | ✅ | Chemin absolu vers la base SQLite des traces |
| `diff_path` | string | ❌ | Chemin vers le fichier de diff de code à indexer |
| `port` | integer | ❌ | Port local pour l'interface web (défaut: 8080) |
| `read_only` | boolean | ❌ | Forcer le mode lecture seule (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `server_url` | string | URL de l'interface web de visualisation |
| `traces_indexed` | integer | Nombre de traces d'exécution indexées |
| `diffs_indexed` | integer | Nombre de diffs de code indexés |
| `evidence_hash` | string | Hash SHA-256 de la session |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que trace_db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence de la base SQLite des traces sur ENV2
```

### Étape 2 — Indexation et visualisation

```
→ Indexer les traces d'exécution depuis la base SQLite
→ Indexer les diffs de code si diff_path est fourni
→ Lancer l'interface web locale sur le port spécifié
```

### Étape 3 — Preuve d'exécution

```
→ Capturer l'URL du serveur et les statistiques d'indexation
→ Calculer le hash SHA-256 de la session
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base de traces
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un serveur web externe ou cloud pour la visualisation des traces
- ❌ Modifier les traces pendant la visualisation
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
