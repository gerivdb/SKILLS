---
name: datasette
description: Outil d'exploration, de filtrage par facettes/requêtes et de publication de bases SQLite (incluant Datasette Lite en WASM). Pattern inspiré de https://github.com/simonw/datasette
version: 1.0.0
intent_hash: 0xSKILL_DATASETTE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/simonw/datasette
source_url: https://github.com/simonw/datasette
path: datasette
---

# Datasette — Skill KiloCode

## Objectif

Fournir une référence canonique pour Datasette, outil d'exploration, de filtrage par facettes/requêtes et de publication de bases SQLite. Adapté à ENV2 pour l'accès web local léger aux bases SQLite sans serveur externe lourd.

## Déclencheur

Ce skill s'active quand :
- Il faut explorer une base SQLite via une interface web locale légère
- Un filtrage par facettes ou par requêtes SQL est nécessaire
- Une publication rapide de données SQLite est requise
- Datasette Lite (WASM) est préféré pour la simplicité de déploiement sur ENV2

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `port` | integer | ❌ | Port local pour l'interface web (défaut: 8080) |
| `facet_column` | string | ❌ | Colonne pour le filtrage par facettes |
| `sql_query` | string | ❌ | Requête SQL à exécuter via l'interface |
| `read_only` | boolean | ❌ | Forcer le mode lecture seule (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `server_url` | string | URL de l'interface Datasette locale |
| `tables_explored` | array | Tables explorées via l'interface |
| `facet_results` | array | Résultats du filtrage par facettes |
| `read_only_mode` | boolean | True si le mode lecture seule était actif |
| `evidence_hash` | string | Hash SHA-256 de la session |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Lancement de Datasette

```
→ Lancer Datasette sur la base cible avec le port spécifié
→ Activer le mode lecture seule
→ Appliquer le filtrage par facettes si facet_column est fourni
→ Exécuter la requête SQL si fournie
```

### Étape 3 — Preuve d'exécution

```
→ Capturer l'URL du serveur et les tables explorées
→ Calculer le hash SHA-256 de la session
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un serveur web externe ou cloud pour l'exploration SQLite
- ❌ Désactiver le mode lecture seule sans autorisation explicite
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
