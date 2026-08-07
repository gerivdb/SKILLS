# Skill: ctulu-graph-builder

## Contexte
Construit le graphe NetworkX DiGraph G(V,E) depuis la structure NEXUS. Noeuds: repos + INTENTs + PRDs + EPICs. Edges: depends_on, intent_to_prd, prd_to_epic.

## Outil CTULU
- **Package**: `graph_builder` (PRD-082)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\graph-builder\`
- **CLI**: `graph-builder --nexus <NEXUS_path> --out graphs/ [--dry-run] [--wal] [--output json|text]`

## Contrat CLI (PRD-019)
```bash
graph-builder --nexus D:\DO\WEB\TOOLS\L1-INFRA\NEXUS --out graphs/ --output json
```

## Types de noeuds
| Type | Source | Attributs |
|---|---|---|
| `repo` | `NEXUS/repos/*.yaml` | id, label, path |
| `intent` | `NEXUS/INTENTS/*.md` | id, label |
| `prd` | `NEXUS/PRD/*.md` | id, label |
| `epic` | `NEXUS/EPICS/*.md` | id, label |

## Types d'edges
- `intent_to_prd`: INTENT -> PRD (meme prefixe de stem)
- `intent_to_epic`: INTENT -> EPIC (meme prefixe de stem)
- `prd_to_epic`: PRD -> EPIC (meme prefixe de stem)

## Sorties
- `graph_<timestamp>.graphml`: format GraphML (NetworkX)
- `graph_<timestamp>.json`: format JSON (nodes + edges)

## Anti-patterns
- Ne JAMAIS construire un graphe sans NEXUS valide
- Ne JAMAIS inclure des noeuds sans type
- Ne JAMAIS ecraser un graph existant (immuabilite)
