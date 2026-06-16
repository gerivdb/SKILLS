# Skill: ctulu-louvain-clusterer

## Contexte
Détection de communautés Louvain sur le graphe écosystème. Produit les partitions de clusters avec vérification de stabilité (< 5% variation run-to-run).

## Outil CTULU
- **Package**: `louvain_clusterer` (PRD-082)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\louvain-clusterer\`
- **CLI**: `louvain-clusterer --graph <graphml> --out partitions/ [--dry-run] [--wal] [--output json|text]`

## Contrat CLI (PRD-019)
```bash
louvain-clusterer --graph graphs/graph_20260616.graphml --out partitions/ --output json
```

## Algorithme
- **Principal**: `python-louvain` (`community.best_partition()`)
- **Fallback**: `networkx.algorithms.community.greedy_modularity_communities`
- **Stabilité**: N=5 runs, variation < 5% cible

## Sortie JSON
```json
{
  "computed_at": "2026-06-16T02:30:00",
  "node_count": 150,
  "community_count": 8,
  "avg_variation": 0.0234,
  "partitions": {
    "repo:BRAIN": 0,
    "repo:FLUENCE": 0,
    "repo:ONTOLOGY": 1
  }
}
```

## Anti-patterns
- Ne JAMAIS utiliser des partitions avec variation > 5%
- Ne JAMAIS clusteriser un graphe disconnected sans composantes connexes
- Ne JAMAIS écraser des partitions existantes (immuabilité)
