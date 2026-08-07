---
name: atomic-task-planner
description: "Decompose une tache en micro-steps SLM atomiques"
version: "1.0.0"
layer: TRANSVERSE
intent_hash: 0xATOMIC_TASK_PLANNER_CMD_20260731
---

# Command: atomic-task-planner

## Usage

```powershell
# Decomposition depuis ligne de commande
python scripts/plan.py --task "Creer validateur pour atoms.md" --context "Repo ECOS-CLI"

# Depuis fichier spec YAML
python scripts/plan.py --spec spec.yaml --output plan.json

# Lister templates disponibles
python scripts/plan.py --list-templates
```

## Arguments

| Argument | Requis | Description |
|----------|--------|-------------|
| `--task` | Non* | Description de la tache (requis si pas --spec) |
| `--context` | Non | Contexte additionnel (repo, contraintes, etc.) |
| `--spec` | Non* | Fichier YAML de specification complete |
| `--output` | Non | Fichier sortie plan JSON (defaut: stdout) |
| `--template` | Non | Template a utiliser (A/B/C/D, defaut: auto) |
| `--list-templates` | Non | Affiche templates disponibles |

* Au moins --task ou --spec requis.

## Templates

| ID | Nom | Usage |
|----|-----|-------|
| A | file_creation | Creer un fichier (read -> write -> verify) |
| B | batch_patch | Modifier plusieurs fichiers (read -> edit x N -> verify) |
| C | gap_resolution | Resoudre gap SGR (read gap -> analyze -> implement -> test -> verify) |
| D | cli_command | Executer commande CLI (bash -> verify) |

## Exemples

```powershell
# Auto-detection template
python scripts/plan.py --task "Creer script de validation atoms.md" --context "D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI"

# Template explicite
python scripts/plan.py --task "Patch frontmatter 50 fichiers" --template B --output plan.json

# Spec complete
python scripts/plan.py --spec my_task.yaml --output plan.json
```

## Format spec YAML

```yaml
task: "Description courte"
context: "Contexte detaille"
template: "B"  # optionnel, auto si absent
constraints:
  max_tokens: 150
  single_tool: true
  absolute_paths: true
  verify_included: true
steps_hint: 3  # nombre etapes estime
```

## Sortie

Plan JSON valide pour task-graph-validator (stdout ou --output fichier)
