---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_PROXY_CHECK_20261102
status: active
extends: bdcp-clapet-guard
---

# Skill: bdcp-proxy-check

## Purpose
Verifier que le proxy CDP (localhost:18000) ecoute et est disponible pour relayer le trafic git/clasp avec le clapet BDCP ferme. Si le proxy n'ecoute pas, aucune operation reseau (git push, git fetch, clasp push, gas-direct-sync.js) ne peut reussir.

## Contexte important

Le clapet BDCP ferme bloque les connexions directes sortantes. Pour qu'une operation reseau fonctionne avec le clapet ferme, le trafic DOIT transiter par un proxy local. Sur ENV2, ce proxy est le **CDP sur `localhost:18000`**.

**Si le proxy CDP n'ecoute pas sur 18000 :**
- `git push` -> ECHEC (connexion refusee)
- `git fetch` -> ECHEC (connexion refusee)
- `clasp push` -> ECHEC (connexion refusee)
- `gas-direct-sync.js` -> ECHEC (connexion refusee)

Ce n'est PAS un echec de BDCP, c'est un echec du proxy CDP qui n'est pas demarre.

## Prerequisites
- Clapet BDCP ferme (bdcp-clapet-guard valide)
- Acces PowerShell sur ENV2

## Workflow

### 1. Verifier que le proxy CDP ecoute sur 18000
```powershell
$proxyTest = Test-NetConnection -ComputerName localhost -Port 18000
if ($proxyTest.TcpTestSucceeded) {
    Write-Host "[BDCP-PROXY-CHECK] PROXY CDP DISPONIBLE sur localhost:18000" -ForegroundColor Green
    Write-Host "Les operations git reseau (push, fetch) peuvent proceder avec le clapet ferme."
} else {
    Write-Error "[BDCP-PROXY-CHECK] PROXY CDP NON DISPONIBLE sur localhost:18000" -ForegroundColor Red
    Write-Host "Aucune operation reseau git ne peut reussir avec le clapet ferme sans proxy."
    Write-Host ""
    Write-Host "ACTIONS POSSIBLES :"
    Write-Host "  1. Demarrer le proxy CDP sur 18000 (voir documentation CDP/ENV2)"
    Write-Host "  2. Ouvrir le clapet (instruction explicite de l utilisateur requise : 'ouvre le clapet')"
    Write-Host "  3. Attendre que le proxy CDP soit demarre par une autre session"
    exit 1
}
```

### 2. Verifier la configuration git pour utiliser le proxy (optionnel mais recommande)
```powershell
# Verifier si git est configure pour utiliser le proxy local
git config --global --get http.proxy
git config --global --get https.proxy
# Si vide, configurer pour que git utilise le proxy CDP :
git config --global http.proxy http://localhost:18000
git config --global https.proxy http://localhost:18000
```

### 3. Verifier que Node.js respectera le proxy (pour clasp / gas-direct-sync.js)
```powershell
# Node.js utilise les variables d environnement HTTPS_PROXY / HTTP_PROXY
# Verifier qu elles sont defini :
Get-ChildItem Env: | Where-Object { $_.Key -in @("HTTPS_PROXY","HTTP_PROXY","NO_PROXY") }
# Si non definies, les definir avant clasp push ou node gas-direct-sync.js :
$env:HTTPS_PROXY = "http://localhost:18000"
$env:HTTP_PROXY  = "http://localhost:18000"
$env:NO_PROXY    = "127.0.0.1,localhost"
```

## Resultats possibles

| Etat du proxy | Clapet | git push | git fetch | clasp push | Action |
|---|---|---|---|---|---|
| Ecoute sur 18000 | Ferme | OK | OK | OK | Proceder |
| N'ecoute pas | Ferme | ECHEC | ECHEC | ECHEC | Demarrer proxy OU ouvrir clapet |
| N'ecoute pas | Ouvert | OK (direct) | OK (direct) | OK (direct) | Clapet ouvert (BDCP viole) |

## Anti-patterns interdits
- [KO] Tenter `git push` ou `clasp push` sans avoir verifie que le proxy CDP ecoute sur 18000
- [KO] Ouvrir le clapet pour "contourner" l'absence de proxy (instruction explicite requise)
- [KO] Pretendre que git push fonctionne avec le clapet ferme sans verifier le proxy

## Bloquants
| Condition | Action |
|---|---|
| Proxy CDP non ecoutant sur 18000 | STOP - demarrer le proxy CDP ou ouvrir le clapet (instruction explicite) |
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |

## Exemple complet
```powershell
# Script de verification complete avant toute operation reseau BDCP

# 1. Verifier clapet ferme
$clapetState = Join-Path $env:TEMP "ecos_clapet_state"
if (Test-Path $clapetState) {
    Write-Error "CLAPET OUVERT - fermeture requise"
    & "C:\DevTools\bin\clapet.ps1" close
    exit 1
}

# 2. Verifier proxy CDP
$proxyTest = Test-NetConnection -ComputerName localhost -Port 18000
if (-not $proxyTest.TcpTestSucceeded) {
    Write-Error "PROXY CDP NON DISPONIBLE sur localhost:18000"
    Write-Host "Impossible d'effectuer des operations reseau git avec le clapet ferme."
    Write-Host "Demarrer le proxy CDP ou ouvrir le clapet (instruction explicite requise)."
    exit 1
}

# 3. Configurer git pour utiliser le proxy
git config --global http.proxy http://localhost:18000
git config --global https.proxy http://localhost:18000

# 4. Configurer Node.js pour clasp / gas-direct-sync.js
$env:HTTPS_PROXY = "http://localhost:18000"
$env:HTTP_PROXY  = "http://localhost:18000"
$env:NO_PROXY    = "127.0.0.1,localhost"

Write-Host "[BDCP-PROXY-CHECK] TOUTES LES VERIFICATIONS SONT OK" -ForegroundColor Green
Write-Host "Operations reseau git autorisees avec le clapet ferme."
```

## References
- **Rule** : bdcp-clapet-guard (verification etat clapet)
- **Rule** : bdcp-safe-push (push securise, requiert proxy CDP)
- **Rule** : bdcp-git-sync (sync remote, requiert proxy CDP)
- **Rule** : bdcp-clasp-proxy (clasp via proxy CDP)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD (BDCP inviolable)
