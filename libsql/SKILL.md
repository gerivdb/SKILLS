---
name: libsql
description: Fork open source de SQLite avec répliques embarquées, UDFs et extensions d'exécution. Pattern inspiré de https://github.com/tursodatabase/libsql
version: 1.0.0
intent_hash: 0xSKILL_LIBSQL_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/tursodatabase/libsql
source_url: https://github.com/tursodatabase/libsql
path: libsql
---

# libSQL — Skill KiloCode

## Objectif

Fournir une référence canonique pour libSQL, fork open source de SQLite avec répliques embarquées, UDFs et extensions d'exécution. Adapté à ENV2 pour l'accès local structuré avec capacités de réplication légère et extensions définies par l'utilisateur.

## Déclencheur

Ce skill s'active quand :
- Il faut utiliser libSQL comme alternative à SQLite sur ENV2
- Une réplication embarquée légère est nécessaire entre instances locales
- Des UDFs (User Defined Functions) doivent être enregistrées pour des requêtes personnalisées
- Des extensions d'exécution doivent être chargées sans dépendances lourdes

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier libSQL/SQLite |
| `replica_mode` | boolean | ❌ | Activer le mode réplique embarquée (défaut: false) |
| `udf_name` | string | ❌ | Nom de l'UDF à enregistrer |
| `udf_implementation` | string | ❌ | Implémentation de l'UDF (Python/JS) |
| `target_query` | string | ✅ | Requête SQL à exécuter |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `query_result` | array | Résultats de la requête SQL |
| `replica_status` | string | Statut de la réplique (si activée) |
| `udf_registered` | boolean | True si l'UDF a été enregistrée |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier sur ENV2
```

### Étape 2 — Exécution libSQL

```
→ Ouvrir la base avec le driver libSQL
→ Si replica_mode est true, configurer la réplication embarquée
→ Si udf_name est fourni, enregistrer l'UDF
→ Exécuter la requête target_query
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

- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Enregistrer des UDF sans validation de sécurité
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 pour la réplication

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
