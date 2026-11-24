---
name: timerise-skills
description: Modèle de skills découpés (SKILL.md, references/, assets/, evals/) avec règles strictes et versions. Pattern inspiré de https://github.com/timerise-ai/skills
version: 1.0.0
intent_hash: 0xSKILL_TIMERISE_SKILLS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/timerise-ai/skills
source_url: https://github.com/timerise-ai/skills
path: timerise-skills
---

# Timerise Skills — Skill KiloCode

## Objectif

Modèle de skills découpés avec structure canonique (SKILL.md, references/, assets/, evals/), règles strictes et versioning. Ce skill encapsule le pattern du repo externe `skills` (Timerise) adapté à ENV2, avec respect des règles de gouvernance et de preuve fraîche.

## Déclencheur

Ce skill s'active quand :
- Un skill doit être créé selon une structure découpée et versionnée
- Des évaluations (evals/) doivent être associées à un skill pour validation
- Des assets doivent être liés à un skill
- Un skill doit être versionné avec règles strictes

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `skill_name` | string | ✅ | Nom du skill à créer |
| `version` | string | ✅ | Version semver (ex: 1.0.0) |
| `has_evals` | boolean | ❌ | Le skill a-t-il des évaluations (défaut: true) |
| `has_assets` | boolean | ❌ | Le skill a-t-il des assets (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `skill_structure` | object | Structure complète (SKILL.md, references/, assets/, evals/) |
| `skill_path` | string | Chemin absolu vers le répertoire du skill |
| `eval_results` | array | Résultats des évaluations (si has_evals = true) |
| `version_recorded` | string | Version enregistrée dans skills-index.json |
| `evidence_hash` | string | Hash SHA-256 de la structure complète |

## Protocole Obligatoire

### Étape 1 — Création de la structure découpée

```
→ Créer le répertoire sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/<skill_name>/
→ Créer le fichier SKILL.md avec frontmatter complet (name, description, version, intent_hash)
→ Créer le sous-répertoire references/ pour les références documentaires
→ Créer le sous-répertoire assets/ pour les assets associés
→ Créer le sous-répertoire evals/ pour les évaluations de validation
```

### Étape 2 — Rédaction du SKILL.md canonique

```
→ Définir l'objectif, le déclencheur, l'entrée, la sortie
→ Spécifier le protocole obligatoire étape par étape
→ Déclarer les anti-patterns bloquants
→ Lier les références ADR et règles applicables
```

### Étape 3 — Évaluations (evals/)

```
→ Créer des fichiers d'évaluation dans evals/ pour valider le skill
→ Chaque évaluation doit tester un critère de sortie spécifique
→ Exécuter les évaluations et capturer les preuves brutes (stdout, code de retour, hash)
→ Si une évaluation échoue → corriger le skill avant promotion
```

### Étape 4 — Versioning et enregistrement

```
→ Enregistrer la version semver dans skills-index.json
→ À chaque modification, incrémenter selon semver
→ Calculer le hash SHA-256 de la structure complète
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Créer un skill sans structure découpée (manque de SKILL.md, evals/, etc.)
- ❌ Ne pas exécuter les évaluations avant promotion du skill
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
