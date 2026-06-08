---
skill_id: prd-frontmatter-validator
trit_primitive: TritDecompose
version: 1.1.0
updated: 2026-06-09
status: active
tags: [prd, frontmatter, yaml, validation, governance]
---

# prd-frontmatter-validator

## Purpose
Valider et corriger automatiquement le frontmatter YAML des PRDs avant commit.

## Trigger
Use when: user mentions "frontmatter", "PRD validation", "YAML header", or hook pre-commit blocks on frontmatter. Also invoked by `skill-trit-patcher` for batch operations.

## Steps

1. **Lire le frontmatter** du fichier PRD cible
2. **Valider les champs obligatoires** :
   ```yaml
   type: PRD
   status: draft | in_review | approved | archived
   date: YYYY-MM-DD
   author: string
   nexus_tag: CONFORME_NEXUS | À_VALIDER_NEXUS | HORS_NEXUS
   intent_hash: 0x[A-Z_]+_[0-9]{8}
   ```
3. **Appliquer les règles de validation** (see Rules below)
4. **Corriger automatiquement** si autorisé (see Corrections below)
5. **Signaler** les corrections nécessitant validation humaine

## Rules
- `status` : valeur dans enum strict — reject any other value
- `reviewed_at` : required if `status: in_review | approved`, format `YYYY-MM-DD`
- `superseded_by` : required if `status: archived`
- `supersedes` : required if version > 1
- Duplicate fields: forbidden — signal `PRD_FRONTMATTER_DUPLICATE`
- `φ-CPS ≥ 4.559` : required if `nexus_tag: CONFORME_NEXUS`

## Corrections automatiques autorisées
- Normalisation de la casse des valeurs enum
- Ajout de `reviewed_at: <today>` si manquant et status `in_review`

## Corrections nécessitant validation humaine
- Changement de `status`
- Modification de `intent_hash`
- Ajout de `superseded_by`

## Output
- Valid frontmatter YAML
- Report of auto-corrections applied
- List of items requiring human validation

## Example

```yaml
# Before (invalid)
type: PRD
status: in_review
date: 2026-06-09
author: owl-alpha

# After (auto-corrected)
type: PRD
status: in_review
date: 2026-06-09
author: owl-alpha
reviewed_at: 2026-06-09
nexus_tag: À_VALIDER_NEXUS
intent_hash: 0xPRD_EXAMPLE_20260609
```
