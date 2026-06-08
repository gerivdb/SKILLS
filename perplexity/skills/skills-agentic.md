---
name: skills-agentic
version: "2.0.0"
description: "Orchestrateur agentic v2 du pipeline SKILLS_AGENTIC. Coordonne 9 agents spécialisés (DELEGATOR, PARSER, REWRITER, PLANNER, ROUTER, COVERAGE+DRAFT+GAP, FANOUT, SYNTH, ITERATOR). Orchestration conditionnelle à 3 niveaux de complexité. Équivalent adapté du Google Agentic RAG pour le métacluster gerivdb (185 repos, strates L0-L9). Utiliser quand l'utilisateur mentionne 'orchestrer', 'pipeline agentic', 'multi-skill', 'couverture skills', 'SKILLS_AGENTIC'."
triggers:
  - "orchestrer"
  - "pipeline agentic"
  - "multi-skill"
  - "couverture skills"
  - "SKILLS_AGENTIC"
  - "décomposer requête"
  - "activer skills"
  - "déléguer"
  - "niveau complexité"
  - "orchestration conditionnelle"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "known_repositories.yaml (GOVERNANCE-HUB)"
  - "MANIFEST.json (SKILLS)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — pipeline 7 agents"}
  - {v: "2.0.0", date: "2026-06-07", notes: "v2 — + DELEGATOR (Agent 0), + REWRITER (Agent 1b), orchestration conditionnelle 3 niveaux"}
trit_primitive: TritDocumentClassify
---

# SKILLS_AGENTIC — Orchestrateur Agentic v2

## Domaine et périmètre

Ce skill est l'**orchestrateur principal** du pipeline SKILLS_AGENTIC v2. Il coordonne **9 agents spécialisés** pour transformer une requête utilisateur complexe en un livrable cohérent. La v2 introduit l'**orchestration conditionnelle** (3 niveaux de complexité) et le **REWRITER** pour la reformulation des intents.

**Inspiration** : Google Agentic RAG (Google Research, 5 juin 2026) — 6 patterns exploités (3 en v1, 3 en v2).

## Architecture v2 — Les 9 Agents

```
Requête utilisateur
       │
       ▼
┌─────────────────┐
│ 0. DELEGATOR    │  Évalue complexité → niveau 1/2/3
│ Agent           │
│                 │  Niveau 1 (simple)  → skill direct (< 2s)
│                 │  Niveau 2 (moyen)   → pipeline court 4 agents (< 8s)
│                 │  Niveau 3 (complexe) → pipeline complet 9 agents (< 15s)
└────────┬────────┘
         │ (niveau 2 ou 3)
         ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1. PARSER   │───▶│ 1b. REWRITER│───▶│ 2. PLANNER  │
│             │    │             │    │             │
│ Décompose   │    │ Reformule   │    │ Sélectionne │
│ en intents  │    │ en sous-    │    │ les skills  │
│             │    │ quêtes      │    │ nécessaires │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐
│ 6. SYNTH    │◀───│ 5. FANOUT   │◀───│ 3. ROUTER              │
│             │    │             │    │                         │
│ Agrège les  │    │ Exécute les │    │ Mappe skill → repo      │
│ résultats   │    │ skills en   │    │ cible (L0-L9)           │
│             │    │ parallèle   │    │                         │
└─────────────┘    └─────────────┘    └──────────┬──────────────┘
       ▲                                         │
       │         ┌───────────────────────────────┘
       │         │
       │         ▼
       │  ┌─────────────────────────────────────────────┐
       │  │ 4. COVERAGE Agent (enrichi v2)              │
       │  │                                             │
       │  │  4a. Coverage Checker (4 critères)          │
       │  │  4b. Draft Agent (brouillon intermédiaire)  │
       │  │  4c. Gap Analyzer (feedback ciblé)          │
       │  └──────────────────┬──────────────────────────┘
       │                     │
       │                     ▼ (si INSUFFICIENT)
       │  ┌─────────────┐
       │  │ 7. ITERATOR │───▶ Relance REWRITER + PLANNER
       │  │             │     avec feedback ciblé du GAP
       │  └─────────────┘     Analyzer
       │
       ▼
  Réponse finale
```

## Méthodologie

### Phase 0 — DELEGATOR : Évaluation de complexité (nouveau v2)

**Objectif** : Évaluer la complexité de la requête et décider du niveau d'activation.

**Entrée** : Requête utilisateur (texte libre)
**Sortie** : Niveau de complexité (1, 2, ou 3) + justification

**Critères d'évaluation** :

| Critère | Niveau 1 (Simple) | Niveau 2 (Moyen) | Niveau 3 (Complexe) |
|---------|-------------------|-------------------|---------------------|
| Nombre d'intents | 1 | 2-3 | 4+ |
| Nombre de strates | 1 | 1-2 | 2+ |
| Ambiguïté | Claire | Moyenne | Vague |
| Mots-clés | — | "complet", "vérifier" | "global", "cross-repo", "tout" |

