---
name: notion-connector
description: Skill for connecting to Notion API and retrieving data from databases
triggers:
  - notion
  - api
  - database
  - data-retrieval
  - connector
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - notion
  - api
  - database
  - data
  - connector
  - integration
phi_weight: 0.005
---

# Notion Connector — API Notion et Bases de Données

## Description

Ce skill fondamental fournit une interface unifiée pour se connecter à l'API Notion et récupérer des données depuis les bases de données. Il normalise les données, calcule les hashs d'intégrité et exporte vers différents formats.

## Usage

```
Quand [récupération de données Notion] OU [synchronisation de bases de données]
→ Appliquer notion-connector pour:
  1. Se connecter à l'API Notion
  2. Récupérer les données avec pagination
  3. Normaliser en DataFrame pandas
  4. Calculer les hashs d'intégrité
  5. Exporter vers JSON/CSV
```

## Composants

### 1. NotionIDEClient

```python
class NotionIDEClient:
    """Client principal pour l'API Notion"""
    
    def __init__(self, config: NotionConfig):
        self.token = config.token
        self.databases = config.databases
    
    def get_database(self, database_id: str) -> pd.DataFrame:
        """Récupère une base de données Notion"""
        # Implémentation avec pagination automatique
```

### 2. DataNormalizer

```python
def normalize_notion_data(raw_data: dict) -> pd.DataFrame:
    """Normalise les données Notion en DataFrame"""
    # Conversion des propriétés Notion en colonnes pandas
```

### 3. IntegrityHasher

```python
def calculate_integrity_hash(data: pd.DataFrame) -> str:
    """Calcule un hash d'intégrité pour anti-hallucination"""
    # Hash SHA256 des données normalisées
```

## BIZ Domains

- **BIZ-1 (CANDIDATOR)**: Récupération des expériences et profils candidats depuis les bases Notion
- **BIZ-2 (BANK-BUSTER)**: Synchronisation potentielle de données financières
- **BIZ-3 (RACINES)**: Gestion potentielle de données généalogiques

## Exemples

### Exemple 1: Récupération Expériences Candidat

**Input:**
```python
config = load_config_from_env()
client = NotionIDEClient(config)
experiences_df = client.get_database('experiences')
```

**Output:**
```
DataFrame avec colonnes:
- id: str
- title: str
- company: str
- start_date: datetime
- end_date: datetime
- description: str
- integrity_hash: str
```

### Exemple 2: Export Multi-Format

**Input:**
```python
# Export JSON
json_data = client.export_json(experiences_df)

# Export CSV
csv_path = client.export_csv(experiences_df, 'experiences.csv')
```

**Output:**
- JSON: Données structurées avec métadonnées
- CSV: Fichier exportable vers Excel/Google Sheets

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `workflow-orchestrator` (pour récupération de données)
- `recruitment` (domain)

## Intégration

### CANDIDATOR
```python
from skills.notion_connector import NotionIDEClient, load_config_from_env

config = load_config_from_env()
client = NotionIDEClient(config)
experiences = client.get_database('experiences')
```

### FLUENCE
```python
# Utilisation pour synchronisation contenu
from skills.notion_connector import NotionIDEClient

client = NotionIDEClient(config)
content_db = client.get_database('content')
```

## Configuration

```yaml
notion:
  token: "${NOTION_TOKEN}"
  databases:
    experiences: "${NOTION_EXPERIENCES_DB_ID}"
    profiles: "${NOTION_PROFILES_DB_ID}"
  
  export:
    formats: [json, csv]
    integrity_hash: true
    pagination_limit: 100
```

## Métriques

- **Temps de connexion**: < 2s
- **Pagination**: 100 items/page
- **Hash calculation**: < 100ms pour 1000 lignes
- **Export CSV**: < 500ms pour 1000 lignes

## Changelog

- 1.0.0 (2026-03-27) - Version initiale extraite de CANDIDATOR

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
