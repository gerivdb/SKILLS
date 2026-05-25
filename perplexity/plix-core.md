---
name: plix-core
description: "PLIX video substrate, CODEC-243, PLAYER-243, PLIXVAULT, OCTOPUS, BitNet mapping. Use when user mentions 'PLIX', 'CODEC-243', 'PLAYER-243', 'PLIXVAULT', 'OCTOPUS'."
---
|
# PLIX Core

## Domaine et périmètre

PLIX est le **substrat vidéo ternaire** de l'écosystème. Ce skill couvre :
- PLIX (substrat brut, PLIXVAULT, API)
- CODEC-243 (quantification 2D, RHT, stochastic rounding)
- PLAYER-243 (lecteur/navigateur PLIXVAULT)
- VEC-243 (certification vectorielle)
- Le mapping BitNet b1.58 et l'architecture Adobe-like

## Méthodologie

### Phase 1 : Compréhension du besoin
- Identifier le composant PLIX concerné.
- Vérifier l'état d'avancement (Phases 0-8).
- Consulter le PRD PLIX Suite v2.

### Phase 2 : Analyse technique
- Expliquer le fonctionnement (pentades, frames, GOP).
- Faire le lien avec le matériel Z600 (CPU-only, 24 GB RAM).
- Proposer des optimisations (compression, navigation).

## Règles de décision
- **Règle 1** : PLIX est ternaire (3⁵ = 243 états par canal) — ne pas confondre avec du binaire.
- **Règle 2** : Toujours vérifier la compatibilité CPU (pas de GPU requis).
- **Règle 3** : Les benchmarks de compression sont la métrique clé.

## Format de sortie

```markdown
## Récapitulatif PLIX
- Dépôt : ...
- Statut : ...
- Prochaine étape : ...
```

## Exemples d'utilisation
- "Fais un récapitulatif de PLIX" → Structure et roadmap.
- "Explique le mapping BitNet dans PLIX" → Décrire les pentades.
- "Optimise CODEC-243 pour le Z600" → Proposer des améliorations.

## Intégration avec l'écosystème
- Dépôts concernés : PLIX, CODEC-243, PLAYER-243, VEC-243, GOV-243
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [DÉRIVÉ]
