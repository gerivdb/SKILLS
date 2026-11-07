---
type: ADR
status: proposed
date: "2026-08-19"
intent_hash: 0xADR_SKILL_REVIEW_TO_INTENT_MAPPER_20260819
---

# ADR-2026-08-19-SKILL-REVIEW-TO-INTENT-MAPPER -- Mapping automatique review → INTENT

## Contexte

Les revues V10.0 produisent des retours structurés (M1-M5, items manquants,
recommandations). La transposition manuelle vers l'INTENT est :
- Répétitive
- Source d'oublis
- Non tracée

## Décision

Créer le skill `review-to-intent-mapper` dans L4-TOOLS/SKILLS/skills/ :

**Responsabilité** : mapper les retours de revue vers des patches INTENT :
- "Relation SPEAKS manquante" → ajout Section 2
- "Contrats KG-L manquants" → ajout Section 5
- "Métriques KG-L manquantes" → ajout Section 10
- "Trajectory Replay manquant" → création S14

**Structure** :
- Frontmatter : type=skill, intent_hash, version, date, status
- Sections : Purpose, Input, Action, Verify, Ref

## Conséquences

- Transposition automatique des retours en patches
- Checklist des modifications générée
- Réutilise governance-architect (M1-M4 mapping)

## Référence

- **ADR** : ADR-2026-08-19-SKILL-REVIEW-TO-INTENT-MAPPER
- **IntentHash** : 0xADR_SKILL_REVIEW_TO_INTENT_MAPPER_20260819
- **Dépôt** : gerivdb/SKILLS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
