---
type: SKILL
version: "1.0.0"
intent_hash: 0xCLASPR_AUTH_GUARD_20261102
name: claspr-auth-guard
role: guard
wal_id: WAL-0x243
depends_on: claspr-clapet-guard
friction: 0.0
entropy: 0.0
---

# Skill - claspr-auth-guard

## Role

Verifier que le fichier d'authentification C:\Users\GG\.clasprc.json est present et contient des tokens OAuth valides (refresh_token et access_token) avant toute operation clasp.

## Declencheur

Toute operation clasp (push, pull, status, login) necessitant une authentification Google Apps Script.

## Protocole obligatoire

### Etape 1 - Verifier la presence du fichier

```powershell
Test-Path -LiteralPath "C:\Users\GG\.clasprc.json"
# Doit retourner True
```

### Etape 2 - Verifier la structure JSON

Le fichier doit contenir une cle tokens avec au moins une entree default possedant refresh_token et access_token.

```powershell
$rc = Get-Content -LiteralPath "C:\Users\GG\.clasprc.json" -Raw | ConvertFrom-Json
$tokens = $rc.tokens
if (-not $tokens -or -not $tokens.default -or -not $tokens.default.refresh_token) {
    throw "[CLASPR-AUTH-GUARD] refresh_token manquant dans .clasprc.json"
}
if (-not $tokens.default.access_token) {
    throw "[CLASPR-AUTH-GUARD] access_token manquant dans .clasprc.json"
}
```

### Etape 3 - Verifier la session clasp (si proxy disponible)

Si le proxy CDP est disponible sur localhost:18000, verifier clasp login --status. Sinon, verifier uniquement la presence des tokens.

## Interdictions

- L'agent ne peut JAMAIS generer de faux tokens ou credentials
- L'agent ne peut JAMAIS executer clasp login (flux OAuth interactif necessitant un navigateur)
- L'agent ne peut JAMAIS revoquer un token cote GitHub

## Sceau WAL

WAL-0x243-CLASPR-AUTH-GUARD (RC = 0, F = 0.0, H = 0.0)

## Voûte de Référence SSoT

[GOUV](https://gemini.google.com/notebook/83e23803-655d-4f3b-9e40-db7e45f8cad4)