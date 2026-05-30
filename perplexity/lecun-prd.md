---
name: lecun-prd
description: "Generate PRD from LeCun's positions, PLIX world model, Triade alignment. Use when user mentions 'PRD LeCun', 'plix world model', 'triade alignment'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# LeCun PRD

## Domaine et périmètre

Ce skill couvre la **génération de PRD** basé sur les positions de Yann LeCun :
- Génération de PRD alignés sur la vision LeCun (JEPA, world models, objective-driven AI)
- Application au projet PLIX (substrat vidéo ternaire)
- Alignement avec la Triade Cognitive (IRIS, KRONOS, FLUX)
- Contraintes matérielles Z600 (CPU-only, pas de GPU)

## Méthodologie

### Phase 1 : Analyse des positions LeCun
- Identifier les concepts clés : JEPA, world model, energy-based models.
- Évaluer la pertinence pour l'écosystème gerivdb.
- Mapper les concepts vers les composants existants (PLIX, CODEC-243, Triade).

### Phase 2 : Génération du PRD
- Structurer le PRD : contexte, objectifs, spécifications, contraintes.
- Intégrer les contraintes matérielles (Z600, CPU-only, 24 GB RAM).
- Aligner avec les ADR et standards NEXUS existants.

### Phase 3 : Validation
- Vérifier la cohérence avec les ADR constitutionnels.
- Évaluer la faisabilité technique sur le matériel cible.
- Tagger selon la conformité NEXUS.

## Règles de décision
- **Règle 1** : Le PRD doit mentionner explicitement les contraintes Z600 (pas d'AVX, CPU-only).
- **Règle 2** : Les références à JEPA doivent distinguer approche générative vs prédictive.
- **Règle 3** : Tout PRD > 10 Ko doit être externalisé (pas dans NEXUS directement).

## Format de sortie

```markdown
## PRD : [Titre]
- **Inspiration** : Yann LeCun — [concept]
- **Composant cible** : [PLIX | CODEC-243 | Triade | ...]
- **Contraintes matérielles** : Z600 (CPU-only, 24 GB RAM)
- **Conformité NEXUS** : [CONFORME_NEXUS | À_VALIDER_NEXUS]
```

## Exemples d'utilisation
- "Génère un PRD pour adapter JEPA à PLIX" → Structurer le document.
- "Crée un PRD pour le world model de la Triade" → Aligner IRIS/KRONOS/FLUX.
- "Évalue la faisabilité LeCun sur Z600" → Analyser les contraintes.

## Intégration avec l'écosystème
- Dépôts concernés : PLIX, NEXUS, BRAIN, CODEC-243
- Couche EECS : L5_META
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
