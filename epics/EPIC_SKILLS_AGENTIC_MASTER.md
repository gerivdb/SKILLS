# EPIC Maître — SKILLS_AGENTIC v2 : Architecture Agentic RAG pour le Métacluster gerivdb

**ID** : EPIC-SKILLS-AGENTIC-MASTER
**Version** : 2.0
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE
**Statut** : DRAFT v2
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md v2.0
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_MASTER_v2_20260606`
**Changelog v2** :
- Architecture : 7 → 9 agents (+ DELEGATOR, + REWRITER, + DRAFT/GAP dans COVERAGE)
- Phases : 4 → 5 (Phase 4 nouvelle : patterns Google manquants)
- Slots : 63 → 64/100
- Planning : 3 → 4 jours

---

## 1. Vision

Transformer le repo `gerivdb/SKILLS` d'un registre statique de 59 skills isolés en un **système agentique orchestré** capable de :
- **Évaluer** la complexité des requêtes et **délègue** conditionnellement (3 niveaux)
- **Décomposer** automatiquement les requêtes complexes en intents et les **reformuler** en sous-quêtes atomiques
- **Sélectionner** et activer les skills pertinents (mono ou multi-skill)
- **Router** chaque skill vers le bon repo parmi les 185 repos gerivdb
- **Vérifier** la couverture fonctionnelle avec **brouillon intermédiaire** et **feedback ciblé** sur les pièces manquantes
- **Itérer** si des skills manquants sont détectés
- **Synthétiser** les résultats en un livrable cohérent

**Inspiration** : Google Agentic RAG (5 juin 2026) — 6 patterns exploités (3 en v1, 3 en v2).

---

## 2. Objectifs Globaux

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Zéro skill manquant** | Le COVERAGE Agent détecte 100% des gaps sur 30 requêtes de test |
| **Feedback ciblé** | Le GAP ANALYZER génère un feedback avec skills recommandés pour 100% des gaps |
| **Orchestration adaptative** | Le DELEGATOR identifie correctement le niveau de complexité (3 niveaux) |
| **Reformulation** | Le REWRITER produit des sous-quêtes qui matchent des skills existants (100% match) |
| **Traçabilité complète** | Chaque activation de skill est loggée avec intent, repo, strate, résultat |
| **Conformité écosystème** | Respect strict L0→L9, BDCP inviolable, φ-CPS ≥ 4.559 pour les ADR |
| **Marge de slots** | ≤ 64 skills sur 100 (marge de 36 pour évolutions futures) |

---

## 3. Architecture v2 — Les 9 Agents

```
Requête → DELEGATOR (évalue complexité → niveau 1/2/3)
              │
              ▼ (niveau 2 ou 3)
          PARSER (décompose en intents)
              │
              ▼
          REWRITER (reformule en sous-quêtes atomiques)
              │
              ▼
          PLANNER (sélectionne les skills)
              │
              ▼
          ROUTER (mappe skill → repo cible)
              │
              ▼
          COVERAGE (vérifie couverture + DRAFT + GAP ANALYZER)
              │
              ▼ (si SUFFICIENT)
          FANOUT (exécute en parallèle)
              │
              ▼
          SYNTH (agrège les résultats)
              │
              ▼
          Réponse finale

          (si INSUFFICIENT → ITERATOR relance REWRITER + PLANNER avec feedback ciblé)
```

| Agent | Rôle | Skill dédié | Pattern Google |
|-------|------|-------------|----------------|
| 0. DELEGATOR | Évalue complexité → niveau 1/2/3 | skills-agentic.md | Orchestration conditionnelle |
| 1. PARSER | Décompose en intents | skills-agentic.md | — |
| 1b. REWRITER | Reformule en sous-quêtes | skills-rewriter.md | Query Rewriter |
| 2. PLANNER | Sélectionne les skills | skills-agentic.md | Planner Agent |
| 3. ROUTER | Mappe skill → repo | skills-router.md | Cross-Corpus Retrieval |
| 4. COVERAGE | Vérifie couverture + Draft + Gap | skills-coverage.md | Sufficient Context Agent |
| 5. FANOUT | Exécution parallèle | skills-agentic.md | Search Fanout |
| 6. SYNTH | Agrège les résultats | skills-agentic.md | Synthesis Agent |
| 7. ITERATOR | Relance si gaps | skills-agentic.md | Iteration loop |

---

## 4. Phases et Sous-EPICs

| Phase | EPIC | Livrables | Slots | Durée | Statut |
|-------|------|-----------|-------|-------|--------|
| **P1 — Création v1** | EPIC-SKILLS-AGENTIC-001 | skills-agentic.md, skills-coverage.md, skills-router.md | +3 | 1 jour | ✅ Fait |
| **P2 — Manifest + CI v1** | EPIC-SKILLS-AGENTIC-002 | MANIFEST.json v2, validate-skills.yml, outils | 0 | 0.5 jour | ✅ Fait |
| **P3 — Tests v1** | EPIC-SKILLS-AGENTIC-003 | skills-agentic-test.md, 20 requêtes | +1 | 1 jour | ✅ Fait |
| **P4 — Patterns v2** | EPIC-SKILLS-AGENTIC-004 | skills-rewriter.md, enrichir agentic/coverage/test | +1 | 1 jour | ⏳ À faire |
| **P5 — Revue v2** | EPIC-SKILLS-AGENTIC-005 | Rapport consolidé, correctifs, merge | 0 | 0.5 jour | ⏳ À faire |
| **Total** | | | **+5** | **4 jours** | |

---

## 5. Dépendances Inter-Phases

```
P1 (Création v1) ──▶ P2 (Manifest + CI)
      │                 │
      └────────▶ P3 (Tests v1) ──▶ P4 (Patterns v2) ──▶ P5 (Revue v2 + Merge)
