---
name: gedcom-parser
description: Skill for parsing and analyzing GEDCOM genealogy files
triggers:
  - gedcom
  - genealogy
  - family-tree
  - parsing
  - ancestry
domain: genealogy
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - gedcom
  - genealogy
  - family-tree
  - parsing
  - ancestry
  - racines
phi_weight: 0.005
rgpd_note: "Données personnelles sensibles (noms, dates de naissance, liens familiaux). Conformité RGPD requise."
alive_check_required: true
---

# GEDCOM Parser — Analyse de Fichiers Généalogiques

## Description

Ce skill domaine parse et analyse les fichiers GEDCOM (GEnealogical Data COMmunication). Il extrait les arbres généalogiques, les relations familiales, les événements de vie et les métadonnées pour les structurer en format exploitable.

## Usage

```
Quand [analyse généalogique] OU [parsing GEDCOM] OU [construction arbre familial]
→ Appliquer gedcom-parser pour:
  1. Parser les fichiers GEDCOM (.ged)
  2. Extraire les individus et leurs attributs
  3. Identifier les relations familiales
  4. Reconstruire l'arbre généalogique
  5. Exporter en JSON/GraphML
```

## Composants

### 1. GEDCOMParser

```python
class GEDCOMParser:
    """Parser principal pour fichiers GEDCOM"""
    
    def __init__(self, config: ParserConfig):
        self.config = config
        self.individuals = {}
        self.families = {}
    
    def parse(self, gedcom_file: str) -> FamilyTree:
        """Parse un fichier GEDCOM et retourne un arbre familial"""
```

### 2. IndividualExtractor

```python
def extract_individuals(records: list[Record]) -> dict[str, Individual]:
    """Extrait les individus du fichier GEDCOM"""
    # Parsing des enregistrements INDI
```

### 3. FamilyRelationMapper

```python
def map_family_relations(records: list[Record]) -> dict[str, Family]:
    """Mappe les relations familiales"""
    # Parsing des enregistrements FAM
```

### 4. EventParser

```python
def parse_events(record: Record) -> list[LifeEvent]:
    """Parse les événements de vie (naissance, mariage, décès)"""
    # Extraction BIRT, MARR, DEAT, etc.
```

## BIZ Domains

- **BIZ-3 (RACINES)**: Usage principal pour l'analyse généalogique
- **BIZ-1 (CANDIDATOR)**: Extraction potentielle de données biographiques

## Exemples

### Exemple 1: Parsing Fichier GEDCOM

**Input:**
```python
parser = GEDCOMParser(config)
tree = parser.parse("family.ged")

print(f"Individus: {len(tree.individuals)}")
print(f"Familles: {len(tree.families)}")
```

**Output:**
```
Individus: 156
Familles: 45
Arbre généalogique: 8 générations
Export: family_tree.json
```

### Exemple 2: Extraction Relations

**Input:**
```python
relations = parser.get_relations("I001")
# Retourne parents, conjoints, enfants
```

**Output:**
```json
{
  "individual": "I001",
  "name": "Jean Dupont",
  "parents": ["I002", "I003"],
  "spouses": ["I004"],
  "children": ["I005", "I006", "I007"]
}
```

## Dépendances

### Dépend de
- Aucun

### Requis par
- `alive-check` (pour vérification de statut)
- `genealogy` (domain)

## Intégration

### RACINES
```python
from skills.gedcom_parser import GEDCOMParser, ParserConfig

config = ParserConfig(
    strict_mode=True,
    extract_events=True
)
parser = GEDCOMParser(config)
tree = parser.parse("racines.ged")
```

## Configuration

```yaml
gedcom_parser:
  strict_mode: true
  encoding: UTF-8
  extract_events: true
  extract_notes: true
  extract_sources: true
  
  export:
    formats: [json, graphml, csv]
    include_metadata: true
  
  rgpd:
    anonymize_living: true
    retention_days: 3650
```

## Métriques

- **Temps de parsing**: < 5s pour 1000 individus
- **Précision extraction**: 98%
- **Couverture relations**: 95%

## Changelog

- 1.0.0 (2026-03-27) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
