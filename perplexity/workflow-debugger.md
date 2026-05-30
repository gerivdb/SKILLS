---
name: workflow-debugger
description: "GitHub Actions debugging: startup_failure, permissions, PYTHONPATH. Use when user mentions 'startup_failure', 'permissions', 'PYTHONPATH'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# Workflow Debugger

## Domaine et périmètre

Ce skill couvre le **débogage des workflows GitHub Actions** :
- Diagnostic des `startup_failure` (échec rapide, souvent permissions)
- Vérification des scopes GITHUB_TOKEN et Settings Actions
- Résolution des problèmes PYTHONPATH et dépendances Python
- Analyse des logs d'exécution (stdout, stderr, exit codes)

## Méthodologie

### Phase 1 : Diagnostic rapide
- Vérifier le temps d'exécution : < 2s = problème de permissions Settings.
- Contrôler les scopes du GITHUB_TOKEN (repo, workflow, admin:org).
- Inspecter les logs du run échoué.

### Phase 2 : Analyse approfondie
- Vérifier le PYTHONPATH dans le workflow.
- Contrôler les dépendances (requirements.txt, pip install).
- Tester localement si possible (act ou docker).

### Phase 3 : Correction
- Proposer les corrections (ajuster les permissions, fixer le PYTHONPATH).
- Créer une PR avec les changements.
- Relancer le workflow pour valider.

## Règles de décision
- **Règle 1** : Un startup_failure en < 2s = toujours un problème de permissions Settings.
- **Règle 2** : Le GITHUB_TOKEN par défaut n'a pas accès aux dépôts d'autres orgs.
- **Règle 3** : Les workflows Python doivent définir explicitement le PYTHONPATH.

## Format de sortie

```markdown
## Diagnostic Workflow
- Workflow : [nom]
- Erreur : [type]
- Cause : [permissions | PYTHONPATH | dépendances | autre]
- Correction : [description]
- PR : [lien]
```

## Exemples d'utilisation
- "Le workflow IRIS échoue au startup" → Vérifier les permissions.
- "PYTHONPATH introuvable dans le workflow" → Corriger le path.
- "Débogue le workflow kronos-qualify" → Analyser les logs.

## Intégration avec l'écosystème
- Dépôts concernés : IRIS, KRONOS, FLUX, Gitnote
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS]
