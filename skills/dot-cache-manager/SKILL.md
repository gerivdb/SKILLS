---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xDOT_CACHE_20260801
status: active
---

# Skill: dot-cache-manager

## Purpose
SHA256-based cache with LRU eviction and 30-day TTL for DOT graph generation. Used by plix-graph-generator.

## Context
DOT generation from 200+ source files is expensive. Cache avoids regeneration when sources unchanged.

## Cache Structure
`
.kilo/cache/dot/
  index.yaml          # key -> {path, sha256, size, created_at, accessed_at}
  <sha256>.dot        # cached DOT output
  <sha256>.svg        # cached SVG output
  <sha256>.html       # cached HTML output
`

## Cache Key
SHA256 of concatenated source file contents (sorted by path):
`
key = SHA256(file1_content + file2_content + ... + config_hash)
`

## Operations

### Get
`python
cache.get(key, format='dot')  # returns path or None
`

### Set
`python
cache.set(key, dot_content, format='dot')  # writes file, updates index
`

### Eviction Policy
- LRU: Least recently accessed evicted first
- TTL: Entries older than 30 days auto-evicted
- Max size: 500 MB (configurable)

## Maintenance Command
`powershell
python -m tools.dot_cache --clean --max-age 30 --max-size 500MB
`

## Integration
- Called by plix graph via S-005: plix-graph-generator
- Transparent to caller: cache hit = instant return
- Cache miss = generate + store + return

## Anti-patterns
- Not checking cache before generation
- Storing without updating index.yaml
- Ignoring TTL (stale cache)
- Cache directory not in .gitignore

## References
- S-005: plix-graph-generator (skill)
- D-001: fractal-engineering-strata (design)
