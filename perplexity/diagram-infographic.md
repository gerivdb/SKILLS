---
name: diagram-infographic
description: "Infographics, KPI cards, mind maps, layered architecture. Use when user mentions 'infographie', 'KPI', 'carte mentale', 'architecture'."
---
|
# Diagram Infographic

## Domaine et périmètre

Ce skill génère des **infographies et visualisations synthétiques** :
- KPI cards (cartes de métriques clés)
- Mind maps (cartes mentales hiérarchiques)
- Architecture en couches (stack technique)
- Diagrammes en ASCII art pour intégration chat

## Méthodologie

### Phase 1 : Analyse du contenu
- Identifier les données à visualiser (métriques, hiérarchie, relations).
- Choisir le format approprié (KPI card, mind map, couches ASCII).
- Définir la palette (emojis, caractères ASCII, indentation).

### Phase 2 : Générer l'infographie
- Construire la visualisation en ASCII art ou Markdown structuré.
- Formater les KPI (valeur, tendance, seuil).
- Organiser la mind map (racine → branches → feuilles).

### Phase 3 : Livraison
- Intégrer dans la réponse Markdown.
- Proposer des variantes si pertinent.
- Documenter les choix de visualisation.

## Règles de décision
- **Règle 1** : Privilégier l'ASCII art pour la compatibilité chat.
- **Règle 2** : Les KPI cards doivent inclure valeur + tendance (↑↓→).
- **Règle 3** : Les mind maps sont limitées à 3 niveaux de profondeur.

## Format de sortie

```
┌─────────────────────────────┐
│  📊 KPI Card                │
│  Valeur : [X] (±[Y]%)       │
│  Seuil  : [Z]               │
│  Tendance : ↑|↓|→           │
└─────────────────────────────┘
```

## Exemples d'utilisation
- "Crée une KPI card pour la santé de l'écosystème" → Générer.
- "Génère une mind map de l'architecture NEXUS" → Construire.
- "Visualise le stack technique en ASCII" → Diagramme.

## Intégration avec l'écosystème
- Dépôts concernés : ECOS-VISION, documentation
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS]
