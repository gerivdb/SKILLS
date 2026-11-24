---
name: agent-skills-survey
description: Cartographie les approches d'acquisition, distillation, composition et raffinement de skills (ex. Voyager, SkillWeaver, ASI, CASCADE, ReMe, LEGOMem). Pattern inspiré de https://github.com/yashonwu/agent-skills-survey
version: 1.0.0
intent_hash: 0xSKILL_AGENT_SKILLS_SURVEY_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/yashonwu/agent-skills-survey
source_url: https://github.com/yashonwu/agent-skills-survey
path: agent-skills-survey
---

# Agent Skills Survey — Skill KiloCode

## Objectif

Fournir une cartographie de référence des approches d'acquisition, distillation, composition et raffinement de skills d'agents. Ce skill sert de référence théorique avant de créer ou modifier un skill canonique dans l'écosystème ENV2.

## Déclencheur

Ce skill s'active quand :
- Il faut choisir une approche de création de skill (acquisition, distillation, composition, raffinement)
- Un skill doit être comparé à un pattern de référence externe
- Une architecture de mémoire procédurale doit être conçue
- Il faut valider qu'un nouveau skill ne duplique pas un pattern existant

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `approach_type` | enum | ✅ | acquisition / distillation / composition / refinement |
| `target_domain` | string | ✅ | Domaine cible du skill (ex: CDP, git, memory, mcp) |
| `existing_skills` | array | ❌ | Liste des skills déjà indexés dans skills-index.json |
| `intent_hash` | string | ❌ | IntentHash du besoin à couvrir |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `recommended_approach` | string | Approche recommandée pour le skill |
| `reference_patterns` | array | Patterns de référence (Voyager, SkillWeaver, etc.) |
| `duplicate_check` | bool | True si un skill similaire existe déjà |
| `skill_template` | string | Template SKILL.md adapté à l'approche choisie |
| `evidence_hash` | string | Hash SHA-256 de l'analyse |

## Protocole Obligatoire

### Étape 1 — Vérification des doublons

```
→ Consulter skills-index.json pour chercher un skill avec le même intent_hash
→ Consulter skills-index.json pour chercher un skill avec le même name
→ Si doublon trouvé → signaler et stopper (règle anti-doublon)
```

### Étape 2 — Sélection de l'approche

```
→ acquisition : extraire un skill depuis un repo externe (nécessite HITL clone gate)
→ distillation : extraire un skill depuis une trace d'exécution existante
→ composition : assembler plusieurs skills existants en un nouveau
→ refinement : améliorer un skill existant (incrément semver)
```

### Étape 3 — Génération du template

```
→ Créer le SKILL.md avec frontmatter (name, description, version, intent_hash)
→ Définir les triggers et anti_triggers
→ Spécifier l'entrée, la sortie et le protocole obligatoire
→ Lier les références ADR et règles applicables
```

### Étape 4 — Enregistrement

```
→ Ajouter l'entrée dans skills-index.json
→ Créer le répertoire du skill sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\
→ Valider le frontmatter avec frontmatter-guardian
```

## Anti-patterns

- ❌ Créer un skill sans vérifier l'absence de doublon (même name ou même intent_hash)
- ❌ Utiliser une approche d'acquisition (clone externe) sans passer par hitl-clone-gate
- ❌ Oublier les anti_triggers dans le SKILL.md
- ❌ Ne pas lier les règles et ADR applicables

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : hitl-clone-gate
- **Règle** : zero-manual-proper-name
