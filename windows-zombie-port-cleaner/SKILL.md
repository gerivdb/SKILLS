---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_WZPC_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/windows-zombie-port-cleaner/SKILL.md
---

# Skill - windows-zombie-port-cleaner

## Objectif

Detecter et liberer les ports TCP verrouilles par des processus enfants orphelins (python.exe, node.exe, uvicorn.exe) apres un crash de serveur ASGI/WSGI ou un rechargement d'IDE, sur l'hote Windows ENV2 (HP Z600).

## Declencheur

- Erreur d'ecoute sur un port (ex: 9000, 3001, 8080) indiquee comme deja utilise alors qu'aucun serveur n'est actif.
- Presence de processus python.exe ou node.exe orphelins qui conservent un descripteur de socket ouvert.
- Echec de redemarrage du gateway-manager ou de tout serveur uvicorn suite a un echec de bind.

## Entrees

- Numero de port cible a verifier (ex: 9000, 3001, 8080, 9223).
- Chemin vers l'executable du serveur incrimine (optionnel, pour filtrer les processus a arreter).

## Sorties

- Liste des processus detenteurs du port avec leur PID et leur ligne de commande.
- Arret propre des processus orphelins detenteurs du port.
- Liberation du descripteur de socket et verification que le port est libre (netstat / Get-NetTCPConnection).
- Rapport d'action avec les PIDs arretes et le statut final du port.

## Regles Operationnelles

### 1. Interdiction de tuer un processus actif sans verification
Avant tout arret, verifier que le processus detenteur du port n'est pas un serveur legitimement en cours d'execution. Utiliser Get-NetTCPConnection pour associer le port au PID.

### 2. Preflight d'identification du detenteur de port
Executer systematiquement :
```powershell
Get-NetTCPConnection -LocalPort <PORT> | Select-Object LocalPort, OwningProcess, State
Get-Process -Id <PID> | Select-Object Id, ProcessName, Path, CommandLine
```

### 3. Arret propre des processus orphelins
Si le processus est identifie comme orphelin (pas de serveur actif sur ce port), l'arreter :
```powershell
Stop-Process -Id <PID> -Force
```
Puis attendre 2 secondes et verifier que le port est libre.

### 4. Verification post-liberation
Confirmer que le port n'est plus occupe :
```powershell
Get-NetTCPConnection -LocalPort <PORT> -ErrorAction SilentlyContinue
# Aucun resultat = port libre
```

### 5. Escalade en cas d'echec
Si l'arret echoue (Acces refuse, processus systeme), signaler le PID et le chemin de l'executable pour intervention manuelle HITL.
