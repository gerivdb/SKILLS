---
name: multi-repo-syncer
description: "Cross-repo synchronization, KIVA, NEXUS, gateway GPU, ECOS_ROOT. Use when user mentions 'sync multi-dépôts', 'KIVA', 'NEXUS', 'gateway GPU'."
---
|
# Multi-Repo Syncer

Domaine et périmètre

Ce skill couvre les opérations de synchronisation entre dépôts au sein de l'écosystème gerivdb.

Méthodologie

Phase 1 : Identification
- Déterminer le contexte exact de la synchronisation.
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
- "Synchronise les tags entre NEXUS et DevTools" → Proposer un script de sync.
- "Vérifie les incohérences entre ECOS_ROOT et les dépôts réels" → Lancer un audit.
- "Propager une mise à jour de gateway GPU vers tous les dépôts" → Générer des PR.

Intégration avec l'écosystème
- Dépôts concernés : NEXUS, KIVA-CLI, gateway GPU, ECOS_ROOT
- Couche EECS : L1 à L5 selon le contexte
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS], [HORS_NEXUS]
```

---
