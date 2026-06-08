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

## Architecture P10 réelle

The actual P10 scaffold architecture uses `gap_parser`, `GapMeta`, and `--gap-id`:

```
GAP_REPORT_{timestamp}.json (SGR output)
  → gap_parser.py --gap-id SGR-TEST-001
    → GapMeta(gap_id, title, severity, source, trit, action, check_type)
      → scanner_template.py --from-gap-id SGR-TEST-001
        → ARGUS/scanners/declared/{slug}_health.yaml
          → declarative_runner --gap-id SGR-TEST-001 (test)
```

### gap_parser.py

```powershell
# Parse a specific gap from GAP_REPORT
python -m kiva_cli.scaffold.gap_parser `
  --report GAP_REPORT_20260609.json `
  --gap-id SGR-TEST-001

# Output: GapMeta dataclass
# GapMeta(
#   gap_id='SGR-TEST-001',
#   title='REPO_UNCOVERED_CANDIDATOR',
#   severity='P1',
#   source='CANDIDATOR',
#   trit='TritObserve',
#   action='Create STRATUM_RELAY.md + ECOS_ROOT.json',
#   check_type='composite'
# )
```

### GapMeta fields

| Field | Type | Description |
|-------|------|-------------|
| `gap_id` | str | Unique gap identifier (e.g., `SGR-TEST-001`) |
| `title` | str | Gap title from SGR |
| `severity` | str | P1 / P2 / P3 |
| `source` | str | Source repo or citizen |
| `trit` | str | Inferred TritRegistry primitive |
| `action` | str | Remediation text |
| `check_type` | str | Inferred CHECK_TYPE for scanner |

### --gap-id workflow

```powershell
# Full workflow: gap → scanner → test
python -m kiva scaffold scanner --gap-id SGR-TEST-001 `
  --from-report GAP_REPORT_20260609.json `
  --output-dir ARGUS/scanners/declared/ `
  --register `
  --test
```

## Référence

- gap_parser : `KIVA-CLI/kiva_cli/scaffold/gap_parser.py`
- template : `KIVA-CLI/kiva_cli/scaffold/scanner_template.py`
- patcher : `KIVA-CLI/scripts/patch_skill_frontmatter.py`
- Skills : `L4-TOOLS/SKILLS/skills/scaffold-scanner/SKILL.md`
- P15 flat reference : `L4-TOOLS/SKILLS/perplexity/skills/scaffold-scanner.md`
