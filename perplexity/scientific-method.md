---
name: scientific-method
description: "Poincaré, Feynman, scientific method, hypothesis validation, NEXUS protocol. Use when user mentions 'Poincaré', 'Feynman', 'méthode scientifique', 'hypothèse'."
---
|
# Scientific Method

Domaine et périmètre

Ce skill couvre l'application de la méthode scientifique à l'écosystème gerivdb.

Méthodologie

Phase 1 : Identification
- Déterminer le contexte exact de la demande.
- Lister les dépôts et fichiers concernés.
- Vérifier les prérequis (tokens, permissions, CI).

Phase 2 : Analyse
- Collecter les données via mcp_github ou ecos CLI.
- Appliquer les règles de décision du domaine.
- Identifier les anomalies ou les actions nécessaires.

Phase 3 : Action
- Proposer une action concrète (commande, PR, modification de config).
- Documenter la justification.
- Tagger selon la conformité NEXUS.

Règles de décision
- Règle 1 : Toujours vérifier l'état du CI avant de proposer une modification.
- Règle 2 : Les dépendances fantômes (shadow deps) doivent être enregistrées dans ECOS_ROOT.
- Règle 3 : Toute action sur un dépôt P0_CONSTITUTIONAL nécessite une validation φ‑CPS.

Format de sortie

```markdown
## Diagnostic
- État actuel : ...
- Anomalies détectées : ...

## Recommandation
- Action : ...
- Commande : `...`
- Impact : ...
```

Exemples d'utilisation
- "Applique la méthode de Feynman à ce problème" → Décomposer et valider.
- "Vérifie l'hypothèse sur la latence de PLIX" → Proposer un protocole de test.

Intégration avec l'écosystème
- Dépôts concernés : NEXUS, BRAIN
- Couche EECS : L5_META
- Tags NEXUS : [HYPOTHÈSE_NON_CONFIRMÉE], [CONFORME_NEXUS]
