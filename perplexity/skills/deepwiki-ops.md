---
name: deepwiki-ops
version: "1.0.0"
description: "Fused skill combining DeepWiki-based repo analysis (analyse-repo-deepwiki) and DeepWiki repo enrichment (deepwiki_repo_enricher). Provides constitutional ECOS analysis, ENV2 scoring, GitHub issue coverage, alternatives comparison, and final recommendation. Use when user mentions any of the original triggers."
triggers: ["/analyse-repo", "évalue dépôt", "DeepWiki", "scoring ECOS", "citoyennisation", "DeepWiki Enricher", "constitutionnelle ECOS", "ENV2 compliance", "GitHub coverage", "alternatives"]
layer: "L5_META"
nexusTags: ["CONFORME_NEXUS"]
prerequisites: []
slotWeight: 1
status: active
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Fusion of analyse-repo-deepwiki.md and deepwiki_repo_enricher.md"}
trit_primitive: TritDiscoverArtifact
---
# DeepWiki Ops (Fused)

This skill merges the two original DeepWiki‑related skills:

* **Analyse Repo DeepWiki** – performs a constitutional ECOS analysis of a public GitHub repo via DeepWiki, includes ENV2 scoring, GitHub issue coverage, and recommendation.
* **DeepWiki Repo Enricher** – enriches the analysis with detailed enrichment steps, YAML output, alternative comparison, and a final recommendation statement.

## Domaine et périmètre
(Combined from the two sources)

## Méthodologie
(Combined from the two sources)

## Règles de décision
(Combined from the two sources)

## Format de sortie
(Combined from the two sources)

## Exemples d'utilisation
(Combined from the two sources)

## Intégration avec l'écosystème
- Dépôts concernés : any public GitHub repo (analysis via DeepWiki)
- Couche EECS : L5_META
- Tags NEXUS : [CONFORME_NEXUS]