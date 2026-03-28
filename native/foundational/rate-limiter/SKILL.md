---
id: rate-limiter
label: Rate Limiter Skill
family: foundational
rank: F0
biz_domains: ["BIZ-FINANCE", "BIZ-BOOKING"]
owner: BIZ-2
ref: ISI-20260328-RATELIMITER
phi_weight: 0.005
rgpd_note: "Logs de rate limiting peuvent révéler des patterns d'utilisation — rétention max 30j"
---

# RateLimiterSkill

Contrôle de débit sur les appels API externes et internes. Supporte token bucket et sliding window.

## Usage

```python
from skills.foundational.rate_limiter import RateLimiterSkill
limiter = RateLimiterSkill(strategy="sliding_window", max_calls=100, window_seconds=60)
with limiter.guard(key="user:123"):
    call_external_api()
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `strategy` | str | `token_bucket` \| `sliding_window` |
| `max_calls` | int | Nombre max d'appels par fenêtre |
| `window_seconds` | int | Durée de la fenêtre en secondes |

## Consommateurs

- `BIZ-FINANCE` (owner) — protection API bancaires, scraping régulé
- `BIZ-BOOKING` (consumer) — limitation requêtes de réservation
