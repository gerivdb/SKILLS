---
source: SKILLS
target: TALEX
type: semantic_graph_ingestion
direction: outbound
status: active
intent_hash: 0xCROSSLINK_SKILLS_TALEX_20260804
---

# Crosslink SKILLS -> TALEX

SKILLS ingere son REGISTRY.yaml et ses skills natifs dans le UnifiedSemanticGraph de TALEX.

## Cible

| Attribut | Valeur |
|----------|--------|
| **Repo** | `gerivdb/TALEX` |
| **Module** | `src/talex/core/unified_graph.py` |
| **Reader** | `src/talex/readers/__init__.py::EcosystemReader._read_skills` |
| **Strate** | L4-TOOLS |

## Artefacts consommes par TALEX

| Artefact SKILLS | Type TALEX | EdgeKind |
|-----------------|------------|----------|
| `REGISTRY.yaml` | `SemanticNode[SKILL]` | CONSUMES / PRODUCES |
| `native/**/SKILL.md` | `SemanticNode[SKILL]` | CONSUMES / PRODUCES |

## Usage

```bash
x-forge analyze repo --name SKILLS --root D:\DO\WEB
x-forge analyze triangulate --target SKILL:talex --root D:\DO\WEB
```

## Reference

- **Repo source** : `gerivdb/SKILLS`
- **IntentHash SKILLS** : `0xSKILLS_ENGINE_20260801`
