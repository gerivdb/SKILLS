---
type: SKILL
version: "1.1.0"
status: active
date: "2026-08-14"
intent_hash: 0xSKILL_MOX_PLAN_CONSULTANT_20260814
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/mox-plan-consultant/SKILL.md
---

# Skill — mox-plan-consultant

Interface unifiée pour que MOX consulte les plans des repos citoyens.

## Objectifs
- Lister les repos citoyens
- Lire les plans PRD/MOC de chaque repo
- Extraire les besoins en nouveaux PRD/MOC
- **Valider que tous les livrables utilisent un statut autorisé de la taxonomy MOX**
- **Rejeter `✅ FAIT` dans les sections `## 7. Implémentation`**

## Entrées
- `repo_name`: nom du repo
- `plans_root`: chemin racine des plans

## Sorties
- `dict`: plans disponibles
- `validation`: résultat de validation MOX

## Règles de validation MOX

### R-MOX-001 : Section 7 et 8 obligatoires

Tout PRD/MOC/ADR/INTENT doit contenir :
- `## 7. Implémentation` avec tableau des livrables
- `## 8. Glossaire des statuts` avec la taxonomy à 8 statuts

### R-MOX-002 : Statuts autorisés

Seuls les 8 statuts suivants sont autorisés :
- 📄 Documenté
- 🔧 Implémenté
- 🧪 Testé
- 🚀 Opérationnel
- 🟢 Actif
- 🟡 Passif
- ⏸️ Pending
- ❌ Bloqué

### R-MOX-003 : Interdiction `✅ FAIT`

`✅ FAIT` est strictement interdit dans les sections `## 7. Implémentation`.
Tout livrable déclaré avec `✅ FAIT` doit être remplacé par un statut autorisé.

### R-MOX-004 : Cohérence statut/preuves

| Statut déclaré | Preuve requise |
|----------------|----------------|
| 📄 Documenté | Fichier présent, frontmatter valide |
| 🔧 Implémenté | Git log + build réussi (compile/test) |
| 🧪 Testé | Tests unitaires + intégration passants |
| 🚀 Opérationnel | Health-check OK, endpoint 200 |
| 🟢 Actif | Dépendants actifs vérifiés |
| 🟡 Passif | Artefact présent, aucun dépendant actif |
| ⏸️ Pending | Blocage governance/HITL/ADR documenté |
| ❌ Bloqué | Dépendance manquante ou ADR refusé documenté |

## Commandes

### audit
```powershell
mox-plan-consultant audit --repo <repo_name>
```
Liste les PRD/MOC et valide les statuts.

### validate
```powershell
mox-plan-consultant validate --path <prd_moc_path>
```
Valide un PRD/MOC spécifique.

### fix
```powershell
mox-plan-consultant fix --path <prd_moc_path>
```
Remplace `✅ FAIT` par le statut autorisé approprié.

## Anti-patterns
- Accepter `✅ FAIT` comme statut valide
- Omettre la section `## 8. Glossaire des statuts`
- Déclarer `🚀 Opérationnel` sans health-check documenté

## Référence ADR
- **ADR** : ADR-2026-08-13-001-PRD-MOC-IMPLEMENTATION-STATUS-TAXONOMY
- **IntentHash** : `0xADR_PRD_MOC_IMPLEMENTATION_STATUS_TAXONOMY_20260813`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