```

- P2 dépend de P1
- P3 dépend de P1 + P2
- P4 dépend de P1 + P2 + P3 (base v1 existante)
- P5 dépend de P4

---

## 6. Contraintes

| Contrainte | Description |
|------------|-------------|
| **BDCP inviolable** | Aucun appel réseau sortant non autorisé |
| **Strates L0-L9** | Un skill L0 ne peut pas dépendre d'un skill L3+ |
| **φ-CPS** | Les ADR constitutionnelles doivent avoir φ-CPS ≥ 4.559 |
| **Plafond 100 slots** | Maximum 100 skills dans le registre |
| **Parallélisme** | Maximum 5 skills en parallèle |
| **Itération** | Maximum 3 itérations du pipeline, puis escalade HITL |
| **Délégation** | Niveau 1 = pas de pipeline, Niveau 2 = pipeline court, Niveau 3 = pipeline complet |

---

## 7. Risques Globaux

| Risque | Probabilité | Impact | Mitigation |
|--------|--------------|--------|------------|
| Explosion combinatoire | Moyenne | Haut | Limiter à 5 skills parallèles ; budget d'itérations max = 3 |
| Coverage Agent circulaire | Moyenne | Moyen | Jeu de test de 30 requêtes pour calibrer |
| Latence excessive | Moyenne | Haut | Délégation conditionnelle (niveau 1 = pas de pipeline) |
| Conflit de strate | Faible | Haut | Règle dure dans le ROUTER : respect strict L0→L9 |
| Dérive BDCP | Faible | Critique | Audit de chaque skill agentic par Alfred |
| REWRITER trop agressif | Moyen | Moyen | Limiter à 5 sous-quêtes par intent |

---

## 8. Critères d'Acceptation Globaux

1. **Toutes les phases complétées** : P1, P2, P3, P4, P5 mergés sur `main`
2. **Slot count** : 64 skills maximum (marge de 36)
3. **CI verte** : `validate-skills.yml` valide tous les skills agentic
4. **Tests passants** : 30/30 requêtes de test produisent les résultats attendus
5. **Revue croisée** : Les 4 agents ont validé l'architecture v2
6. **BDCP** : Aucun appel réseau sortant non autorisé
7. **Traçabilité** : Chaque activation de skill est loggée

---

## 9. Comparaison v1 vs v2

| Dimension | v1 | v2 |
|-----------|----|----|
| Agents | 7 | 9 |
| Slots | 63/100 | 64/100 |
| Orchestration | Linéaire | Conditionnelle (3 niveaux) |
| Reformulation | Non | Oui (REWRITER) |
| Brouillon | Non | Oui (DRAFT AGENT) |
| Feedback gaps | Générique | Ciblé (GAP ANALYZER) |
| Latence | Fixe (~15s) | Adaptée (2s-15s) |
| Tests | 20 requêtes | 30 requêtes |
| Phases | 4 | 5 |
| Durée | 3 jours | 4 jours |

---

## 10. Prochaines Étapes

1. ✅ Créer les EPICs v1 (P1, P2, P3)
2. ✅ Implémenter les Phases 1-3 (v1)
3. ✅ Créer les EPICs v2 (P4, P5)
4. ✅ Mettre à jour l'EPIC maître en v2
5. ✅ Mettre à jour le PRD en v2
6. ⏳ Implémenter Phase 4 (patterns v2)
7. ⏳ Implémenter Phase 5 (revue + merge)

---

*Fin de l'EPIC Maître v2 | IntentHash : `0xEPIC_SKILLS_AGENTIC_MASTER_v2_20260606`*
