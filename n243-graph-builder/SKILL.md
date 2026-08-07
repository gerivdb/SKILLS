---
name: n243-graph-builder
description: >
  Construit le graphe souverain cross-repo N243.
  Ingeste les metadonnees de tous les repos, construit les edges de dependances,
  et maintient l'index a jour. Utilise TOPOS, GOVERNANCE-HUB, et TQL.
version: "1.0.0"
status: active
intent_hash: 0xN243_GRAPH_BUILDER_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: SKILLS/n243-graph-builder/SKILL.md
triggers:
  - "construire graphe N243"
  - "ingerer repos"
  - "mettre a jour index N243"
  - "cross-repo graph"
tools:
  - bash
  - read
  - grep
  - codebase_search
citizen: "N243-BUILDER"
layer: "L4"
---

# Skill — N243 Graph Builder

> **Verdict** : **SKILL D'EXECUTION** — Construit et maintient le graphe souverain N243.

---

## Objectif

Ingester les metadonnees de tous les repos actifs, construire le graphe de dependances cross-repo, et maintenir l'index N243 a jour.

## Source de verite

| Source | Role |
|--------|------|
| `TOPOS/repo-manifest.yaml` | SOT topologique (local_path, strate, b243) |
| `GOVERNANCE-HUB/known_repositories.yaml` | SOT noms (full_name, status, role) |
| `ONTOLOGY/ONTOLOGY.yaml` | SOT semantique (termes, concepts) |

## Processus

### Etape 1 — Charger les SOT

```powershell
# Charger TOPOS
$topos = Get-Content "D:\DO\WEB\TOOLS\L1-INFRA\TOPOS\repo-manifest.yaml" -Raw | ConvertFrom-Yaml

# Charger GOVERNANCE-HUB
$repos = Get-Content "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\known_repositories.yaml" -Raw | ConvertFrom-Yaml
```

### Etape 2 — Ingester les repos

Pour chaque repo actif :
1. Lire `repo-manifest.yaml` pour local_path, strate, b243_vector
2. Lire `known_repositories.yaml` pour full_name, status, role
3. Detecter les bridges cross-repo (CROSSLINKS/, bridges.yaml)
4. Extraire les metadonnees : ADR, PRD, INTENT, EPIC, IMPENSE, REPORT, ROADMAP, SPEC

### Etape 3 — Construire le graphe

```yaml
graphe:
  nodes:
    - id: repo:gerivdb/GOVERNANCE-HUB
      type: repo
      strate: L0-CANON
      role: SOT noms
    - id: repo:gerivdb/TOPOS
      type: repo
      strate: L1-INFRA
      role: SOT topologique
  edges:
    - source: repo:gerivdb/GOVERNANCE-HUB
      target: repo:gerivdb/TOPOS
      type: bridge
      bridge: GOVERNANCE-TOPOS
```

### Etape 4 — Mettre a jour l'index

- Sauvegarder le graphe dans `D:\DO\WEB\TOOLS\L4-TOOLS\N243\data\graph.yaml`
- Mettre a jour les embeddings dans `D:\DO\WEB\TOOLS\L4-TOOLS\N243\data\embeddings.json`
- Logger dans WAL

## Criteres

| CRITERE | SEUIL | METHODE |
|---------|-------|---------|
| Repos ingeres | 100% des repos actifs | Comparaison known_repositories.yaml |
| Edges construites | 100% des bridges detectes | Scan CROSSLINKS/ |
| Fraicheur | < 5 min apres commit | Hook git |
| Disponibilite | 99.9% | Health check N243 |

## Rollback

1. Restaurer le graphe precedent depuis git.
2. Logger le revert dans WAL.
3. Corriger via PR review MOX.

## References

- `TOPOS/repo-manifest.yaml`
- `GOVERNANCE-HUB/known_repositories.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
- `D:\DO\WEB\TOOLS\L4-TOOLS\N243\`
