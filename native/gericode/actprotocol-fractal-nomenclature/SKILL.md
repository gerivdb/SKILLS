---
name: actprotocol-fractal-nomenclature
description: >
  Exécution du design unified-design/designs/actprotocol-fractal-nomenclature.yaml.
  Applique la nomenclature verrouillée PRD-MOC-{CONTEXT}/ pour éliminer la confusion
  ontologique N243 (repo/EPIC/dossier). Utiliser pour créer, valider et migrer
  les structures PRD-MOC selon les règles AEP.
version: "1.0.0"
status: active
intent_hash: 0xACTPROTOCOL_FRACTAL_NOMENCLATURE_SKILL_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/actprotocol-fractal-nomenclature/SKILL.md
triggers:
  - "PRD-MOC-N243"
  - "PRD-MOC-MATHEMES"
  - "nomenclature PRD-MOC"
  - "fractal nomenclature"
  - "ACT-PROTOCOL"
tools:
  - bash
  - read
  - write
  - edit
  - git
citizen: "PRIMUS"
layer: "L4"
---

# Skill — ACTPROTOCOL Fractal Nomenclature

> **Verdict** : **SKILL D’EXÉCUTION** — Applique la nomenclature verrouillée
> `PRD-MOC-{CONTEXT}/` pour éliminer la confusion ontologique `N243`.

---

## Objectif

Exécuter le design `unified-design/designs/actprotocol-fractal-nomenclature.yaml` pour :
1. Créer de nouveaux PRD-MOC selon la nomenclature canonique
2. Valider les structures existantes
3. Migrer les anciens termes vers les nouveaux (ex: `PRD-MOC-N243` → `PRD-MOC-ACTPROTOCOL`)

---

## Principes

| Principe | Règle d’application |
|----------|---------------------|
| **Nomenclature verrouillée** | `PRD-MOC-{CONTEXT}/` uniquement |
| **Pas de nom repo dans MOC** | `N243`, `VERSES`, etc. interdits comme nom de dossier MOC |
| **Auto-similarité** | Chaque repo applique le même motif AEP |
| **Ontologie d’abord** | Tous les termes doivent être dans `ONTOLOGY/ONTOLOGY.yaml` |

---

## Processus

### Création d’un nouveau PRD-MOC

1. **Créer la structure**
   ```powershell
   New-Item -ItemType Directory -Path "PRD-MOC-{CONTEXT}/fractal" -Force
   New-Item -ItemType Directory -Path "PRD-MOC-{CONTEXT}/components" -Force
   ```

2. **Créer README.md**
   ```markdown
   # PRD-MOC-{CONTEXT}
   ```

3. **Créer les fractals**
   ```
   PRD-MOC-{CONTEXT}/fractal/PRD-MOC-{CONTEXT}-{SLUG}.md
   ```

4. **Ajouter à l’index**
   ```powershell
   # Mettre à jour PRD-000-index.md
   ```

### Validation d’un PRD-MOC existant

1. **Vérifier la structure**
   ```powershell
   Test-Path "PRD-MOC-{CONTEXT}/README.md"
   Test-Path "PRD-MOC-{CONTEXT}/fractal/"
   Test-Path "PRD-MOC-{CONTEXT}/components/"
   ```

2. **Vérifier les noms**
   ```powershell
   Get-ChildItem "PRD-MOC-{CONTEXT}/fractal" -File | Where-Object { $_.Name -notmatch "^PRD-MOC-{CONTEXT}-" }
   ```

3. **Vérifier les termes**
   ```powershell
   python .kilo/scripts/verify-terms.py
   ```

### Migration de nomenclature

1. **Audit**
   ```powershell
   grep -r "PRD-MOC-N243" act-protocol/PRD/
   ```

2. **Backup**
   ```powershell
   git tag -a "backup-PRD-MOC-before-nomenclature-fix-$(Get-Date -Format yyyyMMdd)"
   ```

3. **Renommage** (utiliser `git-atomic-rename` skill)

4. **Vérification**
   ```powershell
   # 0 occurrence des anciens termes
   ```

5. **Commit**
   ```powershell
   git add -A
   git commit -m "refactor(PRD-MOC): rename per nomenclature design"
   git push origin main
   ```

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `PRIMUS` | Orchestre la création/maintenance des PRD-MOC/ |
| `MOX` | Valide la structure AEP |
| `ARGUS` | Détecte les termes litigieux |
| `TOPOS` | Valide les chemins et strates |
| `NEXUS` | Trace les modifications dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1101   PRD-MOC-{CONTEXT}/ existe                                           |
| P-1102   fractal/ contient uniquement PRD-MOC-{CONTEXT}-*.md                 |
| P-1103   components/ contient uniquement templates/composants               |
| P-1104   README.md présent et à jour                                         |
| P-1105   Aucun terme interdit dans les noms/chemins/contenu                 |
| P-1106   verify-terms.py passe                                               |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          PRD-MOC-{CONTEXT}/ présent et valide                             |
| ✓          Structure AEP conforme (fractal/, components/, README.md)        |
| ✓          Nomenclature cohérente (PRD-MOC-{CONTEXT}-{SLUG}.md)            |
| ✓          0 terme interdit dans tout le sous-arbre                         |
| ✓          verify-terms.py passe                                            |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer `PRD-MOC-{CONTEXT}/`.
2. Restaurer depuis le tag git.
3. Logger dans WAL.

---

## Références

- Design : `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- Ontologie : `ONTOLOGY/ONTOLOGY.yaml`
- Script : `.kilo/scripts/setup-unified-design-junction.ps1`
- PRD MOC : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/PRD-MOC-ACTPROTOCOL-MATHEMES-NOMENCLATURE-2026-08-05.md`
