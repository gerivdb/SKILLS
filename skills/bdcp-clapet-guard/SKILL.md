---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_CLAPET_GUARD_20261102
status: active
extends: bdcp-mode-verification
---

# Skill: bdcp-clapet-guard

## Purpose
Verifier que le clapet BDCP est ferme avant toute operation git (add, commit, push, pull, fetch, merge). Empeche toute connexion sortante directe qui contournerait le proxy CDP.

## Context
Le mode BDCP (Behind CDP) est le mode de protection par defaut sur ENV2. Le clapet ferme interdit toute socket sortante directe. Le trafic git transite obligatoirement par le proxy CDP local (localhost:18000). Ce skill garantit qu'aucune operation git n'est executee tant que le clapet n'est pas verifie ferme.

## Prerequisites
- Repo git initialise avec remote configure
- Acces au proxy CDP sur localhost:18000
- Aucun appel `POST /clapet/open` n'a ete emis dans la session

## Workflow

### 1. Verifier l'etat du clapet
```powershell
# Le clapet doit etre ferme (retour 200 ou refus de connexion)
# Toute tentative de connexion directe vers github.com doit echouer sans proxy
Test-NetConnection -ComputerName localhost -Port 18000
```

### 2. Verifier qu'aucun processus ne contourne le clapet
```powershell
# Aucun processus ne doit avoir de connexion directe vers github.com
Get-NetTCPConnection -RemotePort 443 | Where-Object { $_.RemoteAddress -like "*github*" }
# Si resultat non vide -> STOP, stopper le processus
```

### 3. Confirmer le mode BDCP actif
```powershell
# Le mode BDCP est actif par defaut. Verifier qu'aucune variable d'environnement
# ne force le mode FREE
Get-ChildItem Env: | Where-Object { $_.Key -like "*BDCP*" -or $_.Key -like "*CLAPET*" }
# Si BDCP_MODE=FREE ou CLAPET=OPEN -> STOP, remettre en BDCP
```

### 4. Autoriser l'operation git
Si toutes les verifications passent, l'operation git peut etre lancee. Le trafic sera automatiquement proxyfie par le CDP.

## Anti-patterns interdits
- [KO] Appeler `POST /clapet/open` avant un push
- [KO] Basculer en mode FREE pour "debloquer" un push
- [KO] Utiliser `gh` CLI (interdit par BDCP)
- [KO] Ouvrir une connexion directe vers github.com sans proxy

## Bloquants
| Condition | Action |
|---|---|
| Clapet ouvert (ou tentative d'ouverture) | STOP - refuser l'operation |
| Connexion directe vers github.com detectee | STOP - tuer le processus |
| Variable BDCP_MODE=FREE | STOP - remettre en BDCP |

## References
- **Rule** : bdcp-kiva-workflow.md (interdiction gh, GitHub Actions, web interface)
- **Rule** : bash-cwd-persistence.md (chemins absolus obligatoires)
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD (BDCP inviolable)
- **ADR** : ADR-2026-04-16 (BDCP mode inviolable, IntentHash 0xBDCP_INVIOLABLE_20260416)
