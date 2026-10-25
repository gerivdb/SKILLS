---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WTG_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-gap-detector/SKILL.md
---

# Skill — worktree-gap-detector

## Objectif

Détecte les worktrees "fuites" : idle depuis trop longtemps avec branche non mergée, ou worktrees avec `ahead > 0` non pushés depuis plusieurs jours. Génère des recommandations d'action (`closeout`, `crush`, `merge`, `push`). Couche CRUD — opération Read + Alerte.

## Déclencheur

- `worktree-gap-detector`, `fuites worktrees`, `worktrees stagnants`
- Vérification périodique avant clôture de session

## Entrées

- `idle_threshold_hours`: seuil d'inactivité en heures (défaut : 24)
- `unmerged_threshold_days`: seuil de branche non mergée en jours (défaut : 3)
- `project_filter`: `RAGX` ou `SKILLS` (optionnel)

## Sorties

- Liste des worktrees à risque avec recommandation : `closeout`, `crush`, `merge`, `push`
- Nombre total de worktrees à traiter

## Règles

### 1. Détection des fuites

- Worktree idle + branche non mergée > `idle_threshold_hours` → recommandation `closeout`
- Worktree avec `ahead > 0` et `behind = 0` depuis > `unmerged_threshold_days` → recommandation `push`
- Worktree sans session depuis > 24h → recommandation `crush`

### 2. Surcouche GeriCode/ACT

Signale si un worktree en fuite détient un verrou ACT ou modifie des fichiers de citoyen (GeriCode L2-PLATFORM).

## Script d'investigation

`scripts/detect-gaps.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_gap_detector.ps1` — créer des worktrees avec différents états, vérifier les recommandations.

## Probes

- Zéro worktree en fuite non détecté
- Chaque worktree à risque a une recommandation explicite

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-gap-detector action=detect_gaps timestamp=<ISO> project=<PROJECT> idle=<n> unmerged=<m> orphaned=<k> recommendations=<list>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
