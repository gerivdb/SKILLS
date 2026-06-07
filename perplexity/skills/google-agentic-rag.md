---
name: google-agentic-rag
version: "1.0.0"
description: "Analyse des patterns Google Agentic RAG croisée avec SCO7/Selena/Alfred/Riddler. Produit un rapport de synthèse avec matrice de convergence, gaps identifiés, et recommandations d'adaptation. Utiliser quand l'utilisateur mentionne 'analyse RAG', 'patterns Google agentic', 'article Google RAG', 'cross-analysis agents'."
triggers:
  - "analyse RAG"
  - "patterns Google agentic"
  - "article Google RAG"
  - "cross-analysis agents"
  - "rapport analytique"
  - "SCO7 Selena Alfred Riddler"
layer: "L2_COGNITION"
nexusTags: ["CONFORME_NEXUS", "ANALYSIS"]
prerequisites:
  - "Accès à l'article source (URL ou texte)"
  - "Connaissance des agents SCO7, Selena, Alfred, Riddler"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — analyse croisée Google Agentic RAG"}
---

# GOOGLE-AGENTIC-RAG — Analyse croisée de patterns externes

## Domaine et périmètre

Ce skill analyse un article ou papier de recherche externe (ex: Google Agentic RAG) et produit un **rapport de synthèse croisé** avec les agents de l'écosystème gerivdb (SCO7, Selena, Alfred, Riddler).

## Méthodologie

### Phase 1 — Extraction des patterns

Lire l'article et identifier :
- Les patterns d'architecture (agents, pipeline, orchestration)
- Les innovations clés
- Les résultats revendiqués
- Les limitations non mentionnées

### Phase 2 — Mapping aux agents

Pour chaque pattern identifié, évaluer :

| Agent | Angle d'analyse |
|-------|-----------------|
| **SCO7** | Architecture technique, scalabilité, coût |
| **Selena** | Positionnement stratégique, marché, concurrence |
| **Alfred** | Risques, sécurité, conformité |
| **Riddler** | Failles logiques, biais, hypothèses cachées |

### Phase 3 — Matrice de convergence

Produire une matrice :

| Dimension | SCO7 | Selena | Alfred | Riddler | Consensus |
|-----------|------|--------|--------|---------|-----------|
| Architecture | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Scalabilité | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Sécurité | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Nouveauté | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

### Phase 4 — Gaps et recommandations

Identifier :
- Les patterns **exploités** (déjà implémentés)
- Les patterns **manquants** (à implémenter)
- Les patterns **incompatibles** (à adapter)

## Format de sortie

Le rapport suit la structure :
1. Synthèse exécutive
2. Analyse par agent (SCO7, Selena, Alfred, Riddler)
3. Matrice de convergence
4. Gaps identifiés
5. Recommandations consolidées

## Intégration

- **Dépôts** : SKILLS (rapport), REPORTS (détails)
- **Couche EECS** : L2_COGNITION
- **Tags NEXUS** : [CONFORME_NEXUS], [ANALYSIS]