**Règles** :
1. Niveau 1 → activer directement le skill identifié (pas de pipeline)
2. Niveau 2 → pipeline court (PARSER → REWRITER → PLANNER → ROUTER → FANOUT → SYNTH)
3. Niveau 3 → pipeline complet (9 agents avec COVERAGE enrichi + ITERATOR)
4. En cas de doute → privilégier le niveau supérieur

**Exemple** :
```
Requête : "Vérifie FLUENCE"
→ Niveau 1 (1 intent, 1 strate, clair) → activer reposcope-run directement

Requête : "Audit FLUENCE + vérifie conformité NEXUS"
→ Niveau 2 (2 intents, 2 strates) → pipeline court

Requête : "Audit complet FLUENCE : structure, conformité NEXUS, ADR, PRD, rapport"
→ Niveau 3 (5 intents, cross-strate) → pipeline complet
```

### Phase 1 — PARSER : Décomposition de la requête

**Objectif** : Transformer la requête libre en intents atomiques structurés.

**Entrée** : Requête utilisateur (texte libre)
**Sortie** : Liste d'intents au format JSON

**Règles** :
1. Chaque intent doit être **atomique** (une seule action, un seul scope)
2. Chaque intent doit inclure : `action`, `scope` (repo ou domaine), `strate` (L0-L9)
3. Maximum 7 intents par requête (au-delà → escalade HITL)
4. Si la requête est ambiguë → demander clarification (ne pas deviner)

**Exemple** :
```
Requête : "Audit complet du repo FLUENCE avec vérification conformité NEXUS et génération du rapport"

Sortie :
[
  {"action": "audit_structure", "scope": "FLUENCE", "strate": "L1"},
  {"action": "verifier_conformite", "scope": "NEXUS", "strate": "L0"},
  {"action": "generer_rapport", "scope": "FLUENCE", "strate": "L1"}
]
```

### Phase 2 — PLANNER : Sélection des skills

**Objectif** : Mapper chaque intent aux skills nécessaires et définir l'ordre d'exécution.

**Entrée** : Liste d'intents
**Sortie** : Plan d'exécution ordonné avec dépendances

**Règles** :
1. Consulter le `MANIFEST.json` pour trouver les skills correspondant à chaque intent
2. Vérifier les `triggers` et la `description` de chaque skill
3. Respecter la hiérarchie L0→L9 : un skill L0 ne peut pas dépendre d'un skill L3+
4. Détecter les dépendances inter-skills (ex: nexus-auditor dépend de reposcope-run)
5. Maximum 5 skills par plan (au-delà → décomposer en sous-plans)

**Exemple** :
```
Plan :
[
  {"step": 1, "skill": "reposcope-run", "intents": ["audit_structure"], "deps": []},
  {"step": 2, "skill": "nexus-auditor", "intents": ["verifier_conformite"], "deps": [1]},
  {"step": 3, "skill": "workflow-orchestration", "intents": ["generer_rapport"], "deps": [2]}
]
```

### Phase 3 — ROUTER : Mapping skill → repo

**Objectif** : Associer chaque skill au(x) repo(s) cible(s) en utilisant `known_repositories.yaml`.

**Entrée** : Plan d'exécution
**Sortie** : Plan enrichi avec repos cibles et strates

**Règles** :
1. Source de vérité : `gerivdb/GOVERNANCE-HUB/known_repositories.yaml` (GATE-0 obligatoire)
2. Chaque skill doit être mappé à un repo existant dans le registre
3. Vérifier la strate L0-L9 du repo cible
4. Si le repo n'existe pas dans le registre → erreur + feedback
5. Un skill peut être mappé à plusieurs repos si nécessaire (ex: nexus-auditor → NEXUS + FLUENCE)

### Phase 4 — COVERAGE : Vérification de couverture

**Objectif** : Vérifier que l'ensemble des skills sélectionnés couvre tous les intents.

**Entrée** : Plan routé + intents originaux
**Sortie** : Verdict (SUFFICIENT / INSUFFICIENT) + gaps identifiés

**Critères** (voir `skills-coverage.md` pour le détail) :
1. **Exhaustivité** : Chaque intent a-t-il au moins un skill assigné ?
2. **Compétence** : Le skill assigné a-t-il la capacité de traiter l'intention ?
3. **Strate** : Le skill est-il dans la bonne strate L0-L9 ?
4. **Dépendance** : Les dépendances inter-skills sont-elles respectées ?

**Si INSUFFICIENT** → générer feedback structuré pour l'ITERATOR

### Phase 5 — FANOUT : Exécution parallèle

**Objectif** : Exécuter les skills validés par le COVERAGE Agent.

**Entrée** : Plan routé validé
**Sortie** : Résultats bruts de chaque skill

