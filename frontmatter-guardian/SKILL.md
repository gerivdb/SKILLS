---
name: frontmatter-guardian
description: Audit, validation et auto-correction du frontmatter YAML des documents de gouvernance (EPIC, PRD, INTENT, ADR, REPORT, RPT, GUI, RUN) avec validation JSON Schema HADMG. Utiliser quand le hook pre-commit bloque, quand on écrit un doc de gouvernance, ou pour auditer/corriger le frontmatter existant.
version: 1.1.0
intent_hash: 0xFRONTMATTER_GUARDIAN_HADMG_20260811
---

# Frontmatter Guardian — HADMG Extended

## Quand l'utiliser

- Le hook `pre-commit` bloque un commit avec des erreurs de frontmatter
- On crée ou modifie un document de gouvernance (EPIC, PRD, INTENT, ADR, REPORT, RPT, GUI, RUN)
- On veut auditer l'état du frontmatter dans le repo
- On veut corriger en masse des documents mal formés
- On veut valider le frontmatter contre le schéma HADMG

## Comment l'utiliser

### Diagnostic (dry-run)

```powershell
python scripts/governance/fix_frontmatter.py --dry-run
```

Affiche les corrections nécessaires sans modifier les fichiers.

### Correction automatique

```powershell
python scripts/governance/fix_frontmatter.py --inject
```

Corrige tous les fichiers du repo puis re-stage.

### Fichiers staged uniquement

```powershell
python scripts/governance/fix_frontmatter.py --inject --staged
```

Utile pour corriger uniquement les fichiers du prochain commit.

### Fichier unique

```powershell
python scripts/governance/fix_frontmatter.py --inject --file path/to/doc.md
```

## Règles

### Inférence du type depuis le path

| Segment de path | Type inféré |
|-----------------|-------------|
| `EPICS/` | `EPIC` |
| `INTENTS/` | `INTENT` |
| `PRD/` ou `specs/` | `PRD` |
| `ADR/` | `ADR` |
| `REPORTS/` ou `reports/` | `REPORT` |
| `RPT/` | `RPT` |
| `GUI/` | `GUI` |
| `RUN/` | `RUN` |

### Champs requis par type

| Type | Champs requis |
|------|--------------|
| `PRD` | `type`, `version`, `date`, `status`, `intent_hash` |
| `EPIC` | `intent_hash`, `status`, `priority`, `owner`, `repo` |
| `ADR` | `status`, `date`, `intent_hash` |
| `INTENT` | `intent_hash`, `status`, `priority` |
| `RPT` | `type`, `date`, `intent_hash` |
| `GUI` | `type`, `intent_hash` |
| `RUN` | `type`, `intent_hash` |
| `REPORT` | `type`, `status`, `date`, `owner`, `repo` |

### Status valides par type

| Type | Status valides |
|------|---------------|
| `PRD` | `draft`, `in_review`, `approved`, `archived` |
| `EPIC` | `planned`, `active`, `completed`, `archived` |
| `ADR` | `proposed`, `accepted`, `rejected`, `deprecated`, `archived` |
| `INTENT` | `exploratory`, `proposed`, `approved`, `implemented`, `archived` |
| `RPT` | `draft`, `final`, `archived` |
| `GUI` | `draft`, `active`, `archived` |
| `RUN` | `draft`, `active`, `archived` |
| `REPORT` | `draft`, `final`, `archived` |

### Normalisation automatique

Le script corrige :
- **type** manquant ou invalide → inféré depuis le path
- **status** invalide → normalisé via table de mapping (ex: `Active` → `active`, `in_progress` → `active`, `done` → `completed`)
- **intent_hash** manquant → généré depuis le nom de fichier (`0x{NOM_FICHIER}_AUTOFIX`)
- **priority** manquant → `P2`
- **owner** manquant → `gerivdb`
- **repo** manquant → inféré depuis le path (`gerivdb/{parent}`)
- **version** manquant → `1.0`
- **date** manquant → date du jour

## Validation HADMG (JSON Schema)

Outre les champs YAML standards, le frontmatter doit être validé contre le schéma HADMG :

### Schéma HADMG

| Champ HADMG | Type | Requis | Description |
|-------------|------|--------|-------------|
| `id` | string | ✅ | UUID v4 unique |
| `type` | enum | ✅ | `project`, `goal`, `health`, `finance`, `idea`, `resource`, `proof`, `citizen`, `skill` |
| `domain` | enum | ✅ | `professional`, `personal`, `health`, `finance`, `learning`, `creative` |
| `status` | enum | ✅ | `draft`, `active`, `paused`, `completed`, `archived` |
| `priority` | enum | ✅ | `P0`, `P1`, `P2`, `P3` |
| `created` | string | ✅ | ISO8601 |
| `updated` | string | ✅ | ISO8601 |
| `version` | string | ✅ | Semver (`x.y.z`) |
| `mode` | enum | ✅ | `real`, `plan`, `simulation` |
| `verification_status` | enum | ✅ | `pending`, `passed`, `failed` |

### Vérification HADMG

```powershell
# Valider le frontmatter contre le schéma HADMG
python scripts/governance/validate_hadmg.py --file path/to/doc.md
```

Sortie attendue :
```
HADMG_VALIDATION: PASS
- id: valid UUID
- type: valid enum
- domain: valid enum
- status: valid enum
- priority: valid enum
- created: valid ISO8601
- updated: valid ISO8601
- version: valid semver
- mode: valid enum
- verification_status: valid enum
```

### Auto-correction HADMG

Si des champs HADMG sont manquants ou invalides :
- `id` manquant → générer UUID v4
- `type` invalide → `project` par défaut
- `domain` invalide → `professional` par défaut
- `status` invalide → `draft` par défaut
- `priority` invalide → `P2` par défaut
- `version` invalide → `1.0.0` par défaut
- `mode` invalide → `real` par défaut
- `verification_status` invalide → `pending` par défaut

## Flux pre-commit

1. Le hook détecte les fichiers `.md` staged
2. Il lance `fix_frontmatter.py --inject --staged` (auto-correction)
3. Il re-stage les fichiers corrigés
4. Il valide : champs requis, status valides, unicité intent_hash
5. Il valide HADMG : schéma JSON, champs requis, enums valides
6. Si erreurs résiduelles → commit bloqué

## Référence ADR

- **ADR** : ADR-2026-08-09-001-VALIDATION-CHECKLIST
- **IntentHash** : `0xFRONTMATTER_GUARDIAN_HADMG_20260811`
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
