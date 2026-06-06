# PRD — SKILLS_AGENTIC : Architecture Agentic RAG pour le Métacluster gerivdb

**Version** : 2.0
**Date** : 2026-06-06
**Auteur** : OPS-ENGINE (inspiré de l'analyse Google Agentic RAG, adapté au métacluster gerivdb)
**Statut** : DRAFT v2 — intégration des 3 patterns Google manquants
**IntentHash** : `0xSKILLS_AGENTIC_RAG_v2_20260606`
**Changelog v2** :
- Ajout Agent 0 — DELEGATOR (délégation conditionnelle)
- Ajout Agent 1b — REWRITER (reformulation des intents)
- Enrichissement Agent 4 — COVERAGE avec Draft + Gap Analyzer
- Mise à jour architecture : 9 agents (vs 7 en v1)
- Mise à jour livrables : +1 slot (skills-rewriter.md)
- Mise à jour planning : 4 phases (vs 3 en v1)

---

## 1. Contexte et Motivation

### 1.1 Le problème actuel

Le repo `gerivdb/SKILLS` contient **63 skills** spécialisés couvrant les strates L0-L9 du métacluster gerivdb (185 repos). La v1 du pipeline SKILLS_AGENTIC a posé les fondations (7 agents) mais **3 patterns Google** n'ont pas été exploités :

1. **Query Rewriter** — les intents ne sont pas reformulés en sous-quêtes atomiques optimisées
2. **Intermediate Draft + Missing Pieces** — le COVERAGE Agent ne produit pas de brouillon intermédiaire ni de feedback ciblé
3. **Orchestration conditionnelle** — le pipeline est toujours linéaire, même pour les requêtes simples

### 1.2 L'inspiration : Google Agentic RAG (relecture)

L'article Google Research (5 juin 2026) contient **6 patterns** exploitables. La v1 en a implémenté 3. La v2 complète avec les 3 restants :

| # | Pattern Google | v1 | v2 | Adaptation gerivdb |
|---|----------------|----|----|--------------------|
| 1 | Sufficient Context Agent | ✅ | ✅ Enrichi | COVERAGE Agent + Draft + Gap Analyzer |
| 2 | Cross-Corpus Retrieval | ✅ | ✅ | ROUTER Agent (185 repos) |
| 3 | Search Fanout + Iteration | ✅ | ✅ | FANOUT + ITERATOR |
| 4 | Query Rewriter | ❌ | ✅ Nouveau | REWRITER Agent — reformule les intents |
| 5 | Intermediate Draft + Missing Pieces | ❌ | ✅ Nouveau | Draft Agent + Gap Analyzer dans COVERAGE |
| 6 | Orchestrator conditionnel | ❌ | ✅ Nouveau | DELEGATOR Agent — activation sélective |

### 1.3 Différence fondamentale

| Dimension | Google Agentic RAG | SKILLS_AGENTIC v2 (gerivdb) |
|-----------|---------------------|---------------------------|
| **Objet du retrieval** | Documents (PDFs, DB) | Skills (capacités) |
| **Corpus** | 2 676 PDFs statiques | 63 skills dynamiques + 185 repos |
| **Critère de suffisance** | Contexte informationnel complet | Couverture fonctionnelle complète + brouillon validé |
| **Routing** | Cross-corpus (4 datasets) | Cross-repo (185 repos, strates L0-L9) |
| **Itération** | Recherche de données manquantes | Activation de skills manquants |
| **Orchestration** | Linéaire | Conditionnelle (3 niveaux) |
| **Contrainte unique** | Latence < 12s | Conformité BDCP, φ-CPS, strates L |

---

## 2. Objectif

Concevoir et implémenter **SKILLS_AGENTIC v2**, une couche d'orchestration agentique complète au-dessus des 63 skills, qui :

1. **Évalue** la complexité de la requête et **délègue** conditionnellement (DELEGATOR)
2. **Analyse** la requête et **reformule** les intents en sous-quêtes atomiques (PARSER + REWRITER)
3. **Sélectionne** les skills pertinents (PLANNER)
4. **Route** chaque skill vers le(s) repo(s) cible(s) (ROUTER)
5. **Vérifie** la couverture fonctionnelle avec **brouillon intermédiaire** et **analyse des pièces manquantes** (COVERAGE enrichi)
6. **Exécute** les skills en parallèle (FANOUT)
7. **Agrège** les résultats (SYNTH)
8. **Itère** si des gaps sont détectés (ITERATOR)

Le résultat visé : **zéro skill manquant** + **feedback ciblé** sur les pièces manquantes + **latence adaptée** à la complexité.

---

## 3. Architecture v2 — Les 9 Agents

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SKILLS_AGENTIC v2 — Pipeline                              │
│                                                                              │
│  Requête utilisateur                                                         │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────────┐                                                         │
│  │ 0. DELEGATOR    │  Évalue la complexité → choisit le niveau d'activation │
│  │ Agent           │                                                         │
│  │                 │  Niveau 1 (simple)  → skill direct                     │
│  │                 │  Niveau 2 (moyen)   → pipeline court (4 agents)         │
│  │                 │  Niveau 3 (complexe) → pipeline complet (9 agents)      │
│  └────────┬────────┘                                                         │
│           │                                                                  │
│           ▼ (Niveau 2 ou 3)                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ 1. PARSER   │───▶│ 1b. REWRITER│───▶│ 2. PLANNER  │                      │
│  │ Agent       │    │ Agent       │    │ Agent       │                      │
│  │             │    │             │    │             │                      │
│  │ Décompose   │    │ Reformule   │    │ Sélectionne │                      │
│  │ en intents  │    │ en sous-    │    │ les skills  │                      │
│  │             │    │ quêtes      │    │ nécessaires │                      │
│  └─────────────┘    └─────────────┘    └──────┬──────┘                      │
│                                               │                              │
│                                               ▼                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ 6. SYNTH    │◀───│ 5. FANOUT   │◀───│ 3. ROUTER   │                      │
│  │ Agent       │    │ Agent       │    │ Agent       │                      │
│  │             │    │             │    │             │                      │
│  │ Agrège les  │    │ Exécute les │    │ Mappe skill │                      │
│  │ résultats   │    │ skills en   │    │ → repo cible│                      │
│  │             │    │ parallèle   │    │ (L0-L9)     │                      │
│  └─────────────┘    └─────────────┘    └──────┬──────┘                      │
│       ▲                                       │                              │
│       │         ┌─────────────────────────────┘                              │
│       │         │                                                             │
│       │         ▼                                                             │
│       │  ┌─────────────────────────────────────────────┐                     │
│       │  │ 4. COVERAGE Agent (enrichi v2)              │                     │
│       │  │                                             │                     │
│       │  │  4a. Coverage Checker (4 critères)          │                     │
│       │  │  4b. Draft Agent (brouillon intermédiaire)  │                     │
│       │  │  4c. Gap Analyzer (analyse pièces manquantes)│                    │
│       │  │                                             │                     │
│       │  │  Sortie : verdict + brouillon + feedback     │                     │
│       │  │         ciblé                                │                     │
│       │  └──────────────────┬──────────────────────────┘                     │
│       │                     │                                                │
│       │                     ▼ (si INSUFFICIENT)                              │
│       │  ┌─────────────┐                                                    │
│       │  │ 7. ITERATOR │───▶ Relance REWRITER + PLANNER avec feedback       │
│       │  │ Agent       │     ciblé du Gap Analyzer                           │
│       │  └─────────────┘                                                    │
│       │                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Matrice de Délégation (DELEGATOR)

| Complexe | Critères | Niveau | Agents activés | Latence cible |
|----------|----------|--------|----------------|---------------|
| **Simple** | 1 intent, 1 strate, 1 skill | 1 | Skill direct | < 2s |
| **Moyen** | 2-3 intents, 1-2 strates | 2 | PARSER → REWRITER → PLANNER → ROUTER → FANOUT → SYNTH | < 8s |
| **Complexe** | 4+ intents, cross-strate, ou requête ambiguë | 3 | Pipeline complet (9 agents) | < 15s |

### 3.2 Description des Nouveaux Agents (v2)

#### Agent 0 — DELEGATOR (nouveau)
**Rôle** : Évaluer la complexité de la requête et décider du niveau d'activation.

**Entrée** : Requête utilisateur
**Sortie** : Niveau de complexité (1, 2, ou 3) + justification

**Critères d'évaluation** :
1. **Nombre d'intents** : 1 → niveau 1 ; 2-3 → niveau 2 ; 4+ → niveau 3
2. **Nombre de strates** : 1 → niveau 1-2 ; 2+ → niveau 3
3. **Ambiguïté** : requête vague → niveau 3 (nécessite REWRITER)
4. **Mots-clés de complexité** : "complet", "global", "cross-repo" → niveau 3

**Règles** :
- Niveau 1 : activer directement le skill identifié (pas de pipeline)
- Niveau 2 : pipeline court (pas de DELEGATOR, pas de ITERATOR)
- Niveau 3 : pipeline complet avec itération

#### Agent 1b — REWRITER (nouveau)
**Rôle** : Reformuler chaque intent en sous-quêtes atomiques optimisées pour le retrieval dans le MANIFEST.

**Entrée** : Liste d'intents (du PARSER)
**Sortie** : Liste de sous-quêtes enrichies

**Exemple** :
```
Intent : audit_structure (FLUENCE)
Sous-quêtes :
  - scan_repo_structure (reposcope-run)
  - check_ddd_compliance (nexus-auditor)
  - detect_epic_size_violations (nexus-auditor)
  - validate_naming_conventions (nexus-compliance)
```

**Règles** :
1. Chaque sous-quête doit correspondre à un skill existant dans le MANIFEST
2. Maximum 5 sous-quêtes par intent (au-delà → découper en sous-intents)
3. Les sous-quêtes doivent être **recherchables** dans les `triggers` ou `description` des skills
4. Conserver le mapping intent → sous-quêtes pour la traçabilité

#### Agent 4b — DRAFT AGENT (nouveau, dans COVERAGE)
**Rôle** : Produire un brouillon de réponse basé sur les skills activés, avant l'exécution réelle.

**Entrée** : Plan routé (skills + repos + intents)
**Sortie** : Brouillon de réponse structuré

**Format** :
```markdown
## Brouillon — [Titre]

### Couverture
- Skills activés : [liste]
- Intents couverts : [liste]
- Intents non couverts : [liste]

### Résultats attendus
#### [skill-1] — [intent]
- Résultat attendu : [description]
- Source : [repo]

#### [skill-2] — [intent]
...

### Lacunes identifiées
[Liste des intents sans skill assigné]
```

#### Agent 4c — GAP ANALYZER (nouveau, dans COVERAGE)
**Rôle** : Comparer le brouillon à la requête originale et générer un feedback ciblé sur les pièces manquantes.

**Entrée** : Brouillon (Draft Agent) + Requête originale
**Sortie** : Feedback structuré avec pièces manquantes et skills recommandés

**Format** :
```json
{
  "coverage_verdict": "INSUFFICIENT",
  "draft_summary": "Le brouillon couvre l'audit structurel et la conformité NEXUS",
  "missing_pieces": [
    {
      "intent": "generer_rapport",
      "reason": "Aucun skill de génération de rapport n'est activé",
      "recommended_skills": ["workflow-orchestration", "prd-factory"],
      "priority": "HIGH"
    }
  ],
  "targeted_feedback": "Le skill reposcope-run couvre l'audit structurel, mais il manque un skill pour générer le rapport final. Ajouter workflow-orchestration (L4) ou prd-factory (L2)."
}
```

### 3.3 Agents v1 (inchangés mais enrichis)

| Agent | v1 | v2 | Changement |
|-------|----|----|------------|
| PARSER | Décompose en intents | Décompose en intents | Enrichi : passe les intents au REWRITER |
| PLANNER | Sélectionne les skills | Sélectionne les skills | Enrichi : utilise les sous-quêtes du REWRITER |
| ROUTER | Mappe skill→repo | Mappe skill→repo | Inchangé |
| COVERAGE | 4 critères | 4 critères + Draft + Gap Analyzer | **Enrichi** |
| FANOUT | Exécution parallèle | Exécution parallèle | Inchangé |
| SYNTH | Agrège les résultats | Agrège les résultats | Inchangé |
| ITERATOR | Relance si gaps | Relance avec feedback ciblé | Enrichi : utilise le feedback du Gap Analyzer |

---

## 4. Livrables v2

| ID | Livrable | Description | Impact | Statut |
|----|----------|-------------|--------|--------|
| **L1** | `skills-agentic.md` | Orchestrateur principal — pipeline 9 agents (v2) | +1 slot | ✅ Créé v1, à enrichir v2 |
| **L2** | `skills-coverage.md` | Vérification de couverture + Draft + Gap Analyzer | +1 slot | ✅ Créé v1, à enrichir v2 |
| **L3** | `skills-router.md` | Routing cross-repo via known_repositories.yaml | +1 slot | ✅ Créé v1 |
| **L4** | `skills-rewriter.md` | **NOUVEAU** — Reformulation des intents en sous-quêtes | +1 slot | ❌ À créer |
| **L5** | `MANIFEST.json` v2 | Manifest enrichi avec métadonnées agentic | 0 slot | ✅ Créé v1 |
| **L6** | `skills-agentic-test.md` | Suite de tests — 20 requêtes + tests v2 | +1 slot | ✅ Créé v1, à enrichir v2 |
| **L7** | `validate-skills.yml` v2 | CI avec validation agentic v2 | 0 slot | ✅ Créé v1, à enrichir v2 |
| **L8** | `validate-agentic.py` v2 | Validation agentic avec Draft + Gap Analyzer | 0 slot | ✅ Créé v1, à enrichir v2 |

**Impact slots v2** : +5 slots (de 59 → 64, marge de 36 slots restants sur 100)

---

## 5. Critères d'acceptation v2

### Critères v1 (conservés)
1. **Couverture** : Toute requête multi-intents (≥3) déclenche automatiquement les skills pertinents
2. **Suffisance** : Le COVERAGE Agent détecte 100% des gaps sur 20 requêtes
3. **Traçabilité** : Chaque activation de skill est loggée
4. **Itération** : Convergence en ≤3 itérations
5. **Conformité** : Aucun skill L0 sans contexte GOVERNANCE-HUB
6. **BDCP** : Aucun appel réseau sortant non autorisé
7. **CI vert** : `registry-sync.yml` valide le frontmatter agentic

### Critères v2 (nouveaux)
8. **Délégation** : Le DELEGATOR identifie correctement le niveau de complexité sur 10 requêtes test (5 simples, 3 moyennes, 2 complexes)
9. **Reformulation** : Le REWRITER produit des sous-quêtes qui matchent des skills existants dans le MANIFEST (100% de match sur 10 intents test)
10. **Brouillon** : Le DRAFT AGENT produit un brouillon structuré pour toute requête de niveau 2+
11. **Feedback ciblé** : Le GAP ANALYZER génère un feedback avec skills recommandés pour 100% des gaps injectés
12. **Latence adaptée** : Niveau 1 < 2s, Niveau 2 < 8s, Niveau 3 < 15s (mesuré sur 5 requêtes par niveau)

---

## 6. Planning v2

| Phase | Objectif | Livrables | Durée | Statut |
|-------|----------|-----------|-------|--------|
| **Phase 1** | Créer les 3 skills agentic v1 | L1, L2, L3 | 1 jour | ✅ Fait |
| **Phase 2** | Enrichir le manifest et la CI | L5, L7 | 0.5 jour | ✅ Fait |
| **Phase 3** | Tests et validation v1 | L6 | 1 jour | ✅ Fait |
| **Phase 4** | **NOUVELLE** — Implémenter les 3 patterns v2 | L4, L8, enrichir L1/L2/L6/L7 | 1 jour | ❌ À faire |
| **Phase 5** | Revue croisée + merge v2 | Rapport consolidé | 0.5 jour | ❌ À faire |

**Total v2** : 4 jours (vs 3 jours en v1)

---

## 7. Risques et Mitigations v2

| Risque | Probabilité | Impact | Mitigation |
|--------|--------------|--------|------------|
| **Explosion combinatoire** | Moyenne | Haut | Limiter à 5 skills parallèles ; budget d'itérations max = 3 |
| **Coverage Agent circulaire** | Moyenne | Moyen | Jeu de test de 20 requêtes pour calibrer |
| **Latence excessive** | Haute | Haut | Délégation conditionnelle (niveau 1 = pas de pipeline) |
| **Conflit de strate** | Faible | Haut | Règle dure dans le ROUTER : respect strict L0→L9 |
| **Dérive BDCP** | Faible | Critique | Audit de chaque skill agentic par Alfred |
| **REWRITER trop agressif** (trop de sous-quêtes) | Moyenne | Moyen | Limiter à 5 sous-quêtes par intent |
| **DRAFT AGIONT trop lent** | Faible | Moyen | Brouillon léger (structure seulement, pas de contenu détaillé) |

---

## 8. Comparaison v1 vs v2

| Dimension | v1 | v2 |
|-----------|----|----|
| **Agents** | 7 | 9 (+ DELEGATOR, + REWRITER, + DRAFT/GAP dans COVERAGE) |
| **Slots** | 63/100 | 64/100 |
| **Orchestration** | Linéaire | Conditionnelle (3 niveaux) |
| **Reformulation** | Non | Oui (REWRITER) |
| **Brouillon** | Non | Oui (DRAFT AGENT) |
| **Feedback gaps** | Générique | Ciblé (GAP ANALYZER) |
| **Latence** | Fixe (~15s) | Adaptée (2s-15s selon complexité) |
| **Tests** | 20 requêtes | 30 requêtes (+10 pour v2) |

---

## 9. Prochaines étapes

1. **Implémenter Phase 4** — Créer `skills-rewriter.md`, enrichir `skills-coverage.md` (Draft + Gap Analyzer), enrichir `skills-agentic.md` (DELEGATOR)
2. **Enrichir les tests** — Ajouter 10 requêtes de test spécifiques à v2 (délégation, reformulation, brouillon)
3. **Mettre à jour la CI** — Enrichir `validate-agentic.py` pour valider les nouveaux champs v2
4. **Revue croisée** — SCO7 + Selena + Alfred + Riddler sur la v2
5. **Merge** — Tous les livrables v2 mergés sur `main`

---

*Fin du PRD v2 | IntentHash : `0xSKILLS_AGENTIC_RAG_v2_20260606`*
