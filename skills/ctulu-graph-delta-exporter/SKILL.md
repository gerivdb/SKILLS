# Skill: ctulu-graph-delta-exporter

## Contexte
Calcule le diff entre deux snapshots du graphe ecosysteme. Detecte les noeuds/aretes ajoutes/supprimes/modifies. Zero faux positifs sur graphes identiques.

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
| `added_nodes` | Noeuds presents dans t1 mais pas t0 |
| `removed_nodes` | Noeuds presents dans t0 mais pas t1 |
| `added_edges` | Aretes presentes dans t1 mais pas t0 |
| `removed_edges` | Aretes presentes dans t0 mais pas t1 |
| `modified_nodes` | Noeuds dans les deux mais attributs differents |

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
- Ne JAMAIS comparer des graphes de formats differents
- Ne JAMAIS utiliser un delta avec faux positifs (verifier t0=t1 d'abord)
- Ne JAMAIS ecraser un delta existant (immuabilite)
