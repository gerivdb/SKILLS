# Skill - n243-query-engine

> **IntentHash** : 0xSKILL_N243_QUERY_ENGINE_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L4  
> **Status** : proposed  

## Objectif

Repondre aux requetes cross-repo sur le graphe N243 via CTULU et TQL,
avec support temporel N+2, detection de contradictions et tracabilite WAL.

## Declencheur

- Requete utilisateur vers N243
- Appel depuis `n243-query.yaml` workflow
- Requete auto-dev pour analyse de graphe

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `query` | object | Requete TQL : `type`, `target`, `filters` |
| `scope` | object | Perimetre : `strates`, `repos`, `time_range` |
| `options` | object | Options : `trace_sources`, `detect_contradictions`, `max_results` |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `result` | JSON | Resultat de la requete |
| `sources` | list | Sources tracees (repo, strate, document) |
| `contradictions` | list | Contradictions detectees |
| `wal_entry` | JSON | Entree WAL pour tracabilite |

## Etapes

### 1. Valider la requete

- Valider contre `n243-query.schema.yaml`
- Verifier que le type est dans : `search`, `crossref`, `topology`, `temporal`, `contradiction`
- Verifier que les strates sont valides

### 2. Interroger CTULU

- Formuler la requete TQL selon le type :
  - `search` : recherche plein texte dans les embeddings
  - `crossref` : liens entre artefacts
  - `topology` : structure du graphe
  - `temporal` : requete sur canal `time` de `.piano-diff`
  - `contradiction` : detection de contradictions
- Executer via CTULU avec timeout 2s
- Si CTULU indisponible : fallback cache KORX

### 3. Detecter les contradictions (si demande)

- Si `detect_contradictions: true` :
  - Comparer les resultats cross-repo
  - Detecter les incoherences de frontmatter, IntentHash, references
  - Logger dans WAL via NEXUS

### 4. Tracer les sources

- Pour chaque resultat : lier au repo, strate, document source
- Generer le chemin de source : `gerivdb/<repo>/<path>#<intent_hash>`

### 5. Serialiser la reponse

- Format : Markdown, ASCII, ou JSON selon `options.output_format`
- Inclure : resultats, sources, contradictions, metadonnees N+2

### 6. Logger dans WAL

- Entree WAL : timestamp, query_hash, repos touches, contradictions, duree

## Dependances

| Dependance | Role | Version |
|------------|------|---------|
| CTULU | Execution TQL | Latest |
| TQL | 12 operateurs requete fractal | Latest |
| KORX | Cache .kbin, phi-CPS | Latest |
| PLIX | Codec `.piano-diff` | Latest |
| NEXUS | WAL, tracabilite | Latest |
| n243-query.schema.yaml | Validation requete | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_search_query` | Requete search | < 2s, sources tracees |
| `test_crossref_query` | Requete crossref | 0 contradiction |
| `test_temporal_query` | Requete temporelle | Support canal time |
| `test_contradiction_query` | Requete contradiction | Detectee en < 1s |

## References

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > N243, CTULU, TQL, KORX`
- Atom : `unified-design/atoms/governance/n243-sovereign-reasoning.yaml`
- Schema : `REPO-STANDARDS/schemas/n243-query.schema.yaml`
