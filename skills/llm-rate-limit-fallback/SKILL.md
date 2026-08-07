# Skill: llm-rate-limit-fallback

## Objectif
Gerer automatiquement l'erreur recurrente:
```
Upstream error from Nvidia: ResourceExhausted: Worker local total request limit reached (32/32)
```

## Problemes
- Modele par defaut: `nvidia/nemotron-3-ultra-550b-a55b:free` (OpenRouter)
- Limite dure: 32 requetes/worker (free tier)
- Pas de retry, pas de queue, erreur immediate
- Aucun fallback automatique -> switch manuel requis

## Declencheurs
| Hook | Moment | Action |
|---|---|---|
| `pre-request` | Avant chaque appel LLM | Verifier compteur local (si dispo) |
| `post-error` | Sur erreur rate-limit | Detecter pattern, declencher fallback |
| `session-boot` | Debut session | Lire quota connu, logger etat |

## Niveaux d'integration

### Niveau 1: Skill KiloCode (Client-side)
- Detecte l'erreur dans la reponse LLM
- Suggere/applique fallback via `switch_model()`
- Log dans WAL: `[LLM_FALLBACK] from=nemotron-3-ultra-free to=glm-4.5 reason=rate_limit_32`

### Niveau 2: GATEWAY-MANAGER (Server-side) - **RECOMMANDE**
- Routeur central LLM (`D:\DO\WEB\TOOLS\L1-INFRA\GATEWAY-MANAGER\src\gateway_manager\router.py`)
- Detection native `ResourceExhausted: Worker local total request limit reached (32/32)`
- Backend dedie: `openrouter-nemotron-free` avec quota 30 RPM (conservative)
- Failover automatique vers `google-ai-studio`, `groq`, `github-models`, etc.
- Task-type routing: `general`, `zero_conf_fallback` incluent `openrouter-nemotron-free`

### Niveau 3: AGENT_RAM.yaml (Cross-repo governance)
- Entree `ERR_LLM_001` dans `llm_known_errors`
- Mitigation reference: skill + GATEWAY-MANAGER + ADR

## Modeles de fallback (ordre de priorite)
1. `z.ai/glm-4.5` - free, limite plus haute, bon raisonnement
2. `qwen/qwen3-coder` - free, specialise code, limite plus haute
3. `nvidia/nemotron-3-ultra-550b-a55b` (payant) - meme modele, pas de limite

## Configuration
```yaml
# .kilocode/llm-fallback.yaml
fallback_models:
  - id: "z.ai/glm-4.5"
    provider: "openrouter"
    free: true
    priority: 1
  - id: "qwen/qwen3-coder"
    provider: "openrouter"
    free: true
    priority: 2
  - id: "nvidia/nemotron-3-ultra-550b-a55b"
    provider: "openrouter"
    free: false
    priority: 3
rate_limit_pattern: "Worker local total request limit reached \(\d+/32\)"
max_retries: 1
log_to_wal: true
```

## Implementation (Python)
```python
# skills/llm-rate-limit-fallback/detector.py
import re
import yaml
from pathlib import Path

RATE_LIMIT_PATTERN = re.compile(r"Worker local total request limit reached \(\d+/32\)")

def detect_rate_limit_error(error_msg: str) -> bool:
    return bool(RATE_LIMIT_PATTERN.search(error_msg))

def get_fallback_model(config_path: Path) -> str:
    with open(config_path) as f:
        config = yaml.safe_load(f)
    for model in sorted(config["fallback_models"], key=lambda m: m["priority"]):
        if model["free"] or has_budget(model["id"]):
            return model["id"]
    return config["fallback_models"][0]["id"]

def has_budget(model_id: str) -> bool:
    # TODO: integrer avec Kilo Gateway billing API
    return False
```

## Integration KiloCode
- Declarer dans `.kilocode/skills.yaml` (ou global config)
- Hook `post-error` -> appelle `detector.detect_rate_limit_error()`
- Si vrai -> `switch_model(get_fallback_model())` -> retry request
- Log dans WAL : `[LLM_FALLBACK] from=nemotron-3-ultra-free to=glm-4.5 reason=rate_limit_32`

## Integration GATEWAY-MANAGER
```python
# Dans src/gateway_manager/router.py
# Backend dedie avec quota conservateur
"openrouter-nemotron-free": {
    "max_tpm": 30,
    "priority": 7,
    "is_free_tier": True,
    "free_tier_quota_rpm": 30,
    "hard_limit_per_worker": 32,
}

# Detection saturation Nemotron Free
if "ResourceExhausted" in error_text and "Worker local total request limit reached (32/32)" in error_text:
    self._nemotron_free_saturated_until[backend_id] = datetime.now() + timedelta(seconds=60)
    return {"status": "saturated", "retry_after": 60}
```

## References
- ADR : `ADR-2026-07-29-002-LLM-RATE-LIMIT-FALLBACK-POLICY`
- INTENT cross-repo : `GOVERNANCE-HUB/INTENTS/INTENT-LLM-RATE-LIMIT-FALLBACK-CROSSREPO.md`
- INTENT local FLUENCE : `FLUENCE/INTENTS/INTENT-NEMOTRON-3-ULTRA-RATE-LIMIT.md`
- AGENT_RAM : `GOVERNANCE-HUB/AGENT_RAM.yaml` section `llm_known_errors` -> `ERR_LLM_001`
- GATEWAY-MANAGER : `D:\DO\WEB\TOOLS\L1-INFRA\GATEWAY-MANAGER\src\gateway_manager\router.py`
- Provider registry : `D:\DO\WEB\TOOLS\L1-INFRA\GATEWAY-MANAGER\managers\llm_provider_registry.py`
- Backends config : `D:\DO\WEB\TOOLS\L1-INFRA\GATEWAY-MANAGER\config\backends.yaml`