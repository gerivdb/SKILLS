---
type: SKILL
version: "1.0.0"
intent_hash: 0xCLASPR_SAFE_DEPLOY_20261102
name: claspr-safe-deploy
role: action
wal_id: WAL-0x243
depends_on: claspr-atomic-deploy
friction: 0.0
entropy: 0.0
---

# Skill - claspr-safe-deploy

## Role

Deployer de maniere securisee vers le projet Google Apps Script distant. Verifie le scriptId cible, la branche locale, et l'historique distant avant tout push. Interdit le --force.

## Declencheur

Un deploiement atomique valide par claspr-atomic-deploy.

## Protocole obligatoire

### Etape 1 - Verifier le remote

```powershell
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" remote -v
# Doit retourner origin -> https://github.com/gerivdb/ENV3.git
```

### Etape 2 - Verifier la branche

```powershell
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" branch --show-current
# Doit retourner main
```

### Etape 3 - Verifier l'historique distant

```powershell
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" log origin/main --oneline -5
# Verifier que le distant n'a pas ete ecrase
```

### Etape 4 - Verifier le scriptId cible

Le fichier .clasp.json doit contenir le scriptId cible :
1fRGLY4S5vwkQlvjuGvTAQdLtEk-IpxUweStb2RNF87kttfm-QOiMr9Gq

### Etape 5 - Executer le deploiement

Sans --force. En cas de conflit (Conflicting files found), ne pas forcer : le remote est deja a jour.

## Interdictions

- Jamais git push --force
- Jamais clasp push --force
- Jamais modification du scriptId sans revision ADR

## Sceau WAL

WAL-0x243-CLASPR-SAFE-DEPLOY (RC = 0, F = 0.0, H = 0.0)

## Voûte de Référence SSoT

[GOUV](https://gemini.google.com/notebook/83e23803-655d-4f3b-9e40-db7e45f8cad4)