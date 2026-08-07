# Skill — n243-graph-builder

> **IntentHash** : 0xSKILL_N243_GRAPH_BUILDER_20260806  
> **Citizen** : L2-PLATFORM  
> **Layer** : L4  
> **Status** : proposed  

## Objectif

Construire le graphe souverain cross-repo N243 en scannant tous les dépôts actifs,
extrayant leurs métadonnées (ADR, PRD, INTENT, EPIC, IMPENSE, REPORT, ROADMAP, SPEC)
et en construisant un graphe exploitable par le moteur de requête N243.

## Déclencheur

- Tout appel à N243 nécessitant une mise à jour du graphe
- Scan manuel via `n243-ingestion.yaml`
- Hook git post-commit sur `known_repositories.yaml` ou tout ADR/PRD/INTENT/EPIC/REPORT/ROADMAP/SPEC

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `repos` | list | Liste des dépôts actifs depuis `known_repositories.yaml` |
| `strates` | list | Strates à scanner (`-1`, `L0`, `L1`, `L1b`, `L1-INFRA`, `L2`, `L2b`, `L3`, `L1-L4`, `L4`, `L5`, `L6`, `P2P`) |
| `output` | path | Chemin de sortie du graphe (`plixvault/` ou `vdb/`) |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `graph` | JSON | Graphe des repos, métadonnées, edges |
| `embeddings` | binary | Embeddings LLUX horodatés |
| `wal_entry` | JSON | Entrée WAL pour traçabilité |

## Étapes

### 1. Scanner les dépôts

Pour chaque dépôt dans `known_repositories.yaml` :
- Vérifier que le chemin local existe
- Extraire les métadonnées :
  - ADR : `ADR/` ou `docs/ADR/`
  - PRD : `PRD/` ou `act-protocol/PRD/`
  - INTENT : `INTENTS/` ou `act-protocol/INTENTS/`
  - EPIC : `EPICS/` ou `act-protocol/EPICS/`
  - IMPENSE : `IMPENSES/` ou `act-protocol/IMPENSES/`
  - REPORT : `REPORTS/` ou `act-protocol/REPORTS/`
  - ROADMAP : `ROADMAPS/` ou `act-protocol/ROADMAPS/`
  - SPEC : `SPEC/` ou `act-protocol/SPEC/`
- Stocker les métadonnées dans un index temporaire

### 2. Extraire les métadonnées

Pour chaque artefact trouvé :
- Lire le frontmatter YAML
- Extraire : `type`, `version`, `status`, `date`, `intent_hash`, `citizen`, `layer`, `author`, `source_repo`, `source_path`
- Valider avec `artifact-quality.schema.yaml`
- Si validation échoue : logger dans WAL et continuer

### 3. Construire le graphe

- Nœuds : dépôts, artefacts, concepts
- Edges :
  - `depends_on` : dépôt A dépend de dépôt B
  - `references` : artefact A référence artefact B
  - `owns` : dépôt A possède artefact B
  - `orchestrates` : dépôt A orchestre dépôt B
  - `bridges_to` : dépôt A a un bridge vers dépôt B
- Stratégie d'embedding :
  - Si `llux` disponible : générer embeddings via LLUX
  - Sinon : utiliser embeddings TF-IDF fallback
  - Horodater avec `KRONOS`

### 4. Sérialiser le graphe

- Format : `.piano-diff` via PLIX
- Base 243 : états triadiques compatibles DAG-3
- Canaux : RVB (modifications), alpha (confiance), index (référence), time (N+2)
- Stocker dans `plixvault/` pour index, `vdb/` pour embeddings

### 5. Mettre à jour le WAL

- Logger l'ingestion complète dans WAL via NEXUS
- Inclure : timestamp, repos scannés, artefacts indexés, edges créés, contradictions détectées

## Dépendances

| Dépendance | Rôle | Version |
|------------|------|---------|
| TOPOS | Matrice de routage, topologie des repos | Latest |
| GOVERNANCE-HUB | `known_repositories.yaml`, WAL | Latest |
| PLIX | Codec `.piano-diff` | Latest |
| LLUX | Engine inférence SSE4.2, embeddings | Latest |
| KRONOS | Qualificateur temporel | Latest |
| NEXUS | WAL, registre des registres | Latest |
| artifact-quality.schema.yaml | Validation frontmatter | Latest |

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_scan_all_repos` | Scan tous les repos actifs | 100% repos détectés |
| `test_extract_metadata` | Extrait ADR, PRD, INTENT | Métadonnées complètes |
| `test_build_graph` | Construit le graphe | Edges cohérentes |
| `test_update_embeddings` | Met à jour embeddings | < 10 min pour 50 docs |

## Références

- PRD MOC : `PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md`
- ONTOLOGY : `ONTOLOGY.yaml > concepts > N243, MOX, CTULU, PLIX, LLUX, KRONOS`
- Atom : `unified-design/atoms/governance/n243-sovereign-reasoning.yaml`
- Schéma : `REPO-STANDARDS/schemas/n243-query.schema.yaml`
