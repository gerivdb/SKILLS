---
name: talex
version: "1.1.0"
type: engine
domain: engines
status: active
author: gerivdb
license: MIT
created: "2026-08-04"
updated: "2026-08-04"
phi_weight: 0.012
intent_hash: 0xTALEX_ENGINE_20260801
source_engine: TALEX/src/talex
api_endpoint: x-forge (CLI)
triggers:
  - narrate
  - forge
  - x-forge
  - tale
  - story
  - narrative
  - spidx
  - dag3
  - verse
  - spider-graph
  - rewriting
  - analyze
  - triangulate
  - awareness
  - ecosystem
consumes_from:
  - ecosystem-principles
  - spidx
  - dag-3
  - batverse
  - holmes
  - tina
  - ontology
  - verses
  - personae
provides_to:
  - BATVERSE
  - HOLMES
  - DAG-3
  - VERSES
  - BUZZ-X
  - FLUX
  - BRAIN
  - TINA
  - ONTOLOGY
  - SKILLS
  - REPO-STANDARDS
  - unified-design
  - personae
---

# TALEX — Moteur Narratif X-FORGE

> **v1.1.0** — Moteur de triangulation sémantique cross-repo

Engine narratif qui convertit les graphes de réécriture (Spider Graphs SPIDX,
DAG-3) en récits cohérents et **analyse la big picture de l'écosystème**.

## Position

| Attribut | Valeur |
|----------|--------|
| **Strate** | L4-TOOLS |
| **Type** | Engine + Semantic Graph Engine |
| **Rôle** | Moteur narratif × triangulation sémantique × awareness |
| **Citoyens dépendants** | BATVERSE, HOLMES, DAG-3, VERSES, BUZZ-X, FLUX, TINA, ONTOLOGY |

## Interface CLI

```bash
# ── Narration (existant) ───────────────────────────────────────────
x-forge narrate generate --input "data.csv" --output "narration.md"
x-forge narrate weave     --graph "spidx-graph.xml" --output "story.html"
x-forge narrate export    --format video --output "story.mp4"

# ── Analyse cross-repo (nouveau v1.1.0) ───────────────────────────
x-forge analyze ecosystem --root D:\DO\WEB --output report.json
x-forge analyze repo      --name SKILLS --root D:\DO\WEB
x-forge analyze triangulate --target SKILL:talex --root D:\DO\WEB
x-forge analyze strata    --root D:\DO\WEB
```

## Architecture — Unified Semantic Graph

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TALEX UNIFIED SEMANTIC GRAPH                     │
│                     (core/unified_graph.py)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Sources ingérées :                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ TINA         │  │ ONTOLOGY     │  │ VERSES       │              │
│  │ SymbolGraph  │  │ concepts/    │  │ MANIFEST     │              │
│  │ (CITIZEN,   │  │ relations/   │  │ personae_    │              │
│  │  TRIT,      │  │ graph.json   │  │ mapping.md   │              │
│  │  SKILL,     │  │ bridges/     │  │ verses/      │              │
│  │  ADR, REPO) │  │ crossrefs/   │  │ graph/       │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ SKILLS L4    │  │ REPO-STD L4  │  │ personae L0  │              │
│  │ REGISTRY.yaml│  │ citizens.yaml│  │ souls/       │              │
│  │ native/      │  │ bridges.yaml │  │ personae/    │              │
│  │ engines/     │  │ standards/   │  │ sections/    │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                 │                      │
│         └─────────────────┼─────────────────┘                      │
│                           │                                        │
│  ┌────────────────────────▼────────────────────────┐               │
│  │         unified_graph.py                          │               │
│  │  Nodes : SKILL, CITIZEN, STANDARD, DESIGN,       │               │
│  │          VERSE, PERSONA, SOUL, CONVERSATION,     │               │
│  │          CONCEPT, RELATION, REPO, ADR, TRIT,     │               │
│  │          ATOM, BRIDGE                             │               │
│  │  Edges : IMPLEMENTS, CONSUMES, PRODUCES,         │               │
│  │          BACKS, BRIDGES, CROSSREF, INFLUENCES,   │               │
│  │          PART_OF, DEFINES, VALIDATES,            │               │
│  │          ORCHESTRATES, TRACKS, PROTECTS, USES,   │               │
│  │          EMITS, MITIGATES, DEPENDS_ON             │               │
│  └────────────────────────┬────────────────────────┘               │
│                           │                                        │
│  ┌────────────────────────▼────────────────────────┐               │
│  │         narrative_modules/                       │               │
│  │  - batverse/  → 𝒱_AB entanglement narratives    │               │
│  │  - holmes/   → causal analysis (who influences) │               │
│  │  - nexus/    → big picture awareness reports    │               │
│  │       • generate_awareness_report()              │               │
│  │       • generate_triangulation_report(target)     │               │
│  │       • generate_stratum_analysis()               │               │
│  └─────────────────────────────────────────────────┘               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Modules narratifs

