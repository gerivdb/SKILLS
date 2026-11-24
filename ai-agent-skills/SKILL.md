---
name: ai-agent-skills
description: Patterns inspirés de Voyager (curriculum automatique, bibliothèque de skills vérifiés, raffinement itératif et composition de skills). Pattern inspiré de https://github.com/sreerevanth/AI-Agent-Skills
version: 1.0.0
intent_hash: 0xSKILL_AI_AGENT_SKILLS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/sreerevanth/AI-Agent-Skills
source_url: https://github.com/sreerevanth/AI-Agent-Skills
path: ai-agent-skills
---

# AI Agent Skills — Skill KiloCode

## Objectif

Mettre en place une bibliothèque de skills vérifiés avec curriculum automatique, raffinement itératif et composition de skills, inspiré du pattern Voyager. Ce skill structure l'auto-amélioration des skills dans l'environnement ENV2.

## Déclencheur

Ce skill s'active quand :
- Un nouveau skill doit être ajouté à la bibliothèque vérifiée
- Un skill existant doit être raffiné itérativement
- Plusieurs skills doivent être composés pour accomplir une tâche complexe
- Un curriculum d'apprentissage doit être défini pour une séquence de skills

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `skill_name` | string | ✅ | Nom du skill à ajouter ou raffiner |
| `verification_proof` | object | ✅ | Preuve de vérification (tests, compilation, exécution RC=0) |
| `composition_target` | string | ❌ | Tâche cible pour la composition de skills |
| `curriculum_step` | integer | ❌ | Étape du curriculum (1 = débutant, N = avancé) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `verified_skill` | string | Nom du skill vérifié et promu |
| `composition_plan` | array | Plan de composition des skills pour la tâche cible |
| `curriculum` | array | Séquence ordonnée de skills pour l'apprentissage |
| `version` | string | Nouvelle version semver après raffinement |
| `evidence_hash` | string | Hash SHA-256 de la preuve de vérification |

## Protocole Obligatoire

### Étape 1 — Vérification du skill

```
→ Exécuter le skill dans un environnement isolé
→ Capturer le code de retour (doit être 0)
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 de la sortie
→ Vérifier que le working tree est propre après exécution
```

### Étape 2 — Promotion dans la bibliothèque

```
→ Si vérification réussie → promouvoir le skill de draft → active
→ Mettre à jour skills-index.json avec le nouveau statut
→ Incrémenter la version si nécessaire (semver)
```

### Étape 3 — Composition de skills

```
→ Décomposer la tâche cible en sous-tâches atomiques
→ Assigner chaque sous-tâche à un skill existant
→ Ordonner les skills par dépendance (parent → enfant)
→ Valider que chaque skill de la chaîne est actif
```

### Étape 4 — Curriculum automatique

```
→ Définir les prérequis de chaque skill
→ Ordonner les skills par difficulté croissante
→ Générer un parcours d'apprentissage (curriculum)
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Promouvoir un skill sans preuve de vérification (RC=0, stdout brut, hash)
- ❌ Composer des skills sans vérifier leurs dépendances mutuelles
- ❌ Créer un skill en doublon sans vérifier skills-index.json
- ❌ Oublier l'incrément semver après raffinement

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : slm-fragmented-approach
- **Règle** : proof-recalculation
