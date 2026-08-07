# Skill — n243-query-engine

> **IntentHash** : 0xSKILL_N243_QUERY_ENGINE_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L4  
> **Status** : proposed  

## Objectif

Répondre aux requêtes cross-repo sur le graphe N243 via CTULU et TQL,
avec support temporel N+2, détection de contradictions et traçabilité WAL.

## Déclencheur

- Requête utilisateur vers N243
- Appel depuis `n243-query.yaml` workflow
- Requête auto-dev pour analyse de graphe

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `query` | object | Requête TQL : `type`, `target`, `filters` |
| `scope` | object | Périmètre : `strates`, `repos`, `time_range` |
| `options` | object | Options : `trace_sources`, `detect_contradictions`, `max_results` |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `result` | JSON | Résultat de la requête |
| `sources` | list | Sources tracées (repo, strate, document) |
| `contradictions` | list | Contradictions détectées |
| `wal_entry` | JSON | Entrée WAL pour traçabilité |

## Étapes

### 1. Valider la requête

- Valider contre `n243-query.schema.yaml`
- Vérifier que le type est dans : `search`, `crossref`, `topology`, `temporal`, `contradiction`
- Vérifier que les strates sont valides

### 2. Interroger CTULU

- Formuler la requête TQL selon le type :
  - `search` : recherche plein texte dans les embeddings
  - `crossref` : liens entre artefacts
  - `topology` : structure du graphe
  - `temporal` : requête sur canal `time` de `.piano-diff`
  - `contradiction` : détection de contradictions
- Exécuter via CTULU avec timeout 2s
- Si CTULU indisponible : fallback cache KORX

### 3. Détecter les contradictions (si demandé)

- Si `detect_contradictions: true` :
  - Comparer les résultats cross-repo
  - Détecter les incohérences de frontmatter, IntentHash, références
  - Logger dans WAL via NEXUS

### 4. Tracer les sources

- Pour chaque résultat : lier au repo, strate, document source
- Générer le chemin de source : `gerivdb/<repo>/<path>#<intent_hash>`

### 5. Sérialiser la réponse

- Format : Markdown, ASCII, ou JSON selon `options.output_format`
- Inclure : résultats, sources, contradictions, métadonnées N+2

### 6. Logger dans WAL

- Entrée WAL : timestamp, query_hash, repos touchés, contradictions, durée

## Dépendances

| Dépendance | Rôle | Version |
|------------|------|---------|
| CTULU | Exécution TQL | Latest |
| TQL | 12 opérateurs requête fractal | Latest |
| KORX | Cache .kbin, φ-CPS | Latest |
| PLIX | Codec `.piano-diff` | Latest |
| NEXUS | WAL, traçabilité | Latest |
| n243-query.schema.yaml | Validation requête | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_search_query` | Requête search | < 2s, sources tracées |
| `test_crossref_query` | Requête crossref | 0 contradiction |
| `test_temporal_query` | Requête temporelle | Support canal time |
| `test_contradiction_query` | Requête contradiction | Détectée en < 1s |

## Références

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > N243, CTULU, TQL, KORX`
- Atom : `unified-design/atoms/governance/n243-sovereign-reasoning.yaml`
- Schéma : `REPO-STANDARDS/schemas/n243-query.schema.yaml`
