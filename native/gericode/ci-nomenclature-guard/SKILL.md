---
name: ci-nomenclature-guard
description: >
  Workflow GitHub Actions pour valider la nomenclature PRD-MOC-ACTPROTOCOL
  sur chaque PR/push. Exécute verify-terms.py et bloque le merge si des termes
  non déclarés dans ONTOLOGY/ONTOLOGY.yaml sont détectés.
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

# Skill — CI Nomenclature Guard

> **Verdict** : **SKILL D’EXÉCUTION** — Workflow GitHub Actions pour bloquer
> la divergence terminologique sur chaque PR/push.

---

## Objectif

Garantir que la nomenclature `PRD-MOC-{CONTEXT}/` est respectée sur chaque PR/push
en exécutant `verify-terms.py` dans CI.

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

### Étape 1 — Créer le workflow

```powershell
New-Item -ItemType Directory -Path ".github/workflows" -Force
Set-Content -Path ".github/workflows/nomenclature-guard.yml" -Value $workflowYaml
```

### Étape 2 — Commit

```powershell
git add .github/workflows/nomenclature-guard.yml
git commit -m "ci: add nomenclature guard workflow"
git push origin main
```

### Étape 3 — Vérifier

- Aller sur GitHub → Actions
- Vérifier que le workflow passe sur main
- Créer une PR avec un terme interdit → vérifier que CI bloque

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `FLUX-D4` | Valide le workflow avant merge |
| `ONTOLOGY-GUARDIAN` | Maintient la liste des termes autorisés |
| `NEXUS` | Trace les résultats CI dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1001   Workflow .github/workflows/nomenclature-guard.yml existe            |
| P-1002   Workflow exécuté sur push main                                     |
| P-1003   Workflow exécuté sur PR vers main                                  |
| P-1004   verify-terms.py passe quand termes conformes                        |
| P-1005   verify-terms.py échoue quand termes non conformes                   |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          Workflow déployé sur le repo                                     |
| ✓          Exécution automatique sur push/PR                                |
| ✓          Blocage si terme interdit détecté                                |
| ✓          Passage si tous les termes sont conformes                        |
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

## Références

- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `ONTOLOGY/ONTOLOGY.yaml`
- `.kilo/scripts/verify-terms.py`
- `.github/workflows/nomenclature-guard.yml`
