---
type: SKILL
version: "1.0.0"
intent_hash: 0xSKILL_YAML_DEBUG_FORENSIC_20260807
---

# Skill - yaml-debug-forensic

## Objectif

Diagnostiquer les erreurs YAML courantes sans modifier le fichier.
Genere un rapport de corruption.

## Declencheur

- Fichier YAML qui refuse de parser
- Erreur apres tentative d'injection
- Audit preventif de `known_repositories.yaml`
- Verification avant commit

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `yaml_path` | Path | Chemin du fichier YAML a diagnostiquer |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `report` | YAMLCorruptionReport | Rapport de corruption detaille |

## Verifications

| Verification | Description |
|--------------|-------------|
| Parse YAML | Le fichier parse-t-il correctement ? |
| Cles dupliquees | Y a-t-il des cles dupliquees dans un mapping ? |
| Quotes cassees | Les quoted strings sont-elles fermees ? |
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
| `test_valid_yaml` | YAML valide -> rapport clean |
| `test_parse_error` | YAML invalide -> parse_ok=False |
| `test_duplicate_keys` | Detecte les cles dupliquees |
| `test_broken_quotes` | Detecte les quotes cassees |
| `test_invalid_anchors` | Detecte les ancres invalides |

## Reference ADR

- **ADR** : ADR-2026-08-07-003-YAML-DEBUG-FORENSIC
- **IntentHash** : 0xADR_YAML_DEBUG_FORENSIC_20260807
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
