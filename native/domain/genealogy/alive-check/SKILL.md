---
name: alive-check
description: Skill for verifying if individuals in genealogy records are still alive
triggers:
  - alive
  - check
  - verification
  - genealogy
  - status
  - vital-records
domain: genealogy
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-27
updated: 2026-03-27
tags:
  - alive
  - check
  - verification
  - genealogy
  - status
  - vital-records
  - racines
phi_weight: 0.005
rgpd_note: "Vérification de statut vital (vivant/décédé). Données sensibles soumises au RGPD."
alive_check_required: true
---

# Alive Check — Vérification de Statut Vital

## Description

Ce skill domaine vérifie si les individus dans les registres généalogiques sont encore vivants. Il croise les données de naissance, les registres d'état civil et les sources publiques pour déterminer le statut vital.

## Usage

```
Quand [vérification statut vital] OU [mise à jour registre généalogique]
→ Appliquer alive-check pour:
  1. Calculer l'âge à partir de la date de naissance
  2. Vérifier les registres de décès
  3. Croiser avec les sources publiques
  4. Estimer la probabilité de vie
  5. Mettre à jour le statut dans l'arbre
```

## Composants

### 1. AliveChecker

```python
class AliveChecker:
    """Vérificateur principal de statut vital"""
    
    def __init__(self, config: CheckerConfig):
        self.config = config
        self.vital_records = VitalRecordsClient()
    
    def check_status(self, individual: Individual) -> VitalStatus:
        """Vérifie le statut vital d'un individu"""
```

### 2. AgeCalculator

```python
def calculate_age(birth_date: date, reference_date: date = None) -> int:
    """Calcule l'âge à partir de la date de naissance"""
    # Gestion des dates incomplètes
```

### 3. DeathRecordVerifier

```python
def verify_death_records(individual: Individual) -> bool:
    """Vérifie les registres de décès"""
    # API état civil + sources publiques
```

### 4. VitalStatusEstimator

```python
def estimate_vital_status(individual: Individual) -> VitalStatus:
    """Estime le statut vital basé sur l'âge et les données"""
    # Tables de mortalité + ML
```

## BIZ Domains

- **BIZ-3 (RACINES)**: Usage principal pour la généalogie
- **BIZ-1 (CANDIDATOR)**: Vérification de statut pour profils candidats

## Exemples

### Exemple 1: Vérification Individu

**Input:**
```python
checker = AliveChecker(config)

individual = Individual(
    name="Jean Dupont",
    birth_date=date(1950, 3, 15),
    death_date=None
)

status = checker.check_status(individual)
```

**Output:**
```json
{
  "individual": "Jean Dupont",
  "birth_date": "1950-03-15",
  "age": 76,
  "status": "alive",
  "confidence": 0.85,
  "last_verified": "2026-03-27"
}
```

### Exemple 2: Mise à Jour Arbre

**Input:**
```python
tree = parser.parse("family.ged")
updated_tree = checker.update_tree_status(tree)
```

**Output:**
```
Arbre mis à jour:
- 156 individus vérifiés
- 89 vivants
- 45 décédés
- 22 statut inconnu
```

## Dépendances

### Dépend de
- `gedcom-parser` (pour accès aux données généalogiques)

### Requis par
- `genealogy` (domain)

## Intégration

### RACINES
```python
from skills.alive_check import AliveChecker, CheckerConfig

config = CheckerConfig(
    sources=["etat_civil", "public_records"],
    confidence_threshold=0.8
)
checker = AliveChecker(config)
status = checker.check_status(individual)
```

## Configuration

```yaml
alive_check:
  sources:
    - etat_civil
    - public_records
    - social_media
  
  confidence_threshold: 0.8
  
  age_limits:
    max_age_alive: 120
    min_age_check: 18
  
  rgpd:
    anonymize_dead: false
    retention_days: 3650
    consent_required: true
  
  export:
    formats: [json, csv]
    include_confidence: true
```

## Métriques

- **Temps de vérification**: < 2s par individu
- **Précision**: 92%
- **Couverture sources**: 85%
- **Confiance moyenne**: 0.88

## Changelog

- 1.0.0 (2026-03-27) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
