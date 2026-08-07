---
name: n243-query-engine
description: >
  Moteur de requête N243. Execute des requêtes TQL sur le graphe souverain
  via CTULU. Supporte les requêtes cross-repo, temporelles et de contradiction.
version: "1.0.0"
status: active
intent_hash: 0xN243_QUERY_ENGINE_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: SKILLS/n243-query-engine/SKILL.md
triggers:
  - "requete N243"
  - "TQL query"
  - "cross-repo search"
  - "graph query N243"
tools:
  - bash
  - read
  - grep
citizen: "N243-QUERY"
layer: "L4"
---

# Skill — N243 Query Engine

> **Verdict** : **SKILL D'EXECUTION** — Moteur de requête sur le graphe N243.

---

## Objectif

Repondre aux requêtes cross-repo, temporelles et de contradiction via TQL et CTULU.

## Architecture

```
[Client] → [N243 Query Engine] → [CTULU] → [TQL] → [PLIX/VERSES] → [Result]
```

## Processus

### Etape 1 — Valider la requête

```yaml
# Schema de validation (n243-query.schema.yaml)
query:
  type: search|crossref|topology|temporal|contradiction
  target: <repo|strate|IntentHash>
scope:
  strates: [L0, L1, L2, L3, L4]
  repos: [gerivdb/*]
```

### Etape 2 — Router vers CTULU

- `search` → CTULU full-text sur les embeddings
- `crossref` → CTULU cross-repo references
- `topology` → CTULU graphe TOPOS
- `temporal` → CTULU + KRONOS time-series
- `contradiction` → CTULU + MOX validation

### Etape 3 — Executer et formater

- Timeout : 2s par requête
- Cache : KORX .kbin 372B
- Format de sortie : markdown, JSON, ASCII

## Criteres

| CRITERE | SEUIL | METHODE |
|---------|-------|---------|
| Reponse < 2s | 95% des requêtes | Benchmark |
| 0 contradiction non detectée | 100% | MOX validation |
| Cache hit | > 50% | KORX metrics |
| Sources tracees | 100% | IntentHash par affirmation |

## Rollback

1. Revenir au cache precedent.
2. Logger le gap dans WAL.
3. Corriger via PR review N243-BUILDER.

## References

- `TQL/` : operateurs de requête
- `CTULU/` : orchestrateur TQL
- `KORX/` : cache contexte
- `KRONOS/` : time-series
- `MOX/` : validation contradictions
