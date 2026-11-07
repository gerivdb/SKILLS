---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_META_COHERENCE_VALIDATOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/meta-coherence-validator/SKILL.md
---

# Skill — meta-coherence-validator

Valider la méta-cohérence entre tous les PRD MOC de l'écosystème.

## Rôle
- Vérifier que les références entre PRD MOC sont cohérentes
- Détecter les contradictions
- Valider les designs, concepts, skills, boot sequences
- Valider la présence des sections `## 7. Implémentation` et `## 8. Glossaire des statuts`
- Vérifier que tous les livrables utilisent un statut autorisé de la taxonomy MOX

## Taxonomy des statuts (ADR-2026-08-13-001)

Seuls les 8 statuts suivants sont autorisés :
- 📄 Documenté
- 🔧 Implémenté
- 🧪 Testé
- 🚀 Opérationnel
- 🟢 Actif
- 🟡 Passif
- ⏸️ Pending
- ❌ Bloqué

## Commandes
- `meta-coherence-validator validate --prd-moc <path>`
- `meta-coherence-validator validate --all`

## Règles de validation
1. Section `## 7. Implémentation` présente avec tableau des livrables
2. Section `## 8. Glossaire des statuts` présente avec la taxonomy à 8 statuts
3. Tous les livrables utilisent un statut autorisé
4. Preuves cohérentes avec le statut déclaré
5. `✅ FAIT` générique interdit dans les nouvelles sections `## 7. Implémentation`
