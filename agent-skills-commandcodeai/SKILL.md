---
name: agent-skills-commandcodeai
description: Organisation de skills combinant instructions (SKILL.md), scripts exécutables, templates et ressources. Pattern inspiré de https://github.com/commandcodeai/agent-skills
version: 1.0.0
intent_hash: 0xSKILL_AGENT_SKILLS_COMMANDCODEAI_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/commandcodeai/agent-skills
source_url: https://github.com/commandcodeai/agent-skills
path: agent-skills-commandcodeai
---

# Agent Skills (CommandCodeAI) — Skill KiloCode

## Objectif

Organiser les skills en combinant instructions (SKILL.md), scripts exécutables, templates et ressources. Ce skill encapsule le pattern du repo externe `agent-skills` (CommandCodeAI) adapté à ENV2, avec respect des règles de chemins explicites et de preuve fraîche.

## Déclencheur

Ce skill s'active quand :
- Un skill doit être organisé selon une structure modulaire (SKILL.md + scripts + templates + ressources)
- Des templates d'exécution doivent être créés pour un skill
- Des ressources de référence doivent être associées à un skill
- La structure d'un skill doit être auditée pour conformité

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `skill_name` | string | ✅ | Nom du skill à organiser |
| `instructions` | string | ✅ | Contenu du SKILL.md (instructions) |
| `scripts` | array | ❌ | Scripts exécutables associés |
| `templates` | array | ❌ | Templates d'exécution |
| `resources` | array | ❌ | Ressources de référence |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `skill_structure` | object | Structure du skill (SKILL.md, scripts/, templates/, resources/) |
| `skill_path` | string | Chemin absolu vers le répertoire du skill |
| `script_inventory` | array | Inventaire des scripts avec leurs hash SHA-256 |
| `template_inventory` | array | Inventaire des templates avec leurs hash SHA-256 |
| `evidence_hash` | string | Hash SHA-256 de la structure complète |

## Protocole Obligatoire

### Étape 1 — Création de la structure modulaire

```
→ Créer le répertoire du skill sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/<skill_name>/
→ Créer le fichier SKILL.md avec frontmatter complet
→ Créer le sous-répertoire scripts/ pour les scripts exécutables
→ Créer le sous-répertoire templates/ pour les templates d'exécution
→ Créer le sous-répertoire resources/ pour les ressources de référence
```

### Étape 2 — Rédaction des instructions (SKILL.md)

```
→ Définir l'objectif du skill
→ Déclarer les déclencheurs (triggers) et anti-déclencheurs (anti_triggers)
→ Spécifier l'entrée, la sortie et le protocole obligatoire
→ Lier les références ADR et règles applicables
```

### Étape 3 — Organisation des scripts et templates

```
→ Placer chaque script exécutable dans scripts/ avec un chemin absolu explicite
→ Placer chaque template dans templates/ avec un hash SHA-256
→ Documenter chaque ressource dans resources/ avec sa source
→ Vérifier que tous les chemins sont absolus et explicites (règle explicit-path-compliance)
```

### Étape 4 — Inventaire et preuve

```
→ Générer l'inventaire des scripts avec leurs hash SHA-256
→ Générer l'inventaire des templates avec leurs hash SHA-256
→ Calculer le hash SHA-256 de la structure complète du skill
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Créer un skill sans structure modulaire (SKILL.md + scripts + templates + ressources)
- ❌ Utiliser des chemins relatifs dans les scripts ou templates (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 pour chaque script et template
- ❌ Ne pas mettre à jour skills-index.json après organisation

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : skill-citizen-prealable
