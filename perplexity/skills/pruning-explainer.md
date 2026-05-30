---
name: pruning-explainer
description: "Pruning in dev and Git, git remote prune, optimization. Use when user mentions 'pruning', 'élagage', 'git remote prune'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
|
# Pruning Explainer

Domaine et périmètre

Ce skill couvre les techniques d'élagage (pruning) dans le développement et Git.

Méthodologie

Phase 1 : Identification
- Déterminer le contexte exact de la demande.
- Lister les dépôts et branches concernés.
- Vérifier les prérequis (accès Git, CI).

Phase 2 : Analyse
- Inspecter les branches obsolètes avec `git remote prune origin --dry-run`.
- Identifier les dépendances inutilisées dans le code.
- Appliquer les règles de décision.

Phase 3 : Action
- Proposer une commande concrète (ex. `git remote prune origin`).
- Nettoyer les imports et dépendances fantômes.
- Tagger selon la conformité NEXUS.

Règles de décision
- Règle 1 : Toujours faire un dry-run avant un prune destructif.
- Règle 2 : Les branches mergées depuis plus de 30 jours peuvent être supprimées.
- Règle 3 : Toute suppression sur un dépôt P0 nécessite une validation.

Format de sortie

```markdown
## Diagnostic
- Branches obsolètes : ...
- Dépendances inutilisées : ...

## Recommandation
- Commande : `git remote prune origin`
- Impact : ...
```

Exemples d'utilisation
- "Nettoie les branches obsolètes sur NEXUS" → `git remote prune origin`
- "Qu'est-ce que le pruning en deep learning ?" → Expliquer l'élagage de modèles.

Intégration avec l'écosystème
- Dépôts concernés : tous
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS]
