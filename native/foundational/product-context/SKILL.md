---
name: product-context
description: Contextualisation produit et audience pour optimisation marché
triggers:
  - product-context
  - audience
  - market-fit
  - positionnement
  - persona
  - cible
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-17
updated: 2026-03-17
tags:
  - contextualization
  - audience
  - marketing
  - product
phi_weight: 0.005
---

# Product Context — Contextualisation Produit

## Description

Ce skill fondateur permet de contextualiser un produit ou service en fonction de son audience cible. Il analyse et génère des informations de positionnement market-fit.

## Usage

```
Quand [création de contenu commercial] OU [définition de persona] OU [analyse de marché]
→ Appliquer product-context pour:
  1. Identifier l'audience cible
  2. Définir le positionnement
  3. Adapter le message
```

## Composants

### 1. Audience Analyzer

```python
def analyze_audience(product_description: str) -> AudienceProfile:
    """Analyse le produit et déduit l'audience optimale"""
    # Implémentation dans FLUENCE/BRAIN
```

### 2. Positionnement Generator

```python
def generate_positioning(audience: AudienceProfile, competitors: list) -> Positioning:
    """Génère un positionnement différenciant"""
```

### 3. Message Adapter

```python
def adapt_message(base_message: str, audience: AudienceProfile) -> str:
    """Adapte le message à l'audience cible"""
```

## Exemples

### Exemple 1: Landing Page SaaS

**Input:**
- Produit: "Outil de gestion de projet pour équipes"
- Audience: "PME, 10-50 employés"

**Output:**
- Titre: "Gérez vos projets d'équipe sans complexité"
- Sous-titre: "La solution pensée pour les PME qui grandissent"
- CTA: "Essai gratuit 14 jours"

### Exemple 2: Email Commercial

**Input:**
- Produit: "CRM pourStartup"
- Audience: "Startup tech, seed Series A"

**Output:**
- Opening: "Félicitations pour votre levée!"
- Proposition: "Centralisez vos relations clients dès le jour 1"

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `content` (domain)
- `booking` (domain)
- `recruitment` (domain)

## Intégration

### FLUENCE
```python
# Utilisation dans FLUENCE
from skills.product_context import analyze_audience, generate_positioning
```

### BRAIN
```python
# Utilisation dans BRAIN
context = product_context.analyze(product_description)
```

## Changelog

- 1.0.0 (2026-03-17) - Version initiale

---

*Skill natif gerivdb · Part du registre SKILLS ecosystem-1*
