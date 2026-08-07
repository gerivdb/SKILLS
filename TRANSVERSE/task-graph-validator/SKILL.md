---
type: skill
version: "1.0.0"
date: "2026-07-31"
intent_hash: 0xTASK_GRAPH_VALIDATOR_20260731
status: active
layer: TRANSVERSE
nexusTags: ["SLM", "VALIDATION", "TASK_GRAPH", "ATOMIC"]
scope: ecosystem
guards:
  - agent-budget-check
---

# task-graph-validator -- Validation de graphes de taches pour SLM

## But
Valide qu un plan de taches (task graph) respecte les contraintes SLM (Small Language Model) :
- **Token budget** : <= 150 tokens par step
- **Single tool** : 1 seul outil (read/write/edit/bash) par step
- **No nesting** : Pas de conditionnels imbriques (if/else/loop > 1 niveau)
- **Absolute paths** : Chemins absolus explicites, pas de chemins relatifs
- **Verify included** : Chaque step inclut une action de verification

## Contexte
SLM local (Z600 : 2xe Xeon E5620, 18 GB DDR3, pas de GPU) :
- Contexte effectif : ~2000 tokens fiables
- Vitesse : ~200 tok/s CPU
- Echec si : prompts > 200 tokens, multi-etapes, conditionnels imbriques

Ce skill s applique a **tout plan de taches** avant execution par slm-micro-executor.

## Format d entree (plan JSON)

```json
{
  "steps": [
    {
      "id": "step-1",
      "tool": "read",
      "input": {"path": "/absolute/path/to/file.py"},
      "output": "content",
      "verify": "Test-Path /absolute/path/to/file.py",
      "tokens_est": 80
    },
    {
      "id": "step-2",
      "tool": "edit",
      "input": {"path": "/absolute/path/to/file.py", "old": "foo", "new": "bar"},
      "output": "patched",
      "verify": "Select-String 'bar' /absolute/path/to/file.py",
      "tokens_est": 120
    }
  ],
  "deps": [{"from": "step-1", "to": "step-2"}]
}
```

## Regles de validation (rules/)

| Rule | Fichier | Verification |
|------|---------|--------------|
| MaxTokens | max_tokens.py | tokens_est <= 150 par step |
| SingleTool | single_tool.py | 1 seul champ tool par step |
| NoNesting | no_nesting.py | Pas de if/else/loop imbriques > 1 niveau |
| AbsolutePaths | absolute_paths.py | Tous chemins input.path sont absolus |
| VerifyIncluded | verify_included.py | Chaque step a un champ verify non-vide |

## CLI

```powershell
# Validation complete
python scripts/validate.py --plan plan.json

# Validation specifique
python scripts/validate.py --plan plan.json --rules max_tokens,single_tool

# Output JSON pour CI
python scripts/validate.py --plan plan.json --format json
```

## Codes de sortie

| Code | Signification |
|------|---------------|
| 0 | Plan valide (toutes regles OK) |
| 1 | Echec validation (details sur stderr) |
| 2 | Erreur fichier/format (plan.json invalide) |

## Integration

- **Pre-execution** : Appele par slm-micro-executor avant chaque plan
- **CI/CD** : Integre dans KIVA-CI stage `validate`
- **Pattern-router** : Declenche par mots-cles "valider plan", "task graph", "plan json"
