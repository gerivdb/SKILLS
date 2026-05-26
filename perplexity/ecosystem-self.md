---
name: ecosystem-self
description: "Self-learning, semantic cache, META-CLUSTER GRAPH, cosine similarity. Use when user mentions 'apprentissage interne', 'cache sémantique', 'META-CLUSTER'."
---
|
# Ecosystem Self

## Domaine et périmètre

Ce skill couvre les mécanismes d'**apprentissage interne** de l'écosystème gerivdb :
- Cache sémantique (mise en cache des réponses par similarité)
- META-CLUSTER GRAPH (graphe de clusters sémantiques inter-dépôts)
- Similarité cosinus pour la déduplication et la recherche
- Auto-amélioration des réponses basée sur l'historique

## Méthodologie

### Phase 1 : Collecte
- Récupérer les interactions passées (prompts, réponses, feedback).
- Générer les embeddings (nomic-embed-text, 768-dim).
- Construire/mettre à jour le META-CLUSTER GRAPH.

### Phase 2 : Analyse
- Calculer la similarité cosinus entre la requête actuelle et le cache.
- Identifier les clusters pertinents (seuil : cosinus ≥ 0.85).
- Détecter les doublons et les contradictions.

### Phase 3 : Réponse
- Si cache hit (similarité ≥ 0.85) : servir la réponse mise en cache.
- Si cache miss : générer une nouvelle réponse, la stocker avec son embedding.
- Mettre à jour le graphe de clusters.

## Règles de décision
- **Règle 1** : Seuil de similarité cosinus = 0.85 (au-dessus = cache hit).
- **Règle 2** : Le cache sémantique a une TTL de 7 jours.
- **Règle 3** : Les contradictions détectées déclenchent une alerte [HYPOTHÈSE_NON_CONFIRMÉE].

## Format de sortie

```markdown
## Résultat Self-Learning
- Cache : [hit | miss]
- Similarité : [X.XX]
- Cluster : [nom]
- Réponse : [contenu]
```

## Exemples d'utilisation
- "Vérifie si cette question a déjà été traitée" → Recherche sémantique.
- "Mets à jour le META-CLUSTER GRAPH" → Recalculer les clusters.
- "Détecte les contradictions dans le cache" → Analyser les écarts.

## Intégration avec l'écosystème
- Dépôts concernés : BRAIN, NEXUS, VDB
- Couche EECS : L5_META
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
