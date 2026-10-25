---
name: agent-corridor-handoff
description: Optimise la transmission de mission d'un agent a un autre (DO -> CHECK, Specification -> Implémentation) via .kilo/transfers/. Genere un payload ultra-compact pour eviter la saturation de contexte.
version: 1.0.0
intent_hash: 0xAGENT_CORRIDOR_HANDOFF_20261025
---

# Agent Corridor Handoff

## Objectif
Optimiser la transmission de mission d'un agent a un autre (ex: DO => CHECK ou Specification => Implementation) via le repertoire .kilo/transfers/. Elimine le bruit de bavardage pour reduire la consommation de tokens et saturer moins la fenetre de contexte du modele.

## Declencheur
- Cloture de session (SESSION-CLOSEOUT)
- Bascule d'agent (changement de role ou de corridor)
- Passage de relais architecture DO + CHECK

## Prerequis
- Repertoire .kilo/transfers/ accessible en ecriture
- Repo git valide avec historique de commits
- Accès en lecture aux diffs git et aux resultats de tests

## Protocole

### Etape 1 - Extraire les elements de la session sortante
1. Diffs git : `git diff HEAD~1..HEAD --stat` pour identifier les fichiers modifies
2. Tests valides : lister les fichiers de test modifiés ou ajoutes
3. Decisions clées : extraire les decisions architektoniques prises (messages de commit, commentaires)

### Etape 2 - Generer le HANDOFF_PAYLOAD.json
Creer un fichier JSON ultra-compact contenant :
- `session_id` : identifiant de la session sortante
- `timestamp_utc` : horodatage ISO-8601
- `modified_files` : liste des fichiers modifies avec leur statut
- `test_files` : liste des fichiers de tests valides
- `key_decisions` : decisions architektoniques prises
- `open_questions` : questions en suspens pour la session entrante
- `next_actions` : actions prioritaires pour la session suivante

### Etape 3 - Injecter le payload dans la session entrante
Le fichier HANDOFF_PAYLOAD.json est place dans .kilo/transfers/ et doit etre injecte directement dans le prompt d'initialisation de la session entrante.

## Sortie standard

```json
{
  "session_id": "<id>",
  "timestamp_utc": "<ISO-8601>",
  "modified_files": ["file1.py", "file2.py"],
  "test_files": ["test_file1.py"],
  "key_decisions": ["decision 1", "decision 2"],
  "open_questions": ["question 1"],
  "next_actions": ["action 1", "action 2"]
}
```

## Anti-patterns bloquants
- Injecter l'historique complet de la session (saturation de contexte)
- Oublier les decisions clees (perte de contexte architektonique)
- Ne pas verifier que le payload est lisible par la session entrante
- Placer le payload hors de .kilo/transfers/

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xAGENT_CORRIDOR_HANDOFF_20261025
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed

## Script cible
`scripts/pack_handoff.py`