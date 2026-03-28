---
name: semantic-search
description: Skill for performing semantic search using vector embeddings and natural language understanding
triggers:
  - semantic-search
  - search
  - vector-search
  - similarity
  - nlp
  - retrieval
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - semantic-search
  - search
  - vector-search
  - similarity
  - nlp
  - retrieval
  - embedding
phi_weight: 0.005
biz_domains:
  - BIZ-RECRUIT
  - BIZ-GENEALOGY
  - BIZ-DEV
---

# Semantic Search — Recherche Sémantique avec Embeddings

## Description

Ce skill fondamental effectue des recherches sémantiques en utilisant des embeddings vectoriels et la compréhension du langage naturel. Il indexe les documents, calcule les similarités et retourne les résultats les plus pertinents.

## Usage

```
Quand [recherche sémantique] OU [recherche par similarité] OU [retrieval intelligent]
→ Appliquer semantic-search pour:
  1. Indexer les documents avec embeddings
  2. Comprendre l'intention de recherche
  3. Calculer les similarités sémantiques
  4. Retourner les résultats pertinents
  5. Gérer les requêtes complexes
```

## Composants

### 1. SemanticSearchEngine

```python
class SemanticSearchEngine:
    """Moteur de recherche sémantique principal"""
    
    def __init__(self, config: SearchConfig):
        self.config = config
        self.embedder = EmbeddingGenerator(config.embedding)
        self.index = VectorIndex(config.index)
    
    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Effectue une recherche sémantique"""
```

### 2. QueryProcessor

```python
class QueryProcessor:
    """Processeur de requêtes intelligent"""
    
    def __init__(self, config: QueryConfig):
        self.config = config
        self.nlp = spacy.load("fr_core_news_sm")
    
    def process(self, query: str) -> ProcessedQuery:
        """Traite et enrichit une requête"""
```

### 3. RelevanceScorer

```python
class RelevanceScorer:
    """Calculateur de pertinence"""
    
    def __init__(self, config: ScoringConfig):
        self.config = config
    
    def score(self, query_embedding: np.ndarray, doc_embedding: np.ndarray) -> float:
        """Calcule le score de pertinence"""
```

### 4. ResultRanker

```python
class ResultRanker:
    """Classeur de résultats"""
    
    def __init__(self, config: RankingConfig):
        self.config = config
    
    def rank(self, results: list[SearchResult]) -> list[SearchResult]:
        """Classe les résultats par pertinence"""
```

## BIZ Domains

- **BIZ-RECRUIT (CANDIDATOR)**: Recherche de candidats par compétences et expérience
- **BIZ-GENEALOGY (RACINES)**: Recherche d'individus dans les arbres généalogiques
- **BIZ-DEV (ECOYSTEM)**: Recherche de documentation et code dans les repositories

## Exemples

### Exemple 1: Recherche de Candidats

**Input:**
```python
engine = SemanticSearchEngine(config)
results = engine.search(
    query="Développeur Python avec expérience en machine learning",
    top_k=5
)
```

**Output:**
```
5 résultats trouvés:
1. Jean Dupont - Développeur Python Senior (similarité: 0.92)
   Compétences: Python, ML, TensorFlow, scikit-learn
   
2. Marie Martin - Data Scientist (similarité: 0.87)
   Compétences: Python, Deep Learning, PyTorch
   
3. Pierre Durand - ML Engineer (similarité: 0.85)
   Compétences: Python, MLOps, Kubernetes
```

### Exemple 2: Recherche Généalogique

**Input:**
```python
engine = SemanticSearchEngine(config)
results = engine.search(
    query="Personnes nées à Paris au 19ème siècle",
    top_k=10
)
```

**Output:**
```
10 résultats trouvés:
1. Marie Dupont (1823-1895) - Née à Paris 3ème
2. Jean Martin (1845-1910) - Né à Paris 5ème
3. Louise Bernard (1867-1932) - Née à Paris 7ème
...
```

## Dépendances

### Dépend de
- `embedding` (pour génération de vecteurs)

### Requis par
- `recruitment` (domain)
- `genealogy` (domain)

## Intégration

### CANDIDATOR
```python
from skills.semantic_search import SemanticSearchEngine, SearchConfig

config = SearchConfig(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    index_type="faiss",
    similarity_metric="cosine"
)
engine = SemanticSearchEngine(config)

# Recherche de candidats
candidates = engine.search(
    query="Ingénieur DevOps avec expérience AWS",
    filters={"experience_years": {"$gte": 3}},
    top_k=20
)
```

### RACINES
```python
# Recherche dans l'arbre généalogique
engine = SemanticSearchEngine(config)
results = engine.search(
    query="Ancêtres de Jean Dupont nés avant 1800",
    filters={"birth_year": {"$lt": 1800}},
    top_k=50
)
```

### ECOYSTEM
```python
# Recherche de documentation
engine = SemanticSearchEngine(config)
docs = engine.search(
    query="Comment configurer le rate limiting",
    filters={"type": "documentation"},
    top_k=5
)
```

## Configuration

```yaml
semantic_search:
  embedding:
    model: "sentence-transformers/all-MiniLM-L6-v2"
    dimension: 384
    batch_size: 32
  
  index:
    type: faiss
    nlist: 100
    nprobe: 10
  
  search:
    default_top_k: 10
    max_top_k: 100
    similarity_threshold: 0.7
  
  ranking:
    algorithm: bm25_hybrid
    boost_recent: true
    boost_relevant: true
  
  query_processing:
    language: fr
    expand_query: true
    remove_stopwords: true
```

## Métriques

- **Temps de recherche**: < 100ms pour 10k documents
- **Précision**: 92% de pertinence
- **Rappel**: 88% de couverture
- **Indexation**: 1000 documents/seconde

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
