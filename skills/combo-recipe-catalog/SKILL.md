---
type: skill
version: "1.0.0"
date: "2026-10-25"
intent_hash: 0xCOMBO_RECIPE_CATALOG_20261025
status: active
---

# Skill: combo-recipe-catalog

## Rôle
Registre des Combos standards de l'écosystème (ex: Combo-Incident-Triage), permettant de lister, valider et récupérer les recettes de combo disponibles.

## Objectif
Maintenir un catalogue centralisé de recettes de combo, valider leur structure (compétences, dépendances, contexte), et fournir les métadonnées nécessaires à l'exécution par le pipeline.

## Script
`scripts/catalog.ps1` — liste et valide les recettes de combo

## Usage
```powershell
# Lister toutes les recettes du catalogue
.\scripts\catalog.ps1 -Action List

# Valider une recette spécifique
.\scripts\catalog.ps1 -Action Validate -Recipe "combo-incident-triage"

# Récupérer la définition d'une recette
.\scripts\catalog.ps1 -Action Get -Recipe "combo-incident-triage"
```

## Catalogue de recettes (JSON)
```json
{
  "catalogVersion": "1.0.0",
  "recipes": [
    {
      "id": "combo-incident-triage",
      "name": "Combo-Incident-Triage",
      "version": "1.0.0",
      "description": "Triage d'incident : détection ? qualification ? notification ? clôture",
      "skills": ["skill-detect", "skill-qualify", "skill-notify", "skill-close"],
      "domain": "incident-management"
    }
  ]
}
```

## WAL NEXUS
- Entité : COMBO_RECIPE_CATALOG
- Action : catalog_query
- WAL path : WAL/combo/recipe-catalog.wal
- Preuve : `[COMBO_CATALOG] action=<List|Validate|Get> recipe=<id> status=OK|FAIL skills=<N> ts=<UTC>`
- Contrat : toute recette listée doit posséder au moins une compétence et un identifiant unique.

## Opérations supportées
| Action | Description |
|--------|-------------|
| `List` | Retourne toutes les recettes enregistrées |
| `Validate` | Vérifie la structure d'une recette (skills, dépendances, contexte) |
| `Get` | Retourne la définition complète d'une recette |

## Anti-patterns
- Recette sans compétence (liste vide)
- Identifiant de recette dupliqué dans le catalogue
- Référence à une compétence non déclarée dans le catalogue de skills

## Références
- ADR : PRD-MOC-GEN-012 DESIGN-F (registre de recettes, cohérence)
- INTENT : INTENT-COMBO-RECIPE-CATALOG (GOVERNANCE-HUB/INTENTS/)