**Stratégie** :
1. Skills sans dépendances mutuelles → exécution parallèle (via `task` tool)
2. Skills avec dépendances → exécution séquentielle (respecter l'ordre du plan)
3. Maximum 5 skills en parallèle (contrainte SLM)
4. Timeout par skill : 120s (au-delà → marquer comme FAILED)
5. Logger chaque exécution : skill, intent, repo, strate, statut, durée

### Phase 6 — SYNTH : Agrégation des résultats

**Objectif** : Transformer les résultats bruts en un livrable cohérent.

**Entrée** : Résultats bruts du FANOUT
**Sortie** : Réponse finale structurée

**Format** :
```markdown
## Résultat — [Titre de la requête]

### Exécution
- Skills activés : [liste]
- Repos cibles : [liste]
- Couverture : [SUFFICIENT / INSUFFICIENT]

### Résultats par skill
#### [skill-1] — [intent]
- Statut : [OK / FAILED / PARTIEL]
- Résultat : ...

#### [skill-2] — [intent]
...

### Synthèse
[Conclusion globale]

### Traçabilité
| Skill | Intent | Repo | Strate | Statut |
|-------|--------|------|--------|--------|
| ... | ... | ... | ... | ... |
```

### Phase 7 — ITERATOR : Boucle de correction avec feedback ciblé (enrichi v2)

**Objectif** : Relancer le pipeline si le COVERAGE Agent a détecté des gaps, en utilisant le **feedback ciblé du GAP ANALYZER**.

**Entrée** : Verdict INSUFFICIENT + feedback ciblé du GAP ANALYZER
**Sortie** : Nouveau plan enrichi avec les skills manquants

**Règles** :
1. Maximum 3 itérations (au-delà → escalade HITL)
2. Chaque itération doit enrichir le plan avec au moins 1 nouveau skill
3. Utiliser le feedback ciblé du GAP ANALYZER pour guider le REWRITER et le PLANNER
4. Si aucune amélioration après 2 itérations → escalade HITL
5. Logger chaque itération : numéro, gaps détectés, skills ajouté, source du feedback

**flux d'itéRATION v2** :
```
GAP ANALYZER → feedback ciblé → REWRITER (reformule les intents manquants)
                              → PLANNER (ajoute les skills recommandés)
                              → ROUTER (route les nouveaux skills)
                              → COVERAGE (re-vérifie)
                              → Si SUFFICIENT → FANOUT
                              → Si INSUFFICIENT → ITERATION (max 3)
```

**Exemple de feedback ciblé** :
```
Itération 1 :
  GAP ANALYZER : "Il manque un skill pour générer le rapport. Recommandé : workflow-orchestration (L4)"
  REWRITER : Ajoute sous-quête "compile_audit_results" → workflow-orchestration
  PLANNER : Ajoute workflow-orchestration (step 4)
  COVERAGE : SUFFICIENT → passer à FANOUT
```

## Règles de décision

- **Règle 1** : Aucun skill L0 ne peut être activé sans contexte GOVERNANCE-HUB chargé (GATE-0)
- **Règle 2** : Aucun appel réseau sortant non autorisé (conformité BDCP inviolable)
- **Règle 3** : Maximum 5 skills en parallèle (contrainte SLM)
- **Règle 4** : Maximum 3 itérations du pipeline (puis HITL)
- **Règle 5** : Maximum 7 intents par requête (au-delà → HITL)
- **Règle 6** : Toujours vérifier `known_repositories.yaml` avant de router (GATE-0/1/2/3)
- **Règle 7** : En cas de conflit de strate → privilégier la strate la plus haute (L0 > L9)
- **Règle 8** (v2) : Le DELEGATOR évalue toujours la complexité avant d'activer le pipeline
- **Règle 9** (v2) : Le REWRITER reformule les intents uniquement pour les niveaux 2 et 3
- **Règle 10** (v2) : L'ITERATOR utilise le feedback ciblé du GAP ANALYZER (pas un feedback générique)

## Format de sortie

```markdown
## SKILLS_AGENTIC v2 — Rapport d'exécution

### Requête
[Requête utilisateur originale]

### Délégation
- Niveau de complexité : [1 / 2 / 3]
- Justification : [raison]
- Agents activés : [liste]

### Décomposition
- Intents identifiés : [N]
- Sous-quêtes générées : [N] (REWRITER)
- Skills sélectionnés : [N]
- Repos cibles : [liste]

### Couverture
- Verdict : [SUFFICIENT / INSUFFICIENT]
- Brouillon produit : [Oui / Non]
- Gaps identifiés : [N]
- Itérations : [N]

### Résultats
[Résultats par skill]

### Traçabilité
| Skill | Intent | Repo | Strate | Statut |
|-------|--------|------|--------|--------|
| ... | ... | ... | ... | ... |
```

## Intégration avec l'écosystème

- **Dépôts concernés** : Tous les 185 repos gerivdb (via known_repositories.yaml)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-coverage.md, skills-router.md, skills-rewriter.md
- **Skills complémentaires** : Tous les 63 skills existants (comme cibles d'activation)
- **Agents liés** : SCO7, Selena, Alfred, Riddler (pour les requêtes d'analyse croisée)
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]

## Contraintes

| Contrainte | Valeur |
|------------|--------|
| Max intents par requête | 7 |
| Max skills par plan | 5 |
| Max skills en parallèle | 5 |
| Max itérations | 3 |
| Timeout par skill | 120s |
| Plafond slots Perplexity | 100 |
| Slots utilisés (v2) | 64/100 |
| Latence niveau 1 | < 2s |
| Latence niveau 2 | < 8s |
| Latence niveau 3 | < 15s |
