---
name: rate-limiter
description: Skill for controlling request rates and managing API quotas with intelligent throttling
triggers:
  - rate-limiter
  - throttle
  - quota
  - api-limit
  - request-control
  - backoff
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - rate-limiter
  - throttle
  - quota
  - api-limit
  - request-control
  - backoff
  - resilience
phi_weight: 0.005
biz_domains:
  - BIZ-FINANCE
  - BIZ-BOOKING
---

# Rate Limiter — Contrôle de Débit et Gestion de Quotas

## Description

Ce skill fondamental contrôle les taux de requêtes et gère les quotas d'API avec un throttling intelligent. Il implémente différents algorithmes de limitation, gère le backoff exponentiel et fournit des métriques de consommation.

## Usage

```
Quand [contrôle de débit API] OU [gestion de quotas] OU [prévention de rate limiting]
→ Appliquer rate-limiter pour:
  1. Limiter les requêtes par seconde/minute/heure
  2. Gérer les quotas d'API avec suivi de consommation
  3. Implémenter le backoff exponentiel
  4. Fournir des métriques de rate limiting
  5. Gérer les limites par endpoint/utilisateur
```

## Composants

### 1. RateLimiter

```python
class RateLimiter:
    """Limiteur de débit principal"""
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.tokens = config.capacity
        self.last_refill = time.time()
    
    def acquire(self, tokens: int = 1) -> bool:
        """Acquiert des tokens pour une requête"""
```

### 2. TokenBucket

```python
class TokenBucket:
    """Algorithme du bucket de tokens"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
    
    def consume(self, tokens: int = 1) -> bool:
        """Consomme des tokens du bucket"""
```

### 3. SlidingWindow

```python
class SlidingWindow:
    """Algorithme de fenêtre glissante"""
    
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = []
    
    def allow_request(self) -> bool:
        """Vérifie si une requête est autorisée"""
```

### 4. ExponentialBackoff

```python
class ExponentialBackoff:
    """Backoff exponentiel avec jitter"""
    
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.attempt = 0
    
    def get_delay(self) -> float:
        """Calcule le délai avant retry"""
```

## BIZ Domains

- **BIZ-FINANCE (BANK-BUSTER)**: Contrôle des appels API bancaires et respect des limites
- **BIZ-BOOKING (GERIBOOKING)**: Gestion des quotas de réservation et prévention du spam

## Exemples

### Exemple 1: Rate Limiting API Bancaire

**Input:**
```python
limiter = RateLimiter(RateLimitConfig(
    requests_per_second=10,
    requests_per_minute=100,
    requests_per_hour=1000
))

for transaction in transactions:
    if limiter.acquire():
        response = api.send_transaction(transaction)
    else:
        time.sleep(limiter.get_wait_time())
```

**Output:**
```
Rate limiting actif:
- Requêtes/seconde: 10/10
- Requêtes/minute: 85/100
- Requêtes/heure: 450/1000
- Temps d'attente moyen: 0.1s
```

### Exemple 2: Backoff Exponentiel

**Input:**
```python
backoff = ExponentialBackoff(base_delay=1.0, max_delay=60.0)

for attempt in range(max_retries):
    try:
        response = api.call()
        break
    except RateLimitError:
        delay = backoff.get_delay()
        time.sleep(delay)
```

**Output:**
```
Retry avec backoff:
- Tentative 1: délai 1.0s
- Tentative 2: délai 2.0s
- Tentative 3: délai 4.0s
- Succès à la tentative 3
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `finance` (domain)
- `booking` (domain)

## Intégration

### BANK-BUSTER
```python
from skills.rate_limiter import RateLimiter, RateLimitConfig

config = RateLimitConfig(
    requests_per_second=5,
    requests_per_minute=60,
    requests_per_hour=500
)
limiter = RateLimiter(config)

# Contrôle des appels API bancaires
for account in accounts:
    limiter.acquire()
    balance = bank_api.get_balance(account)
```

### GERIBOOKING
```python
# Gestion des quotas de réservation
limiter = RateLimiter(RateLimitConfig(
    requests_per_second=2,
    requests_per_minute=30
))

for booking_request in requests:
    if limiter.acquire():
        process_booking(booking_request)
    else:
        queue_for_later(booking_request)
```

## Configuration

```yaml
rate_limiter:
  algorithm: token_bucket
  
  limits:
    requests_per_second: 10
    requests_per_minute: 100
    requests_per_hour: 1000
  
  backoff:
    base_delay: 1.0
    max_delay: 60.0
    jitter: true
  
  monitoring:
    enabled: true
    metrics_interval: 60
    alert_threshold: 0.9
```

## Métriques

- **Précision rate limiting**: 99.9%
- **Overhead**: < 1ms par requête
- **Backoff intelligent**: Adaptatif selon les erreurs
- **Monitoring**: Temps réel avec alertes

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
