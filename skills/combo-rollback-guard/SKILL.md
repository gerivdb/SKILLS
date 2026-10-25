---
type: skill
version: "1.0.0"
date: "2026-10-25"
intent_hash: 0xCOMBO_ROLLBACK_GUARD_20261025
status: active
---

# Skill: combo-rollback-guard

## Rôle
Fournit un mécanisme de transaction atomique aux Combos (undo en cas d'échec), garantissant que chaque étape partiellement appliquée peut être révoquée dans l'ordre inverse.

## Objectif
Enregistrer les effets de bord de chaque step d'un combo, et en cas d'échec, exécuter les opérations d'undo dans l'ordre inverse (LIFO) pour restaurer l'état cohérent antérieur.

## Script
`scripts/rollback.ps1` — gère le rollback atomique d'un combo

## Usage
```powershell
# Démarrer une transaction atomique pour un combo
.\scripts\rollback.ps1 -Action Begin -ComboId "combo-incident-triage"

# Enregistrer un effet de bord avec sa fonction d'undo
.\scripts\rollback.ps1 -Action Record -ComboId "combo-incident-triage" -Step "skill-a" -UndoFn "Undo-SkillA"

# Exécuter le rollback en cas d'échec
.\scripts\rollback.ps1 -Action Rollback -ComboId "combo-incident-triage"
```

## Format d'enregistrement de transaction (JSON)
```json
{
  "comboId": "combo-incident-triage",
  "transactionId": "txn-001",
  "steps": [
    { "stepId": "skill-a", "undoFn": "Undo-SkillA", "applied": true },
    { "stepId": "skill-b", "undoFn": "Undo-SkillB", "applied": false }
  ],
  "status": "active|rolled-back|committed"
}
```

## WAL NEXUS
- Entité : COMBO_ROLLBACK_GUARD
- Action : atomic_transaction
- WAL path : WAL/combo/rollback-guard.wal
- Preuve : `[COMBO_TXN] comboId=<id> txnId=<id> step=<id> action=BEGIN|RECORD|UNDO|COMMIT|ROLLBACK status=OK|FAIL ts=<UTC>`
- Contrat : le rollback est toujours exécuté dans l'ordre inverse de l'application (LIFO).

## États de transaction
| État | Signification |
|------|---------------|
| `ACTIVE` | Transaction en cours, aucun échec détecté |
| `COMMITTED` | Toutes les étapes ont réussi, transaction validée |
| `ROLLED_BACK` | Rollback effectué, état restauré |
| `FAILED` | Échec irrécupérable, rollback impossible |

## Anti-patterns
- Ne jamais enregistrer un effet de bord sans fonction d'undo associée
- Ne pas appeler COMMIT avant que toutes les étapes soient vérifiées
- Exécuter le rollback dans le même ordre que l'application (au lieu de LIFO)

## Références
- ADR : PRD-MOC-GEN-012 DESIGN-E (transaction atomique, proof-of-life)
- INTENT : INTENT-COMBO-ROLLBACK-GUARD (GOVERNANCE-HUB/INTENTS/)