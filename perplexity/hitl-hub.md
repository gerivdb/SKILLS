---
name: hitl-hub
description: "HITL review, signal evaluation, workflow building, world-model review. Use when user mentions 'HITL', 'review signals', 'audit', 'workflow builder'."
---
|
# HITL Hub

## Domaine et périmètre

Ce skill couvre le **Human-In-The-Loop (HITL)** dans l'écosystème gerivdb :
- Review des signaux qualifiés par KRONOS (confidence HIGH/MEDIUM/LOW)
- Évaluation et approbation/rejet des signaux avant assimilation NEXUS
- Construction et maintenance des workflows de review
- Review du world-model (cohérence sémantique de l'écosystème)

## Méthodologie

### Phase 1 : Collecte des signaux
- Récupérer les signaux en attente de review depuis FLUX.
- Filtrer par priorité (HIGH d'abord, puis MEDIUM, LOW en dernier).
- Présenter le contexte (commit_sha, fragment, source).

### Phase 2 : Review
- Pour chaque signal : lire le diff, évaluer la pertinence.
- Décision : APPROVE, REJECT, ou REQUEST_MORE_INFO.
- Documenter la justification de chaque décision.

### Phase 3 : Promotion ou archivage
- Les signaux APPROVED → déplacer vers NEXUS/intelligence/signals/assimilated/.
- Les signaux REJECTED → archiver avec la raison.
- Mettre à jour le registre et les statistiques.

## Règles de décision
- **Règle 1** : Ne jamais approuver un signal sans avoir lu le diff complet.
- **Règle 2** : Les signaux HIGH doivent être traités en priorité (SLA : 24h).
- **Règle 3** : Un signal rejeté deux fois est définitivement écarté.

## Format de sortie

```markdown
## Session HITL
- Signaux reviewés : [N]
- Approuvés : [N]
- Rejetés : [N]
- En attente : [N]
```

## Exemples d'utilisation
- "Fais la revue HITL des signaux en attente" → Lister et approuver/rejeter.
- "Pourquoi le signal RS-001 a-t-il été rejeté ?" → Afficher l'historique.
- "Promeut tous les signaux HIGH approuvés" → Déplacer vers NEXUS.

## Intégration avec l'écosystème
- Dépôts concernés : FLUX, KRONOS, NEXUS, BRAIN
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
