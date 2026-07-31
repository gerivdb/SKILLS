---
type: skill
version: "1.0.0"
date: "2026-07-31"
intent_hash: 0xATOMIC_TASK_PLANNER_20260731
status: active
layer: TRANSVERSE
nexusTags: ["SLM", "PLANNING", "DECOMPOSITION", "ATOMIC"]
scope: ecosystem
guards:
  - agent-budget-check
  - task-graph-validator
---

# atomic-task-planner -- Decomposition de taches en micro-steps SLM

## But
Transforme une description de tache libre en plan JSON valide pour task-graph-validator.
Decompose en micro-steps atomiques (<= 150 tokens, 1 tool/step, chemins absolus, verify inclus).

## Contexte
SLM local (Z600 : 2xe Xeon E5620, 18 GB DDR3, pas de GPU) :
- Contexte effectif : ~2000 tokens fiables
- Vitesse : ~200 tok/s CPU
- Echec si : prompts > 200 tokens, multi-etapes, conditionnels imbriques

Ce skill s utilise AVANT slm-micro-executor. Sortie validee par task-graph-validator.

## Templates de decomposition (patterns/)

| Pattern | Usage | Template |
|---------|-------|----------|
| **A** File creation | Creer nouveau fichier | pattern-a.yaml |
| **B** Batch patch | Modifier plusieurs fichiers | pattern-b.yaml |
| **C** Gap resolution | Resoudre un gap SGR | pattern-c.yaml |
| **D** CLI command | Executer commande CLI | pattern-d.yaml |

## Format d entree

```yaml
task: "Creer validateur pour atoms.md"
context: "Repo ECOS-CLI, besoin validation frontmatter"
constraints:
  - max_tokens: 150
  - single_tool: true
  - absolute_paths: true
  - verify_included: true
```

## Format de sortie (plan JSON pour task-graph-validator)

```json
{
  "steps": [
    {
      "id": "step-1",
      "tool": "read",
      "input": {"path": "D:/abs/path/to/file.py"},
      "output": "content",
      "verify": "Test-Path D:/abs/path/to/file.py",
      "tokens_est": 80
    }
  ],
  "deps": []
}
```

## CLI

```powershell
# Decomposition interactive
python scripts/plan.py --task "Creer validateur atoms.md" --context "ECOS-CLI repo"

# Depuis fichier spec
python scripts/plan.py --spec spec.yaml --output plan.json

# Validation immediate
python scripts/plan.py --task "..." | python -m task_graph_validator --plan -
```

## Integration

- **Pre-execution** : Appele avant slm-micro-executor
- **Validation** : Sortie pipee vers task-graph-validator
- **Pattern-router** : Declenche par "decomposer", "planifier", "micro-steps"
