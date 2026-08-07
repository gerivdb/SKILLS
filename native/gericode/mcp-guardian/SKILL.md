---
name: mcp-guardian
description: >
  Gestion, découverte et validation des serveurs MCP installés et déclarés.
  Détecte les MCP dans .kilocode/mcp.json, .kilo/mcp.json, et les binaires installés.
  Valide la connectivité, la configuration et les chemins autorisés.
  Utiliser pour toute opération liée aux MCP : installation, diagnostic, audit.
version: "1.0.0"
status: active
intent_hash: 0xMCP_GUARDIAN_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/mcp-guardian/SKILL.md
triggers:
  - "mcp"
  - "codebase manager"
  - "cbm"
  - "mcp installé"
  - "mcp config"
  - "serveur mcp"
  - "diagnostic mcp"
tools:
  - bash
  - read
  - edit
citizen: "PRIMUS"
layer: "L4"
---

# Skill — MCP Guardian

> **Verdict** : **SKILL D'EXÉCUTION** — Gestion, découverte et validation des serveurs MCP.

---

## Objectif

Centraliser la découverte, la validation et la gestion des serveurs MCP
installés et déclarés dans l'écosystème Kilocode/GeriCode.

---

## Scan et découverte

### Sources scannées

| Source | Chemin |
|--------|--------|
| **mcp.json principal** | `C:\DevTools\.kilocode\mcp.json` |
| **mcp.json utilisateur** | `C:\Users\GG\.kilocode\mcp.json` |
| **Binaire CBM** | `C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe` |
| **Index écosystème** | `ecosystem-index.json` → `installed_mcps` |

### Commandes de scan

```powershell
# Scan via index-ecosystem.py
python .kilo/scripts/index-ecosystem.py --scan-all
python .kilo/scripts/index-ecosystem.py --query "codebase-memory-mcp"
python .kilo/scripts/index-ecosystem.py --query "mcp"
```

---

## Validation

### Checklist MCP

| Vérification | Commande |
|--------------|----------|
| Fichier mcp.json existe | `Test-Path C:\DevTools\.kilocode\mcp.json` |
| Serveur déclaré | `python -c "import json; json.load(open('C:\DevTools\.kilocode\mcp.json'))['mcpServers']"` |
| Binaire CBM existe | `Test-Path C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe` |
| Cache CBM présent | `Test-Path C:\DevTools\.cache\codebase-memory-mcp` |
| Processus MCP actif | `Get-Process -Name "codebase-memory-mcp*" -ErrorAction SilentlyContinue` |

### Probe de connectivité

```powershell
# Vérifier que le MCP filesystem répond
$mcp = Get-Content "C:\DevTools\.kilocode\mcp.json" -Raw | ConvertFrom-Json
$filesystem = $mcp.mcpServers.filesystem
Write-Output "[MCP-GUARDIAN] filesystem command: $($filesystem.command)"
Write-Output "[MCP-GUARDIAN] allowed dirs: $($filesystem.allowedDirectories -join ', ')"
```

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `PRIMUS` | Orchestre la découverte et la validation MCP |
| `NEXUS` | Trace les événements dans WAL |
| `ARGUS` | Détecte les MCP manquants ou mal configurés |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1201   C:\DevTools\.kilocode\mcp.json existe et est valide JSON           |
| P-1202   Tous les serveurs déclarés ont une commande/args valide             |
| P-1203   codebase-memory-mcp.exe existe dans C:\DevTools\bin\               |
| P-1204   CBM_CACHE_DIR existe et est accessible                             |
| P-1205   C:\Users\GG\.kilocode\mcp.json existe et est valide JSON           |
| P-1206   Aucun processus MCP fantôme (zombie)                               |
| P-1207   allowedDirectories cohérents entre mcp.json et globalSettings      |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          mcp.json valide et lisible                                       |
| ✓          Tous les serveurs déclarés sont installés                        |
| ✓          Codebase Manager MCP opérationnel                                |
| ✓          Cache CBM accessible                                             |
| ✓          Zéro processus MCP fantôme                                       |
| ✓          allowedDirectories cohérents                                    |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Sauvegarder `mcp.json` avant modification.
2. Restaurer la version précédente en cas d'erreur.
3. Logger dans WAL.
4. Valider par PR review PRIMUS.

---

## Références

- `C:\DevTools\.kilocode\mcp.json`
- `C:\Users\GG\.kilocode\mcp.json`
- `C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe`
- `ecosystem-index.json` → `installed_mcps`
- `unified-design/designs/mcp-integration.yaml`
