---
name: building-with-decision-models
description: Exemple de skill structuré pour ancrer des décisions dans des modèles explicites. Pattern inspiré de https://github.com/aaddrick/building-with-decision-models
version: 1.0.0
intent_hash: 0xSKILL_BUILDING_WITH_DECISION_MODELS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/aaddrick/building-with-decision-models
source_url: https://github.com/aaddrick/building-with-decision-models
path: building-with-decision-models
---

# Building with Decision Models — Skill KiloCode

## Objectif

Ancrer des décisions dans des modèles explicites, traçables et vérifiables. Ce skill encapsule le pattern du repo externe `building-with-decision-models` adapté à ENV2, avec respect des règles de gouvernance, de preuve fraîche et de traçabilité WAL.

## Déclencheur

Ce skill s'active quand :
- Une décision architecturale doit être prise et documentée
- Un modèle de décision explicite doit être créé pour une action
- La traçabilité d'une décision doit être garantie via le WAL
- Une décision doit être révisable et réversible

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `decision_context` | string | ✅ | Contexte de la décision à prendre |
| `options` | array | ✅ | Options possibles avec avantages/inconvénients |
| `criteria` | array | ❌ | Critères de sélection (ex: conformité ADR, impact, complexité) |
| `adr_reference` | string | ❌ | Référence ADR applicable à la décision |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `decision_model` | object | Modèle de décision explicite (option choisie, justification, critères) |
| `decision_path` | string | Chemin absolu vers le fichier de décision |
| `wal_entry` | string | Référence d'entrée WAL pour la décision |
| `reversibility_notes` | string | Notes sur la réversibilité de la décision |
| `evidence_hash` | string | Hash SHA-256 du modèle de décision |

## Protocole Obligatoire

### Étape 1 — Modélisation de la décision

```
→ Déclarer le contexte de la décision
→ Lister les options possibles avec avantages et inconvénients
→ Définir les critères de sélection (conformité ADR, impact, complexité, etc.)
→ Vérifier que la décision ne viole aucune règle existante (skill-citizen-prealable, etc.)
```

### Étape 2 — Sélection de l'option

```
→ Appliquer les critères de sélection à chaque option
→ Choisir l'option qui maximise la conformité et minimise l'impact négatif
→ Documenter la justification du choix
→ Vérifier que la décision est réversible (règle m3tree)
```

### Étape 3 — Ancrage dans un modèle explicite

```
→ Créer le fichier de modèle de décision sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\building-with-decision-models\decisions\
→ Inclure le contexte, les options, les critères, le choix et la justification
→ Calculer le hash SHA-256 du modèle de décision
→ Créer une entrée WAL avec le hash et l'horodatage UTC
```

### Étape 4 — Traçabilité et réversibilité

```
→ Enregistrer l'entrée WAL (WAL-0x243) avec référence à la décision
→ Documenter comment la décision peut être réversée si nécessaire
→ Mettre à jour skills-index.json si un skill est impacté par la décision
→ Produire le hash SHA-256 du modèle de décision
```

## Anti-patterns

- ❌ Prendre une décision sans modèle explicite documenté
- ❌ Ne pas enregistrer la décision dans le WAL (pas de traçabilité)
- ❌ Prendre une décision irréversible sans documentation de réversibilité
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : m3tree
