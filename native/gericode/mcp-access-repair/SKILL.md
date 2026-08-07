---
name: mcp-access-repair
description: >
  Reparation causale des acces MCP filesystem refuses pour chemins hors workspace root.
  Cree une jonction NTFS `unified-design` vers `L0-CANON/unified-design` pour rendre
  les chemins L0 accessibles au MCP sans modifier allowedDirectories.
  Utiliser quand le MCP filesystem renvoie "Access denied" pour un chemin sous D:\DO\WEB\TOOLS\L0-CANON\.
version: "1.0.0"
status: active
intent_hash: 0xMCP_ACCESS_REPAIR_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/mcp-access-repair/SKILL.md
triggers:
  - "acces refuse MCP"
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

# Skill - MCP Access Repair

> **Verdict** : **SKILL D'EXECUTION** - Reparation causale des refus d'acces MCP filesystem
> pour chemins hors workspace root, par jonction NTFS.

---

## Objectif

Quand le MCP filesystem refuse l'acces a `D:\DO\WEB\TOOLS\L0-CANON\unified-design\` parce que le workspace root est `D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode`, ce skill cree une jonction NTFS a l'interieur du workspace pour rendre le chemin accessible **sans modifier** `allowedDirectories`.

---

## Principe causal

```
GeriCode\unified-design  --(jonction NTFS)-->  L0-CANON\unified-design
```

Le MCP filesystem voit `unified-design/` comme un chemin local sous le workspace root.
L'ecriture/lecture passe donc sans restriction.

---

## Prerequis

- Windows avec droits d'ecriture sur `D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\`
- PowerShell 7+ (pwsh)
- Git Bash ou PowerShell pour executer le script
- Aucune modification de `mcp.json` necessaire

---

## Processus

### Etape 1 - Diagnostic

```powershell
# Verifier que la jonction n'existe pas deja
$junction = "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design"
if (Test-Path $junction) {
  $item = Get-Item $junction -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    Write-Output "[MCP-REPAIR] Junction already exists"
    exit 0
  }
}
```

### Etape 2 - Creation de la jonction

```powershell
# Executer le script de setup
.\.kilo\scripts\setup-unified-design-junction.ps1
```

### Etape 3 - Verification

```powershell
# Test lecture MCP
Get-Content "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design\designs\actprotocol-fractal-nomenclature.yaml" -Head 5

# Test ecriture via bash
$test = "test-mcp-access-repair"
Set-Content -Path "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design\$test.txt" -Value "OK"
Remove-Item "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design\$test.txt"
```

### Etape 4 - Nettoyage (optionnel)

```powershell
# Supprimer la jonction
Remove-Item "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design" -Force
```

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `NEXUS` | Trace la creation/suppression de jonction dans WAL |
| `PRIMUS` | Orchestre la reparation MCP |
| `TOPOS` | Valide que la cible `L0-CANON/unified-design` existe |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-801    Junction "unified-design" existe et pointe vers L0-CANON           |
| P-802    Lecture MCP via unified-design/ fonctionne                         |
| P-803    Ecriture MCP via unified-design/ fonctionne                        |
| P-804    Aucune modification de mcp.json necessaire                         |
| P-805    Pas de elevation/admin requis                                      |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          Junction creee et fonctionnelle                                  |
| [OK]          MCP filesystem lit unified-design/ sans erreur                   |
| [OK]          MCP filesystem ecrit dans unified-design/ sans erreur            |
| [OK]          Aucun reboot de serveur MCP necessaire                           |
| [OK]          Procedure reversible (suppression jonction)                      |
+-----------------------------------------------------------------------------+
```

---

## Rollback

```powershell
# Supprimer la jonction
Remove-Item "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design" -Force

# Verifier
Test-Path "D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\unified-design"  # Doit retourner False
```

---

## References

- Script : `.kilo/scripts/setup-unified-design-junction.ps1`
- Design : `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- PRD MOC : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/PRD-MOC-ACTPROTOCOL-SKILLS-CITIZENS-2026-08-06.md`
- Regle : `.kilocode/rules/ecos-cli-launcher.md`

---

## Notes

- Ce skill ne modifie **jamais** `allowedDirectories` dans `mcp.json`.
- Il ne modifie **jamais** la configuration du serveur MCP.
- Il fonctionne exclusivement par jonction NTFS locale.
- La jonction est un artefact local, **ne pas la commiter** dans git.
