---
type: SKILL
version: "1.0.0"
intent_hash: 0xCLASPR_ATOMIC_DEPLOY_20261102
name: claspr-atomic-deploy
role: action
wal_id: WAL-0x243
depends_on: claspr-auth-guard
friction: 0.0
entropy: 0.0
---

# Skill - claspr-atomic-deploy

## Role

Deployer atomiquement les fichiers .gs vers le projet Google Apps Script distant. Maximum 3 fichiers par deploiement, message de commit conventionnel, sceau WAL emis apres succes.

## Declencheur

Une ou plusieurs modifications de fichiers .gs pretes a etre deplyees vers le projet Google Apps Script cible.

## Protocole obligatoire

### Etape 1 - Verifier le nombre de fichiers

Maximum 3 fichiers .gs par deploiement. Si plus de 3 fichiers, creer plusieurs deploiements sequentiels.

### Etape 2 - Choisir la methode de deploiement

| Methode | Condition | Commande |
|---------|-----------|----------|
| clasp push | Cache clasp sain, remote accessible | clasp push |
| gas-direct-sync.js | Cache clasp corrompu, API REST directe | node gas-direct-sync.js |

### Etape 3 - Executer le deploiement

```powershell
# Depuis D:\DO\WEB\TOOLS\L0-CANON\ENV3
clasp push
# ou
node gas-direct-sync.js
```

### Etape 4 - Sceller dans la WAL

Emettre un sceau WAL avec l'identifiant du scriptId cible, les fichiers deplyes, et le code de retour.

## Contraintes

- Maximum 3 fichiers .gs par deploiement
- Message de commit conventionnel : feat(env3): <description>
- Jamais --force sur un push clasp
- Clapet BDCP doit etre fermee (verifie par claspr-clapet-guard)

## Sceau WAL

WAL-0x243-CLASPR-ATOMIC-DEPLOY (RC = 0, F = 0.0, H = 0.0)

## Voûte de Référence SSoT

[GOUV](https://gemini.google.com/notebook/83e23803-655d-4f3b-9e40-db7e45f8cad4)