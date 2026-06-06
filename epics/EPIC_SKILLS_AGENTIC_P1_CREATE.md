# EPIC — SKILLS_AGENTIC Phase 1 : Création des Skills Agentic

**ID** : EPIC-SKILLS-AGENTIC-001
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE (inspiré de l'analyse Google Agentic RAG)
**Statut** : DRAFT — soumis à revue SCO7 + Selena + Alfred + Riddler
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_P1_20260606`

---

## 1. Vision

Créer les 3 skills agentic fondamentaux qui constituent le cœur du pipeline SKILLS_AGENTIC : l'orchestrateur principal, le vérificateur de couverture (équivalent du Sufficient Context Agent de Google), et le routeur cross-repo. Ces skills posent les fondations de l'orchestration agentique au-dessus des 59 skills existants.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Créer `skills-agentic.md`** | Skill principal orchestrant le pipeline 7 agents (PARSER → PLANNER → ROUTER → COVERAGE → FANOUT → SYNTH → ITERATOR) |
| **Créer `skills-coverage.md`** | Skill dédié à la vérification de couverture fonctionnelle — détecte les gaps de skills et génère le feedback d'itération |
| **Créer `skills-router.md`** | Skill de routing cross-repo utilisant `known_repositories.yaml` — mappe chaque skill vers le(s) repo(s) cible(s) avec contrainte L0→L9 |
| **Respecter le format canonique** | Frontmatter YAML complet (name, version, description, triggers, layer, nexusTags, prerequisites, slotWeight, status, changelog) |
| **Conformité BDCP** | Aucun appel réseau sortant non autorisé dans les skills créés |

---

## 3. Périmètre

### Inclus
- `perplexity/skills/skills-agentic.md` — orchestrateur principal
- `perplexity/skills/skills-coverage.md` — vérificateur de couverture
- `perplexity/skills/skills-router.md` — routeur cross-repo
- Mise à jour du `MANIFEST.json` pour inclure les 3 nouveaux skills

### Exclus
- Modification des 59 skills existants (pas de refactoring dans cette phase)
- CI/CD (Phase 2)
- Tests (Phase 3)
- Intégration avec les agents SCO7/Selena/Alfred/Riddler (Phase 4)

---

## 4. Livrables

| ID | Fichier | Description | Slots |
|----|---------|-------------|-------|
| L1.1 | `perplexity/skills/skills-agentic.md` | Skill principal — pipeline 7 agents | +1 |
| L1.2 | `perplexity/skills/skills-coverage.md` | Skill COVERAGE — vérification de couverture fonctionnelle | +1 |
| L1.3 | `perplexity/skills/skills-router.md` | Skill ROUTER — mapping skill→repo via known_repositories.yaml | +1 |
| L1.4 | `MANIFEST.json` (mise à jour) | Enregistrement des 3 nouveaux skills | 0 |

**Impact total** : +3 slots (de 59 → 62)

---

## 5. Critères d'acceptation

1. **Format** : Les 3 skills passent le lint YAML de `validate-skills.yml`
2. **Frontmatter** : Chaque skill contient tous les champs obligatoires (name, version, description, triggers, layer, nexusTags, prerequisites, slotWeight, status, changelog)
3. **Triggers** : Chaque skill se déclenche sur au moins 3 mots-clés pertinents
4. **Couverture** : Le `skills-coverage.md` documente les 4 critères de couverture (exhaustivité, compétence, strate, dépendance)
5. **Routing** : Le `skills-router.md` référence `known_repositories.yaml` comme source de vérité et documente la contrainte L0→L9
6. **BDCP** : Aucun appel réseau sortant non autorisé dans les 3 skills
7. **Manifest** : Le `MANIFEST.json` est à jour avec les 3 nouveaux skills

---

## 6. Dépendances

| Dépendance | Type | Statut |
|------------|------|--------|
| `known_repositories.yaml` (GOVERNANCE-HUB) | Source de vérité pour le routing | ✅ Existant |
| `MANIFEST.json` v1 | Base à enrichir | ✅ Existant |
| 59 skills existants | Contexte de couverture | ✅ Existants |
| Format canonique (`SKILL_FORMAT_CANONICAL.md`) | Contrainte de format | ✅ Existant |

---

## 7. Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|--------------|--------|------------|
| **Scope creep** (ajouter trop de logique dans les skills) | Moyenne | Haut | Limiter chaque skill à son périmètre strict |
| **Conflit de triggers** avec les skills existants | Faible | Moyen | Vérifier les triggers existants avant de définir les nouveaux |
| **Dépassement du plafond 100 slots** | Faible | Haut | Impact de +3 slots seulement (62/100) |

---

## 8. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Créer `skills-agentic.md` | 2h |
| Créer `skills-coverage.md` | 2h |
| Créer `skills-router.md` | 2h |
| Mettre à jour `MANIFEST.json` | 0.5h |
| Revue croisée SCO7+Selena+Alfred+Riddler | 1h |
| **Total** | **7.5h (1 jour)** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_AGENTIC_P1_20260606`*
