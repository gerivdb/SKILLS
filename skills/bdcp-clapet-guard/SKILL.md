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

## Contexte important - clapet ferme != reseau disponible

Le mode BDCP (Behind CDP) est le mode de protection par defaut sur ENV2. Le clapet ferme interdit toute socket sortante directe. **Cependant, le clapet ferme seul ne garantit pas que le reseau fonctionne** : pour qu'une operation git (push, fetch) ou clasp fonctionne, le trafic doit transiter par un proxy local. Sur ENV2, ce proxy est le **CDP sur `localhost:18000`**.

**Le clapet ferme + proxy CDP non demarre = aucune operation reseau ne fonctionne.**

Ce skill garantit que le clapet est verifie ferme. Pour les operations reseau, invoquer egalement `bdcp-proxy-check` pour verifier que le proxy CDP ecoute sur 18000.

## Prerequisites
- Repo git initialise avec remote configure
- Aucun appel `POST /clapet/open` n'a ete emis dans la session

## Workflow

### 1. Verifier l'etat du clapet
```powershell
# Le fichier $env:TEMP\ecos_clapet_state doit etre ABSENT (clapet ferme = BDCP mode)
Test-Path "$env:TEMP\ecos_clapet_state"
# Si le fichier existe -> clapet ouvert -> BDCP viole, STOP
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

### 4. Pour les operations reseau (push, fetch, clasp) - invoquer bdcp-proxy-check
Avant toute operation git reseau (push, fetch) ou clasp, invoquer `bdcp-proxy-check` pour verifier que le proxy CDP ecoute sur 18000. Sans proxy, l'eoperation echouera avec le clapet ferme.

## Anti-patterns interdits
- [KO] Appeler `POST /clapet/open` avant un push
- [KO] Basculer en mode FREE pour "debloquer" un push
- [KO] Utiliser `gh` CLI (interdit par BDCP)
- [KO] Ouvrir une connexion directe vers github.com sans proxy
- [KO] Push/fetch sans verifier que le proxy CDP ecoute sur 18000 (invoquer bdcp-proxy-check d'abord)

## Bloquants
| Condition | Action |
|---|---|
| Clapet ouvert (ou tentative d'ouverture) | STOP - refuser l'operation |
| Connexion directe vers github.com detectee | STOP - tuer le processus |
| Variable BDCP_MODE=FREE | STOP - remettre en BDCP |
| Proxy CDP non ecoutant sur 18000 (pour ops reseau) | STOP - invoquer bdcp-proxy-check |

## References
- **Rule** : bdcp-kiva-workflow.md (interdiction gh, GitHub Actions, web interface)
- **Rule** : bash-cwd-persistence.md (chemins absolus obligatoires)
- **Rule** : bdcp-proxy-check (verification proxy CDP avant ops reseau)
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD (BDCP inviolable)
- **ADR** : ADR-2026-04-16 (BDCP mode inviolable, IntentHash 0xBDCP_INVIOLABLE_20260416)
