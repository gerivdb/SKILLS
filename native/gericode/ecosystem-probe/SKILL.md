---
name: ecosystem-probe
description: "Découverte automatique de l'écosystème avant toute session. Scanne skills, workflows, citizens, designs et produit ecosystem-index.json."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_ECOSYSTEM_PROBE_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ecosystem-probe/SKILL.md
triggers:
  - "découvrir écosystème"
  - "scan skills"
  - "scan workflows"
  - "ecosystem-index"
tools:
  - bash
  - read
  - write
citizen: "ECOSYSTEM-BRAIN"
layer: "L4"
---

# Skill — ecosystem-probe

> **Verdict** : **SKILL D'EXÉCUTION** — Découverte automatique de l'écosystème.

---

## Objectif

Scanner skills, workflows, citizens, designs et produire `ecosystem-index.json`.

---

## Déclencheur

- Début de session multi-skill
- BOOT-0 (session-boot-sequence)
- Avant toute création de skill/workflow/citizen

---

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `repo_root` | Path | Racine du repo GeriCode |

---

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `index` | EcosystemIndex | Index de l'écosystème |
| `ecosystem-index.json` | file | Index sauvegardé |

---

## Règles

1. Scanner `.kilo/skills/` pour les skills
2. Scanner `.kilo/workflows/` pour les workflows
3. Scanner `act-protocol/citizens.yaml` pour les citizens
4. Scanner `unified-design/designs/` pour les designs
5. Sauvegarder dans `ecosystem-index.json`

---

## Exemple d'usage

```python
from pathlib import Path
from ecosystem_probe import EcosystemProbe

probe = EcosystemProbe(Path("."))
index = probe.scan_all()
probe.save(Path("ecosystem-index.json"))
```

---

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_scan_skills` | Scan skills | Skills détectés |
| `test_scan_workflows` | Scan workflows | Workflows détectés |
| `test_scan_citizens` | Scan citizens | Citizens détectés |
| `test_scan_designs` | Scan designs | Designs détectés |
| `test_save_index` | Sauvegarde index | Fichier JSON créé |

---

## Référence ADR

- **ADR** : ADR-2026-08-07-006-ECOSYSTEM_PROBE
- **IntentHash** : 0xADR_ECOSYSTEM_PROBE_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `ECOSYSTEM-BRAIN` | Découverte automatique |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-720    ecosystem-index.json existe                                        |
| P-721    Tous les skills sont découverts                                    |
| P-722    Tous les workflows sont découverts                                 |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          ecosystem-index.json présent                                      |
| ✓          Scan complet en < 30s                                             |
| ✓          Zéro élément orphelin                                             |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer `ecosystem-index.json`.
2. Logger dans WAL.

---

## Références

- `ecosystem-discovery-boot.yaml`
- `.kilo/skills/ecosystem-brain/SKILL.md`
