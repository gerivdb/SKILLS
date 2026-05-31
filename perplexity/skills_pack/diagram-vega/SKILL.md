---
name: diagram-vega
description: "Vega-Lite charts, data visualization, analytics. Use when user mentions 'Vega-Lite', 'graphique', 'data analytics'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
# Diagram Vega

## Domaine et périmètre

Ce skill génère des **graphiques de données** via Vega-Lite :
- Graphiques en barres, lignes, aires, scatter plots
- Visualisations de métriques écosystème (φ-CPS, CI status, activité)
- Dashboards de données (multi-graphiques)
- Export JSON pour intégration dans des applications

## Méthodologie

### Phase 1 : Préparation des données
- Identifier les données à visualiser (tableau, JSON, CSV).
- Définir les axes (X, Y) et les dimensions (couleur, taille).
- Choisir le type de marque (bar, line, point, area).

### Phase 2 : Écriture Vega-Lite
- Construire la spécification JSON Vega-Lite.
- Définir le `mark`, les `encoding`, et les `transform`.
- Ajouter les titres, légendes, et annotations.

### Phase 3 : Livraison
- Encadrer dans un code fence `json` (spécification Vega-Lite).
- Expliquer les choix de visualisation.
- Proposer des alternatives (log scale, faceting).

## Règles de décision
- **Règle 1** :Toujours inclure un titre et des labels d'axes.
- **Règle 2** : Les couleurs sont sémantiques (vert = OK, rouge = erreur, jaune = warning).
- **Règle 3** : Limiter à 5 séries de données par graphique (au-delà, faceting).

## Format de sortie

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": "φ-CPS par dépôt",
  "mark": "bar",
  "encoding": {
    "x": {"field": "depot", "type": "nominal"},
    "y": {"field": "phi_cps", "type": "quantitative"},
    "color": {"field": "status", "type": "nominal"}
  }
}
```

## Exemples d'utilisation
- "Graphique des φ-CPS par dépôt" → Vega-Lite bar chart.
- "Évolution de l'activité GitHub dans le temps" → Line chart.
- "Scatter plot commits vs issues" → Scatter plot.
- "Dashboard de santé de l'écosystème" → Multi-graphiques.

## Intégration avec l'écosystème
- Dépôts concernés : ECOS-VISION, NEXUS, analytics
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS]
