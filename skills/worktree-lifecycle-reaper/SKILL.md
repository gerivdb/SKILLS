---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_WLR_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-lifecycle-reaper/SKILL.md
---

# Skill — worktree-lifecycle-reaper

## Objectif

Protocole d'épitaphe et de restitution propre à la clôture d'une session. Déployé en symétrie du `setup-script.ps1`, ce script de teardown automatique s'active à la fin de la tâche : vérification que la branche est mergée ou archivée, suppression des jonctions NTFS temporaires, restitution du bail dans `leases.jsonl`, émission de la trace WAL scellant l'expérience. Couche Worktree Engineering — opération de clôture.

## Déclencheur

- `worktree-lifecycle-reaper`, `clôture worktree`, `teardown worktree`, `reaper worktree`, `fin de session`
- À la fin de chaque session de travail sur un worktree

## Entrées

- `worktree_path`: chemin physique du worktree (défaut : `$env:WORKTREE_PATH`)
- `branch_name`: nom de la branche (obligatoire)
- `session_id`: ID de la session Agent Manager (optionnel)
- `repo_path`: racine du dépôt maître parent (défaut : `$env:REPO_PATH`)

## Sorties

- Jonctions NTFS temporaires supprimées
- Bail restitué dans `leases.jsonl`
- Trace WAL scellée (`wal/wt-reaper.log`)
- Entrée WAL NEXUS horodatée

## Règles

### 1. Vérification de merge avant clôture

Le reaper vérifie que la branche est soit mergée dans `main`, soit archivée (`archive/<branche>`). Sinon, il refuse la clôture et signale le risque.

### 2. Nettoyage physique

Suppression des jonctions NTFS créées par `worktree-zero-copy-hydrator` et des fichiers `.tmp` résiduels.

### 3. Restitution du bail

Le bail est rendu dans `leases.jsonl` avec l'horodatage de clôture.

### 4. Trace WAL

Chaque clôture est inscrite dans le WAL avec le statut (succès, bloqué, annulé).

## Script d'investigation

`scripts/reap.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_lifecycle_reaper.ps1` — créer un worktree mergé, exécuter le reaper, vérifier la restitution du bail.

## Probes

- Zéro worktree clôturé sans vérification de merge
- Zéro bail fantôme dans `leases.jsonl` après clôture

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-lifecycle-reaper action=reap timestamp=<ISO> worktree=<PATH> branch=<BRANCH> merged=<bool> bail_restituted=<bool>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-PR-LIFECYCLE-GATE
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
