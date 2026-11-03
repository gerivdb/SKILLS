---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_EIPG_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/ecos-ipc-fastpath-guardian/SKILL.md
---

# Skill - ecos-ipc-fastpath-guardian

## Objectif

Surveiller et valider la presence du socket IPC (/tmp/fluence.ipc) avant de router le trafic CLI en ENV3, selon la regle globale ECOS. Empeche toute tentative de communication inter-processus lorsque le socket est absent ou injoignable.

## Declencheur

- Tentative de routage CLI ECOS-CLI vers FLUENCE sans verification prealable du socket IPC.
- Erreur de connexion au socket /tmp/fluence.ipc (fichier absent, permission refusee, connexion rejetee).
- Demande d'envoi de trafic inter-depots sans preflight de presence du canal IPC.

## Entrees

- Chemin vers le socket IPC (par defaut /tmp/fluence.ipc).
- Identifiant du client CLI demandeur (ex: ECOS-CLI, KIVA-CLI).
- Type de trafic a router (registry, health, sync, etc.).

## Sorties

- Rapport de presence/absence du socket avec son etat (actif, inactif, absent).
- Autorisation formelle de routage si le socket est accessible.
- Blocage avec message d'erreur si le socket est absent ou injoignable.
- Code retour 0 si autorise, code retour 2 si bloque.

## Regles Operationnelles

### 1. Verification prealable obligatoire du socket
Avant tout routage de trafic CLI, verifier l'existence et l'accessibilite du socket IPC :
```powershell
Test-Path -LiteralPath "/tmp/fluence.ipc"
```

### 2. Test de connexion active au socket
Si le fichier existe, tenter une connexion pour confirmer que le socket est actif et non un fichier orphelin :
```powershell
# Test de reachability du socket (via client ECOS ou sondage direct)
```

### 3. Blocage en cas d'absence
Si le socket est absent ou injoignable, bloquer le routage et retourner une erreur explicite indiquant le chemin du socket manquant.

### 4. Timeout de verification
La verification du socket doit respecter un timeout maximum de 2 secondes pour ne pas bloquer le client indefiniement.

### 5. Escalade
Si le socket est absent de maniere repetee, signaler pour intervention sur le service FLUENCE ou ECOS-CLI.
