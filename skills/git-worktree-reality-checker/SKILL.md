---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_GWRC_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/git-worktree-reality-checker/SKILL.md
---

# Skill — git-worktree-reality-checker

## Objectif

Interdire formellement à un agent d'affirmer qu'un worktree "n'existe pas" sur un simple appel CLI négatif. Applique la **règle de la double preuve** : un worktree existe si l'une des trois sources de vérité le confirme. Couche CRUD — opération Read + Vérification.

## Déclencheur

- `git-worktree-reality-checker`, `vérifier worktree`, `worktree existe`, `double preuve worktree`
- Avant toute conclusion d'absence sur un worktree Agent Manager

## Entrées

- `worktree_path`: chemin du worktree à vérifier (obligatoire)
- `worktree_id`: ID du worktree dans agent-manager.json (optionnel)
- `project_id`: `RAGX` ou `SKILLS` (optionnel, défaut SKILLS)

## Sorties

- Rapport JSON : `exists`, `sources` (dossier physique, git worktree, agent-manager.json), `confirmed_by` (liste des sources positives)
- Recommandation : `treat_as_existing` ou `treat_as_absent`

## Règles

### 1. Règle de la double preuve

$$\text{Existence} = (\text{dossier physique}) \lor (\text{déclaré dans Git}) \lor (\text{déclaré dans agent-manager.json})$$

Si l'une des trois est vraie, le worktree existe et doit être traité comme tel.

### 2. Interdiction absolue

Jamais conclure "n'existe pas" sur la seule base d'un appel CLI négatif (ex: `git worktree list` vide depuis un mauvais CWD).

### 3. Sources de vérité

| Source | Méthode de vérification |
|--------|------------------------|
| Dossier physique | `Test-Path` sur le chemin du worktree |
| Git | `git worktree list` depuis la racine du dépôt |
| agent-manager.json | Lecture du fichier JSON, recherche par ID ou path |

## Script d'investigation

`scripts/verify_worktree_reality.ps1` — voir ci-dessous.

## Tests

- `tests/test_git_worktree_reality_checker.ps1` — créer un worktree factice, vérifier qu'il est détecté par au moins une source.

## Probes

- Zéro worktree existant déclaré "absent" par erreur
- Zéro appel CLI négatif utilisé comme preuve d'absence

## WAL NEXUS

```
[WAL_NEXUS] skill=git-worktree-reality-checker action=verify timestamp=<ISO> path=<PATH> exists=<bool> sources=<liste>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
