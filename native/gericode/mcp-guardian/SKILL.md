---
name: mcp-guardian
description: >
  Gestion, decouverte et validation des serveurs MCP installes et declares.
  Detecte les MCP dans .kilocode/mcp.json, .kilo/mcp.json, et les binaires installes.
  Valide la connectivite, la configuration et les chemins autorises.
  Utiliser pour toute operation liee aux MCP : installation, diagnostic, audit.
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
  - "mcp installe"
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

# Skill - MCP Guardian

> **Verdict** : **SKILL D'EXECUTION** - Gestion, decouverte et validation des serveurs MCP.

---

## Objectif

Centraliser la decouverte, la validation et la gestion des serveurs MCP
installes et declares dans l'ecosysteme Kilocode/GeriCode.

---

## Scan et decouverte

### Sources scannees

| Source | Chemin |
|--------|--------|
| **mcp.json principal** | `C:\DevTools\.kilocode\mcp.json` |
| **mcp.json utilisateur** | `C:\Users\GG\.kilocode\mcp.json` |
| **Binaire CBM** | `C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe` |
| **Index ecosysteme** | `ecosystem-index.json` -> `installed_mcps` |

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

| Verification | Commande |
|--------------|----------|
| Fichier mcp.json existe | `Test-Path C:\DevTools\.kilocode\mcp.json` |
| Serveur declare | `python -c "import json; json.load(open('C:\DevTools\.kilocode\mcp.json'))['mcpServers']"` |
| Binaire CBM existe | `Test-Path C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe` |
| Cache CBM present | `Test-Path C:\DevTools\.cache\codebase-memory-mcp` |
| Processus MCP actif | `Get-Process -Name "codebase-memory-mcp*" -ErrorAction SilentlyContinue` |

### Probe de connectivite

```powershell
# Verifier que le MCP filesystem repond
$mcp = Get-Content "C:\DevTools\.kilocode\mcp.json" -Raw | ConvertFrom-Json
$filesystem = $mcp.mcpServers.filesystem
Write-Output "[MCP-GUARDIAN] filesystem command: $($filesystem.command)"
Write-Output "[MCP-GUARDIAN] allowed dirs: $($filesystem.allowedDirectories -join ', ')"
```

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `PRIMUS` | Orchestre la decouverte et la validation MCP |
| `NEXUS` | Trace les evenements dans WAL |
| `ARGUS` | Detecte les MCP manquants ou mal configures |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1201   C:\DevTools\.kilocode\mcp.json existe et est valide JSON           |
| P-1202   Tous les serveurs declares ont une commande/args valide             |
| P-1203   codebase-memory-mcp.exe existe dans C:\DevTools\bin\               |
| P-1204   CBM_CACHE_DIR existe et est accessible                             |
| P-1205   C:\Users\GG\.kilocode\mcp.json existe et est valide JSON           |
| P-1206   Aucun processus MCP fantome (zombie)                               |
| P-1207   allowedDirectories coherents entre mcp.json et globalSettings      |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          mcp.json valide et lisible                                       |
| [OK]          Tous les serveurs declares sont installes                        |
| [OK]          Codebase Manager MCP operationnel                                |
| [OK]          Cache CBM accessible                                             |
| [OK]          Zero processus MCP fantome                                       |
| [OK]          allowedDirectories coherents                                    |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Sauvegarder `mcp.json` avant modification.
2. Restaurer la version precedente en cas d'erreur.
3. Logger dans WAL.
4. Valider par PR review PRIMUS.

---

## References

- `C:\DevTools\.kilocode\mcp.json`
- `C:\Users\GG\.kilocode\mcp.json`
- `C:\DevTools\bin\codebase-memory-mcp\codebase-memory-mcp.exe`
- `ecosystem-index.json` -> `installed_mcps`
- `unified-design/designs/mcp-integration.yaml`
