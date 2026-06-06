---
name: skills-agentic
version: "1.0.0"
description: "Orchestrateur agentic du pipeline SKILLS_AGENTIC. Décompose les requêtes complexes en intents, sélectionne les skills pertinents, route vers les repos cibles, vérifie la couverture fonctionnelle, et synthétise les résultats. Équivalent adapté du Google Agentic RAG pour le métacluster gerivdb (185 repos, strates L0-L9). Utiliser quand l'utilisateur mentionne 'orchestrer', 'pipeline agentic', 'multi-skill', 'couverture skills', 'SKILLS_AGENTIC'."
triggers:
  - "orchestrer"
  - "pipeline agentic"
  - "multi-skill"
  - "couverture skills"
  - "SKILLS_AGENTIC"
  - "décomposer requête"
  - "activer skills"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "known_repositories.yaml (GOVERNANCE-HUB)"
  - "MANIFEST.json (SKILLS)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — pipeline 7 agents"}
---

# SKILLS_AGENTIC — Orchestrateur Agentic

## Domaine et périmètre

Ce skill est l'**orchestrateur principal** du pipeline SKILLS_AGENTIC. Il coordonne 7 agents spécialisés pour transformer une requête utilisateur complexe en un livrable cohérent, en passant par la décomposition, la sélection, le routing, la vérification de couverture, l'exécution parallèle, et la synthèse.

**Inspiration** : Google Agentic RAG (Google Research, 5 juin 2026) — adapté aux contraintes du métacluster gerivdb (BDCP inviolable, strates L0-L9, φ-CPS, 185 repos).

## Architecture — Les 7 Agents

```
Requête utilisateur
       │
       ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1. PARSER   │───▶│ 2. PLANNER  │───▶│ 3. ROUTER   │
│             │    │             │    │             │
│ Décompose   │    │ Sélectionne │    │ Mappe skill │
│ en intents  │    │ les skills  │    │ → repo cible│
└─────────────┘    └─────────────┘    └─────────────┘
                                               │
                                               ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 6. SYNTH    │◀───│ 5. FANOUT   │◀───│ 4. COVERAGE │
│             │    │             │    │             │
│ Agrège les  │    │ Exécute les │    │ Vérifie la  │
│ résultats   │    │ skills en   │    │ couverture  │
│             │    │ parallèle   │    │ fonctionnelle│
└─────────────┘    └─────────────┘    └──────┬──────┘
       ▲                                       │
       │         ┌─────────────┐               │
       └─────────│ 7. ITERATOR │◀──────────────┘
                 │             │  (si couverture
                 │ Relance le  │   insuffisante)
                 │ Planner     │
                 └─────────────┘
```

## Méthodologie

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

### Phase 7 — ITERATOR : Boucle de correction

**Objectif** : Relancer le pipeline si le COVERAGE Agent a détecté des gaps.

**Entrée** : Verdict INSUFFICIENT + feedback du COVERAGE Agent
**Sortie** : Nouveau plan enrichi avec les skills manquants

**Règles** :
1. Maximum 3 itérations (au-delà → escalade HITL)
2. Chaque itération doit enrichir le plan avec au moins 1 nouveau skill
3. Si aucune amélioration après 2 itérations → escalade HITL
4. Logger chaque itération : numéro, gaps détectés, skills ajoutés

## Règles de décision

- **Règle 1** : Aucun skill L0 ne peut être activé sans contexte GOVERNANCE-HUB chargé (GATE-0)
- **Règle 2** : Aucun appel réseau sortant non autorisé (conformité BDCP inviolable)
- **Règle 3** : Maximum 5 skills en parallèle (contrainte SLM)
- **Règle 4** : Maximum 3 itérations du pipeline (puis HITL)
- **Règle 5** : Maximum 7 intents par requête (au-delà → HITL)
- **Règle 6** : Toujours vérifier `known_repositories.yaml` avant de router (GATE-0/1/2/3)
- **Règle 7** : En cas de conflit de strate → privilégier la strate la plus haute (L0 > L9)

## Format de sortie

```markdown
## SKILLS_AGENTIC — Rapport d'exécution

### Requête
[Requête utilisateur originale]

### Décomposition
- Intents identifiés : [N]
- Skills sélectionnés : [N]
- Repos cibles : [liste]

### Couverture
- Verdict : [SUFFICIENT / INSUFFICIENT]
- Itérations : [N]

### Résultats
[Résultats par skill]

### Traçabilité
[Tableau de traçabilité]
```

## Intégration avec l'écosystème

- **Dépôts concernés** : Tous les 185 repos gerivdb (via known_repositories.yaml)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-coverage.md, skills-router.md
- **Skills complémentaires** : Tous les 59 skills existants (comme cibles d'activation)
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
| Slots utilisés (Phase 1) | 62/100 |
