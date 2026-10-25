---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTCR_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-crush/SKILL.md
---

# Skill — worktree-crush

## Objectif

Purge définitive d'un worktree managé ou orphelin, avec sauvegarde optionnelle de la branche avant destruction. Couche CRUD — opération Delete définitive.

## Déclencheur

- `worktree-crush`, `supprimer worktree`, `purge worktree`
- Worktree orphelin sans session et sans branche utile
- Worktree stagnant avec branche obsolète

## Entrées

- `worktree_id`: ID du worktree managé (obligatoire)
- `backup_branch`: créer une branche `archive/<nom>` avant suppression (défaut : false)
- `hitl_confirm`: confirmation HITL explicite requise (obligatoire)
- `project_id`: `RAGX` ou `SKILLS` (optionnel)

## Sorties

- Confirmation de suppression
- Chemin de sauvegarde si `backup_branch=true`

## Règles

### 1. Confirmation HITL obligatoire

Ne jamais exécuter sans `hitl_confirm` explicite. C'est une opération irréversible.

### 2. Sauvegarde optionnelle

Si `backup_branch=true` : créer une branche `archive/<ancien_nom_branche>` depuis le dernier commit du worktree avant suppression.

### 3. Purge de l'entrée

Supprime l'entrée `ungrouped` même si pas de session associée.

## Script d'investigation

`scripts/crush.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_crush.ps1` — créer un worktree orphelin, vérifier qu'il est supprimé avec sauvegarde.

## Probes

- Zéro worktree écrasé sans confirmation HITL
- Zéro entrée orpheline après crush

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-crush action=crush timestamp=<ISO> worktree_id=<ID> branch=<BRANCH> backed_up=<bool> hitl_confirmed=<bool>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-BRANCH-RESURRECTION-PROTOCOL
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
