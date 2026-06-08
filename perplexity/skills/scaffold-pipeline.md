---
name: scaffold-pipeline
description: "ScaffoldScanner CLI, gap_parser.py, GapMeta, inférence trit_primitive. Use when user mentions 'scaffold', 'gap_parser', 'GapMeta', 'trit_patch', 'batch frontmatter'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-06-08", notes: "Créé — architecture scaffold P10"}
triggers: ["scaffold", "gap_parser", "GapMeta", "trit_patch", "batch frontmatter"]
layer: "L3_CITIZEN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritDecompose
---
# Scaffold Pipeline

## Domaine et périmètre

Pipeline de création automatique de scanners ARGUS depuis les gaps SGR. Couvre : gap_parser.py, GapMeta, inférence trit_primitive, batch patch frontmatter.

## Architecture

```
GAP_REPORT (SGR output)
  → gap_parser.py (parse_gap → GapMeta)
    → scanner_template.py (generate_scanner_yaml)
      → ARGUS/scanners/declared/{scanner_id}.yaml
        → declarative_runner (test score 1.0)
```

## Composants

### gap_parser.py
Parse un GAP_REPORT SGR et extrait les métadonnées :
- `gap_id`, `title`, `severity`, `source`, `trit`, `action`
- Infère le CHECK_TYPE depuis le pattern du gap

### scanner_template.py
Génère un scanner YAML déclaratif depuis un GapMeta :
- `scanner_id` = `{slug}_health`
- `citizen` = source du gap
- `trit` = primitive du gap
- `checks` = 1 check principal inféré

### patch_skill_frontmatter.py
Batch patch `trit_primitive` dans les frontmatters skills :
- 80+ règles d'inférence nom → trit
- `--force` pour remplacer les valeurs existantes
- `--dry-run` pour preview

## Utilisation

```powershell
# Parser un gap
python -c "from gap_parser import parse_gap; gap = parse_gap('GAP_REPORT.json', 'SCR-TEST-001')"

# Générer un scanner
from scanner_template import generate_from_gap_id
out_path, content = generate_from_gap_id('SCR-TEST-001', 'GAP_REPORT.yaml', 'ARGUS/scanners/declared/')

# Batch patch skills
python scripts/patch_skill_frontmatter.py --skills-dir SKILLS/perplexity/skills/ --force
```

## Référence

- gap_parser : `KIVA-CLI/kiva_cli/scaffold/gap_parser.py`
- template : `KIVA-CLI/kiva_cli/scaffold/scanner_template.py`
- patcher : `KIVA-CLI/scripts/patch_skill_frontmatter.py`
- Skills : `L4-TOOLS/SKILLS/skills/scaffold-scanner/SKILL.md`
