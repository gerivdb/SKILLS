---
type: SKILL
version: "1.0.0"
intent_hash: 0xSKILL_SOT_REGISTRY_GUARDIAN_20260807
---

# Skill — sot-registry-guardian

## Objectif

Protéger `known_repositories.yaml` contre les modifications non validées.
Bloque les writes directs, force l'usage du mapping local ou du skill d'injection.

## Déclencheur

- Avant toute écriture dans `known_repositories.yaml`
- Hook git pre-commit sur `known_repositories.yaml`
- Vérification avant tout script de mise à jour du SOT

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
| `caller` | str | Nom de l'appelant (skill/script) |
| `channel` | str | Canal d'écriture utilisé |

## Canaux approuvés

| Canal | Description |
|-------|-------------|
| `yaml-safe-injector` | Injection YAML sécurisée via skill validé |
| `verse_mapping` | Lecture seule depuis mapping local |
| `sot-registry-guardian` | Vérifications internes du guardian |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `audit` | list | Journal des accès vérifiés |

## Règles

### 1. Toute écriture doit être déclarée
- Appeler `check_write(caller, channel)` AVANT toute modification
- Si le channel n'est pas approuvé → `SOTGuardianError`

### 2. Les writes directs sont interdits
- `open(path, "w")` → BLOQUÉ
- `Path.write_text()` → BLOQUÉ
- `yaml.dump()` direct → BLOQUÉ
- Uniquement via `yaml-safe-injector`

### 3. Audit systématique
- Toutes les vérifications sont loggées
- Le journal est consultable via `audit()`

## Exemple d'usage

```python
from pathlib import Path
from sot_registry_guardian import SOTGuardian, SOTGuardianError

guardian = SOTGuardian(Path("known_repositories.yaml"))

try:
    guardian.check_write("my-skill", "yaml-safe-injector")
    # ... injection autorisée ...
except SOTGuardianError as e:
    print(f"Write bloqué: {e}")
```

## Tests

| Test | Description |
|------|-------------|
| `test_approved_channel_passes` | Canal approuvé passe |
| `test_unknown_channel_blocked` | Canal inconnu est bloqué |
| `test_audit_log` | Journal des accès |

## Référence ADR

- **ADR** : ADR-2026-08-07-002-SOT-REGISTRY-GUARDIAN
- **IntentHash** : 0xADR_SOT_REGISTRY_GUARDIAN_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
