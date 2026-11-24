---
name: sqlite-zig
description: Réimplémentation native d'un moteur compatible SQLite en Zig (pages B-tree, parseur, planificateur). Pattern inspiré de https://github.com/muhammad-fiaz/sqlite.zig
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_ZIG_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/muhammad-fiaz/sqlite.zig
source_url: https://github.com/muhammad-fiaz/sqlite.zig
path: sqlite-zig
---

# SQLite Zig — Skill KiloCode

## Objectif

Fournir une référence canonique pour sqlite.zig, réimplémentation native d'un moteur compatible SQLite en Zig (pages B-tree, parseur, planificateur). Adapté à ENV2 pour l'exécution de moteurs SQLite compatibles sans dépendance C, avec contrôle mémoire fin sur la station legacy.

## Déclencheur

Ce skill s'active quand :
- Il faut exécuter un moteur compatible SQLite écrit en Zig sur ENV2
- Un contrôle mémoire fin est nécessaire pour la station legacy (24 Go RAM, CPU E5620)
- Le parseur et le planificateur SQL doivent être inspectés ou modifiés
- Une implémentation native sans dépendance C est préférée

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite compatible Zig |
| `sql_query` | string | ✅ | Requête SQL à exécuter via le moteur Zig |
| `btree_inspect` | boolean | ❌ | Inspecter les pages B-tree après exécution (défaut: false) |
| `explain_plan` | boolean | ❌ | Afficher le plan d'exécution (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `query_result` | array | Résultats de la requête SQL |
| `btree_pages` | array | Pages B-tree inspectées (si activé) |
| `execution_plan` | string | Plan d'exécution du planificateur (si activé) |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier sur ENV2
```

### Étape 2 — Exécution via moteur Zig

```
→ Compiler ou lancer le moteur SQLite compatible Zig
→ Exécuter la requête SQL fournie
→ Si btree_inspect est true, inspecter les pages B-tree
→ Si explain_plan est true, afficher le plan d'exécution
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture non autorisée n'a été effectuée
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser le binaire C SQLite quand une implémentation Zig native suffit
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 pour la compilation Zig

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
