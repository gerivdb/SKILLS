---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTSA_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-sync-all/SKILL.md
---

# Skill — worktree-sync-all

## Objectif

Effectue un `fetch` explicite puis un `rebase` sur `main` pour tous les worktrees managés d'un projet, en séquence. Couche CRUD — opération Update globale.

## Déclencheur

- `worktree-sync-all`, `synchroniser worktrees`, `rebase tous worktrees`
- Avant une session de merge massive ou un déploiement

## Entrées

- `project_id`: `RAGX` ou `SKILLS` (obligatoire)
- `base_branch`: branche de base (défaut : `main`)

## Sorties

- Rapport par worktree : `synced`, `conflict`, `skipped`, `ahead_after`, `behind_after`

## Règles

### 1. Fetch explicite avant rebase

Protocole BDCP : toujours `git fetch` avant tout `git rebase`. Ne jamais rebase sans fetch préalable.

### 2. Séquencement

Traiter les worktrees un par un, en séquence, pour éviter les conflits d'accès concurrentiels.

### 3. Gestion des conflits

Si un worktree génère un conflit lors du rebase : stoppe et signale, ne force pas la résolution.

### 4. Worktrees occupés

Ne pas synchroniser les worktrees en état `busy` (session active).

### 5. Surcouche GeriCode/ACT

Ne pas synchroniser les fichiers gérés par ACT (beads.json, `.kilo/bus/`) pour éviter les collisions de signaux inter-worktrees.

## Script d'investigation

`scripts/sync-all.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_sync_all.ps1` — créer plusieurs worktrees avec branches décalées, vérifier le rebase sur tous.

## Probes

- Zéro worktree rebase avec conflit non signalé
- Zéro worktree busy modifié

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-sync-all action=sync_all timestamp=<ISO> project=<PROJECT> synced=<n> conflicts=<m> skipped=<k>
```

## Référence ADR

- **ADR** : ADR-2026-06-29-001-POST-MERGE-SYNC
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
