---
type: skill
version: "1.0.0"
date: "2026-09-15"
status: draft
intent_hash: 0xINVENTORY_RECONCILER_INTERPRETER_20260915
---

# Skill: inventory-reconciler-interpreter

## Purpose
Interprète les sorties JSON de l'inventaire et filtre les faux positifs :
- `do_not_create: true`
- `archived`
- `dormant`
- Garde uniquement les entrées `BLOCKING`

## Context
L'inventaire des repos (`known_repositories.yaml`) génère des alertes qui nécessitent
une interprétation humaine. Ce skill automatise le filtrage et ne garde que les
écarts bloquants nécessitant une action.

## Prerequisites
- `known_repositories.yaml` à jour
- Accès en lecture au fichier d'inventaire JSON

## Workflow

### 1. Charger l'inventaire
```yaml
# known_repositories.yaml
# Extraire les entrées avec do_not_create: true, archived, dormant
```

### 2. Filtrer
| Filtre | Action |
|--------|--------|
| `do_not_create: true` | Ignorer |
| `status: archived` | Ignorer |
| `status: dormant` | Ignorer |
| `status: active` + `local_path` manquant | **BLOCKING** |
| `status: active` + remote manquant | **BLOCKING** |

### 3. Classifier
```json
{
  "blocking": [...],
  "warning": [...],
  "info": [...]
}
```

### 4. Générer un rapport
```
[INVENTORY] total=<N> blocking=<M> warning=<K> info=<L>
[INVENTORY] blocking_items:
  - repo=<name> issue=<description>
```

## Anti-patterns
- ❌ Signaler tous les items comme bloquants
- ❌ Ignorer les vrais BLOCKING
- ❌ Traiter les archived comme actifs

## References
- **Rule** : clone-causal-prevention.md
- **Rule** : hitl-clone-gate.md
- **Skill** : repo-cleanliness-validator
