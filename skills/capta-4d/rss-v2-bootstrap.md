# RSS-v2 Bootstrap — Procédure Complète

## Description

Procédure complète de bootstrap RSS-v2 pour un nouveau repo gerivdb — structure de dossiers, fichiers obligatoires, frontmatter, et vérification. Ce skill capitalise l'expérience de la session de conformité 2026-06-17.

## Quand l'utiliser

- Création d'un nouveau repo dans l'écosystème gerivdb
- Bootstrap RSS-v2 from scratch
- Vérification de conformité post-bootstrap
- Migration d'un repo existant vers RSS-v2

## Structure obligatoire

```
<repo>/
├── README.md
├── LICENSE
├── .gitignore
├── VERSION
├── STATUS.md
├── CHANGELOG.md
├── CITIZENS.yaml
├── STRATUM_RELAY.md
├── ADR/
│   ├── ADR-000-index.md
│   └── ADR-<NNN>-<slug>.md
├── EPICS/
│   ├── EPIC-000-index.md
│   └── EPIC-<NNN>-<slug>.md
├── PRD/
│   ├── PRD-000-index.md
│   └── PRD-<NNN>-<slug>.md
├── INTENTS/
│   ├── INTENT-000-index.md
│   └── INTENT-<NNN>-<slug>.md
├── src/
│   └── <package>/
│       ├── core/
│       └── cli/
├── tests/
├── config/
├── docs/
├── scripts/
├── pipelines/
│   └── ci.kiva.yaml
└── .github/
    └── workflows/
        ├── ci.yml
        └── rss-lint.yml
```

## Frontmatter obligatoire par type

### ADR
```yaml
---
type: ADR
status: accepted
date: "YYYY-MM-DD"
intent_hash: 0x<HEX>
id: ADR-<NNN>
title: "<Titre>"
repo: gerivdb/<REPO>
author: gerivdb
created: "YYYY-MM-DD"
---
```

### EPIC
```yaml
---
type: EPIC
intent_hash: 0x<HEX>
status: active
priority: P1
owner: gerivdb
repo: gerivdb/<REPO>
title: "<Titre>"
---
```

### PRD
```yaml
---
type: PRD
version: "0.1.0"
date: "YYYY-MM-DD"
status: draft
intent_hash: 0x<HEX>
id: PRD-<NNN>
title: "<Titre>"
repo: gerivdb/<REPO>
author: gerivdb
created: "YYYY-MM-DD"
epic: EPIC-<NNN>
---
```

### INTENT
```yaml
---
type: INTENT
status: active
date: "YYYY-MM-DD"
intent_hash: 0x<HEX>
id: INTENT-<NNN>
title: "<Titre>"
repo: gerivdb/<REPO>
author: gerivdb
created: "YYYY-MM-DD"
---
```

## Procédure de bootstrap

### Étape 1 — Structure de base
```bash
mkdir -p ADR EPICS PRD INTENTS src tests config docs scripts pipelines .github/workflows
```

### Étape 2 — Fichiers obligatoires
Créer README.md, LICENSE, .gitignore, VERSION, STATUS.md, CHANGELOG.md, CITIZENS.yaml, STRATUM_RELAY.md

### Étape 3 — Index
Créer ADR/ADR-000-index.md, EPICS/EPIC-000-index.md, PRD/PRD-000-index.md, INTENTS/INTENT-000-index.md avec frontmatter + table

### Étape 4 — Artefacts
Créer au minimum 1 ADR, 1 EPIC, 1 PRD, 1 INTENT avec frontmatter conforme

### Étape 5 — CI
Créer pipelines/ci.kiva.yaml + .github/workflows/ci.yml + .github/workflows/rss-lint.yml

### Étape 6 — Vérification
```bash
# Local
kiva cicd run .

# Remote (via KIVA-CLI)
python <kiva_root>/rss_lint.py --repo . --all-checks --check-artifacts
```

## Checklist de conformité

- [ ] 3 dossiers ADR/PRD/EPICS présents
- [ ] Index dans chaque dossier (frontmatter + table)
- [ ] Frontmatter conforme sur tous les fichiers
- [ ] Pattern de nommage `ADR-NNN-slug.md` (kebab-case)
- [ ] `rss_lint.py --all-checks --check-artifacts` passe
- [ ] `kiva cicd run .` passe (lint + tests)
- [ ] CITIZENS.yaml présent et conforme
- [ ] STRATUM_RELAY.md avec strate et intent_hash

## Références

- Standards: `gerivdb/REPO-STANDARDS/`
- Linter: `gerivdb/KIVA-CLI/rss_lint.py`
- CI: `gerivdb/KIVA-CLI/pipelines/ci.kiva.yaml`
- Exemple conforme: `gerivdb/CAPTA-4D/`
