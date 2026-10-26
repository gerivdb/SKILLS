---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_WZCH_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-zero-copy-hydrator/SKILL.md
---

# Skill — worktree-zero-copy-hydrator

## Objectif

Hydratation instantanée d'un worktree neuf via jonctions NTFS vers le cache partagé du repo maître (node_modules, .venv, etc.). Évite les 2-5 minutes d'`npm install` / `pip install` et la duplication de centaines de Mo sur le disque de la station Z600. Le `setup-script.ps1` du worktree exécute cette hydratation à la naissance de l'isolat. Couche Worktree Engineering — opération d'hydratation.

## Déclencheur

- `worktree-zero-copy-hydrator`, `hydrater worktree`, `zero-copy worktree`, `setup-script.ps1`
- À chaque création de worktree managé via `wt:spawn-clean` ou `agent_manager worktree`

## Entrées

- `worktree_path`: chemin physique du nouveau worktree (défaut : `$env:WORKTREE_PATH`)
- `repo_path`: racine du dépôt maître parent (défaut : `$env:REPO_PATH`)
- `cache_dirs`: répertoires à lier (défaut : `node_modules`, `.venv`, `.cache/pip`)

## Sorties

- Jonctions NTFS créées dans le worktree pointant vers le cache maître
- Rapport JSON : `hydrated_dirs`, `skipped_dirs`, `space_saved_mb`
- Entrée WAL NEXUS horodatée

## Règles

### 1. Zero-copy absoluto

Jamais de `npm install` / `pip install` à la création d'un worktree. Seules des jonctions NTFS (`mklink /J`) vers le cache partagé du repo maître.

### 2. Sécurité

Si une jonction existe déjà dans le worktree, la préserver (ne pas écraser). Si le répertoire source n'existe pas dans le maître, sauter et journaliser.

### 3. Surcouche GeriCode/ACT

Le worktree hydraté est immédiatement prêt à exécuter les tests et scripts sans latence d'installation, ce qui permet l'enrôlement immédiat dans `.kilo/bus/` et WAZAA.

## Script d'investigation

`scripts/hydrate.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_zero_copy_hydrator.ps1` — créer un worktree factice avec node_modules source, vérifier la jonction.

## Probes

- Hydratation < 200 ms par répertoire
- Zéro duplication d'espace disque

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-zero-copy-hydrator action=hydrate timestamp=<ISO> worktree=<PATH> dirs=<liste> space_saved_mb=<N>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
