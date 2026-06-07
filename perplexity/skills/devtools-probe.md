---
name: devtools-probe
description: "Verification des outils installes dans C:\DevTools\bin avant toute installation ou recherche de binaire sur ENV2. Ne jamais installer ailleurs que C:\DevTools\bin\<tool>. Utiliser avant toute installation, tout nouveau pipeline CI, tout step qui depend d'un outil externe."
version: "1.0.0"
triggers:
  - "installation outil"
  - "zig version"
  - "python --version"
  - "node --version"
  - "Get-Command"
  - "nouveau pipeline CI"
  - "step CI depend d'un outil"
  - "ajout au PATH"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "DEVTOOLS", "ENV2", "PRE_CONDITION"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Creation — decision ADR devtools-centralization-20260607"}
prerequisites:
  - "Acces shell PowerShell (ENV2) ou bash (ENV3)"
  - "Acces C:\DevTools (via script hors MCP si hors workspace)"
slotWeight: 1
adr_ref: "adr-llm-intent-gate-20260607"
---

# DEVTOOLS-PROBE — Sonde C:\DevTools\bin avant toute action

## Objectif

Verifier ce qui existe deja dans `C:\DevTools\bin\` **avant** d'installer, creer ou referencer un outil sur ENV2. Ne **jamais** installer ailleurs que `C:\DevTools\bin\<tool>\`.

Cree suite a la tentative d'installation de Zig dans `C:\zig` hors de l'organisation centralisee existante.

## Regle absolue

```
C:\DevTools\bin\<tool>\   = SEUL emplacement autorise pour les binaires tiers
C:\<tool>\                = INTERDIS (dispersion)
C:\Program Files\<tool>\  = sauf installeurs systeme natifs uniquement
```

## Protocole

### Phase 1 — Sonde DevTools

```powershell
$devtoolsBin = "C:\DevTools\bin"
if (Test-Path $devtoolsBin) {
    $tools = Get-ChildItem $devtoolsBin -Directory | Select-Object -ExpandProperty Name
    Write-Output "[DEVTOOLS_PROBE] Presents : $($tools -join ', ')"
} else {
    Write-Output "[DEVTOOLS_PROBE] WARN: C:\DevTools\bin n'existe pas"
}
```

### Phase 2 — Sonde PATH pour l'outil cible

```powershell
param([string]$tool)
$found = Get-Command $tool -ErrorAction SilentlyContinue
if ($found) {
    Write-Output "[DEVTOOLS_PROBE] $tool PRESENT : $($found.Source)"
} else {
    Write-Output "[DEVTOOLS_PROBE] $tool ABSENT"
}
```

### Phase 3 — Decision

| Resultat | Action |
|---|---|
| Outil present dans `C:\DevTools\bin\` | Utiliser le chemin existant. NE PAS reinstaller. |
| Outil present hors DevTools (ex: `C:\zig`) | Signaler dispersion. NE PAS creer de doublon. Utiliser l'existant en attendant migration. |
| Outil absent | Installer **uniquement** dans `C:\DevTools\bin\<tool>\` |

## Cas d'usage — Session MC-RNN

Commande executee : `$found = Get-Command zig -ErrorAction SilentlyContinue`
Resultat attendu : `C:\zig\zig.exe`
Decision : utiliser l'existant, signaler la dispersion, NE PAS installer dans `C:\DevTools\bin\zig`.

## Sonde rapide mono-ligne

```powershell
Get-ChildItem "C:\DevTools\bin" -Directory | Select Name
```

A executer avant toute commande `install`, `download`, `setup`, `winget install`, `choco install`.

## Dependances

- **ADR** : `adr-devtools-centralization-20260607.md` (decision)
- **ADR gate** : `adr-llm-intent-gate-20260607.md` (principe verifier-avant-d-agir)
