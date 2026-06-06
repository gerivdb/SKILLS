# EPIC — SKILLS_AGENTIC v2 Phase 5 : Revue Croisée et Merge

**ID** : EPIC-SKILLS-AGENTIC-005
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE
**Statut** : DRAFT — dépend de EPIC-SKILLS-AGENTIC-004
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md v2.0
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_P5_V2_20260606`

---

## 1. Vision

Soumettre l'ensemble du travail v2 (Phase 4) à une revue croisée par les 4 agents analytiques (SCO7, Selena, Alfred, Riddler) et consolider les retours en un rapport final. Cette phase garantit que l'architecture SKILLS_AGENTIC v2 est validée sous tous les angles avant le merge sur `main`.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Revue technique SCO7** | Valider l'architecture v2 (9 agents), la scalabilité, et les choix d'implémentation |
| **Revue stratégique Selena** | Évaluer l'impact v2 sur le métacluster gerivdb et le positionnement vs Google |
| **Revue risques Alfred** | Auditer les vulnérabilités du pipeline v2 (BDCP, conformité, surface d'attaque) |
| **Revue critique Riddler** | Identifier les failles logiques, les biais, et les hypothèses cachées de la v2 |
| **Rapport consolidé** | Synthèse des 4 revues avec plan d'action pour les correctifs |
| **Merge sur `main`** | Tous les livrables v2 mergés après résolution des findings |

---

## 3. Périmètre

### Inclus
- Revue croisée SCO7 + Selena + Alfred + Riddler
- Rapport consolidé dans `REPORTS/SKILLS_AGENTIC_V2_REVIEW_20260606.md`
- Correctifs issus des revues
- Merge final sur `main`

### Exclus
- Nouvelles fonctionnalités (hors correctifs)
- Refactoring des 59 skills existants
- Déploiement en production Perplexity

---

## 4. Livrables

| ID | Fichier | Description | Slots |
|----|---------|-------------|-------|
| L5.1 | `REPORTS/SKILLS_AGENTIC_V2_REVIEW_20260606.md` | Rapport consolidé des 4 revues v2 | 0 |
| L5.2 | Correctifs (si nécessaire) | Modifications des skills/agentic suite aux retours | 0 |
| L5.3 | Merge PR | Tous les livrables v2 mergés sur `main` | 0 |

**Impact total** : 0 slot

---

## 5. Critères d'acceptation

1. **4 revues complétées** : SCO7, Selena, Alfred, Riddler ont chacun produit leur rapport v2
2. **Rapport consolidé** : Synthèse des findings avec matrice de convergence
3. **Findings résolus** : Tous les findings P0 et P1 sont corrigés ou documentés avec justification
4. **CI verte** : `validate-skills.yml` passe sur tous les skills après correctifs
5. **Slot count** : Le nombre total de skills reste ≤ 100 (cible : 64)
6. **BDCP** : Aucun appel réseau sortant non autorisé dans les skills finaux
7. **Merge** : Tous les livrables v2 mergés sur `main` avec commit conventionnel

---

## 6. Dépendances

| Dépendance | Type | Statut |
|------------|------|--------|
| EPIC-SKILLS-AGENTIC-004 (Phase 4) | Précédence | ⏳ En attente |
| EPIC-SKILLS-AGENTIC-001/002/003 (v1) | Base existante | ✅ Fait |
| Agents SCO7, Selena, Alfred, Riddler | Ressources de revue | ✅ Disponibles |

---

## 7. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Revue SCO7 (technique) | 1h |
| Revue Selena (stratégique) | 1h |
| Revue Alfred (risques) | 1h |
| Revue Riddler (critique) | 1h |
| Consolidation du rapport | 1h |
| Correctifs (si nécessaire) | 1h |
| Merge sur `main` | 0.5h |
| **Total** | **6.5h (0.5 jour)** |

---

## 8. Matrice de Convergence (à remplir après les revues)

| Dimension | SCO7 | Selena | Alfred | Riddler | Consensus |
|-----------|------|--------|--------|---------|-----------|
| Architecture v2 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Scalabilité | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Sécurité | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Cohérence écosystème | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Recommandation finale | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_AGENTIC_P5_V2_20260606`*
