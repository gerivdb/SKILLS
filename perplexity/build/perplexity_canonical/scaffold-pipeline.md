---
name: scaffold-pipeline
description: "SCAFFOLD governance flow: issue→intent, WAL, constitutional validation, artifact cataloging. Use when user mentions 'SCAFFOLD', 'pipeline gouvernance', 'WAL', 'issue to intent'."
---
|

# scaffold-pipeline
|
# Scaffold Pipeline

Domaine et périmètre

Ce skill couvre le pipeline de gouvernance SCAFFOLD au sein de l'écosystème gerivdb.

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
- "Transforme cette issue en intention SCAFFOLD" → Générer le WAL.
- "Valide la conformité constitutionnelle de cette PR" → Appliquer les règles.

Intégration avec l'écosystème
- Dépôts concernés : NEXUS, GOVERNANCE-HUB
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]

