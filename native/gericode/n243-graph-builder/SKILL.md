# Skill - n243-graph-builder

> **IntentHash** : 0xSKILL_N243_GRAPH_BUILDER_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L4  
> **Status** : proposed  

## Objectif

Construire le graphe souverain cross-repo N243 en scannant tous les depots actifs,
extrayant leurs metadonnees (ADR, PRD, INTENT, EPIC, IMPENSE, REPORT, ROADMAP, SPEC)
et en construisant un graphe exploitable par le moteur de requete N243.

## Declencheur

- Tout appel a N243 necessitant une mise a jour du graphe
- Scan manuel via `n243-ingestion.yaml`
- Hook git post-commit sur `known_repositories.yaml` ou tout ADR/PRD/INTENT/EPIC/REPORT/ROADMAP/SPEC

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `repos` | list | Liste des depots actifs depuis `known_repositories.yaml` |
| `strates` | list | Strates a scanner (`-1`, `L0`, `L1`, `L1b`, `L1-INFRA`, `L2`, `L2b`, `L3`, `L1-L4`, `L4`, `L5`, `L6`, `P2P`) |
| `output` | path | Chemin de sortie du graphe (`plixvault/` ou `vdb/`) |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `graph` | JSON | Graphe des repos, metadonnees, edges |
| `embeddings` | binary | Embeddings LLUX horodates |
| `wal_entry` | JSON | Entree WAL pour tracabilite |

## Etapes

### 1. Scanner les depots

Pour chaque depot dans `known_repositories.yaml` :
- Verifier que le chemin local existe
- Extraire les metadonnees :
  - ADR : `ADR/` ou `docs/ADR/`
  - PRD : `PRD/` ou `act-protocol/PRD/`
  - INTENT : `INTENTS/` ou `act-protocol/INTENTS/`
  - EPIC : `EPICS/` ou `act-protocol/EPICS/`
  - IMPENSE : `IMPENSES/` ou `act-protocol/IMPENSES/`
  - REPORT : `REPORTS/` ou `act-protocol/REPORTS/`
  - ROADMAP : `ROADMAPS/` ou `act-protocol/ROADMAPS/`
  - SPEC : `SPEC/` ou `act-protocol/SPEC/`
- Stocker les metadonnees dans un index temporaire

### 2. Extraire les metadonnees

Pour chaque artefact trouve :
- Lire le frontmatter YAML
- Extraire : `type`, `version`, `status`, `date`, `intent_hash`, `citizen`, `layer`, `author`, `source_repo`, `source_path`
- Valider avec `artifact-quality.schema.yaml`
- Si validation echoue : logger dans WAL et continuer

### 3. Construire le graphe

- Noeuds : depots, artefacts, concepts
- Edges :
  - `depends_on` : depot A depend de depot B
  - `references` : artefact A reference artefact B
  - `owns` : depot A possede artefact B
  - `orchestrates` : depot A orchestre depot B
  - `bridges_to` : depot A a un bridge vers depot B
- Strategie d'embedding :
  - Si `llux` disponible : generer embeddings via LLUX
  - Sinon : utiliser embeddings TF-IDF fallback
  - Horodater avec `KRONOS`

### 4. Serialiser le graphe

- Format : `.piano-diff` via PLIX
- Base 243 : etats triadiques compatibles DAG-3
- Canaux : RVB (modifications), alpha (confiance), index (reference), time (N+2)
- Stocker dans `plixvault/` pour index, `vdb/` pour embeddings

### 5. Mettre a jour le WAL

- Logger l'ingestion complete dans WAL via NEXUS
- Inclure : timestamp, repos scannes, artefacts indexes, edges crees, contradictions detectees

## Dependances

| Dependance | Role | Version |
|------------|------|---------|
| TOPOS | Matrice de routage, topologie des repos | Latest |
| GOVERNANCE-HUB | `known_repositories.yaml`, WAL | Latest |
| PLIX | Codec `.piano-diff` | Latest |
| LLUX | Engine inference SSE4.2, embeddings | Latest |
| KRONOS | Qualificateur temporel | Latest |
| NEXUS | WAL, registre des registres | Latest |
| artifact-quality.schema.yaml | Validation frontmatter | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_scan_all_repos` | Scan tous les repos actifs | 100% repos detectes |
| `test_extract_metadata` | Extrait ADR, PRD, INTENT | Metadonnees completes |
| `test_build_graph` | Construit le graphe | Edges coherentes |
| `test_update_embeddings` | Met a jour embeddings | < 10 min pour 50 docs |

## References

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > N243, MOX, CTULU, PLIX, LLUX, KRONOS`
- Atom : `unified-design/atoms/governance/n243-sovereign-reasoning.yaml`
- Schema : `REPO-STANDARDS/schemas/n243-query.schema.yaml`
