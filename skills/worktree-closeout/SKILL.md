---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTC_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-closeout/SKILL.md
---

# Skill — worktree-closeout

## Objectif

Ferme proprement un worktree managé après vérification que sa branche est mergée dans `main`. Sequence : unassign de section (`sectionID: null`), stop de session, suppression de l'entrée `ungrouped`. Couche CRUD — opération Delete partiel (nettoyage de session).

## Déclencheur

- `worktree-closeout`, `fermer worktree`, `worktree terminé`
- Fin de session de développement sur une branche feature

## Entrées

- `worktree_id`: ID du worktree managé (obligatoire)
- `session_id`: ID de la session (optionnel, déduit du worktree si absent)
- `verify_merge`: vérifier que la branche est mergée dans `main` (défaut : true)
- `project_id`: `RAGX` ou `SKILLS` (optionnel)

## Sorties

- Confirmation de fermeture
- SHA de la branche mergée
- Lien vers le commit de merge sur `main`

## Règles

### 1. Vérification de merge préalable

Avant toute fermeture, vérifier que `git log main..<branche>` est vide (aucune commit non mergée). Si `verify_merge=true` et que la branche n'est pas mergée : arrêt avec erreur.

### 2. Sequence de fermeture

1. `agent_manager move` avec `sectionID: null` (unassign)
2. `agent_manager stop` sur la session
3. Suppression de l'entrée `ungrouped` si elle persiste

### 3. Surcouche GeriCode/ACT

Avant suppression, vérifier qu'aucun signal ACT en attente dans `.kilo/bus/` ne référence ce worktree.

## Script d'investigation

`scripts/closeout.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_closeout.ps1` — créer un worktree mergé, vérifier qu'il est fermé proprement.

## Probes

- Zéro worktree fermé avec branche non mergée
- Zéro entrée `ungrouped` résiduelle après closeout

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-closeout action=closeout timestamp=<ISO> worktree_id=<ID> branch=<BRANCH> merged=<bool> session_stopped=<bool>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-PR-LIFECYCLE-GATE
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
