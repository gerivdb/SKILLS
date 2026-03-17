---
name: recruitment
description: Matching candidats et analyse de profil pour recrutement
triggers:
  - recruitment
  - candidate
  - matching
  - hiring
  -CV
  - profil
domain: recruitment
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-17
updated: 2026-03-17
tags:
  - recruitment
  - matching
  - candidates
  - hiring
phi_weight: 0.005
deps:
  - product-context
---

# Recruitment — Matching Candidats

## Description

Ce skill domaine gère le matching entre candidats et postes. Il est utilisé par CANDIDATOR pour l'analyse et le matching de profils.

## Fonctionnalités

### 1. Profile Analyzer

```python
def analyze_profile(cv_text: str) -> CandidateProfile:
    """
    Analyse un CV et extrait:
    - Compétences techniques
    - Expérience
    - Formation
    - Soft skills
    """
    # NLP processing + extraction
```

### 2. Job Matcher

```python
def match_to_jobs(
    profile: CandidateProfile,
    jobs: list[JobDescription]
) -> list[Match]:
    """
    Calcule un score de compatibilité
    pour chaque poste
    """
    # Scoring algorithm
```

### 3. Ranking Engine

```python
def rank_candidates(
    candidates: list[CandidateProfile],
    job: JobDescription
) -> list[Ranking]:
    """
    Classe les candidats par score
    et retourne le top matches
    """
```

## Usage

```
Quand [nouveau CV soumis]
→ Analyser profil (analyze_profile)
→ Matcher avec jobs ouverts (match_to_jobs)
→ Classer résultats (rank_candidates)
→ Générer recommandations
```

## Exemples

### Exemple 1: Matching Développeur

**Input CV:**
```
Expérience: 5 ans Python, 3 ans JavaScript
Formation: Master Informatique
Seniorité: Senior
```

**Job Match:**
```
Poste: Full Stack Developer
Required: Python, React, 3+ ans
Score: 87%
```

**Output:**
- Match: ✓ (87% match)
- Points forts: Python, expérience
- Gaps: React manquant
- Recommandation: Entretien technique

### Exemple 2: Ranking Multi-Candidats

**Input:** 50 candidats pour 1 poste

**Process:**
1. Filter: 20 passent le screening initial
2. Score: 20 calculés
3. Rank: Top 5 sélectionnés
4. Output: Liste ordonnée

## Dépendances

### Dépend de
- `product-context` - Pour adapter les critères selon le poste

### Requis par
- CANDIDATOR

## Intégration

### CANDIDATOR
```python
from skills.recruitment import (
    analyze_profile,
    match_to_jobs,
    rank_candidates
)

# Usage
profile = analyze_profile(cv_text)
matches = match_to_jobs(profile, open_jobs)
top5 = rank_candidates(matches, senior_dev_role)
```

### BRAIN (Analysis)
```python
from skills.recruitment import get_skill_gaps

# Identification des gaps
gaps = get_skill_gaps(profile, target_job)
# → ["React", "TypeScript"]
```

## Configuration

```yaml
recruitment:
  scoring:
    skills_weight: 0.4
    experience_weight: 0.3
    formation_weight: 0.2
    soft_skills_weight: 0.1
  
  thresholds:
    min_score: 60
    interview_threshold: 75
  
  ranking:
    top_candidates: 5
    include_gaps: true
```

## Algorithme de Matching

```
Score = (Skills × 0.4) + (Experience × 0.3) + (Formation × 0.2) + (Soft × 0.1)

Where:
- Skills = % de compétences requises présentes
- Experience = Années / Années requises (cappé à 1.0)
- Formation = Niveau matching
- Soft = Soft skills matching
```

## Changelog

- 1.0.0 (2026-03-17) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