| Module | Rôle | Entry point |
|--------|------|-------------|
| `batverse/` | OPÉRATEUR D'INTRICATION NARRATIVE 𝒱_AB | `crossref_matrix.py` |
| `holmes/` | criminalverse, epistemverse, mythoverse_h, psychoverse_h, scientiverse, socialverse_h | `generation.py` |
| `nexus/` | Big picture awareness, triangulation, stratum analysis | `__init__.py` |

## Modes d'opération

| Mode | Dépendances | Usage |
|------|-------------|-------|
| **Standalone** | Aucune | Tests isolés, fallback sûr, Xeon E5620 |
| **Full** | BatMCP + BRAIN + LLUX + KORX + BLO | Production orchestrée |
| **Analyze** | TINA + ONTOLOGY + VERSES + personae + SKILLS + REPO-STANDARDS | Big picture awareness |

## Sources du graphe unifié

| Source | Format | Nœuds | Edges |
|--------|--------|-------|-------|
| TINA SymbolGraph | Python dataclass | CITIZEN, TRIT, ADR, SKILL, REPO | IMPLEMENTS, BACKS, PRODUCES, CONSUMES, DEPENDS_ON |
| ONTOLOGY concepts/ | YAML/MD | CONCEPT | DEFINES, VALIDATES |
| ONTOLOGY relations/ | YAML/JSON-LD | CONCEPT, RELATION | CROSSREF, CONSUMES, PRODUCES |
| VERSES MANIFEST.yaml | YAML | VERSE | (self) |
| personae | YAML/MD | SOUL, PERSONA | PART_OF |
| SKILLS REGISTRY.yaml | YAML | SKILL | CONSUMES, PRODUCES |
| REPO-STANDARDS | YAML/MD | CITIZEN, STANDARD, BRIDGE | BRIDGES |
| unified-design | YAML/MD | DESIGN, ATOM | DEPENDS_ON, USES |

## Ponts narratifs (bridges)

| Bridge | Cible | Direction | Usage |
|--------|-------|-----------|-------|
| `batverse` | BATVERSE | bidir | OPÉRATEUR D'INTRICATION NARRATIVE 𝒱_AB |
| `holmes` | HOLMES | bidir | atmoverse, criminalverse, epistemverse, logicoverse, mythoverse_h, psychoverse_h, scientiverse, socialverse_h |
| `batmcp` | BatMCP | stub | Fallback sans MCP |
| `brain` | BRAIN | stub | Fallback sans CLI cognitive |
| `llux` | LLUX | stub | Fallback sans loader .piano-diff/.kbin |
| `korx` | KORX | stub | Fallback sans Path Manager |
| `blo` | BLO | stub | Fallback sans WAL |

## Usages et triangulation

TALEX est le **point de convergence** des flux narratifs de l'écosystème :

```
TINA SymbolGraph ──┐
ONTOLOGY concepts ─┤
VERSES verses ─────┤
personae ──────────┤
SKILLS registry ───┤
REPO-STANDARDS ────┼──► TALEX/x-forge ──► Récits / HTML / Vidéo / JSON
unified-design ────┘         │
                              ├──► BATVERSE (𝒱_AB entanglement)
                              ├──► HOLMES (verses: criminal, epi, psycho, social...)
                              ├──► VERSES (génération de verses)
                              ├──► TINA (symbol_graph augmentation)
                              ├──► ONTOLOGY (concept enrichment)
                              └──► BUZZ-X / FLUX (diffusion narrative)
```

## Conformité

- Stratum L4-TOOLS : lecture L0/L1/L3, écriture L4 uniquement
- Pas d'import depuis L2-PLATFORM ou L5-ARCHIVE
- Bridges Zig standalone pour mode dégradé garanti
- Unified graph respecte les IntentHash et frontmatters de chaque source

## Références

- **Repo** : `gerivdb/TALEX`
- **IntentHash** : `0xTALEX_ENGINE_20260801`
- **Bridges** : `packages/standalone/src/bridges/`
- **Modules narratifs** : `src/talex/narrative_modules/`
- **Unified Graph** : `src/talex/core/unified_graph.py`
- **Readers** : `src/talex/readers/`
- **Nexus** : `src/talex/narrative_modules/nexus/`
