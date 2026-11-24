---
name: thread-keeper
description: Récolte automatique de skills (SKILL.md), validation/purge par usage et synchronisation multi-CLI via MCP local. Pattern inspiré de https://github.com/po4erk91/thread-keeper
version: 1.0.0
intent_hash: 0xSKILL_THREAD_KEEPER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/po4erk91/thread-keeper
source_url: https://github.com/po4erk91/thread-keeper
path: thread-keeper
---

# Thread Keeper — Skill KiloCode

## Objectif

Récolter automatiquement les skills (SKILL.md), les valider ou les purger par usage, et les synchroniser via MCP local. Ce skill encapsule le pattern du repo externe `thread-keeper` adapté à ENV2.

## Déclencheur

Ce skill s'active quand :
- Un nouveau SKILL.md est créé ou modifié dans D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\
- Un skill doit être validé via validate-skill.ps1
- Un skill doit être purgé par manque d'usage (score ≤ -5)
- Les skills doivent être synchronisés via MCP local entre plusieurs instances

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `skill_path` | string | ✅ | Chemin absolu vers le SKILL.md à traiter |
| `action` | enum | ✅ | harvest / validate / purge / sync |
| `mcp_endpoint` | string | ❌ | Endpoint MCP pour la synchronisation |
| `usage_threshold` | integer | ❌ | Seuil de score pour la purge (défaut: -5) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `harvested_skills` | array | Liste des skills récoltés avec leur metadata |
| `validation_result` | enum | valid / invalid / proposed |
| `purged_skills` | array | Liste des skills purgés avec justification |
| `sync_status` | enum | synced / pending / failed |
| `evidence_hash` | string | Hash SHA-256 de l'opération |

## Protocole Obligatoire

### Étape 1 — Récolte des skills

```
→ Scanner D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\ pour les fichiers SKILL.md
→ Extraire le frontmatter YAML (name, description, version, intent_hash, triggers)
→ Vérifier l'absence de doublon (même name ou même intent_hash)
→ Enregistrer dans le registre local de récolte
```

### Étape 2 — Validation

```
→ Appeler validate-skill.ps1 sur chaque SKILL.md récolté
→ Vérifier la cohérence du frontmatter avec le schéma
→ Vérifier que les triggers et anti_triggers sont définis
→ Marquer le skill comme validé ou proposer des corrections
```

### Étape 3 — Purge par usage

```
→ Consulter le score d'utilité de chaque skill (skills-index.json ou feedback)
→ Si score ≤ -5 → marquer pour purge (superseded → archived)
→ Déplacer le skill vers l'archive (skill-bank/) pour traçabilité
→ Mettre à jour skills-index.json
```

### Étape 4 — Synchronisation MCP

```
→ Exporter les skills validés vers le format MCP (outils invoquables)
→ Synchroniser via l'endpoint MCP local
→ Vérifier que tous les clients MCP ont la version à jour
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Purger un skill sans vérifier son score d'utilité et son historique
- ❌ Synchroniser des skills non validés via MCP
- ❌ Créer un skill sans passer par la récolte/validation (validate-skill.ps1)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC dans l'opération

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : proof-recalculation
- **Règle** : explicit-path-compliance
