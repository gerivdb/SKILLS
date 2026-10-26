---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_WPA_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-precommit-armorer/SKILL.md
---

# Skill — worktree-precommit-armorer

## Objectif

Armement immédiat des garde-fous Git dans le nouveau worktree. Le `setup-script.ps1` configure `core.hooksPath` pour pointer vers le système de sécurité central (`.githooks` du repo maître), interdisant tout commit invalide dès la première seconde : encodage CP1252, fichiers interdits, pollution de l'index. Couche Worktree Engineering — opération de sécurisation.

## Déclencheur

- `worktree-precommit-armorer`, `armement worktree`, `githooks worktree`, `core.hooksPath`
- À chaque création de worktree via `wt:spawn-clean` ou `agent_manager worktree`

## Entrées

- `worktree_path`: chemin physique du nouveau worktree (défaut : `$env:WORKTREE_PATH`)
- `repo_path`: racine du dépôt maître parent (défaut : `$env:REPO_PATH`)

## Sorties

- Configuration `core.hooksPath` appliquée dans le worktree
- Entrée WAL NEXUS horodatée

## Règles

### 1. Armement systématique

Tout worktree créé doit pointer ses hooks Git vers le système central du repo maître. Aucun commit ne doit pouvoir sortir d'un worktree sans passer par les hooks de sécurité.

### 2. Encodage CP1252

Les hooks bloquent tout fichier contenant des caractères Unicode non-CP1252 (émojis, tirets longs, etc.).

### 3. Fichiers interdits

Les hooks bloquent tout fichier situé dans des chemins interdits (FORBIDDEN_PATHS du manifeste multi-repo-governance).

### 4. Interdiction de contourner

Aucun worktree ne doit pouvoir désactiver ses hooks sans autorisation explicite HITL.

## Script d'investigation

`scripts/armor.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_precommit_armorer.ps1` — créer un worktree, vérifier que `core.hooksPath` pointe vers le repo maître.

## Probes

- 100% des worktraits créés ont `core.hooksPath` configuré
- Zéro commit invalide provenant d'un worktree

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-precommit-armorer action=armor timestamp=<ISO> worktree=<PATH> hooks_path=<PATH>
```

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
