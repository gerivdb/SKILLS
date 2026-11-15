---
name: verbatim-extraction-gate
description: Protocole de lecture stricte : interdit toute paraphrase ou synthèse de données brutes (DOM, logs, fichiers). Toute lecture doit être citée en bloc de code avec hash SHA-256.
---
# Skill : env6-verbatim-extraction-gate

## Objet
Interdire tout résumé, paraphrase ou interprétation d'une donnée brute (DOM, log, fichier, sortie d'outil). Toute lecture doit être restituée textuellement, avec hash SHA-256 pour vérification.

## Cause racine
Les LLM sont des moteurs de synthèse, pas des extracteurs de données. Lorsqu'un LLM lit un fichier ou un DOM, il a tendance à reformuler, omettre des détails ou inventer des contenus plausibles. Dans un système de gouvernance, cela transforme une preuve factuelle en interprétation subjective.

## Règles obligatoires

### 1. Interdiction de paraphraser
Toute donnée lue depuis une source externe (fichier, DOM, fichier de log, sortie d'outil, réponse d'un autre agent) doit être restituée textuellement, entre triple backticks.

Interdit :
- "Le fichier dit que l'opération a réussi" → le texte exact du fichier doit être cité intégralement.
- "Le handler retourne 202" → le corps de la réponse doit être cité intégralement.
- "L'ACK est présent" → le texte exact `[ENV6] ACK <token>` doit être cité.

Obligatoire :
- ````text
<texte exact lu dans la source>
``` ``
Hash SHA-256 : <hash>

### 2. Obligation de hash SHA-256
Tout texte cité doit être accompagné de son empreinte SHA-256 calculée sur le texte brut exact. Sans hash, la lecture n'est pas opposable.

### 3. Filtrage par rôle (pour les conversations)
Dans un DOM de conversation, seules les lignes appartenant au rôle cible (ex: `assistant`) sont éligibles à une corrélation. Les blocs `user` sont exclus de la corrélation de réponse.

### 4. Filtrage par format (pour les réponses ACK)
Dans un bloc assistant, seule une ligne commençant par `[ENV6] ACK <token>` est considérée comme un ACK valide. Toute autre occurrence du token (ex: dans un exemple, dans une phrase de refus) est ignorée.

### 5. Détection de non-concordance
Si le hash du texte cité ne correspond pas au hash du fichier/source original, la lecture est considérée comme invalide et doit être rejetée.

## Contrat de sortie
Tout document citant une donnée brute doit contenir :

```
```text
<texte exact lu dans la source>
```
Hash SHA-256 : <hash>
```

## Anti-patterns bloqués
- `Le fichier dit que l'opération a réussi` → interdit.
- `"Il dit oui"` → interdit.
- `"Le document confirme..."` → interdit.
- Tout résumé sans le texte original cité intégralement.

## Fichier de référence
- `scripts/env6_channel.py` : utilisateur du skill pour la lecture CDP.
- `scripts/env6_channel_v2.py` : utilise le même contrat.
- `scripts/env6_channel_engine.py` : moteur de corrélation ACK qui utilise le même contrat.
- `scripts/env6_channel_v2.py` : même contrat.

## Référence ADR
- **ADR** : ADR-2026-11-15-006-COGNITIVE-DETERMINISM.md
- **IntentHash** : 0xCOGNITIVE_DETERMINISM_20261115
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
