# EPIC — SKILLS_AGENTIC v2 Phase 4 : Patterns Google Manquants

**ID** : EPIC-SKILLS-AGENTIC-004
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE
**Statut** : DRAFT — dépend de EPIC-SKILLS-AGENTIC-001/002/003 (v1)
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md v2.0
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_P4_V2_20260606`

---

## 1. Vision

Implémenter les **3 patterns Google** identifiés comme manquants dans la v1 du pipeline SKILLS_AGENTIC. La v1 a posé les fondations (7 agents, 63 skills) mais n'a pas exploité tout le potentiel de l'article Google Agentic RAG. La v2 complète avec :

1. **DELEGATOR Agent** — orchestration conditionnelle (3 niveaux de complexité)
2. **REWRITER Agent** — reformulation des intents en sous-quêtes atomiques
3. **DRAFT + GAP ANALYZER** — brouillon intermédiaire + feedback ciblé sur les pièces manquantes

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Créer `skills-rewriter.md`** | Reformule chaque intent en sous-quêtes atomiques optimisées pour le retrieval MANIFEST |
| **Enrichir `skills-agentic.md`** | Ajouter DELEGATOR (Agent 0) + orchestration conditionnelle (3 niveaux) |
| **Enrichir `skills-coverage.md`** | Ajouter DRAFT AGENT (4b) + GAP ANALYZER (4c) |
| **Enrichir `skills-agentic-test.md`** | Ajouter 10 requêtes de test v2 (délégation, reformulation, brouillon) |
| **Enrichir `validate-agentic.py`** | Valider les nouveaux champs v2 (draft_quality, gap_feedback, delegation_level) |

---

## 3. Périmètre

### Inclus
- `perplexity/skills/skills-rewriter.md` — nouveau skill REWRITER
- `perplexity/skills/skills-agentic.md` — enrichi avec DELEGATOR + orchestration conditionnelle
- `perplexity/skills/skills-coverage.md` — enrichi avec DRAFT AGENT + GAP ANALYZER
- `perplexity/skills/skills-agentic-test.md` — enrichi avec 10 requêtes v2
- `tools/validate-agentic.py` — enrichi avec validation v2

### Exclus
- Création de nouveaux skills v1 (Phase 1-3 déjà fait)
- Refactoring des 59 skills existants
- Revue croisée (Phase 5)

---

## 4. Livrables

| ID | Fichier | Description | Slots |
|----|---------|-------------|-------|
| L4.1 | `perplexity/skills/skills-rewriter.md` | REWRITER — reformulation intents → sous-quêtes | +1 |
| L4.2 | `perplexity/skills/skills-agentic.md` (v2) | + DELEGATOR + orchestration conditionnelle | 0 |
| L4.3 | `perplexity/skills/skills-coverage.md` (v2) | + DRAFT AGENT + GAP ANALYZER | 0 |
| L4.4 | `perplexity/skills/skills-agentic-test.md` (v2) | +10 requêtes de test v2 | 0 |
| L4.5 | `tools/validate-agentic.py` (v2) | + validation Draft + Gap + Delegation | 0 |

**Impact total** : +1 slot (de 63 → 64)

---

## 5. Critères d'acceptation

1. **DELEGATOR** : Identifie correctement le niveau de complexité sur 10 requêtes test (5 simples → niveau 1, 3 moyennes → niveau 2, 2 complexes → niveau 3)
2. **REWRITER** : Produit des sous-quêtes qui matchent des skills existants dans le MANIFEST (100% de match sur 10 intents test)
3. **DRAFT AGENT** : Produit un brouillon structuré pour toute requête de niveau 2+
4. **GAP ANALYZER** : Génère un feedback avec skills recommandés pour 100% des gaps injectés
5. **Latence adaptée** : Niveau 1 < 2s, Niveau 2 < 8s, Niveau 3 < 15s
6. **Format** : Le nouveau skill passe le lint YAML
7. **BDCP** : Aucun appel réseau sortant non autorisé

---

## 6. Dépendances

| Dépendance | Type | Statut |
|------------|------|--------|
| EPIC-SKILLS-AGENTIC-001 (Phase 1) | Précédence | ✅ Fait |
| EPIC-SKILLS-AGENTIC-002 (Phase 2) | Précédence | ✅ Fait |
| EPIC-SKILLS-AGENTIC-003 (Phase 3) | Précédence | ✅ Fait |
| MANIFEST.json v2 | Base à enrichir | ✅ Existant |
| 63 skills existants | Contexte de test | ✅ Existants |

---

## 7. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Créer `skills-rewriter.md` | 2h |
| Enrichir `skills-agentic.md` (DELEGATOR) | 1.5h |
| Enrichir `skills-coverage.md` (Draft + Gap) | 2h |
| Enrichir `skills-agentic-test.md` (+10 requêtes) | 1h |
| Enrichir `validate-agentic.py` | 1h |
| Tests manuels | 0.5h |
| **Total** | **8h (1 jour)** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_AGENTIC_P4_V2_20260606`*
