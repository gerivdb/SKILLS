# EPIC Maître — SKILLS_AGENTIC : Architecture Agentic RAG pour le Métacluster gerivdb

**ID** : EPIC-SKILLS-AGENTIC-MASTER
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE
**Statut** : DRAFT
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_MASTER_20260606`

---

## 1. Vision

Transformer le repo `gerivdb/SKILLS` d'un registre statique de 59 skills isolés en un **système agentique orchestré** capable de :
- Décomposer automatiquement les requêtes complexes en intents
- Sélectionner et activer les skills pertinents (mono ou multi-skill)
- Router chaque skill vers le bon repo parmi les 185 repos gerivdb
- Vérifier la couverture fonctionnelle et itérer si des skills manquants sont détectés
- Synthétiser les résultats en un livrable cohérent

**Inspiration** : Google Agentic RAG (5 juin 2026) — adapté aux contraintes du métacluster gerivdb (BDCP, strates L0-L9, φ-CPS, 185 repos).

---

## 2. Objectifs Globaux

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Zéro skill manquant** | Le COVERAGE Agent détecte 100% des gaps sur 20 requêtes de test |
| **Orchestration automatique** | Toute requête multi-intents (≥3) déclenche les skills pertinents sans intervention |
| **Traçabilité complète** | Chaque activation de skill est loggée avec intent, repo, strate, résultat |
| **Conformité écosystème** | Respect strict L0→L9, BDCP inviolable, φ-CPS ≥ 4.559 pour les ADR |
| **Marge de slots** | ≤ 63 skills sur 100 (marge de 37 pour évolutions futures) |

---

## 3. Architecture des 7 Agents

```
Requête → PARSER → PLANNER → ROUTER → COVERAGE → FANOUT → SYNTH → Réponse
                                      ↓
                                   ITERATOR (si INSUFFICIENT)
```

| Agent | Rôle | Skill dédié |
|-------|------|-------------|
| PARSER | Décompose la requête en intents | skills-agentic.md |
| PLANNER | Sélectionne les skills nécessaires | skills-agentic.md |
| ROUTER | Mappe skill → repo cible (L0-L9) | skills-router.md |
| COVERAGE | Vérifie la couverture fonctionnelle | skills-coverage.md |
| FANOUT | Exécute les skills en parallèle | skills-agentic.md |
| SYNTH | Agrège les résultats | skills-agentic.md |
| ITERATOR | Relance si gaps détectés | skills-agentic.md |

---

## 4. Phases et Sous-EPICs

| Phase | EPIC | Livrables | Slots | Durée |
|-------|------|-----------|-------|-------|
| **P1 — Création** | EPIC-SKILLS-AGENTIC-001 | skills-agentic.md, skills-coverage.md, skills-router.md | +3 | 1 jour |
| **P2 — Manifest + CI** | EPIC-SKILLS-AGENTIC-002 | MANIFEST.json v2, registry-sync.yml v2, dashboard | 0 | 0.5 jour |
| **P3 — Tests** | EPIC-SKILLS-AGENTIC-003 | skills-agentic-test.md, 20 requêtes, matrice | +1 | 1 jour |
| **P4 — Revue** | EPIC-SKILLS-AGENTIC-004 | Rapport consolidé, correctifs, merge | 0 | 0.5 jour |
| **Total** | | | **+4** | **3 jours** |

---

## 5. Dépendances Inter-Phases

```
P1 (Création) ──▶ P2 (Manifest + CI)
      │                 │
      └────────▶ P3 (Tests) ──▶ P4 (Revue + Merge)
```

- P2 dépend de P1 (les skills doivent exister pour être dans le manifest)
- P3 dépend de P1 + P2 (les skills doivent être créés et enregistrés)
- P4 dépend de P1 + P2 + P3 (tout doit être testé avant la revue)

---

## 6. Contraintes

| Contrainte | Description |
|------------|-------------|
| **BDCP inviolable** | Aucun appel réseau sortant non autorisé dans les skills agentic |
| **Strates L0-L9** | Un skill L0 ne peut pas dépendre d'un skill L3+ |
| **φ-CPS** | Les ADR constitutionnelles doivent avoir φ-CPS ≥ 4.559 |
| **Plafond 100 slots** | Maximum 100 skills dans le registre Perplexité |
| **Parallélisme** | Maximum 5 skills en parallèle (contrainte SLM) |
| **Itération** | Maximum 3 itérations du pipeline, puis escalade HITL |

---

## 7. Risques Globaux

| Risque | Probabilité | Impact | Mitigation |
|--------|--------------|--------|------------|
| Explosion combinatoire | Moyenne | Haut | Limiter à 5 skills parallèles ; budget d'itérations max = 3 |
| Coverage Agent circulaire | Moyenne | Moyen | Jeu de test de 20 requêtes pour calibrer |
| Latence excessive | Haute | Haut | Modèles légers pour les agents simples ; cache des plans |
| Conflit de strate | Faible | Haut | Règle dure dans le ROUTER : respect strict L0→L9 |
| Dérive BDCP | Faible | Critique | Audit de chaque skill agentic par Alfred |

---

## 8. Critères d'Acceptation Globaux

1. **Tous les sous-EPICs complétés** : P1, P2, P3, P4 mergés sur `main`
2. **Slot count** : 63 skills maximum (marge de 37)
3. **CI verte** : `registry-sync.yml` valide tous les skills agentic
4. **Tests passants** : 20/20 requêtes de test produisent les résultats attendus
5. **Revue croisée** : Les 4 agents (SCO7, Selena, Alfred, Riddler) ont validé l'architecture
6. **BDCP** : Aucun appel réseau sortant non autorisé
7. **Traçabilité** : Chaque activation de skill est loggée

---

## 9. Prochaines Étapes

1. ✅ Créer les 4 EPICs de phase (P1, P2, P3, P4)
2. ⏳ Revue croisée SCO7 + Selena + Alfred + Riddler du PRD et des EPICs
3. ⏳ Implémentation Phase 1 (création des 3 skills agentic)
4. ⏳ Implémentation Phase 2 (manifest v2 + CI)
5. ⏳ Implémentation Phase 3 (tests)
6. ⏳ Implémentation Phase 4 (revue + merge)

---

*Fin de l'EPIC Maître | IntentHash : `0xEPIC_SKILLS_AGENTIC_MASTER_20260606`*
