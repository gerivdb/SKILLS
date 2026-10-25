---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTS_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-spawn/SKILL.md
---

# Skill — worktree-spawn

## Objectif

Instancie un nouveau worktree managé dans un projet Agent Manager, depuis une branche existante ou nouvelle. Couche CRUD — opération Create.

## Déclencheur

- `worktree-spawn`, `créer worktree`, `nouveau worktree`
- Démarrage d'une nouvelle tâche de développement isolée

## Entrées

- `project_id`: projet cible (`RAGX` ou `SKILLS`) (obligatoire)
- `branch_name`: nom de la branche à créer ou utiliser (obligatoire)
- `base_branch`: branche de base (défaut : `main`)
- `session_name`: nom d'affichage de la session (optionnel)

## Sorties

- `worktree_id`, `session_id`, `worktree_path`, `branch_name`

## Règles

### 1. Vérification d'unicité

Vérifier que `branch_name` n'existe pas déjà dans le dépôt cible avant création.

### 2. Création de branche

Créer la branche depuis `base_branch` si elle n'existe pas.

### 3. Instanciation via Agent Manager

Appeler `agent_manager` avec `mode: worktree` pour créer le worktree et la session associée.

### 4. Section initiale

Le worktree apparaît dans `ungrouped` jusqu'à assignation explicite à une section via `agent_manager move`.

### 5. Surcouche GeriCode/ACT

Option `init_act_bus=true` pour initialiser `.kilo/bus/` dans le nouveau worktree (coordination inter-worktrees via WAZAA en L4).

## Script d'investigation

`scripts/spawn.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_spawn.ps1` — créer un worktree, vérifier qu'il apparaît dans `ungrouped` avec la bonne branche.

## Probes

- Zéro worktree spawné avec branche dupliquée
- Chaque worktree spawné a une session associée

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-spawn action=spawn timestamp=<ISO> project=<PROJECT> branch=<BRANCH> worktree_id=<ID> session_id=<ID>
```

## Référence ADR

- **ADR** : ADR-2026-06-07-001-SESSION-BOOT-SEQUENCE
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
