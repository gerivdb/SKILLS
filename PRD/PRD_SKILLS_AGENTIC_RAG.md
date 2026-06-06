# PRD — SKILLS_AGENTIC : Architecture Agentic RAG pour le Métacluster gerivdb

**Version** : 1.0
**Date** : 2026-06-06
**Auteur** : OPS-ENGINE (inspiré de l'analyse Google Agentic RAG, adapté au métacluster gerivdb)
**Statut** : DRAFT — soumis à revue SCO7 + Selena + Alfred + Riddler
**IntentHash** : `0xSKILLS_AGENTIC_RAG_20260606`

---

## 1. Contexte et Motivation

### 1.1 Le problème actuel

Le repo `gerivdb/SKILLS` contient **59 skills** spécialisés couvrant les strates L0-L9 du métacluster gerivdb (185 repos). Chaque skill est un fichier Markdown autonome avec un frontmatter YAML. Le système actuel est **statique et mono-skill** :

- **Sélection manuelle** : l'utilisateur (ou l'LLM) doit identifier le bon skill pour sa requête
- **Pas de composition** : aucune mécanique pour activer plusieurs skills en parallèle
- **Pas de vérification de couverture** : aucun mécanisme pour détecter qu'un skill manque pour traiter complètement une requête
- **Pas de routing cross-repo** : un skill sait quoi faire, mais pas dans quel repo chercher
- **Pas d'itération** : si un skill produit un résultat incomplet, pas de boucle de correction

### 1.2 L'inspiration : Google Agentic RAG

L'article Google Research (5 juin 2026) introduit un framework multi-agent RAG avec un **Sufficient Context Agent** qui vérifie la complétude du contexte avant de générer une réponse. Nous adaptons ce pattern à notre problématique : **non pas vérifier la complétude des données, mais la complétude de la couverture des skills**.

### 1.3 Différence fondamentale

| Dimension | Google Agentic RAG | SKILLS_AGENTIC (gerivdb) |
|-----------|---------------------|---------------------------|
| **Objet du retrieval** | Documents (PDFs, DB) | Skills (capacités) |
| **Corpus** | 2 676 PDFs statiques | 59 skills dynamiques + 185 repos |
| **Critère de suffisance** | Contexte informationnel complet | Couverture fonctionnelle complète |
| **Routing** | Cross-corpus (4 datasets) | Cross-repo (185 repos, strates L0-L9) |
| **Itération** | Recherche de données manquantes | Activation de skills manquants |
| **Contrainte unique** | Latence < 12s | Conformité BDCP, φ-CPS, strates L |

---

## 2. Objectif

Concevoir et implémenter **SKILLS_AGENTIC**, une couche d'orchestration agentique au-dessus des 59 skills existants, qui :

1. **Analyse** la requête utilisateur et décompose les besoins en sous-tâches
2. **Sélectionne** les skills pertinents (mono ou multi-skill)
3. **Route** chaque skill vers le(s) repo(s) cible(s) approprié(s)
4. **Vérifie** la couverture fonctionnelle (équivalent du Sufficient Context Agent)
5. **Itère** si des skills manquants sont détectés
6. **Synthétise** les résultats en un livrable cohérent

Le résultat visé : **zéro skill manquant** pour toute requête complexe, avec traçabilité complète de la chaîne d'activation.

---

## 3. Architecture

### 3.1 Vue d'ensemble — Les 5 Agents SKILLS_AGENTIC

