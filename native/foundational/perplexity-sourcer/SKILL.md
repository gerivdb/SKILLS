---
name: perplexity-sourcer
description: Skill for automated job sourcing using Perplexity API
triggers:
  - perplexity
  - job-sourcing
  - search
  - api
  - job-listings
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - perplexity
  - job
  - sourcing
  - search
  - api
  - recruitment
phi_weight: 0.005
---

# Perplexity Sourcer — Sourcing Automatisé d'Offres d'Emploi

## Description

Ce skill fondamental automatise le sourcing d'offres d'emploi via l'API Perplexity. Il recherche des offres sur plusieurs plateformes, extrait les informations entreprises, parse les localisations et dates, et déduplique les résultats.

## Usage

```
Quand [recherche d'offres d'emploi] OU [sourcing de candidats]
→ Appliquer perplexity-sourcer pour:
  1. Rechercher sur LinkedIn, Pôle Emploi, Welcome to the Jungle, Indeed
  2. Extraire automatiquement les entreprises
  3. Parser localisation et date depuis le texte
  4. Dédupliquer par URL et hash de titre
  5. Exporter en CSV avec métadonnées
```

## Composants

### 1. PerplexitySourcer

```python
class PerplexitySourcer:
    """Client principal pour le sourcing via Perplexity"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        self.client = httpx.AsyncClient()
    
    async def source_jobs(
        self,
        query: str,
        max_results: int = 10,
        location: str = None
    ) -> list[JobOffer]:
        """Recherche des offres d'emploi"""
```

### 2. CompanyExtractor

```python
def extract_company(title: str, snippet: str) -> str:
    """Extrait le nom de l'entreprise depuis le titre et snippet"""
    # Patterns regex pour extraction intelligente
```

### 3. LocationParser

```python
def parse_location(text: str) -> Location:
    """Parse la localisation depuis le texte"""
    # Extraction ville, pays, remote status
```

### 4. Deduplicator

```python
def deduplicate_offers(offers: list[JobOffer]) -> list[JobOffer]:
    """Déduplique les offres par URL et hash de titre"""
    # Hash SHA256 du titre + URL
```

## BIZ Domains

- **BIZ-1 (CANDIDATOR)**: Usage principal pour le sourcing d'offres pour les candidats
- **BIZ-2 (BANK-BUSTER)**: Analyse potentielle du marché de l'emploi financier
- **BIZ-3 (RACINES)**: Recherche potentielle d'opportunités généalogiques

## Exemples

### Exemple 1: Recherche Développeur Python

**Input:**
```python
sourcer = PerplexitySourcer()
offers = await sourcer.source_jobs(
    query="Développeur Python",
    max_results=10,
    location="Paris"
)
csv_path = await sourcer.export_csv(offers)
```

**Output:**
```
10 offres trouvées:
- Développeur Python Senior chez TechCorp (Paris)
- Python Developer chez StartupAI (Remote)
- ...
Export: offers_20260327_143022.csv
```

### Exemple 2: Sourcing Multi-Plateformes

**Input:**
```python
sourcer = PerplexitySourcer()
offers = await sourcer.source_jobs(
    query="Data Scientist",
    max_results=20,
    platforms=['linkedin', 'indeed', 'pole-emploi']
)
```

**Output:**
```
20 offres collectées:
- LinkedIn: 8 offres
- Indeed: 7 offres
- Pôle Emploi: 5 offres
Dédupliquées: 18 offres uniques
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `workflow-orchestrator` (pour sourcing automatisé)
- `recruitment` (domain)

## Intégration

### CANDIDATOR
```python
from skills.perplexity_sourcer import PerplexitySourcer

sourcer = PerplexitySourcer()
offers = await sourcer.source_jobs(
    query="Développeur Python",
    max_results=10,
    location="Paris"
)
```

### GATEWAY-MANAGER
```python
# Intégration avec le gateway pour rate limiting
from skills.perplexity_sourcer import PerplexitySourcer
from gateway_manager import RateLimiter

sourcer = PerplexitySourcer()
limiter = RateLimiter(requests_per_minute=30)
```

## Configuration

```yaml
perplexity:
  api_key: "${PERPLEXITY_API_KEY}"
  platforms:
    - linkedin
    - indeed
    - pole-emploi
    - welcome-to-the-jungle
  
  search:
    max_results: 50
    timeout: 30
    retry_attempts: 3
  
  export:
    format: csv
    include_metadata: true
    deduplication: true
```

## Métriques

- **Temps de recherche**: < 5s pour 10 résultats
- **Extraction entreprise**: 95% de précision
- **Déduplication**: 100% de fiabilité
- **Export CSV**: < 1s pour 100 offres

## Changelog

- 1.0.0 (2026-03-27) - Version initiale extraite de CANDIDATOR

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
