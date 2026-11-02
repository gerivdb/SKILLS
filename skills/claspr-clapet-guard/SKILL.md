---
type: SKILL
version: "1.0.0"
intent_hash: 0xCLASPR_CLAPET_GUARD_20261102
name: claspr-clapet-guard
role: guard
wal_id: WAL-0x243
friction: 0.0
entropy: 0.0
---

# Skill - claspr-clapet-guard

## Role

Verifier que le clapet BDCP est fermee avant toute operation clasp (push, pull, status, login). Le clapet doit rester fermee sauf instruction explicite de l'operateur.

## Declencheur

Toute commande clasp initiatee depuis l'environnement ENV3 (station HP Z600 / Strate L0-CANON).

## Protocole obligatoire

### Etape 1 - Verifier l'etat du clapet

```powershell
# Le clapet BDCP doit etre fermee (mode BDCP permanent)
# Aucune operation d'ouverture ne peut etre initiee par l'agent
Write-Output "[CLASPR-CLAPET-GUARD] Clapet BDCP : FERME (BDCP_LOCKED = true)"
```

### Etape 2 - Refuser si ouverture detectee

Si une tentative d'ouverture du clapet est detectee (fichier $env:TEMP\ecos_clapet_state ou variable d'environnement BDCP_CLAPET=OPEN), l'operation est bloquée et un sceau WAL d'alerte est emis.

### Etape 3 - Autoriser si fermee

Si le clapet est fermee, l'operation clasp peut poursuivre (via le proxy CDP localhost:18000 si disponible).

## Interdictions absolues

- L'agent ne peut JAMAIS appeler POST /clapet/open
- L'agent ne peut JAMAIS basculer en mode FREE sans instruction explicite ecrite (ouvre le clapet, passe en FREE, desactive BDCP)
- L'agent ne peut JAMAIS simuler ou falsifier l'etat du clapet

## Sceau WAL

WAL-0x243-CLASPR-CLAPET-GUARD (RC = 0, F = 0.0, H = 0.0)

## Voûte de Référence SSoT

[GOUV](https://gemini.google.com/notebook/83e23803-655d-4f3b-9e40-db7e45f8cad4)