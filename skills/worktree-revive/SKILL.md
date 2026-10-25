---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTR_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-revive/SKILL.md
---

# Skill — worktree-revive

## Objectif

Ressuscite un worktree managé orphelin ou supprimé par erreur, via `git reflog`. Couche CRUD — opération Restore.

## Déclencheur

- `worktree-revive`, `ressusciter worktree`, `worktree perdu`
- Branche feature supprimée accidentellement mais dont le SHA est encore dans le reflog

## Entrées

- `worktree_id`: nom ou ID du worktree à ressusciter (optionnel si `branch_name` fourni)
- `branch_name`: nom de la branche à ressusciter (optionnel si `worktree_id` fourni)
- `reflog_sha`: SHA spécifique à restaurer (optionnel, déduit du reflog si absent)
- `project_id`: `RAGX` ou `SKILLS` (optionnel)

## Sorties

- `worktree_id` restauré, `session_id` recréée, confirmation de réintégration

## Règles

### 1. Récupération via reflog

Consulter `git reflog` pour retrouver le SHA du dernier commit de la branche supprimée.

### 2. Recréation du worktree

Recréer le worktree avec `git worktree add` sur le SHA retrouvé.

### 3. Réintégration

Réintégrer dans `ungrouped` via `agent_manager` (move sectionID=null).

### 4. Surcouche GeriCode/ACT

Vérifier la cohérence du bus ACT avant réintégration pour éviter les collisions de signaux.

## Script d'investigation

`scripts/revive.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_revive.ps1` — supprimer un worktree, le ressusciter via reflog, vérifier qu'il est fonctionnel.

## Probes

- Zéro worktree ressuscité avec SHA incorrect
- Zéro ressuscitation sans vérification reflog

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-revive action=revive timestamp=<ISO> worktree_id=<ID> branch=<BRANCH> sha=<SHA> reflog_used=<bool>
```

## Référence ADR

- **ADR** : ADR-2026-08-28-001-BRANCH-RESURRECTION-PROTOCOL
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
