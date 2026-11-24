---
name: agent-memory-techniques
description: Notebook et implémentation de mémoire procédurale (extraction de séquences d'actions, paramétrisation de templates et réutilisation). Pattern inspiré de https://github.com/NirDiamant/Agent_Memory_Techniques
version: 1.0.0
intent_hash: 0xSKILL_AGENT_MEMORY_TECHNIQUES_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/NirDiamant/Agent_Memory_Techniques
source_url: https://github.com/NirDiamant/Agent_Memory_Techniques
path: agent-memory-techniques
---

# Agent Memory Techniques — Skill KiloCode

## Objectif

Implémenter la mémoire procédurale par extraction de séquences d'actions depuis des traces d'exécution, paramétrisation de templates et réutilisation. Ce skill encapsule les techniques du repo externe `Agent_Memory_Techniques` adapté à ENV2.

## Déclencheur

Ce skill s'active quand :
- Il faut extraire une procédure répétitive depuis une trace d'exécution
- Un template d'action doit être paramétré pour réutilisation
- Une séquence d'actions doit être transformée en skill exécutable
- La mémoire procédurale doit être interrogée avant une action

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `execution_trace` | string | ✅ | Trace brute d'exécution (commandes, fichiers, sortie) |
| `template_name` | string | ❌ | Nom du template à paramétrer |
| `parameters` | object | ❌ | Paramètres à injecter dans le template |
| `target_skill` | string | ❌ | Nom du skill cible de la réutilisation |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `action_sequence` | array | Séquence d'actions extraites et ordonnées |
| `parameterized_template` | string | Template avec paramètres injectés |
| `reusable_skill` | string | Nom du skill généré ou réutilisé |
| `execution_proof` | object | Preuve d'exécution (hash, timestamp, exit_code) |
| `evidence_hash` | string | Hash SHA-256 de la trace source |

## Protocole Obligatoire

### Étape 1 — Analyse de la trace d'exécution

```
→ Lire la trace brute (stdout, logs, git diff, fichiers modifiés)
→ Identifier les étapes atomiques (1 action = 1 outil = 1 résultat vérifiable)
→ Valider que chaque étape a une preuve brute correspondante
```

### Étape 2 — Extraction de séquences d'actions

```
→ Ordonner les actions par séquence chronologique
→ Paramétrer les variables (chemins absolus, noms de repos, IntentHash)
→ Dédupliquer les séquences identiques
→ Stocker sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\agent-memory-techniques\templates\
```

### Étape 3 — Paramétrisation du template

```
→ Remplacer les valeurs concrètes par des paramètres nommés
→ Définir le type et la contrainte de chaque parameter
→ Générer le SKILL.md associé au template
```

### Étape 4 — Réutilisation et preuve

```
→ Avant toute réutilisation, vérifier que le template existe et est valide
→ Injecter les paramètres fournis
→ Exécuter le skill et capturer la preuve brute (stdout, hash SHA-256, timestamp UTC)
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Extraire une séquence d'actions sans preuve brute (stdout, hash, timestamp)
- ❌ Utiliser des chemins relatifs au lieu de chemins absolus explicites (règle explicit-path-compliance)
- ❌ Créer un script inline pour réutiliser un template sans vérifier qu'un skill existe déjà
- ❌ Oublier l'enregistrement WAL après exécution

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
