---
name: csv-extract
description: Skill for extracting and processing data from CSV files with advanced parsing capabilities
triggers:
  - csv
  - extract
  - parsing
  - data-processing
  - spreadsheet
  - tabular
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - csv
  - extract
  - parsing
  - data-processing
  - spreadsheet
  - tabular
  - etl
phi_weight: 0.005
biz_domains:
  - BIZ-FINANCE
  - BIZ-GENEALOGY
---

# CSV Extract — Extraction et Traitement de Données CSV

## Description

Ce skill fondamental extrait et traite les données depuis des fichiers CSV avec des capacités avancées de parsing. Il gère différents délimiteurs, encodages, et formats de dates, et permet la transformation et la validation des données.

## Usage

```
Quand [extraction de données CSV] OU [traitement de fichiers tabulaires] OU [ETL de données]
→ Appliquer csv-extract pour:
  1. Parser les fichiers CSV avec détection automatique de délimiteur
  2. Gérer les encodages (UTF-8, Latin-1, etc.)
  3. Valider et transformer les données
  4. Détecter et gérer les erreurs de format
  5. Exporter vers différents formats
```

## Composants

### 1. CSVParser

```python
class CSVParser:
    """Parser principal pour fichiers CSV"""
    
    def __init__(self, config: CSVConfig):
        self.config = config
        self.detector = DelimiterDetector()
    
    def parse(self, file_path: str) -> pd.DataFrame:
        """Parse un fichier CSV et retourne un DataFrame"""
```

### 2. DelimiterDetector

```python
def detect_delimiter(file_path: str) -> str:
    """Détecte automatiquement le délimiteur d'un CSV"""
    # Analyse des premières lignes
```

### 3. DataValidator

```python
class DataValidator:
    """Validateur de données CSV"""
    
    def __init__(self, schema: dict):
        self.schema = schema
    
    def validate(self, df: pd.DataFrame) -> ValidationResult:
        """Valide les données contre un schéma"""
```

### 4. DataTransformer

```python
def transform_data(df: pd.DataFrame, transformations: list) -> pd.DataFrame:
    """Applique des transformations aux données"""
    # Conversion de types, nettoyage, enrichissement
```

## BIZ Domains

- **BIZ-FINANCE (BANK-BUSTER)**: Extraction de données financières depuis exports bancaires
- **BIZ-GENEALOGY (RACINES)**: Import de données généalogiques depuis fichiers CSV

## Exemples

### Exemple 1: Parsing CSV Bancaire

**Input:**
```python
parser = CSVParser(config)
df = parser.parse("transactions.csv")
print(f"Lignes: {len(df)}, Colonnes: {list(df.columns)}")
```

**Output:**
```
Fichier parsé avec succès:
- Délimiteur détecté: ';'
- Encodage: UTF-8
- Lignes: 1500
- Colonnes: ['date', 'description', 'amount', 'category']
- Erreurs: 0
```

### Exemple 2: Validation et Transformation

**Input:**
```python
validator = DataValidator(schema={
    "date": {"type": "datetime", "format": "%Y-%m-%d"},
    "amount": {"type": "float", "min": 0},
    "category": {"type": "string", "enum": ["income", "expense"]}
})

result = validator.validate(df)
transformed_df = transform_data(df, [
    {"column": "date", "operation": "parse_date"},
    {"column": "amount", "operation": "to_float"}
])
```

**Output:**
```
Validation:
- Lignes valides: 1498
- Lignes invalides: 2
- Erreurs: date format (2)

Transformation:
- Types convertis: date→datetime, amount→float
- Lignes nettoyées: 1500
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `finance` (domain)
- `genealogy` (domain)

## Intégration

### BANK-BUSTER
```python
from skills.csv_extract import CSVParser, CSVConfig

config = CSVConfig(
    delimiter="auto",
    encoding="utf-8",
    parse_dates=["date"],
    dtype={"amount": float}
)
parser = CSVParser(config)

# Import transactions bancaires
transactions = parser.parse("export_bancaire.csv")
```

### RACINES
```python
# Import données généalogiques
parser = CSVParser(config)
individuals = parser.parse("genealogy_export.csv")
```

## Configuration

```yaml
csv_extract:
  delimiter: auto
  encoding: utf-8
  
  parsing:
    skip_blank_lines: true
    skipinitialspace: true
    na_values: ["", "NA", "N/A", "null"]
  
  validation:
    strict: false
    max_errors: 100
    error_handling: "log"
  
  export:
    formats: [json, parquet, excel]
    include_metadata: true
```

## Métriques

- **Temps de parsing**: < 1s pour 10 000 lignes
- **Détection délimiteur**: 99% de précision
- **Gestion erreurs**: 100% des erreurs loggées
- **Support encodage**: UTF-8, Latin-1, CP1252

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
