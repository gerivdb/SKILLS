---
name: cass-memory-system
description: Transforme l'historique dispersé des sessions d'agents en mémoire procédurale persistante et détecte les anti-patterns récurrents. Pattern inspiré de https://github.com/Dicklesworthstone/cass_memory_system
version: 1.0.0
intent_hash: 0xSKILL_CASS_MEMORY_SYSTEM_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/Dicklesworthstone/cass_memory_system
source_url: https://github.com/Dicklesworthstone/cass_memory_system
path: cass-memory-system
---

# Cass Memory System — Skill KiloCode

## Objectif

Systématiser la transformation de l'historique dispersé des sessions d'agents en mémoire procédurale persistante, avec détection automatique des anti-patterns récurrents. Ce skill encapsule le pattern du repo externe `cass_memory_system` adapté à l'environnement local ENV2 (BDCP, strates L*, known_repositories.yaml).

## Déclencheur

Ce skill s'active quand :
- Une session d'agent se termine et laisse des traces d'exécution non structurées
- Un anti-pattern récurrent est détecté dans plusieurs sessions
- Il faut extraire une procédure réutilisable depuis une trajectoire d'exécution
- Une mémoire procédurale doit être consultée avant d'agir sur un repo

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `session_trace` | string | ✅ | Traces brutes de la session (logs, stdout, fichiers modifiés) |
| `agent_id` | string | ✅ | Identifiant de l'agent qui a généré la trace |
| `repo_target` | string | ❌ | Repo cible de la session (pour corrélation avec la SOT) |
| `intent_hash` | string | ❌ | IntentHash de la tâche exécutée |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `procedural_memory` | array | Séquences d'actions extraites et paramétrées |
| `anti_patterns` | array | Anti-patterns détectés avec fréquence |
| `skill_candidates` | array | Skills canoniques proposés pour cristallisation |
| `evidence_hash` | string | Hash SHA-256 de la trace source |
| `timestamp_utc` | string | Horodatage UTC de l'extraction |

## Protocole Obligatoire

### Étape 1 — Collecte des traces de session

```
→ Lire les fichiers de log, stdout, git status, git diff de la session
→ Vérifier que le working tree est propre avant extraction
→ Calculer le hash SHA-256 de la trace source
```

### Étape 2 — Extraction de séquences d'actions

```
→ Identifier les verbes d'action ordonnés (A → B → C)
→ Paramétrer les variables (chemins, noms de repos, IntentHash)
→ Dédupliquer les séquences identiques
→ Stocker dans la mémoire procédurale locale (D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\cass-memory-system\memories\)
```

### Étape 3 — Détection des anti-patterns

```
→ Comparer les séquences extraites avec les anti-patterns connus (règle clone-causal-prevention, hitl-clone-gate, etc.)
→ Signaler les récurrences > 3 occurrences
→ Proposer une correction canonique (skill ou citizen)
```

### Étape 4 — Proposition de skill canonique

```
→ Si une séquence extraite n'a pas de skill correspondant dans skills-index.json → créer un skill draft
→ Si un skill existe déjà → lier la mémoire procédurale au skill existant
→ Enregistrer l'intent_hash du nouveau skill
```

## Anti-patterns

- ❌ Créer un script inline pour extraire de la mémoire sans vérifier qu'aucun skill ne couvre déjà le besoin
- ❌ Storer des traces brutes sans hash SHA-256 ni horodatage UTC
- ❌ Conclure "n'existe pas" sans consulter `known_repositories.yaml` et `skills-index.json`
- ❌ Oublier la preuve d'exécution (hash + timestamp + git status propre)

## Référence ADR

- **ADR** : ADR-20260622-001-illegitimate-clone-prevention
- **IntentHash** : 0xADR_ILLEGIT_CLONE_PREV_20260622
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : hitl-clone-gate
- **Règle** : clone-causal-prevention
- **Règle** : explicit-path-compliance
