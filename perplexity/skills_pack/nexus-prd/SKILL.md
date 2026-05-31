---
name: nexus-prd
description: "Magistral PRD synthesis, ASCII diagrams, recommendations. Use when user mentions 'PRD magistral', 'synthèse', 'diagramme ASCII', 'recommandations'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
# NEXUS PRD

## Domaine et périmètre

Ce skill couvre la **synthèse magistrale de PRD** pour l'écosystème gerivdb :
- Génération de PRD complets et structurés
- Diagrammes ASCII intégrés (architecture, flux, séquence)
- Recommandations stratégiques basées sur les ADR et l'ontologie
- Synthèse multi-dépôts (PRD couvrant plusieurs composants)

## Méthodologie

### Phase 1 : Collecte du contexte
- Lire les ADR, EPICs et PRD existants liés au sujet.
- Consulter ONTOLOGY pour les termes métier.
- Identifier les contraintes (matérielles, architecturales, temporelles).

### Phase 2 : Génération du PRD
- Structurer : Contexte, Objectifs, Spécifications, Contraintes, Risques.
- Intégrer des diagrammes ASCII (architecture, flux de données).
- Aligner avec les standards NEXUS (RSS-v1, REPO-STANDARDS).

### Phase 3 : Recommandations
- Proposer des recommandations stratégiques.
- Évaluer la faisabilité (matériel, temps, complexité).
- Tagger selon la conformité NEXUS.

## Règles de décision
- **Règle 1** : Tout PRD doit référencer les ADR applicables.
- **Règle 2** : Les diagrammes ASCII sont privilégiés (lisibilité dans tout éditeur).
- **Règle 3** : Un PRD magistral couvre maximum 3 dépôts (au-delà, scinder).

## Format de sortie

```markdown
## PRD Magistral : [Titre]

### Contexte
[description]

### Diagramme ASCII
```
[diagramme]
```

### Spécifications
- ...

### Recommandations
1. ...
2. ...
```

## Exemples d'utilisation
- "Génère un PRD magistral pour la Triade" → Synthèse IRIS/KRONOS/FLUX.
- "Crée un diagramme ASCII de l'architecture NEXUS" → Générer et intégrer.
- "Quel est l'état des lieux de PLIX ?" → PRD synthétique.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, tous les dépôts gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS]
