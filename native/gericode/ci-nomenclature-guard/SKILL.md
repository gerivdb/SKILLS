---
name: ci-nomenclature-guard
description: >
  Workflow GitHub Actions pour valider la nomenclature PRD-MOC-ACTPROTOCOL
  sur chaque PR/push. Execute verify-terms.py et bloque le merge si des termes
  non declares dans ONTOLOGY/ONTOLOGY.yaml sont detectes.
  Utiliser comme garde CI obligatoire pour tous les repos avec PRD-MOC.
version: "1.0.0"
status: active
intent_hash: 0xCI_NOMENCLATURE_GUARD_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ci-nomenclature-guard/SKILL.md
triggers:
  - "CI nomenclature guard"
  - "GitHub Actions nomenclature"
  - "verify-terms CI"
  - "workflow PRD-MOC"
tools:
  - bash
  - read
  - grep
citizen: "FLUX-D4"
layer: "L4"
---

# Skill - CI Nomenclature Guard

> **Verdict** : **SKILL D'EXECUTION** - Workflow GitHub Actions pour bloquer
> la divergence terminologique sur chaque PR/push.

---

## Objectif

Garantir que la nomenclature `PRD-MOC-{CONTEXT}/` est respectee sur chaque PR/push
en executant `verify-terms.py` dans CI.

---

## Workflow GitHub Actions

```yaml
name: Nomenclature Guard
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  verify-terms:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Verify ontology terms
        run: python .kilo/scripts/verify-terms.py
```

---

## Processus

### Etape 1 - Creer le workflow

```powershell
New-Item -ItemType Directory -Path ".github/workflows" -Force
Set-Content -Path ".github/workflows/nomenclature-guard.yml" -Value $workflowYaml
```

### Etape 2 - Commit

```powershell
git add .github/workflows/nomenclature-guard.yml
git commit -m "ci: add nomenclature guard workflow"
git push origin main
```

### Etape 3 - Verifier

- Aller sur GitHub -> Actions
- Verifier que le workflow passe sur main
- Creer une PR avec un terme interdit -> verifier que CI bloque

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `FLUX-D4` | Valide le workflow avant merge |
| `ONTOLOGY-GUARDIAN` | Maintient la liste des termes autorises |
| `NEXUS` | Trace les resultats CI dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1001   Workflow .github/workflows/nomenclature-guard.yml existe            |
| P-1002   Workflow execute sur push main                                     |
| P-1003   Workflow execute sur PR vers main                                  |
| P-1004   verify-terms.py passe quand termes conformes                        |
| P-1005   verify-terms.py echoue quand termes non conformes                   |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          Workflow deploye sur le repo                                     |
| [OK]          Execution automatique sur push/PR                                |
| [OK]          Blocage si terme interdit detecte                                |
| [OK]          Passage si tous les termes sont conformes                        |
+-----------------------------------------------------------------------------+
```

---

## Rollback

```powershell
# Supprimer le workflow
Remove-Item ".github/workflows/nomenclature-guard.yml" -Force
git add -A
git commit -m "revert: remove nomenclature guard workflow"
git push origin main
```

---

## References

- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
- `.kilo/scripts/verify-terms.py`
- `.github/workflows/nomenclature-guard.yml`
