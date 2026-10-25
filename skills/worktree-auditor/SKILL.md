---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTA_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-auditor/SKILL.md
---

# Skill — worktree-auditor

## Objectif

Audite systématiquement tous les worktrees managés d'Agent Manager : état (idle/busy/retry/offline/waiting), branche, avance/délai sur `main`, âge de la dernière activité, présence de fichiers non committés. Détecte les worktrees orphelins (sans session), stagnants (idle > 24h) et dérivants (branche non pushée). Couche CRUD — opération Read.

## Déclencheur

- `worktree-auditor`, `audit worktrees`, `état worktrees`, `worktrees orphelins`
- Avant toute opération de closeout ou de purge massive

## Entrées

- `project_filter`: optionnel (`RAGX` ou `SKILLS`)
- `etat_filter`: optionnel (`idle`, `busy`, `retry`, `offline`, `waiting`)
- `age_max_hours`: seuil d'inactivité en heures (défaut : 24)

## Sorties

- Rapport JSON des worktrees avec `worktree_id`, `session_id`, `name`, `branch`, `state`, `ahead`, `behind`, `age_hours`, `has_uncommitted`, `orphan_flag`, `stagnant_flag`, `drifting_flag`
- Nombre de worktrees à risque

## Règles

### 1. Détection des états

- **Orphelin** : `session` absent ou `null` (coquille vide après stop de session)
- **Stagnant** : état `idle` depuis plus de `age_max_hours`
- **Dérivant** : `ahead > 0` et `behind = 0` (branche avec commits non pushés)

### 2. Surcouche GeriCode/ACT

Détecte si un worktree modifie des fichiers surveillés par ACT Protocol (`.kilo/bus/`, `beads.json`, signatures GPG) et signale le risque de collision avec l'extension `gerivdb.act-vscode`.

## Script d'investigation

`scripts/audit.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_auditor.ps1` — crée un worktree factice, vérifie qu'il est détecté avec les bons flags.

## Probes

- Zéro worktree orphelin non signalé
- Zéro worktree stagnant non signalé

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-auditor action=audit timestamp=<ISO> project=<PROJECT> worktrees=<n> orphans=<o> stagnants=<s> drifters=<d>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
