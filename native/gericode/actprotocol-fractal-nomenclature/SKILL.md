---
name: actprotocol-fractal-nomenclature
description: >
  Execution du design unified-design/designs/actprotocol-fractal-nomenclature.yaml.
  Applique la nomenclature verrouillee PRD-MOC-{CONTEXT}/ pour eliminer la confusion
  ontologique N243 (repo/EPIC/dossier). Utiliser pour creer, valider et migrer
  les structures PRD-MOC selon les regles AEP.
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

# Skill - ACTPROTOCOL Fractal Nomenclature

> **Verdict** : **SKILL D'EXECUTION** - Applique la nomenclature verrouillee
> `PRD-MOC-{CONTEXT}/` pour eliminer la confusion ontologique `N243`.

---

## Objectif

Executer le design `unified-design/designs/actprotocol-fractal-nomenclature.yaml` pour :
1. Creer de nouveaux PRD-MOC selon la nomenclature canonique
2. Valider les structures existantes
3. Migrer les anciens termes vers les nouveaux (ex: `PRD-MOC-N243` -> `PRD-MOC-ACTPROTOCOL`)

---

## Principes

| Principe | Regle d'application |
|----------|---------------------|
| **Nomenclature verrouillee** | `PRD-MOC-{CONTEXT}/` uniquement |
| **Pas de nom repo dans MOC** | `N243`, `VERSES`, etc. interdits comme nom de dossier MOC |
| **Auto-similarite** | Chaque repo applique le meme motif AEP |
| **Ontologie d'abord** | Tous les termes doivent etre dans `ONTOLOGY/ONTOLOGY.yaml` |

---

## Processus

### Creation d'un nouveau PRD-MOC

1. **Creer la structure**
   ```powershell
   New-Item -ItemType Directory -Path "PRD-MOC-{CONTEXT}/fractal" -Force
   New-Item -ItemType Directory -Path "PRD-MOC-{CONTEXT}/components" -Force
   ```

2. **Creer README.md**
   ```markdown
   # PRD-MOC-{CONTEXT}
   ```

3. **Creer les fractals**
   ```
   PRD-MOC-{CONTEXT}/fractal/PRD-MOC-{CONTEXT}-{SLUG}.md
   ```

4. **Ajouter a l'index**
   ```powershell
   # Mettre a jour PRD-000-index.md
   ```

### Validation d'un PRD-MOC existant

1. **Verifier la structure**
   ```powershell
   Test-Path "PRD-MOC-{CONTEXT}/README.md"
   Test-Path "PRD-MOC-{CONTEXT}/fractal/"
   Test-Path "PRD-MOC-{CONTEXT}/components/"
   ```

2. **Verifier les noms**
   ```powershell
   Get-ChildItem "PRD-MOC-{CONTEXT}/fractal" -File | Where-Object { $_.Name -notmatch "^PRD-MOC-{CONTEXT}-" }
   ```

3. **Verifier les termes**
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

4. **Verification**
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

## Roles

| Role | Responsabilite |
|------|----------------|
| `PRIMUS` | Orchestre la creation/maintenance des PRD-MOC/ |
| `MOX` | Valide la structure AEP |
| `ARGUS` | Detecte les termes litigieux |
| `TOPOS` | Valide les chemins et strates |
| `NEXUS` | Trace les modifications dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1101   PRD-MOC-{CONTEXT}/ existe                                           |
| P-1102   fractal/ contient uniquement PRD-MOC-{CONTEXT}-*.md                 |
| P-1103   components/ contient uniquement templates/composants               |
| P-1104   README.md present et a jour                                         |
| P-1105   Aucun terme interdit dans les noms/chemins/contenu                 |
| P-1106   verify-terms.py passe                                               |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          PRD-MOC-{CONTEXT}/ present et valide                             |
| [OK]          Structure AEP conforme (fractal/, components/, README.md)        |
| [OK]          Nomenclature coherente (PRD-MOC-{CONTEXT}-{SLUG}.md)            |
| [OK]          0 terme interdit dans tout le sous-arbre                         |
| [OK]          verify-terms.py passe                                            |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer `PRD-MOC-{CONTEXT}/`.
2. Restaurer depuis le tag git.
3. Logger dans WAL.

---

## References

- Design : `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- Ontologie : `ONTOLOGY/ONTOLOGY.yaml`
- Script : `.kilo/scripts/setup-unified-design-junction.ps1`
- PRD MOC : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/PRD-MOC-ACTPROTOCOL-MATHEMES-NOMENCLATURE-2026-08-05.md`
