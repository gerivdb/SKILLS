# Skill: ctulu-artifact-builder

## Contexte
Le stage ARTEFACT du pipeline REPOSCOPE-COMPARE. Genere le rapport final Markdown + JSON + Mermaid diagram.

## Outil CTULU
- **Package**: `artifact_builder` (PRD-081)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\artifact-builder\`
- **CLI**: `artifact-builder --scores <scores.json> --clusters <clusters.json> [--extract <yaml>] --out artifacts/ [--dry-run] [--wal]`

## Contrat CLI (PRD-019)
```bash
artifact-builder --scores scores/scores_20260616.json --clusters clusters/clusters_20260616.json --out artifacts/ --output json
```

## Sections du rapport Markdown
1. **Summary**: metriques globales (repo_count, top_score, action, cluster_count)
2. **Top 20 Repos**: tableau classe par score avec classification
3. **Clusters**: tableau des clusters (ID, size, dominant strate, centroid phi)
4. **Recommandation**: action suggeree (archive/promote/escalate)
5. **Diagram**: Mermaid `graph TD` avec repos colores par cluster

## Recommandation d'action
- **escalate** (top_score >= 0.70): collision forte, decision humaine requise
- **promote** (top_score in [0.30, 0.70)): match modere, review recommandee
- **archive** (top_score < 0.30): pas de match significatif

## Sorties
- `reposcope_report_<timestamp>.md`: rapport Markdown complet
- `report_<timestamp>.json`: donnees structurees

## Anti-patterns
- Ne JAMAIS generer de rapport sans scores valides
- Ne JAMAIS inclure >50 noeuds Mermaid (limite de lisibilite)
- Ne JAMAIS ecraser un rapport existant (immuabilite)
