---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_CLASP_PROXY_20261102
status: active
extends:
  - bdcp-clapet-guard
  - bdcp-safe-push
---

# Skill: bdcp-clasp-proxy

## Purpose
Forcer le trafic `clasp` et `gas-direct-sync.js` (Node.js `https.request`) a transiter par le proxy CDP local (`localhost:18000`) avec le clapet BDCP ferme, sans jamais ouvrir le clapet ni basculer en mode FREE.

## Context
Contrairement a `git` qui peut utiliser des mecanismes de proxy natifs Windows, `clasp` (wrapper Node.js autour de `@google/clasp`) et `gas-direct-sync.js` (Node.js `https.request` direct) ne respectent pas automatiquement la configuration proxy systeme Windows. Ils necessitent les variables d'environnement `HTTPS_PROXY` / `HTTP_PROXY` explicites.

Sans ces variables, `clasp push` et `gas-direct-sync.js` tentent une connexion directe vers `script.googleapis.com` / `oauth2.googleapis.com`, ce qui est bloque par le clapet ferme (mode BDCP).

## Prerequisites
- Clapet BDCP ferme (verifie via `bdcp-clapet-guard` : fichier `$env:TEMP\ecos_clapet_state` absent)
- Proxy CDP en ecoute sur `localhost:18000` (port du proxy local)
- `.clasprc.json` present a `C:\Users\GG\.clasprc.json` (tokens d'authentification Google)
- Repo GAS cible avec `.clasprc.json` ou scriptId configure

## Workflow

### 1. Verifier que le clapet est ferme
```powershell
# Le fichier $env:TEMP\ecos_clapet_state doit etre ABSENT (clapet ferme = BDCP mode)
Test-Path "$env:TEMP\ecos_clapet_state"
# Si le fichier existe -> clapet ouvert -> invoquer bdcp-clapet-guard close d'abord
```

### 2. Verifier que le proxy CDP ecoute sur 18000
```powershell
Test-NetConnection -ComputerName localhost -Port 18000
# Si TcpTestSucceeded = False -> le proxy CDP n'est pas encore demarre
```

### 3. Configurer les variables d'environnement Node.js
```powershell
# Dans PowerShell (scope de la session courante uniquement)
$env:HTTPS_PROXY = "http://localhost:18000"
$env:HTTP_PROXY  = "http://localhost:18000"
$env:NO_PROXY    = "127.0.0.1,localhost"
```

### 4. Executer clasp push (via le proxy)
```powershell
# Depuis le repo GAS
clasp push
# Node.js utilise automatiquement HTTPS_PROXY pour les requetes https.request
# Le trafic transite par le proxy CDP local, pas par une connexion directe
```

### 5. Executer gas-direct-sync.js (via le proxy)
```powershell
# Depuis D:\DO\WEB\TOOLS\L0-CANON\ENV3
cd D:\DO\WEB\TOOLS\L0-CANON\ENV3
$env:HTTPS_PROXY = "http://localhost:18000"
$env:HTTP_PROXY  = "http://localhost:18000"
$env:NO_PROXY    = "127.0.0.1,localhost"
node gas-direct-sync.js
```

### 6. Nettoyer les variables apres execution (optionnel)
```powershell
# Les variables sont deja scoped a la session PowerShell
# Pour nettoyer explicitement :
Remove-Item Env:\HTTPS_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:\HTTP_PROXY  -ErrorAction SilentlyContinue
Remove-Item Env:\NO_PROXY    -ErrorAction SilentlyContinue
```

## Regles BDCP specifiques

| Regle | Application |
|---|---|
| Clapet ferme | Verifie avant toute operation - fichier `$env:TEMP\ecos_clapet_state` absent |
| Pas d'ouverture de clapet | Jamais appele `POST /clapet/open` ni `clapet.ps1 open` |
| Pas de mode FREE | `GATEWAY_BYPASS` non defini |
| Trafic proxyfie | `HTTPS_PROXY=http://localhost:18000` route via le proxy CDP local |
| Pas de `gh` CLI | Jamais utilise pour les operations Google Apps Script |

## Anti-patterns interdits

| Anti-pattern | Pourquoi bloquant |
|---|---|
| `clasp push` sans `HTTPS_PROXY` | Connexion directe vers google.com bloquee par clapet ferme |
| `clapet.ps1 open` avant `clasp push` | Ouverture du clapet = violation BDCP |
| `$env:GATEWAY_BYPASS = "1"` | Bascule en mode FREE = violation BDCP |
| Connexion directe sans proxy | Echoue car clapet ferme bloque les sockets sortantes directes |

## Exemple complet (PowerShell)

```powershell
# === SCRIPT COMPLET BDCP-CLASP-PROXY ===

# 1. Verifier clapet ferme
$clapetState = Join-Path $env:TEMP "ecos_clapet_state"
if (Test-Path $clapetState) {
    Write-Error "CLAPET OUVERT - fermeture requise avant toute operation"
    & "C:\DevTools\bin\clapet.ps1" close
}

# 2. Verifier proxy CDP
$test = Test-NetConnection -ComputerName localhost -Port 18000 -ErrorAction SilentlyContinue
if (-not $test.TcpTestSucceeded) {
    Write-Error "PROXY CDP NON DISPONIBLE sur localhost:18000"
    Write-Host "Demarrer le proxy CDP avant de continuer"
    exit 1
}

# 3. Configurer proxy Node.js
$env:HTTPS_PROXY = "http://localhost:18000"
$env:HTTP_PROXY  = "http://localhost:18000"
$env:NO_PROXY    = "127.0.0.1,localhost"

# 4. Executer clasp push
Write-Host "[BDCP-CLASP-PROXY] Execution de clasp push via proxy CDP..." -ForegroundColor Cyan
clasp push

# 5. Ou executer gas-direct-sync.js
# Set-Location "D:\DO\WEB\TOOLS\L0-CANON\ENV3"
# node gas-direct-sync.js

# 6. Nettoyage
Remove-Item Env:\HTTPS_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:\HTTP_PROXY  -ErrorAction SilentlyContinue
Remove-Item Env:\NO_PROXY    -ErrorAction SilentlyContinue
```

## Blocages possibles

| Symptome | Cause | Resolution |
|---|---|---|
| `clasp push` : `getaddrinfo ENOTFOUND` | Proxy CDP non demarre sur 18000 | Demarrer le proxy CDP, reessayer |
| `clasp push` : `403 Forbidden` | Token Google expire ou invalide | Re-authentifier : `clasp login` |
| `gas-direct-sync.js` : `Erreur reseau` | Proxy CDP non accessible | Verifier `Test-NetConnection localhost:18000` |
| `clasp push` reussit mais pas via proxy | `HTTPS_PROXY` non defini | Definir les variables avant `clasp push` |

## References
- **Rule** : bdcp-clapet-guard (verification etat clapet)
- **Rule** : bdcp-safe-push (push securise, pas de force)
- **Rule** : bash-cwd-persistence.md (chemins absolus pour toutes operations)
- **Rule** : bdcp-kiva-workflow.md (interdiction mode FREE, gh CLI)
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD (BDCP inviolable)
- **ADR** : ADR-2026-04-16 (BDCP mode permanent)
