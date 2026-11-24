---
name: memskill
description: Boucle d'apprentissage qui extrait, raffine et réutilise des skills à partir des trajectoires et retours d'exécution. Pattern inspiré de https://github.com/ViktorAxelsen/MemSkill
version: 1.0.0
intent_hash: 0xSKILL_MEMSKILL_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/ViktorAxelsen/MemSkill
source_url: https://github.com/ViktorAxelsen/MemSkill
path: memskill
---

# MemSkill — Skill KiloCode

## Objectif

Boucle d'apprentissage continue qui extrait, raffine et réutilise des skills à partir des trajectoires d'exécution et des retours (feedback). Ce skill encapsule le pattern du repo externe `MemSkill` adapté à l'environnement local ENV2.

## Déclencheur

Ce skill s'active quand :
- Une exécution de skill se termine avec un code de retour (succès ou échec)
- Un utilisateur fournit un feedback sur un skill (succès, échec, contournement)
- Un skill doit être raffiné ou promu de draft → active
- Le score d'utilité d'un skill atteint un seuil de révision

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `skill_name` | string | ✅ | Nom du skill exécuté |
| `execution_trace` | string | ✅ | Trajectoire d'exécution (commandes, fichiers, sortie) |
| `feedback_score` | integer | ❌ | Score d'utilité (+1 succès, -2 échec, -1 contourné) |
| `exit_code` | integer | ❌ | Code de retour de l'exécution |
| `timestamp_utc` | string | ✅ | Horodatage UTC de l'exécution |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `refined_skill` | string | Nom du skill raffiné (ou même nom si inchangé) |
| `version_increment` | string | Nouvelle version semver (ex: v0.1.0 → v0.1.1) |
| `utility_score` | integer | Score d'utilité mis à jour |
| `status` | enum | draft / active / superseded / archived |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Extraction de la trajectoire

```
→ Lire la trace d'exécution du skill
→ Identifier les étapes atomiques (1 action = 1 outil)
→ Valider que chaque étape a une preuve brute (stdout, hash, timestamp)
```

### Étape 2 — Raffinement du skill

```
→ Si exit_code == 0 et preuve brute présente → promouvoir ou incrémenter la version
→ Si exit_code != 0 → analyser l'erreur et corriger le SKILL.md
→ Incrémenter semver (v0.1.0 → v0.1.1 pour correction mineure)
```

### Étape 3 — Mise à jour du score d'utilité

```
→ score += feedback_score
→ Si score ≤ -5 → marquer le skill comme "mort" (révision ou archivage)
→ Si score ≥ 5 → confirmer le statut active
```

### Étape 4 — Régénération de l'index

```
→ Appeler index-skills.ps1 pour régénérer skills-index.json
→ Vérifier que le nouveau skill est indexé et découvrable
```

## Anti-patterns

- ❌ Écrire un script inline pour raffiner un skill sans passer par le protocole de promotion (validate-skill.ps1)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC dans la preuve d'exécution
- ❌ Créer un skill en doublon avec le même intent_hash qu'un skill existant
- ❌ Ne pas mettre à jour skills-index.json après promotion

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : proof-recalculation
- **Règle** : explicit-path-compliance
