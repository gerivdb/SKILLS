---
name: finance
description: Analyse financière et banking pour décisions métier
triggers:
  - finance
  - banking
  - analysis
  - transactions
  - budgétaire
  - investissement
domain: finance
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-17
updated: 2026-03-17
tags:
  - finance
  - banking
  - analysis
  - transactions
phi_weight: 0.005
deps:
  - ecosystem-principles
---

# Finance — Analyse Financière

## Description

Ce skill domaine fournit des capacités d'analyse financière et banking. Il est utilisé par BANK-BUSTER pour l'analyse de transactions et les recommandations d'investissement.

## Fonctionnalités

### 1. Transaction Analyzer

```python
def analyze_transactions(transactions: list[Transaction]) -> Analysis:
    """
    Analyse un flux de transactions:
    - Catégorisation
    - Détection anomalies
    - Tendances
    """
```

### 2. Risk Assessor

```python
def assess_risk(profile: FinancialProfile) -> RiskScore:
    """
    Calcule un score de risque:
    - Credit risk
    - Market risk
    - Operational risk
    """
```

### 3. Investment Recommender

```python
def recommend_investments(
    profile: FinancialProfile,
    goals: InvestmentGoals
) -> list[Recommendation]:
    """
    Génère des recommandations
    d'investissement personnalisées
    """
```

## Usage

```
Quand [nouvelle transaction]
→ Catégoriser (categorize)
→ Détecter anomalies (detect_anomalies)
→ Mettre à jour profil
```

## Exemples

### Exemple 1: Catégorisation Transactions

**Input:**
```json
[
  {"amount": -50, "merchant": "Carrefour"},
  {"amount": -1200, "merchant": "Loyer"},
  {"amount": 3500, "description": "Salaire"}
]
```

**Output:**
```json
{
  "alimentaire": 50,
  "logement": 1200,
  "revenus": 3500,
  "balance": 2250
}
```

### Exemple 2: Recommandation Investissement

**Profil:**
- Épargne: 10,000€
- Horizon: 10 ans
- Profil: Modéré

**Recommandations:**
1. ETF World: 60% (diversifié)
2. Obligations: 30% (stabilité)
3. Crypto: 10% (speculatif)

## Dépendances

### Dépend de
- `ecosystem-principles` - Pour validation KISS/DRY des algorithmes

### Requis par
- BANK-BUSTER

## Intégration

### BANK-BUSTER
```python
from skills.finance import (
    analyze_transactions,
    assess_risk,
    recommend_investments
)

# Usage
analysis = analyze_transactions(monthly_transactions)
risk = assess_risk(customer_profile)
recommendations = recommend_investments(profile, goals)
```

### FLUENCE (Rapports)
```python
from skills.finance import generate_report

# Génération rapport financier
report = generate_report(analysis, format="pdf")
```

## Configuration

```yaml
finance:
  categories:
    - revenus
    - logement
    - alimentation
    - transport
    - divertissement
  
  risk_thresholds:
    low: 0.3
    medium: 0.6
    high: 0.8
  
  analysis:
    anomaly_detection: true
    trends: true
    forecasting: true
```

## Changelog

- 1.0.0 (2026-03-17) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
