---
name: agent-skills-addy-osmani
description: Encodage de workflows avec critères de sortie, garde-fous anti-rationalisation et exigences de vérification. Pattern inspiré de https://github.com/addyosmani/agent-skills
version: 1.0.0
intent_hash: 0xSKILL_AGENT_SKILLS_ADDY_OSMANI_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/addyosmani/agent-skills
source_url: https://github.com/addyosmani/agent-skills
path: agent-skills-addy-osmani
---

# Agent Skills (Addy Osmani) — Skill KiloCode

## Objectif

Encodage de workflows avec critères de sortie, garde-fous anti-rationalisation et exigences de vérification. Ce skill encapsule le pattern du repo externe `agent-skills` (Addy Osmani) adapté à ENV2, avec respect strict des règles de gouvernance et de preuve fraîche.

## Déclencheur

Ce skill s'active quand :
- Un workflow doit être encodé en skill avec critères de sortie explicites
- Des garde-fous anti-rationalisation doivent être appliqués à un skill
- Une exigence de vérification (preuve brute) doit être formalisée
- Un skill doit être audité pour détecter une rationalisation post-hoc

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `workflow` | string | ✅ | Workflow à encoder en skill |
| `exit_criteria` | array | ✅ | Critères de sortie (conditions pour considérer le skill comme terminé) |
| `guardrails` | array | ❌ | Garde-fous anti-rationalisation |
| `verification_required` | boolean | ❌ | Vérification obligatoire (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `encoded_skill` | string | Nom du skill encodé |
| `skill_path` | string | Chemin absolu vers le SKILL.md |
| `exit_criteria_spec` | array | Spécification des critères de sortie |
| `guardrail_spec` | array | Spécification des garde-fous appliqués |
| `verification_proof` | object | Preuve de vérification (hash, timestamp, code de retour) |
| `evidence_hash` | string | Hash SHA-256 du skill encodé |

## Protocole Obligatoire

### Étape 1 — Encodage du workflow

```
→ Lire le workflow à encoder
→ Décomposer en étapes atomiques (1 action = 1 outil)
→ Définir les critères de sortie pour chaque étape
→ Vérifier que chaque étape a une preuve brute correspondante
```

### Étape 2 — Application des garde-fous anti-rationalisation

```
→ Interdire la déclaration de succès sans preuve brute (stdout, hash SHA-256, timestamp UTC)
→ Interdire le paraphrasage de sortie (règle verbatim-fidelity)
→ Exiger la vérification sur le fichier réel (pas de copie ancienne)
→ Ajouter des garde-fous pour chaque critère de sortie
```

### Étape 3 — Génération du SKILL.md

```
→ Créer le répertoire du skill sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\
→ Écrire le SKILL.md avec frontmatter (name, description, version, intent_hash)
→ Définir les critères de sortie et les garde-fous dans le protocole
→ Lier les références ADR et règles applicables
```

### Étape 4 — Vérification et enregistrement

```
→ Exécuter le skill et capturer la preuve brute
→ Vérifier que tous les critères de sortie sont remplis
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Déclarer un skill terminé sans preuve brute (stdout, hash, timestamp)
- ❌ Paraphraser la sortie d'un skill au lieu de citer textuellement (règle verbatim-fidelity)
- ❌ Utiliser une preuve recopiée d'une exécution précédente (règle proof-recalculation)
- ❌ Oublier les garde-fous anti-rationalisation

## Référence ADR

- **ADR** : ADR-2026-11-16-001-ZERO-TRUST-EVIDENCE
- **IntentHash** : (lié au ADR de zéro confiance sur les preuves)
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : proof-recalculation
- **Règle** : verbatim-fidelity
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
