---
name: talex-structural-fixes-applier
description: Applique automatiquement les corrections structurelles causales identifiées par le friction analyzer TALEX. Utiliser pour corriger les ERR PowerShell, SQLite, imports, chemins, edit tools, et intégrer les patterns de gouvernance (ONTOLOGY-first, dryrun causal, editorial lock).
version: 1.0.0
intent_hash: 0xTALEX_STRUCTURAL_FIXES_APPLIER_20260923
---

# TALEX Structural Fixes Applier

## Objectif
Appliquer automatiquement les corrections structurelles identifiées par `D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/scripts/talex_friction_analyzer.py`, en respectant les principes causaux et les contraintes SLM.

## Déclencheur
- Rapport `reports/talex_friction_analysis_*.json` généré
- Session complexe multi-repo avec frictions identifiées
- Besoin de corrections structurelles automatisées

## Architecture

```
FRICTION → ANALYZER → RAPPORT JSON → APPLIER → CORRECTIONS
                │                     │
                │                     ├── Dry-run (par défaut)
                │                     ├── Apply (avec confirmation)
                │                     └── Rollback (si besoin)
                │
                └── 18 ERR classées par sévérité
```

## Protocole

### Étape 1 — Charger le rapport

```powershell
$report = Get-Content reports/talex_friction_analysis_<date>.json | ConvertFrom-Json
```

### Étape 2 — Classer les fixes par automatisation

| Fix | Automatique | Manuel | Raison |
|-----|-------------|--------|--------|
| ERR-101: `rm -f` → `Remove-Item -Force` | ✅ | | Pattern regex simple |
| ERR-102: `head` → `Select-Object -First` | ✅ | | Pattern regex simple |
| ERR-104/112: SQLite migration idempotente | ✅ | | Code déjà écrit |
| ERR-105/113: Chemins de test invalides | ✅ | | Pattern regex simple |
| ERR-106/114: tmp_path isolation | ⚠️ | | Nécessite revue manuelle |
| ERR-107/115: conftest.py racine | ✅ | | Fichier unique |
| ERR-111: ONTOLOGY stubs | | ✅ | Création manuelle requise |
| ERR-103/108/109/116: Editorial lock | | ✅ | Documentation seule |
| ERR-117/118/119: Process adoption | | ✅ | Adoption équipe |

### Étape 3 — Dry-run

```powershell
python D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/scripts/talex_structural_fixes_applier.py --dry-run
```

Affiche les corrections sans les appliquer.

### Étape 4 — Apply

```powershell
python D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/scripts/talex_structural_fixes_applier.py --apply
```

Applique les corrections automatiques uniquement.

### Étape 5 — Validation

```powershell
python -m pytest tests -q
```

Vérifie qu'aucune régression n'a été introduite.

## Corrections automatiques disponibles

### PowerShell safe patterns

- `rm -f` → `Remove-Item -Force`
- `head -N` → `Select-Object -First N`
- `tail -N` → `Select-Object -Last N`
- `grep` → `Select-String`
- `sed` → `-replace` PowerShell

### SQLite idempotent migrations

- `PRAGMA index_list` avant `CREATE INDEX`
- `ALTER TABLE` avec vérification colonnes existantes
- Logging des migrations appliquées

### Test hygiene

- Remplacement caractères `/` dans noms fichiers
- Isolation `tmp_path` par cas de test
- Ajout `conftest.py` racine si absent

## Critères de succès

- [ ] Rapport friction chargé
- [ ] Corrections automatiques appliquées
- [ ] Tests passent après corrections
- [ ] Rollback disponible si besoin

## Coordination

| Repo | Action |
|---|---|
| **HERMES** | Exécuter l'applier |
| **GOVERNANCE-HUB** | Mettre à jour les rules PowerShell |

## Références

- `D:/DO/WEB/TOOLS/L4-TOOLS/TALEX/scripts/talex_friction_analyzer.py` — Analyseur de frictions
- `reports/talex_friction_analysis_*.json` — Rapports générés
- `docs/rules/slm-fragmented-approach.md` — Règles SLM
- `tools/infx_checkpoint_bridge.py` — Exemple de migration idempotente

---

## Proof-of-Life
- [x] 2026-09-23T02:16:07+02:00 — Skill créé : talex-structural-fixes-applier


