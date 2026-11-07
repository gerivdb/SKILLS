---
type: ADR
status: proposed
date: "2026-08-19"
intent_hash: 0xADR_SKILL_INTENT_GENERATION_20260819
---

# ADR-2026-08-19-SKILL-INTENT-GENERATION -- Skill de génération d'INTENT

## Contexte

La génération d'INTENTs est entièrement manuelle : à chaque version (v0.9 → v1.0),
l'agent réécrit l'intégralité du document en transposant les retours de revue.
Aucun skill ne couvre ce workflow.

## Décision

Créer le skill `intent-generation` dans L4-TOOLS/SKILLS/skills/ :

**Responsabilité** : générer un INTENT complet depuis :
- Base INTENT existante
- Revue V10.0 (mathèmes M1-M5, items manquants)
- Alignements frameworks (DSH, TrueForge, Frontier, OpenBot)
- Version cible

**Structure** :
- Frontmatter : type=skill, intent_hash, version, date, status
- Sections : Purpose, Input, Action, Verify, Ref
- Réutilise : governance-architect, governance-doc-writer, prd-generation

**Livrable** : brouillon INTENT prêt pour validation frontmatter-guardian

## Conséquences

- Fin de la réécriture manuelle complète à chaque version
- Structure canonique garantie (27 sections + alignements)
- IntentHash généré par primitive intent-hash-gen

## Référence

- **ADR** : ADR-2026-08-19-SKILL-INTENT-GENERATION
- **IntentHash** : 0xADR_SKILL_INTENT_GENERATION_20260819
- **Dépôt** : gerivdb/SKILLS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
