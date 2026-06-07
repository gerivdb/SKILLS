# EPIC — SKILLS UAE-KEEL Phase 1 : coords.yaml

**ID** : EPIC-SKILLS-UAE-KEEL-001
**Date de création** : 2026-06-07
**Auteur** : OPS-ENGINE
**Statut** : DRAFT
**Lié au PRD** : PRD_SKILLS_UAE_KEEL_METAMORPHIC_V1.md
**IntentHash** : `0xEPIC_SKILLS_UAE_KEEL_P1_20260607`

---

## 1. Vision

Générer le fichier `TAXONOMY/coords.yaml` qui attribue à chacun des 64 skills ses **5 coordonnées UAE** (strate, domaine, env, phase, urgence) plus le score UAE et la zone LADYBIRD.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Créer `TAXONOMY/coords.yaml`** | 64 skills avec 5 coordonnées UAE chacune |
| **Score UAE calculé** | `1/√d` depuis le centre du plateau pour chaque skill |
| **Zone LADYBIRD** | ≥ 80 = LADYBIRD, 60-79 = STANDARD, < 60 = BASIC |
| **Validation** | `validate_coords.py --strict` → 0 erreur |

---

## 3. Format UAE (5 axes)

| Axe | Valeurs possibles | Description |
|-----|-------------------|-------------|
| strate | L0, L1, L2, L3, L4 | Strate écosystème |
| domaine | governance, sot, cognition, automation, git, agentic, domain, external | Domaine fonctionnel |
| env | ENV1, ENV2, BOTH | Environnement cible |
| phase | create, audit, fix, close, route | Phase du cycle de vie |
| urgence | P0, P1, P2, P3 | Priorité opérationnelle |

---

## 4. Critères d'acceptation

1. Les 64 skills ont tous 5 coordonnées UAE valides
2. Le score UAE est calculé pour chaque skill
3. La zone LADYBIRD est attribuée
4. Le fichier passe la validation YAML
5. Aucun skill n'est manquant

---

## 5. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Analyser les 64 skills du MANIFEST | 1h |
| Attribuer les coordonnées UAE | 2h |
| Calculer les scores UAE | 0.5h |
| Écrire coords.yaml | 0.5h |
| **Total** | **4h** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_UAE_KEEL_P1_20260607`*
