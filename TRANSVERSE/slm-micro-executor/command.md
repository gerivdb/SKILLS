---
name: slm-micro-executor
description: "Execute UNE micro-tache atomique (1 step = 1 tool call)"
version: "1.0.0"
layer: TRANSVERSE
intent_hash: 0xSLM_MICRO_EXECUTOR_CMD_20260731
---

# Command: slm-micro-executor

## Usage

```powershell
# Execution complete (tous steps)
python scripts/execute.py --plan plan.json

# Execution step unique
python scripts/execute.py --plan plan.json --step step-1

# Reprendre depuis etat sauvegarde
python scripts/execute.py --plan plan.json --resume

# Lister steps du plan
python scripts/execute.py --plan plan.json --list-steps

# Reset etat (recommencer)
python scripts/execute.py --plan plan.json --reset
```

## Arguments

| Argument | Requis | Description |
|----------|--------|-------------|
| `--plan` | Oui | Fichier plan JSON (valide par task-graph-validator) |
| `--step` | Non | Executer seulement ce step (ex: step-2) |
| `--resume` | Non | Reprendre depuis etat .slm/state.json |
| `--list-steps` | Non | Afficher liste steps sans executer |
| `--reset` | Non | Supprimer etat .slm/state.json avant exec |
| `--state-dir` | Non | Repertoire etat (defaut: .slm) |

## Etat (.slm/state.json)

```json
{
  "plan_hash": "sha256...",
  "current_step": 2,
  "completed_steps": ["step-1"],
  "step_results": {
    "step-1": {"status": "ok", "output": "...", "duration_ms": 45}
  },
  "created_at": "2026-07-31T23:00:00Z"
}
```

## Tool Mapping

| Tool | Implementation |
|------|----------------|
| read | Path.read_text() |
| write | Path.write_text() |
| edit | String replace in file |
| bash | subprocess.run() |

## Codes de sortie

- `0` : Succes (tous steps ou step demande)
- `1` : Echec step (voir stderr + etat sauvegarde)
- `2` : Plan invalide / etat corrompu

## Integration

- **Pre-execution** : Plan valide par task-graph-validator (obligatoire)
- **Post-execution** : Etat mis a jour dans .slm/state.json
- **Reprise** : --resume continue au step suivant
- **Pattern-router** : Declenche par "executer plan", "micro-step", "step par step"