```
┌─────────────────────────────────────────────────────────────────┐
│                    SKILLS_AGENTIC Pipeline                       │
│                                                                  │
│  Requête utilisateur                                             │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │ 1. PARSER   │───▶│ 2. PLANNER  │───▶│ 3. ROUTER   │          │
│  │ Agent       │    │ Agent       │    │ Agent       │          │
│  │             │    │             │    │             │          │
│  │ Décompose   │    │ Sélectionne │    │ Mappe skill │          │
│  │ la requête  │    │ les skills  │    │ → repo cible│          │
│  │ en intents  │    │ nécessaires │    │ (L0-L9)     │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│                                               │                  │
│                                               ▼                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │ 6. SYNTH    │◀───│ 5. FANOUT   │◀───│ 4. COVERAGE │          │
│  │ Agent       │    │ Agent       │    │ Agent       │          │
│  │             │    │             │    │             │          │
│  │ Agrège les  │    │ Exécute les │    │ Vérifie la  │          │
│  │ résultats   │    │ skills en   │    │ couverture  │          │
│  │ en réponse  │    │ parallèle   │    │ fonctionnelle│         │
│  │ finale      │    │             │    │             │          │
│  └─────────────┘    └─────────────┘    └──────┬──────┘          │
│       ▲                                       │                  │
│       │         ┌─────────────┐               │                  │
│       └─────────│ 7. ITERATOR │◀──────────────┘                  │
│                 │ Agent       │  (si couverture insuffisante)    │
│                 │             │                                  │
│                 │ Relance le  │                                  │
│                 │ Planner avec│                                  │
│                 │ feedback    │                                  │
│                 └─────────────┘                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Description des Agents

#### Agent 1 — PARSER
**Rôle** : Décomposer la requête utilisateur en intents atomiques.

**Entrée** : Requête libre (ex: "Audit complet du repo FLUENCE avec vérification conformité NEXUS et génération du rapport")
**Sortie** : Liste d'intents structurés
```json
{
  "intents": [
    {"action": "audit_structure", "scope": "FLUENCE", "strate": "L1"},
    {"action": "verifier_conformite", "scope": "NEXUS", "strate": "L0"},
    {"action": "generer_rapport", "scope": "FLUENCE", "strate": "L1"}
  ]
}
```

**Mapping skills** : `reposcope-run`, `nexus-auditor`, `adr-manager`

#### Agent 2 — PLANNER
**Rôle** : Sélectionner les skills nécessaires et définir l'ordre d'exécution.

**Entrée** : Liste d'intents
**Sortie** : Plan d'exécution ordonné avec dépendances
```json
{
  "plan": [
    {"step": 1, "skill": "reposcope-run", "intents": ["audit_structure"], "deps": []},
    {"step": 2, "skill": "nexus-auditor", "intents": ["verifier_conformite"], "deps": [1]},
    {"step": 3, "skill": "adr-manager", "intents": ["verifier_conformite"], "deps": [1]},
    {"step": 4, "skill": "workflow-orchestration", "intents": ["generer_rapport"], "deps": [2, 3]}
  ]
}
```

**Règle clé** : Respecter la hiérarchie L0→L9. Un skill L0 (gouvernance) ne peut pas dépendre d'un skill L3+ (outil).

#### Agent 3 — ROUTER
**Rôle** : Mapper chaque skill vers le(s) repo(s) cible(s) en utilisant `known_repositories.yaml`.

**Entrée** : Plan d'exécution
**Sortie** : Plan enrichi avec repos cibles
```json
{
  "routed_plan": [
    {"step": 1, "skill": "reposcope-run", "repo": "D:\\DO\\WEB\\FLUENCE", "strate": "L1"},
    {"step": 2, "skill": "nexus-auditor", "repo": "D:\\DO\\WEB\\TOOLS\\L0-CANON\\NEXUS", "strate": "L0"},
    {"step": 3, "skill": "adr-manager", "repo": "D:\\DO\\WEB\\TOOLS\\L0-CANON\\GOVERNANCE-HUB", "strate": "L0"},
    {"step": 4, "skill": "workflow-orchestration", "repo": "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS", "strate": "L4"}
  ]
}
```

**Source de vérité** : `gerivdb/GOVERNANCE-HUB/known_repositories.yaml` (GATE-0/1/2/3 obligatoire)

#### Agent 4 — COVERAGE (l'innovation clé — équivalent du Sufficient Context Agent)
**Rôle** : Vérifier que l'ensemble des skills sélectionnés couvre tous les intents de la requête.

**Entrée** : Plan routé + intents originaux
**Sortie** : Verdict de couverture + gaps identifiés

```json
{
  "coverage_verdict": "INSUFFICIENT",
  "covered_intents": ["audit_structure", "verifier_conformite"],
  "missing_intents": ["generer_rapport"],
  "missing_skills": ["prd-factory"],
  "feedback": "Le plan couvre l'audit et la conformité, mais ne génère pas de rapport. Ajouter prd-factory ou workflow-orchestration."
}
```

**Critères de couverture** :
1. **Exhaustivité** : Chaque intent a-t-il au moins un skill assigné ?
2. **Compétence** : Le skill assigné a-t-il la capacité de traiter l'intention ? (vérification via le frontmatter `description` du skill)
3. **Strate** : Le skill est-il dans la bonne strate L0-L9 pour le repo cible ?
4. **Dépendance** : Les dépendances inter-skills sont-elles respectées ?

#### Agent 5 — FANOUT
**Rôle** : Exécuter les skills en parallèle quand c'est possible (pas de dépendances entre eux).

**Entrée** : Plan routé validé par le COVERAGE Agent
**Sortie** : Résultats bruts de chaque skill

**Stratégie** :
- Skills sans dépendances mutuelles → exécution parallèle (via `task` tool)
- Skills avec dépendances → exécution séquentielle
- Maximum 5 skills en parallèle (contrainte SLM)

#### Agent 6 — SYNTH
**Rôle** : Agréger les résultats de tous les skills en un livrable cohérent.

**Entrée** : Résultats bruts du FANOUT
**Sortie** : Réponse finale structurée

**Format** : Markdown avec sections par skill, tags de conformité NEXUS, et traçabilité complète.

#### Agent 7 — ITERATOR
**Rôle** : Relancer le pipeline si le COVERAGE Agent a détecté des gaps.

**Entrée** : Verdict INSUFFICIENT + feedback du COVERAGE Agent
**Sortie** : Nouveau plan enrichi avec les skills manquants

**Condition d'arrêt** :
- Couverture SUFFICIENT → passer à FANOUT
- 3 itérations max → si toujours INSUFFICIENT, escalade HITL

---

## 4. Livrables

| ID | Livrable | Description | Impact |
|----|----------|-------------|--------|
| **L1** | `skills-agentic.md` | Nouveau skill principal orchestrant le pipeline 5 agents | +1 slot |
| **L2` | `skills-coverage.md` | Skill dédié à la vérification de couverture (équivalent Sufficient Context Agent) | +1 slot |
| **L3** | `skills-router.md` | Skill de routing cross-repo utilisant known_repositories.yaml | +1 slot |
| **L4** | `MANIFEST.json` v2 | Manifest enrichi avec métadonnées agentic (intents, coverage_rules, strate_constraints) | 0 slot |
| **L5** | `skills-agentic-test.md` | Suite de tests pour valider le pipeline agentic | +1 slot |
| **L6** | `registry-sync.yml` v2 | CI enrichie avec validation de couverture | 0 slot |

