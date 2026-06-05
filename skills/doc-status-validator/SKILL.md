# Skill: doc-status-validator

## Contexte
Les hooks pre-commit de GOVERNANCE-HUB valident les statuts autorisés par type de document. Écrire un statut invalide cause un rejet systématique du commit.

## Règles par type
- **PRD** : `draft` | `in_review` | `approved` | `archived`
- **EPIC** : `planned` | `active` | `completed` | `archived`
- **INTENT** : `proposed` | `active` | `completed` | `archived`

## Mécanisme
1. Avant écriture d'un PRD/EPIC/INTENT, lire le fichier `.githooks/` ou la documentation de validation du repo cible
2. Extraire les valeurs autorisées pour le type
3. Valider le champ `status` contre cette liste
4. Si invalide : proposer la valeur la plus proche (ex: `implemented` → `approved`, `pending` → `active`, `in_progress` → `active`)
5. Refuser l'écriture si pas de correspondance

## Mapping de secours (si hook non lisible)
- `implemented` → `approved`
- `in_progress` → `active`
- `pending` → `active`
- `Active` (casse) → `active`
- `Done` → `completed`

## Anti-pattern interdit
- Écrire un statut inventé sans validation
- Ignorer le rejet pre-commit et tenter `--no-verify` sans ordre explicite
- Copier un statut d'un autre document sans vérifier le type cible

## Exemple d'application
```
Type : EPIC
Status tenté : Active
→ Validation : FAIL (camelCase interdit)
→ Correction automatique : active
→ Réécriture du fichier
→ Re-validation : OK
```
