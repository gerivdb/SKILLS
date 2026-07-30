# LLM Rate Limit Fallback - KiloCode Integration Guide

## Quick Start: How to Activate Right Now

### Option 1: Manual (Immediate - Works Now)

**At session start**, run:
```bash
python C:\Users\GG\.kilocode\skills\llm-rate-limit-fallback\session_boot.py
```

**When you hit the rate limit**, run:
```bash
python C:\Users\GG\.kilocode\skills\llm-rate-limit-fallback\integrate.py "Upstream error from Nvidia: ResourceExhausted: Worker local total request limit reached (32/32)"
```
Output will show: `Switch Model -> z.ai/glm-4.5` → click Switch Model in KiloCode UI → select `z.ai/glm-4.5`

---

### Option 2: Auto-Hook via KiloCode Skills Config (Recommended)

Add to `C:\Users\GG\.config\kilo\kilo.jsonc` in the `skills` section:

```json
"skills": {
  "paths": [
    "C:\\Users\\GG\\.kilocode\\skills"
  ],
  "hooks": {
    "session-boot": [
      "C:\\Users\\GG\\.kilocode\\skills\\llm-rate-limit-fallback\\session_boot.py"
    ],
    "post-error": [
      "C:\\Users\\GG\\.kilocode\\skills\\llm-rate-limit-fallback\\integrate.py"
    ]
  }
}
```

**Then restart KiloCode** - hooks will fire automatically.

---

### Option 3: Agent Manager Workflow (For Team Sharing)

Create a workflow in `C:\Users\GG\.kilocode\agent-manager.json`:

```json
{
  "workflows": {
    "llm-rate-limit-check": {
      "steps": [
        {
          "name": "check-quota",
          "command": "python C:\\Users\\GG\\.kilocode\\skills\\llm-rate-limit-fallback\\session_boot.py"
        },
        {
          "name": "monitor-errors",
          "command": "python C:\\Users\\GG\\.kilocode\\skills\\llm-rate-limit-fallback\\integrate.py {error}"
        }
      ]
    }
  }
}
```

---

## What Each Hook Does

| Hook | Script | Trigger | Action |
|------|--------|---------|--------|
| `session-boot` | `session_boot.py` | Session start | Shows quota status, lists fallback models |
| `post-error` | `integrate.py` | LLM error response | Detects rate limit, suggests fallback model |

---

## Integration with GATEWAY-MANAGER (Server-Side)

**Already deployed** - no action needed:
- Backend: `openrouter-nemotron-free` (30 RPM, hard limit 32/worker)
- Auto-detection in `router.py` → backoff 60s → failover to `google-ai-studio`, `groq`, `github-models`
- Task routing includes Nemotron in `general` and `zero_conf_fallback`

---

## Files Created

| File | Purpose |
|------|---------|
| `detector.py` | Core detection logic + fallback suggestion |
| `fallback.yaml` | Model config (priority, free/paid, context window) |
| `integrate.py` | Post-error hook - detects error → suggests switch |
| `session_boot.py` | Session-boot hook - shows quota status |
| `SKILL.md` | Full documentation |

---

## Testing

```bash
# Test detector
python -c "
from C:\Users\GG\.kilocode\skills\llm-rate-limit-fallback.detector import detect_rate_limit_error, suggest_fallback
err = 'Upstream error from Nvidia: ResourceExhausted: Worker local total request limit reached (32/32)'
print('Detected:', detect_rate_limit_error(err))
print('Fallback:', suggest_fallback(err))
"

# Test hooks
python C:\Users\GG\.kilocode\skills\llm-rate-limit-fallback\session_boot.py
python C:\Users\GG\.kilocode\skills\llm-rate-limit-fallback\integrate.py "Upstream error from Nvidia: ResourceExhausted: Worker local total request limit reached (32/32)"
```

---

## Next Level: Full Automation

To make it fully automatic (no manual Switch Model click):

1. **KiloCode API**: Use `switch_model` tool if available
2. **Agent Manager**: Create a session that monitors and auto-switches
3. **GATEWAY-MANAGER**: Already does server-side failover

The server-side (GATEWAY-MANAGER) is the most robust - it handles the failover transparently without any client action needed.