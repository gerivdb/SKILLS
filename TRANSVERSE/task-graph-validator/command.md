---
name: task-graph-validator
description: "Valide un plan de tâches (task graph) contre les contraintes SLM"
version: "1.0.0"
layer: TRANSVERSE
intent_hash: 0xTASK_GRAPH_VALIDATOR_CMD_20260731
---

# Command: task-graph-validator

## Usage

```powershell
# Validation complete
python scripts/validate.py --plan plan.json

# Validation specifique (regles comma-separated)
python scripts/validate.py --plan plan.json --rules max_tokens,single_tool,no_nesting

# Format JSON pour CI/CD
python scripts/validate.py --plan plan.json --format json

# Help
python scripts/validate.py --help
```

## Arguments

| Argument | Requis | Description |
|----------|--------|-------------|
| `--plan` | Oui | Chemin vers le fichier plan JSON |
| `--rules` | Non | Liste de regles a verifier (defaut: toutes) |
| `--format` | Non | Format sortie: `text` (defaut) ou `json` |

## Regles disponibles

- `max_tokens` : tokens_est <= 150 par step
- `single_tool` : 1 seul outil par step
- `no_nesting` : Pas de conditionnels imbriques
- `absolute_paths` : Chemins absolus obligatoires
- `verify_included` : Champ verify present

## Exemples

```powershell
# Validation standard
python scripts/validate.py --plan D:\path\to\plan.json

# Validation CI (JSON output)
python scripts/validate.py --plan plan.json --format json 2>errors.json
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) { Write-Error "Validation failed: $(Get-Content errors.json)" }
```

## Sortie JSON (--format json)

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "rules_checked": ["max_tokens", "single_tool", "no_nesting", "absolute_paths", "verify_included"],
  "steps_count": 5
}
```

## Codes de sortie

- `0` : Valide
- `1` : Invalide (voir stderr)
- `2` : Erreur fichier/format
