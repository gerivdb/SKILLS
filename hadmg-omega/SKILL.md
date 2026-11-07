---
name: hadmg-omega
description: Méta-méta-architecture HADMG-Ω pour l'écosystème gerivdb. Observe les patterns d'intégration, rétropropage les échecs, régularise les worktrees stagnants, apprend des séquences récurrentes et optimise automatiquement. À utiliser pour l'audit architectural, la détection de patterns récurrents, la régularisation des worktrees, l'apprentissage de méta-connaissances et l'optimisation des cycles d'intégration.
---

# HADMG-Ω — Méta-Méta-Architecture

## Overview

HADMG-Ω est l'étage N+4 de l'écosystème gerivdb. Il ajoute 5 mécanismes d'auto-apprentissage au-dessus de la Méta-Architecture de Relaxation Causale (MRC) :

1. **Observateur de patterns** — détecte les séquences récurrentes d'échec/succès
2. **Rétropropagateur (R24)** — fait remonter les échecs d'intégration vers les spécifications
3. **Régularisateur (R25)** — associe un coût aux worktrees non fusionnés après N cycles
4. **Apprenti par patterns (R26)** — abstrait les séquences récurrentes en anti-patterns documentés
5. **Auto-optimisateur** — propose des optimisations structurelles basées sur les observations

## When to Use

- Audit architectural d'un worktree ou d'un pattern récurrent
- Détection de blocages d'intégration worktree → main
- Analyse causale des échecs de fusion
- Apprentissage de méta-connaissances à partir de l'historique git
- Régularisation des worktrees stagnants
- Optimisation des cycles d'intégration

## Workflow

### Step 1: Observateur de patterns

```bash
# Lister les worktres actifs et leur âge
git worktree list --porcelain

# Détecter les branches non fusionnées depuis N jours
git branch -r --no-merged main

# Analyser les commits uniques par branche
git log origin/main..HEAD --oneline
```

### Step 2: Rétropropagateur (R24)

Si un worktree échoue à l'intégration après N cycles :
1. Identifier le PRD/INTENT/ADR source
2. Mettre à jour le template pour éviter le pattern d'échec
3. Documenter l'anti-pattern dans `PRD/META-ARCHITECTURE/anti-patterns.md`

### Step 3: Régularisateur (R25)

Calculer le coût de régularisation :
```
cost = (days_since_creation * weight_age) + (commits_unique * weight_commits) + (files_changed * weight_files)
```

Si `cost > threshold` → action automatique : fusion ou archivage.

### Step 4: Apprenti par patterns (R26)

Détecter les séquences récurrentes :
1. Collecter l'historique des commits et des PRs
2. Extraire les motifs récurrents (keywords, fichiers modifiés, auteurs)
3. Abstraire en primitives et anti-patterns
4. Stocker dans `references/learned-patterns.md`

### Step 5: Auto-optimisateur

Proposer des optimisations :
- Simplification de PRD trop volumineux
- Fusion de worktrees similaires
- Archivage de branches mortes
- Mise à jour des dépendances

## Resources

### references/

- `references/learned-patterns.md` — Patterns appris par R26, anti-patterns documentés
- `references/relaxation-theory.md` — Formalisation mathématique de la convergence worktree → main
- `references/causal-algebra.md` — Algèbre des intégrations, bisimulation entre modèles
- `references/meta-ontology.md` — Relations entre modèles causaux
