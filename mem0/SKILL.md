---
name: mem0
description: Couche mémoire pour agents IA combinant recherche sémantique, mots-clés et liens d'entités. Pattern inspiré de https://github.com/mem0ai/mem0
version: 1.0.0
intent_hash: 0xSKILL_MEM0_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/mem0ai/mem0
source_url: https://github.com/mem0ai/mem0
path: mem0
---

# Mem0 — Skill KiloCode

## Objectif

Fournir une référence canonique pour Mem0, couche mémoire pour agents IA combinant recherche sémantique, mots-clés et liens d'entités. Adapté à ENV2 pour la mémoire d'agent locale avec recherche hybride (sémantique + symbolique) sans dépendance cloud.

## Déclencheur

Ce skill s'active quand :
- Il faut stocker et récupérer de la mémoire d'agent sur ENV2
- Une recherche hybride (sémantique via FTS5/vec, mots-clés, liens d'entités) est nécessaire
- La mémoire doit être locale et souveraine (pas de cloud externe)
- L'environnement ENV2 nécessite une couche mémoire légère pour les agents

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers la base de mémoire SQLite |
| `entity_id` | string | ✅ | Identifiant de l'entité/agent pour la mémoire |
| `memory_content` | string | ❌ | Contenu de la mémoire à stocker |
| `search_query` | string | ❌ | Requête de recherche (sémantique ou mots-clés) |
| `search_mode` | enum | ❌ | `semantic` / `keyword` / `entity` / `hybrid` (défaut: `hybrid`) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `memory_stored` | boolean | True si la mémoire a été stockée |
| `search_results` | array | Résultats de la recherche mémoire |
| `entities_found` | array | Entités liées trouvées |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence de la base de mémoire sur ENV2
```

### Étape 2 — Opération mémoire

```
→ Si memory_content est fourni : stocker la mémoire avec l'entity_id
→ Si search_query est fourni : rechercher selon le mode (semantic, keyword, entity, hybrid)
→ Retourner les résultats avec les entités liées
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier l'intégrité de la base de mémoire après l'opération
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser une couche mémoire cloud externe au lieu de Mem0 local sur ENV2
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 pour l'index sémantique

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
