---
name: ecosystem-principles
description: Principes architecturaux ONTOLOGY, DRY, KISS, φ-CPS pour ecosystem-1
triggers:
  - ontology
  - dry
  - kiss
  - phi-cps
  - principles
  - architecture
  - gouvernance
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-17
updated: 2026-03-17
tags:
  - principles
  - architecture
  - governance
  - ontology
phi_weight: 0.005
---

# Ecosystem Principles — Principes Architecturaux

## Description

Ce skill fondateur expose et applique les principes architecturaux fondamentaux d'ecosystem-1. Il guide les décisions de conception selon les standards établis.

## Principes

### 1. ONTOLOGY

**Définition**: Chaque entité doit avoir une définition claire et canonique dans le système.

```python
# Exemple d'application
class Entity:
    """Toute entité doit avoir:
    - Identifiant unique (UUID)
    - Métadonnées standardisées
    - Traçabilité complète
    """
```

**Usage**:
```
Quand [création de nouvelle entité]
→ Vérifier existence dans l'ontologie
→ Définir les propriétés canoniques
→ Enregistrer dans le registre
```

### 2. DRY (Don't Repeat Yourself)

**Définition**: Une information ne doit exister qu'en un seul endroit.

**Usage**:
```
Quand [nouvelle fonctionnalité]
→ Identifier si elle existe déjà
→ Réutiliser au lieu de dupliquer
→ Extraire si duplication nécessaire
```

**Patterns**:
- Shared libraries
- Common modules
- Registry-based lookup

### 3. KISS (Keep It Simple, Stupid)

**Définition**: Privilégier la simplicité sur la complexité.

**Usage**:
```
Quand [conception complexe]
→ Évaluer si nécessaire
→ Décomposer en tâches simples
→ Valider chaque étape
```

**Gardes**:
- Si >100 lignes, éclater
- Si >3 dépendances, repenser
- Si >1 niveau d'indirection, simplifier

### 4. φ-CPS (Phi - Cognitive Processing Score)

**Définition**: Métrique de complexité cognitive des systèmes.

```python
# Calcul du φ-CPS
def calculate_phi_cps(components: list, dependencies: list) -> float:
    """
    φ-CPS = Σ(weight_i * complexity_i) / coherence_factor
    """
    base = sum(c.weight * c.complexity for c in components)
    coherence = calculate_coherence(dependencies)
    return base / coherence
```

**Usage**:
```
Quand [nouveau composant]
→ Estimer le φ-CPS
→ Vérifier < 0.5 (target)
→ Alerter si > 0.7 (seuil critique)
```

## Application dans ecosystem-1

### Dépôts

| Dépôt | Principes Prioritaires |
|-------|------------------------|
| ECOYSTEM | ONTOLOGY, φ-CPS |
| FLUENCE | DRY, KISS |
| BRAIN | ONTOLOGY, DRY |
| CANDIDATOR | KISS, DRY |
| GERIBOOKING | DRY, φ-CPS |

### Décisions

| Situation | Principe Appliqué |
|-----------|-------------------|
| Nouvelle entité | ONTOLOGY |
| Code dupliqué | DRY |
| Design complexe | KISS |
| Architecture système | φ-CPS |

## Exemples

### Exemple 1: Création d'un Citizen

```yaml
# Bon: Application de ONTOLOGY
citizen:
  name: my-new-citizen
  ontology: "Defined in citizens/ontology.yaml"
  properties:
    - name
    - level
    - lifecycle
  metadata:
    created: 2026-03-17
```

### Exemple 2: Refactoring DRY

```python
# Avant: Duplication
def calculate_score_a():
    return sum(items) / len(items)

def calculate_score_b():
    return sum(items) / len(items)

# Après: DRY
def calculate_mean(items):
    return sum(items) / len(items)
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `content` (domain)
- `finance` (domain)

## Intégration

### BRAIN
```python
# Validation des principes
from skills.principles import validate_ontology, check_dry, assess_kiss
```

### ECOYSTEM
```python
# Calcul φ-CPS
from skills.principles import calculate_phi_cps
```

## Changelog

- 1.0.0 (2026-03-17) - Version initiale

---

*Skill natif gerivdb · Part du registre SKILLS ecosystem-1*
