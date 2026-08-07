---
name: git-atomic-rename
description: >
  Renommage atomique de fichiers/dossiers git avec backup et verification post-migration.
  Remplace batch les anciens termes par les nouveaux, trace les changements dans WAL,
  et commit/push atomiquement. Utiliser pour les migrations de nomenclature a grande echelle.
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

# Skill - Git Atomic Rename

> **Verdict** : **SKILL D'EXECUTION** - Renommage atomique avec backup et verification,
> pour migrations de nomenclature a grande echelle.

---

## Objectif

Effectuer un renommage batch de fichiers/dossiers en respectant :
- la creation d'un backup avant migration
- le remplacement des references dans le contenu
- la verification post-migration
- le commit/push atomique

---

## Principes

| Principe | Regle d'application |
|----------|---------------------|
| **Backup d'abord** | Sauvegarder tous les fichiers avant modification |
| **Atomicite** | Un commit = une migration complete |
| **Verification systematique** | Post-migration : 0 occurrence des anciens termes |
| **Tracabilite** | Logger dans WAL chaque etape |

---

## Processus

### Etape 1 - Audit

```powershell
# Lister les fichiers a renommer
$files = Get-ChildItem -Recurse -File | Where-Object { $_.Name -match "OLD_TERM" }

# Verifier l'ontologie
python ONTOLOGY/validate_term_registry.py --check NEW_TERM
```

### Etape 2 - Backup

```powershell
$backupDir = ".rename-backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
foreach ($f in $files) {
  Copy-Item $f.FullName "$backupDir\$($f.Name)" -Force
}
```

### Etape 3 - Renommage

```powershell
# Renommage fichiers
Get-ChildItem -Recurse -File | Where-Object { $_.Name -match "OLD_TERM" } | ForEach-Object {
  $newName = $_.Name -replace "OLD_TERM", "NEW_TERM"
  Rename-Item $_.FullName -NewName $newName
}

# Renommage dossiers
# (utiliser robocopy ou PowerShell selon la complexite)
```

### Etape 4 - Remplacement contenu

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

### Etape 5 - Verification

```powershell
# Verifier qu'aucun ancien terme ne subsiste
$oldTerms = @("OLD_TERM", "ANCIEN_TERME")
foreach ($term in $oldTerms) {
  $matches = Get-ChildItem -Recurse -File | Select-String -Pattern $term
  if ($matches) {
    Write-Error "Old term '$term' still present"
    exit 1
  }
}
```

### Etape 6 - Commit atomique

```powershell
git add -A
git commit -m "refactor: rename OLD_TERM to NEW_TERM per nomenclature design"
git push origin main
```

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `PRIMUS` | Orchestre le renommage |
| `NEXUS` | Trace les etapes dans WAL |
| `TOPOS` | Valide les chemins et strates |
| `MOX` | Valide la structure AEP post-migration |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1001   Backup cree avant migration                                        |
| P-1002   Tous les fichiers renommes                                          |
| P-1003   Toutes les references mises a jour                                 |
| P-1004   0 occurrence des anciens termes post-migration                     |
| P-1005   Commit atomique reussi                                              |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          Backup cree et complet                                           |
| [OK]          Tous les fichiers/dossiers renommes                              |
| [OK]          Toutes les references mises a jour                               |
| [OK]          0 ancien terme restant                                           |
| [OK]          Commit + push atomiques                                          |
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

## References

- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `.kilo/scripts/setup-unified-design-junction.ps1`
- `.kilocode/rules/git-atomic-commit.md`
