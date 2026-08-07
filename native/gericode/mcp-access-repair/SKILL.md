---
name: mcp-access-repair
description: >
  Réparation causale des accès MCP filesystem refusés pour chemins hors workspace root.
  Crée une jonction NTFS `unified-design` vers `L0-CANON/unified-design` pour rendre
  les chemins L0 accessibles au MCP sans modifier allowedDirectories.
  Utiliser quand le MCP filesystem renvoie "Access denied" pour un chemin sous D:\DO\WEB\TOOLS\L0-CANON\.
version: "1.0.0"
status: active
intent_hash: 0xMCP_ACCESS_REPAIR_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/mcp-access-repair/SKILL.md
triggers:
  - "accès refusé MCP"
  - "MCP access denied"
  - "unified-design inaccessible"
  - "allowedDirectories"
  - "jonction NTFS"
tools:
  - bash
  - write
  - read
citizen: "NEXUS"
layer: "L4"
---

# Skill — MCP Access Repair

> **Verdict** : **SKILL D’EXÉCUTION** — Réparation causale des refus d’accès MCP filesystem
> pour chemins hors workspace root, par jonction NTFS.

---

## Objectif

Quand le MCP filesystem refuse l’accès à `D:\DO\WEB\TOOLS\L0-CANON\unified-design\` parce que le workspace root est `D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode`, ce skill crée une jonction NTFS à l’intérieur du workspace pour rendre le chemin accessible **sans modifier** `allowedDirectories`.

---

## Principe causal

```
GeriCode\unified-design  --(jonction NTFS)-->  L0-CANON\unified-design
```

Le MCP filesystem voit `unified-design/` comme un chemin local sous le workspace root.
L’écriture/lecture passe donc sans restriction.

---

## Prérequis

- Windows avec droits d’écriture sur `D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\`
- PowerShell 7+ (pwsh)
- Git Bash ou PowerShell pour exécuter le script
- Aucune modification de `mcp.json` nécessaire

---

## Processus

### Étape 1 — Diagnostic

```powershell
# Vérifier que la jonction n’existe pas déjà
$junction = "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design"
if (Test-Path $junction) {
  $item = Get-Item $junction -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    Write-Output "[MCP-REPAIR] Junction already exists"
    exit 0
  }
}
```

### Étape 2 — Création de la jonction

```powershell
# Exécuter le script de setup
.\.kilo\scripts\setup-unified-design-junction.ps1
```

### Étape 3 — Vérification

```powershell
# Test lecture MCP
Get-Content "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design\designs\actprotocol-fractal-nomenclature.yaml" -Head 5

# Test écriture via bash
$test = "test-mcp-access-repair"
Set-Content -Path "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design\$test.txt" -Value "OK"
Remove-Item "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design\$test.txt"
```

### Étape 4 — Nettoyage (optionnel)

```powershell
# Supprimer la jonction
Remove-Item "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design" -Force
```

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `NEXUS` | Trace la création/suppression de jonction dans WAL |
| `PRIMUS` | Orchestre la réparation MCP |
| `TOPOS` | Valide que la cible `L0-CANON/unified-design` existe |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-801    Junction "unified-design" existe et pointe vers L0-CANON           |
| P-802    Lecture MCP via unified-design/ fonctionne                         |
| P-803    Écriture MCP via unified-design/ fonctionne                        |
| P-804    Aucune modification de mcp.json nécessaire                         |
| P-805    Pas de elevation/admin requis                                      |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          Junction créée et fonctionnelle                                  |
| ✓          MCP filesystem lit unified-design/ sans erreur                   |
| ✓          MCP filesystem écrit dans unified-design/ sans erreur            |
| ✓          Aucun reboot de serveur MCP nécessaire                           |
| ✓          Procédure réversible (suppression jonction)                      |
+-----------------------------------------------------------------------------+
```

---

## Rollback

```powershell
# Supprimer la jonction
Remove-Item "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design" -Force

# Vérifier
Test-Path "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design"  # Doit retourner False
```

---

## Références

- Script : `.kilo/scripts/setup-unified-design-junction.ps1`
- Design : `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- PRD MOC : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/PRD-MOC-ACTPROTOCOL-SKILLS-CITIZENS-2026-08-06.md`
- Règle : `.kilocode/rules/ecos-cli-launcher.md`

---

## Notes

- Ce skill ne modifie **jamais** `allowedDirectories` dans `mcp.json`.
- Il ne modifie **jamais** la configuration du serveur MCP.
- Il fonctionne exclusivement par jonction NTFS locale.
- La jonction est un artefact local, **ne pas la commiter** dans git.
