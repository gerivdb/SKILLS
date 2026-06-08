---
trit_primitive: TritDecompose
---
# prd-frontmatter-validator

## Objectif
Valider et corriger automatiquement le frontmatter YAML des PRDs avant commit.

## Champs obligatoires PRD

```yaml
type: PRD
status: draft | in_review | approved | archived
date: YYYY-MM-DD
author: string
nexus_tag: CONFORME_NEXUS | À_VALIDER_NEXUS | HORS_NEXUS
intent_hash: 0x[A-Z_]+_[0-9]{8}
```

## Validations
- `status` : valeur dans enum strict — refuser toute autre valeur
- `reviewed_at` : présent si `status: in_review | approved`, format `YYYY-MM-DD`
- `superseded_by` : présent si `status: archived`
- `supersedes` : présent si version > 1
- Doublons de champs : interdits — signaler `PRD_FRONTMATTER_DUPLICATE`
- `φ-CPS ≥ 4.559` : obligatoire si `nexus_tag: CONFORME_NEXUS`

## Corrections automatiques autorisées
- Normalisation de la casse des valeurs enum
- Ajout de `reviewed_at: <today>` si manquant et status `in_review`

## Corrections nécessitant validation humaine
- Changement de `status`
- Modification de `intent_hash`
- Ajout de `superseded_by`
