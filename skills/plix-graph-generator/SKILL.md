---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xPLIX_GRAPH_20260801
status: active
---

# Skill: plix-graph-generator

## Purpose
Generate DAG-3 visualization in 5 formats: ASCII, Mermaid, DOT, SVG, HTML. Used by plix graph command.

## Context
PLIX is the design language for the ecosystem. The graph generator renders the design DAG for documentation and analysis.

## Input
- Source: designs/ and toms/ YAML files with elations field
- Config: .kilo/plix-graph-config.yaml (format, depth, filters)

## Output Formats

| Format | Use Case | Command Flag |
|--------|----------|--------------|
| scii | Terminal quick view | --format ascii |
| mermaid | Markdown docs, GitHub | --format mermaid |
| dot | Graphviz processing | --format dot |
| svg | Static documentation | --format svg |
| html | Interactive browser | --format html |

## Generation Command
`powershell
plix graph --source designs --source atoms --format all --output .kilo/plix-graph/
`

## DOT Cache Integration
- Uses S-006: dot-cache-manager for SHA256+LRU+TTL 30d caching
- Cache key: SHA256 of concatenated source files
- On cache hit: return cached output instantly
- On cache miss: generate, store, return

## DAG-3 Constraints
- Max depth: 3 (per fractal recursion limit)
- Max nodes per render: 200 (performance)
- Filter: --filter-kind requires,inherits etc.

## Output Structure
`
.kilo/plix-graph/
  dag3.ascii
  dag3.mermaid
  dag3.dot
  dag3.svg
  dag3.html
  metadata.yaml  # node_count, edge_count, depth, generated_at
`

## Anti-patterns
- Generating without cache check first
- Rendering > 200 nodes (use --filter)
- Missing elations field in source YAML
- Output formats not matching CI requirements

## References
- S-006: dot-cache-manager (skill)
- S-007: plix-inspector (skill)
- D-001: fractal-engineering-strata (design)
- ATOM-042: REPOSITORY-CENSUS
