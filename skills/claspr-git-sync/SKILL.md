---
type: SKILL
version: "1.0.0"
intent_hash: 0xCLASPR_GIT_SYNC_20261102
name: claspr-git-sync
role: action
wal_id: WAL-0x243
depends_on: claspr-safe-deploy
friction: 0.0
entropy: 0.0
---

# Skill - claspr-git-sync

## Role

Synchroniser le depot local ENV3 avec le remote distant. Verifie la divergence, fait un rebase si necessaire, et confirme l'alignement local/distant.

## Declencheur

Apres un deploiement securise valide par claspr-safe-deploy, ou avant un nouveau deploiement pour s'assurer de l'alignement.

## Protocole obligatoire

### Etape 1 - Verifier le statut du working tree

```powershell
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" status --porcelain
# Doit retourner vide (working tree propre)
```

### Etape 2 - Verifier l'alignement local/distant

```powershell
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" log --oneline main..origin/main
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" log --oneline origin/main..main
# Les deux doivent etre vides (identiques)
```

### Etape 3 - Rebase si necessaire (sans --force)

Si le distant a avance, faire un rebase local sur origin/main sans ecraser l'historique distant.

### Etape 4 - Confirmer l'alignement

```powershell
git -C "D:\DO\WEB\TOOLS\L0-CANON\ENV3" log --oneline main origin/main
# Les deux branches doivent pointer vers le meme commit
```

## Interdictions

- Jamais git push --force
- Jamais git reset --hard sur une branche partagee
- Jamais suppression de l'historique distant

## Sceau WAL

WAL-0x243-CLASPR-GIT-SYNC (RC = 0, F = 0.0, H = 0.0)

## Voûte de Référence SSoT

[GOUV](https://gemini.google.com/notebook/83e23803-655d-4f3b-9e40-db7e45f8cad4)