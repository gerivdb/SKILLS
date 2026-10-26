---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_GMSG_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/git-merge-safety-gate/SKILL.md
---

# Skill — git-merge-safety-gate

## Objectif

Remplacer les hésitations manuelles avant suppression de branche par un test déterministe. Exécute `git branch --merged main` et, si la branche est déjà mergée, recommande l'utilisation du skill `agent-worktree-pruner`. Couche CRUD — opération Read + Décision.

## Déclencheur

- `git-merge-safety-gate`, `branche mergée`, `supprimer branche`, `git branch --merged main`, `agent-worktree-pruner`
- Avant toute tentative de suppression de branche feature ou worktree

## Entrées

- `branch_name`: nom de la branche à vérifier (obligatoire)
- `repo_path`: chemin du dépôt git (optionnel, défaut : répertoire courant)
- `base_branch`: branche de référence (défaut : `main`)

## Sorties

- Rapport : `branch_name`, `is_merged` (bool), `merged_into` (branche), `recommendation` (`prune` ou `keep`)
- Code de sortie : 0 = mergée (prunable), 1 = non mergée (à conserver), 2 = erreur

## Règles

### 1. Test déterministe obligatoire

Exécuter `git branch --merged <base_branch>` depuis la racine du dépôt. Si le nom de la branche apparaît dans la sortie, elle est mergée et peut être supprimée.

### 2. Interdiction de suppression sans test

Jamais supprimer une branche feature sans avoir d'abord exécuté le test de fusion. Une hésitation manuelle doit être résolue par ce skill.

### 3. Recommandation conditionnelle

- Si `is_merged = true` → recommander `agent-worktree-pruner` pour nettoyer le worktree physique et l'entrée agent-manager.json
- Si `is_merged = false` → recommander de conserver la branche et d'investiguer pourquoi elle n'est pas mergée

## Script d'investigation

`scripts/merge_safety_gate.ps1` — voir ci-dessous.

## Tests

- `tests/test_git_merge_safety_gate.ps1` — créer une branche mergée et une non mergée, vérifier le code de sortie.

## Probes

- Zéro branche mergée supprimée sans test préalable
- Zéro branche non mergée supprimée par erreur

## WAL NEXUS

```
[WAL_NEXUS] skill=git-merge-safety-gate action=check_merged timestamp=<ISO> branch=<BRANCH> is_merged=<bool> recommendation=<prune|keep>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed