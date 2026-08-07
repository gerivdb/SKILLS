---
type: SKILL
version: "1.0.0"
intent_hash: 0xSKILL_YAML_DEBUG_FORENSIC_20260807
---

# Skill — yaml-debug-forensic

## Objectif

Diagnostiquer les erreurs YAML courantes sans modifier le fichier.
Génère un rapport de corruption.

## Déclencheur

- Fichier YAML qui refuse de parser
- Erreur après tentative d'injection
- Audit préventif de `known_repositories.yaml`
- Vérification avant commit

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `yaml_path` | Path | Chemin du fichier YAML à diagnostiquer |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `report` | YAMLCorruptionReport | Rapport de corruption détaillé |

## Vérifications

| Vérification | Description |
|--------------|-------------|
| Parse YAML | Le fichier parse-t-il correctement ? |
| Clés dupliquées | Y a-t-il des clés dupliquées dans un mapping ? |
| Quotes cassées | Les quoted strings sont-elles fermées ? |
| Ancres invalides | Les alias `*anchor` existent-ils ? |

## Exemple d'usage

```python
from pathlib import Path
from yaml_debug_forensic import YAMLDebugForensic

forensic = YAMLDebugForensic(Path("known_repositories.yaml"))
report = forensic.diagnose()

if report.is_clean:
    print("YAML valide")
else:
    for issue in report.issues:
        print(f"ERREUR: {issue}")
```

## Tests

| Test | Description |
|------|-------------|
| `test_valid_yaml` | YAML valide → rapport clean |
| `test_parse_error` | YAML invalide → parse_ok=False |
| `test_duplicate_keys` | Détecte les clés dupliquées |
| `test_broken_quotes` | Détecte les quotes cassées |
| `test_invalid_anchors` | Détecte les ancres invalides |

## Référence ADR

- **ADR** : ADR-2026-08-07-003-YAML-DEBUG-FORENSIC
- **IntentHash** : 0xADR_YAML_DEBUG_FORENSIC_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
