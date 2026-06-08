---
name: nexus-deps
description: "Shadow dependency detection, dependency matrix, inter-layer coupling. Use when user mentions 'shadow dependency', 'matrice dépendances', 'inter-strates'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritCheckDependencies
---
# NEXUS Deps

Domaine et périmètre

Ce skill couvre la détection et la gestion des dépendances inter‑dépôts dans l'écosystème gerivdb.

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
- "Détecte les dépendances fantômes entre PLIX et CODEC-243" → Scanner les imports.
- "Génère la matrice de dépendances inter‑strates L1‑L5" → Créer un tableau.
- "Quels dépôts dépendent de gateway GPU ?" → Lister les références.

Intégration avec l'écosystème
- Dépôts concernés : tous
- Couche EECS : L1 à L5 selon le contexte
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS], [HORS_NEXUS]
```
