# Skill: ctulu-pagerank-runner

## Contexte
Calcule le Personalized PageRank sur le graphe écosystème. Les nœuds strate L0/L1 reçoivent un poids 2× pour refléter leur importance architecturale.

## Outil CTULU
- **Package**: `pagerank_runner` (PRD-082)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\pagerank-runner\`
- **CLI**: `pagerank-runner --graph <graphml> --alpha 0.85 --out scores/ [--dry-run] [--wal] [--output json|text]`

## Contrat CLI (PRD-019)
```bash
pagerank-runner --graph graphs/graph_20260616.graphml --alpha 0.85 --out scores/ --output json
```

## Paramètres
| Paramètre | Défaut | Description |
|---|---|---|
| `--graph` | requis | Path vers fichier GraphML |
| `--alpha` | 0.85 | Facteur d'amortissement (damping) |
| `--out` | `scores/` | Répertoire de sortie |

## Personnalisation
- Nœuds L0/L1: poids 2× dans le vecteur de personnalisation
- Algorithme: `networkx.pagerank()` avec `personalization=` dict
- Scores normalisés (somme = 1.0)

## Sortie JSON
```json
{
  "computed_at": "2026-06-16T02:30:00",
  "alpha": 0.85,
  "node_count": 150,
  "scores": [
    {"node_id": "repo:BRAIN", "score": 0.045231},
    {"node_id": "repo:FLUENCE", "score": 0.032100}
  ]
}
```

## Anti-patterns
- Ne JAMAIS utiliser alpha < 0.50 (convergence instable)
- Ne JAMAIS calculer PageRank sans graphe valide
- Ne JAMAIS modifier les poids L0/L1 sans recalcul
