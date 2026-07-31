---
type: skill
version: "1.0.0"
date: "2026-07-31"
intent_hash: 0xSLM_MICRO_EXECUTOR_20260731
status: active
layer: TRANSVERSE
nexusTags: ["SLM", "EXECUTION", "MICRO_STEP", "ATOMIC"]
scope: ecosystem
guards:
  - agent-budget-check
  - task-graph-validator
  - atomic-task-planner
---

# slm-micro-executor -- Execution atomique de micro-steps SLM

## But
Execute UNE SEULE micro-tache atomique (1 step = 1 tool call) depuis un plan valide.
Maintient l etat minimal entre steps (.slm/state.json).

## Contexte
SLM local (Z600 : 2xe Xeon E5620, 18 GB DDR3, pas de GPU) :
- Contexte effectif : ~2000 tokens fiables
- Vitesse : ~200 tok/s CPU
- Echec si : prompts > 200 tokens, multi-etapes, conditionnels imbriques

Ce skill s utilise APRES atomic-task-planner + task-graph-validator.
Execute step par step, verifie, passe au suivant.

## Format d entree (plan JSON valide)

```json
{
  "steps": [
    {"id": "step-1", "tool": "read", "input": {"path": "..."}, "verify": "...", "tokens_est": 80}
  ],
  "deps": []
}
```

## Etat persistant (.slm/state.json)

```json
{
  "plan_id": "plan-abc123",
  "current_step": 1,
  "completed_steps": ["step-1"],
  "step_results": {
    "step-1": {"status": "ok", "output": "...", "duration_ms": 45}
  },
  "created_at": "2026-07-31T23:00:00Z"
}
```

## CLI

```powershell
# Execution complete (tous steps)
python scripts/execute.py --plan plan.json

# Execution step unique
python scripts/execute.py --plan plan.json --step step-1

# Reprendre depuis etat
python scripts/execute.py --plan plan.json --resume

# Lister steps
python scripts/execute.py --plan plan.json --list-steps

# Reset etat
python scripts/execute.py --plan plan.json --reset
```

## Integration

- **Pre-execution** : Plan valide par task-graph-validator (obligatoire)
- **Post-execution** : Resultats stockes dans .slm/state.json
- **Pattern-router** : Declenche par "executer plan", "micro-step", "step par step"
