---
name: wiki-mimir
description: "Wiki back-office, MIMIR, Atomic, project management, cross-repo docs. Use when user mentions 'wiki back-office', 'MIMIR', 'Atomic', 'projets'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
# Wiki Mimir

## Domaine et périmètre

Ce skill couvre le **back-office wiki** de l'écosystème gerivdb :
- MIMIR (système de gestion de connaissances)
- Atomic (structure atomique des documents)
- Gestion de projets cross-repo
- Documentation centralisée et inter-dépôts

## Méthodologie

### Phase 1 : Identification du besoin
- Déterminer le type d'action : créer, mettre à jour, rechercher, ou structurer.
- Identifier le dépôt ou projet concerné.
- Vérifier l'existence de la documentation dans MIMIR.

### Phase 2 : Action
- Créer ou mettre à jour la documentation au format Atomic.
- Structurer selon les standards MIMIR (titre, contexte, contenu, références).
- Lier aux dépôts et ADR pertinents.

### Phase 3 : Validation
- Vérifier la cohérence avec l'ontologie (ONTOLOGY).
- S'assurer que les liens cross-repo fonctionnent.
- Tagger selon la conformité NEXUS.

## Règles de décision
- **Règle 1** : Toute documentation doit suivre le format Atomic (titre, contexte, contenu, refs).
- **Règle 2** : Les documents MIMIR doivent référencer les ADR applicables.
- **Règle 3** : La documentation obsolète (> 90 jours sans mise à jour) est marquée [À_REVOIR].

## Format de sortie

```markdown
## Document MIMIR
- Titre : [titre]
- Format : Atomic
- Dépôts liés : [liste]
- Dernière MAJ : [date]
- Statut : [actif | à_revoir | obsolète]
```

## Exemples d'utilisation
- "Crée la doc pour le projet PLIX" → Structurer dans MIMIR.
- "Met à jour la doc de la Triade" → Mettre à jour les sections.
- "Quels docs sont obsolètes ?" → Scanner et lister.

## Intégration avec l'écosystème
- Dépôts concernés : MIMIR, NEXUS, documentation
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS]
