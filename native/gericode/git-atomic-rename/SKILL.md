---
name: git-atomic-rename
description: >
  Renommage atomique de fichiers/dossiers git avec backup et vérification post-migration.
  Remplace batch les anciens termes par les nouveaux, trace les changements dans WAL,
  et commit/push atomiquement. Utiliser pour les migrations de nomenclature à grande échelle.
version: "1.0.0"
status: active
intent_hash: 0xGIT_ATOMIC_RENAME_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/git-atomic-rename/SKILL.md
triggers:
  - "renommage batch"
  - "migration nomenclature"
  - "PRD-MOC-N243"
  - "atomic rename"
tools:
  - bash
  - git
citizen: "PRIMUS"
layer: "L4"
---

# Skill — Git Atomic Rename

> **Verdict** : **SKILL D’EXÉCUTION** — Renommage atomique avec backup et vérification,
> pour migrations de nomenclature à grande échelle.

---

## Objectif

Effectuer un renommage batch de fichiers/dossiers en respectant :
- la création d’un backup avant migration
- le remplacement des références dans le contenu
- la vérification post-migration
- le commit/push atomique

---

## Principes

| Principe | Règle d’application |
|----------|---------------------|
| **Backup d’abord** | Sauvegarder tous les fichiers avant modification |
| **Atomicité** | Un commit = une migration complète |
| **Vérification systématique** | Post-migration : 0 occurrence des anciens termes |
| **Traçabilité** | Logger dans WAL chaque étape |

---

## Processus

### Étape 1 — Audit

```powershell
# Lister les fichiers à renommer
$files = Get-ChildItem -Recurse -File | Where-Object { $_.Name -match "OLD_TERM" }

# Vérifier l’ontologie
python ONTOLOGY/validate_term_registry.py --check NEW_TERM
```

### Étape 2 — Backup

```powershell
$backupDir = ".rename-backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
foreach ($f in $files) {
  Copy-Item $f.FullName "$backupDir\$($f.Name)" -Force
}
```

### Étape 3 — Renommage

```powershell
# Renommage fichiers
Get-ChildItem -Recurse -File | Where-Object { $_.Name -match "OLD_TERM" } | ForEach-Object {
  $newName = $_.Name -replace "OLD_TERM", "NEW_TERM"
  Rename-Item $_.FullName -NewName $newName
}

# Renommage dossiers
# (utiliser robocopy ou PowerShell selon la complexité)
```

### Étape 4 — Remplacement contenu

```powershell
$files = Get-ChildItem -Recurse -File -Include *.md,*.yaml,*.yml,*.json
foreach ($f in $files) {
  $content = Get-Content $f.FullName -Raw
  $new = $content -replace "OLD_TERM", "NEW_TERM"
  if ($new -ne $content) {
    Set-Content -Path $f.FullName -Value $new -NoNewline
  }
}
```

### Étape 5 — Vérification

```powershell
# Vérifier qu’aucun ancien terme ne subsiste
$oldTerms = @("OLD_TERM", "ANCIEN_TERME")
foreach ($term in $oldTerms) {
  $matches = Get-ChildItem -Recurse -File | Select-String -Pattern $term
  if ($matches) {
    Write-Error "Old term '$term' still present"
    exit 1
  }
}
```

### Étape 6 — Commit atomique

```powershell
git add -A
git commit -m "refactor: rename OLD_TERM to NEW_TERM per nomenclature design"
git push origin main
```

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `PRIMUS` | Orchestre le renommage |
| `NEXUS` | Trace les étapes dans WAL |
| `TOPOS` | Valide les chemins et strates |
| `MOX` | Valide la structure AEP post-migration |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1001   Backup créé avant migration                                        |
| P-1002   Tous les fichiers renommés                                          |
| P-1003   Toutes les références mises à jour                                 |
| P-1004   0 occurrence des anciens termes post-migration                     |
| P-1005   Commit atomique réussi                                              |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          Backup créé et complet                                           |
| ✓          Tous les fichiers/dossiers renommés                              |
| ✓          Toutes les références mises à jour                               |
| ✓          0 ancien terme restant                                           |
| ✓          Commit + push atomiques                                          |
+-----------------------------------------------------------------------------+
```

---

## Rollback

```powershell
# Restaurer depuis backup
Copy-Item "$backupDir\*" . -Recurse -Force
Remove-Item $backupDir -Recurse -Force
```

---

## Références

- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `.kilo/scripts/setup-unified-design-junction.ps1`
- `.kilocode/rules/git-atomic-commit.md`
