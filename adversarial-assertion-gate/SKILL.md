---
name: adversarial-assertion-gate
description: Assertions E2E rigoureuses : interdit le `includes()` permissif, impose l'ancrage regex `^`, le test de négation, le hash SHA-256 et le timestamp UTC.
---
# adversarial-assertion-gate

## Rôle
Assurer que toute preuve de communication machine (ACK, token, handshake, livraison de message) est **incontestable** : pas de sous-chaîne dans une phrase de refus, pas d'affirmation sans preuve, pas de timestamp manquant.

## Cause racine
Un `t.includes("[ENV6] ACK M-TEST-991")` matchait la phrase *"Je ne réponds pas [ENV6] ACK M-TEST-991"* comme un succès, créant un faux positif. Le mot "ack" apparait aussi dans des refus.

## Contrat obligatoire

### 1. Ancre de début (`^`)
Toute vérification de token/ACK utilise une regex ancrée :
```
^\[ENV6\]\s+ACK\s+([A-Za-z0-9._:-]{4,128})\b
```
L'ACK doit être en début de message, pas enfoui dans une phrase de refus ou une citation.

### 2. Exclusion des refus (négation testée)
Avant d'accepter un message comme ACK valide, vérifier qu'il **ne contient pas** un pattern de négation :
- `Je ne réponds pas`
- `Je ne suis pas ENV6`
- `pas [ENV6]`
- `refus`

Si le message contient un refus, il est rejeté même s'il contient le token.

### 3. Preuve par hash et timestamp
Toute correspondance ACK est accompagnée :
- Hash SHA-256 du texte brut du message validé
- Horodatage UTC ISO-8601 au moment de la détection
- Rôle de l'émetteur (doit être `assistant`, pas `user`)

### 4. Filtrage par rôle assistant
Seuls les blocs marqués comme assistant (`.f9bf7997` / `[class*="f9bf"]`) sont candidats à un ACK. Les blocs utilisateur (`.fa81` / `[class*="fa81"]`) sont exclus.

## Contrat de sortie
```json
{
  "verified": true|false,
  "matched_token": "M-TEST-991",
  "matched_text": "[ENV6] ACK M-TEST-991",
  "matched_role": "assistant",
  "hash_sha256": "<hash>",
  "timestamp_utc": "2026-11-15T19:XX:XXZ",
  "conv_id": "...",
  "reason": null | "message_from_user_role" | "negation_phrase_detected" | "anchor_missing"
}
```

## Antipatterns bloqués
- `t.includes("ACK")` → interdit
- `t.includes("[ENV6] ACK M-TEST-991")` sans vérification de rôle → interdit (matche un refus)
- `re.search("ACK", text)` sans ancrage → interdit
- Acceptation sans hash SHA-256 → interdit
- Acceptation sans horodatage → interdit