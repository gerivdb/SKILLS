# Skill: ctulu-cluster-propagator

## Contexte
Le stage PROPAGATE du pipeline REPOSCOPE-COMPARE. Propage les partitions Louvain vers NEXUS/metacluster avec classification collision/synergie/neutre.

## Outil CTULU
- **Package**: `cluster_propagator` (PRD-081)
- **Chemin**: `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\cluster-propagator\`
- **CLI**: `cluster-propagator --partitions <louvain.json> --out NEXUS/metacluster/ [--scores <scores.json>] [--dry-run] [--wal]`

## Contrat CLI (PRD-019)
```bash
cluster-propagator --partitions partitions/louvain_20260616.json --scores scores/scores_20260616.json --out NEXUS/metacluster/ --output json
```

## Métadonnées de cluster
Pour chaque cluster détecté:
- `cluster_id`: identifiant numérique
- `repos`: liste des repos membres
- `centroid_phi`: φ-CPS moyen du cluster
- `dominant_strate`: strate majoritaire (L0-L9)
- `size`: nombre de repos

## Sortie JSON
```json
{
  "propagated_at": "2026-06-16T02:30:00",
  "version": "1.0",
  "cluster_count": 5,
  "clusters": [
    {
      "cluster_id": 0,
      "repos": ["gerivdb/BRAIN", "gerivdb/FLUENCE"],
      "centroid_phi": 3.85,
      "dominant_strate": "L3",
      "size": 2
    }
  ]
}
```

## Dépendances
- `louvain-clusterer` (PRD-082): doit avoir tourné avant
- `reposcope-scorer` (PRD-081): optionnel, pour centroid_phi

## Anti-patterns
- Ne JAMAIS propager sans partitions Louvain valides
- Ne JAMAIS écraser un clusters_<date>.json existant (immuabilité)
- Ne JAMAIS utiliser centroid_phi sans scores (sera 0.0)
