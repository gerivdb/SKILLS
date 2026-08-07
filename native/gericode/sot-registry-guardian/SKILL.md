---
type: SKILL
version: "1.0.0"
intent_hash: 0xSKILL_SOT_REGISTRY_GUARDIAN_20260807
---

# Skill - sot-registry-guardian

## Objectif

Proteger `known_repositories.yaml` contre les modifications non validees.
Bloque les writes directs, force l'usage du mapping local ou du skill d'injection.

## Declencheur

- Avant toute ecriture dans `known_repositories.yaml`
- Hook git pre-commit sur `known_repositories.yaml`
- Verification avant tout script de mise a jour du SOT

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `known_repositories_path` | Path | Chemin vers known_repositories.yaml |
| `caller` | str | Nom de l'appelant (skill/script) |
| `channel` | str | Canal d'ecriture utilise |

## Canaux approuves

| Canal | Description |
|-------|-------------|
| `yaml-safe-injector` | Injection YAML securisee via skill valide |
| `verse_mapping` | Lecture seule depuis mapping local |
| `sot-registry-guardian` | Verifications internes du guardian |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `audit` | list | Journal des acces verifies |

## Regles

### 1. Toute ecriture doit etre declaree
- Appeler `check_write(caller, channel)` AVANT toute modification
- Si le channel n'est pas approuve -> `SOTGuardianError`

### 2. Les writes directs sont interdits
- `open(path, "w")` -> BLOQUE
- `Path.write_text()` -> BLOQUE
- `yaml.dump()` direct -> BLOQUE
- Uniquement via `yaml-safe-injector`

### 3. Audit systematique
- Toutes les verifications sont loggees
- Le journal est consultable via `audit()`

## Exemple d'usage

```python
from pathlib import Path
from sot_registry_guardian import SOTGuardian, SOTGuardianError

guardian = SOTGuardian(Path("known_repositories.yaml"))

try:
    guardian.check_write("my-skill", "yaml-safe-injector")
    # ... injection autorisee ...
except SOTGuardianError as e:
    print(f"Write bloque: {e}")
```

## Tests

| Test | Description |
|------|-------------|
| `test_approved_channel_passes` | Canal approuve passe |
| `test_unknown_channel_blocked` | Canal inconnu est bloque |
| `test_audit_log` | Journal des acces |

## Reference ADR

- **ADR** : ADR-2026-08-07-002-SOT-REGISTRY-GUARDIAN
- **IntentHash** : 0xADR_SOT_REGISTRY_GUARDIAN_20260807
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