**Impact slots** : +4 slots (de 59 → 63, marge de 37 slots restants sur 100)

---

## 5. Critères d'acceptation

1. **Couverture** : Toute requête multi-intents (≥3 intents) doit déclencher automatiquement les skills pertinents sans intervention manuelle
2. **Suffisance** : Le COVERAGE Agent doit détecter 100% des gaps de skills sur un jeu de test de 20 requêtes complexes
3. **Traçabilité** : Chaque activation de skill doit être loggée avec intent, repo cible, strate L, et résultat
4. **Itération** : Le pipeline doit converger en ≤3 itérations pour toute requête
5. **Conformité** : Aucun skill L0 ne peut être activé sans contexte GOVERNANCE-HUB chargé (GATE-0)
6. **BDCP** : Aucun appel réseau sortant non autorisé (conformité règle BDCP inviolable)
7. **CI vert** : `registry-sync.yml` doit valider le frontmatter agentic de chaque skill

---

## 6. Planning

| Phase | Objectif | Livrables | Durée |
|-------|----------|-----------|-------|
| **Phase 1** | Créer les 3 nouveaux skills agentic | L1, L2, L3 | 1 jour |
| **Phase 2** | Enrichir le manifest et la CI | L4, L6 | 0.5 jour |
| **Phase 3** | Tests et validation | L5 | 1 jour |
| **Phase 4** | Revue croisée SCO7+Selena+Alfred+Riddler | Rapport consolidé | 0.5 jour |

**Total** : 3 jours

---

## 7. Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|--------------|--------|------------|
| **Explosion combinatoire** (trop de skills activés simultanément) | Moyenne | Haut | Limiter à 5 skills parallèles ; budget d'itérations max = 3 |
| **Coverage Agent circulaire** (détecte des gaps qui n'en sont pas) | Moyenne | Moyen | Jeu de test de 20 requêtes pour calibrer les seuils |
| **Latence excessive** (7 agents = 7 appels LLM) | Haute | Haut | Utiliser des modèles légers (Flash) pour les agents simples ; cache des plans |
| **Conflit de strate** (skill L0 activé après L3) | Faible | Haut | Règle dure dans le ROUTER : respect strict L0→L9 |
| **Dérive BDCP** (appel réseau non autorisé) | Faible | Critique | Audit de chaque skill agentic par Alfred avant merge |

---

## 8. Différences clés avec Google Agentic RAG

| Aspect | Google | SKILLS_AGENTIC |
|--------|--------|----------------|
| **Ce qu'on retrieve** | Documents | Skills (capacités) |
| **Critère d'arrêt** | Contexte suffisant | Couverture fonctionnelle suffisante |
| **Source de vérité** | Corpus statique | `known_repositories.yaml` dynamique |
| **Contrainte de strate** | Aucune | L0→L9 obligatoire |
| **Itération max** | Non spécifiée | 3 (puis HITL) |
| **Parallélisme** | Fanout illimité | Max 5 skills |
| **Compliance** | Standard enterprise | BDCP inviolable + φ-CPS |

---

## 9. Prochaines étapes

1. **Revue technique SCO7** — Valider l'architecture des 7 agents
2. **Revue stratégique Selena** — Évaluer l'impact sur le métacluster
3. **Revue risques Alfred** — Auditer les vulnérabilités du pipeline agentic
4. **Revue critique Riddler** — Identifier les failles logiques et les biais
5. **Implémentation Phase 1** — Créer les 3 skills agentic

---

*Fin du PRD | IntentHash : `0xSKILLS_AGENTIC_RAG_20260606`*
