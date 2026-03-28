---
name: cv-parser
description: Skill for parsing and extracting structured data from CV/resume documents
triggers:
  - cv
  - resume
  - parsing
  - extraction
  - recruitment
domain: recruitment
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - cv
  - resume
  - parsing
  - extraction
  - recruitment
  - candidate
phi_weight: 0.005
---

# CV Parser — Extraction de Données depuis CV/Resume

## Description

Ce skill domaine extrait et structure les données depuis des documents CV/Resume. Il parse les informations personnelles, expériences professionnelles, compétences et formations pour les convertir en format structuré.

## Usage

```
Quand [analyse de CV] OU [extraction de données candidat]
→ Appliquer cv-parser pour:
  1. Extraire les informations personnelles (nom, email, téléphone)
  2. Parser les expériences professionnelles
  3. Identifier les compétences techniques et soft skills
  4. Extraire les formations et certifications
  5. Structurer en format JSON/Markdown
```

## Composants

### 1. CVParser

```python
class CVParser:
    """Parser principal pour CV/Resume"""
    
    def __init__(self, config: ParserConfig):
        self.config = config
        self.nlp = spacy.load("fr_core_news_sm")
    
    def parse(self, cv_text: str) -> CandidateProfile:
        """Parse un CV et retourne un profil structuré"""
```

### 2. ExperienceExtractor

```python
def extract_experiences(text: str) -> list[Experience]:
    """Extrait les expériences professionnelles"""
    # Patterns regex pour dates, entreprises, postes
```

### 3. SkillsDetector

```python
def detect_skills(text: str) -> SkillsProfile:
    """Détecte les compétences techniques et soft skills"""
    # NLP + dictionnaires de compétences
```

### 4. EducationParser

```python
def parse_education(text: str) -> list[Education]:
    """Parse les formations et certifications"""
    # Extraction diplômes, établissements, dates
```

## BIZ Domains

- **BIZ-1 (CANDIDATOR)**: Usage principal pour l'analyse de CV des candidats
- **BIZ-3 (RACINES)**: Extraction potentielle de données biographiques

## Exemples

### Exemple 1: Parsing CV Développeur

**Input:**
```python
parser = CVParser(config)
cv_text = """
Jean Dupont
Développeur Python Senior
Email: jean.dupont@email.com

Expérience:
- TechCorp (2020-2024): Développeur Python
- StartupAI (2018-2020): Data Scientist

Compétences: Python, Django, PostgreSQL, Docker
"""

profile = parser.parse(cv_text)
```

**Output:**
```json
{
  "name": "Jean Dupont",
  "title": "Développeur Python Senior",
  "email": "jean.dupont@email.com",
  "experiences": [
    {
      "company": "TechCorp",
      "position": "Développeur Python",
      "start_date": "2020",
      "end_date": "2024"
    }
  ],
  "skills": ["Python", "Django", "PostgreSQL", "Docker"]
}
```

## Dépendances

### Dépend de
- Aucun

### Requis par
- `recruitment` (domain)

## Intégration

### CANDIDATOR
```python
from skills.cv_parser import CVParser, ParserConfig

config = ParserConfig(language='fr', strict=True)
parser = CVParser(config)
profile = parser.parse(cv_text)
```

## Configuration

```yaml
cv_parser:
  language: fr
  strict_mode: true
  extract_skills: true
  extract_education: true
  date_format: YYYY-MM-DD
```

## Métriques

- **Temps de parsing**: < 2s par CV
- **Précision extraction**: 92%
- **Couverture compétences**: 85%

## Changelog

- 1.0.0 (2026-03-27) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
