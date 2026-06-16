# Skill: ctulu-graph-delta-exporter

## Contexte
Calcule le diff entre deux snapshots du graphe écosystème. Détecte les nœuds/arêtes ajoutés/supprimés/modifiés. Zéro faux positifs sur graphes identiques.

## Outil CTULU
- **Package**: `graph_delta_exporter` (PRD-082)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\graph-delta-exporter\`
- **CLI**: `graph-delta-exporter --t0 <graphml> --t1 <graphml> --out NEXUS/graphs/deltas/ [--dry-run] [--wal] [--output json|text]`

## Contrat CLI (PRD-019)
```bash
graph-delta-exporter --t0 graphs/graph_t0.graphml --t1 graphs/graph_t1.graphml --out NEXUS/graphs/deltas/ --output json
```

## Types de delta
| Type | Description |
|---|---|
| `added_nodes` | Nœuds présents dans t1 mais pas t0 |
| `removed_nodes` | Nœuds présents dans t0 mais pas t1 |
| `added_edges` | Arêtes présentes dans t1 mais pas t0 |
| `removed_edges` | Arêtes présentes dans t0 mais pas t1 |
| `modified_nodes` | Nœuds dans les deux mais attributs différents |

## Sortie JSON
```json
{
  "computed_at": "2026-06-16T02:30:00",
  "t0": "graphs/graph_t0.graphml",
  "t1": "graphs/graph_t1.graphml",
  "delta": {
    "added_nodes": ["repo:NEW-REPO"],
    "removed_nodes": ["repo:OLD-REPO"],
    "added_edges": [{"source": "repo:A", "target": "repo:B"}],
    "removed_edges": [],
    "modified_nodes": ["repo:CHANGED"]
  }
}
```

## Anti-patterns
- Ne JAMAIS comparer des graphes de formats différents
- Ne JAMAIS utiliser un delta avec faux positifs (vérifier t0=t1 d'abord)
- Ne JAMAIS écraser un delta existant (immuabilité)
