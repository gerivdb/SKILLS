---
type: ADR
status: proposed
date: "2026-08-19"
intent_hash: 0xADR_SKILL_INTENT_VERSION_BUMPER_20260819
---

# ADR-2026-08-19-SKILL-INTENT-VERSION-BUMPER -- Skill de versioning d'INTENT

## Contexte

Le passage v0.9 → v1.0 d'un INTENT nécessite :
- Renumérotation de toutes les sections
- Mise à jour de l'IntentHash
- Update du titre, résumé, conclusion
- Insertion de nouvelles sections
Ce processus est entièrement manuel et source d'erreurs.

## Décision

Créer le skill `intent-version-bumper` dans L4-TOOLS/SKILLS/skills/ :

**Responsabilité** : bumper un INTENT existant vers une nouvelle version :
- Update frontmatter : intent_hash, version
- Renumérotation automatique des sections
- Insertion de nouvelles sections à la position correcte
- Mise à jour des références internes
- Validation frontmatter-guardian

**Structure** :
- Frontmatter : type=skill, intent_hash, version, date, status
- Sections : Purpose, Input, Action, Verify, Ref

## Conséquences

- Versioning d'INTENT en 1 appel au lieu de N éditions manuelles
- Cohérence garantie entre numéros de sections
- Pas de perte de contenu lors des upgrades

## Référence

- **ADR** : ADR-2026-08-19-SKILL-INTENT-VERSION-BUMPER
- **IntentHash** : 0xADR_SKILL_INTENT_VERSION_BUMPER_20260819
- **Dépôt** : gerivdb/SKILLS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
