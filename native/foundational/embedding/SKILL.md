---
name: embedding
description: Skill for generating and managing vector embeddings for semantic search and similarity matching
triggers:
  - embedding
  - vector
  - semantic
  - similarity
  - search
  - representation
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - embedding
  - vector
  - semantic
  - similarity
  - search
  - representation
  - nlp
phi_weight: 0.005
biz_domains:
  - BIZ-FINANCE
  - BIZ-GENEALOGY
---

# Embedding — Vector Embeddings for Semantic Search

## Description

Ce skill fondamental génère et gère des embeddings vectoriels pour la recherche sémantique et la similarité. Il convertit le texte en représentations vectorielles, calcule les similarités et indexe pour des recherches rapides.

## Usage

```
Quand [recherche sémantique] OU [similarité de texte] OU [indexation vectorielle]
→ Appliquer embedding pour:
  1. Convertir le texte en vecteurs
  2. Calculer les similarités cosinus
  3. Indexer pour recherche rapide
  4. Gérer les métadonnées associées
  5. Exporter les embeddings
```

## Composants

### 1. EmbeddingGenerator

```python
class EmbeddingGenerator:
    """Générateur d'embeddings vectoriels"""
    
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.model = load_model(config.model_name)
    
    def generate(self, text: str) -> np.ndarray:
        """Génère un embedding pour un texte"""
```

### 2. SimilarityCalculator

```python
def calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcule la similarité cosinus entre deux vecteurs"""
    # Similarité cosinus normalisée
```

### 3. VectorIndex

```python
class VectorIndex:
    """Index vectoriel pour recherche rapide"""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors = []
        self.metadata = []
    
    def add(self, vector: np.ndarray, metadata: dict):
        """Ajoute un vecteur à l'index"""
```

## BIZ Domains

- **BIZ-FINANCE (BANK-BUSTER)**: Recherche sémantique de transactions et documents financiers
- **BIZ-GENEALOGY (RACINES)**: Similarité de profils généalogiques et recherche d'ancêtres

## Exemples

### Exemple 1: Embedding de Document

**Input:**
```python
generator = EmbeddingGenerator(config)
embedding = generator.generate("Transaction bancaire de 1500€")
```

**Output:**
```
Vecteur de dimension 768:
[0.023, -0.156, 0.089, ..., 0.234]
Similarité avec 'virement bancaire': 0.87
```

### Exemple 2: Recherche Sémantique

**Input:**
```python
index = VectorIndex(dimension=768)
index.add(embedding1, {"type": "transaction", "amount": 1500})
index.add(embedding2, {"type": "transaction", "amount": 2000})

results = index.search(query_embedding, top_k=5)
```

**Output:**
```
5 résultats trouvés:
1. Transaction 1500€ (similarité: 0.92)
2. Transaction 2000€ (similarité: 0.78)
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `semantic-search` (pour recherche sémantique)
- `finance` (domain)
- `genealogy` (domain)

## Intégration

### BANK-BUSTER
```python
from skills.embedding import EmbeddingGenerator, VectorIndex

generator = EmbeddingGenerator(config)
index = VectorIndex(dimension=768)

# Indexer les transactions
for transaction in transactions:
    embedding = generator.generate(transaction.description)
    index.add(embedding, transaction.metadata)
```

### RACINES
```python
# Recherche de profils similaires
generator = EmbeddingGenerator(config)
profile_embedding = generator.generate(profile.biography)
similar_profiles = index.search(profile_embedding, top_k=10)
```

## Configuration

```yaml
embedding:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  dimension: 384
  batch_size: 32
  
  similarity:
    metric: cosine
    threshold: 0.7
  
  index:
    type: faiss
    nlist: 100
    nprobe: 10
```

## Métriques

- **Temps de génération**: < 50ms par texte
- **Dimension**: 384-768 selon le modèle
- **Précision similarité**: 95%
- **Indexation**: 1000 vecteurs/seconde

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
